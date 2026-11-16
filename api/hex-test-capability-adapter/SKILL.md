---
name: hex-test-capability-adapter
description: Use when testing the infrastructure adapter behind an `ICan<Verb>` capability port in one of its three flavours — a containerized backend through testcontainers, an HTTP gateway driven over a real `httpx2` client whose transport is a stub, or a pure-CPU parser, renderer or verifier — asserting the SDK-error to catalogue-exception translation row by row. Not a repository adapter, which is `hex-test-repository-contract`, and not a token verifier, which is `hex-test-restapi-auth`.
---

# Hex Test — Capability Adapter

Consult `test-principles` for the testing constitution. Where this skill contradicts `test-principles`, the constitution wins.

Produces one test file per capability adapter. Catches what unit-level coverage cannot: real SDK exception shapes, real upstream wire format, real crypto/parsing behavior, and the SDK-exception-to-domain-exception translator's mapping. This is the capability-adapter analogue of `hex-test-repository-contract` for repository adapters.

## When to use vs. neighbours

- A new or modified adapter under `infrastructure/<adapter>/` (not `infrastructure/postgres/repositories/`) → this skill, in whichever of the three flavours the adapter is.
- A repository adapter, relational or client-store → `hex-test-repository-contract`, not this skill. The port tells them apart — `IFooRepository` there, `ICan<Verb>` here.
- The adapter under test itself → `hex-capability-adapter`; the `ICan<Verb>` protocol it satisfies → `hex-domain-ports`.
- A fake of this capability that the unit-test layer consumes → `hex-test-application-handler`. The fake's exception contract must match what the integration test pins here.
- A handler test that consumes such a fake → `hex-test-application-handler`.
- The rollback / container `conftest.py` itself — including "add a testcontainer fixture" → `hex-test-integration-setup` (one-shot). This skill only consumes the resource fixtures it defines.
- HTTP-layer (route + OpenAPI) → `hex-test-restapi-endpoint`.
- The token-verifier adapter's own test, and every other auth fixture → `hex-test-restapi-auth` (`UNIT.md` for the verifier); it is this skill's pure-CPU flavor bound to auth, and it lives there so auth is taught in one place.
- The catalogue exception the translator raises, or a new row in it → `exception-catalog`.
- Speed targets, the substitution ladder and marker rules → `test-principles`.
- A pure domain entity, value object, enum or service, with no adapter and no IO → `hex-test-domain`.
- A flat-layered service's `*_client.py` tested over a stub transport → `flat-test-service-client`, in the `pyhouse-flat` plugin; this skill's HTTP-gateway flavor is for an adapter behind an `ICan<Verb>` port, not for a flat client class.

## Template(s) — pytest, `httpx2.MockTransport` under a real `httpx2` client

The test file mirrors the adapter's module (`test-principles`, *Test naming*).

### Pick the flavor

- **Containerized backend.** Adapter speaks to a service that runs in a Testcontainer (an object store, a broker, a cache). Drives the real client against the real container; consumes the resource fixtures from the integration conftest. **Lives under `tests/integration/<adapter>/`.**
- **HTTP gateway over a stub transport.** Adapter speaks `httpx2` to a third-party HTTP API. Drives a real `httpx2.AsyncClient` whose transport is the stub and asserts the request shape on the way out (`test-principles`, *Intercepting HTTP* rule 5) and the translated response on the way back. The adapter code is real; only the network is replaced. Nothing runs, so it is a boundary unit test (`test-principles`) and **lives under `tests/unit/infrastructure/<adapter>/`**, clear of the integration tree's container and migration fixtures.
- **Pure-CPU.** Adapter does no IO — a parser, a renderer over in-memory bytes, a verifier. Stdlib + the real parsing / crypto library. No fixtures, no containers. **Lives under `tests/unit/infrastructure/<adapter>/`.**

The flavor mirrors the adapter's form in `hex-capability-adapter` — an SDK client, an HTTP gateway (the one it templates) or sync pure CPU. If two flavors are asked for in one file, split — one file per adapter, but `integration/` for a test that needs a running backend and `unit/` for everything else means a containerized adapter and a gateway or CPU adapter live in different roots regardless.

### Containerized backend

`tests/integration/<adapter>/`, in the file mirroring the adapter's module, driving the real SDK client against
a container the integration conftest starts (`hex-test-integration-setup`), in a per-test namespace
(`test-principles` reliability rule 2) whose worked instance is that skill's key-value add-on. One happy-path test per public method, observed by reading the
backend directly; one test per error code the adapter translates, each triggered where the backend
really reports it and asserting the catalogue class and its `context`; and the fallback — a client the
backend refuses, or one pointed at no backend — landing on the upstream error (rule 8). A reversing method the
compensation path calls (a delete) pins success on a key that was never written, where the backend
answers success for it, rather than a not-found it can never raise.

