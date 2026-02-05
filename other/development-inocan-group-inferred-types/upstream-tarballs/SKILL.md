---
name: upstream-tarballs
description: Use when maintaining a fork of a Python package without GitHub access, importing upstream releases from PyPI tarballs, or merging upstream updates into a fork using vendor branch strategy
---

# Managing Upstream Tarballs

## Overview

Maintain a fork of a Python package when you only have access to PyPI (not GitHub). Uses a **vendor branch strategy**: dedicated `upstream` branch with one commit per release, development on `main`, upstream updates merged in.

**Core principle:** Keep upstream branch pure (vendor mirror only), merge into main, never rebase.

## When to Use

- Setting up a fork from PyPI tarball (no GitHub access)
- Importing a new upstream version into existing fork
- Merging upstream changes into your fork
- Resolving conflicts between fork and upstream changes
- Enterprise environment where GitHub blocked but PyPI accessible

**When NOT to use:**
- You have GitHub access (clone/fork normally)
- One-time package vendoring (just copy files)

## Quick Reference

```powershell
# === INITIAL SETUP ===
git init && git checkout --orphan upstream
pip download --no-deps --no-binary :all: pkg==1.0.0
tar -xzf pkg-1.0.0.tar.gz --strip-components=1
git add -A && git commit -m "upstream: import pkg v1.0.0"
git tag upstream/v1.0.0
git checkout -b main

# === UPDATE FROM UPSTREAM ===
git checkout upstream
git rm -rf . && git clean -fd
pip download --no-deps --no-binary :all: pkg==1.1.0
tar -xzf pkg-1.1.0.tar.gz --strip-components=1
git add -A && git commit -m "upstream: import pkg v1.1.0"
git tag upstream/v1.1.0
git checkout main
git merge upstream --allow-unrelated-histories -m "merge: upstream v1.1.0 into main"
pytest tests/

# === CONFLICT RESOLUTION ===
git diff --name-only --diff-filter=U   # List conflicts
# resolve each, then:
git add <resolved-file>
pytest tests/ -x
git commit

# === ROLLBACK ===
git revert -m 1 <merge-commit-hash>

# === USEFUL ===
pip index versions pkg              # Check PyPI versions
git log --oneline main ^upstream    # Fork-only commits
git diff upstream main              # All fork differences
```

## Version Numbering

```
1.2.3+fork.1  # Upstream 1.2.3, first fork revision
1.2.3+fork.2  # Same upstream, second fork revision  
1.2.4+fork.1  # New upstream, reset fork revision
```

## Fork Architecture (Re-Export Layer)

Minimize merge conflicts by keeping upstream structure intact:

```
src/
  original_pkg/     # Upstream code (untouched)
  myfork/           # Your re-export layer
    __init__.py     # Re-exports public API + extensions
    extensions.py   # Your custom code
```

```python
# src/myfork/__init__.py
from original_pkg import Client, Config, SomeClass
from myfork.extensions import CustomFeature

__all__ = ["Client", "Config", "SomeClass", "CustomFeature"]
```

## pyproject.toml Changes

Keep your sections, accept upstream for dependencies:

| Section | Owner |
|---------|-------|
| `name`, `version`, `[project.scripts]` | **Your fork** |
| `dependencies`, `[build-system]` | **Upstream** |
| `[project.optional-dependencies]` | Merge carefully |

## Conflict Resolution Workflow

For each conflicted file:

1. **Categorize:** Upstream bugfix vs your feature? Same logic changed?
2. **Propose resolution** with rationale
3. **Apply and test immediately** (`pytest tests/ -x`)
4. **Document significant decisions** in `FORK_CHANGES.md`

## Commit Prefixes

| Prefix | Use For |
|--------|---------|
| `upstream:` | Importing new upstream versions |
| `fork:` | Fork infrastructure (CI, configs) |
| `merge:` | Merge commits from upstream |
| `feat:`, `fix:`, `docs:` | Your changes |

## Common Mistakes

| Mistake | Correct |
|---------|---------|
| Extract tarball over existing files | Clear branch first: `git rm -rf . && git clean -fd` |
| Rebase main onto upstream | Use merge commits to preserve history |
| Commit your changes on upstream branch | Upstream is vendor mirror only |
| Skip versions | Import each version sequentially |

## Red Flags - STOP

- About to commit changes directly on `upstream` branch
- About to rebase instead of merge
- Extracting without clearing directory first
- Skipping test run after merge

## Edge Cases

**File renamed upstream:** Check with `git diff upstream~1 upstream --name-status | Select-String "^R"` and manually port changes.

**Cherry-pick specific fix:** Download both versions, diff, apply manually to main.

**pyproject.toml conflicts:** Expected every merge. Keep your `name`/`version`, accept upstream deps.

## Files to Maintain

**FORK_CHANGES.md** - Track what you modified:
```markdown
## Current Base: upstream v1.2.0 → fork 1.2.0+fork.3

### Modified (in original_pkg/)
- client.py: Added retry logic (lines 45-60)

### Added (in myfork/)
- extensions.py: Custom caching

### Conflict Log
| Date | Version | Notes |
|------|---------|-------|
| 2025-01-15 | v1.0.0 | Initial |
| 2025-03-20 | v1.1.0 | Clean merge |
```

## The Bottom Line

**Upstream branch = pure vendor mirror. Development on main. Merge, never rebase.**

Clear before extract → commit with tag → merge into main → test → bump version.
