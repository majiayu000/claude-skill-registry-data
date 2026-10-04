---
name: task-status
description: Send reliable progress and completion updates to chat for long-running tasks in OpenClaw. Use when a task may take over 1 minute, when users require periodic updates, or when you must guarantee a final "completed/failed" callback even if command execution errors.
---

# Task Status Skill

Use these scripts to keep users informed and prevent silent finishes.

## 0) One-time default config

Persist your default target/channel once:

```bash
python scripts/configure_status.py --target YOUR_CHAT_ID --channel telegram --test
```

After this, other scripts can omit `--target`.

## 1) Guaranteed start/end callbacks (recommended)

Run long commands via `run_with_status.py` so completion is always reported.

```bash
python scripts/run_with_status.py \
  --task "windows-cursor-check" \
  --channel telegram \
  -- bash -lc "sleep 2 && echo done"
```

- Sends one `progress` message before command execution.
- Sends `success` or `error` when command exits.
- Includes elapsed time in final status.

## 2) One-off manual status messages

```bash
python scripts/send_status.py "开始执行" progress setup
python scripts/send_status.py "执行完成" success setup
python scripts/send_status.py "执行失败" error setup
```

If you do not want persisted config, pass `--target` each time.

## 3) Periodic monitor for very long tasks

```bash
python scripts/monitor_task.py start data-sync --interval 300
python scripts/monitor_task.py status
python scripts/monitor_task.py stop data-sync --final-status success --final-message "同步完成"
```

- `start` launches a detached background runner.
- `stop` always sends one final status update.
- `cancel_all` clears all active monitors.

## Status types

- `progress`: ongoing work
- `success`: completed
- `error`: failed
- `warning`: completed with risk/partial issues

## Troubleshooting

- Missing target: run `configure_status.py` or pass `--target`.
- No message sent: test with `--dry-run` first.
- Stale monitor: run `python scripts/monitor_task.py cancel_all`.
