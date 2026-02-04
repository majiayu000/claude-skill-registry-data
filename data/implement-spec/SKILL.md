---
name: implement-spec
description: Orchestrate spec-to-PR workflow with session tracking, worktree isolation, and audit trail
---

# Implement-Spec Orchestrator

## Skill Usage Announcement

**MANDATORY**: When using this skill, announce it at the start with:

```
Using Skill: implement-spec | [brief purpose based on context]
```

**Example:**
```
Using Skill: implement-spec | Implementing spec-auth-system.md with full audit trail
```

This creates an audit trail showing which skills were applied during the session.

## Overview

End-to-end orchestration that takes a specification file and produces a GitHub Pull Request with comprehensive audit trail.

**Core principle:** Single command produces PR with verified implementation, full observability, and recovery capability.

**Entry point:** `/wrangler:implement [spec-file]`

**Produces:**
- GitHub Pull Request with comprehensive summary
- Audit trail in `.wrangler/sessions/{session-id}/`
- Machine-verifiable execution log

## When to Use

**Use this skill when:**
- User says "implement this spec" and wants a PR
- You want full audit trail and observability
- You need session recovery capability
- You want isolated worktree for implementation

**Do NOT use this skill when:**
- Implementing a single issue (use `implement` skill directly)
- User wants manual control over each step
- Working on existing PR or branch (use `implement` skill)

## Workflow Phases

The orchestrator executes 6 phases in order:

```
INIT -> PLAN -> EXECUTE -> VERIFY -> PUBLISH -> REPORT
```

Each phase is tracked via MCP session tools for full observability.

## Phase 1: INIT

Initialize session, create worktree, and establish context.

### Steps

1. **Start session**

   Call `session_start` MCP tool:
   ```
   session_start(specFile: "{SPEC_FILE}")
   ```

   Capture response:
   - `SESSION_ID` = response.sessionId
   - `WORKTREE_ABSOLUTE` = response.worktreePath
   - `BRANCH_NAME` = response.branchName
   - `AUDIT_PATH` = response.auditPath

2. **Verify worktree**

   ```bash
   cd {WORKTREE_ABSOLUTE} && \
     echo "=== WORKTREE VERIFICATION ===" && \
     echo "Directory: $(pwd)" && \
     echo "Git root: $(git rev-parse --show-toplevel)" && \
     echo "Branch: $(git branch --show-current)" && \
     test "$(git branch --show-current)" = "{BRANCH_NAME}" && echo "VERIFIED" || echo "FAILED"
   ```

   **If verification fails, STOP and report error.**

3. **Log phase complete**

   ```
   session_phase(
     sessionId: SESSION_ID,
     phase: "init",
     status: "complete"
   )
   ```

### Outputs

- Session ID for all subsequent phases
- Worktree absolute path for subagent context
- Branch name for PR creation

## Phase 2: PLAN

Create implementation plan with MCP issues.

### Steps

1. **Log phase start**

   ```
   session_phase(sessionId: SESSION_ID, phase: "plan", status: "started")
   ```

2. **Invoke writing-plans skill**

   Use the Task tool to dispatch planning subagent:

   ```markdown
   Tool: Task
   Description: "Create implementation plan for {SPEC_FILE}"
   Prompt: |
     You are creating an implementation plan for a specification.

     ## Working Directory Context

     **Working directory:** {WORKTREE_ABSOLUTE}
     **Branch:** {BRANCH_NAME}
     **Session ID:** {SESSION_ID}

     ## Specification

     Read and analyze: {SPEC_FILE}

     ## Your Job

     1. Read the specification file
     2. Break down into implementable tasks
     3. Create MCP issues for each task using issues_create
     4. Return the list of issue IDs created

     Use the writing-plans skill approach:
     - Each task should be <250 LOC
     - Clear acceptance criteria per task
     - Dependencies between tasks if any

     ## Output Required

     Return:
     - Total task count
     - List of issue IDs created (e.g., ["ISS-000042", "ISS-000043"])
     - Any blockers or clarification needed
   ```

3. **Capture issue IDs**

   Parse planning subagent response for:
   - `ISSUE_IDS` = list of created issue IDs
   - `TASK_COUNT` = number of tasks created

