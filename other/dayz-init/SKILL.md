---
name: dayz-init
description: "Runs first-run DayZ setup in an Agentic-Z clone (environment check, scaffold or import a mod, optional test server), then serves as a status hub that dispatches to the /dayz-* skills. Use when the user starts DayZ modding, says \"init\" or \"set up DayZ\", or wants a status overview and next action."
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-init

The agent is the wizard: it runs the scripts below with Bash and asks the user questions with AskUserQuestion. None of the scripts prompt for input. Every action goes through the sibling skill that owns it; this skill never re-implements them.

Follow `skills/_shared/dayz-conventions.md`. This skill does not gate on `/dayz-preflight` itself, because its own environment check covers the same ground and also fixes `P:\` first. Every child skill it runs gates on preflight.

State is per clone, in `.claude/local-memory/` (gitignored): `dayz-current-project.txt` (the project root other DayZ skills read) and `dayz-init-state.json` (the active mod). The project root is the clone: `$CLAUDE_PROJECT_DIR`, else the nearest folder at or above the current directory (below the home folder) that holds `dayz-current-project.txt`, else the clone that holds the skill scripts when that clone has the cache, else the current directory. Mods live in `workspace/<ModName>/`, test servers in `.server/<instance>/`.

## Step 1: setup check

```
python "<skill-dir>\check_setup.py"
```

If it prints a path, setup is done: go to Step 6. If it prints nothing, continue.

## Step 2: environment check

```
python "<skill-dir>\check_env.py"
```

Read-only. Prints `OK`, or one line per issue (always exits 0):

- `AUTO p_drive`: `P:\` is not mounted. Mount it now without asking (non-destructive), then re-run `check_env.py`, because the `P:\` checks are skipped while it is unmounted:
  ```
  python "<skill-dir>\dispatch.py" mount-p
  ```
  If the mount fails, show its output and stop.
- `HARD <name> ...`: DayZ Tools missing, vanilla data not extracted, `P:\Mods` the wrong shape (or missing with no DayZ install found), or Python too old. Tell the user what is wrong and the fix or link on the line, then stop. They re-run `/dayz-init` after fixing it.

A missing `P:\Mods` is not an issue when the DayZ install's `!Workshop` folder exists: `/dayz-preflight`, which the first child skill in Step 5 runs, creates the junction.

## Step 3: setup questions

Ask questions 1 to 3 in one AskUserQuestion call, putting the usual choice first:

1. New mod or import an existing mod folder?
2. Test server: chernarus, livonia, sakhal, nasdara, or none. AskUserQuestion shows at most 4 options, so offer chernarus, livonia, sakhal and none, and accept nasdara when the user types it as the other answer. Any other map needs `/dayz-add-server` with the mission folder name.
3. Build the PBO now? (yes / no)
4. Launch DayZ Diag now? (yes / no; launching implies building). Ask this in a second AskUserQuestion call, and only when question 2 picked a server: `plan.py` refuses `--launch` without `--server`.

Then ask in chat for the free-text values:

- Mod name (letters, digits and underscores, starting with a letter, at most 64 characters; `plan.py` refuses any other name). For an import, offer the source folder's name as the default.
- Import only: the source folder path or a GitHub (or other git) link, which `/dayz-import-mod` clones, and whether to write missing scaffold pieces into it (`--scaffold`) or only link it (`--no-scaffold`).
- New mod, or import with `--scaffold`, when `.claude/local-memory/dayz-author.txt` does not exist: the author handle shown in mod descriptions (a scaffolded import writes it into `config.cpp`). Pass it as `--author`.
- Optional spec, only when `workspace\<ModName>\spec.md` does not exist and the mod is not a `--no-scaffold` import: "What should the mod do? Say skip to leave it for later." This is the only spec question. If the user skips, pass no spec flags. Otherwise turn the answer into one `--goal` sentence plus `--item` (each item or class the mod adds), `--behavior` (each thing a player can do or see in game) and `--done-check` (each check that proves it works), all repeatable. Use the user's own words and don't invent features they did not ask for. The plan writes these to `spec.md`, and dayz-mod-architect reads it first when it plans the mod.
- The spec question is not asked when `workspace\<ModName>` is a linked import, because `plan.py` never writes into a linked source folder on a re-run.
- Import with launch: read the source folder's `config.cpp` `requiredAddons[]` (the same check as the hub's `Needs:` line). When it lists anything that does not start with `DZ_`, such as `JM_CF_Scripts`, ask which `@mods` under `P:\Mods\` provide those addons, in load order, and pass them as `--deps`. Without them the mod fails to load on the first launch, so `plan.py` refuses `--launch` (exit 2, naming the addons) until `--deps` is given. A prebuilt bundle (an `Addons\*.pbo` folder) is not checked, the same as `/dayz-gate ingame`. For a GitHub link there is no folder to read yet, so the plan adds a step after the clone that checks the cloned `config.cpp` and stops with exit 2, naming the addons, before the build and launch; re-run with `--deps` (the import is kept and skipped on the re-run).

## Step 4: show the plan

```
python "<skill-dir>\plan.py" --mod <ModName> [--import-from <path-or-link> --scaffold|--no-scaffold] [--author <handle>] [--goal <text> [--item <text>]... [--behavior <text>]... [--done-check <text>]...] [--server <map>] [--build] [--launch [--deps <mod> ...]]
```

Prints the numbered plan, for example:

```
Plan:
  1. Scaffold workspace\MyMod
  2. Write workspace\MyMod\spec.md
  3. Record MyMod as the active mod
  4. Set up the chernarus test server
  5. Build MyMod.pbo
  6. Launch DayZ Diag with MyMod on chernarus
