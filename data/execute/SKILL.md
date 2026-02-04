---
name: execute
description: >
  Execute implementation plans with checkpoints.
  Use to systematically work through planned tasks with progress tracking.
---

# Executing Implementation Plans

## Overview

Load plan, review critically, execute tasks in batches, report for review between batches.
Stop immediately when blocked - never guess.

**Core principle:** Batch execution with checkpoints for review.

**Announce at start:** "I'm using the execute skill to implement this plan."

## The Process

### Step 1: Load and Review Plan

1. Read the plan file completely
2. Review critically - identify any questions or concerns
3. **If concerns:** Raise them before starting. Don't proceed with unclear instructions.
4. **If no concerns:** Create TodoWrite with all tasks, proceed to Step 2

**Questions to ask:**
- Are file paths clear and complete?
- Is the code complete or does it have placeholders?
- Do I understand the test expectations?
- Are there implicit dependencies not listed?

### Step 2: Execute Batch

**Default batch size: 3 tasks**

For each task in the batch:
1. Mark task as `in_progress` in TodoWrite
2. Follow each step exactly as written
3. Run verifications as specified in plan
4. Mark as `completed` only when ALL steps pass
5. Capture learnings: `kodo reflect --signal "Pattern that worked: ..."`

**Execute steps literally:**
- If plan says "run `cargo test`" - run exactly that
- If plan says "expected output: FAIL" - verify you see FAIL
- If plan shows code - use that exact code

### Step 3: Report

When batch complete:
```
Completed tasks 1-3:
- Task 1: [summary] - PASS
- Task 2: [summary] - PASS
- Task 3: [summary] - PASS

Verification output:
[key test results]

Ready for feedback before continuing.
```

**Wait for user response before proceeding.**

### Step 4: Continue or Adjust

Based on feedback:
- **"Continue"** - Execute next batch
- **"Fix X"** - Apply changes, re-verify, then continue
- **"Stop"** - Save progress, note remaining tasks

Repeat Steps 2-4 until complete.

### Step 5: Completion

After all tasks complete:
1. Run full test suite
2. Verify all commits are clean
3. Offer code review: "Ready for review with `kodo:review` skill?"
4. Capture session learnings: `kodo reflect`

## When to Stop Immediately

**STOP executing when:**
- Hit a blocker (missing dependency, unclear instruction)
- Test fails unexpectedly (not expected failure)
- Plan has critical gaps
- You don't understand what a step means
- Verification fails after 2 attempts

**Ask for clarification rather than guessing.**

```
BLOCKED on Task 3, Step 2:

Plan says: "Run migration"
Problem: No migration file exists at specified path

Options:
A) Create migration file (show me what to create)
B) Skip this step (may cause issues in Task 4)
C) Abort and revise plan

Which approach?
```

## Progress Tracking

Use TodoWrite to track:
```
- [x] Task 1: Add config struct
- [x] Task 2: Implement parser
- [ ] Task 3: Add validation (IN PROGRESS)
- [ ] Task 4: Wire up CLI
- [ ] Task 5: Add tests
```

Update after each task completion, not at batch boundaries.

## Integration with Kodo

**During execution:**
```bash
kodo reflect --signal "This pattern worked well"
kodo query "error handling"  # When stuck, check context
```

**After completion:**
```bash
kodo reflect              # Capture all session learnings
kodo track link #123      # Update linked GitHub issue
```

## Key Principles

- **Review plan critically first** - Don't blindly execute broken plans
- **Follow steps exactly** - Plans are pre-validated, trust them
- **Don't skip verifications** - They catch issues early
- **Stop when blocked** - Guessing creates more problems
- **Report and wait** - User feedback between batches

## Red Flags

**You're doing it wrong if:**
- Executing without reviewing plan first
- Skipping verification steps
- Continuing past unexpected failures
- Batches larger than 3 tasks without checkpoint
- Guessing when instructions are unclear
- Not updating TodoWrite progress
