---
name: test-compressor-fixtures
description: >
  This skill covers patterns for creating fixtures to test compression passes.
  Trigger: Load this skill when working with test_compressor.
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
# test-compressor-fixtures

This skill covers patterns for creating fixtures to test compression passes.

**Trigger**: Load this skill when working with test_compressor.
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Create user fixture | `create_user` |
| Get user fixture | `get_user` |

## Critical Patterns (Summary)
- **Create User Fixture**: Use `create_user` to set up a user for testing.
- **Get User Fixture**: Utilize `get_user` to retrieve user data for tests.
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns (Detailed)

### Create User Fixture

Use `create_user` to set up a user for testing compression passes in your tests.

```python
from tests.test_compressor import create_user

user = create_user(name="Test User", email="test@example.com")
```

### Get User Fixture

Utilize `get_user` to retrieve user data for tests, ensuring the user exists before running tests.

```python
from tests.test_compressor import get_user

user = get_user(user_id=1)
```

## When to Use

- When you need to create a user for testing compression functionality.
- When you need to retrieve user data to validate compression results.

## Commands

```bash
pytest tests/test_compressor.py
```

## Anti-Patterns

### Don't: Hardcode User Data

Hardcoding user data can lead to brittle tests that fail when data changes.

```python
# BAD
user = create_user(name="Hardcoded User", email="hardcoded@example.com")
```
<!-- L3:END -->