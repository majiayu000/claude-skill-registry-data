---
name: distill-knowledge
description: Curate durable residue from a completed task packet into canonical tracked `AGENTS.md` files or choose an explicit no-op.
---

# distill-knowledge

This is the only workflow phase that may make semantic updates to tracked `AGENTS.md`.

`review-agents-tree` may auto-apply only trivial non-semantic hygiene fixes.

It must never write `AGENTS.override.md`.

This skill must run from a fresh context window. If the current context contains implementation/review backstory beyond what a fresh distiller should rely on, stop and restart before curating durable context.

Run it after implementation and both code-review phases are clean enough to freeze the task outcome.

## Read first

- `../references/task-packet-contract.md`
- `../references/persistent-artifacts-contract.md`
- `../references/review-phases-contract.md`
- `../references/final-state-authoring-policy.md`
- `../references/initiative-workflow-contract.md` when distilling an initiative outcome
- `../../references/communication-mode.md`
- relevant tracked `AGENTS.md` chain
- current task packet
- final relevant code and tests for any candidate under consideration
- final diff

If `AGENTS.override.md` exists locally, do not rely on it for canonical repository semantics.

## Distill workflow

1. Read the packet and final code/tests for durable residue only.
   - Focus on `PLAN.md`, review files, `AMENDMENTS.md`, `ARTIFACT_CANDIDATES.md`, the final relevant code/tests, and the final diff.
   - Verify candidates against the current code/tests, not just the diff hunks.
   - Ignore implementation chatter that does not survive contact with the final code.
2. Triage candidates.
   - Promote only candidates that are:
     - not recoverable reliably from code/tests
     - durable beyond the current task
     - costly to forget
     - not better encoded in code, names, or tests
   - Prefer no-op over weak prose.
3. Choose the right landing zone.
   - Use the nearest stable tracked `AGENTS.md` owner boundary.
   - Prefer the deepest correct tracked shard for one clear owner, but stop at the smallest stable common owner when the residue spans a broader module or several sibling owners.
   - In cross-repo initiative work, durable landing follows residue ownership, not automatically the parent initiative repo.
   - Do not create a new tracked shard without explicit human approval.
4. Choose the right section.
   - Every tracked `AGENTS.md` needs `## Scope`.
   - Keep `## Scope` lean and non-tautological: owner / applies-to / boundary clarification only. Do not merely restate the current directory path or obvious folder ownership.
   - `## Commands & Validation` for durable run/build/test/lint commands, first validation, or `done when` checks.
   - `## Entrypoints` only for root or hub-level start-here navigation that materially reduces search time. Deep leaf shards should usually omit it.
   - Avoid raw file-path links by default; prefer stable owner/module names or task-class wayfinding.
   - `## Constraints` for hard do/don't rules, invariants, or externally imposed constraints.
   - `## Decisions & Gotchas` for non-obvious rationale, tempting rejected paths, revisit triggers, or traps.
5. Handle drift explicitly.
   - If tracked `AGENTS.md` conflicts with code/tests, trust code/tests.
   - Propose update, supersede, or removal instead of preserving stale guidance.
6. Apply the approval rule.
   - Trivial navigation/hygiene updates may be applied directly.
   - Semantic add/supersede/delete requires explicit human approval before writing.
   - Sharding, scope changes, or meaning-changing conflict resolution requires explicit human approval.
7. Prune aggressively.
   - Append-only is forbidden.
   - Remove or supersede stale guidance when code/tests now encode it better.
8. Update `INDEX.md` with a short distill outcome note.
   - If the packet has no further implementation or review work after distill, it may be marked `done`.
9. Commit before reporting back when distill changed the workspace.
   - If you updated tracked `AGENTS.md`, packet artifacts, or other repo files, make a focused git commit before reporting to the lead.
   - Use a Conventional Commit message matching the actual distill change.
   - Include the commit hash and subject in the handoff.
   - If the correct distill result is `no_op`, do not create a dummy commit.

## Selection heuristics

Promote decisions when the future agent needs to know:

- why a strange choice is intentional
- which rejected path should not be resurrected casually
- what hidden external constraint shaped the code
- what revisit trigger would make the decision worth reopening

Promote entrypoints when the future agent would otherwise waste time rediscovering:

- where a recurring class of change starts
- which owner/module defines the behavior
- which first validation command gives fast confidence

Promote commands/validation when the future agent would otherwise guess:

- how to run the area safely
- which command gives the fastest useful signal
- what `done` means for recurring work in this boundary

## Commit-before-report rule

For distill work that changed the workspace:

- commit before reporting back to the requester
- include the commit hash and subject in the handoff
- prefer a focused commit over bundling unrelated residue edits together
- if the result is `no_op`, explicitly say no commit was needed

## Requester-response rule

Always report the distill result back to the requesting side.

- If the lead/orchestrator requested the distill pass, reply back to the lead/orchestrator.
- If a human directly requested the distill pass in this pane, reply back in this pane.
- Local pane output without an explicit reply to the requester does not count as completion.

## Output shape

Default distill outcome should say one of:

- `no_op`
- `updated_tracked_root_agents`
- `updated_tracked_local_agents`
- `proposed_semantic_agents_update_pending_approval`
- `pruned_stale_agents_guidance`

## Do not

- summarize the implementation
- restate behavior already obvious from code/tests
- promote every candidate just because it exists
- use tracked `AGENTS.md` as a worklog or shadow spec
- write `AGENTS.override.md`

## Initiative mode
When initiative mode is active:
- treat `sync-initiative` as the working-memory sync phase, not the durable distill phase
- read the parent initiative packet plus relevant child `ARTIFACT_CANDIDATES.md`
- read `INDEX.md` field `Next durable distill: now | later`
- default to `no_op` mid-initiative unless the field says `now` and the residue is already stable/reusable
- a child packet may live in an owner repo different from the parent initiative repo; durable distill should run in the repo that owns the residue
- cross-repo initiatives may require separate fresh-context distill passes in different owner repos
- at initiative close, run a final pass even if the correct durable result is still `no_op`
- after any non-final pass or explicit no-op, reset `Next durable distill: later`
- only the closeout pass that updates the parent initiative packet should write initiative `Status: completed`

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
