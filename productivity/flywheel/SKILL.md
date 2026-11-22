---
name: flywheel
description: >-
  Drive real work through XYZ Forge's existing skills with explicit work modes,
  bounded autonomous repair, independent review, landing, and continuation to the
  next eligible item. Use for "flywheel", "run the factory flywheel", "keep real
  work moving", or "drive Jog through completion". Routes to start-task, jog,
  start-marathon, 10days, optional Daily observation, relay-xyz, handsfree, unstuck, merge-cleanup, and explicitly
  requested skills-army-hq deployment; never creates another runner or queue.
---

# /flywheel — adaptive delivery over existing workflows

Use flywheel when the operator wants real repository work to advance through intake,
execution, recovery, review and landing without repeated stop-and-go coordination.
Flywheel selects and resumes existing skills; it does not reimplement their commands,
state, locks, limits or evidence.

The current text of each linked skill owns its workflow. An explicit operator
instruction or a more specific requested skill takes precedence. Flywheel does not
install itself, start a durable scheduler, grant new marathon-firing authority or merge
a PR by itself. An explicitly invoked 10days sweep retains its named firing exception.

## Choose the work and answer the three rubrics

Name the current objective, observed baseline, intended capability and critical-path
blocker. More PRs, repeated component checks and longer runtime are not capability
gains by themselves. Keep this to a short decision in the existing issue or plan, not
a new document per milestone.

### Rubric 1A: Formal Unattended Work

Use for formal unattended execution of real work. Before the window starts, establish
the actual deployment, workload, observation, approval arrangement and stop/recovery
controls. Formal unattended operation may still adapt and repair; it does not mean
freezing a broken configuration.

**Autonomous bounded repairs allowed and recorded; human assistance disclosed; no silent cap, permission, safety, or gate changes.**

### Rubric 1B: Setup and Repair Work

Use while establishing or repairing the connections needed for later formal work.
An unresolved prerequisite may be the subject of the work rather than a reason to
stop. Use real work, observable results and hard time, spending and attention limits.
Follow the same repair and authorization ladder as 1A.

### Rubric 2: Discriminating real-world test

Use needed work with observable success and failure. Confirm prerequisites and
measurement before formal dispatch. Record whether recovery was automatic,
agent-repaired or human-assisted, and which transitions actually ran.

### Rubric 3: Decision value for cost

State what pass or fail changes, why this is the smallest sufficient experiment, the
numeric time/model/attention budgets, ownership and stop conditions. Set limits before
launch and report actual usage afterward. Unknown usage stays unknown and does not
erase a technical result.

Answer all three rubrics before either mode. Formal work requires the deployed
prerequisites to be ready; setup/repair may establish them. Small routine fixes inherit
the milestone's justification.

## Standing authorization ladder

Apply this ladder in order without reopening routine authorization each session:

1. **Recover and continue.** Use an existing supported retry, recovery or alternative
   path within the recorded time, spending and attempt limits. No additional approval
   is needed.
2. **Make the smallest routine repair.** If recovery is insufficient, repair the task,
   code, configuration or environment within the issue's scope and standing
   operator/repository authorization. Use required isolation, record the reason and
   change, run the existing relevant checks and continue. Supervisor/configuration
   repairs are not a special stopping class. If they change the running version, record
   the new version and its verification, then continue.
3. **Keep independent work moving.** If an item remains blocked within its budget,
   preserve its state and advance eligible independent work. Never bypass dependencies
   or locks.
4. **Escalate only the actual boundary.** Ask the operator when the action needs per-PR
   merge approval, increases caps or spending, requires new credentials, accounts,
   destinations or network exposure, is destructive or irreversible, or disables or
   bypasses a gate or safety control. Otherwise a needed routine repair within these
   limits is already authorized; do not manufacture a per-session permission decision.

