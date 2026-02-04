---
name: pydantic-model
description: Guide for creating Pydantic v2 models with proper validation, field examples, and schema separation following this project's conventions.
---
# Pydantic Model Creation

Use this skill when creating Pydantic models for request/response schemas in this FastAPI application.

For comprehensive coding guidelines, see `AGENTS.md` in the repository root.

## Model File Structure

Create models in `app/models/<domain>/` (e.g., `app/models/profile/`) with separate files:
- `requests.py` - Request models (`ResourceBase`, `ResourceCreate`, `ResourceUpdate`)
- `responses.py` - Response models (`Resource`) and collection constants
- `__init__.py` - Re-exports for convenient imports

Example structure:
```
app/models/resource/
├── __init__.py       # Re-exports all models and constants
├── requests.py       # ResourceBase, ResourceCreate, ResourceUpdate
└── responses.py      # Resource, RESOURCE_COLLECTION
```

**Request models** (`app/models/resource/requests.py`):
```python
"""
Resource request models.
"""

from pydantic import BaseModel, ConfigDict, Field

from app.models.types import NormalizedEmail, Phone
```

**Response models** (`app/models/resource/responses.py`):
```python
"""
Resource response models.

Constants
---------
`RESOURCE_COLLECTION` is the canonical Firestore collection name for resource documents.
"""

from pydantic import BaseModel, ConfigDict, Field

from app.models.types import UtcDatetime

# Firestore collection name
RESOURCE_COLLECTION = "resources"
```

## Request Models (Base and Create)

Use `extra="forbid"` for request models to reject unknown fields:

```python
class ResourceBase(BaseModel):
    """
    Base resource model with common fields.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Resource name",
        examples=["My Resource"],
    )
    email: NormalizedEmail = Field(
        ...,
        description="Email address (auto-lowercased)",
        examples=["user@example.com"],
    )
    active: bool = Field(
        default=True,
        description="Whether the resource is active",
        examples=[True],
    )

    model_config = ConfigDict(extra="forbid")


class ResourceCreate(ResourceBase):
    """
    Model for creating a new resource.
    """
```

## Update Models

Make all fields optional for partial updates:

```python
class ResourceUpdate(BaseModel):
    """
    Model for updating an existing resource.
    """

    name: str | None = Field(
        None,
        min_length=1,
        max_length=100,
        description="Resource name",
        examples=["Updated Resource"],
    )
    active: bool | None = Field(
        None,
        description="Whether the resource is active",
        examples=[False],
    )

    model_config = ConfigDict(extra="forbid")
```

## Entity Models (Response)

Response models should NOT inherit from request base models with `extra="forbid"`. Use `serialize_by_alias=True` for models with field aliases like `$schema`:

```python
class Resource(BaseModel):
    """
    Complete resource model with metadata.

    Note: Does not inherit from ResourceBase to avoid extra="forbid" which is
    inappropriate for response models.
    """

    model_config = ConfigDict(populate_by_name=True, serialize_by_alias=True)

    schema_url: str | None = Field(
        default=None,
        alias="$schema",
        description="JSON Schema URL for this response",
        examples=["https://api.example.com/schemas/ResourceData.json"],
    )
    id: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="Unique identifier",
        examples=["resource-abc123"],
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Resource name",
        examples=["My Resource"],
    )
    active: bool = Field(
        default=True,
        description="Whether the resource is active",
        examples=[True],
    )
    created_at: UtcDatetime = Field(
        ...,
        description="Creation timestamp",
        examples=["2025-01-15T10:30:00.000Z"],
    )
    updated_at: UtcDatetime = Field(
        ...,
        description="Last update timestamp",
        examples=["2025-01-15T10:30:00.000Z"],
    )
```

## Response Convention

**Return resources directly** - do not use wrapper response models. This follows REST best practices:

```python
# Correct - return resource directly
@router.get("")
async def get_resource(...) -> Resource:
    return await service.get_resource(user_id)

# Wrong - do not use wrapper responses
@router.get("")
async def get_resource(...) -> ResourceResponse:
    return ResourceResponse(success=True, resource=resource)
```

POST endpoints return 201 with `Location` header. DELETE endpoints return 204 No Content.

## Field Requirements

Every field MUST have:
- `Field(...)` with `description` for OpenAPI documentation
- `examples=[...]` for per-field examples in Swagger/ReDoc

Example formats by type:
| Field Type | Example Format |
|------------|----------------|
| `str` | `examples=["value"]` |
| `int` | `examples=[123]` |
| `float` | `examples=[19.99]` |
| `bool` | `examples=[True]` |
| `UtcDatetime` | `examples=["2025-01-15T10:30:00.000Z"]` |
| `list[str]` | `examples=[["item1", "item2"]]` |
| `list[Model]` | **Omit examples** (nested schema auto-documents via `$ref`) |
| `EmailStr` | `examples=["user@example.com"]` |
| `T \| None` | Provide example for `T`; omit `None` |

## Shared Type Aliases

Use predefined types from `app/models/types.py`:
- `UtcDatetime` for timestamps with consistent `.000Z` milliseconds format
- `NormalizedEmail` for auto-lowercased emails
- `Phone` for E.164 phone numbers
- `LanguageCode` for ISO 639-1 codes
- `CountryCode` for ISO 3166-1 alpha-2 codes

## Naming Conventions

| Purpose | Pattern | Example |
|---------|---------|---------|
| Base class (internal) | `{Resource}Base` | `ProfileBase` |
| Create request | `{Resource}Create` | `ProfileCreate` |
| Update request | `{Resource}Update` | `ProfileUpdate` |
| Full entity (response) | `{Resource}` | `Profile` |

## Serialization

Use Pydantic v2 methods:
- `.model_dump()` instead of deprecated `.dict()`
- `.model_dump(exclude_unset=True)` for partial updates
- `.model_validate()` instead of deprecated `.parse_obj()`

## Model Config Options

Common `ConfigDict` settings:
- `extra="forbid"` - Reject unknown fields (request models only)
- `populate_by_name=True` - Allow field name or alias in input
- `serialize_by_alias=True` - Use aliases in output (for `$schema` etc.)
- `from_attributes=True` - Construct from ORM-like objects
