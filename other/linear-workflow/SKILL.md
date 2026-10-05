---
name: linear-workflow
description: Execute feature implementation following the standardized Linear workflow for spec-driven development.
---

# Linear Workflow Skill
Execute feature implementation following the standardized Linear workflow for spec-driven development.

## When to Use

Use this skill when implementing a Linear issue (e.g., PROJ-18, PROJ-19) that has well-defined tasks from a spec.

## Workflow Steps

### 1. Initialize Linear Issue

**Action**: Update the Linear issue to "In Progress"
```
Use: mcp__plugin_linear_linear__update_issue
Parameters:
  - id: {ISSUE_ID}
  - state: "In Progress"
```

### 2. Setup Task Tracking

**Action**: Create TodoWrite list for all tasks in the issue
```
Use: TodoWrite tool
Include:
  - All test tasks (e.g., T045, T046)
  - All implementation tasks (e.g., T047-T052)
  - Mark first task as "in_progress"
```

### 3. Follow TDD Approach

**For each task group:**

a. **Write Tests First** (Tasks like T045, T046)
   - Create test files
   - Verify tests would fail without implementation
   - Mark test tasks as completed in TodoWrite

b. **Implement Code** (Tasks like T047-T048)
   - Create implementation files
   - Mark implementation tasks as completed in TodoWrite

c. **Pause for Xcode Project Updates**
   - If new files created, STOP and ask user to add them to Xcode
   - Wait for confirmation before proceeding

d. **Run Tests** (Task like T052)
   - Run full test suite: `xcodebuild -project ... test`
   - Verify all tests pass (e.g., "126/126 passing")
   - Check specific test suites passed (e.g., "OnboardingStateTests: 4/4 passed")
   - Mark test verification task as completed

### 4. Prepare Commit

**Action**: Draft commit message following Linear format
```
Format:
{Brief description (T{start}-T{end})}. Completes {ISSUE_ID}

{Detailed body with:**
- **Test Files Created (T{X}-T{Y}):**
  - File descriptions with test counts

- **Implementation Files Created (T{X}):**
  - File descriptions with features

- **Files Modified:**
  - What changed and why (with task references)

- **Test Results (T{X}):**
  - X/X unit tests passing (added Y tests)
  - X/X UI tests passing
  - Specific test suite results

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**CRITICAL**: "Completes {ISSUE_ID}" MUST be at the END of the title line, NOT in the body

### 5. Get Approval

**Action**: Present commit message to user
```
Say: "Please review and approve this commit message before I proceed with the commit."
Wait for user approval before committing
```

### 6. Commit Changes

**Action**: Commit with approved message
```
Use: git add -A && git commit -m "$(cat <<'EOF'
{approved commit message}
EOF
)"
```

### 7. Update Linear Issue Status

**Action**: Mark issue as "In Review" (or "Done" if no manual testing)
```
Use: mcp__plugin_linear_linear__update_issue
Parameters:
  - id: {ISSUE_ID}
  - state: "In Review"  // or "Done" if fully complete
```

### 8. Update tasks.md

**Action**: Mark completed tasks in spec tasks.md file
```
Change: [ ] T{X} -> [x] T{X}
For all completed tasks

Then commit:
git add specs/{spec-name}/tasks.md && \
git commit -m "Update tasks.md: Mark T{X}-T{Y} as complete ({ISSUE_ID})"
```

## Example Usage

```
User: "Use the linear workflow to execute tasks in PROJ-20"

Claude:
1. Updates PROJ-20 to "In Progress"
2. Creates TodoWrite with T066-T072
3. Implements T066 (tests), T067 (code), etc.
4. Pauses for Xcode file additions
5. Runs tests, verifies all pass
6. Drafts commit message with "Completes PROJ-20" at end of title
7. Gets user approval
8. Commits changes
9. Updates PROJ-20 to "In Review"
10. Updates tasks.md with completed tasks
```

## Commit Message Examples

### ✅ CORRECT Format
```
Phase 5: Implement location permission screen (T045-T052). Completes PROJ-18

{body text}
```

### ❌ INCORRECT Format
```
[PROJ-18] Phase 5: Implement location permission screen (T045-T052)

{body text}
Completes PROJ-18
```

## Key Principles

1. **Always TDD**: Tests before implementation
2. **Pause for Xcode**: Never assume files are added automatically
3. **Get Approval**: Always show commit message before committing
4. **Linear Format**: "Completes {ISSUE-ID}" at END of title
5. **Track Progress**: Use TodoWrite throughout
6. **Update Status**: Keep Linear issue status current
7. **Document Tasks**: Update tasks.md after completion

