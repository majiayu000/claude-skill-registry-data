---
name: test-principles
description: Use when writing or changing tests in any Python project and the question is a rule rather than a file — the layer budgets, where tests and shared fixtures sit and what may be autouse, fixture versus module-level builder, the substitution ladder and no-mocks contract, assert strength and literal expected values, intercepting HTTP, what a test against a real datastore pins, reliability, and the failing test a defect's fix starts with. Holds for a service, a library or a CLI tool alike. The fixture files a family lays are `hex-test-integration-setup`'s or `flat-test-integration-setup`'s. - Also when fixing a defect or a bug, before the fix is written.
---

# Test — Principles (reference)

Every test skill consults this one. The rules here are the **catalog-level testing constitution** for any Python project, whichever architecture family it is in or none; where another test skill contradicts this constitution, this constitution wins. Reference only — it produces no file.

The obligations below are runner-neutral. Every *spelling* of them is **pytest** — the fixture and
marker decorators, parametrization, path-based collection, and the `[tool.pytest.ini_options]` block
that declares the run. That is this catalogue's binding, not part of the constitution; what moves
under another runner, and what does not, is in `## Other runners`.

## When to use vs. neighbours

The `hex-*` and `flat-*` names in this skill are forward references into the `pyhouse-hex` and
`pyhouse-flat` plugins. Each one routes to the skill that *produces* a file in that family; none
carries a rule this skill leaves unstated, so with neither plugin installed the constitution is still
complete.

- Adding or changing any test → this skill **and** the skill that owns that test file; this one is
  reference-only and produces no file.
- Domain unit tests → `hex-test-domain`.
- Handler tests and protocol fakes → `hex-test-application-handler`.
- **Where a fixture lives is this skill's rule; the fixture file is not.** A distribution's
  `tests/integration/conftest.py`, its containers and isolation fixtures, and the shared plugin module
  several members load → the family's integration-setup skill — `hex-test-integration-setup` for a
  hexagonal package, `flat-test-integration-setup` for a flat one.
- The runner's configuration block that declares the run → `python-toolchain`.
- The root configuration that registers a shared fixture module across several distributions →
  `python-workspace`.
- A static "no X in Y" invariant → `test-architecture-rule`.
- A skill that owns a test file contradicts something here → fix that skill; this constitution is the
  source of truth.
- Naming a builder, fixture or test function → `naming`.

## Other runners

- **A different runner** — `unittest` with a plugin set, or any collector of its own. What changes is
  spelling: how a fixture declares its setup, teardown and scope; how one body is run over a set of
  inputs; how a marker is registered and selected; where the run's configuration is declared. What
  does not change is the whole constitution — the layer budget and what each layer may touch, the
  naming contract, the substitution ladder and the no-mocks rule, the AAA shape, assert strength, and
  the isolation and determinism rules. A runner with no fixture lifecycle pays for it in duplicated
  `setUp`/`tearDown`; that is a cost to carry, never a licence to share state between tests.
- **A different async plugin in `pytest-asyncio`'s role** (`anyio`'s pytest plugin). Auto mode and the
  marker ban are one obligation in pytest's spelling: async-ness is declared once, project-wide, never
  per test function. Whatever declares it, it is one declaration.
- **A different HTTP interception library** — `respx` under `httpx` (or under `httpx2` through
  `pytest-httpx2`), `responses` under `requests`, `aioresponses` under `aiohttp`. These patch the
  library rather than being handed to the client, so how a route is registered and read back changes,
  and rule 1's patching clause is the one that binds: the patch is active for the whole test. The other
  rules are unchanged.

## Rules

### The testing pyramid

A row is a **test layer**, and what defines one is what it substitutes, what it leaves real, the defect
class it is the cheapest place to catch, and the budget that keeps it cheap. The last column names the
skills that *produce* that row's files in each architecture family — those are bindings of the layer,
not its identity. A project in neither family has the same layers and writes them itself.