The policy source for these modes and this ladder is
[#1358](https://github.com/HiQS-Labs/XYZ-forge/issues/1358). General outer-loop policy
remains in [#1328](https://github.com/HiQS-Labs/XYZ-forge/issues/1328). Flywheel applies
this projection to runs that explicitly select it; it does not rewrite unrelated
campaigns' policies.

## Compose the existing owners with one handoff

Keep the objective, exact work/PR identities and heads, dependencies, approved scope,
remaining budgets, evidence and next owner in the existing plan or batch record.
Re-read those facts on resume; a new conversation supplies no new attempt allowance.
Preparation, execution and landing retain their own canonical writers.
Before reporting completion, map every requested outcome and later amendment to observed
evidence or an explicit unresolved disposition in that same plan or batch record. A completed
subtask does not establish integration.

**Prepared intake is a signal for selection.** When upstream preparation (such as
`conveyor`, GH-1401) publishes a capture and Preflight Contract, the selected execution
owner still checks current issue/PR state, contract probes, dependencies, rating and
admission at pickup. A `status:ready-for-pickup` label is neither automatic Jog selection
nor execution approval. Hold missing or stale prerequisites with the preparation owner;
continue independent eligible work without inventing a second intake queue.

**An approved batch needs one landing owner.** After the outer reviewer has checked
each PR's base, exact head, logical scope and current QA/gate evidence, obtain the
required per-PR merge approval. The operator may give those approvals together as an
explicit batch list; neither a ready PR nor a `--prs` pin grants approval. Then use
merge-cleanup's existing dry run to pin exactly that list. Before `--execute`, compare
every full-SHA pin on the printed `Pinned for --execute:` line with its reviewed
and approved full SHA. If any differs, stop
that PR's landing, re-establish eligibility and QA/review approval as applicable,
and obtain a fresh matching pin; neither bare PR numbers nor a newly recorded pin
prove that a moved head was approved. Only execute the verified matching pins, passed inline as
`--prs N@<approved-full-sha>,...`, so execution checks the approved heads directly.
Use that execution to own dependency ordering, landing, reconciliation and the batch record. Do not nudge
through those stages one PR at a time or discover extra approved PRs during execution.
Keep the existing project policy, landing-plan checkpoint and review requirements.
Never silently widen the list or reset repair history.

**Wait on the result that can unlock work.** Prefer a native exact-PR/head check watcher
(for example `watch_pull_request` where the harness provides it) or a delegated task's
completion notification over repeated chat status calls. Record the awaited identity,
next action, hard deadline and subscription/job identity in the existing handoff.
Follow the native tool's continuation and cancellation contract. On wake, verify the
live head and actual terminal result before resuming; pending, missing, failed or stale
results do not prove readiness. Use handsfree's bounded same-conversation timer only
when no suitable event continuation exists and its capability/readback checks pass.
Do not arm duplicate watchers/timers for one wait or substitute a shell polling loop.
When neither mechanism is available, state that continuation is unarmed and leave a
resumable handoff; do not promise a wake. End subscriptions as required when the wait
ends, the deadline expires or the owner hands control back.

**Accounting belongs to the operation's owner.** Before a repair, use that owner's
existing reservation/wrapper and durable record, and retain its outcome and consumed
budget across heads, retries and resumes. Merge-cleanup's per-PR `attempt_record.py`
and relay/Marathon lane attempts have different scopes; a nested counted flag is not
a new allowance. If the required reservation is absent or unreadable, hold the repair
and resolve it through the existing owner rather than edit first and reconstruct later.
Universal push/gate enforcement is proposed in GH-1399; these instructions do not
claim that raw edits are mechanically intercepted today.

Report the driver's actual outcome: stopped/deferred work and landed-but-QA-pending
batches remain open under merge-cleanup's existing recovery protocol. Preserve failures
and partial delivery instead of calling every zero/nonzero exit a completed batch.
Measure useful deliveries, elapsed time, gates/publications, repairs and parent/human
interventions; leave unavailable tokens/spend unknown. A prose change or green component
check does not qualify unattended progression or establish a supervision-cost saving.

## Daily observation and 10days batches

**Daily is an optional observation-only companion.** When installed and configured,
use the `daily` skill's synthesis to surface progress or blockers, then verify relevant
live state before Flywheel acts within existing authorization. Daily owns its local
synthesis logs; it does not dispatch, repair, merge or grant authority. Missing, stale
or unavailable Daily data is not a blocker to eligible work; use the execution owner's
live evidence. This is instruction-level support, not an automatic observer adapter.
Do not install Daily, start schedules or edit deployed copies as part of a run.

**An explicitly requested [10days](../../3-weekly/10days/SKILL.md) sweep keeps one batch
owner.** 10days owns its scan window, issue selection, `HAS-PR` routing, ratings, plan,
preflight and batch execution. Its named auto-fire exception applies only when that skill is
explicitly invoked; selecting Flywheel alone does not invoke it or authorize a sweep.
In default `marathon` mode do not send its issues through Jog, and in any mode do not
silently re-enqueue issues or start a second sweep to resume it. When the operator
explicitly selects `10days` `serial` mode (Step 3.5), handing committed survivors to
`jog` (after Step 4 / `conveyor` prep) or `start-task` under that one batch owner is
permitted with no duplicate enqueueing and no auto-merge. Standalone 10days remains
supported without Flywheel. The start-marathon route still needs its own exact-plan/order
confirmation.

For a Flywheel-coordinated 10days run, a red wave gate stops advancement. Preserve
its halt and evidence; within the recorded limits, repair only the affected work
through its owner, rerun the existing failed/relevant checks and recheck readiness
before continuing the same plan. Ownership, containment, git-safety violations and
unknown causes remain held for resolution; never skip a failed wave. Independent
work may proceed only when the owner's dependencies and locks permit it. No automatic
restart, new execution identity to reset attempts, cap increase or gate bypass.

Handoff in the existing plan/results: objective and mode, scan window and exact plan,
clone/revision, claims/lock state, budgets and attempt/repair history, halt/gate evidence
and next owner. A returning owner reconciles those facts before continuing; a new
conversation is not a fresh allowance. Use start-task/relay for scoped repairs when
needed and step 6 for verified ready PRs, preserving per-PR merge approval.

## One ordered operating flow

1. **Anchor the outcome and existing state.** Read the live issue, canonical plan,
   current queue and latest verified result. Name the nearest observable milestone,
   selected rubric mode, budgets and next owner. Resolve an explicitly requested
   execution owner before choosing preparation: for 10days, continue to step 2 and
   let that owner select issues and prepare its dedicated clone; do not run a generic
   start-task prelude. For an individual task that still needs the start-task lifecycle
   and has no existing execution owner, use
   [start-task](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/1-hourly/start-task/SKILL.md).
   Reuse its resume reconciliation instead of creating duplicate issues, clones,
   branches or ledger rows. If start-task or existing state already supplies a
   verified ready PR, go directly to step 6 for approval and landing; do not send
   that issue back through Jog for another build.
2. **Choose the existing execution engine.** For an explicitly requested 10days sweep,
   keep 10days as batch owner under the compatibility contract above. Otherwise use
   [jog](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/2-daily/jog/SKILL.md)
   for immediate serial work. Use
   [start-marathon](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/2-daily/start-marathon/SKILL.md)
   only for genuinely marathon-shaped work that needs its preparation, lanes and dry-run.
   Marathon preparation never authorizes firing. A single task does not need a new
   marathon, queue or parallel executor.
3. **Ready and dispatch through the selected owner.** For 10days, honor the operator's
   selected mode (Step 3.5): in default `marathon` mode use its preflight, collision
   checks and existing firing exception without substituting Jog dispatch or adding
   start-marathon confirmation; in `remediate` mode stop after Step 4 preparation; in
   explicitly selected `serial` mode route committed survivors through `conveyor` → `jog`
   or `start-task` under the same batch owner without duplicate enqueueing. For a prepared multi-lane
   marathon, retain start-marathon ownership and hand off to `/pre-marathon` only
   after the operator confirms the exact dry-run-approved plan and order. Do not
   route that arc into serial Jog dispatch. For the Jog route, use [Jog’s preparation handoff](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/2-daily/jog/SKILL.md#preparation-handoff-gh-1439) for missing preparation and reuse its one readiness record; do not duplicate its environment/capacity/clone checklist here. Jog owns pickup-time ledger registration,
   admission, the primary writer, preflight, the driver lock and the separate full-clone
   runner. Preserve its explicit builder/reviewer split and existing attempt limits.
   Formal work verifies the selected deployment and observer before dispatch; setup and
   repair work fixes missing connections under the ladder instead of merely reporting
   them. Never improvise relay or Marathon driver invocations outside their skills.
4. **Execute and independently review.** Let the selected engine own build
   attempts, branches, gates, receipts and PR identity. Use
   [relay-xyz](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/1-hourly/relay-xyz/SKILL.md)
   for required independent plan/final review and its locator, containment and receipt
   contract. A green suite alone is not independent review.
5. **Continue or recover without a premature handoff.** Use the result-specific native
   continuation above when available. If external work requires a same-conversation
   timer, use
   [handsfree](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/1-hourly/handsfree/SKILL.md)
   within its native-scheduler and deadline limits; it is not a durable deployed
   scheduler. When narration, repeated planning, tool exits or delegation produce no
   milestone movement, invoke
   [unstuck](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/1-hourly/unstuck/SKILL.md),
   take one goal-moving action and re-drive the primary engine. For Jog state, preserve
   its recovery order: `resume` first, `retry-gate` for an approved build with a failed
   gate, then `retry-build` when the build genuinely needs a fresh bounded attempt.
   Never reset counters by changing sessions or identities.
6. **Land only within approval, then advance.** Hand the exact approved pinned batch
   to one landing owner as above; keep per-PR merge approval. Use
   [merge-cleanup](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/2-daily/merge-cleanup/SKILL.md)
   for the authorized landing, reconciliation, Jog completion and safe retirement.
   Verify the actual merge and clean synchronized primary before calling it landed.
   Record approval waits separately and advance eligible independent work when the
   existing engine supports it. After a landing, select the next eligible item rather
   than waiting for a redundant prompt.
7. **Deploy only when explicitly requested.** After the source skill is ready and
   merged, use
   [skills-army-hq](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/3-weekly/skills-army-hq/SKILL.md)
   for preview, source-to-collection intake, target synchronization and separate app
   discovery checks. Never edit a deployed copy, create an app symlink by hand or point
   an app at a disposable task clone.

## Completion contract

Do not return with an available, authorized next action merely because a tool exited,
a delegate handed back or a review finished. Perform it or arrange the existing
continuation mechanism. Stop the affected work only for a verified outcome, a genuine
authority or safety boundary, an exhausted recorded budget, or no eligible real work.

Report the capability delivered, actual PR/queue state, verification, repairs and human
assistance, remaining gaps and one next recommended action. A prepared plan, open PR,
healthy process or elapsed window is not completion of the work itself.

## Source and maintenance

The canonical source is `skills/2-daily/flywheel/SKILL.md` in XYZ Forge, indexed from
`ARCHITECTURE.md` → Skills Index. Changes land there first. Deployed collections and app
links are managed projections through Skills Army HQ, not editing workspaces.
