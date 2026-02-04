---
name: python-project-init
description: Initialize complete Python project with comprehensive documentation, development environment, and tooling. Use when creating a new Python project from scratch.
allowed-tools: Read, Write, Bash, Glob, AskUserQuestion
---

# Python Project Initialization

Initialize a complete Python project with comprehensive documentation, development environment, and tooling.

## What This Skill Creates

**Documentation:**

- `README.md` - Project overview and vision
- `CLAUDE.md` - Development guide for AI sessions
- `docs/` - Delegates to `/plinth:project-tracking` for session tracking files

**Python Setup:**

- `pyproject.toml` - uv-based dependency management with dev tools
- `.gitignore` - Python-specific gitignore

**Package Structure:**

- `{package_name}/` - Main package directory
- `{package_name}/cli.py` - CLI entry point placeholder
- `tests/` - Test directory

**Workflow:**

- Session continuity (works with `/plinth:session-pickup` and `/plinth:session-wrapup`)
- "Plan like waterfall, implement in agile" approach
- Decision logging with rationale

## Step 1: Gather Project Information

Ask the user for the following (use AskUserQuestion if needed):

**Required:**

1. **PROJECT_NAME** - Display name (e.g., "Temoa", "Apantli")
   - Used in documentation and human-readable contexts
   - Can contain spaces and capital letters

2. **PACKAGE_NAME** - Python package name (e.g., "temoa", "apantli")
   - Must be valid Python identifier (lowercase, underscores only)
   - If not provided, derive from PROJECT_NAME: lowercase, replace spaces/hyphens with underscores

3. **DESCRIPTION** - One-sentence project description
   - What does this project do?
   - Example: "Nahuatl language learning platform with spaced repetition"

**Optional (with defaults):**

4. **PYTHON_VERSION** - Default: ">=3.11"
   - Minimum Python version requirement

5. **VERSION** - Default: "0.1.0"
   - Initial project version

**Derived:**

- **PACKAGE_NAME_UPPER** = PACKAGE_NAME.upper().replace("-", "_")
  - Used for environment variables if needed

## Step 2: Create Directory Structure

Create the project directory and subdirectories:

```bash
mkdir -p {PROJECT_NAME}
mkdir -p {PROJECT_NAME}/{PACKAGE_NAME}
mkdir -p {PROJECT_NAME}/tests
```

## Step 3: Generate Files from Templates

For each template file in `skills/python-project-init/templates/`:

1. Read the template file
2. Replace all template variables:
   - `{{PROJECT_NAME}}` → PROJECT_NAME
   - `{{PACKAGE_NAME}}` → PACKAGE_NAME
   - `{{DESCRIPTION}}` → DESCRIPTION
   - `{{PYTHON_VERSION}}` → PYTHON_VERSION
   - `{{VERSION}}` → VERSION
3. Write the result to the target location

**Template mapping:**

| Template | Target Location |
|----------|----------------|
| `pyproject.toml.template` | `{PROJECT_NAME}/pyproject.toml` |
| `README.md.template` | `{PROJECT_NAME}/README.md` |
| `CLAUDE.md.template` | `{PROJECT_NAME}/CLAUDE.md` |
| `.gitignore.template` | `{PROJECT_NAME}/.gitignore` |

## Step 4: Create Package Files

Create minimal Python package structure:

**{PROJECT_NAME}/{PACKAGE_NAME}/__init__.py**:

```python
"""{{PROJECT_NAME}} - {{DESCRIPTION}}"""

__version__ = "{{VERSION}}"
```

**{PROJECT_NAME}/{PACKAGE_NAME}/cli.py**:

```python
"""Command-line interface for {{PROJECT_NAME}}."""

import argparse
from . import __version__


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog="{{PACKAGE_NAME}}",
        description="{{DESCRIPTION}}",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"{{PROJECT_NAME}} {__version__}",
    )

    args = parser.parse_args()

    # Add your CLI logic here
    print(f"{{PROJECT_NAME}} v{__version__}")
    print("Ready to go!")


if __name__ == "__main__":
    main()
```

**{PROJECT_NAME}/tests/__init__.py**:

```python
"""Test suite for {{PROJECT_NAME}}."""
```

**{PROJECT_NAME}/tests/test_basic.py**:

```python
"""Basic tests for {{PROJECT_NAME}}."""

from {{PACKAGE_NAME}} import __version__


def test_version():
    """Test version is defined."""
    assert __version__ is not None
    assert isinstance(__version__, str)
```

