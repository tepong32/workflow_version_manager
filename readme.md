# 🧭 Version Manager

> Automate versioning and changelog updates in your Git projects with a single Python script.

---

### 🚀 Overview
**Version Manager** is a lightweight command-line utility that simplifies version control in Git repositories.  
It automatically manages semantic version bumps, updates your changelog, and creates Git commits and tags — all in one step.

This tool is ideal for developers who want consistent release tracking without manual editing or complex CI scripts.

---

### ✨ Features
- 🔢 **Semantic versioning** (`major`, `minor`, `patch`)
- 🧾 **Auto-generated changelog entries** with date stamps
- 📦 **VERSION file management**
- 🪣 **Git integration:** automatic add, commit, and tag creation
- 🧪 **Dry-run mode** to preview changes
- 🎨 **Color-coded terminal output** for easy reading

---

### ⚙️ Usage

#### Basic command
```bash
python version_manager.py "Commit message" [major|minor|patch]
```

#### Example
```bash
python version_manager.py "Initial release of version_manager.py" minor

Multiline changelog example
python version_manager.py """\
Added new CLI options and improved validation.
- Supports dry-run previews
- Handles invalid VERSION formats gracefully
""" patch

Dry-run preview (no files modified)
python version_manager.py "Testing preview" patch --dry-run
```
### 🧰 Requirements

Python 3.8+

colorama

Install dependencies:
```bash
pip install colorama
```

### 🗂️ Files Managed
File	Purpose
VERSION	Tracks the current semantic version
CHANGELOG.md	Stores release notes, auto-updated on each bump
🪄 Example Workflow
#### Patch bump with commit + tag
```bash
python version_manager.py "Fix minor bug" patch
```

#### Minor bump for new features
```bash
python version_manager.py "Add new command-line options" minor
```

#### Preview changes without saving
```bash
python version_manager.py "Test changelog formatting" --dry-run
```

### 🏷️ Git Integration

Each bump automatically:

- Adds VERSION and CHANGELOG.md

- Commits with your changelog message and version

- Creates a Git tag (e.g., v1.2.0)

You can push these as usual:
```bash
git push && git push --tags
```

### 📜 License

MIT License © 2025 — Created by Tepong Agapito

### 💡 Tip

Use this tool as part of your release process — run it before each git push to maintain a clean, traceable version history.