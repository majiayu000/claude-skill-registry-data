---
name: oe-hil-and-billing-triage
description: "Debug common manager/HIL + billing/deposit regressions: tasks not appearing in the panel, approve/reject button failures, billing capture loops, and “deposit paid but workflow stuck”. Produces a targeted repro + test run and points to the likely faulty layer (frontend vs backend)."
---

# oe-hil-and-billing-triage

## Fast signal: run the dedicated approve path tests

- `pytest backend/tests/agents/test_manager_approve_path.py -v`
- `pytest tests/specs/gatekeeping/test_hil_gates.py -v`

## If “Approve” fails (500 or missing attribute)

1. Confirm the handler symbol exists and is exported from the canonical step module.
2. Confirm any deprecated wrapper modules re-export the symbol used by `backend/workflow_email.py`.
3. Use `docs/guides/TEAM_GUIDE.md` (“HIL Approve Button Fails - Missing Export”) as the exact checklist.

## If HIL tasks don’t appear in the frontend “Manager Tasks” panel

1. Confirm the task payload uses the same `thread_id` as the frontend session id.
2. Confirm the frontend is not appending the API response directly into chat (bypassing task rendering).
3. Use `docs/guides/TEAM_GUIDE.md` (“HIL Task Not Appearing in Tasks Panel After Deposit Payment”) for known root causes and files:
   - `atelier-ai-frontend/app/page.tsx`
   - `backend/workflows/steps/step1_intake/trigger/step1_handler.py`

## If billing/deposit flow is stuck (accept → billing → deposit → HIL)

1. Re-test in UI with a fresh session (reset client / new email) to avoid stale session artifacts.
2. Verify the gate checks use fresh deposit status (reload from DB for deposit; in-memory for billing):
   - `backend/workflows/common/confirmation_gate.py`
3. Use `docs/guides/TEAM_GUIDE.md` (“Frontend Billing Capture Intermittent Failure”) for the suspected frontend/backend boundary issue and involved files:
   - `backend/api/routes/messages.py`
   - `backend/api/routes/events.py`
