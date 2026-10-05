---
name: python-cleanup
description: Remove dead code, fix PEP 8 violations, add type hints, consolidate duplicates, and modernize Python codebases. Use when cleaning up Python projects.
---

# Python Code Cleanup

Systematically identify and remove dead code, consolidate duplicate logic, and modernize legacy Python patterns to maintain a lean, current, and maintainable codebase.

## When to Use This Skill

Use this skill when you need to:

- Remove unused imports and dead code
- Fix PEP 8 style violations
- Add type hints to functions
- Consolidate duplicate code
- Modernize legacy Python (2→3)
- Clean up before code review

**Trigger phrases**: "cleanup Python", "remove dead code", "fix PEP 8", "add type hints", "Python modernization", "refactor Python"

## What This Skill Does

### Cleanup Areas

1. **Dead Code Removal**
   - Unused imports
   - Unreachable code
   - Unused variables/functions
   - Commented-out code

2. **Empty Line Cleanup**
   - Remove blank lines inside function/method bodies
   - Comments should directly precede their code (no blank line before comment)
   - KEEP: 1 blank line between functions, 2 blank lines between classes
   - KEEP: Blank lines around section headers (`# ----------- #`)

3. **Style Compliance**
   - PEP 8 formatting
   - Naming conventions
   - Line length
   - Import organization

4. **Type Annotations**
   - Function signatures
   - Variable annotations
   - Return types

5. **Modernization**
   - f-strings over .format()
   - pathlib over os.path
   - dataclasses
   - walrus operator

## Instructions

### Step 1: Run Analysis Tools

```bash
# Install tools
pip install ruff black mypy isort autoflake

# Find dead code
autoflake --check -r src/

# Check style
ruff check .
black --check .

# Check types
mypy src/

# Check import sorting
isort --check-only .
```

### Step 2: Remove Dead Code

```bash
# Remove unused imports and variables
autoflake --in-place --remove-all-unused-imports --remove-unused-variables -r src/

# Or with ruff
ruff check --fix .
```

### Step 3: Fix Style Issues

```bash
# Format code
black .

# Sort imports
isort .

# Fix remaining issues
ruff check --fix .
```

### Step 4: Remove Empty Lines Within Functions

Remove unnecessary blank lines inside function bodies. Comments should directly precede their code.

```python
# Before - Too many blank lines
def process_data(signals, config):
    """Process signals with config."""
    # Normalize signals
    normalized = normalize(signals)
    scaled = scale(normalized)

    # Apply transformation
    result = transform(scaled, config)

    # Format output
    output = format_output(result)

    return output

# After - Compact style (preferred)
def process_data(signals, config):
    """Process signals with config."""
    # Normalize signals
    normalized = normalize(signals)
    scaled = scale(normalized)
    # Apply transformation
    result = transform(scaled, config)
    # Format output
    output = format_output(result)
    return output
```

**Keep blank lines:**
- Between functions (1 blank line)
- Between classes (2 blank lines)
- Around section headers (`# ----------- #`)

### Step 5: Add Type Hints

```python
# Before
def calculate_total(items, tax_rate):
    total = sum(item['price'] for item in items)
    return total * (1 + tax_rate)

# After
from typing import List, Dict

def calculate_total(items: List[Dict[str, float]], tax_rate: float) -> float:
    total = sum(item['price'] for item in items)
    return total * (1 + tax_rate)
```

### Step 6: Modernize Patterns

```python
# String formatting: .format() → f-string
# Before
message = "Hello, {}!".format(name)
# After
message = f"Hello, {name}!"

# Path handling: os.path → pathlib
# Before
import os
path = os.path.join(base, "file.txt")
# After
from pathlib import Path
path = Path(base) / "file.txt"

# Data classes
# Before
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
# After
from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str
```

## Common Cleanup Targets

| Pattern | Before | After |
|---------|--------|-------|
| String format | `"{}".format(x)` | `f"{x}"` |
| Dict access | `d.get('key', None)` | `d.get('key')` |
| List comprehension | `list(map(f, l))` | `[f(x) for x in l]` |
| Context manager | manual open/close | `with open()` |
| Type checking | `type(x) == str` | `isinstance(x, str)` |

## Tools

- **ruff**: Fast linter, replaces flake8/isort/pyupgrade
- **black**: Opinionated formatter
- **mypy**: Static type checker
- **autoflake**: Remove unused imports
- **isort**: Import sorting

## Quality Checklist

- [ ] Unused imports removed
- [ ] Unused variables removed
- [ ] Empty lines within functions removed
- [ ] PEP 8 compliance verified
- [ ] Type hints added
- [ ] Modern patterns applied
- [ ] Tests still pass
- [ ] No functionality changed

## Related Skills

- `code-review-quality` - Code quality assessment
- `generate-docstrings` - Add documentation

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates code_cleanup/python_cleanup.md


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
