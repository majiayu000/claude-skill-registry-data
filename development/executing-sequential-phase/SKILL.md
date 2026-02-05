---
name: executing-sequential-phase
description: Use when orchestrating sequential phases in plan execution - executes tasks one-by-one in main worktree using git-spice natural stacking (NO manual upstack commands, NO worktree creation, tasks build on each other)
---

# Executing Sequential Phase

## Overview

**Sequential phases use natural git-spice stacking in the main worktree.**

Each task creates a branch with `gs branch create`, which automatically stacks on the current HEAD. No manual stacking operations needed.

**Critical distinction:** Sequential tasks BUILD ON each other. They need integration, not isolation.

## When to Use

Use this skill when `execute` command encounters a phase marked "Sequential" in plan.md:
- ✅ Tasks must run in order (dependencies)
- ✅ Execute in existing `{runid}-main` worktree
- ✅ Trust natural stacking (no manual `gs upstack onto`)
- ✅ Stay on task branches (don't switch to base between tasks)

**Sequential phases never use worktrees.** They share one workspace where tasks build cumulatively.

## The Natural Stacking Principle

```
SEQUENTIAL PHASE = MAIN WORKTREE + NATURAL STACKING
```

**What natural stacking means:**
1. Start on base branch (or previous task's branch)
2. Create new branch with `gs branch create` → automatically stacks on current
3. Stay on that branch when done
4. Next task creates from there → automatically stacks on previous

**No manual commands needed.** The workflow IS the stacking.

## The Process

**Announce:** "I'm using executing-sequential-phase to execute {N} tasks sequentially in Phase {phase-id}."

### Step 0: Verify Orchestrator Location

**MANDATORY: Verify orchestrator is in main repo root before any operations:**

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
CURRENT=$(pwd)

if [ "$CURRENT" != "$REPO_ROOT" ]; then
  echo "❌ Error: Orchestrator must run from main repo root"
  echo "Current: $CURRENT"
  echo "Expected: $REPO_ROOT"
  echo ""
  echo "Return to main repo: cd $REPO_ROOT"
  exit 1
fi

echo "✅ Orchestrator location verified: Main repo root"
```

**Why critical:**
- Orchestrator delegates work but never changes directory
- All operations use `git -C .worktrees/path` or `bash -c "cd path && cmd"`
- This assertion catches upstream drift immediately

### Step 1: Verify Setup and Base Branch

**First, verify we're on the correct base branch for this phase:**

```bash
# Get current branch in main worktree
CURRENT_BRANCH=$(git -C .worktrees/{runid}-main branch --show-current)
EXPECTED_BASE="{expected-base-branch}"  # From plan: previous phase's last task, or {runid}-main for Phase 1

if [ "$CURRENT_BRANCH" != "$EXPECTED_BASE" ]; then
  echo "⚠️  WARNING: Phase {phase-id} starting from unexpected branch"
  echo "   Current: $CURRENT_BRANCH"
  echo "   Expected: $EXPECTED_BASE"
  echo ""
  echo "This means the previous phase ended on the wrong branch."
  echo "Possible causes:"
  echo "- Code review or quality checks switched branches"
  echo "- User manually checked out different branch"
  echo "- Resume from interrupted execution"
  echo ""
  echo "To fix:"
  echo "1. Verify previous phase completed: git log --oneline $EXPECTED_BASE"
  echo "2. Switch to correct base: cd .worktrees/{runid}-main && git checkout $EXPECTED_BASE"
  echo "3. Re-run /spectacular:execute"
  exit 1
fi

echo "✅ Phase {phase-id} starting from correct base: $CURRENT_BRANCH"
```

**Then check and install dependencies from main repo (orchestrator never cd's):**

```bash
# Check if dependencies installed in main worktree
if [ ! -d .worktrees/{runid}-main/node_modules ]; then
  echo "Installing dependencies in main worktree..."
  bash <<'EOF'
  cd .worktrees/{runid}-main
  {install-command}
  {postinstall-command}
  EOF
fi
```

**Why heredoc:** Orchestrator stays in main repo. Heredoc creates subshell that exits after commands.

**Why main worktree:** Sequential tasks were created during spec generation. All sequential phases share this worktree.

**Red flag:** "Create phase-specific worktree" - NO. Sequential = shared worktree.

### Step 1.5: Extract Phase Context (Before Dispatching)

**Before spawning subagents, extract phase boundaries from plan:**

The orchestrator already parsed the plan in execute.md Step 1. Extract:
- Current phase number and name
- Tasks in THIS phase (what TO implement)
- Tasks in LATER phases (what NOT to implement)

**Format for subagent context:**
```
PHASE CONTEXT:
- Phase {current-phase-id}/{total-phases}: {phase-name}
- This phase includes: Task {task-ids-in-this-phase}

LATER PHASES (DO NOT IMPLEMENT):
- Phase {next-phase}: {phase-name} - {task-summary}
- Phase {next+1}: {phase-name} - {task-summary}
...

If implementing work beyond this phase's tasks, STOP and report scope violation.
```

**Why critical:** Spec describes WHAT to build (entire feature). Plan describes HOW/WHEN (phase breakdown). Subagents need both to avoid scope creep.

### Step 2: Execute Tasks Sequentially

**For each task in order, spawn ONE subagent with embedded instructions:**

```
Task(Implement Task {task-id}: {task-name})

ROLE: Implement Task {task-id} in main worktree (sequential phase)

WORKTREE: .worktrees/{run-id}-main
CURRENT BRANCH: {current-branch}

TASK: {task-name}
FILES: {files-list}
ACCEPTANCE CRITERIA: {criteria}

PHASE BOUNDARIES:
===== PHASE BOUNDARIES - CRITICAL =====

Phase {current-phase-id}/{total-phases}: {phase-name}
This phase includes ONLY: Task {task-ids-in-this-phase}

DO NOT CREATE ANY FILES from later phases.

Later phases (DO NOT CREATE):
- Phase {next-phase}: {phase-name} - {task-summary}
  ❌ NO implementation files
  ❌ NO stub functions (even with TODOs)
  ❌ NO type definitions or interfaces
  ❌ NO test scaffolding or temporary code

If tempted to create ANY file from later phases, STOP.
"Not fully implemented" = violation.
"Just types/stubs/tests" = violation.
"Temporary/for testing" = violation.

==========================================

CONTEXT REFERENCES:
- Spec: specs/{run-id}-{feature-slug}/spec.md
- Constitution: docs/constitutions/current/
- Plan: specs/{run-id}-{feature-slug}/plan.md
- Worktree: .worktrees/{run-id}-main

INSTRUCTIONS:

1. Navigate to main worktree:
   cd .worktrees/{run-id}-main

2. Read constitution (if exists): docs/constitutions/current/

3. Read feature specification: specs/{run-id}-{feature-slug}/spec.md

   This provides:
   - WHAT to build (requirements, user flows)
   - WHY decisions were made (architecture rationale)
   - HOW features integrate (system boundaries)

   The spec is your source of truth for architectural decisions.
   Constitution tells you HOW to code. Spec tells you WHAT to build.

4. VERIFY PHASE SCOPE before implementing:
   - Read the PHASE BOUNDARIES section above
   - Confirm this task belongs to Phase {current-phase-id}
   - If tempted to implement later phase work, STOP
   - The plan exists for a reason - respect phase boundaries

5. Implement task following spec + constitution + phase boundaries

6. Run quality checks with exit code validation:

   **CRITICAL**: Use heredoc to prevent bash parsing errors:

   bash <<'EOF'
   npm test
   if [ $? -ne 0 ]; then
     echo "❌ Tests failed"
     exit 1
   fi

   npm run lint
   if [ $? -ne 0 ]; then
     echo "❌ Lint failed"
     exit 1
   fi

   npm run build
   if [ $? -ne 0 ]; then
     echo "❌ Build failed"
     exit 1
   fi
   EOF

   **Why heredoc**: Prevents parsing errors when commands are wrapped by orchestrator.

7. Create stacked branch using verification skill:

   Skill: phase-task-verification

   Parameters:
   - RUN_ID: {run-id}
   - TASK_ID: {phase}-{task}
   - TASK_NAME: {short-name}
   - COMMIT_MESSAGE: "[Task {phase}.{task}] {task-name}"
   - MODE: sequential

   The verification skill will:
   a) Stage changes with git add .
   b) Create branch with gs branch create
   c) Verify HEAD points to new branch
   d) Stay on branch (next task builds on it)

