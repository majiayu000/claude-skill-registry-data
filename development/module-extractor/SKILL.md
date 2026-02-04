---
name: module-extractor
description: Extract classes, functions, or code blocks from large modules into separate files. This skill should be used during refactoring to break up monolithic files while maintaining import compatibility and test coverage.
---

# Module Extractor

Safely extract code from large modules into smaller, focused files while preserving imports, tests, and backwards compatibility.

## Purpose

Large Python modules become difficult to maintain, test, and understand. This skill provides a systematic approach to extracting components into separate modules while:
- Maintaining all existing imports (backwards compatibility)
- Updating internal references
- Preserving test coverage
- Following PRISM project conventions

## When to Use

Use this skill when:
- A module exceeds ~500 lines
- Multiple unrelated responsibilities exist in one file
- You want to improve testability by isolating components
- Following REFACTORING_DESIGN_DOCUMENT.md extraction tasks
- Creating new submodules from existing code

## Extraction Workflow

### Step 1: Analyze the Source Module

Before extracting, understand what you're working with:

```python
# Read the module and identify:
# 1. Classes/functions to extract
# 2. Internal dependencies (what they use from the same module)
# 3. External dependencies (imports from other modules)
# 4. Dependents (what uses the code to extract)

# Example analysis for prism/core/telescope.py
# Target: Extract TelescopeConfig class

# Internal deps: Uses Grid from same module
# External deps: torch, dataclasses
# Dependents: Telescope class, tests/test_telescope.py
```

### Step 2: Create the New Module

Create the destination file with proper structure:

```python
# prism/core/telescope_config.py
"""Telescope configuration dataclass.

This module was extracted from prism/core/telescope.py.
"""
from __future__ import annotations

# Standard library
from dataclasses import dataclass, field
from typing import Optional

# Third-party
import torch

# Local imports (if any internal deps)
# from .grid import Grid  # If Grid was also extracted

@dataclass
class TelescopeConfig:
    """Configuration for telescope simulation.

    Parameters
    ----------
    n_pixels : int
        Number of pixels in aperture grid
    aperture_radius_pixels : float
        Aperture radius in pixels
    ...
    """
    n_pixels: int = 512
    aperture_radius_pixels: float = 25.0
    # ... rest of class
```

### Step 3: Update the Source Module

Modify the original module to re-export the extracted component:

```python
# prism/core/telescope.py (AFTER extraction)
"""Telescope simulation for PRISM.

Note: TelescopeConfig has been moved to telescope_config.py
but is re-exported here for backwards compatibility.
"""
from __future__ import annotations

# Re-export for backwards compatibility
from .telescope_config import TelescopeConfig

# ... rest of module continues to use TelescopeConfig normally
```

### Step 4: Update Package __init__.py

Ensure the new module is accessible:

```python
# prism/core/__init__.py
from .telescope import Telescope, TelescopeConfig  # TelescopeConfig still works
from .telescope_config import TelescopeConfig as TelescopeConfig  # Also direct import

# Explicit __all__ for documentation
__all__ = [
    "Telescope",
    "TelescopeConfig",
    # ...
]
```

### Step 5: Update Internal References

Find and update any direct imports within the codebase:

```bash
# Find all imports of the extracted component
grep -r "from.*telescope.*import.*TelescopeConfig" prism/
grep -r "from prism.core.telescope import" prism/
```

Update if needed (though re-exports should handle most cases):

```python
# If a module imported directly, it still works:
from prism.core.telescope import TelescopeConfig  # Still works (re-export)

# Or use new location:
from prism.core.telescope_config import TelescopeConfig  # Direct import
```

### Step 6: Update Tests

Ensure tests still pass and update imports if needed:

```python
# tests/unit/test_telescope.py
# Both import styles should work:
from prism.core.telescope import TelescopeConfig  # Via re-export
from prism.core.telescope_config import TelescopeConfig  # Direct

def test_telescope_config_defaults():
    """Test TelescopeConfig default values."""
    config = TelescopeConfig()
    assert config.n_pixels == 512
    assert config.aperture_radius_pixels == 25.0
```

### Step 7: Run Validation

```bash
# 1. Type check the affected modules
uv run mypy prism/core/telescope.py prism/core/telescope_config.py

# 2. Run related tests
uv run pytest tests/unit/test_telescope.py -v

# 3. Check for import errors
uv run python -c "from prism.core.telescope import TelescopeConfig; print('OK')"
uv run python -c "from prism.core.telescope_config import TelescopeConfig; print('OK')"

# 4. Run full test suite
uv run pytest tests/ -v
```

## Import Management Guidelines

### Backwards Compatibility Pattern

Always re-export extracted components from the original location:

```python
# GOOD: Maintains backwards compatibility
# original_module.py
from .new_module import ExtractedClass

# Any code using `from original_module import ExtractedClass` still works
```

### Import Order (PRISM Convention)

Follow this import order in new modules:

