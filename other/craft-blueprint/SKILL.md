---
name: craft-blueprint
description: Crafting blueprints. Persistent task tracking with user confirmation.
---

# Skill: Craft Blueprint

> "A plan is a guess. A blueprint is a contract."

## When

Use blueprint when:
- Starting implementation from spec.md
- Tracking multi-task feature work
- Coordinating across sessions

## The Standard

1. **Source from Spec**: Tasks come from spec.md Low-Level Tasks. Never invent.
2. **Assess Ownership**: Apply `ground-delegation` criteria to assign Owner.
3. **User Confirms Completion**: Never mark `done` without user confirmation.
4. **Single In-Progress (self)**: One self task active. Multiple agent tasks allowed.
5. **Defer, Never Delete**: Out-of-scope tasks move to Deferred with reason.
6. **Log All Changes**: Every mutation recorded in Changes table.

## Ownership

Each task has an Owner: `self` or `agent`.

| Owner | Meaning | Status Flow |
|-------|---------|-------------|
| `self` | Architect does it | `pending` → `in-progress` → `done` |
| `agent` | Delegated to sub-agent | `pending` → `delegated` → `in-review` → `done` |

See `ground-delegation` for criteria (Bounded, Context-free, Mechanical, Verifiable).

## The Protocol

1. **Initialize**: Copy `templates/blueprint.md` to branch memory.
2. **Populate**: Extract tasks from spec.md. Assess Owner for each.
3. **Work (self)**: Mark one task `in-progress`. Sync to working.md Focus.
4. **Delegate (agent)**: Brief agent per `ground-delegation`. Mark `delegated`.
5. **Review (agent)**: When agent completes, mark `in-review`. Verify output.
6. **Complete**: User confirms. Add date to Confirmed column. Mark `done`.
7. **Defer**: Move task to Deferred table with reason. Log in Changes.
8. **Evolve**: Any plan change logged in Changes with date and reason.

## Parallel Delegation

- Up to 3 agent tasks may run simultaneously (soft limit).
- Track in Delegated section of blueprint.
- Architect reviews all agent output before marking `done`.

## Phases

The Status section tracks where you are in the lifecycle:

| Phase              | Trigger             | Activities                            |
|--------------------|---------------------|---------------------------------------|
| **Discovery**      | Blueprint created   | Reading spec, clarifying requirements |
| **Implementation** | First task started  | Writing code, marking tasks done      |
| **Testing**        | All code tasks done | Running tests, fixing failures        |
| **Refinement**     | Tests passing       | Polish, documentation, PR prep        |

Update Phase when transitioning. Log in Changes.

## The Anti-Patterns

| Don't | Do | Why |
|-------|-----|-----|
| Mark done without asking | Request user confirmation | User owns completion |
| Multiple self in-progress | Single active self task | Focus and clarity |
| Delete inconvenient tasks | Defer with reason | Audit trail |
| Silent plan changes | Log in Changes table | Traceability |
| Invent tasks | Source from spec.md | Spec is the contract |
| Skip delegation assessment | Apply criteria to each task | Lead, don't drown |
| Auto-merge agent output | Review before commit | Quality gate |

## Real-World Examples

See [examples.md](examples.md).
