---
name: plan
description: >
  Entry point for all new work. Orchestrates the full agent pipeline:
  architect (Opus) designs spec+todo, tdd-developer (Sonnet) implements
  via TDD, qa (Opus) hunts spec/impl gaps, reviewer (Sonnet) reviews code.
  Triggers on: plan, new feature, start work, build feature.
disable-model-invocation: true
---

## Pipeline: /plan <description or ticket ID>

```
architect (Opus) → spec.md + todo.md (atomic steps)
  ↓ per step:
tdd-developer (Sonnet) → RED→GREEN→REFACTOR → commit
qa (Opus) → adversarial test + spec-gap & security hunt
reviewer (Sonnet) → present findings → user triages
  ↓ max 3 fix loops, then next step
```

### Usage
1. `/plan <description>` → architect creates spec + todo
2. Approve plan, then: `Use tdd-developer on Step 1 of <todo>.md`
3. After each step: `Use qa to verify` → `Use reviewer to review`
4. Triage: [F]ix / [T]ech debt / [I]gnore → next step
