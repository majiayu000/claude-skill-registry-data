---
name: flat-test-service-client
description: Use when testing one external-service HTTP client class with its transport stubbed — URL assembly, the outgoing request, response parsing, timeouts, translation into the service's catalog exception — bound here to `httpx2.MockTransport` under a real `httpx2` client. A unit test needing no database and no container, unlike `flat-test-entrypoint`, which stubs the same transport under the whole run against a real datastore. Not a hexagonal `ICan<Verb>` capability adapter — `hex-test-capability-adapter`, in the `pyhouse-hex` plugin.
---

# Flat-Layered Test — Service Client

Consult `test-principles` for the testing constitution. Where this skill contradicts `test-principles`, the constitution wins.

One unit-test file per client class, under the distribution's own `tests/unit/`. No database, no
container, no network — the `httpx2.AsyncClient` the test hands the client has a stub as its transport,
so everything the client itself does (URL assembly, headers, `raise_for_status`, JSON parsing, the
`except httpx2.HTTPError` translation) runs unchanged. That is why this is a *unit* test despite involving HTTP: nothing crosses a
process boundary.

The client has no `Protocol` and needs none. The test substitutes the transport, which is somebody else's
boundary — not an abstraction invented to make the code mockable.

## When to use vs. neighbours

- The client wraps a vendor SDK rather than raw `httpx2` (a cloud SDK, a database driver) → not a stub transport;
  test it against the real thing in a container under this distribution's `tests/integration/`, or, where
  there is no container for it, against the SDK's own test double if it ships one.
- The filter/normalize function the client's output feeds → a plain unit test with no fixtures; it is
  pure and needs nothing from this skill.
- The work a trigger calls reaching this client → `flat-test-entrypoint`, which stubs the same transport under
  the whole run against a real datastore, and so lives under `tests/integration/`.
- The catalog exception this client translates *to*, and where it is declared → `exception-catalog`;
  asserting the catalog's own shape is a separate unit test, not this skill.
- Where the client module sits in a flat service's package layout → `flat-layered`.
- The family's shared datastore fixtures → `flat-test-integration-setup`; nothing in this file needs
  one.
- The shared groundwork — the substitution ladder, naming, AAA → `test-principles`.
- The client is an adapter behind a hexagonal `ICan<Verb>` capability port rather than a flat
  `*_client.py` → `hex-test-capability-adapter`, in the `pyhouse-hex` plugin, whose HTTP-gateway flavor
  is the same stub transport bound to a port.

## Template — pytest, `httpx2.MockTransport` under a real `httpx2` client

`tests/conftest.py` — the upstream stub and the client over it, in the one conftest above both `unit/`
and `integration/`, because the tests of the work and of its wrapper use the same pair (`test-principles`,
fixture versus builder):

```python
from collections.abc import AsyncIterator

import httpx2
import pytest

from myapp.qux import QuxClient

_QUX_URL = "https://qux.test"
_TIMEOUT_SECONDS = 1.0


@pytest.fixture
def qux_requests() -> list[httpx2.Request]:
    return []


@pytest.fixture
def qux_answers() -> list[httpx2.Response | httpx2.TransportError]:
    return []


@pytest.fixture
async def qux_client(
    qux_requests: list[httpx2.Request], qux_answers: list[httpx2.Response | httpx2.TransportError]
) -> AsyncIterator[QuxClient]:
    def answer(request: httpx2.Request) -> httpx2.Response:
        qux_requests.append(request)
        if not qux_answers:
            pytest.fail(f"no answer queued for {request.method} {request.url}")
        next_answer = qux_answers.pop(0)
        if isinstance(next_answer, httpx2.TransportError):
            raise next_answer
        return next_answer

    transport = httpx2.MockTransport(answer)
    async with httpx2.AsyncClient(base_url=_QUX_URL, timeout=_TIMEOUT_SECONDS, transport=transport) as http:
        yield QuxClient(http)
```

`tests/unit/test_qux_client.py`:

```python
import httpx2
import pydantic
import pytest

from myapp.exceptions import QuxRequestFailedError
from myapp.qux import QuxClient
from myapp.schemas import FooPayload


async def test_fetch_foos_returns_the_parsed_payloads(
    qux_requests: list[httpx2.Request],
    qux_answers: list[httpx2.Response | httpx2.TransportError],
    qux_client: QuxClient,
) -> None:
    qux_answers.append(httpx2.Response(200, json={"items": [{"id": "f1", "name": "alpha"}]}))

    result = await qux_client.fetch_foos()

    assert [(request.method, request.url.path) for request in qux_requests] == [("GET", "/foos")]
    assert result == (FooPayload(id="f1", name="alpha"),)


@pytest.mark.parametrize("status", [400, 404, 500, 503])
async def test_non_2xx_becomes_a_qux_request_failed_error(
    qux_answers: list[httpx2.Response | httpx2.TransportError], qux_client: QuxClient, status: int
) -> None:
    qux_answers.append(httpx2.Response(status))

    with pytest.raises(QuxRequestFailedError) as exc_info:
        await qux_client.fetch_foos()

    assert isinstance(exc_info.value.__cause__, httpx2.HTTPStatusError)


async def test_a_timeout_becomes_a_qux_request_failed_error(
    qux_answers: list[httpx2.Response | httpx2.TransportError], qux_client: QuxClient
) -> None:
    qux_answers.append(httpx2.ConnectTimeout("timed out"))

    with pytest.raises(QuxRequestFailedError) as exc_info:
        await qux_client.fetch_foos()

    assert isinstance(exc_info.value.__cause__, httpx2.TimeoutException)


@pytest.mark.parametrize(
    "body",
    [b"<html>not json</html>", b'{"items": [{"name": "alpha"}]}'],
    ids=["not-json", "missing-field"],
)
async def test_a_200_with_a_malformed_body_becomes_a_qux_request_failed_error(
    qux_answers: list[httpx2.Response | httpx2.TransportError], qux_client: QuxClient, body: bytes
) -> None:
    qux_answers.append(httpx2.Response(200, content=body))

    with pytest.raises(QuxRequestFailedError) as exc_info:
        await qux_client.fetch_foos()

    assert isinstance(exc_info.value.__cause__, pydantic.ValidationError)
```

