---
name: browser-game-playtest-sentinel
description: Use when a user asks to playtest, smoke test, screenshot, inspect console errors, check mobile layout, verify HUD overlap, or produce evidence for a browser game. Works with local URLs, static HTML, canvas games, and web game prototypes using project-neutral paths.
---

# Browser Game Playtest Sentinel

Run or plan repeatable browser-game checks with evidence.

## Inputs

Ask for or infer:

- `<PROJECT_ROOT>` or `<GAME_URL>`;
- target viewport;
- expected player flow;
- report destination `<REPORT_DIR>`;
- known risk such as overlap, blank canvas, console errors, or mobile clipping.

## Check Order

1. Boot the game.
2. Capture screenshot evidence.
3. Check console/page errors.
4. Verify player-visible objective and primary action.
5. Check layout overlap or clipping.
6. Run the smallest relevant route again after a fix.

## Report

Include:

- pass/fail;
- screenshots or report paths;
- console/page errors;
- viewport;
- player impact;
- next safest fix;
- rollback note for runtime changes.

## Stop Rules

Do not deploy, publish, install unknown dependencies, use credentials, or change runtime files unless the user explicitly approved that exact scope.
