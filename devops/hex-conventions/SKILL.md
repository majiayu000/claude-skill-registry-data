---
name: hex-conventions
description: Use when asking where does this file go or what is this class called — the registry deriving a path and class name from a bare identifier, plus the two store profiles with their connection-factory names and `<subdomain>:<Name>` cross-context resolution. Produces no file of its own. What a thing is *called* in general is `naming`; layer boundaries are `hex-architecture`.
paths: ["**/domain/**", "**/application/**", "**/infrastructure/**", "**/restapi/**"]
---

# Hexagonal Conventions — the derivation registry

This is the **derivation layer**: the rules that turn the bare identifiers a change introduces — an
entity name, a protocol name, a command base-name, a datastore kind — into concrete file paths, class
names and package placement. Other skills own what goes *inside* an artifact; this one owns the mapping
between a name and its place in the tree. It produces **no file of its own**.

All paths below are relative to the target package root `src/myapp/`. Worked names use a deliberately
neutral vocabulary — subdomains `foos` and `bars`, entities `Foo` and `Bar` — so nothing here reads as
belonging to one product. Technology tokens (`postgres`, `redis`, `s3`, `jwt`) stay concrete, because the
whole point of the infrastructure rule is that the folder is named after the real technology.

## When to use vs. neighbours

- Turning a bare identifier into a file path or class name → this skill.
- Deciding which repository form a datastore gets, or writing its connection factory → block B.
- Resolving a `<subdomain>:<Name>` reference, or deciding what is shared across contexts → block C.
- Layer boundaries → `hex-architecture`; `__all__`, the re-export contract and import forms → `python-packaging`.
- What goes *inside* the artifact whose name you just derived → the skill that owns it
  (`hex-persistence`, `exception-catalog`, `hex-application`). This skill is consulted **alongside**
  them, never instead of them — it produces no file of its own.
- Which libraries the project carries → `hex-project-setup`; how the toolchain is configured → `python-toolchain`.
- Choosing what an identifier should be *called* once you know where it goes — the derivation procedure and the naming tests → `naming`. This skill maps a name to a place; `naming` picks the name.
- One class per module, `__all__`, and the `__init__.py` re-exports → `python-packaging`.
- The composition root a store profile's connection factory is wired from → `hex-wiring`; the settings class that factory reads sits beside the store's adapter (`hex-persistence`, `hex-store-repository`) and follows `python-settings`.
- Whether the service should be hexagonal at all → `architecture-choice`.
- The command, query or handler that lives at the path you just derived → `hex-application`.

## A. Path & name derivation

**`snake_case`** — PascalCase → snake by inserting `_` before each interior capital, then lowercasing:
`IFooRepository` → `i_foo_repository`, `S3ObjectStorage` → `s3_object_storage`. Acronym runs are **not**
special-cased.

**`pluralize`** (table names) — `y` after a consonant → `ies`; trailing `s`/`x`/`z`/`ch`/`sh` → `+es`;
else `+s`. So `Category` → `categories`, `Box` → `boxes`, `Foo` → `foos`. Table name =
`pluralize(snake(aggregate))`. That a table name is derived by one rule declared once is `persistence`
rule 13; this is the hexagonal family's rule. Singular and plural table names are both long-standing
house styles with no winner, so the catalogue picks one, and a project that prefers singular changes
this one derivation rule, not every table.

**Class names** carry only the identifier plus a derived suffix. Protocol identifiers already include
their `I`-prefix / `Repository` suffix.

Everything below is mechanical **given a good identifier**, and this skill cannot supply one: it turns
`Foo` into a path, it does not judge whether `Foo` was the right word. Choose the identifier by
`naming`'s rules first — a generic one (`Manager`, `Data`, `Worker`) propagates through
every derived path and class name here, multiplying one careless choice across the tree.

