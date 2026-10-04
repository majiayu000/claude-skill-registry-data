---
name: manage-schedules
description: View, add, update, or cancel scheduled tasks. Use when asked about schedules, cron jobs, reminders, or recurring tasks.
---

# Manage Scheduled Tasks

## When to use

- User asks to schedule a reminder, recurring task, or one-time task
- User asks to see, list, update, or cancel scheduled tasks

## CLI

All operations go through `tsx src/schedule-cli.ts` from the project root (`/data_fast/home/jusjinuk/codes/internbot`).

### List tasks

```bash
tsx src/schedule-cli.ts list                    # all active tasks
tsx src/schedule-cli.ts list --channel C0AJCU4H020  # tasks in a specific channel
```

### Add a task

```bash
# One-time (--value is an ISO timestamp in UTC)
tsx src/schedule-cli.ts add --channel C0AJCU4H020 --user "alice" --prompt "check server status" --type once --value "2026-03-04T10:00:00.000Z"

# Recurring (--value is a cron expression)
tsx src/schedule-cli.ts add --channel C0AJCU4H020 --user "alice" --prompt "search arxiv for RL papers" --type cron --value "0 9 * * 1"
```

### Get task details

```bash
tsx src/schedule-cli.ts get task-abc123
```

### Cancel a task

```bash
tsx src/schedule-cli.ts cancel task-abc123
```

### Update a task

```bash
tsx src/schedule-cli.ts update task-abc123 --prompt "new prompt text"
tsx src/schedule-cli.ts update task-abc123 --value "0 9 * * 1-5"   # updates cron and recomputes next_run
```

### View run history

```bash
tsx src/schedule-cli.ts logs task-abc123
```

## Notes

- The scheduler polls every 60 seconds; tasks may run up to 60s after their scheduled time
- All times are stored in UTC. The server timezone is `Asia/Seoul` (KST = UTC+9)
- For cron expressions: `0 9 * * 1-5` = weekdays at 9am KST, `0 0 * * 1` = Monday midnight KST
- `--type once` tasks auto-complete after running; `--type cron` tasks repeat
- The `--channel` and `--user` for `add` should match the Slack channel ID and username from the conversation context
