---
name: hex-architecture
description: Use when the family is already settled as hexagonal and the question is where a module belongs or whether an import may cross a boundary — the four layers, inward-only dependencies, ports, adapters, the composition root. Not whether hexagonal is the right family at all (`architecture-choice`), not where a boundary goes in the first place (`coupling`). - Which layer does this class go in; may infrastructure import application; a cycle between layers; where the DI container or composition root lives; where a queue consumer or a CLI entrypoint goes and what it may import; moving code between layers.
paths: ["**/domain/**", "**/application/**", "**/infrastructure/**", "**/restapi/**"]
---

# Hexagonal Architecture — the layer contract

Which layer a thing belongs to, and what it is allowed to reach. This skill owns boundaries only: the
mechanics of packaging a module and spelling an import are `python-packaging`, and they are the same here
as in any other project. What goes *inside* a module belongs to whichever skill owns that artifact.

## When to use vs. neighbours

- Whether this style is the right one at all, or the service belongs in the flat-layered family →
  `architecture-choice`, which owns the hex-vs-flat decision in full and is universal, so it is
  available whichever family plugins are installed.
- The family is settled the other way — a worker, crawler, pipeline or integration service grouped by
  technical role, with no ports until a second real implementation → `flat-layered`, in the
  `pyhouse-flat` plugin. Nothing in this skill applies there.
- Where a boundary goes at all — split vs merge, whether an integration needs a contract, how much
  structure a component deserves → `coupling`, loaded alongside this skill; it owns the boundary
  reasoning, this skill owns the layer layout.
- Deciding where a module belongs, or whether an import may cross a boundary → this skill.
- Moving code between layers, or restructuring a layer package's public surface → this skill for where
  it lands; `python-packaging` for how the module and its re-exports are spelled.
- Editing the body of an existing module, once its layer is settled → that artifact's skill
  (`hex-domain-model`, `hex-domain-ports`, `hex-domain-service`, `hex-application`, `hex-persistence`,
  `hex-restapi-endpoint`, …). Each already assumes the boundaries this skill sets.
- One class per module, `__all__`, the `__init__.py` contract, relative vs absolute → `python-packaging`.
- Choosing an annotation form or a collection type → `python-style`; the level and fields of a log
  event → `python-logging`; which layer logs is below.
- The error catalog → `exception-catalog`.
- What a queue consumer or a webhook route owes the unit delivered to it, and what a relay owes the
  effect it sends → `at-least-once-delivery`; where the entrypoint does it is below.
- Deriving a concrete path or class name from an identifier → `hex-conventions`.
- Library substrate and the migration bootstrap → `hex-project-setup`; toolchain config → `python-toolchain`.
- A table, a relational repository, a migration → `hex-persistence`.
- Compensation → `hex-application`; a unit of work → `hex-persistence`.
- What the composition root actually binds — providers, lifetimes, settings, teardown, declaration
  order → `hex-wiring`. This skill owns only that the root exists — one module, `src/myapp/containers.py`
  — and that nothing else imports a concrete adapter.
- Turning the import rules below into an automated test → `test-architecture-rule`.

## The four layers

Three are core — `domain/`, `application/`, `infrastructure/`; the fourth is one or more entrypoint
packages (`restapi/`, `cli/`, `worker/`). The split exists so the business rules in `domain/` stay
independent of databases, HTTP frameworks and SDKs, and so the dependency graph stays acyclic.

```
                    ┌──────────────────┐
                    │  entrypoints     │   restapi/, cli/, worker/
                    │                  │   build containers.py, translate
                    │                  │   transport ↔ application
                    └────────┬─────────┘
                             │ may import all three core layers
                             ▼
        ┌────────────────────────────────────────┐
        │            application/                │   commands, queries,
        │   (orchestration, no business logic)   │   handlers (CQRS)
        └────────────┬───────────────────────────┘
                     │ imports domain only
                     ▼
        ┌────────────────────────────────────────┐
        │              domain/                   │   entities, VOs, enums,
        │   (pure logic, stdlib only)            │   protocols, exceptions,
        │                                        │   services
        └────────────▲───────────────────────────┘
                     │ implements protocols
                     │
        ┌────────────┴───────────────────────────┐
        │           infrastructure/              │   adapters, repositories,
        │   (third-party SDKs, IO)               │   tables, clients
        └────────────────────────────────────────┘
```