| Layer | What is substituted | What stays real | What it catches | Budget | Bindings |
|---|---|---|---|---|---|
| Pure unit | nothing — the subject has no out-of-process collaborator | the subject | construction-time invariants, identity and equality, enum and constant values, single-rule policies, filter and normalize functions, schema validation, the exception catalog | < 10 ms | `hex-test-domain`; elsewhere the test file stands alone |
| Collaborator unit | every out-of-process collaborator, by an in-memory double the subject already accepts, or by the runtime's own test environment | the subject's own orchestration | orchestration and step dispatch, branch selection, partial-update semantics, normalization, retry and continuation policy, exception propagation, compensating undo | < 50 ms, or < 2 s where the double is a runtime's test environment | `hex-test-application-handler`, `flat-test-entrypoint` (orchestration level) |
| Boundary unit | only the transport beneath one dependency — the socket, never the dependency's own code | the client's request building, response parsing and error translation | request shape, response parsing, library-error → catalog translation, timeouts | < 100 ms | `flat-test-service-client`, `hex-test-capability-adapter` |
| Wiring smoke | nothing, but nothing out-of-process is reached either | the object graph, constructed the way the entrypoint constructs it | construct-time wiring and framework dependencies the type, lint and unit layers all miss; a generated schema's build, where the entrypoint generates one | < 100 ms | `hex-test-app-invariants` (in `pyhouse-hex`); elsewhere the project writes it where its entrypoint builds an object graph |
| Datastore contract | nothing — a real store, started and disposed by the suite | the driver, the schema, the statements | constraint behaviour and generated constraint names, conflict and upsert semantics, cascades, returned and auto-updated values, driver-error translation, chunking where a write batches | < 500 ms | `hex-test-repository-contract`, `flat-test-persistence` |
| Entrypoint | nothing, or only the transport beneath a remote dependency | the entrypoint driven the way a caller drives it, with its real dependencies | dispatch and routing, dependency wiring, input and output validation, the run wired end to end; where the entrypoint authenticates, role gating and tenancy scoping | < 1 s, or < 2 s with a real datastore behind it | `hex-test-restapi-endpoint` (with `hex-test-restapi-auth`), `flat-test-entrypoint` |
| Surface invariant | nothing — the surface is enumerated from the running program | the program's own declared surface | global properties no single test owns — every error code the published contract advertises carrying the program's one error shape, every protected route refusing an anonymous caller, cross-origin and request-size policy | < 500 ms | `hex-test-app-invariants` |
| Architecture | everything — nothing runs | the source tree, read as text | static "no X in layer Y" invariants | < 100 ms | `test-architecture-rule` |

**A project has the layers its subject has, and writes no others.** One with no datastore has no
datastore-contract row and is missing nothing; a library's entrypoint layer is its public API called
the way a caller calls it, and its surface-invariant layer is what that API promises — every name in
`__all__` importable, every documented error class reachable; a command-line tool's entrypoint layer
invokes the command in process through the CLI library's runner (`python-cli` rule 6). A row with
no defects of its own to catch is not written to fill the table.

The shape is the goal: **fast layers run on every save; slow layers run on every commit; the slowest
layers run in CI.** If a pure unit test starts touching IO, or a datastore test starts constructing the
entrypoint, the layer is leaking and the speed budget is gone.

### Where tests and fixtures sit

1. **Tests sit beside what they cover**, in the distribution's own `tests/`, split into `unit/` —
   nothing must be running, so a unit test takes a fake, a stubbed transport or nothing, never a real
   adapter, engine or connection — and `integration/` — something must. In a repository of several
   distributions each member keeps its own, so a member is read, reviewed or extracted together with
   the tests that pin it. The one exception is a test whose subject is the repository itself, the grep
   firewall (`test-architecture-rule` owns both placements).
2. **A fixture lives in the lowest conftest every one of its consumers sits beneath.** Resolution walks
   from the consuming test outward, so a fixture defined down-tree is visible only to tests under it —
   and a fixture up-tree that consumes a down-tree one is usable only from there.
3. **Fixtures several distributions share live in one module registered once per session** — a pytest
   plugin, never a conftest copied into each member, which is two copies of one setup waiting to
   diverge. It sits
   beside the tests of the library that owns what it provisions, never in `src/`: test support does not
   ship in the wheel.
