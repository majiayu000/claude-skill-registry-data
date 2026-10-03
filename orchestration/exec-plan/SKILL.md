---
name: exec-plan
description: Execute or resume an approved kotgent structured plan using coordinated worker sessions, worktrees, independent review and serial merges. Use when the user asks to execute, implement, finish, or resume a kotgent plan.
---

# Execute Plan

Carry the approved plan through implementation, verified findings, integrated checks, and human task
review. Use the `kotgent` CLI for every daemon operation and Git for repository changes. Do not use
direct HTTP, an SDK, or database edits. Honor a narrower user-selected scope; never mark the whole plan
complete when authorized work remains.

## Establish identity and state

Read repository instructions and `kotgent --version` / help. Require `plan` execution commands and
`session done`. Use the live Kotgent pane as caller. Outside a pane, require the exact Kotgent session ID
from the user or invocation context; never infer it from environment variables, provider conversations,
names, cwd, recency, or `kotgent list`. Append `--session ID` to caller-dependent plan/task commands only
in that explicit mode. `start`, `stop`, and `session done` address explicit sessions and have no such flag.

Resolve the linked task using ref-less `kotgent task show` (plus the explicit session flag when needed).
If the user supplied a different task, reconcile that mismatch before execution; do not silently relink.
Keep its explicit reference for all plan commands, and read `kotgent plan show REF`. Require an
`in_progress` backlog task and an `approved` or `executing` plan. A draft or outstanding review goes
through `kotgent:make-plan`; never manufacture approval. A done plan needs a human-review handoff, not
another execution. Inspect task activity, session links, Git status, worktrees and existing branches.
Owned child sessions already assigned in this plan are coordinated work; unrelated overlapping sessions
need coordination under `kotgent:work-task` before edits.

Run `kotgent plan claim REF`. Read `execution.orchestratorSessionId` from its successful response as the
validated parent ID for children. A live different orchestrator is a conflict; do not kill or impersonate
it. A dead owner's plan can be claimed and resumed. The task plan is the source of runtime truth, not
an old transcript or local checklist.

Read [orchestration and recovery](references/orchestration.md) before starting or resuming workers.
Use its state table to reconcile existing sessions, branches and merges before launching anything.

## Execute and review

Keep the plan's selected mode and concurrency unless the user asks to change them. The default mode is
supervised. Use explicit dependencies and the configured concurrency to schedule ready tasks. Establish
an owned feature checkout, start real Kotgent worker children in separate worktrees, and record each
returned session/branch/worktree assignment. Use the [worker prompt](references/worker.md), filled with
the task reference, daemon-issued task ID, parent ID, ownership, current base and verification commands.

Workers implement; the orchestrator coordinates and reviews. Each finished task receives independent
specialist review and a separate verifier under [the review contract](references/review.md). Persist
findings and verification through the CLI. In supervised reviews, the operator decides and sends the
batch in the browser. In autonomous reviews, the assigned worker decides with a note and fixes or
records the disposition of each finding. Read the task review's stored mode; changing the plan mode
applies to the next review, not the current one. Stop unsuccessful automatic review loops at three
iterations and report the blocker with its evidence.

Use `kotgent plan wait REF --after CURSOR --wait 90 --json` for orchestrator events. Handle every returned
event, reconcile the current document, then advance the cursor. Pending is not completion. A disconnected
wait may return only `{"event":"pending"}`: retain the cursor and retry the same command. Lost cursor
state is recoverable by replaying from 0 and reconciling durable status before acting. Do not restart or
reapply completed work just because an event is replayed. Continue independent ready work while one
supervised batch awaits its operator.

Merge one reviewed worker at a time using the ancestry checks and `--ff-only` sequence in the
orchestration reference. Request worker rebases when needed. Record done before stopping and archiving
the child; remove only an owned, clean worktree whose commits are reachable from the feature branch.
Never force-remove a dirty worktree or delete unmerged work.

## Finish the integrated plan

Drain ordinary tasks, then run the final phase in the orchestration reference: full relevant checks,
specialist review of the integrated diff, an independent Codex opinion via `heapy:call-codex`, a
critical-only pass, and fixes in a child session. Rebase on the repository's main/default branch and
repeat affected checks and critical review on the resulting commits. Track this phase as a real plan
task; an otherwise green collection of worker branches does not prove the combined result.

After every task, including final verification/fixes, is done, inspect the integrated diff and call
`kotgent plan complete REF`. Move durable decisions to authoritative repository documentation. Put
accepted deferred work in focused backlog tasks with `kotgent:create-tasks`, carrying finding evidence
and provenance, instead of silently dropping it. Preserve old Markdown plans.

Follow `kotgent:work-task`'s final review handoff using the original linked task and caller: report
behavior, commits, checks, meaningful change statistics, finding decisions (including deferred/rejected
ones), and any manual checks not run; then `kotgent task review -m -` with that report on stdin. Confirm
the returned state is `review`. Do not run task done/unlink, merge into main, push, publish or release
unless those actions are separately within the user's instruction.
