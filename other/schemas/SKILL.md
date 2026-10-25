---
name: add-schemas-endpoint
description: >
  Pydantic v2 request/response schemas for RepoForge Web API.
  Trigger: when defining or validating schemas in apps/server/app/models/schemas.py
license: Apache-2.0
metadata:
  author: repoforge
  version: "1.0"
complexity: low
token_estimate: 450
dependencies: []
related_skills: [auth, generate]
load_priority: high
---

<!-- L1:START -->
# add-schemas-endpoint

Pydantic v2 request/response schemas for RepoForge Web API.

**Trigger**: when defining or validating schemas in apps/server/app/models/schemas.py
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Validate user input | `UserInfo` |
| Structure API responses | `UserResponse` |
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns (Detailed)

### Pattern: UserInfo Validation

Validates incoming user data with required fields and type coercion.

```python
// Real code using actual exported names from this module
from pydantic import BaseModel

class UserInfo(BaseModel):
    username: str
    email: str
    is_active: bool = True
```
### Pattern: UserResponse Structure

Structures API response with computed fields and serialization.

```python
// Real code using actual exported names from this module
from pydantic import BaseModel, Field

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
```
## When to Use

- When defining request models for `/auth/validate` endpoint
- When structuring user data in API responses

## Commands

```bash
# Run the server with uvicorn
uvicorn apps.server.main:app --reload

# Apply database migrations
alembic upgrade head
```
## Anti-Patterns

### Don't: Omit required fields

<Why it's wrong.> Omitting required fields like `username` or `email` causes Pydantic validation errors at runtime, breaking API endpoints.

```python
// BAD
class BadUserInfo(BaseModel):
    # Missing required 'username' field
    email: str
```
<!-- L3:END -->