4. **Nothing is autouse except the suite's safety guard, its schema setup and its per-test isolation
   reset, where the suite has a store** — and nothing in a shared plugin module is autouse at all,
   because it loads for every collection, pure-unit runs included; a member turns one on in its own
   integration conftest. Each autouse fixture is documented; no one adds a "convenience" autouse.

### Fixture vs. builder

| | Builder (module-level `def`) | Fixture (`@pytest.fixture`) |
|--|------------------------------|------------------------------|
| Use for | Constructing one value with sensible defaults — a record, an entity, a payload | Anything with a lifecycle — a container, an engine, a connection, a stubbed transport and the client over it, a factory that writes real rows |
| Lives in | The test module that uses it; one several files share is a plain function under `tests/helpers/`, imported directly | A conftest at the level *Where tests and fixtures sit* rule 2 picks |
| Examples | `_foo(*, name: str = "alpha") -> Foo` | a rollback-scoped connection, a per-test namespace, `make_foo` writing one real row per call |
| Why | Builders are pure Python; wrapping one in a fixture adds ceremony without value. | Fixtures own setup and teardown — sessions, transactions, transports — which is what they are for. |

**Rule:** if the thing you're constructing has no setup or teardown beyond its `__init__`, write a module-level `def`, not a fixture.

### Fixture scope rules

- **Session scope** — what is expensive to construct and stateless across tests: a container, an
  engine or pool, a long-lived client, the schema setup and the guard in front of it. A feature the
  project does not have contributes none.
- **Function scope** — everything else: every isolation handle, every per-test namespace, every
  row factory, every client over a stubbed transport. Per-test rows are non-negotiable: rollback or
  wipe isolation requires them.
- **A session-scoped async resource and everything that uses it share one event loop.** A connection
  or client opened on one loop fails when used or closed on another — on first use, or with some drivers
  only at teardown after a command errors, as an unrelated "event loop is closed". Under this binding both `asyncio_default_fixture_loop_scope` and
  `asyncio_default_test_loop_scope` are `"session"`.
- **No `module`-scoped or `class`-scoped fixtures.** Two scopes are enough — one for what is expensive and stateless across tests, one for everything else — and every scope beyond them is state shared with tests that never asked for it, in a grouping (the file, the class) that exists for readability rather than for lifecycle. A test that passes alone and fails beside its neighbours is the cost.

### Test naming

- **Test file**: mirror the source file with a `test_` prefix, inside the tests of the distribution that owns it. `src/myapp/foo_summary.py` → `tests/unit/test_foo_summary.py`.
- **Test function**: `test_<rule_being_pinned>` in snake_case. `test_assigns_uuid_and_stores`, `test_duplicate_name_raises_conflict`, `test_partial_update_leaves_unspecified_fields_untouched`. The name **is** the spec line — reading the file's `def test_*` list reads as a list of behaviors.
- **A test file whose subject is the tree, not a module, is named for the property it pins**, because
  there is no source file to mirror — `test_architecture.py` for the static source rules
  (`test-architecture-rule`). Reach for this only when the file genuinely covers no single module; a
  file named for a subject when it could have been named for its source is how a suite grows a
  catch-all.
- Builder, failure-injection subclass, and other identifier names → `naming`.

### When to parametrize — and when not to

**Use `@pytest.mark.parametrize`** when:

- The parameter set is **discovered from the running system** — every operation an app serves, every entry its published document lists; `hex-test-app-invariants`, in the `pyhouse-hex` plugin, is one example.
- The test is **input-domain coverage**: a single behavior verified against many inputs (10 invalid emails, 20 valid date formats). The behavior is one thing; the inputs vary.
- Adding a new parameter would extend, not duplicate, an existing test set.

**Every parameter set yields one reported case per item, never a loop inside one test** — a loop stops
at the first failure and hides the rest. A discovered set is also asserted non-empty, by a separate test
that does not take the parameters — an empty parameter set reports as skipped, so a check inside the
parametrized body never runs, and the run goes green having checked nothing. Under this binding a
discovered set is read in the collection hook (`pytest_generate_tests`): a fixture cannot feed
parametrization.

