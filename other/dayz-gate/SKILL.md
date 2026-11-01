---
name: dayz-gate
description: "Runs the build, in-game, behavior and visual gates as scripts, with PASS or FAIL, triaged failures and a stored result for each. Use when gating a finished wave or checking a mod builds, loads, works and looks right in game."
argument-hint: "build <ModName> [--yes] [--json] | ingame <ModName> [--deps CF ...] [--server <instance>] [--port N] [--timeout S] [--settle S] [--ready-pattern REGEX] [--yes] [--json] | behavior <ModName> [--checks FILE] [--deps CF ...] [--server <instance>] [--port N] [--timeout S] [--done-timeout S] [--ready-pattern REGEX] [--prepare-only | --logs [FILE ...]] [--yes] [--json] | visual <ModName> [--shots FILE] [--deps CF ...] [--server <instance>] [--port N] [--timeout S] [--threshold R] [--ready-pattern REGEX] [--compare [DIR] | --accept [DIR] [--shot ID ... [--replace-failed]]] [--yes] [--json]"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-gate

Script versions of the `dayz-build-checker` and `dayz-ingame-tester` gates, plus a behavior gate that tests what each new item does and a visual gate that compares screenshots of the game with the expected look. They run the existing skill scripts as subprocesses and apply the same rules those agents follow, so a wave costs one command and a short report instead of two agent runs. The gates gate on `/dayz-preflight` through the scripts they call.

Follow `skills/_shared/dayz-conventions.md`.

## How to run

```cmd
python "<skill-dir>\gate.py" build <ModName> [--yes] [--json]
python "<skill-dir>\gate.py" ingame <ModName> [--deps CF ...] [--server <instance>] [--port N] [--timeout S] [--settle S] [--ready-pattern REGEX] [--yes] [--json]
python "<skill-dir>\gate.py" behavior <ModName> [--checks FILE] [--deps CF ...] [--server <instance>] [--port N] [--timeout S] [--done-timeout S] [--ready-pattern REGEX] [--yes] [--json]
python "<skill-dir>\gate.py" behavior <ModName> [--checks FILE] [--deps CF ...] [--server <instance>] --prepare-only [--json]
python "<skill-dir>\gate.py" behavior <ModName> [--checks FILE] [--server <instance>] --logs [FILE ...] [--json]
python "<skill-dir>\gate.py" visual <ModName> [--shots FILE] [--deps CF ...] [--server <instance>] [--port N] [--timeout S] [--threshold R] [--ready-pattern REGEX] [--yes] [--json]
python "<skill-dir>\gate.py" visual <ModName> [--shots FILE] [--threshold R] --compare [DIR] [--json]
python "<skill-dir>\gate.py" visual <ModName> [--shots FILE] [--threshold R] --accept [DIR] [--shot ID ... [--replace-failed]] [--json]
```

