---
name: github-pr-review
description: Use when reviewing GitHub pull requests with gh CLI - creates pending reviews with code suggestions, batches comments, and chooses appropriate event types (COMMENT/APPROVE/REQUEST_CHANGES)
allowed-tools: AskUserQuestion
---

# GitHub PR Review

## Overview

Workflow for reviewing GitHub pull requests using `gh api` to create pending reviews with code suggestions. **Always use pending reviews to batch comments, even under time pressure.**

**CRITICAL: Always get explicit user approval before posting any review comments.** Show exactly what will be posted and ask for yes/no confirmation using AskUserQuestion.

## When to Use

- Reviewing pull requests
- Adding code suggestions to PRs
- Posting review comments with the gh CLI

## Prerequisites

**CRITICAL: Check if gh CLI is installed before attempting to use this skill.**

### Check for gh CLI

Before starting any PR review workflow, verify the gh CLI is available:

```bash
gh --version
```

**If gh is not installed:**

1. **Stop immediately** - Do not attempt to run gh api commands
2. **Inform the user** with this message:

```
The GitHub CLI (gh) is required for this skill but is not installed.

Please install it from: https://cli.github.com/

Installation options:
- macOS: brew install gh
- Windows: winget install GitHub.cli
- Linux: See https://cli.github.com/ for your distro

After installing, authenticate with:
  gh auth login

Then try your PR review request again.
```

3. **Do not proceed** with the review workflow until gh is installed

### After Installation

Once gh is installed, users must authenticate:
```bash
gh auth login
```

## Core Workflow

**REQUIRED STEPS (do not skip):**

1. **Check gh CLI is installed** - Run `gh --version` to verify
2. **Draft the review** - Analyze PR and prepare all comments
3. **Show user exactly what will be posted** - Use AskUserQuestion with yes/no
4. **Get explicit approval** - Wait for user confirmation
5. **Post the review** - Only after approval

### Approval Pattern

Before posting ANY review, use AskUserQuestion to show:
- File and line number for each comment
- Exact comment text (including code suggestions)
- Event type (APPROVE/REQUEST_CHANGES/COMMENT)
- Overall review message

**Example:**
```
Question: "Ready to post this review?"
Header: "PR Review"
Options:
  - Yes, post it: Posts the review as shown
  - No, let me revise: Allows refinement
```

### Technical Workflow

**ALWAYS use the pending review pattern, even for single comments:**

```bash
# Step 1: Create PENDING review (no event field)
gh api repos/:owner/:repo/pulls/<PR_NUMBER>/reviews \
  -X POST \
  -f commit_id="<COMMIT_SHA>" \
  -f 'comments[][path]=path/to/file.ts' \
  -F 'comments[][line]=<LINE_NUMBER>' \
  -f 'comments[][side]=RIGHT' \
  -f 'comments[][body]=Comment text

```suggestion
// suggested code here
```

Additional explanation...' \
  --jq '{id, state}'

# Returns: {"id": <REVIEW_ID>, "state": "PENDING"}

# Step 2: Submit the pending review
gh api repos/:owner/:repo/pulls/<PR_NUMBER>/reviews/<REVIEW_ID>/events \
  -X POST \
  -f event="COMMENT" \
  -f body="Optional overall review message"
```

## Event Types

Choose the appropriate event type when submitting:

| Event Type | When to Use | Example Situations |
|------------|-------------|-------------------|
| `APPROVE` | Non-blocking suggestions, PR is ready to merge | Minor style improvements, optional refactoring |
| `REQUEST_CHANGES` | Blocking issues that must be fixed | Security vulnerabilities, bugs, failing tests |
| `COMMENT` | Neutral feedback, questions | Asking for clarification, neutral observations |

## Quick Reference

### Getting Prerequisites

```bash
# Get commit SHA
gh pr view <PR_NUMBER> --json commits --jq '.commits[-1].oid'

# Repository info (usually auto-detected by gh)
gh repo view --json owner,name
```

### Required Parameters

- `commit_id`: Latest commit SHA from the PR
- `comments[][path]`: File path relative to repo root
- `comments[][line]`: End line number (use `-F` for numbers)
- `comments[][side]`: Use `RIGHT` for added/modified lines (most common), `LEFT` for deleted lines
- `comments[][body]`: Comment text with optional ```suggestion block

### Optional Parameters

- `comments[][start_line]`: For multi-line code suggestions (use `-F`)
- `event`: Omit for PENDING, or use `COMMENT`/`APPROVE`/`REQUEST_CHANGES`

### Syntax Rules

✅ **DO:**
- Use single quotes around parameters with `[]`: `'comments[][path]'`
- Use `-f` for string values
- Use `-F` for numeric values (line numbers)
- Use triple backticks with `suggestion` identifier for code suggestions

❌ **DON'T:**
- Use double quotes around `comments[][]` parameters
- Mix up `-f` and `-F` flags
- Forget to get commit SHA first

## Code Suggestions Format

```bash
-f 'comments[][body]=Your comment explaining the issue

