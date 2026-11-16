---
name: hex-capability-adapter
description: Use when implementing an `ICan<Verb>` capability against a real external system — the adapter under `infrastructure/<technology>/` wrapping an SDK client, an HTTP gateway or a pure-CPU library, translating the library's own errors into `exception-catalog` classes. Not aggregate CRUD — that is `hex-persistence` or `hex-store-repository`; the protocol is `hex-domain-ports`.
paths: ["**/infrastructure/**"]
---

# Hex — Capability Adapter (infrastructure)

Produces one adapter class that adapts a domain `ICan<Verb>` capability protocol to a concrete external
system. It is the last place the external library's own exceptions exist: translation happens here,
into the classes `exception-catalog` owns.

## When to use vs. neighbours

- Aggregate-root CRUD over a relational store → `hex-persistence`, not this skill.
- Aggregate-root persistence on a key-value or document store, or an index kept beside it → `hex-store-repository`; an injected SDK client alone does not make something a capability.
- The `ICan<Verb>` protocol file this adapter satisfies → `hex-domain-ports`.
- The obligations the adapter's settings class must meet → `python-settings`, its name and prefix → `naming`; the HTTP gateway's own is shown here, beside it.
- The lifetime and declaration-order rules the adapter's binding follows, and the base composition root it merges into → `hex-wiring`; the binding itself is shown here, beside the adapter.
- The catalogue exception classes the SDK's own errors are translated into → `exception-catalog`.
- The undo a compensating handler calls on this adapter (`delete` beside `upload`) → an ordinary method that raises on failure, declared on a port by `hex-domain-ports`; the handler-side guard that tolerates its failure is `hex-application`'s (Compensation).
- An in-memory test stand-in for this capability (the `Fake<Capability>` flavor) → `hex-test-application-handler`.
- Testing the real adapter — containerized backend, HTTP over a stub transport, or pure CPU → `hex-test-capability-adapter`.
- A token verifier — its port, its adapter and the dependency that resolves it → `hex-restapi-auth`; it is a pure-CPU adapter in this skill's sense, bound there.
- The `infrastructure/<technology>/` folder, the module name and the class name → `hex-conventions` and `naming`.

## Template — httpx2, pydantic-settings, dishka

### Template — async HTTP gateway (httpx2)

In `infrastructure/http/http_foo_classifier.py`, with its settings class beside it:

```python
import httpx2

from myapp.domain.exceptions import (
    UpstreamError,
    ValidationError,  # only where the upstream judges input the caller can correct
)
from myapp.domain.foos import Foo, FooKind

from .foo_classifier_settings import FooClassifierSettings

__all__ = ["HttpFooClassifier"]


class HttpFooClassifier:
    def __init__(self, client: httpx2.AsyncClient, settings: FooClassifierSettings) -> None:
        self._client = client
        self._base_url = settings.base_url
        self._api_key = settings.api_key.get_secret_value()  # only where the upstream takes a credential

    async def classify(self, foo: Foo) -> FooKind:
        foo_id = str(foo.id)
        try:
            response = await self._client.post(
                f"{self._base_url}/classifications",
                json={"name": foo.name},
                headers={"Authorization": f"Bearer {self._api_key}"},  # only where the upstream takes a credential
            )
            response.raise_for_status()
        except httpx2.HTTPStatusError as exc:
            status = exc.response.status_code
            # only where the upstream judges input the caller can correct
            if status == 400:
                raise ValidationError("foo classifier rejected foo", {"foo_id": foo_id, "status": status}) from exc
            raise UpstreamError("foo classifier failed", {"foo_id": foo_id, "status": status}) from exc
        except httpx2.HTTPError as exc:
            raise UpstreamError("foo classifier unreachable", {"foo_id": foo_id}) from exc
        try:
            return FooKind(response.json()["kind"])
        except (KeyError, TypeError, ValueError) as exc:
            raise UpstreamError("foo classifier returned a malformed body", {"foo_id": foo_id}) from exc
```

Where the call returns a value, a `200` is not a result until its body has been read, and whatever the
conversion to the domain type raises is the upstream's fault: a body that is not JSON, a missing field, a
value the domain type refuses — an enum's `ValueError` here, a value object's own `ValidationError`, a
decimal's `InvalidOperation` — arrives as `UpstreamError` from a translated scope of its own (rule 8). A
call that returns nothing reads no body.

A call the service makes on its own behalf — a notification — maps every status to the fallback, as
rule 9 does the adapter's own credential.

