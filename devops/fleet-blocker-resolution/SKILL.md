---
name: fleet-blocker-resolution
description: How PM resolves blocked tasks — the 5 resolution options, the 2-blocker fleet limit, and when to escalate vs self-resolve.
---

# Blocker Resolution — PM's Fleet Unblocking Protocol

A blocked task is a stopped agent. Two blocked tasks is a warning. Three or more is a fleet emergency. Your job is to keep the fleet moving — never more than 2 active blockers at any time.

## The 2-Blocker Rule

The fleet has a hard limit: **maximum 2 active blockers simultaneously**. When you call `pm_blocker_resolve(task_id)`, it counts fleet-wide blockers. If the count exceeds 2, the tool returns `warning: "Fleet has N active blockers (limit: 2). RESOLVE URGENTLY."`

This isn't arbitrary. Blockers cascade: if architect is blocked, engineer can't get design_input. If engineer is blocked, QA can't validate. Three blockers can freeze half the fleet.

## The 5 Resolution Options

### 1. Reassign
**When:** The blocking dependency is on an agent, and another agent can handle it.
**Example:** Architect is offline (SLEEPING) and engineer needs design_input. DevOps has secondary architecture capability for simple tasks.
**Action:** `fleet_task_create(agent_name="devops", ...)` or update blocked task's dependency.

### 2. Split
**When:** Part of the task CAN proceed, part is blocked.
**Example:** Task needs security review (blocked — devsecops offline) but non-security work can continue.
**Action:** Split into two subtasks: one for non-security work (unblocked), one for security-dependent work (stays blocked).

### 3. Remove Dependency
**When:** The dependency was set too broadly, or the blocker has been resolved outside the system.
**Example:** Task blocked on "design review" but architect already provided design_input via chat — just not recorded as a formal contribution.
**Action:** Update task to remove the blocking dependency. Post a comment explaining why.

### 4. Escalate
**When:** Resolution requires PO decision — conflicting priorities, resource allocation, scope change.
**Example:** Both architect and engineer are blocked on the same external API being down. This is an infrastructure issue, not a coordination issue.
**Action:** `fleet_escalate(title="...", details="...", task_id="...")`

### 5. Create Subtask
**When:** The blocker IS the missing work — no one has been assigned to produce the blocking input.
**Example:** Engineer blocked on design_input, but no contribution task exists for architect.
**Action:** `fleet_task_create(title="Design input for: {blocked_task}", agent_name="architect", task_type="subtask", parent_task=blocked_task_id)`

## Resolution Decision Tree

```
Blocked task identified
  |
  +-- Is the blocker a missing contribution?
  |     YES --> Is there a contribution task for it?
  |     |         YES --> Is the contributor agent online?
  |     |         |         YES --> Wait (it's in progress). Check back in 2 heartbeats.
  |     |         |         NO  --> Option 1: REASSIGN to backup agent
  |     |         NO  --> Option 5: CREATE contribution subtask
  |     NO --> Continue
  |
  +-- Is the blocker an external dependency?
  |     YES --> Can we work around it?
  |     |         YES --> Option 2: SPLIT the task
  |     |         NO  --> Option 4: ESCALATE to PO
  |     NO --> Continue
  |
  +-- Is the blocker a task that's stuck?
  |     YES --> Is the stuck task's agent active?
  |     |         YES --> fleet_chat(@agent, "Your task X is blocking Y. ETA?")
  |     |         NO  --> Option 1: REASSIGN the stuck task
  |     NO --> Continue
  |
  +-- Is the dependency actually necessary?
        NO  --> Option 3: REMOVE dependency
        YES --> Option 4: ESCALATE — need PO decision
```

## After Resolution

Always:
1. Post a comment on the blocker task explaining what you did and why
2. Record trail via board memory
3. Check fleet blocker count — is it back to <=2?
4. If the resolution created new tasks, triage them properly (all 12 fields)
