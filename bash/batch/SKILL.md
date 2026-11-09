---
name: batch
description: Coordinate explicitly authorized unattended work on selected queue items through definition, architecture, implementation, and independent review, with bounded concurrency, repairs, deferral, and resumable records. Use to start or continue a batch.
---

# Batch

Apply the [core](../../README.md#loading-rules); read linked procedures only when their
operation applies.
Read [batch execution](../../references/batch-execution.md), applicable project instructions,
and the selected queue items and their owning records.
Persona: batch coordinator. Own scheduling, reconciliation, integration, the queue, and
shared handoffs. This skill supplies coordination, not a second implementation workflow or
a background execution guarantee.

## Establish the batch

- Resolve an explicit subset or all current active queue items. Exclude Icebox unless the user
  explicitly reactivates selected parked outcomes under the [queue rules](../../references/queue.md).
  On resume, keep parked members ineligible until explicitly reactivated; retain their repair counts
  and defer dependents that need them. Ambiguous selection blocks dispatch; ask to resolve it.
  Freeze membership before execution; discovered work remains outside it. Queue presence,
  Ready state, and selection alone are not implementation authority.
- Record authority, routine decision delegation, TDD/completion references, and existing active
  ownership under the [batch execution exceptions](../../references/batch-execution.md). Reconcile ownership before claiming work;
  reuse settled decisions and verified results only while their inputs still match.
- Create `docs/lusona/batches/<batch-slug>.md` in the consuming project from
  [the batch template](../../templates/batch.md). Derive the slug with
  the bundled helper ([Bash](../../scripts/work-record.sh) or
  [PowerShell](../../scripts/work-record.ps1)), using its `slug` command and the
  [available shell](../../references/work-record.md). Check for
  existence first: reuse only an explicitly selected continuation, otherwise select a distinct
  suffix. Give each entry a stable local ID such as B1, including Ideas without specs.
  Link eventual owning records; membership IDs are neither queue states nor authority.
- Record a requested assignment ceiling of four by default, or five if selected, reduced by
  host capacity. All responsibilities and nested grants share one pool. Reserve parent occupancy when
  the host counts it; a four-agent host permits at most three delegates alongside the parent.
  Parent-executed specialist assignments are permitted only under the core's
  [local fallback conditions](../../README.md#personas-and-subagents) and also consume the assignment pool; waiting agents still occupy host capacity. Record both limits and actual grants. Default to two corrective rounds per item.
- Read [execution and recovery](references/execution.md) before dispatch, production edits,
  or resumption. Only the parent writes coordination facts; requirements and evidence remain
  in their existing owning documents. Use the record helper for independent creation and handle its collision responses.

## Reconcile and dispatch

Screen selected work for shared behavior, interfaces, data ownership, assumptions, dependencies,
write scopes, and mutable check environments. Disjoint files or isolated copies do not establish
independence. Only dispatch when prerequisites, authority, required policy, ownership, and resources
are available. Keep unused capacity when independence is uncertain. Responsibilities are
described in the [workflow guide](../../references/workflow-guide.md#skills).

| Responsibility | Inputs and dispatch condition |
| --- | --- |
| [specify](../specify/SKILL.md) | Ideas or incomplete definitions; concurrent scopes preserve known shared constraints and return possible coupling |
| Definition reconciliation | Parent compares relevant definitions with accepted decisions, resolves routine inconsistencies, and records dependency/compatibility references before dependent decisions or implementation |
| [architect](../architect/SKILL.md) | Settled, reconciled behavior needing consequential technical decisions; one owner for each shared decision, parallel only across compatible scopes |
| Architecture reconciliation | Parent compares outputs and resolves conflicts through decision owners before dependent execution; record why an existing decision suffices when no new ADR is needed |
| [implement](../implement/SKILL.md) | Authorized outcomes or tasks, reconciled dependencies, explicit applicable TDD, independent ownership/resources, and safe workspace; decomposition belongs here; unset TDD prevents implementation, not useful definition/planning |
| [review](../review/SKILL.md) | Fresh independent review of the resulting integration candidate, its actual diff, governing records, and verification evidence |
| [investigate](../investigate/SKILL.md) | Bounded uncertainty with a finite experiment set and stopping condition; preliminary findings may inform unsettled definition but do not accept architecture |

After each result, choose each outcome's next eligible action from current evidence, unmet
criteria, and authority. Revisit any responsibility when needed, without a batch-wide stage
barrier. An unrelated settled item may advance while other definitions continue. New coupling stops affected writers for
reconciliation and reassessment of designs, plans, and evidence before dependent work resumes.
Apply [incremental reporting](references/execution.md#incremental-reporting) as results arrive:
persist each result before further dispatch or waiting, and update its queue row only when its
state, blocker, or next action changed, without waiting for batch closeout.

Apply [delegation](../../references/delegation.md) and
[model routing](../../references/model-routing.md) through the shared pool. Persist dispatch intent before starting and evidence links before
releasing ownership. Serialize queue/handoff writes, integration, index
operations, and mutable check resources.

## Finish or defer

Use the execution reference to charge repairs, isolate unfinished changes, and reconcile surviving
writers. Safe deferral releases scheduling capacity without rewinding the queue's lifecycle state.
Dependent items needing the missing result remain ineligible; continue independent selected work.
If safe separation or ownership cannot be established, stop and preserve the recoverable state.

Apply the [batch completion gates](../../references/batch-execution.md) to final relevant content, including independent review
and any required human acceptance or delivery. The parent performs
[closeout](../../references/closeout.md), verifies preserved links, and updates batch
pointers to history before removing completed queue rows.

Preserve one current batch handoff. Finish with links to completed outcomes, deferred items and
their questions, interrupted/remaining work, and a concrete owner/action/input for every blocker.
Distinguish exhausted selected work from interruption or unsafe continuation. Report actual
concurrency and unavailable host capabilities without claiming execution or independent review
that did not occur.

## Next action

Continue the next eligible authorized assignment. If none remains, name the exact decision,
authority, environment repair, acceptance, or delivery action for each unfinished item and the
batch record to resume. Newly discovered outcomes require a separate authorized selection.
