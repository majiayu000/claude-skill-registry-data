---
name: pr-review-fix
description: Start a PR review inline comments fixing session. Use when users want to address, fix, or resolve inline review comments on a GitHub PR. Fetches unresolved comments and helps fix each one systematically.
user_invocable: true
---

# PR Review Inline Comments Fixing Session

## Overview

This skill starts an interactive session to systematically address and fix inline review comments on a GitHub Pull Request. It uses the `gh pr-review` extension to fetch unresolved comments and guides you through fixing each one.

## Prerequisites

- `gh` CLI must be installed and authenticated
- `gh pr-review` extension must be installed (`gh extension install agynio/gh-pr-review`)

## Workflow

### Step 1: Identify the PR

First, determine the PR number. Check if the current branch has an associated PR:

```bash
gh pr view --json number,title,url 2>/dev/null
```

If no PR is found, ask the user for the PR number.

### Step 2: Fetch Unresolved Review Comments

Use the `gh pr-review` extension to get all unresolved review threads:

```bash
gh pr-review review view --pr <PR_NUMBER> --unresolved --not_outdated
```

This returns a hierarchical view of all review threads with:
- File path and line numbers
- Original comment body
- Any replies in the thread
- Thread IDs for resolution

### Step 3: Process Each Comment

For each unresolved comment:

1. **Show the comment context:**
   - Display the file path, line number(s), and comment body
   - Show any follow-up replies in the thread

2. **Read the relevant code:**
   - Read the file at the specified location
   - Show surrounding context (5-10 lines before and after)

3. **Understand the issue:**
   - Analyze what the reviewer is asking for
   - Determine if it's a bug fix, style change, refactor, clarification, etc.

4. **Propose a fix:**
   - Suggest code changes that address the reviewer's feedback
   - Explain the reasoning behind the fix

5. **Apply the fix:**
   - After user approval, edit the file to implement the fix

6. **Ask about resolution:**
   - Ask if the user wants to resolve the thread
   - If yes, resolve it using: `gh pr-review threads resolve --thread-id <THREAD_ID> --pr <PR_NUMBER>`

### Step 4: Summary

After processing all comments:
- Summarize what was fixed
- List any comments that were skipped or need follow-up
- Remind user to commit changes if any were made

## Commands Reference

### View all unresolved comments
```bash
gh pr-review review view --pr <NUMBER> --unresolved --not_outdated
```

### View comments from a specific reviewer
```bash
gh pr-review review view --pr <NUMBER> --reviewer <login> --unresolved
```

### List threads (alternative view)
```bash
gh pr-review threads list --unresolved --pr <NUMBER>
```

### Resolve a thread
```bash
gh pr-review threads resolve --thread-id <THREAD_ID> --pr <NUMBER>
```

### Reply to a thread
```bash
gh pr-review comments reply --thread-id <THREAD_ID> --body "<message>" --pr <NUMBER>
```

## Example Session Flow

```
User: /pr-review-fix

Claude: I'll help you fix inline review comments. Let me check your current PR...

[Runs: gh pr view --json number,title,url]

Found PR #42: "Add user authentication"

Fetching unresolved review comments...

[Runs: gh pr-review review view --pr 42 --unresolved --not_outdated]

Found 3 unresolved comments:

---
**Comment 1 of 3** (Thread: PRRT_abc123)
File: src/auth/login.ts:25-28
Reviewer: @senior-dev

> This should handle the case where the user doesn't exist. Currently it will throw an unhandled error.

Let me read the relevant code...

[Shows code context]

**Proposed fix:** Add a try-catch block and return a proper error response when user is not found.

Should I apply this fix? [yes/no]

User: yes

[Applies edit]

Fix applied! Should I resolve this thread? [yes/no]

User: yes

[Resolves thread]

Moving to comment 2 of 3...
```

## Tips

- Use `--not_outdated` to skip comments on code that has already been changed
- If a comment requires discussion rather than a code fix, use the reply command to respond
- Always read the full thread context before making changes
- Consider running tests after fixes: `bun run test`
