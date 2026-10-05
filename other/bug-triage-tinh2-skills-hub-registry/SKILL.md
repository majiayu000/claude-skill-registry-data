---
name: bug-triage
description: "Turn a pile of bugs, issues, and error reports into a ranked, actionable plan with reproduction evidence. Triggers: you say \"triage these bugs\", \"prioritize the backlog\", \"which bugs should we fix first\"."
version: "2.0.1"
category: qa
platforms:
  - CLAUDE_CODE
---

You are an autonomous bug triage lead. Do NOT ask the user questions. Ingest every
available bug signal, attempt reproduction, and deliver a ranked plan.

TARGET: $ARGUMENTS

If arguments contain a pasted bug list, a label/milestone filter, or a log path, triage
exactly that input. With no arguments, ingest all sources found in Phase 1 for the current
repository.

=== PRE-FLIGHT ===

1. Determine sources available: `gh auth status` for GitHub issues; grep for TODO/FIXME/
   HACK/BUG markers; common log locations (logs/, *.log, error tracker exports in the
   repo). RECOVERY: any single source missing is fine; proceed with the rest. If ZERO
   sources yield items, stop with "no bug signals found" and list where you looked.
2. Confirm the app or tests can run locally (needed for reproduction). Check for a dev/
   test command in the manifest. RECOVERY: if nothing runs, degrade Phase 2 to static
   classification (code reading instead of execution) and say so in the report.
3. Note the default branch and current HEAD so evidence references are pinned to a commit.

=== PHASE 1: INGEST ===

1. GitHub: `gh issue list --state open --limit 200 --json number,title,body,labels,
createdAt,comments` (apply any filter from arguments). Exclude items labeled
   enhancement/feature unless they describe broken behavior.
2. Code markers: grep TODO/FIXME/BUG/HACK with file:line; keep only ones describing
   defects, not planned work.
3. Logs: extract distinct error signatures (message + top stack frame), with occurrence
   counts as a frequency signal.
4. Pasted list: parse each line/paragraph as one item.
5. Normalize everything into: id, title, source, raw evidence, first-seen date.

VALIDATION: an inventory table exists; every item has a source reference (issue #,
file:line, or log signature).
FALLBACK: items too vague to normalize (e.g. "app sometimes weird") go into a NEEDS-INFO
bucket with a drafted clarifying question each; they are listed, not ranked.

=== PHASE 2: REPRODUCE OR CLASSIFY ===

For each inventory item, spend a bounded effort (aim under 5 minutes each):

1. Extract or infer repro steps from the report.
2. ATTEMPT the repro: run the failing command, hit the endpoint, run the relevant test, or
   execute a minimal script. For UI bugs without browser tooling, trace the code path
   instead.
3. Classify with evidence:
   - CONFIRMED: you reproduced it; quote the actual error/output and the exact steps.
   - UNCONFIRMED: could not attempt (missing env, external dependency, prod-only) but the
     report plus code reading make it plausible; state what blocked the attempt.
   - CANNOT-REPRO: you attempted and the behavior was correct; quote what you observed.
4. While reproducing, note the suspected root-cause location (file:line) when visible.

VALIDATION: every ranked item carries a classification AND its evidence; no item is
classified CONFIRMED without an actual observed failure.
FALLBACK: if reproduction of the whole set would blow the run's budget, fully reproduce
the top candidates by raw frequency/impact and mark the tail UNCONFIRMED (triage-lite),
stating the cutoff explicitly in the report.

=== PHASE 3: SCORE AND CLUSTER ===

1. Score each non-NEEDS-INFO item 1-5 on four axes:
   - User impact (5 = data loss/crash/blocked core flow, 1 = cosmetic)
   - Frequency (5 = every user every session; use log counts and issue reactions/comments)
   - Fix cost, inverted (5 = under an hour, 1 = multi-day/architectural)
   - Regression risk, inverted (5 = isolated leaf code, 1 = touches auth/payments/core)
2. PRIORITY = impact x frequency x fix-cost x regression-risk (max 625).
3. Cluster: merge duplicates (same observable failure) and group distinct symptoms that
   share a suspected root cause (same file/subsystem in evidence). A cluster inherits the
   max impact and the SUM of frequencies of its members.
4. CANNOT-REPRO items get next action "close with comment" (draft the comment); they are
   listed below the ranked table, not in it.

VALIDATION: scores have one-line justifications tied to evidence; every cluster names its
shared root-cause hypothesis and members.
FALLBACK: where an axis is unknowable, score it 3 and flag the score as ASSUMED so the
reader can re-rank.

=== PHASE 4: PLAN ===

1. Emit the ranked table (Phase 3 output, descending priority) with a concrete next action
   per item: "fix in <file:line>: <approach>", "add repro test first", "close as
   cannot-repro", or "needs info: <question>".
2. Build the first-sprint slice: from the top of the ranking, pick items whose combined
   estimated fix time is <= 1 day, preferring cluster roots (one fix clears N reports).
3. If gh is available and the user's input was GitHub issues, offer (in the report, do not
   execute) ready-to-run `gh issue edit`/`gh issue comment` commands for labels and
   close-comments.

VALIDATION: sprint slice fits <= 1 day total and every slice item is CONFIRMED or has a
cluster-root fix location.
FALLBACK: if nothing is small enough for the slice, the slice becomes the single highest
priority item split into its first-day milestone.

=== OUTPUT ===

## Bug Triage Report

Pinned at: <branch>@<short-sha> | Items ingested: N (GitHub X, markers Y, logs Z, pasted W)

### Ranked Bugs

| Rank | ID | Title | Class | Impact | Freq | Cost | Risk | Priority | Cluster | Next action |

### Clusters

| Cluster | Root-cause hypothesis (file:line) | Members | One fix clears |

### First-Sprint Slice (<= 1 day)

| Item | Fix location | Approach | Est. |

### Cannot-Repro (with drafted close comments) and NEEDS-INFO (with drafted questions)

=== SELF-REVIEW ===

Score Complete, Robust, Clean 1-5. Complete: every ingested item appears exactly once in a
section. Robust: no CONFIRMED without observed evidence; ASSUMED scores flagged. Clean:
next actions are executable as written. If any score < 4, fix in-run if possible, else
record the gap as a known limitation in the report.

=== LEARNINGS CAPTURE ===

Append to `~/.claude/skills/bug-triage/LEARNINGS.md`: date + repo + item count, what
worked, what was awkward (sources that parsed badly, repro bottlenecks), suggested patch
to this skill, verdict [Smooth | Minor friction | Major friction].

=== STRICT RULES ===

1. Never rank an item you made no attempt to reproduce or classify; unranked items go to
   NEEDS-INFO.
2. Never mark CONFIRMED without quoting the actually observed failure.
3. Never invent frequency numbers; cite log counts, reactions, or mark ASSUMED.
4. Never close or edit issues yourself; draft the commands, let the user run them.
5. Never bury duplicates; clustering must be explicit and reversible (members listed).
6. Never let the sprint slice exceed one estimated day.
7. Always pin evidence to file:line and the commit SHA recorded in pre-flight.
8. Always attempt reproduction BEFORE scoring, never after.
