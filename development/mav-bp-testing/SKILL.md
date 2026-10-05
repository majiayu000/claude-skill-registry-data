---
name: mav-bp-testing
description: 'Testing standards — unit and integration testing as one discipline. Maverick''s opinionated rules: behaviour over implementation, mock at boundaries only, 60% unit-coverage CI gate, critical-path integration coverage with a no-decrease ratchet. Applied when writing or reviewing tests.'
user-invocable: false
disable-model-invocation: true
---

# Testing Standards

Unit and integration testing as one discipline. Unit tests verify
behaviour in isolation; integration tests verify real wiring across
boundaries. Together they are the only automated evidence that generated
code actually works.

## Maverick's Rules

**Unit tests**
- **Test behaviour, not implementation.** Assert on outputs and effects,
  never on reimplemented logic (tautological tests) or internal calls.
- **Mock at the boundary only** (APIs, DB, filesystem). Never mock what
  you own; prefer stubs over mocks; >3 mocks in one test means the unit's
  design is wrong.
- **No logic in tests** — no conditionals, loops, or try/catch in test
  bodies. No test interdependence. Delete flaky tests rather than keep
  them.
- A unit test taking >100ms is hitting real I/O — fix it.

**Integration tests**
- **Complement, don't duplicate** — cover cross-boundary behaviour
  (endpoints, persistence, external clients); never re-test unit-covered
  logic.
- Each test owns its data and cleans up; parallel runs never collide.
- Real dependencies in order of preference: containers → sandboxes →
  fakes. Never production services.
- Health-check polling with timeouts, never sleeps. Every test has an
  explicit timeout.

**Coverage (enforced, not aspirational)**
- **Unit: 60% minimum, gated in CI** — the build fails below it. The
  number is a floor, not a goal: coverage with weak assertions is worse
  than less coverage with strong ones.
- **Integration: every critical cross-boundary path** (auth, payment,
  persistence, external APIs) **has at least one test, and coverage
  must not decrease** — a ratchet, not a percentage floor.

## Project Implementation Lookup

Check `docs/maverick/skills/unit-testing/SKILL.md` and
`docs/maverick/skills/integration-testing/SKILL.md` for the project's
framework, conventions, and extra requirements. If present, they win on
specifics. If missing, proceed with these standards and note the gap in
your summary — do not trigger skill generation mid-task.

## Detecting Testing Issues in Code Review

| Pattern | Issue | Fix |
| ------- | ----- | --- |
| Test with no assertions | False confidence | Add meaningful assertions |
| Mocking internal modules | Brittle tests | Mock at boundaries only |
| Test name describes implementation | Couples to internals | Describe behaviour instead |
| Shared mutable state between tests | Test pollution | Use beforeEach/factory functions |
| Test catches and swallows errors | Hidden failures | Let errors propagate or assert on them |
| >3 mocks in one test | Unit has too many dependencies | Refactor the unit's design |
| Test duplicates implementation logic | Tautological test | Assert on outputs, not reimplemented logic |
| Commented-out tests | Dead tests hiding failures | Delete or fix |
| Test hits production service | Side effects and flakiness | Use container, sandbox, or stub |
| No cleanup after test | Data leaks between tests | Add teardown or transaction rollback |
| Sleep-based waits for dependencies | Flaky timing | Health-check polling with timeout |
| Integration test duplicates unit coverage | Wasted execution time | Delete and rely on the unit test |
| No timeout set | Hanging test blocks CI | Set explicit per-test timeout |
| Hard-coded connection strings | Breaks across environments | Use environment variables or config |
| Test requires manual environment setup | Not reproducible | Automate with containers or scripts |

<!-- maverick-plugin-version: 4.0.2-dev -->
