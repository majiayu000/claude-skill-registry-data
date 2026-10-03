---
name: focus-runway
description: A quiet focus launcher that trims context switching and starts the next working block cleanly.
---

# Focus Runway

Use this skill when the user wants a polished macOS surface for starting the next work block with less setup and less context switching.

## Presentation

- Make the surface feel like a premium Apple utility.
- Lead with one calm summary line and one clear action.
- Keep the visual language restrained, dark, and readable at a glance.

## Build shape

- Prefer a menu-bar popover or compact status-item panel.
- Show the primary state first, then the useful detail lines.
- Starts the next work block with less setup and fewer interruptions.
- Keeps just enough context visible to begin quickly.
- Prefers one calm action over a stack of settings.

## Guardrails

- Do not invent unsupported metrics or background services.
- Keep the app simple enough to feel native on macOS.
- Use one primary action and a small set of supporting actions.

## Prototype

- SwiftUI starter files live in `prototype/`.
- The prototype should stay menu-bar first and easy to transplant into a real macOS target.

## When extending

- Add more depth only when it improves the single workflow the skill is meant to solve.
- If the skill grows, keep the menu-bar path short and the detail panel readable.
