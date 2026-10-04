---
name: insolvia-testing
description: >-
  How Insolvia tests — which shape applies where, where a new test file goes,
  and the per-stack conventions that are easy to get subtly wrong. Use this
  BEFORE writing or changing any test in this repo: a pytest test under
  services/api or services/mailer, a Jest test in apps/insolvia_app, a Vitest
  test in packages/insolvia_api_client, or a
  Playwright spec under e2e/. Reach for it the moment a task says "add a test",
  "write tests for", "improve coverage", "this needs test coverage", or when you
  have just added an endpoint, a component, a route, or a config value and owe
  it a test. Also read it before proposing a coverage threshold, a new test
  runner, a mocking library, or an end-to-end test — this repo has decided
  against several of those and the reasons are not obvious. Consult it when a
  test is failing in a way that suggests it was testing the wrong thing.
---

# Testing in Insolvia

Four runners, six units, ~400 tests. **The shape differs by area on purpose** —
[ADR 0008](../../docs/adr/0008-testing-shape-follows-the-code-it-tests.md) owns
that decision and the reasoning. **Every test belongs to one of four tiers,
and the tier is a directory** —
[ADR 0021](../../docs/adr/0021-test-tiers-and-seed-fixtures.md) owns which tier
runs against which environment. This file owns *how* to write one.

| Tier | Where | Runner | Command | Runs against |
|---|---|---|---|---|
| **unit** | `services/*/tests/unit/`, `packages/insolvia_core/tests/unit/` | pytest | each unit's `scripts/dev-test.sh` (ruff → mypy → pytest, exactly as CI); a bare `pytest` is unit-only | nothing — memory adapters |
| **unit** | `apps/insolvia_app` (colocated) | Jest (`jest-expo`) | `npm test --workspace apps/insolvia_app` | nothing — mocks |
| **unit** | `packages/insolvia_api_client`, `apps/insolvia_admin` (colocated) | Vitest | `npm run test --workspace <pkg>` / `npm test` | nothing — stubbed `fetch` |
| **unit**, all of the above at once | — | `scripts/dev-test-unit.sh` | every suite, or the ones a set of files touches; what the **pre-push hook** runs. Python areas run CI's ruff lint + format check first (not mypy) | nothing |
| **integration** | `services/api/tests/integration/` | pytest, gated on `INSOLVIA_INTEGRATION=1` | `services/api/scripts/dev-test-integration.sh` (dev); `api-staging.yml` (staging) | the RUNNING API over HTTP, signed in by SRP as a seeded person |
| **e2e `flows`** | `e2e/tests/flows/` | Playwright | `e2e/scripts/dev-test.sh` (dev); `app-staging.yml` (staging) | a real browser, signed in |
| **e2e `smoke`** | `e2e/tests/smoke/` | Playwright | same wrappers; `app-prod.yml` (production) | HTTP + a browser, **no credentials** — the only thing that runs on prod |
| `tool/` | none — gated by `npm run tokens:check` | — | `npm run tokens:check` | — |

**Pick the tier by what the test needs to touch.** If it needs AWS, a running
server or a secret, it is not a unit test, whatever it asserts — and the unit
conftests give it nothing that reaches a network. If it needs to sign in, it is
integration (HTTP) or `flows` (browser). If it must run against production, it
is `smoke`, and it gets no credentials at all.

## Before you write it

1. **Push it down.** Verify the behaviour at the cheapest level that can
   observe it. A rule about *imports* belongs in `test_architecture.py`, not in
   a route test.
2. **Ask what would catch this in production.** If `tsc --strict`, `mypy
   --strict`, ESLint or ruff already makes the failure impossible, the test is
   noise. Static analysis is the base layer here, not a separate concern.
3. **Colocation is not uniform.** TypeScript tests sit **beside** the file they
   test (`heading.tsx` ↔ `heading.test.tsx`) — never a `__tests__/` directory.
   Python tests live in a **flat `tests/unit/`** directory, `test_<module>.py`,
   never beside the source; shared fixtures stay in `tests/conftest.py` (the
   parent — every tier inherits it) and `tests/paths.py` is the one place that
   counts its way to `src/`. `tests/__init__.py` is each unit's map.
4. **Name the behaviour, not the function.** `test_malformed_email_is_rejected`,
   not `test_parse`. The existing suites are consistent about this; match them.

## React Native (`apps/insolvia_app`) — Jest + RNTL v13

