---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a `domain.md`, or recording or editing an ADR.
---

# Domain modeling

Build and sharpen the project's domain model as you design. This is the active discipline. Challenge terms, invent edge-case scenarios, and write the glossary and decisions down as soon as they settle. Reading `domain.md` for vocabulary is not this skill. Any skill can do that in one line. This skill is for changing the model, not consuming it.

## File structure

```bash
├── .farseer/
│   └── domain.md
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

Create files lazily, only when you have something to write. If no `.farseer/adr/` directory exists, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `domain.md`, say so right away. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses a vague or overloaded term, propose a precise canonical one. "You're saying 'account'. Do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships come up, test them with specific scenarios. Invent ones that probe edge cases and force the user to be precise about where one concept ends and the next begins.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, raise it. "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update domain.md inline

When a term is resolved, update `.farseer/domain.md` right there. Don't batch these up. Capture them as they happen.

Keep `.farseer/domain.md` free of implementation details. It is not a spec, a scratch pad, or a place to record implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse.** Changing your mind later would cost something real.
2. **Surprising without context.** A future reader will wonder "why did they do it this way?"
3. **A real trade-off.** There were genuine alternatives and you picked one for specific reasons.

If any of the three is missing, skip the ADR. Use the Skill tool with `architecture-decision-records` to create one only when all three hold.
