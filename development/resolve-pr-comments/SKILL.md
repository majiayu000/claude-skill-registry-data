---
name: resolve-pr-comments
description: Orchestrate replying to multiple GitHub PR review comments in parallel. Use when the user wants to reply to multiple PR review comments or resolve all unresolved comments on a PR.
---

# Resolve PR Comments

Orchestrate replying to multiple GitHub PR review comments in parallel using the `general-purpose` subagent with focused prompts.

> **Note:** This skill uses `general-purpose` subagents (not custom agents) because custom agent types
> defined in `.claude/agents/` do not receive tool access. The `general-purpose` subagent has full
> tool access (`Tools: *`) and can execute the required `gh api` commands.

## Critical Constraints - Session Statelessness

**IMPORTANT:** You are operating in a stateless session. Each Claude Code session is isolated.

**You CANNOT:**
- Track issues across sessions
- Remember to do something later
- Follow up on tasks in the future
- Promise to handle something "in a follow-up"

**You MUST NOT say things like:**
- "I'll track this in a follow-up issue"
- "I'll remember to fix this later"
- "I'll handle this in a subsequent PR"

## PR Comment Response Decision Framework

When replying to comments, each response MUST use ONE of these options:

### Option 1: Implement Now (Preferred)
**When:** The change is small-ish and worth doing.
**Action steps:**
1. Implement the fix immediately
2. Commit the change
3. Reply to the comment with: "Fixed in commit {sha}: {brief description}"

### Option 2: Defer with Issue (Expensive)
**When:** Change is large AND worth doing AND not critical to PR.
**Action BEFORE replying:**
1. Create GitHub issue NOW: `gh issue create --title "..." --body "..."`
2. Add to same milestone as PR's issue
3. Add as sub-issue of parent ticket
**Reply format:** "Created #XYZ to track this. Not addressing in this PR because {reason}."

### Option 3: Disagree / Won't Fix
**When:** Suggestion is nitpicky, negligible, or you disagree.
**Reply format:** Professional explanation of why not addressing.
**NEVER use for:** Test failures, errors, security concerns.

## Overview

This skill automates the process of replying to multiple PR review comments by:
1. Fetching all review comments from a PR
2. Filtering for unresolved or unanswered comments (optional)
3. Spawning parallel subagents to handle each reply
4. Collecting and reporting results

## When to Use This Skill

**Use this skill when:**
- User wants to reply to multiple PR review comments at once
- User asks to "resolve all comments" on a PR
- User wants to batch-reply with similar messages (e.g., "Fixed")
- User needs to mark multiple comments as addressed

**Example user requests:**
- "Reply to all unresolved comments on PR #300"
- "Mark all review comments as fixed"
- "Reply to comments 123, 456, and 789 on this PR"
- "Resolve all pending review feedback"

## Prerequisites

**Before using this skill:**
1. Ensure the `gh` CLI is authenticated with proper permissions
2. Verify the repository and PR exist
3. Have the reply text prepared (or a strategy for generating replies)

**Permissions required:**
- Read access to PR comments
- Write access to post comment replies

## Workflow

### Step 1: Identify the PR

Determine which PR to work with:
- If user provides PR number, use that
- If in a PR context (e.g., PR comment in GitHub Actions), extract from context
- Otherwise, ask the user for the PR number

### Step 2: Fetch PR Review Comments

Use the GitHub API to fetch all review comments:

```bash
# IMPORTANT: Use --paginate to get ALL comments (default page size is 30)
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments --paginate \
  --jq '.[] | {id: .id, body: .body, user: .user.login, in_reply_to_id: .in_reply_to_id}'
```

**What this returns:**
- `id`: Comment ID (needed for replying)
- `body`: Comment text
- `user`: Who posted the comment
- `in_reply_to_id`: null if top-level comment, otherwise ID of parent comment

### Step 3: Filter Comments (Optional)

Depending on user requirements, filter the comments:

**Unresolved comments** (no replies yet):
- First, filter for comments where `in_reply_to_id` is null (top-level comments)
- For each top-level comment, check if there are any other comments where `in_reply_to_id` equals this comment's `id`
- If no such child comments exist, then the top-level comment is unresolved

**Specific comments:**
- If user provides comment IDs, only process those

**All comments:**
- Process every comment in the PR

### Step 4: Prepare Reply Content

Determine what to reply with:
- **User-provided text**: If user specifies reply text, use it for all comments
- **Per-comment text**: If user provides mapping of comment → reply text
- **Generated text**: Generate appropriate replies based on comment content
- **Interactive**: Ask user for reply text for each comment (not recommended for many comments)

