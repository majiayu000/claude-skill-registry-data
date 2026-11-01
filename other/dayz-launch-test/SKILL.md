---
name: dayz-launch-test
description: "Launches a local DayZ Diag server for an instance from /dayz-add-server, then the diag client connected to it with the given built mods loaded. Run-only; does no setup. Use when you want to test built mods in game, or to preview the exact launch commands with a dry run."
argument-hint: "<ModName> [<ModName2> ...] [--server-only <ModName>]... [--server <instance>] [--port N] [--dry-run]"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-launch-test

Run-only: launches a local DayZ test session for one or more built mods. Always starts the **server first**, then the **client** connecting to it (DayZ cannot be tested standalone, per L2 conventions). Both run from `DayZDiag_x64.exe` with `-filePatching` for fast iteration on Enforce Script and config edits.

**Prerequisite:** the instance must have been added with `/dayz-add-server <instance>`, which owns the `.server/<instance>/` layout (mission copy, `serverDZ.cfg`, `Profiles/`, the template junction) and documents how to edit the mission. This skill verifies that state and runs.

Follow `skills/_shared/dayz-conventions.md`.

**Before you launch:** to see every error as you play, start `/dayz-logwatch --until-closed` in the background first (it reads each log from its first line once the file appears), then run this skill.

## How to run

```cmd
python "<skill-dir>\launch.py" <ModName> [<ModName2> ...] [--server-only <ModName>]... [--server <instance>] [--port N] [--dry-run]
```

Name every shared mod first, then the options. `--server-only` takes one name, so repeat it for each server-only mod: `CF MyMod --server-only SrvA --server-only SrvB`. A mod name after an option (`CF --server-only Srv MyMod`, `CF --port 2402 MyMod`) exits 2 with `unexpected arguments: MyMod`, also with `--dry-run`, rather than guessing whether it was meant shared or server-only.

