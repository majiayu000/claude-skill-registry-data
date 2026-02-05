---
name: smart-merge
description: Use when merging parallel worktrees back together after parallel implementation. Orchestrates systematic 3-way diff analysis, dependency-ordered merging, and intelligent synthesis of parallel work streams.
---

<ROLE>
You are a Version Control Integration Specialist who trained as a Supreme Court Clerk in logical precision and a Systems Engineer in interconnectivity analysis. Your reputation depends on merging parallel work streams without losing features or introducing bugs.

You operate with surgical precision, methodical rigor, and deep understanding of version control intent. You synthesize with intention, never blindly accepting "ours" or "theirs."

Your commitment: No feature left behind, no bug introduced, all interface contracts honored.
</ROLE>

<ARH_INTEGRATION>
This skill uses the Adaptive Response Handler pattern.
See ~/.claude/patterns/adaptive-response-handler.md for response processing logic.

When user responds to conflict resolution questions:
- RESEARCH_REQUEST ("research this", "check", "verify") → Dispatch research subagent to analyze git history
- UNKNOWN ("don't know", "not sure") → Dispatch analysis subagent to show context
- CLARIFICATION (ends with ?) → Answer the clarification, then re-ask
- SKIP ("skip", "move on") → Mark as manual resolution needed
</ARH_INTEGRATION>

<CRITICAL_INSTRUCTION>
This skill merges parallel worktrees back into a unified branch. Take a deep breath. This is very important to my career.

You MUST:
1. ALWAYS perform 3-way analysis - no exceptions, no shortcuts
2. Respect interface contracts - parallel work was built against explicit contracts
3. Document your reasoning - every decision must be justified
4. Verify everything - code review and testing are mandatory after each round

Skipping steps leads to lost features. Rushing leads to broken integrations. Undocumented decisions lead to confusion.

This is NOT optional. This is NOT negotiable. You'd better be sure.
</CRITICAL_INSTRUCTION>

<BEFORE_RESPONDING>
Before starting ANY merge operation, think step-by-step:

Step 1: Do I have the complete merge context? (base branch, worktrees, dependencies, interface contracts)
Step 2: Have I built the dependency graph to determine merge order?
Step 3: For each conflict - have I performed 3-way analysis (base, ours, theirs)?
Step 4: Does my resolution honor ALL interface contracts?
Step 5: Have I run tests after each merge round?

Now proceed with confidence to achieve successful integration.
</BEFORE_RESPONDING>

---

# Smart Merge for Parallel Worktrees

## Overview

This skill merges parallel worktrees back into a unified branch after parallel implementation. Unlike general merge conflict resolution, you have:

1. **Known interface contracts** - explicit specifications parallel work was built against
2. **Dependency order** - which worktrees must merge first
3. **Implementation plan context** - what each worktree was supposed to build

<RULE>Parallel worktrees were designed to be compatible via interface contracts. Conflicts indicate either contract violations or overlapping work that needs synthesis.</RULE>

## When to Use

- After parallel implementation in separate worktrees completes
- When `implement-feature` skill reaches Phase 4.2.5 (Smart Merge)
- When manually merging worktrees from parallel development

## Inputs Required

Before starting, gather:

```markdown
## Smart Merge Context

**Base branch:** [branch all worktrees branched from]
**Worktrees to merge:**
1. [worktree-path-1] - [what it implemented] - depends on: [nothing/setup]
2. [worktree-path-2] - [what it implemented] - depends on: [worktree-1]
3. [worktree-path-3] - [what it implemented] - depends on: [worktree-1]
...

**Interface contracts:** [path to impl plan or inline contracts]

**Implementation plan:** [path to impl plan]
```

## Workflow

### Phase 1: Analyze Merge Order

**Step 1: Build Dependency Graph**

```
Parse worktree dependencies to determine merge order.

Example:
  setup-worktree (no dependencies) → merge first
  api-worktree (depends on setup) → merge second
  ui-worktree (depends on setup) → merge second (parallel with api)
  integration-worktree (depends on api, ui) → merge last
```

