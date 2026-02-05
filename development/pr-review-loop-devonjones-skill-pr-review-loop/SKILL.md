---
name: pr-review-loop
description: |
  Manage the PR review feedback loop: monitor CI checks, fetch review comments, and iterate on fixes.
  Use when: (1) pushing changes to a PR and waiting for CI/reviews, (2) user says "new reviews available",
  (3) iterating on PR feedback from Gemini, Cursor, Claude, or other reviewers, (4) monitoring PR status.

  Supports multiple review bots: Gemini Code Assist, Cursor Bugbot, and Claude agent fallback.
  Automatically detects priority levels from different bot formats and handles rate limits.

  RECOMMENDED: Spawn a Task agent (subagent_type: general-purpose) to execute the review loop autonomously.
  See "Recommended Usage: Run as Task Agent" section for the prompt template.

  CRITICAL: When using this skill, NEVER use raw git commit/push commands. ALWAYS use commit-and-push.sh script.
  The user has NOT granted permission for raw git commands - only the script is allowed.
---

# PR Review Loop

## ⛔ STOP - READ THIS FIRST ⛔

**YOU DO NOT HAVE PERMISSION TO USE RAW GIT COMMANDS.**

| ❌ FORBIDDEN | ✅ USE INSTEAD |
|--------------|----------------|
| `git commit` | `~/.claude/skills/pr-review-loop/scripts/commit-and-push.sh "msg"` |
| `git commit -m "..."` | `~/.claude/skills/pr-review-loop/scripts/commit-and-push.sh "msg"` |
| `git push` | `~/.claude/skills/pr-review-loop/scripts/commit-and-push.sh "msg"` |
| `git push origin` | `~/.claude/skills/pr-review-loop/scripts/commit-and-push.sh "msg"` |

**If you use `git commit` or `git push` directly, it will be BLOCKED.**

---

## ⭐ Recommended Usage: Run as Task Agent

**The PR review loop should be executed as a background Task, not in the main conversation.**

When the user creates a PR or wants to iterate on reviews, spawn a Task agent to handle the loop autonomously:

```yaml
Task tool:
  subagent_type: general-purpose
  model: sonnet
  description: PR review loop for #<PR>
  prompt: |
    Execute the PR review feedback loop for PR #<PR>.

    The autonomous loop workflow:
    1. Get summary of comments: scripts/summarize-reviews.sh <PR>
    2. Check for unresolved comments: scripts/get-review-comments.sh <PR> --with-ids --wait
    3. For EACH comment: evaluate critically, fix if worthwhile, ALWAYS reply with scripts/reply-to-comment.sh <PR> <comment-id> "Fixed - [description]" or "Won't fix - [reason]"
    4. Commit and push: scripts/commit-and-push.sh "fix: address review comments" (NEVER use raw git commands)
    5. Trigger next review: scripts/trigger-review.sh <PR> --wait
    6. Repeat steps 1-5 until no new unresolved comments
    7. Do ONE MORE verification loop - if no actionable feedback, you're done
    8. Report back when ready to merge or if user input is needed

    Critical rules:
    - ALWAYS use commit-and-push.sh, NEVER git commit/push
    - ALWAYS reply to every comment using reply-to-comment.sh
    - ALWAYS use --wait flags when polling for reviews (5min timeout)
    - Be skeptical of review suggestions - not all should be implemented
    - Track state with TodoWrite (especially "final verification loop" todo)
```

This keeps the main conversation clean while the agent autonomously handles the review cycles.

---

Streamline the push-review-fix cycle for PRs with automated reviewers.

## Supported Review Bots

| Bot | Trigger | Priority Format |
|-----|---------|-----------------|
| **Gemini Code Assist** | `/gemini review` comment | `![critical]`, `![high]`, `![medium]`, `![low]` |
| **Cursor Bugbot** | Auto on push | `<!-- **High Severity** -->`, `### Bug:` |
| **Claude** | Manual via script | `**Critical**`, `### Critical Issues` |