4. **Log phase complete**

   ```
   session_phase(
     sessionId: SESSION_ID,
     phase: "plan",
     status: "complete",
     metadata: {
       issues_created: ISSUE_IDS,
       total_tasks: TASK_COUNT
     }
   )
   ```

5. **Save checkpoint**

   ```
   session_checkpoint(
     sessionId: SESSION_ID,
     tasksCompleted: [],
     tasksPending: ISSUE_IDS,
     lastAction: "Created implementation plan with {TASK_COUNT} tasks",
     resumeInstructions: "Continue with execute phase, implement issues: {ISSUE_IDS}"
   )
   ```

### Gate

If planning fails or returns blockers, ESCALATE to user.

## Phase 3: EXECUTE

Implement all tasks using subagents.

### Steps

1. **Log phase start**

   ```
   session_phase(sessionId: SESSION_ID, phase: "execute", status: "started")
   ```

2. **Invoke implement skill**

   Use the `implement` skill with worktree context:

   ```markdown
   I'm using the implement skill to execute all tasks.

   ## Context for Implement Skill

   **Scope:** issues {ISSUE_IDS}
   **Working directory:** {WORKTREE_ABSOLUTE}
   **Branch:** {BRANCH_NAME}
   **Session ID:** {SESSION_ID}

   ## CRITICAL: Worktree Context

   ALL subagents MUST receive:
   - Working directory: {WORKTREE_ABSOLUTE}
   - Branch: {BRANCH_NAME}

   ALL bash commands MUST use:
   ```bash
   cd {WORKTREE_ABSOLUTE} && [command]
   ```

   ## Checkpoint After Each Task

   After each task completes, call:
   ```
   session_checkpoint(
     sessionId: {SESSION_ID},
     tasksCompleted: [...completed_ids],
     tasksPending: [...remaining_ids],
     lastAction: "Completed task {task_id}: {task_title}",
     resumeInstructions: "Continue with next task or proceed to verify if all done"
   )
   ```
   ```

3. **Track task completion**

   For each completed task:
   - Record task audit entry via `session_phase` with phase="task"
   - Save checkpoint via `session_checkpoint`

4. **Log phase complete**

   When all tasks complete:
   ```
   session_phase(
     sessionId: SESSION_ID,
     phase: "execute",
     status: "complete",
     metadata: {
       tasks_completed: TASK_COUNT,
       total_commits: N
     }
   )
   ```

### Gate

If any task cannot be completed after escalation, session pauses.

## Phase 4: VERIFY

Fresh test run and requirements check.

### Steps

1. **Log phase start**

   ```
   session_phase(sessionId: SESSION_ID, phase: "verify", status: "started")
   ```

2. **Run fresh test suite**

   ```bash
   cd "{WORKTREE_ABSOLUTE}" && npm test 2>&1 | tee ".wrangler/sessions/{SESSION_ID}/final-test-output.txt"
   ```

   Capture:
   - `TEST_EXIT_CODE` = exit code
   - `TESTS_TOTAL` = total test count
   - `TESTS_PASSED` = passing test count

3. **Check git status**

   ```bash
   cd "{WORKTREE_ABSOLUTE}" && git status --short
   ```

   Capture:
   - `GIT_CLEAN` = true if output is empty

4. **Log phase complete**

   ```
   session_phase(
     sessionId: SESSION_ID,
     phase: "verify",
     status: "complete",
     metadata: {
       tests_exit_code: TEST_EXIT_CODE,
       tests_total: TESTS_TOTAL,
       tests_passed: TESTS_PASSED,
       git_clean: GIT_CLEAN
     }
   )
   ```

### Gate

**CRITICAL:** Do NOT proceed to publish if:
- `TEST_EXIT_CODE != 0` - tests failing
- `GIT_CLEAN == false` - uncommitted changes

If verification fails:
1. Log error and halt
2. Inform user of verification failure
3. Session remains in "paused" state for recovery

## Phase 5: PUBLISH

Push branch and create PR.

### Steps

1. **Log phase start**

   ```
   session_phase(sessionId: SESSION_ID, phase: "publish", status: "started")
   ```

2. **Push branch**

   ```bash
   cd "{WORKTREE_ABSOLUTE}" && git push -u origin "{BRANCH_NAME}"
   ```

