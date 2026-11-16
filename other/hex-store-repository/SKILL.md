---
name: hex-store-repository
description: Use when an aggregate is persisted on a nonrelational store — key-value, document or wide-column (redis, mongo, dynamo) — reached through an injected SDK client, or a derived index is kept beside the authoritative store. Produces the repository adapter satisfying the narrower port such a store answers, the store's settings class and connection factory, its container token and namespace keys, record mapping, and SDK-error translation. Not a relational `Table` and its migration (`hex-persistence`), and not a single-action `ICan<Verb>` port (`hex-capability-adapter`).
paths: ["**/infrastructure/**"]
---

# Hex — Store Repository

Produces one repository class that adapts a domain repository protocol to a client-style datastore — any store reached through an injected SDK client rather than the shared relational bootstrap. That sentence is the whole selection rule: **the store profile, not the vendor, decides that this skill applies.**

**A new vendor is its own `infrastructure/<kind>/` package under this skill — never a fork of it** (Rule 12). The pattern is fixed here (client injection, a fixed container token, record↔entity mapping, boundary translation via `exception-catalog`); the vendor rides in through three things and nothing else: the injected client type, the store's settings class and connection factory, and the SDK semantics that store documents. Key-value, document and wide-column stores are all one profile under that rule, and so is an index kept beside the authoritative store, which is why one skill serves them.

## When to use vs. neighbours

