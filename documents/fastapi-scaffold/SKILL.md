---
name: fastapi-scaffold
description: Generate FastAPI project scaffold with uvicorn, OpenAPI docs, and configuration management
allowed-tools: Read, Write, Bash, Glob, AskUserQuestion
---

# FastAPI Project Scaffold Skill

Generate a complete FastAPI project structure with modern Python tooling (uv, FastAPI, uvicorn) following best practices from temoa and apantli projects.

## What This Skill Generates

A production-ready FastAPI project with:

- **FastAPI application** with OpenAPI docs (/docs, /redoc)
- **CLI entry point** with argparse and uvicorn
- **Configuration management** (JSON/YAML, multiple search paths)
- **Version management** via importlib.metadata
- **CORS middleware** for web clients
- **Lifespan management** for startup/shutdown
- **Modern Python tooling** (uv, pyproject.toml)
- **Development tools** (pytest, mypy, ruff)

## Project Structure

```
{PROJECT_NAME}/
├── pyproject.toml
├── config.example.json
├── {PACKAGE_NAME}/
│   ├── __init__.py
│   ├── __version__.py
│   ├── __main__.py
│   ├── server.py
│   └── config.py
├── .gitignore
├── .env.example
└── README.md
```

## Implementation Steps

### Step 1: Gather Parameters

Collect the following information from the user (use AskUserQuestion if needed):

**Required parameters:**

1. **PROJECT_NAME** (string) - Display name (e.g., "Temoa", "Apantli")
   - Used in documentation and API title
   - Example: "MyAPI"

2. **PACKAGE_NAME** (string) - Python package name (e.g., "temoa", "apantli")
   - Must be valid Python identifier (lowercase, underscores only)
   - Usually lowercase version of PROJECT_NAME
   - Example: "myapi"

3. **DESCRIPTION** (string) - One-line project description
   - Used in pyproject.toml and API docs
   - Example: "Lightweight API for data processing"

**Optional parameters (with defaults):**

4. **SERVER_HOST** (string) - Default: "0.0.0.0"
   - Host to bind server to

5. **SERVER_PORT** (integer) - Default: 8000
   - Port to bind server to

6. **PYTHON_VERSION** (string) - Default: ">=3.11"
   - Minimum Python version requirement

7. **VERSION** (string) - Default: "0.1.0"
   - Initial project version

### Step 2: Derive Additional Variables

From the collected parameters, derive:

- **PACKAGE_NAME_UPPER** = PACKAGE_NAME.upper().replace("-", "_")
  - Used for environment variables
  - Example: "myapi" → "MYAPI"

### Step 3: Create Project Directory

Create the project root directory:

```python
Path(PROJECT_NAME).mkdir(exist_ok=True)
```

### Step 4: Create Package Directory

Create the Python package directory:

```python
Path(PROJECT_NAME) / PACKAGE_NAME).mkdir(exist_ok=True)
```

### Step 5: Generate Files from Templates

For each template file in `skills/fastapi-scaffold/templates/`:

1. Read the template file
2. Replace all template variables:
   - `{{PROJECT_NAME}}` → PROJECT_NAME
   - `{{PACKAGE_NAME}}` → PACKAGE_NAME
   - `{{PACKAGE_NAME_UPPER}}` → PACKAGE_NAME_UPPER
   - `{{DESCRIPTION}}` → DESCRIPTION
   - `{{SERVER_HOST}}` → SERVER_HOST
   - `{{SERVER_PORT}}` → SERVER_PORT (as string)
   - `{{PYTHON_VERSION}}` → PYTHON_VERSION
   - `{{VERSION}}` → VERSION
3. Write the result to the target location

**Template mapping:**

