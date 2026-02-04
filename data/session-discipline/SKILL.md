---
name: session-discipline
description: Enforce session-first workflow (plan → implement → verify → document). Use whenever starting non-trivial work, debugging >15 minutes, or doing cross-cutting changes.
---

# Session Discipline

## Scope

- Ensure every non-trivial task has a session folder under `docs/sessions/`
- Keep evidence (commands/tests) and outcomes discoverable
- Reduce “handover friction” by making every action resumable from docs

## Inputs

- Desired session slug (short, descriptive)
- Session type/category and objective one-liner

## Procedure

1. Create a session directory with the official CLI.
2. Fill in `PLAN.md` (objective, done-when, change set, risks, tests).
3. Log commands + findings in `WORKING_NOTES.md`.
4. Summarize outcomes + follow-ups with named owners.

## Validation

- Confirm session appears in `docs/sessions/SESSIONS_HUB.md`.
- Ensure `FOLLOW_UPS.md` has owners if anything is deferred.

## Escalation / Research request

If you need deeper background and existing docs aren’t sufficient:

- Add a follow-up: “Request research agent to expand Skill <name>”
- Include: expected triggers, target files, and what validation should exist

## References

- Session-first requirement: `AGENTS.md`
- docs-memory lessons: `docs/agi/LESSONS.md`
