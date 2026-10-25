---
name: main-layer
description: >
  This layer encompasses the core functionality of the project, managing the primary modules and their interactions.
  Trigger: When working in main/ — adding, modifying, or debugging core functionalities.
license: Apache-2.0
metadata:
  author: repoforge
  version: "1.0"
  complexity: medium
  token_estimate: 450
  dependencies: []
  related_skills: []
  load_priority: high
---

<!-- L1:START -->
# main-layer

This skill covers the core functionality and structure of the main layer.

**Trigger**: When working in main/ directory and its main responsibility.
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Create a new module | `eval/harness.py` |

## Critical Patterns (Summary)
- **Module Initialization**: Ensure proper path setup when running modules directly.
- **Data Adaptation**: Use adapters for valid target identifiers in the project.
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns (Detailed)

### Module Initialization

Ensure proper path setup when running modules directly to avoid import errors.

```python
# eval/harness.py
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
```

### Data Adaptation

Utilize adapters to manage valid target identifiers, ensuring consistent data handling across modules.

```python
# repoforge/adapters.py
def adapt_for_cursor(data):
    # Adapt data for cursor usage
    pass
```

## When to Use

- When creating or modifying core modules that interact with the main functionality.
- When integrating new features that require adjustments to existing data handling.

## Commands

```bash
python -m eval.harness
```

## Anti-Patterns

### Don't: Modify core modules without testing

Changing core modules can lead to unexpected behavior across the project.

```python
# BAD
def broken_function():
    return undefined_variable
```
<!-- L3:END -->