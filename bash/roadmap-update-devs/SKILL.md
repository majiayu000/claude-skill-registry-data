---
name: "Roadmap: Assign Devs"
description: "Interview-led assignment of roadmap tasks to devs: collect the team roster, walk the chosen tasks in batches, write the approved assignee changes to roadmaps.json"
when_to_use: "When roadmap tasks need owners: a fresh roadmap with nobody assigned, a new dev joining, one dev's load to hand over or a rebalance before a sprint. For setting the assignee on a single task as it is added, roadmap-update-tasks already asks."
model: sonnet
effort: medium
metadata:
  glyph: ᛊ
  family: roadmap
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Edit", "Bash(python3:*)"]
arguments: ["horizon", "scope", "where", "roadmap"]
argument-hint: "[ready|open] [free|taken|all|<dev>] [<phase>|current[:project|focus|<tiers>|<milestones>]] (defaults: ready free current:project)"
---

# Roadmap Dev Assigner

Sets the `assignee` field on many tasks in one sitting. The user decides every assignment; this skill supplies the structure: which tasks are in play, what each dev already carries and a reply grammar short enough that 30 tasks take a few lines of typing.

Shared conventions: `~/.claude/library/references/roadmap-conventions.md`. The CLI is `python3 "$HOME"/.claude/library/scripts/roadmap.py`.

**Hard rule, inherited from the conventions:** an assignee is never inferred. Never propose, pre-fill or hint at a dev for a task, whether from its description, category, milestone, git history or who owns the tasks around it. Show facts; the user picks.

---

## Step 0: Parse the arguments

Every argument is optional, but they are positional: passing argument N requires arguments 1 to N-1. Defaults are `ready free current:project`.

| # | Argument | Value | Meaning |
|---|---|---|---|
| 1 | `$horizon` | `ready` (default) | only tasks that are currently unblocked (effective status `todo`) and unclaimed |
| 1 | `$horizon` | `open` | every unfinished task: any status except `done` and `out_of_scope` |
| 2 | `$scope` | `free` (default) | only tasks with no `assignee` |
| 2 | `$scope` | `taken` | only tasks with an `assignee` |
| 2 | `$scope` | `all` | every task inside the horizon, assigned or unassigned |
| 2 | `$scope` | `<dev>` | only tasks assigned to that dev (case-insensitive match) |
| 3 | `$where` | `<roadmap>[:<filter>]` | which phase, and which slice of it (below) |
| 4 | `$roadmap` | a path | the `roadmaps.json` to use; recognised by ending in `.json` or containing a `/`, so it never collides with `$where` |

**`$where`** is `<roadmap>:<filter>`, split on the **last** `:`. When passed, `<roadmap>` is required and `<filter>` is optional.

| Part | Value | Meaning |
|---|---|---|
| `<roadmap>` | `current` (default) | the only active phase, or the one the user picks in Step 1 when several are active |
| `<roadmap>` | a phase name | that phase, matched case-insensitively against the active phases |
| `<filter>` | `project` (default) | the whole phase |
| `<filter>` | `focus` | tasks in the tier now underway (the lowest tier with unfinished work) |
| `<filter>` | `<tiers>` | comma-separated tier words: `core`, `secondary`, `tertiary`, … (tasks in milestones of those tiers) |
| `<filter>` | `<milestones>` | comma-separated milestone ids: `M2,M4` |

Tiers and milestones are mutually exclusive in one call. `M2,secondary` is a hard stop.

Matching is case-insensitive. A multi-word dev name or phase name arrives quoted (`"Mary Ann"`); take the quoted string whole. `free`, `taken` and `all` are reserved words in the scope slot, so a dev with one of those names needs the roadmap edited by hand.

Hard stop (print the usage line, run nothing, never guess) when: argument 1 is passed and is not `ready` or `open`; the phase name matches no active phase (list the active names); the filter mixes tiers and milestones; a tier word or milestone id is unknown for the phase, or `focus` has no tier underway (the CLI says which and exits 2; relay its message).

```text
Usage: /roadmap-update-devs [ready|open] [free|taken|all|<dev>] [<phase>|current[:project|focus|<tiers>|<milestones>]]
Defaults: ready free current:project
```

Before doing anything else, echo the resolved form so a defaulted argument is never a surprise: `→ ready free MVP:focus` (the phase name once Step 1 has resolved it).

---

## Step 1: Locate the roadmap and check the format

