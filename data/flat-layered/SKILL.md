---
name: flat-layered
description: Use when structuring a worker, crawler, pipeline, ETL job or integration service whose family is already settled as flat — one distribution on its own by default, and one of several in a repository under the same rules. Defines the four role kinds a flat service divides into and the import contract between them, the packages named for the roles this service actually has, the package and settings class each configured component owns, the single-implementation client holding one pooled transport and a refreshable credential, and why no `Protocol` appears until a second real implementation does. Data access is one package per store, named for its technology, whose rules are `flat-persistence`; several distributions sharing one repository is `python-workspace`; an unsettled family is `architecture-choice`. - Also when asked for a worker's or a pipeline's package layout, where a client class or a settings class belongs, whether a dependency deserves an interface, or how to lay out a single-distribution repository with no workspace around it.
---

# Flat-Layered Architecture — package-by-technology, no ports

Covers project layout for services where the ports-and-adapters split (domain/application/
infrastructure/entrypoints, `Protocol` ports, DIP) would add indirection with nothing to protect. The
code groups by **technical role**, dependencies point wherever they need to, and an interface is
introduced only when a second real implementation is about to exist — not in anticipation of one.
This skill assumes the family is already chosen; `architecture-choice` chooses it.

**The worked example throughout is a service that fetches from an upstream and lands rows in a store**,
because it exercises every role at once. The roles are not that workload: a service that consumes a
queue and calls an API, one that renders reports, one that only transforms what it is handed, fills the
same four roles and leaves empty the ones it has no use for. A role with nothing in it is not a gap.

**The subject is one distribution on its own** — its own package and its own datastores where it has any.
A service that shares a repository with siblings is the same service under the same rules with a
workspace root above it, and that root is a separate skill. Nothing below requires one.

The style has established names: what the literature calls **package by layer**, after Simon Brown, with
what Fowler calls **transaction scripts** above it.

## When to use vs. neighbours

- The style is not settled yet — a greenfield service, or one that may have outgrown the family it was
  built in → `architecture-choice`, which owns the hex-vs-flat decision in full: the question that
  settles it, what each family costs, and the cases the bullets below do not cover. It is universal, so
  it is there whichever family plugins are installed.
- The service enforces business invariants that must survive a change of database, queue or framework
  → not this skill; use a hexagonal / ports-and-adapters layout instead — `hex-architecture`, in the
  `pyhouse-hex` plugin. Nothing in this skill applies there.
- More than one entrypoint drives the same domain logic (REST + gRPC + a queue consumer, all calling
  the same rules) → not this skill; that shared core is exactly what ports exist to protect.
- A dependency already has, or is about to get, a second real production implementation (two providers
  the service switches between) → not this skill for that dependency; extract a narrow `Protocol` for
  it and keep the rest flat. A test double is not a second implementation (rule 3).
- A single script with no more than a couple of modules → still too heavy for this skill; just write
  the script (`architecture-choice` states what does apply to one).
- The question is not the layout but the boundary — split vs merge, contract vs shared knowledge,
  how much structure something deserves → `coupling` decides that; it loads alongside this skill,
  never instead of it.
- The service is mostly "call external system A, transform, call external system B/C, repeat" with one
  implementation per system and no rules worth isolating → this skill.
- Where this service's SQL, table definitions and write path live, and how a second store sits beside
  the first → `flat-persistence`, which owns the data-access role. A service with no datastore skips it.
- This service is one of several distributions sharing one repository → this skill still covers its own
  internal layout unchanged; the repository root, the member split and the tooling settled once are
  `python-workspace`. One distribution on its own needs none of that.
- What triggers a run — a loop, a cron entry, a stream, an HTTP request, or durable execution once it
  is earned → `flat-entrypoint`, which owns the obligations of the work every trigger calls.
- The dependencies each role brings and the migration environment, laid once when the service is
  created → `flat-project-setup`; the src layout and the lint and type-check configuration →
  `python-toolchain`.

