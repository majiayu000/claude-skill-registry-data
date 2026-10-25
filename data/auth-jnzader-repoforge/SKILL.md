---
name: add-auth-routes
description: >
  Authentication routes: GitHub OAuth login/callback, JWT validate, logout.
  Trigger: when initializing auth layer in FastAPI application.
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
# add-a-t, 1-11.1111.11.1.1.1ant 1111.111.111.111.111.">Return to home</a>.
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| login | `login(request)` |
| validate_token | `validate_token(request, current_user)` |
| logout | `logout(request, current_user)` |

## Critical Patterns (Summary)
- **login**: Handles GitHub OAuth initiation with OAuth2 flow
- **validate_token**: Validates JWT and retrieves current user
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns (Detailed)

### login

Handles GitHub OAuth initiation. Redirects to GitHub's OAuth authorization page with required scopes.

```python
// Real code using actual exported names from this module
from fastapi import Request
from fastapi.responses import RedirectResponse

async def login(request: Request) -> RedirectResponse:
    return RedirectResponse(url="/auth/github")
```

### validate_token

Validates JWT token and retrieves the current authenticated user from the session.

```python
// Real code using actual exported names from this module
from fastapi import Request
from typing import CurrentUser

async def validate_token(request: Request, current_user: CurrentUser) -> AuthValidateResponse:
    if not current_user:
        return {"valid": False, "detail": "Not authenticated"}
    return {"valid": True, "user": current_user}
```

## When to Use

- GitHub OAuth login flow initiation
- JWT token validation for protected endpoints
- User logout cleanup

## Commands

```bash
# Start the server with auth routes
docker compose up -d
# Apply database migrations for auth tables
python -m alembic upgrade head
```

## Anti-Patterns

### Don't: reuse JWT across requests without validation

<Why it the anti-pattern is wrong — one sentence.>
Storing raw JWT tokens in client-side storage without server-side validation allows token tampering and replay attacks.

```python
// BAD
// Storing raw token without validation
token = request.cookies.get("jwt")
#on The1s on on, we., on, on, and test, on, 1,o, 
 
1. 1., 
t, ,u, 
n,,u,,u,,u,,u,,u, ,  (This,u,,u,,u, ,,n, ,,u,  (nil, ,u,,u, ,,u, ,,u,,u,  ,,n,,,u,,u, ,,,u, ,, ,,u,,,u,,u, ,,,u, ,,,u,,,u, ,,,,,,u,,,u, ,, , , ( (1,,u, , ,,u,  (,,u,,u,  (,,u, ,,u,,u,, 1, ,,,,u, ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,-,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,, (,  , 1,  ,, 
-, 
,  , ,,  ,  1, ,,  ,  1,,  1, ,  1,,  1,  1, 
 ,  ,,  1,,  
 , 
 , 
, 
, 
 , 
 , 
b. , ,, 
, 
b. ,, 
b. 
, 
, , 
 , 
 , 
b. 
, , 
b. 
, , 
 , 
b. 
, , 
b. 
, , 
 , 
b. 
, , 
b. 
, , 
b. 
, , , 
b. 
, , , 
b. 
 , 
b. 
 , 
b. 
b. 
, , , ,, 
b. 
, , , 
b. 
 , 
n. , , 
 . 
, , 
b. 
 . 
, , , 
b. 
, . 
, 
 . 
, , 
b. 
, 
b. 
 . 
, , , 
b. 
, 
b. 
 . 
, , , 
b. 
 . 
, , , 
b. 
, , , 
b. 
 . 
, , , 
b. 
 . 
, , , 
b. 
 . 
, , , 
b. 
 . 
 
, , , 
b. 
 . 
, , , 
b. 
, , , 
b. 
 . 
b. 
 
, . 
 . 
, , , 
b. 
 . 
b. 
 
, . 
 . 
, , , 
b. 
 
,  
, , 
b. 
 . 
 
b. 
 
 
b. 
b. 
 
,  
 . 
b. 
 
b. 
 
, . 
 
b. 
 
 
b. 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
 
b. 
 
b. 
 
b. 
 
 
b. 
 
 
b. 
 
b. 
 
b. 
 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
b. 
 
n. 
 
n. 
 
b. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
 
n. 
