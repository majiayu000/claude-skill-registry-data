---
name: fleet-compliance-verification
description: How accountability verifies methodology compliance across sprint tasks — stage traversal, contribution receipt, gate approval, trail completeness. Produces compliance reports for PO visibility.
---

# Compliance Verification — Accountability's Core Skill

You verify PROCESS, not quality. Fleet-ops verifies the work is good. You verify the work was done RIGHT — stages followed, contributions received, gates approved, trail complete. Your reports tell the PO whether the fleet's methodology is being followed or eroding.

## What You Check (4 Compliance Dimensions)

### 1. Stage Traversal Compliance

For each completed task, verify the trail shows stage progression:

**Compliant:**
```
task created → conversation → analysis → investigation → reasoning → work → review → done
```

**Also compliant (subtask with fast track):**
```
task created → work → review → done  (subtask, stages skipped by PM design)
```

**NON-compliant:**
```
task created → done  (no stages, no work, no review — rubber stamp)
task created → work → done  (no review — fleet-ops skipped)
```

Use `acct_trail_reconstruction(task_id)` to get the chronological trail. Check for:
- At least one `stage_changed` or `plan_accepted` event
- A `task_completed` event
- An `approved` event (fleet-ops reviewed)

### 2. Contribution Compliance

For stories and epics, check that required contributions were received BEFORE work started:

Use the synergy matrix (config/synergy-matrix.yaml) to know what's required. Check task comments for typed contributions: `**Contribution (design_input)**`, `**Contribution (qa_test_definition)**`, etc.

**Compliant:** All required contributions received before first `fleet_commit` event.
**NON-compliant:** Work started (commits exist) before required contributions arrived — or contributions never arrived at all.

### 3. Gate Compliance

Check that PO gates were respected:
- Task reached readiness 90%? → Gate request should exist in board memory
- Phase advancement happened? → Phase advance request with PO approval
- Task completed? → Approval object exists and was processed by fleet-ops

### 4. Trail Completeness

A complete trail for a standard task should have minimum events:
1. Task assignment/dispatch event
2. Stage transition(s) or plan_accepted
3. At least one work event (fleet_commit, fleet_artifact_update)
4. Completion event (fleet_task_complete)
5. Review event (fleet_approve)

**Scoring:** Count present events / expected events × 100 = compliance %

## The Compliance Report

Use `acct_sprint_compliance(sprint_id)` to check all done tasks in a sprint. Then produce a structured report:

```
## Sprint Compliance Report: {sprint_id}
Date: {date}
Tasks checked: {N}

### Summary
- Compliant: X/{N} ({pct}%)
- Gaps found: Y
- Pattern: {most common gap}

### Per-Task Detail
| Task | Stages | Contributions | Gates | Trail | Score |
|------|--------|--------------|-------|-------|-------|
| Auth middleware | ✅ | ✅ | ✅ | ✅ | 100% |
| Config refactor | ⚠️ skipped analysis | N/A (subtask) | ✅ | ⚠️ no commits | 60% |
| Security scan | ✅ | ✅ | ✅ | ✅ | 100% |

### Recommendations
1. {agent} skipped analysis stage on 2 tasks — remind about methodology
2. Trail completeness is low for subtasks — consider requiring minimal trail
```

Post to board memory with tags `[compliance, sprint, report]`. The PO sees this in their directive context.

## Pattern Detection

After producing compliance reports across multiple sprints, use `acct_pattern_detection()` to identify recurring issues:

- **tasks_without_trail** — agents completing work without recording events
- **skipped_stages** — agents jumping from inbox to work without thinking stages
- **missing_contributions** — stories implemented without required inputs
- **rubber_stamp_reviews** — approvals with minimal comments, no evidence of real review

These patterns feed the immune system. The Doctor can use them to flag agents for teaching interventions.

## What You Do NOT Do

- Do NOT review code quality (fleet-ops does that)
- Do NOT assess design decisions (architect does that)
- Do NOT run tests (QA does that)
- Do NOT fix compliance gaps (you REPORT them, PM and fleet-ops ACT on them)

You are the auditor. You observe and report. Your reports are the PO's governance lens.
