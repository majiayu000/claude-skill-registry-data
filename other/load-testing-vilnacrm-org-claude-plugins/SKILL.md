---
name: load-testing
description: Create and manage K6 load tests for the key user journeys of a React frontend SPA. Use when creating load tests, writing K6 scripts, testing page-load and sign-up flow performance, debugging load-test failures, or setting up performance-under-load monitoring. Covers journey scripts, deterministic VU patterns, test-data isolation, result artifacts, configuration, and load troubleshooting. Skip with a note when capabilities.load_testing is false.
---

# Load Testing Skill

## Profile keys consumed

- `capabilities.load_testing`
- `make.test_load`
- `make.start_prod`
- `framework.ui`
- `architecture.modules`

## Gating

This skill is gated by `capabilities.load_testing`. When `capabilities.load_testing`
is `false`, or when `make.test_load` is `null`, record a capability-absent note
(NFR-4) and skip — never improvise raw `k6 run` invocations against a repository
that does not declare the capability:

```text
SKIPPED: load testing not configured for this project (capabilities.load_testing=false)
```

The dependent lane simply does not run; no quality threshold is weakened by the skip.

## Overview

This skill provides guidance for creating and managing K6 load tests for the
real user journeys a React SPA serves — page loads, route navigations, and
multi-step flows such as sign-up. Load testing measures the **production build**
under concurrent virtual users (VUs); it is distinct from lab performance
budgets (Lighthouse / web-vitals), which live in the
[frontend-performance-accessibility skill](../frontend-performance-accessibility/SKILL.md).
Journeys exercise the built UI (`framework.ui`, e.g. Material UI v7 + Emotion),
so a page-load scenario reflects the production bundle the user actually receives.

## Core Principles

### 1. Individual Journey Testing

- Create one K6 script per user journey, not composite/random scripts
- Follow the harness convention: `homepage.js`, `signup.js`, one file per flow
- Target journeys that exercise a real feature module (`architecture.modules`)
  end to end — e.g. the authentication module's sign-up flow — not isolated
  component renders
- Avoid mixed "do a random thing" scripts: one journey per file keeps failures
  attributable and summaries readable

### 2. Deterministic Testing

- **NEVER use random operations** in load tests
- Use predictable, iteration-based patterns (`__ITER % N`) so runs are comparable
- Reproducible results are what make a regression in p95 latency meaningful
- Keep scripts deterministic enough to diff one run against the next

### 3. Proper Resource Management

- Implement `setup()` to create any dependencies the journey needs
- Implement `teardown()` to clean up data the journey created
- A flow that registers accounts MUST isolate or remove them, or repeated runs
  collide on unique constraints (duplicate email) and skew the failure rate
- Navigate by the real route paths the router serves (e.g. `/sign-up`), not by
  guessed URLs

### 4. Run Through the Profile's make Target

- The full suite runs through the target mapped by `make.test_load`
- Result artifacts are written under `tests/load/results/` on the host
- No bespoke commands: invoke load tests only through the profile's `make` map;
  a `null` mapping means the capability is absent (see **Gating**)

## Available Commands

The suite runs through the target mapped by `make.test_load`. Repositories that
adopt the canonical K6 harness also expose a flow-specific runner (sign-up) and
level variants (smoke/average/stress/spike) as **Makefile siblings next to the
`make.test_load` target** — find them in the repository Makefile. Canonical
upstream layout:

```bash # profile-example
make test-load             # make.test_load → homepage page-load journey
make test-load-signup      # comprehensive sign-up journey (positive, negative, rate-limit)
K6_TEST_SCRIPT=/loadTests/homepage.js make test-load       # override the script
K6_RESULTS_FILE=/loadTests/results/homepage.html make test-load
K6_SIGNUP_SCRIPT=/loadTests/signup.js make test-load-signup
```

