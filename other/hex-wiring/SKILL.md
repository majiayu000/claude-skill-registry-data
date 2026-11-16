---
name: hex-wiring
description: Use when adding a binding in `containers.py` — provider classes, binding lifetimes, the `create_container` composition root and its declaration order, and where each settings class is constructed and bound — every one before the process serves or takes work. Bound here to dishka, with other DI libraries mapped under `## Other bindings`. What a settings class declares, defaults and keeps secret is `python-settings`; the class being bound must already exist — `hex-application`, `hex-capability-adapter`; the project substrate is `hex-project-setup` and the toolchain `python-toolchain`, not runtime wiring.
paths: ["**/domain/**", "**/application/**", "**/infrastructure/**", "**/restapi/**"]
---

# Hex — Wiring

Handing objects to whoever needs them, from one composition root. Settings are among those objects:
what a settings class declares is `python-settings`, and this skill says where, in a hexagonal service,
it is constructed and bound — at a composition root and nowhere else (`python-settings` rule 13). Each
settings class is shown beside the adapter that reads it: the relational store's `PostgresSettings`
in `hex-persistence`, `FooClassifierSettings` in `hex-capability-adapter`, `RedisSettings` in
`hex-store-repository`, `JwtSettings` in `hex-restapi-auth`. The composition roots of that rule are,
in this catalogue's layout, `src/myapp/containers.py` (the process's container), `migrations/env.py`
(the migration environment, `hex-project-setup`) and `TestInfrastructureProvider` with its fixtures in
`tests/integration/conftest.py` (the test infrastructure, `hex-test-integration-setup`), which
constructs settings with explicit values (`test-principles`).

## When to use vs. neighbours

- What a settings class declares — its namespace, defaults, secrets, derived values, validation → `python-settings`.
- Binding a new class in the composition root, or choosing its lifetime → this skill.
- The class being wired must already exist — a handler, repository, service, adapter → `hex-application`, `hex-persistence`, `hex-store-repository`, `hex-domain-service`, `hex-capability-adapter`.
- A frozen domain-shaped view of settings values the domain consults → the tunable variant in `hex-domain-model`; its provider reads the single field off a settings class and passes it.
- Attaching the composition root to the HTTP app, running its settings check at startup and closing it at shutdown, which runs every declared teardown → `hex-restapi-app`.
- Resolving a bound object inside a route → `hex-restapi-endpoint`.
- The token-verifier port, its adapter and the route dependencies that consume the resolved caller → `hex-restapi-auth`.
- Substituting a binding for a test → `hex-test-integration-setup`.
- Which libraries the project carries and the Alembic bootstrap → `hex-project-setup`; the ruff and mypy configuration → `python-toolchain`. Both are laid once, not per binding.
- What a settings class, its env prefix or a provider method is called → `naming`.
- Whether a class may be bound here at all, and which layer it belongs to → `hex-architecture`; it owns the layer contract this composition root sits outside of.
- The unit-of-work factory binding a multi-repository transaction needs → `hex-persistence` (`UNIT_OF_WORK.md`); the compensating-handler shape → `hex-application`.

## Template — dishka

`src/myapp/containers.py` is the only file this skill touches. Bindings are grouped into provider classes
by layer and by subdomain; `create_container` assembles them. **Every dependency is resolved by type** —
no binding is reached by its attribute name, so renaming a class cannot silently break a call site. The
template is the **base** a project extends — the provider classes and the handlers — and binds no
store, no optional adapter and no feature. **A store's or an add-on's binding lives with what it
binds**: the relational engine, session factory and repository in `hex-persistence`, the HTTP gateway
in `hex-capability-adapter`, the Redis repository in `hex-store-repository`, the token verifier in
`hex-restapi-auth`, the tunable in `hex-domain-model`, the unit-of-work factory in `hex-persistence`; a project merges the ones it has.

**Read `CONTAINER.md`** in this skill's directory before writing or extending `containers.py`. It
carries the base composition root — the provider classes in declaration order, `create_container` and
the settings check an entrypoint runs at start — and how an add-on binding merges into it; only `SKILL.md` is loaded automatically.

## Other bindings

