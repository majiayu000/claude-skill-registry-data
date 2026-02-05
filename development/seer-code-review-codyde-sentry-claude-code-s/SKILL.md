---
name: seer-code-review
description: Analyze, validate, and fix issues identified by sentry bot in GitHub Pull Request reviews. Use this when asked to review or address sentry bot comments on PRs. Can review specific PRs by number or automatically find recent PRs with sentry comments.
---

# Sentry Bot PR Comment Reviewer

This skill helps you systematically analyze, validate, and fix issues identified by the sentry automated code review bot in GitHub Pull Requests.

## When to Use This Skill

Invoke this skill when:
- User asks to "review sentry comments" or "check sentry bot feedback"
- user asks to "check for code reviews"
- User mentions a PR with automated review comments
- User wants to validate or implement fixes from automated review tools
- User asks about a specific sentry bot comment
- User asks to check recent PRs for sentry comments

## Workflow

### Phase 0: Determine Target PR(s)

**If PR number is provided:**
- Proceed directly to Phase 1 with that PR number

**If NO PR number is provided:**
1. **List Recent PRs**
   ```bash
   gh pr list --limit 10 --json number,title,author,updatedAt,headRefName
   ```

2. **Check Each PR for Sentry Comments**
   For the most recent PRs (up to 5), check for sentry bot comments:
   ```bash
   gh api repos/{owner}/{repo}/pulls/{pr_number}/comments
   ```
   Filter for comments from `sentry[bot]`

3. **Present Options to User**
   If multiple PRs have sentry comments:
   ```markdown
   Found sentry bot comments on multiple recent PRs:
   - PR #42: "Fix authentication flow" (3 sentry comments)
   - PR #38: "Update build script" (1 sentry comment)

   Which PR would you like me to review? Or should I review all of them?
   ```

4. **Default Behavior**
   If only one PR has sentry comments, automatically proceed with that PR.
   If no recent PRs have sentry comments, inform the user.

### Phase 1: Fetch and Parse Comments

1. **Get PR Comments**
   ```bash
   gh api repos/{owner}/{repo}/pulls/{pr_number}/comments
   ```

   Look for comments from user `sentry[bot]` (login: `sentry[bot]`)

2. **Parse Comment Structure**
   Sentry bot comments typically include:
   - **Summary**: Brief description of the issue
   - **Description**: Detailed explanation of the problem
   - **Suggested fix**: Concrete recommendation
   - **Severity**: Float value (0.0-1.0) indicating criticality
   - **Confidence**: Float value (0.0-1.0) indicating certainty
   - **File path**: Location in the PR diff
   - **Line number**: Specific line being flagged

3. **Organize by Priority**
   Sort comments by:
   - Severity × Confidence (highest first)
   - Breaking issues before warnings
   - Blocking issues (CI failures) before improvements

### Phase 2: Validate the Issue

For each comment, systematically verify:

1. **Understand the Context**
   - Read the relevant file sections using the Read tool
   - Check surrounding code for context
   - Review the PR diff to understand what changed

2. **Verify the Problem**
   - Does the issue actually exist in the current code?
   - Is the bot's analysis correct?
   - Check file paths and line numbers are accurate

3. **Assess Impact**
   - **Severity >= 0.8**: Critical - likely blocks functionality
   - **Severity 0.5-0.7**: Medium - causes issues but not blocking
   - **Severity < 0.5**: Low - minor improvements or nitpicks
   - **Confidence >= 0.9**: Very likely correct
   - **Confidence 0.7-0.8**: Probably correct, verify carefully
   - **Confidence < 0.7**: May be false positive, investigate thoroughly

4. **Risk Matrix**
   ```
   High Severity × High Confidence = FIX IMMEDIATELY
   High Severity × Low Confidence  = INVESTIGATE THOROUGHLY
   Low Severity × High Confidence  = FIX IF TIME PERMITS
   Low Severity × Low Confidence   = LIKELY IGNORE
   ```

### Phase 3: Test the Analysis

Before implementing fixes, validate the bot's claim:

1. **Path Resolution Issues**
   - Verify file paths exist
   - Check for typos in paths or variable names
   - Confirm line numbers match current code

2. **Logic Errors**
   - Trace the execution flow
   - Check for edge cases mentioned
   - Look for similar patterns elsewhere in codebase

3. **Build/CI Issues**
   - Review CI workflow files
   - Check build scripts
   - Verify environment configurations

4. **Create a Reproduction**
   If possible, write a test case or scenario that demonstrates the issue

### Phase 4: Implement the Fix

When you've validated the issue is real:

1. **Checkout PR Branch**
   ```bash
   git fetch origin pull/{pr_number}/head:temp-branch-name
   git checkout temp-branch-name
   ```