| Argument | Notes |
|---|---|
| `<ModName>` | A mod under `workspace/<ModName>/` in the project cached by `/dayz-init`. |
| `--deps` | `ingame`, `behavior` (also with `--prepare-only`, for its launch command), `visual`: dependency mods in load order, with or without `@` (`--deps CF`). Required when `config.cpp`'s `requiredAddons` lists anything not starting with `DZ_`; map each to the `@mod` under `P:\Mods\` that ships it. |
| `--server` | `ingame`, `behavior`, `visual`: instance added with `/dayz-add-server` (default `chernarus`). `--port` default `2302`. |
| `--timeout` | `ingame`, `behavior`, `visual`: seconds to wait for the client to reach the mission (default 300). |
| `--settle` | `ingame` only: seconds to keep reading after that, to catch spawn-time errors (default 30). `visual` has no `--settle`: it reads until its last shot is taken. |
| `--done-timeout` | `behavior` only: the most seconds to wait for the test mission's `DONE` line after the client joins (default 600). The gate stops as soon as that line appears. |
| `--ready-pattern` | `ingame`, `behavior` and `visual` in-game runs: regex in the client script log that means the mission is running. Default `Creating Mission: mpmissions\__cur_mp.`, printed by vanilla `CreateMission()` (`P:\scripts\5_mission\somemission.c`) when the client joins. |
| `--checks` | `behavior`: the checks file. Default `output/<ModName>-plan/behavior-checks.json`, which `dayz-mod-architect` writes with the plan. |
| `--prepare-only` | `behavior`: write the instance copy and stop. The first line is `PREPARED` (exit 0), then the `/dayz-launch-test` command for the copy with the `--deps` mods ahead of the mod (`launch` in `--json`). A mod that needs `--deps` and got none is refused (exit 2) before the copy is written. |
| `--logs` | `behavior`: judge the logs of a session that already ran instead of launching one. With no files it reads the copy's server script logs. |
| `--shots` | `visual`: the shots file. Default `output/<ModName>-plan/visual-shots.json`. |
| `--threshold` | `visual` runs, `--compare` and `--accept`: the share of pixels, 0 to 1, that may differ for a shot that sets no threshold of its own. It beats the shots file's `threshold`; the default is 0.01. |
| `--compare` | `visual`: compare captures already taken instead of launching. With no folder it uses the newest run. |
| `--accept` | `visual`: copy captures into the baselines. With no folder it uses the newest run; `--shot` limits it to some shots (`--shot` without `--accept` is refused, exit 2). A shot named with `--shot` that has no capture in the run is refused (exit 2); without `--shot`, shots with no capture are skipped, their baselines stay as they were, and they are named on a `skipped, no capture` line (`skipped` in `--json`). Each baseline it replaces is first copied to `baseline/.prev/<id>.<date_time>.png` (listed under `backups` in `--json`). It compares each capture with its current baseline first, the same way the gate does, and when any of them FAILs it refuses (exit 2) and copies nothing. The first line is `ACCEPTED` (exit 0). |
| `--replace-failed` | `visual --accept --shot <id> ...` only (refused otherwise, exit 2): accept the named shots even when their capture FAILs against the current baseline, after you have looked at the capture and its diff. |
| `--yes` | `build`, `ingame`, `behavior`, `visual` runs that stop a session: stop a `DayZDiag_x64.exe` session the gate did not start without asking. Without it the gate asks `[y/N]` on an interactive terminal and, with no terminal (an agent or a pipe), refuses with `ERROR` (exit 2) and leaves the session running, since it may be your own play session. The session the gate launches itself is always stopped without asking. |
| `--json` | Print the full report as JSON after the verdict line. |

## Output and exit codes

The first line is the verdict: `PASS` (exit 0), `FAIL` (exit 1) or `ERROR` (exit 2: bad arguments, no cached project, `/dayz-stop-test` failed, a session the gate did not start is running and was not confirmed, a dependency list is needed, `--accept` refused a capture that fails against its baseline, or the gate crashed). Then a short summary, or with `--json`:

```json
{
  "verdict": "FAIL", "mode": "ingame", "mod": "MyVest",
  "steps": [{"step": "stop-session", "result": "no DayZDiag session running"}, {"step": "dayz-launch-test", "rc": 0}, ...],
  "ready": {"file": "script_2026-10-20_12-00-31.log", "line": 214, "text": "SCRIPT : Creating Mission: mpmissions\\__cur_mp.chernarusplus\\mission.c"},
  "failures": [{
    "category": "null_pointer", "file": ".server\\!ClientDiagLogs\\script_...log", "line": 230,
    "text": "SCRIPT    (E): NULL pointer to instance", "context": ["Class: 'MyVest_Helper'", "Stack trace:", "MyVest/scripts/4_World/vest.c:42"],
    "points_to": ["MyVest/scripts/4_World/vest.c"], "count": 1,
    "triage": {"status": "known", "id": "null-pointer", "fix": "...", "owner_agent": "dayz-script-specialist", "fingerprint": "..."}
  }],
  "warnings": [...], "noise": [...], "baseline": ["...older vanilla-only RPT..."],
  "source_findings": [...]
}
```

Each failure carries `triage`: `known` (with `id`, `meaning`, `fix` and `owner_agent`) or `new` (send it to `dayz-mod-debugger`). Owner `user` means the user has to act (mount `P:`, install tools); owner `dayz-orchestrator` means a skill run fixes it. On a FAIL, `source_findings` lists known defects found in the mod's source (a `modded class` with an extends clause, a `config.cpp` without `CfgPatches`); they don't change the verdict. Warnings and noise are deduplicated and capped at 30 entries each.

