---
name: mission-command
description: "Run a bounded technical mission with commander's intent, exact authority and artifact binding, one accountable owner, freedom of action inside stated limits, and a falsifiable ADMIT, COMPLETE or HARD_NACK closeout. Use when someone asks for mission command, hands over a stalled or complex engineering or research effort, or needs several workers coordinated without duplicate work or new authority."
---

# Chefli (mission-command)

Turn an ambiguous or stalled objective into one executable mission. Preserve
initiative inside the user's authority while making scope expansion impossible
without a new order.

A mission order records and narrows existing authority; it never creates new
authority. If the user asks only to frame, draft, or issue an order, stop after
the order. Execute the phase only when the user asks to run, do, begin, or
continue the mission and the actions are already authorized.

## Operating principles

- Lead with purpose, key task, and desired end state.
- Bind decisions to current evidence, not stale narrative.
- Give one owner the ball. Park other roles unless a distinct review gate opens.
- State what the owner may decide without asking again.
- Prefer one decisive falsifier or proof artifact over broad activity.
- Close the precise candidate or family tested; never generalize beyond evidence.
- Treat provider use, spend, network actions, submission, pushing, and other
  external-state changes as separate authorities.
- Keep credentials, tokens, private provider output, and other secrets out of
  orders, evidence, command output, and mailbox records.
- Do not use military phrasing to bypass safety, repository policy, or the
  user's literal resource and numeric bounds.

## 1. Orient from authoritative state

Before issuing an order:

1. Read every named handover, policy, and `AGENTS.md` in its required order.
2. Inspect the live repository path, branch or detached commit, worktree status,
   active dispatch, gates, worker inventory, and submission policy when present.
3. Verify drift-prone facts directly. Hash exact artifacts that will govern the
   mission and timestamp the live check.
4. Preserve dirty trees and unrelated work. Do not resurrect stale workers or
   duplicate an active owner.
5. Identify the most recent authoritative milestone and any dependency that the
   local policy considers stale.

Give the user a concise orientation before lengthy work. Distinguish confirmed
facts, inferences, and unresolved conflicts.

## 2. Form commander's intent

Write three compact elements:

- **Purpose:** why this mission has to happen now.
- **Key task:** the single result to produce.
- **End state:** the observable condition that ends the mission.

The key task must have an exact bound: time, numeric range, artifact count,
build count, file scope, or a combination. If no safe bound can be inferred,
stop and request one.

## 3. Bind the mission

Record:

- activity and authorization;
- authoritative repository, commit/tree, route, and artifact hashes;
- allowed owner, supporting roles, compute, tools, and external resources;
- numeric and artifact bounds;
- current gate and submission state;
- allowed actions and explicit prohibitions;
- required evidence and terminal verdict;
- stop, escalation, and stale-dependency triggers.

Use [references/mission-order-template.md](references/mission-order-template.md)
when a durable order or handoff is needed.

Never silently convert a read-only mission into implementation, an
implementation mission into execution, or a local mission into provider or
submission work.

## 4. Assign roles and decision rights

Choose exactly one ball owner for the current phase. Give that owner freedom to
select inspection methods and make reversible in-scope choices. Define which
events require escalation.

Use additional workers only when the user or repository policy authorizes them
and their work is independent. Assign supporting roles to a later, nonduplicate
gate such as provenance review, mutation testing, or receipt verification.
Do not spawn a reviewer merely to reproduce discovery.

## 5. Execute one bounded phase

Work until the phase reaches its evidence condition or a stop trigger fires.

- Start with the cheapest decisive check.
- Keep source, generated artifacts, runtime evidence, and claims traceable.
- Test the first falsifier before expanding effort.
- Report concise progress during tool work.
- Do not broaden the family, range, worker count, or resource class because the
  first approach is difficult.
- If a command or mailbox post fails, correct it transparently without erasing
  history.

For long-running fleet work, obey the repository's cadence for gate refresh,
housekeeping, handoffs, and stale dependencies. Unchanged state is
not evidence of progress.

## 6. Decide from evidence

Use one of these outcomes:

- **ADMIT:** the candidate clears every stated admission gate and earns only the
  explicitly named next phase.
- **COMPLETE:** the requested end state is fully achieved and no required work
  remains.
- **HARD_NACK:** a decisive witness disproves the precise candidate or family
  inside the stated model and bound.
- **BLOCKED:** use only when the platform's blocked threshold is genuinely met;
  name the missing authority, artifact, or external-state change.

Do not report HARD_NACK for timeout, missing evidence, a broken unrelated test,
or an ambiguous lifetime. Do not report ADMIT from projected savings alone when
correctness, provenance, accounting, or replay remains unproven.

There is no fixed elapsed-time limit for research or technical execution.
Elapsed time alone never makes a worker, dependency, or lane stale and never
justifies a terminal verdict. A monitoring cadence may trigger a status
request, evidence checkpoint, owner review, or explicit reassignment, but the
existing owner retains the ball until command revokes or transfers it. Close a
lane only from a predeclared falsifier, an evidence-backed blocker, source
supersession, owner revocation, or the owner's terminal artifact.

Quantify the outcome: affected count, projected or measured deltas, peak
resource use, artifact hash, and exact falsifier. Keep submission state explicit.

## 7. Close and hand off

1. Write a durable evidence artifact when repository policy supports one.
2. Hash it and verify the intended diff or read-only scope.
3. Post one bounded mailbox record through the named wrapper if present.
   Verify the wrapper accepted the intended nonempty payload and inspect only a
   bounded mailbox tail when confirmation is needed.
4. State what did not occur: source edit, build, provider, GPU, network, range,
   benchmark, push, or submission, as applicable.
5. Open a follow-on phase only when the verdict authorizes it. Otherwise stop.

Keep the final response self-contained: verdict first, decisive evidence,
artifact link/hash, gate state, and next authorized action or stop.
