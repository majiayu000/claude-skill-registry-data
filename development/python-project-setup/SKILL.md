---
name: python-project-setup
description: Sets up a new Python project with uv, virtual environment, and best practices for Windows 11. Use this when creating a new Python project or helping users set up their Python development environment with modern tooling.
---

## Python Project Setup with uv for Windows 11

When setting up a new Python project, use `uv` for fast, reliable package management. This skill includes helper scripts in the `scripts/` directory.

### 1. Check and Install uv
Use the provided script to check if uv is installed:
```powershell
# Check if uv is installed, install if missing
python scripts/check_uv.py
```

Or manually:
```powershell
# Install uv using pip
pip install uv
```

### 2. Quick Setup with Script
For a complete automated setup:
```powershell
# Run the setup script with project name
.\scripts\setup_project.ps1 -ProjectName "my-new-project"
```

### 3. Manual Setup Steps

#### Create Virtual Environment with uv
```powershell
# uv creates and manages virtual environments automatically
uv venv
```

#### Activate Virtual Environment
```powershell
# PowerShell activation
.\.venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Create pyproject.toml
Use the template script or create manually:
```powershell
# Generate pyproject.toml from template
python scripts/create_pyproject.py --name "your-project-name" --python-version "3.10"
```

Or manually create with this structure:
```toml
[project]
name = "your-project-name"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]
```

#### Install Dependencies with uv
```powershell
# Install project dependencies (much faster than pip)
uv pip install -e ".[dev]"
```

### 4. Project Structure
The scripts will create this structure:
```
project-name/
├── .venv/          # Virtual environment (don't commit)
├── src/            # Source code
│   └── __init__.py
├── tests/          # Test files
│   └── __init__.py
├── .gitignore      # Includes .venv, __pycache__, *.pyc
├── README.md       # Project documentation
└── pyproject.toml  # Modern Python project file
```

### 5. .gitignore Configuration
Always exclude:
```
.venv/
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.ruff_cache/
dist/
build/
*.egg-info/
```

## Helper Scripts Reference

### scripts/check_uv.py
Checks if uv is installed and installs it if missing.

### scripts/setup_project.ps1
Complete project setup automation:
- Creates project directory structure
- Initializes virtual environment with uv
- Generates pyproject.toml
- Creates .gitignore
- Sets up basic README.md

### scripts/create_pyproject.py
Generates a pyproject.toml file with common configurations.

## Why This Matters
- `uv` is 10-100x faster than pip for package installation
- Uses modern `pyproject.toml` instead of legacy `requirements.txt`
- Helper scripts automate repetitive setup tasks
- Ensures consistent setup across all team members
- Prevents common Windows-specific Python issues
- Follows best practices automatically