Every `PASS` or `FAIL` is stored for `/dayz-health` under `.server/!Health/<ModName>/results/` (a `build` run stores its lint step too), and the mod's health page is rebuilt. The report then gains `"health"`, the path of the page's Markdown file. If storing fails, the report gains `"health_error"` instead and the verdict stays the same. An `ERROR` and `--prepare-only` store nothing.

## What `build` does

1. Runs `/dayz-lint <ModName>` first. Any lint error is a FAIL (category `lint`, file and line from the lint finding, triaged by its `lint-<rule>` entry) and the gate stops there, leaving a running session alone. Lint warnings join the report's warnings, and the report gains `"lint": {"verdict", "errors", "warnings"}`.
2. Stops any running `DayZDiag_x64.exe` with `/dayz-stop-test` (a session holds the PBO open), only after `--yes` or a yes at the prompt (see `--yes`).
3. Runs `/dayz-build-pbo <ModName>`. FAIL on a non-zero exit (every `[FAIL]` line is quoted with its hint), or on any AddonBuilder line after the command echo that reports an error, or a warning about missing files, textures or unknown classes.
4. Bundles ("Bundle / umbrella mods" in `skills/_shared/conventions/config.md`): with no `config.cpp` and a payload in `workspace/<ModName>/Addons/*.pbo`, the build is skipped and `/dayz-deploy-pbo <ModName>` runs instead; it must exit 0, and every `[FAIL]` and every `[WARN]` about a missing `.bisign` fails the gate. A bundle with a linker `config.cpp` gets both, build first.

## What `ingame` does

1. Stops any running session, records the size of every log in `.server/<instance>/Profiles/` and `.server/!ClientDiagLogs/`, then runs `/dayz-launch-test <deps...> <ModName> --server <instance>`. A launch refusal is a FAIL with its `[FAIL]` lines.
2. Polls the new log lines every 2 s until the ready line appears in the client script log plus `--settle` seconds, or `--timeout` (FAIL: no ready signal). It stops early on a `Can't compile ... script module` line, a new `crash*.log`, or a server or client process exiting (FAIL: crash).
3. Always stops the session with `/dayz-stop-test`, then judges only the lines written after step 1, with the `dayz-ingame-tester` rules:
   - Fail: script compile errors, missing config entries, textures or models, crashes; `NULL pointer` and `Can't find` errors only when they name the mod.
   - A line names the mod when it, or its stack trace, mentions the mod's folder, its `$PBOPREFIX$` root, or a class the mod declares (top-level classes in `config.cpp`'s `Cfg*` blocks and non-modded script classes).
   - Vanilla noise: a line that names nothing of the mod and also appears in a vanilla-only run, meaning one of the two newest older sessions in the same folder whose RPT `CLI params:` line has no `@<ModName>` (plus the script logs created within 30 s after that RPT). Noise is listed, not failed. With no such run the line is a warning.

## What `behavior` does

1. Reads the checks file and refuses a bad one (exit 2) before touching anything. Stops any running session.
2. Copies `.server/<instance>/` to `.server/<instance>-behavior/`: `serverDZ.cfg`, `mission/` without its `storage_*` persistence folders, the `<template>/` junction that `/dayz-launch-test` needs, and the settings in `Profiles/` (every file and folder except logs and crash dumps: `*.log`, `*.RPT`, `*.mdmp`, `*.bidmp`, `crash*`), so a mod or CF/COT that reads its config from the server profile behaves as it does on the instance. A previous copy is replaced: its own logs stay and its settings are overwritten by the instance's. Your own instance is never changed.
3. Adds a test mission to the copy's `init.c`: the class `AZ_BehaviorTest` above `main()` and an `AZ_BehaviorTest.Start();` call as the last line of `main()`.
4. Runs the `ingame` flow on the copy, so every `ingame` rule still applies. The test mission waits for the first player (up to 240 s), waits 10 s more, empties the player's hands and clothing slots, then runs one check per second and prints to the server script log:

   ```text
   [AZ-BEHAVIOR] START <count>
   [AZ-BEHAVIOR] PASS <check id>
   [AZ-BEHAVIOR] FAIL <check id> <reason>
   [AZ-BEHAVIOR] DONE
   ```

