---
name: chrome-tab-sweeper
description: Build or operate a macOS menu-bar Chrome tab control surface that lists overloaded browser tabs, groups them by domain or task, and closes explicit selected tab batches with a safe review step.
---

# Chrome Tab Sweeper

Use this skill when the user wants a Mac menu-bar utility for understanding a chaotic Google Chrome tab state and closing selected tab piles without digging through every window.

## Core Workflow

- Start by listing Chrome tabs before any close action.
- Group tabs by domain, window, or guessed task so the user can understand the pile quickly.
- Treat "delete tabs" as "close tabs"; closing should require an explicit selected set.
- Use compact top-bar UI language: count, mess level, top domains, and one cleanup action.
- Keep the main interaction reversible-feeling: preview the selected tabs and close only after confirmation.

## Local Helper

Use `scripts/chrome_tab_sweeper.py` when a deterministic local tab read is useful:

```bash
python skills/chrome-tab-sweeper/scripts/chrome_tab_sweeper.py list
python skills/chrome-tab-sweeper/scripts/chrome_tab_sweeper.py close w1:t8 w1:t9 --yes
```

The script uses macOS `osascript` with Google Chrome's scripting interface. It does not use network access. Close tokens are generated from the current window and tab indices, so list again if the browser changes.

## Guardrails

- Never close every tab blindly. Show the set first.
- Avoid closing pinned, active, auth, checkout, writing, or meeting tabs unless the user explicitly names them.
- If Chrome is not running or macOS denies automation permission, explain the permission path instead of inventing tab state.
- Do not claim full browser history, passwords, or content access; this skill is about visible tab metadata and controlled closing.

## Prototype

The SwiftUI starter in `prototype/` sketches the menu-bar layer: a compact top icon, tab count, domain groups, selected cleanup batch, and action buttons. Use it as the top-level UI shell for a real macOS target.
