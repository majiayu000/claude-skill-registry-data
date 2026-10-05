---
name: pydantic-settings-python
description: >-
  Use for writing, reviewing, debugging, migrating, or testing Python
  application configuration built with pydantic-settings. Trigger for
  BaseSettings, SettingsConfigDict, environment names, dotenv, secrets
  directories, nested settings, CLI sources, custom source precedence, and
  secret-safe startup configuration. Do not use for ordinary Pydantic model
  validation, direct os.environ access in a small script, or external secret
  manager administration.
argument-hint: "[settings model, sources, precedence, or configuration failure]"
---

# Pydantic Settings source contracts

Treat settings as two ordered phases:

```text
configured sources -> candidate field values -> Pydantic validation -> Settings
```

`BaseSettings` is an application configuration boundary, not a global service
locator. Instantiate it once near the composition root and inject the validated
result.

## Workflow

1. Inspect the installed `pydantic-settings` and Pydantic versions separately.
   Do not infer one package's API from the other.
2. Define the settings ownership boundary, field types, required values,
   defaults, environment prefix, case policy, nested delimiter, dotenv policy,
   secrets source, CLI use, and extra-key behavior.
3. List every enabled source and its required priority. Use the documented
   defaults only when they match the application contract; otherwise implement
   and test `settings_customise_sources` explicitly.
4. Use nested Pydantic models for nested configuration. Use Pydantic secret
   types for sensitive values, but do not mistake redacted representation for
   storage or access control.
5. Keep I/O, network secret retrieval, and business logic out of validators.
   Add a narrow custom source only when built-in sources cannot express the
   input contract.
6. Test each source alone, source collisions, malformed values, missing
   required fields, unknown dotenv keys, nested overrides, secret redaction,
   and isolated environment/filesystem state.

## Canonical application boundary

```python
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    host: str
    port: int = 5432
    password: SecretStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_nested_delimiter="__",
        env_file=".env",
        extra="forbid",
    )

    debug: bool = False
    database: DatabaseSettings


def load_settings() -> Settings:
    return Settings()
```

Do not manually call `os.getenv` inside validators. Complex environment values
can use JSON decoding; nested keys override the matching top-level JSON subkey.
If a different grammar is required, make it explicit and reject ambiguity.

## Source priority

Default priority can include CLI arguments when enabled, then initializer,
environment, dotenv, secrets directory, and defaults. Verify current docs and
the installed signature before relying on the exact sequence. When policy says
environment must override initializer values, return the sources in that exact
order from `settings_customise_sources` and test a collision.

Never commit production secrets in `.env`, log a settings dump, or claim that
`SecretStr` encrypts data. Secrets-directory file permissions, rotation, and
provider authorization remain external controls.

Completion requires isolated tests of names, conversion, nesting, precedence,
extras, missing and malformed values, and secret exposure. Read [the source
model](references/settings.md), [settings recipes](references/recipes-settings.md),
and [verification matrix](references/testing.md) for nontrivial configurations.
