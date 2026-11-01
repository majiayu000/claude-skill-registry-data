---
name: dayz-conflict-check
description: "Compares a mod with other mods under P:\\Mods (CF, COT and Expansion by default) and reports prefix, path and class name collisions with file:line, owner and fix. Use before releasing a mod that runs beside CF, COT or Expansion."
argument-hint: "<ModName> [--against MOD ... | --all] [--ingame [--server <instance>]] [--json] | --mod-dir <folder> [--json]"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-conflict-check

A script reads your mod and the other mods and lists every name and path you share with them: `$PBOPREFIX$` and path collisions, shared `CfgPatches` and config class names, script classes declared twice, and modded classes both mods override (see Rules). It reads only unpacked configs and scripts and PBO headers, and never extracts or copies another mod. `--ingame` then runs `/dayz-gate ingame` with those mods loaded. It starts no process unless you add `--ingame`. A default run takes about a second and `--all` against a full mods folder about 15 seconds. When your mod and an unpacked mod define the same config class, it also reads the vanilla class names from `P:\DZ\` once, which adds about 4 seconds, and prints `reading vanilla config classes from P:\DZ ...` to stderr first. The AI only reads the findings and hands each one to its owner.

Follow `skills/_shared/dayz-conventions.md`.

## How to run

```cmd
python "<skill-dir>\conflict_check.py" <ModName> [--against MOD ... | --all] [--json]
python "<skill-dir>\conflict_check.py" --mod-dir <folder> [--against MOD ... | --all] [--json]
python "<skill-dir>\conflict_check.py" <ModName> --ingame [--server <instance>] [--port N] [--json]
```

| Argument | Notes |
|---|---|
| `<ModName>` | A mod under `workspace/<ModName>/` in the project cached by `/dayz-init`. |
| `--mod-dir` | Check any folder instead. Its name is the mod name unless `<ModName>` is given too. |
| `--against` | The mods to compare with, in load order: names under the mods folder (`CF` or `@CF`) or folder paths, such as an unpacked mod source on `P:\`. An entry that is absolute or holds a `/` or `\` is a path, relative to the current folder. A bare word is a mod name first, and a folder in the current folder only when the mods folder has no such mod. |
| `--all` | Compare with every `@mod` under the mods folder. When `@DayZ-Expansion-Bundle` is there the separate `@DayZ-Expansion-*` parts are skipped, as in the default run. |
| `--mods-root` | The folder that holds the `@mods`. Default `P:\Mods`. When it is missing, every run that needs it stops with `ERROR` and `mods folder <path> not found (is P:\ mounted?)`; only an `--against` list made of paths runs without it. |
| `--ingame` | After the scan, run `/dayz-gate ingame <ModName> --deps <the same mods>`. Needs a built PBO and a server from `/dayz-add-server`. Every compared mod must be an `@mod` under the mods folder, so a source folder in `--against` is refused with `ERROR`. |
| `--server`, `--port` | `--ingame` only: the test instance (default `chernarus`) and port (default `2302`). |
| `--json` | Print the full report as JSON after the verdict line. |

With no `--against` or `--all` it compares with `@CF`, `@Community-Online-Tools` and the Expansion mods that are there. When `@DayZ-Expansion-Bundle` is there it is used alone, since it holds every Expansion part; otherwise each `@DayZ-Expansion*` folder is used, Core first. Your own `@<ModName>` is never compared with itself.

## What it reads, and what it never does

- **Your mod:** `$PBOPREFIX$`, every `config.cpp` and every `.c` file under the mod folder.
- **A packed mod:** only the header of each `.pbo` in its `Addons` folder: the `prefix` and the list of file names. The packed data after the header is never read, so their config and script classes are not compared, and a clean result is `PARTIAL`, not `PASS`. `--ingame` covers those at run time. CF, COT and Expansion from the Workshop are all packed, so a default run without `--ingame` ends in `PARTIAL` or `FAIL`.
- **An unpacked mod:** an addon folder inside `Addons` that holds a `config.cpp`, or a source folder passed to `--against`. Its `$PBOPREFIX$`, `config.cpp` and `.c` files are read for names only.
- It never extracts a PBO, never writes to another mod's folder and never copies their files or code. The report holds class names, prefixes and paths, nothing else.

## Rules

Errors fail the check. Warnings are listed and do not.

| Rule | Severity | Finds |
|---|---|---|
| `prefix-same` | error | Your `$PBOPREFIX$` is the prefix of one of their addons. |
| `prefix-nested` | warning | One prefix sits inside the other, so the two can ship the same path. |
| `path-collision` | error | A file of yours has the same game path (prefix plus file) as one of theirs. |
| `cfgpatches-collision` | error | A `CfgPatches` class with the same name as one of theirs. |
| `class-collision` | error | A class one level inside a `Cfg` section (such as `CfgVehicles`) that they define too, when you do not require them. |
| `class-override` | warning | The same, but one of their `CfgPatches` classes is in your `requiredAddons[]`, so you change their class on purpose. |
| `vanilla-class-overlap` | warning | Both mods change a vanilla class: vanilla defines that name in the same `Cfg` section, read from `P:\DZ\`. The mod loaded last wins each property it sets. The same name in another section (a `CfgAmmo` class named after a vanilla `CfgWeapons` class) is a `class-collision`. |
| `script-class-collision` | error | A script `class` or `enum` they declare too. The scripts would not compile together. |
| `modded-class-overlap` | warning | A `modded class` both mods override. Each override must call `super` or the other mod loses its code. |
| `script-name-match` | warning | Their PBO header lists a `.c` file named after one of your classes, so they may declare or mod it too. |

Names are compared without case. Comments, strings and preprocessor lines are skipped. Forward declarations such as `class Clothing;` are not definitions.

## Output and exit codes

The first line on stdout is the verdict (the vanilla progress line goes to stderr, so `--json` output stays parseable):

| Verdict | Exit | Means |
|---|---|---|
| `PASS` | 0 | No error (warnings allowed), and every compared mod had its classes compared: each was unpacked, or `--ingame` loaded them all and the gate passed. |
| `PARTIAL` | 0 | No error found, but at least one mod was read from PBO headers only, so its config and script classes were not compared. The next line names those mods and says to run again with `--ingame`. Do not report this as a pass. |
| `FAIL` | 1 | At least one error, or the in-game gate did not pass. |
| `ERROR` | 2 | The check could not run: bad or unknown arguments (the message carries the usage line), no cached project, no mod folder, a mods folder that is not there, an `--against` mod that is not there, an `--against` source folder with `--ingame`, or no mods to compare with. The last message says why: the only mod given is your own, `--all` found no `@mod`, or none of CF, COT or Expansion is there. |

When some mods were header-only, the line under the verdict says so. Then one block per finding:

```
FAIL
  not a full check: @CF read from PBO headers only (prefixes, paths and script file names), so their config and script classes were not compared. Run again with --ingame to check them.
