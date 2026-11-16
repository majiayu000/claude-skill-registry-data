---
name: flat-entrypoint
description: Use when choosing how a flat-layered service is triggered and writing the process that triggers it — one run per process started by a cron entry or a timer, a loop, a continuous stream or queue consumer, a thin HTTP wrapper, or durable execution — and deciding whether a workflow engine is earned at all; one run per process is the default, and an engine is earned only by durability across process death, retries that outlive the process, or orchestration long enough that the sequence itself must survive. Owns the framework-free function every trigger calls, the process definition that builds its dependencies once and passes them down, the retry declared where the work is invoked, the aggregate a run returns, the containment that keeps one failed run from killing a long-lived process, and where a consumer acknowledges or returns its unit, under `at-least-once-delivery`. It also carries the obligations an earned engine adds, inert under every other trigger. Testing any of it is `flat-test-entrypoint`. - Also when asked for a polling loop, a `__main__` entrypoint, a nightly or periodic job, a queue or websocket consumer process, a webhook, an internal CRUD or proxy endpoint on a service with no invariants, a durable workflow, a batch loop, a heartbeat, a schedule or a cron expression, an overlap or catch-up policy, or whether this service needs a workflow engine at all.
---

# Flat-Layered Entrypoint — loop vs schedule vs stream vs HTTP vs durable

Covers the **process-definition** and **framework-wrapper** roles of one `flat-layered` service, whatever
this service calls those packages. The shapes differ only in *what triggers a run*; the work itself is
always the same functions, so switching later is a wrapper change, not a rewrite.

The invariant that makes that true: **the work a trigger performs is a plain async function in a module
named for that work, taking every dependency as an argument and importing no framework**, and named by
`naming` for what it does. Everything in this skill is a wrapper around one of those.

Every template below is one distribution: `myapp` is this service's own root package (`flat-layered`), and
nothing here assumes a sibling distribution or a repository above it.

## When to use vs. neighbours

- The architecture family is not settled yet — this may not be a flat-layered service at all →
  `architecture-choice` decides hexagonal versus flat first; everything here assumes flat.
- The service's own settings and logging modules, its client and payload packages → not this skill, use
  `flat-layered`, which owns the role kinds and the import contract between them.
- The tables, the write path and the repository class the work calls → `flat-persistence`.
- Several distributions sharing one repository — the member split, the container profiles, the root task
  runner → `python-workspace`. One distribution on its own needs none of it.
- **Durable execution, once it is earned** → still this skill, in the `## Rules` subsection that applies
  once rule 1 has earned an engine. Nothing else in this file depends on it.
- The scheduling needs are met by a loop, a cron entry or a timer — the default → none of those
  obligations apply; do not add orchestration modules "for later".
- The named exceptions a wrapper translates → `exception-catalog`; the one place they are rendered is
  this skill's HTTP shape (`HTTP.md`).
- What a consumer or a webhook route owes the unit delivered to it — acknowledged after its effect,
  redelivered to a limit and dead-lettered, unchanged by a redelivery, its signature checked first →
  `at-least-once-delivery`; where the wrapper does it is here (rules 9 and 15).
- The service answers HTTP but has business invariants, or several entrypoints share its rules → not
  this family; `architecture-choice` decides, and the HTTP shell is `hex-restapi-app`, in the
  `pyhouse-hex` plugin.
- Testing any of it — the work, the loop's containment, the wrapper, the orchestration above them
  → `flat-test-entrypoint`.

## The trigger process — four shapes

| The work is… | Shape | Lives in |
|---|---|---|
| Anything on a schedule, as the starting assumption — a poll, a periodic pass, a nightly job — or a run started by hand from the command line | **One run per process**, started by an external scheduler, by hand, or repeated by a loop around it | the process definition |
| Scheduled work that must *also* survive a restart mid-run, retry across process death, or orchestrate steps over hours or days | **Durable execution** — a workflow engine | a framework-wrapper package plus its serving process |
| A never-ending stream — a log or change feed, a queue consumer, a websocket feed | **Standalone stream process**, watched by an external liveness check | a process definition of its own |
| A request someone else sends — a webhook, an internal CRUD or proxy endpoint, on a service with no invariants of its own | **HTTP trigger** — a thin web-framework wrapper | a framework-wrapper package plus its server process |

