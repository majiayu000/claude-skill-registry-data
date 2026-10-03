---
name: context-shelf
description: A menu-bar shelf for parking the current tab, clipboard snippet, and scratch note before you switch tasks, so resuming takes one glance instead of a rebuild.
---

# Context Shelf

Use this skill when the user wants a polished macOS menu-bar utility for parking in-flight context before switching tasks and resuming it cleanly later.

## Presentation

- Make the surface feel like a premium Apple utility.
- Lead with one calm summary line and one clear action.
- Keep the visual language restrained, dark, and readable at a glance.

## Build shape

- Prefer a menu-bar popover or compact status-item panel.
- Show the primary state first, then the useful detail lines.
- Parks the front tab, clipboard text, and a short scratch note into one compact resume bundle.
- Keeps the next thing to reopen visible in the menu bar so task switches stop turning into scavenger hunts.
- Stays deliberately small with shelf, pin, resume, and clear actions instead of a sprawling workspace manager.

## Workflow

- Capture the current browser tab, clipboard text, and a quick note as one shelf item.
- Show the most recent shelf first and keep older items lightweight.
- Treat the shelf as a resume aid, not a permanent database or workspace manager.

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
