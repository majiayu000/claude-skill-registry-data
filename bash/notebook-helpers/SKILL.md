---
name: notebook-helpers
description: Reference for notebook manipulation scripts (notebook_helpers.py, notebook_tools.py). Use when working with Jupyter notebooks, analyzing structure, executing cells, or manipulating notebook content.
---

# Notebook Helper Scripts Reference

## notebook_helpers.py - Low-level notebook manipulation

### Python API

```python
from scripts.notebook_helpers import NotebookHelper, CellIterator, NotebookExecutor

# Read and analyze
helper = NotebookHelper("path/to/notebook.ipynb")
helper.list_cells()                          # List all cells with type, preview
helper.get_cell_source(5)                    # Source code of cell 5
helper.set_cell_source(5, "new code")        # Modify cell content
helper.find_cells_with_pattern("import")     # Search by regex
helper.find_cells_with_errors()              # Cells with error outputs
helper.find_consecutive_code_cells()         # Code cells without markdown between
helper.save()                                # Save modifications

# Iterative correction
iterator = CellIterator(
    notebook_path="notebook.ipynb",
    cell_index=5,
    objective="Output should contain 'SUCCESS'",
    max_iterations=5
)
```

### CLI Usage

```bash
# List cells (verbose shows source preview)
python scripts/notebook_tools/notebook_helpers.py list notebook.ipynb --verbose

# Execute a specific cell
python scripts/notebook_tools/notebook_helpers.py execute notebook.ipynb --cell 5 --timeout 60

# Execute entire notebook cell-by-cell
python scripts/notebook_tools/notebook_helpers.py execute notebook.ipynb --verbose

# Detect kernel type
python scripts/notebook_tools/notebook_helpers.py detect-kernel notebook.ipynb

# Get cell source or output
python scripts/notebook_tools/notebook_helpers.py get-source notebook.ipynb 5
python scripts/notebook_tools/notebook_helpers.py get-output notebook.ipynb 5
```

## notebook_tools.py - High-level CLI

```bash
# Validate structure (quick) or full (with execution)
python scripts/notebook_tools/notebook_tools.py validate Sudoku --quick
python scripts/notebook_tools/notebook_tools.py validate MyIA.AI.Notebooks/Sudoku/Sudoku-01-Backtracking-Python.ipynb

# Extract skeleton for README generation
python scripts/notebook_tools/notebook_tools.py skeleton MyIA.AI.Notebooks/Tweety --output markdown

# Analyze notebook structure
python scripts/notebook_tools/notebook_tools.py analyze MyIA.AI.Notebooks/SymbolicAI

# Check environment requirements
python scripts/notebook_tools/notebook_tools.py check-env Lean

# Execute notebook
python scripts/notebook_tools/notebook_tools.py execute GameTheory --timeout 120 --cell-by-cell
```

## extract_notebook_skeleton.py

```bash
# Quick summary
python scripts/notebook_tools/extract_notebook_skeleton.py MyIA.AI.Notebooks/Sudoku

# Markdown table for README
python scripts/notebook_tools/extract_notebook_skeleton.py MyIA.AI.Notebooks/Sudoku --output markdown

# Detailed with code previews
python scripts/notebook_tools/extract_notebook_skeleton.py MyIA.AI.Notebooks/Sudoku --output detailed --code-preview

# JSON for programmatic use
python scripts/notebook_tools/extract_notebook_skeleton.py MyIA.AI.Notebooks/Sudoku --output json
```

## GenAI-specific scripts (scripts/genai-stack/)

| Script | Description |
|--------|-------------|
| `validate_stack.py` | Full ComfyUI stack validation |
| `validate_notebooks.py` | Papermill execution of GenAI notebooks |
| `check_vram.py` | GPU/VRAM availability check |
| `list_models.py` | List available ComfyUI models |
| `list_nodes.py` | List ComfyUI nodes |
| `docker_manager.py` | Docker service management |

## Key Patterns

- **Always use these scripts** rather than ad-hoc Python for notebook manipulation
- `notebook_helpers.py list` is the fastest way to understand a notebook's structure
- `notebook_tools.py validate --quick` for rapid structural validation
- For GenAI notebooks, always run `validate_stack.py` first