**The default for scheduled work is one run per process.** A process that does one run and exits,
started by a cron entry or a timer, or a loop that repeats it, is the whole of most scheduling
requirements, and it costs one module and no infrastructure. Start there.

**A workflow engine is earned, not assumed.** Three things earn it, and nothing else does:

- **Durability across process death** — a run that is half-finished when the pod is evicted must resume,
  not restart. A loop cannot offer this; its state is in the process.
- **Cross-restart retries with a real backoff and a history** — an operator needs to see that attempt 3
  of 5 failed at 04:12 and why, after the process that made it is gone.
- **Long-running orchestration** — several steps, with waits, timers or human input between them,
  where the sequence itself is the thing that must survive.

If one of them is true, a loop reinvents the engine badly: a `_state` table, a retry counter, a lease,
an at-most-once guard, hand-rolled and untested. Shapes 3 and 4 are outside that choice: a continuous
stream and a request are **not** scheduled work.

## The work — one function every shape calls

`src/myapp/foo_sync.py` — the work of a service that fetches from an upstream and records what it
fetched: no framework import, every dependency a parameter, the module named for its work
(`flat-layered`).

```python
from myapp.postgres import FooRepository
from myapp.qux import QuxClient
from myapp.schemas import Foo, FooExternalId, FooPayload, FooSyncResult

__all__ = ["build_foo", "sync_foos"]


def build_foo(payload: FooPayload) -> Foo:
    return Foo(external_id=FooExternalId(payload.id), name=payload.name)


async def sync_foos(client: QuxClient, repository: FooRepository) -> FooSyncResult:
    payloads = await client.fetch_foos()
    for payload in payloads:
        await repository.upsert(build_foo(payload))
    return FooSyncResult(fetched_count=len(payloads))
```

`build_foo` is the mapping as one pure step, so a test covers it without a datastore; a filter the run
needs belongs in the same pure step. The body writes what one call returns, a record at a time: each
record commits on its own, and a rerun completes a partial run because the write is idempotent by its
key. A batched write is earned by the volume, not assumed (`persistence` rule 21), and a source whose
size the service does not control is read in bounded slices instead (rule 10).

**The work opens no transaction.** The repository class owns its own (`persistence` rule 1); a
body that opens a connection has moved data access out of the one package allowed it.

It returns an **aggregate**, not the rows (rule 5): the rows are in the datastore, and a trigger that
serializes the return value into a durable history makes this load-bearing rather than merely tidy.

## Shape 1 — one run per process, on asyncio (the default)

`src/myapp/__main__.py` — the process definition of a service with one process:

```python
import asyncio

import httpx2  # only with an upstream

from myapp.postgres import FooRepository, PostgresSettings, create_engine  # only with a store
from myapp.qux import QuxClient, QuxSettings  # only with an upstream

from .foo_sync import sync_foos
from .logging import configure_logging


async def _run() -> None:
    qux_settings = QuxSettings()  # only with an upstream, as is the block below; without one the run moves out of it
    # only with a store (so are try/finally, repository)
    engine = create_engine(PostgresSettings().dsn)
    try:
        # only with an upstream
        async with httpx2.AsyncClient(base_url=qux_settings.url, timeout=qux_settings.timeout_seconds) as http:
            await sync_foos(QuxClient(http), FooRepository(engine))
    finally:
        await engine.dispose()


def main() -> None:
    configure_logging()
    asyncio.run(_run())


if __name__ == "__main__":
    main()
```

**Logging is configured once, first** (`python-logging` rule 3). **The run is not contained:** a failure
propagates out of `main()` to a non-zero exit, which is how the scheduler that started the process
sees it. `python -m myapp` runs the one process; a service with several defines each as a module in
`entrypoints/` — the same module without its last two lines, its imports of the package root's own
modules written `..` — declares one console script per module in
`[project.scripts]` (`python-toolchain`), and has no `__main__.py`. A run started by hand from the
command line is this process: its entry function is the composition root, and a value its caller picks
per invocation is an argument parsed there, never a setting (`python-settings` rules 13 and 15). Its
command line is `python-cli`'s; where a run is started both by a command and by a scheduler, the
scheduler runs that same command (`python-cli` rule 7).

