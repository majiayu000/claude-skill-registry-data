---
name: ground-interview
description: Spec refinement via AskUserQuestion. Extract requirements before implementation.
---

# Skill: Interview

> "The spec you don't write is the bug you will ship."

## When

Before implementing any feature that involves:
- Multiple files or domains
- UI/UX decisions
- Architectural choices
- Unclear requirements

## Dynamic Cognitive Friction

> Match friction to stakes. Flow for the trivial. Rigor for the irreversible.

| Criticality | Reversibility | Depth                  | Examples                              |
|-------------|---------------|------------------------|---------------------------------------|
| Low         | High          | **Minimal** (2-5 Qs)  | Rename, add field, config change      |
| Medium      | Medium        | **Focused** (5-15 Qs) | New endpoint, refactor module         |
| High        | Low           | **Thorough** (15-40+) | Auth system, payment flow, migration  |

## The Protocol

1. **Read** the minimal spec (spec.md, task description, or user prompt)
2. **Assess criticality** — what's the blast radius? How reversible?
3. **Interview** using `AskUserQuestion` tool:
   - Technical implementation questions
   - UI & UX questions
   - Concerns and edge cases
   - Tradeoffs and alternatives
4. **Questions must NOT be obvious** - dig into the non-trivial
5. **Scale depth to criticality** — use the friction table above
6. **Write** the detailed spec to file

## Question Categories

| Category       | Example Questions                             |
|----------------|-----------------------------------------------|
| **Technical**  | "Should this use events or direct calls?"     |
| **UI/UX**      | "How should validation errors appear?"        |
| **Edge Cases** | "What happens when X is null?"                |
| **Tradeoffs**  | "Performance vs simplicity - which priority?" |
| **Scope**      | "Is Y in scope for this feature?"             |

## The Anti-Patterns

- **Assuming**: Making decisions without asking
- **Obvious questions**: "Do you want tests?" (yes, obviously)
- **Rushing**: 5 questions is not enough for a high-criticality feature
- **Alarm fatigue**: 40 questions for a config change. Match depth to stakes.
- **Implementing without spec**: Code before clarity

## The Output

Write to `$CLAUDE_MEMORY_DIR/spec.md`:
- High-level objective
- Mid-level objectives
- Implementation notes
- Low-level tasks
- Answered questions log

Then: NEW SESSION to execute.
