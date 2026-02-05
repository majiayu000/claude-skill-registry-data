---
name: implementing-a-plan
description: Loads plan, reviews critically, executes each batch, and reports for review between batches. Use when implementing a plan from a plan file.
---

## The Process
1. Load plan and review critically
2. Execute each batch with using a subagent in order
3. Report for review between batches
4. Incorporate feedback, if any
4. Continue until all batches are done

### Step 1: Load and Review Plan
1. Read plan file
2. Review critically. Identify any questions or concerns about the plan
3. If concerns: Raise them with your human partner before starting
4. If no concerns: Proceed with implementation

### Step 2: Execute Batch
Dispatch fresh subagent

```
Task tool (general-purpose):
  description: "Implement Batch N"
  prompt: |
    You are implementing Batch N from [batch-file] created from [plan-file].

    Read both the plan and the batch carefully. Your job is to:
    1. Implement exactly what the batch file specifies
    2. Verify implementation works
    3. Commit your work
    4. Report back

    Work from: [directory]

    Report: What you implemented, what you executed and their results, files changed, any issues
```

### Step 3: Report
When batch is complete:
- Show what was implemented
- Show verification output
- Say: "Ready for feedback."

### Step 4: Continue
- Incorporate and apply changes if needed
- Fill out the recap section of the next batch file
  - Include any deviations from the plan that resulted from human feedback
  - Include the agent output from the most recent batch
- Execute next batch
- Repeat until complete

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker mid-batch (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

**Core principle:** Batch execution with checkpoints for architect review.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Between batches: just report and wait
- Stop when blocked, don't guess
