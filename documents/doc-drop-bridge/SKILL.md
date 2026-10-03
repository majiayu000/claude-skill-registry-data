---
name: doc-drop-bridge
description: A document packaging bridge that turns notes, markdown, and fragments into share-ready handoff files.
---

# Doc Drop Bridge

Use this skill when the user wants a polished macOS surface for A document packaging bridge that turns notes, markdown, and fragments into share-ready handoff files.

## Presentation

- Make the surface feel like a premium Apple utility.
- Lead with one calm summary line and one clear action.
- Keep the visual language restrained, dark, and readable at a glance.

## Build shape

- Prefer a menu-bar popover or compact status-item panel.
- Show the primary state first, then the useful detail lines.
- Makes it easy to wrap a working note into a shareable artifact.
- Keeps PDF, markdown, and plain-text exports close at hand.
- Focuses on fast delivery rather than a giant document suite.

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
