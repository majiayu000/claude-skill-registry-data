---
name: phase-validator
description: "Use when running build verification and QA gates after pipeline execution. Triggers: 'build verification', 'QA gate', 'smoke tests', 'post-build validation'."
---

## 1. Overview

Final validation gates for build pipeline: Phase 6 (build verification) and Phase 7 (QA).

## 2. Quick Reference

| Phase | Pass Criteria | Verdict Options |
|-------|---------------|-----------------|
| 6: Build verification | No compilation errors; binary runs ≥5s without crash | SUCCESS / FAILURE |
| 7: QA | Smoke tests pass for EventBus/ECS/State Machine/Input Handler; no systematic failures | SUCCESS / PARTIAL / FAILURE |

Both phases mandatory. Max 2 auto-fix retries per phase.

## 3. Execution Flow

| Phase | Focus | Method |
|-------|-------|--------|
| 6 | Build verification | Detect build system, run build, fix (max 2 retries) or abort |
| 7 | QA | Smoke tests, runtime testing, auto-fix (max 2 retries) |

## 3. Phase 6: Build Verification (MANDATORY)

Detect build system, run build, fix (max 2 retries) or abort. Run binary 5+ seconds. Verify no crash. Report: SUCCESS / FAILURE.

## 4. Phase 7: QA (MANDATORY FINAL)

* `implement-qa-automation` — smoke tests for EventBus, ECS, State Machine, Input Handler
* Runtime testing (Playwright/binary), auto-fix (max 2 retries), spec validation
* Report: SUCCESS / PARTIAL / FAILURE

## Golden Rules

* **MANDATORY**: Both phases are mandatory.
* **Auto-fix limit**: Max 2 retries per phase.
* **Report**: Always report SUCCESS / FAILURE / PARTIAL.
* Delegation rules inherited from pipeline-orchestrator documentation.

## 5. Red Flags

* **Build Success**: Compilation completes without errors; binary runs ≥5 seconds without crash
* **QA Pass Rate**: Smoke tests for EventBus, ECS, State Machine, Input Handler complete without systematic failures
* **Spec-to-Code Alignment**: Implementation matches specifications; mismatches trigger review before proceeding
* **Stable Runtime**: Application responds to inputs, state machine transitions correctly, no performance degradation

## 6. Final Integrity Audit
- [ ] Phase 6 build verification completed with SUCCESS (no compilation errors, binary runs ≥5 seconds without crash)
- [ ] Phase 7 QA smoke tests executed for EventBus, ECS, State Machine, Input Handler — no systematic failures
- [ ] Final report issued with clear verdict: SUCCESS / PARTIAL / FAILURE

## 7. Execution Command

`/phase-validator`
