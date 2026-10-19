---
name: moria
description: Use when the user runs /moria [--scope mine|all] [--dry-run] [--auto] [--confirm]. Sweeps every repo in your global mend list (mend_repos.md) for open PRs/MRs bearing unaddressed comments — loops /durin --repo over each root in turn, then prints one combined report ending in a plain STIRRED/QUIET verdict. Mend follows comments across all your repos, on no project's schedule. The forge of each repo is auto-detected from its origin (github | gitlab). Per-repo behavior matches /durin exactly; one global list, set once.
purpose: Sweeps every repo in the global mend list for unaddressed PR/MR comments.
user_invocable: true
stage: vigil
composes: durin:dispatch+mend
---

# Moria — The Realm of Many Halls

Durin walked the doorways of one hall; Moria is the whole realm beneath the
mountains, hall upon hall, gate upon gate. So this skill: where `/durin` sweeps the
open doors of one repo, Moria walks every repo in your keeping, summons Durin at each,
and brings back one report of all. Mending follows the comments that gather on your
PRs wherever they land — it answers to no single project's forge pass.

## Ethos

- **Moria walks; Durin still sweeps.** Per-repo behavior matches `/durin --repo`
  exactly. Moria mends nothing of its own — it only orders the many and sums their
  reports. Every amending commit is Durin's (and Narvi's beneath it).
- **One global list, not per-project.** The repos to sweep come from `mend_repos.md` —
  a flat list of repo roots, set once. Mend is decoupled from any council→forge
  pipeline: a comment may land on any repo at any time, and Moria answers them all.
- **One outer gate, not N.** Moria asks once before the whole sweep, then dispatches
  each repo's Durin with `--auto` — the human's word, given up front, stands for every
  hall. This mirrors how `/durin` owns one gate and dispatches `/narvi --no-confirm`.
  `--auto` skips even the outer gate; `--dry-run` writes nothing and needs none.
- **Sequential across repos.** Moria rides one repo's Durin to its end before the
  next. No two sweeps contend; the order is the list's order.
- **A repo error does not sink the rest.** A root that is no git tree, or whose
  `origin` resolves to no known forge, makes that one Durin run stop with its own
  error — Moria records it and rides on to the next hall.

## Argument parsing

`/moria [--scope mine|all] [--dry-run] [--auto] [--confirm]`

| Argument | Required | Meaning |
|---|---|---|
| `--scope mine\|all` | no | Passed to each `/durin`. `mine` (default) — PRs/MRs you authored. `all` — every open PR/MR in each repo. |
| `--dry-run` | no | Render each repo's manifest, write nothing. Each `/durin` runs with `--dry-run`; no outer gate (nothing writes). |
| `--auto` | no | Skip Moria's outer gate; sweep unattended. Each `/durin` runs with `--auto`. |
| `--confirm` | no | Redundant with the default-on outer gate; accepted for parallel with `/durin` and `/glorfindel`. |

There is **no repo argument** — the roots come from the global list.

## The global list

Read `mend_repos.md` from `~/.skadi/moria/` — the global skadi store, beside
`/handoff`'s and `/rhovanion`'s own state. It is **not** in the per-project memory
directory (where `repo_routing.md` and `default_filters.md` live), for the mend list
is yours across every repo, not any one project's — so it reads the same from
whatever directory you summon Moria. Its body is a flat list of absolute repo roots,
one per line (a leading `- ` is optional):

```
- /Users/you/metis_app
- /Users/you/metis_core
- /Users/you/skadi
```

- **No file, or no roots** → stop with: *"Moria has no halls to walk — add repo roots
  to mend_repos.md."*
- A line that is not an existing git tree is **kept** in the sweep — Durin's own
  `--repo` validation will surface it as a per-repo error, so the report names the
  broken root rather than silently dropping it.

## Workflow

### 1. Resolve the halls

Read `mend_repos.md` and parse its roots in listed order. If none, stop per the
global-list rule above.

### 2. The gate

Render the halls to be swept:

```
Moria — <N> hall(s) to sweep — scope <mine|all>
  1. /Users/you/metis_app
  2. /Users/you/metis_core
  3. /Users/you/skadi
```

