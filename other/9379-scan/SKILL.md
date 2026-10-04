---
description: "Proactively hunt unobserved bugs in resting code: a read-only two-stage scan, recall-biased per-lens hunter subagents, then a separate fresh-context default-refute gate, over a target path/feature/diff or a rotated lane, emitting only verified 5-field findings. Use when: 'find a bug', 'bug hunt', 'scan for bugs', 'hunt for bugs in <X>'. Skip when: reviewing a diff (`review:code-review`); security auditing (`review:security-review`); root-causing an observed failure (`debugging:debug`); doc/config/code/arch claim drift, all dimensions (`codebase-health:audit`); structural tidying (`code-tidying:tidy`); comment markers (`work-items:scan-todos`); coverage gaps (`testing:audit`, `mutation-testing:audit`). Disambiguation: 'scan repo for issues' is the upstream known-issue registry (`harness-ops:known-issues`); 'file a bug' the user observed is `bugs:write`. Bare invocation neither edits nor files; `--track` files verified findings as raw intake (subject to the team's `filing_posture`)."
argument-hint: "[<path|feature|diff>] [--lane <name>] [--track] [--dry-run]"
user-invocable: true
disable-model-invocation: false
shell: bash
metadata:
  workflow-stage: operator
  summary: Proactively hunt resting code for unobserved bugs, verify adversarially, report read-only
  cadence: daily
---

## Repository context. Gather first

Collect these with **individual** Bash calls, one command per call, never combined into a single
invocation:

- Current branch, `git branch --show-current`
- Recent commits, `git log --oneline -10`
- Shallow clone, `git rev-parse --is-shallow-repository`

Treat a failure (not a repository, git unavailable) as an unknown value and carry on. Keep these as
separate body Bash calls rather than pre-compute lines: the harness runs a skill's whole pre-compute
block as one shell invocation, and a worktree-isolated session refuses a compound command that
contains git.

## Pre-computed context

Lane config: !`ls "${CLAUDE_PROJECT_DIR:-.}/.claude/bugs.md" 2>/dev/null || echo "absent — bundled default lanes apply"`

Consumer gotchas:
!`bash "${CLAUDE_PLUGIN_ROOT}/scripts/concat-gotchas.sh"`

## Variables

Arguments: `$ARGUMENTS`

## Purpose

`/bugs:scan` is the front of the bug lifecycle: it hunts defects **nobody has observed yet**, in
code that is resting. Every other finding-producer in reach needs an oracle first, a diff, a failing
test, a stack trace, a factual claim, a comment marker. This one needs none of them.

One invocation is **one bounded pass**: hunt a target (or a rotated lane), verify each candidate
through a separate fresh-context gate, report what survives in the plugin's five-field shape, stop.
That makes it equally usable interactively ("find a bug in the billing module"), from a `/loop`, or as
a daily operator routine, the same bounded unit either way.

The design premise, taken from published practice: per-run recall is low and the raw false-positive
rate is high, so **recall and precision are separated into two stages**. Hunters are told to be
generous; the verification gate is told to refute. A finding that reaches the report survived an agent
whose job was to kill it.

## Verb contract. Read-only toward the repository

Bare invocation is **read-only**: it never edits code, never branches, never pushes, never files a
tracker item. Filing sits behind `--track`, and model auto-invocation never supplies `--track` on its
own. A user (or a standing lane rule) must ask for it.

**Reconciliation:** persisting the findings report and its cursor block under `${CLAUDE_PLUGIN_DATA}`
is plugin-owned state, not target-repo mutation. The scanned repository's working tree, index, and
history are untouched by a bare run. `--dry-run` goes further: it emits the findings to stdout and
persists **nothing**. No report file, no cursor advance, no filing.

Durable cursor state never lives in `.work/`. Anything a wrapping session leaves under `.work/` is a
checkout-local cache that a fresh clone or a `git clean` erases; the ladder below must re-derive the
cursor from rungs 1–3 without it, and never treats a cache note as authority.

