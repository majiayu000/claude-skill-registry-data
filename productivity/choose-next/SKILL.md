---
name: choose-next
description: Use when the user wants to pick the next epic to work on from the status dashboard's queue — "/choose-next", "suggest something to do", "pick an epic", "what should I work on next", "give me 3 options". Surveys all speccing/planning epics on the dashboard, computes which are blocked (deps not yet done) vs ready, and proposes three deliberately diverse options (quick win + strategic-unblocker + drift-recovery). On selection, invokes `/project <spec-path>` to start the planning + dispatch pipeline. Note for "what's next?" routing — if the current TaskList has pending/in-progress items, suggest those FIRST and only invoke this skill if the TaskList is empty or fully done.
---

# Orc's Choice

## Overview

A queue accumulates more spec/plan placeholders than any one session can run through. This skill is the "give me three reasonable picks" routine — it reads the dashboard, applies blocking-aware filtering, and proposes a small diverse set rather than a long list. Once picked, it hands off to `/project`.

The name is a tip of the hat to "orchestrator's choice": the pick it hands over is what the next orchestrator run takes. Pronounce however you like.

## When to use

- User invokes `/choose-next` directly
- User says: "suggest something to do", "pick an epic", "give me 3 options", "what's next?", "what should I work on", "find me work", "I'm idle, what should I run", or similar
- User has just shipped an epic and wants the next one teed up
- User has 5 minutes and wants a small win pre-loaded

## When NOT to use

- User asks "what's next?" while there are pending/in-progress items in the current chat's TaskList — suggest THOSE first; this skill is the fallback when the chat queue is empty
- User is mid-conversation about a specific topic and wants to defer — that's `backlog`, not this
- User wants to browse the whole queue — this skill is for picking ONE thing to do, not enumerating everything; survey the disk directly if a full listing is needed
- The survey turns up nothing (inbox-zero) — say so plainly; don't fabricate suggestions from memory

## Procedure

### Step 1: Survey queue state from disk

```python
from agentflow.config import load_environment
from agentflow.epic_survey import survey_epics, ready_set, blocked_status, blocks_count

env = load_environment()
records = survey_epics(env.data_root, env.mtime_cutoff_iso, include_archived=True)
```

**`include_archived=True` is load-bearing, not tidiness.** Without it `survey_epics` deletes
archived records at the end of pass 4, *before* `ready_set` ever sees them — while `_done_slugs`
counts `lifecycle_state in ("done", "archived")`. So an epic whose prerequisite was **archived**
is never READY, permanently, with nothing logged. Worse than merely hidden: `blocked_status`
buckets it **MISSING-DEP**, which reads as *this dependency does not exist* rather than *this
dependency is finished*, pointing the reader at a phantom problem. **And it is free.** `include_archived=True` adds rows and **no measurable time**: the archived specs are walked and parsed either way — the flag only decides whether they survive a list comprehension at the very end. Widening the corpus here is a correctness fix with no cost to trade against it.

`survey_epics()` returns one `EpicRecord` per slug (the disk replacement for the old work-discovery API). Each record carries at minimum: `slug`, `lifecycle_state`, `current_state`, `depends_on`, `priority`, `domain`, `title`, `source_path`, `last_modified`, `progress`, `paused`.

**This call is deliberately PROJECT-WIDE — `project=` is omitted on purpose, not by oversight.** The builder loops pass `project=<name>` so they can only build their own fleet's work; you are a human-facing *selection* aid, and selection needs the full set — the operator asking "what should I work on next" may well pick an epic from another project on this `data_root`. Nothing here dispatches: `/project` is invoked on the chosen spec with a human in the seat, and `dispatchable(..., project=<name>)` is what keeps a foreign-project record out of an autonomous builder's claim.

If the survey returns 0 records, that's inbox-zero — nothing is pending. It is NOT an error: the survey reads local disk, which can't be "down". Report inbox-zero plainly; do NOT fabricate suggestions from memory.

### Step 2: Bucket the epics

Build these sets:
- **In-flight**: `lifecycle_state == "running"` — these are blockers for anything that depends on them (transitively)
- **Terminal**: what `_done_slugs` counts (`done`, `archived` and the rest of `TERMINAL_CURRENT_STATES`) — the only states that satisfy a dep
- **Ended boards**: an orchestrator run that ended without delivering. `abandoned` and `failed` will never land. `done_on_hold` ended with its PR open for a human merge decision: not in flight, not done, and it satisfies nothing until the merge
- **Candidates**: `lifecycle_state in ("speccing", "planning")` — these are what you'll suggest from

