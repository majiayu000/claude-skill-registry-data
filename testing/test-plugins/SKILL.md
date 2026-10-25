---
name: test-plugins-build-commands
description: >
  This skill covers testing plugins for various repository types.
  Trigger: Load this skill when working with test_plugins.
license: Apache-2.0
metadata:
  author: repoforge
  version: "1.0"
  complexity: low
  token_estimate: 350
  dependencies: []
  related_skills: []
  load_priority: high
---

<!-- L1:START -->
# test-plugins-build-commands

This skill covers testing plugins for various repository types.

**Trigger**: Load this skill when working with test_plugins.
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Map Python repositories | `python_repo_map` |
| Map Node repositories | `node_repo_map` |

## Critical Patterns (Summary)
- **Python Repository Mapping**: Use `python_repo_map` to map Python repositories.
- **Node Repository Mapping**: Use `node_repo_map` to map Node.js repositories.
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns (Detailed)

### Python Repository Mapping

Utilize `python_repo_map` to effectively map Python repositories for testing.

```python
# Example of using python_repo_map
repo_mapping = python_repo_map()
```

### Node Repository Mapping

Leverage `node_repo_map` to map Node.js repositories for your testing needs.

```python
# Example of using node_repo_map
node_mapping = node_repo_map()
```

## When to Use

- When you need to test Python plugins in a repository.
- When you are validating Node.js plugins in your project.

## Commands

```bash
pytest tests/test_plugins.py
```

## Anti-Patterns

### Don't: Hardcode Repository Paths

Hardcoding paths can lead to maintenance issues and reduce flexibility.

```python
# BAD
repo_path = "/path/to/repo"
```
<!-- L3:END -->