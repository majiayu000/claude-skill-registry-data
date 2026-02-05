---
name: review-git-changes
description: Analyzes and refactors code changes in the current git working tree (staged, unstaged, or recent commits). Ensures changes follow best practices, coding standards, and maintain code quality. Use when the user asks to "review my git changes", "check what I changed", "refactor my changes", "ensure my changes are clean", or "review before commit".
allowed-tools: Read, Edit, Bash(git:*), Bash(pytest:*), Bash(python:*), Grep, Glob, WebSearch
---

# Review Git Changes Skill

This skill provides focused code quality analysis and refactoring specifically for code that has been modified in git. It analyzes only the files you've changed, ensuring your modifications follow best practices before committing.

## When to Use This Skill

Trigger this skill when users ask to:
- "Review my git changes"
- "Check what I changed and make sure it's good"
- "Refactor my recent changes"
- "Ensure my changes follow best practices"
- "Review before I commit"
- "Clean up my git diff"
- "Make sure my changes are production-ready"

**Key Difference from Other Skills:**
- **code-analysis**: Analyzes entire files/modules (not just changes)
- **refactor-code**: Refactors based on implementation plan (broader scope)
- **critic**: Full audit of existing code
- **review-git-changes**: Analyzes ONLY the git delta (what you changed)

## Workflow Overview

```
1. Git Change Detection
   ├─ Run git status (staged + unstaged files)
   ├─ Run git diff (see actual changes)
   ├─ Optionally check recent commits (git log)
   └─ Identify all changed files

2. Change Analysis Phase
   ├─ Read each changed file
   ├─ Analyze only the modified sections
   ├─ Check against best practices
   ├─ Identify issues in changes
   └─ Create focused improvement plan

3. Review & Decision Point
   ├─ Present findings summary
   ├─ Categorize: Critical/Moderate/Minor
   └─ Ask: Refactor now? [Yes/No/Selective]

4. Refactoring Phase (if approved)
   ├─ Apply fixes to changed code
   ├─ Run tests after each change
   ├─ Verify git diff looks clean
   └─ Report final results
```

## Step-by-Step Process

### Phase 1: Detect Git Changes

**1. Identify what's been changed:**

Run git commands to understand the scope:

```bash
# Check current status
git status

# See unstaged changes
git diff

# See staged changes
git diff --cached

# Get list of changed files
git diff --name-only HEAD

# Optionally: recent commits (if analyzing past changes)
git log -5 --oneline
git diff HEAD~3..HEAD  # changes in last 3 commits
```

**2. Parse and categorize changes:**

Extract the list of changed files:
- **Unstaged changes**: Files modified but not `git add`ed
- **Staged changes**: Files ready to commit
- **Recent commits**: Already committed (if user wants to review)

**3. Determine scope:**

Ask user for clarification if needed:
- "I see 8 files changed. Should I review all of them, or specific ones?"
- "You have staged changes and unstaged changes. Review both?"
- "Do you want to include the last 2 commits in the review?"

### Phase 2: Analyze Changed Code

**For each changed file:**

**1. Read the full file:**
   - Use Read tool to get complete context
   - Understand the file's purpose and structure

**2. Focus on the git diff:**
   - Identify the specific lines that changed
   - Understand the intent of the change (what was the goal?)
   - Check the surrounding context (how does it fit?)

**3. Analyze change quality:**

Check these aspects specifically for the CHANGED code:

#### Code Structure (Changed sections only)
- **New duplication**: Did the change introduce repeated code?
- **New complexity**: Did the change make code harder to understand?
- **New magic numbers**: Are there hardcoded values in the change?
- **Naming quality**: Are new variables/functions well-named?
- **Function length**: Did changes make functions too long (>100 lines)?
- **Parameter count**: Did changes add too many parameters (>5)?

#### Best Practices (Language-specific)
- **Python**:
  - Type hints for new functions
  - Docstrings for public methods
  - PEP 8 compliance
  - Proper exception handling
  - Context managers for resources

- **JavaScript/TypeScript**:
  - Consistent async/await usage
  - Proper error handling
  - TypeScript types for new code
  - Modern ES6+ patterns

