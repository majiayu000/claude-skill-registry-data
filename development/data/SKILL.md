---
name: data
description: Use for running and editing notebooks efficiently via jtool/Jupyter; prefers uv for deps and headless execution.
---

# Data (notebook ops)

## When to use
- You need to run, edit, or execute Jupyter notebooks headlessly.
- You want to use jtool for notebook execution/control when a Jupyter server is available.
- You need a clean way to install deps for notebooks without polluting the system (use uv).

## Notebook execution (prefer jtool if server exists)
- Start a Jupyter server if needed: `uv run jupyter notebook --no-browser --port 8888 --NotebookApp.token=''`.
- Add server once: `jtool add-server http://127.0.0.1:8888`.
- Execute a notebook: `jtool execute-cells path/to/notebook.ipynb --max-output-lines 200`.
- If no server is available, fall back to `uv run ... jupyter nbconvert --execute`.

## Headless execution via uv (no server)
- `uv run --with pandas --with matplotlib --with notebook python -m jupyter nbconvert --to notebook --execute your.ipynb --output your.ipynb --ExecutePreprocessor.timeout=180`
- Use `--with` flags to supply lightweight deps without altering global envs.

## Editing notebooks programmatically
- Generate/patch notebooks with small Python scripts that write JSON (nbformat v4).
- Keep cells compact; prefer clear markdown titles and minimal outputs when shipping.

## Path & env tips
- Default workspace: `~/github/...`.
- Ensure `~/.local/bin` on PATH so `jtool` is discoverable (`export PATH=\"$HOME/.local/bin:$PATH\"`).