```

The `Check <ModName>'s requiredAddons need no --deps` step appears only for a link import with `--launch` and no `--deps`. The spec step appears only with `--goal`, and is skipped when `spec.md` already exists, so a spec the user edited is never overwritten.

Scaffolding or importing is skipped when `workspace\<ModName>\` already exists (a folder or a link, including a `--no-scaffold` import that has no `config.cpp` yet), so re-running `/dayz-init` for an existing mod just makes it active. Show the plan in chat. Don't ask for a yes/no: the user already chose everything in it, and none of it is destructive.

## Step 5: run the plan

Same command plus `--execute`. Each step's output streams through; the first failing step stops the run, and the script exits with that step's exit code. Tell the user which step failed and what the child skill said. Exit 2 means the environment check failed again or a value was missing.

| Step | Runs |
|---|---|
| new-mod | `dayz-new-mod\new_mod.py <ModName> [--author <handle>]` |
| import-mod | `dayz-import-mod\import_mod.py --source <path-or-link> --name <ModName> --scaffold\|--no-scaffold [--author <handle>]` (author only with `--scaffold`) |
| check-deps | reads the cloned `workspace\<ModName>\config.cpp` `requiredAddons[]`; exit 2 when they need `--deps` |
| spec | writes `workspace\<ModName>\spec.md` with Goal, Items, Behaviors and Done checks sections |
| record | writes the two state files above |
| add-server | `dayz-add-server\add_server.py <map> --map <map>` |
| build | `dayz-build-pbo\build.py <ModName>` |
| launch | `dayz-launch-test\launch.py <ModName> --server <map>`, with the `--deps` mods loaded first |

`/dayz-new-mod` creates the `P:\<ModName>` junction itself. When the plan succeeds, go to Step 6.

## Step 6: hub

```
python "<skill-dir>\hub_status.py"
```

Shows the active mod, PBO age, test servers, whether DayZ Diag is running, and search status. Test servers are the `.server\<instance>\` folders with a `serverDZ.cfg`; the `<instance>-behavior` copies that `/dayz-gate behavior` rebuilds are not listed. A `Needs:` line lists the active mod's `requiredAddons` that vanilla does not provide, such as `JM_CF_Scripts`. A prebuilt bundle (`Addons\*.pbo`) gets no `Needs:` line, because its own PBOs may provide them and launch does not ask it for `--deps`. Then ask "What next?" with AskUserQuestion and dispatch the choice. Repeat until the user is done.

| Choice | Do |
|---|---|
| Build and launch | `dispatch.py build`, then `dispatch.py launch --server <instance> [--deps CF ...]` (ask for the instance if there are several; offer add-server if there are none). When the status has a `Needs:` line, ask which `@mods` provide those addons, in load order, and pass them as `--deps`; `dispatch.py launch` refuses without them (exit 2) |
| Lint the mod | `dispatch.py lint` (`/dayz-lint`) |
| Gate the build | `dispatch.py gate-build [--yes]` (`/dayz-gate build`: lint, build and a stored result) |
| Gate in game | `dispatch.py gate-ingame [--server <instance>] [--deps CF ...] [--yes]` (`/dayz-gate ingame`; `--server` defaults to chernarus; ask for `--deps` as for launch) |
| Show mod health | `dispatch.py health` (`/dayz-health`: last build, last test and open findings) |
| Stop DayZ Diag | `dispatch.py stop` |
| Show the server log | Read the newest `script*.log` in `.server\<instance>\Profiles\` |
| Open in Workbench | `dispatch.py workbench` |
| Open in Object Builder | `dispatch.py objectbuilder` (opens the mod's one `.p3d` under `P:\<ModName>\`; opens Object Builder empty when the mod has no model yet; with several models, run `/dayz-launch-objectbuilder --file <p3d>`) |
| Review the mod | Hand `workspace\<ModName>\` to the dayz-mod-reviewer agent |
| Add a test server | `dispatch.py add-server --server <map>` |
| Set up search | See "Search (optional)" below, then `dispatch.py search-download` |
| Set up or switch to another mod | Go back to Step 3 for that mod; `plan.py` skips scaffolding for a mod that already exists |

When the status's `Diag:` line says `running` (for example right after "Build and launch"), both gate actions must stop that session first, and `/dayz-gate` does that only with `--yes`; without it the gate exits with an error telling you to rerun with `--yes`. Before a gate choice in that state, ask the user with AskUserQuestion whether the gate may stop the running DayZ Diag session (offer "Stop DayZ Diag" as the alternative), and pass `--yes` only on a yes. Never pass `--yes` without asking.

All `dispatch.py` actions default `--mod` to the active mod (only `add-server`, `launch` and `gate-ingame` take `--server`; only `launch` and `gate-ingame` take `--deps`; only `gate-build` and `gate-ingame` take `--yes`) and exit with the child skill's exit code (2 when a required value is missing or an action got an option it cannot use). `python "<skill-dir>\dispatch.py" --list` prints the actions.

## Search (optional)

Only when the user asks for it. The dayz-rag MCP server needs a Voyage AI key and an installed index (Voyage `voyage-code-3` embeddings in LanceDB under `~/.claude/dayz-search-index/`). The user adds `VOYAGE_API_KEY=pa-...` to `.env` at the project root themselves (don't ask them to paste the key into chat), then runs `/dayz-search-download` for the prebuilt index or `/dayz-search-index` to build it locally.
