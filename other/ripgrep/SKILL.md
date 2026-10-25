---
name: check-ripgrep-availability
description: >
  This skill covers patterns for checking the availability of ripgrep.
  Trigger: When verifying if ripgrep is installed and accessible.
license: Apache-2.0
metadata:
  author: repoforge
  version: "1.0"
---

## Critical Patterns

### Check Availability

Use `rg_available` to determine if ripgrep is installed.

```python
from repoforge.ripgrep import rg_available

if rg_available():
    print("Ripgrep is available.")
else:
    print("Ripgrep is not available.")
```

### Get Version

Retrieve the version of the installed ripgrep using `rg_version`.

```python
from repoforge.ripgrep import rg_version

print(f"Ripgrep version: {rg_version()}")
```

## When to Use

- When setting up a development environment that requires ripgrep.
- During CI/CD pipeline checks to ensure ripgrep is available.
- To debug issues related to file searching capabilities.

## Commands

```bash
python -m repoforge.cli
```

## Anti-Patterns

### Don't: Assume Ripgrep is Installed

Assuming ripgrep is installed without checking can lead to runtime errors.

```python
# BAD
from repoforge.ripgrep import rg_version

print(f"Ripgrep version: {rg_version()}")
```

## Quick Reference

| Task                     | Pattern                     |
|--------------------------|-----------------------------|
| Check if ripgrep is available | `rg_available()`          |
| Get ripgrep version      | `rg_version()`              |