---
name: implementing-specs
description: Orchestrates specification implementation through planning, execution, verification, and PR publication phases with session recovery. Use when implementing specifications requiring phased workflow and resumable progress tracking.
disable-model-invocation: true
---

# Implementing Specs

## Purpose

Orchestrates specification implementation by invoking existing wrangler skills (writing-plans, implementing-issue) rather than reimplementing their logic. Focuses on workflow coordination, subagent dispatch, and compliance verification.

## When to Use

- Implementing specifications (SPEC-XXXXXX files)
- User-facing features requiring verification gates
- Need systematic audit trail through GitHub PR
- Want to leverage existing planning and implementation skills

## Prerequisites

- Specification file exists in `.wrangler/specifications/`
- `gh` CLI installed and authenticated
- Git worktree configured (session_start will create it)
- Bash 4.0+ (for scripts)
- `jq` command-line JSON processor

## Architecture: Skill Orchestration

This skill orchestrates existing wrangler skills rather than reimplementing their logic:

**Phase 1 (INIT)**: Uses `session_start` MCP tool (session tools)
**Phase 2 (PLAN)**: Invokes `writing-plans` skill to create MCP issues
**Phase 3 (REVIEW)**: Validates planning coverage before execution
**Phase 4 (EXECUTE)**: Dispatches subagents per issue following `implementing-issue` skill
**Phase 5 (VERIFY)**: LLM-based compliance audit
**Phase 6 (PUBLISH)**: GitHub PR finalization

**Benefits of this approach:**

- No duplicated planning logic (writing-plans is source of truth)
- Direct coordination of subagents for each issue
- Modular and maintainable (changes to planning flow in one place)
- Testable (each skill can be tested independently)

## Workflow Phases

```
INIT → PLAN → REVIEW → EXECUTE → VERIFY → PUBLISH → COMPLETE
```

---

## Phase 1: INIT

Initialize session, create worktree, and establish context.

### Objective

Create isolated worktree using MCP session tools and verify environment.

### Actions

1. **Start session** - Call `session_start` MCP tool

   ```
   session_start(specFile: "{SPEC_FILE}")
   ```

   Capture response:
   - `SESSION_ID` = response.sessionId
   - `WORKTREE_ABSOLUTE` = response.worktreePath
   - `BRANCH_NAME` = response.branchName
   - `AUDIT_PATH` = response.auditPath

2. **Verify worktree** - Ensure on correct branch

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

### Quality Gate

Worktree must exist and be on correct branch.

---

## Phase 2: PLAN

Create implementation plan using writing-plans skill.

### Objective

Break specification into implementable tasks tracked as MCP issues.

### Actions

1. **Log phase start**

   ```
   session_phase(sessionId: SESSION_ID, phase: "plan", status: "started")
   ```