Dependency direction: **`application → domain ← infrastructure`**, and **entrypoints → all three**. No
other arrow is legal.

### What each layer may import

**`domain/`**

- Allowed: stdlib (`dataclasses`, `datetime`, `enum`, `uuid`, `typing`), other domain modules.
- Forbidden: everything else. No third-party libraries — no ORM, no settings library, no HTTP client, no
  cloud SDK, no web framework. No `application/`, no `infrastructure/`, no entrypoint imports.
- Defines: entities, value objects, enums, filter records, domain protocols (`I*` / `ICan*`), domain
  services, domain exceptions, type aliases. In a hexagonal service the project's one exception
  catalogue (`exception-catalog`) lives in `domain/exceptions.py`.
- Zero IO. No file reads, no network, no database, no logging.

**`application/`**

- Allowed: stdlib, the logging library, domain modules. **The logging carve-out exists for one reason**:
  this is the layer that logs business successes (the layer table under *Who logs, by layer* allocates it), so it
  carries the logging facade and nothing else outward. A second third-party import is not covered by it.
- Forbidden: third-party libraries beyond logging. No `infrastructure/` imports, no entrypoint imports.
- Defines: commands, queries, handlers, result DTOs.
- Depends on infrastructure capabilities only through domain protocols, and receives concrete adapters
  by injection.

**`infrastructure/`**

- Allowed: stdlib, any third-party library, domain modules for protocol types and entities.
- Forbidden: `application/` imports, entrypoint imports.
- Defines: adapters implementing domain protocols — relational repositories, object storage, token
  verifiers, renderers.
- Translates between external representations (database rows, HTTP JSON, queue messages) and domain
  objects. Translation happens *inside* the adapter; a raw row or SDK object never leaks upward.

**Entrypoint packages** — **one package per entrypoint kind, named for the kind**, so that dropping or
adding a transport moves one directory. The catalogue spells the HTTP one `restapi/`; `api/`, `web/` and
`http/` are equally good words and nothing depends on which, but two transports sharing a package is a
defect. Siblings are `cli/` and `worker/`; a command's own rules are `python-cli`'s.

- Allowed: everything. An entrypoint builds the composition root, `src/myapp/containers.py`, at
  startup, runs its settings check (`hex-wiring` rule 2) before it serves or takes work, and closes it at
  shutdown; the root itself is that one module, not the entrypoint package.
- Defines: HTTP routes, CLI commands or queue consumers; request and response wire schemas; the central
  error handler; the dependency wiring.
- Wires `containers.py` at startup, resolves handlers, translates transport ↔ application DTOs.
- Opens one per-operation scope per request, message or call, and closes it when the operation ends.
- Has one scope that catches what propagates, logs it once and turns it into that transport's outcome —
  a status, an exit code, the unit returned or rejected (`at-least-once-delivery` rules 1 and 2) — mapped from
  its class here and never stored on it in
  `domain/`, with any body read off the exception's own attributes (`exception-catalog` rules 6 and 13).
- Acknowledges a message only after its handler returns, and returns it when the handler raises. A
  create it drives carries the identity the message supplies (`hex-application`, command handler rule
  6), so a redelivery finds what the first delivery wrote. A redelivered create that meets the record
  its first delivery wrote, under the same identity, is acknowledged as done, never mapped to a
  conflict or a dead letter (`at-least-once-delivery` rule 3): a create a delivered unit drives is
  written to resolve a conflict on its own identity as nothing to do (`persistence` rule 15), the
  statement being `hex-persistence`'s, so no conflict reaches the scope. The
  rest of what a delivered unit is owed —
  bounded redelivery to a dead letter, a redelivery that changes nothing, a sender's signature — is
  `at-least-once-delivery`'s.

