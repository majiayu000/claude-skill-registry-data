---
name: to-issues
description: Break a plan/PRD into independent vertical-slice Beads issues with explicit dependencies.
---

# to-issues

Convert a plan, PRD, or feature brief into small, independently executable Beads tasks.

## When to use

- User asks to break work into tickets/issues.
- You have a PRD/plan and need execution-ready slices.

## Process

### 1) Gather source context

Use available material first:

- Conversation context
- PRD/plan text
- Existing bead (`bd show <id>`)
- Relevant codebase context

If user provides an external issue/URL, map it into local context before decomposition.

### 2) Draft tracer-bullet vertical slices

Each slice must be an end-to-end path through relevant layers (contract, logic, integration, verification), not a single-layer chunk.

Rules:

- Demoable/verifiable on its own
- Prefer many thin slices over few large slices
- Minimize cross-slice coupling
- Mark slices as:
  - `AFK`: can execute without user intervention
  - `HITL`: requires human decision/review checkpoint

### 3) Review slice plan with user

Present a numbered list with:

- Title
- Type (`AFK`/`HITL`)
- Blocked by (if any)
- User stories covered (if source has stories)

Refine until approved.

### 4) Create Beads issues

Create issues in dependency order so blockers exist first.

Use this issue body format:

<issue-template>
## What to build
Concise vertical-slice behavior description.

## Acceptance criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Blocked by
- None - can start immediately
or
- <bead-id>

## Notes
- Type: AFK/HITL
- Risks or assumptions
</issue-template>

Commands:

```bash
bd create --type task --title "<slice title>" --description "<template markdown>" --priority 2 --repo .
bd dep add <slice-id> --blocks <blocked-id>
```

If slices derive from a parent PRD/feature, attach children:

```bash
bd create --type task --parent <parent-id> --title "<slice title>" --description "<template markdown>" --priority 2 --repo .
```

### 5) Validate and report

- Verify dependency graph (`bd children <parent-id>` and/or `bd graph`)
- Confirm no orphaned critical-path work
- Add `worklog:` comment to parent summarizing decomposition decisions
