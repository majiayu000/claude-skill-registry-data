---
name: roblox-ui
description: "Design or review responsive Roblox interfaces across touch, keyboard, mouse, and gamepad input."
---

# Roblox UI

Read [`../../references/roblox-engineering.md`](../../references/roblox-engineering.md). Preserve the project's visual language, UI architecture, and existing input abstraction before introducing new patterns.

## Build for changing screens and inputs

- Separate authoritative game state from client presentation state. UI sends intent and renders server-confirmed state; it does not decide purchases, rewards, inventory, cooldowns, or progression.
- Prefer layouts, constraints, automatic sizing, and content-driven composition over scripts that continuously place pixels. Use scale and offset deliberately; test aspect ratio, text expansion, safe areas, and reserved touch controls.
- Bind gameplay actions, not device-specific keys. Support touch, keyboard and mouse, and gamepad through the project's current action layer; update prompts when the preferred input changes.
- Use activation events that work across input types. Define gamepad selection order, initial focus, focus restoration, modal trapping, back/cancel behavior, and a non-pointer path to every required action.
- Give touch controls sufficient reach and target size. Preserve legibility at small screens and distance viewing; allow localization and dynamic text to expand without clipping critical controls.
- Render from explicit state. Prefer event-driven updates and targeted reconciliation over rebuilding the full tree or polling every frame. Own and clean up connections, tweens, input bindings, and transient instances.
- Keep animation responsive and cosmetic. Do not delay authoritative actions behind a tween, and respect any project setting for reduced motion or disabled effects.

## Deliverable

State the UI state owner, component boundaries, action bindings, responsive layout rules, selection behavior, lifecycle cleanup, and server interaction. Verify pure state and layout helpers locally. Give the user a compact Studio matrix covering phone, tablet, desktop, and gamepad; never run that playtest through MCP.