- **`dependency-injector`.** The obligations are identical; what changes is the spelling and one extra
  rule. A `containers.DeclarativeContainer` subclass replaces the provider classes, `providers.*`
  replace the factories, and — the rule dishka does not need — **a binding is reached at the call site
  by its attribute name, which must be the snake_case form of the class** — the call site writes
  `<root>.<snake_case_attribute>()`. That name-based contract is unenforced: rename the class and the call
  site breaks at runtime. Test substitution differs in kind, and its trap is
  `hex-test-integration-setup`'s.

  | dishka | dependency-injector |
  |---|---|
  | `Provider` + `@provide` | `DeclarativeContainer` + `providers.*` |
  | `Scope.APP` | `providers.Singleton` |
  | `Scope.REQUEST` | `providers.Factory` |
  | `provides=IFooRepository` | `providers.Provider[IFooRepository]` annotation |
  | constructor arguments resolved by annotation | each argument passed explicitly |
  | generator factory + `container.close()` | `providers.Resource`, or teardown in the entrypoint |
  | `FromDishka[T]` at the call site | `container.<snake_case_attribute>()` |
  | an extra provider with `override=True`, before the container is built | `.override()` / `.reset_override()` on a built container |
  | `resolve_settings` over `SettingsProvider`'s declarations | each provider of the settings sub-container, walked with `.traverse()`, called once at start |

- **Manual composition — a plain factory module.** A service small enough not to want a framework
  writes `create_container()` as a function that constructs each object and returns a frozen dataclass
  of them. Every rule below still holds; declaration order becomes literal statement order, teardown
  becomes an `AsyncExitStack` the entrypoint closes, and per-operation lifetime becomes a stored factory
  callable rather than a stored instance. Building such a root constructs its settings, so it is its
  own startup check, and its construct smoke passes explicit settings rather than reading the
  environment.

## Rules

1. **Settings are constructed only at a composition root and bound there by type** (`python-settings`
   rule 13) — never in a handler, an adapter, an entrypoint module or another settings class. An adapter
   receives the whole settings object it reads, by type, as a constructor parameter; nothing below the
   root reads the environment.
2. **Every settings class the composition root provides is built when the process starts, before it
   serves or takes work** (`python-settings` rule 13). Under a graph that resolves lazily every
   entrypoint takes that step once at start — the REST shell in its lifespan (`hex-restapi-app`), a
   consumer's launcher before its first message — as a step of its own rather than part of building the
   root, which a test does with no environment. A root that several entrypoint processes share makes
   each of them require every settings class it provides, so each is deployed with all of them.
3. **The process's container module is the composition root.** Every concrete class is bound to the
   protocol it satisfies there and **only** there. Domain and application code never instantiates a
   concrete type.
4. **Every binding declares a lifetime, and the choice is deliberate.** Nothing is bound without an
   answer to "how long does this live".
5. **Anything holding a resource that must be released declares its teardown in the same place as its
   construction**, so construction and release cannot drift apart. The entrypoint closes the composition
   root exactly once, which runs every declared teardown (`hex-restapi-app`).
6. **Bindings are reached by type, not by name.** A call site names the type it needs; the composition
   root decides what satisfies it. Nothing outside the composition root may depend on how a binding is spelled.
7. **A unit of work is bound as its factory callable, never as an instance**, so each call opens its own
   transaction and no two callers share one. `hex-persistence`'s `UNIT_OF_WORK.md` shows the form it binds.

### Where a settings class sits

- **The module a settings class sits in** → `hex-conventions` block A. There is no central settings
  module.