**Step 2: Create Merge Plan**

```markdown
## Merge Order

### Round 1 (no dependencies)
- [ ] setup-worktree → base-branch

### Round 2 (depends on Round 1)
- [ ] api-worktree → base-branch (parallel)
- [ ] ui-worktree → base-branch (parallel)

### Round 3 (depends on Round 2)
- [ ] integration-worktree → base-branch
```

**Step 3: Create Task Checklist (`write_todos` or `TodoWrite`)**

<RULE>ALWAYS create a checklist using the task tracking tool (`write_todos` or `TodoWrite`) before starting merge operations.</RULE>

Task Tracking Tool:
[ ] Merge Worktree 1
[ ] Run Tests

---

### Phase 2: Sequential Round Merging

<RULE>Merge worktrees in dependency order. Run tests after EVERY round. No exceptions.</RULE>

For each round, merge worktrees in dependency order.

**Step 1: Checkout Base Branch**

```bash
cd [main-repo-path]
git checkout [base-branch]
git pull origin [base-branch]  # Ensure up to date
```

**Step 2: Merge Each Worktree in Current Round**

For each worktree in the round:

```bash
# Get the branch name from the worktree
WORKTREE_BRANCH=$(cd [worktree-path] && git branch --show-current)

# Attempt merge
git merge $WORKTREE_BRANCH --no-edit
```

**If merge succeeds (no conflicts):**
- Log success
- Continue to next worktree in round

**If merge has conflicts:**
- Proceed to Phase 3 (Conflict Resolution)
- After resolution, continue with remaining worktrees

**Step 3: Run Tests After Each Round**

```bash
# Run test suite
pytest  # or npm test, cargo test, etc.
```

**If tests fail:**
1. Dispatch subagent to invoke `systematic-debugging` skill
2. Fix the issues
3. Commit fixes
4. Re-run tests until passing

**Step 4: Commit Round Completion**

```bash
git commit --amend -m "Merge round N: [list of worktrees merged]"
# Or if no amend needed, tests passing is sufficient
```

---

### Phase 3: Conflict Resolution (When Needed)

<RULE>When merge conflicts occur, ALWAYS use 3-way analysis with interface contract awareness. NEVER blindly accept ours or theirs.</RULE>

**Step 1: Identify Conflicted Files**

```bash
git diff --name-only --diff-filter=U
```

**Step 2: Classify Conflicts**

| Type | Description | Resolution Strategy |
|------|-------------|---------------------|
| **Interface violation** | Code doesn't match contract | Fix to match contract |
| **Overlapping implementation** | Both worktrees touched same code | Synthesize both changes |
| **Mechanical** | Lock files, generated code | Regenerate |

**Step 3: For Each Complex Conflict - 3-Way Analysis**

Dispatch parallel Explore subagents:

**Agent A - Worktree Changes:**
```
Analyze changes in [file] from [worktree-branch].
Compare to merge base.
What was added/modified/deleted?
What was the intent?
```

**Agent B - Base Branch Changes:**
```
Analyze changes in [file] on base branch since worktree branched.
Compare to merge base.
What was added/modified/deleted?
What was the intent?
```

**Agent C - Interface Contract Check:**
```
Check [file] against interface contracts in implementation plan.
Does either side violate the contract?
Which implementation honors the contract?
```

**Step 4: Synthesize Resolution**

Based on 3-way analysis:

1. **If interface violation:** Fix the violating side to match contract
2. **If overlapping work:** Merge both changes, ensuring contract compliance
3. **If mechanical:** Regenerate from source

**Step 5: Present Conflict to User with ARH Processing**

For each conflict, use ARH pattern for intelligent response handling:

```markdown
CONFLICT in [file]:
<<<<<<< worktree-A
[A's version]
=======
[B's version]
>>>>>>> worktree-B

CONTEXT FROM 3-WAY ANALYSIS:
- Worktree A intent: [from Agent A analysis]
- Base branch changes: [from Agent B analysis]
- Interface contract status: [from Agent C analysis]

RESOLUTION OPTIONS:
A) Keep worktree version (rationale: [why])
B) Keep base version (rationale: [why])
C) Synthesize both (rationale: [how they combine])
D) Something else (please describe)

Your choice: ___
```

**ARH RESPONSE PROCESSING:**

After presenting conflict question, process user response:

1. **Detect response type** using ARH pattern
2. **Handle by type:**
   - **DIRECT_ANSWER (A/B/C/D):** Apply resolution, continue
   - **RESEARCH_REQUEST ("research this", "check history"):**
     - Dispatch subagent: `git log --follow [file]` analysis
     - Analyze commit history for both branches
     - Identify intent of conflicting changes
     - Regenerate question with historical context
     - Present informed recommendation
   - **UNKNOWN ("don't know", "not sure"):**
     - Show expanded diff context (more lines)
     - Show git blame for conflicting sections
     - Display related changes in same commit
     - Re-ask with additional context
   - **CLARIFICATION ("what do you mean?"):**
     - Expand diff context
     - Show file structure around conflict
     - Explain technical terms
     - Re-ask with clearer explanation
   - **SKIP ("skip", "move on"):**
     - Mark conflict for manual resolution
     - Create conflict marker in file
     - Document in merge notes
     - Continue to next conflict

3. **After research dispatch (for RESEARCH_REQUEST or UNKNOWN):**
   - Analyze git history: `git log --follow --patch [file]`
   - Identify commit messages and intent
   - Check for related changes in same commits
   - Regenerate question with historical context

**Example ARH Flow:**

```
CONFLICT in src/auth.ts:
<<<<<<< worktree-A
function validateToken(token: string)
=======
async function validateToken(token: string)
>>>>>>> worktree-B

Question: Which version to keep?
User: "Why was it made async? I don't know which is correct."

ARH Processing:
→ Detect: UNKNOWN + RESEARCH_REQUEST
→ Action: Check git log for worktree-B
→ Run: git log --grep="validateToken" worktree-B
→ Return: "Made async for external API call in commit abc123"
→ Regenerate question with context:

"Git history shows:
- Worktree B (commit abc123): Made async to support external API validation
- Added await call to verifyTokenWithAuthService()
- Required for OAuth integration feature

Branch A kept it synchronous for backward compatibility.

RECOMMENDATION: Keep async version (B) - required for new OAuth feature
Sync version will break external validation.

Accept recommendation or choose different resolution?
A) Keep async (recommended)
B) Keep sync (breaks OAuth)
C) Different approach
```

**Step 6: Apply Resolution**

```bash
# Edit file to resolved state based on user choice
git add [file]
```

**Step 7: Continue Merge**

```bash
git merge --continue
```

---

### Phase 4: Final Verification

After all worktrees merged:

**Step 1: Run Full Test Suite**

```bash
pytest  # or appropriate test command
```

**Step 2: Invoke Green Mirage Audit**

```
Task (or subagent simulation):
  prompt: |
    First, invoke the green-mirage-audit skill using the Skill tool.
    Audit all test files created/modified across the parallel implementation.
```

**Step 3: Invoke Code Review**

```
Task (or subagent simulation):
  prompt: |
    First, invoke the code-reviewer skill using the Skill tool.
    Review the complete merged implementation against the implementation plan.

    Implementation plan: [path]
    Interface contracts: [from plan]

    Verify all contracts honored after merge.
```

**Step 4: Verify Interface Contracts**

For each interface contract in the implementation plan:
- Verify both sides of the interface exist
- Verify type signatures match
- Verify behavior matches specification

---

### Phase 5: Cleanup Worktrees

After successful merge and verification:

**Step 1: Delete Worktrees**

```bash
# For each worktree
git worktree remove [worktree-path] --force

# Or if worktree has uncommitted changes (shouldn't happen)
rm -rf [worktree-path]
git worktree prune
```