### Step 5: Spawn Parallel Subagents

For each comment to reply to, spawn a `general-purpose` subagent with a focused prompt:

**Important:** Use a SINGLE message with MULTIPLE Task tool calls to spawn agents in parallel:

> **Note:** The following is conceptual pseudo-code showing the general pattern.
> The actual Task tool invocation syntax may differ based on the specific implementation.

```
# Example pseudo-code structure
# Send ONE message with multiple tool uses:

Task(
  subagent_type="general-purpose",
  description="Reply to comment 2565891355",
  prompt="""
    Execute this EXACT command to reply to a GitHub PR comment:

    gh api repos/{owner}/{repo}/pulls/300/comments \
      -f body="Fixed in commit abc123" \
      -F in_reply_to=2565891355

    Report success or failure. Do NOT ask questions or do anything else.
  """,
  model="haiku"
)

Task(
  subagent_type="general-purpose",
  description="Reply to comment 2565891356",
  prompt="""
    Execute this EXACT command to reply to a GitHub PR comment:

    gh api repos/{owner}/{repo}/pulls/300/comments \
      -f body="Fixed in commit abc123" \
      -F in_reply_to=2565891356

    Report success or failure. Do NOT ask questions or do anything else.
  """,
  model="haiku"
)

# ... more Task calls in the same message
```

**Key points:**
- All Task calls must be in a SINGLE message for parallel execution
- Each subagent handles one comment reply independently
- Use Haiku model for cost efficiency and speed
- Use `general-purpose` subagent type (has full tool access)
- Provide the EXACT `gh api` command to execute - be explicit to avoid ambiguity

### Step 6: Collect Results

After all subagents complete:
- Parse each subagent's response
- Count successes and failures
- Identify which comments failed (if any)
- Provide summary to user

### Step 7: Report to User

Provide a comprehensive report:
```
Replied to 8/10 comments on PR #300:

✅ Succeeded (8):
  - Comment 2565891355: "Fixed in commit abc123"
  - Comment 2565891356: "Fixed in commit abc123"
  - ... (list all successful replies)

❌ Failed (2):
  - Comment 2565891999: Error 404 - Comment not found
  - Comment 2565892000: Error 403 - Permission denied

Summary: Successfully replied to 8 out of 10 comments.
```

## Example Usage Scenarios

### Scenario 1: Resolve All Unresolved Comments

**User request:** "Reply to all unresolved comments on PR #300 with 'Fixed'"

**Workflow:**
1. Fetch all comments from PR #300
2. Build a map of parent → children relationships by iterating over all comments and recording which comments have their `in_reply_to_id` set to another comment's `id`
3. Filter for comments where `in_reply_to_id` is null (top-level) and the comment's `id` does not appear as a parent in the map (i.e., no other comment references it as a parent)
4. For each unresolved comment, spawn subagent to reply with "Fixed"
5. Report results

### Scenario 2: Reply to Specific Comments

**User request:** "Reply to comments 123, 456, and 789 on PR #300 with 'Addressed'"

**Workflow:**
1. No need to fetch all comments (user provided specific IDs)
2. For each comment ID (123, 456, 789), spawn subagent to reply with "Addressed"
3. Report results

### Scenario 3: Custom Replies Per Comment

**User request:** "Reply to PR #300 comments with these responses:
- Comment 123: 'Fixed in v2.0'
- Comment 456: 'This is working as intended'
- Comment 789: 'Good catch, resolved'"

**Workflow:**
1. Parse user's comment → reply mapping
2. For each comment, spawn subagent with the specific reply text
3. Report results

### Scenario 4: Context-Aware Replies

**User request:** "Read all unresolved comments on PR #300 and reply with appropriate responses"

**Workflow:**
1. Fetch all unresolved comments
2. For each comment, analyze the content
3. Generate appropriate reply based on comment context
4. Spawn subagents with generated replies
5. Report results

## Best Practices

### Batching

**Optimal batch sizes:**
- Small PRs (< 10 comments): Process all at once
- Medium PRs (10-50 comments): Process all, but use Haiku model for speed
- Large PRs (> 50 comments): Consider asking user which comments to prioritize

### Error Handling

**Graceful degradation:**
- If some replies fail, still report successes
- Provide actionable error messages for failures
- Offer to retry failed comments

**Common errors:**
- 404: Comment or PR doesn't exist → Verify comment ID
- 403: Permission denied → Check repository access
- 422: Invalid parameters → Verify comment ID format