Priority detection automatically parses all formats when summarizing and fetching comments.

## Critical: Be Skeptical of Reviews

**Not all suggestions are good.** Evaluate each review comment critically:

- Does this actually improve the code, or is it pedantic?
- Is this suggestion appropriate for the project's context?
- Would implementing this introduce unnecessary complexity?

**Skip suggestions that are:**
- Platform-specific when not applicable (Windows comments for Linux-only code)
- Overly defensive (excessive null checks, unlikely edge cases)
- Stylistic preferences that don't match project conventions
- Adding documentation for self-explanatory code

When in doubt, ask the user rather than blindly applying changes.

## Diminishing Returns Detection

Track review cycles. After 2-3 iterations, evaluate:
- Are new comments addressing real issues or nitpicks?
- Are we fixing the same type of issue repeatedly?
- Is the reviewer finding fewer/lower-priority issues?

**ONE MORE LOOP rule**: When you reach a point where there are no unresolved comments (or only "Won't fix" responses), do ONE additional review cycle to catch any final feedback Gemini may have held back.

**Tracking state**: Use TodoWrite to track whether you're in the "final verification loop". Create a todo like "Final verification loop - if no actionable feedback, ready to merge".

**Reset condition**: If the final verification loop produces feedback you actually fix (not just "Won't fix"), remove the "final verification loop" todo - you need a fresh "one more" after pushing those fixes.

