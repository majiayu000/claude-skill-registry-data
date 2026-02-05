---
name: linter-driven-development
description: |
  Orchestrates complete autopilot workflow: design → test → lint → refactor → review → commit.
  AUTO-INVOKES when user wants to implement code: "implement", "ready", "execute", "continue",
  "do step X", "next task", "let's go", "start coding". Runs automatically through all phases
  until commit-ready. Uses parallel linter+review analysis and intelligent combined reports.
  For: features, bug fixes, refactors. Requires: Go project (go.mod).
---

# Linter-Driven Development Workflow

META ORCHESTRATOR for implementation workflow: design → test → lint → refactor → review → commit.
Use for any commit: features, bug fixes, refactors.

## When to Use
- Implementing any code change that should result in a commit
- Need automatic workflow management with quality gates
- Want to ensure: clean code + tests + linting + design validation

## Pre-Flight Check (ALWAYS RUN FIRST)

Before starting the autopilot workflow, verify all conditions are met:

### 1. Confirm Implementation Intent
Look for keywords indicating the user wants to implement code:
- **Direct keywords**: "implement", "ready", "execute", "do", "start", "continue", "next", "build", "create"
- **Step references**: "step 1", "task 2", "next task", "do step X"
- **Explicit invocation**: "@linter-driven-development"

### 2. Verify Go Project
Check that `go.mod` exists in the project root or parent directories.

### 3. Find Project Commands
Discover test and lint commands by reading project documentation:

**Search locations** (in order):
1. Project docs: `README.md`, `CLAUDE.md`, `agents.md`
2. Build configs: `Makefile`, `Taskfile.yaml`, `.golangci.yaml`
3. Git repository root for workspace-level commands

**Extract commands**:
- **Test command**: Look for `go test`, `make test`, `task test`, or similar
- **Lint command**: Look for `golangci-lint run --fix`, `make lint`, `task lintwithfix`, or similar
- **Prefer**: Commands with autofix capability (e.g., `--fix` flag)

**Fallback defaults** (if not found in docs):
- Tests: `go test ./...`
- Linter: `golangci-lint run --fix`

**If fallbacks don't work**:
- Ask user: "What commands should I use for testing and linting?"
- Document discovered commands in project docs for future runs

**Store discovered commands** for use throughout the workflow.

### 4. Identify Plan Context
Scan conversation history (last 50 messages) for:
- Step-by-step implementation plan
- Which step the user wants to implement
- Any design decisions or architectural context

### 5. Decision Tree

✅ **All conditions met → AUTOPILOT ENGAGED**
- Announce: "Engaging autopilot mode for [feature/step description]"
- Proceed directly to Phase 1

❓ **Unclear intent or missing context → ASK FOR CONFIRMATION**
- "I detected you want to implement something. Should I start the autopilot workflow?"
- Clarify which step to implement if multiple options exist

❌ **No plan found → SUGGEST CREATING PLAN FIRST**
- "I don't see an implementation plan. Would you like me to help create one first?"
- Offer to use @code-designing skill for design planning

❌ **Not a Go project → EXPLAIN LIMITATION**
- "This skill requires a Go project with go.mod. Current project doesn't appear to be Go."

## Workflow Phases

### Phase 1: Implementation Foundation

**Design Architecture** (if new types/functions needed):
- Invoke @code-designing skill
- Output: Type design plan with self-validating domain types
- When in plan mode, invoke with plan mode flag

**Write Tests First**:
- Invoke @testing skill for guidance
- Write table-driven tests or testify suites
- Target: 100% coverage on new leaf types

**Implement Code**:
- Follow coding principles from coding_rules.md
- Keep functions <50 LOC, max 2 nesting levels
- Use self-validating types, prevent primitive obsession
- Apply storifying pattern for readable top-level functions

### Phase 2: Quality Analysis (Agent is the Gate)

**Invoke quality-analyzer agent** for parallel quality analysis:

