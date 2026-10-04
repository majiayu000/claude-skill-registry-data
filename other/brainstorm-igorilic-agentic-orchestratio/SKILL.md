---
name: brainstorm
description: >
  Iterative spec elicitation for vague ideas. Asks one question at a
  time to develop a thorough, step-by-step spec. Use BEFORE /plan when
  the idea is too fuzzy to hand to the architect. Pairs with explorer
  if the brainstorm leads to wanting to prototype.
  Triggers on: brainstorm, fuzzy idea, help me think, vague idea.
disable-model-invocation: true
---

## /brainstorm <idea>

Use when you have an idea but not enough clarity to write a spec.
Brainstorm asks one question at a time to converge on a structured
spec — then hands off to either `/plan` (to ship) or `/explore` (to
prototype).

```
/brainstorm <idea>
  ↓
one-question-at-a-time elicitation
  ↓
docs/context/specs/<id>-brainstorm.md  ← captured ideas
  ↓
either:
  → /plan <id>   (production track)
  → /explore <id> (exploration track)
```

### Workflow
1. Restate the idea back in your own words. Confirm.
2. Ask ONE question at a time. Build context iteratively.
3. Capture decisions in `docs/context/specs/<id>-brainstorm.md`.
4. When the shape is clear, recommend a track:
   - **Production-ready idea** → `/plan` (spec → todo → TDD)
   - **Needs prototyping first** → `/explore` (spike under spikes/)
   - **Still too fuzzy** → keep brainstorming or shelve

### Rules
- ONE question per turn. No multi-part questions.
- Don't propose solutions until the problem is clear.
- Don't write code. Brainstorm is text-only.
- If the user says "just build it", redirect to `/plan` or `/explore`.