### HTTP gateway over a stub transport

```
tests/unit/infrastructure/<adapter>/
└── test_http_foo_classifier.py
```

```python
import json
import uuid
from collections.abc import AsyncIterator

import httpx2
import pytest
from pydantic import SecretStr  # only where the upstream takes a credential

from myapp.domain.exceptions import (
    UpstreamError,
    ValidationError,  # only where the upstream judges input the caller can correct
)
from myapp.domain.foos import Foo, FooKind
from myapp.infrastructure.http import FooClassifierSettings, HttpFooClassifier

_BASE_URL = "https://classifier.example"
_SETTINGS = FooClassifierSettings(
    base_url=_BASE_URL,
    api_key=SecretStr("test-key"),  # only where the upstream takes a credential
    timeout_seconds=5.0,
)


@pytest.fixture
def upstream_requests() -> list[httpx2.Request]:
    return []


@pytest.fixture
def upstream_answers() -> list[httpx2.Response | httpx2.TransportError]:
    return []


@pytest.fixture
async def client(
    upstream_requests: list[httpx2.Request], upstream_answers: list[httpx2.Response | httpx2.TransportError]
) -> AsyncIterator[httpx2.AsyncClient]:
    def answer(request: httpx2.Request) -> httpx2.Response:
        upstream_requests.append(request)
        if not upstream_answers:
            pytest.fail(f"no answer queued for {request.method} {request.url}")
        next_answer = upstream_answers.pop(0)
        if isinstance(next_answer, httpx2.TransportError):
            raise next_answer
        return next_answer

    async with httpx2.AsyncClient(transport=httpx2.MockTransport(answer)) as http_client:
        yield http_client


async def test_classify_happy_path(
    upstream_requests: list[httpx2.Request],
    upstream_answers: list[httpx2.Response | httpx2.TransportError],
    client: httpx2.AsyncClient,
) -> None:
    upstream_answers.append(httpx2.Response(200, json={"kind": "B"}))
    adapter = HttpFooClassifier(client=client, settings=_SETTINGS)

    kind = await adapter.classify(Foo(id=uuid.uuid4(), name="alpha"))

    assert kind == FooKind.B
    [request] = upstream_requests
    assert (request.method, str(request.url)) == ("POST", f"{_BASE_URL}/classifications")
    assert json.loads(request.content) == {"name": "alpha"}
    assert request.headers["Authorization"] == "Bearer test-key"  # only where the upstream takes a credential


@pytest.mark.parametrize("body", [b'{"kind": "UNKNOWN"}', b"not json"], ids=["unknown-kind", "not-json"])
async def test_classify_unparseable_body_raises_upstream(
    upstream_answers: list[httpx2.Response | httpx2.TransportError], client: httpx2.AsyncClient, body: bytes
) -> None:
    upstream_answers.append(httpx2.Response(200, content=body))
    adapter = HttpFooClassifier(client=client, settings=_SETTINGS)
    foo = Foo(id=uuid.uuid4(), name="alpha")

    with pytest.raises(UpstreamError, match="malformed body") as exc_info:
        await adapter.classify(foo)

    assert exc_info.value.context == {"foo_id": str(foo.id)}


# only where the upstream judges input the caller can correct
async def test_classify_400_raises_validation(
    upstream_answers: list[httpx2.Response | httpx2.TransportError], client: httpx2.AsyncClient
) -> None:
    upstream_answers.append(httpx2.Response(400))
    adapter = HttpFooClassifier(client=client, settings=_SETTINGS)
    foo = Foo(id=uuid.uuid4(), name="alpha")

    with pytest.raises(ValidationError) as exc_info:
        await adapter.classify(foo)

    assert exc_info.value.context == {"foo_id": str(foo.id), "status": 400}


async def test_classify_503_raises_upstream(
    upstream_answers: list[httpx2.Response | httpx2.TransportError], client: httpx2.AsyncClient
) -> None:
    upstream_answers.append(httpx2.Response(503))
    adapter = HttpFooClassifier(client=client, settings=_SETTINGS)
    foo = Foo(id=uuid.uuid4(), name="alpha")

    with pytest.raises(UpstreamError) as exc_info:
        await adapter.classify(foo)

    assert exc_info.value.context == {"foo_id": str(foo.id), "status": 503}


async def test_classify_network_error_raises_upstream(
    upstream_answers: list[httpx2.Response | httpx2.TransportError], client: httpx2.AsyncClient
) -> None:
    upstream_answers.append(httpx2.ConnectError("boom"))
    adapter = HttpFooClassifier(client=client, settings=_SETTINGS)
    foo = Foo(id=uuid.uuid4(), name="alpha")

    with pytest.raises(UpstreamError, match="unreachable") as exc_info:
        await adapter.classify(foo)

    assert exc_info.value.context == {"foo_id": str(foo.id)}


async def test_classify_read_timeout_raises_upstream(
    upstream_answers: list[httpx2.Response | httpx2.TransportError], client: httpx2.AsyncClient
) -> None:
    upstream_answers.append(httpx2.ReadTimeout("slow"))
    adapter = HttpFooClassifier(client=client, settings=_SETTINGS)
    foo = Foo(id=uuid.uuid4(), name="alpha")

    with pytest.raises(UpstreamError, match="unreachable") as exc_info:
        await adapter.classify(foo)

    assert exc_info.value.context == {"foo_id": str(foo.id)}
```

