---
name: release-ramp
description: A release-prep board that turns a shipping checklist into a clean launch lane.
---

# Release Ramp

Use this skill when the user wants a polished macOS surface for A release-prep board that turns a shipping checklist into a clean launch lane.

## Presentation

- Make the surface feel like a premium Apple utility.
- Lead with one calm summary line and one clear action.
- Keep the visual language restrained, dark, and readable at a glance.

## Build shape

- Prefer a menu-bar popover or compact status-item panel.
- Show the primary state first, then the useful detail lines.
- Turns the shipping checklist into something visible and manageable.
- Highlights missing steps before a release goes live.
- Feels like a small launch control panel instead of a giant PM app.

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
