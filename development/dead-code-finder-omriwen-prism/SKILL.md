---
name: dead-code-finder
description: Identify and remove unused code, commented blocks, unreachable code, and unused imports. This skill should be used during Phase 1 cleanup tasks to improve codebase maintainability.
---

# Dead Code Finder

Identify and remove dead code including unused functions, commented blocks, unreachable code, and unused imports.

## Purpose

Dead code clutters the codebase, makes it harder to maintain, and can confuse developers. This skill systematically finds and removes code that serves no purpose.

## When to Use

Use this skill during:
- Phase 1 (Cleanup) - removing old commented code
- Before major refactoring - clean slate
- Code reviews - ensure no dead code merged
- After feature removal - cleanup leftovers

## Types of Dead Code

### 1. Commented Code Blocks

```python
# DEAD CODE - Commented out
# def old_function():
#     return 42

# Should be removed - use git history if needed
```

### 2. Unused Imports

```python
# DEAD CODE - Unused imports
import os  # Not used anywhere
import sys  # Not used
from typing import Optional  # Not used

import torch  # ✓ Used

# Remove unused, keep used
```

### 3. Unused Functions

```python
# DEAD CODE - Never called
def unused_function():
    return "nobody calls me"

# Should be removed unless it's part of public API
```

### 4. Unreachable Code

```python
def process(x):
    if x > 0:
        return x * 2
    else:
        return x / 2
    print("This is never reached")  # DEAD CODE after return
```

### 5. Unused Variables

```python
def calculate(a, b):
    result = a + b
    temp = a * b  # DEAD CODE - never used
    return result
```

### 6. Redundant Conditions

```python
# DEAD CODE - condition always True
if True:
    process()

# Just use: process()
```

## Detection Tools

### 1. vulture (Recommended)

```bash
uv add --dev vulture

# Find dead code
vulture prism/

# With confidence threshold
vulture prism/ --min-confidence 80

# Ignore certain patterns
vulture prism/ --ignore-names "test_*,_*"
```

### 2. autoflake (Remove Unused Imports)

```bash
uv add --dev autoflake

# Check for unused imports
autoflake --check --remove-all-unused-imports -r prism/

# Remove unused imports
autoflake --in-place --remove-all-unused-imports -r prism/
```

### 3. pylint (Unreachable Code)

```bash
uv add --dev pylint

# Check for issues including dead code
pylint prism/ --disable=all --enable=unreachable,unused-variable
```

## Systematic Cleanup Process

### Step 1: Find Commented Code

```bash
# Find Python comments (manual review)
grep -rn "^[[:space:]]*#.*def\|^[[:space:]]*#.*class" prism/ --include="*.py"

# Find large commented blocks
grep -rn "^[[:space:]]*# " prism/ --include="*.py" | wc -l
```

Review and remove if:
- Code is old and superseded
- Git history has the information
- No TODO or explanation

Keep if:
- Contains important TODO
- Explains why something is NOT done
- Documents alternative approach considered

### Step 2: Remove Unused Imports

```bash
# Automatically remove
autoflake --in-place --remove-all-unused-imports -r prism/

# Or manually with ruff
ruff check prism/ --select F401 --fix
```

### Step 3: Find Unused Functions

```bash
# Use vulture
vulture prism/ --min-confidence 60

# Review output
# Confidence 100% = definitely unused
# Confidence 60-99% = probably unused (check manually)
```

### Step 4: Check for Unreachable Code

```bash
# Pylint unreachable code
pylint prism/ --disable=all --enable=unreachable
```

## Manual Review Patterns

### Safe to Remove

```python
# Old implementation commented out
# def old_calculate(x):
#     return x + 1

# Debugging code left in
# print("DEBUG:", x)

# Unused helper functions (not in public API)
def _helper_never_called():
    pass
```

### Potentially Keep

```python
# Public API - might be used externally
def public_api_function():
    """Part of public API."""
    pass

# Override/callback - used by framework
def on_epoch_end(self):
    """Called by training framework."""
    pass

# Test fixtures - used by pytest
@pytest.fixture
def sample_data():
    return [1, 2, 3]
```

## PRISM-Specific Cleanup

### Remove Old Algorithm Code

```python
# Old implementation (if superseded by refactored version)
# def old_reconstruct(image, measurement):
#     # Old algorithm
#     pass

# Remove if replaced by updated implementation
```

### Remove Debug Visualization

```python
# Debug code
# import matplotlib.pyplot as plt
# plt.imshow(tensor.cpu().numpy())
# plt.show()

# Remove unless behind debug flag:
if args.debug:
    plt.imshow(tensor.cpu().numpy())
    plt.show()
```

### Remove Unused Physics Functions

```python
# Old Fresnel calculation (if not used)
def calculate_fresnel_number(d, lambda, L):
    return d**2 / (lambda * L)

# Check if called - remove if unused
```

## Cleanup Script

Create a cleanup script:

```bash
#!/bin/bash
# cleanup_dead_code.sh

echo "Removing unused imports..."
autoflake --in-place --remove-all-unused-imports -r prism/

echo "Finding dead code with vulture..."
vulture prism/ --min-confidence 80 > dead_code_report.txt

echo "Checking for unreachable code..."
pylint prism/ --disable=all --enable=unreachable >> dead_code_report.txt

echo "Report saved to dead_code_report.txt"
echo "Review and manually remove identified dead code."
```

## Validation Checklist

After cleanup:
- [ ] All tests still pass
- [ ] No import errors
- [ ] Public API still works
- [ ] Documentation still accurate
- [ ] Git commit shows only dead code removed

## Safe Removal Guidelines

### When to Remove

- Code commented out > 1 month ago
- Imports flagged as unused by autoflake
- Functions with 0% confidence of use (vulture)
- Code after return/raise/break/continue statements
- Variables assigned but never read

### When to Keep

- Public API functions (even if unused internally)
- Test fixtures and helpers
- Framework callbacks (on_*, handle_*, etc.)
- __init__.py imports (for public API)
- Type checking imports under TYPE_CHECKING

### Ask Before Removing

- Code with TODO comments
- Recently added code (< 1 week)
- Code in active development branches
- Functions that might be external API

## Common False Positives

### Vulture False Positives

```python
# Vulture may flag these as unused:

# 1. Overridden methods
class MyModel(nn.Module):
    def forward(self, x):  # vulture: might say unused
        pass

# 2. Properties
@property
def value(self):  # vulture: might say unused
    return self._value

# 3. Magic methods
def __str__(self):  # vulture: might say unused
    return "MyClass"

# 4. Pytest fixtures
@pytest.fixture
def data():  # vulture: might say unused (used by pytest)
    return [1, 2, 3]

# Add to whitelist in vulture config
```

Create `.vulture_whitelist.py`:
```python
# Whitelist for known false positives
_.forward  # nn.Module forward
_.backward  # Autograd backward
_.*property  # All properties
```

## Documentation

After cleanup, document what was removed:

```markdown
# Cleanup Summary

## Removed (2024-XX-XX)

- Old deprecated implementation (replaced by refactored version)
- Unused utility functions: `old_helper()`, `deprecated_transform()`
- Commented debugging code (300+ lines)
- 45 unused imports across 20 files

## Impact

- Codebase reduced by 15%
- All tests pass
- No functionality lost
```
