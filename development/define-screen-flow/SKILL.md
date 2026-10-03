---
name: define-screen-flow
description: "Use when defining application-level screen navigation hierarchy and transitions through a guided interview. Triggers: 'screen flow', 'screen navigation'."
---

# define-screen-flow

## 1. Template Binding

- **Output**: `{TARGET_FOLDER}/docs/screen_flow.md`
- **Logic**: Interview the user to build a complete directed graph of screens, transitions, and persistent layers, then emit a structured spec that UI and code builders can implement without guessing.

## 2. Core Pattern: Sequential Screen Inventory Interview

Conduct a structured, one-question-at-a-time interview to capture the full screen hierarchy. Each answer informs the next question. Only after all six phases are complete do you generate the spec.

**CRITICAL: Interview the user BEFORE generating any spec via `question` tool.**

### Mandatory Interview Steps (SEQUENTIAL — ONE AT A TIME)

**RULE: Ask ONE question group per turn. Wait for answer before proceeding.**

1. Ask about screen inventory (splash, main menu, settings, gameplay, pause, game over, credits, loading — what screens exist?) via `question` → **STOP**
2. Ask about entry point and boot sequence (which screen appears first, is there a loading/init screen before it?) via `question` → **STOP**
3. Ask about the transition map (for each screen identified, which screens can it navigate to? define all directed edges) via `question` → **STOP**
4. Ask about persistent layers (HUD, overlays, modals, or UI elements that remain visible across multiple screens) via `question` → **STOP**
5. Ask about back/escape behavior (what happens when the player presses back or escape on each screen — go to previous, pause, quit, nothing?) via `question` → **STOP**
6. Confirm summary with user → Generate `screen_flow.md`

## 3. When to Use

- **Starting** a new game project where screen navigation hasn't been defined yet
- **Refocusing** an existing project that has screens scattered across code without a documented flow
- **Triggers**: 'screen flow', 'screen navigation', 'scene transitions', 'menu flow', 'screen hierarchy', 'app flow', 'define screens', 'map screens', 'navigation design'
- **Scope boundary**: Screen navigation only — use `define-game-loop` for gameplay mechanics, `define-visual-style` for styling/layout, `define-player-controls` for input bindings

## 4. Quick Reference

**Output**: `{TARGET_FOLDER}/docs/screen_flow.md`. **Tool**: `question` (one per turn).

Interview phases:
1. Screen inventory — what screens exist?
2. Entry point and boot sequence — which screen first?
3. Transition map — for each screen, where can it navigate to?
4. Persistent layers — HUD, overlays, modals visible across screens?
5. Back/escape behavior — what happens on back/escape per screen?
6. Summary confirmation → generate spec

Every screen must be reachable and have defined back-navigation.

## 5. Interaction Protocol

| Phase | Type | Tool |
|---|---|---|
| Steps 1-5 | One question at a time | `question` |
| Step 6 | Summary confirmation | `question` |
| Final | Spec generation | File write |

**Intercepts:**

- **[Implementation Intercept]**: User starts describing how transitions are coded (e.g., "we'll use a scene manager, the transition will fade over 300ms") → "I'll note that as an implementation detail. Right now let's stay at the navigation level — which screen does this transition lead to?"
- **[Gameplay Intercept]**: User blends gameplay mechanics into screen definitions (e.g., "on the gameplay screen the player can move and shoot") → "That's gameplay behavior, which we'll capture separately. For now, I just need to know what screens the gameplay screen can navigate to — pause menu, game over, or anything else?"

## 5. Quality Gates

- Every screen must have defined back-navigation or an explicit "no back nav" statement
- Every screen must be reachable from at least one other screen via entry and exit edges
- Screen state stays separate from game state (e.g., "player is dead" triggers the game over screen; it is not itself a screen)
- One interview question per turn only — wait for user answer before proceeding
- All five interview phases complete before generating `screen_flow.md`
- Screen names clarified concretely — no vague labels like "the main thing"

## 6. Execution Command

Command: `/define-screen-flow`