```
Task(subagent_type: "quality-analyzer")

Prompt:
"Analyze code quality for this Go project.

Mode: full

Project commands:
- Test: [PROJECT_TEST_COMMAND from Pre-Flight Check]
- Lint: [PROJECT_LINT_COMMAND from Pre-Flight Check]

Files to analyze:
[list files from: git diff --name-only main...HEAD | grep '\.go$']

Run all quality gates in parallel and return combined analysis."
```

**The quality-analyzer agent automatically**:
- Executes tests, linter, and code review in parallel (40-50% faster)
- Normalizes outputs into common format
- Identifies overlapping issues (same file:line from multiple sources)
- Performs root cause analysis (why multiple issues occur together)
- Prioritizes fixes by impact (issues resolved per fix)
- Returns structured report with one of 4 statuses

**Route based on agent status**:

### Status: TEST_FAILURE → Enter Test Focus Mode

**When**: Agent returns TEST_FAILURE status (tests failed)

**Action**: Focus exclusively on fixing tests before any quality analysis

```
Loop until tests pass:
  1. Display test failures from agent report
  2. Analyze failure root cause
  3. Apply fix to implementation or tests
  4. Re-run quality-analyzer (mode: "full")
  5. Check status:
     - Still TEST_FAILURE → Continue loop
     - ISSUES_FOUND or CLEAN_STATE → Exit Test Focus Mode, proceed with new status

Max 10 iterations. If stuck, ask user for guidance.
```

**Why Test Focus Mode**:
- Tests are Gate 1 - nothing else matters if tests fail
- Prevents wasting time on linter/review issues when code doesn't work
- Ensures quality analysis runs on working code

**After tests pass**: Re-run quality-analyzer and continue with new status

### Status: CLEAN_STATE → Skip to Phase 5 (Documentation)

**When**: Agent returns CLEAN_STATE status
- ✅ Tests passed
- ✅ Linter clean (0 errors)
- ✅ Review clean (0 findings)

**Action**: All quality gates passed! Skip fix loop, proceed directly to Phase 5 (Documentation)

### Status: ISSUES_FOUND → Continue to Phase 3 (Fix Loop)

**When**: Agent returns ISSUES_FOUND status
- ✅ Tests passed
- ❌ Linter has errors OR ⚠️ Review has findings

**Action**: Display agent's combined report and proceed to Phase 3

**Agent Report Contains**:
- 📊 Summary: Tests, linter, review status
- 🎯 Overlapping issues with root cause analysis
- 📋 Isolated issues (single source only)
- 🔢 Prioritized fix order (by impact)

**Example Report** (generated by quality-analyzer agent):
```
═══════════════════════════════════════════════════════
QUALITY ANALYSIS REPORT
Mode: FULL
Files analyzed: 8
═══════════════════════════════════════════════════════

📊 SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tests: ✅ PASS (coverage: 87%)
Linter: ❌ FAIL (5 errors)
Review: ⚠️ FINDINGS (8 issues: 0 bugs, 3 design, 4 readability, 1 polish)

Total issues: 13 from 3 sources

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OVERLAPPING ISSUES ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Found 3 locations with overlapping issues:

┌─────────────────────────────────────────────────────┐
│ pkg/parser.go:45 - function Parse                   │
│ OVERLAPPING (4 issues):                             │
│                                                      │
│ ⚠️ Linter: Cognitive complexity 18 (>15)           │
│ ⚠️ Linter: Function length 58 statements (>50)     │
│ 🔴 Review: Mixed abstraction levels                 │
│ 🔴 Review: Defensive null checking                  │
│                                                      │
│ 🎯 ROOT CAUSE:                                      │
│ Function handles multiple responsibilities at       │
│ different abstraction levels (parsing, validation,  │
│ building result).                                   │
│                                                      │
│ Impact: HIGH (4 issues) | Complexity: MODERATE      │
│ Priority: #1 CRITICAL                               │
└─────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRIORITIZED FIX ORDER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Priority #1: pkg/parser.go:45 (4 issues, HIGH impact)
Priority #2: pkg/validator.go:23 (3 issues, HIGH impact)
Priority #3: pkg/handler.go:67 (2 issues, MEDIUM impact)

Isolated issues: 6 (fix individually)

Total fix targets: 3 overlapping groups + 6 isolated = 9 fixes

STATUS: ISSUES_FOUND
```