8. Report completion

CRITICAL:
- Work in .worktrees/{run-id}-main, NOT main repo
- Stay on your branch when done (next task builds on it)
- Do NOT create worktrees
- Do NOT use `gs upstack onto`
- Do NOT implement work from later phases (check PHASE BOUNDARIES above)
```

**Sequential dispatch:** Wait for each task to complete before starting next.

**Red flags:**
- "Dispatch all tasks in parallel" - NO. Sequential = one at a time.
- "Create task-specific worktrees" - NO. Sequential = shared worktree.
- "Spec mentions feature X, I'll implement it now" - NO. Check phase boundaries first.
- "I'll run git add myself" - NO. Let subagent use phase-task-verification skill.

### Step 3: Verify Natural Stack Formation

**After all tasks complete (verify from main repo):**

```bash
# Display and verify stack using bash subshell (orchestrator stays in main repo)
bash <<'EOF'
cd .worktrees/{runid}-main

echo "📋 Stack after sequential phase:"
gs log short
echo ""

# Verify stack integrity (each task has unique commit)
echo "🔍 Verifying stack integrity..."
TASK_BRANCHES=( {array-of-branch-names} )
STACK_VALID=1
declare -A SEEN_COMMITS

for BRANCH in "${TASK_BRANCHES[@]}"; do
  if ! git rev-parse --verify "$BRANCH" >/dev/null 2>&1; then
    echo "❌ ERROR: Branch '$BRANCH' not found"
    STACK_VALID=0
    break
  fi

  BRANCH_SHA=$(git rev-parse "$BRANCH")

  # Check if this commit SHA was already seen
  if [ -n "${SEEN_COMMITS[$BRANCH_SHA]}" ]; then
    echo "❌ ERROR: Stack integrity violation"
    echo "   Branch '$BRANCH' points to commit $BRANCH_SHA"
    echo "   But '${SEEN_COMMITS[$BRANCH_SHA]}' already points to that commit"
    echo ""
    echo "This means one task created no new commits."
    echo "Possible causes:"
    echo "- Task implementation had no changes"
    echo "- Quality checks blocked commit"
    echo "- gs branch create failed silently"
    STACK_VALID=0
    break
  fi

  SEEN_COMMITS[$BRANCH_SHA]="$BRANCH"
  echo "  ✓ $BRANCH @ $BRANCH_SHA"