### Who logs, by layer

`python-logging`'s rule — an error is logged once, by the scope that stops it — lands here as a layer
table: every error propagates to one central handler, so the scope that does not re-raise is the
entrypoint.

| Layer | May log |
|---|---|
| `domain/` | **Nothing.** Zero IO includes the log socket; raise an exception carrying `context` instead. |
| `infrastructure/` | **Nothing.** An adapter translates and re-raises, so it is never the layer that stops; the low-level detail goes into the translated exception's `context`, where the layer that does log will find it. |
| `application/` | **Successes only**, at `info`, after the operation completes. Never errors — they propagate. Two exceptions, each a failure the handler stops rather than re-raises: a failed undo under best-effort compensation, logged at `warning` (`python-logging`, "A failed undo under compensation"), and a failed side effect of a command already committed, logged once after the success event (`hex-application`, After the store write). |
| entrypoints | Errors, once, at the central handler, with request context attached. |

**A central handler takes `python-logging`'s level guide**, plus one case only it sees: an exception that is not a
catalogue class → `error`, logged by the entrypoint's own catch-all, which answers it without handing it
back to the framework or server, whose last-resort handler would log it a second time.
The call that implements it is `error_handler.py` in `hex-restapi-app`.

### Top-level layout

```
src/myapp/
├── containers.py         # dependency wiring (the composition root)
├── domain/               # pure business model
├── application/          # CQRS orchestration
├── infrastructure/       # adapters
└── restapi/              # HTTP entrypoint
```

`domain/` and `application/` mirror the same subdomain partition — `domain/foos/`, `application/foos/`.
**`infrastructure/` groups by external technology, not by subdomain**: `infrastructure/postgres/`,
`infrastructure/redis/`, `infrastructure/s3/`, `infrastructure/jwt/` (the derivation is
`hex-conventions`). A new subdomain adds a folder under `domain/` and `application/`; a new external
technology adds one under `infrastructure/`.

## Packaging and imports — not owned here

One class per module, `__all__` placement, the `__init__.py` wildcard re-export contract, relative vs
absolute imports, the collapsed same-package form and import ordering are **architecture-neutral** and
live in `python-packaging`. They apply here unchanged; this skill adds only what the layer split imposes
on top of them:

- **The distribution root's `__init__.py` stays empty** — `python-packaging`'s carve-out for an
  application's root, with a layered reason: aggregating the layer subpackages to the root would make
  `import <package>` transitively pull infrastructure and entrypoint third-party dependencies on every
  use, and would destroy the dependency-free `domain` / `application` import path.
- **A layer package re-exports its subdomain subpackages**, not only its direct modules:
  `from . import bars, foos` + the wildcards + `__all__ = bars.__all__ + foos.__all__`, so
  `from myapp.domain import Foo` resolves.
- **A subdomain package re-exports its whole public surface** — entities, value objects, enums and type
  aliases; every `i_*_repository.py` and `i_can_*.py` protocol; domain services; and in `application/`,
  every command, query, result and handler.
- **The entrypoint package is a side-effect carve-out.** `restapi/__init__.py` must not
  `from .main import *`, because importing `main.py` builds the application object; and the router
  package stays empty, because route modules each export a colliding `router`. A middleware package is
  **not** exempt — its class names are distinct, so it re-exports normally.
- **The declaration sets `python-packaging`'s one-class test lets share a module are, here, two, and
  they are not one rule.**
  The exception catalogue is a single file by principle — `exception-catalog` owns it, and it survives
  any framework. Grouping one resource group's wire schemas into a single module is a REST binding and
  belongs to `hex-restapi-schema`; a project with no HTTP surface has only the first.
- **Cross-layer imports are absolute**, always: `application/` reaching into `domain/`, `restapi/`
  reaching into `application/`. Relative imports stay within one layer. This is `python-packaging`'s
  across-a-package-boundary rule applied to the layer split, not a second rule.

