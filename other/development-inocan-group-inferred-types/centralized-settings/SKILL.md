---
name: centralized-settings
description: Centralized settings pattern for all configuration and environment variables. Use when adding or accessing settings, secrets, or config in code.
---

# Centralized Settings Pattern (Python)

All configuration and environment variables MUST be centralized in a single settings module. Never scatter `os.getenv()` or `os.environ` calls across the codebase.

## The Pattern

Use Pydantic BaseSettings for type-safe, validated configuration:

```python
# settings.py - Single source of truth
from pydantic import Field
from pydantic_settings import BaseSettings

DEFAULT_TIMEOUT_SECONDS = 30
DEFAULT_MODEL = "gpt-4"

class Settings(BaseSettings):
    # Type annotation + default + description + validation
    api_key: str | None = Field(
        default=None,
        description="API key for external service.",
    )
    timeout_seconds: int = Field(
        DEFAULT_TIMEOUT_SECONDS,
        description="Request timeout in seconds (>0).",
        gt=0,
    )
    model_name: str = Field(
        DEFAULT_MODEL,
        description="LLM model to use.",
    )

settings = Settings()
```

## Forbidden Patterns

```python
# BAD: Scattered os.getenv() calls
api_key = os.getenv("API_KEY")
timeout = int(os.getenv("TIMEOUT", "30"))
debug = os.getenv("DEBUG", "false").lower() == "true"

# BAD: os.environ dictionary access
database_url = os.environ["DATABASE_URL"]

# BAD: Inline defaults scattered in code
model = os.getenv("MODEL_NAME", "gpt-4")  # Why is this the default?

# BAD: Module-level env access
TIMEOUT = int(os.getenv("TIMEOUT", "30"))
```

## Required Pattern

```python
# GOOD: Import centralized settings
from myproject.settings import settings

async def call_api():
    timeout = settings.timeout_seconds  # Typed, validated
    api_key = settings.api_key           # Centralized

# GOOD: Import defaults for documentation
from myproject.settings import DEFAULT_TIMEOUT_SECONDS
```

## For Secrets

```python
# In settings.py - use secret manager
from myproject.secrets import get_secret

class Settings(BaseSettings):
    api_key: str | None = Field(
        default_factory=lambda: get_secret("API_KEY"),
        description="API key (from secret manager or env).",
    )
```

## Exceptions

1. **Test files** - May use `patch.dict(os.environ, ...)` for mocking
2. **CLI scripts** - May read env for `--prod/--local` switching, then use settings
3. **The settings.py file itself** - Obviously reads env vars

## Benefits

1. **Single source of truth** - All settings in one place
2. **Type safety** - Pydantic validates at startup
3. **Documentation** - Every setting has a description
4. **Validation** - Constraints catch config errors early
5. **IDE support** - Autocomplete works
6. **Testability** - Mock settings object, not scattered env vars
