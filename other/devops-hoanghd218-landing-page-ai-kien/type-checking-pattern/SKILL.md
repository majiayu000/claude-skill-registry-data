---
name: type-checking-pattern
description: "Fix F821 undefined name errors for optional dependencies using TYPE_CHECKING"
author: KINTSUGI Team
date: 2025-12-11
---

# TYPE_CHECKING Pattern for Optional Dependencies

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-12-11 |
| **Goal** | Fix ruff F821 "undefined name" errors for type hints using optional dependencies |
| **Environment** | Python 3.10+, ruff linter |
| **Status** | Success |

## Context

When using type hints for optional dependencies (like `dask`, `cupy`, `pandas`), ruff reports F821 "undefined name" errors because the import doesn't exist at the module level. You can't just import these at the top because they're optional and may not be installed.

### Error Signature

```
src/kintsugi/denoise/filters.py:45:21: F821 Undefined name `dask`
src/kintsugi/qc/batch_qc.py:23:35: F821 Undefined name `pd`
src/kintsugi/edf.py:67:18: F821 Undefined name `cp`
```

## Verified Workflow

### Solution: Use `TYPE_CHECKING` with Quoted Annotations

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import dask.array
    import pandas as pd
    import cupy as cp

def process_data(arr: "dask.array.Array") -> "dask.array.Array":
    """Process a dask array."""
    # Actual dask import happens at runtime when needed
    import dask.array as da
    return da.map_blocks(some_func, arr)

def get_metrics() -> "pd.DataFrame":
    """Return metrics as DataFrame."""
    import pandas as pd  # Runtime import
    return pd.DataFrame(...)
```

### Key Components

1. **`from __future__ import annotations`** - Makes all annotations strings by default (PEP 563)

2. **`TYPE_CHECKING` block** - Only runs during static analysis, not at runtime

3. **Quoted type hints** - Use `"dask.array.Array"` instead of `dask.array.Array` for safety

### Real Example from KINTSUGI

**Before (broken):**
```python
import numpy as np
from typing import Union

# F821: Undefined name 'dask'
def denoise_dask(image: dask.array.Array) -> dask.array.Array:
    import dask.array as da
    ...
```

**After (working):**
```python
from __future__ import annotations
from typing import TYPE_CHECKING, Union
import numpy as np

if TYPE_CHECKING:
    import dask.array

def denoise_dask(image: "dask.array.Array") -> "dask.array.Array":
    import dask.array as da
    ...
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Adding `# noqa: F821` to every line | Hides real errors, clutters code | Only use noqa for intentional exceptions |
| Importing at top level unconditionally | Breaks when optional dep not installed | Optional deps must stay optional |
| Using `Any` type instead | Loses type safety, IDE features | TYPE_CHECKING preserves full typing |
| Using string literals without TYPE_CHECKING | Works but IDE can't resolve types | TYPE_CHECKING gives IDE the imports |

## Final Parameters

### Standard Pattern

```python
from __future__ import annotations
from typing import TYPE_CHECKING, Union, Optional

if TYPE_CHECKING:
    import pandas as pd
    import dask.array
    import cupy as cp
    # Add any optional dependency used in type hints

# Now use quoted strings in annotations
def func(data: "pd.DataFrame") -> "pd.DataFrame":
    import pandas as pd  # Runtime import
    ...
```

### For Type Aliases

```python
from __future__ import annotations
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    import cupy as cp
    import numpy as np

# Type alias using quoted strings
ArrayLike = Union["np.ndarray", "cp.ndarray"]
```

## Key Insights

- `from __future__ import annotations` is essential - it defers annotation evaluation
- The `TYPE_CHECKING` block runs during static analysis but not at runtime
- Always use quoted strings for the type hints to be safe across Python versions
- This pattern is the standard way to handle optional dependency type hints
- IDEs like VS Code/PyCharm understand TYPE_CHECKING and provide autocomplete

## Files Modified in KINTSUGI

- `src/kintsugi/qc/batch_qc.py` - pandas types
- `src/kintsugi/qc/cell_qc.py` - pandas types
- `src/kintsugi/qc/image_qc.py` - pandas types
- `src/kintsugi/denoise/filters.py` - dask types
- `src/kintsugi/denoise/care.py` - dask types
- `src/kintsugi/denoise/n2v.py` - dask types
- `src/kintsugi/denoise/patch_based.py` - dask types
- `src/kintsugi/edf.py` - cupy types

## References

- PEP 563 - Postponed Evaluation of Annotations: https://peps.python.org/pep-0563/
- typing.TYPE_CHECKING: https://docs.python.org/3/library/typing.html#typing.TYPE_CHECKING
- ruff F821 rule: https://docs.astral.sh/ruff/rules/undefined-name/