2. **Invoke writing-plans skill on worktree**

   Use Task tool to dispatch planning subagent:

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

   1. Read the specification file completely
   2. Invoke the writing-plans skill to break it down into tasks
   3. The writing-plans skill will:
      - Create MCP issues for each task (issues_create)
      - Optionally create plan file if architecture context needed
      - Return list of issue IDs created
   4. Return to me:
      - Total task count
      - List of issue IDs created (e.g., ["ISS-000042", "ISS-000043"])
      - Any blockers or clarification needed

   IMPORTANT: Let writing-plans handle all planning logic. Your job
   is to invoke it and report back the results.
   ```

3. **Capture issue IDs**

   Parse planning subagent response for:
   - `ISSUE_IDS` = list of created issue IDs
   - `TASK_COUNT` = number of tasks created

4. **Create GitHub PR with overview (not full plan)**

   ```bash
   cd "{WORKTREE_ABSOLUTE}" && \
   gh pr create \
     --title "feat: {SPEC_TITLE}" \
     --body "Implements {SPEC_FILE}. See .wrangler/issues/ for task details." \
     --draft \
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
     phase: "plan",
     status: "complete",
     metadata: {
       issues_created: ISSUE_IDS,
       total_tasks: TASK_COUNT,
       pr_url: PR_URL,
       pr_number: PR_NUMBER
     }
   )
   ```

6. **Save checkpoint**
   ```
   session_checkpoint(
     sessionId: SESSION_ID,
     tasksCompleted: [],
     tasksPending: ISSUE_IDS,
     lastAction: "Created implementation plan with {TASK_COUNT} tasks",
     resumeInstructions: "Continue with execute phase, issues: {ISSUE_IDS}"
   )
   ```

### Outputs

- Wrangler issues created (ISS-XXXXXX files in .wrangler/issues/)
- Local plan file (if writing-plans created it for architecture context)
- GitHub PR created (draft mode)
- Issue IDs list for execution phase

### Quality Gate

Planning succeeds and issues are created. If planning fails or returns blockers, ESCALATE to user.

### Key Design Decision

**Why GitHub PR shows overview, not full plan:**

- PR is for stakeholders/reviewers (high-level context)
- MCP issues are source of truth (complete implementation details)
- Optional plan file (if created) provides architecture reference
- This keeps PR descriptions concise while maintaining full traceability

---

## Phase 3: REVIEW

Validate planning completeness BEFORE execution starts.

### Objective

Catch planning gaps early before wasting time on execution.

### Actions

1. **Log phase start**

   ```
   session_phase(sessionId: SESSION_ID, phase: "review", status: "started")
   ```

2. **Read plan file coverage analysis** (if plan file was created)

   Read `.wrangler/plans/YYYY-MM-DD-PLAN_<spec>.md` and extract:
   - "Acceptance Criteria Coverage" section
   - Coverage summary (% covered)
   - List of AC with no implementing tasks

3. **Validate coverage**

   | Coverage | Status                             |
   | -------- | ---------------------------------- |
   | >= 95%   | ✅ PASS (automatic approval)       |
   | < 95%    | ⚠️ NEEDS ATTENTION (user decision) |

4. **If coverage < 95%:**

   Present coverage report to user:

   ```markdown
   REVIEW Phase: Planning Coverage Gap Detected

   Coverage: X% (Y/Z acceptance criteria covered)

   Missing AC:

   - AC-XXX: [description]
   - AC-YYY: [description]
     ...

   Options:
   a) Auto-create missing tasks (Recommended)
   b) Proceed anyway (risks VERIFY failure)
   c) Abort and replan from scratch

   Your decision?
   ```

5. **If auto-create chosen:**

   For each uncovered AC:
   - Create MCP issue with implementation details
   - Add `satisfiesAcceptanceCriteria: ["AC-XXX"]` metadata
   - Add to ISSUE_IDS list

   Update plan file with new tasks and re-calculate coverage.

6. **Update session checkpoint**

   ```
   session_checkpoint(
     sessionId: SESSION_ID,
     tasksCompleted: [],
     tasksPending: ISSUE_IDS, // updated list
     lastAction: "REVIEW phase complete, coverage: X%",
     resumeInstructions: "Continue with execute phase"
   )
   ```

7. **Log phase complete**
   ```
   session_phase(
     sessionId: SESSION_ID,
     phase: "review",
     status: "complete",
     metadata: {
       coverage_percentage: X,
       supplemental_tasks_created: N
     }
   )
   ```

### Outputs

- Validated plan with >= 95% AC coverage (or user approval to proceed)
- Updated ISSUE_IDS list (if supplemental tasks created)
- Session checkpoint with review results

### Quality Gate

**Advisory gate** - offers to fix gaps, doesn't block arbitrarily:

- Coverage >= 95%: Automatic PASS → EXECUTE
- Coverage < 95%: User decision required → EXECUTE or ABORT

### Skip Condition

If spec has no explicit acceptance criteria section:

- Skip REVIEW phase
- Proceed directly to EXECUTE
- Log warning: "Skipping REVIEW (no AC in spec)"

---

## Phase 4: EXECUTE

Implement all tasks by dispatching subagents for each issue.

### Objective

Execute all implementation tasks with TDD and code review, coordinated directly by this orchestrator.

### Actions

1. **Log phase start**

   ```
   session_phase(sessionId: SESSION_ID, phase: "execute", status: "started")
   ```

2. **Execution loop** - For each issue in ISSUE_IDS:

   **a) Mark issue in progress**

   ```
   issues_update(id: ISSUE_ID, status: "in_progress")
   ```

   **b) Dispatch implementation subagent**

   Use Task tool to dispatch a subagent that follows the `implementing-issue` skill:

   ````markdown
   Tool: Task
   Description: "Implement {ISSUE_ID}: {issue_title}"
   Prompt: |
   You are implementing a single issue.

   ## Working Directory Context

   **Working directory:** {WORKTREE_ABSOLUTE}
   **Branch:** {BRANCH_NAME}

   ### MANDATORY: Verify Location First

   Before any work, run:

   ```bash
   cd {WORKTREE_ABSOLUTE} && \
     echo "Directory: $(pwd)" && \
     echo "Branch: $(git branch --show-current)" && \
     test "$(pwd)" = "{WORKTREE_ABSOLUTE}" && echo "VERIFIED" || echo "FAILED - STOP"
   ```
   ````

   ALL bash commands MUST use: `cd {WORKTREE_ABSOLUTE} && [command]`

   ## Issue

   {ISSUE_ID}: {issue_title}

   Read the full issue with: issues_get(id: "{ISSUE_ID}")

   ## Your Job

   Follow the implementing-issue skill:
   1. Read the issue and understand requirements
   2. Follow TDD (practicing-tdd skill) - write failing test, implement, refactor
   3. Request code review (requesting-code-review skill)
   4. Fix any Critical/Important issues (2 attempts each)
   5. Verify all tests pass
   6. Commit your work
   7. Report back:
      - Implementation summary
      - Test results (all passing)
      - TDD Compliance Certification
      - Commit hash
      - Any blockers encountered

   If requirements are unclear, STOP and report the blocker.

   ```

   **c) Verify subagent response**

   Check for:
   - Location verification passed (VERIFIED)
   - Implementation summary provided
   - All tests passing
   - TDD Compliance Certification
   - Work committed

   **d) Handle blockers**

   If subagent reports a blocker:
   - Unclear requirements: ESCALATE to user immediately
   - Failed after 2 fix attempts: ESCALATE to user
   - Git conflicts: ESCALATE to user
   - Missing dependencies: Try to resolve, escalate if cannot

   **e) Save checkpoint**
   ```

   session_checkpoint(
   sessionId: SESSION_ID,
   tasksCompleted: [...completed_ids],
   tasksPending: [...remaining_ids],
   lastAction: "Completed {ISSUE_ID}: {issue_title}",
   resumeInstructions: "Continue with next issue or proceed to VERIFY if all done"
   )

   ```

   **f) Mark issue complete**
   ```

   issues_mark_complete(id: ISSUE_ID)

   ```

   ```

3. **Log phase complete**
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

### Outputs

- All issues implemented with TDD
- Code reviewed for each issue
- Checkpoints saved after each issue
- PR description updated with progress

### Quality Gate

All issues complete. If any issue cannot be completed, escalate to user with blocker details and pause session.

---

## Phase 5: VERIFY

Run compliance audit using LLM-based verification.

### Objective

Verify all acceptance criteria met using intelligent extraction (not brittle scripts).

### Actions

1. **Log phase start**

   ```
   session_phase(sessionId: SESSION_ID, phase: "verify", status: "started")
   ```

2. **Extract acceptance criteria from spec (LLM-based)**

   Read specification and use LLM to extract:
   - All acceptance criteria (AC-001, AC-002, etc.)
   - E2E test requirements
   - Manual testing checklist items

   **Why LLM not script:**
   - Handles varied spec formats gracefully
   - Can infer criteria from prose descriptions
   - Won't break if spec structure differs slightly
   - More intelligent than regex parsing

3. **Verify each criterion has evidence**

   For each acceptance criterion:
   - Search for corresponding test
   - Search for implementing code
   - Search for relevant commits
   - Calculate compliance percentage

4. **Run fresh test suite**

   ```bash
   cd "{WORKTREE_ABSOLUTE}" && npm test 2>&1 | tee ".wrangler/sessions/{SESSION_ID}/final-test-output.txt"
   ```

   Capture:
   - `TEST_EXIT_CODE` = exit code
   - `TESTS_TOTAL` = total test count
   - `TESTS_PASSED` = passing test count

5. **Check git status**

   ```bash
   cd "{WORKTREE_ABSOLUTE}" && git status --short
   ```

   Capture:
   - `GIT_CLEAN` = true if output is empty

6. **Calculate compliance percentage**

   ```
   COMPLIANCE = (criteria_met / total_criteria) * 100
   ```

7. **Log phase complete**
   ```
   session_phase(
     sessionId: SESSION_ID,
     phase: "verify",
     status: "complete",
     metadata: {
       compliance_percentage: COMPLIANCE,
       tests_exit_code: TEST_EXIT_CODE,
       tests_total: TESTS_TOTAL,
       tests_passed: TESTS_PASSED,
       git_clean: GIT_CLEAN
     }
   )
   ```

### Outputs

- Compliance report (X% complete)
- Test results (all passing or failures documented)
- Git status (clean or uncommitted changes documented)

### Quality Gate & Self-Healing

**Goal**: Achieve >= 95% compliance through autonomous remediation.

**Self-Healing Workflow**:

1. **Initial Compliance Audit**
   - Run compliance check
   - Calculate compliance percentage
   - Categorize gaps

2. **Gap Categorization**

   For each unmet acceptance criterion, classify:
   - **AUTO_FIX_TEST**: Missing test coverage
   - **AUTO_FIX_DOC**: Missing documentation
   - **AUTO_FIX_EDGE**: Missing edge case handling
   - **SEARCH_RETRY**: Evidence likely exists but not found
   - **FUNDAMENTAL_GAP**: Core requirement not implemented (planning failure)

3. **Autonomous Remediation** (max 3 iterations)

   For AUTO*FIX*\* gaps:
   - Create supplemental MCP issue with specific requirement
   - Execute using implementing-issue skill
   - Commit changes
   - Re-run compliance audit
   - Loop until compliance >= 95% OR 3 iterations reached OR no more auto-fixable gaps

   Log each remediation iteration:

   ```
   session_phase(
     sessionId: SESSION_ID,
     phase: "verify-remediation",
     status: "started",
     metadata: {
       iteration: N,
       gaps_to_fix: GAP_COUNT,
       gap_types: ["AUTO_FIX_TEST", ...]
     }
   )
   ```

4. **Quality Gate Decision**

   | Compliance | Behavior                                                              |
   | ---------- | --------------------------------------------------------------------- |
   | **>= 95%** | ✅ PASS → Document any gaps-fixed in PR, proceed to PUBLISH           |
   | **90-94%** | ⚠️ PASS WITH WARNINGS → Document minor gaps in PR, proceed to PUBLISH |
   | **< 90%**  | ❌ FAIL → Escalate to user with detailed gap analysis                 |

5. **Escalation Format** (if < 90%)

   ```markdown
   VERIFY Phase: Compliance Below Threshold

   Current compliance: X%
   Quality gate: 90% required

   Self-healing attempted:

   - Created and executed Y supplemental tasks
   - Fixed Z auto-fixable gaps
   - Remaining gaps: W

   Gap Analysis:

   - FUNDAMENTAL_GAP: [list core requirements not implemented]
   - SEARCH_RETRY failures: [list evidence not found after retries]

   Options:

   1. Review and approve current implementation (partial delivery)
   2. Let me create additional tasks for remaining gaps
   3. Abort session and revisit planning

   Your decision?
   ```

6. **Document self-healing in PR** (if any remediation occurred)

   Append to PR body:

   ```markdown
   ### Compliance Self-Healing

   During verification, the following gaps were auto-fixed:

   - Created ISS-XXXXX: Added missing test for feature X
   - Created ISS-XXXXX: Added documentation for API Y
   - Created ISS-XXXXX: Added edge case handling for Z

   Final compliance: 96%
   ```

**Critical Rules**:

- NEVER escalate for missing tests/docs/edge cases - auto-fix them
- ONLY escalate for fundamental requirement gaps or after self-healing exhaustion
- Document all self-healing activity in PR description

**Also block if:**

- `TEST_EXIT_CODE != 0` - tests failing (cannot proceed)
- `GIT_CLEAN == false` - uncommitted changes (cannot proceed)

---

## Phase 6: PUBLISH

Finalize PR and mark ready for review.

### Objective

Update PR with final summary and mark ready for merge.

### Actions

1. **Log phase start**

   ```
   session_phase(sessionId: SESSION_ID, phase: "publish", status: "started")
   ```

2. **Generate final PR description**

   Create comprehensive PR body from audit data:

   ```markdown
   ## Summary
   ```

## References

For detailed information, see:

- `references/detailed-guide.md` - Complete workflow details, examples, and troubleshooting