**The process definition builds every settings object and hands concrete values down** — it is
this family's composition root, so the rule is `python-settings` rule 13.

**The transport and the engine are built once and wrap the whole run.** One pooled `httpx2.AsyncClient`
and one engine exist before the run starts and are closed when it ends, the engine disposed even when
the run leaves by an exception (`flat-layered` rule 12). A second process definition building the same
things takes them from one builder rather than a copy (rule 14).

### A process that outlives one run

A loop catches each run's failure around that one run, logs it once and goes on to the next (rule 8).
The catch sits in a function of the process definition that performs one run and takes
what it needs as parameters, so a test calls it without driving the loop; `log` is the module's logger
(`python-logging`):

```python
async def sync_foos_contained(client: QuxClient, repository: FooRepository) -> None:
    try:
        await sync_foos(client, repository)
    except Exception:
        log.exception("foo_sync_failed")
```

This function is the loop's. A consumer contains a unit's failure too, but never by swallowing it: the
failed unit is returned to the broker for redelivery, never acknowledged (rule 15,
`at-least-once-delivery` rule 1).

A loop waits between runs on an interval read from the process's settings — `MyappSettings` declaring
`poll_interval_seconds: float`, a required field with no default (rule 16) — and stops when asked, after
the run in flight (rule 16). These imports join the module's own, with the module's logger bound
below them:

```python
import contextlib
import signal

import structlog

from .myapp_settings import MyappSettings

log = structlog.get_logger()
```

The first lines of `_run` install the stop request and build the process's settings:

```python
stopping = asyncio.Event()
loop = asyncio.get_running_loop()
for signum in (signal.SIGTERM, signal.SIGINT):
    loop.add_signal_handler(signum, stopping.set)
settings = MyappSettings()
```

And the loop takes the place of the single `await sync_foos(...)` inside the transport block:

```python
client, repository = QuxClient(http), FooRepository(engine)
while not stopping.is_set():
    await sync_foos_contained(client, repository)
    with contextlib.suppress(TimeoutError):
        await asyncio.wait_for(stopping.wait(), settings.poll_interval_seconds)
log.info("process_stopped")
```

## Shape 2 — durable execution, once it is earned

Reach here only once one of the three conditions above has earned it. The shape is **three modules**:
an orchestration module that invokes units of work and computes nothing, a wrapper class adapting the
work into the engine's unit of work, and a process definition that builds the dependencies once and
serves the engine's work — the only modules importing the engine's SDK (`flat-layered` rule 8). The
work does not move, and none of the rules below changes.

Under a managed cloud orchestrator the orchestration definition leaves the repository and the wrapper
becomes the handler; under an in-process durable-function engine the three roles collapse into a durable
function plus its host.

**An engine adds obligations of its own** — replay determinism, continuations, progress reporting,
schedules as code — in the `## Rules` subsection that applies only once rule 1 has earned an engine.

## Shape 3 — the continuous stream process

A never-ending stream stays a standalone process with its own entrypoint module, whatever else the
service runs. It needs not a trigger but a **liveness check**: something outside the process reads the
stream's last observation timestamp and alarms if it is too old — a container healthcheck, a liveness
probe, or a scraped freshness metric with an alert rule.

A service that runs a stream beside scheduled work therefore has two processes, each a module in
`entrypoints/` with a console script of its own (`flat-layered`); the stream is the one that holds state
of its own between observations, written atomically where it is kept in a file (`flat-layered` rule 14),
and it contains each unit's failure like any process that
outlives one run (rule 8).

Never park the stream in one long-lived unit of work or make each item a workflow (rule 7): a workflow
per item is overhead and history for nothing, and a long-lived unit fights the engine's replay model.

A consumer's broker is its trigger: the SDK that receives messages is imported only by the
framework-wrapper package, which parses the message, calls the work with it, and
acknowledges the message once the run succeeds or returns it when the run fails (rule 15;
`at-least-once-delivery` rules 1–4). A broker the service publishes to is an external
system with a package of its own (`flat-layered` rule 14).

## Shape 4 — an HTTP trigger, on FastAPI