**Exit condition**: If the "final verification loop" todo exists AND you get no actionable feedback (only nitpicks/won't-fix responses), you're done - ask about merge.

**After the final loop**, ask the user: "We've completed the review cycles. Ready to merge, or want to address more?"

## Autonomous Loop Workflow

**CRITICAL RULES - NEVER VIOLATE THESE:**
1. **ALWAYS use `commit-and-push.sh`** - NEVER `git commit` or `git push` (see table at top of document)
2. **ALWAYS reply to EVERY comment** using `reply-to-comment.sh` - never leave a comment without a reply
3. **ALWAYS use `--wait` flag** when checking for comments - this ensures proper 5-minute polling
4. **PR creation automatically triggers Gemini review** - use `get-review-comments.sh --wait` to wait for the first review

### The Loop

```
1. Get unresolved comments (use --wait to poll for up to 5 minutes)
2. For EACH comment: fix OR decide to skip, then REPLY using reply-to-comment.sh
3. Use commit-and-push.sh (NEVER raw git commands)
4. Trigger next review with --wait: trigger-review.sh <PR> --wait
5. Go to step 1
6. When no new unresolved: do ONE MORE loop, then ask user about merge
```

### Step-by-step

**1. Check for unresolved comments (ALWAYS use --wait for first check after PR creation or push):**
```bash
~/.claude/skills/pr-review-loop/scripts/summarize-reviews.sh <PR>
~/.claude/skills/pr-review-loop/scripts/get-review-comments.sh <PR> --with-ids --wait
```
The `--wait` flag polls every 30s for up to 5 minutes, waiting for Gemini to respond. Do NOT skip this or use a shorter timeout.

**2. For EACH unresolved comment (MANDATORY - never skip this):**
- Evaluate if suggestion is worthwhile
- Apply fix locally OR decide to skip
- **ALWAYS reply using the script** - this resolves the thread:
```bash
~/.claude/skills/pr-review-loop/scripts/reply-to-comment.sh <PR> <comment-id> "Fixed - description"
# OR
~/.claude/skills/pr-review-loop/scripts/reply-to-comment.sh <PR> <comment-id> "Won't fix - reason"
```

**3. Commit and push (ALWAYS use the script, NEVER raw git):**
```bash
~/.claude/skills/pr-review-loop/scripts/commit-and-push.sh "fix: description"
```
This script runs pre-commit, commits with proper footer, and pushes.

**4. Trigger next review and wait for response:**
```bash
~/.claude/skills/pr-review-loop/scripts/trigger-review.sh <PR> --wait
```
The `--wait` flag polls for up to 5 minutes until new comments appear. Do NOT use sleep or manual polling.

**5. When new reviews detected, go to step 1**

## Reply Templates

**ALWAYS reply to every comment using `reply-to-comment.sh`.** Use these templates:
- Fixed: "Fixed - [description]"
- Won't fix: "Won't fix - [reason]"
- Deferred: "Good catch, tracking in #issue"
- Acknowledged: "Acknowledged - [explanation]"

## Triggering Reviews by Bot Type

### Gemini Code Assist (Default)
```bash
~/.claude/skills/pr-review-loop/scripts/trigger-review.sh <PR> --gemini --wait
```
Gemini has a daily quota. When exceeded, the skill automatically detects this and suggests alternatives.

### Cursor Bugbot
```bash
~/.claude/skills/pr-review-loop/scripts/trigger-review.sh <PR> --cursor --wait
```
Cursor auto-reviews on push, so `--cursor` just waits for comments to appear (typically 1-2 minutes).

### Claude Agent (Fallback)
```bash
~/.claude/skills/pr-review-loop/scripts/trigger-review.sh <PR> --claude
```
Uses a Claude agent to review the PR and post comments. Useful when:
- Gemini is rate-limited
- You want a different perspective
- Cursor isn't configured on the repo

### Claude Review Workflow

When using Claude fallback:

1. **Run the script to get the prompt:**
   ```bash
   ~/.claude/skills/pr-review-loop/scripts/claude-review.sh <PR>
   ```

2. **Use the Task tool with the generated prompt:**
   ```
   Task tool:
     subagent_type: general-purpose
     description: Review PR #<PR>
     prompt: (copy from /tmp/claude_review_prompt_<PR>.txt)
   ```

3. **The agent will post the review as a PR comment**

4. **Continue the normal review loop** - address comments using `reply-to-comment.sh`

## Rate Limit Detection

The scripts automatically detect Gemini quota limits by checking for:
> "You have reached your daily quota limit"

When detected, the script suggests:
1. Use Cursor if available: `--cursor --wait`
2. Use Claude fallback: `--claude`

## Scripts

| Script | Purpose |
|--------|---------|
| `commit-and-push.sh "msg"` | **ALWAYS USE** - Never use raw git commit/push |
| `reply-to-comment.sh <PR> <id> "msg"` | **ALWAYS USE** - Reply and auto-resolve every comment |
| `get-review-comments.sh <PR> [--with-ids] [--wait]` | **USE --wait** - Fetch comments, polls 5min if --wait |
| `trigger-review.sh [PR] [--gemini\|--cursor\|--claude] [--wait]` | **USE --wait** - Trigger review and poll for response |
| `summarize-reviews.sh <PR> [--all]` | Summary of unresolved by priority/file |
| `watch-pr.sh <PR>` | Background monitor (optional, for long-running watches) |
| `claude-review.sh <PR>` | Generate Claude agent prompt for code review |
| `check-gemini-quota.sh <PR>` | Check if Gemini is rate-limited |
| `resolve-comment.sh <node-id> [reason]` | Manually resolve a thread |

## Permission Setup

To enable autonomous loops, user should grant access:
```
Bash(~/.claude/skills/pr-review-loop/scripts/commit-and-push.sh:*)
Bash(~/.claude/skills/pr-review-loop/scripts/reply-to-comment.sh:*)
Bash(~/.claude/skills/pr-review-loop/scripts/trigger-review.sh:*)
```

## Prerequisites

- `gh` CLI authenticated
- `pre-commit` (optional) - If `.pre-commit-config.yaml` exists in the repo, pre-commit will be run.
  If pre-commit is not installed, a warning is shown but commits proceed.
  Install with: `pip install pre-commit && pre-commit install`
