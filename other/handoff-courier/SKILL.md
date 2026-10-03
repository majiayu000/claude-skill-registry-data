---
name: handoff-courier
description: A polished menu-bar courier for moving files, snippets, and exports between apps without window gymnastics.
---

# Handoff Courier

Use this skill when the user wants a polished macOS surface for A polished menu-bar courier for moving files, snippets, and exports between apps without window gymnastics.

## Presentation

- Make the surface feel like a premium Apple utility.
- Lead with one calm summary line and one clear action.
- Keep the visual language restrained, dark, and readable at a glance.

## Build shape

- Prefer a menu-bar popover or compact status-item panel.
- Show the primary state first, then the useful detail lines.
- Collects files, text, and export bundles into a single calm handoff tray.
- Shows the next destination and the cleanest transfer path before you commit.
- Keeps the transfer UI minimal so it feels native on macOS instead of bolted on.

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
