---
name: story-arc-board
description: A menu-bar board for capturing repeated hooks from notes, captions, and comments before they disappear into app sprawl.
---

# Story Arc Board

Use this skill when the user wants a polished macOS menu-bar utility for catching recurring phrases, symbols, or post ideas across notes, drafts, and community chatter before that context gets scattered again.

## Presentation

- Make the surface feel like a premium Apple utility.
- Lead with one calm summary line and one clear action.
- Keep the visual language restrained, dark, and readable at a glance.

## Build shape

- Prefer a menu-bar popover or compact status-item panel.
- Show the intake lane first, then the pinned beats that deserve follow-up.
- Reduce tab-hopping between Notes, browser tabs, and social drafts.
- Keep the UI focused on capturing, pinning, and promoting the next strong hook.

## Guardrails

- Do not invent unsupported metrics or background services.
- Keep the app simple enough to feel native on macOS.
- Use one primary action and a small set of supporting actions.

## Prototype

- SwiftUI starter files live in `prototype/`.
- Keep the prototype menu-bar first and easy to transplant into a real macOS target.
- Favor pinned snippets, short labels, and one obvious next-step action over dashboard sprawl.

## When extending

- Add more depth only when it improves the single workflow the skill is meant to solve.
- If the skill grows, keep the menu-bar path short and the detail panel readable.
