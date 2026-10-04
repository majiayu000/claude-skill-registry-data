---
name: analyze
description: Use this skill after Phase 1 Plan to create or intake requirements for a task. Produces requirements with stable IDs (REQ-001, REQ-002, ...), validates each requirement against the project's scope statement, and — critically — halts and asks for UX designs and brand guidelines whenever the work touches a frontend or user interface. Trigger whenever a plan has been approved and requirements are not yet written, or when the user asks to "gather requirements", "write user stories", or "define acceptance criteria". Runs before Design.
next_suggestions:
  - when: analyze_gate_signed
    suggest: "run /design to produce the architecture bundle and test cases"
  - when: pending_signoff_for_current_user
    suggest: "write your sign-off at sign-offs/<REQ-ID>-<role>.md, then /design when all roles are covered"
---

# Analyze (Phase 2)

Turn a task into structured, testable requirements.

## Prerequisite

The plan gate must exist: `.claude/sdlc/gates/plan-<task-slug>.md`. If it does not, tell the human to run `/plan` first.

## Step 1 — Detect frontend involvement

Before writing requirements, determine whether the task touches a user interface. Check:

- The plan's in-scope files for UI frameworks (React, Vue, Angular, HTML templates, mobile views)
- Keywords in the plan: "screen", "page", "form", "button", "UI", "UX", "design"

If **yes, and no UX artifact exists** under `.claude/sdlc/architecture/ux/`:

- **Halt.** Ask the human for UX designs (Figma link, wireframes, mockups) and brand guidelines (colors, typography, spacing tokens, component library).
- Do not proceed to write requirements until a UX artifact is linked or written at `.claude/sdlc/architecture/ux/<task-slug>.md`.

This is a hard rule. Frontend without UX specs produces UI debt.

## Step 2 — Write requirements

Write to `.claude/sdlc/requirements/<task-slug>.md` using `templates/requirements.md`. Each requirement has:

- **Stable ID:** `REQ-<n>` — never renumbered once published
- **Title:** short imperative
- **Description:** what the system must do
- **Acceptance criteria:** testable, unambiguous (Given/When/Then works)
- **Priority:** must / should / could
- **Source:** ticket, CR, stakeholder, or project scope section
- **Dependencies:** other REQ IDs or external systems

Stable IDs matter: Design references them, Build validates against them, Test maps cases to them, Deploy records them, Docs traces them.

## Step 3 — Contract / scope coverage check

For each requirement, confirm it maps to a section of `.claude/sdlc/scope.md` (or the relevant contract/SOW artifact). Any unmapped requirement is a **scope question** — surface it, don't hide it. The human decides whether to expand scope or drop the requirement.

Produce a coverage table in the requirements file:

| REQ ID  | Scope section  | Status         |
|---------|----------------|----------------|
| REQ-001 | 2.1 Checkout   | ✓ mapped       |
| REQ-002 | —              | ? unmapped     |

## Step 4 — Human gate

Summarize: total REQs, mapped vs. unmapped, frontend yes/no, UX artifact status. Ask the human to confirm. Write the sign-off to `.claude/sdlc/gates/analyze-<task-slug>.md`.

## What this skill must NOT do

- Do not design architecture here (that's Phase 3).
- Do not skip the UX ask for frontend work — "we'll figure it out in build" is how UX debt accrues.
- Do not renumber REQ IDs on edits — add new ones and deprecate old ones in place.

## References

- `templates/requirements.md`
- `templates/gate.md`
- `docs/SDLC.md` Analyze

## Next step hint

After writing the gate file, pipe the `next_suggestions` conditions to `skills/_shared/next-hint.sh` and print any output:

```bash
printf '%s\n' \
  'analyze_gate_signed|run /design to produce the architecture bundle and test cases' \
  'pending_signoff_for_current_user|write your sign-off at sign-offs/<REQ-ID>-<role>.md, then /design when all roles are covered' \
  | bash skills/_shared/next-hint.sh
```

Print any output verbatim. If the script outputs nothing, add nothing.