Then:

- **`--dry-run`** → proceed straight to step 3 with per-repo `--dry-run`; nothing
  writes, so no approval is needed.
- **`--auto`** → skip the gate; proceed to step 3 with per-repo `--auto`. The flag is
  the human's word for the whole sweep, given up front.
- **Otherwise** (bare, or `--confirm`) → AskUserQuestion (options: `sweep all <N>` /
  `abort`). On `abort`, stop. On `sweep all`, proceed to step 3 with per-repo `--auto`
  — the human's word now covers every hall.

The slash invocation alone is not authority for a forge-write across N repos; the
outer gate is on unless `--dry-run` or `--auto`.

### 3. Sweep each hall (Durin)

For each root in turn, invoke `/durin` through the Skill tool with `--repo <root>`, the
resolved gate flag, and `--scope`:

- **dry-run path** → `/durin --repo <root> --scope <scope> --dry-run`.
- **otherwise** → `/durin --repo <root> --scope <scope> --auto`.

Use the Skill tool with `skill: durin`, `args: "--repo <root> ..."`. Each Durin runs
unattended (`--auto`) or read-only (`--dry-run`) — its own outer gate never prompts,
because Moria already took the human's word in step 2. Let each run do its whole job —
detect that repo's forge, list the open PRs/MRs, build the unaddressed-comment manifest
(dedup by trail marker), the per-URL Narvi dispatch, and its aggregate report. Hold
each report.

A Durin-side error or abort on one root does not halt Moria — record the row and ride
on to the next.

### 4. Aggregate the report and verdict

Print one block:

```
Moria — sweep of <N> hall(s) — scope <mine|all>

| # | Repo       | Forge  | Outcome                              |
|---|------------|--------|--------------------------------------|
| 1 | metis_app  | github | forged 3/3 across 2 PR               |
| 2 | metis_core | gitlab | quiet — no unaddressed comments      |
| 3 | skadi      | —      | error — <path> is no git tree        |

Total: <N> repo(s) — <x> mended, <y> quiet, <z> error.

Moria — STIRRED   (or)   Moria — QUIET
```

Decide the verdict:

- **STIRRED** if any repo's Durin landed a commit — any per-URL outcome `forged N/N`,
  `forged M/N`, `verify-failed`, `weigh-failed`, or `push-failed` on any PR/MR in any
  hall.
- **QUIET** if every hall was quiet — no unaddressed comments anywhere, or only
  `dry-run` / `error` rows with no commit landed.

The verdict line is the contract an adaptive watcher reads to set its streak. Always
emit exactly one of the two tokens.

> **Wrapping in `/amon-sul`.** `/amon-sul moria --auto [--scope mine|all] [--active HH-HH]`
> rides Moria on the adaptive back-off ladder, reading this verdict line each tick to
> pace itself. **`--auto` is required** for an unattended watch — without it Moria's
> outer gate freezes the ride waiting for a word no one is there to give. For a fixed
> cadence without the ladder, `/loop /moria --auto` serves; or run `/moria` by hand.

## Rules

- **Moria never mends of its own.** Every write is Durin's (and Narvi's beneath it).
  Moria orders the halls and sums the reports.
- **Sequential across repos, always.** One repo's sweep finishes before the next
  begins. Never dispatch them in parallel.
- **One outer gate, always on for non-dry-run runs unless `--auto`.** Per-repo Durin
  dispatch then uses `--auto` (or `--dry-run`) — Moria owns the gate, Durin does not
  re-ask, exactly as Durin owns the gate over `/narvi --no-confirm`.
- **The roots come only from `mend_repos.md`.** Moria does not scan directories for
  git trees — an explicit list, no surprises, no knocking on a repo you did not name.
- **A per-repo error does not halt the sweep.** Record the row and continue.
- **Do not duplicate Durin's logic** — dispatch the skill. One source of truth for the
  per-repo workflow, as Durin is for the per-URL one.
- Do not surface forge tokens in logs, responses, or saved files.
- Sweep order is the order the roots appear in `mend_repos.md`.
