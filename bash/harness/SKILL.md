---
name: add-harness-parent-path
description: >
  This skill covers adding the parent directory to the path when running the harness directly.
  Trigger: When using the harness module in a standalone context.
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
# add-harness-parent-path

This skill covers adding the parent directory to the path when running the harness directly.

**Trigger**: When using the harness module in a standalone context.
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Create FastAPI CRUD module | `make_fastapi_crud_module` |
| Create Next.js page module | `make_nextjs_page_module` |

## Critical Patterns (Summary)
- **Create FastAPI CRUD module**: Generates a CRUD module for FastAPI.
- **Create Next.js page module**: Generates a page module for Next.js.
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns (Detailed)

### Create FastAPI CRUD module

Generates a CRUD module for FastAPI, allowing for quick API development.

```python
from eval.harness import make_fastapi_crud_module

module = make_fastapi_crud_module("User")
```

### Create Next.js page module

Generates a page module for Next.js, facilitating frontend development.

```python
from eval.harness import make_nextjs_page_module

module = make_nextjs_page_module("HomePage")
```

## When to Use

- When developing a new FastAPI service and needing CRUD operations.
- When creating a new page in a Next.js application.

## Commands

```bash
python repoforge/cli.py run
```

## Anti-Patterns

### Don't: Hardcode paths

Hardcoding paths can lead to issues with portability and maintainability.

```python
# BAD
import sys
sys.path.append('/absolute/path/to/harness')
```
<!-- L3:END -->