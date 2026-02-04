---
name: private-function-shim-export
description: "Fix compatibility shims that fail to export private functions. Trigger when: (1) import errors for _prefixed functions after module reorganization, (2) 'cannot import name' errors from shim files, (3) creating backwards-compat shims for moved modules."
author: Claude Code
date: 2024-12-31
---

# Private Function Export in Compatibility Shims

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-31 |
| **Goal** | Fix import failures for private functions when using compatibility shims |
| **Environment** | Python module reorganization with backwards-compat shims |
| **Status** | Success |

## Context

**Problem**: After reorganizing modules (e.g., moving `broker.py` to `trading/broker.py`), compatibility shims using `from .trading.broker import *` fail to export private functions like `_read_keys_from_file`.

**Root Cause**: Python's `import *` only exports:
1. Names listed in `__all__` (if defined)
2. Names NOT starting with underscore `_` (if `__all__` not defined)

Private functions (starting with `_`) are NEVER exported by `import *`, even if they're used by other modules.

**Symptom**:
```python
# In data/fetcher.py
from ..broker import _read_keys_from_file
# ImportError: cannot import name '_read_keys_from_file' from 'alpaca_trading.broker'
```

## Verified Solution

### The Fix Pattern

When creating a compatibility shim, explicitly import any private functions that other modules depend on:

```python
# alpaca_trading/broker.py (shim)
"""Compatibility shim - broker moved to trading/broker.py"""
from .trading.broker import *  # noqa: F401,F403

# Explicitly export private functions used by other modules
from .trading.broker import _read_keys_from_file  # noqa: F401
from .trading.broker import _parse_config  # noqa: F401  (if needed)
```

### How to Find Missing Private Exports

1. **Search for private function usage**:
```bash
grep -r "from.*broker import _" alpaca_trading/
```

2. **Check import errors in tests**:
```bash
python -m pytest tests/ -v 2>&1 | grep "cannot import name"
```

3. **Test the import directly**:
```python
python -c "from alpaca_trading.broker import _read_keys_from_file; print('OK')"
```

## Failed Attempts

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Only use `import *` | Private functions not exported | Must explicitly import `_prefixed` functions |
| Add to `__all__` in source | Works but pollutes public API | Prefer explicit import in shim |
| Rename private to public | Breaks API contract | Private functions should stay private |

## Checklist for Creating Shims

- [ ] Create shim with `from .new_location import *`
- [ ] Search codebase for `from ..old_location import _`
- [ ] Add explicit imports for each private function found
- [ ] Test imports: `python -c "from module import _func"`
- [ ] Run full test suite to catch any missed imports

## When This Pattern Applies

1. **Module reorganization**: Moving files to subpackages
2. **Archive patterns**: Moving deprecated code to `_archive/`
3. **Package consolidation**: Grouping related modules
4. **Any shim using `import *`**: Always check for private function usage

## Python Import Behavior Reference

```python
# module.py
__all__ = ['public_func']  # If defined, * only exports these

def public_func(): pass
def _private_func(): pass  # NEVER exported by *
def another_public(): pass  # Only exported if in __all__ or no __all__ defined

# Importing module
from module import *  # Gets: public_func (and another_public if no __all__)
                      # Does NOT get: _private_func
```

## Related Skills

- `codebase-consolidation-pattern`: Full module reorganization workflow
- `branch-integration-workflow`: Safe branch merging patterns

## References

- Commit `160ebff`: Fix for broker.py shim
- Python docs: https://docs.python.org/3/tutorial/modules.html#importing-from-a-package