**Do not parametrize** when:

- Each case is a distinct rule whose **name forms part of the spec**. `test_assigns_uuid_and_stores` and `test_duplicate_name_raises_conflict` are different behaviors; collapsing them into `@pytest.mark.parametrize("scenario, expected", [...])` hides the spec lines in tuples.
- The case differs in setup or assertions, not just input values.
- Each case pins a different construction-time invariant — those are individual rules.

The rule of thumb: if you can read the parametrize ids out loud and they sound like a list of behaviors, parametrize is fine. If you can't (because the ids would be `0`, `1`, `2`), the cases are different rules and want different `def test_*` names.

### AAA structure (Arrange / Act / Assert)

Every test follows three visually-separated blocks. **Separated by blank lines, never by comments** —
`# Arrange` / `# Act` / `# Assert` are structural labels, which `python-style` bans and deletes. The
phases are the shape of the code, not an annotation on it:

```python
def test_summary_counts_every_foo() -> None:
    foos = [_foo(name="alpha"), _foo(name="beta")]

    summary = summarise_foos(foos)

    assert summary.count == 2
```

Rules:

1. **Blank lines separate the three blocks.** Comments follow `python-style`.
2. **One Act per test.** If a test calls the subject twice, the first call is part of Arrange (setup) for an assertion about the second. When in doubt, split into two tests.
3. **One assertion subject per test.** Multiple `assert` statements that all check the same returned object are fine (`assert stored.name == "alpha"; assert stored.created_at >= ...`). Multiple assertions across different objects often means two tests in one.
4. **Arrange constructs valid state.** Don't write defensive `try/except` in Arrange — if the setup fails, the test fails, and that's the right outcome.

### Assert strength — pin the contract, not a coincidence

**Fixed natural keys are fine.** With per-test isolation — an empty database, a temporary directory of
its own — `identity="alpha"` needs no random suffix, and `assert len(rows) == 2` is correct; no
defensive `any(...)` filters, no `+1` for the test's own row.

**Pin the contract, not a coincidence.** Assert the returned state or observable effect that proves the behavior, including exact values and counts the contract guarantees. A successful call alone does not prove that the intended state was written. An assert is **strong** only if a plausibly-wrong body would fail it, so read each one against *would this fail on a plausibly-wrong implementation?* Six recipes keep it strong at authoring time, whatever the artifact under test:

1. **Assert a survivor, never an empty result.** A drop, skip or filter asserted on an empty result passes a body that drops everything, or empties for the wrong reason. Seed one item that must survive alongside the one that must go, and assert the survivor present and the other absent.
2. **Seed at least two rows wherever one cannot prove scoping or a join.** A tenant-scope, parent-link or join assertion made against a single seeded row passes a body that ignores the scope entirely. Seed a second row — another tenant, another parent — that must be excluded.
3. **For an echoed or derived field, pick an input a constant would not satisfy.** Asserting a returned role, a token subject or a copied identifier against a default or fixed-looking value passes a body that returns a constant. Choose a non-default input, so only the real wiring satisfies it.
4. **On a reject path, assert that no side effect occurred — not just the raised exception.** Over-quota, already-in-final-state, not-found and unauthorized must also assert that nothing was persisted, sent or recorded, or a body that raises *after* writing still passes.
5. **Exercise a non-boundary case, not only the boundary.** A test that pins only the `>=` edge, or only one tier of a graded rule, leaves the selection logic — is the right threshold even chosen? — unpinned. Add a case clearly inside the rule alongside the one on its edge.
6. **On a raise path, expect the narrowest class the contract raises**, never `Exception` or any ancestor of that class shared with unrelated failures, and assert the one attribute that distinguishes this failure from others of the same class — an error code, a key in the exception's context, the offending input — or, where the class carries none, the part of its message that does. A bare `Exception` passes a body that fails for any reason at all, a misspelled name included. Where the raised class translates another failure, assert that failure is its cause.

**Assert against literal expected values.** Never re-implement the rule under test to compute the
expected value — that hides the defect where both sides make the same mistake.

