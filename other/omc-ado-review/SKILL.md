---
name: omc-ado-review
description: "Review Azure DevOps pull requests: read diffs, add reviewers, comment, vote, and manage PR threads. Not for automated review (omc-ado-auto-review), triage, or GitHub repos (omc-gh-review). Creating PRs → git-master."
---

# OMC ADO Review

Perform a full Azure DevOps pull request review cycle. Reads `.omg/config.json` for connection settings, lists open PRs, surfaces existing review threads, and supports adding comments, managing reviewers, and updating PR status.

**When this skill is invoked, immediately execute the workflow below. Do not only restate or summarize these instructions back to the user.**

## Trigger Patterns

- "ado review"
- "review pr"
- "review pull request"
- "add reviewer"
- "pr comments"
- "vote on pr"
- "manage pr threads"
- "omc-ado-review"

---

## Step 1: Load Configuration

Read `.omg/config.json`:

```bash
node -e "const f=require('fs');try{process.stdout.write(f.readFileSync('.omg/config.json','utf8'))}catch{console.log('NOT_FOUND')}"
```

Extract from the `ado` key:
- `org` — full org URL (e.g. `https://dev.azure.com/contoso`)
- `project` — ADO project name
- `repo` — repository name

If config is NOT_FOUND or missing the `ado` key: tell the user to run `/oh-my-copilot:omc-ado-setup` first and stop.

---

## Step 2: List Open PRs

Fetch all active pull requests for the configured repository.

MCP (preferred):
```
mcp__azure-devops__repo_list_pull_requests_by_repo_or_project
  → repositoryId: "{repo}"
  → project: "{project}"
  → status: "active"
```

az CLI fallback:
```bash
az repos pr list \
  --repository "{repo}" \
  --project "{project}" \
  --org "{org}" \
  --status active \
  -o json 2>&1
```

Present results in a table:

```
### Open Pull Requests ({N})
| ID | Title | Author | Target Branch | Reviewers | Age |
|----|-------|--------|--------------|-----------|-----|
| !42 | Add retry logic    | alice | main | 2 of 3 approved | 3d |
| !43 | Fix login timeout  | bob   | dev  | No votes yet    | 1d |
```

For each PR, summarize reviewer vote status:
- `-10` = Rejected
- `-5` = Waiting for author
- `0` = No vote
- `5` = Approved with suggestions
- `10` = Approved

If there are no open PRs, report "(0)" and ask the user if they want to check a specific PR by ID.

---

## Step 3: Select PR for Review

Prompt the user to select a PR from the list, or accept a PR ID directly.

Fetch full PR details:

MCP (preferred):
```
mcp__azure-devops__repo_get_pull_request_by_id
  → pullRequestId: {prId}
  → project: "{project}"
```

az CLI fallback:
```bash
az repos pr show \
  --id {prId} \
  --org "{org}" \
  -o json 2>&1
```

Display a summary:

```
### PR !{id}: {title}
Author:        {author}
Source:        {sourceBranch} → {targetBranch}
Created:       {createdDate}
Description:   {description}
Work Items:    #{id} {title}
Reviewers:     {name} ({voteLabel}), ...
Auto-complete: {enabled/disabled}
```

---

## Step 4: Review Changes

Fetch existing review threads and comments to understand the current review state before adding new feedback.

**4a. List PR threads:**

MCP (preferred):
```
mcp__azure-devops__repo_list_pull_request_threads
  → repositoryId: "{repo}"
  → pullRequestId: {prId}
  → project: "{project}"
```

**4b. Read thread comments (for active threads):**

MCP (preferred):
```
mcp__azure-devops__repo_list_pull_request_thread_comments
  → repositoryId: "{repo}"
  → pullRequestId: {prId}
  → threadId: {threadId}
  → project: "{project}"
```

Present a summary of threads:

```
### Review Threads ({N} active, {N} resolved)
| Thread | File | Comment | Author | Status |
|--------|------|---------|--------|--------|
| #1 | src/auth.ts:42 | "Should handle null case" | charlie | Active |
| #2 | — (general) | "LGTM overall" | alice | Resolved |
```

If there are no threads, note "No review threads yet."

---

## Step 5: Add Review Comments

Create new review feedback as threads. Threads can target a specific file/line or be general PR-level comments.

**File-level comment:**

MCP (preferred):
```
mcp__azure-devops__repo_create_pull_request_thread
  → repositoryId: "{repo}"
  → pullRequestId: {prId}
  → project: "{project}"
  → comments: [{ content: "{comment}", commentType: 1 }]
  → threadContext: { filePath: "{filePath}", rightFileStart: { line: {lineNumber}, offset: 1 }, rightFileEnd: { line: {lineNumber}, offset: 1 } }
  → status: 1
```

**General PR comment:**

MCP (preferred):
```
mcp__azure-devops__repo_create_pull_request_thread
  → repositoryId: "{repo}"
  → pullRequestId: {prId}
  → project: "{project}"
  → comments: [{ content: "{comment}", commentType: 1 }]
  → status: 1
```

az CLI fallback:
```bash
az repos pr comment create \
  --id {prId} \
  --content '{comment}' \
  --org "{org}" \
  -o json 2>&1
```

