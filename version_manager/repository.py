"""Repository inspection and safe documentation discovery."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from .config import ReleaseConfig
from .git import GitService
from .versioning import VersionCalculator


@dataclass(frozen=True)
class RepositoryInfo:
    """Runtime facts discovered from the repository rather than assumptions."""

    root: Path
    name: str
    branch: str
    default_branch: str | None
    tags: tuple[str, ...]
    version: str
    version_file: Path | None
    changelog: Path | None
    documentation: tuple[Path, ...]


class RepositoryInspector:
    """Discover common release files without requiring a fixed project layout."""

    DOC_NAMES = ("README.md", "CHANGELOG.md", "ROADMAP.md", "RELEASE_NOTES.md", "VERSION.md")
    VERSION_NAMES = ("VERSION", "VERSION.txt", "version.txt")

    def __init__(self, root: Path, config: ReleaseConfig, git: GitService) -> None:
        self.root, self.config, self.git = root, config, git

    def inspect(self) -> RepositoryInfo:
        docs = self.documentation_files()
        version_file = self.find_version_file()
        tags = tuple(self.git.tags())
        version = self.read_version(version_file, tags)
        return RepositoryInfo(self.root, self.root.name, self.git.branch(), self.git.default_branch(),
                              tags, version, version_file, self.find_changelog(docs), tuple(docs))

    def documentation_files(self) -> list[Path]:
        found: set[Path] = set()
        names = {name.lower() for name in self.DOC_NAMES}
        # Match conventional names case-insensitively so a copied tool behaves
        # the same on Windows, macOS, and case-sensitive Linux filesystems.
        found.update(path for path in self.root.iterdir() if path.is_file() and path.name.lower() in names)
        for relative in (*self.DOC_NAMES, *self.config.documentation_files):
            path = self.root / relative
            if path.is_file(): found.add(path)
        for directory in (self.root / "docs", self.root / "documentation"):
            if directory.is_dir(): found.update(p for p in directory.rglob("*.md") if p.is_file())
        return sorted(found)

    def find_version_file(self) -> Path | None:
        candidates = ([self.config.version_file] if self.config.version_file else []) + list(self.VERSION_NAMES)
        for relative in candidates:
            path = self.root / relative
            if path.is_file(): return path
        return None

    def find_changelog(self, docs: list[Path]) -> Path | None:
        if self.config.changelog_file:
            path = self.root / self.config.changelog_file
            return path if path.is_file() else None
        return next((path for path in docs if path.name.lower() == "changelog.md"), None)

    def read_version(self, version_file: Path | None, tags: tuple[str, ...]) -> str:
        if version_file:
            value = VersionCalculator.validate(version_file.read_text(encoding="utf-8").strip())
            if value: return value
        pyproject = self.root / "pyproject.toml"
        if pyproject.exists():
            match = re.search(r'^version\s*=\s*["\']([^"\']+)', pyproject.read_text(encoding="utf-8"), re.M)
            if match and (value := VersionCalculator.validate(match.group(1))): return value
        package = self.root / "package.json"
        if package.exists():
            try:
                if value := VersionCalculator.validate(json.loads(package.read_text(encoding="utf-8")).get("version", "")): return value
            except json.JSONDecodeError: pass
        return next((value for tag in tags if (value := VersionCalculator.validate(tag))), "0.0.0")
