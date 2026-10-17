---
name: uefn-scripting-batch
description: Run 5+ MCP calls server-side in one request with ProgrammaticToolset (get_execution_environment, execute_tool_script) for batched reads, widget chains and edit+build. Use when several calls can share one request and cleanup is planned. Requires uefn-mcp-lab-guard.
last_reviewed: 2026-10-16
sources: [original]
---

# uefn-scripting-batch

Source: `Claude/docs/mcp/scripting-batch.md`, `recipes.json` (only `tool-ok` or `proven`; `proven` = the same call form already worked in real work), `SKILLS-PROPOSAL.md` B7.

## Read first
1. Read `uefn-mcp-lab-guard` (the guard sees only the OUTER call, so the script itself must use lab paths only).
2. Ping with a cheap read before the first write script.
3. If the MCP does not answer: stop and report. Never close or kill a running editor (after a crash: `uefn_session.py recover`, opt-in).

## Rules
- Paths inside scripts: GUID form `/09e4e8d3-83f9-4ee0-9777-072ed3984380/root_ai_lab/...`; nothing outside the lab, no other project's mount.
- The guard is not bypassed (no sandbox-escape attempts; dunder access is out of scope); a refusal is reported verbatim.
- If a recipe fails: exact error text, then STOP.
- No write script without a cleanup plan: inner errors cannot be caught and there is NO rollback, the caller deletes what was created.

## Verified recipes (toolset `editor_toolset.toolsets.programmatic.ProgrammaticToolset`)

| Tool | Args | Note |
|---|---|---|
| get_execution_environment | `{}` | returns instructions, supported_modules (json, math, datetime, copy, re, time), language python |
| execute_tool_script `#batch_reads` | script: several read tools, returns a dict | read only; timing with `time` |
| execute_tool_script `#create_widget_chain` | CreateWidgetBlueprint, AddWidget Overlay (`parentWidget` None), AddWidget StackBox, CompileWidgetBlueprint, save | cleanup: `AssetTools/delete {path}` of the blueprint |
| execute_tool_script `#verse_edit_build` | Replace + BuildAll, returns diagnostics | ~5 s for two builds; cleanup as Replace |

Script shape: define `run()` returning a dict; call `execute_tool("<Toolset>.<Tool>", json.dumps(args))["returnValue"]` (dot between toolset and tool inside scripts).

## Traps (exact messages)
- Forbidden import: `Import of 'os' is not permitted. Allowed modules: frozenset({'json', 'time', 'math', 'datetime', 'copy', 're'})`; same for subprocess, sys, unreal.
- `Script must define a callable run() function.`; `run() must return a dict[str, Any], returned list`.
- Args as dict: `TypeError: the JSON object must be str, bytes or bytearray, not dict` (use `json.dumps`).
- A failing inner tool cannot be caught (`try/except` does not work); the script aborts and earlier writes stay (seen: orphan `WBP_Scr007` with its Overlay).
- No state between scripts; `open(..., "w")` refused (`Mode 'w' is not permitted`); reads only in the editor's allowed directories; `eval`/`exec` are NameError.
- Before a write script check `exists` inside it; on failure list what was written and delete it.

## To try (not verified)
- `recipe/apply_material_instance_to_actor` (ONE script: add actor, set overrideMaterials, read back, reset, remove): status unverified in recipes.json; materials area; apply+read+reset+remove must stay in one script.
- `recipe/animate_owner_actor_with_script_and_restore`: status field is unverified (the inner `verified` flag is inconsistent); loop of `set_actor_transform` with `time.sleep`, restores the original transform. Confirm before use.
