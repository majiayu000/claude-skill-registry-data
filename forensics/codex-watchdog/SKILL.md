---
name: codex-watchdog
description: Monitor long-running Codex tools and diagnose stalled, oversized, or UI-stale tasks. Use for watchdog, 看门狗, stuck Thinking indicators after backend completion, stuck tool calls, tool timeouts, 卡死监控, session health, adaptive no-progress thresholds, bounded cleanup, safe handoff recovery, explicit visible sidebar task creation during recovery, enabling or disabling local monitoring, or work expected to run longer than 30 seconds. Never auto-retry side effects or delete Codex data.
---

# Codex Watchdog

Use `scripts/codex_watchdog.py` as the only state-changing interface. Resolve it from this skill's directory and invoke it by absolute path; do not rely on the current working directory.

## Honor control requests

Treat these requests as executable controls, including in a brand-new conversation:

- On “关闭watchdog” or equivalent, run `python <WD_SCRIPT> disable`, then report the returned state.
- On “启用watchdog” or equivalent, run `python <WD_SCRIPT> enable`, then report the returned state.
- On a watchdog status request, run `python <WD_SCRIPT> status`, then report the result.
- On “卸载/彻底移除 watchdog”, run `disable` and then `uninstall`. Preserve the skill and incident files unless the user separately asks to delete them.

Do not merely acknowledge these requests. `disable` persists across conversations; while disabled, do not arm jobs unless the user enables monitoring again.

## Monitor long work

For each tool or delegated worker expected to exceed 30 seconds:

1. Check `status` once before an immediately launched batch. If enabled, classify each attempt and have the main conversation choose a rolling no-progress threshold from [references/timeout-policy.md](references/timeout-policy.md). Run `arm --kind KIND --turn auto --generation 1 --timeout-seconds CHOSEN-SECONDS --label SHORT-LABEL` for every initial attempt. The script uses `CODEX_THREAD_ID` when available and otherwise keeps an `unknown-thread` diagnostic label; tag UUIDs still isolate jobs. Retain the exact unique tag returned by the script.
2. Keep parallel work isolated: assign one tag to one attempt, and pass that exact tag to every later command.
3. Observe the real worker or output at least every 30 seconds. The main conversation or a dedicated monitoring subagent may record a heartbeat after judging the attempt healthy from current evidence such as advancing scan counters, new stream/log/tool-call records, changing output files, active process work, worker phase changes, or other task-specific progress. A timer tick or an unchanged “thinking” label alone is not proof of progress.
4. Treat expiry of the chosen interval as a mandatory review point, not an automatic stop. Inspect the exact attempt without preempting the main task. If current evidence shows normal progress, run `heartbeat TAG --note EVIDENCE` and continue waiting. Absence-only evidence—including no completed command, unchanged files, no child process, `post_tool_transition_unobserved`, `model_preparing_no_request`, or a quiet model stream—never authorizes interruption. Stop only on explicit user instruction or positive terminal/failure evidence. A task may run much longer than `timeout_seconds` while it continues producing verified progress. Keep the separate 180-second hard limit for a single image-generation attempt when the active repository or user instructions require it.
5. Always run `disarm TAG --reason REASON` immediately on completion, failure, cancellation, or a confirmed abnormal stall. Use a new generation and a new tag for any retry.

Never automatically replay a tool that can spend quota, send messages, mutate files, or otherwise cause side effects unless an active user instruction explicitly pre-authorizes that retry. After a reconnect or interruption, inspect `status`, bounded `list`, bounded `incidents`, and actual outputs before deciding whether anything is genuinely missing. Compatibility `--all` output is still capped and must not be used as a routine context dump.

The external timer cannot penetrate an app-server, client, or network stall and cannot force the model to resume. It can persist evidence and notify the user; it is not proof that the Agent is alive.

## Review and recover a stopped task

Run `python <WD_SCRIPT> recover-plan --thread THREAD [--turn TURN]` after an alert. This command is bounded and read-only: it does not send a prompt, replay a tool, stop a worker, or create a task.

Then recover in this order:

1. Inspect the target task through the Codex task/thread interface, including incomplete model output and current activity. Do not judge only from completed tool-call logs or file timestamps; an agent may be actively composing code before either changes.
2. If the task is active, streaming, preparing a model request, editing, or otherwise advancing, leave it untouched. Heartbeat only the exact tag when there is concrete progress evidence.
3. If the task is confirmed terminal or idle, remains unfinished, and has no advancing output, send one concise continuation to that same task. Tell it to inspect its existing disk state and continue the exact unfinished step. Do not duplicate the work in the monitoring task and do not start a competing worker.
4. After a reconnect, verify actual outputs before any retry. A missing UI notification is not proof that a side effect failed.
5. Use a small disk handoff and ask for a clean task only when same-task recovery is impossible or thread health is `critical`. Never fork or clone a critical history.

