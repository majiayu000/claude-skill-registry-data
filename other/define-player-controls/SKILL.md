---
name: define-player-controls
description: "Use when mapping player actions to input devices (KBM, Xbox, PS, Touch) — need an Action → Input device matrix for a game with defined gameplay loop and rules."
---

## 1. Overview

Extracts player actions from the gameplay loop and maps them to abstract input definitions before generating hardware-specific bindings. Core principle: define abstract actions first, then assign devices — never start with buttons.

## 2. Core Pattern: Extract → Confirm → Map

**CRITICAL**: Conduct full interview with user via `question` tool BEFORE generating any spec. Ask ONE question per turn. Wait for answer before proceeding.

1. Read `game_loop.md` and `raw_rules.md`
2. Extract player actions → `question` tool → **STOP**
3. Select input devices/platforms → `question` tool → **STOP**
4. Present final mapping matrix → `question` tool → **STOP**
5. Generate `input_mapping.md`

| Phase | Focus | Result |
|-------|-------|--------|
| Analyze & Extract | Player-triggerable actions only (movement, combat) | Categorized action list |
| User Confirmation | Explicit approval of action list | Verified intention set |
| Device Mapping | Industry-standard mappings (KBM, Controller) | Finalized matrix |

## 3. When to Use

Use when:
- Starting a new project and `input_mapping.md` doesn't exist yet.
- You have `game_loop.md` and `raw_rules.md` and need to extract player actions into an input mapping.
- You want industry-standard control mappings before generating hardware bindings.

Do not use when:
- `input_mapping.md` already exists and you're only extending it — use `core/apply-input-bindings` instead.
- The gameplay loop and rules haven't been defined yet.

## 4. Interaction Protocol

**Every step MUST use `question` tool. Present abstract actions, not hardware buttons.**

- **One Question Per Turn (MANDATORY)**: After `question()`, response is COMPLETE. Wait for answer before next question.
- **[Missing Spec]**: "Cannot extract actions without `game_loop.md` and `raw_rules.md`. Define them first."
- **[Action Bloat]**: ">15 actions extracted. Combine or categorize more strictly?"

## 4. Quality Gates - STOP
- **Hardware Dependency**: Map abstract action list before assigning hardware buttons
- **Environmental Noise**: Include only player-triggerable actions from input mapping
- **Action Bloat**: Group similar mechanics into single abstract inputs instead of individual mappings
- **Question Batching**: One question per turn only

## 5. Execution Command
`/define-player-controls`