Its settings class, in `infrastructure/http/foo_classifier_settings.py` beside it — the module named for
the class (`python-packaging`). The adapter reads the base URL and, where the upstream takes one, the
credential; the composition root reads the timeout when it builds this integration's own
`httpx2.AsyncClient` (`hex-wiring`).

```python
from pydantic import SecretStr  # only where the upstream takes a credential
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["FooClassifierSettings"]


class FooClassifierSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MYAPP_FOO_CLASSIFIER_",
        env_file=".env",  # only where the project keeps a dotenv file for development
        extra="ignore",
        hide_input_in_errors=True,
    )

    base_url: str
    api_key: SecretStr  # only where the upstream takes a credential
    timeout_seconds: float
```

**A timeout is a per-integration decision.** It is set from the integration's own observed latency plus
headroom, and bounded above by what the caller can wait for — a request-path adapter whose timeout
exceeds the app's own request timeout can never fire usefully. What the template does fix is that the
timeout is a **settings field**, read once by the composition root and injected — never a constant
hardcoded inside the adapter. It is a tunable with no single right value, so it carries no default
(`python-settings` rule 5).

A pure-CPU adapter over a third-party library — a parser, a renderer, a verifier — has no client to
inject, and settings only where it has something to configure; it still translates the library's own
failure into a catalogue exception and returns a domain type. Work the standard library can do is domain
logic, not an adapter (`hex-domain-ports`).

### The composition-root binding — dishka

The adapter's binding is an add-on to `hex-wiring`'s base composition root, merged as `CONTAINER.md`
says. It is process-lifetime — an adapter keeps no state across calls (rule 12).

The HTTP gateway: the settings provider, and one factory that builds this integration's own client — the
timeout is read here, where the client is built — hands it to the adapter, binds the adapter to its port
by its return type and closes the client after its yield. A second integration adds a factory of its
own, so no integration's timeout or retry policy reaches another's calls.

```python
from collections.abc import AsyncIterator

import httpx2
from dishka import Provider, Scope, provide

from myapp.domain.foos import ICanClassifyFoos
from myapp.infrastructure.http import FooClassifierSettings, HttpFooClassifier


class SettingsProvider(Provider):
    scope = Scope.APP

    @provide
    def foo_classifier_settings(self) -> FooClassifierSettings:
        return FooClassifierSettings()


class InfrastructureProvider(Provider):
    scope = Scope.APP

    @provide
    async def foo_classifier(self, settings: FooClassifierSettings) -> AsyncIterator[ICanClassifyFoos]:
        async with httpx2.AsyncClient(timeout=settings.timeout_seconds) as client:
            yield HttpFooClassifier(client=client, settings=settings)
```

## Other bindings

- **An object store.** The bucket is read from settings, the SDK's error codes map to
  `NotFoundError`/`ValidationError` with an `UpstreamError` fallback, and one adapter may satisfy the
  store port and the fetch port together (`AnyOf`).
- **Another vendor SDK for the same capability** — a different mail provider or model API.
  The client type, its exception family and the code/status vocabulary change together; the port
  conformance, the inject-client-plus-settings constructor, the translate-before-it-escapes rule and the
  context keys are unchanged. Budget the swap as one new error map, not a new adapter shape.
- **A different async HTTP client** — `httpx`, the predecessor, with the same API under the old import,
  or `aiohttp`, stubbed in its test with `aioresponses`. The call and the exception family change; the
  status-to-catalogue mapping, the fallback and the thinness rules do not.
- **A sync-only SDK inside an async service.** The port stays async and the adapter runs the blocking
  call on a worker thread (`asyncio.to_thread`) — calling it inline blocks the event loop for every other
  request. Translation, context and no-instance-state are unchanged.

## Rules

### Form

1. **One adapter class per module**, named for the concrete technology it wraps (`HttpFooClassifier`, not
   `FooClassifier`), so two implementations of one port can coexist. Module structure is
   `python-packaging`'s; the names are `naming`'s.
2. **The adapter satisfies its protocol structurally** — it neither inherits nor imports it
   (`hex-architecture` rule 7).
3. **Method signatures match the protocol exactly** — parameter names, keyword-only markers and
   async/sync mode included. A near-match satisfies no structural check and fails at the injection site,
   not at the adapter.
4. **The module's directory is the technology it wraps** — `hex-conventions` block A's adapter token —
   never the domain concern it serves.

### Constructor

