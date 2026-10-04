---
name: fleet-fix-task-handling
description: How engineers handle rejected tasks — read feedback, find root cause, add regression tests, re-submit. The fix cycle that prevents repeat rejections.
---

# Fix Task Handling — Engineer's Rejection Recovery

When fleet-ops rejects your work, the system creates a fix task. This skill teaches how to handle it correctly — addressing root causes, not symptoms.

## What Happens When You're Rejected

1. Fleet-ops calls `fleet_approve(decision="rejected", comment="specific feedback")`
2. Your task regresses: status → inbox (rework), readiness → 80%, stage → reasoning
3. The rejection comment appears on your task as a typed comment
4. A fix task may be auto-created with the rejection as its verbatim requirement
5. You see the rejection on your next heartbeat

## The Fix Cycle

### Step 1: Read the Feedback — Call eng_fix_task_response

```
eng_fix_task_response()  # reads rejection from current task or parent
```

This extracts: what was rejected, why, the original verbatim requirement for re-grounding.

### Step 2: Identify the ROOT CAUSE

The rejection says "Missing input validation on /api/tasks." The symptom is missing validation. The root cause might be:
- You didn't read the security_requirement contribution (process failure)
- You read it but didn't implement all controls (implementation gap)
- The requirement was ambiguous (communication failure → escalate, don't guess)

Fix the cause, not the symptom. If you only add the one missing validation but the real cause is "didn't read contributions," you'll be rejected again for the next missing control.

### Step 3: Add Regression Tests FIRST

Before fixing the code, write a test that would have caught the issue:
```
# This test would have caught the missing validation
def test_api_tasks_rejects_invalid_input():
    response = client.post("/api/tasks", json={"title": ""})
    assert response.status_code == 400
```

Then fix the code to make the test pass. This is TDD applied to fix tasks — the rejection becomes a test case.

### Step 4: Verify Against Original Contributions

Re-read ALL contributions on your task. For each one, verify your implementation:
- design_input: does the code follow the architect's pattern?
- qa_test_definition: does each TC-XXX pass?
- security_requirement: is each control implemented?

### Step 5: Re-submit

Call `fleet_task_complete(summary="Fixed: [what was wrong] by [what you changed]. Added regression test for [specific scenario].")`.

The summary should prove you understood the feedback, not just patched the symptom.

## What NOT to Do

- Do NOT argue with the rejection in chat. The feedback is specific for a reason.
- Do NOT only fix the exact thing mentioned. Look for the pattern — if one validation was missing, check all validations.
- Do NOT skip the regression test. The test proves the fix and prevents recurrence.
- Do NOT change the design. If the architect's design_input was correct, follow it. If you think it was wrong, escalate via `fleet_chat(mention="architect")` — don't silently deviate.

## If You're Rejected Three Times

The Doctor detects repeated rejections via `signal_rejection()`. Three rejections on the same task may trigger:
- Teaching lesson (disease detection → you must complete an exercise)
- Session prune (contaminated context is killed, fresh session on next heartbeat)
- Escalation to PO

This is the immune system protecting the fleet from stuck agents. The fix: slow down, re-read everything from scratch, and address the actual root cause.
