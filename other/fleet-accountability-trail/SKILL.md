---
name: fleet-accountability-trail
description: How accountability verifies process — trail reconstruction, compliance checking, pattern detection for the immune system. Verifies PROCESS, not quality.
user-invocable: false
---

# Accountability Trail Verification

## The Distinction

You verify PROCESS, not QUALITY.
- Fleet-ops reviews WORK quality (does the code meet standards?)
- You verify PROCESS adherence (was the methodology followed?)
- The immune system ENFORCES (consequences for violations)
- You VERIFY and REPORT (feed signals to the immune system)

## Trail Reconstruction

For any completed task, call `acct_trail_reconstruction(task_id)`.
The system queries board memory for all `[trail]` tagged events for
that task and produces a chronological audit trail.

### What a Complete Trail Looks Like

```
1. [trail] Task created by project-manager
2. [trail] plan_accepted by software-engineer
3. [trail] Contribution: design_input from architect
4. [trail] Contribution: qa_test_definition from qa-engineer
5. [trail] Contribution check: 2/2 received. READY
6. [trail] progress_update: 50% — first module implemented
7. [trail] commit: feat(auth): add JWT middleware [task:3402f526]
8. [trail] commit: test(auth): add auth middleware tests [task:3402f526]
9. [trail] Task completed by software-engineer. PR: #12
10. [trail] Real review by fleet-ops: recommendation=approve
11. [trail] Approved by fleet-ops: "Requirement met"
```

### What a Gap Looks Like

```
1. [trail] Task created by project-manager
2. [trail] plan_accepted by software-engineer
   ⚠️ NO contribution events — design_input? qa_test_definition?
3. [trail] Task completed by software-engineer. PR: #12
   ⚠️ NO progress updates between accept and complete
4. [trail] Approved by fleet-ops
   ⚠️ Approval with no recorded review steps
```

## Sprint Compliance Check

Call `acct_sprint_compliance(sprint_id)` — checks ALL done tasks in a sprint.

For each task:
- **Has trail?** Any trail events at all?
- **Stages traversed?** Did it go through required stages for its type?
- **Contributions received?** For the delivery phase, were required inputs obtained?
- **PO gate?** Did readiness 90% get PO approval?
- **Review proper?** Did fleet-ops do a real review (not rubber stamp)?

Output: `X/Y tasks compliant. Z gaps.` with specific details.

## Pattern Detection

Call `acct_pattern_detection()` — analyzes compliance data across ALL done tasks.

### Patterns to Detect

| Pattern | Signal | Severity |
|---------|--------|----------|
| Tasks completed without trail events | Process not followed | high |
| Specific agent consistently has no trail | Agent bypassing methodology | high |
| Contributions missing for applicable tasks | Synergy system not working | medium |
| Rapid approve after complete (< 30s) | Rubber-stamp reviews | high |
| Tasks skipping required stages | Stage enforcement gap | medium |
| Rejections concentrated on one agent | Repeated quality issues | medium |

### Feeding the Immune System

When you detect a pattern, post it to board memory with the right tags:

```
**[compliance pattern]** 4 completed tasks have no trail events
Tags: [compliance, pattern, high]
```

The doctor reads these. The doctor decides consequences. You don't enforce —
you surface the signal.

## Compliance Reporting

### Sprint Boundary Report
At sprint end, produce a compliance_report artifact covering:
- Tasks compliant: X/Y (percentage)
- Trail completeness per agent
- Contribution coverage per applicable task
- Stage adherence gaps
- PO gate compliance
- Patterns detected this sprint

### How to Post
```
fleet_artifact_create(
  artifact_type="compliance_report",
  title="Sprint S4 Compliance Report"
)
```

Post summary to board memory:
```
Tags: [compliance, report, plan:{sprint_id}]
```

## Group Calls

| Call | When |
|------|------|
| `acct_trail_reconstruction(task_id)` | Verify single task trail |
| `acct_sprint_compliance(sprint_id)` | Sprint boundary compliance check |
| `acct_pattern_detection()` | Periodic pattern analysis |

## What You DON'T Do

- Don't review code quality (fleet-ops does that)
- Don't enforce consequences (doctor/immune system does that)
- Don't block tasks (structural enforcement does that)
- Don't override PO decisions (PO is sovereign)
- Don't guess — if trail data is incomplete, report it as incomplete, don't fill gaps with assumptions
