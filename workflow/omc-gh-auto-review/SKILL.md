---
name: omc-gh-auto-review
description: "Auto-review GitHub PRs where you are a requested reviewer and post AI review comments. Not for interactive review (omc-gh-review), issue triage, or Azure DevOps repos."
---

# OMC GitHub Auto Review

Automatically review GitHub pull requests where the current user is requested as a reviewer. Reads `.omg/config.json` for connection settings, discovers pending PRs, fetches diffs, spawns a code-reviewer agent to analyse changes, and posts structured inline comments back to each PR as a batched review.

**When this skill is invoked, immediately execute the workflow below. Do not only restate or summarize these instructions back to the user.**

## Trigger Patterns

- "auto review"
- "auto-review prs"
- "review my assigned prs"
- "automated pr review"
- "omc-gh-auto-review"

---

## Step 1: Load Configuration

Read `.omg/config.json`:

```bash
node -e "const f=require('fs');try{process.stdout.write(f.readFileSync('.omg/config.json','utf8'))}catch{console.log('NOT_FOUND')}"
```

Extract from the `github` key:
- `owner` — GitHub owner (org or user)
- `repo` — repository name

Also read optional `github.autoReview` settings (apply defaults when absent):

| Setting | Default | Purpose |
|---------|---------|---------|
| `severityThreshold` | `"MEDIUM"` | Minimum severity to post as inline comment |
| `autoSubmit` | `false` | Automatically submit approve/request-changes |
| `maxFilesPerReview` | `50` | Cap on number of files analysed per PR |
| `excludePatterns` | `["*.lock", "*.min.js", "*.generated.*"]` | Glob patterns for files to skip |

If config is NOT_FOUND or missing the `github` key: tell the user to run `/oh-my-copilot:omc-gh-setup` first and stop.

---

## Step 2: Find PRs Requesting My Review

```bash
gh pr list --repo {owner}/{repo} --search "review-requested:@me" --state open --json number,title,author,headRefName --limit 10 2>&1
```

Present a table of pending PRs:

```
### PRs Pending Your Review ({N})
| # | Title | Author | Branch | Age |
|---|-------|--------|--------|-----|
| #42 | Add retry logic | alice | feat/retry | 3d |
| #43 | Fix login timeout | bob | fix/login | 1d |
```

**If no PRs are found:** report "No PRs pending your review" and stop.

**If invoked with a specific PR number** (e.g. `omc-gh-auto-review 42`): skip discovery and process that PR directly, regardless of reviewer assignment.

---

## Step 3: Fetch PR Diff and Changed Files

For each PR to be reviewed:

### 3a. Fetch the unified diff

```bash
gh pr diff {prNumber} --repo {owner}/{repo} 2>&1
```

### 3b. Retrieve PR details for context

```bash
gh pr view {prNumber} --repo {owner}/{repo} --json title,body,files,headRefOid 2>&1
```

### 3c. Filter files

Parse file paths from the diff headers (lines beginning `diff --git a/`). Apply `excludePatterns` from config — skip any file whose path matches one of those glob patterns.

If the remaining file count exceeds `maxFilesPerReview`, warn the user:

```
Warning: PR #{number} touches {total} files. Reviewing first {maxFilesPerReview} by diff order.
```

Then truncate to the first `maxFilesPerReview` files.

### 3d. Read full file content

For each included file, read the full content using the Read tool to provide complete context to the reviewer agent.

---

## Step 4: Spawn Code Reviewer Agent

For each PR, spawn an `oh-my-copilot:code-reviewer` agent via the Agent tool with the following payload:

- Full unified diff of the PR
- Full content of each changed file (post-filter)
- PR title and description
- Instruction to output **only** a structured JSON findings array:

```json
[
  {
    "file": "src/auth/login.ts",
    "line": 42,
    "severity": "HIGH",
    "message": "Unhandled null return from getUser() will throw at runtime.",
    "suggestion": "Add a null check: `if (!user) return { error: 'USER_NOT_FOUND' };`"
  }
]
```

Each finding must contain:

