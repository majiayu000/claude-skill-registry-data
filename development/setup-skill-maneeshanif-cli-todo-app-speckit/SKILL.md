---
name: setup-skill
description: Initialize Python project structure with proper directory layout, configuration files, and best practices. Use when creating new projects or restructuring existing ones.
allowed-tools: Bash, Write, Read, Glob
---

# Setup Skill

## Purpose
Create and configure Python project structures following modern best practices.

## Instructions

1. **Create Directory Structure**
   ```bash
   mkdir -p src/package_name/{models,database,services,ui,utils}
   mkdir -p tests
   touch src/package_name/__init__.py
   touch src/package_name/main.py
   ```

2. **Create pyproject.toml**
   ```toml
   [project]
   name = "project-name"
   version = "0.1.0"
   description = "Project description"
   requires-python = ">=3.11"
   dependencies = []
   
   [project.scripts]
   app = "package_name.main:app"
   
   [build-system]
   requires = ["hatchling"]
   build-backend = "hatchling.build"
   ```

3. **Create .gitignore**
   ```
   __pycache__/
   *.py[cod]
   .venv/
   .env
   *.json
   !package.json
   .pytest_cache/
   .coverage
   htmlcov/
   dist/
   build/
   *.egg-info/
   ```

4. **Create README.md**
   ```markdown
   # Project Name
   
   ## Installation
   ```bash
   uv sync
   ```
   
   ## Usage
   ```bash
   uv run app
   ```
   ```

## Examples

### Create a new todo app structure
```bash
mkdir -p retro_todo/{models,database,services,ui,utils}
mkdir -p tests
touch retro_todo/__init__.py
touch retro_todo/main.py
```

## Best Practices

- Use `src` layout for packages that will be distributed
- Keep flat layout for internal tools
- Always include `__init__.py` files
- Create separate directories for different concerns
- Include proper configuration files from start