A service with no invariants of its own that answers requests — an internal CRUD surface, a webhook
receiver, a proxy — takes the same functions behind a web framework. The framework is one more
wrapper (rule 9): routes validate, call one function and hold no logic; every failure leaves in one
shape from one place; and the app is built by a factory the process definition calls with the
dependencies it built.

**Read `HTTP.md`** in this skill's directory before writing the app factory, its error handling, the
route or the server's process definition — it carries the FastAPI and uvicorn templates
for rule 9.

## Other bindings

- **An external scheduler around the run-once process.** A cron entry, a systemd timer or a Kubernetes
  `CronJob` starts the process as written. Containment does not apply there: a failed run exits
  non-zero and the scheduler records it. The cadence becomes operable without a redeploy and the idle
  process goes, so prefer it to a loop wherever the platform runs a scheduler. A run killed halfway is
  still a run lost.
- **A durable-execution engine in place of either.** Restate and DBOS take the durable-function shape
  in-process; Step Functions and Azure Durable Functions are the managed equivalents; Airflow, Dagster
  and Prefect solve the batch-DAG half. The wrapper package and its process appear, every rule below
  holds unchanged, and the work moves in none of them. What the engine *adds* is the durable
  obligations under `## Rules`, which hold in all of them.
- **Another web framework in place of FastAPI.** Starlette, Litestar, aiohttp or Flask: the app factory,
  the routes and the one error handler are spelled in that framework, and the process definition starts
  its server. The factory taking built dependencies, the routes that validate and call one function,
  and the single rendering of catalogue errors are unchanged.

## Rules

1. **The trigger is chosen; a workflow engine is earned.** A loop, a cron entry or a timer is the
   default for scheduled work. Adopt a durable-execution engine only when a half-finished run must
   resume rather than restart, retries must outlive the process that made them, or a sequence runs
   long enough that the sequence itself has to survive. Absent one of those, the engine is the heaviest
   thing in the deployment and buys nothing. Present, it is adopted rather than reimplemented inside a
   loop: a state table, a lease, an attempt counter and an at-most-once guard, hand-rolled and untested,
   are a workflow engine rebuilt badly.
2. **Every trigger calls the same framework-free function.** The loop body, the scheduled process and
   any framework wrapper all call one plain function from a module named for its work, the function
   named for what it does (`naming`). The wrapper holds the trigger and no logic of its own; that is
   what keeps the shape choice reversible and keeps two triggers of the same work from drifting apart.
3. **The work takes its dependencies as parameters** — the client, the repository class, whatever
   connection handle the data-access package's declared owner needs — and so does a wrapper that needs any:
   the process definition builds them once and hands them in. Never a module-level engine, never a
   settings singleton read from inside the body: a body that reaches for a global cannot be pointed at a
   test container, so a test of it proves nothing, and a wrapper that reaches for one puts the service's
   wiring back into global state, out of the process definition's reach and out of a test's.
4. **Retry and backoff are declared where the work is invoked, never hand-rolled inside it.** Under a
   loop the next run is the retry and the interval its backoff; under any trigger that offers a retry
   policy it is declared at the call site. Work that sleeps and counts its own attempts has two retry
   policies and the outer one no longer bounds it.
5. **Return aggregates, not lists of items.** Where the work has something to report, it returns frozen
   dataclasses of counters or timestamps, so what a trigger reports, logs or stores stays bounded; the
   items themselves live in the datastore; a trigger's report is not a data bus. A read served over HTTP
   is the one exception by construction — it returns the single record it was asked for, never the
   items a run processed.
6. **The routing name a run is addressed to has exactly one source, and every participant reads it from
   that one place.** A queue URL, a topic, a subscription name or the name an engine routes work by is
   normally a per-deployment value and then belongs with the rest of the process's settings
   (`flat-layered` rule 7); where the platform makes the schedule itself code in the same repository, the
   name is a module constant both the schedule and the process serving it import, and a firewall rule
   pins that both read the one source. What is never
   acceptable is two sources — a schedule resolving the name from one environment and the process
   serving it from another — because the disagreement surfaces as work that silently goes nowhere, with
   nothing to catch it.
