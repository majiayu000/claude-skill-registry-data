---
name: Initialize New Python Project
description: Setup a new python project in this directory.
---

New python projects must use the following:

- They must use `uv`. Use `uv init --name=<project-name> .`
  - If this is for a cli or other package then use `uv init --name=<project-name> --package .`
- Setup pre-commit hooks using `pre-commit`. The pre-commit hooks should include `ruff` check and formatting, and `ty` type checks.
- All dependencies should be add using `uv add` to ensure the latest versions are used.
- The directory structure should contain the following:
  - `main.py`: initially binary for the project, this should be pretty minimal
  - `pyproject.toml`: configured by the `uv init` tool 
  - `README.md`: a brief description of the project and how to run it
  - `.gitignore`: ignore files that should not be committed to git
  - `.pre-commit-config.yaml`: configuration for pre-commit hooks
  - `<project-name-dir>/`: directory for the project's source code
  - `<project-name-dir>/__init__.py`: empty file to mark the directory as a python package
- If this is being initialized from a design or scope, create a symlink to the design or scope directory, and ensure it is git ignored.
- Always prefer async when possible
  
Common technologies that should be used based on the project:

- For a web server use FastAPI
- Pydantic should be used for data validation and serialization
- Typer should be used for command-line interfaces
- SQLAlchemy should be used for database interactions
