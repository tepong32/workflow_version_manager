"""Regression tests for the single-file Version Manager.

Git-mutating tests run only inside disposable temporary repositories with a
local bare remote, never against a real project.
"""

import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import version_manager as vm  # noqa: E402


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, check=True, text=True,
                          capture_output=True).stdout.strip()


def run_vm(*argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = vm.main(list(argv))
    return code, out.getvalue(), err.getvalue()


class VersioningTests(unittest.TestCase):
    def test_bumps(self):
        self.assertEqual(vm.next_version("1.2.3", "patch"), "1.2.4")
        self.assertEqual(vm.next_version("1.2.3", "minor"), "1.3.0")
        self.assertEqual(vm.next_version("1.2.3", "major"), "2.0.0")

    def test_explicit_version_must_increase(self):
        self.assertEqual(vm.next_version("1.2.3", "v1.10.0"), "1.10.0")
        with self.assertRaises(vm.VMError):
            vm.next_version("1.2.3", "1.2.3")
        with self.assertRaises(vm.VMError):
            vm.next_version("1.2.3", "banana")

    def test_parse_version(self):
        self.assertEqual(vm.parse_version("v3.4.5"), "3.4.5")
        self.assertEqual(vm.parse_version("rel-3.4.5", "rel-"), "3.4.5")
        self.assertIsNone(vm.parse_version("1.2"))


class ChangelogTests(unittest.TestCase):
    def test_inserts_below_h1_newest_first(self):
        old = "# Changelog\n\n## [1.0.0] - 2020-01-01\n### Added\n- first\n"
        new = vm.insert_changelog_entry(old, "1.1.0", "second", "Added")
        self.assertLess(new.index("[1.1.0]"), new.index("[1.0.0]"))
        self.assertTrue(new.startswith("# Changelog\n\n## [1.1.0]"))
        self.assertIn("- second\n\n## [1.0.0]", new)

    def test_keeps_unreleased_section_on_top(self):
        old = "# Changelog\n\n## [Unreleased]\n- wip\n\n## [1.0.0] - 2020-01-01\n- first\n"
        new = vm.insert_changelog_entry(old, "1.1.0", "second", "Added")
        self.assertLess(new.index("[Unreleased]"), new.index("[1.1.0]"))
        self.assertLess(new.index("[1.1.0]"), new.index("[1.0.0]"))

    def test_preserves_crlf_and_handles_empty_or_headless(self):
        crlf = vm.insert_changelog_entry("# Changelog\r\n\r\n## [1.0.0]\r\n- a\r\n", "1.0.1", "b", "Fixed")
        self.assertNotIn("\n", crlf.replace("\r\n", ""))
        self.assertTrue(vm.insert_changelog_entry("", "0.1.0", "x", "Added").startswith("# Changelog\n\n## [0.1.0]"))
        self.assertTrue(vm.insert_changelog_entry("legacy notes\n", "0.1.0", "x", "Added").startswith("# Changelog"))

    def test_multiline_message_kept_verbatim(self):
        entry = vm.build_entry("1.0.0", "Summary\n\n- detail", "Added")
        self.assertIn("Summary\n\n- detail", entry)


class RepoTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name)
        self.remote = base / "remote.git"
        self.repo = base / "work"
        git(base, "init", "-q", "--bare", str(self.remote))
        git(base, "init", "-q", "-b", "main", str(self.repo))
        for key, value in (("user.name", "Test"), ("user.email", "t@example.com"), ("commit.gpgsign", "false")):
            git(self.repo, "config", key, value)
        git(self.repo, "remote", "add", "origin", str(self.remote))
        (self.repo / "VERSION").write_text("1.0.0\n", encoding="utf-8")
        (self.repo / "CHANGELOG.md").write_text("# Changelog\n\n## [1.0.0] - 2020-01-01\n- init\n", encoding="utf-8")
        (self.repo / "README.md").write_text("Historic note: shipped 1.0.0\n", encoding="utf-8")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "init")
        git(self.repo, "push", "-q", "-u", "origin", "main")
        # Safety net: run from inside the disposable repo so no code path can
        # ever fall back to the real working directory.
        self._cwd = os.getcwd()
        os.chdir(self.repo)

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def committed_files(self):
        return git(self.repo, "show", "--name-only", "--format=", "HEAD").splitlines()


