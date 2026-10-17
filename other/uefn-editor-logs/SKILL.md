---
name: uefn-editor-logs
description: Read the new UEFN editor log lines after an action, set verbosity, camera/viewport/CVar, selection and content browser via MCP (LogsToolset, EditorAppToolset). Use when you need to understand what the editor wrote after an MCP call.
last_reviewed: 2026-10-16
sources: [original]
---

# uefn-editor-logs

Source: `Claude/docs/mcp/editor-logs.md`, recipes in `recipes.json`. Before every call, apply `uefn-mcp-lab-guard` (open project = lab, lab paths only). To create/use/remove a test asset, see `uefn-create-use-remove-one-script`.

## Rules
- Paths always in GUID form: `/<guid>/<project>/...`. The guard is not bypassed: a refusal is reported as is.
- If a recipe fails: report the exact error and stop (no creative retries).
- DO NOT read the whole log (2.4 MB): always use a cursor + `maxEntries`.

## Verified recipes
1. **Cursor**: `EditorToolset.LogsToolset/GetLogEntries {category:"", pattern:"", maxEntries:1}` -> last line.
2. Perform the action, then `GetLogEntries {category:"", maxEntries:300}`; new lines = after the LAST occurrence of the cursor line.
3. **Noise filter**: `GetLogEntries {category:"", maxEntries:50, pattern:"^(?!.*LogModelContextProtocol)"}`.
4. `LogsToolset/GetLogCategories` (warn), `GetVerbosity`, `SetVerbosity` (restore the initial value).
5. Reason for StartSession failure: `GetLogEntries {category:"", maxEntries:0, pattern:"UEFNValidation"}`.
6. `EditorAppToolset`: `SetCameraTransform` (restore the transform saved by GetCameraTransform), `CaptureViewport`, `SetViewportViewMode` (enum `VMI_...`), `GetCVarValue`, `SearchCVars`, `ShowNotification`, `SetShowFlag`, `SetEditorMode`, `SetContentBrowserPath` (subfolders only), `SelectAssets`, `OpenEditorForAsset`.

## Pitfalls
- `GetLogEntries {}` fails: the default category is the toolset name; always `category:""`.
- Every MCP call is itself in the log: a diff is never empty (filter out `LogModelContextProtocol`).
- `ShowNotification` writes no log lines: for a marker, use a call that fails.
- Invalid regex -> silent `[]`.

## To try (not verified)
- `SessionToolset/GetClientLogEntries`: NOT verified. Always answers "No client log was found; start a play-in-client session first." even with a live client (3 sessions, T-015 C2). Working route: `LogsToolset/GetLogEntries` (Verse Print of a session in the editor log, see the recipe note).
- `SelectActors` / `FocusOnActors` / `SelectOutlinerFolders` with a real target: refused by the guard (actor path with `.` after the root) or no Outliner panel open; with `[]` they answer ok. Do not bypass.
