---
name: sync-initiative
description: Fold a child loop back into the parent initiative packet, update canonical parent truth, record the sync log, and route the next durable-distill timing decision.
---

# sync-initiative

Use after a child local loop has produced parent-truth that must be reconciled before more initiative work proceeds.
The child packet may live in a different owner repo from the parent initiative packet.

## Read first
- `../references/initiative-packet-contract.md`
- `../references/initiative-workflow-contract.md`
- `../references/persistent-artifacts-contract.md`
- `../references/final-state-authoring-policy.md`
- parent initiative packet in the orchestrating repo
- child packet including `ARTIFACT_CANDIDATES.md` in its declared `Packet Root`
- `../../references/communication-mode.md`

## Responsibilities
1. Enter initiative `Status: sync_needed`.
2. Update the child row in `TASK_GRAPH.md` using only the canonical child statuses:
   - keep it `active` when more child-local work is still required
   - mark it `blocked` when an explicit blocker is now the governing fact
   - mark it `done` when the child outcome has been reconciled into parent truth
3. Recompute untouched rows from `pending` to `ready` when dependencies clear.
4. Fold stable child decisions into `DECISIONS.md`.
5. Fold stable contract changes into `CONTRACTS.md`.
6. Update `UBIQUITOUS_LANGUAGE.md` only when terminology changed.
7. Append an outcome entry to `SYNC_LOG.md`.
8. Update `INDEX.md` `Next durable distill: now | later`.
9. Exit initiative `Status: active`.

## Distill rule
- set `Next durable distill: now` only when stable reusable residue is ready for a durable-memory pass before more child work
- otherwise keep `Next durable distill: later`
- durable-memory routing follows residue ownership, not automatically the parent initiative repo
- after the last child sync, `active` remains the normal resting state until final `distill-knowledge` closes the initiative

## Writing rule
Reconcile parent truth into one canonical state model.
Do not preserve superseded child-status names, durable-distill fields, or ownership rules in initiative artifacts.

## Do not
- write tracked `AGENTS.md` directly here
- treat sync as a second implementation phase
- overwrite stable parent truth with tentative child-local notes
- invent packet-state mutations outside the initiative contract
- copy the child packet into the parent repo just to make sync easier

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