**Durability on a cloud or scheduled run.** `${CLAUDE_PLUGIN_DATA}` is ephemeral on a cloud session
and unreachable from the next scheduled run on another host, so the persisted report and its cursor
vanish with the container. On such a run pass `--track`: a filed item is the only output that
survives, and it is also what rung 1 of the cursor ladder reads back. Without `--track` a cloud run
is a one-off whose findings live only in the transcript.

## Modes

| Argument | Mode | Behavior |
|---|---|---|
| `<path>` / `<feature>` / `<diff-ish ref>` | **Targeted** | Hunt exactly that scope. No lane rotation, no cursor advance. |
| `--lane <name>` | **Named lane** | Hunt the named lane's globs. Advances the cursor to that lane. |
| *(empty)* | **Rotation** | Self-select the next lane via the cursor ladder, then hunt it. |
| `--track` | **Filing** | After reporting, file verified findings as raw intake (see below), subject to the team's `filing_posture` and the filing ladder in Step 7. Composable with any mode. |
| `--dry-run` | **Plan-and-report only** | Full hunt + verification, report to stdout, zero persistence and zero cursor advance. Composable with any mode; overrides `--track`. |

Lane definitions (`lanes`, `filing_posture`) resolve from `.claude/bugs.md` per the cascade
contract. Keys, layers, and merge semantics live in
[`${CLAUDE_PLUGIN_ROOT}/reference/config.md`](../../reference/config.md), which is their single home.
When no layer declares lanes, use the bundled generic default lanes in
[`context/lenses.md`](context/lenses.md).

## Cursor ladder (rotation mode)

Which lane comes next is derived **statelessly**, first rung that answers wins:

1. **Tracker history.** When the `work-items` plugin is installed and a tracker binding resolves,
   search items (`--state all`) for the provenance line `Filed by /bugs:scan (lane: <name>)`.
   The most recently filed lane is the previous lane; take the next one in declaration order. The
   search must be an **exact match** on that line (the seam's search verb, or the provider's literal
   body match with the string quoted): a semantic or fuzzy search cannot tell "no match" from
   "missed", so it is not an answer. When only a fuzzy search is available, or no search ran against
   a bound tracker, print why and fall through to rung 2; confirm the search actually ran against a
   bound tracker before trusting an empty result. An unbound tracker returns nothing, which is not
   the same answer as "no prior scan filings".
2. **Persisted-report cursor.** Otherwise resolve the report directory by the **same precedence
   persistence uses**. Step 5 below defers to `/bugs:write`'s Step 4, and so does this rung;
   reading a directory reports no longer land in is how a configured `output_dir` silently strands the
   cursor. Then search **backward from the newest report** for the newest one carrying a *valid*
   rotation cursor block, one that names the rotation lane (see
   [`context/findings-report.md`](context/findings-report.md)), and use it the same way. Reports
   without such a block are skipped, not read as a cursor: `/bugs:write`'s reports share that
   directory and carry none, and a targeted scan's report must never advance rotation. If no report
   carries one, fall through to rung 3.
3. **Date-derived floor.** Otherwise pick deterministically: index the declared lane list by
   `(days since 1970-01-01 UTC) mod (lane count)`. Zero state, no history, still rotates daily.

State the rung you used in the report. An operator reading a rotation run should be able to tell
tracker-derived rotation from the zero-state floor.

**Reset semantics.** Deleting the plugin-data reports (or scanning from a fresh machine) drops the run
to rung 3, which is a valid state, not an error. `<project-slug>` is the kebab-cased basename of the
project root, so two checkouts sharing a basename (`~/work/api` and `~/oss/api`) share one cursor
directory. Name the absolute project root in the report so a reader can spot the collision. Two
sessions started the same day on a zero-state checkout will select the **same** lane; that is accepted
(the dedupe steps below absorb the duplicate findings) rather than jittered, because a
deterministic floor is what makes daily coverage predictable.

## Budget

