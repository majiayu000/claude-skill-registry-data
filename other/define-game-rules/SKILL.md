---
name: define-game-rules
description: "Use when defining game rules and event chains — when player actions need explicit WHEN/IF/THEN consequences, edge cases, and failure conditions."
---

## 1. Overview

Defines game rules as quantitative WHEN/IF/THEN chains — capturing triggers, conditions, consequences, and edge cases in an event-driven format. Core principle: every rule must be measurable; vague language is a bug.

## 2. Output Artifact
- **Target**: `{TARGET_FOLDER}/docs/raw_rules.md`
- **Format**: Quantitative, event-driven `WHEN [Trigger] -> IF [Condition] -> THEN [Consequence]` chains.

## 3. Core Pattern: Rule Atomization & Audit

**CRITICAL**: Conduct full interview via `question` tool BEFORE generating any spec. Ask ONE question per turn. Wait for answer before proceeding.

1. Read `game_loop.md` for context
2. Ask trigger types/conditions → `question` tool → **STOP**
3. Ask consequences/edge cases → `question` tool → **STOP**
4. Present rule summary → `question` tool → **STOP**
5. Generate `raw_rules.md`

| Phase | Focus | Result |
|-------|-------|--------|
| Causality Mapping | Micro/Macro loop temporal framework | Contextualized triggers |
| Rule Atomization | `WHEN → IF → THEN` patterns | Formal rules |
| Edge Case Audit | Exploits, stuck states, dead-ends | Logic verification |

**When to use**: Starting a new project where raw_rules.md does not yet exist, or for initial rule definition. Use bootstrap-game-project for refinement of existing specs; use define-game-systems or define-player-controls for those respective tasks.

## 4. Interaction Protocol

**Every phase MUST use `question` tool. Present rules in WHEN/IF/THEN format.**

- **One Question Per Turn (MANDATORY)**: After `question()`, response is COMPLETE. Wait for answer.
- **[Infinite Loop]**: No failure/end state → "Every loop requires stakes. What's the failure trigger or resource depletion mechanic?"
- **[Narrative]**: Story-driven descriptions → "Establishing loops now. What's the repeating gameplay loop?"

## 5. Quality Gates - STOP
- **Quantifiable Rules**: Use measurable conditions for all rules ("Player speed > 10" instead of "Player moves fast")
- **Bounded Loops**: Define clear exit conditions for every loop
- **Mechanical Triggers**: Use mechanical triggers as rule definitions
- **Question Batching**: One question per turn only