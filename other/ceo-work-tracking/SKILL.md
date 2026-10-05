---
name: ceo-work-tracking
description: Use when source context contains one or more trackable Tasks needing extraction, evidence, explicit ownership, commitment/date interpretation, Project clustering, follow-up, completion evidence, or closure. Tasks must be derived from source context; never invent tasks or assignees. Use ceo-message-triage when no durable work item is needed and ceo-meeting-work for meeting synthesis before actions are confirmed. Load the relevant task operation Skill before changing tracked work.
metadata:
  managed_by: ceo-agent-service
  version: 2
---

# CEO Work Tracking

Treat extraction, creation, follow-up, replies, completion verification, and
closure as one lifecycle. Preserve identity, intent, evidence, and links across
every state change. Do not use keyword routers, hardcoded business terms,
person names, or static routing branches to make work decisions.

Load `dingtalk-todo` for DingTalk TODO operations, `task-management` for local task records, and `dingtalk-chat` before requesting updates or reporting closure.

## Task-First Lifecycle Decision

1. Extract zero or more distinct Tasks from supplied source context. Every Task
   decision must cite the exact source excerpt/reference. Never originate a
   Task, deliverable, owner, assignment, or date from Agent judgment alone.
2. If the source contains no plausible action or decision, skip it. Retain
   source-backed low-impact work when its source workflow needs a record, but
   do not promote it to CEO attention merely because it was recorded.
3. Classify each source-backed action as candidate or formal. A formal Task
   needs an evidenced explicit commitment, authorized explicit assignment,
   formal external TODO, or concrete meeting action item, and the responsible
   owner/team must be explicitly identified by the source or authoritative
   metadata. If ownership is missing or ambiguous, retain it as a candidate or
   unmatched evidence; do not create a formal assignment with an invented or
   blank owner. An external TODO proves a formal record exists; it does not
   prove its assignee accepted it.
4. Use an assignee only when source text or authoritative metadata names the
   responsible person/team. Preserve owner identity, assignment evidence,
   assigner/creator, and actor provenance. A participant, speaker, host, sender,
   group member, contact lookup, or name match alone proves neither ownership
   nor authority to assign. If the owner is unclear, retain missing evidence;
   never guess.
5. Derive commitment status from evidence, not an Agent-selected status. An
   explicit assignment is `assigned_unaccepted`. `accepted` requires explicit
   acceptance/commitment evidence from the identified owner, uniquely bound to
   that existing Task. A named owner in a meeting action item or external TODO
   remains `assigned_unaccepted` unless that owner's acceptance is separately
   evidenced; the minutes author/meeting host or TODO creator is not the owner
   accepting it. “收到” alone confirms receipt, not acceptance of the
   deliverable or its date. If a reply could refer to multiple Tasks, do not
   select one by semantic rank. Agent-authored or service-created messages and
   TODOs are not evidence of the owner's personal acceptance.
6. Keep date meanings separate and source-backed:
   - `created_at`: when the system recorded the Task;
   - `assigned_at`: when the source shows the assignment occurred;
   - `requested_deadline_at`: an explicit due date requested by the assigner;
   - `external_deadline_at`: a due date recorded in an external system;
   - `committed_deadline_at`: a concrete date the owner explicitly accepted or
     committed to;
   - `estimated_deadline_at`: an estimate, never evidence of owner default;
   - `next_check_at`: the Agent's operational check time, never a due date.
   Preserve source and actor for every source-derived date. A week-level or
   otherwise non-parseable date phrase stays only in the linked original source
   signal; do not create a typed date fact or manufacture a timestamp from it.
   An estimate is attributed to the identified source speaker who made it,
   never to the extracting Agent. `next_check_at` is Agent-authored only when
   the source explicitly supplies a check date.
   Do not turn “尽快”, “应该这周可以”, a guessed date, or a next-check
   schedule into a committed deadline.
   In the Task 6 Task Agent path, record `next_check_at` only when a check date
   is explicit in the source. Do not invent a check cadence or convert a due
   date into a check date; a future scheduling policy needs separate definition.
   Missing dates do not prevent recording a Business Task. A concrete,
   parseable deadline is still required before mirroring a Task as a DingTalk
   TODO.
7. Keep a Task independent of Projects. Match only against the supplied
   canonical Project/anchor registry; propose uncertain anchor matches or
   Project candidates for explicit confirmation. Semantic similarity, a
   cluster, or a Project candidate does not create an official Project or prove
   business relevance.
8. Merge only identical deliverables supported by explicit identity evidence.
   Distinct deliverables with a shared goal may be clustered or linked; they
   retain independent owners, dates, and completion. When identity is uncertain,
   link or keep separate rather than merge.
