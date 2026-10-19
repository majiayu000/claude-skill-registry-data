---
name: rhovanion
description: Use when the user runs /rhovanion [--dry-run] [--confirm]. Sweeps every tracker project in your global pipeline list (pipeline_projects.md), but gates each behind a cheap per-project movement probe — it dispatches the full /anduin council→forge pipeline for a project only when that project's tickets have moved since its last ride (tracked by a per-project cursor in pipeline_cursors.md). Quiet projects cost one tracker query apiece, not a whole pipeline. Prints one combined report ending in a plain STIRRED/QUIET verdict. The forge stage inherits /anduin's default — UNATTENDED unless --dry-run or --confirm. Sequential across projects, so no two pipelines contend. Run alone for a single pass, or wrap in /amon-sul rhovanion … for an adaptive, single-timer watch of the whole watershed.
purpose: Sweeps every project in the global pipeline list, gated by a movement probe.
user_invocable: true
stage: vigil
composes: anduin:dispatch
---

# Rhovanion — The Watershed of Many Rivers

Anduin, the Great River, ran one project's tickets from council to forge.
Rhovanion is the wide land all the rivers drain — Wilderland, where tributary
after tributary feeds the one current. So this skill: where `/anduin` carries a
single project down the channel, Rhovanion walks every project in your keeping,
summons Anduin at each, and brings back one report of all.

The thing Rhovanion adds that a bare loop would not: a **cheap probe before each
ride**. A tick fires the full pipeline only on the projects whose tickets have
actually moved; the still rivers cost a single tracker query, not a council.

## Ethos

- **Rhovanion walks; Anduin still rides.** Per-project behavior matches `/anduin`
  exactly. Rhovanion posts, transitions, and forges nothing of its own — it only
  probes, orders the many, and sums their reports. Every comment, verdict, and PR
  is Anduin's (and Glorfindel's and Aulë's beneath it).
- **One global list, not per-project.** The projects to sweep come from
  `pipeline_projects.md` — a flat list of `<tracker> <project> --filter …` lines,
  set once.
- **The cursor is the gate.** A per-project cursor in `pipeline_cursors.md` records
  the epoch-ms of each project's last ride. The probe counts in-scope tickets
  updated since that mark; **zero moved → skip, paying one query; some moved →
  ride the full pipeline, then advance the cursor.** This is what keeps a hot watch
  from re-planning still boards every tick.
- **Sequential across projects.** Rhovanion rides one project's Anduin to its end
  before the next. No two pipelines contend; the order is the list's order.
- **A project error does not sink the rest.** A probe that fails (credentials gone,
  tracker unreachable) or an Anduin that errors makes that one row stop with its
  error — Rhovanion records it and rides on to the next river.

## Argument parsing

`/rhovanion [--dry-run] [--confirm]`

| Argument | Required | Meaning |
|---|---|---|
| `--dry-run` | no | Probe every project and report what *would* ride; pass `--dry-run` to each dispatched `/anduin` (plans/reports, forges nothing). **Cursors are not advanced** — a dry pass must not blind the next real run. |
| `--confirm` | no | Pass `--confirm` to each dispatched `/anduin` (prompt before each council post and each PR-open). Cursors advance on each ride. |

There is **no project argument** — the projects come from the global list. There is
no `--auto` to type: like `/anduin`, the forge runs **unattended by default**; the
gate flags are how you turn it off.

> **The forge blast radius is the default, by design.** Bare `/rhovanion` dispatches
> each moved project's `/anduin` with no gate, and `/anduin` forges unattended up to
> its `--max` (default 3) per pass. So a bare sweep opens real PRs across every moved
> project, and `/amon-sul rhovanion …` does so every tick a project stirs. The brakes
> are `--dry-run` (forge nothing) and `--confirm` (prompt per PR). Prefer a
> `--dry-run` watch first to see what would forge before arming the real thing.

## The two memory files

Both live under `~/.skadi/rhovanion/` — the global skadi store, beside `/handoff`'s and
`/moria`'s own state. They are **not** in the per-project memory directory (where
`default_filters.md` and `repo_routing.md` live): the watershed is yours across every
project, and — crucially — the cursor is persistent state. Were it keyed per working
directory, summoning Rhovanion from a different folder would find no cursor, read every
project as cold-start, and re-forge the whole watershed. A fixed global path reads the
same from anywhere.

### `pipeline_projects.md` — the list, set once

Its body is a flat list of pipeline lines, one per project (a leading `- ` is
optional). Each line is an `/anduin` invocation **less its gate flags** — tracker,
project, the straddle filter, and an optional per-project `--max`:

```
- youtrack URD --filter "#Unresolved"
- jira     PSG --filter "statusCategory != Done" --max 2
- youtrack MET --filter "#Unresolved"
```

- **No file, or no lines** → stop with: *"Rhovanion has no rivers to walk — add
  pipeline lines to pipeline_projects.md."*
- The **filter must straddle Open and the `forth` state**, exactly as `/anduin`
  requires (`#Unresolved` on YouTrack, `statusCategory != Done` on Jira) — else the
  forge stage never sees a council-advanced ticket. If a line's filter is a
  single-state scope, warn once per that line and ride it anyway; the hand-off
  stalls but the council stage still works.

### `pipeline_cursors.md` — the state, written by Rhovanion

Keyed by `<tracker>:<project>`, each value the epoch-ms of that project's last
ride. Rhovanion reads it before each probe and rewrites it after each ride:

