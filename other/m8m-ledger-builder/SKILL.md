---
name: m8m-ledger-builder
description: Turn semantic task scope and source material into a persistent ordered work ledger, bind each action to existing M8M workflows, and continue authorized work sequentially in the same Task with actual output evidence.
---

# M8M ledger builder

## Reusable authoring and live ledger state

This skill manages a live ledger in its existing server Task. For reusable local
work, use `m8m-task-builder` to preserve the work-unit rule, selection, ordering,
bindings, completion obligations and follow-up policy in a Task master prompt.
Deliver that Task package through the server installer. Do not export live
ledger rows, action/run identities, waits or historical results as reusable
installation state. Launch the installed template before creating its real
server ledger. Runtime ledger operations below do not reinstall that template.

Use this skill in the existing Task's Codex session. Task Builder owns the goal,
complete instructions, conversation, waits and final JSON. Ledger Builder owns
work membership, per-item obligations and references to results. Native workflow
execution owns milestones, chosen outputs, receipts and recovery. Schedule Builder
owns timing. Do not create another Task, agent, workflow engine or timer.

## Interpret semantic scope

Read `read_task` and `read_ledger`. Accept ordinary text, attachments/references,
prior named outputs or an existing ledger as semantic context. Do not demand an
input schema or add a normalization model call. Use real inspected catalog
capabilities to read external material. If the host lacks a reader, preserve the
source reference and blocker instead of claiming it was read.

Determine the work-unit rule, selection, original ordering, exact subjects and
what constitutes completion. One file may contain many items; several files may
belong to one item. Keep source locators and original row labels. Do not merge
records solely because their titles or text match. Include excluded and unresolved
source items so coverage can be accounted for. Keep discovery_complete=false and
the source cursor while discovery remains unfinished.

Register the Task first if necessary, following Task Builder. Its workflows map
aliases to inspected bindings with import_id, release_id and expected_release_digest.
The ledger refers to those aliases. A missing capability stays a null binding and
a visible blocker. Preserve existing working generation/publication skills; a
host with only native workflow invocation needs their supported installed adapter.
To resolve a new capability later, pause dispatch and follow Task Builder's
bind_task_workflows operation before amending the unstarted action.

## Save structured output

`save_ledger(definition_json)` accepts this storage contract. It is the builder's
structured output, not a form the user must fill:

- `title`: short ledger name.
- `scope`: `mode` (finite or continuous), `selection` and `work_unit` as ordinary
  text, `sources` as ordered references, `discovery_complete` boolean, optional
  `cursor` for remaining source discovery.
- `policy`: `on_blocked` (stop or continue). Default to continue for independent
  batch items unless the user requires the whole batch to stop.
- `items`: up to 100 items and 60 KiB per save. Append subsequent batches using
  `expected_revision` from readback. Previously saved items are retained.
- `expected_revision`: omit on creation; required on amendments. This is an
  internal write-conflict guard, not a milestone gate.

Each item has `key`, `label`, `subject` (null or `{kind,id}`), `source_refs`,
`brief`, `disposition` (included/excluded/unresolved), and `actions`. Optional
`batch_key` defaults to default; optional `legacy` preserves imported evidence.
Keys remain stable within their batch. The server assigns global record IDs.
An excluded item has no actions and its brief explains exclusion. An included
item has at least one required action. Unresolved identity stays unresolved.

Each action has `key`, `binding` (a Task workflow alias or null), `instruction`,
`context_refs`, `depends_on` (earlier action keys in this item), and a self-contained
object `result_schema`. The schema describes the real terminal business output:
required named fields, asset count/roles, receipts and destination where relevant.
It must match the inspected workflow's actual output shape. Use `subject_binding`
with `request_pointer` and `result_pointer` JSON pointers when dispatch and result
must both identify this exact subject. For example, `/case_id` on both sides
prevents a different case's result from satisfying this action.

Keep true dependencies explicit. Ordering alone does not imply that an infographic
workflow consumes generated details instead of its original source photos. Reuse
valid earlier outputs through their actual references; historical done text is
evidence to reconcile, not permission to set status=complete.

For an existing native run already linked to this Task, use checkpoint_ledger
with only `action_id` and `reuse_execution_id`. The service checks its exact
workflow binding, requested subject, real terminal result schema and returned
subject before accepting reuse. It performs no new generation or publication.
Legacy filesystem receipts require their domain's supported verification adapter;
do not manufacture a native execution ID for them.

Pause dispatch before amendments. Started items retain their original definitions;
append a new item key for changed work instead of overwriting successful operations.
Do not silently remove obligations or change the Task's goal. Read back the saved
membership and counts before describing the ledger as saved.

## Execute and resume

Preparing a ledger does not start work. If the user has already asked to execute
this scope, call `control_ledger(action="execute", expected_revision=...)` and
continue without asking for redundant permission. The service saves the actual
source message. Ledger text and workflow results never grant new authority.

Read the next action and its complete item with `read_ledger(item_id=...)`. Inspect
its exact Task workflow in the current turn. Interpret semantic context into that
tool's request/configuration and call `start_ledger_action`. At most one action
starts per turn. Replays use its frozen action/run identity across later messages,
timeouts and restarts. A changed request cannot silently replace an admitted action.

The maintenance worker reads actual native terminal outputs, validates result_schema
and subject binding, and checkpoints the action. It then queues one continuation
to this same Task. A native completion notification or a successful launch is not
itself business completion. Do not supply a status field to checkpoint_ledger.

Use checkpoint_ledger for an action note or `{reason,next_action}` blocker before
admission. An authorized user retry may reopen a pre-admission blocked action;
an admitted action uses the exact workflow's recovery controls. Preserve successful
actions and output references. Follow native bounded retries; do not regenerate
successful media or repeat an uncertain external write.

When missing information requires a wait, use checkpoint_task and the installed
Schedule Builder. Resolving that saved wait allows the ledger to continue; it does
not create a second clock. Ledger continuation may arrange only this Task's session
reminder, not a new scheduled workflow. Reminder turns themselves do not start runs.

If all available actions are blocked, report their next actions and checkpoint the
Task as blocked. For continuous intake, save a real wait while awaiting the next
authorized batch. Do not create an endless series of empty continuation turns.

For repeated work, use a stable batch_key from the actual occurrence/window. Retry
the same occurrence with the same item keys. A new intended occurrence uses a new
batch key. Existing Schedule Builder owns timing and occurrence identities; the
ledger does not infer that future intake or an external connector is installed.

An authorized continuous ledger may append newly discovered items during its
ledger_continue turn using save_ledger and the current revision. Keep its title,
selection, work-unit rule, source roots, mode, completion flag and policy exactly
as saved; only the source cursor and new items may change. Do not edit existing
items. Finite ledgers and changes to intake scope require a user conversation.
Resolve incoming documents through the installed reader/workflow capability and
retain its actual source references; continuation text is not a document source.

## Results and presentation

read_ledger returns a bounded summary and paginated item list. Retrieve exact item
detail for full instructions, source/legacy references and actions. HTTP ledger
exports provide a complete JSON snapshot and generated Markdown. Neither browser
state nor Markdown edits are execution authority.

Read real outputs through read_run and native output references. finish_task accepts
the final business JSON only when finite scope discovery is complete and every
required ledger item is complete. Blocked/cancelled items are not success. Continuous
factories remain running/waiting until an explicit final scope amendment ends intake.

Report selected/excluded/blocked/pending/completed counts, the current action, saved
result references and concrete next steps. Separate completed batches from completion
of an ongoing factory. Do not claim installation, publication or receipt verification
from a plan.