| Artifact | Given | Derived class name(s) | Derived file path(s) |
|---|---|---|---|
| domain enum | `FooKind` in subdomain `foos` | `FooKind` | `domain/foos/foo_kind.py` |
| domain value object | `FooCode` in `foos` | `FooCode` | `domain/foos/foo_code.py` |
| tunable value object | `FooRetentionTunable` in `foos` | `FooRetentionTunable` | `domain/foos/foo_retention_tunable.py` — built from a settings class by its own provider (`hex-domain-model`) |
| domain entity | `Foo` in `foos` | `Foo` | `domain/foos/foo.py` |
| domain service | `FooVerifier` in `foos` | `FooVerifier` | `domain/foos/foo_verifier.py` |
| domain filter | `FooListFilter` in `foos` | `FooListFilter` | `domain/foos/foo_list_filter.py` |
| filter sort enum | `FooSort` in `foos` | `FooSort` | `domain/foos/foo_sort.py` — its own module, not folded into the filter's (one class per module); the filter imports it |
| repository protocol | `IFooRepository` in `foos` | `IFooRepository` | `domain/foos/i_foo_repository.py` |
| capability protocol | `ICanSendNotification` in `foos` | `ICanSendNotification` | `domain/foos/i_can_send_notification.py` |
| unit-of-work protocol | `IUnitOfWork`; a second scope `I<Scope>UnitOfWork` | `IUnitOfWork` / `I<Scope>UnitOfWork` | `domain/uow/i_unit_of_work.py` / `domain/uow/i_<scope>_unit_of_work.py` — the cross-cutting subdomain `uow`, never an aggregate's (`hex-persistence`) |
| domain exception | `NotFoundError` | `NotFoundError` | appended to `domain/exceptions.py` (single catalog) |
| application command | `CreateBar` (subdomain derived, see below) | `CreateBarCommand` + `CreateBarHandler` | `application/bars/create_bar_command.py` + `application/bars/create_bar_handler.py` |
| application query | `ListBars` | `ListBarsQuery` + `ListBarsHandler` + `ListBarsResult` | `application/bars/list_bars_query.py` + `_handler.py` + `_result.py` |
| datastore | named `<name>`, kind `<kind>` (e.g. `baz_store` on a `redis` store) | — (a configured resource, no class) | `infrastructure/<kind>/connection.py`, holding `create_<name>_client` |
| settings | `RedisSettings` | `RedisSettings` | `infrastructure/redis/redis_settings.py` — subpackage = the consuming technology; one settings class per configured component (`python-settings` rule 1) |
| repository adapter | implements `IFooRepository`, backs `Foo`, on store `main` | `FooRepository` | `infrastructure/<store-kind>/repositories/<repository-stem>.py` (+ a write-once `Table` at `infrastructure/<store-kind>/tables/foos.py` for a relational store) |
| capability adapter | implements `ICanClassifyFoos`, adapter `http`, role `FooClassifier` | `HttpFooClassifier` | `infrastructure/http/http_foo_classifier.py` |
| wire schema | `FooCreateRequest` for resource `foos` | `FooCreateRequest` | grouped into `restapi/schemas/foos.py` |
| endpoint | method + path, resource `foos` | endpoint function (name from method + path) | grouped into `restapi/routers/foos.py` |
| middleware | `RequestId` | `RequestIdMiddleware` | `restapi/middleware/request_id.py` — except the catch-all, which completes the error handlers in `restapi/error_handler.py` (`hex-restapi-app` rule 6) |

**An application handler's subdomain is derived, not chosen.** It is the subdomain of the first
repository protocol the handler depends on (a repository protocol carries its own subdomain); with no
repository dependency, fall back to the subdomain of the first domain entity it touches. So `CreateBar`
depending on `IBarRepository` (subdomain `bars`) lands in `application/bars/`.

**Infrastructure groups by external TECHNOLOGY, never by a domain subdomain and never under a catch-all
`db/`.** The technology token is:

- a repository's **store kind** — the kind of the datastore it sits on; with no datastore named, the
  project's single relational store under whatever kind it is named (block B: a project has at most one
  relational kind). Relational repositories, their write-once table, and the shared engine / session
  factory / shared-metadata bootstrap all sit under `infrastructure/<relational-kind>/`
  (`repositories/`, `tables/`).
