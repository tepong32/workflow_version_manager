"""Optional configuration loading for Version Manager."""

from __future__ import annotations

import json
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ReleaseConfig:
    """Configurable release conventions with portable defaults."""

    version_file: str | None = None
    changelog_file: str | None = None
    version_files: tuple[str, ...] = ()
    documentation_files: tuple[str, ...] = ()
    tag_prefix: str = "v"
    commit_template: str = "Release {tag}: {message}"
    categories: dict[str, str] = field(default_factory=lambda: {
        "feature": "Added", "fix": "Fixed", "refactor": "Refactored",
        "chore": "Maintenance", "docs": "Documentation",
    })


class ConfigLoader:
    """Load JSON configuration or ``[tool.version-manager]`` from pyproject."""

    JSON_FILES = (".versionmanager.json", "version_manager.json")

    @classmethod
    def load(cls, root: Path) -> ReleaseConfig:
        data: dict[str, Any] = {}
        for name in cls.JSON_FILES:
            path = root / name
            if path.exists():
                data = json.loads(path.read_text(encoding="utf-8"))
                break
        else:
            pyproject = root / "pyproject.toml"
            if pyproject.exists():
                with pyproject.open("rb") as handle:
                    data = tomllib.load(handle).get("tool", {}).get("version-manager", {})
        return ReleaseConfig(
            version_file=data.get("version_file"),
            changelog_file=data.get("changelog_file"),
            version_files=tuple(data.get("version_files", [])),
            documentation_files=tuple(data.get("documentation_files", [])),
            tag_prefix=data.get("tag_prefix", "v"),
            commit_template=data.get("commit_template", "Release {tag}: {message}"),
            categories=data.get("categories", ReleaseConfig().categories),
        )
