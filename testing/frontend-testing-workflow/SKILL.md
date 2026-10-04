---
name: frontend-testing-workflow
description: Author and maintain frontend tests — Jest unit suites (jsdom client + node server), Testing Library semantic queries, Playwright E2E and visual regression, seeded Faker builders, and mutation-killing assertions. Use when writing, structuring, or fixing Jest, Testing Library, Playwright, or visual tests, or strengthening tests to kill escaped mutants.
---

# Frontend Testing Workflow Skill

## Profile keys consumed

- `make.test_unit_client`
- `make.test_unit_server`
- `make.test_integration`
- `make.test_e2e`
- `make.test_visual`
- `make.test_mutation`
- `make.merge_mutation_reports`
- `make.start`
- `make.start_prod`
- `quality.coverage_statements`
- `quality.coverage_branches`
- `quality.coverage_functions`
- `quality.coverage_lines`
- `quality.mutation_msi`
- `quality.visual_diffs`
- `capabilities.visual_testing`
- `capabilities.mutation_testing`
- `architecture.source_root`
- `architecture.modules`
- `architecture.component_prefix`
- `architecture.path_aliases`
- `framework.bundler`
- `framework.package_manager`
- `framework.graphql_mock`

All test invocations go through the profile's `make` target map. A `null`
value for a `make.*` key means the capability is absent: skip that suite
with an explicit capability-absent note instead of failing or improvising
a raw command. Generic tooling (`gh`, the project package manager
`framework.package_manager`, `git`) may be invoked directly when needed,
but every suite runs through its mapped target.

## Context (Input)

- A component, hook, store, repository, or feature flow needs new or
  updated tests.
- A failing suite needs debugging, or coverage / mutation gaps need
  closing.
- This skill governs **how tests are authored** (environments, selectors,
  builders, assertions). For the run-and-fix loop and the gate thresholds
  themselves, pair it with the
  [testing-workflow skill](../testing-workflow/SKILL.md).

## Task (Function)

Write tests that exercise behavior through the public UI or exported API,
locate elements by user-facing semantics, use deterministic generated data,
and assert specifically enough to kill mutants — so the suite passes with
full coverage and a clean mutation score through the profile's `make`
targets.

## Test Tiers & Where Tests Live

| Tier             | Invocation                               | Environment            | Typical location          |
| ---------------- | ---------------------------------------- | ---------------------- | ------------------------- |
| Unit (client)    | target mapped by `make.test_unit_client` | Jest **jsdom** + RTL   | `tests/unit/`             |
| Unit (server)    | target mapped by `make.test_unit_server` | Jest **node**          | `tests/apollo-server/`    |
| Integration      | target mapped by `make.test_integration` | Jest jsdom, global 100%| `tests/integration/`      |
| E2E              | target mapped by `make.test_e2e`         | Playwright             | `tests/e2e/`              |
| Visual           | target mapped by `make.test_visual`      | Playwright snapshots   | `tests/visual/`           |
| Mutation         | target mapped by `make.test_mutation`    | Stryker (driven by RTL)| component layer under root|

Mirror source ownership: a test's directory tracks the source area it
covers under `architecture.source_root` — typically one of the feature
modules declared in `architecture.modules`, or a shared layer. Reference
values from the canonical upstream profile:

```bash # profile-example
make test-unit-client    # make.test_unit_client → jsdom + Testing Library
make test-unit-server    # make.test_unit_server → Apollo mock (node env)
make test-integration    # make.test_integration → integration suite (global 100%)
make test-e2e            # make.test_e2e         → Playwright user flows
make test-visual         # make.test_visual      → visual regression
make test-mutation       # make.test_mutation    → Stryker mutation testing
```

**Multi-repo note**: a component library may collapse the client/server
split into a single unit target (`make.test_unit_client` /
`make.test_unit_server` map to the same target or one is `null`). Run the
non-`null` target and note the absent lane — never invent a host command.

## Jest Environments

Two environments back the unit/integration tiers, selected by the runner's
`TEST_ENV`:

- **Client (jsdom)** — React component, hook, store, mapper, and utility
  tests. Render with Testing Library; assert on the rendered output and
  accessible tree, not on internal state.
- **Server (node)** — the local GraphQL mock (`framework.graphql_mock`,
  e.g. an Apollo server) behaves correctly in a node environment. Test the
  resolver/handler contract, not the framework internals.
- **Integration (jsdom)** — wires real collaborators together and enforces
  a **global 100%** coverage floor over `architecture.source_root`
  (`quality.coverage_statements` / `quality.coverage_branches` /
  `quality.coverage_functions` / `quality.coverage_lines`). A line left
  uncovered anywhere under the source root fails this tier.

