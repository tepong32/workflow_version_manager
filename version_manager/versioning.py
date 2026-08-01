"""Semantic-version parsing and calculation."""

from __future__ import annotations

import re


class VersionCalculator:
    """Calculate stable semantic-version bumps without external dependencies."""

    PATTERN = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")

    @classmethod
    def validate(cls, value: str) -> str | None:
        """Return the normalized version if it is ``major.minor.patch``."""
        match = cls.PATTERN.fullmatch(value.strip().removeprefix("v"))
        return ".".join(match.groups()) if match else None

    @classmethod
    def bump(cls, current: str, kind: str) -> str:
        """Return the next major, minor, or patch version."""
        normalized = cls.validate(current)
        if not normalized:
            raise ValueError(f"Not a semantic version: {current!r}")
        major, minor, patch = map(int, normalized.split("."))
        if kind == "major":
            major, minor, patch = major + 1, 0, 0
        elif kind == "minor":
            minor, patch = minor + 1, 0
        elif kind == "patch":
            patch += 1
        else:
            raise ValueError(f"Unsupported bump type: {kind}")
        return f"{major}.{minor}.{patch}"
