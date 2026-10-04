---
name: ops-runbook
version: 1.0.0
description: Write an operational runbook any qualified operator can execute under pressure, with verification, failure paths, and escalation.
author: matrixx0070
tags: [operations, runbook, on-call, procedure, incident, sop]
capabilities: []
---

# Runbook

## When to use
Use this to write a step-by-step operational runbook for a recurring task or incident response, so any qualified operator — including on-call under pressure — can execute it correctly without tribal knowledge.

**Not for:** documenting a multi-role business process with a RACI (use ops-process-doc), or high-level policy. A runbook is one operator, one task, executable top-to-bottom.

## Method
1. **Define task and trigger.** State what the runbook covers, when it runs (schedule, alert, or condition), and the expected outcome.
2. **List prerequisites.** Access, credentials, tools, and preconditions that must be true before starting.
3. **State safety and impact.** Note what this affects, who to notify, and any destructive steps. *Decision:* flag every irreversible step with a confirm-before-proceeding gate.
4. **Write the procedure.** Numbered, copy-runnable steps. Per step: the action, the expected result, and how to tell it worked.
5. **Add verification.** Specify the checks that confirm end-to-end success.
6. **Cover failure paths.** For likely failure points, give symptom -> recovery/rollback action; include an escalation contact. *Decision:* if a step can fail silently, add an explicit check rather than assuming success.
7. **Record metadata.** Owner, last-tested date, review cadence — a runbook untested in 90 days is suspect.

## Example
**Title:** Clear stuck payment queue. **Trigger:** alert `queue_depth > 500 for 10m`. **Prereqs:** prod DB read/write, PagerDuty access.
1. Check queue depth (expected: >500). 2. Identify the blocking message ID (expected: one poison message). 3. Move it to the dead-letter queue (**destructive — confirm ID first**); expected: depth drops. **Verify:** depth < 50 within 5 min, no new errors. **Failure:** depth stays high -> restart the consumer; still high -> escalate to payments on-call (@payments-oncall).

## Pitfalls
- **Assuming context the reader lacks.** On-call at 3am has none of your mental model; spell out prereqs and expected results.
- **No expected result per step.** Without "you should see X," an operator can't tell success from silent failure.
- **Untested runbook.** Steps that were never rehearsed drift from reality; stamp and re-test on cadence.
- **Missing failure paths.** The happy path is the easy half; the value is knowing what to do when step 3 errors.

## Output format
```
Header:         title | purpose | trigger | severity
Prerequisites:  access | tools | preconditions
Impact:         what it affects | who to notify
Procedure:      numbered steps, each with expected result
Verification:   end-to-end success checks
Troubleshooting: symptom -> action table
Escalation:     who | when | how
Metadata:       owner | last tested | review cadence
```
