---
name: add-incremental-endpoint
description: >
  Incremental data model operations for chapter dependencies and manifest management.
  Trigger: incremental or manifest operations
license: Apache-2.0
metadata:
  author: repoforge
  version: "1.0"
  complexity: medium
  token_estimate: 600
  dependencies: []
  related_skills: []
  load_priority: high
---

<!-- L1:START -->
# add-incremental-endpoint

One sentence: Handles incremental chapter dependency tracking and manifest persistence for the repoforge build system.

**Trigger**: incremental or manifest operations
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Load manifest | `load_manifest(out_dir)` |
| Get git SHA | `get_git_sha(repo_root)` |
| Check stale chapters | `stale_chapter_names(changed_files, consumed_by_chapter)` |
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns (Detailed)

### Pattern 1: Manifest Persistence

Load and save the manifest to track chapter state across incremental builds.

```python
# Load existing manifest
manifest: Optional[Manifest] = load_manifest(out_dir)

# Save updated manifest after changes
save_manifest(out_dir, manifest)  # type: ignore
```

### Pattern 2: Stale Chapter Detection

Identify which chapters need rebuilding after file changes by comparing dependencies.

```python
# Detect chapters that are stale due to changed files
stale: list[str] = stale_chapter_names(changed_files, consumed_by_chapter)
```

## When to Use

- After git operations to determine which chapters need rebuilding
- When file changes invalidate chapter dependencies
- Before running incremental builds to skip up-to-date chapters

## Commands

```bash
# Run incremental build
python -m repoforge.cli build --incremental

# Check git state
python -c "from repoforge.incremental import get_git_sha; print(get_git_sha(Path('.')))"
```

## Anti-Patterns

### Don't: Skip dependency tracking

```python
# BAD: Assuming no chapters are stale without checking dependencies
stale = []  # Wrong: never empty if files changed
```

```python
# BAD: Missing manifest persistence
save_manifest(out_dir, manifest)  # Required after chapter changes
```
<!-- L3:END -->