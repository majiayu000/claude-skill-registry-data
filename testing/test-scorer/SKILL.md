---
name: add-test-scorer-endpoint
description: >
  This skill covers patterns for creating and managing test scorer endpoints.
  Trigger: Load this skill when working with the test_scorer module.
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
# add-test-scorer-endpoint

This skill covers patterns for creating and managing test scorer endpoints.

**Trigger**: Load this skill when working with the test_scorer module.
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Create a user | `create_user` |
| Retrieve users | `get_users` |

## Critical Patterns (Summary)
- **Create User**: Use `create_user` to add a new user to the system.
- **Get Users**: Utilize `get_users` to fetch a list of all users.
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns (Detailed)

### Create User

Use `create_user` to add a new user to the system, ensuring proper data handling.

```python
from tests.test_scorer import create_user

new_user = create_user(name="John Doe", email="john@example.com")
```

### Get Users

Utilize `get_users` to fetch a list of all users, which can be useful for displaying user data.

```python
from tests.test_scorer import get_users

users = get_users()
```

## When to Use

- When you need to add new users for testing purposes.
- When retrieving user data for validation in tests.

## Commands

```bash
pytest tests/test_scorer.py
```

## Anti-Patterns

### Don't: Hardcode User Data

Hardcoding user data can lead to brittle tests that fail with changes in requirements.

```python
# BAD
user = create_user(name="Hardcoded User", email="hardcoded@example.com")
```
<!-- L3:END -->