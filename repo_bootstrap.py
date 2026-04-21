import shutil
import subprocess
from pathlib import Path
import sys

# -------------------------------
# CONFIG (edit once, reuse everywhere)
# -------------------------------

# 🔁 CHANGE THIS to your master tools folder
TEMPLATE_DIR = Path.home() / "dev-tools"

# Files inside TEMPLATE_DIR to copy into repo/tools/
FILES_TO_COPY = [
    "auto_merge.py",
    "version_manager.py",
]

# Default AGENTS.md template
AGENTS_TEMPLATE = """# AGENTS.md

## Core Rules
- Conserve tokens when possible
- Avoid unnecessary verbosity
- Respect existing architecture before suggesting changes

## Development Principles
- Prefer clarity over cleverness
- Keep logic centralized (avoid duplication)
- Fail safely (handle edge cases explicitly)

## Merge Policy
- Do not auto-resolve critical logic files
- Prefer safe merges for VERSION and CHANGELOG
- Review service/model changes manually

"""

# -------------------------------
# CORE FUNCTIONS
# -------------------------------

def ensure_git_repo():
    """Ensure current directory is a git repo."""
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        print("❌ Not a git repository. Run 'git init' first.")
        sys.exit(1)


def copy_tools():
    """Copy tool scripts into ./tools/"""
    tools_dir = Path.cwd() / "tools"
    tools_dir.mkdir(exist_ok=True)

    copied = []
    skipped = []

    for file_name in FILES_TO_COPY:
        src = TEMPLATE_DIR / file_name
        dst = tools_dir / file_name

        if not src.exists():
            print(f"⚠️ Missing in template: {file_name}")
            skipped.append(file_name)
            continue

        if dst.exists():
            print(f"⏭️ Already exists (skipped): {file_name}")
            skipped.append(file_name)
            continue

        try:
            shutil.copy(src, dst)
            copied.append(file_name)
            print(f"✅ Copied: tools/{file_name}")
        except Exception as e:
            print(f"❌ Failed to copy {file_name}: {e}")

    return copied, skipped


def create_agents_md():
    """Create AGENTS.md if not present."""
    path = Path.cwd() / "AGENTS.md"

    if path.exists():
        print("⏭️ AGENTS.md already exists (skipped)")
        return False

    try:
        path.write_text(AGENTS_TEMPLATE, encoding="utf-8")
        print("✅ Created: AGENTS.md")
        return True
    except Exception as e:
        print(f"❌ Failed to create AGENTS.md: {e}")
        return False


def initial_commit():
    """Optional initial commit if repo is empty."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        has_commit = result.returncode == 0

        if has_commit:
            print("⏭️ Repo already has commits (skipping initial commit)")
            return

        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Initial project bootstrap"], check=True)

        print("🚀 Initial commit created.")

    except Exception as e:
        print(f"⚠️ Could not create initial commit: {e}")


# -------------------------------
# MAIN
# -------------------------------

def main():
    print("🚀 Bootstrapping repository...\n")

    ensure_git_repo()

    copied, skipped = copy_tools()
    agents_created = create_agents_md()

    # Summary
    print("\n--- SUMMARY ---")
    print(f"Tools copied: {len(copied)}")
    print(f"Skipped: {len(skipped)}")
    print(f"AGENTS.md created: {'Yes' if agents_created else 'No'}")

    # Optional commit
    initial_commit()

    print("\n🎉 Repo is ready.\n")


if __name__ == "__main__":
    main()