class EndToEndTests(RepoTestCase):
    def test_shorthand_commit_includes_staged_excludes_unstaged_and_pushes(self):
        (self.repo / "feature.py").write_text("x = 1\n", encoding="utf-8")
        (self.repo / "scratch.txt").write_text("not mine\n", encoding="utf-8")
        git(self.repo, "add", "feature.py")
        sub = self.repo / "pkg" / "deep"
        sub.mkdir(parents=True)
        code, out, err = run_vm("-C", str(sub), "Add feature", "minor")  # root found from a subdirectory
        self.assertEqual(code, 0, err)
        self.assertEqual((self.repo / "VERSION").read_text(encoding="utf-8"), "1.1.0\n")
        self.assertEqual(sorted(self.committed_files()), ["CHANGELOG.md", "VERSION", "feature.py"])
        self.assertIn("?? scratch.txt", git(self.repo, "status", "--porcelain"))
        self.assertEqual(git(self.repo, "log", "-1", "--format=%s"), "Release v1.1.0: Add feature")
        self.assertIn("v1.1.0", git(self.remote, "tag"))
        self.assertEqual(git(self.remote, "rev-parse", "main"), git(self.repo, "rev-parse", "HEAD"))
        # Docs are never rewritten implicitly.
        self.assertEqual((self.repo / "README.md").read_text(encoding="utf-8"), "Historic note: shipped 1.0.0\n")

    def test_all_flag_and_no_push(self):
        (self.repo / "new.txt").write_text("hi\n", encoding="utf-8")
        code, _, err = run_vm("--repo", str(self.repo), "commit", "Everything", "--all", "--no-push", "-c", "fix")
        self.assertEqual(code, 0, err)
        self.assertIn("new.txt", self.committed_files())
        self.assertNotIn("v1.0.1", git(self.remote, "tag"))
        self.assertIn("### Fixed", (self.repo / "CHANGELOG.md").read_text(encoding="utf-8"))

    def test_preview_and_dry_run_change_nothing(self):
        head = git(self.repo, "rev-parse", "HEAD")
        for argv in (("preview", "major", "Big"), ("commit", "Big", "major", "-d")):
            code, out, err = run_vm("-C", str(self.repo), *argv)
            self.assertEqual(code, 0, err)
            self.assertIn("2.0.0", out)
        self.assertEqual(git(self.repo, "rev-parse", "HEAD"), head)
        self.assertEqual((self.repo / "VERSION").read_text(encoding="utf-8"), "1.0.0\n")

    def test_release_requires_yes_when_not_interactive(self):
        code, _, err = run_vm("-C", str(self.repo), "release", "patch", "Ship")
        self.assertEqual(code, 1)
        self.assertIn("--yes", err)
        code, _, err = run_vm("-C", str(self.repo), "release", "patch", "Ship", "it", "--yes", "--allow-dirty")
        self.assertEqual(code, 0, err)
        self.assertEqual(git(self.repo, "log", "-1", "--format=%s"), "Release v1.0.1: Ship it")

    def test_existing_tag_and_invalid_version_are_refused(self):
        git(self.repo, "tag", "v1.0.1")
        code, _, err = run_vm("-C", str(self.repo), "Patch", "--no-push")
        self.assertEqual(code, 1)
        self.assertIn("already exists", err)
        (self.repo / "VERSION").write_text("one\n", encoding="utf-8")
        code, _, err = run_vm("-C", str(self.repo), "Patch", "--no-push")
        self.assertEqual(code, 1)
        self.assertIn("MAJOR.MINOR.PATCH", err)

    def test_require_clean(self):
        (self.repo / "README.md").write_text("unstaged edit\n", encoding="utf-8")
        code, out, err = run_vm("-C", str(self.repo), "inspect", "--json")
        self.assertEqual(code, 0, err)
        facts = json.loads(out)
        self.assertEqual(facts["staged"], [])
        self.assertEqual(facts["unstaged"], ["README.md"])
        code, _, err = run_vm("-C", str(self.repo), "Patch", "--require-clean")
        self.assertEqual(code, 1)
        self.assertIn("require_clean", err)

    def test_failed_commit_restores_files(self):
        hook = self.repo / ".git" / "hooks" / "pre-commit"
        hook.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
        hook.chmod(0o755)
        code, _, err = run_vm("-C", str(self.repo), "Patch", "--no-push")
        self.assertEqual(code, 1)
        self.assertIn("restored", err)
        self.assertEqual((self.repo / "VERSION").read_text(encoding="utf-8"), "1.0.0\n")
        self.assertEqual(git(self.repo, "status", "--porcelain"), "")

    def test_config_version_files_and_template(self):
        (self.repo / "pyproject.toml").write_text('[project]\nversion = "1.0.0"\ndeps = ["x==1.0.0"]\n', encoding="utf-8")
        (self.repo / ".versionmanager.json").write_text(json.dumps({
            "version_files": ["pyproject.toml"], "commit_template": "chore(release): {tag} - {message}",
            "tag_prefix": "rel-", "push": False}), encoding="utf-8")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "cfg")
        code, _, err = run_vm("-C", str(self.repo), "Cfg release")
        self.assertEqual(code, 0, err)
        pyproject = (self.repo / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('version = "1.0.1"', pyproject)
        self.assertIn('"x==1.0.0"', pyproject)  # unrelated pins untouched
        self.assertIn("rel-1.0.1", git(self.repo, "tag"))
        self.assertEqual(git(self.repo, "log", "-1", "--format=%s"), "chore(release): rel-1.0.1 - Cfg release")
        self.assertNotIn("rel-1.0.1", git(self.remote, "tag"))

    def test_repo_option_honoured_before_and_after_command(self):
        elsewhere = Path(self._tmp.name)  # not a Git repository
        os.chdir(elsewhere)
        for argv in (("-C", str(self.repo), "inspect", "--json"), ("inspect", "--json", "-C", str(self.repo))):
            code, out, err = run_vm(*argv)
            self.assertEqual(code, 0, err)
            self.assertEqual(Path(json.loads(out)["root"]).resolve(), self.repo.resolve())
        code, _, err = run_vm("inspect")
        self.assertEqual(code, 1)
        self.assertIn("Not inside a Git repository", err)

    def test_inspect_json_and_init(self):
        (self.repo / "VERSION").unlink()
        git(self.repo, "tag", "v1.4.0")
        code, out, err = run_vm("-C", str(self.repo), "inspect", "--json")
        self.assertEqual(code, 0, err)
        facts = json.loads(out)
        self.assertEqual(facts["version"], "1.4.0")
        self.assertEqual(facts["tool_version"], vm.TOOL_VERSION)
        code, out, err = run_vm("-C", str(self.repo), "init")
        self.assertEqual(code, 0, err)
        self.assertEqual((self.repo / "VERSION").read_text(encoding="utf-8"), "1.4.0\n")

    def test_lowercase_changelog_and_app_metadata_discovery(self):
        (self.repo / "VERSION").unlink()
        git(self.repo, "mv", "CHANGELOG.md", "changelog.md")
        (self.repo / "app_metadata.py").write_text('APP_VERSION = "2.3.0"\n', encoding="utf-8")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "lowercase cl + metadata")
        code, out, err = run_vm("-C", str(self.repo), "inspect", "--json")
        self.assertEqual(code, 0, err)
        facts = json.loads(out)
        self.assertEqual(facts["version"], "2.3.0")
        self.assertEqual(facts["version_source"], "app_metadata.py")
        self.assertEqual(facts["changelog"], "changelog.md")
        code, _, err = run_vm("-C", str(self.repo), "Case preserved release", "--no-push")
        self.assertEqual(code, 0, err)
        self.assertEqual(sorted(self.committed_files()), ["VERSION", "changelog.md"])


if __name__ == "__main__":
    unittest.main()