**Test what the author wrote, never what the data model already guarantees.** Field-by-field
equality, hashability and immutability come free with a frozen `@dataclass`, and a type the checker
already enforces needs no runtime test; asserting them is maintenance with no defect-detection value,
because no plausibly-wrong change could red them. What is not free is the constructor's invariants,
the computed properties and the methods — those are the whole coverage target.

**A boolean result is asserted with `is True` / `is False`**, never `==` — `==` may accidentally
compare `int(1)` to `True`, and a truthy-but-not-`True` return then passes.

**Pair every happy path with a rejection test.** Single-direction tests are incomplete: a rule pinned
only where it accepts passes a body that accepts everything.

**Never assert on what the subject logged.** A log line is a side effect of a successful run, not the
contract: a subject that logs the right event and writes nothing must red, and it passes every test
that watches the log instead of the result. Event names are also a stable operational contract that
dashboards key on (`python-logging`), so a test asserting on one couples the suite to the observability
surface and reddens on a rename that broke nothing. Assert the returned value and the persisted
state. Who logs an error, and what a line may carry → `python-logging`; which layer may log at all is
the architecture family's.

Artifact-specific coverage for domain behavior → `hex-test-domain`; repository contracts → `hex-test-repository-contract` or `flat-test-persistence`; request shape → *Intercepting HTTP* rule 5; error translation at a client boundary → `flat-test-service-client` or `hex-test-capability-adapter`. Pin the observable contract those tests own.

### No-mocks contract

| Tool | Forbidden? | Notes |
|------|-----------|-------|
| `unittest.mock.MagicMock` | yes | always |
| `unittest.mock.AsyncMock` | yes | always |
| `unittest.mock.patch` | yes | always |

`monkeypatch.setenv` is allowed inside settings-parsing tests, which exercise the environment-reading code
itself, and nowhere else. Every other substitution follows the ladder below.

The rationale: mocks describe *what was called*; a real dependency or a fake describes *what state
would result*. The state-based assertion catches whole classes of bug the call-based assertion can't.
Mocks also encode interface details that drift independently of the real signature — a refactor that
adds a parameter silently breaks no `MagicMock` test, where a hand-written fake or subclass fails the
type check.

### The substitution ladder

**The rungs are the rule; the libraries named in them are this binding's examples.** Each rung down
buys isolation and pays realism, so take the highest rung that can reach the case.

| Rung | What is substituted | When |
|------|---------------------|------|
| 1 | **Nothing — the real dependency**, started and disposed by the suite | The default. Any datastore, run or entrypoint test. Here: a container through testcontainers. |
| 2 | **The transport beneath the dependency**, leaving the dependency's own code running | Any client of a remote system. Only the socket is replaced, so request building, response parsing and error translation all still execute. Here: `httpx2.MockTransport`, handed to a real `httpx2` client as its transport. |
| 3 | **A hand-written fake of a port, where the architecture defines one** | A subject tested above the dependency — a collaborator unit. The fake satisfies the whole port and keeps state a test reads back. A project with no ports skips this rung; it is never a reason to create one. |
| 4 | **One method of the concrete class**, through a subclass overriding exactly the method that must fail | One-off failure injection, at test-module scope and underscore-prefixed: `class _RaiseQuxClient(QuxClient): ...` overriding one method to raise the catalogue exception. |
| 5 | **An attribute the caller builds internally**, patched for the test | Last, and only where the caller constructs its own dependency with no parameter to pass. Here: `monkeypatch.setattr`. A dependency that has a port never reaches this rung — its fake is always there. |
| — | **An interface extracted only so something becomes substitutable** | **Never.** A port exists because the architecture puts one there; one added for a test is an anticipatory abstraction. |

**The ladder is violated by skipping, not by using a low rung.** Rung 5 where the dependency is
already a constructor parameter, rung 4 where the failure can be produced through the transport stub,
rung 2 where the real datastore is already running for the rest of the file — each of those is a test
that bought isolation nobody needed and paid realism for it. The check is one question at the point
of substitution: *what stopped the rung above from reaching this case?* If the answer is "nothing, it
was quicker", climb back up. A test reaching for rung 5 is a hint that the caller wants a constructor
parameter.