Test behavior through the public UI or the exported API. Mock network and
service boundaries intentionally; **do not test the mock's internals**.
Keep setup state explicit so a reader can see what the component received.

## Testing Library — Semantic Queries

Locate elements the way a user (or assistive technology) perceives them.
Source ships **no `data-testid`**; query priority is:

1. `getByRole` (with `name`) — buttons, links, headings, form controls.
2. `getByLabelText` — inputs tied to a visible or `aria` label.
3. `getByText` / `getByPlaceholderText` — visible copy.
4. A stable `id` **only** when no semantic query fits.

```typescript
// Good — user-facing semantics, generated data bound once
const user = buildUser();
render(<ProfileCard email={user.email} />);
expect(screen.getByRole('heading', { name: user.fullName })).toBeVisible();
expect(screen.getByText(user.email)).toBeInTheDocument();

// Bad — test-only hook the source does not ship
screen.getByTestId('profile-card');
```

This is enforced: ESLint flags `data-testid` as an **error** under the
source root and warns on `*ByTestId` queries in tests (mock-stub queries
stay valid). Satisfy the gate by refactoring to a semantic query or adding
a real accessible name — never with a suppression directive or a test-only
attribute. When a component cannot be queried semantically, fix the
component's accessibility, then the test follows. See the
[accessibility-audit skill](../accessibility-audit/SKILL.md) and
[frontend-component-development skill](../frontend-component-development/SKILL.md).

## Playwright — E2E & Visual Authoring

E2E specs drive real user flows in a browser; visual specs assert pixel
stability. Both use accessible Playwright locators first
(`getByRole` / `getByLabel` / `getByText`), falling back to a stable `id`
only when no semantic locator fits — the same priority as the unit tier.

```typescript
// Accessible locator, explicit state, no test-id
await page.goto('/');
await page.getByRole('button', { name: submitLabel }).click();
await expect(page.getByRole('status')).toHaveText(submittingLabel);
```

Authoring rules:

- Keep setup state explicit; do not rely on prior-spec side effects.
- Use the project's mocked API responses (e.g. Mockoon-backed, available
  per the project's test stack) so flows are deterministic and offline.
- Add a page helper only when it removes **real** duplication, not
  speculatively.
- The default E2E/visual path builds production parity (target mapped by
  `make.start_prod`); a dev-container fast path against the running dev
  server (target mapped by `make.start`) exists for a single-spec inner
  loop — scope it to one spec while iterating.

**Visual regression** is capability-gated:

- `SKIPPED: make.test_visual` when `capabilities.visual_testing` is `false`
  or `make.test_visual` is `null` — record a capability-absent note and
  skip; do not author visual specs for a repo without the capability.
- The bar is `quality.visual_diffs` (ceiling `0`): zero unintended pixel
  diffs. On a diff, open the diff image and decide whether the change is
  **intended** before doing anything else.
  - Unintended → it is a regression: fix the component or style.
  - Intended → regenerate the baseline with the snapshot-update variant
    next to the `make.test_visual` target (find it in the repository
    Makefile), but **only after** inspecting the diff. Never update
    snapshots blind to silence a failing run.
- Keep test data deterministic (seeded Faker, below) so baselines stay
  stable across runs and workers.

## Faker Builders

Tests generate arbitrary user/domain data (emails, names, passwords, ids,
tokens) with `@faker-js/faker` via shared builders under `tests/builders/`,
imported through a builders path alias (one of `architecture.path_aliases`,
e.g. `@tests/builders`, resolving in both the Jest and Playwright
runners). Each builder returns **domain-valid data by construction** and
accepts an `overrides` object:

```typescript
import { buildUser, buildCredentials, buildEmail } from '@tests/builders';

const user = buildUser();              // all fields generated and valid
const creds = buildCredentials({       // override only what the test pins
  email: buildEmail(),
});
```

- **Seeded determinism**: Faker is seeded via `seedFaker()` in each
  runner's setup (default `DEFAULT_FAKER_SEED`, override with
  `FAKER_SEED=<integer>`; the seed is reported once per worker), so the
  suite is reproducible and visual snapshots stay stable.
- **Bind once, reuse**: assign a generated value to a `const` and reuse it
  across the input and the assertion — never call a generator twice and
  compare its two results.
- **Keep literals only when the value IS the case**: invalid/edge-case
  inputs, golden text, config, URLs, error codes/messages, i18n strings,
  and mock sentinels stay hardcoded because the literal is the contract.

```bash # profile-example
FAKER_SEED=12345 make test-unit-client   # reproduce a seed-specific failure
```

## Writing Tests That Kill Mutants

Mutation coverage proves assertions are **specific**, not just present.
This tier is capability-gated:

