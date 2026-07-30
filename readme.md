# Version Manager

Version Manager is a portable Git release automation toolkit. Copy
`version_manager.py` and the `version_manager/` directory into any repository,
or package it later as a Python command. It discovers repository metadata,
updates release documentation when present, creates a release commit and tag,
and can push both to a remote. It contains no project, milestone, folder, or
release-style assumptions.

## Features

- Inspects the Git root, repository name, current/default branch, tags, and
  documentation before acting.
- Calculates semantic-version patch, minor, and major releases.
- Discovers `README.md`, `CHANGELOG.md`, `ROADMAP.md`, `RELEASE_NOTES.md`,
  `VERSION.md`, and Markdown files under `docs/` or `documentation/`.
- Updates an existing `VERSION` file and changelog; a minimal repository gets
  new `VERSION` and `CHANGELOG.md` files so release notes remain durable.
- Replaces exact existing version references in discovered release-facing docs
  and configured version files, without assuming a project layout.
- Creates a release commit and lightweight tag; optionally pushes branch and
  tag. Preview, dry-run, confirmation, and clean-working-tree protection are
  built in.
- Reads optional JSON or `pyproject.toml` configuration; it works without one.

## Requirements and installation

Python 3.11+ and Git must be available on `PATH`. No third-party Python
packages are required.

Copy these items into the target repository (keeping the package directory
beside the script):

```text
version_manager.py
version_manager/
```

Run from the repository root, or pass `--repo PATH` before the command:

```bash
python version_manager.py inspect
```

## Quick start and typical release workflow

Inspect first, preview a release, then confirm a real release:

```bash
python version_manager.py inspect
python version_manager.py preview patch "Correct login timeout"
python version_manager.py release patch "Correct login timeout"
```

The final command displays the version, commit message, files to update, and
tag, then asks for confirmation. On acceptance it updates the discovered
release files, creates one commit and one tag locally. Add `--push` to publish
the current branch and tag to `origin`.

Example result:

```text
Version: v1.4.3
Commit: Release v1.4.3: Correct login timeout
Files to update:
  - .../VERSION
  - .../CHANGELOG.md
Tag: v1.4.3
Released v1.4.3. Commit: Release v1.4.3: Correct login timeout
```

## Commands

### `inspect`

Purpose: report the Git root, repository identity, branch, default branch,
current version, latest tag, version source, changelog, and discovered docs.

Syntax: `python version_manager.py [--repo PATH] inspect [--json]`

`--json` makes the expected output machine-readable. Example:

```bash
python version_manager.py inspect --json
```

Expected output includes fields such as `version: 1.4.2`, `latest_tag: v1.4.2`,
and the discovered documentation paths.

### `preview`

Purpose: calculate and print a release plan without modifying files or Git.

Syntax: `python version_manager.py [--repo PATH] preview {patch|minor|major} "message" [options]`

Options: `-c, --category NAME` chooses a release-note heading; `-d, --dry-run`
is accepted for compatibility (preview is already dry); `--push`, `--yes`, and
`--allow-dirty` are accepted but do not cause changes in preview.

```bash
python version_manager.py preview minor "Add CSV export" -c feature
```

Expected output: the proposed version/tag, commit message, and every file that
would change, followed by `Preview only: no files or Git state changed.`

### `release`

Purpose: make a version bump, generate release notes, update documentation,
commit, and create a tag.

Syntax: `python version_manager.py [--repo PATH] release {patch|minor|major} "message" [options]`

Options:

- `-c, --category NAME` — release-note category, default `feature`.
- `-d, --dry-run` — show the same plan without changes.
- `--yes` — skip the confirmation prompt, useful for controlled automation.
- `--push` — push the active branch and new tag to `origin` after local success.
- `--allow-dirty` — bypass the normal clean-tree check. Use only when the
  uncommitted changes are intentional and outside the release files.

```bash
python version_manager.py release patch "Correct login timeout" -c fix --yes
python version_manager.py release major "Redesigned API" --push
```

Expected local result: `VERSION` is bumped, `CHANGELOG.md` gains a dated entry,
other eligible docs with the old exact version are updated, then Git receives a
`Release vX.Y.Z: message` commit and a `vX.Y.Z` tag. With `--push`, both are
pushed. A repository without a remote still supports local/offline releases;
simply omit `--push`.

### Legacy invocation

Purpose: preserve the original command-line contract.

Syntax: `python version_manager.py "message" [patch|minor|major] [-c category] [-d]`

```bash
python version_manager.py "Update dependencies" patch -c chore -d
```

It behaves like `release`, with patch as the default bump. `-d` performs a
dry run. The newer explicit commands are recommended for scripts.

## Automatic documentation discovery

Version Manager never requires a documentation layout. It finds root-level
common release documents and recursively scans Markdown files under `docs/`
and `documentation/`. If `CHANGELOG.md` exists, the new dated entry is inserted
after its first top-level heading. If no changelog exists, a standard one is
created on release. Other discovered docs are changed only when they already
contain the old version as an exact version token. Nothing assumes a roadmap,
milestone, or product name.

## Configuration

Configuration is optional. Place `.versionmanager.json` or
`version_manager.json` at the Git root, or add `[tool.version-manager]` to
`pyproject.toml`. Start with [version_manager.example.json](version_manager.example.json).

```toml
[tool.version-manager]
version_file = "metadata/release-version.txt"
changelog_file = "docs/history.md"
version_files = ["pyproject.toml", "package.json"]
documentation_files = ["README.md", "docs/release-process.md"]
tag_prefix = "release-"
commit_template = "Publish {tag}: {message}"

[tool.version-manager.categories]
feature = "New"
fix = "Corrections"
```

Available template variables are `{version}`, `{tag}`, and `{message}`.
`version_files` are explicit project integration points; they are deliberately
outside the core’s assumptions.

## Git, hosting, and offline examples

For a GitHub repository with an `origin` remote:

```bash
python version_manager.py release minor "Add audit log" --push --yes
```

For a private repository, the same command works using your existing Git
credentials; Version Manager does not contact hosting APIs or require GitHub.
For a private/offline repository without a remote:

```bash
python version_manager.py release patch "Internal maintenance" --yes
```

This creates the commit/tag locally. Push later with normal Git, or rerun a
new release with `--push` after adding an `origin` remote.

## Troubleshooting and FAQ

**“Working directory is not clean.”** Commit or stash unrelated work, use
`preview`, or intentionally use `--allow-dirty`.

**“No Git remote is configured.”** The local release completed. Omit `--push`
for offline use, or add/configure `origin` before publishing.

**Which version wins?** An explicit/conventional version file is used first,
then `pyproject.toml`, `package.json`, the newest semantic Git tag, and finally
`0.0.0`.

**Can I use a non-`v` tag style?** Yes: configure `tag_prefix`, for example
`release-` or an empty string.

**Does it update every document?** No. It discovers release-facing docs but
only replaces exact existing version values. Add files under `version_files`
when an integration needs an explicit guarantee.