```python
"""Module docstring."""
from __future__ import annotations

# Standard library
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

# Third-party
import numpy as np
import torch
from torch import Tensor

# Local imports (prism package)
from prism.config.constants import nm, um
from prism.utils.transforms import fft, ifft

# Relative imports (same package)
from .grid import Grid
from .propagator import Propagator
```

### Circular Import Prevention

When extracting, watch for circular imports:

```python
# PROBLEM: Circular import
# module_a.py imports ClassB from module_b.py
# module_b.py imports ClassA from module_a.py

# SOLUTION 1: Move shared code to third module
# shared.py contains common dependencies
# Both module_a and module_b import from shared

# SOLUTION 2: Use TYPE_CHECKING for type hints only
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .module_b import ClassB  # Only for type hints

def function(b: "ClassB") -> None:  # String annotation
    pass
```

### Type Hint Imports

Use TYPE_CHECKING for expensive imports needed only for hints:

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # These imports only happen during type checking
    from torch import Tensor
    from .heavy_module import HeavyClass

def function(tensor: Tensor, obj: HeavyClass) -> None:
    # At runtime, annotations are strings (due to __future__.annotations)
    pass
```

## Common Extraction Patterns

### Pattern 1: Extract Config Dataclass

Most common extraction - configuration classes:

```
BEFORE:
  telescope.py (600 lines)
    - TelescopeConfig (50 lines)
    - Telescope (550 lines)

AFTER:
  telescope_config.py (60 lines)
    - TelescopeConfig
  telescope.py (560 lines)
    - from .telescope_config import TelescopeConfig (re-export)
    - Telescope
```

### Pattern 2: Extract Base Class

Extract abstract base for multiple implementations:

```
BEFORE:
  trainers.py (800 lines)
    - AbstractTrainer (abstract, 100 lines)
    - ProgressiveTrainer (350 lines)
    - EpochalTrainer (350 lines)

AFTER:
  trainers/
    __init__.py (re-exports all)
    base.py (110 lines)
      - AbstractTrainer
    progressive.py (360 lines)
      - ProgressiveTrainer
    epochal.py (360 lines)
      - EpochalTrainer
```

### Pattern 3: Extract Utility Functions

Move helper functions to utils:

```
BEFORE:
  measurement_system.py (500 lines)
    - MeasurementSystem class
    - _compute_overlap() helper
    - _validate_centers() helper
    - _normalize_masks() helper

AFTER:
  measurement_system.py (400 lines)
    - MeasurementSystem class
    - from .measurement_utils import compute_overlap, validate_centers, normalize_masks
  measurement_utils.py (120 lines)
    - compute_overlap()
    - validate_centers()
    - normalize_masks()
```

### Pattern 4: Extract Constants/Enums

Move constants and enumerations:

```
BEFORE:
  optics.py (700 lines)
    - PropagationMethod enum
    - DEFAULT_WAVELENGTH constant
    - SUPPORTED_REGIMES dict
    - ... optical classes

AFTER:
  optics_constants.py (50 lines)
    - PropagationMethod
    - DEFAULT_WAVELENGTH
    - SUPPORTED_REGIMES
  optics.py (660 lines)
    - from .optics_constants import PropagationMethod, DEFAULT_WAVELENGTH
    - ... optical classes
```

## Extraction Checklist

Before starting:
- [ ] Identify component(s) to extract
- [ ] Map internal and external dependencies
- [ ] Check for circular import risks
- [ ] Review test coverage of target code

During extraction:
- [ ] Create new module with proper docstring
- [ ] Add `from __future__ import annotations`
- [ ] Copy imports (only what's needed)
- [ ] Copy code with original docstrings
- [ ] Add re-export in source module
- [ ] Update `__init__.py` if needed

After extraction:
- [ ] Run mypy on both modules
- [ ] Run related tests
- [ ] Check import from both locations works
- [ ] Run full test suite
- [ ] Update any direct imports in codebase

## Related Skills

- **import-updater**: Update imports across codebase after extraction
- **dead-code-finder**: Find unused code before extraction
- **unit-test-generator**: Generate tests for extracted modules
- **architecture-reviewer**: Verify extracted code follows patterns

## Example: Full Extraction Workflow

Extracting `ExperimentConfig` from `prism/config/experiment.py`:

```bash
# 1. Analyze
grep -n "class ExperimentConfig" prism/config/experiment.py
grep -r "ExperimentConfig" prism/ tests/

# 2. Create new file
# prism/config/experiment_config.py with ExperimentConfig class

# 3. Update source
# Add: from .experiment_config import ExperimentConfig

# 4. Update __init__.py
# Verify: from .experiment import ExperimentConfig works

# 5. Validate
uv run mypy prism/config/experiment.py prism/config/experiment_config.py
uv run pytest tests/unit/test_config.py -v
uv run python -c "from prism.config import ExperimentConfig; print('OK')"
```
