---
name: test-pyramid
description: Use this skill whenever writing unit tests, integration tests, E2E tests, or simulator-specific tests for the Myelin platform. This defines what belongs at each layer of the test pyramid, coverage targets, test data requirements, and the specific test cases that are mandatory before release. Load before writing any test code.
---

This skill defines the test pyramid for the Myelin platform. Tests are the executable specification of the platform's correctness. The pyramid structure prevents slow, brittle E2E tests from doing the work that fast unit tests should do — and prevents unit tests from missing the integration failures that only surface when real systems talk to each other.

---

## Pyramid Layers

```
           [ E2E — Learner & Lecturer Journeys ]
         [   Integration — API + DB + Queue + Storage   ]
     [         Unit — Domain Logic, Scoring, Policy          ]
  [ Simulator-Specific — Sequence Gating, Events, Budget Tests  ]
```

Target distribution: 60% unit, 25% integration, 10% E2E, 5% simulator-specific.

---

## Layer 1 — Unit Tests

### What belongs here

Domain logic with no external dependencies. Every function that makes a decision must have unit tests. These run in milliseconds — there is no excuse for skipping them.

### Mandatory unit test subjects

**Simulation scoring and gating:**
- `validateRotationAngle(angle)` — pass at exactly `π/2 ± 0.05`, fail outside
- `validateHaspDistance(distance)` — pass at < 0.02m, fail at >= 0.02m
- `validatePressure(bar)` — pass at < 0.1, fail at >= 0.1
- `resolveTorquePhase(angle)` — returns correct phase torque from `[8.2, 3.1, 11.8]` array
- All 8 `dispatch()` action handlers in the simulation state machine
- `SESSION_COMPLETE` guard — must require all 7 step pass flags true; must reject partial completion

**State machine transitions:**
- Every valid transition in the simulation state machine
- Every invalid transition — must reject and not mutate state
- Wrong-order interaction — must not change state, must return feedback only
- Session reset — must return all step states to LOCKED/UNLOCKED as per scenario config

**Authentication and authorisation:**
- `requireRole()` — pass for correct roles, reject for all others, including adjacent roles
- `requireTenantScope()` — pass for matching tenant, reject for mismatched tenant
- `verifyAccessToken()` — valid token passes, expired token rejects, tampered token rejects, revoked jti rejects

**Scoring and KPI formulas:**
- Module completion rate formula with known numerator/denominator
- First-pass rate formula
- Median time-to-competency with known dataset
- Baseline freeze — must reject second freeze call on same cohort

**Agent context and safety:**
- `assembleAgentContext()` — verify all required fields present, correct fallbacks when simulation not active
- `recentErrors` trimming — must return last 3 only when more than 3 exist
- `classifyAgentResponse()` — each of the 8 response classes with representative inputs
- Safety guardrail trigger detection — assessment boundary, distress keywords, out-of-scope

**POPIA and consent:**
- `requireConsent()` middleware — must block when consent absent, must block when version mismatch
- `resolveChannels()` — mandatory notifications bypass all prefs; SMS requires explicit opt-in
- `resolveScheduledTime()` — must defer to after quiet hours window

```javascript
// Example: SESSION_COMPLETE guard
describe('SESSION_COMPLETE guard', () => {
  it('fires when all 7 steps are PASSED', () => {
    const state = buildAllPassedState();
    const result = dispatch(state, { type: 'SESSION_COMPLETE' });
    expect(result.sessionStatus).toBe('COMPLETED');
  });

  it('rejects when any step is not PASSED', () => {
    const state = buildStateWithStep6NotPassed();
    expect(() => dispatch(state, { type: 'SESSION_COMPLETE' }))
      .toThrow('SESSION_COMPLETE_GUARD_FAILED');
  });
});
```

---

## Layer 2 — Integration Tests

### What belongs here

Behaviour that crosses system boundaries: API endpoints that write to the database, queue jobs that trigger downstream effects, storage operations.

Use a real test database (not mocks) seeded with fixtures. Use a real queue (in-memory or test container). Do not mock the database in integration tests — mocks hide the real failure modes.

### Mandatory integration test subjects

**API + Database:**
- Learner registration flow: POST `/auth/register` → user created in DB → consent record absent → consent gate blocks training access
- Simulation session creation: POST `/sim/session` → session record created → demoMode flag set correctly → immutable after creation
- Step event ingestion: POST `/sim/event` → event written to correct table (live vs demo) → state machine advances
- Role assignment: POST `/admin/roles` → role record created → audit log entry written in same transaction
- Cross-tenant rejection: attempt to read another tenant's submission → 403 returned, no data leaked, audit entry written as SECURITY_TENANT_SCOPE_VIOLATION

**Queue + Storage:**
- File upload: POST `/upload` → malware scan queued → transcode job queued → object key is system-generated (never original filename) → signed URL expires at 15 minutes
- Notification dispatch: trigger `RESULT_STATEMENT_ISSUED` → notification record inserted as QUEUED → job enqueued → `MENTOR_INVITE` (mandatory) cannot be suppressed by recipient prefs

