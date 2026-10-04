---
name: advanced-alchemy
description: "Auto-activate for advanced_alchemy, alembic/, SQLAlchemyAsyncRepositoryService, SQLAlchemyAsyncConfig, repository_type, service_class, filters, or storage. Not for raw SQLAlchemy without Advanced Alchemy."
---

# Advanced Alchemy

## Code Style Rules

- Use `Mapped[...]` for columns and `T | None` for optional fields.
- Keep business transformations in service lifecycle hooks.
- Prefer the inner `Repo` service pattern and `advanced_alchemy.*` imports.
- Use `from __future__ import annotations` when it matches the project; 1.11
  supports it in model modules.

## Match-Your-Framework — read first

advanced-alchemy ships first-party extensions for five web frameworks. If your project uses one of these, **jump directly to the matching integration guide and skip the others**:

- **Litestar** — `SQLAlchemyPlugin` with full DI, session store, CLI. The rest of this SKILL.md covers Litestar by default; also see [`references/litestar_plugin.md`](references/litestar_plugin.md).
- **FastAPI** → [`references/fastapi-integration.md`](references/fastapi-integration.md) — `AdvancedAlchemy(config=..., app=app)`, `Depends(alchemy.provide_session())` DI, `provide_service()`/`provide_filters()`, Alembic CLI via `assign_cli_group`.
- **Flask** → [`references/flask-integration.md`](references/flask-integration.md) — `AdvancedAlchemy(config=..., app=app)` or `init_app()` factory, pull-based `alchemy.get_sync_session()`, async-via-portal.
- **Sanic** → [`references/sanic-integration.md`](references/sanic-integration.md) — `AdvancedAlchemy(sqlalchemy_config=..., sanic_app=app)` (note: `sqlalchemy_config=` kwarg, not `config=`), sanic-ext DI, `request.ctx` sessions.
- **Starlette** → [`references/starlette-integration.md`](references/starlette-integration.md) — `AdvancedAlchemy(config=..., app=app)`, `request.state` session access, lifespan wrapping.

Transaction configuration is framework-specific. Litestar uses
`before_send_handler`; FastAPI, Flask, Starlette, and Sanic use
`commit_mode="manual"`, `"autocommit"`, or
`"autocommit_include_redirect"`. Read the matching framework guide, then
[`references/commit-modes.md`](references/commit-modes.md) and
[`references/multi-database.md`](references/multi-database.md).

The rest of this SKILL.md covers framework-agnostic topics: base classes, repositories, services, filters, custom types, caching, replicas, operations, and Alembic migrations.

## Overview

Advanced Alchemy is NOT a raw ORM — it is a **service/repository layer** built on top of SQLAlchemy 2.0+ with opinionated base classes, audit mixins, and deep framework integrations (Litestar, FastAPI, Flask, Starlette, Sanic). It provides:

- **Base models** with automatic `id`, `created_at`, `updated_at` fields
- **Repository pattern** for type-safe async CRUD
- **Service layer** with lifecycle hooks (`to_model_on_create`, `to_model_on_update`, `to_model_on_upsert`, `to_model_on_delete`)
- **Framework plugins** for automatic session/transaction management
- **Custom types**: `EncryptedString`, `EncryptedText`, `PasswordHash`, `FileObject`, `StoredObject`, `DateTimeUTC`, `GUID`, `Bool`, `JsonB`, `Vector`, `TOTPSecret`, `OneTimeCode`
- **Alembic integration** for migrations via CLI

## Quick Reference

### Base Classes

| Base Class | PK Type | Audit Columns | When to Use |
| --- | --- | --- | --- |
| `UUIDAuditBase` | UUID v4 | `created_at`, `updated_at` | Default choice for most models |
| `UUIDBase` | UUID v4 | None | Lookup tables, tags, no audit needed |
| `UUIDv7AuditBase` / `UUIDv7Base` | UUID v7 | `created_at`, `updated_at` / None | Time-ordered IDs when `uuid-utils` is installed or Python supplies UUIDv7 |
| `UUIDv6AuditBase` / `UUIDv6Base` | UUID v6 | `created_at`, `updated_at` / None | Time-ordered UUIDv6 IDs |
| `BigIntAuditBase` / `BigIntBase` | BigInt auto-increment | `created_at`, `updated_at` / None | Legacy systems, integer PKs |
| `NanoIDAuditBase` / `NanoIDBase` | NanoID string | `created_at`, `updated_at` / None | URL-friendly short IDs |
| `IdentityAuditBase` / `IdentityBase` | database identity | `created_at`, `updated_at` / None | Native IDENTITY columns |
| `DefaultBase` | None (define yourself) | None | Custom or composite primary keys with AA table naming |
| `SQLQuery` | None | None | Custom mapped read-only SQL query projections |