Skip any epic with `paused: true`.

### Step 3: Compute blocked status per candidate

For each candidate, classify its dependency posture with `blocked_status(record, records)`. It
evaluates in this order, first match wins (quoted from its docstring):

```
* any dep is forbidden (cross-project)    → ``MISSING-DEP``
* every dep terminal (``_done_slugs``)    → ``READY``
* any dep's board ended undelivered (``abandoned``/``failed``) → ``MISSING-DEP``
* any dep is a running epic               → ``NEAR-READY``
* any dep is a candidate (speccing/planning) → ``CHAINED``
* any dep is unknown (not surveyed)       → ``MISSING-DEP``
* otherwise, e.g. a ``done_on_hold`` dep awaiting a human merge → ``CHAINED``
```

What each bucket tells the operator:
- **READY** — every dep is terminal.
- **NEAR-READY** — a dep is running; it unblocks when that epic finishes.
- **MISSING-DEP** — no dep the survey can resolve, for one of three reasons; name which:
  - a cross-project dep, which is unsatisfiable by construction;
  - an `abandoned` or `failed` parent, which will never land. `warn_stranded_terminal_dependencies` names the stranded edge; the fix is to re-plan the parent or re-point the edge, not to wait;
  - a dep slug that is not surveyed at all, which may be a future epic that does not exist yet.
- **CHAINED** — deeper queue ahead: a dep is itself a candidate (speccing/planning), or a `done_on_hold` parent is awaiting a human merge (it unblocks when that PR merges), or a dep sits at another unfinished state.

The fully-unblocked subset is `ready_set(records)` — use it to prefer READY candidates.

Also call `blocks_count(record, records)` for each candidate — how many other surveyed epics list this candidate as a dep. High count = strategic value (working on it unblocks downstream work).

### Step 4: Pick 3 with deliberate diversity

Don't pick 3 candidates of the same flavor. Aim for variety across these axes:

