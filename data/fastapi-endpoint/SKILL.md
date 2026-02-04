---
name: fastapi-endpoint
description: Guide for creating FastAPI endpoints following this project's conventions including routers, dependency injection, error handling, and OpenAPI documentation.
---
# FastAPI Endpoint Creation

Use this skill when creating new API endpoints for this FastAPI application. Follow these patterns to ensure consistency with the existing codebase.

For comprehensive coding guidelines, see `AGENTS.md` in the repository root.

## Router Setup

Create routers in `app/api/` with proper configuration:

```python
"""
Resource router for resource management.
"""

import logging

from fastapi import APIRouter, HTTPException, Request, Response, status

from app.core.cbor import CBORRoute
from app.dependencies import CurrentUser, ResourceServiceDep
from app.exceptions import ResourceAlreadyExistsError, ResourceNotFoundError
from app.models.error import ProblemResponse, ValidationProblemResponse
from app.models.resource import Resource, ResourceCreate, ResourceUpdate

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/resource",
    tags=["Resource"],
    route_class=CBORRoute,
    responses={
        401: {"model": ProblemResponse, "description": "Unauthorized"},
        422: {"model": ValidationProblemResponse, "description": "Validation error"},
        500: {"model": ProblemResponse, "description": "Server error"},
    },
)
```

## Endpoint Pattern

Always include:
- `status_code` for non-200 responses
- Return type annotation (serves as implicit `response_model`)
- `summary` and `description` for OpenAPI docs
- `operation_id` with pattern `<resource>_<action>`
- `responses` dict for all possible status codes

### POST with 201 Created

Return resources directly with `Location` header:

```python
@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create resource",
    description="Create a new resource for the authenticated user.",
    operation_id="resource_create",
    responses={
        201: {"model": Resource, "description": "Resource created successfully"},
        403: {"model": ProblemResponse, "description": "Forbidden"},
        409: {"model": ProblemResponse, "description": "Resource already exists"},
    },
)
async def create_resource(
    request: Request,
    resource_data: ResourceCreate,
    current_user: CurrentUser,
    service: ResourceServiceDep,
    response: Response,
) -> Resource:
    """
    Create a new resource for the authenticated user.

    Stores the resource data in Firestore under the user's UID.
    Returns 409 Conflict if a resource already exists.
    """
    try:
        resource = await service.create_resource(current_user.uid, resource_data)
        response.headers["Location"] = str(request.url.path)
        response.headers["Link"] = '</schemas/ResourceData.json>; rel="describedBy"'
        return Resource(
            schema_url=str(request.base_url) + "schemas/ResourceData.json",
            id=resource.id,
            name=resource.name,
            created_at=resource.created_at,
            updated_at=resource.updated_at,
        )
    except (HTTPException, ResourceAlreadyExistsError):
        raise
    except Exception:
        logger.exception("Error creating resource", extra={"user_id": current_user.uid})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create resource"
        ) from None
```

### GET Endpoint

```python
@router.get(
    "",
    summary="Get resource",
    description="Get the resource of the authenticated user.",
    operation_id="resource_get",
    responses={
        200: {"model": Resource, "description": "Resource retrieved successfully"},
        404: {"model": ProblemResponse, "description": "Resource not found"},
    },
)
async def get_resource(
    request: Request,
    response: Response,
    current_user: CurrentUser,
    service: ResourceServiceDep,
) -> Resource:
    """
    Retrieve the resource of the authenticated user.

    Returns 404 Not Found if no resource exists for the user.
    """
    try:
        resource = await service.get_resource(current_user.uid)
        response.headers["Link"] = '</schemas/ResourceData.json>; rel="describedBy"'
        return Resource(
            schema_url=str(request.base_url) + "schemas/ResourceData.json",
            id=resource.id,
            name=resource.name,
            created_at=resource.created_at,
            updated_at=resource.updated_at,
        )
    except (HTTPException, ResourceNotFoundError):
        raise
    except Exception:
        logger.exception("Error getting resource", extra={"user_id": current_user.uid})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve resource"
        ) from None
```

### DELETE with 204 No Content

```python
@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete resource",
    description="Delete the resource of the authenticated user.",
    operation_id="resource_delete",
    responses={
        204: {"description": "Resource deleted successfully"},
        404: {"model": ProblemResponse, "description": "Resource not found"},
    },
)
async def delete_resource(
    current_user: CurrentUser,
    service: ResourceServiceDep,
) -> None:
    """
    Delete the resource of the authenticated user.

    Returns 404 Not Found if no resource exists.
    """
    try:
        await service.delete_resource(current_user.uid)
    except (HTTPException, ResourceNotFoundError):
        raise
    except Exception:
        logger.exception("Error deleting resource", extra={"user_id": current_user.uid})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete resource"
        ) from None
```

## Dependencies

Use typed dependency aliases from `app/dependencies.py`:
- `CurrentUser` for authenticated user context
- Service dependencies like `ResourceServiceDep`

Create new service dependencies in `app/dependencies.py`:

```python
from typing import Annotated
from fastapi import Depends
from app.services.resource import ResourceService


def get_resource_service() -> ResourceService:
    """
    Dependency provider for ResourceService.
    """
    return ResourceService()


ResourceServiceDep = Annotated[ResourceService, Depends(get_resource_service)]
```

## Error Handling

- Re-raise domain exceptions and `HTTPException` to let handlers convert them
- Use `logger.exception()` with structured `extra={}` for unexpected errors
- Use `from None` to suppress exception chaining in generic 500 responses
- Never expose internal error details to clients

## PATCH Endpoints

For partial updates, use `response_model_exclude_unset=True`:

```python
@router.patch(
    "",
    response_model=Resource,
    response_model_exclude_unset=True,
    summary="Update resource",
    description="Partially update the resource of the authenticated user.",
    operation_id="resource_update",
    responses={
        200: {"model": Resource, "description": "Resource updated successfully"},
        404: {"model": ProblemResponse, "description": "Resource not found"},
    },
)
async def update_resource(
    request: Request,
    resource_data: ResourceUpdate,
    current_user: CurrentUser,
    service: ResourceServiceDep,
    response: Response,
) -> Resource:
    ...
```

## Router Registration

Register new routers in `app/api/__init__.py` and include in `app/main.py`:

```python
# In app/api/__init__.py - add to v1_router for versioned endpoints
from app.api import resource

v1_router.include_router(resource.router)

# In app/main.py - for unversioned endpoints
from app.api import resource

app.include_router(resource.router)
```

## URL Conventions

- Always use empty string `""` for root resource paths (e.g., `@router.post("")`)
- Use plural nouns for collection endpoints
- Keep routes RESTful: POST for create, GET for read, PATCH for update, DELETE for delete

## Error Response Models

Use `ProblemResponse` for standard errors and `ValidationProblemResponse` for 422 validation errors:

```python
from app.models.error import ProblemResponse, ValidationProblemResponse
```

These models follow RFC 9457 Problem Details format.
