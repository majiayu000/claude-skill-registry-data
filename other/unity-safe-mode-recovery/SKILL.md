---
name: unity-safe-mode-recovery
description: Diagnose and recover a Unity editor that is in Safe Mode, stuck compiling, stuck in a domain reload, or unreachable from MCP and CLI tools - detect the state with the Unity CLI, read only the compiler errors from Editor.log, fix the code, and restart cleanly. Use whenever every live Unity surface stops responding or the CLI reports Safe Mode.
license: Unlicense
metadata:
  tags: "Unity, Troubleshooting, MCP, Editor"
  category: "testing-validation"
---

# Unity Safe Mode and stuck editor recovery

## Detect

```powershell
unity status --json --no-banner            # connected editors with the pipeline package
unity pipeline list --json --no-banner     # isRunning, hasPipelinePackage, safeMode, reachable server
```

- `safeMode: true`: the last compilation failed; scripts are not loaded; every MCP tool that lives in an
  editor assembly is gone.
- `isRunning: true` but `isReachable: false`: the editor is compiling, importing, or the pipeline package is
  not resolved yet (focus the editor so it imports the manifest).
- No instance at all: the editor is closed, or a different project is open.

## Read the errors (never the whole log)

```powershell
Select-String -Path "$env:LOCALAPPDATA\Unity\Editor\Editor.log" -Pattern "error CS" | Select-Object -Last 20
```

macOS: `grep "error CS" ~/Library/Logs/Unity/Editor.log | tail -20`. Batch runs: the log path passed with
`-logFile` or printed by the CLI.

Each line has `Assets/.../File.cs(line,col): error CSxxxx: message`. Fix them all; one remaining error keeps
the editor in Safe Mode.

## Fix and recover

1. Edit the C# (the editor watches the files and recompiles when focused; in Safe Mode press "Exit Safe Mode"
   after the compile succeeds, or let it exit automatically).
2. Confirm: `unity pipeline list` shows `safeMode: false` and a reachable server; the console tool reports no
   errors.
3. MCP bridges that do not reconnect within a minute: restart the editor (`unity open` or the Hub), then
   re-approve the MCP client connection if the project asks.
4. A never-ending domain reload or import: look for exceptions in `[InitializeOnLoad]`, asset postprocessors or
   custom importers in the console; remove the offending change; as the last resort close the editor from the OS
   and report it, since unsaved scene changes are lost.
5. Headless verification without touching the open editor: `unity test <project> --mode EditMode` (needs the
   project closed) compiles everything and reports the same errors.

## Prevent

- Compile-check after every C# edit before moving on.
- Keep editor-only code under an `Editor` folder or an editor assembly definition.
- Never write to `Assets/` while a batch editor is starting (it imports what it finds).
