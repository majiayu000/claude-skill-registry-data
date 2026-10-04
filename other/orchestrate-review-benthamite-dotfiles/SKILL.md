---
name: orchestrate-review
description: Use when coordinating two live Emacs agent sessions for a staged implementation that needs independent artifact review, fixed author/reviewer roles, unattended completion, or role reversal. Not for auditing this skill or merely explaining orchestration.
---

# orchestrate-review

## Overview

Run one complete Superpowers-style stage across two live `agent.el` sessions.
Agent 1 owns every authoring and implementation phase; Agent 2 independently
reviews the specification and plan once each. The helper enforces phase order,
fixed roles, one initial whole-stage implementation handoff, and targeted
whole-stage steering only after a genuine incomplete return.

Reading or auditing this skill does not authorize live orchestration. Start or
contact sessions only when the user requested that workflow. Persistence never
expands the user's scope or overrides higher-priority instructions or guards.

## Role contract

- **Agent 1 creates the spec.**
- **Agent 2 reviews the spec once.**
- **Agent 1 creates the plan, incorporating the spec-review feedback.**
- **Agent 2 reviews the plan once.**
- **Agent 1 implements the plan, incorporating the plan-review feedback.**
- Treat both reviews as one-way handoffs. Do not send the artifact back for
  another review pass. Agent 1 adjudicates the feedback and proceeds to the
  next stage.
- Agent 1 defaults to Claude/Fable and Agent 2 defaults to Codex.
- A user-requested reversal swaps the entire role bundle: the new Agent 1 owns
  spec creation, plan creation, and implementation; the new Agent 2 owns both
  independent reviews. Never reverse only one stage.
- Plan tasks belong exclusively to Agent 1's internal execution. They are not
  orchestration phases, progress units, handoff points, or acceptance gates.
- In a multi-stage engineering project, delegate top-level stages sequentially,
  one stage per fresh Agent 1 session. Do not reuse that implementation session
  for the next stage. Internal plan tasks stay inside their stage's single
  session and never receive separate orchestration delegations. `init-run`
  rejects prior user or actor history for a new, non-adopted stage. A matching
  Codex startup header is allowed; unknown records are not assumed harmless.
  Sequencing the stage runs remains the orchestrator's responsibility.

## Stage atomicity

The entire stage is the smallest orchestration unit. After the plan review,
send one initial implementation handoff to Agent 1 and wait for the complete
stage. Agent 1 owns implementation and stage-final verification.
Agent 1 must never end its turn to wait: the injected implementation
contract tells it that an unfinished background job, subagent, or reviewer is
not a reason to return, and that it must wait inside the turn with bounded
waiting through the host's supported wait or recurring-monitor mechanism,
within its documented limits. Resume yielded operations through their existing
handles; do not launch duplicate work. An ended turn is a stop, not evidence
that the background operation failed or finished.

- Never report progress as `Task N`; report only the stage and current phase.
- Never inspect or steer Agent 1's internal tasks, subagents, task transcripts,
  task commits, or per-task processes.
- Never send task-specific corrections, liveness checks, generic continuation
  prompts, or independent verification instructions.
- Never run independent acceptance gates at internal task boundaries. Agent 1
  owns implementation checks until the complete stage returns.
- Never treat a task commit or batch boundary as permission to prompt Agent 1.
- Send exactly one initial implementation handoff. While Agent 1 is active,
  never send a continuation, reminder, marker-repair, model-switch, or recovery
  prompt.
- Intermediate narration and tool activity are not returns. Only an
  authoritative transition to awaiting input permits return handling.
- When Agent 1 genuinely returns early, read the bounded final return, diagnose
  the specific reason for the stop, and send one targeted steering message that
  directs Agent 1 back to the whole-stage outcome.
- Never send a generic continuation prompt. Never repeat a steering message.
  A targeted message names the actual obstacle and resolves it using authority
  and evidence already available from the stage.
- Agent 1 owns implementation and stage-final verification. The orchestrator
  does not run acceptance tests, compare outputs, or add an
  implementation-review pass.

## Supervision and stop-loss

Observe the stage through the fixed actor's lifecycle state and the evidence
Agent 1 publishes. Monitoring does not authorize interrupting a busy actor.

- The implementation contract names a progress file (`<run-file>.progress`).
  Agent 1 publishes stage-level progress and obstacles there. `status` and
  `watch` expose its latest line and age; do not use it to supervise internal
  tasks or infer completion without a final return.
- Keep the host's required commentary cadence while waiting. Explain material
  phase changes or stale progress plainly; do not imply that a quiet file
  proves the actor has stopped.
