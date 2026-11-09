# Workflow Version Manager - continuation

Baseline: 2026-11-09 on feature/universal-single-file-vm (v2.0.0).

## Resume

Read [AGENTS.md](AGENTS.md), inspect current branch/status and recent history, then follow its documentation map.

Read README.md and tests/test_version_manager.py before changing release behavior. Validate in a disposable repository (the test suite's pattern) before any real release.

## State and boundaries

v2.0.0 replaced the `version_manager/` package (which `repo_bootstrap.py` never copied, leaving bootstrapped repos with a broken entry point, and which auto-rewrote docs) with a single stdlib-only file. Repo-specific wrappers in Peryanomy (`tools/release_vm.py`) and teppy-verse (`tools/vm_release.py`) existed only to suppress doc rewriting and were removed during the rollout. `repo_bootstrap.py --update` refreshes tools in existing repos.

## Validation and next handoff

PASS: `python -m unittest discover -s tests` (17 tests: versioning, changelog insertion, staged-only commit, --all, --no-push, preview/dry-run, --yes gating, tag/VERSION refusal, require-clean, hook-failure restoration, config/version_files/template, inspect/init, -C placement).

Next: none required. Future changes must keep the tool single-file and be rolled out with `repo_bootstrap.py <repo> --update`.