- workspace/MyVest/config.cpp:3  error cfgpatches-collision: CfgPatches class DayZExpansion_Core is also declared by @DayZ-Expansion-Core.
    theirs: @DayZ-Expansion-Core/Addons/core/config.cpp:1
    -> dayz-config-specialist: Rename the CfgPatches class to a name only your mod uses, such as <ModName>_<Part>.
  scanned @CF: 3 PBO header(s), 0 unpacked addon(s)
  scanned @DayZ-Expansion-Core: 0 PBO header(s), 1 unpacked addon(s)
  1 error(s), 0 warning(s)
```

With `--json` each finding has `rule`, `severity`, `mod` (theirs), `where` (yours, `file:line`), `other` (theirs), `message`, `owner` and `fix`, `scanned` lists each compared mod with its PBO header count, unpacked addon count and any `.pbo` whose header could not be read, `header_only` names the mods with no unpacked addon, and `note` holds the not-a-full-check line. A bad-argument `ERROR` with `--json` is `{"verdict": "ERROR", "error": ...}` like every other refusal. With `--ingame` the report gains `"ingame": {"deps", "server", "rc", "verdict", "report"}`, where `report` is the `/dayz-gate ingame` JSON.

## Limits

- Packed mods give only prefixes, paths and script file names. A `script-name-match` is a hint from a file name, not proof; `--ingame` gives the real answer.
- Classes are compared one level inside each `Cfg` section. Nested classes and `#include` files are not followed.
- Two of their mods are never compared with each other; only your mod with each of them.
- Without `P:\DZ\` a vanilla class both mods change is reported as `class-collision` or `class-override`, and the note says so.

## Do not

- Don't extract, unpack or copy another mod to get more out of this check. Use `--ingame`, or ask the user for that mod's source.
- Don't rename another mod's classes. Fix your own mod.