### Repository Pattern

| Repository | Purpose |
| --- | --- |
| `SQLAlchemyAsyncRepository[Model]` / `SQLAlchemySyncRepository[Model]` | Standard async/sync CRUD |
| `SQLAlchemyAsyncSlugRepository[Model]` / `SQLAlchemySyncSlugRepository[Model]` | CRUD + slug generation helpers |
| `SQLAlchemyAsyncQueryRepository` / `SQLAlchemySyncQueryRepository` | Complex read-only queries (no `model_type`) |

### Service Layer

| Service | Purpose |
| --- | --- |
| `SQLAlchemyAsyncRepositoryService[Model]` / `SQLAlchemySyncRepositoryService[Model]` | Full CRUD with lifecycle hooks |
| `SQLAlchemyAsyncRepositoryReadService[Model]` / `SQLAlchemySyncRepositoryReadService[Model]` | Read-only (`get_many`, `get`, `count`, `exists`) |
| `SQLAlchemyAsyncQueryService` / `SQLAlchemySyncQueryService` | Service wrapper around arbitrary SQL queries |

Key lifecycle hooks: `to_model_on_create`, `to_model_on_update`, `to_model_on_upsert`, `to_model_on_delete`.

## Custom Types

| Type | Purpose | Notes |
| --- | --- | --- |
| `FileObject` / `StoredObject` | Object storage with lifecycle hooks | Tracks file state across session; auto-deletes on row delete via `StoredObject` tracker; use `FileObjectList` for multi-file JSON arrays |
| `PasswordHash` | Hashed password storage | Supports Argon2, Passlib, and Pwdlib backends; returns `HashedPassword` with `.verify()` and `.verify_and_update()` |
| `EncryptedString` / `EncryptedText` | Transparent encryption at rest | Supports `FernetBackend` (client-side) and `PGCryptoBackend` (server-side); pass a stable key explicitly |
| `GUID` | Cross-dialect UUID column | Native `UUID` on PostgreSQL/DuckDB/CockroachDB, `BINARY(16)` or `CHAR(32)` fallback elsewhere; pair with `UUIDv7AuditBase` / `UUIDv6AuditBase` for time-sortable UUIDs |
| `DateTimeUTC` | Timezone-aware UTC datetime | Stores as UTC; normalizes or raises on naive datetimes |
| `Bool` | Dialect-aware boolean | Uses Oracle 23ai native `BOOLEAN` when SQLAlchemy exposes it; falls back to stock SQLAlchemy `Boolean` |
| `JsonB` | Dialect-aware JSON / JSONB | Uses `JSONB` on PostgreSQL/CockroachDB, `JSON` on other backends, `BLOB` with `OSON` on Oracle |
| `Vector` | Dialect-aware vector storage and distance operators | Oracle 23ai `VECTOR`, PostgreSQL/CockroachDB `pgvector`, JSON fallback without distance operators |
| `TOTPSecret` / `OneTimeCode` | MFA and single-use code storage | `TOTPSecret` encrypts shared secrets and returns `TOTPProvider`; `OneTimeCode` hashes codes with TTL/attempt tracking and returns `HashedOneTimeCode` |

## Repository Service Layer

`SQLAlchemyAsyncRepositoryService` is the primary service base class. Key behaviors:

- **Dict-to-model conversion**: pass raw `dict` to `create()`, `update()`, `upsert()` — the service converts via `to_model_on_create` / `to_model_on_update` lifecycle hooks before persistence
- **Bulk operations**: `create_many(data)`, `update_many(data)`, `upsert_many(data)`, `delete_many(item_ids)` — batched in a single transaction; `delete_many()` accepts raw primary keys, composite-key tuples/dicts, model instances, or mixed lists
- **Lifecycle hooks**: `to_model_on_create`, `to_model_on_update`, `to_model_on_upsert` — override to transform input data, hash passwords, normalize strings, etc.

## Mixins

| Mixin | Fields Added | When to Use |
| --- | --- | --- |
| `AuditColumns` | `created_at`, `updated_at` | Add timestamps to a model with a custom primary key |
| `SlugKey` | unique `slug` column | Pair with a slug repository; the mixin does not generate values |
| `UniqueMixin` | `as_unique_async()` / `as_unique_sync()` | Session-cached select-or-create after defining `unique_hash()` and `unique_filter()` |
| `SentinelMixin` | hidden `sa_orm_sentinel` column | Deterministic ordering for SQLAlchemy bulk inserts; not optimistic locking |

