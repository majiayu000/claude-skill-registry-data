---
name: dayz-launch-objectbuilder
description: "Opens DayZ Tools' Object Builder (the .p3d model editor), optionally on a specific .p3d or the one .p3d in a mod's P: folder. Needs /dayz-setup-objectbuilder run once. Use when you need to inspect or edit a .p3d model, such as adding LODs, named selections or memory points."
argument-hint: "[--file <p3d> | --mod <ModName>]"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-launch-objectbuilder

Open Object Builder without leaving the terminal. Optionally pre-loads a `.p3d`: one you name with `--file`, or the one model anywhere under a mod's `P:\<ModName>\` folder with `--mod`.

Follow `skills/_shared/dayz-conventions.md`.

## What it does

1. Gates on `/dayz-preflight` (as `/dayz-launch-workbench` does), so an unmounted `P:\` fails with preflight's fix before `--mod` looks under it.
2. Resolves the open target:
   - `--file <path>`: that `.p3d`. A relative path is looked up under the project root first, then the current folder; when neither has it, the error lists both paths it tried. Fails if the path is missing or is a folder (Object Builder opens model files, not folders); warns if the extension isn't `.p3d`.
   - `--mod <ModName>`: checks the name against `/dayz-new-mod`'s naming rule (a letter first, then letters, digits or underscores, at most 64 characters; the same `NAME_PATTERN`, loaded from its `new_mod.py`) and refuses the top-level `P:\` folders that are not mods (vanilla data such as `P:\DZ`, `P:\scripts` or `P:\gui`, and the `P:\Mods` junction; the same `RESERVED_P_FOLDERS` list `/dayz-launch-workbench` uses, loaded from its `launch.py`) before joining it onto `P:\`. It then takes the `.p3d` anywhere under `P:\<ModName>\` (every subfolder, so `data\`, `models\` or any other layout). Object Builder opens model files, not folders, so the skill never passes it a directory. Fails if the name is invalid or reserved, or the mod folder is missing. With no `.p3d` yet (a fresh `/dayz-new-mod` scaffold), it says so and opens Object Builder with no model. With several, it lists the first 20 (plus a count of the rest) and asks for `--file`.
   - Neither: no argument; Object Builder opens its last-used file.
3. Locates `ObjectBuilder.exe` via DayZ Tools.
4. Verifies the registry has been populated by `/dayz-setup-objectbuilder` (with that skill's own check, loaded from its `setup.py`), and fails with a hint if not.
5. Refuses if `ObjectBuilder.exe` is already running (checked with `tasklist`, using `/dayz-setup-objectbuilder`'s own check) and tells you to switch to that window, so a second instance never opens on the same `.p3d`. If `tasklist` itself fails, it prints a `[WARN]` and carries on as if Object Builder were not running.
6. Spawns `ObjectBuilder.exe` detached, with working directory `<DayZ Tools>\Bin\ObjectBuilder\`, so the shell returns immediately. The window may take a few seconds to appear.
7. Watches the new process for about a second. If it has already exited, the skill reports a failure with its exit code (exit 1) instead of printing "launched".

## How to run

**Just open the editor:**
```cmd
python "<skill-dir>\launch.py"
```

**Open a specific .p3d:**
```cmd
python "<skill-dir>\launch.py" --file P:\MyMod\data\model.p3d
```

**Open a mod's model:**
```cmd
python "<skill-dir>\launch.py" --mod MyMod
```
(Requires `P:\MyMod\`, typically created by `/dayz-new-mod`. Opens the one `.p3d` anywhere under it, or the editor with no model when there is none yet. With several, use `--file`.)

## When to run

- Anytime you need to inspect or edit a `.p3d` model.
- After `/dayz-new-mod` produced a scaffold and you want to drop a model into `data/`.
- Before adding LODs, named selections, or memory points to a custom asset.

## Output

```
DayZ Object Builder launcher

DayZ preflight

[OK]    P:\ is mounted
[OK]    DayZ Tools found: C:\...\steamapps\common\DayZ Tools
[OK]    Vanilla data found: P:\dz
[OK]    P:\Mods -> C:\...\steamapps\common\DayZ\!Workshop

Preflight complete.

[OK]    ObjectBuilder.exe: ...\Bin\ObjectBuilder\ObjectBuilder.exe
[OK]    Registry configured
[INFO]  Opening: P:\MyMod\data\model.p3d

[OK]    Object Builder launched (PID 12345). The window may take a few seconds to appear.
```

## Flag rules

- `--file` and `--mod` are mutually exclusive (argparse rejects both together); pass one or neither.
- `--file` takes an absolute path, or a relative one. A relative path is tried under the project root first, then under the current folder, and the first that exists wins; if neither exists, the error names both. The root is found the way the other DayZ skills find it (`/dayz-init`'s `find_project_dir()`): `CLAUDE_PROJECT_DIR`, else the nearest folder at or above the current one that holds the `/dayz-init` project cache, else the clone that holds the skill scripts when that clone has the cache, else the current folder. So `--file data\model.p3d` works both from the project root (`data\model.p3d` there) and from `workspace\<ModName>\` (its own `data\model.p3d`). Warns if the extension isn't `.p3d` (Object Builder may refuse it).
- `--mod` is just the mod name; the skill opens the single `.p3d` anywhere under `P:\<ModName>\`, or the editor with no model when there is none. Fails, right after preflight, if the name breaks the naming rule, names a vanilla or reserved `P:\` folder (for example `--mod DZ`; pass a vanilla model with `--file` instead), or the folder isn't there. With more than one `.p3d` it lists up to 20 of them, then how many more there are.

## Why detached

The editor is spawned detached (shared `DETACH_FLAGS` in `_shared/skill_helpers.py`) so the terminal returns at once and closing it doesn't kill Object Builder; the printed PID identifies the process.

## Do not

- Don't run before `/dayz-setup-objectbuilder` on a fresh machine — the skill will tell you to run setup first.
- Don't rely on a relative `--file` when the same relative path exists under both the project root and the current folder: the project root's copy wins. Pass an absolute path to be sure which model opens.
- Don't try to open a second instance: the skill refuses while `ObjectBuilder.exe` is running. Switch to the open window, or close it and re-run.
