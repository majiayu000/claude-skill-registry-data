---
name: fix-the-suite
description: Composite skill — diagnose, repair, and validate a test suite end-to-end. Chains test-health (diagnose) → config-drift-detect (gate compatibility) → test-cleanup (prune + add integration tests) → mutation-test (validate survivors) → adr-write (capture decisions) → docs-sync. Use when "the test suite is bad" or you've hit the test-cleanup-bails-at-the-gate failure mode.
triggers:
  - fix-the-suite
  - bloated-suite
  - slow-suite
  - test-failure-clusters
  - composite skill
  - cleanup
  - mutation
  - capture
---

# Fix The Suite

Replaces the pass-1 / pass-2 / pass-3 cycle (where each pass deletes 16 tests then
bails out at the coverage gate) with one workflow that runs all the right skills in
the right order.

## Auto-invocation triggers

- Test count is >2× the proportionality target for the app type
- Suite runtime >5 minutes
- User reports "tests are slow", "too many tests", "test cleanup didn't work"
- After any cleanup pass that reported "needs further work / out of scope"

## Workflow

### Phase 1 — Diagnose (always)
Invoke `test-health` for the full picture: count vs proportionality, coverage vs
threshold, runtime, slowest tests, dead weight, mocked-SUT count, flake estimate.

If verdict is HEALTHY → exit; nothing to fix.

### Phase 2 — Gate compatibility check (always)
Invoke `config-drift-detect` scoped to test config (jest/vitest thresholds).
If a CRITICAL gate conflict surfaces (e.g., 99% functions on a 3k-LOC project),
**resolve it before pruning**:
- Surface the conflict per the test-cleanup Step 1.5 protocol
- Get explicit user choice: lower gate / exclude files / commit to integration tests
- Do not start Phase 3 until resolution is recorded

### Phase 3 — Prune + replace (always)
Invoke `test-cleanup` with the resolution from Phase 2.
The skill already chains internally: skipped tests → whole files → waste patterns →
batched coverage check → integration test replacement (it.each) → consolidation.

### Phase 4 — Validate survivors (always)
Invoke `mutation-test` per-file or scoped to changed files.
If mutation score <60% on critical modules: loop back to Phase 3 to write
real-behavior tests for the survivor mutants.

### Phase 5 — Capture (mandatory if Phase 2 changed gates)
Invoke `adr-write` to record:
- The gate change (if any) and why
- The cleanup outcome
- The proportionality reasoning
Without an ADR, the next person will revert the gate change.

### Phase 6 — Sync (always)
Invoke `docs-sync` to ensure any modified standards/skills propagate.

## Reconciliation

Final report:
```
FIX THE SUITE — <repo>
  Diagnose:   tests=N coverage=X% runtime=Ts → BLOATED
  Gates:      <conflicts found, resolution>
  Cleanup:    N → M tests (-X%), runtime -Y%, coverage maintained at X%
  Mutation:   score <Z>% on changed files
  ADR:        <path> (if gate changed)
```

## Outputs / Evidence

- test-health report (before)
- config-drift verdict + resolution
- test-cleanup report (deletions, integration tests written)
- mutation score
- ADR path if applicable
- Final coverage proof from CI

## Failure / Stop Conditions

- Phase 2 conflict cannot be resolved (user declines all options) → stop with
  clear "this suite cannot be efficiently cleaned without one of: A/B/C"
- Phase 4 mutation score collapses (<40%) after cleanup → revert the cleanup,
  the deletions removed real protection
- Never skip Phase 2 — it's the failure mode this whole workflow exists to prevent