7. **A continuous stream is a process, not a scheduled run.** Give it its own entrypoint module and
   watch it from outside with a liveness check on the freshness of its last observation — for a queue,
   on the age of its oldest unconsumed message. Never model
   each incoming item as an orchestration, and never park the stream inside one long-lived unit of
   work — its retries restart a stream that was meant to resume.
8. **A process that outlives one run keeps running when one run fails.** Each run's failure is caught
   around that run and logged once, and the process goes on to the next; a failure that escapes ends
   every run after it. The catch wraps one run in something a test can call on its own — "one failed
   run does not stop the next" is such a process's only testable contract, and a `try/except` written
   inline inside the loop can be reached only by driving the loop, which needs an artificial escape
   that changes the thing under test. A process that does one run and exits contains nothing: its failure is its exit
   status, which is how whatever started it sees it. A unit a broker delivered whose run failed is
   returned, never acknowledged (rule 15).
9. **An HTTP route validates its input, calls one function, and holds no logic.** The app is built
   by a factory from dependencies the process definition hands it, never at module scope, and every
   failure — a catalogue error, the framework's validation failure, an unexpected exception — is
   rendered in one shape, in one place, never per route, and logged once there. A route that branches on
   the data, reaches the repository class or the client, or catches a catalogue error or maps it to a
   status of its own, has become a second place the work lives. A request a third party delivers is held to
   `at-least-once-delivery` rules 3 and 5; the route is where its signature is verified.
10. **An input whose size the service does not control is processed in bounded memory.** An upstream
    file, an export or a feed is streamed — read and transformed a bounded slice at a time, each slice
    written before the next is read — and
    nothing in the process accumulates a whole source: no list of every record, no in-process set of
    every key seen. Deduplicating an unbounded input is the data-access package's job, by the record's
    key (`persistence` rules 15 and 17), not a set's. The size that fits today is the size that exhausts the
    process the day upstream grows.
11. **A progress marker is written only after the data it confirms is durably written.** A cursor, a
    watermark or a checkpoint for a unit of work is written after that unit's own writes have returned,
    never while any of its rows sits in a buffer; and a buffer is never shared across units whose
    markers are written independently, because one unit's marker then confirms rows another unit's
    failure loses. A message acknowledgement is a progress marker too — sent only after the unit's
    effect is durable. A marker ahead of its data is data lost with a record saying it was kept.
12. **A file the process writes for another reader is written atomically** — `flat-layered` rule 14.
13. **A run that fans out over independent units contains each unit's failure and fails as a whole
    afterwards.** With bounded parallelism, one unit's failure neither cancels nor orphans the others:
    every unit is awaited to completion, each failure is recorded with the unit it belongs to, and a
    non-empty list of failed units at the end fails the run, so the loop or the trigger sees it. A
    concurrency primitive that propagates the first failure — a bare `asyncio.gather`, or a task group
    whose units raise — leaves the rest unawaited or cancelled, and the run reports one failure of many.
14. **Construction that several process definitions share is written once, in the process-definition
    package, and closes what it built.** Reading a component's settings and building its client, pool or
    engine lives in one builder there that every process definition imports, never copied into each; a
    copy per process is one wiring per copy, and they drift. The builder owns the thing's end as well as
    its start — the pool closed, the engine disposed — when the process leaves it, by any exit
    (`flat-layered` rule 12).
15. **A unit a broker delivered is held to `at-least-once-delivery`, and the framework-wrapper package
    is where.** The wrapper acknowledges the unit once the work returns, returns it when the work
    raises, and sends it to the dead letter where parsing fails and the broker allows it — a malformed
    unit is never acknowledged and dropped. The containment function of a process that outlives one run
    is the loop's and is never handed to a consumer. A run reading a source that keeps no delivery state
    for it — a table, an API, a file listing — needs none of this: its next tick is the retry. A broker
    or a stream read by polling is still delivering.
16. **A process that waits between runs waits for an interval its settings declare, required and with
    no default** (`python-settings` rule 5) — never a constant in the code, which only a redeploy can
    change. A consumer that never waits, taking its next unit as soon as one arrives, declares none.
    **The wait ends when the process is asked to stop; the run in flight does not.** Both the termination
    and the interrupt signal set one stop request, installed before anything is built and checked before
    each run, so a stop finishes the current run and exits 0 with one event rather than a traceback.

