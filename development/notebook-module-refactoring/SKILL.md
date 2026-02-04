---
name: notebook-module-refactoring
description: "Safe refactoring of Jupyter notebook code into Python modules"
author: Claude Code
date: 2025-12-27
---

# Notebook-to-Module Refactoring

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-12-27 |
| **Goal** | Extract long functions from notebook cells into reusable Python modules |
| **Environment** | KINTSUGI Jupyter notebooks, Python modules in notebooks/ directory |
| **Status** | Success (after fixing) |

## Context
When notebook cells contain both:
1. **Function definitions** (candidates for extraction)
2. **Variable definitions** (processing parameters, configuration)

Extracting only the functions to a module leaves the variables undefined, breaking downstream cells.

## Verified Workflow

### CORRECT: Preserve Variable Definitions
When refactoring a cell that contains both functions and variables:

```python
# BEFORE (single notebook cell):
# =============================================================================
# PROCESSING PARAMETERS
# =============================================================================
n_rows = 13
n_cols = 9
start_cycle = 1
end_cycle = 9
n_workers = CPU_COUNT

# =============================================================================
# CHANNEL NAME FUNCTIONS (to be extracted)
# =============================================================================
def load_channel_names(meta_dir):
    ...

def make_channel_names_unique(channel_dict):
    ...

# Usage
channel_name_dict = load_channel_names(meta_dir)
rows = list(...)  # Uses n_rows, n_cols
```

```python
# AFTER (two notebook cells + module):

# --- Cell 1: Processing Parameters (KEEP IN NOTEBOOK) ---
n_rows = 13
n_cols = 9
start_cycle = 1
end_cycle = 9
n_workers = CPU_COUNT

# --- Cell 2: Module Import + Usage ---
from Kio import load_channel_names, make_channel_names_unique

channel_name_dict = load_channel_names(meta_dir)
rows = list(...)  # Still works - variables defined in Cell 1

# --- Kio.py module (NEW FILE) ---
def load_channel_names(meta_dir):
    ...
def make_channel_names_unique(channel_dict):
    ...
```

### Checklist Before Refactoring
1. [ ] Identify ALL variable definitions in the cell
2. [ ] Identify ALL function definitions to extract
3. [ ] Check what the remaining code (after function removal) depends on
4. [ ] Create module with ONLY the functions
5. [ ] Keep variable definitions in notebook cell
6. [ ] Add import statement to notebook
7. [ ] Test that all downstream cells still work

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Moved entire cell content to module | Variables like `n_workers`, `n_rows` became undefined | Only move function definitions, keep variables |
| Replaced cell with just import | Lost 26 variable definitions | Cell content besides functions must be preserved |
| Edited project folder directly | Changes overwritten on sync | Always edit main repo first (repo-project-sync-workflow) |

## Variables Commonly Left Behind

When extracting channel name functions, these variables were accidentally removed:

| Category | Variables |
|----------|-----------|
| Grid config | `n_rows`, `n_cols`, `rows`, `cols` |
| Processing range | `start_cycle`, `end_cycle`, `start_channel`, `end_channel`, `n_zplanes` |
| HPC settings | `n_workers`, `CPU_COUNT`, `IO_WORKERS`, `ZPLANES_PER_GPU`, `max_cores` |
| Stitching | `pou`, `overlap_percentage`, `initial_ncc_threshold` |
| BaSiC params | `BASIC_IF_DARKFIELD`, `BASIC_MAX_ITERATIONS`, etc. |
| Blend mode | `BLEND_MODE`, `BLEND_SIGMA` |

## Key Insights
- Notebook cells often mix configuration and implementation
- Function extraction should be surgical - only the `def` blocks
- Variable definitions are cell-level configuration, not module content
- Always verify imports work by running the refactored cells
- Use `/advise` before refactoring to check for related skills

## Related Skills
- `repo-project-sync-workflow` - Edit main repo first, then sync
- `channel-name-parsing` - The functions that were extracted

## References
- KINTSUGI `notebooks/Kio.py` - Channel name I/O module
- KINTSUGI `notebooks/2_Cycle_Processing.ipynb` - Cell 7 refactoring
