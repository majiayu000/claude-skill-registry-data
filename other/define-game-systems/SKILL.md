---
name: define-game-systems
description: "Use when selecting game systems from a menu (save, audio, shop, etc.) and priority-ranking them (P0/P1/P2) to establish MVP scope."
---

# define-game-systems

## 1. Template Binding

- **Output**: `{TARGET_FOLDER}/docs/system_roster.md`
- **Logic**: Aggregate, triage, and prioritize systems by their contribution to the core gameplay loop.

## 2. Core Pattern: Triage Workflow

**CRITICAL: Interview the user BEFORE generating any spec via `question` tool.**

### Mandatory Interview Steps (SEQUENTIAL — ONE AT A TIME)

**RULE: After each `question()` call, STOP. One question per turn.**
**Exception: Step 2 (system catalog) is the only allowed multi-option question.**

1. Read `game_loop.md` for context
2. Present full system catalog via `question` (checkbox options, grouped by category) → **STOP**
3. Ask user to assign P0/P1/P2 priorities via `question` → **STOP**
4. Present triage summary for confirmation via `question` → **STOP**
5. Generate `system_roster.md`

| Phase | Focus | Action |
| :--- | :--- | :--- |
| **System Inventory** | Collect requested systems | Baseline roster |
| **Loop Mapping** | Validate links to `game_loop.md` | Identify non-essential features |
| **MVP Triage** | Categorize P0/P1/P2 | Prioritized list |
| **Complexity Audit** | Flag high-effort/low-value | Velocity protection |

## 3. When to Use

- **Scope**: After `game_loop.md` is defined, for feature prioritization, before implementation to establish MVP scope. Use `bootstrap-game-project` for refining existing `system_roster.md`; use `define-game-rules` or `define-player-controls` for those respective tasks.

## 4. Interaction Protocol

Every step MUST use the `question` tool. One question per turn.

Split catalog across multiple questions if >20 options.

**Intercepts:**
- **[Wishlist Intercept]**: Unprioritized list → "I've noted these systems. To maintain velocity, we need to triage them into P0, P1, and P2 based on their necessity for the core loop."
- **[Scope Creep Intercept]**: Non-essential system as P0 → "Adding [System] as P0 will significantly impact our MVP timeline. Can we reclassify this as P1 or P2 to protect the core loop?"

## 5. Quality Gates

- **Prioritized Features**: All features categorized with clear P0/P1/P2 assignments.
- **Loop Alignment**: Every system links mechanically to `game_loop.md`.
- **Bounded Scope**: High-complexity systems flagged and weighed against velocity impact.
- **One Question Per Turn**: Single question at a time (except Step 2 catalog).

## 6. Execution Command

Command: `/define-game-systems`
