---
name: post-run-debrief
description: Converts telemetry and user notes into a structured reflection, confidence score, and next-step guidance.
metadata:
  short-description: Post-run reflection with confidence scoring and actionable guidance.
---

## When Codex should use it
- Immediately after run save to prompt reflection.
- When user asks for a recap or confidence check.

## Invocation guidance
1. Provide `RecentRunTelemetry`, derived metrics, and user notes.
2. Generate reflection bullets, confidence (0–1), and next-step guidance linked to the plan.
3. Output must include optional `SafetyFlag[]` if pain/abnormal HR reported.

## Input schema
See `references/input-schema.json`.

## Output schema
See `references/output-schema.json`.

## Integration points
- UI: Post-run modal and chat thread insertion.
- Storage: Save alongside run insight in Dexie (`v0/lib/db.ts`).
- Telemetry: Emit `ai_insight_created`.

## Safety & guardrails
- If user notes include pain/dizziness → advise stopping further activity and consulting a professional.
- Keep debrief ≤140 words, supportive tone.
- Default to conservative next-step if data incomplete.

## Telemetry
- Emit `ai_skill_invoked`, `ai_insight_created`, and `ai_safety_flag_raised` when applicable.
