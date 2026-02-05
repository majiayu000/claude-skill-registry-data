---
name: oe-architectural-guardrails
description: Essential architectural rules, pipeline order, and bug prevention checklists. MUST be consulted before modifying routing, state, or detection logic.
---

## When to use
- **Before** modifying `workflow_email.py`, `pre_route.py`, `router.py`, or any `stepX_handler.py`.
- **Before** implementing new detection logic or regex.
- **When** debugging "lost messages", "wrong step" bugs, or "ignored inputs".
- **When** adding new steps or gates to the workflow.

## Core Reference
**READ THIS FILE FIRST:** `docs/architecture/MASTER_ARCHITECTURE_SHEET.md`

## Quick Checklist (The "Don't Break It" List)

1.  **Pipeline Order:** Remember that `Step 1` runs *before* `Pre-Route`. Changes in Step 1 affect what Pre-Route sees. Capture runs *before* OOC.
2.  **Interference:** If adding a keyword check, did you check `unified_detection` first? Don't let a regex override an LLM signal.
3.  **Idempotency:** Is your "confirm" logic safe if the user says "Yes" to an *already verified* gate? (It should be a NO-OP, not a detour).
4.  **Anchoring:** If extracting a date, are you sure it's the *Event Date* and not a payment/quote date? Use `detect_change_type_enhanced`.
5.  **Hybrid Handling:** If the user sends "Confirm + Question", does your handler answer the question? Don't drop the QnA part.
6.  **Hard Facts:** Did you verify that LLM verbalization includes all units and prices exactly as in the data?

## Critical Files
- `docs/architecture/MASTER_ARCHITECTURE_SHEET.md` (The Law)
- `backend/workflows/runtime/pre_route.py` (The Gatekeeper)
- `backend/workflows/steps/step1_intake/trigger/step1_handler.py` (The Intake & Change Detector)
- `backend/ux/universal_verbalizer.py` (The Voice)

## Common "False Friends" (Traps)
- `body` vs `body_markdown`: Use `body` for client email, `body_markdown` for internal HIL display.
- `confirm_date` intent: Often triggers OOC if used in Step 4+. Use **Gate-Aware Arbitration**.
- `event_date` vs `payment_date`: Raw regex will confuse them. Use **Normalization** and **Anchoring**.