5. Reads those lines. A check passes only on its `PASS` line. A `FAIL` line, or no line at all (the mission never started, or a script error stopped it first), fails the check. A new `START` line starts over, so the newest run in the logs wins. When there is no `START` line at all and the session shows nothing else wrong (the client joined, no crash, no script error), the verdict is `ERROR`, not `FAIL`: the gate's own test mission did not run, so it says nothing about the mod.

The report adds `checks` (one entry per check with `status`, `reason`, `file` and `line`) and `behavior` (`started`, `done`, and `unexpected` ids that are not in the checks file). Each failed check is a failure with category `behavior` and its `check` id; triage marks it `new`, so it goes to `dayz-mod-debugger` with the reason line.

### Checks file

`dayz-mod-architect` writes one check per feature, each with an `id`, a `feature`, an `item` and one of the actions `spawn`, `hands`, `wear`, `attach` or `cargo`. The format and what each action does are in [checks-file.md](checks-file.md); read it before writing or fixing a checks file.

### Running it by hand

`behavior <ModName> --deps <Dep1> [<Dep2> ...] --prepare-only` writes the copy and prints the launch command: `/dayz-launch-test <Dep1> [<Dep2> ...] <ModName> --server <instance>-behavior`, with the dependency mods in load order before the mod (the launch script takes them as names ahead of the mod, not as a `--deps` flag). Run it, stop the session with `/dayz-stop-test`, then judge it with `behavior <ModName> --logs`.

## What `visual` does