2. **Apply the Fix**
   - Use Edit tool for targeted changes
   - Follow the suggested fix if it's correct
   - Improve upon the suggestion if needed
   - Maintain code style consistency

3. **Verify the Fix**
   - Re-read the modified file
   - Check that the change addresses the root cause
   - Ensure no new issues were introduced
   - Run relevant tests if applicable

4. **Commit the Change**
   ```bash
   git add <files>
   git commit -m "fix: address sentry bot comment - <brief description>

   <detailed explanation of what was fixed>

   Resolves issue identified by sentry bot.
   Severity: <severity>, Confidence: <confidence>

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

5. **Push to PR Branch**
   ```bash
   git push origin <branch-name>
   ```

### Phase 5: Report Findings

Provide a structured summary:

```markdown
## Sentry Bot Comment Review

### Comment Analysis
- **Location**: file_path:line_number
- **Issue**: <brief description>
- **Severity**: X.X (Critical/Medium/Low)
- **Confidence**: X.X (High/Medium/Low)

### Validation Result
✅ VALID / ❌ FALSE POSITIVE / ⚠️ PARTIALLY VALID

**Analysis**: <your assessment>

### Action Taken
✅ FIXED / ⏭️ SKIPPED / 🔍 NEEDS INVESTIGATION

**Details**: <what you did or why you skipped>

### Impact
<explain what would have happened without the fix>
```

## Best Practices

### DO:
- ✅ Always verify the bot's analysis before implementing
- ✅ Read surrounding code for context
- ✅ Test fixes when possible
- ✅ Provide detailed commit messages
- ✅ Reference the bot comment in your fix
- ✅ Switch back to original branch after pushing fixes

### DON'T:
- ❌ Blindly implement suggestions without validation
- ❌ Fix low-confidence issues without investigation
- ❌ Ignore high-severity warnings
- ❌ Make unrelated changes in the same commit
- ❌ Push directly to main/master
- ❌ Forget to switch branches after fixing

## Common Sentry Bot Issue Types

### 1. Path Resolution Errors
**Pattern**: Build scripts move files to wrong locations
**Example**: `mv file.tgz ../../wrong/path/`
**Validation**: Trace the path from the command's working directory

### 2. Missing Error Handling
**Pattern**: Functions that can throw but aren't wrapped in try/catch
**Validation**: Check if calling code handles errors

### 3. Race Conditions
**Pattern**: Async operations without proper awaits
**Validation**: Trace async/await chains

### 4. Type Mismatches
**Pattern**: TypeScript/type errors in builds
**Validation**: Check type definitions and usages

### 5. Configuration Issues
**Pattern**: Missing or incorrect config files
**Validation**: Check if config is read by the application

### 6. Security Vulnerabilities
**Pattern**: Exposed secrets, SQL injection, XSS
**Validation**: ALWAYS FIX - verify the vulnerability exists

## Handling False Positives

If you determine a comment is a false positive:

1. **Document Why**
   - Explain what the bot missed
   - Show why the code is actually correct
   - Provide evidence (logs, test results, etc.)

2. **Add a Comment to PR**
   ```bash
   gh pr comment {pr_number} --body "Sentry bot comment at file:line appears to be a false positive because..."
   ```

3. **Consider Improving the Code**
   Even if not a bug, unclear code led to the false positive
   Consider refactoring for clarity

## Quick Reference

**Fetch PR comments**: `gh api repos/{owner}/{repo}/pulls/{pr_number}/comments`
**Get PR diff**: `gh pr diff {pr_number}`
**Checkout PR**: `git fetch origin pull/{pr}/head:branch && git checkout branch`
**Push fix**: `git push origin {branch-name}`
**Switch back**: `git checkout main`

For a comprehensive command reference, see [QUICKREF.md](QUICKREF.md).

## Example Workflow

```bash
# 1. Fetch comments
gh api repos/codyde/sentryvibe/pulls/38/comments > comments.json

# 2. Analyze each comment
# (use Read tool to view code, validate issues)

# 3. Checkout PR branch
git fetch origin pull/38/head:fix-branch
git checkout fix-branch

# 4. Apply fix
# (use Edit tool)

# 5. Commit and push
git add .
git commit -m "fix: correct path in build script

Fixes path resolution issue identified by sentry bot.
..."
git push origin fix-branch

# 6. Return to main
git checkout main
```

For detailed real-world examples and scenarios, see [EXAMPLES.md](EXAMPLES.md).

## Success Criteria

A successful sentry-reviewer session:
- ✅ All comments analyzed and categorized
- ✅ Critical issues (severity >= 0.8) addressed or documented
- ✅ Fixes validated before committing
- ✅ Clear commit messages explain the changes
- ✅ PR updated with fixes
- ✅ Summary report provided to user
