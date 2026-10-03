---
name: replay-relay
description: A menu-bar share lane for turning game clips, screenshots, and quick notes into send-ready handoffs without Finder hopping.
---

# Replay Relay

Use this skill when the user wants a polished macOS surface built around this workflow:

- A menu-bar share lane for turning game clips, screenshots, and quick notes into send-ready handoffs without Finder hopping.

## Presentation

- Make the surface feel like a premium Apple utility.
- Lead with one calm summary line and one clear action.
- Keep the visual language restrained, dark, and readable at a glance.

## Build shape

- Prefer a menu-bar popover or compact status-item panel.
- Show the primary state first, then the useful detail lines.
- Stages the latest screenshot or a dropped clip with one note field and one destination choice.
- Keeps rename, caption, copy-path, and reveal actions close to the menu bar so sharing starts without a Finder cleanup pass.
- Focuses on the send-ready handoff instead of becoming another media library or editor.

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