- a non-relational datastore's **kind** — `infrastructure/<kind>/`, one directory per kind the project
  actually uses, holding `connection.py` (the `create_<name>_client` factory) and its settings. The kind
  is the vendor's own token, kept concrete: a cache, a document store and an index each get their
  own directory under their own name.
- a capability adapter's **adapter** token — `infrastructure/jwt/`, `infrastructure/s3/`.
- a settings class's **consuming technology** — the adapter of the capability that uses it, or the kind of the
  datastore that uses it; a settings class with no consumer falls back to its own snake name.

**Capability adapter class** = `<AdapterPascal><Suffix>`, where `Suffix` is the capability's agent-noun
role when there is one (adapter `http`, role `FooClassifier` → `HttpFooClassifier`) and otherwise the
protocol name minus its `ICan` prefix (adapter `http`, implements `ICanClassifyFoos`, no role →
`HttpClassifyFoos`). The role is named explicitly precisely because the agent-noun is not mechanically
derivable from the verb.

**Repository file stem — aggregate-derived for a relational store, protocol-derived for a client store.**
The class is always `<Aggregate>Repository` (backs `Foo` → `FooRepository`), but its **file stem** depends
on the store profile (block B), because an aggregate's one authoritative store may have a derived
projection beside it — an index over the same aggregate, on a second store, behind a narrower port of its
own (`hex-store-repository` rule 1):

- a **relational store** repository → `<snake(aggregate)>_repository.py` (`Foo` on `main` →
  `foo_repository.py`).
- a **client-style store** repository → the **protocol-derived** stem: the implemented protocol name minus its
  leading `I`, snaked (`IBazRepository` on `baz_store` → `baz_repository.py`).

So a `Foo` stored relationally behind `IFooRepository`, with a search index beside it behind an
`IFooSearchIndex`, lands two distinct files — `<relational-kind>/repositories/foo_repository.py` and
`<index-kind>/repositories/foo_search_index.py`. An aggregate-only stem would collide.

**Which repository form applies is decided by the store profile, not the vendor.** A relational store →
the SQLAlchemy Core form in `hex-persistence`. **Any** client-style store → a vendor-agnostic
client-repository form covering every key-value / cache / document backend. A new client-style backend is
**its own `infrastructure/<kind>/` package under that form**, never a new form.

**Imports and package mechanics are not restated here.** A referenced type resolves to its owning module:
same-subdomain domain types use a relative `.module` import, cross-subdomain a relative `..subdomain`,
cross-layer an absolute `myapp.domain.<subdomain>` import, stdlib its usual import, builtins none.
`python-packaging` owns the import rules, `__all__`, and the `from .module import *` re-export contract
the collapsed import form depends on; `hex-architecture` owns only which layer may import which.

## B. Store profiles

A datastore's kind is a free token — the vendor's own name, kept concrete — and every kind falls into
one of exactly **two** profiles:

- **Relational** — reached through the shared engine bootstrap. The repository is `hex-persistence`'s
  form, reusing the one engine and session factory under `infrastructure/<relational-kind>/` (a project
  has at most one relational kind, whatever it is named), with a write-once `Table` under its `tables/`.
  The file stem is aggregate-derived (block A).
- **Client-style** — reached through an injected SDK client. The repository is `hex-store-repository`'s
  form; `infrastructure/<kind>/connection.py` holds a `create_<datastore-name>_client(settings)` factory
  that the composition root binds at process lifetime and injects into every repository on that store,
  and there is **no** table. The file stem is protocol-derived (block A).

**The connection factory is complete glue, not a stub.** It carries zero judgment — it is a fixed
function of the settings shape — so it is written in **full**, never as `raise NotImplementedError`. A
stub type-checks and lints clean, then crashes the container at app construct. The factory name is the
datastore's *name*, not its kind: `create_baz_store_client` for a datastore named `baz_store`. The
relational engine and session factory are `hex-persistence`'s; a client-style store's `connection.py` is
`hex-store-repository`'s, worked for redis.

## C. Multi-context apps