5. **The client and the settings arrive by injection, never by construction.** Both are built once by
   the composition root (`hex-wiring`) and handed in; a method that builds its own client
   (`httpx2.AsyncClient(...)`, an SDK's own client factory) defeats connection pooling and cannot be replaced in a
   test without patching the library. A client carries one upstream's timeout and whatever is set on it,
   so a second upstream gets a client of its own, built from its own settings and bound so neither
   adapter can be handed the other's — a second factory for the same client type replaces the first
   rather than joining it.
6. **Stash the fields the methods use, not the settings object** — unless several methods read several
   fields. What each method reads is then visible in the constructor; the settings object itself arrives
   whole, by type (`hex-wiring`).
7. **Where the adapter holds a secret, it is unwrapped once, in the adapter's constructor, and kept out
   of the URL** — `python-settings` rule 9.

### Exception translation

8. **The library's exception type never escapes the adapter, and neither does a bare `Exception`** — each
   is raised as a catalogue class `from` its cause (`exception-catalog` rule 8). No SDK error, HTTP status
   error or parse error crosses into `application/` or an entrypoint — the application layer catches only
   `MyappError`. Where the request does not say which external errors a method raises, derive the mapping
   from the library's documented exception family: the specific cases are judgement, the broad
   catch-and-translate fallback (rule 9) is not — no method is left able to raise an untranslated
   external exception. Nor does the upstream's vocabulary escape: the domain type's values are the
   domain's own, the adapter maps the upstream's labels onto them wherever the two differ, and a label it
   cannot map is a malformed body.
9. **Which class, the fallback, `context` and never swallowing are `exception-catalog`'s rules 9–12, 14
   and 15, unchanged.** In an adapter: `ValidationError` only when the upstream rejected the inputs as
   malformed, never when the domain type refuses what the upstream sent back; `NotFoundError` when the
   object does not exist; the fallback `UpstreamError` for the rest — a network fault, a 5xx, an unmapped
   code, the upstream refusing the adapter's own credential; `UnauthorizedError` only in an adapter
   verifying the caller's credential (`hex-restapi-auth`); a failed undo is stopped in the calling
   handler (`hex-application`, Compensation), never here.

### No business logic, no logging

10. **Adapters are thin.** No retries, no caching, no batching, no domain reasoning. Retry and backoff
    belong to the client's own policy (configured where the client is built) or to a dedicated wrapper
    class, so that the adapter stays one call wide and its failure modes stay readable.
11. **An adapter never logs.** Not the call, not the failure: the central error handler owns failure logs
    and the calling handler owns success logs, so a line here is a second entry for one event.
12. **No instance state across calls** beyond constructor-injected handles. An adapter is then safe to
    bind at process lifetime and share across concurrent requests.

### Compensating-transaction contract

13. **A capability whose write a handler compensates exposes the undo beside the forward operation** (`hex-application`, Compensation, decides which writes need one): a storage adapter has `upload` *and* `delete`; a publisher that supports retraction has `publish` *and* `retract`; a write nothing compensates has no undo. The catch-and-undo logic lives in the application handler (`hex-application`, Compensation), not in the adapter. The adapter's job is to make the undo callable; like every other method it raises a catalogue exception when it fails, and the handler decides whether that failure may be tolerated.

## Inlined typing / import rules

- Domain imports absolute (`from myapp.domain.foos import Foo, FooKind` — the domain types the signatures name). **Never import the capability protocol the adapter satisfies** (`ICanStoreFoos`, `ICanClassifyFoos`, …; rule 2). Sibling modules within the same `infrastructure/<adapter>/` package use relative imports (`from .foo_classifier_settings import FooClassifierSettings`).
- No `from __future__ import annotations`. Full annotations on every method.
- `X | None` over `Optional`. `Mapping[K, V]` / `Sequence[T]` (from `collections.abc`) for read-only views.
- **A raw SDK value typed `Any` is narrowed with `cast`, never silenced.** An SDK return that mypy sees as `Any` (an untyped client method, a body read the SDK does not type) flowing into a typed protocol return is a `[no-any-return]`/`[return-value]` error — fix it with `cast(<protocol-return-type>, …)` at the boundary, the same way `hex-restapi-auth`'s `dependency-injector` binding casts a verifier resolved by attribute name. An adapter can always restate the vendor type, so an inline ignore never meets `python-style`'s last-resort test here.
- SDK types stay inside the adapter; method signatures use domain types or primitives only.
- No `Any` except at the immediate raw-SDK-payload boundary (e.g. `payload: dict[str, Any] = response.json()` — convert to the domain type on the next line).

## Package wiring

For package wiring, see `python-packaging`; for infrastructure placement, see `hex-architecture`.

## Hard stops

- The adapter is asked to carry relational aggregate CRUD — a table, the statements against it and the
  migration that ships it → stop, that is a repository and not a capability; use `hex-persistence`, or
  `hex-store-repository` for an aggregate held in a key-value or document store.
