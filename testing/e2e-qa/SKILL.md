---
name: e2e-qa
description: "End-to-end testing with Playwright and Cypress plus real CLI and HTTP journeys: test architecture, locator discipline, network interception, flake elimination, CI parallelization. Use when writing, fixing, or debugging E2E, browser, or user-journey tests. Unit and integration testing belongs to qa-automation."
license: MIT
allowed-tools: Bash
metadata:
  display-name: "E2E QA"
  version: "1.1"
  platforms: "claude-code codex"
  tags: "testing e2e playwright cypress"
---

# End-to-end QA

E2E tests exercise the real, running application through its public interface. They are expensive (slow, flaky, hard to debug). Use them deliberately - for the few critical flows that *must* work - and aggressively for everything else.

## What belongs in E2E

- The login → core action → logout golden path.
- Payment / checkout / signup - anything that loses revenue or trust when broken.
- A handful of cross-page flows that span auth + data + UI state.

What does **not** belong in E2E:
- Form validation (unit-test the validator).
- Pure rendering (component test).
- Backend logic (integration test against the real API).
- Anything you can cover faster at a lower level.

If you find yourself writing the 30th E2E test for the same page, the pyramid is upside-down. Push them down to component or integration.

## Locator discipline

- **Prefer accessible queries.** `page.getByRole('button', { name: 'Save' })`, `page.getByLabel('Email')`, `page.getByText(...)`. They double as accessibility checks.
- **Fall back to test-ids only when role/label is ambiguous.** Test-ids are coupling between test and DOM - keep them rare.
- **Never select by CSS class.** Classes change with refactors; tests should not.
- **One assertion-style locator per test.** Don't `await page.locator('div').nth(3)` - name the thing.

## Waiting and synchronization

- **Wait for state, not for time.** `await expect(locator).toBeVisible()` retries automatically; `await page.waitForTimeout(500)` is a flake waiting to happen. Prefer a *visible* signal over a transport one; for animations, `prefers-reduced-motion` or disabled transitions in the test build.
- The general flake doctrine - a flaky test is broken, fix it instead of retrying it green - belongs to `qa-automation`.

## Network handling

- **Real backend for E2E.** That's the point. Hitting a mocked API is integration testing.
- Stub *only* third-party services you don't control (payment providers, email gateways, analytics).
- Use Playwright `route` / Cypress `intercept` to inject deterministic responses for those edges.
- Avoid recording-and-replaying entire user journeys; tests become brittle to harmless backend changes.

## Test data

- **Isolated state per test.** No shared user, no shared session. The next test must not depend on the previous one's side effects.
- Seed via API, not UI. `await api.createUser(...)` beats `await page.fill('email', ...).click('signup')`.
- Tear down at the end (or use a per-test transaction / namespace). Leaked test data poisons future runs.
- Generate unique identifiers per test (`crypto.randomUUID()`, `Date.now()`) - no hardcoded `test@example.com`.

## Browser context strategy

- One worker per test, one context per test. Isolation is non-negotiable.
- `storageState` snapshots for "already-logged-in" tests - generate once in `globalSetup`, reuse across tests that don't need a login flow.
- Multi-user / multi-tab tests: spin up multiple `context`s; never share cookies between them.

## Parallel CI

- In CI, default to full parallelism only when runner memory is sized for the browser worker count (`fullyParallel: true` in Playwright; `--parallel` in Cypress Cloud).
- On a shared local machine, run one browser suite at a time and cap its workers to available memory. Never let multiple agents launch Chromium, Playwright, or Cypress concurrently unless the user explicitly asks and capacity has been verified.
- Sharding for monorepos: `--shard=1/4` across 4 CI workers cuts wall-clock by ~4×.
- Retries: `retries: 1` is reasonable; `retries: 3` is masking flake - investigate instead.
- Trace + video on first retry only. Don't record everything; storage cost adds up.

## Debugging a failing E2E

1. Reproduce locally with `--headed --debug` (Playwright) or `cypress open` first.
2. Look at the trace / video / screenshots from CI before adding logs.
3. If it's "works locally, fails in CI" - almost always timing, headless rendering, or test-data leakage. Not a real bug.
4. If it's genuinely racy in the app - fix the app. The test surfaced a real bug.

## Auth patterns

Three patterns - cookie injection via a test seed endpoint, `storageState` + `globalSetup`, and full mocking - with code in `references/auth-patterns.md`. Pick by app type; never script the login UI in every test.

## CI baseline config

Every project should have these guards in `playwright.config.ts`:

```ts
export default defineConfig({
  fullyParallel: true,                          // false + workers:1 only if tests share a DB file
  forbidOnly: !!process.env['CI'],              // prevents .only from blocking CI
  retries: process.env['CI'] ? 1 : 0,          // 1 retry hides transient flakes; 2+ masks real bugs
  reporter: process.env['CI']
    ? [['github'], ['list']]                    // github = inline PR annotations
    : 'list',
  use: { trace: 'on-first-retry' },            // captures trace on flakes without bloating storage
});
```

## Stack notes

The stack is whatever the repository declares, not a fixed list. Before concluding "no E2E here," enumerate the project's own runnable journey targets - build-file targets (`Makefile`/`justfile`), `package.json` scripts, CI job names, README validation section - engine and CLI projects included; treat those targets as existing E2E and run them.

### Playwright (TypeScript)
- `npx playwright codegen <url>` for initial scaffolding - but rewrite the generated locators to role-based ones.
- `expect(locator).toHaveScreenshot()` for visual regression, with a generous `maxDiffPixelRatio`. Commit baselines per platform (Linux + macOS diverge).
- `test.step('description', async () => { ... })` to make trace files readable.

### Cypress
- One assertion per command chain. `cy.get(...).should(...)` retries; long chains amplify retries badly.
- `cy.session()` for cached login state across tests.
- Avoid `cy.wait(ms)` - it's the most common cause of flake in Cypress suites.

### CLI / API E2E
- Same principles: real binary, real network, real data lifecycle. Spawn the process with `execa` / `subprocess`, assert on `stdout`/`stderr` AND exit code.

## Verification before declaring done

- Run the suite headless 3× locally with random ordering. No flakes.
- Open the trace from a CI run, walk through the failing-then-passing diff.
- Check wall-clock - if the suite went from 2 min to 8 min, the cost of "one more E2E" was real.