1. **Quick win** — a candidate that looks small (read the spec body's `**Tier:**` line if present, or estimate from acceptance criteria count). READY status preferred. These ship quickly and clear the queue.

2. **Strategic unblocker** — high `blocks_count` OR a candidate whose `depends_on` is small/READY and which itself blocks 2+ downstream epics. Doing this opens up future work. CHAINED is OK if the candidate itself is unblocked.

3. **Drift recovery** — a candidate whose `last_modified` is oldest among the candidates (most stale). These tend to fall off the radar; surfacing them prevents permanent rot. READY or NEAR-READY only — don't drag up something with deep chained deps.

If the candidate set has fewer than 3 items: present what's there with a note. Don't pad with archived/done epics.

If two of the three "best" candidates are the same item (e.g., a small quick-win that also unblocks a lot): pick that one + two distinct alternatives, don't repeat.

### Step 5: Read each picked candidate's spec to enrich the suggestion

For each of the 3 picks:
- Locate the spec file at `<data_root>/projects/<name>/design/specs/YYYY-MM-DD-<slug>.md` (the record's `project` gives `<name>`; filename usually has a date prefix; if multiple match the slug, take the most recent)
- Read the first ~40 lines (frontmatter + Problem + Goal sections)
- Extract: tier hint, problem one-liner, key context

This gives the user enough to make a real choice without re-reading specs themselves.

### Step 6: Present 3 options via AskUserQuestion

Use AskUserQuestion with one question and 3 options. Each option's `label` is the slug; each `description` is one short line stating: tier, blocking status, and the why-pick-this rationale.

Format example:
- **Label**: `aggregator-peer-federation-resilience`
- **Description**: `small (single-function fix, READY). Quick win — federation timeout fix shippable in ~30 min, unblocks no one but cleans up dashboard noise.`

The 4th "Other" option is auto-included by AskUserQuestion — lets user say "show me different ones" or pick an epic the skill didn't suggest.

### Step 7: On selection, invoke `/project`

After the user picks one of the 3:
- Locate the spec path on disk (the same file you read in Step 5)
- Invoke `/project <spec-path>` via the Skill tool with `skill: project, args: <path>`
- This routes the chosen epic into the brainstorm-or-plan-then-orchestrator pipeline

If the user picks "Other" with a custom slug:
- Look up that slug in the survey records
- If found: read the spec path, invoke `/project <path>`
- If not found: ask the user to clarify (slug typo? new placeholder needed via `backlog` first?)

If the user picks "Other" asking for different filtering (e.g., "show me speccing only" / "show me only blockers" / "give me a bigger one"): re-run Steps 4-6 with the requested filter. Don't iterate forever — if a third re-roll happens, ask the user to just pick one.

## Examples

### Example 1: routine "what's next" with empty TaskList

User: *"What's next?"*

You first check TaskList — empty (or all `completed`). Fall through to this skill.

You survey the disk, find 5 candidates (3 speccing, 2 planning). Pick 3 with diversity:
- `aggregator-peer-federation-resilience` (small, READY, quick win)
- `platform-cutover-pre-flight-blockers` (medium, READY, blocks 1 other epic — strategic)
- `production-bug-fixes-plan` (planning state, last_modified 4 days ago, drift recovery)

Present via AskUserQuestion. User picks the first. You invoke `/project <data_root>/projects/<name>/design/specs/2026-05-10-aggregator-peer-federation-resilience.md`.

### Example 2: blocked-heavy queue

User: *"/choose-next"*

You survey, find 8 candidates but 5 of them depend on `platform-cutover-pre-flight-blockers` which is itself a candidate (not in-flight). Most candidates are CHAINED.

Pick:
- `platform-cutover-pre-flight-blockers` (READY, strategic — unblocks 5 downstream epics)
- `pythonw-silent-death-fix` (small, READY, quick win, unrelated chain)
- `polish-round-post-cutover-verify` (CHAINED via cutover-blockers, small, drift recovery)

Present with rationale visible. User likely picks the first to unblock the queue.

### Example 3: "what's next" with active TaskList

User: *"What's next?"*

You check TaskList — there's a pending task "Restart the app after cutover-blocker fix". Suggest THAT inline, do NOT invoke this skill:

> "You've got a pending task in this session: 'Restart the app after cutover-blocker fix.' Want to do that, or look at the dashboard for something else?"

If user picks the dashboard option, then invoke this skill.

### Example 4: empty candidate pool

User: *"Pick an epic"*

You survey, find 0 candidates (everything is done or running). Surface plainly:

> "Nothing pending — 0 speccing, 0 planning. The 3 in-flight epics are: ... You're either at inbox-zero or behind the orchestrator catching up. Want to pin something new with `/backlog`?"

Don't invent suggestions.

## Constraints

- **Always read live survey data** — never suggest from memory or recent conversation context. Memory is stale; the disk survey is current.
- **Diversity is non-negotiable** — three quick wins is a worse suggestion set than one quick win + one strategic + one drift recovery. The whole value of the skill is the contrast.
- **Honor the "what's next?" routing rule** — check TaskList first when that phrase is used. The user explicitly asked for this routing; respect it.
- **Don't auto-pick** — even if one candidate is obviously best, present 3 and let the user choose. The user's judgment about what they want to do right now beats your scoring.
- **Don't bundle picks** — if the user picks one, hand it off to `/project`. Don't try to set up a chain of multiple `/project` invocations across the picks.
- **Stop at one re-roll if filter is requested** — open-ended "show me different ones" loops are a footgun.
- **Empty means inbox-zero** — the disk survey can't be "down", so zero records unambiguously means nothing is pending; there is no broken-vs-empty ambiguity to resolve. Surface inbox-zero clearly, with no health probe to tell "broken" from "empty".

## Failure modes

| Failure | Action |
|---|---|
| Survey returns 0 records | Inbox-zero — report "nothing pending — pin something or queue planning." (The disk survey can't be "down", so empty unambiguously means inbox-zero; if you suspect a mis-config, confirm `data_root` points at the right tree rather than probing a health endpoint.) |
| All candidates are CHAINED behind one stuck dep | Suggest the dep itself as #1 (strategic unblocker). Note explicitly that the rest of the queue waits on it. |
| Spec file for a slug can't be located on disk | Skip that candidate, pick another. Note in the final summary: "couldn't locate spec for `<slug>` — record exists in the survey but no file matches." |
| User picks "Other" without specifying | Ask once: "different filter, or a specific slug?" Don't loop. |
| User picks an epic whose deps aren't met | `/project` will accept it anyway; the orchestrator's gate #2 will surface the issue. Add a one-line warning when handing off: "note: this epic's dep `<slug>` isn't done yet — orchestrator may flag it." |
