---
name: exceptions
description: Guide for creating exceptions using fastapi-problem that are automatically converted to RFC 9457 Problem Details responses.
---
# Exception Creation

Use this skill when creating exceptions that are automatically converted to RFC 9457 Problem Details responses.

For comprehensive coding guidelines, see `AGENTS.md` in the repository root.

## Base Exception Classes

The project uses `fastapi-problem` base classes from `app/exceptions/base.py`:

```python
from fastapi_problem.error import (
    BadRequestProblem,
    ConflictProblem,
    ForbiddenProblem,
    NotFoundProblem,
    ServerProblem,
    UnauthorisedProblem,
    UnprocessableProblem,
)
```

| Base Class | Status Code | Use Case |
|------------|-------------|----------|
| `NotFoundProblem` | 404 | Resource not found |
| `ConflictProblem` | 409 | Duplicate resource, state conflict |
| `BadRequestProblem` | 400 | Invalid request (cursor, parameter) |
| `ForbiddenProblem` | 403 | Access denied |
| `UnauthorisedProblem` | 401 | Authentication required |
| `UnprocessableProblem` | 422 | Validation failure |
| `ServerProblem` | 500 | Internal server error |

## Creating Resource-Specific Exceptions

Create new exceptions in `app/exceptions/`:

```python
# app/exceptions/resource.py
"""
Resource-related exceptions.
"""

from fastapi_problem.error import ConflictProblem, NotFoundProblem


class ResourceNotFoundError(NotFoundProblem):
    """
    Raised when a resource cannot be found.
    """

    title = "Resource not found"


class ResourceAlreadyExistsError(ConflictProblem):
    """
    Raised when attempting to create a duplicate resource.
    """

    title = "Resource already exists"
```

## Exporting Exceptions

Export new exceptions from `app/exceptions/__init__.py`:

```python
from app.exceptions.base import (
    BadRequestProblem,
    ConflictProblem,
    ForbiddenProblem,
    NotFoundProblem,
    ServerProblem,
    UnauthorisedProblem,
    UnprocessableProblem,
)
from app.exceptions.resource import ResourceAlreadyExistsError, ResourceNotFoundError

__all__ = [
    "BadRequestProblem",
    "ConflictProblem",
    "ForbiddenProblem",
    "NotFoundProblem",
    "ResourceAlreadyExistsError",
    "ResourceNotFoundError",
    "ServerProblem",
    "UnauthorisedProblem",
    "UnprocessableProblem",
]
```

## Using Exceptions

Import from the package root:

```python
# In routers and services
from app.exceptions import ResourceNotFoundError, ResourceAlreadyExistsError
```

Raise exceptions in services:

```python
async def get_resource(self, user_id: str) -> Resource:
    snapshot = await doc_ref.get()
    if not snapshot.exists:
        raise ResourceNotFoundError("Resource not found")
    return Resource(**snapshot.to_dict())
```

## Exception Handling in Routers

Re-raise exceptions to let handlers convert them:

```python
@router.get("/")
async def get_resource(
    current_user: CurrentUser,
    service: ResourceServiceDep,
) -> Resource:
    try:
        return await service.get_resource(current_user.uid)
    except (HTTPException, ResourceNotFoundError):
        raise
    except Exception:
        logger.exception("Error getting resource", extra={"user_id": current_user.uid})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve resource"
        ) from None
```

## RFC 9457 Problem Details Response

Exceptions are automatically converted to Problem Details format:

```json
{
  "type": "about:blank",
  "title": "Resource not found",
  "status": 404,
  "detail": "Resource not found"
}
```

The exception handler in `app/core/exception_handler.py`:
- Uses `fastapi-problem` singleton `eh` with pre/post hooks
- Adds `X-Request-ID` to all error responses
- Adds `$schema` field and `Link` header with `rel="describedBy"` to error responses
- Supports CBOR error responses via `CBORProblemPostHook`
- Strips extras from 5xx errors in production via `StripExtrasPostHook`

## Custom Detail Message

Pass a custom message when raising:

```python
raise ResourceNotFoundError(detail="Resource with ID 'abc123' was not found")
```

## Naming Convention

Use descriptive names with `Error` suffix:
- `{Resource}NotFoundError`
- `{Resource}AlreadyExistsError`
- `{Resource}InvalidError`
- `{Resource}ExpiredError`

## Testing

Test exception behavior:

```python
def test_returns_404_when_not_found(
    client: TestClient,
    with_fake_user: None,
    mock_resource_service: AsyncMock,
) -> None:
    mock_resource_service.get_resource.side_effect = ResourceNotFoundError()

    response = client.get("/v1/resource")

    assert response.status_code == 404
    body = response.json()
    assert body["title"] == "Resource not found"
    assert body["status"] == 404
```