3. **Generate PR body**

   Create comprehensive PR body from audit data:

   ```markdown
   ## Summary

   Implements specification: `{SPEC_FILE}`

   ### Changes

   {git log main..HEAD --oneline formatted as bullet list}

   ### Test Results

   - All tests passing ({TESTS_TOTAL} tests)

   ### Tasks Completed

   {For each task from session:}
   - [x] {task_id}: {task_title} ({commit_hash})

   ### Implementation Details

   - TDD compliance: All functions certified
   - Code review: All tasks approved

   ---

   **Session ID:** `{SESSION_ID}`
   **Audit trail:** `.wrangler/sessions/{SESSION_ID}/`

   Generated with [Claude Code](https://claude.com/claude-code)
   ```

4. **Create PR**

   ```bash
   cd "{WORKTREE_ABSOLUTE}" && gh pr create \
     --title "feat({SPEC_NAME}): implement specification" \
     --body "{PR_BODY}" \
     --base main \
     --head "{BRANCH_NAME}"
   ```

   Capture:
   - `PR_URL` = PR URL from output
   - `PR_NUMBER` = PR number from output

5. **Log phase complete**

   ```
   session_phase(
     sessionId: SESSION_ID,
     phase: "publish",
     status: "complete",
     metadata: {
       pr_url: PR_URL,
       pr_number: PR_NUMBER,
       branch_pushed: true
     }
   )
   ```

### Gate

If push or PR creation fails:
1. Log error
2. Inform user (may need to configure gh auth)
3. Session pauses but work is preserved

## Phase 6: REPORT

Complete session and present summary.

### Steps

1. **Complete session**

   ```
   session_complete(
     sessionId: SESSION_ID,
     status: "completed",
     prUrl: PR_URL,
     prNumber: PR_NUMBER,
     summary: "Implemented {TASK_COUNT} tasks from {SPEC_FILE}"
   )
   ```

2. **Present summary to user**

   ```markdown
   ## Implementation Complete

   **Specification:** {SPEC_FILE}
   **PR:** {PR_URL}
   **Session:** {SESSION_ID}

   ### Summary

   | Metric | Value |
   |--------|-------|
   | Tasks completed | {TASK_COUNT}/{TASK_COUNT} |
   | Tests passing | {TESTS_TOTAL} |
   | Code reviews | {TASK_COUNT} approved |

   ### Audit Trail

   Location: `.wrangler/sessions/{SESSION_ID}/`

   **Verify execution:**
   ```bash
   cat .wrangler/sessions/{SESSION_ID}/audit.jsonl | jq -s '{
     phases: [.[].phase] | unique,
     tasks: [.[] | select(.phase == "task")] | length,
     all_passed: [.[] | select(.phase == "task") | .tests_passed] | all,
     pr_created: ([.[] | select(.phase == "publish")] | length) > 0
   }'
   ```
   ```

## Session Recovery

If a session is interrupted, it can be resumed.

### Detection

On session start, check for interrupted sessions:

```
session_get()  // No sessionId = find most recent incomplete
```

If interrupted session found:
1. Read checkpoint
2. Present resume option to user
3. If user confirms, continue from last checkpoint

### Resume Flow

1. Call `session_get(sessionId: "{SESSION_ID}")`
2. Read `checkpoint.resumeInstructions`
3. Continue from indicated phase/task
4. All MCP calls use existing sessionId

## Worktree Isolation

**CRITICAL:** All subagent operations MUST use worktree context.

### Context Injection

Every subagent prompt MUST include:

```markdown
## CRITICAL: Working Directory Context

**Working directory:** {WORKTREE_ABSOLUTE}
**Branch:** {BRANCH_NAME}

### MANDATORY: Verify Location First

Before ANY work, run:
```bash
cd {WORKTREE_ABSOLUTE} && \
  echo "Directory: $(pwd)" && \
  echo "Branch: $(git branch --show-current)" && \
  test "$(pwd)" = "{WORKTREE_ABSOLUTE}" && echo "VERIFIED" || echo "FAILED"
```

**If verification fails, STOP immediately.**

### Command Pattern

ALL bash commands MUST use:
```bash
cd {WORKTREE_ABSOLUTE} && [command]
```
```

### Why This Matters

- Worktree is separate from main repository
- Without explicit context, subagents may work in wrong directory
- Commits in wrong directory corrupt main branch

## Error Handling

### Phase Failures