| Template | Target Location |
|----------|----------------|
| `__init__.py.template` | `{PROJECT_NAME}/{PACKAGE_NAME}/__init__.py` |
| `__version__.py.template` | `{PROJECT_NAME}/{PACKAGE_NAME}/__version__.py` |
| `server.py.template` | `{PROJECT_NAME}/{PACKAGE_NAME}/server.py` |
| `__main__.py.template` | `{PROJECT_NAME}/{PACKAGE_NAME}/__main__.py` |
| `config.py.template` | `{PROJECT_NAME}/{PACKAGE_NAME}/config.py` |
| `pyproject.toml.template` | `{PROJECT_NAME}/pyproject.toml` |
| `.gitignore.template` | `{PROJECT_NAME}/.gitignore` |
| `.env.example.template` | `{PROJECT_NAME}/.env.example` |
| `config.example.json.template` | `{PROJECT_NAME}/config.example.json` |
| `README.md.template` | `{PROJECT_NAME}/README.md` |

### Step 6: Verify Generated Files

Confirm all files were created successfully:

```bash
ls -la {PROJECT_NAME}/
ls -la {PROJECT_NAME}/{PACKAGE_NAME}/
```

Expected: 10 files total (3 in root, 5 in package, 2 dotfiles)

### Step 7: Initialize Git Repository (Optional)

Ask the user if they want to initialize a git repository:

```bash
cd {PROJECT_NAME}
git init
git add .
git commit -m "Initial commit: FastAPI project scaffold"
```

### Step 8: Setup Development Environment

Guide the user through initial setup:

```bash
cd {PROJECT_NAME}

# Install dependencies
uv sync

# Create config from example
cp config.example.json config.json
```

### Step 9: Verification & Next Steps

Provide verification commands and next steps:

```bash
# Verify installation
uv run {PACKAGE_NAME} --version

# Run development server
uv run {PACKAGE_NAME} --reload

# Open in browser
open http://localhost:{SERVER_PORT}/docs
```

## Template Variable Reference

| Variable | Example | Description |
|----------|---------|-------------|
| `{{PROJECT_NAME}}` | "MyAPI" | Display name for documentation |
| `{{PACKAGE_NAME}}` | "myapi" | Python package name (lowercase) |
| `{{PACKAGE_NAME_UPPER}}` | "MYAPI" | Uppercase for env vars |
| `{{DESCRIPTION}}` | "API for data" | One-line description |
| `{{SERVER_HOST}}` | "0.0.0.0" | Default server host |
| `{{SERVER_PORT}}` | "8000" | Default server port |
| `{{PYTHON_VERSION}}` | ">=3.11" | Python version requirement |
| `{{VERSION}}` | "0.1.0" | Initial project version |

## Example Execution

**User request:** "Create a FastAPI project for my blog API"

**Parameters collected:**
- PROJECT_NAME: "BlogAPI"
- PACKAGE_NAME: "blogapi"
- DESCRIPTION: "RESTful API for blog management"
- SERVER_PORT: 8080
- (others use defaults)

**Derived:**
- PACKAGE_NAME_UPPER: "BLOGAPI"

**Generated structure:**
```
BlogAPI/
├── pyproject.toml
├── config.example.json
├── blogapi/
│   ├── __init__.py
│   ├── __version__.py
│   ├── __main__.py
│   ├── server.py
│   └── config.py
├── .gitignore
├── .env.example
└── README.md
```

**Verification:**
```bash
cd BlogAPI
uv sync
uv run blogapi --version  # → "BlogAPI 0.1.0"
uv run blogapi --reload   # → Server at http://0.0.0.0:8080
```

## Common Issues

### Invalid Package Name

If PACKAGE_NAME contains invalid characters (spaces, hyphens in wrong places), normalize it:

```python
package_name = PROJECT_NAME.lower().replace(" ", "_").replace("-", "_")
```

### Port Already in Use

Suggest the user choose a different port if the default is occupied.

### Missing uv

If uv is not installed, guide the user:

```bash
brew install uv
```

## Post-Generation Customization

After generating the scaffold, users typically:

1. **Edit config.json** with their specific configuration
2. **Add API endpoints** to `server.py`
3. **Add dependencies** to `pyproject.toml` and run `uv sync`
4. **Customize README.md** with project-specific details
5. **Set up launchd service** using `/macos-launchd-service` skill

## Notes

- All templates use `{{VARIABLE}}` syntax for substitution
- Port numbers should be written as integers (no quotes) in templates
- File paths use Path objects for cross-platform compatibility
- Git initialization is optional - ask the user first
