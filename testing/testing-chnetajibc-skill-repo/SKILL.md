---
name: testing
description: "Test pyramid unit/integration/E2E/contract: happy path, edges, invalid input, authz, concurrency, idempotency. Tests are proof; run them."
---

# testing

Tests are proof: red first, green with the fix, refactor under cover. No claim without a run.

## Activate when

- Writing tests, fixing bugs (regression test mandatory), or judging coverage adequacy.

## Do NOT activate for

- Manual-only verification where automation fits (automate it); UI probing specifics (see frontend/ui-verification).

## Procedure

1. Level by risk: units for logic, integration for seams (DB/API with Testcontainers where real), E2E for critical journeys (Playwright/Cypress), contracts for API surfaces.
2. Red-green: failing test first, then the minimal fix; behavior-focused assertions, no implementation-mirroring tests.
3. Matrix: happy path, edges, invalid input, authz-cross-user, concurrency, idempotency, timeouts/retries.
4. Hygiene: isolated (no order dependence, no shared mutable fixtures), deterministic (seeded randomness, controlled time), fast enough to run always.
5. UI proof via probes where available (`../../frontend/ui-verification/`).
6. Verify: full related suite green, new tests fail without the fix (spot-check by revert), flaky tests quarantined with owner — never deleted silently.

## References
- Related: `../../frontend/ui-verification/`.