- Treat repeated reported failures or prolonged silence as an anomaly to
  report and track, not permission to send a busy-session steering prompt.
  Recheck the fixed actor's state. Diagnose and steer only after a genuine
  incomplete return. If interruption is necessary, it requires separate
  authority; this helper does not provide an out-of-band interrupt route.
- The helper does not inspect runner processes or login/error screens during
  implementation, automatically alert on a silence threshold, or enforce a
  timed stop-loss. Do not promise those capabilities. It displays evidence;
  the orchestrator owns supervision within the allowed surfaces.
- Plan efficient retries before implementation: reuse valid cached outputs
  when a failed downstream check does not require repeating an expensive
  cycle. Agent 1 owns those decisions during the stage.
- Use only supported waiting mechanisms and actual documented host limits.
  Never route around a denied wait command through a different interpreter.

Internal decomposition is allowed; external task-level orchestration is not.
The absence of another Agent 2 review does not make task-level supervision
acceptable.

Use the helper script for deterministic Emacs/session operations. In the
examples, `SKILL_DIR` means the absolute directory containing this `SKILL.md`;
resolve it explicitly rather than assuming the host defines that variable.

```bash
python3 "$SKILL_DIR/scripts/orchestrate_review.py" --help
```

## Operating rules

- While orchestration is active, do not send a final response unless the workflow reached a terminal state or a real blocker requires user input. Use commentary updates instead.
- Treat review findings as input to Agent 1's next stage, not as a request to
  revise and resubmit the current artifact.
- Require Agent 1 to address valid findings in the next artifact or in the
  implementation. If Agent 1 rejects a finding, it records a concise reason
  while continuing; it does not ask Agent 2 to adjudicate the rejection.
- Perform exactly two inter-model review handoffs: one after the spec and one
  after the plan. Do not add implementation review unless the user explicitly
  requests a separate review phase.
- Use the guarded run file for every submission. Do not call the underlying
  Emacs submit functions directly or create ad-hoc ask/interrupt bypasses.
- Stage atomicity does not override a user stop request or a safety constraint.
  Stop new handoffs at that boundary; do not continue merely to obtain a marker.
  Stopping orchestration does not cancel a busy actor. Report its actual state
  and use only a separately authorized cancellation path.
- Preserve unrelated worktree changes. If the repo is dirty for unrelated reasons, report it and avoid staging or committing those files.
- Never use the interactive `agent-start-new-session` path for unattended runs when an instance-name prompt is possible. Start sessions with explicit instance names.

## Step 1: Establish the run

Identify:

- repo root
- improvement area and spec/plan paths
- Agent 1 backend/session, usually Claude/Fable
- Agent 2 backend/session, usually Codex
- expected first actor
- current workflow checkpoint

If the user did not provide enough information and no reasonable default exists, ask one focused question. Otherwise infer from the current repo and live sessions.

Identify the two top-level buffer names and transcript paths from the visible
Emacs sessions before creating the run. The helper deliberately has no global
buffer-list command: once implementation exists, global enumeration could leak
internal task/subagent names and states. After initialization, every status
probe resolves only the two fixed top-level actors from the run file.

Live Emacs status is transferred through one-shot mode-`0600` temp files while
the evaluated Emacs form returns `nil`, so structured status data does not
travel through the `emacsclient --eval` return channel. The status contract
contains buffer name, state, and directory; identity checks additionally bind
the backend, session ID, and transcript. They do not include buffer text.

Create a private directory outside the repository with `mktemp -d` and use
unique paths inside it for the run, prompts, and evidence. The illustrative
paths below are placeholders, not shared filenames to overwrite. Keep prompt
and evidence files mode `0600`; the helper creates the run exclusively:

```bash
python3 "$SKILL_DIR/scripts/orchestrate_review.py" init-run \
  --run-file /tmp/improvement-5-run.json \
  --repo /path/to/repo \
  --stage 5 \
  --agent1-buffer '*claude:...*' --agent1-backend claude-code \
  --agent1-transcript /path/to/claude.jsonl \
  --agent2-buffer '*codex:...*' --agent2-backend codex \
  --agent2-transcript /path/to/codex.jsonl
```

The file fixes the complete role bundles and permits exactly these phases in
order: `spec`, `spec-review`, `plan`, `plan-review`, `implementation`.
The author and reviewer must be distinct live sessions in the declared repo;
a buffer name alone is not identity proof. Wait for their session identities
to initialize before creating the run.