### Intercepting HTTP

Rung 2 for any code that calls an HTTP service — a client class, a gateway adapter, a function
calling either:

1. **The stub covers every request the subject makes, from before the first one, so nothing leaves the process.** A request it misses goes to the real network, which fails opaquely or — worse — reaches the real upstream. A stub that is a client's transport covers that client only, so the subject is handed its client and the test builds it over the stub (`transport=httpx2.MockTransport(...)` here); a library that patches the HTTP client covers only from when it is entered, so it is active for the whole test and a fixture that itself issues requests requests it.
2. **The test of each call's happy path, and any test of a sequence — a retry, a refresh, a second endpoint — pins every request's exact method and URL, read from the stub's record.** A stub answers whatever arrives, so a test that never reads where its requests went passes without proving the call it was written for went where it should; where one stub serves several endpoints it either answers each by its method and path, or answers in the order the test queued and the test pins that order; never one answer for every request.
3. **Every happy-path test asserts the request it exercises actually reached the stub — on the stub's own record.** A stub answers whatever arrives and reports success by default, so a subject that never made the call — an un-awaited coroutine is the standing case — passes a test that only checks the return value — never by requiring every queued answer or stubbed route to be used, which pins how many requests the subject makes, so a skipped retry reddens a test about something else (a shared router's all-called check is off).
4. **Trigger a transport failure with a transport-level error, not a status code.** Only a raised connect or timeout error (an `httpx2.ConnectError` raised by the stub here) reaches the subject's transport-error arm; every status-code test lands on the response arm and leaves that branch unexercised.
5. **At least one test pins what the subject sent beyond its method and URL** — the query, the headers the upstream requires (its credential, where it takes one), the body — read back from the stub's record. Rule 2 already pins method and URL; a subject that parses a canned response correctly while sending the wrong query or body passes every response-shaped test. Where a call sends nothing beyond its method and URL, rules 2 and 3 are that pin.
6. **Where the subject parses a response body, a success response whose body it cannot parse is tested, and it fails as the catalogue exception** (`exception-catalog`) with the parse error as its cause — never a bare decode or key error escaping to the caller. Both halves of parsing are covered: a body that is not the declared format at all, and one that is but does not fit the declared shape.
7. **A stubbed body is copied from the upstream's documented or recorded response, never written from the subject's own model** — a stub shaped by the parser it feeds passes whatever the parser expects.

### Datastore contract

Rung 1 for any code that reads or writes a store — the datastore-contract layer of the pyramid. Which
of these binds follows the store's properties (`persistence`, *Which rules bind*):

1. **The store is real, and the assertion reads it back.** Nothing below the data-access code is
   substituted — a double answers none of the questions this layer exists for — and what the store
   holds after the act is read back — through a query of the test's own, or through the subject's own
   read where that read is under test too — never taken from the write's return value alone, which is
   what the statement said and so the thing under test.
2. **Where the translator branches on a constraint's name, the test pins that name, not just the
   exception class**, on the raised exception's identifying context (`persistence` rules 6 and 7). The
   name comes from the declared convention, and asserting it catches a migration that dropped or
   renamed the intended constraint.
3. **A unique constraint the translator branches on is tested on the plain write *and*, where the code
   has one, on the conflict-resolution or update path.** A partial or expression index can be honoured by an insert and
   silently not matched by a conflict clause, and a translator can handle the insert's violation and
   miss the update's; only exercising both paths separates those outcomes.
4. **A forced driver error asserts the catalogue exception and its identifying context, on each kind of
   call the code makes — a write and a read, each where it has one** — never the driver's own class, which is precisely what must
   never escape (`persistence` rule 4). A translation written only around the writes leaves every read
   leaking the driver's type, and no write test notices. The failure is forced through something the
   store itself refuses, or a store it cannot reach, never through a value that only happens to be
   rejected today.
5. **The subject's own rows are arranged through the subject**; where it has no write for them, through
   the layout the code itself declares, where it declares one, rather than a second hand-written copy of
   that layout in the test — and never from another test's leftovers, which isolation removes. A
   contract test that seeds behind its own subject proves nothing about the subject; a row
   the subject only references is not its own and is seeded directly.
