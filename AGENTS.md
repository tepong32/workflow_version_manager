# Workflow Version Manager - repository guide

## Project context and documentation map

Portable Python 3.11+ and Git release automation toolkit. version_manager.py is the entry point and version_manager/ holds reusable logic for discovery, versioning, release-document edits, commits and tags.

### Durable boundaries

Remain repository-neutral: no hard-coded project identity, branch or milestone assumptions. Preserve preview/dry-run, confirmation, clean-tree protection and optional push behavior. Test release mutations only in disposable temporary repositories.

### Development state

The July 31 overhaul provides reusable release workflows. README.md documents current commands; no new release or product roadmap is introduced by continuity setup.

### Read next

- [README.md](README.md)
- [CHANGELOG.md](CHANGELOG.md)
- [version_manager.example.json](version_manager.example.json)
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
