---
name: run-postmortem
description: Reconstruct what a finished agent run or overnight branch actually did — plan lineage, commit ownership, working/not-working with receipts, rot seeds — and deliver a verdict. Use the morning after an unattended run, when the user asks "what did the agent actually do?", "did it work?", "audit this branch", or before deciding whether to land, trim, or redo agent-produced work.
disable-model-invocation: true
---

# Run postmortem

A finished agent run reports what it *intended*; this skill establishes what it *did*. Read-only reconstruction, no universes, no replays — the deliverable is a report the user can land/trim/redo from. A completion claim in a session log is not evidence; every claim in the report cites a SHA, a plan path, a session turn, or a command you ran yourself.

Sibling of `catch-up` (which summarizes for re-entry) — run-postmortem *audits*, with receipts.

## Freeze

Pin what you're auditing before reading anything: repo, branch, `HEAD` SHA, dirty state, and a base. Prefer a base the user names, else the earliest relevant plan's commit, else merge-base with trunk. If no base is defensible, stop and say so — a postmortem without a base audits nothing.

Done when the report header names branch, HEAD, base SHA, and dirty state.

## Plan lineage

Inventory every plan the run worked from: exported plan files (`prompt-exports/`, `docs/plans/`, wherever this repo keeps them), the original user request, and superseding revisions. For each: task, gates, **and the alternatives it considered but discarded** — discards are where the run's judgment shows.

When plan exports are missing, degrade explicitly: reconstruct intent from session history and commit messages, and mark the lineage `reconstructed` so the reader knows it's inference.

Done when every discovered plan is classified relevant / superseded / abandoned, or the lineage is marked `reconstructed`.

## Session recovery

RepoPrompt: `agent_manage op=list_sessions` + `get_log` for workers; `history op=search` for older sessions. **Gotcha (from `workflows/README.md`):** `history` indexes tool *summaries* only — a zero-match search reads like absence and lies. Before believing any negative ("the review never ran"), grep the session JSON under `~/Library/Application Support/RepoPrompt CE/Workspaces/*/AgentSessions/`.

Keep summaries, not transcripts — dispatch an `explore` agent for bulk log reduction and hold only its findings.

Done when every relevant session has an ID, its contribution, and a terminal state — or the gap is named in the report.

## Commit ownership

Walk `base..HEAD` plus the dirty snapshot. Map every changed region to a plan item, a justified enabling change, or **unowned**. Note reverts, and work that landed then got disconnected (wired in, later orphaned).

Done when every in-scope commit and dirty path has an owner or is listed unowned.

## Rot

Run `rot-hunt` over the generation: patterns the run planted first and then copied. Its seed table lands in the report verbatim.

## Working / not working — with receipts

The core of the report. For each planned outcome, one row:

- **Claim** — the behavior the run says it delivered
- **Receipt** — what proves it *on this branch*: a command you ran now, a runtime log from the run showing the new code path fired, or `not_run` + one reason (`blocked` / `not_applicable` / `instrumentation_absent`)
- **Status** — `working` / `not_working` / `unverified`

A green test suite alone caps a row at `unverified` — tests prove the code can pass tests; a receipt proves the feature ran. Prefer running the named gates and the feature itself; where you can't, say `not_run` and why rather than promoting the run's own claim.

Done when every planned outcome has a row and no row's receipt is another agent's assertion.

## Verdict and rollup

Close with:

1. **Verdict** — `DONE` / `DONE_WITH_LIMITATIONS` / `PARTIAL` / `NOT_DONE` / `INDETERMINATE`, one sentence of justification
2. The working/not-working table
3. Rot seed table with `remove`/`tolerate` calls
4. Unowned changes and disconnected work
5. **Recommendation** — land as-is, trim first (name the cuts), fix the seeds first (ordered list from `rot-hunt`), or redo with the lessons (name the lessons: what the next run's plan must say differently)

Write the report to `docs/investigations/postmortem-<branch>-<date>.md` when that folder exists, else present inline. Landing, trimming, and redoing all wait for the user.

## When this skill is the wrong fit

- Re-entry summary, no audit needed → `catch-up`
- One recurring pattern, run already understood → `rot-hunt` directly
- Reviewing a human-authored branch → `aa-second-opinion` / `taste-review`
