---
name: feature-resolve
description: Internal helper invoked only by other skills in this plugin (feature-storm, feature-design, feature-plan, feature-implement) as their resolution step. Determines the correct features/feature-vN-<description>/ folder, version, and stage file path the caller must use. Creates the features/ folder and the feature subfolder if they don't exist, seeds feature-vN-tracker.html from the plugin's template on folder creation, and returns the resolution as a parseable block. Never edits or creates stage .md files — that is the caller's job. Not user-invocable.
user-invocable: false
allowed-tools: Read, Glob, Write, AskUserQuestion, Bash(ls *), Bash(find *), Bash(mkdir -p *), Bash(test *), Bash(cp *), Bash(pwd)
---

# feature-resolve

Invoked as the resolution step of another feature-* skill in this plugin. Computes which `features/feature-v<N>-<description>/` folder the caller should write into, ensures the folder and tracker file exist, and returns the resolution as a structured block for the caller to parse.

**You are running inline, inside the calling skill's own turn.** The `Skill` tool loads these instructions into the caller's context — it does not delegate to a subagent. There is no second agent on the other side of this: the model reading this text is the same model that will carry on with the caller's remaining steps once the resolution block is out. Read every "the caller" below as "you, a few steps from now".

The point of externalising this is that all four feature skills need identical answers to "what folder, what version, what stage file?". Putting the procedure here means the four skills stay perfectly aligned and a rule change lands in exactly one place.

## Input

The caller passes a comma-separated argument string with these slots:

- `stage=<storm|design|plan|implement>` — **required**. The calling skill's stage slug.
- `version=<N>` — optional. An explicit feature version the user named (e.g. via `$ARGUMENTS`).
- `description=<phrase>` — optional. A new feature's description. Only consulted when creating a new feature folder; ignored (with a warning) when continuing into an existing folder.

Examples:

```
stage=design
stage=plan, version=3
stage=design, description=Add Reminders
stage=storm, version=4, description=Payments checkout
```

If `stage=` is missing or names a slug other than the four allowed values, stop with a one-line error and ask the caller to retry. Do not guess from context.

## Step 1 — Locate or create `features/` in the project root

Run `test -d features` in the current working directory.

- If it does not exist, run `mkdir -p features` to create it.
- Never write `features/` anywhere other than the project root (cwd). Do not migrate or copy from `docs/` — `docs/` is legacy reference material; new artifacts always live under `features/` starting at v1.

## Step 2 — Scan for existing feature folders

Glob `features/` for directories matching `feature-v<N>-*`:

```
find features -maxdepth 1 -type d -iname 'feature-v[0-9]*-*'
```

For each match, parse:

- `N` — the integer version (numeric compare, not lexicographic — `v10` > `v9`).
- `description` — everything after `feature-v<N>-`, preserved verbatim (this is the authoritative description for the feature).
- `present_stages` — set of stages whose file exists in the folder. A stage file is named `feature-<stage>-v<N>-<description>.md`. Check for each of `storm`, `design`, `plan`, `implement`.

Build the map `{N → (folder_path, description, present_stages)}`. Identify `N_max` (the highest existing version) and `latest` (the entry for `N_max`). If the map is empty, treat `N_max` as 0 and `latest` as absent.

## Step 3 — Resolve mode, target version, and target folder

Apply the rules in this priority order. The first matching rule wins.

**Rule A — Explicit `version=<N>` argument.** The user named a specific feature.

- If `features/feature-v<N>-*` does not exist:
  - For `stage=storm` or `stage=design`: this is a forward reference. If `N` ≠ `N_max + 1`, stop with an error — versions must be contiguous, no gaps. If `N` = `N_max + 1`, treat as **create-new** at version `N` (description is required, validate per Step 4).
  - For `stage=plan` or `stage=implement`: stop with an error — these stages cannot create a new feature folder; they need an existing folder with the prerequisite stage file. Tell the caller to specify an existing version or run the earlier stage first.
