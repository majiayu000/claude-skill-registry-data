---
name: session-arcade
description: A launch-night helper for game sessions, cloud gaming, and quick console handoffs.
---

# Session Arcade

Use this skill when the user wants a polished macOS surface for game sessions, cloud gaming, or quick console handoffs.

## Presentation

- Make the surface feel like a premium Apple utility.
- Lead with one calm summary line and one clear action.
- Keep the visual language restrained, dark, and readable at a glance.

## Build shape

- Prefer a menu-bar popover or compact status-item panel.
- Show the primary state first, then the useful detail lines.
- Keeps the next game or session within a few clicks.
- Makes it easier to move from launcher to play mode.
- Feels like a fun utility instead of a generic gaming dashboard.

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
