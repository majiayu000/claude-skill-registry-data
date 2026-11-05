---
name: gateway-testing
description: Route testing tasks to the right library skill. Covers unit, integration, e2e, coverage, and test quality.
type: gateway
tier: core
domains: [testing, qa, verification]
trigger: "test, spec, jest, vitest, pytest, coverage, mock, stub, fixture, e2e, integration test, flaky"
---

## Purpose

You are the Testing Gateway. Route testing tasks to specialized library skills.

## Intent Detection → Skill Routing

| Intent Keywords | Load Skill |
|---|---|
| `unit test`, `mock`, `stub`, `spy`, `isolated` | `skills/library/testing/unit-testing-patterns/SKILL.md` |
| `integration test`, `e2e`, `end-to-end`, `supertest` | `skills/library/testing/integration-testing/SKILL.md` |
| `coverage`, `lcov`, `istanbul`, `c8`, `threshold` | `skills/library/testing/coverage-strategies/SKILL.md` |
| `snapshot`, `visual regression`, `toMatchSnapshot` | `skills/library/testing/snapshot-testing/SKILL.md` |
| `load test`, `stress`, `k6`, `artillery`, `benchmark` | `skills/library/testing/load-testing/SKILL.md` |
| `fixture`, `factory`, `seed`, `faker`, `test data` | `skills/library/testing/test-data-factories/SKILL.md` |
| `flaky`, `race condition`, `async`, `intermittent fail` | `skills/library/testing/fixing-flaky-tests/SKILL.md` |

## Output Format

```
GATEWAY_TESTING:
Domain: testing
Skills to load:
  - [absolute/path/to/SKILL.md]

Instructions: Read the above skill files before proceeding with your task.
```
