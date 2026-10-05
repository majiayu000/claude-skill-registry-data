---
name: codex-model-capacity-retry
description: Use when an existing Codex task or session ends with “Selected model is at capacity”, “model at capacity”, “server_overloaded”, HTTP 429, or “too many requests”, especially when the original task must continue without changing its model or reasoning effort.
---

# Codex model-capacity retry

Use this skill for a provider-capacity interruption, or the specific provider transport failure `stream disconnected before completion`, not for a normal task failure. The important invariant is to continue the existing task: do not create a new `codex exec` task, do not choose a replacement model, and do not set reasoning effort.

## Start an independent watcher

A skill loaded inside the failed turn cannot intercept the request that already failed. Start the watcher from an independent terminal process:

```bash
python3 /Users/derek/.agents/skills/codex-model-capacity-retry/scripts/scan_and_retry_sessions.py --watch --daemon
```

`--daemon` detaches the watcher from the terminal, shell, or Codex tool session that started it. This is required when the launching terminal may close; without it, the operating system may reap the watcher with that terminal. It waits five seconds after detecting a capacity error, then retries indefinitely. Stop it only when the user asks or when the original task has completed. There is no fixed attempt limit. The watcher remembers the exact failed completion, so it does not duplicate one failure; a later capacity failure appended to the same task has a new signature and is retried again.

The detached watcher writes its PID to `~/.codex/codex-capacity-retry.pid` and its output to `~/.codex/codex-capacity-retry.log`. The state-file lock prevents a second watcher from duplicating retries.

Before retrying a capacity-failed completion, the watcher sends the normal `continue` prompt to the same task and waits five seconds. An `active` Goal needs no additional action. When the latest `thread_goal_updated.goal.status` is `paused`, the watcher uses Codex's app-server `thread/goal/set` request with the original `threadId` and `status: "active"`; it never sends a `/goal ...` chat prompt, because that would change the Goal objective instead of invoking an action. A task with no Goal, a completed Goal, or a Goal stopped by budget receives only `continue`; the watcher never invents a Goal. The state file records the successful first `continue` per failure signature, so a temporary failure before the Goal step does not repeat `continue` or activate the Goal early.

The watcher is a detached process, not a Codex task, so it may monitor the task that started the heartbeat as well as other tasks. It does not create a new rollout by scanning; it only reacts to a newly completed capacity-failed turn. The state file records each exact failure signature before allowing it to be retried again, and the latest turn boundary prevents the same failure from being retried twice. Use `--exclude-session-id` only when a separate external owner is already responsible for a specific task, not as a default for the watcher itself. The same list can be supplied through `CODEX_RETRY_EXCLUDE_SESSION_IDS`, separated by commas.

## What it scans

It never resumes a `codex exec` session (`source: exec` / `originator: codex_exec`). That session belongs to the program that ran it, which is waiting on the process and owns its retry; resuming it from here races the owner for the thread's writer (`already has an active writer`) and runs a turn nobody reviews. Services such as ceo-agent-service run every turn this way.

The scanner groups rollout files by session and uses the newest turn boundary across the group. It retries only when that newest boundary is a capacity-failed completion or a completion whose direct error states `stream disconnected before completion`; an older retryable failure is ignored while a newer turn is running or has completed. Symptoms are evaluated only from the completion's direct terminal-error fields: `message`, `codex_error_info`, `error.message`, and `error.codex_error_info`. It never evaluates `last_agent_message`, which is normal answer text and can legitimately mention a status code or an amount such as `$429.06`. It must never retry an authentication, permission, validation, tool, or business-logic failure.

If the rollout metadata marks the record as a `source.subagent`, the scanner uses its existing `parent_thread_id` as the retry target. Multi-agent v2 subagent sessions cannot be resumed directly after they are unloaded; continuing the parent task preserves the original task and avoids repeatedly producing the `resume the parent first` error.

For a CLI-owned session it runs:

```text
codex exec resume --json --skip-git-repo-check SESSION_ID "continue"
```

The command keeps the original session ID, allows the detached watcher to run independently of the launching directory, and does not pass `--model`, `--thinking`, `model_reasoning_effort`, or an effort override.

## Active-writer recovery

The latest `task_complete` is necessary but not sufficient to send `continue`: a Desktop task can still have an active writer after that record has been written. The watcher first tries `codex exec resume` so the task can continue directly.

If normal resume returns `thread-store conflict` or `already has an active writer`, the watcher queues that exact `continue` prompt on the exact same thread with `codex queue --thread SESSION_ID --message PROMPT`. Goal activation is a direct app-server state update and is not represented as a chat message. A successful `continue` queue is recorded as the first stage; a successful Goal activation records the failure signature, so the watcher does not repeat either operation every five seconds. If queueing or Goal activation fails transiently, the signature remains retryable and the watcher tries again later. An incidental `401`/`token_revoked` warning does not override this active-writer result; a genuine authentication error with no writer conflict is suppressed as before.

When checking a Desktop task manually, inspect only the newest turn first. A task is eligible only when its newest error is a capacity error; never revive a task just because it is `failed` or `systemError`.

## Boundaries

- Preserve the original task/session/thread ID and the original model settings.
- Retry continuously at five-second intervals until the task produces a non-capacity completion or the watcher is stopped.
- Do not retry semantic evaluation failures, Buildkite test regressions, missing fixtures, provider authentication failures, ordinary tool errors, or generic stream errors other than `stream disconnected before completion`.
- Do not use a new `codex exec` invocation as a substitute for resume.
- The default scan age is six hours; set `CODEX_RETRY_MAX_AGE_SECONDS=0` to scan all session files.
- Use the state file to coordinate multiple watchers; a lock prevents duplicate watchers from retrying the same task.

## Verification

Run the bundled regression test:

```bash
bash /Users/derek/.agents/skills/codex-model-capacity-retry/tests/test_session_scanner.sh
```

The test proves capacity matching, same-session `continue`, direct activation of a paused Goal through the app-server API, no extra action for an active Goal, suppression of Goal commands for sessions without a Goal, no model/effort override, duplicate suppression, repeated retry after a new capacity failure, suppression of normal answer text that merely contains a `429` amount, historical rollout suppression, controller-session exclusion, and active-writer recovery by queueing exactly one same-thread prompt.

It also verifies that `--daemon --once` returns control to the launching process, preserves the launch working directory for `codex exec resume`, and exits cleanly.