Each phase has verification gates:
- **INIT:** Worktree must exist and be on correct branch
- **PLAN:** Issues must be created successfully
- **EXECUTE:** All tasks must complete (with escalation for blockers)
- **VERIFY:** Tests must pass, git must be clean
- **PUBLISH:** Push and PR creation must succeed

### Recovery Actions

| Error | Recovery |
|-------|----------|
| Worktree creation fails | Check disk space, permissions |
| Planning unclear | Escalate to user for clarification |
| Task blocked | Escalate via implement skill |
| Tests fail | Do not publish, inform user |
| Push fails | Check git remote, auth |
| PR creation fails | Check gh auth, permissions |

### Session States

| State | Meaning | Recovery |
|-------|---------|----------|
| `running` | Currently executing | Continue |
| `paused` | Blocked on something | Resume from checkpoint |
| `completed` | Successfully finished | No action needed |
| `failed` | Unrecoverable error | Start new session |

## Example Execution

```
User: /wrangler:implement spec-auth-system.md

Using Skill: implement-spec | Implementing spec-auth-system.md with full audit trail

PHASE 1: INIT
-> session_start(specFile: "spec-auth-system.md")
-> Created session: 2025-12-07-abc123-f8d2
-> Worktree: /project/.worktrees/spec-auth-system
-> Branch: wrangler/spec-auth-system/2025-12-07-abc123
-> VERIFIED

PHASE 2: PLAN
-> Invoking writing-plans skill
-> Created 5 tasks: ISS-000042 through ISS-000046
-> session_checkpoint saved

PHASE 3: EXECUTE
-> Invoking implement skill with worktree context
-> Task ISS-000042: Complete (TDD certified, code reviewed)
-> session_checkpoint saved
-> Task ISS-000043: Complete
-> session_checkpoint saved
-> Task ISS-000044: Complete
-> session_checkpoint saved
-> Task ISS-000045: Complete
-> session_checkpoint saved
-> Task ISS-000046: Complete
-> session_checkpoint saved

PHASE 4: VERIFY
-> Running test suite: 42 tests, 42 passing
-> Git status: clean
-> PASSED

PHASE 5: PUBLISH
-> Pushed branch to origin
-> Created PR: https://github.com/org/repo/pull/123

PHASE 6: REPORT
-> session_complete

## Implementation Complete

**Specification:** spec-auth-system.md
**PR:** https://github.com/org/repo/pull/123
**Session:** 2025-12-07-abc123-f8d2

| Metric | Value |
|--------|-------|
| Tasks completed | 5/5 |
| Tests passing | 42 |
| Code reviews | 5 approved |

Audit trail: .wrangler/sessions/2025-12-07-abc123-f8d2/
```

## Integration with Other Skills

**Required skills:**
- `implement` - Task execution with TDD and code review
- `writing-plans` - Breaking spec into MCP issues
- `test-driven-development` - TDD compliance in subagents
- `requesting-code-review` - Code review for each task

**Optional skills:**
- `using-git-worktrees` - Manual worktree management (automated here)
- `finishing-a-development-branch` - PR already created by this skill

## Verification Commands

After completion, verify execution:

```bash
# Verify all phases completed
jq -s '[.[].phase] | unique | sort' .wrangler/sessions/{id}/audit.jsonl
# Expected: ["checkpoint","complete","execute","init","plan","publish","task","verify"]

# Verify all tasks passed
jq -s '[.[] | select(.phase == "task" and .tests_passed == false)]' audit.jsonl
# Expected: []

# Verify PR created
jq -s '.[] | select(.phase == "publish") | .pr_url' audit.jsonl
# Expected: "https://github.com/..."

# Get session summary
jq -s '{
  session_id: .[0].session_id,
  phases: [.[].phase] | unique,
  tasks: [.[] | select(.phase == "task")] | length,
  duration_sec: ((.[length-1].timestamp | fromdateiso8601) - (.[0].timestamp | fromdateiso8601))
}' audit.jsonl
```

## Red Flags - Anti-Patterns

**Do NOT:**

- Skip worktree verification (subagents may work in wrong directory)
- Proceed to publish with failing tests
- Create PR without complete audit trail
- Skip checkpoints (recovery becomes impossible)
- Ignore phase gates

**Do:**

- Always verify worktree location
- Save checkpoint after each task
- Use session tools for all phase transitions
- Halt on verification failures
- Provide comprehensive PR body
