---
name: dependency-deprecation
description: "Pattern for deprecating external dependencies while maintaining backward compatibility. Trigger: removing Java/FIJI/MATLAB, deprecating optional deps"
author: KINTSUGI Team
date: 2025-12-11
---

# Dependency Deprecation Pattern

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-12-11 |
| **Goal** | Remove Java/Maven/FIJI/CLIJ2 dependencies from KINTSUGI while maintaining backward compatibility |
| **Environment** | Python 3.10+, cross-platform (Windows/Linux/macOS) |
| **Status** | Success |

## Context
KINTSUGI originally depended on Java/Maven for PyImageJ and CLIJ2 GPU processing. This created installation friction and cross-platform issues. The goal was to replace these with pure Python implementations (CuPy/NumPy) while allowing legacy users to continue using Java if needed.

## Verified Workflow

### Step 1: Identify all dependency touchpoints

Search for all references to the dependency:
```bash
# Search code
grep -r "java\|Java\|FIJI\|fiji\|clij\|CLIJ\|maven\|Maven\|ImageJ\|imagej" src/ notebooks/

# Check configuration files
grep -r "java\|openjdk\|maven" envs/ pyproject.toml
```

Files typically affected:
- `pyproject.toml` - optional dependencies
- `envs/*.yml` - conda environment files
- `src/*/deps.py` - dependency checker
- `docs/*.md` - documentation
- Core modules using the dependency

### Step 2: Update the core module with deprecation

```python
# Example: edf.py - deprecating CLIJ2 backend

import warnings
from typing import Literal

BackendType = Literal["auto", "cupy", "numpy", "clij2"]

def _detect_backend(self, requested: BackendType) -> str:
    """Detect best available backend."""
    if requested == "clij2":
        warnings.warn(
            "CLIJ2 backend is deprecated and will be removed in v2.0. "
            "Use 'cupy' or 'numpy' instead.",
            DeprecationWarning,
            stacklevel=2
        )
        # Still allow it to work for now
        if self._check_clij2_available():
            return "clij2"
        else:
            warnings.warn("CLIJ2 not available, falling back to cupy")
            requested = "auto"

    if requested == "auto":
        # NEW priority order: CuPy > NumPy (CLIJ2 excluded from auto)
        if self._check_cupy_available():
            return "cupy"
        return "numpy"

    return requested
```

### Step 3: Update dependency checker

```python
# deps.py - mark as deprecated but keep functional

def _check_java(self, verbose: bool):
    """Check Java installation.

    .. deprecated::
        Java/Maven dependencies are no longer required for core functionality.
        Kept for backward compatibility with legacy CLIJ2 workflows.
    """
    if verbose:
        print("\n[Java/Maven] (DEPRECATED - no longer required)")

    # Still check and report, but don't fail
    try:
        # ... existing check code ...
        if verbose:
            print(f"  [OK]       java v{version} (optional)")
    except Exception as e:
        if verbose:
            print(f"  [SKIP]     java (optional, not required)")
```

### Step 4: Update pyproject.toml

```toml
[project.optional-dependencies]
# Keep the optional group but exclude from [full]
java = [
    "JPype1>=1.5.0",
    "scyjava>=1.0.0",
    "pyimagej>=1.4.0",
]

# Remove java from full install
full = [
    "kintsugi[gpu,viz,dl,analysis,bio]",  # Note: java excluded
]
```

### Step 5: Update environment files

```yaml
# envs/env-*.yml - comment out with deprecation note

# Java/ImageJ Integration (DEPRECATED - no longer required)
# Uncomment if you need legacy CLIJ2 support:
# - openjdk=11
# - maven
# - jpype1
```

### Step 6: Update documentation

Add deprecation notices to all relevant docs:
```markdown
> **Note:** Java, Maven, and FIJI are no longer required. KINTSUGI now uses
> pure Python implementations (CuPy/NumPy) for all processing including EDF.
```

For historical documents, add a header:
```markdown
> **DEPRECATION NOTICE (2025):** This document is historical. Java/Maven/FIJI
> dependencies have been removed. See `src/kintsugi/edf.py` for current implementation.
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Removing code completely | Broke existing user workflows | Keep deprecated code functional |
| Silent removal | Users confused when code stopped working | Always emit deprecation warnings |
| Keeping in [full] install | Users still got Java install failures | Exclude from aggregate installs |
| No migration path | Users didn't know what to use instead | Document the replacement clearly |

## Key Insights

- **Gradual deprecation**: Mark as deprecated first, remove in next major version
- **Keep it working**: Deprecated doesn't mean broken - users need time to migrate
- **Clear warnings**: Use Python's `warnings.warn()` with `DeprecationWarning`
- **Document the alternative**: Every deprecation notice should say what to use instead
- **Update ALL touchpoints**: Code, configs, docs, environment files, README
- **Test both paths**: Verify deprecated code still works AND new code works

## Checklist for Dependency Deprecation

- [ ] Search entire codebase for dependency references
- [ ] Add deprecation warnings to code using the dependency
- [ ] Update auto-detection to prefer new implementation
- [ ] Keep optional dependency group but exclude from `[full]`
- [ ] Comment out in environment files with explanation
- [ ] Update installation documentation
- [ ] Add deprecation notices to historical docs
- [ ] Update CLAUDE.md / project documentation
- [ ] Test deprecated path still works
- [ ] Test new path works
- [ ] Update changelog/release notes

## References
- Python deprecation warnings: https://docs.python.org/3/library/warnings.html
- Semantic versioning for breaking changes: https://semver.org/
- PEP 387 - Backwards Compatibility Policy: https://peps.python.org/pep-0387/