done

if [ $STACK_VALID -eq 0 ]; then
  echo ""
  echo "❌ Stack verification FAILED"
  echo ""
  echo "To investigate:"
  echo "1. Check task branch commits: git log --oneline \$BRANCH"
  echo "2. Review subagent output for failed task"
  echo "3. Check for quality check failures (test/lint/build)"
  echo "4. Fix and re-run /spectacular:execute"
  exit 1
fi

echo "✅ Stack integrity verified - all tasks have unique commits"
EOF
```

**Each `gs branch create` automatically stacked on the previous task's branch.**

**Verification ensures:** Each task created a unique commit (no empty branches or duplicates).

**Red flag:** "Run `gs upstack onto` to ensure stacking" - NO. Already stacked naturally.

### Step 4: Code Review (Binary Quality Gate)

**Check review frequency setting (from execute.md Step 1.7):**

```bash
REVIEW_FREQUENCY=${REVIEW_FREQUENCY:-per-phase}
```

**If REVIEW_FREQUENCY is "end-only" or "skip":**
```
Skipping per-phase code review (frequency: {REVIEW_FREQUENCY})
Phase {N} complete - proceeding to next phase
```
Mark phase complete and continue to next phase.

**If REVIEW_FREQUENCY is "optimize":**

Analyze the completed phase to decide if code review is needed:

**High-risk indicators (REVIEW REQUIRED):**
- Schema or migration changes
- Authentication/authorization logic
- External API integrations or webhooks
- Foundation phases (Phase 1-2 establishing patterns)
- 3+ parallel tasks (coordination complexity)
- New architectural patterns introduced
- Security-sensitive code (payment, PII, access control)
- Complex business logic with multiple edge cases
- Changes affecting multiple layers (database → API → UI)

**Low-risk indicators (SKIP REVIEW):**
- Pure UI component additions (no state/logic)
- Documentation or comment updates
- Test additions without implementation changes
- Refactoring with existing test coverage
- Isolated utility functions
- Configuration file updates (non-security)

**Analyze this phase:**
- Phase number: {N}
- Tasks completed: {task-list}
- Files modified: {file-list}
- Types of changes: {describe changes}

**Decision:**
If ANY high-risk indicator present → Proceed to code review below
If ONLY low-risk indicators → Skip review:
```
✓ Phase {N} assessed as low-risk - skipping review (optimize mode)
  Reasoning: {brief explanation of why low-risk}