6. **Where writes for one key can arrive out of order, a test writes the newer record and then the
   older, with stamps that differ, and asserts the newer's values remain** (`persistence` rule 16); a
   builder that fixes the stamp makes every write equally new and pins nothing.
7. **Where a write takes a batch, one call crosses a chunk edge and one carries two inputs sharing a
   key.** The first sets the chunk size deliberately small with an uneven last chunk — five rows in
   chunks of two cross two edges and end on a short chunk — and asserts every row landed, since an
   off-by-one in the slice shows only at an edge and production-sized input costs thousands of rows a
   run (`persistence` rule 21). The second asserts one record holding the input the collapse keeps (`persistence`
   rule 17); under an ordering guard the newer stamp goes first, so a collapse that keeps the last input
   fails.
8. **Where the program owns the schema, the suite establishes it by the project's own schema path** —
   its migrations, or the schema creation production runs — once per session, or per store where the
   store is created per test, never by tables the suite writes by hand, so a schema change that was
   never migrated reds here rather than in production. Where another project owns it, the suite creates
   only what the code reads, from the layout the code declares where it declares one (rule 5), and with
   the owner's column types either way (`persistence` rule 23). A store with no schema has nothing here.
9. **Each read the code has is tested on what it returns** — a read-only data-access class's as much as
   one that also writes: rows arranged by rule 5, the result compared whole with the declared values
   they map to, and a filtering read arranged as *Assert strength* recipes 1 and 2 state. A write test
   does not cover a read it happens to call: a read that ignores its filter or drops a field passes
   every test that looks only at the row just written.

### Reliability rules (local-vs-CI parity)

1. **The suite provisions the state it runs against, and no test depends on a machine-specific
   setup.** Dev and CI run the same way, so a green run on one machine predicts a green run on the
   next: every store the suite needs is started and thrown away by the suite itself — testcontainers
   in this binding. Pointing the suite at an **already-provisioned throwaway**
   datastore is the one sanctioned alternative, and it is guarded on both sides: opt in through a
   dedicated variable, never an ambient one, and refuse to run unless something explicitly declared
   the database disposable — an exact match against a declared throwaway name, or a marker set by
   whatever provisioned it — never inferring it from the host, the port or a pattern over the DSN;
   an exact match against a declared name is a declaration. `flat-test-integration-setup` carries the declared-name form and
   `hex-test-integration-setup` the provisioner's-marker form. An *unguarded* "developer's local database" mode is never offered: the suite wipes what it
   can see, and the variable that would divert it is exported by tools that know nothing
   about this suite.
2. **Every test starts from state it established itself, never from a predecessor's leftovers**, and
   the isolation that guarantees it is part of the suite rather than something a test remembers to do.
   Where the subject has a datastore that means an empty store at the start of every test — a store
   created per test where that is cheap (a file-backed or in-process one, in the test's temporary
   directory), otherwise the outer-transaction rollback, a whole-schema truncation, or a per-test
   namespace where the store has no transactions. Where the code fixes its namespace, the namespace a
   test owns is a whole store the suite started, emptied after each test, and a test asserts only
   inside it. The rollback covers only code handed the test's
   connection (`persistence` rule 1): an outer transaction can neither see nor roll back a connection it
   did not open, so code that opens its own takes the wipe. Where it has none, the same rule binds whatever
   state there is: a temporary directory created per test, a fresh in-process object rather than a
   module-level one, an environment the test sets and the fixture restores. So the suite's result does
   not depend on the order it was collected in: run it once in a randomized order and once in file
   order and get the same result — under this binding, `pytest-randomly` supplies the randomization and
   `-p no:randomly` the fixed order.
3. **A test never waits out real time.** A test that looks like it needs a wait needs the right
   `await` on the event it is actually waiting for; a test that needs the clock to move forward
   advances a clock the code under test accepts as a parameter rather than letting one pass. Sleeping
   makes the suite slower than the behaviour it pins and hides the race that will surface in CI, and
   patching a sleep so a loop exits is the same defect wearing a different hat. A runtime that
   exposes no clock control is a reason to pin the policy — the delays computed, the attempts made —
   rather than to sit through it.
