---
name: pr-feedback-workflow
description: Process all PR feedback in one pass. Fetches review comments and CI failures together, creates a unified action plan, applies fixes, replies to reviewers, resolves threads, and posts a summary. Use when asked to address PR feedback, fix review comments, handle CI failures, or process PR reviews. Works on the current branch's open PR.
---

# PR Feedback Workflow

Gather all PR feedback (review comments + CI failures), plan holistically, then execute.

## Phase 1: Gather Context

Run both scripts to collect all feedback:

```bash
scripts/load-pr-feedback.sh
```

This fetches:
- PR number, title, and current branch
- All review comments with thread IDs
- All review threads (resolved and unresolved)
- Latest CI/CD run status and failure logs (if any)

## Phase 2: Analyse

For each piece of feedback (conversation comments, code review comments, CI failures), categorise:

| Category | Action |
|----------|--------|
| **Code fix required** | Note the file, change needed, and which comments/CI failures it addresses |
| **No change needed** | Prepare explanation for reviewer |
| **Out of scope** | Prepare to create a new issue and link it |
| **CI-only failure** | Note the fix needed (may overlap with review comments) |
| **General question/discussion** | Prepare appropriate response |

Look for overlaps where one fix addresses multiple items.

Note the comment type (conversation vs review) as they use different reply mechanisms.

## Phase 3: Create Unified Plan

Before making changes, output a plan:

1. Code changes to make (grouped by file)
2. Which review comments each change addresses
3. Which CI failures each change fixes
4. Comments that need explanation-only replies
5. Out-of-scope items to convert to issues

Ask: "Ready to execute this plan?"

Wait for confirmation.

## Phase 4: Execute

### 1. Apply code fixes

Make all code changes, then commit:

```bash
git add -A
git commit -m "Address PR feedback

- [summary of changes]
- Fixes review comments from @reviewer
- Resolves CI failure in [workflow]"
git push
```

### 2. Reply to comments

**For code review comments** (attached to specific lines):

```bash
gh api repos/{owner}/{repo}/pulls/comments/{comment_id}/replies \
  -f body="✅ Fixed: [description of change]"
```

**For PR conversation comments** (general discussion):

```bash
gh pr comment {PR_NUMBER} -b "Replying to @{author}: [response]"
```

Reply templates:
- Fix applied: `✅ Fixed: [what was changed]`
- No change needed: `ℹ️ No change required: [explanation]`
- Out of scope: `📝 Good suggestion, tracked as #[issue_number]`
- Acknowledgement: `👍 Thanks for the feedback, [response]`

### 3. Create issues for out-of-scope items

```bash
gh issue create \
  -t "Enhancement: [title]" \
  -b "Suggested during PR review of #[PR_NUMBER].

## Context
[Original comment]

## Suggested approach
[Implementation ideas]"
```

### 4. Resolve review threads

Use the helper script:

```bash
scripts/resolve-thread.sh <THREAD_ID>
```

Or manually via GraphQL:

```bash
gh api graphql -f query='
  mutation {
    resolveReviewThread(input: {threadId: "<THREAD_ID>"}) {
      thread { id isResolved }
    }
  }'
```

### 5. Verify CI passes

Wait for CI to complete after pushing:

```bash
gh run watch
```

If still failing, repeat analysis on new logs.

## Phase 5: Summarise and Approve

Post a summary comment and approve:

```bash
gh pr comment -b "## PR Feedback Summary

### Review Comments
- ✅ X comments addressed with code changes
- ℹ️ Y comments resolved with explanations  
- 📝 Z suggestions tracked as new issues

### CI/CD
- [Status of workflow runs]

### Changes Made
- [List of commits/changes]

All feedback has been addressed."

gh pr review --approve -b "All review comments addressed and CI passing."
```

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/load-pr-feedback.sh` | Fetches PR comments, threads, and CI status |
| `scripts/resolve-thread.sh` | Resolves a review thread by ID |
