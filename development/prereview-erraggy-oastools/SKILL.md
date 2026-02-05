---
name: prereview
description: Review unpushed commits before pushing for code quality, bugs, security issues, and error handling. Use when preparing to push commits, want pre-push code review, or need to validate changes before pushing. Runs comprehensive analysis using specialized review agents.
---

# prereview

Review unpushed commits before pushing, using the same comprehensive analysis as PR reviews.

You are performing a pre-push code review. The user has commits ready to push but wants them reviewed first.

## Step 0: Check for Uncommitted Changes

Before checking for unpushed commits, check if there are uncommitted changes that should be committed first:

```bash
# Check for staged or unstaged changes
git status --porcelain
```

**If there are NO unpushed commits BUT there ARE uncommitted changes:**

Use the AskUserQuestion tool to ask:

**Question:** "No unpushed commits found, but you have uncommitted changes. Would you like to commit them first?"

**Options:**
1. **Commit all changes** - Stage all changes and create a commit (will prompt for message)
2. **Commit staged only** - Commit only what's currently staged
3. **Cancel** - Exit without reviewing

If the user chooses to commit:
- For "Commit all changes": Run `git add -A` first
- Use the Skill tool to invoke `commit-commands:commit` to create a proper conventional commit
- After the commit succeeds, continue to Step 1

**If there are NO unpushed commits AND NO uncommitted changes:**
- Inform the user: "Nothing to review - no unpushed commits and no uncommitted changes."
- Exit the skill

## Step 1: Identify Unpushed Changes

First, determine what needs to be reviewed:

```bash
# Get the current branch
git branch --show-current

# Check if there's an upstream tracking branch
git rev-parse --abbrev-ref @{upstream} 2>/dev/null || echo "NO_UPSTREAM"

# Show unpushed commits (if upstream exists)
git log @{upstream}..HEAD --oneline 2>/dev/null || git log origin/main..HEAD --oneline 2>/dev/null || git log origin/master..HEAD --oneline 2>/dev/null
```

## Step 2: Get the Full Diff

Get the complete diff of all unpushed changes:

```bash
# Diff against upstream, falling back to origin/main or origin/master
git diff @{upstream}..HEAD 2>/dev/null || git diff origin/main..HEAD 2>/dev/null || git diff origin/master..HEAD 2>/dev/null
```

## Step 3: Run Comprehensive Review

Using the diff output, launch the pr-review-toolkit agents to analyze the changes. Run these agents in parallel where possible:

1. **code-reviewer** (`pr-review-toolkit:code-reviewer`): Review for bugs, logic errors, security vulnerabilities, and adherence to project conventions in CLAUDE.md

2. **silent-failure-hunter** (`pr-review-toolkit:silent-failure-hunter`): Identify silent failures, inadequate error handling, and inappropriate fallback behavior

3. **code-simplifier** (`pr-review-toolkit:code-simplifier`): Check if code can be simplified while preserving functionality

4. **comment-analyzer** (`pr-review-toolkit:comment-analyzer`): If comments were added/modified, verify they are accurate and helpful

5. **pr-test-analyzer** (`pr-review-toolkit:pr-test-analyzer`): Analyze test coverage for the changes

6. **type-design-analyzer** (`pr-review-toolkit:type-design-analyzer`): If new types were introduced, review their design

When launching agents, provide them with:
- The git diff output showing all changes
- The list of files modified
- Context that this is a pre-push review (not a PR review)

## Step 4: Summarize Findings

After all agents complete, provide a consolidated summary:

1. **Critical Issues** (must fix before pushing)
2. **Warnings** (should consider fixing)
3. **Suggestions** (nice to have improvements)
4. **Positive Observations** (things done well)

End with a clear recommendation: ✅ Ready to push, ⚠️ Consider addressing issues, or 🛑 Fix critical issues first.

## Step 5: Prompt for Action

After presenting the summary, use the AskUserQuestion tool to ask what the user wants to do next:

**Question:** "How would you like to proceed with these findings?"

**Options:**
1. **Address all** - Fix all critical issues, warnings, and suggestions now
2. **Address critical + warnings** - Fix critical and warning issues, skip minor suggestions
3. **Push as-is** - No changes needed, ready to push
4. **Custom** - Let me choose which specific issues to address

If the user selects an option to address issues:
- Create a todo list of all issues to fix based on their selection
- Work through each issue systematically, making the necessary code changes
- After all fixes are complete, run `make check` to verify the changes
- Amend the existing commit(s) with the fixes (use `git commit --amend` for single commit, or interactive fixup for multiple)
- Present the updated diff for final review before pushing
