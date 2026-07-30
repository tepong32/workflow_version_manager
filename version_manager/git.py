"""Small, testable wrapper around Git commands."""

from __future__ import annotations

import subprocess
from pathlib import Path


class GitError(RuntimeError):
    """Raised when a required Git operation cannot be completed."""


class GitService:
    """Run Git commands scoped to one repository root."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def run(self, *args: str, check: bool = True) -> str:
        try:
            result = subprocess.run(["git", *args], cwd=self.root, text=True,
                                    capture_output=True, check=check)
        except FileNotFoundError as error:
            raise GitError("Git is not installed or is not on PATH.") from error
        except subprocess.CalledProcessError as error:
            detail = error.stderr.strip() or error.stdout.strip()
            raise GitError(f"git {' '.join(args)} failed: {detail}") from error
        return result.stdout.strip()

    def root_path(self) -> Path:
        return Path(self.run("rev-parse", "--show-toplevel"))

    def branch(self) -> str:
        return self.run("branch", "--show-current") or "(detached HEAD)"

    def default_branch(self) -> str | None:
        reference = self.run("symbolic-ref", "refs/remotes/origin/HEAD", check=False)
        return reference.rsplit("/", 1)[-1] if reference else None

    def tags(self) -> list[str]:
        return self.run("tag", "--list", "--sort=-version:refname").splitlines()

    def is_clean(self) -> bool:
        return not self.run("status", "--porcelain")

    def remote_exists(self) -> bool:
        return bool(self.run("remote", check=False))

    def commit(self, files: list[str], message: str) -> None:
        self.run("add", "--", *files)
        self.run("commit", "-m", message)

    def tag(self, tag: str) -> None:
        if tag in self.tags():
            raise GitError(f"Tag already exists: {tag}")
        self.run("tag", tag)

    def push(self, tag: str, branch: str) -> None:
        self.run("push", "origin", branch)
        self.run("push", "origin", tag)