Six skills apply here unchanged and are not restated: `python-packaging` (one class per module,
`__all__`, re-exports, import forms), `python-style` (annotations, collection types, the shape a record
takes across a boundary, comments), `python-logging` (the event, who logs a failure, configuring
once at the entry point), `python-settings` (what a settings class declares, its
defaults and secrets, and construction at the composition root), `exception-catalog` (the catalog and
translating SDK errors into it) and `coupling` (where boundaries go at all, and how much structure a
component deserves).

## The four role kinds and the import contract

A flat service divides into four **role kinds**. The kinds are the architecture; the directory names are
this project's and appear nowhere in the rules. A service creates a module or package per role it has,
names it for that role, and declares which kind it is when it creates it.

| Role kind | Holds | May import | Imported by |
|---|---|---|---|
| **data access** | one package per store: its table definitions, its write path, and the mapping from its rows back to this service's own types. **The only role that constructs a statement or opens a connection.** | payload packages, and the settings values handed to it | work units, the framework wrapper, process definitions |
| **work unit** | one plain function per complete run — whatever one invocation of the trigger is for. Takes every dependency as a parameter, imports no framework, returns an aggregate rather than its individual results. | client, payload and data-access packages | the framework wrapper, process definitions |
| **framework wrapper** | the framework's own decorators, classes or handlers adapting a work unit to a trigger. **The only role that imports the framework, and it holds no logic of its own.** | work units, plus payload packages | process definitions |
| **process definition** | builds every settings object once, builds the dependencies, wires them, runs one process. | everything | nothing |

The **columns are the contract**; a service that can fill this table for its own packages has applied
this skill. Everything else in a flat service is a supporting package the four reach for — payload models
and results, one package per external system, the exception catalog, the cross-cutting setup modules at the
package root — and none of them imports any of the four.

The kind is deliberately *not* called a "unit of work" — that name belongs to the transactional pattern
of that name in the other family (`hex-persistence`, in `pyhouse-hex`), and one word for two unrelated
things is how names stop identifying anything. What a work unit is called is `naming`'s decision and it
names the work done, as `sync_foos` does in the templates.

**Rule 8 is enforced by a firewall of `test-architecture-rule`'s standard form** — the framework's
import is forbidden outside the declared wrapper package, whatever the framework; the one entry an
earned durable-execution engine adds to its allow-list is `flat-entrypoint` durable obligation 8's.
The other invariants worth a firewall in a flat service: no
statement or table constructed outside a data-access package (rule 4), no module-level engine
(`python-packaging` rule 8), no engine in a unit test and no mock or sleep in any test
(`test-principles`), and in a repository of several members no runnable member importing another
(`python-workspace` rule 7).

### The package names

A service creates a package only for a role it has, and names it for what it holds (`naming`); a name
copied for a role the service lacks yields an empty package a reviewer assumes holds work. What is fixed
is the decision:

- cross-cutting setup — logging, the exception catalogue, the process's own settings — sits in modules
  at the package root, never in a package named after the category;
- **a component with configuration of its own is a package** at the package root, and its settings
  class sits inside it (`qux/qux_settings.py`, rule 7) — never in a package it shares with another
  component;
- each external system gets one such package, holding its one client class;
- each store gets one data-access package, named for the store's technology (`flat-persistence` rule 5);
- a work unit is a module named for its work, and several that share a concern share a package named
  for it — never the module that defines the process running them;
- a framework wrapper is isolated in its own package so the work it wraps stays framework-free;
- the one process is defined in `__main__.py`; several each get a module in `entrypoints/` and a console
  script of their own, and nothing imports any of them.

## Template — package skeleton

Only what nearly every flat service has. A line marked *only* exists when its condition does; a service
creates nothing else because a tree showed it.

```
src/myapp/
├── __init__.py
├── __main__.py        # the one process: builds its dependencies and runs — `flat-entrypoint`
├── exceptions.py      # this service's exception catalogue — `exception-catalog`
├── logging.py         # configures logging once, called by the process definition
├── myapp_settings.py  # only with settings of the process's own
├── schemas/           # the records more than one package reads, one declared type per module
├── qux/               # only with an external system: one package per system, named for it — its client and its settings class
├── postgres/          # only with a store: one package per store, named for its technology — `flat-persistence`
├── foo_sync.py        # a work unit, named for its work
└── entrypoints/       # only with more than one process: one module per process, replacing __main__.py
```

