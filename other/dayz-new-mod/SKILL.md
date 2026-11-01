---
name: dayz-new-mod
description: "Scaffolds a brand-new DayZ mod under workspace/<ModName>/ (config.cpp, $PBOPREFIX$, script folders, Workbench gproj), links it at P:\\<ModName>\\ and makes it the active /dayz-init project. Use when starting a new mod; use /dayz-import-mod for a folder elsewhere and /dayz-add-scaffold to fill gaps."
argument-hint: "<ModName> [--author \"YourHandle\"] [--project \"<folder>\"]"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-new-mod

Create a new DayZ mod project under `workspace/<ModName>/` in the current project: `CLAUDE_PROJECT_DIR`, else the nearest folder at or above the working directory (below the home folder) that holds a `/dayz-init` project cache, else the clone that holds the skill scripts when that clone has the cache, else the working directory. This is the same lookup every DayZ skill uses; it does not require the cache, because this skill writes it. `--project "<folder>"` replaces the lookup. When the lookup lands on the working-directory fallback, that folder is used only if it is the clone holding the skill scripts or already has a `.claude` or `workspace` folder; otherwise the skill refuses, names the folder it would have used, and writes nothing. This stops a first run from a shell that starts outside the clone from creating the mod, the `P:\` link and the project cache in the wrong folder. Gates on `/dayz-preflight` like every DayZ skill, so it refuses to run when `P:\` is not mounted. The checks that read only the command line and the project folders (the project folder, the mod name and an existing `workspace/<ModName>/`) run just before preflight, so they refuse before anything on disk changes.

Follow `skills/_shared/dayz-conventions.md`.

## How to run

```cmd
python "<skill-dir>\new_mod.py" <ModName> [--author "YourHandle"] [--project "<folder>"]
```

| Argument | Required? | Notes |
|---|---|---|
| `<ModName>` | yes | Folder name and `CfgPatches` class name. Must start with a letter; letters, digits, underscores only; max 64 chars. |
| `--author` | no | Author handle written into `config.cpp` and cached for future runs once the scaffold succeeds. If omitted, the skill checks the cache, then prompts interactively, then fails. |
| `--project` | no | Project folder that holds (or will hold) `workspace/`. Must exist. Use it when the shell starts outside the project and the skill refuses with `No DayZ project found`. |

## Author handle resolution

First hit wins:

1. `--author "Name"` flag — also cached for next time.
2. Cached value at `.claude/local-memory/dayz-author.txt` (per-clone, gitignored).
3. Interactive prompt if stdin is a TTY — also cached for next time.
4. Hard fail with instructions otherwise. The prompt reading an empty answer or end-of-file fails the same way (a null stdin, such as an agent's PowerShell tool, can report itself as a TTY); the message names `--author` and the cache file.

The cache is written only after the scaffold and the `P:\<ModName>\` link both succeed, so a refused or failed run (existing folder, foreign link, junction error) never replaces your cached handle.

The handle is written inside quoted strings in `config.cpp`, so a handle containing `"` or a line break is refused wherever it comes from (flag, cache or prompt).

To change your handle later: pass `--author "NewHandle"` when you scaffold your next mod, or edit / delete `.claude/local-memory/dayz-author.txt`.

## What it creates

```
workspace/<ModName>/
├── config.cpp                 # CfgPatches + CfgMods stub, no content classes yet
├── $PBOPREFIX$                # contains: <ModName>
├── README.md                  # light onboarding notes
├── scripts/
│   ├── 3_Game/.gitkeep
│   ├── 4_World/.gitkeep
│   └── 5_Mission/.gitkeep
├── data/.gitkeep
├── gui/.gitkeep
└── workbench/
    ├── dayz.gproj             # vanilla project file + this mod's script paths
    └── DayZSetting.xml        # vanilla Workbench settings
```

### The `workbench/` folder

