---
name: roblox-studio-workflow
description: Use Roblox Studio MCP safely and productively from Claude. Use when connecting to Studio, inspecting a Roblox place, editing scripts or instances, inserting assets, generating models/materials, or playtesting through MCP tools.
---

# Roblox Studio Workflow

## Purpose

Use this skill when work needs the local `Roblox_Studio` MCP server. Keep the loop grounded in the live Studio session: connect, inspect, read, edit, playtest, and check output.

## Start Every Roblox MCP Session

1. Run `list_roblox_studios` first.
2. If more than one Studio is open, use `set_active_studio` before making changes.
3. Run `get_studio_state` to confirm play state and available DataModel types.
4. If the place has a `ROADMAP.md` or project instruction file, read it before deciding what to build next.

## Tool Loading

If MCP tools are deferred in the current Claude session, use Tool Search to select the exact `mcp__Roblox_Studio__<tool>` names needed before calling them.

## Code Change Rule

For scripts, follow this sequence:

1. Locate with `script_search` or `script_grep`.
2. Read the target with `script_read`.
3. Edit with `multi_edit`.
4. Playtest with `start_stop_play`.
5. Check `get_console_output`.

Never edit a Roblox script you have not read in the current task context.

## Instance And World Changes

- Use `search_game_tree` to find relevant objects.
- Use `inspect_instance` before changing a specific object or hierarchy.
- Use `execute_luau` for small targeted queries, scene setup, or one-off validation.
- Prefer server-side validation and authoritative server logic for currency, inventory, purchases, item grants, and progression.

## Assets

- Search existing assets first with `search_asset`.
- Insert third-party Creator Store or inventory assets with `insert_asset` only into a controlled location first.
- Run `roblox-creator-store-security-audit` after importing any third-party model, package, gameplay asset, UI asset, or plugin-like asset before trusting it or leaving scripts enabled.
- Generate only when marketplace or inventory assets do not fit:
  - `generate_mesh` for one custom mesh.
  - `generate_material` for a surface look.
  - `generate_procedural_model` for configurable primitive-built models.
- Use `store_image` or `upload_image` when local or web images need to become Roblox-ready assets.

## Playtesting

- Use `start_stop_play` for live verification.
- Use `character_navigation`, `user_keyboard_input`, and `user_mouse_input` to exercise gameplay and UI.
- Use `screen_capture` to verify visual state.
- Always check `get_console_output` after a playtest.

## Roadmap Discipline

Only mark roadmap items complete after implementation, testing, and explicit human approval. Use an awaiting-approval marker when a feature is built and tested but not yet approved.

## Next

With Studio connected, move to the task at hand — usually `roblox-luau-architecture` for code, `roblox-ui-implementation` for UI, or `roblox-debugging-bugfix` for a bug. Use `roblox-game-development-lifecycle` if you are unsure what to work on.