**Reply to an existing thread:**

MCP (preferred):
```
mcp__azure-devops__repo_reply_to_comment
  → repositoryId: "{repo}"
  → pullRequestId: {prId}
  → threadId: {threadId}
  → project: "{project}"
  → content: "{reply}"
```

az CLI fallback:
```bash
az repos pr comment create \
  --id {prId} \
  --content '{reply}' \
  --reply-id {commentId} \
  --thread-id {threadId} \
  --org "{org}" \
  -o json 2>&1
```

Confirm after each action:
```
Added comment to PR !{id} on {filePath}:{line}
```

---

## Step 6: Manage Reviewers

Add or remove reviewers from the PR.

MCP (preferred):
```
mcp__azure-devops__repo_update_pull_request_reviewers
  → repositoryId: "{repo}"
  → pullRequestId: {prId}
  → project: "{project}"
  → reviewers: [{ id: "{userId}", vote: 0, isRequired: true }]
```

To find a reviewer's user ID, use:
```
mcp__azure-devops__core_get_identity_ids
  → identities: ["{email or display name}"]
```

az CLI fallback:
```bash
az repos pr reviewer add \
  --id {prId} \
  --reviewers "{email}" \
  --org "{org}" \
  -o json 2>&1
```

To remove a reviewer:
```bash
az repos pr reviewer remove \
  --id {prId} \
  --reviewers "{email}" \
  --org "{org}" \
  -o json 2>&1
```

Confirm:
```
Added {name} as reviewer on PR !{id}
```

---

## Step 7: Update PR Status

Cast a vote, enable auto-complete, set draft status, or abandon/reactivate the PR.

MCP (preferred):
```
mcp__azure-devops__repo_update_pull_request
  → repositoryId: "{repo}"
  → pullRequestId: {prId}
  → project: "{project}"
  → [one or more of the following fields:]
      status: "active" | "abandoned" | "completed"
      isDraft: true | false
      autoCompleteSetBy: { id: "{userId}" }
      mergeStrategy: "squash" | "rebase" | "rebaseMerge" | "noFastForward"
```

To cast a vote (approve/reject), update the reviewer entry:
```
mcp__azure-devops__repo_update_pull_request_reviewers
  → reviewers: [{ id: "{currentUserId}", vote: 10 }]
  (vote: 10=Approved, 5=Approved with suggestions, 0=No vote, -5=Waiting for author, -10=Rejected)
```

az CLI fallback:
```bash
# Set status
az repos pr update \
  --id {prId} \
  --status {active|abandoned|completed} \
  --org "{org}" \
  -o json 2>&1

# Vote (approve)
az repos pr set-vote \
  --id {prId} \
  --vote approve \
  --org "{org}" \
  -o json 2>&1

# Enable auto-complete
az repos pr update \
  --id {prId} \
  --auto-complete true \
  --merge-strategy squash \
  --org "{org}" \
  -o json 2>&1
```

Confirm:
```
Updated PR !{id}: {change description}
```

---

## MCP Tool Reference

| Tool | Purpose |
|------|---------|
| `repo_list_pull_requests_by_repo_or_project` | List open PRs |
| `repo_get_pull_request_by_id` | Get PR details |
| `repo_create_pull_request_thread` | Create review comment thread |
| `repo_list_pull_request_threads` | List existing PR threads |
| `repo_list_pull_request_thread_comments` | Read thread comments |
| `repo_reply_to_comment` | Reply to existing thread |
| `repo_update_pull_request_reviewers` | Add/remove reviewers |
| `repo_update_pull_request` | Update PR status/properties |

---

## az CLI Fallback Commands

Use these when MCP tools are not available in the current session:

```bash
# List open PRs
az repos pr list \
  --repository "{repo}" --project "{project}" --org "{org}" \
  --status active -o table

# Show PR details
az repos pr show --id {prId} --org "{org}" -o json

# Add a comment
az repos pr comment create \
  --id {prId} --content '{comment}' --org "{org}" -o json

# List comments
az repos pr comment list --id {prId} --org "{org}" -o table

# Add a reviewer
az repos pr reviewer add \
  --id {prId} --reviewers "{email}" --org "{org}" -o json

# Vote on a PR
az repos pr set-vote \
  --id {prId} --vote {approve|reject|wait|reset} --org "{org}" -o json

# Update PR status
az repos pr update --id {prId} --status {status} --org "{org}" -o json
```

---

## Error Handling

| Error | Action |
|-------|--------|
| `.omg/config.json` missing | Tell user to run `/oh-my-copilot:omc-ado-setup` first |
| `az login` required | Prompt user to authenticate; do not abort — skip that section |
| PR not found | Verify PR ID and that the repository name in config matches ADO |
| Reviewer identity not found | Use `core_get_identity_ids` to look up the user by email; prompt user to provide full email address |
| Permission denied on vote | User may not be listed as a reviewer; add themselves first via Step 6 |
| Thread update fails | Verify thread is still `Active`; resolved threads cannot receive new replies |
| Rate limit / 429 | Wait 2 seconds and retry once; if still failing, note the section as unavailable |