Open this mod in Workbench via `/dayz-launch-workbench --mod <ModName>` (it loads `workbench/dayz.gproj`). The gproj is a copy of the official `dayz.gproj` shipped with DayZ Tools (`Bin\Workbench\`), with this mod's script paths injected into the `game`/`world`/`mission` modules so Workbench compiles and lints vanilla + your mod together — same as the engine does at runtime. Its single `FileSystem` entry is replaced with two mounts, `P:/` and `P:/<ModName>/`.

The `[OK] workbench/dayz.gproj written (mod paths + filesystem mounts injected)` line prints only when all three module paths and the two mounts went in. If a future DayZ Tools gproj has a `game`, `world` or `mission` module without a `Paths { }` block, that module gets no path (it never spills into the next module) and a `[WARN]` names the module and the path to add by hand. If it has no single-entry `FileSystem` block, the block is left unchanged and a `[WARN]` says to add the two entries by hand. Either case ends with `[WARN] workbench/dayz.gproj written, but fix the pieces above by hand before opening Workbench` instead of the `[OK]` line.

If DayZ Tools isn't installed when you run `/dayz-new-mod`, or it is installed but `Bin\Workbench\dayz.gproj` is missing, the folder is still created (with a README placeholder) but the `.gproj`/`.xml` are skipped with a warning; once Tools is installed or repaired, run `/dayz-add-scaffold <ModName> --piece workbench` to add them.

Plus a directory junction:

```
P:\<ModName>\  -> workspace/<ModName>/   (symlink, falls back to junction on Windows)
```

The `config.cpp` stub registers the three Enforce Script modules (3_Game, 4_World, 5_Mission) so script files dropped into those folders are loaded automatically. No `CfgVehicles` / `CfgWeapons` / `CfgMagazines` entries — add those when you have content to declare.

### Why the P:\ junction

DayZ Tools' AddonBuilder reads source folders from `P:\` and resolves `$PBOPREFIX$` relative to it. Our convention keeps source under `workspace/<ModName>/` (under git, in your editor of choice), but the engine and Tools expect to see it at `P:\<ModName>\`. Creating the junction at scaffold time means:

- You edit files in `workspace/<ModName>/` like any normal repo file.
- AddonBuilder, the engine, and any DayZ tooling see them at `P:\<ModName>\` automatically.
- `dayz-build-pbo` doesn't need to manage the junction — it just verifies it exists.
- No copies, no de-sync.

Junctions don't require admin; symlinks do (Windows only creates them automatically when Developer Mode is on or the process is elevated). The skill tries symlink first, falls back to junction.

### Project cache

After the junction is created, the skill points the `/dayz-init` project cache at this project. `/dayz-build-pbo`, `/dayz-deploy-pbo`, `/dayz-launch-test` and `/dayz-clean-workspace` follow that cache, so scaffolding here makes this the active project. When the cache pointed at a different project, the skill prints `[WARN] Project cache repointed: <old> -> <new>`. It also records the new mod as the active mod (`last_intent.mod_name` in `.claude/local-memory/dayz-init-state.json`, the same record `/dayz-init` writes) and prints `[OK] Active /dayz-init mod: <ModName>`, so the `/dayz-init` hub and its build and launch defaults act on the new mod, not the one active before. Other keys in that file are kept. If the file cannot be read as a JSON object, it is first copied to `dayz-init-state.<timestamp>.bak.json` beside it and a `[WARN]` names the backup; the new file then holds only `last_intent`.

## Refuses to run if

Checked in this order. The scaffold, the link and both caches are written only after every check passes.

- `--project` names a folder that does not exist, or (without `--project`) the project lookup fell back to a working directory that is not the clone holding the skill and has no `.claude` or `workspace` folder. The message names that folder.
- `<ModName>` fails the name pattern.
- `workspace/<ModName>/` already exists (won't clobber an in-progress project).
- `/dayz-preflight` returns non-zero (typically `P:\` not mounted) — its exit code is propagated.
- No author handle is available and stdin is not a TTY, or the prompt reads an empty answer or end-of-file.
- The author handle contains `"` or a line break.
- `P:\<ModName>\` exists as a real folder (won't clobber non-link content).
- `P:\<ModName>\` exists as a link pointing somewhere other than `workspace/<ModName>/` (won't redirect a junction the user set up for a different project).

### Stale-junction auto-clean

If `P:\<ModName>\` exists as a junction or symlink whose target is the about-to-be-scaffolded `workspace/<ModName>/` (typically because a prior scaffold's workspace folder was deleted but the junction wasn't), the skill removes the stale link automatically and proceeds. This handles the common cleanup case where you `rm -rf workspace/<ModName>/` to start over.

If writing the scaffold fails partway or is interrupted with Ctrl+C, or junction creation fails or is interrupted afterwards (permission error, filesystem weirdness), the new `workspace/<ModName>/` folder is removed and the run exits non-zero, so you can retry cleanly. A link an interrupt left behind points at the removed folder, and the next run removes it as a stale junction. A junction failure shows `mklink`'s own message (for example `Access is denied.`).

## Output

```
DayZ preflight

[OK]    P:\ is mounted
...     (rest of the /dayz-preflight report)

Preflight complete.
[OK]    Created workspace\MyMod\
[OK]    config.cpp written (author: YourHandle)
[OK]    $PBOPREFIX$ written
[OK]    Skeleton folders created
[OK]    README.md written
[OK]    workbench/dayz.gproj written (mod paths + filesystem mounts injected)
[OK]    workbench/DayZSetting.xml copied
[OK]    P:\MyMod junction -> workspace\MyMod
[OK]    Active /dayz-init mod: MyMod
[OK]    Project cache set: C:\...\MyProject

Next steps:
  - Add Enforce Script files under workspace\MyMod\scripts\3_Game (or 4_World, 5_Mission)
  - Add models/textures/materials under workspace\MyMod\data
  - Add UI layouts under workspace\MyMod\gui
  - Open in Workbench: /dayz-launch-workbench --mod MyMod
  - When ready, /dayz-build-pbo to pack and deploy to P:\Mods\@MyMod\Addons\
```

The link line says `symlink` instead of `junction` when Windows allows symlinks (Developer Mode or an elevated shell).

## Do not

- Don't pre-populate `data/` or `gui/` with sample assets — the user adds those when they have real content.
- Don't auto-commit the new project to git. The user decides whether to track it.
- Don't bypass the preflight gate; every DayZ skill follows the same rule, scaffolding included.