- If `features/feature-v<N>-<desc>/` exists:
  - If the stage file already exists in that folder: ask the user via `AskUserQuestion` whether to **overwrite** (revisions are explicitly disabled in this plugin's design — overwriting is the only path) or cancel. If they cancel, stop. If they overwrite, proceed with mode = **continue-existing**.
  - If the stage file does **not** exist in that folder: for `plan`/`implement`, confirm the prerequisite stage file is present (design for plan; plan for implement). If the prerequisite is missing, stop with an error naming the missing prerequisite. Otherwise proceed with mode = **continue-existing**.
  - If a `description=` argument was also provided and it conflicts with the folder's description, ignore the user's value and warn in the output `notes` field that the folder name is authoritative.

**Rule B — No `version=` argument, and no existing feature folders.** This is the first ever feature in this repo.

- Allowed only for `stage=storm` or `stage=design` — `plan` and `implement` need a prerequisite and there is none. For plan/implement, stop with an error: "No feature folders exist under `features/`. Run /feature-design (and optionally /feature-storm) first."
- Mode = **create-new**, version = `1`. Description is required; validate per Step 4. If `description=` was not provided, stop with a one-line error asking the caller to re-invoke with a description.

**Rule C — No `version=` argument, the latest folder LACKS this stage's file.** The latest feature is still in progress on this stage.

**Guard — a missing stage file may mean the stage was *skipped*, not left pending.** Check what else the latest folder holds before treating it as in-progress. For `stage=storm` and `stage=design` **only** (plan and implement cannot create a new feature, so the guard does not apply to them), fall straight through to **Rule D** — create-new at `N_max + 1`, without asking — when either of these holds:

- **The latest folder contains a *later* stage's file** — `design`, `plan` or `implement` when `stage=storm`; `plan` or `implement` when `stage=design`. That feature started cold at a later stage, so its earlier stage was skipped rather than left pending, and continuing this stage into it is never the right answer. Expect this after any feature that began at `/feature-design`.
- **The latest folder contains no stage file at all *and* no `feature-v<N>-tracker.html`**, and a `description=` differing from the folder's was provided. A folder this resolver created always carries a seeded tracker, so one with neither is out-of-band — a stray or hand-made directory, not a feature awaiting its first stage.

In both cases there is exactly one sensible outcome, so the `AskUserQuestion` below would cost a round-trip and buy nothing. Record what happened in `notes` (e.g. `latest v<N_max> skipped <stage> — created new feature instead`) so the caller can surface the reasoning. Everything below applies only when the guard did **not** fire.

- For `plan`/`implement`: also confirm the prerequisite stage file exists in `latest`. If not, stop with an error naming the missing prerequisite.
- If `description=` was provided and matches `latest.description`, proceed with mode = **continue-existing**, version = `N_max`, folder = `latest.folder_path`.
- If `description=` was provided and **differs** from `latest.description`: ask via `AskUserQuestion` — "Continue into `feature-v<N_max>-<latest.description>/` (folder name wins) or start a new feature `feature-v<N_max+1>-<new-desc>/`?" Honor the choice.
- If `description=` was not provided, proceed with mode = **continue-existing**, version = `N_max`, folder = `latest.folder_path`, description = `latest.description`.

**Rule D — No `version=` argument, the latest folder ALREADY HAS this stage's file.**

- For `stage=storm` or `stage=design`: mode = **create-new**, version = `N_max + 1`. Description is required; validate per Step 4. If `description=` was not provided, stop with a one-line error asking the caller to re-invoke with a description.
- For `stage=plan` or `stage=implement`: ambiguous (the stage is "done" in the latest folder, and these stages can't make a new feature). Ask the user via `AskUserQuestion` whether to overwrite the existing stage file in `latest` or specify an older version via `version=`. Do not pick for them.

Record the resolved `mode`, `version`, `folder_path`, and `description`.

## Step 4 — Validate description (create-new only)

For mode = **continue-existing**, skip this step — the description came from the folder name and is already valid.

For mode = **create-new**, the description must meet:

1. **Word count ≤ 10.** Count whitespace-separated tokens of the user-provided phrase. If more than 10, stop with an error: "Description must be 10 words or fewer; got <N>: <phrase>". Do not truncate silently.
2. **Filename-safe.** Strip leading/trailing whitespace, collapse internal whitespace runs to single spaces, then replace each space with `-`. Preserve the user's case (so "Add Reminders" → "Add-Reminders", consistent with the example `feature-plan-v2-Reminders`). Reject if the result contains characters outside `[A-Za-z0-9._-]` after the transformation — stop and tell the caller to simplify the description.
3. **Non-empty.** A whitespace-only or zero-length description is rejected.

The validated, hyphenated description becomes the canonical `description` for this feature and goes into the folder name.

## Step 5 — Create the feature folder if needed

If mode = **create-new**, run `mkdir -p features/feature-v<N>-<description>` (relative to cwd). Record the absolute folder path for the output block (resolve via `pwd` if helpful).

If mode = **continue-existing**, the folder already exists from Step 2 — no creation needed.

## Step 6 — Seed the tracker if missing

The tracker file path is `<folder_path>/feature-v<N>-tracker.html`.

- If it already exists, do nothing — the caller (or a previous stage) populated it.
- If it does not exist, copy the plugin's template into place. Locate the template by searching the plugin install location:

  ```
  find ~ -path "*dev-skills*/templates/feature-tracker.html" 2>/dev/null
  ```

  - **First, try the running plugin's own copy** — no search needed. This skill's base directory was announced when it was invoked (`…/dev-skills/<version>/skills/feature-resolve`), so the template sits two levels up at `<base>/../../templates/feature-tracker.html`. If that file exists, use it: it is by definition the template matching the running plugin version.
  - Otherwise run the `find` above. The `*dev-skills*` form is deliberate — an installed plugin lives at `…/plugins/cache/<marketplace>/dev-skills/<version>/templates/`, and the narrower `*/dev-skills/templates/…` pattern silently misses it, matching only a working clone.
  - If exactly one match: `cp <match> <folder_path>/feature-v<N>-tracker.html`.
  - If multiple matches: prefer one under a `plugins/cache/` path (an installed plugin) at the **highest** version over a working clone. Do not key this on `~/.claude/` — a profile directory can live elsewhere (e.g. synced under `~/Library/Mobile Documents/`), and several versions are normally cached side by side. Ask the user via `AskUserQuestion` only if a genuine tie remains.
  - If zero matches: do not fail the whole resolution — emit a note in the output (`tracker_seed: skipped — template not found`) and let the caller decide whether to populate the tracker from scratch.

Do **not** substitute any tokens (`{{FEATURE_VERSION}}`, etc.) — token replacement is the calling skill's responsibility. Tracker file lives as a raw template until each stage fills in its own section.

## Step 7 — Output the resolution block

Echo a single block to chat. Use exactly this shape so the caller can parse it line-by-line:

```
feature-resolve result
---
mode: <create-new | continue-existing>
version: <N>
description: <hyphenated description, exactly as it appears in the folder name>
feature_folder: <absolute path>
stage_file: <absolute path to features/feature-vN-<desc>/feature-<stage>-vN-<desc>.md>
tracker_file: <absolute path to features/feature-vN-<desc>/feature-vN-tracker.html>
prereq_file: <absolute path to the prerequisite stage file, or "n/a" if none>
notes: <single line — overwrites authorised, description conflicts ignored, tracker seeded/skipped, etc.; or "none">
```

The `stage_file` is the path the caller will write to. The file itself **must not exist yet** for mode = create-new and may or may not exist for continue-existing (it exists only when the user authorised an overwrite in Step 3). Either way, this skill does not touch it.

`prereq_file` is set when the caller is `plan` or `implement` — it points at the design (for plan) or plan (for implement) file the caller should read. For `storm` and `design`, set `prereq_file: n/a`.

**Do not end your turn here.** Nothing is waiting to pick this block up — you were loaded inline, so emitting the block is not a hand-off and there is no "return" to make. Emit it, then continue immediately, in the same turn, with the calling skill's next step: `feature-storm` Step 3, `feature-design` Step 3, `feature-plan` Step 2, `feature-implement` Step 2. The block stays in context as the record every later step reads its paths from.

The only paths that do end the turn are the explicit failure exits above: a missing or invalid `stage=`, a non-contiguous `version=`, a missing prerequisite stage file, an invalid description, or a user cancelling the overwrite prompt in Step 3. A successful resolution never ends the turn.

## Constraints (non-negotiable)

- **Never create or edit a stage `.md` file.** Only the caller writes those. This skill creates the folder and (optionally) seeds the tracker html.
- **Never delete anything.** No `rm`, no overwriting existing folders, no removing tracker files. If an overwrite is authorised in Step 3 for an existing stage file, this skill still does not touch it — it just reports the path and lets the caller overwrite.
- **Folder name is authoritative for description.** When continuing into an existing folder, the folder's description wins; any `description=` argument that disagrees is reported in `notes` and discarded.
- **Versions are contiguous.** No gaps allowed when creating new — `N` must equal `N_max + 1`. No minor versioning (`v1.0`, `v1.1`) under any circumstances.
- **No symlinks.** When copying the tracker template, always copy — never `ln -s`.
- **Stop and ask, don't invent.** Any ambiguity (overwrite vs. new feature, multiple template matches, description mismatch on continue) goes through `AskUserQuestion`. Never silently pick a path the caller didn't authorise.
- **Output format is the contract.** The block in Step 7 is read back verbatim by the caller's later steps — which are your own later steps, since you run inline; do not add prose, headers, or extra fields. The exact keys and order matter.
- **A successful resolution never ends the turn.** Emitting the Step 7 block is a checkpoint, not a stopping point. Carry straight on into the calling skill's next step in the same turn. Only the explicit failure exits (bad `stage=`, version gap, missing prerequisite, invalid description, user cancel) stop the run.