To adopt a run whose two reviews already occurred, use
`--adopt-implementation`, `--spec-commit`, `--plan-commit`, and
`--reviews-complete`. Adoption starts at the one whole-stage implementation
handoff; it does not import task state. The supplied commit/review flags are
operator attestations, not automatic checks that those reviews actually ran.
Verify the cited artifacts and handoffs before using adoption.

New runs use schema version 3. `run-status` can inspect legacy version-2 files.
Use `migrate-run --run-file <run>` explicitly to bind an unambiguous legacy run
to its original live actors. Migration preserves completed history and an
unambiguous active boundary; it does not fabricate delivery receipts. Legacy
pending submissions, prior steering, and ambiguous delivery stops refuse
migration without changing the file. Migrated phases lacking an original
context digest cannot use `restart-phase`.

## Step 2: Start fresh sessions when needed

When a new session is required, avoid commands that ask for an instance name. Use explicit instance names:

```elisp
(let ((default-directory "/path/to/repo/"))
  (agent-start-session
   (agent-session-create
    :backend 'codex
    :account (agent-account-resolve 'codex t)
    :directory default-directory
    :instance "improvement-5-codex")))
```

For Claude/Fable, use `:backend 'claude-code` and an instance such as `"improvement-5-claude"`.

A newly initialized Claude session can still report `unknown` before its first
lifecycle event. The guarded first submission reconciles it as waiting only
when the Claude process is live, its configured transcript has no history, and
the per-process status file names that exact transcript. Do not manually mark
other unknown sessions as waiting.

## Step 3: Submit guarded phases

Write phase context to a mode-`0600` file in the private run directory and
submit it through the run. Retain those exact bytes until the phase completes:
process-loss recovery needs the original context. Keep ambiguous attempts'
context while recovery remains possible; remove it after successful completion:

```bash
python3 "$SKILL_DIR/scripts/orchestrate_review.py" submit \
  --run-file /tmp/improvement-5-run.json \
  --phase spec \
  --prompt-file /tmp/prompt.txt
```

The helper selects the actor from the phase and rejects out-of-order,
duplicate, wrong-role, busy-actor, and post-implementation arbitrary
submissions. Before delivery it records the fixed transcript byte boundary;
only after the marker-bearing prompt itself appears in the actor's transcript
past that boundary does it record the phase as active; a busy terminal or
transcript growth alone (a session starting up, compacting, or writing
bookkeeping records) is not acknowledgement. If the initial submit call returns without that
acknowledgement, a non-implementation Codex phase may retry only the submit
keystroke when both its receipt token and full prompt hash match the fixed
actor's composer. It uses `codex-prompt-input`, not terminal prompt syntax.
Claude's terminal API cannot prove an exact composer, so guarded Claude
submissions do not retry Return. The helper also disables the Claude backend's
independent delayed Return retries. It never retransmits the prompt. It does not enable the next handoff
merely because the prompt was delivered. Every phase prompt ends with a fixed
completion marker contract, and the implementation prompt also contains a
whole-stage contract subordinate to user scope and higher-priority safety
instructions. Delivery requires the full submitted text's hash and a unique
attempt receipt token in a user record, not the reusable phase-completion marker. Implementation is stricter: only its current user
receipt acknowledges delivery, and neither the initial submission nor a CLI
recovery command retries Return.

After the fixed top-level actor is awaiting input, record the return:

```bash
python3 "$SKILL_DIR/scripts/orchestrate_review.py" finish-phase \
  --run-file /tmp/improvement-5-run.json \
  --phase spec
```

`finish-phase` reads only bytes appended to that fixed actor's configured
top-level transcript after the current submission and requires the exact
completion marker in a terminal assistant return. Tool calls, reasoning,
intermediate commentary, and unrelated user prompts are not completion
proof. It rejects stale or missing evidence and premature or mismatched phases. Every actor, including implementation, must be authoritatively
awaiting input; transcript text never overrides a busy lifecycle state. Only
then does the next handoff become available.

The helper records a pending attempt before every submission, including
restart and steering. An ambiguous failure blocks further handoffs until
reconciliation; read-only status remains available. Use
`reconcile-submission --delivered` only when the exact current receipt exists.
`--not-delivered` requires concrete non-delivery evidence and an awaiting
actor; it cannot override a positive receipt. Absence of a receipt alone is
not proof of non-delivery, particularly after a timed-out Emacs request.