- **Stop condition:** 3 verified findings, or the lane's budget-bounded sample is complete.
- **Candidate cap:** at most 10 candidates per hunt wave reach the verification gate (5 on a small
  scope, per the sizing table). Rank by evidence strength and drop the tail rather than widening the
  wave; the dropped tail is reported, never discarded.
- **Refill cap:** if a whole wave is refuted, at most **2** refill waves. Then report the refuted set
  and stop. An unbounded refill loop is a token sink against a ~1:50 signal-to-noise base rate.
- **"Lane exhausted" means the sample is complete, not that the lane is bug-free.** The scan is
  budget-bounded sampling; never claim exhaustive coverage of a lane in the report.

Zero verified findings is a clean, successful outcome. Do **not** invent a finding to justify the run.

### Sizing. Model by stage, breadth by scope, effort as the ceiling

Cost follows what is scanned, and precision never pays for it. Three rules, applied in this order:

**Model by stage.** Each stage runs on the tier its job needs, passed through the Agent tool's
per-invocation `model` parameter, never on the session's top model. The tiers below are the
fleet's ordered capability tiers; which alias each one binds today is the loop-lane convention's
to state, not this skill's. Resolve it from the marketplace's
`docs/conventions/loop-lane/README.md` "Capability tiers", whose alias binding is dated and
carries its own recheck trigger:

| Stage | Tier | Why |
|---|---|---|
| Hunters (Step 2) | fast | The recall stage is generous by design and every output is refuted downstream, so a cheaper reader costs little precision and most of the run's tokens live here. |
| Gates (Step 4) | strong | The precision stage; the reproduction it runs is what makes a finding credible. |
| Main thread | the session's model, nothing passed | Orchestration and triage only. |

Name the alias that actually resolved in the report's run metadata, so a reader can tell which
binding the run used. A dispatch the harness rejects means the binding moved: report it and
re-read the owner doc rather than substituting an alias here.

**Breadth by scope.** After Step 1 enumerates the files (test suites excluded), classify the scope
and size the recall stage from it:

| Scope | Definition (files, or lines after hotspot ranking) | Lenses | Gate cap per wave |
|---|---|---|---|
| small | 5 files or 1,000 lines or fewer | 1 to 2, the highest-ranked for the surface | 5 |
| medium | 20 files or 5,000 lines or fewer | 2 to 3 | 10 |
| large | above | 4 | 10, refill waves allowed |

A targeted run over one file is small; a full lane is usually large. The scope class, the lens
count, and the models used go in the report's run metadata.

