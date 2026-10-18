---
name: roblox-playtest-qa
description: Playtest Roblox experiences through Studio MCP with attention to first-session fun, mobile UX, console errors, progression, social hooks, performance, and exploit-sensitive flows.
---

# Roblox Playtest QA

## Purpose

Use this skill to verify that a Roblox change works in Studio and supports player-facing quality. A playtest should prove both behavior and feel.

## Setup

1. Run `list_roblox_studios`.
2. Use `set_active_studio` if needed.
3. Run `get_studio_state`.
4. Start play mode with `start_stop_play` when verification requires live behavior.

## Test Checklist

- First action is reachable within 10-30 seconds.
- Controls work without keyboard-only assumptions.
- HUD text is readable and not blocking gameplay.
- Rewards, currency, XP, or progress update correctly.
- The next objective is visible after each loop.
- Social features are visible early when relevant.
- Monetization prompts are optional and do not interrupt first-session flow.
- Server-side systems own valuable state.
- No obvious frame drops or runaway instance/script growth.
- `get_console_output` has no new errors.

## MCP Tools To Use

- `character_navigation` for movement and route checks.
- `user_keyboard_input` and `user_mouse_input` for controls and UI.
- `screen_capture` for visual verification.
- `get_console_output` for errors and warnings.
- `inspect_instance` or `execute_luau` for state checks after interaction.

## Report Format

Return:

- What was tested.
- Evidence gathered, including screenshots or console results when available.
- Pass/fail by area.
- Bugs or risks ranked by player impact.
- Recommended next verification step.

Do not mark roadmap items complete without human approval, even after a passing playtest.

## Next

Send any bug to `roblox-debugging-bugfix` and any performance issue to `roblox-performance-optimization`. If the slice passes, mark it in `roblox-triage` / `ROADMAP.md` and prepare the build with `roblox-release-operations`.

