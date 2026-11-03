---
name: davinci-resolve
description: "Use when editing video in DaVinci Resolve. Edit video in DaVinci Resolve (21.1, Mac App Store / Free build) from Claude Code via the `davinci-resolve` MCP + ResolveBridge (Lua) inside the app. Use ALWAYS when the owner talks about DaVinci, Resolve, editing/cutting/assembling video, timeline, rendering/exporting video, markers, color/Fusion, or asks to \"edit the videos together\"."
version: 1.0.0
ported: 1.0.0
author: "the owner (ported from his Claude Code skills library)"
license: MIT
metadata:
  hermes:
    tags: [owner-library, video, "DaVinci Resolve", MCP]
    related_skills: [videoediting]
---
> Ported from the owner's skills library (port 1.0.0; the source hash and
> what it needs are in `manifest.json` next to this file). Paths written `{skill_dir}/…` are this skill's own
> folder, `{skills_root}/<name>/…` a sibling icloneOS skill, `{agent_home}/…` the agent's home. Runs on macos only. Needs MCP server `davinci-resolve`, `/Applications/DaVinci Resolve.app`, `~/Movies`, `~/Movies/ResolveBridge`, `~/Movies/.resolve-bridge`.

# DaVinci Resolve — how to work

## Architecture (why)
App Store build (Lite, sandboxed). The free 21.1 edition HAS NO PYTHON (external scripting off, .py
ignored, Lua-only console, stdout silent — all measured). That is why the bridge is Lua: `ResolveBridge.lua`
runs INSIDE Resolve (LuaJIT+ffi, HTTP on 127.0.0.1 + a per-session token in
`~/Movies/.resolve-bridge/state.json`) and `server.py` (MCP, 32 tools) talks to it.
Code: `{agent_home}/mcp-servers/davinci-resolve/` (README with the measured facts).

## Startup (every time Resolve opens)
1. Resolve open with a project. 2. **Workspace › Console** (`app_menu ["Workspace","Console"]` on an English UI; pass the
   menu names in the language the Resolve UI is set to; the item toggles open/close — confirm with `app_list_windows`), click the input line (bottom, y≈626 of the 996×637 window)
   and type: `dofile(os.getenv('HOME') .. '/Movies/ResolveBridge/ResolveBridge.lua')` + Return.
   The Workspace › Scripts menu does NOT run anything in this build (measured) — do not waste time there.
3. `resolve_status`. "Bridge not reachable" → step 2 was not done. Repeating the line kills the old instance.

## Tools (natural order of a job)
- `resolve_status` → `project_list/open/create` → `media_import` (files in **~/Movies**) →
  `media_pool_list` ($ref) → `timeline_create` / `timeline_append` (sub-ranges startFrame/endFrame) →
  `timeline_summary` (see the assembly) → `marker_add/list/delete` → `item_property` (Zoom/Pan/Opacity/Crop) →
  `timeline_insert_title` → `render_presets` → `render_add_job(target_dir=~/Movies/…)` → `render_start` → `render_status`.
- `resolve_call(path, method, args)` = ANY API method; `resolve_lua(code)` = multi-step logic
  inside Resolve (Lua: `timeline:GetName()`, 1-based tables, `result = …` or `return …`);
  `resolve_api_docs("AddMarker")` searches the official README/CHANGELOG/examples (same names in Lua).
- `timeline_export(path, "fcpxml")` + the `fcpxml` MCP for deep analysis/QC (pacing, gaps, flash frames).

## Rules / traps
- Sandbox: only **~/Movies** is readable/writable by the app → media, exports and renders live there.
- `$ref` dies when the bridge restarts; list again.
- Marker frames are relative to the start of the timeline (`absolute=True` for an absolute frame).
- The Lua API returns tables with `__flags`; the bridge already cleans them. Empty lists arrive as `[]`.
- After editing the bridge: `./install.sh` (copies to ~/Movies) + repeat the line in the Console.
- Resolve Console: only `error('…')` shows text; `print` is silent. There is no Py3 selector.
- Studio-only features (Magic Mask, Smart Reframe, Voice Isolation, Super Scale) do not exist in this build.
- Offline tests: `.venv/bin/python tests/test_bridge.py` (needs `luajit`, installed via brew).
