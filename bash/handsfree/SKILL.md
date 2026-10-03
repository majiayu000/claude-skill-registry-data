---
name: handsfree
description: >-
  Keep the current agent moving on an already-authorized task while CI, tests,
  reviews, or other asynchronous work finishes. Arm a native same-conversation
  wake every 10 minutes for at most 3 hours, check live evidence, advance the
  nearest milestone, and cancel the wake when work ends. Use for "handsfree",
  "watch this run and continue", or "keep checking CI without my nudges".
---

# Handsfree

Use the active agent's scheduler to return to **this conversation** every 10
minutes for up to 3 hours. A wake is an action opportunity, not a status-only
notification. Continue useful authorized work now; schedule wakes for periods
when an external result leaves nothing actionable in the current turn.

## Start

1. Infer the active goal from the user's request and the task's canonical plan,
   issue, run, or PR. Name the nearest observable milestone, the exact result
   being awaited, and any relevant commit SHA. If no goal is clear, ask for it
   before arming a schedule. Preserve the task's existing permissions and stop
   gates.
2. Record the start time and a hard deadline no later than 3 hours later. Use
   one unique, non-overwriting `temp/handsfree-YYYY-MM-DD-<session-token>.md`
   file in the current repo (`temp/` is ignored here). Include the goal and
   canonical source, 10-minute cadence, start/deadline with time zone, awaited artifact and SHA,
   current observation, next action, scheduler/job identity and cancellation
   method, and last wake result. Keep this short. It is a local resume note,
   never a replacement for the issue, project plan, CI result, or user message.
   Do not put credentials in it.
3. Inspect the **current harness's** native scheduling tools or UI. Arm exactly
   one recurring 10-minute job only if it can return to this conversation,
   read the note in this workspace, cancel or disable the job from this
   conversation, and show a creation receipt plus an active-job readback.
   Record the job ID and stop method in the note.
   Do not claim a wake is armed until those checks succeed.

   - In ChatGPT/Codex **app** chats, request a scheduled task *inside this chat*
     at a 10-minute interval. A standalone scheduled task starts separate runs;
     it is not equivalent. Do not assume that the app's scheduler exists in
     Codex CLI or the IDE extension.
   - In Claude Code, use a session-scoped `/loop 10m` with the wake instruction
     below; keep the session running. Its cron tools can list and delete the
     job. A closed session cannot be promised a live wake.
   - In Antigravity, inspect `/schedule` or the Schedule UI and verify whether
     the created task returns to this conversation. Project scheduled tasks are
     not proof of that. Antigravity CLI and Gemini CLI require the same live
     capability check; do not infer it from the desktop app.
   - For any other harness, use its native same-conversation scheduler only
     after the same create, readback, and cancel checks.

   If a capability check fails **before creation**, leave the wake unarmed,
   record why, continue what can be done now, and tell the user the limitation.
   If creation was attempted but the receipt or active-job readback fails,
   retain any job ID (or look up the job by this note's unique path), then
   cancel it and verify it is inactive. If its state cannot be proven, report
   that it may still be active and give the manual stop action. Do not create
   a replacement until that state is resolved. A harness with only
   standalone scheduled runs may offer that as a separate option using the
   note, clearly labelled as a new run rather than this conversation waking.
   Do not substitute a shell `sleep`, OS cron, a new headless agent, or an unverified background task
   and call it the current agent waking.

Use this as the scheduled prompt, substituting the note path and the job's own
identity when known:

> Resume the authorized task in `temp/handsfree-...md` in this conversation.
> Check the hard deadline first. Read the original task and its live source of
> truth, including the exact CI/test run and commit SHA. If complete, blocked,
> awaiting user input, stopped by the user, or at the deadline, cancel **this**
> scheduled job and verify it is inactive; report the result. Otherwise take
> the smallest authorized action that advances the next milestone, update the
> note with observed evidence and next action, then return. Never infer a pass
> from a pending, empty, stale, or unrelated result.

## At each wake: observe → act → record → decide

1. Read the note, current user steering, and canonical task state. Check the
   wall clock against the deadline **before** starting another action.
2. Query the specific awaited artifact and verify its identity: run/PR ID,
   target SHA, terminal state, and actual result. Compare with the prior wake.
   An empty response, missing run, or pending state is unknown or pending, not
   success. Do not rerun an expensive gate merely to learn whether an existing
   run has finished.
3. If work can advance, make the smallest authorized move toward the goal:
   inspect a failure, fix its grounded cause, run the relevant existing check,
   address review feedback, or complete the next task step. Follow the repo's
   debugging, isolation, review, and approval rules. Do not expand scope or
   take an irreversible action solely because the timer fired. If nothing is
   actionable, record the unchanged state and wait for the next scheduled wake.
4. Update the note with the wake time, observed artifact/result, action and
   evidence, current milestone, and next move. Give the user a concise update
   only when there is material progress, a blocker, or a terminal result; the
   note carries routine no-change ticks.
5. Stop on verified completion, required user decision/approval, a hard blocker,
   a user stop request, or the deadline. Cancel this job in the same conversation
   and confirm the scheduler reports it inactive or absent. If cancellation or
   its readback fails, report that the job may still be active and give the
   exact manual stop action; never report it as stopped. At the 3-hour limit,
   hand back the current evidence and remaining next step without renewing the
   schedule automatically.

The deadline is the limit even if delayed wakes mean fewer than 18 runs. A
native scheduler may queue a wake while the agent is busy; never overlap a
second work loop or create another job for the same note.

Scheduler references: [ChatGPT/Codex app scheduled tasks](https://learn.chatgpt.com/docs/automations?surface=app),
[Claude Code `/loop`](https://code.claude.com/docs/en/scheduled-tasks), and
[Antigravity `/schedule`](https://codelabs.developers.google.com/getting-started-google-antigravity).
