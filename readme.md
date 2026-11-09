# Workflow Version Manager

One file, zero dependencies, any Git repository. `version_manager.py` bumps the
semantic version, writes a changelog entry, commits, tags and pushes — in one
step — so every repo shares the same **vm-commit** workflow.

- Python 3.8+ and Git on `PATH`. Standard library only (no `colorama`).
- Works from any directory inside the repo; the Git root is discovered.
- Never rewrites README/docs implicitly — historical notes stay intact.
  Extra version strings are synchronised only for files you opt into.

## Install into a repository

```powershell
python C:\Users\TEMP.MARIZ\Desktop\GH\workflow_version_manager\repo_bootstrap.py <repo>            # first time
python C:\Users\TEMP.MARIZ\Desktop\GH\workflow_version_manager\repo_bootstrap.py <repo> --update   # refresh tools
```

This copies `version_manager.py` and `auto_merge.py` into `<repo>/tools/` and
creates `VERSION` / `CHANGELOG.md` when missing (`tools/version_manager.py init`).
Set `DEV_TOOLS_DIR` to use a template stored elsewhere.

## The vm-commit workflow

```powershell
git add <the files that belong to this change>
python tools/version_manager.py "Add CSV export" minor -c feature
```

One commit is created containing **your staged changes + VERSION + CHANGELOG**,
titled `Release v1.4.0: Add CSV export`, tagged `v1.4.0` (annotated) and pushed
(`git push -u origin <branch>` plus the single tag).

| Situation | Behaviour |
|---|---|
| Unstaged / untracked files | Reported and left out of the commit |
| `--all` / `-a` | Stage everything (incl. untracked) first |
| `--no-push` | Commit and tag locally only |
| `--require-clean` | Refuse if anything is uncommitted |
| No `origin` remote | Push skipped with a warning |
| Push fails | Commit + tag kept locally; retry command printed |
| Commit fails (e.g. hook) | VERSION/CHANGELOG restored, nothing committed |
| Tag already exists, detached HEAD, merge in progress, bad VERSION | Refused before any change |

## Commands

```text
version_manager.py "message" [BUMP] [options]        shorthand for `commit`
version_manager.py commit  "message" [BUMP] [options]
version_manager.py preview BUMP "summary" [options]   show the full plan, change nothing
version_manager.py release BUMP "summary" --yes       same as commit, bump first, needs confirmation
version_manager.py inspect [--json]                   branch, version source, tags, staged/unstaged files
version_manager.py init [--initial-version 0.1.0]     create VERSION / CHANGELOG.md if missing
```

- `BUMP`: `patch` (default), `minor`, `major`, or an explicit `X.Y.Z` (must be greater).
- `-c/--category`: `feature` (default), `fix`, `refactor`, `perf`, `security`, `chore`, `docs`, plus any configured.
- `-d/--dry-run`: same as `preview`. `-C/--repo PATH`: operate on another repository.
- Multi-line messages are written to the changelog verbatim; single lines become a bullet.
- `--version` prints the tool version (compare copies across repos with `inspect`).

## Version source

`VERSION` is canonical. If it is missing, the current version is taken from
`pyproject.toml`, `package.json`, or the newest `v*` tag (else `0.0.0`), and
`VERSION` is created on the first release. An invalid `VERSION` is an error —
it is never silently reset.

## Changelog format

New entries are inserted newest-first, below the `# ` title and below any
`## [Unreleased]` section. Line endings and BOMs are preserved.

```markdown
## [1.4.0] - 2026-11-09
### Added
- Add CSV export
```

## Optional configuration

Add `.versionmanager.json` (or `version_manager.json`, or
`[tool.version-manager]` in `pyproject.toml` on Python 3.11+). Every key is
optional; see [versionmanager.example.json](versionmanager.example.json).

| Key | Default | Purpose |
|---|---|---|
| `version_file` | `VERSION` | Canonical version file |
| `changelog_file` | `CHANGELOG.md` | Changelog to prepend |
| `version_files` | `[]` | Extra files to sync: path, or `{"path", "pattern"}` with a `{version}` placeholder |
| `tag_prefix` | `v` | Tag naming |
| `commit_template` | `Release {tag}: {message}` | Placeholders: `tag version previous message category` |
| `push` | `true` | Default push behaviour |
| `remote` | `origin` | Push target |
| `require_clean` | `false` | Make `--require-clean` the default |
| `categories` | see above | Merged with the built-in categories |

The default `version_files` pattern matches `version = "X"`, `__version__ = "X"`,
`"version": "X"`, `APP_VERSION = "X"` and similar assignments only, so pinned
dependencies such as `pkg==1.2.3` are untouched.

## Auto merge

`tools/auto_merge.py` resolves conflicts only in safe files (`VERSION`,
`CHANGELOG.md` by default; configurable via `.auto_merge.json`):

```powershell
python tools/auto_merge.py --strategy theirs
```

## Development

```powershell
python -m unittest discover -s tests -v
```

End-to-end tests create disposable repositories with a local bare remote and
run from inside them; they never touch a real project.
