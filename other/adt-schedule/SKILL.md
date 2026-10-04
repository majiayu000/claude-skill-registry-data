---
name: schedule
description: Define and manage recurring automated agent runs — CI monitoring, dep updates, security scans
triggers:
  - schedule
  - recurring
  - cron
  - run every
  - automate on schedule
---

# Schedule

Define recurring agent tasks that run without manual triggering.

## Common Schedules

| Task | Frequency | Agent | Skill |
|---|---|---|---|
| Dependency audit | weekly | reviewer | secure |
| CI health check | on PR update | explorer | verify |
| Backlog grooming | weekly | orchestrator | plan |
| Security scan | daily | reviewer | secure |
| Context cleanup | per session end | orchestrator | context |
| Memory sync | per session end | orchestrator | resume |

## Definition Format

```json
{
  "name": "<task name>",
  "cron": "<cron expression or keyword>",
  "agent": "<agent name>",
  "skill": "<skill to invoke>",
  "scope": "<files or directories>",
  "notify": "on-failure | always | never"
}
```

## Keywords

- `on-pr` — run when a PR is created or updated
- `on-push` — run on every push to the branch
- `on-session-start` — run at the beginning of each agent session
- `on-session-end` — run at the end of each session
- `daily` / `weekly` / `monthly` — calendar schedules

## Rules

- Scheduled tasks run at the cheapest viable tier
- Never schedule destructive actions (deploy, force push)
- On failure: retry once, then log and continue
- Scheduled results feed back into the next session via memory
- Keep schedules minimal — 3-5 recurring tasks max
