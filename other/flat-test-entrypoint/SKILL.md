---
name: flat-test-entrypoint
description: Use when testing what a flat-layered service's trigger actually runs — the function it calls end to end against the store or files it really writes, with only the upstream transport stubbed and an idempotence test wherever a run can repeat, the containment contract of a process that outlives one run, and the framework wrapper through its own in-process harness, proving only that the wrapper reaches the work and that the work's failure arrives as its catalogue code. Where a durable-execution engine was earned, it adds the orchestration level above those, every step stubbed by its registered wire name. Not the client's own transport, which is `flat-test-service-client`, and not the data-access package's write path, which is `flat-test-persistence`. - Also when asked to test a job's or a consumer's body, a polling loop's error handling, a wrapper class, an HTTP route in front of the work it calls, a workflow's retry policy, a batch loop's termination, or what a continuation carries across runs.
---

# Flat-Layered Test — what a trigger runs

Consult `test-principles` for the testing constitution. Where this skill contradicts `test-principles`, the constitution wins.

The function a trigger calls is where a flat-layered service composes everything, so its test is the one that catches
wiring: what the run reads actually fits what it writes, and the aggregate counts what happened. **This skill covers the levels of wrapping around that one
call, tested at each.** They are one subject because they are layers of the same invocation.

The work — the body every trigger calls — is tested end to end against whatever it really reads and
writes, only a remote transport stubbed; with no store and no local output nothing is running, and it
is a unit test under `tests/unit/`. A process that outlives one run adds the containment test (rule 6),
a framework wrapper adds the wrapper test (rule 4), and an earned durable-execution engine adds the
orchestration level under `## Rules`' last subsection (`flat-entrypoint` rule 1 decides whether it is
earned).

## When to use vs. neighbours

- The HTTP client the body calls → `flat-test-service-client`; this level substitutes that client's
  transport, never the client object itself.
- The tables and repository class the body writes through → `flat-test-persistence`.
- The container and isolation fixtures → `flat-test-integration-setup`; the code here owns its
  transactions, so it takes the whole-schema wipe.
- Writing the work, its containment or the trigger, rather than testing it →
  `flat-entrypoint`.
- The pure mapping step the body calls (`build_foo`) → a unit test with no fixtures; it does not belong
  here.
- The static check that a schedule's routing name matches one a process actually serves →
  `test-architecture-rule`, pinning `flat-entrypoint` rule 6.
- The shared groundwork — the substitution ladder, reliability rules, never waiting out real time →
  `test-principles`.

## Template — the work end to end (pytest, `httpx2.MockTransport` under a real `httpx2` client, real Postgres)

`tests/integration/test_foo_sync.py` — the upstream stub's record `qux_requests`, its queued answers
`qux_answers` and the client over it, `qux_client`, are the shared fixtures in `tests/conftest.py`
(`flat-test-service-client`). A run fed by
its trigger's input — a delivery, a message — is called with a built input and takes none of them:

```python
import httpx2
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from myapp.foo_sync import sync_foos
from myapp.postgres import FooRepository
from myapp.postgres.foo_table import foo_table
from myapp.qux import QuxClient
from myapp.schemas import FooSyncResult

_TWO_FOOS = {"items": [{"id": "alpha", "name": "a"}, {"id": "beta", "name": "b"}]}


async def test_a_run_records_what_it_fetched(
    qux_requests: list[httpx2.Request],
    qux_answers: list[httpx2.Response | httpx2.TransportError],
    qux_client: QuxClient,
    engine: AsyncEngine,
    connection: AsyncConnection,
) -> None:
    qux_answers.append(httpx2.Response(200, json=_TWO_FOOS))

    await sync_foos(qux_client, FooRepository(engine))

    query = select(foo_table.c.external_id, foo_table.c.name).order_by(foo_table.c.external_id)
    rows = (await connection.execute(query)).all()
    assert [(request.method, request.url.path) for request in qux_requests] == [("GET", "/foos")]
    assert [tuple(row) for row in rows] == [("alpha", "a"), ("beta", "b")]


async def test_a_second_run_over_the_same_batch_writes_no_duplicates(
    qux_answers: list[httpx2.Response | httpx2.TransportError],
    qux_client: QuxClient,
    engine: AsyncEngine,
    connection: AsyncConnection,
) -> None:
    qux_answers.extend([httpx2.Response(200, json=_TWO_FOOS), httpx2.Response(200, json=_TWO_FOOS)])
    await sync_foos(qux_client, FooRepository(engine))

    await sync_foos(qux_client, FooRepository(engine))

    query = select(foo_table.c.external_id, foo_table.c.name).order_by(foo_table.c.external_id)
    rows = (await connection.execute(query)).all()
    assert [tuple(row) for row in rows] == [("alpha", "a"), ("beta", "b")]


async def test_a_run_reports_what_it_fetched(
    qux_requests: list[httpx2.Request],
    qux_answers: list[httpx2.Response | httpx2.TransportError],
    qux_client: QuxClient,
    engine: AsyncEngine,
) -> None:
    qux_answers.append(httpx2.Response(200, json=_TWO_FOOS))

    result = await sync_foos(qux_client, FooRepository(engine))

    assert [(request.method, request.url.path) for request in qux_requests] == [("GET", "/foos")]
    assert result == FooSyncResult(fetched_count=2)
```