The stub is the client's transport, built in the `client` fixture: its handler records each request in
`upstream_requests`, which a test reads back for what was sent (rules 2, 3 and 5 of `test-principles`'
*Intercepting HTTP*), and answers it with the next of the `upstream_answers` the test queued — a response,
or a transport error it raises, which the client hands the adapter carrying the request. A sequence, such
as a 429 and then a 200 for an adapter that retries, is two answers queued in order. A request the test
queued no answer for fails the test, even under a caller that catches every exception, so nothing the
test did not expect is answered quietly.

Both halves of parsing are one parametrized test — a `200` whose body is not JSON, and one carrying a
value the domain type refuses: without the adapter's translation around the parse, the decode error or
the `ValueError` escapes and the test reds. Where the adapter sends a credential, the happy-path test
also asserts the header carrying it against the literal test value (`test-principles`, *Intercepting HTTP* rule 5) — the one assertion that reds on a secret sent masked or not at all. Where one class and
one `context` cover several arms, the test tells them apart by the part of the message each sets
(`test-principles`, *Assert strength* recipe 6).

The outgoing body is compared as parsed JSON, never as bytes: separators and key order are the
client library's serialisation choice, not the upstream's contract, and a byte comparison breaks on a
library upgrade that changed nothing on the wire that matters.

### Pure-CPU

`tests/unit/infrastructure/<adapter>/`, in the file mirroring the adapter's module. The worked instance is the token verifier's
test in `hex-test-restapi-auth`'s `UNIT.md`: module-level settings and inputs, the adapter built inline
in each test, real library calls, and one test per check, asserting its `context` (rule 15).

## Other bindings

- **Another stub mechanism.** A stub server on a loopback port, or recorded cassettes, hold the adapter
  real while the socket is not, as the stub transport does, which is all rules 8 and 13 ask for; what
  changes is how the stub is installed and how the outgoing request is read back.
- **A project already on `respx`.** It keeps it — `respx` through `pytest-httpx2` over `httpx2`, routes
  answered with `.respond(...)` and read back from each route's call record. The cases and rule 13 are
  unchanged.
- **An adapter on `httpx`, httpx2's predecessor, or on `aiohttp`.** Under `httpx` the API is the same
  under the old import, `httpx.MockTransport` included, so only the import changes. Under `aiohttp`,
  which takes no transport of this kind, `aioresponses` registers the routes. The cases and rule 13 are
  unchanged.
- **A pre-provisioned backend instead of a disposable container.** Provisioning is
  `hex-test-integration-setup`'s (`## Other bindings`). The per-test namespace and its teardown (rule
  11) get *more* load-bearing, not less — a shared instance keeps whatever a test leaves behind.

## Rules

Consult `test-principles` for the testing constitution and `exception-catalog` for the error catalogue and boundary translation.

### Form

1. **One test file per adapter**, mirroring its module (`test-principles`, *Test naming*).
2. **Path follows the flavor, and the flavor follows whether the test needs something running.** A test that needs a live backend is an integration test (`tests/integration/<adapter>/`). A test whose socket is intercepted, and a pure-CPU adapter that touches nothing, need nothing running and are unit tests (`tests/unit/infrastructure/<adapter>/`) — the intercepted one is `test-principles`' boundary unit. Putting either under `integration/` makes it inherit that tree's container and migration fixtures and pay for infrastructure it never uses. A pure-CPU adapter's test takes neither interception nor a container; an adapter whose test seems to need one has IO and is not the CPU flavor.
3. **Module-level constants, not fixtures, for settings, keypairs and fixed inputs** in the HTTP-gateway and CPU flavors — anything with no setup or teardown (`test-principles`, *Fixture vs. builder*). Construct once at module scope.

### Coverage

