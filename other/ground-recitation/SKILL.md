---
name: ground-recitation
description: Anchor yourself. Prevent context drift.
---

# Skill: Recitation

> "Constantly rewriting todo lists pushes the global plan into recent attention span." — Manus

## The Standard

- **Rewrite**: Goal, Focus, Scratchpad -- current state, not history.
- **Prune**: Remove failures when lesson internalized.
- **Reset**: Blank the file when starting a new goal.

## The Check

Ask yourself:
- Does Goal still match what I'm doing?
- Is Focus pointing to the right domain/files?
- Are stale Failures cluttering context?
- Is Progress synced with blueprint's Current task?

## How to Update

| Section     | Strategy                                       |
|-------------|------------------------------------------------|
| Goal        | Rewrite when objective changes                 |
| Constraints | Add/remove as decisions are made               |
| Focus       | Rewrite each session                           |
| Progress    | Pointer to blueprint + active task             |
| Failures    | Append new. Remove when internalized.          |
| Scratchpad  | Clear freely. Temporary.                       |

## Progress Section

Progress is a **pointer**, not a list. The list lives in `blueprint.md`.

```markdown
## Progress

See `blueprint.md` for task tracking.

Currently: [active task description]
```

Do not duplicate task checkboxes here. The blueprint is the plan.

## When to Blank

Reset to template when:
- Starting a **new goal**
- Goal is **complete**
- Context is **stale**

## Artifact Hierarchy

Memory has layers. Each artifact serves a distinct purpose.

**Every one of them is branch memory, and branch memory is a directory on one machine.** Most
repositories ignore it, this one included. Nothing here is committed, so nothing here outlives the
laptop, the account or the checkout.

| Artifact            | Lasts until       | Purpose        | When                     |
|---------------------|-------------------|----------------|--------------------------|
| `working.md`        | the session ends  | Cognitive RAM  | Always active            |
| `blueprint.md`      | the goal ends     | Task tracking  | Multi-step work          |
| `spec.md`           | the goal ends     | Requirements   | New features             |
| `adr/*.md`          | the machine goes  | Decisions      | Architecture choices     |
| `handoffs/*.md`     | the handoff lands | State transfer | Manual: `/handoff`       |
| `observations/*.md` | the machine goes  | Learnings      | Manual: `/observe`       |

**This table said Permanent for two of those rows.** It meant *the longest-lived thing here*, and a
reader took it for durable. Five files sat in them on one laptop, on branches long merged, with
nothing in any tree pointing at one.

### Clarifying Overlaps

**Failures (working.md) vs Observations**:
- `Failures` = temporary. Remove when lesson internalized.
- `observations/` = the last thing here to go. **Still not durable.**

> Rule: If a failure taught you something worth remembering, write it where it survives. An
> observation here is a draft of that, never the home.

**Where it survives is not this skill's call.** A repository states it, and `craft-observation`
says what to weigh. Don't wait to be asked — but a note nobody can read later was not a learning.

## The File

`working.md` in branch memory. See `ground-topic` for path.