`retry-delivery --run-file <run>` first checks for an existing receipt. It may
send only Return for a non-implementation Codex attempt whose exact composer
and actor still match. It never pastes the prompt again. Initial implementation
and steering do not retry Return. A negatively reconciled initial
implementation freezes the run; an acknowledged attempt can be reconciled
without another contact. A negatively reconciled steering attempt still counts
against its one-attempt-per-return limit. Keep unresolved delivery pending
rather than asserting a negative merely to unblock the workflow.

If a non-implementation actor's process exits after accepting the phase prompt
but before returning any assistant output, start a fresh fixed-role session and
use `restart-phase --run-file <run> --prompt-file <same-context>`. The helper
requires authoritative waiting state and a genuinely fresh session identity.
It checks the original context digest and proves the failed transcript has no
actor output after the guarded boundary, including tool calls or reasoning.
Unreadable, malformed, or truncated evidence cannot prove absence of output.
It records the new attempt before contact and rebinds the role only after that
attempt's exact receipt. An unrelated transcript containing a static phase
marker cannot be adopted. This is zero-output process-loss recovery, not
another review pass; ambiguous restart delivery uses the same pending-attempt
reconciliation and must not be resubmitted. Fresh app-server sessions are treated
as waiting from the backend's authoritative inactive-turn state even when the
cached event state is still `unknown`.

## Step 4: Monitor without ending the turn

Use the host's supported monitoring or wait facility to supervise the watcher.
Keep waits bounded so commentary and new user input remain responsive. Do not
use broad process-kill commands to manage waiters.

For a one-shot status check:

```bash
python3 "$SKILL_DIR/scripts/orchestrate_review.py" status \
  --run-file /tmp/improvement-5-run.json
```

This prints a short human-readable status from repo, live buffer state, and
transcript evidence. Add `--json` only when another program will consume the
output.

For a polling loop:

```bash
python3 "$SKILL_DIR/scripts/orchestrate_review.py" watch \
  --run-file /tmp/improvement-5-run.json \
  --interval 20
```

This prints when its rendered status changes, including progress age. Silence
alone does not prove unchanged state or a healthy watcher: retain the process
handle and check its exit/error result. All repository, buffer, and transcript sources come from
the guarded run; callers cannot substitute a task buffer or transcript. Do not
use a reviewer verdict as a permission gate: a returned review with its fixed
completion marker advances the workflow.
If a read-only poll loses the Emacs server connection, the watcher reports the
error and retries once after the normal interval. A second consecutive failure
exits. Prompt content is never retransmitted automatically.

During specification and planning, use the bounded transcript evidence needed
to pass artifacts between agents. During implementation, the helper disables
transcript and repository monitoring and exposes the run's stage/phase,
Agent 1's fixed top-level session state, and the latest progress-file line
with its age (the supervision channel). Return-handling commands inspect only
the fixed actor's bounded terminal return after it is awaiting input;
`finish-phase` validates its marker and prints only the completed implementation
return. Do not bypass it to read internal task/subagent output or inspect
per-task repository/process state.

If Agent 1 is awaiting input and `finish-phase --phase implementation` rejects
the return because its final marker is missing, run `stage-return --run-file
<run>`. The command prints only the latest bounded assistant return and records
its digest. It is unavailable while Agent 1 is busy and refuses a completed
marker.

Classify the stated reason. Report a blocker if progress requires credentials
or identity only the user holds, new authority for an external or consequential
action, or a product decision the approved scope cannot determine. An action
already expressly authorized is not a blocker merely because it is consequential. Otherwise write a specific
diagnosis to a mode-`0600` prompt file and steer the same fixed Agent 1:

```bash
python3 "$SKILL_DIR/scripts/orchestrate_review.py" steer-stage \
  --run-file /tmp/improvement-5-run.json \
  --prompt-file /tmp/improvement-5-steering.txt
```

The diagnosis states why Agent 1 stopped, supplies the missing evidence or
authority already available, and returns ownership of the complete stage to
Agent 1. Use exactly these three populated lines so the helper can distinguish
specific steering from a generic continuation:

```text
Obstacle: <the concrete reason Agent 1 returned>
Resolution: <the evidence or authority that resolves it>
Whole-stage direction: <how Agent 1 resumes ownership of the complete stage>
```

It never names an internal task sequence. The helper rejects generic,
repeated, busy-session, ambiguous-delivery, and unrecorded-return steering.

Send commentary when the stage phase changes, when the guarded run reaches a
terminal state, and at the host's required update cadence while waiting, using
the progress file without treating it as completion proof. Do not prompt Agent 1
while it is busy; do read its progress file.

## Step 5: Create and review the spec

