---
name: define-game-loop
description: "Use when defining the core gameplay cycle for a new or refocused game — micro loop, macro loop, reward mechanism, and failure state."
---

# define-game-loop

## 1. Template Binding

- **Output**: `{TARGET_FOLDER}/docs/game_loop.md`
- **Logic**: Two-stage extraction process building chronological loop spec from genre and ruleset.

## 2. Core Pattern: Two-Stage Extraction

Refine gameplay cycle from immediate actions to session-long flows.

**CRITICAL: Interview the user BEFORE generating any spec via `question` tool.**

### Mandatory Interview Steps (SEQUENTIAL — ONE AT A TIME)

**RULE: Ask ONE question group per turn. Wait for answer before proceeding.**

1. Ask about micro loop (action cycle) via `question` → **STOP**
2. Ask about reward mechanism via `question` → **STOP**
3. Ask about macro loop (full session flow) via `question` → **STOP**
4. Ask about failure state via `question` → **STOP**
5. Present summary for confirmation via `question` → **STOP**
6. Generate `game_loop.md`

| Phase | Focus | Artifact |
|---|---|---|
| **Micro Loop** | Immediate, repeatable actions (e.g., "Navigate → Scan → Eliminate") | Part of `game_loop.md` |
| **Macro Loop** | Full session: Start → Engagement → Evaluate → Resolve | Finalized `game_loop.md` |

## 3. When to Use

- **Starting** a new game project (first design skill), refining unfocused loop, validating failure state and repeatable cycle. Use bootstrap-game-project for refining existing specs; use dedicated skills for story/art/audio definition.

## 4. Quick Reference

**Output**: `{TARGET_FOLDER}/docs/game_loop.md`. **Tool**: `question` (one per turn).

Interview steps:
1. Micro loop — immediate repeatable actions (e.g., "Navigate → Scan → Eliminate")
2. Reward mechanism — how player is rewarded in the loop?
3. Macro loop — full session flow (Start → Engagement → Evaluate → Resolve)
4. Failure state — what ends or resets the loop?
5. Summary confirmation → generate spec

Every loop needs clear entry points, exit conditions, and consequences.

## 5. Interaction Protocol

Every step MUST use the `question` tool. One question per turn.

**Intercepts:**
- **[Narrative Intercept]**: Story/flavor text → "That is great narrative background, but right now we are establishing loops. What is the repeating gameplay loop while the player is interacting with that wizard?"
- **[Infinite Loop Intercept]**: No failure/end state → "Every gameplay loop requires stakes. What is the direct failure trigger or resource depletion mechanic to prevent an infinite cycle?"

## 5. Quality Gates

- **Narrative Bleed**: Use mechanical specs exclusively for game behavior (e.g., "Player HP increases by 10" instead of "The hero feels brave").
- **Missing State Changes**: Define world/player status changes for every action.
- **Circular Logic**: Ensure loops have clear entry points, exit conditions, and consequences.
- **Question Batching**: One question per turn only.

## 6. Execution Command

Command: `/define-game-loop`
