---
name: python-style
description: Python coding conventions and best practices. Use when writing, reviewing, or refactoring Python code, or when working with Python scripts and projects.
---

# Python Style

Personal coding conventions for writing Python code.

## Dependency Management

### Running Scripts with Dependencies

Use `uv run` to execute Python scripts with temporary dependencies without modifying the environment:

```bash
uv run --with DEPENDENCY==VERSION script.py
```

**Examples:**

```bash
# Run a script with a specific version of requests
uv run --with requests==2.31.0 fetch_data.py

# Run with multiple dependencies
uv run --with requests==2.31.0 --with pandas==2.1.0 analyze.py
```

**Benefits:**
- No need to create virtual environments for quick scripts
- Dependencies are isolated and don't affect the system Python
- Version pinning ensures reproducibility