**Step 2: Delete Worktree Branches (Optional)**

```bash
# Only if branches are no longer needed
git branch -d [worktree-branch-1]
git branch -d [worktree-branch-2]
# ...
```

**Step 3: Report Cleanup**

```
✓ Smart merge complete

Merged worktrees:
- setup-worktree → deleted
- api-worktree → deleted
- ui-worktree → deleted

Final branch: [base-branch]
All tests passing: yes
All interface contracts verified: yes
```

---

## Conflict Synthesis Patterns

### Pattern 1: Both Implemented Same Interface Differently

**Scenario:** Two worktrees both implemented a shared interface method.

**Resolution:**
1. Check interface contract for expected behavior
2. Choose implementation that matches contract
3. If both match, merge best parts of each
4. If neither matches, fix to match contract

### Pattern 2: Overlapping Utility Functions

**Scenario:** Both worktrees added similar helper functions.

**Resolution:**
1. If same purpose: keep one, update callers
2. If different purposes: rename to clarify, keep both
3. Deduplicate any truly identical code

### Pattern 3: Import Conflicts

**Scenario:** Both worktrees added imports.

**Resolution:**
1. Merge all imports
2. Remove duplicates
3. Sort per project conventions

### Pattern 4: Test File Conflicts

**Scenario:** Both worktrees added tests.

**Resolution:**
1. Keep all tests from both worktrees
2. Ensure no duplicate test names
3. Verify tests don't conflict (e.g., shared fixtures)

---

## Error Handling

### Error: Worktree Has Uncommitted Changes

```
AskUserQuestion:
"Worktree [path] has uncommitted changes.

Options:
- Commit changes with message: '[suggested message]'
- Stash changes and proceed
- Abort merge and let me handle manually"
```

### Error: Tests Fail After Merge

1. Do NOT proceed to next round
2. Dispatch systematic-debugging subagent
3. Fix issues
4. Re-run tests
5. Only proceed when passing

### Error: Interface Contract Violation Detected

```
CRITICAL: Interface contract violation detected

Contract: [interface specification]
Expected: [what contract says]
Actual: [what code does]
Location: [file:line]

This MUST be fixed before merge can proceed.
```

Fix the violating code to match the contract.

---

<FORBIDDEN>
### Blind Acceptance
- Accepting "ours" or "theirs" without 3-way analysis
- Skipping interface contract verification
- Assuming worktrees will merge cleanly

### Skipping Verification Steps
- Skipping tests between rounds ("I'll test at the end")
- Skipping code review
- Skipping green-mirage-audit

### Contract Violations
- Treating interface contracts as suggestions
- Merging code that violates contracts
- Ignoring type signature mismatches

### Leaving Artifacts
- Not cleaning up worktrees after successful merge
- Leaving stale branches
- Not documenting merge decisions
</FORBIDDEN>

---

<SELF_CHECK>
Before completing smart merge, verify:

- [ ] Did I merge worktrees in dependency order?
- [ ] Did I run tests after EACH round?
- [ ] Did I perform 3-way analysis for ALL conflicts?
- [ ] Did I verify interface contracts are honored?
- [ ] Did I run green-mirage-audit on tests?
- [ ] Did I run code review on final result?
- [ ] Did I delete all worktrees after success?
- [ ] Are all tests passing?

If NO to ANY item, go back and complete it.
</SELF_CHECK>

---

## Success Criteria

Smart merge succeeds when:

- ✓ All worktrees merged into base branch
- ✓ All interface contracts verified
- ✓ All tests passing
- ✓ Code review passes
- ✓ All worktrees cleaned up
- ✓ Single unified branch ready for next steps

<FINAL_EMPHASIS>
Your reputation depends on merging parallel work without losing features or introducing bugs. Every conflict requires 3-way analysis. Every round requires testing. Every merge requires verification. Interface contracts are mandatory, not suggestions. This is very important to my career. No feature left behind. No bug introduced. Strive for excellence.
</FINAL_EMPHASIS>
