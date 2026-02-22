---
name: review-post-task
description: "[Review & Quality] ⚡⚡⚡ Two-pass code review for task completion"
argument-hint: [optional-focus-area]
infer: true
---

# Post-Task Two-Pass Code Review

Execute mandatory two-pass review protocol after completing code changes.
Focus: $ARGUMENTS

## Summary

**Goal:** Two-pass code review ensuring all changes follow EasyPlatform standards before commit.

| Step | Action | Key Notes |
|------|--------|-----------|
| 1 | Pass 1: Review | Gather `git diff`, check task correctness + code standards + security |
| 2 | Pass 1: Corrections | Fix issues found; set `PASS_1_MADE_CHANGES` flag |
| 3 | Pass 2: Re-review | Only if Pass 1 made changes; verify corrections didn't introduce issues |
| 4 | Final report | Summary with issues found/fixed, remaining concerns, ready-for-commit status |

**Key Principles:**
- Two passes guarantee corrections don't introduce new issues
- Auto-triggered after `/cook`, `/fix`, `/code` workflows
- Check logic in lowest layer, BEM classes, `untilDestroyed()`, platform validation patterns

---

## Protocol Overview

This review ensures ALL code changes follow best practices and project conventions.
Two passes guarantee corrections don't introduce new issues.

---

## Pass 1: Initial Review

### Step 1.1: Gather Changes
```bash
# Get unstaged changes summary
git diff --stat

# Get detailed changes
git diff
```

### Step 1.2: Review Checklist

**Task Correctness:**
- [ ] Changes achieve the intended task objective
- [ ] No unrelated/unnecessary modifications
- [ ] Edge cases handled appropriately
- [ ] Error handling is complete

**Code Standards (EasyPlatform):**

*Backend:*
- [ ] Uses platform repository (IPlatformQueryableRootRepository)
- [ ] Uses PlatformValidationResult fluent API (.And(), .AndAsync())
- [ ] Side effects in Entity Event Handlers, not command handlers
- [ ] DTOs own mapping via MapToEntity()/MapToObject()
- [ ] Command + Result + Handler in ONE file

*Frontend:*
- [ ] Extends appropriate base class (AppBaseComponent, AppBaseVmStoreComponent, AppBaseFormComponent)
- [ ] Uses PlatformVmStore for state management
- [ ] Uses .pipe(this.untilDestroyed()) for subscriptions
- [ ] All template elements have BEM classes

**Architecture:**
- [ ] Logic placed in lowest appropriate layer (Entity > Service > Component)
- [ ] No cross-service direct database access
- [ ] Follows existing patterns found in codebase

**Understanding Verification (soft prompts):**
- Can you explain in 2 sentences why each modified file was changed?
- What would break if this change were reverted?
- What assumption does this change rely on?

**Security:**
- [ ] No hardcoded secrets or credentials
- [ ] Input validation at boundaries
- [ ] Proper authorization checks

### Step 1.3: Execute Corrections
If any issues found:
1. Fix each issue directly
2. Mark `PASS_1_MADE_CHANGES = true`
3. Proceed to Pass 2

If no issues found:
1. Mark `PASS_1_MADE_CHANGES = false`
2. Skip to Final Report

---

## Pass 2: Re-Review (Conditional)

**ONLY EXECUTE IF PASS 1 MADE CHANGES**

### Step 2.1: Verify All Changes
```bash
# Check updated changes
git diff --stat
git diff
```

### Step 2.2: Full Re-Review
Repeat Pass 1 checklist on ALL current changes (original + corrections).

Focus areas:
- [ ] Original task still correctly implemented
- [ ] Corrections are valid and complete
- [ ] No new issues introduced by corrections
- [ ] Code is production-ready

### Step 2.3: Final Corrections
If issues found:
- Apply minimal, targeted fixes
- Document any trade-offs made

---

## Final Report

### Summary Template
```markdown
## Post-Task Review Complete

**Task:** [Brief description]
**Pass 1 Result:** [Clean / N issues fixed]
**Pass 2 Required:** [Yes/No]
**Pass 2 Result:** [N/A / Clean / N issues fixed]

### Changes Summary
- [List of files modified]
- [Key changes made]

### Issues Found & Fixed
1. [Issue]: [Fix applied]
2. ...

### Remaining Concerns (if any)
- [Concern]: [Reason not addressed / Recommended follow-up]

### Verification
- [ ] Task objective achieved
- [ ] Code follows project conventions
- [ ] No security vulnerabilities
- [ ] Ready for commit
```

---

## Quick Commands

```bash
# View changes for review
git diff --stat && git diff

# Check specific file
git diff path/to/file.ts

# Fix a problematic change
# Use `/fix` workflow to apply fixes instead of manual git checkout

# Stage reviewed changes
git add -p  # Interactive staging
```

---

## Integration Notes

- This command is auto-triggered by workflow orchestration after `/cook`, `/fix`, `/code`
- Can be manually invoked anytime with `/review-post-task`
- For PR reviews, use `/review-codebase` instead
- Use `code-reviewer` subagent for complex reviews requiring deeper analysis

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
