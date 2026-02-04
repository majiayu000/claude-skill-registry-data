---
name: tdd-execution
description: This skill should be used when executing plan tasks autonomously, implementing features using TDD, running the red-green-refactor cycle, handling code review loops, or dealing with blocked tasks. Provides the autonomous TDD execution workflow.
version: 0.1.0
---

# TDD Execution

Workflow for executing plan tasks autonomously using Test-Driven Development, with code review gates and root cause analysis for failures.

## Core Principles

**Test-First:**
Write the failing test before any implementation. The test defines what "done" looks like.

**Atomic Tasks:**
Each task = one test file = one commit. Keep changes small and reviewable.

**Evidence-Based:**
Never guess at failures. Use root-cause-analysis before declaring anything blocked.

**Continuous Progress:**
Update the plan file after each task. Progress survives session interruption.

## Execution Loop

```
┌─────────────────────────────────────────────────────────┐
│                  VERIFICATION SWEEP                      │
│              (establish ground truth)                    │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  SELECT NEXT TASK                        │
│           (first pending task by number)                 │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   RED PHASE                              │
│         Write failing test from Gherkin                  │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  GREEN PHASE                             │
│      Implement minimum code to pass test                 │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  CODE REVIEW                             │
│            Loop until approved                           │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    COMMIT                                │
│          Conventional commit message                     │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  UPDATE PLAN                             │
│          Status: pending → complete                      │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
                   More pending? ──yes──► SELECT NEXT TASK
                          │
                         no
                          │
                          ▼
                       DONE
```

## Red Phase: Write Failing Test

### Purpose

Define the expected behavior before writing any implementation. The test is the specification.

### Process

1. Read the task description and related Gherkin scenarios
2. Determine test file location from verification command
3. Write test that captures the Gherkin behavior
4. Run verification command to confirm test fails

### Test Quality Criteria

**Good tests:**
- Title describes outcome, not implementation
- Test validates the Gherkin scenario
- Could replace implementation without changing test
- Single responsibility per test

**From Gherkin to test:**

Gherkin:
```gherkin
Scenario: Successful registration with valid email
  Given I am a new user
  When I register with email "user@example.com" and password "SecurePass123"
  Then my account should be created
  And I should receive a confirmation message
```

Test:
```typescript
describe('User Registration', () => {
  it('should create account and return confirmation for valid registration', async () => {
    // Given: new user (no setup needed)

    // When: register with valid credentials
    const result = await register({
      email: 'user@example.com',
      password: 'SecurePass123'
    });

    // Then: account created and confirmation returned
    expect(result.success).toBe(true);
    expect(result.message).toContain('confirmation');
  });
});
```

### Unexpected Pass

If the test passes immediately:
- The task might already be done
- Run verification sweep to confirm
- If truly complete, update status and move on

## Green Phase: Implement

### Purpose

Write the minimum code necessary to make the test pass.

### Process

1. Implement just enough to satisfy the test
2. Run verification command after each change
3. Continue until test passes

### Implementation Guidelines

**Minimum viable implementation:**
- Don't add features not tested
- Don't optimize prematurely
- Don't refactor during green phase

**Stuck after 3-5 attempts:**
- Stop trying random fixes
- Invoke root-cause-analysis
- Address actual root cause

## Code Review

### Purpose

Ensure implementation quality before committing. Fresh perspective catches issues.

### Process

Launch code-reviewer subagent:

```typescript
Task({
  subagent_type: "pr-review-toolkit:code-reviewer",
  description: "Review task implementation",
  prompt: `Review the implementation:

Task: <task description>
Gherkin: <related scenarios>

Check:
- Does implementation satisfy Gherkin scenarios?
- Code quality and best practices
- Security considerations
- Test quality

Files changed: <list>

Respond: APPROVED or NEEDS_CHANGES with specifics.`
})
```

### Review Loop

If NEEDS_CHANGES:
1. Address feedback
2. Verify tests still pass
3. Request another review
4. Maximum 3 iterations

If still not approved after 3 iterations:
- Investigate with root-cause-analysis
- Identify fundamental issue
- Mark blocked if necessary

## Commit

### Purpose

Create atomic, reviewable commits with clear history.

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

Task: <number> - <description>
```

**Type selection:**
- `feat` - New functionality
- `fix` - Bug fix
- `refactor` - Code improvement
- `test` - Test changes only
- `docs` - Documentation

**Example:**
```
feat(auth): add user registration endpoint

Implement registration with email validation and password hashing.
Returns confirmation message on successful account creation.

Task: 2 - Add registration endpoint
```

### Commit Process

```bash
git add -A
git commit -m "<message>"
```

One task = one commit. No batching.

## Update Plan

### Purpose

Reflect actual completion status in the plan file.

### Process

After successful commit, update the task status:

Find:
```markdown
**Status**: pending
```

Replace:
```markdown
**Status**: complete
```

This ensures:
- Progress survives session interruption
- Next session knows what's done
- Plan file is always accurate

## Handling Failures

### Test Won't Pass

After 3-5 implementation attempts:

1. **Stop trying random fixes**
2. **Invoke root-cause-analysis:**
```typescript
Task({
  subagent_type: "root-cause-analysis:root-cause-analyzer",
  prompt: `Analyze failure:

Error: <what's failing>
Attempts: <what was tried>

Use five-whys methodology.
Identify actual root cause.`
})
```
3. **Apply fix based on root cause**
4. **If still failing, mark blocked:**
```markdown
**Status**: blocked
**Root Cause**: <identified root cause>
```

### Code Review Loop Won't Converge

After 3 review iterations:

1. **Invoke root-cause-analysis** on the review feedback
2. **Identify why fixes aren't addressing core issue**
3. **Either:** Apply targeted fix **or** mark blocked

### Environment Issues

If tests fail due to environment:
- Document the issue
- Report to user
- Do not mark task as blocked for environment issues
- Environment issues need human intervention

## Session Interruption

If work is interrupted:

**Plan file reflects accurate state:**
- Completed tasks marked complete
- Current task stays pending
- No partial commits

**Next session:**
1. Run verification sweep
2. Continue from first pending task
3. No duplicate work

## Progress Tracking

Use TodoWrite for real-time progress:

```typescript
TodoWrite({
  todos: [
    { content: "Task 1: Create user model", status: "completed" },
    { content: "Task 2: Add registration endpoint", status: "in_progress" },
    { content: "Task 3: Add login endpoint", status: "pending" }
  ]
})
```

Update after each task completion.

## Completion

When all tasks complete:

```
## Work Complete

**Plan**: <filename>
**Tasks**: X/X complete
**Commits**: N commits

All tasks verified and complete.
Feature ready for final review.
```

When blocked:

```
## Work Blocked

**Plan**: <filename>
**Progress**: X/Y complete
**Blocked on**: Task N

Root Cause: <explanation>

Human intervention required.
```