1. Reads the shots file and refuses a bad one (exit 2) before touching anything.
2. Packs a small helper mod, `AZ_VisualHelper` (the files in `<skill-dir>\visual_helper\`), into `P:\Mods\@AZ_VisualHelper\` and loads it after your mod for this session only; it is removed when the session ends, even after a failure. The helper sets a fixed scene from inside the game. On the server it sets noon on June 21 and clear weather (no overcast, fog, volumetric fog, rain, snow or wind), and tells the engine not to change it. On the client it closes the pause menu vanilla opens when the window is not active at mission start, hides the HUD and quickbar, and switches to a still camera at the centre of the map facing north. It prints `[AZ-VISUAL] SCENE` (server) and `[AZ-VISUAL] CAMERA` (client); a run without either line fails with `[visual:no-scene]`.
3. Runs the `ingame` flow on your instance with the helper loaded, so every `ingame` rule still applies. The shot clock starts 15 seconds after the client joins, when the scene is set. At each shot's `at` second on that clock it captures the client window in the background with Windows' `PrintWindow` (full-content mode), which reads the window's own picture wherever it sits. It never moves your mouse or brings the window to the front, so you can keep working. It saves each capture to `output/<ModName>-visual/runs/<date_time>/<id>.png`. The session stops two seconds after the last shot.
4. Compares each capture with `output/<ModName>-visual/baseline/<id>.png`. Both images are shrunk to 640 pixels wide, which averages away single pixel noise. A pixel counts as changed when its colour distance, weighted toward brightness the way the eye sees it (the pixelmatch measure), is above a tenth of the largest possible. A shot fails when the share of changed pixels is above its threshold. Areas in its `ignore` list are left out.
5. Writes `<id>.diff.png` next to each capture: the baseline in pale grey, changed pixels in red and ignored areas in blue.

Each shot ends as one of these:

| Status | Means | Failure text |
|---|---|---|
| `PASS` | the share of changed pixels is at or under the threshold | |
| `FAIL` | too many pixels changed, or the capture is a different size from the baseline | `[visual:diff] <id>: ...` |
| `NEW` | the shot has no baseline yet | `[visual:no-baseline] <id>: ...` |
| `MISSING` | no capture: the window was hidden or minimized, or the session ended first | `[visual:no-capture] <id>: ...` |

Every status but `PASS` fails the gate. The report adds `shots` (one entry per shot with `status`, `ratio`, `threshold`, `capture`, `baseline`, `diff` and `reason`) and `visual` (the run and baseline folders). Triage marks each failure `known` with owner `user`, because only a person can say whether a new look is right: look at the capture and the diff, then accept it with `--accept --shot <id>` (add `--replace-failed` for a `FAIL`) or send it to the specialist who owns that part of the screen.

The first run of a shot is always `NEW`. Look at its capture, accept it, and later runs compare against it. Keep the baselines with the project; the runs folder is ignored by git. To undo an accept, copy the shot's newest `baseline/.prev/<id>.<date_time>.png` back to `baseline/<id>.png`.

### Shots file

Each shot has an `id`, a `feature` and an `at` second, with an optional `threshold` and `ignore` areas. The format is in [shots-file.md](shots-file.md); read it before writing or fixing a shots file.

## Triage

`triage.py` matches each failure line against `known-errors.json` and the project's learned file. Run it on its own for any log, or on a log the user pasted (`--stdin` or `--text`); after a reviewer has diagnosed a `new` result, record it so the next run sees it as known:

```cmd
python "<skill-dir>\triage.py" <log-file> [...] [--mod <ModName>] [--mod-dir workspace\<ModName>] [--json]
python "<skill-dir>\triage.py" --stdin --json < pasted.txt
python "<skill-dir>\triage.py" --learn <id> --fingerprint "<fingerprint or raw log line>" [--meaning "..." --fix "..." --owner <agent>]
```

How lines are fingerprinted, what to do with each result of a pasted log, and the rules for `--learn` are in [triage.md](triage.md); read it before triaging a pasted log or recording a diagnosis.

## Limits

- The ready line is the vanilla client print when it joins a multiplayer mission. A mod that replaces `CreateMission` or the mission flow needs `--ready-pattern`.
- AddonBuilder diagnostics are matched by keyword (`error`, `failed`, `undefined base class`, and warning lines that mention missing, not found or unknown class), since AddonBuilder, CfgConvert and Binarize word their messages differently. A non-zero exit with no matching line still fails, with the last 25 output lines as the failure's `context`.
- Dependency mapping from `requiredAddons` to `@mods` is not automatic; pass `--deps`.
- The behavior test mission only knows the five actions above. A feature that needs more (driving, firing, eating) has no check yet; say so in the plan.
- The test player is stripped once before the checks and each check deletes what it made, so no check can prove two items work together on the player.
- The test mission has not yet run in a live session. Every engine name the injected `AZ_BehaviorTest` class uses is checked against its vanilla declaration in `P:\scripts`, and `test_behavior.py` pins that list with the path and line of each, so an unchecked call fails the tests before it can reach a game. The injector and parser are tested on fixture missions and logs. If the mission still fails to start live (for example an Enforce compile error), the gate reports `ERROR` rather than failing the mod, unless the session also shows a mod error. After the first live run, look for `[AZ-BEHAVIOR] START` in `.server/<instance>-behavior/Profiles/script*.log`.
- DayZ scripts cannot save the screenshot themselves: vanilla `MakeScreenshot` (`P:\scripts\1_core\proto\proto.c:142`) made the `ScreenShots` folder in live runs but never wrote a file, so the capture is taken from outside the game with `PrintWindow`. That works while the client window is covered by other windows, but not while it is minimized (a minimized window draws nothing): such a shot, or an all-black capture, is `MISSING`. Two live sessions on October 24, 2026 gave captures that differed by 0.33% of pixels, under the default 1% threshold.
- A shot is taken at a time, not at a game event, and always shows the helper's fixed camera view without the HUD. Shots of the player, a menu or the HUD need the mod to put them there; screens that move on their own need a higher threshold or `ignore` areas.
- The visual gate needs Pillow: `py -m pip install -r "<skill-dir>\requirements.txt"`.

## Do not

- Don't pass `--yes` for the user: a running `DayZDiag_x64.exe` the gate did not start may be their play session. On that `ERROR`, ask them to close it or to agree to the gate stopping it.
- Don't edit `known-errors.json` from `--learn`; learned fingerprints are per project.
- Don't `--accept` a capture nobody has looked at, and don't pass `--replace-failed` for the user; the baseline is the expected look.
