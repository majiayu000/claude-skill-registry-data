---
name: icaire-programme-lead-track-initiatives
description: Convert messy ICAIRE updates into initiative status records with owners, milestones, risks, dependencies, blockers, and next actions. Use when building or refreshing trackers, milestone updates, risk lists, blocker lists, or next-action registers.
---

# ICAIRE Programme Lead: Track Initiatives

Use this skill to turn unstructured ICAIRE updates into tracker-ready initiative
records that can drive follow-up.

## Contract

- Preserve the source distinction between confirmed updates, inferred status,
  and missing details.
- Use BigBrain or the ICAIRE MCP connector for ICAIRE initiative, person,
  meeting, and project context when the user has not supplied enough source
  material.
- Produce records that are operationally useful: each row should make ownership,
  status, dates, dependencies, blockers, and next actions explicit where known.
- Normalize language without changing the underlying meaning of the update.
- Surface duplicate, conflicting, or stale updates instead of silently merging
  them.

## Workflow

1. Identify the tracker format the user needs: table rows, milestone updates,
   risk and blocker list, or next-action register.
2. Gather supplied updates and retrieve current ICAIRE context if initiative
   names, owners, or prior status are unclear.
3. Extract each initiative or workstream and record its owner, current status,
   milestones, due dates, dependencies, risks, blockers, decisions, and next
   actions.
4. Normalize status into a small, explicit set such as `On track`, `At risk`,
   `Blocked`, `Done`, or `Unknown`, unless the user provided another scheme.
5. Add confidence notes where a field is inferred or unsupported.
6. List unresolved questions and follow-up asks needed to make the tracker
   complete.
7. Check that every owner, date, and status came from the source material or
   retrieved ICAIRE context.

## Guardrails

- Do not invent owners, deadlines, milestones, or status colors.
- Do not collapse risks and blockers into generic "needs follow-up" text.
- Do not hide missing dependencies; leave blanks or mark `Unknown` with a
  follow-up question.
- Do not use a broad persona response. Produce concrete tracker artifacts.
- Do not update durable memory unless the user explicitly asks for ingestion or
  persistence.

## Output Expectations

Return the requested tracking artifact. Common fields include:

- initiative or workstream
- owner
- current status
- latest update
- milestone or deliverable
- due date or reporting period
- risks
- blockers
- dependencies
- next action
- follow-up question or missing info
- source or confidence note
