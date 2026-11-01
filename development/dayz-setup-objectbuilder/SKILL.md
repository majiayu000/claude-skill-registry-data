---
name: dayz-setup-objectbuilder
description: "Configures Object Builder (DayZ Tools' .p3d editor) by importing DayZ Tools' default registry settings and preferred view flags. Use when Object Builder is opened for the first time on a machine, after a DayZ Tools reinstall, or when it opens with broken panel layouts."
argument-hint: "[--no-prefs] [--force [--yes]]"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-setup-objectbuilder

One-time configuration of Object Builder. Bohemia ships a `.reg` file with sensible defaults (window layouts, panel positions, render flags) but doesn't auto-import it — without this step, Object Builder runs from a blank `HKCU\Software\Bohemia Interactive\DayZ Tools\Object Builder` tree and looks broken on first open.

Follow `skills/_shared/dayz-conventions.md`.

## What it does

1. Gates on `/dayz-preflight`.
2. Locates DayZ Tools via the shared `find_dayz_tools()` resolver.
3. Verifies these exist:
   - `Bin\ObjectBuilder\ObjectBuilder.exe`
   - `Bin\ObjectBuilder\ObjectBuilder_defaultSettings.reg`
4. Checks `HKCU\Software\Bohemia Interactive\DayZ Tools\Object Builder\CConfig` for an existing config.
5. If `CConfig` is missing (or with `--force`, after confirmation): checks that every key the `.reg` touches is under `HKEY_CURRENT_USER` (refuses otherwise, before touching the registry). Then, whenever the parent Object Builder key already exists, it runs `reg export` on it to `.claude/local-memory/objectbuilder-backup-<YYYYMMDD-HHMMSS>.reg` in the project and prints that path; nothing is imported if the export fails.
   - **Partial tree** (parent key present, `CConfig` missing, with or without `--force`): the defaults are merged over the existing key with no confirmation and no delete, so saved `MainFrame-*` layouts and `HistoryPaths` stay.
   - **Forced reset** (`--force` with `CConfig` present): the key is deleted with `reg delete ... /f` (stops if that fails) so the import starts from an empty tree.
   - **Empty registry**: there is nothing to back up, so the defaults are imported straight away.

   It then runs `reg import` on the `.reg` and verifies `CConfig` now exists. If that import fails or `CConfig` is still missing, and a backup was taken, it clears the key, imports the backup, and reports whether your previous settings came back (if that restore also fails, it prints the `reg import` command to run by hand).
6. Unless `--no-prefs` is given, sets four preferred flags under `CConfig`, writing only the ones not already on: View background LOD, background LOD in the 3D preview, background LOD in the UV editor (all `"1"`), and Direct3D renderer by default (`"On"`). If `CConfig` cannot be opened for writing or a write fails, it prints a `[FAIL]` line with the Windows error and exits 1.

## How to run

**First time (or after a fresh DayZ Tools reinstall):**
```cmd
python "<skill-dir>\setup.py"
```

**Keep your own flag choices (for example Direct3D turned off after a GPU or driver crash):**
```cmd
python "<skill-dir>\setup.py" --no-prefs
```
Without `--no-prefs`, every run turns the four flags back on. Use `--no-prefs` on every later run once you have switched one off on purpose.

**Force re-import (resets Object Builder to factory defaults — wipes any custom panel layout you've saved):**
```cmd
python "<skill-dir>\setup.py" --force
```

On an already-configured machine `--force` asks `[y/N]`, backs up the current settings, deletes the whole Object Builder key (including saved `MainFrame-*` toolbar layouts, `HistoryPaths` recent files, and any value the shipped `.reg` doesn't set), then imports the defaults into the empty tree. `--force` only resets a key that already has `CConfig`: on a partial tree (Object Builder key present, `CConfig` missing) it changes nothing, and the defaults are merged over the saved values after a backup, exactly as without `--force`. If importing the defaults fails, it restores the backup on its own. To undo a reset that succeeded, run `reg import` on the backup file it printed. The backup goes to `.claude/local-memory/` in the project that `/dayz-init` resolves (`CLAUDE_PROJECT_DIR`, else the nearest folder at or above the current one with the `/dayz-init` cache, else the clone that holds the skill scripts when that clone has the cache), so running from a mod subfolder still lands it in the project. Without a terminal (an agent's Bash call) it refuses unless `--yes` is also given, so get the user's go-ahead first and then run `--force --yes`. `--no-prefs` combines with `--force`.

Exits 1 if DayZ Tools, `ObjectBuilder.exe` or the `.reg` is missing, Object Builder is running or `tasklist` cannot tell whether it is (it writes its settings back to the registry when it closes, so close it first), the `.reg` touches a key outside `HKEY_CURRENT_USER`, the reset is not confirmed, the backup export or the key delete fails, `CConfig` is still missing after import, or the preferred flags cannot be written; a failed `reg import` returns its own exit code. Both import failures keep their exit code after an automatic restore, because the import itself did not happen.

## When to run

- After installing DayZ Tools for the first time on a machine.
- After reinstalling DayZ Tools (Steam may have wiped the registry tree).
- If Object Builder opens with floating panels everywhere and weird defaults.

## Output

```
DayZ Object Builder setup

DayZ preflight

[OK]    P:\ is mounted
[OK]    DayZ Tools found: C:\...\steamapps\common\DayZ Tools
[OK]    Vanilla data found: P:\dz
[OK]    P:\Mods -> C:\...\steamapps\common\DayZ\!Workshop

Preflight complete.

[OK]    DayZ Tools: C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools
[OK]    ObjectBuilder.exe: ...\Bin\ObjectBuilder\ObjectBuilder.exe
[OK]    Default settings file: ObjectBuilder_defaultSettings.reg
[INFO]  Registry empty — importing defaults.
[INFO]  Running: reg import ...\ObjectBuilder_defaultSettings.reg
[OK]    Registry imported successfully.

[INFO]  Applying preferred Object Builder defaults (skip with --no-prefs):
[INFO]  View > Background LOD: turned on
[OK]    Background LOD shown in 3D preview pane: already on
...
[INFO]  1 of 4 preferences changed.

[OK]    Object Builder is ready. Launch with: /dayz-launch-objectbuilder
```

On an already-configured machine the import is skipped (`[OK] Registry already configured ...`), but the preference step still runs and turns on any of the four flags that were switched off in Object Builder since the last run, unless `--no-prefs` is given (`[INFO] --no-prefs: preferred flags left as they are.`).

## Why a registry import (and why it's safe)

Object Builder is an old MFC-based Windows tool — its config lives entirely under `HKEY_CURRENT_USER\Software\Bohemia Interactive\DayZ Tools\Object Builder`. The shipped `.reg` file writes window/panel/toolbar defaults into that tree. It's **HKCU-only** (the script verifies this before every import), so:

- No Administrator elevation needed.
- Only affects the current Windows user.
- Reversible: any import over an existing Object Builder key (a forced reset or a partial tree) saves a backup `.reg` first, and you can `reg import` it to get your layout back. The four preferred flags are re-applied on every run without `--no-prefs`.

## Do not

- Don't run as Administrator unless the non-elevated import fails. The `.reg` writes to HKCU, not HKLM.
- Don't edit the `.reg` file in DayZ Tools install — Steam will overwrite it on update. If you want custom defaults, save a layout from inside Object Builder; it persists in the same registry tree but in `MainFrame-*` subkeys you don't need to touch directly.
