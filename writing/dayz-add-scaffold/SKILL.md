---
name: dayz-add-scaffold
description: "Adds missing DayZ mod scaffold pieces (config.cpp, $PBOPREFIX$, Workbench gproj, README, folders) to a folder already in workspace/ without overwriting files, and can create its P:\\ link. Use when a workspace mod lacks scaffold pieces or its P: link, such as a hand-cloned or older mod."
argument-hint: "<ModName> [--piece config|prefix|workbench|readme|skeleton|junction|all] [--author <handle>]"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-add-scaffold

Companion to `/dayz-new-mod`. Where `dayz-new-mod` creates a fresh project from nothing, `dayz-add-scaffold` fills missing scaffold pieces into a folder that already exists, without touching anything already there.

Use this when:

- You cloned someone else's mod into `workspace/<ModName>/` and need `workbench/dayz.gproj` to open it in Workbench, or `$PBOPREFIX$` to build it.
- You used `/dayz-import-mod` to symlink an external repo and answered yes to a "scaffold this missing piece?" prompt - the import skill calls this skill's writer in-process to do the actual writing.
- You're upgrading an older scaffold that pre-dates the workbench-folder convention.
- `/dayz-build-pbo` or `/dayz-import-mod` reports the `P:\<ModName>\` link missing (for example after cloning a mod straight into `workspace/`): `--piece junction` creates it.

The mod folder is `workspace/<ModName>/` in the project cached by `/dayz-init`, the same project `/dayz-build-pbo` uses, so the skill works from any subfolder of it.

Follow `skills/_shared/dayz-conventions.md`.

## How to run

```cmd
python "<skill-dir>\add_scaffold.py" <ModName> [--piece config|prefix|workbench|readme|skeleton|junction|all] [--author "YourHandle"]
```

| Argument | Required? | Notes |
|---|---|---|
| `<ModName>` | yes | Folder name under `workspace/`. The folder must already exist (real or a link). Same `[A-Za-z][A-Za-z0-9_]{0,63}` pattern as `/dayz-new-mod`. |
| `--piece` | no | Default `all` = scan and add only missing file pieces. Pick one to scaffold a single piece even if others are missing. `junction` is never part of `all`. |
| `--author` | no | Author handle for `config.cpp` and `README.md`. Same resolution chain as `/dayz-new-mod`: flag → cache (`.claude/local-memory/dayz-author.txt`) → interactive prompt → fail. A handle from the flag or the prompt is saved to that cache once the pieces are written, so later runs (including ones without a TTY) reuse it. Resolved once, before any piece is written, and only when `config.cpp` or `README.md` is about to be written; if no handle is available (no flag, no cache, no TTY) the skill exits 1 with the folder untouched. A handle containing `"` or a line break is refused, since it is written inside a quoted `config.cpp` string. |

### Pieces