```
youtrack:URD = 1718590440000
jira:PSG     = 1718575200000
youtrack:MET = 1718586300000
```

- **No file, or no entry for a project** → cursor `0` (cold start): every in-scope
  ticket counts as moved, so the project rides its first pass.
- Rhovanion creates the file on first write if absent.

## Workflow

### 1. Resolve the rivers

Read `pipeline_projects.md` and parse its lines in listed order, each into
`<tracker> <project> <filter> [--max N]`. If none, stop per the list rule above.
Read `pipeline_cursors.md` once into memory (absent → all cursors `0`).

### 2. Probe and ride each river, in turn

For each project line, in order:

a. **Capture `now_ms`** — the current epoch-ms, the prospective new cursor for this
   project. Read it once, before the probe, so a write landing mid-ride is caught by
   the next pass rather than silently swallowed.

b. **Cheap probe.** Look up the project's cursor (default `0`). Run the probe hook
   for its tracker through the Bash tool:
   - **youtrack** → `~/.claude/hooks/rhovanion-youtrack-probe.sh <project> <filter> <cursor>`
   - **jira** → `~/.claude/hooks/rhovanion-jira-probe.sh <project> <filter> <cursor>`

   The hook prints a single integer — in-scope tickets updated since the cursor.
   Anything that is not a plain integer — a JSON object, a non-zero exit, an empty
   or malformed line — is a **probe error**: record the row as
   `error — probe failed`, leave the cursor untouched, and continue to the next
   project. Never let one probe failure sink the sweep.

c. **Zero moved → skip.** Record `quiet (probe)`. Cursor unchanged. The pipeline is
   not dispatched — this is the whole saving.

d. **Some moved → ride.** Dispatch `/anduin` through the Skill tool with the line's
   tracker, project, and filter, the line's `--max` if present, and the gate flag:
   - **bare** → `/anduin <tracker> <project> --filter <filter> [--max N]` — forge unattended.
   - **`--dry-run`** → `/anduin <tracker> <project> --filter <filter> [--max N] --dry-run`.
   - **`--confirm`** → `/anduin <tracker> <project> --filter <filter> [--max N] --confirm`.

   Let Anduin do its whole job — both stages, the decider, the merged-ticket close,
   its combined report and verdict. Hold its `Anduin — STIRRED`/`QUIET` line.

e. **Advance the cursor** — set `<tracker>:<project> = now_ms` — **only on a real
   ride** (bare or `--confirm`). On `--dry-run`, leave the cursor unchanged, so the
   next real run still sees the movement.

After the loop, write `pipeline_cursors.md` back if any cursor advanced.

### 3. Aggregate the report and verdict

Print one block:

```
Rhovanion — sweep of <N> river(s)

| # | Project       | Probe   | Outcome                          |
|---|---------------|---------|----------------------------------|
| 1 | youtrack:URD  | moved 2 | Anduin — STIRRED (forged 1/3)    |
| 2 | jira:PSG      | quiet   | skipped (cursor current)         |
| 3 | youtrack:MET  | error   | probe failed — <one-line reason> |

Total: <N> project(s) — <r> rode, <s> skipped, <e> error.

Rhovanion — STIRRED   (or)   Rhovanion — QUIET
```

Decide the verdict:

- **STIRRED** if any ridden project's Anduin returned `Anduin — STIRRED`.
- **QUIET** if every project was skipped, errored, or rode to `Anduin — QUIET`.

The verdict line is the contract an adaptive watcher reads to set its streak. Always
emit exactly one of the two tokens.

> **Wrapping in `/amon-sul`.** `/amon-sul rhovanion [--dry-run|--confirm] [--active HH-HH]`
> rides Rhovanion on the adaptive back-off ladder, reading this verdict line each
> tick to pace itself. The cursor gate is what makes the hot ticks cheap: a single
> busy project keeps the timer at 5 minutes, yet the still projects cost only their
> probe. For a fixed cadence without the ladder, `/loop /rhovanion` serves.

## Rules

- **Rhovanion never posts, transitions, or forges of its own.** Every write is
  Anduin's (and its riders' beneath it). Rhovanion probes, orders the rivers, and
  sums the reports.
- **Sequential across projects, always.** One project's Anduin finishes before the
  next begins. Never dispatch them in parallel — the sequence is the cure for
  contention, exactly as within `/anduin`.
- **The cursor advances only on a real ride.** A `--dry-run` pass changes no cursor,
  so it never blinds the next real run. A probe error changes no cursor either — the
  movement it failed to read is still owed.
- **External PR-merges are caught on the next movement ride, not instantly.** A PR
  merging on the forge leaves no ticket update, so the probe does not see it; Aulë's
  merge-close (Anduin's step 5b) runs the next time that project's tickets move and
  it rides anyway. A project with no further movement keeps its merged ticket open
  until something stirs it. This is the price of a tracker-only probe — named here,
  not hidden. (To force a full sweep regardless of cursors, clear
  `pipeline_cursors.md`.)
- **The projects come only from `pipeline_projects.md`.** Rhovanion does not discover
  projects — an explicit list, no surprises.
- **A per-project error does not halt the sweep.** Record the row and continue.
- **Do not duplicate Anduin's logic** — dispatch the skill. One source of truth for
  the per-project pipeline, as Anduin is for the council→forge sequence and Moria is
  for the per-repo mend.
- Do not surface tracker or forge tokens in logs, responses, or saved files.
- Sweep order is the order the lines appear in `pipeline_projects.md`.
