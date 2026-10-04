---
name: m8m-task-builder
description: Author reusable M8M Task packages for server installation, or persist and manage the current live M8M Task's instructions, progress, waits and final JSON.
---

# M8M task builder

## Choose the context

- **Reusable authoring or delivery:** When creating or changing a Task for
  installation on a server, author its reusable source locally and use the
  dedicated server installer. Follow Local authoring below and read
  [server delivery](references/server-delivery.md) when exporting or delivering.
- **Current live Task:** When working in an existing M8M chat and saving its
  goal, progress, wait or result, follow Server runtime below. Its room-scoped
  `m8m_workspace` operations manage this live Task.

A local authoring request does not become a live Task registration because the
skill is called Task Builder. Available room tools and the user's requested
operation determine the runtime branch. Keep a supplied live Task identity when
continuing its work. Independent reusable authoring can happen outside an M8M
room and does not require `m8m_workspace`.

## Local authoring

Preserve the goal, complete master prompt and a self-contained JSON object
output schema. Retain workflow references, required connections/tools/resources,
external effects and any declared model/reasoning configuration. References may
be semantic names, existing exact pins or explicit installation member references;
the installer resolves them against the destination owner's actual catalog.
Do not replace complete instructions with a synopsis.

Use the bundled `<loaded skill directory>/scripts/m8m_local_bundle.py task` to
export a reusable template. Its `--help` describes goal/master-prompt/schema
files, workflow references, resource requirements and runtime configuration.
The helper preserves parsed source schemas; the server validates its prepared
output. Attach referenced implementation, assets and resource context separately
or collect them with `bundle`. A template JSON is not automatic dependency closure.

Exclude live room/thread IDs, waits, progress, ledger rows and prior outputs.
Reusable ledger behavior belongs in the master prompt: work-unit rule, ordering,
selection and completion obligations. A real ledger is created later in its
launched server Task using the installed Ledger Builder.

Deliver new and changed reusable definitions through `m8m-server-installer`.
The installer installs an immutable Task template. An authenticated launch
creates a fresh live Task through normal admission; exporting or installing a
template does not start that Task or authorize additional external actions.

## Server runtime

Apply this section only in the current live M8M Task room. The host injects
these instructions without requiring filesystem access; local export/transport
instructions above do not grant filesystem or installer tools to this room.

One chat is one task in the existing Codex session. Understand ordinary user
messages directly; do not classify messages through another agent or require
an input schema. Answer related questions and incorporate relevant information.
For independent new work, explain briefly that it belongs in another chat and
keep the original task's progress.

Use only the available `m8m_workspace` tools. Read `read_task` first. If no task
is registered, save the user's goal through `register_task` with a complete
`master_prompt`, `workflows` bindings from the actual inspected catalog (or `{}`
for a simple task), and a self-contained JSON object `output_schema`. Bindings
contain `import_id`, `release_id`, `expected_release_digest`; the server records
the source message. Registration stores instructions; it does not authorize
additional external actions. Do not register a separate task within this room.

When the same goal needs a newly available workflow, inspect it and use
`bind_task_workflows` with `{workflows:{alias:binding}}` from the current user
conversation. Pause ledger dispatch first. Existing aliases and releases stay
fixed; this adds bindings without replacing the goal or full master prompt.

Use `checkpoint_task` only when useful progress or a wait must survive the turn.
For batches, generation queues or repeated work use the installed
`m8m-ledger-builder`. Keep the same Task and its overall goal. The ledger owns
item membership and action/result references; do not duplicate its rows or set
its completion in Task context. The server maintains context.ledger.
`current_step` is ordinary text and `context` is a small JSON patch with useful
facts or references. A new `waiting` object contains `reason`, `match` (string
values), `on_wake` and `remaining_checks` (a finite positive count). The server
returns its `wait_id`; never manufacture or replace server-owned IDs. Resolve
a wait with `waiting: null`. To stop progress, set `status` to `blocked` or
`cancelled` as appropriate. Do not mark cancelled without the user's request.

For future follow-up use the installed **m8m-schedule-builder** skill and the
existing schedule tools. A saved wait alone does not create a timer. After
waking, read current state and actual results before deciding what is still
missing. Keep the same wait and edit its saved reminder for a further check;
the server decrements its remaining check allowance when a reminder is queued.

Read actual workflow results before `finish_task`. Save only the final business
JSON matching the output schema; asset values must be uploaded server URLs.
Never use intentions, local filenames, or a notification's text as proof of a
completed external operation. Workflow execution remains in the existing tools.

Session-reminder turns expose progress and reminder tools only. Resolving a wait
allows an already-authorized active ledger to continue in a separate server
ledger_continue turn in the same session. Each such turn may start one saved
ledger action. The native runtime still owns execution and recovery; ordinary
run_result summaries remain read-only. External email ingress requires its own
installed connector. Never claim that saving a ledger installed that capability.
