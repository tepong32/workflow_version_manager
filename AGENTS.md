# Workflow Version Manager - repository guide

## Project context and documentation map

Portable Python 3.8+ and Git release automation toolkit. version_manager.py is a single self-contained, standard-library-only file (copied verbatim into each repo's tools/ by repo_bootstrap.py); do not split it into a package. auto_merge.py is the companion conflict helper.

### Durable boundaries

Remain repository-neutral: no hard-coded project identity, branch or milestone assumptions. Never rewrite docs implicitly (only opt-in version_files). Preserve preview/dry-run, staged-only commits, release confirmation, failed-commit restoration and push/--no-push behavior. Test release mutations only in disposable temporary repositories.

### Development state

v2.0.0 (2026-11-09) replaced the multi-file package with the universal single-file tool and rolled it out to all GH repos. README.md documents current commands.

### Read next

- [README.md](README.md)
- [CHANGELOG.md](CHANGELOG.md)
- [versionmanager.example.json](versionmanager.example.json)
- [tests/test_version_manager.py](tests/test_version_manager.py)
- [Continuation entry point](CONTINUE.md)

### Project validation

Use `python -m unittest discover -s tests` for the compact release-tool suite; individual test methods can isolate a narrow change. Git mutation tests must use disposable repositories. Expand for discovery, branch/tag handling or version/document replacement compatibility.

## Repository continuity and proportional testing

- Maintain this root AGENTS.md in version control as portable operational context. Preserve applicable nested instructions. Update it in the same phase as durable architecture, security, integration, major completion/deferral or testing-policy changes.
- Keep this file concise: identity, boundaries, decisions and a documentation map. Replace stale summaries; never append transcripts, line-by-line diaries or duplicate full specifications.
- Before substantial work read AGENTS.md, CONTINUE.md (and its canonical handoff target), the relevant roadmap/architecture/feature documents, recent Git history/status and affected tests. Reconcile stale snapshots against source; do not ask the user to repeat documented context.
- At task completion update the canonical handoff for immediate state, actual validation, blockers and next steps; update the roadmap for agreed direction changes and specialized architecture/feature/audit/testing documents where applicable. Cross-link instead of duplicating them. Do not invent completed phases or new priorities.
- Test the changed area first: direct unit/feature tests, related integration tests and dependent regressions. Expand for shared models/services/utilities, auth/permissions, middleware, schema/migrations, settings/environments, shared UI, cross-app APIs, reporting, jobs or build/deployment changes. Uncertain impact requires broader validation.
- Full suites are appropriate for broad refactors, cross-module/security/infrastructure changes, major milestones and release/production gates, not automatically every isolated edit. Preserve stricter project-specific safety, reachability, hardware and release checks.
- Record relevant commands, scope rationale and outcomes in the handoff or appropriate validation report: PASS; FAIL - CAUSED BY CURRENT WORK; FAIL - PRE-EXISTING (with evidence); NOT RUN - OUT OF SCOPE (with rationale); NOT RUN - ENVIRONMENTAL (with limitation).
- Investigate failures before calling them unrelated. Fix regressions caused by the change and document evidence for pre-existing failures. A skipped test or unperformed human/operational acceptance is never a pass.
- Keep documentation, code and validation evidence sufficient for a fresh session to resume without a conversation transcript.
- Install additional standalone software/tooling under C:/xxx/_INSTALLS/_HERE/_xxx unless the user specifies otherwise.