## Litestar Integration

Use `SQLAlchemyPlugin` (composite of `SQLAlchemyInitPlugin` + `SQLAlchemySerializationPlugin`) for full integration:

- **`SQLAlchemyPlugin`**: registers engine/session providers, a Litestar
  `before_send` hook, and ORM type encoders in one call
- **`SQLAlchemyDTO`**: generates Litestar DTOs directly from ORM models with `include`/`exclude` field control
- **Type encoders**: automatic serialization of `datetime`, `UUID`, `Decimal`, `Enum`, and custom column types
- **Exception handling**: `set_default_exception_handler=True` (the default)
  registers `RepositoryError` handling through the plugin

<workflow>

## Workflow

### Step 1: Define the Model

Choose the appropriate base class from the quick reference table. Use `UUIDAuditBase` unless you have a specific reason not to. Define columns with `Mapped[]` typing.

### Step 2: Create the Repository

Create a repository class with `model_type` set to your model. Use `SQLAlchemyAsyncRepository` for standard CRUD, `SQLAlchemyAsyncSlugRepository` if the model uses `SlugKey`.

### Step 3: Build the Service

Create a service class with an inner `Repo` class. Set `match_fields` for upsert logic. Add lifecycle hooks (`to_model_on_create`, `to_model_on_update`) for business logic transformations.

### Step 4: Wire into Framework

Use the framework plugin (Litestar, FastAPI, Flask, Sanic) to inject sessions and register the service as a dependency.

### Step 5: Generate Migration

With Litestar, run `litestar database make-migrations -m "description"` and
then `litestar database upgrade`. With the standalone CLI, put the required
config option before the command:
`alchemy --config path.to.config make-migrations -m "description"`.

</workflow>

<guardrails>

## Guardrails

- **Always use the service layer for business logic** — never put validation, hashing, or transformation logic directly in route handlers or repositories
- **Repositories are for data access only** — no business rules, no side effects beyond database operations
- **Never bypass the service layer** to call repository methods directly from handlers
- **Always set `match_fields`** on services that use `upsert()` to avoid duplicate-key errors
- **Use `schema_dump()` / `schema_dump_config` for explicit dump behavior** — services already convert Pydantic/msgspec/attrs/dataclass inputs during model conversion
- **Prefer `UUIDAuditBase`** as default base class — only deviate when you have a concrete reason
- **Use `advanced_alchemy.*` imports** — the old `litestar.plugins.sqlalchemy` paths are deprecated
- **Pass stable keys to `EncryptedString` and `EncryptedText`.** Omitting
  `key=` emits a 1.11 deprecation warning and produces data that cannot survive
  a process restart.
- **Use `get_many()` and `get_many_and_count()`.** `list()` and
  `list_and_count()` are deprecated until 2.0.

</guardrails>

<validation>

### Validation Checkpoint

Before delivering code, verify:

- [ ] Model inherits from an Advanced Alchemy base class (not raw `DeclarativeBase` from SQLAlchemy)
- [ ] All columns use `Mapped[]` type annotations
- [ ] Service has an inner `Repo` class with `model_type` set
- [ ] Business logic lives in service lifecycle hooks, not in route handlers
- [ ] Imports come from `advanced_alchemy.*`, not deprecated paths
- [ ] Encrypted columns receive a stable explicit key
- [ ] New code uses `get_many()` / `get_many_and_count()`, not deprecated list aliases

</validation>

<example>

## Example

A complete `Tag` entity with model, repository, and service:

```python
"""Tag domain — model, repository, and service."""

from advanced_alchemy.base import UUIDAuditBase
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import ModelDictT, SQLAlchemyAsyncRepositoryService
from sqlalchemy.orm import Mapped, mapped_column


class Tag(UUIDAuditBase):
    """Tag model with audit trail."""

    __tablename__ = "tag"

    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None] = mapped_column(default=None)


class TagRepository(SQLAlchemyAsyncRepository[Tag]):
    """Data access for tags."""

    model_type = Tag


class TagService(SQLAlchemyAsyncRepositoryService[Tag]):
    """Business logic for tags."""

    class Repo(SQLAlchemyAsyncRepository[Tag]):
        model_type = Tag

    repository_type = Repo
    match_fields = ["name"]

    async def to_model_on_create(self, data: ModelDictT[Tag]) -> ModelDictT[Tag]:
        """Normalize tag name before creation."""
        if isinstance(data, dict) and "name" in data:
            data["name"] = data["name"].strip().lower()
        return data
```