9. Enter CEO **需关注** only when a confirmed business anchor and a concrete
   material trigger exist: threatened accepted commitment, material change,
   material assignment/commitment dispute, CEO decision or push, required Gate,
   or meaningful risk escalation. Relevance, acceptance, normal progress, and
   date proximity alone are not triggers. FYI must be material and contain a
   new meaningful change; do not repeat static facts.
10. Apply replies, corrections, disputes, owner changes, scope changes, and
    date changes to the existing Task when identity is explicit. Preserve new
    evidence and actor; record corrections/supersession instead of erasing
    history. Stop follow-up based on a disputed or superseded owner/date until
    current state is resolved.
11. A DingTalk TODO is an external mirror/operation for a source-backed Task,
    never a new source of owner acceptance. Before following up, read the
    current Task/TODO and external status using the relevant operation Skills.
    Bind reminders to the existing Task and linked TODO; never create a
    duplicate commitment or independent reminder.
12. Select an audience and schedule only from verified target/source evidence.
    Use an appropriate verified group that includes the intended owner, or a
    verified direct identity for sensitive content. If target evidence is
    missing, ask for it; do not let the service guess or reroute.

## Lifecycle Cases

- `source_context_can_produce_multiple_tasks`: preserve every distinct action
  from one meeting/message, each with its own source excerpt, owner, dates, and
  commitment evidence.
- `agent_does_not_invent_task_or_assignee`: no unsourced work or inferred owner
  is created; ambiguous ownership remains unresolved.
- `external_todo_is_not_owner_acceptance`: external existence proves a formal
  record only; the named owner must explicitly accept before commitment becomes
  accepted.
- `receipt_acknowledgement_is_not_acceptance`: “收到” alone does not accept a
  deliverable or due date.
- `date_types_are_never_interchanged`: created, assigned, requested/external
  DDL, owner-committed DDL, estimates, and next-check time remain distinct.
- `routine_work_is_not_attention`: retain sourced low-impact work where needed
  but keep it out of CEO attention absent a material trigger.
- `attention_requires_trigger`: anchor/relevance alone does not create FYI,
  WATCH, DECISION, or PUSH attention.
- `follow_up_cannot_exist_without_task`: bind follow-ups to an existing Task;
  any DingTalk TODO mirror must also be linked to that Task and have a valid due
  date.
- `participant_or_speaker_is_not_owner_evidence`: do not assign or contact a
  person merely because they participated, spoke, sent, reported, or appeared.
- `due_follow_up_refreshes_live_task_before_send`: require current Task, linked TODO, and
  external-status reads before deciding that a due reminder remains useful.
- `completed_task_suppresses_follow_up`: close or suppress all pending reminders
  when supported completion evidence exists.
- `owner_correction_updates_existing_task`: preserve correction evidence and
  stop the old owner/date follow-up before considering a new one.
- `follow_up_reply_updates_existing_task`: match a reply by explicit reference
  or one unique evidenced Task; do not create a second Task for the same work.
- `stale_follow_up_is_skipped`: when an old draft is presented for
  reevaluation, read its current Task, linked TODO, external status, and replies;
  suppress it only when those facts show the old question is no longer
  appropriate. The service may enqueue reevaluation but cannot decide the
  semantic outcome. If the decision keeps the follow-up open, provide a new
  future work-hours schedule; the revised draft is a new repair revision.
- `sensitive_follow_up_uses_verified_direct_target`: use only the verified
  direct identity selected in the decision; never convert a group target to a
  direct target in service code.

## TODO Completion Discovery

Runtime integration: one Task Agent returns one `TaskAgentDecision` lifecycle
contract for both new Task extraction and existing Task/TODO/follow-up
transitions. The Work Item source type selects the context and service-side
operations; it does not select a different Agent or decision schema.
`todo_completion_evidence_candidate`, `todo_completion_check`, and
`follow_up_completion_check` are lifecycle inputs. A decision may contain
zero or more source-grounded `task_decisions` plus applicable linked TODO or
follow-up changes in the same result. The service applies Task transitions,
local TODO completion, evidence-candidate status, and linked follow-up changes
within the transaction. TODO-close synchronization uses the existing outbox
only when the DingTalk client is configured. The Task Agent cannot create a
TODO through completion fields, target unlinked records, or add replacement
follow-up drafts during repair. Invalid identities or operations fail the
work-summary input and run without committing domain changes. A completion
check records its bounded `search_trace` even when it finds no completion
evidence.

