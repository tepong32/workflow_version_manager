# 🧭 Version Manager

> Automate versioning and changelog updates in your Git projects with a single Python script.

---

### 🚀 Overview
**Version Manager** is a command-line utility that enforces a clean, consistent release workflow. It automatically handles semantic version bumps, updates your changelog, and now commits, tags, and pushes the release to your remote repository—all in one atomic operation.

This tool ensures a traceable version history with minimal manual effort.

---

### ✨ Key Features
- 🔢 **Semantic Versioning** (`major`, `minor`, `patch`)
- 🧾 **Categorized Changelog:** Auto-generated entries using headers like `✨ Added`, `🐞 Fixed`, etc.
- 📦 **Multi-File Version Sync:** Updates version string in files like `VERSION`, `CHANGELOG.md`, and **`setup.py`** (configurable).
- 🛡️ **Pre-Check Safety:** Prevents releases if the Git working directory is not clean.
- 🚀 **Full Git Automation:** Automatically stages, commits, tags, and **pushes the release and tags** to your remote.
- 🧪 **Dry-Run Mode** to safely preview changes.
- 🎨 **Color-Coded Output** for easy process monitoring.

---

### ⚙️ Usage

#### Basic command
```bash
python version_manager.py "MESSAGE" [BUMP_TYPE] --category CATEGORY --dry-run
```

#### Example
```bash
python version_manager.py "Initial release of version_manager.py" minor -c refactor -d 
```
#### Multiline changelog example
```
python version_manager.py """\
Added new CLI options and improved validation.
- Supports dry-run previews
- Handles invalid VERSION formats gracefully
""" patch -c refactor
```
#### Dry-run preview (no files modified)
```
python version_manager.py "Testing preview" patch --dry-run
```

#### Arguments & Configuration
|Argument |	Purpose | Example Value |
|---------|---------|---------------|
|"MESSAGE" | The required commit message and changelog text. | "Optimized API call handler" |
|[BUMP_TYPE] | (Optional) Which version segment to increment. Defaults to patch. |	minor, major, patch|
|--category (-c) CATEGORY |	(Optional) The header to use in CHANGELOG.md. Defaults to feature. | fix, refactor, chore, docs |
|--dry-run (-d) | (Optional) Shows what would happen without writing files or running Git commands. | --dry-run |

### 🧰 Requirements

Python 3.8+

colorama

Install dependencies:
```bash
pip install colorama
```

### 🗂️ Configurable Files Managed
The script is configured to update version strings in VERSION, CHANGELOG.md, and any files listed in the internal VERSIONED_FILES list (e.g., setup.py).

🪄 Example Workflow
|Action | Command | Result |
|-------|---------|--------|
|New Feature Release | ```python version_manager.py "Implemented OAuth login" minor --category feature``` | "Bumps version (e.g., 1.2.3 → 1.3.0), updates files, commits, tags, and pushes." |
|Bug Fix Release | ```python version_manager.py "Fixed memory leak in parser" --category fix``` | "Bumps patch version (default), updates files, commits, tags, and pushes." |
|Multi-line Changelog | ```python version_manager.py """Added CLI options and improved validation.\n- Supports dry-run\n- Handles invalid VERSION formats""" patch``` | Uses multi-line string for detailed release notes. |
|Safe Preview | ```python version_manager.py "Testing preview" minor --dry-run``` | Shows all file and Git actions without changing anything. |

### 🏷️ Full Git Integration

- You no longer need to run manual push commands!
- On success, the script automatically:
- Ensures the Git working directory is clean.
- Adds all versioned files (VERSION, CHANGELOG.md, setup.py, etc.).
- Commits with your message and new version number.
- Creates a Git tag (e.g., v1.2.0).
- Pushes the new commit and the new tag to your remote repository.


### 📜 License

MIT License © 2025 — Created by tEppy™ (Cristino Agapito Jr)

### 💡 Tip

Use this tool as the final step in your development process. Ensure all feature/bugfix code is committed before running this script, as it handles the final "release" commit.