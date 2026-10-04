---
name: fleet-rollback-procedures
description: How DevOps rolls back safely — database migrations, config changes, service restarts. The difference between "undo" and "rollback" and when each deployment strategy needs what.
---

# Rollback Procedures — DevOps Safety Net

Deployment goes wrong. The question isn't IF but WHEN. Your job is to make rollback a practiced procedure, not a panic response.

## Rollback vs Undo

**Undo** = reverse the exact changes (dangerous — may not be possible for data changes).
**Rollback** = return to the last known good state (safe — always possible if prepared).

The fleet always rolls BACK, never UNDOs.

## Rollback by Layer

### 1. Application Code

**Docker-based services (MC):**
```
# Roll back to previous image tag
docker compose -f docker-compose.yaml up -d mc-backend --no-deps
# Uses the previous image tag from docker-compose.yaml history
```

**Agent behavior (no deployment needed):**
```
# Agent behavior = files in agents/_template/
# Roll back = git revert the template change
git revert HEAD  # revert last commit
# Then re-provision agents
scripts/provision-agent-files.sh
scripts/push-agent-framework.sh
```

**Gateway:**
```
# Stop gateway
scripts/stop-fleet.sh
# Revert changes
git checkout HEAD~1 -- gateway/
# Restart
scripts/start-fleet.sh
```

### 2. Database / State

MC uses SQLite or Postgres. Board state is the source of truth for tasks.

**Before ANY migration:**
- Back up the database: `cp mc.db mc.db.backup.$(date +%s)`
- For Postgres: `pg_dump -U mc -d mc > backup.sql`

**To rollback:**
- Stop MC: `docker compose stop mc-backend`
- Restore: `cp mc.db.backup.TIMESTAMP mc.db` (or `psql -U mc -d mc < backup.sql`)
- Start MC: `docker compose start mc-backend`

**Board memory is append-only.** You can't "undo" a board memory event — but you can post a correction event. Trail events persist permanently.

### 3. Configuration

Config is in `config/*.yaml` — version controlled.

```
# See what changed
git diff HEAD~1 config/
# Roll back specific config
git checkout HEAD~1 -- config/fleet.yaml
# Re-deploy
scripts/reprovision-agents.sh
```

### 4. Agent Sessions

If an agent is behaving incorrectly after a change:
```
# Prune the agent session (kills context, fresh start)
# The orchestrator's immune system does this automatically
# But you can trigger it manually:
fleet chat "Agent X needs session prune" --mention fleet-ops
```

## Rollback by Deployment Strategy

### Rolling Update
```
Rollback = rebuild from last passing tag
1. git checkout last-good-tag
2. docker compose build
3. docker compose up -d
Risk: database state may have advanced. Check migration compatibility.
```

### Blue-Green
```
Rollback = switch traffic back to green (previous)
1. Update load balancer to point to green environment
2. Done. Blue stays up for inspection.
Risk: nearly zero — green was never modified.
```

### Canary
```
Rollback = set canary weight to 0%
1. Route 0% traffic to canary
2. Canary stays up for debugging
3. When fixed: redeploy canary, gradually increase weight
Risk: low — only affected the canary percentage of traffic.
```

## Pre-Rollback Checklist

Before rolling back, verify:
1. **What actually broke?** — Don't rollback on assumptions. Check logs.
2. **Is the database compatible?** — If a migration ran, can the old code read the new schema?
3. **Are there in-flight tasks?** — Agents may be mid-work. Pause fleet first if needed.
4. **Who needs to know?** — `fleet_alert(category="infrastructure", severity="high")` + ntfy PO.

## The IaC Guarantee

Because everything is scripted:
- `setup.sh` produces the same fleet from zero
- `reprovision-agents.sh` regenerates all agent files from templates
- `push-agent-framework.sh` deploys the current state to all workspaces

Rollback = revert git commits + re-run scripts. No manual steps. No "I remember the command was..."

## After Rollback

1. Post incident to board memory: `[infrastructure, incident, rollback]`
2. Alert PO: `fleet_notify_human(title="Rollback: {what}", message="Rolled back {change} because {reason}")`
3. Create fix task: `fleet_task_create(title="Fix: {what failed}", agent_name="devops")`
4. Post-mortem: what broke, why, how to prevent recurrence
