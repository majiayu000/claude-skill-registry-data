---
name: extract-artifact-candidates
description: Mine the current chat/history for forgotten durable-residue candidates and backfill `.plans/<task>/ARTIFACT_CANDIDATES.md` without touching tracked `AGENTS.md`. Use when implementation/debugging ran long, candidate capture was likely missed, or a human wants a manual mid-task history harvest.
---

# extract-artifact-candidates

Manual salvage pass.

Not a workflow gate.
Not a replacement for `distill-knowledge`.

Run this at any point when the conversation may contain non-obvious rationale, hidden constraints, owner-boundary notes, rejected paths, revisit triggers, or start-here breadcrumbs that should be preserved as task-local candidates before they fade.

## Read first
- `../references/task-packet-contract.md`
- `../references/persistent-artifacts-contract.md`
- `../references/initiative-workflow-contract.md` when harvesting from an initiative child packet
- `../../references/communication-mode.md`
- relevant tracked `AGENTS.md` chain
- applicable `AGENTS.override.md` only if local execution constraints matter
- current task packet if one exists: `INDEX.md`, `PLAN.md`, `AMENDMENTS.md`, `ARTIFACT_CANDIDATES.md`

## Scope
This skill owns:
- manual history mining into `ARTIFACT_CANDIDATES.md`
- backfilling candidates earlier phases forgot to record
- compact `INDEX.md` note that a harvest occurred

It does not own:
- writing tracked `AGENTS.md`
- writing `AGENTS.override.md`
- replacing `distill-knowledge`
- changing `PLAN.md`, `AMENDMENTS.md`, or review verdicts
- bootstrapping a brand-new task packet from scratch

## Workflow
1. Establish the target packet.
   - If one current `.plans/<task>/` packet is already in play, use it.
   - If multiple plausible packets exist, stop and ask the human which packet to backfill.
   - If no packet exists, do not invent one silently. Report candidates in chat and recommend packet bootstrap via `plan-task`.
2. Repair candidate-file drift only if a packet exists.
   - If `ARTIFACT_CANDIDATES.md` is missing, create the empty placeholder and note the repair in `INDEX.md`.
3. Read current packet state before mining.
   - Avoid duplicating existing candidates.
   - Use `PLAN.md` and `AMENDMENTS.md` to align terminology, owner boundaries, and already-explicit decisions.
4. Mine current history deliberately.
   - Start with the current visible conversation.
   - Use available history/context-log evidence to surface earlier user decisions, rejected approaches, hidden constraints, review dispositions, and carryover summaries.
   - Ignore tool spam, raw logs, and dead-end debugging unless they reveal a durable trap, a tempting rejected path, or a non-obvious constraint worth preserving.
5. Triage with the candidate bar.
   - Keep only task-local residue that may matter later and is not already obvious from code/tests.
   - Prefer exact facts over softened paraphrase.
   - Good candidate classes:
     - non-obvious rationale
     - hidden constraints
     - owner-boundary clarifications
     - rejected tempting approaches / `do not casually resurrect`
     - revisit triggers
     - start-here navigation / first validation commands
     - repeated slop traps exposed by the chat
   - Reject:
     - implementation summaries
     - transient debugging noise
     - todo/checklist residue
     - behavior prose already obvious from code/tests
6. Write compact candidates.
   - Append or merge into `ARTIFACT_CANDIDATES.md`.
   - Keep each candidate short, concrete, and attributable.
   - Include:
     - `Type:`
     - `Why keep:`
     - `Candidate:`
     - `Source:`
     - optional `Related code:` / `Related packet refs:`
   - If a prior candidate is duplicated or superseded, merge instead of stacking near-identical entries.
7. Note the harvest in `INDEX.md`.
   - Add a short note with what was harvested or `no_new_candidates`.
8. Hand off clearly.
   - Report what was added, what was intentionally skipped, and whether `distill-knowledge` should later revisit any item.

## Candidate bar
Only record a candidate when all are true:
1. not recoverable reliably from code/tests alone
2. durable enough to matter beyond the current moment
3. costly to forget
4. not strong enough yet to become tracked `AGENTS.md` directly

## Edge cases
- If the current packet status is already `done`, prefer a light harvest only when the candidate inbox is clearly incomplete; do not reopen finished implementation work just because the chat was interesting.
- If the chat contradicts code/tests or explicit human decisions in `AMENDMENTS.md`, trust code/tests and amendments; record at most a mismatch note in task artifacts.

## Output shape
Default outcome should say one of:
- `no_new_candidates`
- `backfilled_candidates`
- `packet_missing_candidates_reported_in_chat`
- `packet_repaired_and_candidates_backfilled`

## Do not
- write tracked `AGENTS.md`
- write `AGENTS.override.md`
- summarize the whole implementation
- treat every chat decision as durable
- mine history so aggressively that `ARTIFACT_CANDIDATES.md` becomes a worklog
- use raw chat archaeology to override code/tests or explicit human decisions in `AMENDMENTS.md`

## Initiative mode
When harvesting from an initiative child packet:
- keep the candidate capture child-local first
- make it easy for `sync-initiative` to fold stable working-memory facts into the parent initiative
- make it easy for `distill-knowledge` to decide later whether any candidate is durable enough for tracked memory

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
