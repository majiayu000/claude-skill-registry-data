---
name: close-the-loop
description: >-
  Find documentation and execution follow-through gaps in the current session's available
  conversation. Trace findings, decisions and technical spikes into issue/PR records and
  next-step execution plans; return numbered possible orphaned tasks with evidence and
  next actions. Use for /close-the-loop, "what did we leave unfinished", or "check this
  conversation for follow-up holes". Report-only, not a general backlog or device scan.
---

# Close the loop

Find unfinished commitments and missing handoffs between what this session learned or decided,
where it was recorded, and what the next execution step needs. A gap can exist even when nobody
explicitly promised the missing update. Return candidates; do not execute them or create records.

## Review

Read the available conversation in order, including any continuation summary. State its scope
and disclose missing/compacted history; never imply access to unavailable turns. Do not fetch
other sessions, prompt logs or device-wide telemetry unless asked.

Trace each relevant finding, decision, spike result and agreed action forward: what changed,
which issue/doc/PR received it, and which next-step consumer still needs it. Check the execution
plan for the relevant task/date, issue or PR, acceptance/verification notes, or handoff record
when the conversation or existing workflow gives it a concrete role. Do not demand updates to
every document for every task. Use only directly relevant links and bounded task/date lookups.

For example, a technical spike for tomorrow may be recorded in the main issue while tomorrow's
execution plan still lacks a pointer to its conclusion. Surface the missing plan update even
without a prior promise to make it. Prefer a pointer to the canonical finding plus a brief
execution implication over copying the spike into multiple documents.

Trace later outcomes before proposing work. Respect corrections, cancellations, superseding
decisions and deliberate deferrals unless their stated revisit condition applies. Brainstorms
and unaccepted assistant suggestions are not agreed tasks. A normal pending PR or clear handoff
is not itself an orphan, but a handoff can still be missing the context needed to act.

Use available read-only tools to check relevant records; bind issue/PR numbers to the correct
repository. A merged PR does not prove its doc or deployment follow-up happened, and an updated
main issue does not prove the downstream execution plan carries the finding. Separate observed
facts from recollection and inference. Failed/unavailable queries mean unverified, not absent
or complete. Do not run tests, start workflows, edit files or post to GitHub for this report.

## Report

Return one numbered list, ordered by explicit user priority, consequences and dependencies.
For each candidate give the concrete gap/action, a short quote or faithful paraphrase anchoring
it in the conversation, the source already updated and downstream target when known, status
(confirmed pending, possible, or unverified), and the smallest next step. Distinguish an inferred
handoff gap from an explicitly requested unfinished task; do not pretend the user promised it.
Deduplicate one underlying follow-up while preserving distinct acceptance criteria. Name an
owner only when evidenced. Keep uncertainty neutral rather than assigning defect severity.

Example shape:
1. **Add the spike pointer to tomorrow's execution plan** — The session records the conclusion
   in issue44; the plan has no reference to it. Target: <plan>. Status: confirmed pending after
   inspecting the plan. Next: propose a short issue link and its effect on the execution steps.

If none qualify, say "No likely orphaned follow-ups found in the available conversation."
Do not manufacture candidates or list the whole backlog. Keep visibility/access limits visible.

Stop after the report. This invocation does not authorize executing candidates, creating issues,
changing PR status, merging or deploying. If the user selects items or requests action alongside
the sweep, honor that scope and existing authorization, recheck current state, and reuse the
existing issues/docs/workflows rather than creating duplicates.