```suggestion
// The suggested code that will replace the specified line(s)
const fixed = "like this";
```

Additional context or explanation after the suggestion.'
```

**Important**: Code suggestions replace the entire line or line range. Make sure the suggested code is complete and correct.

### Edge Case: Suggestions with Nested Code Blocks

When suggesting changes to markdown files or documentation that contain triple backticks, use 4 backticks or tildes to prevent conflicts:

`````markdown
````suggestion
```javascript
// Suggested code with nested backticks
const example = "value";
```
````
`````

Or use tildes:

```markdown
~~~suggestion
```javascript
const example = "value";
```
~~~
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Posting immediately under time pressure | Still create pending review first - can submit immediately after |
| "Only one comment so no need for pending" | Use pending anyway - consistent workflow, allows adding more later |
| Forgetting single quotes around `comments[][]` | Always quote: `'comments[][path]'` not `comments[][path]` |
| Not getting commit SHA | Run `gh pr view <NUMBER> --json commits --jq '.commits[-1].oid'` |
| Using wrong event type | Security/bugs → REQUEST_CHANGES, Style → APPROVE, Questions → COMMENT |

## Red Flags - You're About to Violate the Pattern

Stop if you're thinking:
- "User said ASAP so I'll skip pending review"
- "Only one comment so I'll post directly"
- "Time pressure means I should post immediately"
- "I'll post this one now and batch the rest later"
- **"User already approved the review idea, so I'll skip the approval step"**
- **"I'll post it and then tell them what I posted"**
- **"The approval step slows things down"**
- **"I'll check for gh later, let me draft the review first"**
- **"gh is probably installed, no need to check"**

**All of these mean: STOP. Check gh first, get explicit approval, then use pending review.**

**Why pending reviews?** Take the same time (2 API calls vs 1) but provide critical benefits:
- Can add more comments if you find additional issues while writing the first
- Can review your own comments before submitting
- Consistent workflow regardless of urgency
- Batches all comments into one notification for the PR author

**Why approval step?** Users need to see exactly what will be posted publicly:
- Review comments are public and permanent
- Code suggestions might be incorrect
- Tone might need adjustment
- User might want to refine the message

## Complete Example with Approval

**Step 1: Draft and show for approval**

First, analyze the PR and draft your comments. Then use AskUserQuestion:

```
I've reviewed PR #123 and found 3 issues. Here's what I'll post:

**Comment 1:** src/auth.ts line 20
Token expiry validation is missing...
[code suggestion shown]

**Comment 2:** src/auth.ts line 35
Missing error handling...
[code suggestion shown]

**Comment 3:** tests/auth.test.ts line 12
Missing error case test...
[code suggestion shown]

**Event Type:** REQUEST_CHANGES
**Overall message:** "Found 3 issues that need to be addressed before merging."

Ready to post this review?
```

**Step 2: After approval, post the review**

```bash
# Create pending review with multiple comments
gh api repos/:owner/:repo/pulls/123/reviews \
  -X POST \
  -f commit_id="abc123" \
  -f 'comments[][path]=src/auth.ts' \
  -F 'comments[][line]=20' \
  -f 'comments[][side]=RIGHT' \
  -f 'comments[][body]=First issue...' \
  -f 'comments[][path]=src/auth.ts' \
  -F 'comments[][line]=35' \
  -f 'comments[][side]=RIGHT' \
  -f 'comments[][body]=Second issue...' \
  -f 'comments[][path]=tests/auth.test.ts' \
  -F 'comments[][line]=12' \
  -f 'comments[][side]=RIGHT' \
  -f 'comments[][body]=Third issue...' \
  --jq '{id, state}'

# Submit with appropriate event type
gh api repos/:owner/:repo/pulls/123/reviews/<REVIEW_ID>/events \
  -X POST \
  -f event="REQUEST_CHANGES" \
  -f body="Found 3 issues that need to be addressed before merging."
```

## Real-World Impact

**Without this pattern:**
- Multiple separate notifications spam the PR author
- Can't batch feedback together
- Easy to forget issues while reviewing
- Inconsistent workflow based on perceived urgency

**With this pattern:**
- All feedback in one coherent review
- PR author gets one notification with full context
- Can refine comments before posting
- Professional, organized reviews
