---
name: ghi-triage
persona: main-session
description: Use to triage the open GHI queue before planning or choosing what to pull; produces a ranked deliverable.
category: agent-operations
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-17
metadata:
  skill-version: "5.4.1"
model: sonnet
---

# ghi-triage

Real triage — read each issue, classify severity, recommend an order. The
bundled script does the deterministic work (fetch, route, render the
deliverable). The agent does the cognitive work (read each body, compose a
short WHY per issue). Determinism is enforced at the rendering boundary;
cognitive freedom lives only on the input edge.

## Invocation

```text
/ghi-triage              ← triage all open GHIs
/ghi-triage --label defect    ← filter to one label
/ghi-triage --limit 25        ← cap the scan
```

## Triage Procedure (binding — three steps)

When this skill is invoked, the agent MUST execute the three steps below
in order. There is no Rich table view, no per-GHI panel ceremony, and no
recommended-order intermediate table — those views were three redundant
restatements of the same data (GHI #324). The deliverable is the
rank-ordered list from Step 3, full stop.

### Step 1 — Pull structured records (single script call)

Run the script once with `--format json` to fetch the open queue, score
routing, detect duplicates, and emit one record per issue with the full
body inline:

```bash
uv run python .gzkit/skills/ghi-triage/scripts/triage.py [args] --format json
```

Each record contains: `number`, `title`, `labels`, `klass` (one of
`defect`/`enhancement`/`investigation`/`chore`/`unlabeled`), `body`
(full), `files_mentioned`, `dup_of`, `route`, `urgency`, `rationale`,
`blockers`, `family_signal`, `stale_annotations`, `created_at`,
`updated_at`. The `route` field is the script's
mechanical classification per `AGENTS.md` § Defect-fix routing — treat it as
evidence the agent reasons over, not as the final answer.

**`blockers` is the freshness instrument for `ghi-close` § Phase 1 step 1a.**
Each entry carries the blocker comment's `created_at`, its `references`
(`kind` / `identifier` / `state`), and `cites_settled`. A reference resolves
`live`, `settled`, or `unknown`; ADR and OBPI references are always `unknown`,
because their only repo-local index is a Layer-3 derived view. `rationale`
leads with `stale blocker: cites settled #N` when any citation has closed.

**The flag is a citation, not a verdict.** A blocker may name a closed GHI as a
*precondition* (it no longer gates — re-derive and proceed) or as *provenance*
("the pattern #585 established"). Nothing mechanical separates them, so the
script reports and the agent adjudicates. `unknown` is never reported as
settled: missing evidence is not evidence that a precondition cleared.

**`family_signal` and `stale_annotations` are the family-and-staleness pass
(row 4 of `docs/rnd/ghi-landscape-reorganization.md`). They are not peers.**

`stale_annotations` is **exact**. A body that writes `#889 (open)` transcribes a
Layer-2 fact GitHub already renders live, so whether that transcription still
holds is a lookup. Each entry names a reference whose subject has since closed.
The annotation is **decoration, not a precondition** — unlike `blockers`, a
decayed annotation gates nothing, and the body is never rewritten to fix it
(`#889 (open)` is a dated record of what its author observed). Read it as a
reason to discount the annotation and re-derive the relationship yourself. The
remedy is upstream: `ghi-author` § Step 4 no longer writes them.

`family_signal` is **candidate evidence with a measured error rate, never a
count**. It lists the doctrine-declared-without-mechanism phrases a body uses.
Measured 2026-09-20 against the 38 members
`docs/governance/f1-family-share-2026-09-20-evidence/measure.py` names among 57
open issues, it disagrees with that reader on 15 — 9 it matched that the reader
excluded, and 6 members no phrase catches (#950, #968, #997, #1011, #1012,
#1013). **An empty list is not evidence of non-membership.** Root-cause class is
not a surface-word property, which is precisely why the family slips past
`ghi-author` Step 0's title skim; a signal built from surface words inherits the
same limit and may not be reported as a family size.

Neither field enters the rank input, which stays structural-only (GHI #424).
The pass informs the judgment in Step 2; the ranking stays the agent's.

### Step 2 — Read each body, compose rank input

For each GHI in the JSON, read the body (it is inline — no `gh issue view`
needed). While reading, rule on the pass described above: decide family
membership from the body's root cause rather than from whether
`family_signal` fired, and discount any cross-reference listed in
`stale_annotations` instead of inheriting it. Ranking several members of one
family adjacently is a legitimate ordering judgment; reporting a family
*count* from the signal is not.

**Rule each issue's readiness: what ends it.** `ready`: the fix is specified or
derivable from the body, so `ghi-close` could land it now. `ruling`: the next
action is an operator decision. `sequence`: it waits on another landing, a fenced
pool ADR or a live OBPI brief. `design`: an open question with no remedy chosen.
Pick the one that gates first. Re-derive every stated blocker against the tree,
as `ghi-close` Phase 1 step 1a does, because a blocker describes the day it was
written. The script's `route` is authority, not readiness: it reads `direct-fix`
for almost every issue.

**Parallel read (optional, for a large queue).** Split the fetched set into
disjoint chunks and dispatch read-only subagents with this rubric and a JSON
output file each. They read and classify; they edit, comment on and close
nothing. Spot-check a sample of their verdicts against the issues before using
them (`.claude/rules/model-selection.md` claim 5). In the first such run, one
verdict in five cited a false fact (`docs/rnd/ghi-batch-closure.md`).

Compose a single rank-input JSON document with one entry per GHI
the agent recommends working on, in the agent's recommended order:

```json
{
  "rankings": [
    {"number": 324, "severity": "blocking", "readiness": "ready"},
    {"number": 323, "severity": "degrading", "readiness": "ruling"}
  ]
}
```

**Rendering-edge contract (binding — structural-only schema, GHI #424
round 3):**

| Field | Constraint |
|-------|------------|
| `number` | int; must appear in the Step 1 fetched set |
| `severity` | one of `blocking` (current work fails), `degrading` (succeeds but produces drift), `latent` (deferrable) |
| `readiness` | optional; one of `ready`, `ruling`, `sequence`, `design`; on every entry or on none (a partial set exits 1) |
| any other field | **rejected** — the script returns exit 1 if a `rankings[*]` entry contains keys other than `number`, `severity` and `readiness` |

The schema is structural-only by design: prose fields in the rank input
duplicated the renderer's output in the operator's chat surface, and only
removing them from the schema made that impossible (GHI #424). The agent's
cognitive contribution is **selection + ordering + severity + readiness**; the renderer owns
all prose, derived from the fetched issue set.

### Step 3 — Render the deliverable

Write the rank-input JSON to a cache file under `.gzkit/cache/triage/`,
then pass that path to the script with `--format rank`:

```bash
# Write tool: .gzkit/cache/triage/rank.json  ← {"rankings":[…]}
uv run python .gzkit/skills/ghi-triage/scripts/triage.py --format rank --rank-input .gzkit/cache/triage/rank.json
```

`--rank-input` rejects stdin (`-`) and any path outside
`.gzkit/cache/triage/` (GHI #424 round 4). Inline-pipe shapes —
`echo '<json>' | triage.py … --rank-input -` — surface the entire rank
payload on the bash command line and reproduce the duplicate-render shape
in chat; the cache-path requirement makes that structurally impossible.

The script renders a deterministic markdown deliverable: one numbered row
per ranked GHI, each row containing the severity, route, and title in a
fixed shape. **The script's stdout IS the deliverable. The Bash tool
result shown to the operator is the presentation — do not echo, restate,
copy, or paraphrase that output in agent-generated text.**

A PreToolUse `Bash` hook (`.claude/hooks/ghi-triage-chat-silence.py`,
GHI #424 round 4) inspects the assistant's most recent turn whenever
`triage.py --format rank` is invoked. If the turn contains two or more
distinct `#NNN` GHI tokens each within 200 characters of a severity word
(`blocking|degrading|latent`), the hook exits 2 and blocks the tool call.
Compose the rank input silently — the hook is the structural backstop on
the chat-text surface, paired with the `--rank-input` cache-path
requirement on the bash-command-line surface.

With readiness, the rows fall into fixed-order groups: the **landing queue**
(`ready`), the **ruling docket** (`ruling`), waiting on sequence, and open design
questions. The agent's order is kept within each group.

There is no Step 4. The rank list IS the recommended order. What follows belongs
to other skills. The single writer draws the landing queue with `ghi-close`, one
issue at a time, never batch-closed. The ruling docket goes to the operator as a
live ruling session: one question per issue, with a recommended answer
(`AGENTS.md` § Operator Economy of Effort). The docket's prose lives in those
questions, never in the rank input.

## Optional cross-check (conditional, NOT mandatory)

If — and only if — a GHI body's `files_mentioned` plausibly overlaps an
in-flight ADR's allowed paths, run targeted state inspection for that
overlap:

```bash
uv run gz state --json
uv run gz obpi lock list
```

Use the result to set severity to `blocking` (overlap creates a hard
ordering dependency) and to order the dependent GHI after the one it waits on —
the rank input carries no prose field to say why. Do **not** run
this cross-check unconditionally — `gz state --json` is a 1.5 MB output
that takes 10–30 s to compute; running it on every triage burns operator
time for no signal. The default state of this step is *skipped*.

## Output Contract

Declared form: **deterministic markdown**, the script's `--format rank`
output, presented verbatim. Chat-renderable; no Rich box-drawing glyphs
that wrap mid-character in chat surfaces; no ANSI color sequences that
get stripped; no per-GHI panel restating the body excerpt the JSON
already contained.

The rank list is the only deliverable. The script also supports
`--format markdown` (chat-renderable candidate-set table for operator
skim) and `--format rich` (terminal-only, opt-in for TTY operators) but
neither is part of the agent's binding output.

## What the script does

Fetch, precedent cache, duplicate detection, blocker mining, routing, urgency
and rank validation are documented in `scripts/triage.py` (`--help` and its
docstrings). One routing rule binds the agent: the script never emits an OBPI
route. Architectural work goes GHI → ADR → OBPI through `gz plan` / `gz-design`,
at the operator's choice, and triage surfaces the hint only.

## Scope

Triage is read-only: it never edits, comments on, labels or closes an issue. Every
prohibition this skill binds is stated once, at its step. The GHI #424 history
behind Steps 2 and 3 is in the issue itself.

## Related

- `AGENTS.md` § Defect-fix routing — the routing the script encodes
- `.gzkit/skills/ghi-author/SKILL.md` — authors the GHIs this skill triages
- `.gzkit/skills/ghi-close/SKILL.md` — closes GHIs after the routed work lands
- `.gzkit/rules/gh-cli.md` — allowed `gh` commands
- GHI #324 (script renders, agent supplies structured judgment) and GHI #424 (chat-silence: cache-path `--rank-input` plus the PreToolUse Bash hook)
