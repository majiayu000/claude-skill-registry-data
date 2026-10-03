---
name: screen-snippet-studio
description: A menu-bar capture studio for clipping the current screen into clean prompts, tickets, or handoffs.
---

# Screen Snippet Studio

Use this skill when the user wants a polished macOS menu-bar capture surface for turning screen snippets into prompts, tickets, or handoffs.

## Presentation

- Make the surface feel like a premium Apple utility.
- Lead with one calm summary line and one clear action.
- Keep the visual language restrained, dark, and readable at a glance.

## Build shape

- Prefer a menu-bar popover or compact status-item panel.
- Show the primary state first, then the useful detail lines.
- Turns a quick screen shot into a usable prompt or note without extra context switching.
- Keeps the capture flow one click away in the menu bar.
- Pairs well with AI review, bug reports, and launch handoffs.

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
