---
name: omc-gh-review
description: "Review GitHub pull requests: read diffs, post review comments, approve or request changes. Not for automated review (omc-gh-auto-review), issue triage, or Azure DevOps repos."
---

# OMC GitHub Review

Perform an interactive GitHub pull request review. Reads `.omg/config.json` for connection settings, lists open PRs, surfaces existing review threads, and supports reading diffs, posting comments, and submitting review decisions.

**When this skill is invoked, immediately execute the workflow below. Do not only restate or summarize these instructions back to the user.**

## Trigger Patterns

- "gh review"
- "review pr"
- "review pull request"
- "github review"
- "pr review"
- "omc-gh-review"

---

## Step 1: Load Configuration

Read `.omg/config.json`:

```bash
node -e "const f=require('fs');try{process.stdout.write(f.readFileSync('.omg/config.json','utf8'))}catch{console.log('NOT_FOUND')}"
```

Extract from the `github` key:
- `owner` — GitHub owner (org or user)
- `repo` — repository name

If config is NOT_FOUND or missing the `github` key: tell the user to run `/oh-my-copilot:omc-gh-setup` first and stop.

---

## Step 2: List Open PRs

Fetch all open pull requests for the configured repository.

```bash
gh pr list --repo {owner}/{repo} --state open --json number,title,author,headRefName,baseRefName,createdAt,reviewDecision,isDraft --limit 20 2>&1
```

Present results in a table:

```
### Open Pull Requests ({N})
| # | Title | Author | Branch | Review Status | Draft | Age |
|---|-------|--------|--------|--------------|-------|-----|
| #42 | Add retry logic | alice | feat/retry → main | Approved | No | 3d |
| #43 | Fix login timeout | bob | fix/login → dev | Pending | Yes | 1d |
```

Review decision labels:
- `APPROVED` — all required reviewers approved
- `CHANGES_REQUESTED` — at least one reviewer requested changes
- `REVIEW_REQUIRED` — pending review
- Empty — no review policy configured

If there are no open PRs, report "(0)" and ask the user if they want to check a specific PR by number.

---

## Step 3: Select PR for Review

Prompt the user to select a PR from the list, or accept a PR number directly.

Fetch full PR details:

```bash
gh pr view {prNumber} --repo {owner}/{repo} --json title,body,author,headRefName,baseRefName,additions,deletions,changedFiles,reviews,comments,statusCheckRollup,labels,milestone 2>&1
```

Display a summary:

```
### PR #{number}: {title}
Author:         {author}
Branch:         {headRefName} → {baseRefName}
Created:        {createdDate}
Changes:        +{additions} −{deletions} across {changedFiles} files
Labels:         {labels}
Milestone:      {milestone}
CI Status:      {pass/fail/pending}
Description:    {description}
Reviews:        {reviewer} ({state}), ...
```

---

## Step 4: Review Changes

### 4a. Read the diff

```bash
gh pr diff {prNumber} --repo {owner}/{repo} 2>&1
```

If the diff is very large (>500 lines), summarize the changed files first:

```bash
gh pr view {prNumber} --repo {owner}/{repo} --json files --jq '.files[].path' 2>&1
```

Then read individual files of interest using the Read tool.

### 4b. Read existing review comments

```bash
gh api repos/{owner}/{repo}/pulls/{prNumber}/comments --jq '.[] | {id, path, line, body, user: .user.login, created_at}' 2>&1
```

Present a summary of existing comments:

```
### Review Comments ({N})
| File | Line | Author | Comment |
|------|------|--------|---------|
| src/auth.ts | 42 | charlie | "Should handle null case" |
| — (general) | — | alice | "LGTM overall" |
```

If there are no comments, note "No review comments yet."

---

## Step 5: Post Review Comments

Post new review feedback. Comments can target a specific file/line or be general PR-level.

### File-level comment (inline)

Use the review API to batch comments into a single review submission (avoids notification spam):

```bash
gh api repos/{owner}/{repo}/pulls/{prNumber}/reviews \
  -f event=COMMENT \
  -f body="{summary}" \
  -f 'comments[][path]="{filePath}"' \
  -f 'comments[][line]={lineNumber}' \
  -f 'comments[][body]="{comment}"' \
  2>&1
```

For a single inline comment without a full review:

```bash
gh api repos/{owner}/{repo}/pulls/{prNumber}/comments \
  -f body="{comment}" \
  -f path="{filePath}" \
  -F line={lineNumber} \
  -f side=RIGHT \
  -f commit_id="{latestCommitSha}" \
  2>&1
```

### General PR comment

```bash
gh pr comment {prNumber} --repo {owner}/{repo} --body "{comment}" 2>&1
```

Confirm after each action:
```
Added comment to PR #{number} on {filePath}:{line}
```

---

## Step 6: Submit Review Decision

Submit the final review decision.

### Approve

```bash
gh pr review {prNumber} --repo {owner}/{repo} --approve --body "LGTM" 2>&1
```

### Request Changes

```bash
gh pr review {prNumber} --repo {owner}/{repo} --request-changes --body "{reason}" 2>&1
```

### Comment Only (no decision)

```bash
gh pr review {prNumber} --repo {owner}/{repo} --comment --body "{comment}" 2>&1
```

Confirm:
```
Submitted review on PR #{number}: {Approved / Changes Requested / Commented}
```

---

## Step 7: Additional PR Actions (Optional)

If the user requests additional operations:

### Merge PR

```bash
gh pr merge {prNumber} --repo {owner}/{repo} --squash --delete-branch 2>&1
```

Confirm before merging — this is a destructive action.

### Request Reviewers

```bash
gh pr edit {prNumber} --repo {owner}/{repo} --add-reviewer "{username}" 2>&1
```

### Add Labels

```bash
gh pr edit {prNumber} --repo {owner}/{repo} --add-label "{label}" 2>&1
```

---

## Error Handling

| Error | Action |
|-------|--------|
| `.omg/config.json` missing | Tell user to run `/oh-my-copilot:omc-gh-setup` first |
| `gh auth` required | Prompt user to authenticate; stop execution |
| PR not found | Verify PR number and that the repository in config matches |
| No permission to review | User may need write access to the repo |
| Merge conflict | Cannot merge — inform user to resolve conflicts first |
| Rate limit / 403 | Wait 2 seconds and retry once; if still failing, note as unavailable |