## Placing a use case

Outside in: the entry path in its entrypoint package, the handler in `application/<subdomain>/`, one
protocol in `domain/<subdomain>/` for each thing the handler needs from outside, one adapter per
protocol under `infrastructure/<technology>/` (`hex-conventions`), bound in `containers.py` and
resolved by the entrypoint.

## Moving code between layers

- `domain/` → `application/` usually means the rule needed a protocol. Extract the protocol first, then
  move the orchestrator.
- `application/` → `domain/` is rare, and correct only when the logic was pure all along: no IO, no
  protocol calls.
- `infrastructure/` → `application/` almost never happens. If you feel the urge, you probably want to
  move the orchestration up and leave the adapter behind.
- An entrypoint → `application/` is correct when a second entrypoint needs the same logic. Pull it into a
  handler; the entrypoint becomes a thin translator.

## Rules

The checkable form. Each one is decidable by reading a single import, signature or file path; the
subsections beneath give the reasoning and the judgement calls.

1. **Check every import in `domain/` resolves to `domain/` or the standard library.** Nothing else — no
   third-party package, not even a logger, and no other layer.
2. **Check `application/` imports only `domain/`, stdlib and the logging library**, and **`infrastructure/` only `domain/`,
   stdlib and third-party libraries** — that last allowance is the layer's whole purpose, and the table
   above grants it. Neither imports the other, and neither imports an entrypoint. Only entrypoint
   packages may import all three.
3. **Check no import cycle exists** between modules, subpackages or layers. A cycle always signals a
   layering violation: fix the structure, never paper over it with a type-checking-only or in-function
   import.
4. **Check each new module sits in the layer its work belongs to** — pure logic in `domain/`, a rule needing a port
   in `domain/` as a domain service, orchestration, id generation and business-event logging in
   `application/`, anything touching a datastore, filesystem, HTTP API or SDK in `infrastructure/`,
   anything that knows a transport in an entrypoint.
5. **Check every port is a `typing.Protocol` in `domain/<subdomain>/`**, one per module, named
   `I<Thing>Repository` or `ICan<Verb>`.
6. **Check every handler constructor annotates a protocol type, not a concrete class.** `repository:
   IFooRepository`, never `repository: FooRepository`.
7. **Check no adapter inherits from or imports the protocol it satisfies.** Satisfaction is structural
   and is checked at the injection site; an adapter that imports the protocol it satisfies leaves an
   unused import and gains nothing.
8. **Check the composition root is the only module importing concrete adapters** from
   `infrastructure/` — one module, `src/myapp/containers.py` — and that it binds them at startup, not at
   import time. Entrypoints resolve handlers from the container per operation and never construct an
   adapter themselves.
9. **Check no module-level singleton holds a stateful resource** — a connection, an engine, a client.
   Inject it.
10. **Check every cross-layer import is absolute** and every within-layer import is relative.
11. **Check who logs against the layer table** — nothing in `domain/` or `infrastructure/`;
    `application/` logs successes only, apart from a failed undo under compensation and a failed side
    effect after the store write. Every other error
    propagates to the entrypoint's central handler.

If you are tempted to import `infrastructure` from `application` (rule 2), you are wiring a concrete adapter
where a protocol belongs — define the protocol in `domain/` instead. If you are tempted to import
`application` from `infrastructure`, you have an adapter that knows a use case — move the orchestration
up to a handler.

### Worth a firewall

Rules 1 and 2 are absolutes a grep can hold, so they earn a firewall (`test-architecture-rule`), one
layer-scoped test per forbidden import:

- no ORM, validation-library or other third-party import in `domain/` (`test_domain_has_no_sqlalchemy`);
- no `infrastructure/` import in `domain/` or `application/`;
- no mock in tests (`test-principles`).

## Hard stops

- Whether hexagonal is the right family for this service is still open → stop, use
  `architecture-choice` before placing anything.
- A packaging or import rule is being decided here → stop, `python-packaging` owns those; this skill
  adds only the layer-specific re-export rules above.
