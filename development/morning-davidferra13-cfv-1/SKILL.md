---
name: morning
description: One-command daily briefing. Build state, overnight changes, Pi/OpenClaw health, active priorities, session continuity.
user-invocable: true
---

# Morning Briefing

Generate a complete daily briefing so the developer knows exactly where things stand. Run all checks in parallel where possible.

## 1. Generate Session Briefing

```bash
bash scripts/session-briefing.sh
```

Then read `docs/.session-briefing.md` for the compressed state.

## 2. Build State

Read `docs/build-state.md` directly. Report: green or broken, last verified date, last commit.

## 3. What Changed Since Last Session

```bash
git log --oneline --since="18 hours ago"
```

If nothing, say so. If commits exist, summarize them in 1-2 lines each.

## 4. Uncommitted Work

```bash
git status --short
```

Report: clean, or count of modified/untracked files with a quick summary of what areas they touch.

## 5. Server Status (Quick Ping)

Run in parallel:

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3100 2>/dev/null || echo "DOWN"
```

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null || echo "DOWN"
```

Report: Dev (3100) UP/DOWN, Prod (3000) UP/DOWN.

## 6. Database Status

```bash
docker ps --filter "name=chefflow" --format "{{.Names}} {{.Status}}"
```

Report: healthy or not running.

## 7. Pi / OpenClaw Health (Best Effort)

```bash
ssh -o ConnectTimeout=3 -o StrictHostKeyChecking=no davidferra@10.0.0.177 "uptime && systemctl is-active openclaw-dashboard 2>/dev/null && df -h / | tail -1" 2>/dev/null || echo "Pi unreachable (not on home network?)"
```

If reachable: uptime, OpenClaw dashboard status, disk usage.
If unreachable: note it, move on. Not a blocker.

## 8. Staleness Check

Check the last `## ` entry date in `docs/session-log.md`. If older than 48 hours from now, flag:

```
WARNING: Last session log is [X] days old. Context may be stale. Run /status for current git state.
```

## 9. Active Priorities

Read `memory/project_current_priorities.md` and check the last 1-2 entries in `docs/session-log.md` (tail). Summarize what was in-flight and what's next.

## 10. Memory Check

Read `MEMORY.md` index. Flag any memories marked as time-sensitive or with dates approaching today.

## Report Format

Present as a single, scannable briefing:

```
MORNING BRIEFING - [date]

BUILD:     [green/broken] (last verified [date])
SERVERS:   Dev [UP/DOWN] | Prod [UP/DOWN] | DB [HEALTHY/DOWN]
PI:        [status or unreachable]
GIT:       [branch] | [X] uncommitted | [X] unpushed
OVERNIGHT: [summary of commits since last session, or "no changes"]

LAST SESSION: [1-line summary of what was done]
NEXT UP:      [what the active priorities suggest]

FLAGS: [anything unusual: broken build, stale data, approaching deadlines]
```

Keep it under 300 words. The developer has ADHD; dense walls of text get skipped. Visual structure matters.