The app is **React Native**, not react-dom. Guidance written for
`@testing-library/react` mostly transfers, but the package is
`@testing-library/react-native` and it is **pinned to v13** — `userEvent`
semantics changed in v14, so check `package.json` before copying any snippet
found online.

- **Query priority, strictly:** `getByRole` → `getByLabelText` →
  `getByPlaceholderText` → `getByText` → `getByDisplayValue` → `getByTestId`.
  `getByTestId` is a **last resort** — it couples the test to something no user
  can perceive. The suite currently uses it once across 124 tests; keep it that
  way. Prefer `getByRole('button', { name: 'Sign out' })`, which asserts the
  accessible name and the role in one go.
- **`userEvent`, not `fireEvent`.** `userEvent.press()` emits the real
  `pressIn`/`press`/`pressOut` sequence; `fireEvent` fires one synthetic event
  and will pass on components a user could not actually operate. There are
  currently **zero** `fireEvent` calls in the repo — adding one needs a reason.
- **`queryBy*` is only ever for proving absence.** For anything present, `getBy*`
  and `findBy*` throw a useful error; `queryBy*` returns `null` and produces
  `expected null not to be null`, which tells you nothing.
- **`findBy*` for async — never `waitFor` + `getBy*`.** One assertion per
  `waitFor`, and never a side effect inside one.
- **Use `screen`**, don't destructure `render()`'s result.
- **Never call `cleanup()`** and **never wrap `render`/`userEvent`/`fireEvent`
  in `act()`** — RNTL already does. The legitimate exception is calling a hook's
  returned function imperatively (see `session-provider.test.tsx`), and even then
  `act` is imported from `@testing-library/react-native`, never from `react`.
- **Route-level tests use `renderRouter('src/app', { initialUrl: … })`** from
  `expo-router/testing-library`, which mounts the real route tree.
- **Never override `transformIgnorePatterns`.** A hand-copied list silently drops
  `standard-navigation` (pulled in by expo-router) and breaks every route test.

## Python (`services/api`, `services/mailer`) — pytest

- **Arrange–Act–Assert, one act per test.** The
  arrange–assert–act–assert–act pattern makes a failure ambiguous about which
  step broke.
- **`@pytest.mark.parametrize` over copy-paste.** It is the biggest
  coverage-per-line lever available and the suites already use it ~20 times.
  Table-drive the cases; do not write five near-identical functions.
- **Shared fixtures go in `tests/conftest.py`; per-test config does not.** When a
  test needs different config, build the app inline with a local helper — see
  `test_unsubscribe.py` and `test_health.py`. Do not add parameters to the
  shared `client` fixture to serve one caller.
- **`load_config({...})` is the config seam.** Pass an explicit mapping. Do not
  reach for `monkeypatch.setenv` — nothing in the package reads `os.environ`
  outside `load_config`, and keeping it that way is what makes config testable.
- **Monkeypatch the transport, not the logic.** `test_mailer_client.py` patches
  `urlopen`; `test_jwks_provider.py` patches the fetch. There is deliberately
  **no `moto`, no `responses`, no `httpretty`** — do not add one.
- **Fake at the port.** `core/ports.py` defines Protocols; `adapters/memory/`
  implements them. A new external dependency gets a Protocol and a memory
  adapter, not an inline `Mock()`.
- **`tests/` is not type-checked.** `mypy --strict` is scoped to `src` on
  purpose — fakes and monkeypatching are where strictness is noise.
- **`test_architecture.py` is not editable to make your change pass.** If it
  fails, your layering is wrong. Fix the layering.

## The api-client contract pin

`packages/insolvia_api_client/src/index.test.ts` **is** the contract with
`services/api`. There is no OpenAPI codegen, by decision.

- **Every endpoint added to the API gets a hand-written method here *and* a
  contract test**, in the same PR.
- **Assert the exact request and the exact response mapping** — method, URL,
  headers, body — against a stubbed `fetch`. Copy the literal JSON the server
  actually returns; read the route handler to get it, don't infer it.
- **Import by package name**, not relative path, so the test exercises the real
  export map.
- A server field rename is *supposed* to break these tests. That is the feature.

## The integration tier (`services/api/tests/integration/`)

- **It drives the API over HTTP and nothing in-process.** The `Api` helper in
  its conftest is the whole client; `as_user("paralegal")` is a real token from
  the real pool. Do not import the Flask app or a memory adapter here — that is
  a unit test wearing the wrong directory.
