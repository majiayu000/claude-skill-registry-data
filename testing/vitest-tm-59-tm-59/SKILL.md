---
name: vitest
description: Use when writing unit and integration tests with Vitest for TypeScript or JavaScript projects built with Vite — test layout, deterministic tests for seeded simulations, threshold tests that turn benchmarks into regressions, mocking timers and modules, DOM tests with jsdom, and keeping the suite fast enough for a pull-request gate. Also use when tests are flaky, slow, or pass locally but fail in CI.
---

# Vitest

Default: `vitest run` in CI and `vitest` (watch) locally, tests next to code (`*.test.ts`) or in `tests/`, `environment: "node"` unless DOM is needed, no network in unit tests.

## Setup

```ts
// vitest.config.ts (or the `test` key in vite.config.ts)
import { defineConfig } from "vitest/config";
export default defineConfig({
  test: { environment: "node", include: ["src/**/*.test.ts", "tests/**/*.test.ts"], testTimeout: 10_000 },
});
```

Use `environment: "jsdom"` (or `happy-dom`) per file with a `// @vitest-environment jsdom` comment, so most tests stay fast in Node.

## Tests that carry weight

- **Determinism:** same seed → same result. `expect(run(seed)).toEqual(run(seed))` and a snapshot of a short summary (not of huge objects).
- **Thresholds from benchmarks:** run an automated player over several seeds and assert ranges, e.g. "first enemy defeated within 15 s", "no deaths in the first zone", "win rate of the final boss between 55 % and 85 %". This turns "feel" into regressions that fail.
- **Invariants over examples:** "every level is solvable", "all locales have all keys", "no two items overlap", "every UI action has a sound and an effect".
- **Derived numbers:** assert that UI text uses counts derived from data, so adding content does not break tests.

## Mocking

- `vi.useFakeTimers()` + `vi.advanceTimersByTime(ms)` for time-based logic; restore with `vi.useRealTimers()`.
- `vi.mock("./module")` for module boundaries; prefer dependency injection for anything you mock often.
- `vi.spyOn(console, "error")` and fail tests that log unexpected errors.

## Keeping it fast

- Separate heavy suites (`test:full`) from the PR gate (`test`), and run the heavy one locally before releases.
- Avoid real `setTimeout` waits; use fake timers or direct calls.
- Keep fixtures small; generate large inputs in code from a seed.

## Verification loop

1. `npx vitest run` passes with no skipped tests that should run.
2. `npx vitest run --coverage` on core logic when coverage is a goal (do not chase 100 % on rendering code).
3. Run twice in a row; a test that fails on the second run shares state.

## Pitfalls

- **Shared module state** between tests (singletons, caches) causes order-dependent failures; reset in `beforeEach` or isolate.
- **Floating point:** use `toBeCloseTo` for computed values.
- **Snapshot drift:** reviewers approve large snapshot diffs without reading; keep snapshots small and meaningful.
- **Hidden network calls** (fetching data in a module's top level) make tests slow and flaky; move I/O behind functions.
- **Timezone-dependent dates:** set `TZ` in the test script (`TZ=UTC vitest run`) or inject the clock.
