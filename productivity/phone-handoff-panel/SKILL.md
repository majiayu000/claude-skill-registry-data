---
name: phone-handoff-panel
description: A device handoff panel for opening your phone, jump-starting a task, and keeping the Mac in the loop.
---

# Phone Handoff Panel

Use this skill when the user wants a polished macOS surface for A device handoff panel for opening your phone, jump-starting a task, and keeping the Mac in the loop.

## Presentation

- Make the surface feel like a premium Apple utility.
- Lead with one calm summary line and one clear action.
- Keep the visual language restrained, dark, and readable at a glance.

## Build shape

- Prefer a menu-bar popover or compact status-item panel.
- Show the primary state first, then the useful detail lines.
- Puts the phone-centric actions behind a quick Mac surface.
- Keeps a compact link between the desk and the device in your pocket.
- Feels more like a coordination tool than a gadget dashboard.

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
