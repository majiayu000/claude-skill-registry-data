---
name: naming-conventions
description: Python naming conventions for this codebase. Apply when writing or reviewing Python code including functions, classes, variables, and constants.
user-invocable: false
---

# Python Naming Conventions

Apply these naming patterns when writing Python code in this repository.

## Quick Reference

| Element | Case | Pattern | Example |
|---------|------|---------|---------|
| Function | `snake_case` | `<verb>_<noun>` | `fetch_user`, `validate_input` |
| Async function | `snake_case` | `async_<verb>_<noun>` | `async_fetch_user` |
| Variable | `snake_case` | descriptive | `user_count`, `is_valid` |
| Class | `PascalCase` | noun | `SearchIndex`, `UserSession` |
| Constant | `SCREAMING_SNAKE_CASE` | + `Final` | `MAX_RETRIES: Final = 3` |
| Private | `_snake_case` | `_` prefix | `_cache`, `_validate` |
| Type alias | `PascalCase` | noun | `JsonValue`, `Embedding` |

## Functions and Methods

**Pattern**: `<verb>_<noun>` in `snake_case`

### Required Verb Prefixes

| Verb | When to use | Example |
|------|-------------|---------|
| `get_` | Retrieve data already in memory or from local cache | `get_user_by_id`, `get_config` |
| `fetch_` | Retrieve from external source (API, database, file system) | `fetch_api_data`, `fetch_remote_file` |
| `create_` | Instantiate a new object | `create_session`, `create_embedding` |
| `build_` | Construct a complex object step-by-step | `build_query`, `build_request` |
| `parse_` | Convert raw data into structured format | `parse_json`, `parse_response` |
| `validate_` | Check correctness, return bool or raise | `validate_input`, `validate_schema` |
| `calculate_` | Compute and return a value | `calculate_score`, `calculate_distance` |
| `transform_` | Convert from one format to another | `transform_coordinates`, `transform_response` |
| `is_` | Return boolean for state check | `is_valid`, `is_authenticated` |
| `has_` | Return boolean for existence check | `has_permission`, `has_feature` |

### Async Functions

**Required**: Prefix all async functions with `async_`

```python
# CORRECT
async def async_fetch_user(user_id: int) -> User:
    return await client.get(f"/users/{user_id}")

async def async_process_batch(items: list[Item]) -> list[Result]:
    return await asyncio.gather(*[async_process(item) for item in items])

# INCORRECT - missing async_ prefix
async def fetch_user(user_id: int) -> User:  # Bad: not clear await is needed
    ...
```

## Variables

**Pattern**: `snake_case` with descriptive names

### Required Patterns

| Variable type | Pattern | Examples |
|---------------|---------|----------|
| Counts | `<noun>_count` | `user_count`, `retry_count` |
| Maximums | `max_<noun>` | `max_retry_attempts`, `max_connections` |
| Minimums | `min_<noun>` | `min_threshold`, `min_batch_size` |
| Boolean state | `is_<adjective>` | `is_authenticated`, `is_valid` |
| Boolean existence | `has_<noun>` | `has_permission`, `has_feature` |
| Dimensions/sizes | `<noun>_dimensions` or `<noun>_size` | `embedding_dimensions`, `batch_size` |

### Forbidden Variable Names

Never use these generic names:

- `data`, `info`, `temp`, `tmp`, `val`, `value`
- `flag`, `result`, `response` (without qualifier)
- Single letters except in comprehensions: `[x for x in items]`

```python
# CORRECT
user_count = len(users)
max_retry_attempts = 3
embedding_dimensions = 768
is_authenticated = True
has_valid_license = check_license(user)

# INCORRECT
data = len(users)      # Too generic
n = 3                  # Single letter
```

## Classes

**Pattern**: `PascalCase` noun describing what it represents

```python
# CORRECT
class SearchIndex: ...
class EmbeddingModel: ...
class RetryPolicy: ...
class ValidationError: ...

# INCORRECT
class Search: ...          # Verb-like, unclear purpose
class EmbModel: ...        # Abbreviation
class DoValidation: ...    # Verb phrase
```

## Constants

**Pattern**: `SCREAMING_SNAKE_CASE` with `Final` type annotation

```python
from typing import Final

# CORRECT
MAX_RETRY_ATTEMPTS: Final = 3
DEFAULT_TIMEOUT_SECONDS: Final[float] = 30.0
SUPPORTED_FILE_FORMATS: Final[frozenset[str]] = frozenset({"json", "csv", "parquet"})

# INCORRECT
MaxRetries = 3              # Wrong case, missing Final
max_retry_attempts = 3      # Wrong case for constant
MAX_RETRY_ATTEMPTS = 3      # Missing Final annotation
```

## Private Members

**Pattern**: Single underscore `_` prefix for internal implementation

```python
class SearchService:
    def __init__(self, index: VectorIndex) -> None:
        self._index = index              # Private attribute
        self._cache: dict[str, Result] = {}  # Private attribute

    def search(self, query: str) -> list[Result]:  # Public API
        return self._perform_search(query)

    def _perform_search(self, query: str) -> list[Result]:  # Private method
        ...
```

## Type Aliases

**Pattern**: `PascalCase` describing the type

```python
# CORRECT
JsonValue = dict[str, Any] | list[Any] | str | int | float | bool | None
Embedding = list[float]
UserId = int

# INCORRECT
json_value = dict[str, Any] | list[Any] | str | int | float | bool | None  # Wrong case
```