A deployable app may hold more than one bounded context in ONE package — contexts as sibling subpackages
keyed by subdomain (`domain/foos/` + `domain/bars/`, `application/foos/` + `application/bars/`, …). A
single-context app is the degenerate case. Two rules govern the rest:

**A cross-context reference is a cross-subdomain reference.** Where a name is written
`<subdomain>:<Name>` — a `bars` service depending on `foos:IFooRepository`, its body referencing
`foos:FooKind` — this is **not special**. Strip the `<subdomain>:` prefix and resolve `<Name>` in the
`<subdomain>` subpackage of the appropriate layer, by the ordinary import rules. So `foos:IFooRepository`
injected into a `bars` service → `from myapp.domain.foos import IFooRepository`. The prefix **is** the
subpackage, and the provider that injects it is wired in the one shared `containers.py`.

**The shared substrate exists once, as the union of the contexts.** Per-context artifacts — everything
under `domain/<subdomain>/` and `application/<subdomain>/`, a context's repositories and adapters under
their technology subpackage, its entrypoint modules and per-resource schemas — are per context. These are
**one each for the whole app**, and writing them per context would clobber the other context's
contributions. **Each entry below exists only where the app has the thing it names** — the rule is the
union, not the list, so an app with no relational store carries no relational bootstrap row and a
worker- or CLI-only app carries no HTTP ones; whatever the app does have, it has once:

- `domain/exceptions.py` — the single catalog is the union of every context's exceptions, deduped by
  name; two contexts both declaring `ValidationError` collapse to one.
- the relational bootstrap under `infrastructure/<relational-kind>/` (engine, session factory, shared
  metadata) and the single relational settings class — one relational substrate; that settings class, or
  a datastore named in several contexts, collapses to one, deduped by name and environment prefix. Only
  where a relational store backs a repository at all.
- **the shell of each entrypoint package the app has** — one per entrypoint kind, registering **every**
  context's contribution to it: `restapi/main.py` includes every context's router, and a worker's or a
  CLI's shell registers every context's consumers or commands the same way.
- **each entrypoint package's cross-cutting modules** — failure rendering, shared dependencies, shared
  error schemas — one each per entrypoint package, never one per context, and used by every context that
  needs them rather than only the one that introduced them. Under the HTTP binding that is
  `restapi/error_handler.py`, `restapi/schemas/errors.py` and `restapi/dependencies.py`.
- `containers.py` — ONE composition root, binding every context's classes.
- `pyproject.toml` — the substrate plus the union of every context's packages (`hex-project-setup`).

Dedup is by identifier: the same name and shape across contexts → one artifact. A genuine **conflict** —
same name, different shape — is never silently merged. Stop and surface it.

## Rules

1. Choose identifiers with `naming`, then check every derived artifact against block A's table. An
   artifact no row derives gets its row added here first; a path or class name is never invented.
2. Derive an application handler's subdomain, never choose it: its first repository's subdomain, or its
   first domain entity's when it has no repository dependency.
3. Place an injected tunable value object by block A's row; how a settings class builds it is
   `hex-domain-model`'s.
4. Select each infrastructure directory by the consuming technology, using block A's technology-token cases —
   never by subdomain, never under a catch-all `db/`.
5. Derive a repository's file stem from the aggregate for relational stores and the protocol for client
   stores, or an aggregate held on two stores lands two colliding files; select its implementation form
   through block B's profile.
6. Place a new datastore kind under one of block B's two profiles — its own `infrastructure/<kind>/`
   package, never a new repository form.
7. Write every connection factory complete, per block B, under the datastore-name-derived factory name:
   a stub type-checks and lints clean, then crashes at app construct.
8. Resolve context-qualified references through the named subdomain, using `python-packaging` for
   imports and `hex-architecture` for layer boundaries.
9. Build the shared substrate from block C's union of contexts; deduplicate identical declarations and
   surface incompatible shapes.
10. Entity ids and where they are minted → `hex-application`, command handler rule 6.

## Hard stops

- Asked to write the artifact whose path or name was derived here → stop, this skill produces no file;
  the skill that owns the artifact writes it.
- Two contexts declare the same name with different shapes → stop, do not silently merge; surface the
  conflict.
