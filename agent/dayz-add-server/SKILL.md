---
name: dayz-add-server
description: "Sets up an isolated DayZ test server instance under .server/<instance>/ with its own mission copy, serverDZ.cfg and profiles. Use when you need a new test instance before /dayz-launch-test (for example chernarus or chernarus-hardcore), or to refresh the mission after a DayZ update."
argument-hint: "<instance> [--map <name>] [--refresh-mission]"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-add-server

Set up a self-contained test server instance for local DayZ mod testing. Each instance lives under `.server/<instance>/` and owns its mission copy, server config, and server logs. Client diag logs are shared across instances at `.server/!ClientDiagLogs/`. Run as many instances as you want, including multiple variants of the same map.

This is the **setup** half of the test loop. `/dayz-launch-test` is the **run** half, and refuses to run for an instance you haven't added yet.

Follow `skills/_shared/dayz-conventions.md`.

## How to run

```cmd
python "<skill-dir>\add_server.py" <instance> [--map <name>] [--refresh-mission]
```

| Argument | Required? | Notes |
|---|---|---|
| `<instance>` | yes | Free-form instance name. Becomes the folder name under `.server/`, so it must be a single folder name (no `/`, `\`, `:`, `..`, or any of the characters Windows forbids in file names, such as `*`, `?` and `"`). It must contain at least one letter or digit, because the server's six character `shardId` is built from them. Examples: `chernarus`, `chernarus-hardcore`, `loot-test`, `livonia-pvp`. |
| `--map` | no | Map alias (`chernarus`, `livonia`, `sakhal`, `nasdara`) or full mission template folder name (e.g. `dayzOffline.namalsk`). It must be a single folder name, with the same rules as `<instance>`, because it is joined into the DayZ Server `mpmissions` path and the junction path under `.server/<instance>/`. When omitted, `<instance>` is used as the map alias if it matches a known one; otherwise the skill fails and asks for `--map`. |
| `--refresh-mission` | no | Re-copy the mission folder from the DayZ Server install. The current `mission/` is first renamed to `mission.bak-<YYYYMMDD-HHMMSS>/` so your edits stay recoverable. Use after a DayZ update brings new mission content. Without this flag, an existing mission folder is left alone. |

## What it does

1. **Project check**: reads the cached project folder; halts if none is cached (run `/dayz-init`).
2. **Preflight gate**: runs `/dayz-preflight`; halts on non-zero.
3. **Old-layout gate**: refuses if `workspace/_server/` still exists. Delete the folder manually; that layout is no longer supported.
4. **Resolve map and mission template**: turns the instance name and `--map` flag into the canonical mission folder name via the alias table. If the instance already has a `serverDZ.cfg` whose active `template = "..."` line names a different template, the skill refuses before copying anything (see Refuses to run if).
5. **Mission copy**: if `.server/<instance>/mission/` doesn't exist or is empty (or `--refresh-mission` was passed), copies it from `<DayZServer>/mpmissions/<template>/`. An empty folder is removed and reported as `Copied`. The copy goes into a temporary `mission.tmp-<timestamp>/` folder first and is moved to `mission/` only once it is complete, so a failed or interrupted copy (including Ctrl+C) never leaves a partial mission behind. A `mission.tmp-*` folder left by a crashed older run is reported with a `[WARN]` line naming it; delete it by hand. With `--refresh-mission`, the existing mission folder is renamed to `mission.bak-<timestamp>/` only after the new copy succeeded; nothing is deleted. The copy is always named `mission/`, and it holds a small `.agentic-z-template` file recording which template it was copied from (a backup keeps its own). When `mission/` is already present and `--refresh-mission` was not passed, the skill checks that it came from this run's template, using that file, or for a mission copied before the file existed, the `<template>/` junction pointing at it. A mission with neither (filled in by hand) is accepted as it is.
6. **Instance directory**: ensures `.server/<instance>/` exists with:
   - `serverDZ.cfg`: default config pointing at the right mission template, with `allowFilePatching = 1;` and a `shardId` made of the first six letters and digits of the instance name (padded with `shard0`). An existing config is preserved, except that `allowFilePatching = 1;` is appended if no active line exists (a commented-out line does not count) or set back to `1` if it holds any other value. A config saved in an ANSI editor (for example an accented hostname) is read and written byte for byte, so those characters survive. `/dayz-launch-test` refuses to start without that line, so rerunning this skill is the fix.
   - `Profiles/`: server-side `-profiles=` dir (RPT, script.log, BattlEye state). Per-instance.
   - `<template>/` (for example `dayzOffline.chernarusplus/`): a junction to `mission/`. The engine looks the mission up by template name during the client connect handshake; without it the client connects but never spawns. The skill checks the link itself and its target, not only whether the target exists. A junction that already points at this instance's `mission/` is reported as `[OK]    Junction <template>/ -> mission/ already present`. A junction that dangles or points somewhere else (for example after you moved or renamed the project folder, or copied it to a second clone) is removed and recreated, with a `[WARN]  Removed stale junction ...` line naming the old target. Removing a link never touches the folder it pointed at. If `mklink` fails, the skill exits non-zero. After a map switch, a junction to `mission/` named after the old template is removed (`[OK]    Removed junction <old template>/ left from the previous mission template`); links to anything other than `mission/` are left alone.
7. **Shared client log dir**: ensures `.server/!ClientDiagLogs/` exists; this is the client-side `-profiles=` dir, shared across all instances.

## Refuses to run if

- No project is cached (run `/dayz-init`).
- `/dayz-preflight` returns non-zero.
- `workspace/_server/` still exists. Delete it manually; the legacy layout is no longer supported.
- DayZ Server install isn't found AND the mission isn't already in `.server/<instance>/mission/`. (Install DayZ Server free from Steam appid 223350 for the initial copy. Once the mission is local, DayZ Server is no longer required.)
- `<instance>` contains a path separator, a drive colon, one of `* ? " < > |`, or is `.`/`..` (argparse rejects it, exit 2).
- `<instance>` starts with `!` (reserved for shared `.server` folders such as `!ClientDiagLogs` and `!Health`) or ends in `-behavior` (reserved for `/dayz-gate` behavior copies). Argparse rejects it, exit 2.
- The instance already exists and its `serverDZ.cfg` `template = "..."` line names a different mission template than this run resolved (for example `chernarus` rerun with `--map livonia`). Add a new instance for the other map, or set the `template =` line yourself and rerun with `--refresh-mission` to swap the mission (the old one is kept as a backup).
- `mission/` was copied from a different template than this run resolved and `--refresh-mission` was not passed (for example you set `template = "dayzOffline.enoch";` but forgot the flag). Without this check the old map's mission would be junctioned under the new name and loaded. Rerun with `--refresh-mission`.
- `.server/<instance>/mission` is a file or a broken link instead of a folder. The skill will not delete it; move it out and rerun.
- `<instance>` isn't a known map alias and `--map` wasn't given. (We have no way to guess the mission template from a free-form name.)
- DayZ Server install lacks the requested mission template (e.g. `--map dayzOffline.namalsk` but DayZ Server doesn't ship namalsk; either provide the mission manually under `.server/<instance>/mission/` or correct the name).
- The `<template>/` junction to `mission/` cannot be created (the `mklink` error is printed), or a stale junction there cannot be removed.
- `.server/<instance>/<template>` is a real folder or file instead of a junction. The skill will not delete it, because it may hold your data. Move it out of the instance folder and rerun.
- `--refresh-mission` cannot rename `mission/` to its backup, usually because a running server or an open editor holds it. Stop the session with `/dayz-stop-test`, close the files and rerun; nothing is changed.
- Copying the mission from the DayZ Server install fails partway (disk full, antivirus lock, Steam updating DayZ Server). The partial copy is deleted, the existing `mission/` is left untouched, and the skill exits non-zero. If the finished copy cannot be moved into `mission/` (for example an empty `mission/` that another program holds open, or a locked folder after the old one was backed up), the copy is deleted and the skill exits non-zero; when a backup was made, the message names the `mission.bak-<timestamp>/` folder to rename back.

## Output

```
DayZ preflight
... (preflight output)
Preflight complete.

[OK]    Project: C:\Projects\MyDayZProject
[OK]    Instance: chernarus-hardcore  (map: chernarus, mission: dayzOffline.chernarusplus)
[OK]    Copied .server\chernarus-hardcore\mission  (from DayZ Server install)
[OK]    Wrote default .server\chernarus-hardcore\serverDZ.cfg
[OK]    Junction dayzOffline.chernarusplus/ -> mission/ (template handshake)
[OK]    .server\chernarus-hardcore\Profiles ready
[OK]    .server\!ClientDiagLogs ready

Instance 'chernarus-hardcore' is ready. Next:
  /dayz-build-pbo <ModName>
  /dayz-launch-test <ModName> --server chernarus-hardcore
```

On a rerun with everything already set up, the changed lines read:

```
[OK]    Mission already present: .server\chernarus-hardcore\mission
[OK]    .server\chernarus-hardcore\serverDZ.cfg unchanged (already configured)
[OK]    Junction dayzOffline.chernarusplus/ -> mission/ already present
```

## Editing what this skill creates

- **Mission folder** at `.server/<instance>/mission/` is yours to edit. The server runs with `-filePatching` so edits to `init.c`, `cfggameplay.json`, `db/types.xml`, etc. are live on the next launch.
- **`serverDZ.cfg`** at `.server/<instance>/serverDZ.cfg` is yours to tune (max players, persistence, etc.). The skill never overwrites your edits, except `allowFilePatching`: it is re-added if you remove it and set back to `1` if you change it (without it, clients launched with `-filePatching` can't connect).

## Do not

- Don't edit missions inside the DayZ Server Steam install; edit the instance copy at `.server/<instance>/mission/`.
- Don't move `.server/` into `workspace/`. The split is deliberate: `workspace/` is for active mod sources, `.server/` is for runtime artifacts.