4. **Every public method gets a happy-path test.** Drive the adapter; assert the observable side effect (the object exists in the backend, the request matches the upstream's contract, the return value equals a literal).
5. **Every row of the adapter's error mapping gets a dedicated test.** The bug class "translator handles error code X but not Y" only surfaces when each row is exercised. A row the backend never actually reports on a given call — an object store's delete of an absent key answers success — is exercised on a call where it does, and the call that cannot raise it pins its success instead.
6. **An adapter call's failure is asserted on the translated catalogue exception, and `assert exc_info.value.context["<key>"] == <value>` on every one.** Never the SDK's own class — translation at the boundary is `exception-catalog`'s, and asserting the SDK class passes an adapter that never translated. The context map is the load-bearing contract this test exists to pin. This is the capability-adapter analogue of the `context["constraint"]` rule in `hex-test-repository-contract`. The fake-based handler test cannot verify this — only this test can.
7. **A verification probe that reads the backend directly names the SDK's own error class**, as the narrowest class the probe can raise (`test-principles` *Assert strength* recipe 6), and asserts the error code that distinguishes "absent" from "unreachable" or "unauthorized". This is the one place an SDK exception is legitimate in a test — the probe is not going through the adapter, so there is nothing translated to assert on. Asserting on an adapter call still follows rule 6: the translated `MyappError` subclass, never the SDK's class.
8. **A failure that never reaches the upstream is covered too, and lands on the upstream error.** The HTTP-gateway flavor needs a connect-refused and a read-timeout case (`ConnectError` / `ReadTimeout` here) asserting `UpstreamError`; the containerized flavor needs a wrong-container or wrong-credential case asserting the fallback translation. Every row of the adapter's error mapping can pass while the transport arm is unexercised, which is the arm that fires in a real outage.

### Real, not mocked

9. **The real SDK client and the real adapter; only the socket or the backend is substituted** (`test-principles`, rungs 1–2), and no fake of the port here — fakes are `hex-test-application-handler`'s.

### Containerized flavor specifics

10. **Take the resource fixture, not raw settings.** Containerized adapters need a live client and settings naming the test's own namespace (the key-value add-on's `redis_client`, for one). Both come from the integration conftest — session scope for the container; function scope for the namespace, and for the client where its teardown is what empties it, as `redis_client`'s does. The one exception is rule 8's refused or unreachable client, which the test builds itself.
11. **Isolate by a per-test namespace with teardown; there is no rollback at this layer.** An object store, a cache or a queue has no nested transaction to discard. Which fixture owns the per-test namespace and which the session-scoped container and client → `hex-test-integration-setup` (its scope split).
12. **Don't bypass the adapter to drive setup.** For success assertions, you may inspect the backend directly — that is the observation. But for setup that exists to drive the test, go through the adapter (`adapter.upload(...)` then `adapter.delete(...)`).

### HTTP-gateway flavor specifics

13. **The interception follows `test-principles`, *Intercepting HTTP* rules 1–7**; this skill's rule 8 names the two transport cases this flavor needs.

### CPU flavor specifics

14. **Real parsing, real crypto.** Drive the actual library: feed a parser real inputs and assert literal outputs; for a verifier, generate a real key at module scope and sign with the real library. Never hand the adapter a pre-baked value the library never produced.
15. **One `test_*` per check the adapter makes** — each input condition that fails, whether it lands on its own library-exception arm, on a catch-all arm shared with others, or on a guard the adapter raises itself. Each test triggers exactly one and asserts the `context` value that case sets (Rule 6). Counting `raise` statements undercounts: one catch-all arm covering three checks is three cases.

## Inlined typing / import rules

- `pytest`, `httpx2` (its `MockTransport` is the HTTP flavor's stub), the real parsing / crypto library (CPU flavor), the real SDK, `myapp.domain.*`, `myapp.infrastructure.<adapter>` — imported from the package, not its inner module (`python-packaging`). No `myapp.application.*`, no `myapp.restapi.*`.
- Full annotations on every test signature, and a yielding fixture is annotated `AsyncIterator[T]` / `Iterator[T]`. Resource-fixture types (`Session`, `httpx2.AsyncClient`) come from the SDK / library, not the project.
- No `from __future__ import annotations`.

## Hard stops

- Nothing up-tree provides the live backend a containerized flavor drives (the key-value add-on's fixtures, for one) → stop, use `hex-test-integration-setup` to extend the fixtures first; what the flavor needs is the running backend, not a particular fixture name.
- Asked to mock the adapter itself → stop, use `hex-test-application-handler`.
- A test references FastAPI, `httpx2.AsyncClient` over `ASGITransport` or the DI container → stop, use `hex-test-restapi-endpoint`.
- Asked for a token-verifier test here → stop, use `hex-test-restapi-auth`; the flavor is this skill's, the example is not, and duplicating it teaches auth twice.