The tree sits under `src/`, beside the distribution's `pyproject.toml` and `tests/` (`python-toolchain`
rule 1). A record one package alone reads lives in that package; a record that crosses packages — the
service's own record, a wire record one package parses and another consumes, what a run returns — sits
in `schemas/`. A service with a framework adds one wrapper package — the HTTP shape's, or a
durable-execution engine's together with its progress helper module (`flat-entrypoint`). A second store is
a sibling of `postgres/` named for its own technology (`flat-persistence` rule 5).

### Template — the declared records, on dataclasses and pydantic

The three records every other flat template and test builds, reads or asserts on. Each is its own
module: they change for three different reasons — the service's model, the upstream's wire format, what
a run reports — so they are not one set (`python-packaging`).

`src/myapp/schemas/foo.py` — the service's own record, built by the work unit and by the
repository's row mapper, identified by its `external_id` — an identifier the source issued, so a distinct
type over `str` (`python-style`), wrapped where a value is mapped into the record:

```python
from dataclasses import dataclass
from typing import NewType

__all__ = ["Foo", "FooExternalId"]

FooExternalId = NewType("FooExternalId", str)


@dataclass(frozen=True, slots=True)
class Foo:
    external_id: FooExternalId
    name: str
```

`src/myapp/schemas/foo_payload.py` — the wire record, parsed and validated where it arrives:

```python
from pydantic import BaseModel, ConfigDict

__all__ = ["FooPayload"]


class FooPayload(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    name: str
```

`src/myapp/schemas/foo_sync_result.py` — the aggregate a run returns (`flat-entrypoint` rule 5):

```python
from dataclasses import dataclass

__all__ = ["FooSyncResult"]


@dataclass(frozen=True, slots=True)
class FooSyncResult:
    fetched_count: int
```

`src/myapp/schemas/__init__.py` re-exports all three modules (`python-packaging`).

### Template — an external-system client, on httpx2

`src/myapp/qux/qux_client.py` — one concrete class, no Protocol:

```python
import httpx2
from pydantic import BaseModel, ValidationError

from myapp.schemas import FooPayload

from ..exceptions import QuxRequestFailedError

__all__ = ["QuxClient"]


class _FooList(BaseModel):
    items: tuple[FooPayload, ...]


class QuxClient:
    def __init__(self, http: httpx2.AsyncClient) -> None:
        self._http = http

    async def fetch_foos(self) -> tuple[FooPayload, ...]:
        try:
            response = await self._http.get("/foos")
            response.raise_for_status()
            return _FooList.model_validate_json(response.content).items
        except (httpx2.HTTPError, ValidationError) as exc:
            raise QuxRequestFailedError("failed to fetch foos") from exc
```

`QuxRequestFailedError` is the one class this client raises, a refinement of the catalogue's `UpstreamError`
(`exception-catalog`); what its
`context` carries when a method takes an input is `exception-catalog`'s.

`src/myapp/qux/qux_settings.py` is `python-settings`' template — `QuxSettings` under
`MYAPP_QUX_`, declaring the client's `url` and `timeout_seconds`. The process's own
`src/myapp/myapp_settings.py`, at the package root beside the rest of the cross-cutting setup, has the
same shape — `MyappSettings` under `MYAPP_` (`naming`) — holding only the fields that configure the
process itself; where `entrypoints/` holds several processes with fields of their own, each process's
class is named for its process (`FooSyncSettings` in `foo_sync_settings.py`). A process with none has
no such module, and a thin HTTP wrapper adds two server fields to it (`flat-entrypoint`).
The data-access package's prefix is `MYAPP_POSTGRES_` (`naming`). The package's `__init__.py`
re-exports the settings and client modules (`python-packaging`), so a caller writes
`from myapp.qux import QuxClient, QuxSettings`. The data-access package declares its settings
class the same way (`flat-persistence`).