**Prerequisites**: the production build is running and healthy (target mapped by
`make.start_prod`, plus the repo's prod health-wait target); the harness points
`BASE_URL` at that running build (default `http://localhost:3001`). The
`make.test_load` recipe starts the prod build, waits for health, prepares the
results directory, and runs K6 through Docker Compose.

## Quick Start Guide

### 1. Choose the Journey

- **Page-load journey**: a single navigation (GET a route, assert it renders)
- **Multi-step flow**: a sequence such as sign-up (load form → submit → assert),
  exercising a feature module the story names (`architecture.modules`)

### 2. Create the Script

```bash
# Create in the harness scripts directory (host path)
touch tests/load/homepage.js   # page-load journey
touch tests/load/signup.js     # multi-step flow
```

### 3. Follow the Script Structure

Use the journey templates in the **Quick Reference** below. Every script:

- imports `http`/`check`/`sleep` from `k6`
- reads `BASE_URL` from `__ENV` with a sane default
- exports `options` with VUs, duration, and `thresholds`
  (`http_req_failed: ['rate<0.05']`, `http_req_duration: ['p(95)<1500']`)
- asserts the response status with `check(...)`
- implements `setup()` / `teardown()` when the flow creates data

### 4. Add Configuration

K6 runs inside a Docker container where the host directory `tests/load/` is
mounted as `/loadTests/`. Makefile variables expect the **container** path; HTML
output written to `/loadTests/results/` lands on the host at `tests/load/results/`:

| Where you set it  | Path form      | Example                            |
| ----------------- | -------------- | ---------------------------------- |
| Makefile / env    | container path | `/loadTests/homepage.js`           |
| Reading results   | host path      | `tests/load/results/homepage.html` |

Override scenario VUs/duration through the K6 env vars
(`K6_TEST_SCRIPT`, `K6_RESULTS_FILE`, `K6_SIGNUP_SCRIPT`,
`K6_SIGNUP_RESULTS_FILE`) and the script's own `VUS` / `DURATION` `__ENV` reads.

### 5. Test and Verify

- Run the smoke level first (lowest VUs/duration)
- Inspect the K6 summary and the generated HTML result
- Verify cleanup: a flow that created accounts leaves none behind

## Load Test Levels

| Level       | VUs     | Duration     | Success Rate | Purpose                           |
| ----------- | ------- | ------------ | ------------ | --------------------------------- |
| **Smoke**   | 2-5     | 10 seconds   | 100%         | Basic functionality verification  |
| **Average** | 10-20   | 2-3 minutes  | >99%         | Normal traffic simulation         |
| **Stress**  | 30-80   | 5-15 minutes | >95%         | Find breaking points              |
| **Spike**   | 100-200 | 1-3 minutes  | >90%         | Test resilience under sudden load |

## Common Pitfalls

### Don't Do This

```javascript
// Random operations - unpredictable results
const operation = Math.random();

// Hardcoded test data - duplicate accounts collide across runs
const email = 'test@example.com';

// Missing cleanup in teardown()
```

### Do This Instead

```javascript
// Deterministic operations
const operationIndex = __ITER % 3;

// Deterministic, isolated test data - unique per VU and iteration
const email = `test_vu${__VU}_iter${__ITER}@example.com`;

// Proper cleanup
export function teardown(data) {
  // Remove any accounts/resources the journey created
}
```

## Checklist for New Load Tests

### Before Creating

- [ ] Identify the specific journey to test (page load vs multi-step flow)
- [ ] Identify the feature module it exercises (`architecture.modules`)
- [ ] Identify required dependencies (data the flow needs to exist first)
- [ ] Plan realistic, isolated test-data generation
- [ ] Choose appropriate VU/duration parameters

### During Creation

- [ ] Follow the appropriate journey template (see **Quick Reference**)
- [ ] Implement `setup()` / `teardown()` when the flow creates data
- [ ] Use deterministic operations (no random)
- [ ] Navigate by real route paths the router serves
- [ ] Set `thresholds` for `http_req_failed` and `http_req_duration`
- [ ] Use clear naming: one file per journey

### After Creation

- [ ] Confirm the script is picked up by the `make.test_load` runner
- [ ] Test with smoke load first
- [ ] Verify a 100% success rate in a controlled environment
- [ ] Check that cleanup works (no leftover accounts/data)
- [ ] Document any special prerequisites

## Performance Monitoring

### Success Criteria

- **Smoke Tests**: 100% success rate
- **Average Tests**: >99% success rate
- **Stress Tests**: >95% success rate
- **Response Times**: under the `http_req_duration` threshold configured per journey

### Key Metrics

- HTTP status codes (200 for a rendered route; the API's success codes for flows)
- Response times (avg, p95, p99 — match the `--summary-trend-stats` the harness reports)
- Error rate (`http_req_failed`) and error types
- Throughput (requests per second)

Load results are an input to the QA verdict gathered by the `qa-visual-tester`
agent; when a journey regresses under load, remediation routes to the
`react-implementer` agent — never lower a threshold to make a run pass.

## Supporting Files

For functional and lab-performance concerns that sit next to load testing:

- **[testing-workflow skill](../testing-workflow/SKILL.md)** — Jest, Testing Library,
  Playwright E2E/visual, and Stryker mutation testing (the functional gates)
- **[frontend-performance-accessibility skill](../frontend-performance-accessibility/SKILL.md)** —
  Lighthouse budgets, web-vitals, and accessibility (lab performance, not load)
- **[ci-workflow skill](../ci-workflow/SKILL.md)** — how the load lane fits the
  overall CI verification suite

## Quick Reference

### Page-Load Journey Structure

1. Import `http`, `check`, `sleep` from `k6`
2. Read `BASE_URL` from `__ENV` with a default
3. Export `options` (VUs, duration, `thresholds`)
4. In the default function, GET the route
5. `check()` the response status is `200`
6. `sleep(1)` to pace the VU realistically

### Multi-Step Flow Structure

1. Import `http`, `check`, `sleep` from `k6`
2. Read `BASE_URL` from `__ENV` with a default
3. Export `options` (VUs, duration, `thresholds`)
4. Implement `setup()` for any dependency data
5. In the default function, walk the steps (load form → submit) deterministically
6. `check()` each step's response and validate the flow completed
7. Implement `teardown()` to clean up accounts/data the flow created

---

This skill ensures consistent, professional, and effective load testing for the
key user journeys of any profiled React frontend SPA.
