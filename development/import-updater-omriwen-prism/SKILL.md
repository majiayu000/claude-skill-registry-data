---
name: import-updater
description: Update import statements across the codebase when modules are moved or renamed. This skill should be used after refactoring operations to ensure all imports remain functional and properly organized.
---

# Import Updater

## Overview

Systematically update import statements throughout a codebase when modules are moved, renamed, or reorganized during refactoring.

## When to Use

Use this skill when:
- Modules have been moved to new locations
- Classes or functions have been extracted to different files
- Package structure has changed
- Converting between relative and absolute imports
- Reorganizing import statements for consistency

## Workflow

### Step 1: Identify the Change

Document what moved:
- Old location: `optics.py`
- New location: `prism/core/telescope.py`
- Items moved: `Telescope`, `TelescopeAgg`

### Step 2: Find All Import Usages

Search for all files importing the moved items:

```bash
# Find direct imports
grep -r "from optics import" .
grep -r "import optics" .

# Find specific class imports
grep -r "Telescope" --include="*.py" .
```

Create a list of files that need updating.

### Step 3: Update Each File

For each file found, update imports systematically:

#### Pattern 1: Update import statement
```python
# Old
from optics import Telescope

# New
from prism.core.telescope import Telescope
```

#### Pattern 2: Update with alias
```python
# Old
import optics

# New
from prism.core import telescope
```

#### Pattern 3: Multiple imports
```python
# Old
from optics import Telescope, TelescopeAgg, Grid

# New
from prism.core.telescope import Telescope, TelescopeAgg
from prism.core.grid import Grid
```

### Step 4: Handle Relative Imports

Within same package, use relative imports:

```python
# In prism/core/aggregator.py importing from prism/core/telescope.py
from .telescope import Telescope  # Preferred

# Cross-package imports use absolute
from prism.models.networks import ProgressiveDecoder
```

### Step 5: Organize Imports

Follow standard Python import organization:

```python
# Standard library imports
import os
import sys
from pathlib import Path

# Third-party imports
import torch
import numpy as np
from torch import nn

# Local application imports
from .telescope import Telescope
from ..models.networks import ProgressiveDecoder
```

### Step 6: Remove Unused Imports

After updating, check for unused imports:
- Imports that are no longer needed
- Duplicate imports
- Imports that can be consolidated

### Step 7: Verify Functionality

Test that updates work:
```bash
# Check syntax
python -m py_compile file.py

# Run tests if available
pytest tests/

# Try importing manually
python -c "from prism.core.telescope import Telescope"
```

## Import Patterns

### Absolute vs Relative

**Use absolute imports** when:
- Importing from different packages
- In scripts or main files
- When import path is short and clear

**Use relative imports** when:
- Within the same package
- Refactoring might change package name
- Avoiding repetition of package name

### TYPE_CHECKING Pattern

Avoid circular imports with type hints:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .telescope import Telescope

def process_telescope(tel: 'Telescope') -> None:
    # String annotation avoids runtime import
    pass
```

## Validation Checklist

After updating imports:
- [ ] All files compile without import errors
- [ ] No circular import warnings
- [ ] Imports follow project conventions
- [ ] Unused imports removed
- [ ] Import organization consistent (isort style)
- [ ] Tests pass
- [ ] No "module not found" errors