</example>

---

## References Index

> **Choosing between `advanced-alchemy` and `sqlspec`:** `advanced-alchemy` (this skill) gives you an opinionated ORM service layer with `UUIDAuditBase`, lifecycle hooks, repository / service / Alembic integration, and `OffsetPagination[T]` out of the box — pick it when you want a complete CRUD surface with attribute-style row access and you're happy inside the SQLAlchemy ecosystem. `sqlspec` gives you direct SQL control, 15+ driver adapters (asyncpg, oracledb, DuckDB, BigQuery, SQLite, and more), Arrow-native result streams for analytics, and a builder API when you need it — pick it when you want explicit SQL, heterogeneous database backends, or Arrow integration. Both skills integrate with Litestar via first-party plugins; see [`../sqlspec/SKILL.md`](../sqlspec/SKILL.md) for the raw-SQL / multi-adapter path.

For detailed guides and code examples, refer to the following documents in `references/`:

- **[Models](references/models.md)**
  Base classes, mixins, special types, relationships, PII tracking, and deferred loading.
- **[Repositories](references/repositories.md)**
  Async repository variants, configuration, slug repos, and query repos.
- **[Services](references/services.md)**
  Service layer, lifecycle hooks, composite services, filtering, and pagination.
- **[Litestar Plugin](references/litestar_plugin.md)**
  SQLAlchemy plugin config, DTOs, dependency injection, and session management.
- **[Migrations](references/migrations.md)**
  Alembic integration, CLI commands, metadata registry, and multi-database support.
- **[Types](references/types.md)**
  Complete catalog of custom column types: EncryptedString, FileObject, DateTimeUTC, GUID, PasswordHash, Bool, Vector, TOTPSecret, OneTimeCode, and more.
- **[Base Classes](references/bases.md)**
  Declarative base classes, UUID/BigInt/Nanoid variants, audit mixins, SlugKey, UniqueMixin, metadata registry, and custom base creation.
- **[Filters](references/filters.md)**
  Filter system, pagination, SearchFilter, CollectionFilter, BeforeAfter, OrderBy, LimitOffset, and frontend integration patterns.
- **[Framework Integrations](references/frameworks.md)**
  FastAPI, Flask, Starlette, and Sanic plugin setup, session management, and feature comparison across frameworks.
- **[Caching](references/caching.md)**
  Dogpile.cache integration, CacheConfig, CacheManager API, automatic cache invalidation via session events, version-based list cache keys, singleflight stampede protection, and serialization.
- **[Read Replicas](references/replicas.md)**
  Read/write routing, RoutingConfig, engine groups, RoundRobinSelector/RandomSelector, sticky-after-write consistency, context managers for explicit routing, and RoutingAsyncSessionMaker.
- **[Storage (obstore)](references/storage.md)**
  FileObject and StoredObject types, ObstoreBackend and FSSpecBackend configuration (S3, GCS, Azure, local), StorageRegistry, presigned URL generation, automatic file lifecycle via session tracker, and Pydantic integration.
- **[Operations, Listeners, Serialization](references/operations.md)**
  `OnConflictUpsert` / `MergeStatement` dialect-aware upsert building blocks, session event listeners (FileObject, cache invalidation, `touch_updated_timestamp`), and the msgspec-first `encode_json` / `decode_json` used across the library.

---

## Official References

- <https://github.com/litestar-org/advanced-alchemy/tree/v1.11.0/advanced_alchemy>
- <https://github.com/litestar-org/advanced-alchemy/blob/v1.11.0/docs/changelog.rst>
- <https://github.com/litestar-org/advanced-alchemy/tree/v1.11.0/tests>
- <https://github.com/litestar-org/advanced-alchemy/tree/v1.11.0/docs/usage>
- <https://docs.litestar.dev/2/release-notes/changelog.html>
- <https://docs.sqlalchemy.org/en/20/orm/quickstart.html>

## Shared Styleguide Baseline

- Use shared styleguides for generic language/framework rules to reduce duplication in this skill.
- [General Principles](../litestar-styleguide/references/general.md)
- [Python](../litestar-styleguide/references/python.md)
- [Litestar](../litestar-styleguide/references/litestar.md)
- Keep this skill focused on tool-specific workflows, edge cases, and integration details.
