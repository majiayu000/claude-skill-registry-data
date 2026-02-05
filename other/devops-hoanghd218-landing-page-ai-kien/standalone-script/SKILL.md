---
name: standalone-script
description: Generate standalone Python scripts (not packaged projects) with PEP 723 inline metadata, a uv run shebang, and Typer CLI scaffolding. Use when the user wants a one-off executable script, automation tool, or runnable file that should declare dependencies inline and not live inside a package or project.
---

# Standalone Script

## Overview

Create a single-file Python script that runs via `uv run --script`, declares dependencies in a PEP 723 block, and uses Typer for a future-proof CLI.

## Workflow

1. Gather requirements: script purpose, inputs/outputs, dependencies, and any file paths.
2. Start from `assets/pep723_typer_script.py` and copy it into the target script.
3. Update the PEP 723 block:
   - Keep `requires-python = ">=3.13"` as the default.
   - List all dependencies, always include `typer`.
4. Implement the logic inside the Typer command(s) and keep it single-file.
5. Ensure the shebang is the very first line: `#!/usr/bin/env -S uv run --script`.
6. Update the Typer command help string to describe what the script does.
7. Mark the script executable after writing it (e.g., `chmod +x <script>`).
8. Provide run instructions (`uv run --script script.py`).

## Requirements

- Always use Typer even if no arguments are currently needed.
- Do not create a package layout or pyproject; keep everything in one script.
- Keep the file ASCII unless the user explicitly needs Unicode.
- Prefer small helper functions over complex classes unless necessary.

## Assets

Use `assets/pep723_typer_script.py` as the starting template for new scripts.