**The client is handed its transport; it never builds one** (rule 12). The process-definition package
builds the pooled HTTP client once from the system's settings — `httpx2.AsyncClient(base_url=settings.url,
timeout=settings.timeout_seconds)`, entered with `async with` for the life of the process so it closes
when the process ends (`flat-entrypoint`) — and passes it to `QuxClient`. A test
builds the same client against a stub base URL and hands that in, without touching the environment.

**An upstream that issues an expiring token keeps the refresh on the transport** (rule 13). Under httpx2
that is an `httpx2.Auth` subclass overriding `auth_flow`, passed as `auth=` where the process definition
builds the transport: its flow logs in when it holds no token, and on a 401 logs in once and resends.
The client's methods stay as above, and a second 401 leaves through `raise_for_status` as a
`QuxRequestFailedError` like any other refusal.

**Parsing sits inside the translated scope.** A 200 whose body is not JSON, or is JSON of the wrong
shape, is as much an upstream failure as a 503, so decode and validation run inside the request's `try`
and leave as the catalogue's error, input in `context`, original chained (`exception-catalog`); a parse
after the `try` lets a malformed 200 escape as the validation library's own exception. The envelope
model is private: it describes the upstream's envelope and never leaves this file (`python-packaging`).

The client returns a declared type, never the parsed `dict` (`python-style`).

## Other bindings

- **A console-script entry point in place of `__main__.py`.** `[project.scripts]` in the packaging
  metadata gives the same one declared place a process starts from, as a named command. What must not
  change is the count: one declared entry point per runnable process.
- **Another HTTP or SDK client in place of `httpx2`.** `httpx`, the predecessor (the same API under the
  old import), `aiohttp` (stubbed in tests with `aioresponses`), `niquests`, a vendor SDK: the client
  class keeps its shape — the session or SDK client built once by the process definition and handed to
  the constructor, the library's own exceptions caught and translated inside it, no `Protocol` above it.
  Only the call, the exception type and the hook a credential refresh attaches to change.
- **A local executable in place of an HTTP API** (rule 14). A client that runs a binary as a subprocess
  keeps the same shape: the executable's path comes in through the constructor, and a non-zero exit, a
  timeout and unparseable output are translated inside the client like any other upstream failure.

## Rules

1. **Group by technical role, not by pretend layer** — one package per role kind the service actually
   has, named for the role it holds. No `domain/`/`application/` split: there is no domain layer to
   protect. Every package fills one row of the import-contract table or is a supporting package the four
   reach for; one that fits two rows holds two roles and is split, and one that fits none, or that exists
   only because a tree shows it, is deleted before any code goes into it.
2. **One responsibility per module even without the layer split.** A module holding several unrelated
   classes, or a function grab-bag with no shared concern, is the failure mode this skill still forbids.
   Split when a module mixes unrelated concerns or grows past a couple hundred lines.
3. **No `Protocol` over a dependency until a second real production implementation is about to be
   written** — a second provider the service switches between. Until then construct the concrete class
   directly, or via a plain factory function if the object graph is non-trivial; a dependency-injection
   container is unwarranted machinery, since with one implementation per dependency there is nothing for
   it to choose between. An interface or a container added "in case we swap it later" is the anticipatory
   abstraction this family exists to avoid. Judge "about to be written" from the domain, not from caution
   (`coupling`): the credible case is a commodity dependency with a nameable alternative the business
   could plausibly adopt; a sticky one — the main datastore, the identity provider — never qualifies,
   however generic it looks. When the case arrives, extract a narrow `Protocol` for *that one
   dependency*; do not retrofit the rest of the service. **A test double never counts**: tests substitute
   at the boundary by `test-principles`' substitution ladder — the real backend, a stubbed transport or a
   subclass — never through a `Protocol` introduced only to make a concrete class mockable.
4. **Data access is a role: only a package whose declared role is data access constructs a statement or
   opens a connection, and each store gets exactly one such package.** A store's table definitions, its
   write path and the mapping from its rows back to this service's own types sit together in that
   package, and every other package asks it for data — never a statement in a work unit, never one
   store's access scattered across packages. A second store is a second such package (`flat-persistence`
   rule 5). A store's SQL is findable in one place or it is everywhere. What such a package contains,
   and what changes where several distributions share one store, is `flat-persistence`.
5. **One exception catalog**, and SDK/library exceptions are translated into it at the boundary — inside
   the client class that called the SDK. Shape and translation rules: `exception-catalog`.
6. **The process definition builds settings and passes them down as values** — it is this family's
   composition root, and the rule is `python-settings` rule 13; the migration environment is a
   migration run's (`flat-project-setup`).
7. **Every component that has configuration is a package, and declares its own settings class inside
   that package, in the module named for it** (`python-settings` rule 1) — `qux/qux_settings.py`. The
   process's configuration, an external system's and a store's are three components and three classes
   — never one class holding two components' fields, and never two components sharing one package. Its
   prefix, and the nested-prefix collision between the process's `MYAPP_` and a component's
   `MYAPP_POSTGRES_`, are `naming`'s rule 7, the same whether the second component is a package inside
   this distribution or a library shared with siblings (`flat-persistence` states that package's half).
8. **Only a package whose declared role is framework wrapper may import the framework**; the one
   exemption, once a durable-execution engine is earned, is `flat-entrypoint` durable obligation 8's
   progress helper. That one rule is what keeps the work units callable from a
   loop, a test or a one-off script, and it is what makes switching a service's trigger a wrapper change
   rather than a rewrite; a framework import anywhere else welds the work unit to the framework. The role
   is declared when the package is created, never inferred from a directory name.
9. **A tunable with no single right value carries no default** (`python-settings` rule 5).
10. **An enum lives beside the module that owns it.** A shared vocabulary module holds only what is
    genuinely used across packages, and admission to it runs `coupling`'s test — a blanket category
    package pulls single-owner types away from their owner and stops naming anything.
11. **Which scope logs a failure is `python-logging`'s rule, and it applies here unchanged.** In a flat
    service the scope that stops a failure is usually the code around each run in a loop or the framework wrapper's error
    handler; a client translating an SDK error re-raises and so stays silent, with the detail riding in
    the translated exception's `context` (`exception-catalog`).
12. **A client holds one pooled transport for the process's life and never opens one per call.** The
    process definition builds the connection pool or SDK session once, hands it to the client's
    constructor, and closes it when the process ends (`flat-entrypoint` rule 14). A client that builds its own transport
    inside a method pays a new connection on every call, discards the pool it would have reused, and can
    be pointed at a stub only by patching the library.
13. **A credential with an expiry is refreshed, never assumed to outlive the process.** A client that
    obtains a token by logging in logs in again when the token expires or the upstream rejects it —
    once, then retries the call; a second rejection is translated like any other failure (rule 5). A
    token cached for the process's life passes every short test run and fails every run after its first
    expiry in a process that lives for days.
14. **An external-system package wraps the interface the system actually exposes, confirmed from that
    system's documentation.** An HTTP API, a vendor SDK, a local executable and its output, files it
    writes — the client calls whichever the system offers, and never assumes an HTTP API. A client
    written against an endpoint, a path or a response shape the system does not have passes every test
    stubbed from the same invention and fails on the first real run. Rules 5 and 12 hold whatever the
    interface is. A directory the service writes to for another reader is an external system too — a
    package with its own settings and one writer class. **A file the process writes for another reader
    is written atomically.** A report, an export, or a position kept for the next start is written under
    a temporary name and moved over the final one in one atomic step (`os.replace` in the standard
    library), never written in place — a crash mid-write otherwise leaves a file its reader cannot
    parse, or reads half of.
15. **A process definition wires and runs; it holds no business logic.** Building settings and
    dependencies, configuring logging, the loop, the containment and the wait around a run, and starting the process
    stay in it (`flat-entrypoint`); a decision about the data a run handles belongs in a work unit, where
    a test can call it directly — taken in the process definition, it runs only when the process does.

## Hard stops

- The service has business invariants that must outlive a change of infrastructure → stop, use a
  ports-and-adapters layout instead (`hex-architecture`, in the `pyhouse-hex` plugin).
- Two or more entrypoints need to share the same business rules → stop, that shared core is what ports
  protect; do not force it flat — `architecture-choice` settles the family (`hex-architecture`, in the
  `pyhouse-hex` plugin).
- A single script of no more than a couple of modules is being given this layout → stop, just write the
  script; `architecture-choice` states what applies to one.
