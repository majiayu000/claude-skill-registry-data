---
name: fleet-phase-testing
description: Phase-appropriate testing — what level of rigor for POC vs MVP vs staging vs production. Prevents over-testing early work and under-testing production code.
user-invocable: false
---

# Phase-Appropriate Testing

## The Problem

Testing a POC with production rigor wastes time. Testing production code
with POC rigor creates incidents. The delivery phase determines the
testing standard.

## Phase Standards

### POC (Proof of Concept)
**Goal:** Does it work at all?

| Test Type | Required | Notes |
|-----------|----------|-------|
| Happy path | Yes | Core functionality works |
| Error handling | No | Crashes are acceptable |
| Edge cases | No | Focus on the concept |
| Performance | No | Speed doesn't matter yet |
| Security | Minimal | No auth bypass, no secrets in code |
| Integration | Manual | Run it, see if it works |
| Coverage target | None | Coverage metrics don't apply |

**QA focus:** Does the concept prove what it set out to prove?

### MVP (Minimum Viable Product)
**Goal:** Can users rely on it?

| Test Type | Required | Notes |
|-----------|----------|-------|
| Happy path | Yes | All primary flows work |
| Error handling | Yes | Graceful failures, clear messages |
| Edge cases | Key ones | Common boundary values |
| Performance | Basic | Doesn't hang, responds in reasonable time |
| Security | Standard | Auth works, inputs validated, no injection |
| Integration | Automated | CI runs tests on every push |
| Coverage target | 60%+ | Critical paths covered |

**QA focus:** Would the PO be comfortable showing this to someone?

### Staging
**Goal:** Production-ready verification

| Test Type | Required | Notes |
|-----------|----------|-------|
| Happy path | Yes | Complete coverage |
| Error handling | Yes | All error paths tested |
| Edge cases | Yes | Boundary value analysis complete |
| Performance | Yes | Load testing, response time SLAs |
| Security | Thorough | Penetration testing mindset |
| Integration | Full | End-to-end with real services |
| Coverage target | 80%+ | All modules covered |

**QA focus:** Does this survive real-world conditions?

### Production
**Goal:** Battle-tested reliability

| Test Type | Required | Notes |
|-----------|----------|-------|
| Happy path | Yes | Complete |
| Error handling | Yes | Including cascading failures |
| Edge cases | Yes | Including adversarial inputs |
| Performance | Yes | Under load, under stress, under degradation |
| Security | Complete | Full audit, dependency scanning, secret detection |
| Integration | Full | With monitoring and alerting |
| Coverage target | 90%+ | Including error paths |
| Regression | Yes | Every bug fix gets a regression test |

**QA focus:** Can we sleep while this runs?

## Applying Phase to Fleet Tasks

When predefined test criteria for a task:

1. Check the task's `delivery_phase` field
2. Apply the phase standard from above
3. Scale your TC-XXX criteria accordingly

```
## Test Definition: {task_title}
## Delivery Phase: {phase}

Phase standard applied: {description}

TC-001: ... (happy path — required at all phases)
TC-002: ... (error handling — required at MVP+)
TC-003: ... (boundary value — required at staging+)
```

### Phase Escalation

When a feature moves from one phase to the next, the test suite must
be upgraded:
- POC → MVP: Add error handling tests, key boundary values
- MVP → Staging: Add full boundary analysis, performance tests
- Staging → Production: Add adversarial inputs, regression suite

## Common Mistakes

1. **Over-testing POC** — Writing 50 tests for throwaway code
2. **Under-testing MVP** — "It works on my machine" is not a test
3. **Skipping phase upgrade** — Feature goes to staging with POC-level tests
4. **Ignoring the phase field** — Testing everything at production level
   regardless of delivery phase — wastes capacity
5. **No security at any phase** — Even POC should not have hardcoded
   credentials or SQL injection
