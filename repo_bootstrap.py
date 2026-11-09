"""Bootstrap or update the shared workflow tools in a Git repository.

Usage (from inside the target repository, or pass its path):
    python <template>/repo_bootstrap.py [TARGET] [--update] [--no-agents] [--no-commit]

* Copies the template tools into TARGET/tools/ (existing files are kept unless
  --update is given, in which case outdated copies are replaced).
* Runs ``tools/version_manager.py init`` so VERSION and CHANGELOG.md exist.
* Creates a starter AGENTS.md when missing (skip with --no-agents).
* Creates an initial commit only for a repository without any commits.

Template location: $DEV_TOOLS_DIR, else the directory containing this script.
"""

from __future__ import annotations

import argparse
import filecmp
import os
import shutil
import subprocess
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    _reconfigure = getattr(_stream, "reconfigure", None)
    if _reconfigure:
        _reconfigure(encoding="utf-8", errors="replace")

# Files inside the template directory that are copied into <repo>/tools/.
FILES_TO_COPY = [
    "auto_merge.py",
    "version_manager.py",
]

AGENTS_TEMPLATE = """# AGENTS.md

## Core Rules
- Conserve tokens when possible
- Avoid unnecessary verbosity
- Respect existing architecture before suggesting changes

## Development Principles
- Prefer clarity over cleverness
- Keep logic centralized (avoid duplication)
- Fail safely (handle edge cases explicitly)

## Release Workflow
- Stage the intended changes, then checkpoint with
  `python tools/version_manager.py "Summary" [patch|minor|major] -c <category>`
- Preview first when unsure: `python tools/version_manager.py preview patch "Summary"`

## Merge Policy
- Do not auto-resolve critical logic files
- Prefer safe merges for VERSION and CHANGELOG
- Review service/model changes manually
"""


def resolve_template_dir() -> Path:
    """$DEV_TOOLS_DIR wins; otherwise the folder this script lives in."""
    env_path = os.getenv("DEV_TOOLS_DIR")
    if env_path:
        path = Path(env_path)
        if path.is_dir():
            return path
        print(f"warning: DEV_TOOLS_DIR does not exist: {env_path}; using script directory")
    return Path(__file__).resolve().parent


def git_root(target: Path) -> Path:
    result = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=target,
                            capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"error: not a Git repository: {target} (run 'git init' first)")
    return Path(result.stdout.strip())


def copy_tools(template: Path, root: Path, update: bool) -> tuple[list[str], list[str]]:
    tools_dir = root / "tools"
    tools_dir.mkdir(exist_ok=True)
    changed, unchanged = [], []
    for name in FILES_TO_COPY:
        src, dst = template / name, tools_dir / name
        if not src.is_file():
            print(f"warning: missing in template: {name}")
            continue
        if dst.exists():
            if filecmp.cmp(src, dst, shallow=False):
                unchanged.append(name)
                continue
            if not update:
                print(f"kept existing tools/{name} (differs from template; use --update to replace)")
                unchanged.append(name)
                continue
        shutil.copyfile(src, dst)
        changed.append(name)
        print(f"{'updated' if update and dst.exists() else 'copied'}: tools/{name}")
    return changed, unchanged


def ensure_release_files(root: Path) -> None:
    subprocess.run([sys.executable, str(root / "tools" / "version_manager.py"), "-C", str(root), "init"], check=False)


def create_agents_md(root: Path) -> bool:
    path = root / "AGENTS.md"
    if path.exists():
        return False
    path.write_text(AGENTS_TEMPLATE, encoding="utf-8")
    print("created: AGENTS.md")
    return True


def initial_commit(root: Path) -> None:
    if subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True).returncode == 0:
        return
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-m", "Initial project bootstrap"], cwd=root, check=True)
    print("created initial commit")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap or update shared workflow tools in a repository.")
    parser.add_argument("target", nargs="?", default=".", help="Repository path (default: current directory)")
    parser.add_argument("--update", action="store_true", help="Replace tools that differ from the template")
    parser.add_argument("--no-agents", action="store_true", help="Do not create AGENTS.md")
    parser.add_argument("--no-commit", action="store_true", help="Never create an initial commit")
    args = parser.parse_args()

    template = resolve_template_dir()
    root = git_root(Path(args.target).resolve())
    print(f"Template: {template}\nRepository: {root}\n")

    changed, unchanged = copy_tools(template, root, args.update)
    ensure_release_files(root)
    agents = False if args.no_agents else create_agents_md(root)
    if not args.no_commit:
        initial_commit(root)

    print(f"\nTools changed: {len(changed)} | unchanged: {len(unchanged)} | AGENTS.md created: {'yes' if agents else 'no'}")


if __name__ == "__main__":
    main()
