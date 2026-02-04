---
name: data-structures
description: Python data structure conventions for this codebase. Apply when choosing between Pydantic models, dataclasses, and other data containers.
user-invocable: false
---

# Data Structure Conventions

Use Pydantic models or dataclasses instead of raw dictionaries or tuples.

## Quick Reference

| Use Case | Choice | Example |
|----------|--------|---------|
| Validation, serialization, API boundaries | Pydantic `BaseModel` | Request/response models |
| Simple internal data containers | `dataclass` | Internal DTOs |
| Immutable value objects, hashable keys | `dataclass(frozen=True)` | Cache keys, IDs |
| Configuration from environment | Pydantic `BaseSettings` | App settings |
| Performance-critical hot paths | `dataclass` | Lower overhead than Pydantic |

## Forbidden Patterns

| Pattern | Reason |
|---------|--------|
| Raw `dict` returns | No IDE support, no validation, error-prone |
| `tuple` returns | Positional access is unclear |
| `NamedTuple` | Only for backward compatibility when refactoring tuple returns |

---

## Pydantic Models

Use for validation, serialization, and API boundaries.

```python
# CORRECT - Pydantic model with Field descriptions
from pydantic import BaseModel, Field

class SearchResult(BaseModel):
    """A single search result from the retrieval system."""

    document_id: str = Field(description="Unique identifier for the document")
    content: str = Field(description="The matched text content")
    score: float = Field(ge=0.0, le=1.0, description="Relevance score")
    metadata: dict[str, str] = Field(default_factory=dict)

# INCORRECT - raw dictionary
def search(query: str) -> dict:  # No type safety, no validation
    return {"id": "123", "content": "...", "score": 0.95}
```

### When to Use Pydantic

- API request/response models
- Data requiring validation constraints (`ge`, `le`, `min_length`, etc.)
- Serialization to/from JSON
- External data boundaries (user input, file parsing, API responses)

---

## Configuration with Pydantic Settings

Use `pydantic_settings.BaseSettings` for environment-based configuration.

```python
# CORRECT - typed settings from environment
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment."""

    openai_api_key: str
    database_url: str
    debug: bool = False
    max_workers: int = 4

    model_config = {"env_prefix": "APP_"}

# Usage: reads APP_OPENAI_API_KEY, APP_DATABASE_URL, etc.
settings = Settings()
```

---

## Dataclasses

Use for simple internal data containers where validation isn't needed.

```python
# CORRECT - simple dataclass
from dataclasses import dataclass

@dataclass
class Point:
    """A 2D point."""
    x: float
    y: float

# CORRECT - frozen for immutability and hashing
@dataclass(frozen=True)
class UserId:
    """Immutable user identifier, safe for use as dict key."""
    value: int

# Can be used as dict key or in sets
cache: dict[UserId, User] = {}
```

### When to Use Dataclasses

- Internal data transfer objects
- Simple value containers
- When Pydantic overhead isn't justified
- When you need hashable objects (`frozen=True`)

---

## Decision Flow

```
Is the data from external source (API, user input, file)?
├── Yes → Use Pydantic BaseModel (validation + serialization)
└── No → Is serialization needed?
    ├── Yes → Use Pydantic BaseModel
    └── No → Is validation needed?
        ├── Yes → Use Pydantic BaseModel
        └── No → Is immutability/hashability needed?
            ├── Yes → Use dataclass(frozen=True)
            └── No → Use dataclass
```

## Examples

### Returning Multiple Values

```python
# INCORRECT - tuple return
def get_user_stats(user_id: int) -> tuple[int, float, str]:
    return (42, 0.95, "active")  # What do these values mean?

# CORRECT - dataclass return
@dataclass
class UserStats:
    """Statistics for a user."""
    post_count: int
    engagement_score: float
    status: str

def get_user_stats(user_id: int) -> UserStats:
    return UserStats(post_count=42, engagement_score=0.95, status="active")
```

### API Response Model

```python
# CORRECT - Pydantic for API boundaries
from pydantic import BaseModel, Field

class UserResponse(BaseModel):
    """API response for user data."""

    id: int = Field(description="User ID")
    name: str = Field(min_length=1, description="Display name")
    email: str = Field(description="Email address")
    is_active: bool = Field(default=True, description="Account status")

    model_config = {"extra": "forbid"}  # Reject unknown fields
```

### Immutable Cache Key

```python
# CORRECT - frozen dataclass as cache key
from dataclasses import dataclass
from functools import lru_cache

@dataclass(frozen=True)
class QueryKey:
    """Immutable key for query caching."""
    query: str
    top_k: int
    filters: tuple[str, ...]  # Use tuple, not list, for hashability

@lru_cache(maxsize=1000)
def cached_search(key: QueryKey) -> list[Result]:
    ...
```
