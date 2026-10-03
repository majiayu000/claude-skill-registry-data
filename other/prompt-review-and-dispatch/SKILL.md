---
name: prompt-review-and-dispatch
description: Audit a GPT-5.6 prompt, clarify purpose through native clickable questions, polish it, require explicit approval, then continue the exact approved prompt in the current Codex conversation by default. Use when the user wants a review-before-execution prompt workflow or explicitly asks to send work to another Codex task.
---

# Prompt Review and Dispatch

Orchestrate `$prompt-master-gpt5` and `$grill-with-docs`. Default to
`current-conversation` execution. After approval, continue the exact prompt in
the current task so the discussion and execution remain visible in one
conversation; this mode does not require a foreground message-injection tool.
Use
`background-task` only when the user explicitly asks for another Codex task or
thread. Read
[`references/approval-protocol.md`](references/approval-protocol.md) before the
first user decision; it is the single source for state, approval, and
execution.
Every user decision in every stage follows
[`../grilling/NATIVE-INPUT.md`](../grilling/NATIVE-INPUT.md).

## 1. Intake

Capture the rough prompt and GPT-5.6 target surface. Set
`execution_mode: current-conversation` unless the user explicitly requests
another Codex task or thread.

For `current-conversation`, label the destination as the current conversation;
do not call `list_threads`, `read_thread`, or `wait_threads`, and do not invent a
destination ID.
For `background-task`, resolve the destination with the host's thread-list/read
capabilities and show its title and ID before approval.

Completion criterion: the execution mode and every working-state field required
by the approval protocol exist; background mode additionally requires one
verified destination task.

## 2. Audit

Invoke `$prompt-master-gpt5` in `audit-only` mode. Consume its gate as
authoritative; this orchestrator does not redefine the audit dimensions.

Completion criterion: the audit returns exactly one gate:
`ready-for-polish` or `needs-purpose-clarification`.

## 3. Align

For an incomplete prompt, invoke `$grill-with-docs`. Resolve facts from files
and docs; ask only the highest-impact unresolved decision.

Re-run `audit-only` after each answer. Repeat until the audit is ready and the
user passes the native alignment gate. A complete user-supplied contract may
skip grilling, but still requires that gate.

Completion criterion: the audit is ready and alignment is explicitly selected.

## 4. Polish

Invoke `$prompt-master-gpt5` in `polish` mode with the aligned brief and audit.
Preserve settled decisions.

Completion criterion: one final copyable prompt passes the prompt-master audit.

## 5. Approve and execute

Show the exact prompt and selected execution mode, then execute the approval
protocol. Rejection returns to alignment with the selected reason as new
evidence; a new draft requires a new approval.

After approval in `current-conversation` mode, treat the exact draft as the
next instruction for this same running Codex task and execute it here. Keep
progress in the current conversation; do not call `list_threads`, `read_thread`,
`wait_threads`, `send_message_to_thread`, `create_thread`, `fork_thread`, or
`handoff_thread`. Use the background dispatch section of the approval protocol
only for an explicitly requested
`background-task`. Current-conversation execution is not dispatch and does not
weaken the verified-dispatch gate: background dispatch still requires its
verified send evidence. Inline completion requires verified evidence of the
same-task continuation and the approved prompt's success criteria.

Completion criterion: current-conversation mode has verified inline-continuation
evidence showing `executed_draft_sha256` equals `draft_sha256`, the approved
prompt's success criteria have actual result/artifact/test evidence, and
execution is complete;
or the explicitly requested background dispatch reaches `complete` with
verified send evidence and exact-byte hash equality.
