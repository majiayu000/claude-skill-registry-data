---
name: pypi-collision-fix
description: "Fix PyPI package name collisions when local package name exists on PyPI"
author: KINTSUGI Team
date: 2025-12-11
---

# PyPI Package Name Collision Fix

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-12-11 |
| **Goal** | Fix issue where `pip install kintsugi[extra]` downloaded wrong package from PyPI |
| **Environment** | Linux (HiPerGator), Python 3.10, pip 24.x |
| **Status** | Success |

## Context

When developing a package locally with `pip install -e .`, if the package name already exists on PyPI (even as a placeholder or different project), running commands like `pip install package[extra]` will download from PyPI instead of using the local editable install.

### The Problem

Our package is named `kintsugi`. There's also a `kintsugi` package on PyPI (version 0.0.1, unrelated project). When running:

```bash
kintsugi install bio  # internally runs: pip install kintsugi[bio]
```

This downloaded `kintsugi-0.0.1` from PyPI, overwriting our local editable install.

### Error Signature

```bash
$ pip show kintsugi
Name: kintsugi
Version: 0.0.1  # Wrong! Should be our development version
Location: /path/to/site-packages
```

Or the package imports fail because the PyPI version has different modules.

## Verified Workflow

### Solution: Use Direct Package Names Instead of Extras

Instead of relying on `pip install package[extra]` syntax, use direct package names:

**Before (broken):**
```python
OPTIONAL_GROUPS = {
    "bio": {
        "install_cmd": "pip install kintsugi[bio]",  # Downloads from PyPI!
        ...
    }
}
```

**After (working):**
```python
OPTIONAL_GROUPS = {
    "bio": {
        "install_cmd": "pip install scanpy scimap squidpy anndata",  # Direct packages
        ...
    }
}
```

### Implementation in KINTSUGI

We updated `src/kintsugi/cli.py` to use direct package names:

```python
OPTIONAL_GROUPS: dict[str, dict[str, Any]] = {
    "bio": {
        "description": "Spatial biology analysis (scanpy, scimap, squidpy)",
        "install_cmd": "pip install scanpy scimap squidpy anndata",
        "packages": ["scanpy", "scimap", "squidpy", "anndata"],
    },
    "gpu": {
        "description": "GPU acceleration (cupy, pytorch)",
        "install_cmd": "pip install cupy-cuda12x torch",
        "packages": ["cupy", "torch"],
    },
    # ... etc
}
```

### Fix Existing Broken Install

If already affected:

```bash
# Remove the wrong package
pip uninstall kintsugi

# Reinstall local editable version
pip install -e /path/to/your/project

# Verify
pip show kintsugi  # Should show your version and location
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Using `pip install kintsugi[bio]` | PyPI has priority over local editable installs for extras resolution | Never use `package[extra]` syntax if package name exists on PyPI |
| Adding `--no-index` flag | Breaks installation of actual dependencies | Only works if all deps are local |
| Using `pip install -e .[bio]` | Works initially but subsequent `pip install kintsugi[x]` still breaks | Users running CLI commands won't use `-e .` syntax |
| Renaming package | Breaking change for existing users | Only viable for new projects |

## Final Parameters

For CLI tools that install optional dependencies:

```python
# pyproject.toml - still define extras for documentation
[project.optional-dependencies]
bio = ["scanpy", "scimap", "squidpy", "anndata"]
gpu = ["cupy-cuda12x", "torch"]

# cli.py - use direct package names for actual installation
OPTIONAL_GROUPS = {
    "bio": {
        "install_cmd": "pip install scanpy scimap squidpy anndata",
        ...
    }
}
```

## Key Insights

- PyPI package names are first-come-first-served - check if your name exists before publishing
- The `pip install package[extra]` syntax queries PyPI even for editable installs
- This is a silent failure - pip happily installs the wrong package
- Always verify with `pip show package` after installation
- Consider using a more unique package name for new projects

## References

- PyPI kintsugi package: https://pypi.org/project/kintsugi/
- pip extras documentation: https://pip.pypa.io/en/stable/cli/pip_install/#examples
- KINTSUGI PR fixing this: commit 6eb5b75
