"""Release-note generation and conservative documentation updates."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from .config import ReleaseConfig
from .repository import RepositoryInfo


class DocumentationUpdater:
    """Create a changelog entry and update discovered version references."""

    def __init__(self, info: RepositoryInfo, config: ReleaseConfig) -> None:
        self.info, self.config = info, config

    def release_notes(self, version: str, message: str, category: str) -> str:
        title = self.config.categories.get(category, category.replace("_", " ").title())
        body = message.strip() if "\n" in message else f"- {message.strip()}"
        return f"## [{version}] - {date.today().isoformat()}\n### {title}\n{body}\n\n"

    def planned_updates(self, version: str, message: str, category: str) -> dict[Path, str]:
        updates: dict[Path, str] = {}
        old = self.info.version
        if self.info.version_file:
            updates[self.info.version_file] = version + "\n"
        else:
            # A standalone release tool needs a durable version source even in a
            # minimal repository. Creating this conventional file is optional in
            # the sense that no existing project file is required.
            updates[self.info.root / "VERSION"] = version + "\n"
        if self.info.changelog:
            updates[self.info.changelog] = self._prepend_changelog(self.info.changelog.read_text(encoding="utf-8"), self.release_notes(version, message, category))
        else:
            updates[self.info.root / "CHANGELOG.md"] = "# Changelog\n\n" + self.release_notes(version, message, category)
        for file in self._version_targets():
            content = file.read_text(encoding="utf-8")
            replacement = self._replace_version(content, old, version)
            if replacement != content: updates[file] = replacement
        return updates

    def _version_targets(self) -> list[Path]:
        explicit = [self.info.root / item for item in self.config.version_files]
        # Documentation updates are opt-in by content: only known release-facing docs containing the old version change.
        candidates = [*explicit, *self.info.documentation]
        return sorted({path for path in candidates if path.is_file() and path != self.info.changelog})

    @staticmethod
    def _replace_version(content: str, old: str, new: str) -> str:
        return re.sub(rf"(?<![\d.]){re.escape(old)}(?![\d.])", new, content)

    @staticmethod
    def _prepend_changelog(content: str, entry: str) -> str:
        if not content.strip(): return "# Changelog\n\n" + entry
        heading = re.search(r"^# .+$", content, re.M)
        if heading:
            end = content.find("\n", heading.end())
            return content[:end + 1] + "\n" + entry + content[end + 1:].lstrip("\n")
        return "# Changelog\n\n" + entry + content
