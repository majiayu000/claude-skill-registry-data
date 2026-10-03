---
name: minesweeper-menubar
description: A Swift macOS menu-bar icon app concept for playing Minesweeper in a compact native popover.
---

# Minesweeper Menu Bar

Use this skill when the user wants a Swift menu bar icon app that plays Minesweeper, or a directly comparable grid-based puzzle in a compact macOS popover.

## Presentation

- Keep the app clearly Mac-native and menu-bar first.
- Let the icon feel playful without turning the UI into toy chrome.
- Prioritize board readability and quick replay.

## Build shape

- Prefer a SwiftUI `MenuBarExtra` shell.
- Keep the board playable without opening a second window.
- Put timer, flags, and reset near the top of the popover.
- Make the first click safe and replay instant.

## Guardrails

- Do not turn it into a launcher, dashboard, or account-backed service.
- Do not rely on background agents or unsupported system tricks.
- Keep the scope to one polished Minesweeper loop before adding variants.

## Prototype

- SwiftUI starter files live in `prototype/`.
- The prototype includes a playable board, reveal and flag modes, timer, local best-time tracking, and a menu bar entry point.

## When extending

- Add difficulty levels only if the popover still reads clearly.
- Reuse the shell for other micro games only after the Minesweeper interaction feels solid.
