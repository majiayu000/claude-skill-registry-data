---
name: dayz-launch-workbench
description: "Opens Enfusion Workbench (DayZ Tools' script and UI editor) on vanilla DayZ or on a mod's gproj so vanilla and mod scripts compile together. Use when you want to write or debug a mod's Enforce Script or .layout files with Workbench's compiler and code completion."
argument-hint: "[--mod <ModName> | --gproj <path>]"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-launch-workbench

Open Workbench without leaving the terminal. Default loads vanilla DayZ; `--mod <ModName>` loads the customized `dayz.gproj` that `/dayz-new-mod` (or `/dayz-add-scaffold --piece workbench`) writes into `workspace/<ModName>/workbench/` (reached as `P:\<ModName>\workbench\` through the `/dayz-new-mod` junction), so Workbench compiles and lints vanilla + your mod together.

Follow `skills/_shared/dayz-conventions.md`.

## What it does

1. Checks a `--mod` name before anything else, so a typo fails before the preflight output: it must match `/dayz-new-mod`'s rule (starts with a letter; letters, digits, underscores; max 64 chars) and must not be a reserved `P:\` folder (see "Flag rules").
2. Gates on `/dayz-preflight`.
3. Resolves the project file, before looking for DayZ Tools:
   - `--mod <ModName>` → uses `P:\<ModName>\workbench\dayz.gproj`. Fails fast if the mod folder or gproj isn't there; a missing gproj is added with `/dayz-add-scaffold <ModName> --piece workbench`.
   - `--gproj <path>` → uses an explicit `.gproj` file (escape hatch for non-scaffolded layouts). Fails fast if it does not exist, is a folder, or contains a space.
   - Neither → no project arg; Workbench loads the default `dayz.gproj` shipped next to `workbenchApp.exe`.
4. Locates `workbenchApp.exe` via DayZ Tools (`Bin\Workbench\workbenchApp.exe`). For a vanilla launch it also checks that the bundled `Bin\Workbench\dayz.gproj` exists and fails with a hint to verify DayZ Tools in Steam if it does not (a partial install otherwise ends in Workbench's "cannot find file dayz.gproj").
5. Refuses (exit 1) when a `workbenchApp.exe` is already running, naming its PID. `tasklist` cannot show which project a running Workbench has open, so any running instance blocks a second launch. If `tasklist` itself cannot run, it prints a `[WARN]` that the check was skipped and launches anyway.
6. Spawns `workbenchApp.exe`, passing any project as `-gproj=<path>` (Workbench's own switch; with no switch it loads `$CurrentDir:dayz.gproj`, the vanilla one), with `cwd=<DayZ Tools>\Bin\Workbench` (so Workbench's support files resolve; see "Why cwd" below), detached so the shell returns immediately.
7. Watches the new process for one second. If `workbenchApp.exe` exits in that time (bad project file, missing DLL), it prints the exit code and exits 1 instead of reporting a launch.

## How to run

**Just open Workbench on vanilla:**
```cmd
python "<skill-dir>\launch.py"
```

**Open with a mod's project file (compiles vanilla + mod together):**
```cmd
python "<skill-dir>\launch.py" --mod MyMod
```
(Requires `P:\MyMod\workbench\dayz.gproj`, created by `/dayz-new-mod MyMod`. For an imported or older mod without it, run `/dayz-add-scaffold MyMod --piece workbench` first.)

**Open with an arbitrary gproj:**
```cmd
python "<skill-dir>\launch.py" --gproj P:\Custom\path\to\my.gproj
```

## When to run

- After `/dayz-new-mod` to start writing scripts/UI for a fresh mod with full code completion against vanilla.
- Anytime you want to edit `.layout` files or browse vanilla scripts in their native IDE.
- When debugging script errors — Workbench's compiler surfaces the same errors the engine would hit at runtime.

## Output

```
DayZ Workbench launcher

DayZ preflight

[OK]    P:\ is mounted
[OK]    DayZ Tools found: C:\...\steamapps\common\DayZ Tools
[OK]    Vanilla data found: P:\dz
[OK]    P:\Mods -> C:\...\steamapps\common\DayZ\!Workshop

Preflight complete.

[OK]    workbenchApp.exe: ...\Bin\Workbench\workbenchApp.exe
[INFO]  Project: P:\MyMod\workbench\dayz.gproj
[OK]    Working directory: ...\Bin\Workbench

[OK]    Workbench launched (PID 12345). The window may take a few seconds to appear.
```

Exit code 0 means `workbenchApp.exe` was still running one second after the spawn. Exit code 1 means preflight failed, DayZ Tools, `workbenchApp.exe` or (for a vanilla launch) the bundled `dayz.gproj` is missing, the `--mod`/`--gproj` target is invalid, Workbench is already running, or the new process exited at once:

```
[FAIL]  workbenchApp.exe exited right after starting (exit code 1).
```

## Flag rules

- `--mod` and `--gproj` are mutually exclusive (argparse rejects both together).
- `--mod` is just the mod name, checked against `/dayz-new-mod`'s name rule before it is joined onto `P:\` (so `..\Windows` or `My-Mod` is refused); the skill expands it to `P:\<ModName>\workbench\dayz.gproj`. Fails fast if either the mod folder or the gproj is missing.
- `--mod` refuses the `P:\` folders that are not mods, in any letter case: the vanilla data folders `dz`, `bin`, `core`, `graphics`, `gui`, `languagecore`, `scripts`, `system` (the PBO prefixes of `DayZ\Addons\*.pbo`, all `DZ\...`, and of `DayZ\dta\*.pbo`), and `Mods` (the Workshop junction). To open vanilla, run without `--mod`.
- `--gproj` accepts an absolute path; a relative path resolves against the project (`CLAUDE_PROJECT_DIR`, else the working directory). It must be a file: a folder such as `P:\MyMod\workbench` is refused; pass the `.gproj` inside it. Warns if the extension isn't `.gproj`. A path containing a space is refused, because Workbench has not been confirmed to open a quoted `"-gproj=<path>"`; use a path without spaces, such as one under `P:\` (a `--mod` path is always `P:\<ModName>\...`, which has none).

## Why cwd=`<DayZ Tools>\Bin\Workbench`

Workbench resolves its own support files (`dta\`, `platforms\`, `ToolAddons\`) from the working directory, and the scaffolded `dayz.gproj` mounts `P:/` and `P:/<ModName>/` explicitly, so vanilla and mod sources resolve no matter where the gproj lives.

## Why detached

The editor is spawned detached (shared `DETACH_FLAGS` in `_shared/skill_helpers.py`) so the terminal returns at once and closing it doesn't kill Workbench; the printed PID identifies the process.

## Editing the gproj

`workbench/dayz.gproj` is yours to edit (for example to add modules beyond the injected `game`/`world`/`mission` paths). No skill rewrites it: `/dayz-new-mod` refuses to run on an existing mod folder and `/dayz-add-scaffold` never overwrites a file. To regenerate it, delete it and run `/dayz-add-scaffold <ModName> --piece workbench`.

## Do not

- Don't pass `--mod` for a mod without `workbench/dayz.gproj`; add it first with `/dayz-add-scaffold <ModName> --piece workbench`.
- Don't spam-launch; Workbench isn't designed to run multiple instances against the same project. The launcher refuses while one is running: use that window, or close it and run the skill again.