The stub's record, its answers and the client over it are fixtures, not module-level builders, because
the client has an end — its transport is closed at teardown — and the record and answers are fresh per
test; they sit in `tests/conftest.py` rather than in each test module because three files at two levels
take them. The client fixture builds its `httpx2.AsyncClient` exactly as the process definition does —
base URL and timeout from constants in place of settings — with the stub as its transport, so no test
can hold the client with anything but the stub under it (rule 7). The stub's handler records each request
in `qux_requests` and answers it with the next of the `qux_answers` the test queued: a response, or a
transport error it raises, which the client hands on carrying the request. A request the test queued no
answer for fails the test, even under a caller that catches every exception, so nothing unexpected is
answered quietly. Where the process definition hands the transport an auth flow (`flat-layered` rule
13), the fixture builds it the same way, and its login requests go through the same stub, so the tests
pin the refresh with answers queued in the order the flow sends its requests — the login's token, the
401, the second login's token, the success — and read `qux_requests` back as that sequence of method
and path, the last carrying the renewed credential. A second rejection raises the catalogue error with
the record ending on the resource request, so the rejection is the resource's and not a failed login;
a credential request that itself fails raises it too.

`fetch_foos` sends nothing beyond its method and path, so the recorded method and path are its request
pin (rule 3); a method that sends a query, a header or a body reads it back from the request in
`qux_requests`.

The error tests assert the translated class and its chained cause. `fetch_foos` takes no input, so its
`context` is empty; a method that takes one also asserts the `context` key set the raise site and its
test agree on — never the message text, which is free to change (`exception-catalog`). The malformed-body
cases cover both halves of parsing: a body that is not JSON, and JSON that does not fit the payload.

A caller's test makes this client fail at its transport (`flat-test-entrypoint` rule 1).

## Other bindings

- **A project already on `respx`.** It keeps it — `respx` through `pytest-httpx2` over `httpx2`, routes
  answered with `.respond(...)` and read back from each route's call record. What the tests assert — the
  translation, the outgoing request, malformed bodies, timeouts — is unchanged, and so is the ban on
  extracting a `Protocol`.
- **A local ASGI app served in-process** as the transport, where the stub must hold state across
  requests. The client already takes its transport pre-built, so nothing in it changes.
- **A client on `httpx`, httpx2's predecessor.** The same API under the old import, `httpx.MockTransport`
  included, so only the import changes.
- **A different HTTP library** — `aiohttp` with `aioresponses`, `requests` with `responses`. The
  interception point and the exception classes the client translates *from* change together; the
  catalogue exception it translates *to*, the cause-chaining requirement and every rule below are
  unchanged.
- **Recorded interactions** — vcrpy cassettes. Response bodies come from a recording rather than a
  literal, which keeps them honest about the vendor's real shape; rule 3 then pins the cassette's
  recorded request. The timeout and malformed-body cases still have to be hand-written, because a
  cassette holds only what actually happened.

## Rules

1. **The transport is stubbed, never the client** (`test-principles`, the substitution ladder, rung 2),
   and no `Protocol` is extracted for it (`flat-layered` rule 3). A test that patches
   `QuxClient.fetch_foos` is testing nothing; the parsing and translation under test live inside it.
2. **Assert the translation, not just the type** — `test-principles`, *Assert strength* recipe 6: the
   catalogue class, its `context` keys where the call takes an input (`exception-catalog` rule 11), and
   the translated failure as its cause, never the message.
3. **Pin what the client sent beyond its method and URL** — `test-principles`, *Intercepting HTTP* rule 5
   (read back from `qux_requests` here).
4. **A 200 the client cannot parse is part of its contract** — `test-principles`, *Intercepting HTTP*
   rule 6; the template's two malformed cases are its two halves.
5. **The base URL is a constant beside the fixture that builds the client, and is passed in.** Never let
   the test depend on a settings value — hand the client an HTTP client built with an explicit
   `base_url`, which is why the client is handed its transport rather than building one.
6. **Assert the request a test exercises reached the stub, on the stub's record** — `test-principles`,
   *Intercepting HTTP* rules 2 and 3 (`qux_requests` here).
7. **No test reaches a real host** (`test-principles`, *Intercepting HTTP* rule 1), and a stubbed body
   is copied from a documented or recorded response (*Intercepting HTTP* rule 7), never read live.

## Hard stops

- The client swallows a transport or parsing failure internally, returning a default instead of raising
  → stop, fix the client (`exception-catalog` rule 15); a boundary that hides its failures cannot be tested,
  and its caller cannot tell a failure from an empty answer.
- The client returns raw `httpx2.Response` objects to its caller → stop, fix the client (`flat-layered`);
  the client owns parsing, and a test cannot pin behaviour that lives in the caller.
- The client is an adapter behind a hexagonal `ICan<Verb>` port → stop, use
  `hex-test-capability-adapter`, in the `pyhouse-hex` plugin.
