---
name: e2e-automation-project
category: testing
description: Maintain a dedicated automation test project per repository - separate from the product's unit tests - with API, worker, and UI suites written scenario-first
enabled: false
---
# E2E Automation Project

## Overview

Every repository worth testing gets a **dedicated automation test project**: a separate project that exercises the real product through its public surface and can be re-run on every change. It is not the product's unit-test folder and never mixes into it — it has its own dependencies, its own entrypoint, and runs in the repository's own pipeline (automation-pipeline-integration).

**Core principle:** scenarios before code (scenario-plan-first). A suite written without a scenario list tests whatever was easy, not what matters. And automation follows the manual pass: you automate the scenarios you have already executed and understood by hand.

## Structure

One automation project per repository, following the project's convention — default `qa-automation/` at the repo root (a sibling repo also works):

```
qa-automation/
  scenarios/        # the human-readable scenario lists, one file per feature
  api/              # backend API suite: HTTP client + assertions
  worker/           # async job suite: trigger → poll → assert side effects
  ui/               # frontend suite: Playwright against the built app
  fixtures/         # seed data
  support/          # helpers, page objects, request builders, stub mappings
  scripts/e2e.sh    # single entrypoint: provision, run all suites, teardown
```

| Surface | Tool (follow the project's existing choice) |
|---------|---------------------------------------------|
| REST API | the language's HTTP test client + assertions (Playwright APIRequest, RestAssured, supertest, Go net/http + testify) |
| Worker / async jobs | same test runner; triggers through the product path, polls for side effects (worker-job-testing) |
| Web UI | Playwright (preferred) / Cypress — headless Chromium via `executablePath: process.env.CHROME_BIN`, no browser download |

Mobile automation is out of scope for now — do not scaffold a mobile suite.

## Determinism

- The app under test boots from the current branch build; the suite never targets stage, prod, or any shared environment.
- Database and infra are disposable containers seeded per run (test-database-seeding, Testcontainers or the project's equivalent).
- External services are stubbed and asserted on (test-doubles-wiremock).
- Each test seeds and cleans its own data; no ordering dependencies; re-running gives the same result.

## The Workflow

1. **Author scenarios first** for the feature: happy path, boundary, negative, auth/permission, key regressions — committed under `scenarios/` and posted on the task.
2. **Stand up the environment** through the entrypoint script, never by hand-managed local state.
3. **Implement one test per scenario**, named for the behavior (`export_forbidden_for_other_tenant`), reading like the scenario via page objects / request helpers.
4. **Run the whole suite**, read the output, capture failure artifacts (screenshots, traces, logs) as evidence.
5. **Wire it into the pipeline** if not already (automation-pipeline-integration) — a suite outside the pipeline enforces nothing.

## Worked Example

Feature: task export to CSV.

- Scenarios: (1) export returns the project's tasks; (2) empty project → header-only CSV; (3) other tenant → 403; (4) export completion event is produced by the worker.
- Environment: app against a Testcontainers Postgres seeded with a known project; auth provider stubbed with WireMock.
- Tests: `api/export_returns_all_tasks`, `api/export_empty_project_header_only`, `api/export_forbidden_for_other_tenant`, `worker/export_event_emitted`. Each seeds its own rows, asserts, cleans up.
- `scripts/e2e.sh` → all green; pipeline runs the same script on the next task.

## Common Mistakes

- Mixing automation into the product's unit-test folders — separate project, separate dependencies.
- A second automation project forked for the same product — extend the existing one.
- Suites that hit staging/shared data → flaky, order-dependent, forbidden.
- A scenario in the plan with no implementing test, or tests with no scenario.

## Red Flags

- The suite passes locally but fails in a clean environment → hidden shared state.
- Re-running gives different results → nondeterminism to fix before anything else.
- UI tests download a browser at run time → use the system Chromium via `CHROME_BIN`.
