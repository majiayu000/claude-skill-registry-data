---
name: verification-sweep
description: This skill should be used when checking plan status, running verification commands, updating task statuses, or determining what work remains. Provides the verification sweep algorithm and status update procedures.
version: 0.1.0
---

# Verification Sweep

Algorithm for verifying task completion by running verification commands and updating plan status.

## Purpose

Verification sweep establishes ground truth about task completion:
- Run verification commands to prove tasks are done
- Update plan file with accurate statuses
- Detect regressions in previously complete tasks
- Report what work remains

## When to Use

Perform verification sweep:
- At the start of `/tommymorgan:work` (before doing any work)
- When running `/tommymorgan:status`
- After returning from a break or new session
- Before reporting completion status

## Algorithm

### Step 1: Load Plan File

Read the plan file and extract all tasks:

```
For each line matching "### \d+\. ":
  - task_number = extracted number
  - task_description = text after number
  - verify_command = content of next **Verify**: `...`
  - current_status = value after **Status**:
```

### Step 2: Run Verification Commands

For each task, execute its verification command:

```bash
<verify_command>
echo "Exit code: $?"
```

Capture:
- Exit code (0 = success)
- Stdout/stderr (for debugging)

### Step 3: Determine New Status

Apply status transition rules:

| Current Status | Exit Code | New Status | Action |
|----------------|-----------|------------|--------|
| pending | 0 | complete | Update plan |
| pending | non-zero | pending | No change |
| complete | 0 | complete | No change |
| complete | non-zero | complete | Warn: regression |
| blocked | 0 | complete | Update plan, clear block |
| blocked | non-zero | blocked | No change |

**Regression handling:**
If a previously complete task now fails, warn but do not change status:
```
WARNING: Regression detected in task N: <description>
Verification command failed but task marked complete.
Investigate before continuing.
```

### Step 4: Update Plan File

For each status change, update the plan file:

Find:
```markdown
**Status**: pending
```

Replace with:
```markdown
**Status**: complete
```

Use precise edits - only change the status value, preserve everything else.

### Step 5: Generate Report

After verification sweep, report results:

```
## Verification Sweep: <plan filename>

**Run at**: <timestamp>
**Progress**: X/Y tasks complete

### Results
- Task 1: <description> - PASS (complete)
- Task 2: <description> - PASS (complete)
- Task 3: <description> - FAIL (pending)
- Task 4: <description> - SKIP (blocked)

### Summary
- Complete: X
- Pending: Y
- Blocked: Z
- Regressions: N

**Next task**: <first pending task description>
```

## Verification Command Best Practices

**Good verification commands:**
```bash
# Run specific test file
pnpm test src/models/user.test.ts

# Run test with specific pattern
pytest -k test_user_registration

# Check file exists with content
grep -q "export class User" src/models/user.ts

# Verify build succeeds
pnpm build && test -f dist/index.js
```

**Bad verification commands:**
```bash
# Too broad - might pass for wrong reasons
pnpm test

# Non-deterministic
curl http://localhost:3000/health

# Requires manual inspection
cat src/models/user.ts
```

## Handling Edge Cases

### Missing Verification Command

If a task lacks a verification command:
```
ERROR: Task N has no verification command.
Cannot determine completion status.
```
Mark as pending and flag for human attention.

### Verification Command Timeout

Set reasonable timeout (30 seconds default):
```bash
timeout 30 <verify_command>
```

If timeout:
- Treat as failure
- Log timeout warning
- Consider if command is appropriate

### Environment Dependencies

Before running verification commands:
- Ensure test environment is ready
- Check required services are running
- Verify dependencies are installed

If environment issue detected, report clearly:
```
ERROR: Verification environment not ready.
Missing: <dependency>
Run: <setup command>
```

## Status Transitions

```
                    ┌─────────────┐
        ┌──────────►│   pending   │◄──────────┐
        │           └──────┬──────┘           │
        │                  │                  │
   (verify fails)    (verify passes)    (unblock)
        │                  │                  │
        │           ┌──────▼──────┐           │
        └───────────│  complete   │───────────┘
                    └──────┬──────┘      │
                           │             │
                    (manual block)       │
                           │             │
                    ┌──────▼──────┐      │
                    │   blocked   ├──────┘
                    └─────────────┘
```

**Transitions:**
- `pending` → `complete`: Verification passes
- `pending` → `blocked`: Manual intervention (with root cause)
- `complete` → `blocked`: Manual intervention (regression)
- `blocked` → `complete`: Verification passes after unblock
- `blocked` → `pending`: Manual unblock

## Integration with Commands

### /tommymorgan:status

Runs verification sweep and reports results. Does not perform any work.

### /tommymorgan:work

Runs verification sweep first, then works on pending tasks:
1. Verification sweep
2. If all complete → done
3. If blocked and no pending → report and stop
4. If pending → work on next task
5. After each task completion → mini-sweep (verify just that task)

## Troubleshooting

**All tasks show as pending:**
- Check verification commands are correct
- Ensure test files exist
- Verify test runner is configured

**Complete tasks regressing:**
- Check for test pollution between runs
- Verify test isolation
- Look for environment-dependent tests

**Verification commands hang:**
- Add timeout handling
- Check for interactive prompts
- Ensure commands are non-blocking