**Auth lifecycle:**
- Login: POST `/auth/login` → valid credentials → access + refresh token returned → tokens verifiable → jti stored
- Token refresh: POST `/auth/refresh` → valid refresh token → new access token returned → old access token still valid until TTL
- Session revocation: POST `/auth/revoke` → jti added to revocation list → subsequent use of revoked token returns 401

---

## Layer 3 — E2E Tests

### What belongs here

Critical user journeys tested against a running staging environment. These are slow — run them before every release, not on every commit.

### Mandatory E2E journeys

**Learner journey:**
1. Register → land on consent gate → confirm consent → enrol in programme
2. Complete module content → enter simulator → complete all 7 LOTO steps → reach SESSION_COMPLETE
3. Submit evidence → receive UNDER_REVIEW status → receive notification when outcome set
4. Receive PASSED result → result statement generated → verification URL resolves

**Lecturer journey:**
1. Login as Lecturer → view cohort dashboard → see pending submission
2. Open submission → score rubric criteria → set outcome PASSED → learner notified
3. View KPI dashboard → completion rate visible → no data from other tenants visible

**Admin journey:**
1. Login as Admin → invite mentor → mentor accepts invite → mentor assigned to placement
2. Trigger data subject access request → export pack contains all required entity types
3. View audit log → actions from own tenant visible → actions from other tenants not visible

**Security rejection journey:**
1. Attempt unauthenticated API call → 401 returned
2. Attempt cross-tenant data access with valid token → 403 returned
3. Attempt file upload with executable MIME type → rejected with FILE_TYPE_NOT_ALLOWED

---

## Layer 4 — Simulator-Specific Tests

### What belongs here

Tests unique to the 3D simulation that cannot be exercised at the unit or integration layer because they depend on the physics engine, timing, or rendering context.

### Mandatory simulator-specific tests

**Step sequence gating:**
- Attempting to interact with Step 3 (hasp) before Step 2 (valve) is PASSED → wrong-order feedback returned, no state change
- Completing steps out of order in all 6 invalid permutations → no false PASS events
- Attempting SESSION_COMPLETE interaction without all steps PASSED → guard fires, session not completed

**Event emission:**
- Every `SimulationStepEvent` PASS and FAIL for all 7 steps must be emitted with the correct `measuredValue` and `requiredThreshold`
- `SimCompleteEvent` emitted exactly once per session at SESSION_COMPLETE — never twice
- `SimPerfEvent` emitted every 60 seconds of active session time — not during tab-hidden time
- Demo mode: all events written to `demo_simulation_step_events`, none to `simulation_step_events`

**Physics validation:**
- Rotation validation: `π/2 ± 0.05 rad` threshold — test at exactly the boundary values
- Hasp distance: test at 0.019m (pass), 0.020m (fail boundary), 0.021m (fail)
- Pressure model: test at 0.09 bar (pass), 0.10 bar (fail boundary), 0.11 bar (fail)
- Torque curve: dispatching motor force at each of the 3 phase boundaries returns correct resistance value

**Performance budget:**
- Simulate 60-second LOTO traversal with all assets loaded at HD quality tier
- Assert: p95 frame time < 22ms (45+ fps equivalent)
- Assert: physics step time avg < 3ms
- Assert: texture memory < 450MB (90% of ceiling)
- Assert: no `requestAnimationFrame` misses during step interaction events

```javascript
describe('Hasp distance threshold', () => {
  it('PASS at 0.019m', () => {
    expect(validateHaspDistance(0.019)).toBe('PASS');
  });
  it('FAIL at exactly 0.020m', () => {
    expect(validateHaspDistance(0.020)).toBe('FAIL');
  });
  it('FAIL at 0.025m', () => {
    expect(validateHaspDistance(0.025)).toBe('FAIL');
  });
});
```

---

## Test Data Requirements

- Unit tests: use pure in-memory fixtures — no database, no network
- Integration tests: dedicated test database, reset between test runs, seeded with known fixture datasets per test suite
- E2E tests: isolated staging environment, dedicated test tenant, synthetic learner accounts
- Never use production data in any test environment
- Fixture learner IDs must be in a reserved namespace (e.g. `test-*`) to prevent accidental inclusion in production reporting

---

## CI/CD Integration

| Layer | When it runs | Must pass to |
|-------|-------------|-------------|
| Unit | Every commit, every PR | Merge to main |
| Integration | Every PR merge to main | Deploy to staging |
| E2E | Every staging deployment | Promote to production |
| Simulator-specific | Every staging deployment | Promote to production |

A failing unit test must not be merged. A failing integration or E2E test must not be promoted to production. Skipped tests are treated as failures in the CI pipeline — do not skip tests to make a build pass.

---

## What Not To Do

- Do not mock the database in integration tests — use a real test database
- Do not use production data in test environments
- Do not skip tests to make a build pass — fix the test or fix the code
- Do not put integration-level assertions (DB state, queue jobs) in unit tests
- Do not run E2E tests on every commit — they are pre-release only
- Do not allow `SESSION_COMPLETE` guard tests to test only the happy path — all 7 step failure permutations must be covered
- Do not test boundary values only at round numbers — always test at the exact threshold value (0.020m, not 0.02m rounded)