The runtime validates `source_kind` against the Work Item's `search_policy`,
checks source timestamps against its supplied time window, service-stamps
retrieval time and rejects a timestamp that predates the window, enforces the
returned-source and observed-tool-call limits, and associates each
trace locator with a tool-call receipt from the current run. The service derives
the persisted call IDs from those receipts; it does not trust model-authored
receipt IDs. Current receipts do not contain a separately verified copy of the
external source's semantic truth, so a trace match is provenance linkage, not
proof that the source really establishes completion. Candidate-source timestamps
are also matched to the persisted candidate timestamp. `completed_at` is checked
only for timestamp syntax and that it is not in the future; the runtime cannot
prove that it matches the source content. The runtime does not enforce the
Skill's suggested raw-read cap. The Agent prompt requests read-only access to
external TODOs, but the current Codex route has no per-turn MCP write-tool
allowlist, so that request is not an enforced boundary. This remains a release
blocker until runtime-level write prevention is separately implemented and
verified. The runtime also lacks typed search-versus-raw-read receipts, so the
`max_raw_reads` cap remains unmet and is a release blocker until calls can be
classified and counted from trusted runtime metadata.

This describes the code contract, not deployment status: Task 6 must remain
undeployed until its complete Task 6/Task 7 acceptance gate is verified. The
separate Task 7 Task-to-DingTalk-TODO mirror remains out of scope; do not infer
an external TODO identity when no trusted producer supplied one.

When the Work Item source is `todo_completion_check`, the service is asking for
a bounded current-state check, not reporting a completion fact. First restate
the TODO's concrete completion condition from its title, description, owner,
deadline, follow-up question, and project context. Then use the supplied
`search_policy` to search only the allowed sources within the allowed budget.

Search in this order when the corresponding tool or link is available:

1. Structured task status such as DingTalk TODO or Lark Task.
2. The original follow-up conversation and nearby replies after the follow-up
   was sent.
3. DWS messages and DWS/AI minutes in the supplied time window.
4. Lark messages, Lark docs, email, and local files under `CEO_WORKSPACE` only
   when the TODO context indicates those sources may contain the result.
5. `memory_recall` for stable background only; memory is never current
   completion evidence by itself.

Respect these operational limits unless the Work Item explicitly supplies
stricter values: at most 8 read/search tool calls, at most 3 raw source reads,
and at most 3 evidence sources in the final decision. The runtime validates
observed call count and trace-source count, but the raw-read cap remains an
instruction rather than an independently enforced counter. Prefer the window from follow-up sent
time or `search_policy.time_window.prefer_since` to now. For local files, use
only `CEO_WORKSPACE`, prefer files changed after
`search_policy.time_window.changed_files_since`, and cite a narrow locator such
as relative path plus line, paragraph, mtime, or hash. Do not read or copy large
files when a snippet search is enough.

Stop searching as soon as one strong, current completion evidence source is
found. Strong evidence must identify who or what system confirmed completion,
where it was recorded, when it happened, and why it directly satisfies the TODO
completion condition. Phrases like "I'll look", "in progress", "arranged",
"should be OK", or generic "done" language are not enough unless the surrounding
source ties them to the exact deliverable.

For TODO completion checks, use the unified TaskAgentDecision contract and the
`dingtalk-todo` operation Skill to recommend a local TODO close; the Agent is
instructed to only read external TODOs and never write them. The service applies
local completion and queues the configured existing outbox sync. Record
complete `completion_evidence.source`, `reason`, `description`, `completed_at`,
and `checked_at`, with a compact `search_trace` showing which sources were
checked and why the evidence is sufficient. Do not emit legacy `todo_changes`
inside the Task Agent's `task_decisions` envelope: that interface can update a
source-backed Task, but it cannot create, close, or mirror an external TODO. If
no strong completion evidence is found, keep the TODO open and summarize the
check in that independent workflow; do not create duplicate TODOs or follow-ups.

## Memory And Evidence

Memory is optional context, not source evidence or completion proof. It cannot
originate Tasks, assign owners, establish acceptance, or authorize a Project.
Only actual source context and authoritative current records establish those
facts. Record a recall query/result only in the designated context field; do not
write it into a Project patch.

Use current source material and live systems as authority for owner, target, and
completion state. Load a specialist Skill when a tracked item belongs to a
specialized workflow instead of copying that workflow here.

## Service Boundary

The service owns source/evidence persistence, Task transition validation,
evidence-derived commitment state, typed date storage, explicit matching to
existing Tasks, scheduled wake-up, due-time and local-work-hours guards, the
parseable due-date gate for a DingTalk TODO mirror, live external-status refresh,
completion-check enqueueing, exact-message idempotency, and sent-result or
retry state. The Agent may extract and propose interpretations only from
supplied source context; the service rejects unsupported owners, acceptance,
dates, transitions, identity merges, or attention triggers. The Agent/service
must not create an unsourced Task or treat their own output as a human
commitment. Preserve exact-message idempotency. A corrected or materially
changed message is a new revision and is not blocked merely because an older
message was stored or sent.
