---
name: fleet-backlog-grooming
description: How PM grooms the backlog — re-estimate, re-prioritize, identify stale items, prepare for PO review. Maps to backlog-grooming CRON and sprint boundary operations.
---

# Backlog Grooming — PM's Maintenance Discipline

The backlog decays. Tasks that were high priority last sprint may be irrelevant now. Estimates that made sense before investigation may be wrong after. Your job is to keep the backlog CURRENT — not just add to it, but maintain it.

## When to Groom

- **backlog-grooming CRON** (Wednesday 2pm): Your scheduled grooming session
- **Sprint boundary:** Before planning the next sprint, groom what's available
- **After major changes:** Scope change, PO directive, project pivot

## The 5 Grooming Actions

### 1. Re-Estimate

Story points set at triage are guesses. After analysis or investigation, the real scope is clearer.

**Check each task in inbox/reasoning:**
- Does the current estimate match what we now know?
- Did investigation reveal unexpected complexity? → Increase SP
- Did architect simplify the design? → Decrease SP
- Is it bigger than an 8? → Should be an epic, not a story

### 2. Re-Prioritize

Priorities shift. A task that was urgent last week may be blocked by something else now.

**Check:**
- Is the priority still correct given current sprint goals?
- Are there new dependencies that change the order?
- Did the PO's directive change what matters most?
- Are high-priority tasks actually ACTIONABLE (not blocked)?

### 3. Identify Stale Tasks

A task that's been in inbox for 3+ sprints without progress is stale.

**Stale indicators:**
- Created >2 weeks ago, still in inbox, no comments
- Assigned but agent never started (SLEEPING agent?)
- Blocked for >1 sprint with no resolution path
- Requirement references outdated information

**Actions:**
- Still relevant? → Update description, re-estimate, re-assign
- No longer relevant? → Flag to PO: "Task X appears stale. Archive?"
- Blocked permanently? → Escalate or split

### 4. Verify Field Completeness

Tasks accumulate with incomplete fields — missing verbatim, no story points, vague descriptions.

**Check each inbox task:**
- requirement_verbatim populated?
- story_points set?
- agent_name assigned?
- task_type correct?
- delivery_phase set?
- acceptance criteria exist and are testable?

Use `/fleet-task-triage` for the full 12-field checklist.

### 5. Prepare for PO

After grooming, prepare a summary for the PO:

```
fleet_chat(
    "Backlog grooming complete:\n"
    "- {N} tasks re-estimated (3 increased, 1 decreased)\n"
    "- {N} priorities adjusted\n"
    "- {N} stale tasks flagged for archive\n"
    "- {N} tasks with incomplete fields updated\n"
    "Sprint-ready: {N} tasks in inbox, {SP} total SP available",
    mention="human"
)
```

Post to board memory: `[backlog, grooming, sprint]`

## CRON Integration

Your **backlog-grooming** CRON runs Wednesday at 2pm:
1. Load all inbox tasks
2. Check each against the 5 actions above
3. Update fields that need correction
4. Flag items that need PO decision
5. Post grooming summary to board memory

This is the PM's maintenance CRON — like the devops infrastructure health check, but for the task backlog.

## What Backlog Grooming is NOT

- NOT sprint planning (that's fleet-sprint-planning — choosing WHAT to commit to)
- NOT task creation (that's triage — processing NEW work)
- NOT completion (grooming doesn't DO the work — it ensures the work is READY to be done)

Grooming is MAINTENANCE. It keeps the backlog healthy so sprint planning has good material to work with.