## Step 5: Create Documentation Structure

Invoke the **project-tracking** skill using the Skill tool:

```
Skill tool call:
  skill: "plinth:project-tracking"
  args: "new project, name: {PROJECT_NAME}, phase: Phase 0 - Research & Design, description: {DESCRIPTION}"
```

This delegates documentation setup to project-tracking, which will create:

- `docs/CONTEXT.md` - Current session state
- `docs/IMPLEMENTATION.md` - Phase 0 setup
- `docs/DECISIONS.md` - Decision tracking registry
- `docs/chronicles/phase-0-foundation.md` - Initial entry

## Step 6: Initialize Git Repository (Optional)

Ask the user if they want to initialize a git repository:

```bash
cd {PROJECT_NAME}
git init
git add .
git commit -m "$(cat <<'EOF'
docs: establish project infrastructure and comprehensive documentation

Set up {PROJECT_NAME} with comprehensive documentation following proven
patterns from plinth project templates. Established tech stack and
development workflow.

Documentation Structure:
- README.md: Project overview and vision
- CLAUDE.md: Development guide for AI sessions
- docs/CONTEXT.md: Current session state
- docs/IMPLEMENTATION.md: Phase-based implementation tracking
- docs/DECISIONS.md: Architectural decision registry
- pyproject.toml: Python setup with uv

Project Structure:
- {PACKAGE_NAME}/: Main Python package
- tests/: Test suite with pytest
- Development tools: mypy, ruff, pytest

Current Status: Phase 0 (Research & Design)
Next Step: Define core features and begin implementation planning
EOF
)"
```

## Step 7: Setup Development Environment (Optional)

Ask the user if they want to set up the development environment now:

```bash
cd {PROJECT_NAME}
uv sync
uv run {PACKAGE_NAME} --version
uv run pytest
```

This will:

- Create `.venv/` directory
- Install all dependencies
- Create `uv.lock` file
- Verify CLI works
- Run initial tests

## Step 8: Verification & Next Steps

Provide verification commands and next steps to the user:

**Verification:**

```bash
cd {PROJECT_NAME}

# Verify structure
ls -la
ls -la {PACKAGE_NAME}
ls -la docs

# Verify CLI
uv run {PACKAGE_NAME} --version

# Run tests
uv run pytest
```

**Next Steps:**

1. Edit `README.md` to add vision and feature details
2. Edit `CLAUDE.md` to add project-specific principles
3. Update `docs/IMPLEMENTATION.md` Phase 0 with specific tasks
4. Add dependencies to `pyproject.toml` as needed
5. Begin implementing core features

**Session Management:**

- Use `/plinth:session-pickup` to resume work in next session
- Use `/plinth:session-wrapup` to document progress and commit changes

## Quality Checks

Before finishing, verify:

- [ ] All files created successfully
- [ ] pyproject.toml has correct project name and package name
- [ ] README.md has project name and description
- [ ] CLAUDE.md has project name and description
- [ ] Documentation structure exists (CONTEXT.md, IMPLEMENTATION.md, DECISIONS.md, chronicles/)
- [ ] Package structure exists with __init__.py and cli.py
- [ ] .gitignore created
- [ ] No emojis anywhere
- [ ] Git commit made (if requested)
- [ ] Tests run successfully (if environment set up)

## What NOT to Do

- Don't create code beyond the minimal CLI placeholder
- Don't install dependencies if user didn't request it
- Don't add emojis to any files
- Don't skip the documentation structure
- Don't create an empty project - always include the basics
- Don't assume the package name - ask if unclear

## Handoff to User

After completion, tell the user:

1. What was created (file counts and structure)
2. Current status: Phase 0 - Research & Design
3. Next step: Define core features and update documentation
4. How to continue: Use `/plinth:session-pickup` in next session
5. Quick start: `cd {PROJECT_NAME} && uv sync && uv run {PACKAGE_NAME} --version`

Keep it brief and technical. Focus on what they need to do next.

## Template Variable Reference

| Variable | Example | Description |
|----------|---------|-------------|
| `{{PROJECT_NAME}}` | "Temoa" | Display name for documentation |
| `{{PACKAGE_NAME}}` | "temoa" | Python package name (lowercase) |
| `{{DESCRIPTION}}` | "Language learning platform" | One-line description |
| `{{PYTHON_VERSION}}` | ">=3.11" | Python version requirement |
| `{{VERSION}}` | "0.1.0" | Initial project version |
