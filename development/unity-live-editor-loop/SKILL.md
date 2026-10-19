---
name: unity-live-editor-loop
description: Work on a Unity project with a live editor attached through MCP and the Unity CLI - route each need to the right surface (scene and hierarchy edits, console, compile status, tests, Play Mode inspection, headless test and build), keep the edit-compile-test-play loop safe (exit Play Mode before editing, never hand-edit serialized assets while the editor is open, wait through compilation), and recover from Safe Mode. Use for any change in a Unity project that has the Unity MCP server, Meta XR MCP bridge or the unity CLI available.
license: Unlicense
metadata:
  tags: "Unity, MCP, Agentic Development, Editor Automation"
  category: "implementation"
---

# Unity live editor loop

## Surfaces

| Need | Surface |
|---|---|
| Hierarchy, components, scene edits, console, run C# in the editor | Unity MCP server (`Unity_ManageScene`, `Unity_ManageGameObject`, `Unity_ReadConsole`, `Unity_RunCommand`, `Unity_ManageScript`) |
| Compile status, run tests from the live editor, editor screenshots, execute menu items, Play Mode inspection | Meta XR MCP bridge (when the Meta XR SDK is in the project) |
| Headless tests and builds, editor state, one-shot editor commands | Unity CLI (`unity test`, `unity build`, `unity status`, `unity pipeline list`, `unity command`) |
| XR head and controller input | Meta XR Operator (OpenXR API layer) |

Rules of thumb: a live surface that stops answering means the editor is compiling or importing, so wait and
retry; nothing answering usually means Safe Mode or a closed editor; `unity test` and `unity build` spawn
their own editor and need the project closed.

## The loop

1. Read the design or architecture notes for the subsystem before editing.
2. Edit C#; let the editor recompile; check `error CS` through the console tool.
3. Run EditMode tests (`unity test <project> --mode EditMode --report-format junit --output TestResults/editmode.junit.xml`
   or the bridge Test Runner); add tests for pure logic.
4. Enter Play Mode through a tool, drive the scenario, inspect state, capture the Game view, read the console.
5. **Exit Play Mode before any further edit**; Play Mode edits are lost.
6. Scene, prefab and asset edits go through editor tools; never hand-edit `.unity/.prefab/.asset/.mat` YAML while
   an editor has the project open (`Temp/UnityLockfile` exists). Editing YAML with the editor closed is fine, say so.
7. Package changes go through the package manager tooling, never by hand-editing `Packages/manifest.json`.
8. Commit small logical steps with evidence (test report, captures) kept for the review.

## Safe Mode recovery

1. `unity pipeline list --json --no-banner` reports `instancesInSafeMode`.
2. Read only the error lines from the editor log (`%LOCALAPPDATA%\Unity\Editor\Editor.log` on Windows,
   `~/Library/Logs/Unity/Editor.log` on macOS): filter for `error CS`; never dump the whole log.
3. Fix the C#; the editor recompiles and leaves Safe Mode; restart it if the MCP bridges do not reconnect.
4. A domain reload that never finishes: look for exceptions in `[InitializeOnLoad]` code; closing the editor from
   the OS is the last resort and must be reported.

## Hooks worth adding to the project

- A pre-edit hook that asks before writing serialized Unity assets while `Temp/UnityLockfile` exists.
- A session-start hook printing branch, editor state (running, pipeline package, Safe Mode) and MCP registration.
- Permission denies for secret files (Firebase configs, keystores, API keys) and force pushes.
