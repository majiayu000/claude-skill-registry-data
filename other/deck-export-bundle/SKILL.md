---
name: deck-export-bundle
description: A menu-bar export bundle for packaging the current slide deck, speaker notes, and send-ready assets without bouncing between Keynote, Finder, and chat.
---

# Deck Export Bundle

Use this skill when the user wants a polished macOS surface built around this workflow:

- A menu-bar export bundle for packaging the current slide deck, speaker notes, and send-ready assets without bouncing between Keynote, Finder, and chat.

## Presentation

- Make the surface feel like a premium Apple utility.
- Lead with one calm summary line and one clear action.
- Keep the visual language restrained, dark, and readable at a glance.

## Build shape

- Prefer a menu-bar popover or compact status-item panel.
- Show the primary state first, then the useful detail lines.
- Pulls the live deck, speaker notes, and output format into one send-ready bundle card.
- Keeps PDF export, notes text, and reveal-in-Finder actions together before the handoff leaves your Mac.
- Turns last-mile deck packaging into one calm menu-bar step instead of a Finder and chat scramble.

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