If `recover-plan` reports `backend_completed_refresh_client_if_busy`, the backend has positively completed even if Codex still displays Thinking. Do not wait, wake, stop, or retry that work. Switch to another task and back; reload Codex only if the stale indicator remains. The report reconstructs recent terminal evidence from at most 1,000 matching read-only log rows when the in-memory detector cache was restarted or pruned. The watchdog cannot observe or mutate the renderer's busy flag, so it records `ui_state: unobservable` and emits a one-time completion notification when a previously reviewed stall later reaches a backend terminal event.

Treat `severity: review`, `evidence_class: absence_only`, or `safe_to_interrupt: false` literally. These are review notices, not stall verdicts. The watchdog must remain lower-cost than the work it monitors; avoid repeated broad log scans or diagnostic prompts that preempt normal work.

## Create a visible sidebar task when explicitly requested

Treat “新开”, “新开对话”, “开 side chat”, “开一个左边栏可见的任务”, “换干净任务继续”, and equivalent wording as explicit authorization when the recovery context already identifies the work to hand off. Do not ask the user to repeat the authorization.

A visible user-owned task is not a subagent or Quick Chat:

- Use the Codex app `create_thread` tool for a task that must appear in the sidebar.
- Never substitute `spawn_agent`, a background worker, a subagent thread, or a commentary promise.
- Load only the exact `list_projects` and `create_thread` tools if they are deferred; do not enumerate a broad tool catalog.

Execute the handoff immediately:

1. Write or verify a small disk handoff first when continuity matters. Include the repository/worktree, branch or commit, dirty files, completed outputs, verification, one next action, safe retries, and forbidden repeats.
2. Run `list_projects` and select the project matching the exact workspace. For repo-scoped work, call `create_thread` with:

```json
{
  "prompt": "Read <HANDOFF_PATH>, use the specified repository/worktree, and perform only the recorded next action. Preserve completed work and forbidden repeats.",
  "target": {
    "type": "project",
    "projectId": "<PROJECT_ID>",
    "environment": { "type": "local" }
  }
}
```

Use a worktree environment only when isolation is requested. Set `startingState` to `working-tree` only when the user explicitly wants current uncommitted changes, or to `branch` only for an existing branch/ref. Omit `model` and `thinking` unless the user explicitly requests them. Use `projectless` only for genuinely non-project work.
3. After success, report the returned task ID and emit `::created-thread{threadId="..."}`; if creation is queued, emit the returned `clientThreadId` form. This receipt is required proof that a sidebar task was actually created.
4. If `create_thread` is unavailable or fails, say that creation did not occur. Do not claim success. Offer the documented fallback `codex://threads/new?prompt=...&path=...` or `Ctrl+N`; note that a deep link pre-fills the composer but does not send automatically.

## Recover oversized tasks

Run `python <SKILL_DIR>/scripts/check_thread_health.py` before substantial work after “continue” or a batch request. Resolve `<SKILL_DIR>` from this skill's own location; never hard-code a user profile path. Use `--thread ID` when diagnosing another task. On `critical`, do not continue or fork that task. Preserve repository and output files and write a small project handoff plus manifest. When the user explicitly requests a new visible task, follow the sidebar-task procedure above immediately instead of merely describing it.

Automatic review incidents write metadata-only recovery manifests under `$CODEX_HOME/watchdog/recovery_manifests` (or `~/.codex/watchdog/recovery_manifests` when `CODEX_HOME` is unset). They may identify a rollout path and byte size but never read, rewrite, compact, or delete rollout contents. A manifest is diagnostic evidence, not authorization to interrupt or retry.

## Keep watchdog metadata bounded

The daemon retains all active/stalled jobs, prunes disarmed jobs after 30 days or beyond the newest 500, and rotates `incidents.jsonl` at 5 MiB with three backups. Run `cleanup --dry-run` to inspect the exact plan; use `cleanup --apply` only when cleanup is requested. Both operations are restricted to the watchdog-owned runtime directory and must report `codex_data_touched: false`.

Read [references/protocol.md](references/protocol.md) before arming parallel jobs, handling a stall, or installing the per-user startup entry. Use [references/manifest.schema.json](references/manifest.schema.json) when reading or writing the job manifest.
Use [references/recovery-manifest.schema.json](references/recovery-manifest.schema.json) when consuming an automatic review recovery manifest.
Read [references/timeout-policy.md](references/timeout-policy.md) before selecting or changing a manual job's no-progress threshold.
