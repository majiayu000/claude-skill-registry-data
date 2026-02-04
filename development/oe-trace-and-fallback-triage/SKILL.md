---
name: oe-trace-and-fallback-triage
description: Debug and eliminate fallback/generic-stub replies quickly. Use when you see empty assistant replies, “Thanks for your message…” stubs, or “no specific information available” messages. Produces a minimal reproduction (test or deterministic trace) and pinpoints the fallback source + trigger.
---

# oe-trace-and-fallback-triage

## Capture the symptom precisely

1. Save the exact client-facing string that indicates fallback (copy/paste).
2. Record the entry context: current step (if known), thread/session id, and whether HIL tasks were pending.

## Turn on diagnostics (dev only)

- Set `OE_FALLBACK_DIAGNOSTICS=true` to get structured fallback reasons in responses/logs (do not enable in production).
- Ensure tracing is enabled so agents can follow the execution path:
  - `export DEBUG_TRACE=1`
  - (optional) `export DEBUG_TRACE_DIR=tmp-debug`

## Reproduce (prefer deterministic lanes)

1. Backend-only repro for intake routing:
   - `python3 scripts/manual_smoke_intake.py`

2. If the issue is Step 7 / site visit related:
   - `python3 scripts/manual_ux_scenario_I.py > /tmp/ux_site_visit_I.json`
   - `python3 scripts/validate_manual_ux_run.py /tmp/ux_site_visit_I.json --require_site_visit`

3. If the issue matches a known regression guard, run its test:
   - `tests/TEST_MATRIX_detection_and_flow.md` (search the stub string and run the matching `DET_*` / `REG_*` test)
   - `docs/guides/TEAM_GUIDE.md` (Known Issues & Fixes → “Chain of Failure” sections)

## Map the fallback source

Use the diagnostic “Source:” / “Trigger:” to jump to the correct module:
- Q&A verbalization fallback: `backend/workflows/qna/verbalizer.py`
- Q&A extraction fallback: `backend/workflows/qna/extraction.py`
- General Q&A body fallback: `backend/workflows/common/general_qna.py`
- Intent/provider fallback: `backend/workflows/llm/adapter.py`
- Workflow-level fallback reasons: `backend/workflows/common/fallback_reason.py`

## Common high-impact failure chains (check first)

- Quoted confirmations triggering General Q&A and emitting the “no specific information available” stub:
  - see `docs/guides/TEAM_GUIDE.md` (“Regression trap: quoted confirmations triggering General Q&A”)
- Event reuse routing a new inquiry into Step 7 site-visit handling and returning no drafts:
  - see `docs/guides/TEAM_GUIDE.md` (“Event reuse logic bug”)
