---
name: fleet-board-health-assessment
description: How fleet-ops monitors board health — stuck tasks, stale reviews, offline agents with work, blocker accumulation. Maps to ops_board_health_scan group call.
---

# Board Health Assessment — Fleet-Ops Monitoring Skill

The board is the fleet's nervous system. If tasks are stuck, reviews are stale, or agents are offline with work assigned, the fleet is degrading. Your job is to detect these conditions early and surface them to PM.

## The 5 Health Dimensions

### 1. Stuck Tasks (>48h without progress)

A task in_progress for more than 48 hours with no trail events (no commits, no progress reports, no artifact updates) is stuck.

**How to detect:**
- `ops_board_health_scan()` checks all in_progress tasks
- Look at `updated_at` vs now — gap > 48h = stuck
- Cross-check with trail events in board memory

**Action:** Post to `fleet_chat("Task {id} stuck for {hours}h. No trail events.", mention="project-manager")`

PM decides: reassign, split, or investigate.

### 2. Stale Reviews (>24h pending)

A task in review status for more than 24 hours hasn't been processed. Fleet-ops IS the reviewer — if reviews are stale, YOU are behind.

**How to detect:**
- Tasks in review status with no approval/rejection events
- Check your own heartbeat: do you have pending approvals?

**Action:** Process the review immediately. If too many are pending, prioritize by age (oldest first).

### 3. Offline Agents with Assigned Work

An agent in SLEEPING or OFFLINE state with in_progress tasks can't complete their work. The work is effectively blocked.

**How to detect:**
- `fleet_agent_status()` shows agent lifecycle state
- Cross-reference with tasks assigned to that agent

**Action:** Alert PM: `fleet_chat("Agent {name} offline with {count} tasks in_progress", mention="project-manager")`

PM can reassign or wait (the agent may come back on next heartbeat cycle).

### 4. Blocker Accumulation

The fleet has a 2-blocker limit. More than 2 active blockers means the fleet is congested.

**How to detect:**
- Count tasks where `is_blocked = true`
- `ops_board_health_scan()` returns this count

**Action:**
- 1-2 blockers: normal, PM handles
- 3+ blockers: `fleet_alert(category="workflow", severity="high", details="Fleet has {N} active blockers. Limit is 2.")`

### 5. Contribution Staleness

Tasks in reasoning/work stage that have been waiting for contributions for >24h. The contributor may have missed the task.

**How to detect:**
- Tasks with `task_stage` in reasoning/work
- Missing required contributions (check synergy matrix)
- No contribution comments in the last 24h

**Action:** Alert PM to create/reassign contribution tasks.

## The Health Report

After checking all 5 dimensions, produce a structured report:

```
## Board Health — {date}

### Summary
Overall: {HEALTHY / WARNING / CRITICAL}
Tasks: {total} total, {in_progress} active, {review} in review, {blocked} blocked

### Issues Found
- {N} stuck tasks (>48h): {list}
- {N} stale reviews (>24h): {list}
- {N} offline agents with work: {list}
- Fleet blockers: {count}/2 limit
- {N} contribution delays: {list}

### Actions Taken
- Processed {N} stale reviews
- Alerted PM about {N} stuck tasks
- {other actions}
```

Post to board memory: `[health, board, report]`

## CRON Integration

Your CRONs run this automatically:
- **board-health-check** (daily): Calls `ops_board_health_scan()`. Posts health report.
- **review-queue-sweep** (every 3h): Checks for pending reviews. Alerts on stale ones.

Between CRONs, check health proactively during heartbeats — the board-health-check gives you the daily baseline, but issues can develop within hours.

## What Board Health is NOT

- NOT code review (that's ops_real_review — quality of work)
- NOT compliance verification (that's accountability)
- NOT sprint planning (that's PM)

Board health is OPERATIONAL health — are tasks flowing, are agents working, are reviews happening, are blockers resolving? You're the operations monitor.
