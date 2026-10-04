---
name: pb-show-build
description: >-
  Build a show across lights (grandMA3), media (Resolume) and generative
  visuals (TouchDesigner) from one cue list, offline first. A lane whose
  console or app is not running is skipped and logged while the others
  continue; the live rig is touched only after GO. Use for "build the show",
  "cue list to grandMA3 Resolume and TouchDesigner", "show programming".
category: media-eventtech
kind: playbook
trigger: ["build the show", "cue list to grandMA3 Resolume and TouchDesigner", "show programming"]
inputs: [tracker, cue_list, fixture_list, media_folder]
requires:
  skills: [godmode-eventtech, bdbmediastorm, bdb-grandma3-mcp, bdb-resolume-mcp, bdb-touchdesigner-mcp, pb-event-tracker]
  agents: []
  mcps: [bdb_grandma3_mcp, bdb_resolume_mcp, bdb_td_minddesigner]
  store: []
go_points: [patch console, live rehearsal]
outputs: ["cue-sheet.md", "production_artifacts/pb-show-build-<date>.md"]
verify: "each available lane answers its ping; TD node errors empty; every cue in cue-sheet.md maps to a TD cue, Resolume clip or MA3 macro"
difficulty: advanced
est_time: 2-6 h
---

# Show build: lights, media, visuals
What you get: a cue sheet and a show built per lane, rehearsed offline first, with the live rig touched only after your GO. A lane that is not available is skipped, not faked.

## Inputs
- tracker — the pb-event-tracker output (`tracker.csv`, `brief.md`)
- cue_list — the cues: number, name, what happens in light, media and visuals
- fixture_list — fixtures with type, mode, universe and address
- media_folder — the clip files for Resolume

## Steps
1. Preflight — one probe per lane, each independent: `grandma3_ping` on `bdb_grandma3_mcp`; `resolume_ping` on `bdb_resolume_mcp`; `get_td_info` on `bdb_td_minddesigner` (pass: `connected: true`). MCP tools may be deferred in the harness: try to load the tool once via the harness tool search before declaring it missing. Tool not loaded, call errors or the pass condition fails → log "Missing MCP: `<server>` (`<tool>` unavailable). Start <the grandMA3 console or onPC|Resolume Arena|TouchDesigner> and check `mcpServers.<server>` in your harness config." and mark that lane `off`; the other lanes continue and every step below runs only for lanes marked `on`. All three `off` → stop and write nothing except the run log — each lane marked `on` or `off` in the run log
2. bdbmediastorm + godmode-eventtech — tracker, cue_list, fixture_list, media_folder → `cue-sheet.md`, one row per cue with its target per lane (MA3 macro, Resolume clip, TD cue; `lane off` where a lane is missing) — stops for approval
3. TouchDesigner lane (bdb-touchdesigner-mcp) — cue-sheet → `compose_cue_list` and `create_safety_blackout_chain`, then `get_td_node_errors` — errors empty; offline: nothing is sent to live outputs
4. Resolume lane (bdb-resolume-mcp) — media_folder, cue-sheet → `get_composition` compared with the clips the cue sheet names — every Resolume clip in the sheet is present in the composition, missing ones listed for the human to load (no MCP tool loads media)
5. [GO] patch console (grandMA3 lane) — `patch_fixture` for each fixture in fixture_list (patching only, no macro is executed here), the full fixture list named in the WAITING FOR GO line. The run stops here until the human types GO. This changes the live console, and no hook guards it, so this GO is the only guard. One GO = this one list, one time.
6. [GO] live rehearsal — walk the cue sheet on live outputs with `trigger_clip` and `clear_layer` (Resolume), the TD cue list and `execute_macro` for each macro in cue-sheet.md (grandMA3), only for lanes marked `on`; the cue count, the macro list and the lanes named in the WAITING FOR GO line. The run stops here until the human types GO. Light, video and projection go live, and no hook guards it, so this GO is the only guard. One GO = one rehearsal pass.
7. Check — every cue row in `cue-sheet.md` maps to a TD cue, Resolume clip or MA3 macro or is marked `lane off`; `get_td_node_errors` empty again after the rehearsal — mapping table and result in the run log

Run log: `production_artifacts/pb-show-build-<date>.md` in the start directory, never committed

Rules
- Anything other than the literal GO (case-insensitive) is not a GO; a GO covers only that one step, one time.
- A failed check stops the run: write the failure into the run log and report. No silent retries.
- Write one run-log line per step as it completes (`N. done|skipped|failed — artifact — check result`) and `WAITING FOR GO: <step>` at each gate. A lane marked `off` is logged `skipped` with its Missing MCP line.