Phase {N} complete - proceeding to next phase
```

**If REVIEW_FREQUENCY is "per-phase" OR optimize mode decided to review:**

Use `requesting-code-review` skill, then parse results STRICTLY.

**AUTONOMOUS EXECUTION:** Code review rejections trigger automatic fix loops, NOT user prompts. Never ask user what to do.

1. **Dispatch code review:**
   ```
   Skill: requesting-code-review

   Context provided to reviewer:
   - WORKTREE: .worktrees/{runid}-main
   - PHASE: {phase-number}
   - TASKS: {task-list}
   - BASE_BRANCH: {base-branch-name}
   - SPEC: specs/{run-id}-{feature-slug}/spec.md
   - PLAN: specs/{run-id}-{feature-slug}/plan.md (for phase boundary validation)

   **CRITICAL - EXHAUSTIVE FIRST-PASS REVIEW:**

   This is your ONLY opportunity to find issues. Re-review is for verifying fixes, NOT discovering new problems.

   Check EVERYTHING in this single review:
   □ Implementation correctness - logic bugs, edge cases, error handling, race conditions
   □ Test correctness - expectations match actual behavior, coverage is complete, no false positives
   □ Cross-file consistency - logic coherent across all files, no contradictions
   □ Architectural soundness - follows patterns, proper separation of concerns, no coupling issues
   □ Scope adherence - implements ONLY Phase {phase-number} work, no later-phase implementations
   □ Constitution compliance - follows all project standards and conventions

   Find ALL issues NOW. If you catch yourself thinking "I'll check that in re-review" - STOP. Check it NOW.

   Binary verdict required: "Ready to merge? Yes" (only if EVERYTHING passes) or "Ready to merge? No" (list ALL issues found)
   ```

2. **Parse "Ready to merge?" field:**
   - **"Yes"** → APPROVED, continue to next phase
   - **"No"** or **"With fixes"** → REJECTED, dispatch fix subagent, go to step 3
   - **No output / missing field** → RETRY ONCE, if retry fails → STOP
   - **Soft language** → REJECTED, re-review required

3. **Re-review loop (if REJECTED):**
   - Track rejections (REJECTION_COUNT)
   - If count > 3: Escalate to user (architectural issues beyond subagent scope)
   - Dispatch fix subagent with:
     * Issues list (severity + file locations)
     * Context: constitution, spec, plan
     * Scope enforcement: If scope creep, implement LESS (roll back to phase scope)
     * Quality checks required
   - Re-review after fixes (return to step 1)
   - On approval: Announce completion with iteration count

**Critical:** Only "Ready to merge? Yes" allows proceeding. Everything else stops execution.

**Phase completion:**
- If `REVIEW_FREQUENCY="per-phase"`: Phase complete ONLY when code review returns "Ready to merge? Yes"
- If `REVIEW_FREQUENCY="end-only"` or `"skip"`: Phase complete after all tasks finish (code review skipped)

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "Need manual stacking commands" | `gs branch create` stacks automatically on current HEAD |
| "Files don't overlap, could parallelize" | Plan says sequential for semantic dependencies |
| "Create phase-specific worktree" | Sequential phases share main worktree |
| "Review rejected, ask user" | Autonomous execution means automatic fixes |
| "Scope creep but quality passes" | Plan violation = failure. Auto-fix to plan |