### Once a durable-execution engine is earned

Rule 1 decides whether an engine is earned at all, and nothing below licenses one. These obligations
exist **only once an engine is in play** — a service on a loop, a cron entry or a timer can neither
satisfy nor violate them, and every rule above holds unchanged under an engine. They are numbered
separately from the rules and cited elsewhere as *durable obligation N*.

1. **Orchestration orchestrates; it does not compute.** The orchestration body is replayed from
   history, so any parsing, filtering, I/O or datastore access in it produces a different answer on
   replay and corrupts the run. It invokes units of work and does nothing else.
2. **Inside replayed code the engine's clock is the only clock.** Reading the wall clock, drawing
   randomness, or minting a random identifier makes replay diverge from the recorded history. Take the
   value from the engine, or pass it in as an argument.
3. **Orchestration code imports nothing with import-time state or side effects.** An engine may load
   or re-load the orchestration module in an isolated environment of its own, so an import that builds
   an object, opens a connection or reads configuration either fails there or runs again on every load.
   The orchestration module imports the engine and the declarations of the units it invokes, and nothing
   else.
4. **The wire name of a unit of work is declared explicitly, separately from the symbol implementing
   it.** Schedules, execution history and test stubs all bind to the wire name, so renaming the method
   must not be able to break a running schedule.
5. **The service's exceptions are translated at the framework boundary**, carrying the message, the
   identifying context and the original type across it. An untranslated exception reaches the history as
   an opaque framework failure with the context stripped, and the operator reading that history is the
   person who needed it.
6. **Where a run continues as a fresh one, the continuation carries every value the next needs, and the
   loop ends on an empty batch.** A continuation starts with fresh defaults, so a value left behind is
   recomputed or lost — a window reprocessed, a total under-reported; and a run that continues never
   reaches the statement after its loop, so a loop bounded by a count has its real termination nowhere.
7. **A unit of work that runs for minutes reports progress, and the gap the engine will tolerate is
   declared at the call site.** Without progress reports a dead serving process goes unnoticed until
   the whole close timeout elapses, and the unit can never be cancelled — so cancelling the run and
   shutting the serving process down gracefully both have to cut it off mid-flight. The tolerated gap
   must exceed the longest realistic interval between reports, the first one included.
8. **Progress reporting goes through one progress helper, never the framework call directly.** The
   same body is called from a plain loop and from its own test, where the raw call raises because there
   is no framework context — the helper, doing nothing outside one, is what lets the body keep one shape
   under every trigger. **The
   helper is one named module at the root of the distribution's own package**, and it is the one module
   outside the framework-wrapper package allowed to import the framework, which is why the architecture
   firewall's allow-list names it (the firewall is `flat-layered` rule 8's). Where several
   distributions share one repository it is promoted to a library they both depend on, and the
   exemption is the same one.
9. **A healthcheck declares no retries.** Its whole job is to turn red the moment the thing it watches
   is stale; a retry hides exactly the failure it exists to surface. Where the engine is already present
   for other work, a short healthcheck run on a schedule is how a continuous stream's liveness check
   (rule 7 above) gets the engine's visibility machinery.
10. **Schedules are code, held in one versioned, re-runnable definition** — never created by hand in a
    console and never from inside the process serving the work. Each one states its catch-up window, its
    overlap policy and its time zone explicitly, never inheriting the engine's: whatever an engine
    defaults to decides how many missed runs replay after an outage, whether an overrunning run stacks
    under the next, and whether the cadence moves with daylight saving — three operational decisions no
    one made.
11. **The engine's connection settings are required, with no default.** Its address, and whatever
    namespace or tenant it routes by, come from the process's settings like any other tunable
    (`flat-layered` rule 9); a default lets a deployment that forgot one start and reach the wrong
    engine instead of failing at startup.

## Hard stops

- The service answering HTTP has business invariants, or several entrypoints share its rules → stop, this
  family is the wrong one; `architecture-choice` decides, and the HTTP shell is `hex-restapi-app`, in the
  `pyhouse-hex` plugin.
- A statement, a table definition or a transaction is being written into the work a trigger calls or
  into a wrapper → stop, use `flat-persistence`; the work calls the data-access package's repository
  class.
