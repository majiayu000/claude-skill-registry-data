---
name: oe-test-matrix-navigator
description: Maps a code change or bug symptom to the smallest high-signal test subset. Use when deciding what tests to run (DET_/FLOW_/REG_), when a regression guard mentions a test ID, or when you need a minimal repro that matches tests/TEST_MATRIX_detection_and_flow.md.
---

# oe-test-matrix-navigator

## Decide the class of change (pick one)

1. **Detection change** (classification/heuristics/routing decisions)
   - Target: `DET_*` tests
2. **Flow change** (Step progression 1–7, detours, gatekeeping, state machine)
   - Target: `FLOW_*` tests + relevant step/unit tests
3. **Regression/bug fix** (TEAM_GUIDE item or previously fixed behavior)
   - Target: `REG_*` tests (or add one)

## Find the right test IDs fast

1. Search the matrix for your symptom/keyword (room choice, billing, deposit, site visit, manager, Q&A, detour):
   - `rg -n "<keyword>" tests/TEST_MATRIX_detection_and_flow.md`

2. If the matrix references a `DET_*` / `FLOW_*` / `REG_*` id, use it as the primary handle in the PR description.

3. Cross-check where the actual tests live and whether they’re currently flaky/failing:
   - `tests/TEST_INVENTORY.md`

## Run the minimum test subset

1. Always run the fast baseline first if you’re unsure:
   - `./scripts/test-smoke.sh`

2. Then run the narrowest relevant suite:
   - **Q&A / detection:** `pytest tests/specs/nlu/ -q` and `pytest tests/specs/date/ -q` (as applicable)
   - **Step 3 room availability:** `pytest tests/specs/room/ -q`
   - **Step 4/5 offer + negotiation:** `pytest tests/specs/products_offer/ -q` and `pytest tests/specs/gatekeeping/ -q`
   - **Detours/change propagation:** `pytest tests/specs/detours/ -q` and `pytest tests/specs/dag/ -q`
   - **Manager/HIL path:** `pytest backend/tests/agents/test_manager_approve_path.py -q`
   - **Prompt-injection defenses:** `pytest backend/tests/regression/test_security_prompt_injection.py -q`

## When adding a missing test ID

- Prefer updating the matrix with a new `REG_*` row and adding the corresponding test near the closest existing file (keep it searchable by the ID).
