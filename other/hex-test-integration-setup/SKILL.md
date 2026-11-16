---
name: hex-test-integration-setup
description: Use when laying or changing the `tests/integration/conftest.py` hierarchy one hexagonal package's suite rests on — session-scoped testcontainers, the Alembic run and the disposable-database guard, savepoint-rollback isolation through the `session_factory` fixture, each store add-on's fixtures (the key-value store is the worked one), the per-test dishka composition root whose infrastructure providers are overridden, and `real_app` over it where the service has a REST entrypoint — or the same fixtures as one plugin module several hexagonal workspace members share. Maps the whole suite tree and names the skill that writes each file in it. Owns the Postgres container fixture; testing a repository against it is `hex-test-repository-contract`. Not a flat-layered service's fixtures, which are `flat-test-integration-setup`, in the `pyhouse-flat` plugin.
---

# Hex Test — Integration Setup

Consult `test-principles` for the testing constitution. Where this skill contradicts `test-principles`, the constitution wins.

One-shot per project, and everything else in the integration suite depends on it.

## When to use vs. neighbours

- Laying the base conftest for the first time, or changing a fixture in it → this skill.
- A repository contract test → `hex-test-repository-contract` (consumes `session_factory`).
- An API endpoint test → `hex-test-restapi-endpoint` (consumes `real_app`, the REST add-on, and the store's own fixture where it seeds rows).
- The app-wide checks — the construct smoke, the error shape of every advertised code, CORS, the request-size limit → `hex-test-app-invariants`; they build the app themselves and take none of these fixtures.
- A handler test that runs on in-memory fakes and needs no database at all → `hex-test-application-handler`; none of these fixtures apply to it.
- A capability adapter's own assertions — the HTTP gateway over a stub transport, the SDK-error translation, the pure-CPU case → `hex-test-capability-adapter`. The session-scoped container its backend needs is still declared here.
- The signing-key and token-minting fixtures, the authenticated client, and the `jwt_settings` override `container` grows in an auth app, where `container` then resolves only under `tests/integration/api/` → `hex-test-restapi-auth`. Only for an app that declares auth; this skill is complete without it.
- The route-side auth dependencies themselves → `hex-restapi-auth`.
- Per-resource row factories (`make_foo`, …) → not this skill; they live in `tests/integration/api/<resource>/conftest.py` next to the tests that use them.
- Which scope a fixture takes, which conftest level it belongs at, builders versus fixtures → `test-principles`, the constitution. This skill is the hexagonal artifact that implements it.
- The runner's configuration block → `python-toolchain`.
- The same fixtures for a flat-layered service → `flat-test-integration-setup`, in the `pyhouse-flat` plugin. Several hexagonal members of one workspace sharing these fixtures → this skill, under `## Other bindings`.
- The composition root has no `session_factory` binding, or no way to pass extra providers into it → `hex-wiring` first; the substitution seam is `create_container`'s parameter, not something a test can bolt on.
- Turning "the sanctioned handle is the only one opened under `tests/integration/`" into a static grep firewall → `test-architecture-rule`, which owns the firewall mechanism. The obligation itself is `test-principles`' (reliability rule 6); no firewall for it ships with the catalogue, so a project that wants it machine-checked writes one.

## Template(s) — pytest, testcontainers, Alembic, SQLAlchemy, dishka

```
tests/
├── unit/                             # nothing here takes a fixture from integration/
└── integration/
    ├── conftest.py                   # base: Postgres container, guard, migrations, engine, `session_factory`,
    │                                 # `container` + each add-on's fixtures (the key-value store is the worked one);
    │                                 # `real_app` only with a REST entrypoint
    ├── postgres/                     # only with a relational store; a client store's sit in <store-kind>/
    └── api/                          # only where the app has an HTTP entrypoint
        ├── conftest.py               # only in an app that declares auth — hex-test-restapi-auth's
        └── <resource>/conftest.py    # per-resource row factories — not this skill's
```

The files that fill that tree belong to the skills that write them, each of which shows its own
fragment: `tests/unit/fakes/` to `hex-test-application-handler`; `tests/unit/test_architecture.py` to
`test-architecture-rule`; `tests/unit/restapi/` to `hex-test-app-invariants`; `tests/helpers/`,
`api/conftest.py` and the anonymous-caller probe to `hex-test-restapi-auth`, only for an app that
declares auth; one file per endpoint under `api/<resource>/` to `hex-test-restapi-endpoint`.

**Read the sibling `CONFTEST.md` before writing or changing any fixture in that hierarchy.** Only this
file is loaded automatically, so open it rather than reconstructing the fixtures from the obligations
below: it carries the base `tests/integration/conftest.py` — relational only, framework-free, ending at the
per-test `container` — and the add-ons a project lays on top of it: each add-on's fixtures (the
key-value store, Redis, is the worked one) with its substitution in `container`, and `real_app` for a
REST entrypoint; then the import rule a root conftest must obey, and the three spellings this binding
adds — the savepoint mode on the outer connection, `expire_on_commit`, and the plain fixture value a
substituting factory returns.

## Other bindings

### Provisioning — where the store under test comes from

The obligations below hold under every one of these; what changes is who creates the store, how the
schema gets there, and what the disposability marker is set by.

- **A developer- or CI-supplied store.** The suite starts nothing; the opt-in and the marker are
  `test-principles` reliability rules 1 and 6, the container fixtures go and everything else stays. A
  store the suite did not start is emptied only behind the same disposability marker; with no
  relational store, the guard moves to the store's add-on.