- The aggregate's store is the relational bootstrap store (SQLAlchemy/Postgres) → `hex-persistence`.
- The protocol file (`i_foo_repository.py`) → `hex-domain-ports`.
- A single-action `ICan<Verb>` port (not an aggregate's collection) → `hex-capability-adapter`.
- The obligations a settings class meets (environment namespace, secrets, construction only at a composition root) → `python-settings`; the store's own settings class is shown here, beside the adapter that reads it.
- The lifetime and declaration-order rules the repository's binding follows, and the base composition root it merges into → `hex-wiring`; the binding itself is shown here, beside the adapter.
- Which store profile a datastore is, and the client factory that profile names → `hex-conventions`.
- The catalogue exception an SDK error is translated into → `exception-catalog`.
- The obligations any store's data access meets — where a driver error is translated and what its
  context carries, the pure mapping, which of them bind on a store with no transactions or schema →
  `persistence`.
- An in-memory test stand-in for handler unit tests → `hex-test-application-handler`.
- The integration contract test that drives this adapter against the real store →
  `hex-test-repository-contract`.

## Template — redis-py, key-value form

One vendor is worked end to end so the shape is concrete; a document store (mongo, dynamo, a
key-value cache) differs only in the SDK's call names and its exception root. The worked aggregate is
`Baz` (`hex-domain-model`), a placeholder held by no other store, so the key-value store is its one
authoritative store (rule 1). A key-value store answers only reads by key, so the adapter satisfies an
`IBazRepository` that declares create, fetch by id and delete and nothing else (`hex-domain-ports`),
and lives in `redis/repositories/baz_repository.py` (`hex-conventions`' protocol-derived stem).

```python
import json
from uuid import UUID

from redis.asyncio import Redis
from redis.exceptions import RedisError

from myapp.domain.bazs import Baz
from myapp.domain.exceptions import NotFoundError, UpstreamError

__all__ = ["BazRepository"]

_KEY_PREFIX = "bazs"


def _key(id: UUID) -> str:
    return f"{_KEY_PREFIX}:{id}"


def _entity_to_record(baz: Baz) -> dict[str, str]:
    return {"id": str(baz.id), "name": baz.name}


def _record_to_entity(record: dict[str, str]) -> Baz:
    return Baz(id=UUID(record["id"]), name=record["name"])


class BazRepository:
    def __init__(self, client: Redis) -> None:
        self._client = client

    async def create(self, baz: Baz) -> None:
        try:
            await self._client.set(_key(baz.id), json.dumps(_entity_to_record(baz)))
        except RedisError as exc:
            raise UpstreamError(
                "store write failed",
                {"key": _key(baz.id)},
            ) from exc

    async def get_by_id(self, id: UUID) -> Baz:
        try:
            raw = await self._client.get(_key(id))
        except RedisError as exc:
            raise UpstreamError(
                "store read failed",
                {"key": _key(id)},
            ) from exc
        if raw is None:
            raise NotFoundError("Baz not found", {"id": str(id)})
        return _record_to_entity(json.loads(raw))

    async def delete(self, id: UUID) -> None:
        try:
            removed = await self._client.delete(_key(id))
        except RedisError as exc:
            raise UpstreamError(
                "store delete failed",
                {"key": _key(id)},
            ) from exc
        if removed == 0:
            raise NotFoundError("Baz not found", {"id": str(id)})
```

The key prefix is the adapter's container token, fixed in code (rule 5). The settings class the store's
connection factory reads, in `infrastructure/redis/redis_settings.py`, follows `python-settings`; the URL is a
secret because it carries the password.

```python
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["RedisSettings"]


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MYAPP_REDIS_",
        env_file=".env",  # only where the project keeps a dotenv file for development
        extra="ignore",
        hide_input_in_errors=True,
    )

    url: SecretStr
```

The connection factory, in `infrastructure/redis/connection.py`, is complete glue named for the
datastore, never a stub (`hex-conventions` block B):

```python
from redis.asyncio import Redis

from .redis_settings import RedisSettings

__all__ = ["create_baz_store_client"]


def create_baz_store_client(settings: RedisSettings) -> Redis:
    return Redis.from_url(settings.url.get_secret_value())
```

Another vendor changes the client class, its import and the constructor keywords, never the name or the
completeness.

The binding, an add-on to the base composition root in `hex-wiring`'s `CONTAINER.md`, which binds no
client store. A project that keeps `Baz` here merges the first two classes into the base's providers of
the same name and adds `BazsProvider()` to the `create_container` list: the settings provider, the client
built once by the connection factory above and closed after its yield,
and the repository bound to its port per operation, like every repository (`hex-wiring`).

```python
from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from myapp.domain.bazs import IBazRepository
from myapp.infrastructure.redis import RedisSettings, create_baz_store_client
from myapp.infrastructure.redis.repositories import BazRepository


class SettingsProvider(Provider):
    scope = Scope.APP

    @provide
    def redis_settings(self) -> RedisSettings:
        return RedisSettings()


class InfrastructureProvider(Provider):
    scope = Scope.APP

    @provide
    async def baz_store_client(self, settings: RedisSettings) -> AsyncIterator[Redis]:
        client = create_baz_store_client(settings)
        yield client
        await client.aclose()


class BazsProvider(Provider):
    scope = Scope.REQUEST

    baz_repository = provide(BazRepository, provides=IBazRepository)
```

## Other bindings

The key-value form is the one worked binding; every other client-style store is the same two files with
different SDK names. What changes, and what does not:

- **Document / wide-column stores** (mongo, dynamo, cassandra) — the key-value form, with the container
  token being a collection or table name instead of a key prefix, and the record a native document
  rather than a JSON string. Mapping helpers, translation and thinness are unchanged.
- **A search index — vector or full-text** (a vector store, OpenSearch) — a derived projection of the aggregate,
  never its authoritative store (Rule 1), so it satisfies a narrower port of its own shaped by what the
  index answers (`hex-domain-ports`) — typically an upsert, a query returning scored pairs (Rule 3) and a
  delete by the field the projection is keyed on. Client injection, the fixed container token,
  the entity rebuilt from the stored payload (Rule 8), translation and ownership are unchanged. An index
  inside the relational database (`pgvector`) is reached through the shared engine, so it is
  `hex-persistence`.
- **Object stores** (`s3`, gcs, azure blob) — a bucket is a container token like any other, but a blob
  is usually a single-action capability rather than an aggregate's collection, so check
  `hex-capability-adapter` first.

Each of these is one `infrastructure/<kind>/` package under the client-style profile (`hex-conventions`). None of them is a
second copy of this skill.

## Rules

### File layout

```
src/myapp/infrastructure/<store-kind>/   # the profile's kind token — infrastructure groups by technology
├── __init__.py
├── connection.py             # create_<store>_client(settings) — shown in the template above
├── <store-kind>_settings.py  # the store's settings class, in the module named for that class (RedisSettings → redis_settings.py) — shown in the template above
└── repositories/
    ├── __init__.py           # package wiring — python-packaging
    └── baz_repository.py     # this skill writes this file — the stem is the port's (`hex-conventions`)
```

### Form

1. **Names and module structure** follow `naming` and `python-packaging`; technology placement follows `hex-architecture` and `hex-conventions`. An aggregate has exactly one **authoritative** store, the one its writes go to (`persistence` rule 3) — unlike a capability port that several vendors may implement. A derived projection of the same aggregate on a second store (an index over `Foo`, see `## Other bindings`) sits behind its own narrower port, which is why the repository file stem is protocol-derived for client stores; see `hex-conventions`.
2. **The adapter satisfies its protocol structurally** (`hex-architecture` rule 7).
3. **Method signatures match the protocol exactly**, including async mode, keyword-only markers, and compound return shapes — a compound return is returned whole, never reduced to the entity with the rest discarded.

### Client & settings

4. **Inject the SDK client** — and the settings class only when rule 5 puts a value there. Both come from `containers.py`; the client is built once by the datastore's `create_<store>_client(settings)` factory and bound at process lifetime (`hex-wiring`). Never construct a client inline in a method, and never swap the injected client type for a different flavor of the SDK.
5. **The container token is fixed in code unless deployments differ.** The store's collection, key prefix, index or bucket name is a module constant in the adapter; it becomes a settings field, read once in `__init__`, only when deployments genuinely point one code base at different names. Stash nothing else the methods do not need.

### Records ↔ entities

6. **Private, pure mapping helpers** (`_record_to_entity` / `_entity_to_record`, and the key builder beside them; module functions by `python-packaging` rule 2, pure by `persistence` rule 8). Where rule 5 makes the prefix a setting, the key builder takes it as a parameter. IDs serialize as strings unless the SDK is UUID-native. **Annotate the SDK's own record type on the parameter and narrow with `isinstance` or `typing.cast`** — never `object` plus a row of `# type: ignore[attr-defined]`. An inline ignore is `python-style`'s last resort, for code the checker is wrong about that cannot be restated (its type suppressions); an adapter is the one place the vendor type is allowed, so the code can always be restated and there is nothing to silence.
7. **The record shape is `persistence` rule 10's**; the aggregate's access patterns and the store's semantics guide it.
8. **An entity is reconstructed from its own stored data.** Never substitute query-side values for stored ones (e.g. an entity rebuilt from a record is built from the record's fields, never patched with the key or the arguments the caller looked it up by); when the read path doesn't consume a stored field, omit it explicitly rather than faking it.

### Exception translation

9. **Boundary exception translation**, including SDKs without a single exception root, follows `exception-catalog`.
10. **Error selection** follows `exception-catalog`. An absent record on `get_by_id` is **not** an SDK error — detect it (a `None`, an empty result, a zero count) and fail.
11. **Exception context** follows `exception-catalog`; the templates show the store-specific inputs.

### Vendor & semantics

12. **Vendor semantics come from the SDK, not from this skill.** Query API, filter DSL, batching (its limit; the obligation is `persistence` rule 21), consistency options — read them from the SDK's own documentation. A **new vendor is its own package under this skill — never a fork of it** (the same way `hex-capability-adapter` serves every vendor with one skill).
13. **No provisioning** (`persistence` rule 14) — a bucket included.
14. **Ordering is explicit** (`persistence` rule 18) — an explicit sort key, or the store's documented result order.
15. **No retries, no caching, no domain reasoning, no logging.** Same thinness contract as every adapter (see `hex-capability-adapter`'s adapters-are-thin rules); a repository never logs by `persistence` rule 22, and which layer does is `hex-architecture`'s.

## Inlined typing / import rules

- Domain imports absolute (`from myapp.domain.bazs import Baz`); a sibling module of the store's package relative (`from ..redis_settings import RedisSettings`, where rule 5 puts a value there). **Never import the protocol the adapter satisfies** (`hex-architecture` rule 7).
- SDK types stay inside the adapter; method signatures use domain types or primitives only.
- Raw SDK payloads may be `dict[str, Any]` / `object` at the immediate boundary — convert to the domain type in the mapping helper, never return them.
- No `from __future__ import annotations`. Full annotations on every method.

## Package wiring

For `repositories/__init__.py`, follow `python-packaging`; package placement follows `hex-architecture`.

## Hard stops

- The aggregate's store is the relational bootstrap store — reached through a shared engine rather than an injected client — or the request is for SQL, SQLAlchemy or a `Table` → stop, use `hex-persistence`.
- Asked for atomicity across this store and another (two stores in one transaction) → stop, use `hex-application` for handler compensation; there is no cross-store transaction.
- The port is a single-action capability (`ICan<Verb>`), not an aggregate's collection → stop, use `hex-capability-adapter`.
