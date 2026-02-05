---
name: flask-setup-for-beginners
description: Set up Python Flask development environment for beginners with step-by-step guidance, virtual environment creation, and troubleshooting
license: Complete terms in LICENSE.txt
---

# Flask Setup for Beginners
**Version:** 0.17.0

## When to Use
- User wants Flask web application
- Beginner needs Flask environment setup
- User asks "How do I set up Flask?"

## Instructions for ASSISTANT
**Format ALL instructions as Claude Code copy/paste blocks.**

**DO NOT:** Manual instructions like "Open File Explorer", "Navigate to folder"
**ALWAYS:** Single code block with TASK, STEPs, and report request

## Setup Steps

### 1. Verify Python
```bash
python --version
```
**Expected:** Python 3.8+ | **If missing:** Install from python.org, check "Add to PATH"

### 2. Create Virtual Environment
```bash
python -m venv venv
```
**What:** Isolated Python environment for project
**Verify:** `venv` folder created (10-30 seconds)

### 3. Activate Virtual Environment
**Windows PowerShell:** `venv\Scripts\Activate.ps1`
**Windows CMD:** `venv\Scripts\activate.bat`
**Mac/Linux:** `source venv/bin/activate`

**Success:** `(venv)` appears in prompt
**Issue (Windows):** `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### 4. Install Flask
```bash
pip install flask
```
**Wait:** 30-60 seconds
**Verify:** "Successfully installed flask-X.X.X"

### 5. Create app.py
Location: Project root (same level as `venv/`)
```
my-project/
├── venv/
└── app.py  ← Create here
```

### 6. Verify Installation
```bash
python --version
pip list
python -c "import flask; print(flask.__version__)"
```

## Troubleshooting
| Issue | Solution |
|-------|----------|
| `python: command not found` | Install Python, add to PATH |
| `pip: command not found` | Activate virtual environment |
| Execution policy error | Run Set-ExecutionPolicy command |
| Permission errors | Ensure venv activated |

## Next Steps
After setup: Create first route, run dev server, build first page.

**Remember:** Keep terminal with `(venv)` open while developing.

---

**End of Skill**
