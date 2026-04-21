# 🚀 Workflow Version Manager

A lightweight, portable toolkit for **versioning, changelog automation, and repository bootstrapping** — designed for fast, consistent, AI-assisted development workflows.

---

## ✨ Core Tools

### 📦 `version_manager.py`

* Semantic versioning (patch / minor / major)
* Auto-generated structured changelog
* Categorized updates (feature, fix, refactor, etc.)
* Updates version across multiple files
* Git integration (add → commit → tag → push)
* Dry-run preview mode

---

### ⚙️ `auto_merge.py`

* Safe Git merge conflict resolution
* Designed for AI-generated diffs
* Protects sensitive files by default
* Optional aggressive (`--unsafe`) mode

---

### 🧱 `repo_bootstrap.py`

* One-command project setup
* Copies tools into `/tools`
* Generates `AGENTS.md`
* Standardizes every repo you create

---

# 📁 Recommended Project Structure

```id="a2q8hz"
project-root/
│
├── tools/
│   ├── version_manager.py
│   ├── auto_merge.py
│
├── VERSION
├── CHANGELOG.md
├── AGENTS.md
```

---

# ⚙️ Setup (Important)

## 1. Clone this repository

```id="l2p7ci"
git clone https://github.com/tepong32/workflow_version_manager.git
```

---

## 2. Set your template directory (RECOMMENDED)

This allows `repo_bootstrap.py` to work from anywhere.

---

### 🪟 Windows (PowerShell)

```id="1k5b0k"
setx DEV_TOOLS_DIR "C:\Users\<you>\Desktop\GH\workflow_version_manager"
```

Restart your terminal after running this.

---

### 🐧 Linux / WSL / Git Bash

```id="b3g9ka"
export DEV_TOOLS_DIR=~/Desktop/GH/workflow_version_manager
```

For persistence:

```id="u7v6mj"
echo 'export DEV_TOOLS_DIR=~/Desktop/GH/workflow_version_manager' >> ~/.bashrc
source ~/.bashrc
```

---

## 🔍 How it works

`repo_bootstrap.py` resolves the template directory using:

1. `DEV_TOOLS_DIR` (environment variable)
2. Fallback: `~/Desktop/GH/workflow_version_manager`  *(this matches tEppy's workflow, you can change this default path on **`resolve_template_dir`**)*

---

# 🚀 Usage

---

## 🔹 Version Manager

### Basic

```id="r3x1lt"
python version_manager.py "your message"
```

### With version bump

```id="d2h9zk"
python version_manager.py "added lifecycle engine" minor
```

### With category

```id="y8k2va"
python version_manager.py "fixed validation bug" -c fix
```

### Dry run

```id="x6j1pw"
python version_manager.py "test release" --dry-run
```

---

## ⚡ Recommended Alias

```id="k1p8zw"
alias vm='python ~/Desktop/GH/workflow_version_manager/version_manager.py'
```

Then:

```id="n4c6jq"
vm "added lifecycle engine" minor
```

---

## 🔹 Auto Merge

### Safe mode

```id="v2m5sa"
python auto_merge.py
```

### Aggressive mode

```id="t7p3nx"
python auto_merge.py --unsafe
```

---

## 🔹 Repo Bootstrap (Key Feature)

### Step-by-step

```id="z5n8pw"
mkdir my-project
cd my-project
git init
```

Then:

```id="e9c2hv"
python ~/Desktop/GH/workflow_version_manager/repo_bootstrap.py
```

---

### What happens

* `/tools/` folder is created
* `version_manager.py` and `auto_merge.py` are copied
* `AGENTS.md` is generated
* Optional initial commit is created

---

## ⚡ Recommended Alias

```id="s8x3jd"
alias bootstrap='python ~/Desktop/GH/workflow_version_manager/repo_bootstrap.py'
```

Usage:

```id="p4v7rq"
git init
bootstrap
```

---

# 🧠 AGENTS.md

This file defines rules for AI-assisted development.

### Default includes:

* conserve tokens
* avoid unnecessary verbosity
* respect architecture
* enforce safe merge behavior

---

# 🧩 Philosophy

This toolkit is built for:

* **Consistency across projects**
* **Safe automation**
* **AI-assisted workflows**
* **Minimal friction setup**

---

# 🔮 Future Direction

* AI-aware merge conflict analysis
* AGENTS.md-driven automation
* CLI packaging (`vm`, `bootstrap`, etc.)
* multi-project workflow orchestration

---

# 📌 Final Note

This is not just a script collection.

It’s a **portable development workflow system**.

Use it consistently, refine it based on real usage, and it will scale with your projects.