| Piece | What it writes | When |
|---|---|---|
| `config` | `config.cpp` (CfgPatches + CfgMods stub) | only if missing |
| `prefix` | `$PBOPREFIX$` (contains `<ModName>`) | only if missing. An existing file that does not hold `<ModName>` (BOM and surrounding whitespace ignored), or is not UTF-8 text, is left unchanged with a `[WARN]` that `/dayz-build-pbo` will refuse it, and counted as needing fixing by hand. |
| `workbench` | `workbench/dayz.gproj` (vanilla copy + injected mod paths + dual FileSystem mounts) and `workbench/DayZSetting.xml` | gproj only if missing; xml only if missing. Skipped with a warning (and counted as skipped) when `workbench/dayz.gproj` is missing and cannot be written: DayZ Tools is not detected, or its `Bin\Workbench\dayz.gproj` is missing (the xml may still be copied). When `workbench/dayz.gproj` is already present and only the xml cannot be copied, the piece counts as present, with a `[WARN]` about the missing xml. |
| `readme` | `README.md` (light onboarding notes) | only if missing |
| `skeleton` | `scripts/3_Game/`, `scripts/4_World/`, `scripts/5_Mission/`, `data/`, `gui/` (each with `.gitkeep`) | each subfolder only if missing. A file sitting where one of these folders (or `scripts/`) belongs is left unchanged with a `[WARN] <name> exists as a file, not a folder`; the other folders are still created and the piece counts as needing fixing by hand. |
| `junction` | the `P:\<ModName>\` link to `workspace/<ModName>/` (symlink, junction fallback; the same code `/dayz-new-mod` uses) | only if missing. Refuses if `P:\<ModName>\` is a real folder or a link pointing anywhere else. |
| `all` | runs `config`, `prefix`, `workbench`, `readme`, `skeleton` in that order (not `junction`) | default |

Wrong kind of entry: when `config.cpp`, `$PBOPREFIX$`, `README.md`, `workbench/dayz.gproj` or `workbench/DayZSetting.xml` exists as a folder, or `workbench` exists as a file, the skill leaves it unchanged, prints `[WARN] <name> exists as a folder, not a file` (or the reverse) and counts the piece as needing fixing by hand.

Whatever piece you pick, the skill is idempotent: a second run on the same folder writes nothing.

`--piece junction` output, first run then second run:

```
[OK]    P:\MyMod junction -> workspace\MyMod
[SKIP]  P:\MyMod present (links to workspace\MyMod)
```

The first line says `symlink` instead of `junction` when Windows allows symlinks (Developer Mode or an elevated shell).

## Refuses to run if

- `<ModName>` fails the name pattern. This is checked first, before preflight, so a typo fails fast.
- `/dayz-preflight` returns non-zero (typically `P:\` not mounted) - preflight runs before anything is read or written and propagates its exit code.
- No project is cached (run `/dayz-init`), or the cached project folder no longer exists.
- `workspace/<ModName>/` does not exist. This skill never creates the top-level mod folder - that's `/dayz-new-mod` (for fresh) or `/dayz-import-mod` (for external).
- `--piece junction` and `P:\<ModName>\` exists as a real folder or as a link to somewhere other than `workspace/<ModName>/`. Remove it by hand first; the skill never deletes anything on `P:\`.
- The author handle (flag, cache or prompt) contains `"` or a line break.
- `config.cpp` or `README.md` would be written and no author handle is available (no `--author`, no cache, stdin not a TTY). Nothing is written.

## Output

Pieces run in the order config, prefix, workbench, readme, skeleton. Example on a folder that already has `config.cpp` and `README.md`:

```
DayZ preflight
... (preflight output)
Preflight complete.

Scaffolding workspace\MyMod\

[SKIP]  config.cpp present
[OK]    $PBOPREFIX$ written
[OK]    workbench/dayz.gproj written (mod paths + filesystem mounts injected)
[OK]    workbench/DayZSetting.xml copied
[SKIP]  README.md present
[OK]    Skeleton folders created (3 added, 2 already present)

[OK]    3 piece(s) added, 2 already present, 0 skipped.
```

A piece counts as skipped when it is missing but cannot be written, such as `workbench` when DayZ Tools is not detected (no empty `workbench/` folder is created in that case). When the one piece named with `--piece` is skipped, the skill ends with `[FAIL] <piece> was not written` and exits 1, so callers can tell nothing was written; with `all`, skipped pieces are counted in the summary and the exit stays 0.

A piece needs fixing by hand when it is present but holds content a later skill refuses (a `$PBOPREFIX$` that does not hold `<ModName>`), or when a file sits where a folder belongs or the reverse (for example a file named `scripts`). Nothing is changed. `--piece <piece>` then ends with `[FAIL] <piece> is present but wrong` and exits 1; with `all`, the summary adds `, 1 need fixing by hand` and the exit stays 0.

The summary line is tagged `[OK]` only when no piece was skipped or needs fixing; otherwise it is tagged `[WARN]`, for example:

```
[WARN]  4 piece(s) added, 0 already present, 1 skipped.
```

If everything is already present:

```
[OK]    Nothing to add - workspace\MyMod is already fully scaffolded.
```

`--piece junction` checks only the link, so it ends with a line about the link instead:

```
[OK]    P:\MyMod link already in place.
```

## What it does not do

- It does not create `workspace/<ModName>/` itself. The folder must exist first.
- It does not create the `P:\<ModName>\` junction unless you pass `--piece junction`, and it never removes or redirects an existing one.
- It does not touch the deployed dir at `P:\Mods\@<ModName>\`. That's `/dayz-build-pbo`.
- It does not overwrite existing files. If you have your own `config.cpp` or `$PBOPREFIX$`, the skill leaves them alone.
- It does not git-add or commit anything. The user decides whether to track scaffold pieces.

## Do not

- Don't add an `--overwrite` flag. Idempotency without surprise overwrites is the contract; if you want to regenerate a piece, delete it manually and re-run.
- Don't copy the templates or gproj helpers out of `dayz-new-mod`'s `new_mod.py`. This skill imports them so both skills produce byte-identical output for the same inputs.
- Don't bypass the preflight gate.
