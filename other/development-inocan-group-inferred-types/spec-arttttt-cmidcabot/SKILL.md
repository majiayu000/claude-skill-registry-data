---
name: spec
description: "Create or enrich issue specification. Use when the user invokes /spec or asks to draft or update a task spec in the tracker."
---

# Spec Command

## Behavior Profile

Use the `planner` skill as the behavior profile for this command.
Treat its rules as mandatory.

Follow `CLAUDE.md`, `conventions.md`, and `ARCHITECTURE.md`.

## Task

Create new issue or enrich existing one with full specification.

## Interaction Contract

1. Always show a draft spec.
2. Wait for explicit user confirmation before creating or updating the issue.

## Algorithm

### Step 1: Parse argument

- Empty → ask "Describe the task:", wait for response
- ID-like (2-4 chars or `DCATgBot-` prefix) → enrich mode
- Otherwise → create mode, use as description

### Step 2: Research and draft

- Study relevant code and conventions
- Prepare specification draft
- Return draft without creating/updating the issue

### Step 3: Confirm

```
## Specification Draft
<draft_spec>
---
Confirm? (ok / corrections)
```

### Step 4: Apply

- If "ok": create/update issue via `beads`
- If corrections: update draft and then create/update

### Step 5: Report

- Create: "Created: `<id>` — <title>"
- Enrich: "Updated: `<id>` — <title>"

## Issue Description Format

```markdown
## Context
[Why this matters — 2-3 sentences]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Scope
[What IS included]

## Out of Scope
[What is NOT included]

## Technical Notes
[Optional — implementation hints]
```

## Important

- Never skip confirmation
- Resolve all questions before creating issues
- Use the `beads` skill for tracker operations