| Field | Type | Values |
|-------|------|--------|
| `file` | string | Relative file path |
| `line` | number | Line number in the post-merge file |
| `severity` | string | `CRITICAL`, `HIGH`, `MEDIUM`, or `LOW` |
| `message` | string | What is wrong and why |
| `suggestion` | string | Concrete fix or improvement |

Parse the agent's response and extract the findings array. If parsing fails, treat the raw response as a general summary and proceed to Step 5 in summary-only mode.

---

## Step 5: Post Findings as Batched Review

Apply the `severityThreshold` filter: only post findings whose severity meets or exceeds the threshold.

Severity order (highest to lowest): `CRITICAL > HIGH > MEDIUM > LOW`

### 5a. Batch all inline comments into a single review submission

GitHub's review API allows submitting multiple inline comments as one review — this produces a single notification instead of one per comment.

Build the review payload:

```bash
gh api repos/{owner}/{repo}/pulls/{prNumber}/reviews \
  --method POST \
  -f event=COMMENT \
  -f body="{summary}" \
  --input comments.json \
  2>&1
```

Where `comments.json` contains:

```json
{
  "event": "COMMENT",
  "body": "## Code Review Summary — PR #{number}\n\n| Severity | Count |\n|----------|-------|\n| CRITICAL | {n} |\n| HIGH | {n} |\n| MEDIUM | {n} |\n| LOW | {n} |\n\n**Files reviewed:** {N} of {total}\n\n---\n*Automated review by oh-my-copilot*",
  "comments": [
    {
      "path": "src/auth/login.ts",
      "line": 42,
      "body": "**[HIGH]** Unhandled null return from getUser() will throw at runtime.\n\n**Suggestion:** Add a null check: `if (!user) return { error: 'USER_NOT_FOUND' };`\n\n---\n*Automated review by oh-my-copilot*"
    }
  ]
}
```

Format each inline comment body:

```
**[{severity}]** {message}

**Suggestion:** {suggestion}

---
*Automated review by oh-my-copilot*
```

Report progress:

```
Posted {N} inline comments on PR #{number} ({CRITICAL}C / {HIGH}H / {MEDIUM}M / {LOW}L)
```

---

## Step 6: Submit Review Decision (Optional)

Only execute this step if `autoSubmit` is `true` in config.

Determine the decision from the highest severity finding:

| Highest Severity | Decision | gh Command |
|-----------------|----------|------------|
| `CRITICAL` | Request changes | `gh pr review {n} --request-changes --body "{reason}"` |
| `HIGH` | Request changes | `gh pr review {n} --request-changes --body "{reason}"` |
| `MEDIUM` | Comment only | `gh pr review {n} --comment --body "{summary}"` |
| `LOW` or none | Approve | `gh pr review {n} --approve --body "LGTM"` |

Report:

```
Submitted review on PR #{number}: {Approved / Changes Requested / Commented}
```

If `autoSubmit` is false, inform the user of the recommended decision and let them choose.

---

## Error Handling

| Error | Action |
|-------|--------|
| `.omg/config.json` missing | Tell user to run `/oh-my-copilot:omc-gh-setup` first |
| `gh auth` required | Prompt user to authenticate; stop execution |
| No PRs for review | Report "No PRs pending your review" and stop |
| PR diff too large (>`maxFilesPerReview` files) | Warn and review first N files per `maxFilesPerReview` config |
| Code reviewer agent fails | Post summary-only comment without inline findings |
| Review submission fails (rate limit) | Wait 2s and retry once; if still failing, post as individual comments |
| Permission denied | Warn user they may need write access to review |

---

## Configuration Reference

`.omg/config.json` with optional `autoReview` section:

```json
{
  "github": {
    "owner": "RobinNorberg",
    "repo": "oh-my-copilot",
    "defaultBranch": "dev",
    "autoReview": {
      "severityThreshold": "MEDIUM",
      "autoSubmit": false,
      "maxFilesPerReview": 50,
      "excludePatterns": [
        "*.lock",
        "*.min.js",
        "*.generated.*"
      ]
    }
  }
}
```

All `autoReview` fields are optional. Defaults are applied when the key is absent.