**Effort as the ceiling.** The [Effort](#effort) row bounds lenses and refill waves; scope picks
within it, never above it. A `low` run over a large lane still dispatches one lens.

### Effort

Caller effort for this run is `${CLAUDE_EFFORT}`. If that reads as a literal placeholder rather than
one of `low`, `medium`, `high`, `xhigh`, or `max`, this body was read directly instead of
skill-loaded, so the substitution never ran: treat the run as `high` and use the full budget above.

Effort scales the **recall stage only**. The verification gate is the precision machinery and never
relaxes: every candidate still faces a separate fresh-context refuting subagent at every level, and
"if uncertain, it is NOT a finding" binds at `low` exactly as it does at `max`.

| Effort | Lenses dispatched (step 2) | Refill waves | Stop condition |
|---|---|---|---|
| `low` | 1, the highest-ranked lens for the scope | 0 | first verified finding |
| `medium` | 2 | 1 | 2 verified findings |
| `high`, `xhigh`, `max` | up to 4, sized to the scope per the sizing table | 2 | 3 verified findings |

The gate cap per wave (10, or 5 on a small scope) holds at every level. Name the effort level and
the lens count in the report's run metadata, so a `low` run reads as the narrower sample it is
rather than as a clean lane.

## The scan pipeline

Process one unit at a time. One target, or one lane. A unit is closed when its verified findings are
reported and deduped (and filed, under `--track` when the team's `filing_posture` allows it); only
then does the cursor advance.

### Step 1. Resolve scope

Resolve the mode, the lane globs, and `filing_posture` from the config cascade. Enumerate the concrete
file list and drop test suites from it (`*.test.*`, `test_*`, `*.Tests.ps1`): hunters read a test to
learn a unit's contract and never hunt the test itself. If the enumeration exceeds ~40 files, narrow
to the highest-signal subset (recently changed, highest fan-in, most branch-dense) and say in the
report that you sampled. Then compute the hotspot reading order described in
[`context/lenses.md`](context/lenses.md), one git command per Bash call; on a shallow clone, print the
skip notice and continue unranked. Classify the scope as small, medium, or large per the
[sizing table](#sizing-model-by-stage-breadth-by-scope-effort-as-the-ceiling).

**Done when** you can name the exact file list the hunters will read, the order they read it in, and
the scope class that sizes the rest of the run.

### Step 2. Dispatch hunters (recall stage)

Dispatch **one subagent per lens** over the resolved scope, on the hunter tier the sizing table
names, each with the four-part contract: objective, output format, tool/source guidance, and task boundaries, spelled out
in [`context/lenses.md`](context/lenses.md). The scope class picks the lens count and the
[Effort](#effort) row is the ceiling. Every hunter is read-only, must attach a verbatim evidence quote
to every candidate, may follow one hop outside the scope (a direct caller or callee of a scoped file)
and tags such a candidate `out-of-lane`, and is explicitly told that **returning no candidate is a
valid and expected outcome**.

**Done when** every dispatched lens has returned.

### Step 3. Triage the candidate list (main thread, before any gate)

Seed, merge, and cut in the main thread, so no gate is spent on a duplicate or on a candidate whose
own hunter says nothing observable breaks:

1. **Seed from the prior tail.** On a rotation or named-lane run, read the newest persisted report
   for this lane (the directory rung 2 reads, resolved by the same precedence) and add its
   "Candidates not gated" rows to the list ahead of the hunters' output: each already carries a
   `path:line`, so at equal evidence strength it ranks first. A row whose quoted location no longer
   exists goes to the side observations. A targeted run has no lane and seeds nothing.
2. **Merge same-cause candidates.** Two lenses often reach one fault by different routes, and a
   seeded row often returns as a fresh candidate. Keep one candidate carrying both lens ids and the
   stronger evidence quote; the gate sees it once.
3. **Drop cosmetic-impact candidates.** A candidate whose stated impact is a comment, a log string,
   or a report field nothing consumes is a side observation, not a bug. Move it to the report's side
   observations rather than gating it.
4. **Rank by evidence strength and cut to the gate cap.** Done when the remaining list is at or
   under the cap. The tail above the cap is retained in the report's "Candidates not gated" section,
   which is what item 1 reads back on the next run over this lane.

Triage never confirms anything: it merges, drops, and orders. Every candidate that remains still
faces the gate.

**Done when** the list is at or under the gate cap and every merged or dropped candidate is accounted
for in the report.

### Step 4. Verification gate (precision stage)

Dispatch a **separate fresh-context subagent per candidate**, on the gate tier the sizing table
names, using the prompt contract in [`context/verification-gate.md`](context/verification-gate.md). The hunter that found a
candidate never grades it. A model re-checking its own work rubber-stamps it. The gate's default
stance is **refute**: it must try to construct the concrete input path that triggers the claimed
fault, and if it cannot, the candidate dies. **If uncertain, it is NOT a finding.**

Survivors are labeled `reproduced` (a check was actually run) or `verified-by-reading` (the fault is
established from the source, with the reproduction argument stated). Refuted candidates are **retained
with their refuting argument**. A high-kill gate catches some true positives, so they are never
silently dropped. A gate's one-line side observation (a stale comment, a weaker sibling check) goes to
the report's side observations.

**Done when** every candidate carries a verdict and a label or a refuting argument.

### Step 5. Assemble and dedupe the report

Format per [`context/findings-report.md`](context/findings-report.md): the five fields per finding
(from `/bugs:write`'s shape), plus the evidence label, the lens id, and the scope tag, then the refuted
tail, the candidates not gated, the side observations, and, on a rotation run, the cursor metadata
block with the sampled scope list; a targeted run emits the no-cursor line in its place. Before
persisting, run the same duplicate scan `/bugs:write` performs over the output directory. See Step 2
("Survey before you write") in [`${CLAUDE_PLUGIN_ROOT}/skills/write/SKILL.md`](../write/SKILL.md),
and drop or merge findings that restate a prior report.

Persist to the path `/bugs:write --file` resolves (its Step 4 owns that precedence:
`output_dir`, then `${CLAUDE_PLUGIN_DATA}/bug-reports/<project-slug>/`, then a project-local
fallback). Do not reinvent either mechanism here. Write the file with the **Write tool**: a shell
redirect or heredoc is what a repository's write guards block, and the plugin data directory is
outside any scratch exemption. Under `--dry-run`, skip persistence entirely.

**Done when** the report is emitted, and (outside `--dry-run`) persisted with its path stated.

### Step 6. `--track` filing (explicit only)

**Posture gate first.** Resolve `filing_posture` from the config cascade. See
[`${CLAUDE_PLUGIN_ROOT}/reference/config.md`](../../reference/config.md), whose bundled default is
`manual-only` when no layer declares it. When it resolves to `manual-only`, file nothing: print one
notice, "filing skipped: filing_posture is manual-only (<layer, or bundled default>); report-only", and stop at the report, the same degrade shape as an absent `work-items`. Only `allowed` reaches the
beats below.

Then apply the filing ladder in Step 7: on an interactive run only the findings the ladder routes
to the tracker are filed; on an unattended run every verified finding is. Then, presence-gated on
`work-items`, follow the dogfood-filing beats by invoking `/work-items:track add`, never by pathing
into another plugin's files:

1. **Dedupe.** Search items over `--state all` first; sameness is judged by underlying cause, not
   wording. An open match gets a comment instead of a second item; a closed match is reopened or
   linked from a fresh item.
2. **Categorize as raw intake.** A scan filing records what was observed, not a verified diagnosis.
3. **File** through `track add`, which owns the body template and the argv-safe write. The body
   carries the five fields, and a provenance line, `Filed by /bugs:scan (lane: <name>)`, which
   is what rung 1 of the cursor ladder later recognizes.
4. **Mark `needs-triage` from the live label set.** Apply that exact name when it exists. **Create no labels.** If it does not exist, say so and file without it.
   The filer does not self-triage.

**Degrade:** if `work-items` is absent, or no tracker binding resolves, do not improvise a filing path.
Print one notice, "filing skipped: <reason>; report-only", and stop at the report.

**Done when** each verified finding is filed, matched to an existing item, or explicitly skipped with a
printed reason.

### Step 7. Hand off through the filing ladder

The scan itself edits nothing. Where a verified finding goes next follows one ladder, so a small
fix does not become a tracker item and an unattended run never leaves work stranded in a transcript:

| Run | Finding | Route |
|---|---|---|
| interactive | **local**: its fix stays inside one plugin or module, changes no documented contract, and has an existing test file to extend | fix it now, in this session and branch, through `/implementation:implement` (or the project's own fix lane) |
| interactive | non-local, or needs a design decision | file it with `--track`, or ask the operator |
| any | security-relevant | file it, and route to the `/review:security-review` lane, which owns that surface |
| unattended (a loop, a routine, a lane rule that passes `--track`) | any | file it; nobody is present to fix it, and the tracker is the only durable output |

"Unattended" is declared by the caller, never inferred from the environment. Recommend the route,
do not auto-invoke it; a finding worth root-causing first goes to `/debugging:debug`. Nothing
verified: say so plainly and name the lane and rung, so the next run rotates on.

## Next

- Verified local finding, interactive run: `/implementation:implement`.
- Verified non-local or security-relevant finding: `/work-items:track add`, then
  `/review:security-review` for the security-relevant ones.
- A finding that needs root-causing before a fix: `/debugging:debug`.

## What this skill does NOT do

- **Does not edit code itself.** No patches, no PRs, from this skill. A verified finding leaves
  through the Step 7 ladder, which in an interactive session routes a local fix to the implement lane
  in the same session rather than to the tracker.
- **Does not file on bare invocation.** Filing needs `--track`.
- **Does not review a diff.** That is `/review:code-review`'s lane; this reads resting code.
- **Does not verify factual claims** in docs or config against code. All four `codebase-health:audit`
  dimensions own that.
- **Does not chase coverage gaps** (`testing:audit`, `mutation-testing:audit`), structural drift
  (`code-tidying:tidy`), or comment markers (`work-items:scan-todos`).
- **Does not emit `type: review-findings` frontmatter.** That frontmatter alone routes a report into
  the `/review:fanout` fix relay; a scan report is intake, not a detector-findings artifact.

## Gotchas

- **The hunter never grades itself.** If you collapse Steps 2 and 4 into one agent, precision collapses
  with them. The gate is a separate fresh-context dispatch, per candidate.
- **A cheaper hunter is fine; a cheaper gate is not.** The gate's reproduction is the whole precision
  claim, so it stays on the gate tier whatever the hunters ran on, and a scope class never lowers
  the gate's stance.
- **The ungated tail is a queue, not an archive.** Step 3 reads the prior report's "Candidates not
  gated" rows back before it merges; a run that skips the seed re-derives what the last run over
  the lane already paid for.
- **Triage merges and drops, it never confirms.** A candidate that survives triage still faces the
  gate; a candidate dropped as cosmetic is written to the side observations, not silently gone.
- **No evidence quote, no finding.** A candidate without a verbatim quote of the offending source is
  retracted at the gate, not "investigated further".
- **Refuted is reported, not deleted.** The refuted tail is a feature: it lets a human overturn a
  wrong kill, and it stops the same dead candidate resurfacing next run.
- **`--dry-run` must not advance the cursor.** A dry run that persists a cursor silently skips a lane
  on the next real run.
- **`--track` is not `--file`.** `--file` is `/bugs:write`'s flag for persisting a report to
  disk; the same token here would mean tracker mutation. This skill uses `--track` for filing.
- **Shallow clones degrade, they do not fail.** The hotspot ranking is skipped with a printed notice
  when history is absent; the four lenses read the scope unranked.
- **A lane with no verified findings is a result.** Report it, advance the cursor, do not refill past
  the cap looking for something to say.
- **Consumer `## Gotchas` concatenate after these bullets.** The pre-computed Consumer gotchas block
  is the cascade `## Gotchas` from `.claude/bugs.md` layers (user-global, team, local overlay) in
  layer order. Treat those lines as additional gotchas for this invocation. Missing layers are
  absent, not an error. Generalizable lines belong in this shipped skill via an issue, not in the
  consumer file.

## Reference index. Load on demand

| File | Load when |
|---|---|
| [`context/lenses.md`](context/lenses.md) | Step 2, writing each hunter's dispatch prompt; also holds the bundled default lanes. |
| [`context/verification-gate.md`](context/verification-gate.md) | Step 4, before dispatching the refute gate on a candidate. |
| [`context/findings-report.md`](context/findings-report.md) | Step 5, emitting the report, and the ladder's middle rung reading a prior cursor back. |
| [`${CLAUDE_PLUGIN_ROOT}/reference/config.md`](../../reference/config.md) | A `.claude/bugs.md` key decides the run (lane, rotation, filing posture) and its layer is unclear. |
| [`${CLAUDE_PLUGIN_ROOT}/skills/write/SKILL.md`](../write/SKILL.md) | Emitting a finding in the five-field shape, running the duplicate scan, or resolving where `--track` persists. |
