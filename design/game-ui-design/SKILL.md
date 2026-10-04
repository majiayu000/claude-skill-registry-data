---
name: game-ui-design
description: Design, implement, and review game user interfaces. Use when Codex is asked to create or improve HUDs, menus, overlays, inventory screens, ability bars, dialogue UI, controller navigation, accessibility, onboarding, game settings, UI motion, visual hierarchy, or game-specific frontend flows.
license: MIT
---

# Game UI Design

## Core Workflow

1. Identify the game genre, platform, input devices, player skill level, session length, and whether the UI is diegetic, overlay, menu-driven, or hybrid.
2. Map the player's immediate decisions before drawing screens. Prioritize the information needed for action, risk, timing, navigation, and feedback.
3. Match UI density to play context: combat and real-time play need fast recognition; management, inventory, and strategy screens can support comparison and detail.
4. Bind UI to explicit game-state owners where possible, such as health, inventory, cooldown, quest, input, or interaction components, rather than reading a large player script.
5. Design complete states, not just the default state: empty, loading, disabled, locked, selected, focused, hover, pressed, error, cooldown, low-resource, warning, success, and paused.
6. Implement controller/keyboard/mouse/touch navigation deliberately. Define focus order, wrap behavior, cancel/back behavior, and input remapping access.
7. Verify in motion and at target resolutions. Check text fit, occlusion, contrast, safe areas, scaling, localization risk, and whether the UI remains readable over gameplay.

## Interface Priorities

- HUD: expose only what changes decisions; group health, resources, objectives, minimap, ability state, and threat indicators by urgency.
- Menus: optimize repeated use, clear hierarchy, reversible actions, persistent selection state, and fast return to play.
- Inventory/equipment: support sorting, comparison, filtering, rarity, affordance, stack state, drag/drop or controller alternatives, and clear item consequences.
- Dialogue: preserve speaker identity, pacing, skip/advance rules, choice consequences, backlog access, and readable line length.
- Settings: include controls, audio, display, graphics, accessibility, language, and reset defaults where appropriate.
- Feedback: use sound, animation, color, haptics, and timing as a coherent response layer rather than decoration.

## Composition-Aware UI

- Treat HUD widgets as views over focused gameplay components: health bars read health state, cooldown UI reads ability state, prompts read interaction state, and debug overlays read movement or physics state.
- Prefer signals/events from components for changes like damage taken, resource spent, item acquired, cooldown ready, objective advanced, or input mode changed.
- Avoid making UI query unrelated owner scripts for every value. If the UI needs many unrelated values, introduce a view model, presenter, or orchestrator that prepares display state.
- Design debug UI around component boundaries so developers can inspect one capability at a time.

## Visual Direction

Keep the UI grounded in the game world and genre. Avoid generic SaaS layouts for games unless the game itself is a simulation, management, or operating-interface experience. Use iconography, materials, typography, spacing, and animation that reinforce the game tone while preserving readability.

## Deliverable Shape

For game UI work, provide:

- Target platform, inputs, and screen context
- Player decisions the UI must support
- Screen/state map
- Layout and hierarchy direction
- Interaction, focus, and controller/touch behavior
- Accessibility and localization considerations
- Implementation or review checklist

## References

- Read `references/game-ui-checklist.md` when auditing a UI, preparing a final pass, or designing a multi-screen flow.