- `SKIPPED: make.test_mutation` (and `make.merge_mutation_reports`) when
  `capabilities.mutation_testing` is `false` or `make.test_mutation` is
  `null` — record a capability-absent note and skip.
- The mutated scope is the component layer
  (`<source_root>/components/**/*.tsx`, where reusable components carry the
  `architecture.component_prefix` such as `UIButton`), driven by the
  client unit suite. The bar is MSI ≥ `quality.mutation_msi` (default read
  from the project's Stryker `break`), **raise-only** — never lower the
  configured `break` to make a run pass.

When a mutant escapes, the assertion was too loose. Strengthen it:

1. Read the mutation diff: what change went undetected?
2. Add the boundary or branch case the diff exposes — e.g. a mutant
   flipping `>` to `>=` needs an exact-boundary test; a removed prop needs
   an assertion that the prop's effect is rendered.
3. Assert on the **observable result** (rendered text, role, attribute,
   callback argument), not on the fact that a function ran.
4. If a component resists testing, refactor it for testability — see the
   [frontend-component-development skill](../frontend-component-development/SKILL.md).

Never silence a mutant with a suppression annotation. The run-and-merge
gate (CI shards `make.test_mutation` and re-enforces `break` via
`make.merge_mutation_reports`) lives in the
[testing-workflow skill](../testing-workflow/SKILL.md).

## Constraints (Parameters)

**NEVER**:

- Cancel long-running tests mid-execution or commit with failing tests.
- Accept coverage below the enforced floors (`quality.coverage_statements`,
  `quality.coverage_branches`, `quality.coverage_functions`,
  `quality.coverage_lines` — all `100`).
- Allow escaped mutants or lower `quality.mutation_msi` / the Stryker
  `break`.
- Accept an unintended visual diff or update snapshots without inspecting
  them (`quality.visual_diffs` ceiling `0`).
- Add a `data-testid` so a test can find an element — refactor to a
  semantic query.
- Add `eslint-disable` / `@ts-ignore` / suppression annotations to dodge a
  check — fix the root cause.
- Run tests outside the profile's `make` target map (no bare `jest` /
  `playwright` / `stryker` on the host; the targets wrap the containerized
  toolchain and the package-manager-managed dependencies).

**ALWAYS**:

- Use seeded Faker builders for dynamic test data; bind a generated value
  to a `const` once and reuse it.
- Test behavior through the public UI or exported API; mock network and
  service boundaries, and do not test mock internals.
- Locate elements by accessible role/label/text (Testing Library and
  Playwright) before any `id` fallback.
- Keep the mocked API behavior explicit in test setup.
- Add regression coverage for a bug fix before changing behavior.
- Keep results deterministic across runs and workers.

## Format (Output)

**Functional tests success**:

```text
PASS  tests (X suites, Y tests)
Coverage: 100% statements / branches / functions / lines (over source root)
Visual: 0 unintended diffs
```

**Mutation testing success**:

```text
MSI >= quality.mutation_msi (default = Stryker `break`)
0 escaped mutants on the mutated component scope
```

After authoring, format then lint through the
[frontend-quality-workflow skill](../frontend-quality-workflow/SKILL.md)
(targets mapped by `make.format` then `make.lint`). Fixes surfaced during
review or QA route back to the `react-implementer` agent.

## Verification Checklist

- [ ] Tests exercise behavior through the public UI / exported API, not
      internals
- [ ] Elements located by accessible queries; no `data-testid` added
- [ ] Dynamic data comes from seeded Faker builders, bound once and reused
- [ ] Correct Jest environment chosen (client jsdom / server node /
      integration), suites mirror source ownership
- [ ] Coverage at the enforced floors over `architecture.source_root`
- [ ] Visual diffs inspected before any snapshot update
      (`SKIPPED` noted when `capabilities.visual_testing` is false)
- [ ] Mutants killed by specific assertions; MSI ≥ `quality.mutation_msi`
      (`SKIPPED` noted when `capabilities.mutation_testing` is false)
- [ ] Ran through the profile's `make` target map (containerized); no
      suppression added

## Related Skills

- [testing-workflow](../testing-workflow/SKILL.md) - Run-and-fix loop, gate
  enforcement, and the sharded mutation merge gate
- [frontend-quality-workflow](../frontend-quality-workflow/SKILL.md) -
  Format + lint after authoring tests
- [accessibility-audit](../accessibility-audit/SKILL.md) - Fix the
  accessibility that makes a semantic query possible
- [frontend-component-development](../frontend-component-development/SKILL.md) -
  Refactor a component for testability when a mutant resists
- [code-organization](../code-organization/SKILL.md) - Place and name test
  files to mirror source ownership