- **General**:
  - SOLID principles
  - DRY (Don't Repeat Yourself)
  - Separation of concerns
  - Error handling

#### Performance
- **Algorithm efficiency**: Are new algorithms optimal?
- **Unnecessary iterations**: New loops that could be avoided?
- **Data structure choice**: Right structure for the operation?
- **Resource leaks**: Proper cleanup in changed code?

#### Security (Critical for new/changed code)
- **Input validation**: Are inputs validated?
- **SQL injection**: Any raw SQL with user input?
- **XSS vulnerabilities**: Proper escaping in web code?
- **Command injection**: Safe use of subprocess/exec?
- **Secret exposure**: No hardcoded credentials?

#### Testing
- **Test coverage**: Are there tests for the changed functionality?
- **Test updates**: Did existing tests need updates?
- **Edge cases**: Are edge cases handled?

**4. Compare with project patterns:**

Use Grep to find how similar functionality is implemented:
```bash
# Example: How does the codebase handle error logging?
grep -r "logger\." --include="*.py" | head -20

# Example: How are API endpoints typically structured?
grep -r "def.*api" --include="*.py"
```

**5. Search for best practices (selective):**

If major issues found in changes, do targeted web search:
- Focus on the specific pattern or anti-pattern found
- Search for official framework/library documentation
- Example: "Python async best practices", "React hooks common mistakes"

### Phase 3: Create Focused Improvement Plan

**Generate a git-change-specific report:**

```markdown
# Git Changes Review Report

**Changed Files:** X files
**Lines Added:** +Y
**Lines Removed:** -Z
**Quality Assessment:** [Excellent/Good/Needs Improvement/Critical Issues]

---

## Summary of Changes

### Files Modified
1. `file1.py`: [Brief description of what changed and why]
2. `file2.py`: [Brief description of what changed and why]
3. `file3.py`: [Brief description of what changed and why]

---

## Issues Found in Changes

### 🔴 Critical Issues (Must Fix Before Commit)
1. **[Issue Name]** - `file.py:line`
   - **Problem:** [What's wrong in the change]
   - **Impact:** [Why it's critical]
   - **Fix:** [Specific solution]
   - **Code:**
     ```python
     # Current (bad)
     [problematic code from diff]

     # Suggested (good)
     [improved code]
     ```

### 🟡 Moderate Issues (Should Fix)
[Same format as critical]

### 🟢 Minor Issues (Nice to Have)
[Same format as critical]

---

## Positive Changes
- ✅ [Good practices observed in the changes]
- ✅ [Well-structured additions]

---

## Testing Recommendations

**Tests to run:**
```bash
# Suggested test commands
pytest tests/test_changed_module.py
```

**Tests to add/update:**
- [ ] Add test for new function `foo()` in file.py
- [ ] Update test for modified function `bar()` in file2.py

---

## Next Steps

**Option 1: Auto-refactor**
I can apply these fixes automatically and run tests.

**Option 2: Manual fixes**
Use this report to fix issues yourself.

**Option 3: Selective refactoring**
Choose specific issues to auto-fix.
```

Save this to `GIT_CHANGES_REVIEW.md`

### Phase 4: Decision Point

**Ask user using AskUserQuestion:**

Present options:
1. **Apply All Fixes** - Refactor all issues automatically
2. **Apply Critical Only** - Fix only critical issues (safe to commit after)
3. **Manual Review** - User will fix manually
4. **Cancel** - Don't make any changes

**Provide context:**
```
I found X issues in your git changes:
- 🔴 Y critical (must fix before commit)
- 🟡 Z moderate (should fix)
- 🟢 W minor (nice to have)

Files affected: A files
Estimated changes: B modifications
Risk: [Low/Medium/High] (based on test coverage and complexity)

How would you like to proceed?
```

### Phase 5: Refactoring (Conditional)

**If user approves refactoring:**

Follow the safety-first methodology from `refactor-code` skill:

**1. Prepare:**
- Create TodoWrite list for tracking
- Identify all tests related to changed files
- Note rollback points (current git state)

**2. Apply changes incrementally:**

For each issue (Critical → Moderate → Minor):

**a. Make focused change:**
```python
# Use Edit tool for precise changes
# Modify ONLY what's needed for THIS issue
# Keep the change atomic and focused
```

**b. Verify immediately after EACH change:**
```bash
# Run relevant tests
pytest tests/test_module.py -v

# Check code quality
ruff check file.py

# Verify git diff still makes sense
git diff file.py
```

**c. Fix if broken:**
- If tests fail, fix immediately
- Don't proceed to next issue until current one is stable
- If unable to fix, ask user for guidance

**d. Track progress:**
- Mark todo as completed
- Update user on progress
- Move to next issue

**3. Iterate until all approved changes are applied**

**4. Final verification:**

```bash
# Run full test suite
pytest

# Run linters
ruff check .
ruff format .

# Review final git diff
git diff

# Verify no unintended changes
git status
```

### Phase 6: Final Report

**Provide comprehensive summary:**

```markdown
## Git Changes Review Complete

### Changes Analyzed
- Files: X modified
- Lines: +Y added, -Z removed
- Review report: `GIT_CHANGES_REVIEW.md`

### Issues Found
- 🔴 Critical: A found
- 🟡 Moderate: B found
- 🟢 Minor: C found

---

### Refactoring Results
[If refactoring was performed]

**Changes Applied:**
- ✅ Fixed A critical issues
- ✅ Fixed B moderate issues
- ✅ Fixed C minor issues

**Files Modified:**
- `file1.py`: [Description of fixes]
- `file2.py`: [Description of fixes]

**Verification:**
- ✅ All tests passing (X/X tests)
- ✅ Linters passing
- ✅ Git diff reviewed

**Git Status:**
```
[Output of git status]
```

**Next Steps:**
Ready to commit! Suggested commit message:

```
[Your descriptive commit message]

Changes:
- [Summary of main changes]
- [Fixed issues from review]

🤖 Reviewed with Claude Code review-git-changes skill
```

---

[If refactoring was skipped]

**Manual Review Mode:**
- No changes applied
- Use `GIT_CHANGES_REVIEW.md` as your guide
- Fix issues before committing

---

### Remaining Items
[If any issues not addressed]
- X moderate issues to consider
- Y minor improvements for later
```

## Important Guidelines

### Safety First
**CRITICAL: Never Break Working Code**
- Run tests after EVERY change
- Make changes incrementally (one at a time)
- Keep track of git state (can always `git reset --hard` if needed)
- If uncertain about a change, ask user first
- Don't remove functionality without approval

### Maintain Functionality
**Changes should improve quality WITHOUT changing behavior:**
- Refactoring ≠ New features
- Keep the same external API
- All existing tests should pass
- Only update tests if behavior intentionally changed
- Don't mix refactoring with feature work

### Focus and Scope
**ONLY analyze and refactor what's in the git diff:**
- Don't expand scope to entire file (unless needed for context)
- Don't refactor unrelated code
- Don't add new functionality
- Don't over-engineer the solution
- Stay focused on the actual changes made

### Respect User's Changes
**This is a review, not a rewrite:**
- Understand the intent behind changes
- Don't undo user's work without good reason
- Suggest improvements, don't impose them
- Preserve coding style and patterns
- Only change what's clearly problematic

### Git Awareness
**Keep git history clean:**
- Don't create merge conflicts
- Preserve commit structure (if reviewing commits)
- Don't mix staged and unstaged changes without asking
- Be aware of what's already committed vs uncommitted
- Suggest atomic commits for refactored changes

### Communication
**Be transparent and helpful:**
- Explain what each change does and why
- Provide before/after code examples
- Link to best practices and documentation
- Celebrate good changes too
- Give actionable feedback

## Common Scenarios

### Scenario 1: Pre-Commit Review

**User:** "Review my changes before I commit"

**Actions:**
1. `git diff` to see unstaged changes
2. `git diff --cached` to see staged changes
3. Analyze all changes
4. Create review report
5. Ask: "Fix issues now or manually?"
6. Apply fixes if approved
7. Run tests
8. Show final git diff
9. Suggest commit message

### Scenario 2: Post-Commit Review

**User:** "Review my last 3 commits"

**Actions:**
1. `git log -3` to see commits
2. `git diff HEAD~3..HEAD` to see changes
3. Analyze the cumulative diff
4. Create review report
5. If issues found: "These commits have X issues. Create a new commit to fix?"
6. Apply fixes in new commit
7. Show git log with new fix commit

### Scenario 3: Large Feature Branch Review

**User:** "Review all changes in my feature branch"

**Actions:**
1. `git diff main..feature-branch` to see all changes
2. Identify scope: "I see 23 files changed. This is large. Options:"
   - Review all (will take time)
   - Review specific files only
   - Review by commit (one at a time)
3. User chooses approach
4. Proceed with focused analysis
5. Create comprehensive report
6. Offer phased refactoring

### Scenario 4: Critical Security Fix Review

**User:** "I fixed a security issue. Make sure I did it right."

**Actions:**
1. `git diff` to see the fix
2. Focus analysis on security aspects
3. Search for OWASP best practices
4. Verify:
   - Input validation present
   - No new vulnerabilities introduced
   - Proper error handling
   - Secure defaults
5. Check if tests cover the vulnerability
6. Recommend security-specific tests
7. Report findings with security focus

## Integration with Other Skills

**Workflow Combinations:**

```
Before Commit:
review-git-changes → [Fix issues] → Commit

Full Code Audit:
code-analysis (full file) → review-git-changes (recent changes) → refactor-code

Production Preparation:
review-git-changes → best-practice (if needed) → commit → deploy

Critical Changes:
review-git-changes → manual security review → review-git-changes (verify fixes)
```

**When to Use Each Skill:**

| Skill | Use When |
|-------|----------|
| **review-git-changes** | Reviewing uncommitted or recent changes |
| **code-analysis** | Quick quality check of entire files |
| **refactor-code** | Applying systematic improvements from a plan |
| **critic** | Complete audit + refactoring workflow |
| **best-practice** | Making MVP code production-ready |

## Quick Reference

**Key Commands:**
```bash
# Detect changes
git status
git diff
git diff --cached
git diff --name-only HEAD

# Verify changes
pytest
ruff check .
git diff  # review after refactoring

# Ready to commit
git add .
git commit -m "message"
```

**Workflow:**
1. **Detect** → Git status/diff
2. **Analyze** → Review changed code
3. **Report** → Create GIT_CHANGES_REVIEW.md
4. **Decide** → User chooses action
5. **Refactor** → Apply fixes (if approved)
6. **Verify** → Run tests
7. **Report** → Final summary

**Output Files:**
- `GIT_CHANGES_REVIEW.md` - Detailed analysis report

**Safety Mantra:**
- ✅ One change at a time
- ✅ Test after each change
- ✅ Fix failures immediately
- ✅ Never skip verification
- ✅ Keep git state clean
