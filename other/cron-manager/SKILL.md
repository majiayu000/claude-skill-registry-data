---
name: cron-manager
description: View, analyze, and modify the current user's crontab on the system
activation_keywords: [cron, crontab, scheduled, task, schedule, job]
execution_mode: client
---

# Cron Manager Skill

## Read (current user / system / status)

- **list** — current user's crontab (`crontab -l`)
- **system** — system crontab files where readable (`/etc/crontab`, `/etc/cron.d/*`)
- **status** — macOS: `launchctl list` (job list; may be long)

## Write (current user crontab only)

Use `builtin_cron_manager` with `operation`:

- **write** — replace entire user crontab. Pass **`content`** (full crontab text, newline-terminated lines as usual).
- **append_line** — append one cron line. Pass **`line`** (single line, no embedded newlines).
- **clear** — remove the current user's crontab (`crontab -r`).

**Safety:** `write`/`append_line`/`clear` affect **only the OS user running the desktop app** (not root). Prefer **append_line** for adding a single job. Review **write** before applying — it replaces the whole file. **Risk is elevated** (medium): confirm in the UI when prompted.

## Parameters

| Field | Used when |
|-------|-----------|
| `operation` | `list` \| `system` \| `status` \| `write` \| `append_line` \| `clear` |
| `content` | `operation=write` |
| `line` | `operation=append_line` |

Note: On Linux servers, `status` uses `launchctl` (macOS); for server-side runs, use **client** execution on the target machine.