The idempotence test is the one worth writing first. A service that runs on a schedule over a feed that
mostly repeats has "the second run over the same batch adds no row" as its central behaviour, and it
is the one a wrong conflict-column list breaks. It compares the values the input determines, not a
count, so a second run that rewrites one fails too.

The aggregate test matters because that return value is what the trigger reports — a payload, a stored
summary, or the loop's own log line: a body that writes the right rows while reporting the wrong counts
fails silently everywhere a human is looking. An aggregate that is constant for its input is not
asserted.

**A framework wrapper's two tests (rule 4)** run through the harness the framework ships for invoking
one unit in-process — no worker, no broker, no scheduler — and take the fixtures the work's own tests
take. Under an HTTP trigger, drive the app `build_app` returns (`flat-entrypoint`, `HTTP.md`) through
`httpx2.AsyncClient(transport=httpx2.ASGITransport(app=...))` on the test's loop, never FastAPI's
synchronous `TestClient`, which runs the app on a loop of its own and hands the session engine's
connections to it.

## Other bindings

- **A different upstream-stub mechanism** — `respx` where the project already uses it, a local stub
  server, a recorded cassette (`flat-test-service-client` names the trade-offs). Only how the upstream is pinned
  changes; rule 1's asymmetry — upstream substituted, datastore not — is the thing that must survive,
  because it is what makes this level catch wiring at all.
- **Another web framework's harness under an HTTP trigger** — Starlette's, Litestar's or aiohttp's own
  in-process client. The two wrapper tests and what they assert are unchanged; the harness drives the
  app on the loop the suite's engine lives on (`test-principles`, *Fixture scope rules*).
- **No framework wrapper at all.** A service triggered by a loop, a cron entry or a timer writes the
  work's tests, and the containment test where the process outlives one run, and stops; nothing is missing, because there is no wrapper to prove.
- **An engine whose harness cannot skip time.** The retry test pins the *declared* policy on the
  orchestration's own declaration, as `test-principles` reliability rule 3 states; every obligation
  below is unchanged.
- **A replay harness over recorded histories**, where the engine ships one. It pins determinism across a
  code change, which none of the tests here do, and it cannot pin a *new* orchestration's behaviour
  because there is no history yet. It is an addition to the orchestration test file, never a
  replacement.

## Rules

1. **The upstream is substituted at its transport; the datastore is not substituted at all** —
   `test-principles`, the substitution ladder, rungs 1 and 2. That asymmetry is what lets this level
   catch wiring.
2. **Where a run can repeat over the same input, the work's own test file pins what the second run
   does — never the wrapper's (rule 4).** A scheduled pass over a feed that mostly repeats, a delivery
   the sender may repeat (a webhook redelivery, an at-least-once broker delivery), and any run a trigger
   may retry after a partial failure all meet that condition — run twice, and assert the second run left
   the same effect (rule 3): no row added and nothing its input determines changed, the same file, or,
   with neither, the same requests the first run sent, which is all a run that keeps no state can
   promise. A run whose input is consumed once, or that is by construction never repeated, has nothing
   to pin and the test would assert a coincidence.
3. **Assert on the run's effect and on the aggregate it returns, where it returns one**, never on log
   lines (`test-principles`). The effect is what the run leaves behind: the rows it wrote; the file it
   produced, read back from a per-test directory handed to the run as a parameter (`tmp_path` here); or,
   with neither, the requests its stubbed transports recorded. A run that logged `"ok"` and left nothing must fail. Rows the run
   reads, or a record it must meet already stored, are arranged committed before it runs
   (`flat-test-integration-setup`, `connection`). Rows arranged on `connection` are invisible to a run that opens
   its own connection, and a write by the run to the same key waits on their lock until teardown.