4. **A timestamp the system assigns is asserted against a bound taken around the act, never by
   equality.** Read the clock before and after the act and assert the value falls between them
   (`>=`, `<=`). A store's clock is not the test's — Postgres `now()`, for one, returns the
   transaction's start time for every row written in it — so equality with a value the test computed
   passes or flakes by coincidence. Where the store stamps a modification instant with a clock fixed
   per transaction and the test runs inside one outer transaction, the arrange and the act share that
   instant; plant a value far in the past before the act and assert the act replaced it.
5. **A UUID a test asserts on is constructed inside that test**, never drawn from `uuid.uuid4()` at
   module scope and shared with its neighbours.
6. **No environment-dependent values.** Tests must not read `os.environ` or check `os.getenv("CI")` to alter behavior. The fixture that provisions the store handles the local/CI fork once, and it does so on a **dedicated opt-in variable**, never on an ambient one like `CI`. A test that needs a settings object constructs it with explicit values and passes it in; one that needs the store takes the suite's fixture and never builds a connection, client or pool of its own nor calls the program's own factory for one, which would sit outside the isolation and the session's teardown — the one exception is a client pointed at an address nothing listens on, built and disposed inside the test that forces a failed connection. A test never mutates or reassigns a factory's cached value. Only a test of the settings parsing itself lets it read an environment, one the test sets, and it disables the loader's file sources, since a dotenv or config path resolved against the working directory makes the test pass or fail by where the runner was started.
7. **Where a test sits is what decides which layer it belongs to — not a tag on it, and not a tag on
   its event loop.** A test under `unit/` is a unit test because of where it is, and where the suite
   has async tests, async-ness is declared once for the project rather than per function. Two tags can
   disagree with the tree; one tree cannot disagree with itself. Under this binding that means no
   `@pytest.mark.integration`, and where the suite has async tests no `@pytest.mark.asyncio`, with
   `pytest-asyncio` in auto mode declared once in `pyproject.toml`.
8. **A warning is a failure, not a line in the tail of the output.** `[tool.pytest.ini_options]` carries `filterwarnings` with `"error"` as its first entry, so a warning raised anywhere in the run turns the suite red. This is part of what "green" means: no extra command, no second run, nothing anyone has to remember to read.
   The price is that a deprecation from a library the project cannot fix reddens the suite too, so an exception is written as one narrow entry after `"error"` — `"ignore:<message>:<Category>:<module>"`, scoped as tightly as the warning allows — and it carries its reason beside it in a comment: whose warning it is, why the project cannot remove it at the source, and what will retire the entry. An exception without a reason is the rule switched off. A warning raised from the project's own `src/` never goes on that list; it gets fixed. Suppression conventions → `python-style`.

### A defect's test

**A fix to behaviour a test can observe starts with a test that fails on the code being fixed.** It
fails on the code before the fix, on the defect's own symptom — the wrong value, the error that escaped
— not on an import or a missing fixture, and the fix turns that same test green. A test never seen
failing proves nothing about the defect, and a defect fixed with no test is free to come back. Where no
test inside the suite can reach the defect — it shows only against a real external system, at
production volume, or in what no test asserts on, such as a log line — the fix's commit message says
so and names the check that would have caught it (`git-commit-message`, in the `pyhouse-git` plugin,
where installed) — never a comment in the code or a skipped test.

## Hard stops

- A producer skill says something this skill forbids → stop, the producer skill is wrong; fix it. This
  skill is the source of truth.
- Asked for a distribution's integration conftest, its containers or isolation fixtures, or the shared
  plugin module several members load → stop, use the family's integration-setup skill
  (`hex-test-integration-setup`, in `pyhouse-hex`, or `flat-test-integration-setup`, in `pyhouse-flat`),
  or the project's own layout where neither applies.
- Asked for a static "no X in Y" invariant → stop, use `test-architecture-rule`.
- Naming a builder, a fixture or a failure-injection subclass → stop, use `naming`.
