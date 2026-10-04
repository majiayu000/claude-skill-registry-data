---
name: playwright-debugging
description: Diagnostic Playwright workflows for flaky or failing tests, including trace analysis, UI mode, and state isolation.
---

# Playwright Debugging

## Flaky Test Diagnosis and Repair

## Overview

Use this skill when a Playwright test fails intermittently, behaves differently in CI, or passes locally but not in a repeatable way. The goal is to identify the specific cause of the failure before changing the test.

Use this skill as the first stop for failures. It is not a rewrite guide and it is not a replacement for `playwright-core` when the test still needs normal authoring discipline.

This skill focuses on four common failure classes: timing and readiness issues, state bleed between tests, hydration or rendering gaps in SPA frameworks, and flakiness that only appears under CI's specific constraints.

Do not use this skill to redesign a test from scratch unless the current test is beyond repair or the user explicitly asks for a rewrite.

## When to Use

- When a test fails only in CI or only on some runs.
- When a click, assertion, or navigation happens before the UI is ready.
- When a test depends on data, cookies, or local storage left behind by another test.
- When the app renders before it becomes interactive.

## When Not to Use

- When you are writing a new test from scratch.
- When the current test is already stable and the task is just to add new coverage.
- When the app behavior itself needs redesign rather than a narrow test repair.

## Diagnostic Workflow

Start with evidence. Use the failing error, the trace viewer, or the exact step that failed before choosing a fix.

1. Capture the terminal error or the trace step that failed.
2. Decide whether the failure is caused by timing, state bleed, hydration, or a CI-only constraint.
3. Fix the narrowest failing line first.
4. Verify the fix with a repeatable run, not a single green pass.

If the failing step is ambiguous, inspect the trace before editing. Do not generalize from one red run.

## Common Failure Modes

### Timing and Readiness

The UI is present, but the app is not ready for interaction yet. In this case, wait for the state the user would observe, not for an arbitrary timer.

Use web-first assertions, actionability checks, or a specific network response instead of `waitForTimeout()`.

```typescript
import { test, expect } from '@playwright/test';

test('submits the form after the data load completes', async ({ page }) => {
  const responsePromise = page.waitForResponse('**/api/v1/data-load');

  await page.goto('/dashboard');
  await responsePromise;

  await expect(page.getByRole('button', { name: 'Submit' })).toBeEnabled();
  await page.getByRole('button', { name: 'Submit' }).click();
});
```

### State Bleed

The test depends on data that another test created or failed to clean up. Make the test self-contained by setting up its own data, storage state, or API state.

Prefer test-local setup over cross-test ordering. If the state comes from login, use a saved storage state. If it comes from application data, create it within the test or through a setup step.

### Hydration and Rendering Gaps

The DOM appears before event handlers or framework state are attached. Wait for the interactive signal, not just the presence of elements.

This often shows up in React, Next.js, or other SPA frameworks when text is visible before a button is actually usable.

### CI-Specific Flakiness

A test that is stable locally but flaky only in CI is not the same problem as timing,
state bleed, or hydration on their own — it usually means a fix that works on a single
local run doesn't hold up under CI's actual constraints: parallel workers competing for
resources, shared services under load, and machines slower than a dev laptop.

Do not assume a local pass means the underlying fix is complete. Before closing out a
CI-only flake, check for:

- **Worker contention** — multiple parallel workers hitting the same route, database
  row, or rate-limited endpoint at once. Isolate per-worker state (for example, keying
  test data off `test.info().workerIndex`) instead of tightening a timeout.
- **Slower, not just different, timing** — CI machines are frequently slower than
  local hardware, not only less predictable. A wait tied to a real condition
  (assertion, response, URL) survives this; a hardcoded timeout tuned on a local
  machine does not.
- **Environment drift** — feature flags, seed data, or environment variables that
  differ between a local `.env` and CI secrets. Confirm the test isn't passing
  locally only because of state that doesn't exist in CI.
- **Retries masking a real bug** — Playwright's CI retry setting can hide a genuine
  flake behind a "passed on retry" result. Treat a test that only passes on retry as
  still broken, not resolved.

Reproduce the CI failure mode locally under real constraints instead of guessing:

```bash
npx playwright test --workers=4 --repeat-each=10
```

If the failure only reproduces under load or parallelism, the fix belongs in resource
isolation or wait strategy, not in a longer timeout.

## Recommended Tools

- Trace Viewer for post-run inspection of the exact failing step.
- UI mode when the failure needs interactive inspection.
- `--repeat-each` to prove a fix is stable.
- `--trace on` when the issue needs a replayable record.
- CI trace/video artifacts from the actual failing run, not just a local reproduction — a local repro that doesn't match the CI trace is not yet confirmed as the same failure.

## Repair Patterns

- Replace an arbitrary sleep with a specific assertion or response wait.
- Replace a brittle locator with a user-facing role, label, placeholder, or text query.
- Replace a one-off click failure with a readiness check on the element or the data behind it.
- Isolate the failing line instead of rewriting the whole test.

If the symptom points to app state rather than locator choice, confirm whether the test needs a setup project, a route mock, or a proper reset between runs before making the test more complex.

## Verification

After the fix, confirm the failure no longer reproduces under repetition.

Typical checks:

```bash
npx playwright test tests/example.spec.ts --repeat-each=5
npx playwright test tests/example.spec.ts --ui
```

Use the trace viewer to confirm the original failure mode is gone and that the fix matches the observed state change.

If the failure was intermittent, keep the repeat count high enough to make a false green unlikely. One passing run is not enough evidence for a flake repair. If the flake was CI-only, verify with `--workers` set to match your CI configuration, not just `--repeat-each` alone.
