---
name: setup-django
description: Sets up a new Django project with RAPID architecture using uv. Creates horizontal layer structure with DRF, Docker/PostgreSQL support, and environment-based configuration. Use when the user wants to initialise a Django web application.
user-invocable: true
allowed-tools: Bash, Write, AskUserQuestion
---

# Setting Up a Django Project with RAPID Architecture

## Overview

This skill scaffolds a Django project using the RAPID horizontal layer architecture:
- **R**eaders - Read-only business logic
- **A**ctions - State-changing business logic
- **P**resentation (Interfaces) - HTTP endpoints, management commands, templates
- **I**nformation (Data) - Models and migrations
- **D**omain - The project configuration

The project structure is generated using a cookiecutter template bundled with this skill.

## Workflow

### Step 1: Verify Prerequisites

Ensure required tools are installed:

```bash
command -v uv >/dev/null || echo "uv not found - please install it first"
command -v docker >/dev/null || echo "docker not found - please install it first"
command -v cookiecutter >/dev/null || pipx install cookiecutter
```

### Step 2: Gather Project Details

Ask the user for:
1. **Project name** - defaults to current directory name
2. **Python version** - default to 3.12 if not specified
3. **Project description** (optional) - for pyproject.toml and README

### Step 3: Generate Project from Template

Get the skill's template directory path and run cookiecutter:

```bash
PROJECT_NAME=$(basename "$(pwd)")
SKILL_DIR="$HOME/.claude/skills/setup-django"

cookiecutter "$SKILL_DIR/template" \
    --no-input \
    --output-dir "$(dirname "$(pwd)")" \
    project_name="$PROJECT_NAME" \
    python_version="<version>" \
    description="<description>"
```

Note: cookiecutter creates a new directory, so we output to parent and it creates the project directory. If the current directory already exists and is empty, move the generated contents into it.

Alternative approach if current directory exists:

```bash
TEMP_DIR=$(mktemp -d)
cookiecutter "$SKILL_DIR/template" \
    --no-input \
    --output-dir "$TEMP_DIR" \
    project_name="$PROJECT_NAME" \
    python_version="<version>" \
    description="<description>"
cp -r "$TEMP_DIR/$PROJECT_NAME"/. .
rm -rf "$TEMP_DIR"
```

### Step 4: Install Dependencies

```bash
uv sync
```

This installs all dependencies defined in the generated pyproject.toml.

### Step 5: Make manage.py Executable

```bash
chmod +x manage.py
```

### Step 6: Git Repository Setup

**First, discover available GitHub organisations:**

```bash
gh org list
```

Then ask the user using AskUserQuestion with these options:

1. **No remote** - Keep it local only
2. **Public repository (personal)** - Create public repo in personal account
3. **Private repository (personal)** - Create private repo in personal account
4. **Organisation repository** - Show list of orgs from `gh org list` and let user pick, then ask public/private

**Creating the repository:**

For personal repos:
```bash
gh repo create <repo-name> --public|--private --source . --push
```

For organisation repos:
```bash
gh repo create <org-name>/<repo-name> --public|--private --source . --push
```

If no remote wanted:
```bash
git init
git add .
git commit -m "Initial commit: scaffold Django project with RAPID architecture"
```

### Step 7: Verify Setup

Start PostgreSQL and run migrations:

```bash
docker compose up -d db
sleep 3  # Wait for PostgreSQL to be ready
uv run python manage.py migrate
```

Verify the development server starts:

```bash
uv run python manage.py runserver &
sleep 3
curl -s http://localhost:8000/api/health/ | grep -q '"status":"ok"' && echo "Health check passed" || echo "Health check failed"
kill %1 2>/dev/null
```

Run tests:

```bash
uv run pytest
```

## Template Structure

The cookiecutter template creates this RAPID structure:

```
<project>/
├── <package>/
│   ├── __init__.py
│   ├── settings.py          # Django settings with env var support
│   ├── urls.py               # Root URL configuration
│   ├── wsgi.py
│   ├── asgi.py
│   ├── data/                 # Data layer
│   │   ├── models/           # Django models
│   │   └── migrations/       # Database migrations
│   ├── readers/              # Read-only business logic
│   ├── actions/              # State-changing business logic
│   └── interfaces/           # External interfaces
│       ├── http/
│       │   ├── api/          # DRF views and URLs
│       │   └── templates/    # HTML templates
│       └── management_commands/
│           └── management/commands/
├── tests/
├── scratch/                  # Gitignored scratch space
├── manage.py
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── justfile
├── README.md
├── CLAUDE.md
└── .gitignore
```

## Checklist

- [ ] Verify prerequisites (uv, docker, cookiecutter)
- [ ] Get project name (default: directory name)
- [ ] Get Python version (default: 3.12)
- [ ] Get optional project description
- [ ] Run cookiecutter with template
- [ ] Run `uv sync` to install dependencies
- [ ] Make manage.py executable
- [ ] Fetch available GitHub orgs with `gh org list`
- [ ] Ask about git remote setup
- [ ] Initialise git and optionally create remote
- [ ] Start PostgreSQL and run migrations
- [ ] Verify development server starts and health check passes
- [ ] Run tests

## Notes

- The template is located at `~/.claude/skills/setup-django/template/`
- PostgreSQL is required - the skill uses Docker to provide it locally
- RAPID architecture keeps business logic separate from Django's MTV pattern
- Readers are for queries, Actions are for mutations
- Use `gh auth status` to check GitHub authentication if needed
