---
name: kelly-app-skill-creator-tests
description: Build, maintain, and run conformance tests for canonical App-in-Skill projects created by kelly-app-skill-creator. Use when a Kelly app skill needs contract checks, local server smoke tests, responsive browser acceptance, temporary open-source Busabase integration, environment-gated Busabase Cloud OAuth verification, lazy provisioning checks, persistence tests, AirApp parity tests, or CI coverage. Keep app creation in kelly-app-skill-creator and own only the reusable test harness, per-skill fixtures, execution gates, diagnostics, and truthful pass/fail/skip reporting.
metadata:
  category: platform
  tags:
    - risk:local-write
---

# Kelly App Skill Creator Tests

Verify generated Kelly app skills without taking ownership of their product or
runtime design. Treat the app source and creator contracts as inputs; never
weaken either contract merely to make a test pass.

## Ownership Boundary

- `$kelly-app-skill-creator` owns product design and creates the canonical
  `<skill-root>/app/` project.
- `$busabase-app-creator` owns AirApp runtime, SDK, security, sync, and deployment
  constraints.
- This skill owns shared test infrastructure, per-skill fixtures and assertions,
  OSS/Cloud execution gates, failure artifacts, CI wiring, and test reporting.
- Keep pure domain and module tests in `<skill-root>/app/test/`. Keep cross-skill
  contract, process, browser, Busabase, OAuth, and AirApp tests under the
  repository-level `tests/app-skills/` tree.

## Required Reading

Before changing tests:

1. Read the target skill's `SKILL.md`, canonical `app/`, resource map, checks,
   and existing tests.
2. Read `$kelly-app-skill-creator` and the runtime rules it delegates to
   `$busabase-app-creator`.
3. Read `references/test-matrix.md` completely for suite boundaries,
   environment variables, and required assertions.

If a dependency skill is unavailable, inspect its checked-in source when
present. Do not invent a weaker replacement contract.

## Workflow

1. Discover canonical apps through `skills/*/app/package.json`. Do not fail
   legacy `app/` directories that have not yet adopted the canonical contract.
2. Reuse one shared harness for process lifecycle, free ports, readiness,
   temporary directories, browser diagnostics, and Busabase startup.
3. Add a small target directory at `tests/app-skills/<skill>/` containing only
   that skill's contract assertions, fixtures, routes, resources, and one
   representative workflow.
4. Run the app's own frozen install and deterministic check before cross-skill
   tests.
5. Run contract and local-server tests, then headless Chromium acceptance at
   1280x820, 390x844, and 360x740.
6. Run the OSS suite against a pinned `busabase server` on a random loopback port
   and temporary data directory. Verify lazy provisioning, exact resources,
   idempotency, representative data, app restart, and Busabase restart.
7. Run Cloud OAuth as a separate suite only when every required credential
   variable is non-empty. Print an explicit skip with missing variable names
   otherwise. Never describe a skipped Cloud suite as validated.
8. Before any live Cloud suite, run deterministic fake-upstream connection
   conformance for zero, one, and multiple Spaces, invalid/stale selection,
   inbound-header bypass, transient auth failure, server change, and logout.
   These cases run on every PR and cannot be skipped because a Cloud account has
   only one Space.
9. Permit Cloud mutations only when the dedicated test Space and explicit
   mutation opt-in are both present. OAuth-only mode must not provision, seed,
   merge, or delete Cloud data.
10. When AirApp credentials and a disposable target are available, run deployed
   ambient-session and local-source parity acceptance separately from standalone
   Cloud OAuth.
11. Report every required suite as pass, fail, or skip, including the exact
    command and failure artifact location. Preserve a failing test when it
    reveals an app, SDK, Busabase, OAuth, or creator-contract defect.

## Integrity Rules

- Pin Busabase, SDK, browser tooling, and package-manager versions used by CI.
- Bind test services to loopback, use random ports, and isolate every OSS run in
  a temporary data and credential directory.
- Use real Busabase APIs for integration tests. Mocks may test error branches but
  cannot satisfy OSS, Cloud, or AirApp acceptance.
- Keep provider-network tests separate from deterministic app tests. Assert
  response contracts and provenance, not volatile prices or counts.
- Never log passwords, API keys, OAuth codes, access/refresh tokens, Vault
  values, cookies, or unredacted response bodies that may contain them.
- Store Cloud OAuth credentials under a temporary `HOME`, revoke the session at
  teardown, and verify the browser did not receive token material.
- Do not run Cloud tests against an unspecified or personal Space. Require a
  dedicated test account; require a dedicated Space before any mutation.
- Capture screenshots and process/API diagnostics on failure, but redact secret
  query parameters, headers, cookies, and bodies first.
- Treat cleanup failure as a test failure when it can leave remote credentials or
  mutable test state behind.

## Completion

Finish only when the target app's own checks, contract tests, local smoke,
responsive Demo flow, and OSS Busabase suite pass. When Cloud variables exist,
Cloud OAuth must pass; when they do not, report the explicit skip and remaining
risk. Do not claim full creator conformance until required AirApp acceptance has
also passed or has been explicitly scoped out by the user.
