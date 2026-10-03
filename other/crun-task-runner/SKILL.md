---
name: crun-task-runner
description: Submit, estimate, monitor, and retrieve Crun asynchronous media tasks through CreateTask and TaskInfo. Use when an exact Crun model and its input parameters are known, when an existing task_id must be checked, or when another Crun skill needs the shared execution workflow.
---

# Crun Task Runner

Treat this skill as the authority for task creation, authorization, monitoring, recovery, and result delivery. Use `../../runtime/crun_cli.py`; optionally set `CRUN_BASE_URL` for a non-default endpoint. Never print or persist an API key in task files.

## Prepare media and JSON

Upload a local image, video, or audio file before putting it in a task input:

```text
python <runtime>/crun_cli.py upload <local-file>
```

Put the returned `file_url` in the model input. Never send Base64, data URIs, or local paths. Reuse a prior Crun task's resource URL directly for derivative work.

Prefer UTF-8 files to avoid shell-specific JSON quoting:

```text
python <runtime>/crun_cli.py task estimate --model <model> --input-file <input.json>
```

Use `--input-file -` to read one JSON object from stdin. Use `--input-json` only when the current shell preserves the JSON string exactly.

## Run a task

1. Describe the selected model when its exact input schema is not already known:

   ```text
   python <runtime>/crun_cli.py models describe --model <model>
   ```

2. Construct only fields permitted by `input_schema`.
3. Estimate the final model and exact input before creating any task, including a user-specified model. Require
   `affordable: true`. This matters because `CreateTask` charges credits and is never retried, so submitting an
   unaffordable or malformed task wastes a real charge.
4. If routing selected the model, report the model, estimate, and relevant settings, then wait for explicit confirmation. Do not treat the original generation request as this confirmation. Skip only this extra confirmation when the user explicitly named the model.
5. Submit once and capture the returned `task_id`:

   ```text
   python <runtime>/crun_cli.py task create --model <model> --input-file <input.json>
   ```

6. Continue only with that ID. Prefer a shorter timeout and resume in rounds, because a single long-running command
   can be killed by the host before it returns — losing the recovery snapshot the runtime prints on timeout:

   ```text
   python <runtime>/crun_cli.py task wait --task-id <task_id> --timeout-seconds 120
   ```

   Re-run the same `task wait` to keep polling. Use a longer `--timeout-seconds` only when the command can run in the
   background without being interrupted.

Keep `task run` and `media run` only for compatibility or deliberate one-shot use. Both create a task directly and do
not estimate affordability or satisfy the routed-model confirmation gate; estimate and confirm yourself before using
them, and do not use them as the default agent workflow. Preserve their flushed `task_created` event so an
interruption never causes a duplicate submission.

## Resume and recover

Inspect an existing task with `task status --task-id <task_id>` or resume it with `task wait --task-id <task_id>`. Treat `pending` and `running` as nonterminal, `success` as successful, and `failed` as terminal.

Never inspect `~/.crun/output/yyyy-mm-dd/` to discover a task ID or infer remote state. It is only a download cache, with each task stored in its own `task_id` subdirectory. If no ID was captured, report that instead of guessing.

When local polling times out:

1. Show `details.last_task`, including at least `task_id` and `status` plus useful available fields. Say explicitly when no remote snapshot was captured.
2. Ask the user to choose between continuing the original task and creating a new task. Warn that a new task does not cancel the original, both may complete, and additional credits may be charged.
3. Stop until the user explicitly chooses. Do not automatically query, wait, or create again.

If the user continues, call `task wait` with the original ID. If the user authorizes a new task, validate and estimate it again, verify affordability, and create exactly once. Keep the original ID in the response.

When a task reaches terminal `failed`, report its ID, model, and error, then obtain explicit permission before any replacement or retry. When an estimate is unaffordable, report the model, estimate, and balance, then obtain explicit permission before changing models; validate and estimate the replacement before creation.

## Reliability rules

- Inspect the JSON response `code`, not only HTTP status.
- Never automatically retry `CreateTask`; an uncertain retry can create a duplicate charged task.
- Retry only safe requests and TaskInfo network failures within the configured limits.
- Never change a model or drop rejected input fields silently.
- Treat a task ID handoff as evidence of creation, not completion.
- Treat only TaskInfo for the captured ID as authoritative task state.

## Deliver results

Return normalized `task_id`, `status`, `model`, `credits`, `local_media_paths`, `media_urls`, `media_info`, `suno_data`, `usage`, and `error`, preserving useful specialized result fields.

Prefer local media paths. Where the client renders inline media, preview images or videos with an absolute
forward-slash path such as `![result](/C:/path/to/file.png)`. Use remote URLs as fallback and identify any download
errors instead of claiming a failed download is local.
