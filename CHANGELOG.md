# Changelog

## [2.0.0] - 2026-11-09
### Refactored
Universal single-file Version Manager

- Merge the local CLI fixes and the GitHub package overhaul into ONE stdlib-only file (Python 3.8+, no colorama)
- vm-commit: staged changes + VERSION + CHANGELOG in one commit, annotated tag, push by default (--no-push to opt out)
- Auto-detect Git root (-C/--repo), explicit X.Y.Z bumps, inspect --json, init, preview/dry-run
- Never rewrite docs implicitly; opt-in version_files with safe patterns (replaces per-repo wrappers)
- Safety: refuse on existing tag/detached HEAD/merge/invalid VERSION; restore files if the commit fails
- repo_bootstrap.py: --update to refresh tools, creates VERSION/CHANGELOG via init, template dir defaults to its own folder
- Remove version_manager/ package (never copied by bootstrap) and v2_include_push.py; end-to-end test suite

## [1.3.0] - 2026-04-21
### ✨ Added
Introduce portable dev toolset with repo bootstrap system

- add repo_bootstrap.py for one-command project initialization
- standardize tools/ folder structure across repositories
- enable automatic setup of AGENTS.md with default AI rules
- integrate auto_merge.py as safe conflict resolution utility
- establish reusable dev-tools template approach for multi-repo workflows
- prepare foundation for scalable AI-assisted development tooling

## [1.2.0] - 2025-10-30
### 🔨 Refactor
- testing v2

## [1.1.0] - 2025-10-30
### 🚀 Added
- released v2 for auto-push inclusion and working directory checker

## [1.0.0] - 2025-10-21
### 🚀 Added
- Initial commit --- stand-alone release.
