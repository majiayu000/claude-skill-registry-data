---
name: dev-swarm-python
description: Install and configure Python and uv. Use when setting up a Python environment.
---

# Python Environment Setup (uv)

This skill assists in installing and configuring the Python environment using `uv` for fast package and project management.

## When to Use This Skill

- User needs to set up Python development environment
- User wants to install or configure uv package manager
- User asks to initialize Python project

## Prerequisites

- `curl` (macOS/Linux) or PowerShell (Windows).

## Your Roles in This Skill

- **DevOps Engineer**: Install and configure Python environment using uv. Initialize Python projects with virtual environments. Manage Python versions and dependencies. Verify installations and troubleshoot setup issues. Update project documentation to reflect environment setup.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.
## Instructions

### 1. Check Existing Installation

Before installing, check if `uv` is already installed.

```bash
uv --version
```

If installed, ask the user for confirmation before reinstalling or updating.

### 2. Install uv

**macOS and Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. Initialize Project with uv

To initialize a new project or set up the current directory:

```bash
uv init
```

This will set up a virtual environment and `pyproject.toml`.

### 4. Python Version

`uv` manages Python versions automatically. The default targeted version is typically the latest stable or system default (e.g., Python 3.12).

To pin a specific version:
```bash
uv python pin 3.12
```

### 5. Save User Preferences

After successful installation, save the Python package manager preference to `dev-swarm/user_preferences.md` so future sessions remember to use `uv`.

**Example:**

Create or update `dev-swarm/user_preferences.md` with:

```markdown
## Python Package Manager
- Use **uv** for all Python package operations
- Python version: 3.12+
```
