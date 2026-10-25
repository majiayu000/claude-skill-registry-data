---
name: add-test-ripgrep-endpoint
description: >
  This skill covers adding endpoints for user management in the test_ripgrep module.
  Trigger: When implementing user management features in the test_ripgrep context.
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
# add-test-ripgrep-endpoint

This skill covers adding endpoints for user management in the test_ripgrep module.

**Trigger**: When implementing user management features in the test_ripgrep context.
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Create User Endpoint | `create_user` |
| Get Users Endpoint | `get_users` |

## Critical Patterns (Summary)
- **Create User Endpoint**: Implements a FastAPI endpoint to create a new user.
- **Get Users Endpoint**: Implements a FastAPI endpoint to retrieve all users.
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns (Detailed)

### Create User Endpoint

This pattern demonstrates how to create a FastAPI endpoint for user creation using the `create_user` function.

```python
from fastapi import FastAPI
from your_module import create_user

app = FastAPI()

@app.post("/users/")
def add_user(user_data: dict):
    return create_user(user_data)
```

### Get Users Endpoint

This pattern shows how to implement an endpoint to fetch all users using the `get_users` function.

```python
from fastapi import FastAPI
from your_module import get_users

app = FastAPI()

@app.get("/users/")
def list_users():
    return get_users()
```

## When to Use

- When you need to implement user creation functionality in the test_ripgrep module.
- When you want to retrieve a list of users for display or processing.

## Commands

```bash
python -m pytest tests/test_ripgrep.py
```

## Anti-Patterns

### Don't: Hardcode User Data

Hardcoding user data can lead to maintenance issues and security vulnerabilities.

```python
# BAD
def add_user():
    user = {"name": "John Doe", "email": "john@example.com"}
    return create_user(user)
```
<!-- L3:END -->