### Rate Limiting

**GitHub API rate limits:**
- GitHub API has rate limits (typically 5000 requests/hour for authenticated users)
- Each reply is one API request
- For very large batches (> 100 comments), consider warning user about rate limits

### User Confirmation

**Before mass-replying:**
- Show user which comments will be replied to
- Show the reply text that will be used
- Ask for confirmation before proceeding

**Example confirmation:**

> **Display rule:** Show the first 5 comments in detail. If more than 5 total, show "and X more" for the remainder.

```
About to reply to 15 unresolved comments on PR #300 with: "Fixed in commit abc123"

Comments to reply to:
  1. Comment 2565891355: "This function doesn't handle null values"
  2. Comment 2565891356: "Missing error handling here"
  3. Comment 2565891357: "Consider using a const here"
  4. Comment 2565891358: "Typo in variable name"
  5. Comment 2565891359: "This could be simplified"
  ... and 10 more

Proceed? (yes/no)
```

## Integration with Other Tools

### With GitHub CLI (`gh`)

This skill heavily uses `gh` CLI:
- `gh api`: For fetching and posting comments
- `gh pr view`: For PR context
- `gh repo view`: For repository information

### With SlashCommands

The `/gh-pr-comment-reply` slash command is available for single comment replies when not using parallel subagents.

### With Other Skills

**Combine with:**
- `github-issue-breakdown`: For managing PR-related issues
- `gh-sub-issue`: For tracking comment resolution as sub-tasks
- `update-github-issue-project-status`: For updating project boards after resolving comments

## Troubleshooting

### Subagents Not Spawning in Parallel

**Cause:** Multiple messages sent instead of one message with multiple Task calls

**Solution:** Ensure all Task tool calls are in a SINGLE response message

### Subagent Has No Tool Access

**Cause:** Using a custom `subagent_type` that doesn't have tools configured

**Solution:** Use `subagent_type="general-purpose"` which has full tool access (`Tools: *`)

### GitHub API Authentication Errors

**Cause:** `gh` CLI not authenticated or lacks permissions

**Solution:**
```bash
# Check authentication
gh auth status

# Re-authenticate with required scopes
gh auth refresh -s repo
```

### Comment IDs Not Found

**Cause:** Using wrong endpoint or stale comment IDs

**Solution:**
- Fetch fresh comment list from GitHub API
- Verify PR number is correct
- Check that comments haven't been deleted

### Permission Denied Errors

**Cause:** No write access to repository

**Solution:**
- Verify repository access: `gh repo view`
- Check if PR is from a fork (forks have different permissions)
- Ensure authenticated user has write access

## Environment Requirements

**Prerequisites:**
- `gh` CLI installed and authenticated
- Write access to repository
- PR must exist and be accessible

**Verification:**
```bash
# Check gh CLI
gh --version

# Check authentication
gh auth status

# Test API access
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments --paginate --jq 'length'
```

## Command Reference

### Fetch All PR Comments

```bash
# IMPORTANT: Use --paginate to get ALL comments (default page size is 30)
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments --paginate
```

Returns array of comment objects.

### Fetch Specific Comment

```bash
gh api repos/{owner}/{repo}/pulls/comments/{comment_id}
```

Returns single comment object.

### Post Reply to Comment

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments \
  -f body="Reply text" \
  -F in_reply_to={comment_id}
```

Returns the created comment object.

### Get Comment Thread

To find all replies to a comment:
```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments --paginate \
  --jq '.[] | select(.in_reply_to_id == COMMENT_ID)'
```

> **Note:** Replace `COMMENT_ID` with the actual numeric comment ID.

## See Also

- **gh-pr-comment-reply** - Slash command for single comment replies (`.claude/commands/gh-pr-comment-reply.md`)
- **GitHub API Documentation** - https://docs.github.com/rest/pulls/comments
- **gh CLI Documentation** - https://cli.github.com/manual/

## Implementation Notes

### Why `general-purpose` Instead of Custom Subagent?

Custom agent types defined in `.claude/agents/` do **not** receive tool access from YAML frontmatter.
The `tools:` field in agent markdown files is documentation only, not actual configuration.

When spawning a custom subagent via the Task tool, it appears with `(Tools: )` - empty tool access.
Without tools, the subagent cannot execute `gh api` commands.

The `general-purpose` subagent type has `(Tools: *)` - full tool access - making it suitable for
executing GitHub API commands. By using focused prompts that specify exact commands, we get the
same behavior as a custom subagent but with working tool access.