Have Agent 1 create the spec using the repository's required design workflow.
When Agent 1 returns the complete spec, run `finish-phase --phase spec`.
Commit the spec once, then submit that commit to Agent 2 for one independent
review. When Agent 2 returns, run `finish-phase --phase spec-review` before
submitting the plan phase to Agent 1.

Spec-review prompt shape:

```text
Independently review the spec at <path/commit>. Identify concrete omissions,
contradictions, feasibility risks, and unclear acceptance criteria that should
affect the implementation plan. Return prioritized findings with reasons. This
is the only spec-review pass; Agent 1 will use the findings when creating the
plan, so do not request a revised spec or another review round.
```

## Step 6: Create and review the plan

Submit the spec and Agent 2's complete review to Agent 1. Have Agent 1 create
the implementation plan while adjudicating every finding. Valid feedback must
change the plan; rejected feedback must receive a concise recorded reason.
Proceed directly to the plan rather than revising and resubmitting the spec.

Use the repository's required planning workflow. If it names a skill, verify
that skill is available and read it; do not assume a Superpowers plugin exists.
When no workflow is specified, write an implementation-ready plan covering
scope, dependencies, and acceptance checks. Commit the plan once, then submit it to Agent 2 for
one independent implementation-readiness review. Record each whole-phase
return with `finish-phase --phase plan` and then
`finish-phase --phase plan-review`; never advance merely because the prior
prompt was accepted by Emacs.

Plan-review prompt shape:

```text
Independently review the implementation plan at <path/commit> against the spec.
Identify concrete correctness gaps, missing verification, sequencing problems,
and scope contradictions that Agent 1 should account for during implementation.
Return prioritized findings with reasons. This is the only plan-review pass;
Agent 1 will use the findings while implementing, so do not request a revised
plan or another review round.
```

## Step 7: Implement with the plan review

Submit the plan and Agent 2's complete plan review to Agent 1. Agent 1
implements the plan while adjudicating every finding. Valid feedback must
change the implementation or its verification; rejected feedback must receive
a concise recorded reason. Do not revise and resubmit the plan first.

Use the implementation workflow required by the plan and available in the
current session. Agent 1 implements the whole stage using the
plan's internal task boundaries for its own tests and commits. The orchestrator
does not observe or manage those boundaries. Do not transfer implementation to
Agent 2 merely because Agent 2 performed the reviews.

Wait for Agent 1 to return the complete implementation and its final
verification evidence.
The final top-level response must end with the helper-injected exact stage
completion marker. Once Agent 1 is awaiting input, run:

```bash
python3 "$SKILL_DIR/scripts/orchestrate_review.py" finish-phase \
  --run-file /tmp/improvement-5-run.json \
  --phase implementation
```

This command rejects a premature return without the stage marker and exposes
the validated terminal implementation report. Preserve that report's stated
checks, outcomes, and limitations in a mode-`0600` evidence file, then close
the run. A completion marker alone is not verification evidence:

```bash
python3 "$SKILL_DIR/scripts/orchestrate_review.py" complete-stage \
  --run-file /tmp/improvement-5-run.json \
  --evidence-file /tmp/improvement-5-acceptance.txt
```

`complete-stage` refuses an active implementation and records the supplied
verification-evidence digest before marking the stage complete. It does not
perform verification itself.

A user-requested post-implementation review is separate, not an implicit third
handoff.

## Stop conditions

Stop and report a blocker when:

- a session is awaiting input but the expected prompt cannot be submitted
- overlapping uncommitted changes cannot be isolated while preserving other work
- review feedback exposes a missing user decision that prevents the next stage
- new authority for an external, destructive, or consequential action is needed
- Agent 1 returns with a blocker that genuinely requires credentials or identity
  only the user holds, or a decision the approved scope cannot determine

## Session cleanup

Track which sessions this run created and which existing sessions it adopted.
After completion, close only run-owned sessions confirmed inactive, using the
backend's normal cleanup path. Preserve adopted or user-owned sessions unless
the user explicitly authorized closing them. A frozen run is not proof its
actor stopped; never force-kill a busy session as cleanup or send signals to
active Emacs without explicit confirmation.

Apply the same ownership and inactivity checks to unused priming sessions.
Remove owned temporary prompts and finished watcher processes; retain private
run/evidence files while needed for recovery. Report any sessions deliberately
preserved because ownership, activity, or cleanup authority is unresolved.

## Final report

Report the stage outcome, actor assignments, spec/plan review handoffs, and
implementation commits. Include branch/worktree state, consequential
verification limitations, and cleanup performed or deliberately deferred.
Keep it brief; expand only when the user needs the details.