4. **A wrapper test proves the wrapper, not the body — two tests.** One drives the trigger and asserts
   the work's effect (rule 3), which proves the wrapper reaches the work; the other forces a failure of
   the work and asserts it arrives at the trigger's error surface as its catalogue code, carrying the
   original's identity rather than an opaque failure. A value the store refuses to hold forces that
   failure with nothing substituted. The translation test is the one that earns its place: an
   untranslated exception reaches the trigger's error surface with the context stripped, and nothing
   else in the suite notices. A wrapper test that re-asserts the work's own test file makes the two
   files change together for one reason.
5. **A run that fans out over independent units is tested with one unit failing inside its write**,
   asserting that the other units' effect (rule 3) — and markers, where units write them — landed and
   that the run's failure names the failed unit (`flat-entrypoint` rules 11 and 13).
6. **A process that outlives one run is tested through the function that performs one contained run,
   never by driving the loop** (`flat-entrypoint` rule 8). Call it with the transport failing — a
   transport error queued as its answer, never an empty queue — it returns without raising — then call it again with the transport answering and assert on that run's
   effect (rule 3). A broker's consumer is tested through the function that handles one delivered
   unit, never the loop's contained run (`flat-entrypoint` rule 15): with the work failing, the unit is
   asserted returned and never acknowledged; with it answering, acknowledged after the effect. The
   logged failure is not asserted
   (`test-principles`). An escape built into the loop — a patched `asyncio.sleep` that raises, a
   counter that breaks out — asserts the mechanism instead of the behaviour; the loop needs no coverage
   of its own.
7. **Where the route verifies a signature, the fixture hands the app a test secret and the tests sign
   with it** (`flat-entrypoint` rule 9), signing the exact bytes they send. One test sends a body whose
   signature does not match and one sends none, each asserting the rejection and that nothing was
   written (`test-principles`, *Assert strength* recipe 4). A switch that disables verification for the
   suite is never added.

### Once a durable-execution engine is earned

An engine is earned by `flat-entrypoint` rule 1 and by nothing else. These obligations cover the
orchestration level that only an engine has; the rules above hold unchanged beneath them, and a service
on a loop, a cron entry or a timer can neither satisfy nor violate them. The work's own tests do not
change under any engine, because the body never imports one.

1. **Time is never slept and never waited out** — timers, backoffs and schedules run on the engine's
   time-skipping clock, the clock `test-principles` reliability rule 3 requires.
2. **An orchestration test asserts orchestration only** — that the step ran, that the retry policy is
   what it claims, that the loop terminates and aggregates. No datastore, no transport stub, no
   assertions about stored rows. That is what keeps this form from re-running the work's own
   coverage: an orchestration test that needs a datastore is exercising I/O `flat-entrypoint`'s durable
   obligation 1 forbids there, and one that needs a transport stub is reaching the real step body
   instead of the stub obligation 3 below registers.
3. **A stub stands in under the registered wire name the orchestration resolves, not by function
   identity.** The orchestration names its steps by string; a stub that is the right function under the
   wrong name is never reached, and the test then exercises the real body against no datastore
   (`flat-entrypoint`'s durable obligation 4 requires the wire name be declared separately from the
   symbol).
4. **A run id is generated fresh per test**, so a re-run cannot collide with a retained execution from a
   previous one.
5. **A batch-loop orchestration is tested against `flat-entrypoint`'s durable obligation 6**: one test
   that the loop ends on an empty batch, and one that a continuation carries every value the next run
   reads, each seeded so that a dropped value changes the observed result. Neither mistake is visible
   from the happy path.
6. **Schedule creation is not tested here.** It is a one-off deploy-time definition, not application
   code, and a test of it would assert only that the engine's SDK works. What *is* worth pinning
   statically is that every schedule's routing name matches one some process actually serves —
   `test-architecture-rule`, pinning `flat-entrypoint` rule 6.

## Hard stops

- The work reaches for a module-level engine instead of taking one → stop, use `flat-entrypoint`
  rule 3 and add the parameter.
- A process that does one run and exits gets a containment test → stop, it contains nothing; its
  failure is its exit status.
- The wrapper body contains logic the work it calls does not → stop, use `flat-entrypoint` rule 2 and
  move it down; the wrapper holds no logic.
- An orchestration, a continuation or a declared retry policy is about to be tested with no engine in
  the service → stop, that level exists only once an engine has been earned (`flat-entrypoint` rule 1).
