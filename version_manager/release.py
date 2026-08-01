"""Orchestrate a complete, previewable release."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .config import ReleaseConfig
from .documentation import DocumentationUpdater
from .git import GitError, GitService
from .repository import RepositoryInfo
from .versioning import VersionCalculator


@dataclass(frozen=True)
class ReleasePlan:
    """The complete set of changes and Git operations for one release."""
    version: str
    tag: str
    commit_message: str
    updates: dict[Path, str]


class ReleaseService:
    """Apply version, documentation, commit, tag, and optional push steps."""

    def __init__(self, info: RepositoryInfo, config: ReleaseConfig, git: GitService) -> None:
        self.info, self.config, self.git = info, config, git

    def plan(self, bump: str, message: str, category: str) -> ReleasePlan:
        version = VersionCalculator.bump(self.info.version, bump)
        tag = f"{self.config.tag_prefix}{version}"
        updates = DocumentationUpdater(self.info, self.config).planned_updates(version, message, category)
        commit = self.config.commit_template.format(version=version, tag=tag, message=message)
        return ReleasePlan(version, tag, commit, updates)

    def execute(self, plan: ReleasePlan, *, dry_run: bool, push: bool, allow_dirty: bool) -> None:
        if not allow_dirty and not self.git.is_clean():
            raise GitError("Working directory is not clean. Commit, stash, or pass --allow-dirty.")
        if dry_run: return
        for path, content in plan.updates.items(): path.write_text(content, encoding="utf-8")
        files = [str(path.relative_to(self.info.root)) for path in plan.updates]
        if not files: raise GitError("No release files were discovered; configure version_files or add a VERSION file.")
        self.git.commit(files, plan.commit_message)
        self.git.tag(plan.tag)
        if push:
            if not self.git.remote_exists(): raise GitError("No Git remote is configured; release was created locally but cannot be pushed.")
            self.git.push(plan.tag, self.info.branch)
