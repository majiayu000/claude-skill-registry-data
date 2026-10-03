---
name: power-sentry
description: A battery-and-power watch that helps you read drain, charging, and energy mode at a glance.
---

# Power Sentry

Use this skill when the user wants a polished macOS surface for A battery-and-power watch that helps you read drain, charging, and energy mode at a glance.

## Presentation

- Make the surface feel like a premium Apple utility.
- Lead with one calm summary line and one clear action.
- Keep the visual language restrained, dark, and readable at a glance.

## Build shape

- Prefer a menu-bar popover or compact status-item panel.
- Show the primary state first, then the useful detail lines.
- Shows battery state and energy mode without the noise of a diagnostics dump.
- Pairs well with lightweight trend cues and significant energy usage.
- Stays calm enough to live in the menu bar all day.

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
