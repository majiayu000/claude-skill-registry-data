---
name: python-environment
description: Python environment setup with uv, shared utilities, and script structure guidelines.
---

# Python Environment

**Always use `uv run`.** Never search for Python or use venv directly.

`uv run` uses the venv from the nearest `pyproject.toml` up the directory tree. Run scripts from the project root:

```bash
cd /path/to/project  # directory with pyproject.toml
uv run python experiments/experiment_X/fit/run_fit.py
```

## Shared Utilities

`shared-utils` is a project dependency. Import directly:

```python
from shared_utils import compile_model, fit_model, check_convergence, ...
```

Read the package source at `/workspace/shared_utils/` for API details.

## Script Structure

Write small, focused scripts - not monolithic files. Separate concerns:

```
experiment_X/
  fit/
    run_fit.py        # Main entry point
    diagnostics.py    # Convergence checks
    plots.py          # Visualization
```

Each script should:
- Do one thing well
- Be runnable independently via `uv run python script.py`
- Import shared logic from `shared_utils`
