---
name: testing-plan
description: Generate a testing plan from FRs, ACs, and decisions. Assigns every acceptance criterion a tier (ci, eval, manual) and a test type and phase. Identifies security, resilience, performance, and E2E test needs. Used at the start of Phase 2.
---

# Testing plan

Draft the testing plan for a build. The PO owns and approves it; developers write the
tests from it; the PO approves each test before it is locked (WORKFLOW.md "Phase 2").

## Input

1. The version spec UC file: `dev/versions/vN/spec/02-use-cases/UC-XXX.md`
2. Every in-scope FR in `dev/versions/vN/spec/` — especially their ACs and `Check` tags.
3. Every in-scope NFR.
4. Decisions from Phase 1: `dev/decisions/DEC-*.md`
5. The research checklist and the matrix: `dev/versions/vN/builds/UC-XXX-label/`

Read the version spec, never the target spec: only the version spec has ACs.

## Process

### Step 1 — Assign a tier to each AC

Start from the matrix's Tier column (seeded in Phase 1 from `Check`):

- `deterministic` → **ci**: an automated test; the model is replaced by a recorded
  fixture or a mock. Name the fixture.
- `evaluation` → **eval**: fixed cases against a real model, scored by a rubric. The
  rubric scores exactly what the AC's Then says. Propose a pass threshold.
- Only a person can judge it (visual quality, feel) → **manual**: describe what the PO
  checks and how.

Flag any AC whose tier looks wrong (for example, a deterministic check that needs a real
model) instead of silently changing it. The PO decides.

### Step 2 — Map ACs to test types

- Pure validation logic → unit test (with implementation)
- Security-related (SSRF, input validation, data leaving the machine) → security test
  (pre-implementation)
- External integration (model provider, file system, runtime) → integration test
  (post-implementation)

For each ci-tier acceptance or security test, write the **Checks** cell: what the test
asserts, in one line. It must let a developer write the test and the PO review it against
the AC without reading anything else.

### Step 3 — Identify UC-level tests

- **E2E test:** UC happy path (all S steps in order)
- **E2E tests:** each alternative flow that reaches a different end state
- **Smoke tests:** minimal checks that prove the build works
- **Recovery/resilience tests:** each alternative flow with a failure condition

### Step 4 — Identify NFR tests

- An NFR with a measurable target → performance test with the target as the assertion.
- An NFR describing a behavior → E2E or integration test.

### Step 5 — Phase assignment

| Test type | Tier | Written | Ticket created in |
|---|---|---|---|
| Acceptance, security | ci | Before implementation | Phase 2 (`phase:test-stubs`) |
| Eval cases and rubric | eval | Before implementation | Phase 2 (`phase:test-stubs`) |
| Manual check | manual | Listed in the plan only | — |
| Unit | ci | With implementation | Phase 4 impl tickets |
| Integration, recovery | ci | After the modules they test | Phase 4 (`phase:post-impl`) |
| E2E, smoke, performance | ci | After all implementation | Phase 4 (`phase:post-impl`) |

## Output

Create `dev/versions/vN/builds/UC-XXX-label/testing-plan.md` from
`dev/templates/testing-plan.md`.

For each acceptance and security test, fill the **DEC column** with the decision that
shaped it (if any), so a changed decision points to the tests to revisit.

Then update `traceability-matrix.md`: the Tier column, and each test on its row's Test
column.

Follow WORKFLOW.md "Document rules": front-load `## At a glance`, keep the template's
section order, reference each AC by id and matrix row — do not copy requirement text.

## Rules

- Every in-scope AC appears in the plan with exactly one tier. No AC is skipped.
- **No orphan (WORKFLOW.md "Traceability"):** every in-scope FR/AC and NFR has at least
  one test, and every in-scope DEC is consumed by at least one test or implementation
  step. Flag gaps.
- Every UC alternative with a failure condition gets a resilience test.
- Do not invent test scenarios beyond what the version spec defines.
- No ci-tier test calls a real model.
- Pre-implementation ci tests must run red — failing on a real assertion, not a syntax
  error.
- The agent drafts; it does not approve tests or close the Phase 2 gate.
