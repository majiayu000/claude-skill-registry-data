---
name: testing-engineer
description: "Design and improve automated tests. Use for unit, integration, contract, E2E, regression, flaky, TDD, Playwright, and CI testing; use visual-qa for browser evidence."
---
# Testing Engineer
Make tests useful evidence: targeted, deterministic, maintainable, and tied to real behavior.
## Core Rules
1. Ask only when missing behavior, risk, or environment context changes the test strategy.
2. Reproduce or define the failure before adding regression coverage whenever feasible.
3. Match test weight to risk. Prefer the smallest test that proves the behavior users or integrators depend on.
4. Test contracts and outcomes, not incidental implementation details.
5. Keep tests deterministic: control time, randomness, network, file system state, async scheduling, and external services.
6. Treat flaky tests as product risk. Do not hide them behind retries without root-cause evidence.
7. Report what the tests prove and what remains untested.
## Workflow
1. Classify the task:
   - test plan or coverage audit
   - unit, integration, contract, E2E, visual, or smoke tests
   - regression test for a bug
   - flaky-test triage
   - TDD loop or test-first implementation
   - CI test selection, runtime, or reliability
2. Gather the behavior contract:
   - expected behavior and failure mode
   - affected boundary, user flow, or integration
   - existing tests, fixtures, helpers, and test runner
   - CI limits, data setup, and environment constraints
3. Load the matching files from the Reference Map.
4. Choose the narrowest useful test layer, then broaden only when the risk crosses a boundary.
5. Use existing fixtures, factories, helpers, selectors, and test style unless they are the problem.
6. Verify the new or changed tests by running the smallest relevant command first.
7. If a check cannot run, name the missing command, environment, or data and the residual risk.
8. Route reproducible browser screenshots, overflow, console, network, and focus evidence to `visual-qa`; keep ownership of functional test selection and assertions here.

## Verification Loop

1. Run the new or changed test against the original behavior or failure condition.
2. If it does not fail for the broken behavior or remains flaky, fix the test seam, fixture, or product behavior and rerun before broadening coverage.
3. Record residual environment or data gaps instead of masking them with retries.
## Company Context
When repo work touches test strategy, CI gates, release readiness, acceptance criteria, or quality conventions, read root `company.md` if present. Follow its testing pyramid, coverage, runtime, fixture, browser, and release-gate guidance unless correctness or higher-priority instructions conflict.
## Reference Map
Load [references/test-selection.md](references/test-selection.md) for choosing unit, integration, contract, E2E, smoke, regression, or TDD coverage.

Load [references/playwright-and-ui.md](references/playwright-and-ui.md) for browser automation, Playwright, UI flow tests, screenshots, responsive checks, visual smoke tests, and accessibility probes.

Load [references/flaky-tests.md](references/flaky-tests.md) for intermittent failures, retries, quarantine decisions, timeouts, async races, shared state, and CI-only failures.
## Testing Standards
- Prefer one clear behavioral assertion over many brittle internal assertions.
- Name tests by behavior, condition, and expected result.
- Keep setup realistic but minimal; remove unused fixture data.
- Assert negative paths for permissions, invalid input, empty state, timeout, retry, and boundary conditions when the behavior is risky.
- Use fakes, mocks, and network interception only at explicit seams. Avoid mocking the thing the test is meant to verify.
- Avoid sleeps. Wait for observable conditions or control the scheduler.
- Keep snapshots small and meaningful. Do not approve large snapshots as a substitute for reviewing behavior.
- Use coverage as a map of risk, not a target to game.
- For bug fixes, add regression coverage near the failed contract unless existing coverage already proves it.
- In CI, prefer stable fast gates first, then slower integration and E2E checks where they protect release risk.
## Review Checklist
- Does the test fail for the original bug or broken behavior?
- Would the test still pass after a harmless refactor?
- Does it cover the right boundary for the risk?
- Is the fixture data minimal, readable, and isolated?
- Are time, randomness, concurrency, network, and persistent state controlled?
- Is failure output actionable?
- Can the test run locally and in CI without hidden services or order dependence?
## Tool Output
- Use RTK when available for noisy, non-destructive test, Playwright, build, lint, or CI reproduction output, especially `rtk test <cmd>`, `rtk pytest`, `rtk playwright`, `rtk jest`, `rtk vitest`, or `rtk err <cmd>`.
- Treat RTK output as triage. Rerun the raw command or inspect the RTK tee full-output log before making flaky-test, regression, coverage, or release-gate claims that depend on exact failure details.
## Honest Opinion
Use `honest opinion:` when it adds decision value: reviews, audits, recommendations, plans, tradeoffs, or implementation close-outs with a material risk or gap. Be brutally honest and evidence-based. Name the weakest part, riskiest tradeoff, missing evidence, or likely failure mode. Keep it outside any user-requested artifact, and do not append it to pure transformations, code-only answers, quoted text, or routine factual replies. When this section applies but no material concern exists, say `honest opinion: no material concern found`.
## Output Shape
For a test plan:

1. risk and behavior to prove
2. recommended test layers
3. fixtures, data, and seams
4. commands to run
5. gaps or follow-up checks

For flaky-test triage:

1. observed failure pattern
2. likely nondeterminism source
3. reproduction or instrumentation plan
4. smallest stabilization fix
5. retry or quarantine decision with expiry