Run `python3 "$HOME"/.claude/library/scripts/roadmap.py detect`, appending `$roadmap` (argument 4) as the PATH argument when one was given. Exit **3** = old simple format: stop and tell the user to run `roadmap-migrate` first. Exit **2** = could not locate or parse: ask the user for the path. Proceed only on exit 0. Every later CLI call in this skill carries the same PATH.

**Phase selection.** Read `roadmaps.json` and list the phases without `archived: true`. A named `<roadmap>` in `$where` selects that phase (hard stop if it matches none). `current`: one active phase, use it; several, ask with AskUserQuestion which to work on, listing the last active phase in the array first and marking it recommended (the array is appended to, so last is most recent). Pass the choice as `--phase "{name}"` on every later CLI call. Never pick silently between active phases.

---

## Step 2: Collect the roster

The interview opens here, before any task is shown.

1. Gather the distinct `assignee` strings already present anywhere in the chosen phase, finished tasks included. These are names the roadmap knows; they are context for the question and carry no weight as assignments.
2. Ask in plain text (names are free text, so AskUserQuestion's fixed options do not fit):

   ```text
   Who is on the dev team? Give me the names, comma-separated.
   Already in this roadmap: {existing names, or "nobody yet"}.
   ```

3. Build the roster from the answer. The user's spelling is canonical. Where a roster name matches an existing assignee case-insensitively but the spelling differs (`jaz` in the roadmap, `Jaz` in the answer), say so and offer to normalise every occurrence to the roster spelling as part of this run's write; `next-task-suggest` filters on the string, so two spellings split one dev's tasks in two.
4. Give each roster member a short handle for the reply grammar: the shortest unique case-insensitive prefix of the name (`j` for Jaz and `m` for Max; `ja` and `jo` for Jaz and Jo). Print the roster with handles once.
5. An existing assignee the user left off the roster stays on their tasks untouched. Mention each such name once; the user may have left the team member out on purpose.

**Named-dev scope check.** When `$scope` is a dev's name and no task in the phase carries it (case-insensitive), say `No task in {phase} is assigned to {name}.`, list the assignees that do exist and stop.

---

## Step 3: Build the working set

Both horizons come from the CLI, so status, claims and tiers are never re-derived. Pass the `$where` filter through: `--milestones M2,M4` for a milestone list, `--tiers core,secondary` for a tier list, `--tiers focus` for `focus`, and nothing for `project`.

- `$horizon` = `ready`: run `roadmap.py ready --json {filter flags}`. The `candidates` array is the complete unblocked, unclaimed set inside the filter, already ordered by leverage, each with `assignee` (empty string when unassigned). Claimed tasks sit apart in its `claimed` list: someone is already working on them, so they are not up for assignment here.
- `$horizon` = `open`: run `roadmap.py open --json {filter flags}`. `candidates` holds every task inside the filter that is not `done` or `out_of_scope`, each with `status`, `display` and `started`. A task with a `started` date is claimed: show it, but flag any proposal to move it to someone else, since that hands over live work. If `roadmap.py validate` reports status discrepancies, tell the user and suggest `roadmap-maintain` first; carry on if they say so, since assignment does not depend on status being fresh.

Filter by `$scope` (`free`: empty `assignee`; `taken`: non-empty; `all`: no filter; `<dev>`: case-insensitive match). An empty working set is a result: report it (`Every ready task in M2 already has a dev.`) and stop.

Compute the **load table**, which the interview reprints as it changes: for each roster member, the count of unfinished tasks they hold across the whole phase, split into in progress (claimed), ready and not-yet-ready, plus one row for unassigned.

```text
Working set: {N} tasks ({horizon}, {scope}) in {phase} · {filter}

Load now        in progress   ready   later   total
  Jaz (j)                 1       2       4       7
  Max (m)                 0       0       1       1
  unassigned              0       6      11      17
```

---

## Step 4: Assign in batches

Split the working set into batches by milestone, in milestone order. A milestone with more than 10 tasks in the working set splits again by topic (the letters between the milestone number and the sequence in the task ID: `2TI.3` → `TI`); a topic still over 10 splits into runs of 10. Keep the Step 3 ordering inside each batch.

Show one batch at a time, numbered from 1 within the batch:

```text
Batch 2 of 5 · M2: Search ({milestoneDonePct}% done) · 4 tasks

 #  ID      Status   Now   Upstream owners   Task
 1  2SE.1   todo     none  none              {full description}
 2  2SE.2   blocked  none  2SE.1 (none)      {full description}
 3  2SE.4   blocked  Max   2SE.2 (none)      {full description}
 4  2TI.3   todo     none  1IN.2 (Jaz)       {full description}

Assign: "<rows> <dev>" clauses split by ";". Example: 1-2 j; 4 m
```

- **Status** reads `in progress` for a claimed task (one with a `started` date) that is `todo` or `blocked`; a paused, deferred or finished status shows as itself.
- **Now** is the current assignee. **Upstream owners** lists the task's direct `dependsOn` tasks with their assignee in brackets; assignments made earlier in this run show up here, and milestone and gate dependencies are omitted. It is a fact about the graph and never a recommendation.
- Full descriptions always; wrap long ones and never truncate.
- Print the grammar reference below in full with the first batch, then only the one-line reminder shown above.

**Reply grammar**

| Reply | Effect |
|---|---|
| `1-3 j` | rows 1 to 3 go to the dev whose handle is `j` |
| `1,4 max` | rows 1 and 4 to Max (full names and handles both work) |
| `all j` / `rest j` | every row / every row not named in an earlier clause |
| `2 -` | clear row 2's assignee |
| `1-2 j; 3 m; rest -` | several clauses, split by `;` or new lines |
| `skip` | leave the whole batch as it is |
| `back` | reopen the previous batch |
| `done` | stop here and go to the proposal with what has been decided |
| `+ Priya` | add a dev to the roster mid-run; handles are recomputed and reprinted |

Rows a reply does not mention stay unchanged. A row named in two clauses, a row number outside the batch or a handle matching no one (or more than one dev): change nothing, quote the offending clause and ask again for that batch only. Never resolve an ambiguous reply by guessing.

After each batch, confirm in one line what was recorded (`2SE.1, 2SE.2 → Jaz · 2TI.3 → Max · 2SE.4 stays with Max`) and reprint the load table with the pending changes applied. Nothing is written to disk during this step.

---

## Step 5: Prepare the proposal (do not edit yet)

```text
Assignee changes: {N} tasks in {phase}

New assignments
  2SE.1   none → Jaz   {description}
  2TI.3   none → Max   {description}

Reassignments
  2SE.4   Max → Jaz    {description}

Cleared
  3UI.2   Jaz → none   {description}

Spelling normalised: "jaz" → "Jaz" on {n} tasks

Load            before   after
  Jaz (j)            7      10
  Max (m)            1       1
  unassigned        17      14

Still unassigned in this working set: {n}
```

Omit any section with no rows. Reassignments and clears take a dev's name off a task, so they always get their own sections; never fold them into the new assignments.

Then ask with AskUserQuestion: **Apply** / **Revise a batch** / **Cancel**. Revise returns to Step 4 at the batch the user names and comes back here afterwards. Cancel writes nothing.

---

## Step 6: Write (once approved)

Edit `roadmaps.json` only. Assignee has no projection in the PHASE file or `ROADMAP_OVERVIEW.md`, so neither is touched.

- **Set or replace**: `"assignee": "{roster spelling}"`, placed by the conventions' task field order (after `notes` when present, before `started` and `pr` when present).
- **Clear**: delete the `assignee` line entirely and fix the trailing comma on the line before it. Never write an empty string; the field is omit-when-empty.
- Tabs for indentation; leave every other field, including `status` and `started`, as found.
- One Edit per task, anchored on the task's `"id"` line so the match is unique. Never use `replace_all` for spelling normalisation: similar names can share a prefix, so each occurrence is edited on its own.

---

## Step 7: Validate and report

Run `roadmap.py validate`; it must report clean, and a discrepancy that was present before Step 6 is reported as pre-existing. If an HTML dashboard exists (`docs/artefacts/roadmap-*.html`), refresh it with `roadmap.py render`, since its dev chips come from this field.

Report: the count of tasks changed; the final load table; how many tasks in the working set are still unassigned; any roster member who ended with nothing. Close with the one next action that fits, for example `/next-task-suggest Jaz` to pull that dev's highest-leverage ready task.

---

## Conventions

- `assignee` is free text with no roster stored in the roadmap. The roster from Step 2 lives only for this run; it is asked for every time.
- `roadmaps.json` is the source of truth. Statuses, field order, formatting and everything else: `~/.claude/library/references/roadmap-conventions.md`.

<raw-arguments value="$ARGUMENTS" />
