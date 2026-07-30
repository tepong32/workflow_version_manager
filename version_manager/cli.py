"""Command-line interface for the standalone Version Manager product."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .config import ConfigLoader
from .git import GitError, GitService
from .release import ReleasePlan, ReleaseService
from .repository import RepositoryInspector


def _root(path: str) -> Path:
    """Resolve a supplied directory to its Git repository root."""
    candidate = Path(path).resolve()
    return GitService(candidate).root_path()


def build_parser() -> argparse.ArgumentParser:
    """Build the documented CLI, including its legacy positional release form."""
    parser = argparse.ArgumentParser(
        description="Portable Git release manager: inspect, preview, or create a release.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Legacy compatibility: version_manager.py 'message' [patch|minor|major] [-c category] [-d]",
    )
    parser.add_argument("--repo", default=".", help="Repository directory (default: current directory).")
    subparsers = parser.add_subparsers(dest="command")

    inspect = subparsers.add_parser("inspect", help="Show discovered repository and release metadata.")
    inspect.add_argument("--json", action="store_true", help="Print the inspection result as JSON.")
    for name, help_text in (("release", "Write docs, commit, tag, and optionally push."),
                            ("preview", "Show a release plan without making changes.")):
        command = subparsers.add_parser(name, help=help_text)
        command.add_argument("bump", choices=("patch", "minor", "major"), help="Version component to increment.")
        command.add_argument("message", help="Release-note and commit summary.")
        command.add_argument("-c", "--category", default="feature", help="Release-note category (default: feature).")
        command.add_argument("-d", "--dry-run", action="store_true", help="Preview without writing or running Git.")
        command.add_argument("--push", action="store_true", help="Push the release branch and tag after local creation.")
        command.add_argument("--yes", action="store_true", help="Do not ask for confirmation before a non-dry release.")
        command.add_argument("--allow-dirty", action="store_true", help="Permit pre-existing uncommitted changes (use carefully).")
    # Old interface: a leading message is interpreted as a patch/minor/major release.
    parser.add_argument("legacy_message", nargs="?", help=argparse.SUPPRESS)
    parser.add_argument("legacy_bump", nargs="?", choices=("patch", "minor", "major"), default="patch", help=argparse.SUPPRESS)
    parser.add_argument("-c", "--category", default="feature", help=argparse.SUPPRESS)
    parser.add_argument("-d", "--dry-run", action="store_true", help=argparse.SUPPRESS)
    return parser


def _describe_plan(plan: ReleasePlan) -> str:
    files = "\n".join(f"  - {path}" for path in plan.updates) or "  - (none)"
    return (f"Version: {plan.tag}\nCommit: {plan.commit_message}\n"
            f"Files to update:\n{files}\nTag: {plan.tag}")


def _confirm(plan: ReleasePlan) -> bool:
    try:
        return input(f"\nCreate this release? [y/N] {_describe_plan(plan)}\n> ").strip().lower() in {"y", "yes"}
    except EOFError:
        return False


def _inspect(root: Path, as_json: bool) -> int:
    config, git = ConfigLoader.load(root), GitService(root)
    info = RepositoryInspector(root, config, git).inspect()
    values = {"root": str(info.root), "name": info.name, "branch": info.branch,
              "default_branch": info.default_branch, "version": info.version,
              "latest_tag": info.tags[0] if info.tags else None,
              "version_file": str(info.version_file) if info.version_file else None,
              "changelog": str(info.changelog) if info.changelog else None,
              "documentation": [str(path) for path in info.documentation]}
    if as_json: print(json.dumps(values, indent=2))
    else:
        for name, value in values.items(): print(f"{name.replace('_', ' ').title()}: {value}")
    return 0


def _release(root: Path, args: argparse.Namespace, *, legacy: bool = False) -> int:
    config, git = ConfigLoader.load(root), GitService(root)
    info = RepositoryInspector(root, config, git).inspect()
    service = ReleaseService(info, config, git)
    bump = args.legacy_bump if legacy else args.bump
    message = args.legacy_message if legacy else args.message
    plan = service.plan(bump, message, args.category)
    print(_describe_plan(plan))
    dry_run = args.dry_run or (not legacy and args.command == "preview")
    if dry_run:
        print("\nPreview only: no files or Git state changed.")
        return 0
    if not getattr(args, "yes", False) and not _confirm(plan):
        print("Release cancelled.")
        return 0
    service.execute(plan, dry_run=False, push=getattr(args, "push", False), allow_dirty=getattr(args, "allow_dirty", False))
    print(f"\nReleased {plan.tag}. Commit: {plan.commit_message}")
    if getattr(args, "push", False): print("Branch and tag pushed to origin.")
    return 0


def main(argv: list[str] | None = None) -> int:
    """Execute the CLI and translate expected operational failures into exit code 1."""
    raw_args = list(sys.argv[1:] if argv is None else argv)
    # argparse subparsers cannot share a first positional token with the old
    # interface. Detect that established form before giving the rest to the
    # explicit-command parser.
    commands = {"inspect", "release", "preview"}
    if raw_args and not raw_args[0].startswith("-") and raw_args[0] not in commands:
        legacy = argparse.ArgumentParser(description="Legacy Version Manager release command.")
        legacy.add_argument("message")
        legacy.add_argument("bump", nargs="?", choices=("patch", "minor", "major"), default="patch")
        legacy.add_argument("-c", "--category", default="feature")
        legacy.add_argument("-d", "--dry-run", action="store_true")
        legacy.add_argument("--repo", default=".")
        args = legacy.parse_args(raw_args)
        args.legacy_message, args.legacy_bump = args.message, args.bump
        try:
            return _release(_root(args.repo), args, legacy=True)
        except (GitError, ValueError, OSError, json.JSONDecodeError) as error:
            print(f"Error: {error}", file=sys.stderr)
            return 1
    parser = build_parser()
    args = parser.parse_args(raw_args)
    try:
        root = _root(args.repo)
        if args.command == "inspect": return _inspect(root, args.json)
        if args.command in {"release", "preview"}: return _release(root, args)
        if args.legacy_message: return _release(root, args, legacy=True)
        parser.print_help()
        return 2
    except (GitError, ValueError, OSError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