- **An in-process store.** Disposable by construction, so the fixture that creates it sets the marker
  and the schema step runs in-process; an engine without nested transactions isolates by a fresh store
  per test (`test-principles` reliability rule 2).
- **A fresh schema (or database) per session on a shared server.** The session creates a uniquely-named
  schema inside a long-lived server and drops it at session end. That creation is what makes the target
  disposable, so it sets the marker; the schema step targets the new namespace and the per-test handle
  sits inside it unchanged. Reach for this where a container is not available to the suite but a server
  is.

### Dependency injection

- **`dependency-injector`.** The container fixtures, the migration run, the guard and the savepoint-rollback `session_factory` are unchanged; only the composition-root fixture differs, and it differs in kind rather than in spelling. There is no `TestInfrastructureProvider`: the fixture builds the real container, calls `.override(value)` on each provider **after** construction, and must `.reset_override()` each one in the `finally` block. Because the substitution lands on a live container, an already-resolved singleton may have captured the pre-override value — the classic case is a singleton whose `__init__` snapshots a settings field — so the same `finally` block also calls `.reset()` on every such capturing singleton — an explicit teardown in the fixture that overrode it, never an autouse one, which `test-principles`' closed autouse set does not admit — and `containers.py` has to be audited once to find them. That failure mode does not exist under the primary binding, where the graph is assembled with the test factories already in it.
- **Manual composition.** The composition root is a factory function, so the fixture calls it with the test objects as arguments. No provider classes, no override marking, and teardown is whatever `AsyncExitStack` the factory returned.

### Shared across workspace members

- **One pytest plugin module several hexagonal members load** (`python-workspace`; `test-principles`,
  *Where tests and fixtures sit* rules 3–4). The session half — containers, guard, migration run,
  engine, each add-on's container — moves into it; each member keeps its isolation handles and
  `container` (with `real_app` where it has a REST entrypoint); the migration run executes from the
  schema-owning library's directory (`python-workspace` rules 3–4).

## Rules

Consult `test-principles` for the testing constitution.

### Scope

- **`tests/integration/conftest.py`** — the containers, the engine, the transaction-rollback `session_factory` and the
  per-test `container`; `real_app` joins them only with a REST entrypoint. A service without one —
  queue-driven, RPC — has a base conftest that ends at `container` and imports no web framework: a
  framework import there fails every collection of a service that does not install it.
- **The autouse pair is the disposable-database guard and the migration run**, both session-scoped and
  both in the base conftest, for a relational app — the closed autouse set `test-principles` allows.
  Everything else, `session_factory`, `container` and `real_app` included, is requested by name.

The Postgres machinery — engine, migration run, savepoint-rollback `session_factory` — is laid only where the app has
a relational store; a service whose stores are all client-style keeps `container` and each store's
add-on, isolated by a per-test namespace (`test-principles` reliability rule 2).

**What this skill owns, exactly: every session-scoped fixture, for every store kind.** Containers,
engines, migration runs and long-lived clients belong here because one container per session is the
guarantee the whole setup rests on, and a fixture duplicated into a store-kind conftest breaks it. The
**per-test** half — a fresh collection, key-prefix, database or bucket path, and its teardown — belongs
in the sibling `tests/integration/<store-kind>/conftest.py`, next to the tests that consume it
(`hex-test-repository-contract`) — **unless `container` binds it too**, in which case it sits up-tree
beside the session half so a route under test reaches it. The worked add-on in `CONFTEST.md` is that
case: the key-value store's per-test client, whose teardown empties the suite's own container, is bound
by `container`, so an entrypoint never reaches a store the environment names.

### The obligations

The suite obligations — an empty store per test with the undo in the handle it is given, or a namespace
per test where the store has no undo; one sanctioned handle; the expensive resource per session and the
isolated unit per test; the disposability guard; the schema established by the project's own schema
path; fixed natural keys — are `test-principles`' (reliability rules 1, 2 and 6, *Fixture scope rules*,
*Datastore contract* rule 8, *Assert strength*). Here the undo also covers the subject's commits,
through the savepoint handle. What this file adds is the substitution, stated without a mechanism
because every binding of this file delivers it:

1. **Substitution happens before the composition root is built, never after.** The test's
   infrastructure objects are in the graph from the start, so nothing production-side can have resolved
   and captured a pre-substitution value, and there is no reset or teardown ordering to get right.
2. **A substituted binding is the fixture object itself, under the exact type the production binding
   declares.** No wrapper, no adapter — the type is what binds it.
3. **Whatever the composition root opened, the fixture closes.** One close call in the fixture's
   `finally`, releasing the test's resources in reverse order.

## Inlined typing / import rules

- `create_container` and `create_app` are imported **inside** the `container` and `real_app` fixture bodies, never at module level (see the root-conftest note in `CONFTEST.md`).
- Full annotations on every fixture signature. `AsyncIterator[T]` for yielding fixtures with cleanup.
- No `from __future__ import annotations`.

## Hard stops

- The composition root has no `session_factory` binding, or no way to pass extra providers into it → stop, use `hex-wiring` first; the substitution seam is `create_container`'s parameter, not something a test can bolt on.
- A token-minting fixture, a signing keypair or an authenticated client is put in the base conftest → stop, use `hex-test-restapi-auth`; they belong to the auth-only fixture set.
- A per-resource row factory (`make_foo`, …) is added inside the base conftest → stop, use `hex-test-restapi-endpoint`; those live in `tests/integration/api/<resource>/conftest.py`, next to the tests that use them.
- The conftest is to carry an add-on for a store the project does not have → stop, write nothing; an add-on goes in with its adapter and not before.
