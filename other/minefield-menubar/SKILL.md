---
name: minefield-menubar
description: A polished macOS menu-bar puzzle that turns Minesweeper-style rounds into quick coffee-break runs.
---

# Minefield Menu Bar

Use this skill when the user wants a real macOS menu-bar game, especially a Minesweeper-style puzzle or a compact replayable arcade loop.

## Presentation

- Make it feel like a sharp native utility with game energy, not a bloated launcher.
- Keep the board readable in one glance.
- Use color and motion restraint so the popover still feels at home in macOS.

## Build shape

- Prefer one compact menu-bar popover over extra windows.
- Lead with the board, the current mode, and one reset action.
- Keep the round length short enough to make sense from the top bar.
- Make replay immediate after a win or loss.

## Guardrails

- Do not depend on accounts, ads, cloud sync, or fake social systems.
- Keep the whole core loop playable inside the menu-bar surface.
- Avoid cramming in multiple half-finished games when one polished loop will do.

## Prototype

- SwiftUI starter files live in `prototype/`.
- The prototype includes a playable board, reveal and flag modes, timer, mine count, and replay flow.

## When extending

- Add difficulty presets only if the popover stays clear at a glance.
- Reuse the shell for other micro games only after the board interaction feels solved.