- **The prefix's stem names the deployable, never a bounded context.** `naming` owns the prefix
  (`MYAPP_` plus the integration's segment). What only a hexagonal service adds: a deployable serves
  every context in it, so a context-named stem becomes wrong the moment a second context shares the
  store — shared settings collapse to one object (`hex-conventions` block C). Working inside one
  context, that context is the salient name; stem on the deployable anyway.

### Lifetimes

| Lifetime | Use for | Examples |
|---|---|---|
| **Process** | Stateless or expensive-to-construct objects whose lifetime spans the process. | Settings (`*Settings`), the engine, the session factory, a token verifier, a stateless library-backed adapter, **tunable value objects**, a stateless factory callable. |
| **Per operation** | Instances meant to be fresh for each request or each job, cheap to construct. | Every `*Handler`, every `*Repository`, **domain services** that compose them, a stateful adapter bound to per-request state. |

**Default to per-operation for application and domain artifacts. Reserve process lifetime for objects
that own a connection pool, parse the environment once, or are pure-data configuration.**

The pitfall: giving a repository process lifetime looks fine because it is stateless, but it freezes the
session factory it was built with for the life of the process, which defeats substituting one for a test
and forecloses any future per-request session. **Repositories are per-operation.**

### Declaration order

Group bindings in dependency order and keep them in that order:

- **Settings first** — everything else may depend on them.
- **Long-lived infrastructure** — engine, session factory, verifiers.
- **Cross-cutting helpers** — capability adapters needed by several subdomains.
- **Per-subdomain block:** repository → services that use it → handlers that use them.
- **Cross-subdomain dependencies come first.** If subdomain A's repository is consumed by subdomain B's
  handlers, declare it before B's block.

Where the mechanism evaluates the composition root top to bottom, this ordering is **load-bearing** — a
binding may only reference an earlier one. Where the mechanism resolves by type it is the reading order
instead, and a binding that would have to forward-reference is the signal that it is grouped wrong. When
adding a binding, find the right section and insert it after the latest declaration it depends on.

### Naming and access

- Factory and attribute naming → `naming`. These names are internal to the composition root.

### Settings lifecycle in the composition root

- Each `*Settings` is process-lifetime, built with no arguments by a factory in the composition root's
  one settings group. The startup check reads that group, so a settings factory declared anywhere else
  escapes it; the dishka spelling is in `CONTAINER.md`.
- A **tunable value object** that needs a single field gets a factory of its own, which reads the field
  off the settings object and passes it. Never pass raw settings fields around otherwise.

### What never goes in the composition root

- **No business logic.** It only wires.
- **No conditionals on the environment.** Different environments produce different settings *values*; the wiring
  stays the same. Hide a feature flag behind a settings field inside the implementation, never behind a
  branch in the wiring.
- **No imports from `restapi/` or another entrypoint.** The composition root sits below the entrypoint
  layer.
- **No mutable module-level state.** `create_container` returns a new composition root per call; a
  module-level singleton makes the test seam unreachable.
- **No instantiation of concrete domain types** — entities, value objects. It builds services, not data.

## Inlined typing / import rules

- Settings field typing and imports → `python-settings`.

- **A factory's return annotation is the binding's type**, and it is the whole contract:
  `-> PostgresSettings` binds `PostgresSettings`, `-> AsyncIterator[AsyncEngine]` binds `AsyncEngine`
  with a teardown. Use `provides=<Protocol>` when the class-attribute form binds an adapter to its port.
  An unannotated or loosely annotated factory binds the wrong type or fails at container construction,
  not at the call site.

- **Import each class from the package that DIRECTLY re-exports it — one `from .module import *` hop —
  never a grandparent** (`python-packaging`). This bites the nested infrastructure layout: a repository class lives in
  `infrastructure/<store>/repositories/<x>.py`, so import it from the **`repositories` subpackage** —
  `from myapp.infrastructure.postgres.repositories import FooRepository` — **not** from the `<store>`
  technology package. The technology-package form resolves at runtime but mypy reports `[attr-defined]`, because the
  intermediate `repositories/__init__.py` has a computed `__all__` mypy cannot evaluate across the
  `from .repositories import *` hop. A class sitting directly under the technology package — the `engine` or
  `settings` module, a capability adapter — is one hop away, so importing it from the technology package is
  correct.

- No `from __future__ import annotations` (`python-style`).

## Package wiring

Composition-root location → `hex-architecture`.

`containers.py` needs no package wiring at all: it is `src/myapp/containers.py`, a module of the
distribution's root package, and the root `__init__.py` does not re-export it — that file stays empty
(`python-packaging`'s carve-out for an application's root). For the classes it imports, follow
`python-packaging`.

## Hard stops

- Asked for an environment read, a new settings field, or a default on one → stop, use `python-settings`.
- Asked to add a binding whose dependency is not yet declared → stop, that dependency's own skill
  runs first.
- The composition root is asked to bind a store connection or transaction handle per operation, so a
  repository can be injected with one outside a unit of work → stop, nothing would then own the commit;
  use the standalone repository form, which opens and owns its own (`hex-persistence` for a relational
  store, `hex-store-repository` for a client-style one), or a unit of work (`hex-persistence`). A store
  whose client is the connection and has nothing to commit is bound at process lifetime, not per
  operation.
