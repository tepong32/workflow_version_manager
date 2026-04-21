# 🚀 Workflow Version Manager

A lightweight, portable toolkit for **versioning, changelog generation, and workflow automation** — designed for developers who want fast, consistent, and repeatable release processes.

---

## ✨ Core Features

### 📦 Version Manager (`version_manager.py`)

* Semantic versioning (patch / minor / major)
* Auto-generates structured changelog entries
* Categorized updates (feature, fix, refactor, etc.)
* Updates version across multiple files
* Git integration:

  * add
  * commit
  * tag
  * push
* Dry-run mode for safe previews

---

### ⚙️ Auto Merge Tool (`auto_merge.py`)

* Safely resolves Git merge conflicts
* Designed for AI-assisted workflows
* Protects critical files by default
* Optional aggressive mode for full auto-resolution

---

### 🧱 Repo Bootstrap (`repo_bootstrap.py`)

* Instantly prepares any new repository
* Copies your toolset into `/tools`
* Generates a standard `AGENTS.md`
* Ensures consistent development environment across projects

---

# 📁 Project Structure (Recommended)

```
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

# ⚡ Installation / Setup

### 1. Clone this repository (your master toolkit)

```
git clone https://github.com/tepong32/workflow_version_manager.git
```

### 2. Store it somewhere stable

Example:

```
~/dev-tools/
```

---

# 🚀 Usage

## 🔹 Version Manager

### Basic Usage

```
python version_manager.py "your message here"
```

### With version bump

```
python version_manager.py "added request lifecycle" minor
```

### With category

```
python version_manager.py "fixed validation bug" patch -c fix
```

### Dry run (preview only)

```
python version_manager.py "test release" --dry-run
```

---

## ⚡ Recommended Shortcut (Alias)

Example:

```
alias vm='python ~/dev-tools/version_manager.py'
```

Then just run:

```
vm "added lifecycle engine" minor
```

---

## 🔹 Auto Merge Tool

### Safe mode (default)

```
python auto_merge.py
```

✔ Resolves only safe files (e.g., VERSION, CHANGELOG)
✔ Skips sensitive logic automatically

---

### Aggressive mode (use carefully)

```
python auto_merge.py --unsafe
```

⚠️ Resolves ALL conflicts — may overwrite important logic

---

## 🔹 Repo Bootstrap (IMPORTANT)

This is your **standard starting point for every new project**.

---

### Step-by-step

```
mkdir my-project
cd my-project
git init
```

Then run:

```
python ~/dev-tools/repo_bootstrap.py
```

---

### What it does

* Creates `/tools/` folder
* Copies:

  * `version_manager.py`
  * `auto_merge.py`
* Generates `AGENTS.md`
* Optionally creates initial commit

---

### Recommended Alias

```
alias bootstrap='python ~/dev-tools/repo_bootstrap.py'
```

Then your workflow becomes:

```
git init
bootstrap
```

---

# 🧠 AGENTS.md (Why it matters)

`AGENTS.md` acts as a **policy file for AI-assisted development**.

Default rules include:

* conserve tokens
* avoid unnecessary verbosity
* respect architecture
* enforce safe merge behavior

This keeps AI tools aligned with your workflow.

---

# 🧩 Philosophy

This toolkit is built around:

* **Consistency over convenience**
* **Automation with safeguards**
* **AI-assisted development readiness**

It is intentionally:

* simple
* portable
* extensible

---

# 🔮 Future Enhancements

* AI-aware merge conflict analysis
* AGENTS.md-driven automation rules
* smarter changelog generation
* multi-project tooling support

---

# 🤝 Contributing

Feel free to fork and adapt to your workflow.

---

# 📌 Final Note

This is not just a script collection.

It’s the foundation of a **repeatable development workflow system**.

Use it consistently, refine it over time, and it will compound your productivity.
