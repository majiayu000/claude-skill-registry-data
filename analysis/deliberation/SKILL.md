---
name: deliberation
description: Structured deliberation support for decisions worth sitting with — ethical questions, architecture choices, trade-offs, decisions where the user wants clarity rather than a handed-down conclusion. Use when a question deserves genuine discernment; may involve clearness, discernment, or gathered depending on the situation.
---

# Deliberation

## Overview

Decision-making through deliberation — seeking unity through discernment rather than consensus through debate.

*This approach draws on Quaker business practice, adapted for AI-assisted decision-making.*

**Core insight:** Some decisions deserve more than quick answers. These skills provide structured approaches for genuine discernment.

## The Three Skills

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `deliberation:discernment` | Internal voices seeking clarity | Weighty questions, ethical decisions, trade-offs, multiple valid approaches |
| `deliberation:clearness` | Multi-agent committee with parallel deep work | Code reviews, architecture decisions, research needing distributed depth |
| `deliberation:gathered` | User participates alongside agent voices | User has stake/perspective, wants to discern together rather than receive advice |

## Routing Logic

```dot
digraph deliberation_routing {
    "Question received" [shape=box];
    "User has stake/perspective?" [shape=diamond];
    "Needs parallel deep analysis?" [shape=diamond];
    "Weighty question?" [shape=diamond];
    "deliberation:gathered" [shape=box, style=filled];
    "deliberation:clearness" [shape=box, style=filled];
    "deliberation:discernment" [shape=box, style=filled];
    "Answer directly" [shape=box];

    "Question received" -> "User has stake/perspective?";
    "User has stake/perspective?" -> "deliberation:gathered" [label="yes"];
    "User has stake/perspective?" -> "Needs parallel deep analysis?" [label="no"];
    "Needs parallel deep analysis?" -> "deliberation:clearness" [label="yes"];
    "Needs parallel deep analysis?" -> "Weighty question?" [label="no"];
    "Weighty question?" -> "deliberation:discernment" [label="yes"];
    "Weighty question?" -> "Answer directly" [label="no"];
}
```

## Signals for Each Skill

**Use `deliberation:gathered` when:**
- "I've been thinking about this for weeks"
- "I'm torn between..."
- "I think X, but..."
- "I don't just want your opinion"
- User expresses their own position in the question

**Use `deliberation:clearness` when:**
- Complex code review touching multiple concerns
- Architecture decision with many dimensions
- Research requiring deep exploration of multiple options
- Task where you'd write a very long response covering many angles shallowly

**Use `deliberation:discernment` when:**
- Ethical weight or potential for harm
- Multiple valid approaches exist
- Significant trade-offs
- You'd naturally want to say "it depends"

## Shared Principles

All three skills share these principles:

| Principle | Meaning |
|-----------|---------|
| **Sense of the meeting** | Clerk discerns where unity lies - not counting votes |
| **Speaking once** | Each perspective speaks once, then listens |
| **Silence** | Pausing between voices lets insights emerge |
| **Standing aside** | "I disagree but won't block" - honest without preventing |
| **Blocking** | Rare - only for violations of core principles |
| **Way opens** | Recognizing when clarity emerges vs. forcing decision |

## Shared Resources

- `skills/shared/principles.md` - Core principles
- `skills/shared/vocabulary.md` - Shared terminology
- `skills/shared/clerk-patterns.md` - Synthesis patterns for clerk role