- **Who exists comes from `seeds/<target>.json`, by handle.** A spec that needs
  a person the fixture lacks adds them to the fixture (and the next seed
  creates them); it never invents an address or a subject.
- **Scratch discipline.** Cases are only soft-deleted through the API (the
  rows stay), so work
  inside the one scratch case the conftest finds-or-opens; delete every
  document you create in teardown; leave a debtor as you found it. A spec that
  opens a case per run fills a table nobody prunes.
- **A test that passes only on one target is a bug in the test.** Both `dev`
  and `staging` run the same files; branch on the fixture's contents (a
  one-firm fixture cannot express cross-tenant isolation — return early and
  say so), never on the target name.
- **Never a required PR check, never a unit-tier dependency.** It runs after
  the staging alias shift and on a developer's dev stack, and its failure
  fails the staging stage.

## End-to-end (`e2e/`)

- **Two projects, by what they may hold.** `flows` signs in and is offered
  against dev and staging; `smoke` holds no credentials and is the only thing
  that runs against production. A smoke spec that needs a token is a `flows`
  spec; a `flows` spec that needs nothing signed-in is a `smoke` spec.
- **Adding a `flows` test needs a reason the other layers cannot satisfy.**
  Slow, environment-dependent, and a flake blocks production promotion through
  `verified-commit`. A `smoke` test needs a reason a `curl` cannot satisfy.
- **Never make either a required PR check** — that puts staging's availability
  on every PR's critical path. Post-deploy only.
- **Write only to the scratch case** (`support/scratch-case.ts`), never to a
  seeded fixture case — the loader will not repair it and the next integration
  run cannot find it. Reading a fixture case is fine.
- **Role-based selectors only**, matching the app's accessibility contract.
- **Never let a credential reach a file, a default, a log line, or an uploaded
  artifact.** Traces record typed values verbatim and the repo is public.
- If a spec starts passing only on retry, **quarantine it** — do not raise the
  retry count.

## Seed data

- **`seeds/<env>.json` says who exists and which fixture cases they hold;
  `seeds/fixtures/<version>/` says what a case contains**, in the API's own
  body shapes. The loader parses both with the route's own parsers, so a
  malformed row fails with the API's field errors — write a fixture the way
  you would write a request.
- **A loaded fixture is never edited; a changed fixture is a new version.**
  Rows that exist are left alone on every load, so editing `v1` after it has
  loaded changes nothing anywhere. `scripts/dev-fixture.sh capture v2 …`
  writes a new version out of your dev stack.
- **Nothing real, ever.** Every value describes nobody; every address ends in
  `.test`; capture refuses any source that is not a dev stack.

## Things this repo has decided against

Each of these looks like an improvement and is not. Do not add one without an
ADR:

- **A coverage threshold as a merge gate.** It rewards exactly the tests
  ADR 0008 says not to write. Measuring coverage for information is fine.
- **`moto` / `responses` / a network-mocking library.** Monkeypatched transports
  plus memory adapters already cover this, with no version coupling to AWS.
- **A second test runner in an existing unit**, or migrating one to another.
- **Snapshot tests.** Nothing in the repo uses them; they pin rendered output
  rather than behaviour, and they get regenerated rather than read.
- **Testing an area's private helpers directly.** Test the exported surface.

## Where a new test file goes

| You changed | Test goes |
|---|---|
| a `core/` function | `services/<svc>/tests/test_<module>.py`, pure, parametrised |
| a Flask route | same file as its module's tests, through `app.test_client()` |
| a new AWS-touching adapter | a Protocol in `core/ports.py`, a fake in `adapters/memory/`, transport monkeypatched |
| an app component | beside it, `<name>.test.tsx`, rendered, queried by role |
| an app route | beside the screen, via `renderRouter` |
| an API endpoint | `services/api` tests **and** the api-client contract pin |
| a design-system component | beside it — and remember the `.web`/`.native` leaves are separate files with separate tests |
| an infra invariant | prefer an executable check (`test_architecture.py`, a workflow guard) over prose |
| something only a real table, bucket, pool or the deployed role can answer | `services/api/tests/integration/test_<subject>.py`, through the `Api` helper, inside the scratch case |
| something only a real browser and a real sign-in can answer | `e2e/tests/flows/<subject>.spec.ts` |
| something a production deploy must announce when broken | `e2e/tests/smoke/<subject>.spec.ts` — no credentials, and it runs on staging first |
| a person or a case a suite needs to exist | `seeds/<env>.json` (who) and `seeds/fixtures/<version>/` (what) — never a script, never a secret |