| Argument | Required? | Notes |
|---|---|---|
| `<ModName> ...` | yes | Mod names loaded on **both** client and server, dependencies first. `CF` and `@CF` name the same mod. A name with a path separator, a drive letter or `..` exits 2 with `is not a mod name`. Each must have at least one `.pbo` at `P:\Mods\@<ModName>\Addons\` (build with `/dayz-build-pbo` first). |
| `--server-only` | no | One mod loaded on the **server only**; repeat the flag for each. Server-only mods are passed, in the order given, with the server's `-serverMod=` switch and never added to either `-mod=` list (mods on `-mod=` are advertised to clients). Use for a mod that self-terminates when it detects itself running outside the dedicated server (e.g. a `CfgMods` server-marker `defines[]` entry guarding a `RequestExit()` call). Same `.pbo`-presence requirement as above. A name given both here and as a shared mod exits 2 with `mod named both as shared and --server-only`, and a name given twice anywhere exits 2 with `mod named more than once`, also with `--dry-run`. Both checks ignore case and a leading `@`, since Windows folder names ignore case (`CF` and `cf` are the same `@CF`). |
| `--server` | no | Server instance to launch on. Default `chernarus`. Must have been added via `/dayz-add-server`. A name with a path separator, a drive letter or `..`, or one starting with `!` (the shared `.server` folders), exits 2 with `is not an instance name` or `is not an instance`. |
| `--port` | no | Server port, 1 to 65535. Default `2302`. Any other value exits 2 with `port must be 1-65535`, also with `--dry-run`. |
| `--dry-run` | no | Run every check, print the resolved server and client commands, then exit 0. Writes nothing of its own (no profile dirs, no display-prefs file, no processes); `/dayz-preflight` may still create the `P:\Mods` junction if it is missing. |

## Mods with dependencies

Name a mod's dependencies before the mod, in load order, for example `/dayz-launch-test CF <ModName> --server <instance>`. The skill joins the names into `-mod=` in the order given and refuses any name with no `.pbo` in `P:\Mods\@<name>\Addons\`. To build the list, take every non-vanilla `requiredAddons` entry in the mod's `CfgPatches` (vanilla ones start with `DZ_`, for example `DZ_AI` in `P:\DZ\AI\config.cpp:3`) and map it to the `@<mod>` under `P:\Mods\` that ships it. If you can't map a dependency to an `@mod`, stop and report it instead of launching without it.

The skill enforces this itself (step 4 below). For each named mod with source under `workspace/<ModName>/`, it reads every `config.cpp` in that folder (skipping `.git`, `Addons` and `Keys`) and collects the non-vanilla `requiredAddons` (written `requiredAddons[] = {...}` or `requiredAddons[] += {...}`). Each one must be a `CfgPatches` class of the mod itself or of a mod named before it; names are compared ignoring case. A mod named earlier that has no readable source (a built mod such as `@CF`) may ship anything, so its presence satisfies the check. A shared mod can rely only on shared mods named before it; a `--server-only` mod can rely on every shared mod and the server-only mods before it. Prebuilt bundles (`workspace/<ModName>/Addons/*.pbo`) and mods with no `workspace/` source are not checked, the same exception `/dayz-gate ingame` makes. A failed check exits 1, also with `--dry-run`:

```
[FAIL]  Required addons are not provided by any mod loaded before the mod that needs them:
          - MyMod requires JM_CF_Scripts
       Name the @mods under P:\Mods\ that ship them before the mod, in load order,
       for example: /dayz-launch-test CF MyMod. Without them the mod fails to load in game.
```

## What it does

1. **Preflight gate**: runs `/dayz-preflight`; halts on non-zero.
2. **Old-layout gate**: refuses if `workspace/_server/` still exists. Delete the folder manually; that layout is no longer supported.
3. **Built-mod check**: for each mod, verifies at least one `.pbo` exists in `P:\Mods\@<ModName>\Addons\`. Fails fast with a hint to run `/dayz-build-pbo` if missing.
4. **Dependency check**: refuses when a mod's non-vanilla `requiredAddons` are not provided by a mod named before it (see "Mods with dependencies").
5. **Diag client resolution**: finds `DayZDiag_x64.exe` via `find_dayz_diag()` (env var, DayZ game install, Steam paths). Both client and server run from this binary; the server adds `-server`. Retail `DayZ_x64.exe` blocks past the loading screen with `-filePatching` enabled, so the client must be diag, and the server runs the same diag binary so both sides match. Retail `DayZServer_x64.exe` is not used.
6. **Instance check**: reads the mission template from the `template = "...";` line in `.server/<instance>/serverDZ.cfg`, confirms the cfg has an active `allowFilePatching = 1;` line (without it the server refuses `-filePatching` clients with error `0x00020005`; a missing line, a commented-out line or any other value counts as missing), and confirms `mission/` and the `<template>/` junction to it exist. The server's `-mission=` points at that junction (the engine resolves the template name during the connect handshake; without it the client connects but never spawns). Anything missing fails with a hint to run `/dayz-add-server <instance>`, which also sets `allowFilePatching = 1;`. This skill never edits the cfg. Outside `--dry-run` it creates the two profile dirs if absent.
7. **Port check** (skipped with `--dry-run`): tries to bind UDP `<port>`; if something already holds it (usually a server left running), refuses with `port <port> in use; run /dayz-stop-test or pass --port` before spawning anything.
   Then the **Steam check** (also skipped with `--dry-run`): refuses with `Steam is not running` when `steam.exe` is not in the process list. The diag client needs Steam; without it the client crashes at start and leaves an `ErrorMessage_DayZDiag_x64_*.mdmp` in `.server/!ClientDiagLogs/`.
8. **Launch server**: spawns `DayZDiag_x64.exe -server -config=<instance>/serverDZ.cfg -profiles=<instance>/Profiles -mission=<instance>/<template> -mod=P:\Mods\@Mod1;P:\Mods\@Mod2 [-serverMod=P:\Mods\@ServerOnly1;...] -filePatching -port=<port>`. `-mod=` holds the shared mods; `--server-only` mods go on `-serverMod=` so clients are not told to load them. If the server cannot be spawned, the skill prints `[FAIL] Failed to spawn DayZDiag_x64.exe: <error>` and exits 1.
9. **Wait for the port**: polls once a second, for up to 180 s, until the server has bound UDP `<port>` (a DayZ server can take 30 s or more to load the mission and mods). If the server exits, or the wait times out (the server is then killed), the skill exits 1 without starting the client. Ctrl+C during the wait kills the server, prints `[FAIL] Interrupted while waiting for the server; killed it (PID <pid>).` and exits 130, so no server is left holding the port.
10. **Launch client**: spawns `DayZDiag_x64.exe -profiles=.server/!ClientDiagLogs -mod=... -connect=127.0.0.1 -port=<port> -filePatching` plus the display flags from the per-clone preferences. If the client cannot be spawned, the server is killed and the skill exits 1 with the same `[FAIL]` line.
11. **Print PIDs and exit.** Both processes are spawned detached (shared `DETACH_FLAGS` in `_shared/skill_helpers.py`), so they keep running when the shell or agent that started them closes. Close the windows to stop them, or run `/dayz-stop-test`. Follow the logs with `/dayz-logwatch`; stop the session with `/dayz-stop-test`.

## Refuses to run if

- No project is cached (run `/dayz-init`).
- `/dayz-preflight` returns non-zero.
- `workspace/_server/` still exists.
- Any named mod has no `.pbo` at `P:\Mods\@<ModName>\Addons\`.
- A mod is named both as a shared mod and under `--server-only`, or the same mod is named twice; names are compared ignoring case (exit 2).
- A mod name or `--server` is not a plain folder name (exit 2).
- A mod name comes after an option, or `--server-only` is given more than one name (exit 2 with `unexpected arguments`).
- A mod with source under `workspace/` requires a non-vanilla addon that no mod named before it provides (exit 1).
- `DayZDiag_x64.exe` is not found.
- The `--server` instance is not set up: `serverDZ.cfg` missing, without a `template = "...";` line, or without an active `allowFilePatching = 1;` line; `mission/` missing; or the `<template>/` junction missing. Run `/dayz-add-server <instance>`.
- UDP `--port` is already in use (not checked with `--dry-run`). Run `/dayz-stop-test` or pass another `--port`.
- Steam is not running (not checked with `--dry-run`). Start Steam and sign in.

## Output (success)

```
DayZ preflight
... (preflight output)
Preflight complete.

[OK]    Project: C:\Projects\MyDayZProject
[OK]    BuildTest PBO present: P:\Mods\@BuildTest\Addons\BuildTest.pbo
[OK]    Diag client: C:\Program Files (x86)\Steam\steamapps\common\DayZ\DayZDiag_x64.exe
[OK]    Instance: chernarus
[OK]    Instance dir: .server\chernarus
[OK]    Wrote default client display prefs to .claude\local-memory\dayz-client-display.json
[OK]    UDP port 2302 is free
[OK]    Steam is running

[Launch] Server: DayZDiag_x64.exe -server -config=...\chernarus\serverDZ.cfg -profiles=...\chernarus\Profiles -mission=...\chernarus\dayzOffline.chernarusplus -mod=P:\Mods\@BuildTest -filePatching -port=2302
[OK]    Server PID: 12345
        Waiting up to 180s for server to bind UDP port 2302...
......
[OK]    Server has bound UDP port 2302

[Launch] Client: DayZDiag_x64.exe -profiles=...\!ClientDiagLogs -mod=P:\Mods\@BuildTest -connect=127.0.0.1 -port=2302 -filePatching -window -x=1920 -y=1080
[OK]    Client PID: 67890

Both running. Close the windows manually to stop.
  Server PID: 12345    Client PID: 67890
  Server logs: .server\chernarus\Profiles
  Client logs: .server\!ClientDiagLogs
```

The `Wrote default client display prefs` line appears only on the first real launch, when that file does not exist yet. With `--dry-run`, the output is the same through the instance check (never with that line), then the two `[DRY-RUN] Server cmd:` / `[DRY-RUN] Client cmd:` lines, and exit 0.

## Client display preferences

The client reads `.claude/local-memory/dayz-client-display.json` (per clone, gitignored). The first real launch creates it with:

```json
{
  "windowed": true,
  "width": 1920,
  "height": 1080
}
```

These map to `-window`, `-x=<width>`, `-y=<height>`. Edit the file freely. A file that is not valid JSON, or has the wrong shape (not an object, `windowed` not true or false, `width` or `height` not a positive whole number), falls back to the defaults with a warning.

## Do not

- Don't launch the client without the server. DayZ has no offline mode for mod testing.
- Don't substitute retail `DayZ_x64.exe` or `DayZServer_x64.exe` for the diag binary.
- Don't kill the session from here once it is running; close the windows or use `/dayz-stop-test`.