### Status: TOOLS_UNAVAILABLE → Report Error

**When**: Agent returns TOOLS_UNAVAILABLE status (missing tools)

**Action**: Display agent report with missing tools and suggestions, ask user to install tools

### Phase 3: Iterative Fix Loop

**For each prioritized fix** (from agent's report):

1. **Apply Fix**:
   - Invoke @refactoring skill with:
     * File and function to fix
     * All issues in that area (from agent's overlapping groups or isolated issues)
     * Root cause analysis from agent (if available)
     * Expected outcome
   - @refactoring applies appropriate patterns:
     * Early returns (reduce nesting)
     * Extract function (break complexity)
     * Storifying (uniform abstractions)
     * Extract type (create domain types)
     * Switch extraction (categorize cases)
     * Extract constant (remove magic numbers)

2. **Verify Fix with Quality-Analyzer Agent (Incremental Mode)**:

   ```
   Task(subagent_type: "quality-analyzer")

   Prompt:
   "Re-analyze code quality after refactoring.

   Mode: incremental

   Project commands:
   - Test: [PROJECT_TEST_COMMAND]
   - Lint: [PROJECT_LINT_COMMAND]

   Files to analyze (changed):
   [list files from: git diff --name-only HEAD~1 HEAD | grep '\.go$']

   Previous findings:
   [paste findings from previous quality-analyzer report]

   Run quality gates and return delta report (what changed)."
   ```

   **Agent returns delta report with status**:
   - ✅ Fixed: Issues resolved since last run
   - ⚠️ Remaining: Issues still present
   - 🆕 New: Issues introduced by recent changes

3. **Route Based on Agent Status**:

   **If status = TEST_FAILURE**:
   - → Enter Test Focus Mode (refactoring broke tests)
   - Loop until tests pass (same as Phase 2)
   - Continue with new status

   **If status = CLEAN_STATE**:
   - → All issues resolved! Break out of fix loop
   - Continue to Phase 4 (Documentation)

   **If status = ISSUES_FOUND**:
   - Check delta report for progress:
     * ✅ If issues were fixed → Continue to next fix
     * ⚠️ If no progress → Analyze why, try different approach
     * 🆕 If new issues introduced → Fix them first

4. **Safety Limits**:
   - Max 10 iterations per fix loop
   - IF stuck (no progress after 3 attempts):
     * Show current status and delta report
     * Ask user for guidance
     * User can review: `git diff`

**Example Delta Report** (from quality-analyzer agent):
```
═══════════════════════════════════════════════════════
QUALITY ANALYSIS DELTA REPORT
Mode: INCREMENTAL
Files re-analyzed: 1 (changed since last run)
═══════════════════════════════════════════════════════

📊 SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tests: ✅ PASS (coverage: 89% ↑)
Linter: ✅ PASS (0 errors)
Review: ✅ CLEAN (0 findings)

✅ Fixed: 4 issues from pkg/parser.go:45
⚠️ Remaining: 0 issues
🆕 New: 0 issues introduced

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESOLUTION DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ FIXED:
  pkg/parser.go:45 | Linter | Cognitive complexity (was 18, now 8)
  pkg/parser.go:45 | Linter | Function length (was 58, now 25)
  pkg/parser.go:45 | Review | Mixed abstraction levels (resolved)
  pkg/parser.go:45 | Review | Defensive null checking (resolved)

STATUS: CLEAN_STATE ✅
Ready to proceed with next fix or move to documentation phase.
```

**Loop until agent returns CLEAN_STATE**:
- ✅ Tests pass
- ✅ Linter clean
- ✅ Review clean

### Phase 4: Documentation

Invoke @documentation skill:

1. Add/update package-level godoc
2. Add/update type-level documentation
3. Add/update function documentation (WHY not WHAT)
4. Add godoc testable examples (Example_* functions)
5. IF last plan step:
   - Add feature documentation to docs/ folder

**Verify**:
- Run: `go doc -all ./...`
- Ensure examples compile
- Check documentation coverage

### Phase 5: Commit Ready

Generate comprehensive summary with suggested commit message.

- Linter passes ✅
- Tests pass with coverage ✅
- Design review complete ✅
- Documentation complete ✅
- Present commit message suggestion

## Output Format

```
📋 COMMIT READINESS SUMMARY

✅ Linter: Passed (0 issues)
✅ Tests: 95% coverage (3 new types, 15 test cases)
⚠️  Design Review: 4 findings (see below)

🎯 COMMIT SCOPE
Modified:
- user/service.go (+45, -12 lines)
- user/repository.go (+23, -5 lines)

Added:
- user/user_id.go (new type: UserID)
- user/email.go (new type: Email)

Tests:
- user/service_test.go (+120 lines)
- user/user_id_test.go (new)
- user/email_test.go (new)

⚠️  DESIGN REVIEW FINDINGS

🔴 DESIGN DEBT (Recommended to fix):
- user/service.go:45 - Primitive obsession detected
  Current: func GetUserByID(id string) (*User, error)
  Better:  func GetUserByID(id UserID) (*User, error)
  Why: Type safety, validation guarantee, prevents invalid IDs
  Fix: Use @code-designing to convert remaining string usages

🟡 READABILITY DEBT (Consider fixing):
- user/service.go:78 - Mixed abstraction levels in CreateUser
  Function mixes high-level steps with low-level validation details
  Why: Harder to understand flow at a glance
  Fix: Use @refactoring to extract validation helpers

🟢 POLISH OPPORTUNITIES:
- user/repository.go:34 - Function naming could be more idiomatic
  SaveUser → Save (method receiver provides context)

📝 BROADER CONTEXT:
While reviewing user/service.go, noticed 3 more instances of string-based
IDs throughout the file (lines 120, 145, 203). Consider refactoring the
entire file to use UserID consistently for better type safety.

💡 SUGGESTED COMMIT MESSAGE
Add self-validating UserID and Email types

- Introduce UserID type with validation (prevents empty IDs)
- Introduce Email type with RFC 5322 validation
- Refactor CreateUser to use new types
- Achieve 95% test coverage with real repository implementation

Follows vertical slice architecture and primitive obsession principles.

────────────────────────────────────────

Would you like to:
1. Commit as-is (ignore design findings)
2. Fix design debt only (🔴), then commit
3. Fix design + readability debt (🔴 + 🟡), then commit
4. Fix all findings (🔴 🟡 🟢), then commit
5. Refactor entire file (address broader context), then commit
```

## Workflow Control

**Sequential Phases**: Each phase depends on previous phase completion
- Phase 1: Design and implementation must complete before quality analysis
- Phase 2: Quality analysis (via quality-analyzer agent) determines next phase
- Phase 3: Fix loop continues until all issues resolved (agent returns CLEAN_STATE)
- Phase 4: Documentation only after all quality gates pass
- Phase 5: Commit ready summary presented to user

**Status-Based Routing**: Agent determines workflow path
- **TEST_FAILURE** → Test Focus Mode (fix tests, retry Phase 2)
- **CLEAN_STATE** → Skip fix loop, go directly to documentation
- **ISSUES_FOUND** → Enter fix loop (Phase 3)
- **TOOLS_UNAVAILABLE** → Report error, ask user to install tools

**Parallel Execution**: Phase 2 and fix verification run 3 tools simultaneously (40-50% faster)

**Incremental Review**: After first run, agent only analyzes changed files for faster iteration

## Integration with Other Skills and Agents

This orchestrator **invokes** other skills and agents automatically:

**Skills**:
- @code-designing (Phase 1, if needed for type design)
- @testing (Phase 1, principles applied)
- @refactoring (Phase 3, when issues found)
- @documentation (Phase 4, always)

**Agents**:
- quality-analyzer agent (Phase 2 and Phase 3 verification)
  - Internally delegates to go-code-reviewer agent for design analysis
  - Executes tests and linter in parallel
  - Returns intelligent combined reports with overlapping issue detection

After committing, consider:
- If feature complete → Feature fully documented in Phase 4
- If more work needed → Run this workflow again for next commit
