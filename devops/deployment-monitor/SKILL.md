---
name: deployment-monitor
description: Self-healing deployment monitoring skill. Use when checking deployment health, responding to failures, or setting up monitoring.
---

Monitor deployments and self-heal when possible.

## Check Flow

Every 30 minutes:
1. Query deployment API for latest status
2. If **READY** → log and exit
3. If **BUILDING** → wait, check next cycle
4. If **ERROR** → enter self-heal flow

## Self-Heal Flow

```
Failure detected
  ├── Attempt redeploy (retry 1/3)
  │   ├── Wait for completion (max 3 minutes)
  │   ├── If READY → alert: "Self-healed after 1 attempt"
  │   └── If ERROR → retry 2/3
  │       ├── If READY → alert: "Self-healed after 2 attempts"
  │       └── If ERROR → retry 3/3
  │           ├── If READY → alert: "Self-healed after 3 attempts"
  │           └── If ERROR → alert: "FAILED — manual review needed"
  └── Last working deployment stays live (platform default)
```

## Alert Format

Success:
```
Deployment self-healed after N attempt(s).
Commit: [message]
URL: [deployment URL]
```

Failure:
```
DEPLOYMENT FAILED — self-heal exhausted (3 attempts).
Commit: [message]
URL: [deployment URL]
State: ERROR
Last working deployment is still live. Manual review needed.
```

## Safety Rules

- Never force-deploy over a working version
- Never skip CI checks
- Never deploy on Fridays unless critical
- Check cron schedule before any restart (no restarts within 5 minutes of a scheduled job)
