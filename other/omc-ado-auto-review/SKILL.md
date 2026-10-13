---
name: omc-ado-auto-review
description: "Auto-review Azure DevOps PRs where you are an assigned reviewer and post AI review comments. Not for interactive review (omc-ado-review) or GitHub repos (omc-gh-auto-review). Creating PRs → git-master."
---

# OMC ADO Auto Review

Automatically review Azure DevOps pull requests where the current user is assigned as a reviewer. Reads `.omg/config.json` for connection settings, discovers pending PRs, fetches diffs, spawns a code-reviewer agent to analyse changes, and posts structured inline comments back to each PR.

**When this skill is invoked, immediately execute the workflow below. Do not only restate or summarize these instructions back to the user.**

## Trigger Patterns

- "auto review"
- "auto-review prs"
- "review my assigned prs"
- "automated pr review"
- "omc-ado-auto-review"

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

Also read optional `ado.autoReview` settings (apply defaults when absent):

| Setting | Default | Purpose |
|---------|---------|---------|
| `severityThreshold` | `"MEDIUM"` | Minimum severity to post as inline comment |
| `autoVote` | `false` | Automatically cast a vote after review |
| `maxFilesPerReview` | `50` | Cap on number of files analysed per PR |
| `excludePatterns` | `["*.lock", "*.min.js", "*.generated.*"]` | Glob patterns for files to skip |

If config is NOT_FOUND or missing the `ado` key: tell the user to run `/oh-my-copilot:omc-ado-setup` first and stop.

---

## Step 2: Identify Current User

Resolve the current user's identity so PRs can be filtered by reviewer assignment.

MCP (preferred):
```
mcp__azure-devops__core_get_identity_ids
  → identities: ["{currentUserEmail}"]
```

az CLI fallback:
```bash
az ad signed-in-user show -o json 2>&1
```

Extract and store:
- `userId` — the ADO identity GUID
- `userEmail` — the user's email address (used for az CLI fallback filtering)

If neither succeeds, prompt the user to run `az login` and stop.

---

## Step 3: Find PRs Assigned for Review

Fetch active PRs where the resolved `userId` appears in the reviewers list.

MCP (preferred):
```
mcp__azure-devops__repo_list_pull_requests_by_repo_or_project
  → repositoryId: "{repo}"
  → project: "{project}"
  → status: "active"
```

Filter the returned list: keep only PRs whose `reviewers` array contains an entry matching `userId` with `vote` of `0` (no vote yet) or `-5` (waiting for author). Skip PRs already voted `10` or `-10`.

az CLI fallback:
```bash
az repos pr list \
  --repository "{repo}" \
  --project "{project}" \
  --org "{org}" \
  --reviewer "{userEmail}" \
  --status active \
  -o json 2>&1
```

Present a table of pending PRs:

```
### PRs Pending Your Review ({N})
| ID   | Title                    | Author | Age | Your Vote       |
|------|--------------------------|--------|-----|-----------------|
| !42  | Add retry logic          | alice  | 3d  | No vote         |
| !43  | Fix login timeout        | bob    | 1d  | Waiting (reset) |
```

Vote label mapping:
- `-10` = Rejected
- `-5` = Waiting for author
- `0` = No vote
- `5` = Approved with suggestions
- `10` = Approved

**If no PRs are found:** report "No PRs pending your review" and stop.

**If invoked with a specific PR ID argument** (e.g. `omc-ado-auto-review 42`): skip discovery and process that PR directly, regardless of reviewer assignment.

---

## Step 4: Fetch PR Diff and Changed Files

For each PR to be reviewed (all discovered, or the single specified PR):

**4a. Fetch the unified diff:**

az CLI:
```bash
az repos pr diff \
  --id {prId} \
  --org "{org}" 2>&1
```

**4b. Retrieve PR details and linked work items for spec compliance context:**

MCP (preferred):
```
mcp__azure-devops__repo_get_pull_request_by_id
  → pullRequestId: {prId}
  → project: "{project}"
```

az CLI fallback:
```bash
az repos pr show --id {prId} --org "{org}" -o json 2>&1
```

**4c. Filter files:**

Parse file paths from the diff headers (lines beginning `diff --git a/`). Apply `excludePatterns` from config — skip any file whose path matches one of those glob patterns.

If the remaining file count exceeds `maxFilesPerReview`, warn the user:

```
Warning: PR !{id} touches {total} files. Reviewing first {maxFilesPerReview} by diff order.
```

Then truncate to the first `maxFilesPerReview` files.

**4d. Read full file content** for each included file to provide complete context to the reviewer agent.

---

## Step 5: Spawn Code Reviewer Agent

For each PR, spawn an `oh-my-copilot:code-reviewer` agent via the Task tool with the following payload:

- Full unified diff of the PR
- Full content of each changed file (post-filter)
- PR title and description
- Linked work item titles and descriptions (for spec compliance check)
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

Parse the agent's response and extract the findings array. If parsing fails, treat the raw response as a general summary and proceed to Step 6 in summary-only mode.

---

## Step 6: Post Findings as Inline Comments

Apply the `severityThreshold` filter: only post findings whose severity meets or exceeds the threshold.

Severity order (highest to lowest): `CRITICAL > HIGH > MEDIUM > LOW`

**6a. Post inline thread for each qualifying finding:**

Format the comment body:

```
**[{severity}]** {message}

**Suggestion:** {suggestion}

---
*Automated review by oh-my-copilot*
```

MCP (preferred):
```
mcp__azure-devops__repo_create_pull_request_thread
  → repositoryId: "{repo}"
  → pullRequestId: {prId}
  → project: "{project}"
  → comments: [{ content: "{formatted}", commentType: 1 }]
  → threadContext: {
      filePath: "/{file}",
      rightFileStart: { line: {line}, offset: 1 },
      rightFileEnd: { line: {line}, offset: 1 }
    }
  → status: 1
```

az CLI fallback:
```bash
az repos pr comment create \
  --id {prId} \
  --content '{formatted}' \
  --org "{org}" \
  -o json 2>&1
```

On `429 Too Many Requests` or rate-limit error: wait 2 seconds and retry once. If still failing, skip that finding and continue.

**6b. Post a general summary thread:**

After all inline comments, post one general PR-level comment summarising the review:

```
## Code Review Summary — PR !{id}

| Severity | Count |
|----------|-------|
| CRITICAL | {n}   |
| HIGH     | {n}   |
| MEDIUM   | {n}   |
| LOW      | {n}   |

**Files reviewed:** {N} of {total} changed files
**Files excluded:** {excluded list or "none"}

---
*Automated review by oh-my-copilot*
```

MCP (preferred):
```
mcp__azure-devops__repo_create_pull_request_thread
  → repositoryId: "{repo}"
  → pullRequestId: {prId}
  → project: "{project}"
  → comments: [{ content: "{summary}", commentType: 1 }]
  → status: 1
```

az CLI fallback:
```bash
az repos pr comment create \
  --id {prId} \
  --content '{summary}' \
  --org "{org}" \
  -o json 2>&1
```

Report progress to the user:

```
Posted {N} inline comments on PR !{id} ({CRITICAL}C / {HIGH}H / {MEDIUM}M / {LOW}L)
```

---

## Step 7: Vote on PR (Optional)

Only execute this step if `autoVote` is `true` in config **or** the `--vote` flag was passed when invoking the skill.

Determine the vote from the highest severity finding across all posted findings:

| Highest Severity | Vote Value | Vote Label |
|-----------------|------------|------------|
| `CRITICAL` | `-10` | Rejected |
| `HIGH` | `-5` | Waiting for author |
| `MEDIUM` | `5` | Approved with suggestions |
| `LOW` or no findings | `10` | Approved |

MCP (preferred):
```
mcp__azure-devops__repo_update_pull_request_reviewers
  → repositoryId: "{repo}"
  → pullRequestId: {prId}
  → project: "{project}"
  → reviewers: [{ id: "{userId}", vote: {vote} }]
```

az CLI fallback:
```bash
az repos pr set-vote \
  --id {prId} \
  --vote {approve|reject|wait|approveWithSuggestions|reset} \
  --org "{org}" \
  -o json 2>&1
```

Vote label mapping for az CLI `--vote` flag:
- `10` → `approve`
- `5` → `approveWithSuggestions`
- `-5` → `wait`
- `-10` → `reject`

Report:

```
Voted "{voteLabel}" on PR !{id}
```

If the API returns a permission error, warn: "Could not cast vote — you may not be listed as a reviewer on PR !{id}."

---

## MCP Tool Reference

| Tool | Purpose |
|------|---------|
| `core_get_identity_ids` | Resolve current user's ADO identity GUID |
| `repo_list_pull_requests_by_repo_or_project` | List active PRs; filtered client-side by reviewer |
| `repo_get_pull_request_by_id` | Fetch PR details, description, and linked work items |
| `repo_create_pull_request_thread` | Post inline or general review comment threads |
| `repo_list_pull_request_threads` | Read existing threads to avoid duplicate comments |
| `repo_update_pull_request_reviewers` | Cast a vote on the PR |

---

## az CLI Fallback Commands

Use these when MCP tools are not available in the current session:

```bash
# Identify current signed-in user
az ad signed-in-user show -o json

# List PRs assigned to reviewer by email
az repos pr list \
  --repository "{repo}" --project "{project}" --org "{org}" \
  --reviewer "{userEmail}" --status active -o json

# Fetch PR details
az repos pr show --id {prId} --org "{org}" -o json

# Get PR unified diff
az repos pr diff --id {prId} --org "{org}"

# Post a general comment
az repos pr comment create \
  --id {prId} --content '{comment}' --org "{org}" -o json

# Vote on a PR
az repos pr set-vote \
  --id {prId} --vote {approve|approveWithSuggestions|wait|reject|reset} \
  --org "{org}" -o json
```

---

## Error Handling

| Error | Action |
|-------|--------|
| `.omg/config.json` missing | Tell user to run `/oh-my-copilot:omc-ado-setup` first |
| `az login` required | Prompt user to authenticate; stop execution |
| No PRs for review | Report "No PRs pending your review" and stop |
| PR diff too large (>`maxFilesPerReview` files) | Warn and review first N files per `maxFilesPerReview` config |
| Code reviewer agent fails | Post summary-only comment without inline threads |
| Thread creation fails (rate limit) | Wait 2s and retry once; skip that finding if still failing |
| Permission denied on vote | Warn user they may not be listed as reviewer on that PR |

---

## Configuration Reference

`.omg/config.json` with optional `autoReview` section:

```json
{
  "ado": {
    "org": "https://dev.azure.com/contoso",
    "project": "MyProject",
    "repo": "my-repo",
    "autoReview": {
      "severityThreshold": "MEDIUM",
      "autoVote": false,
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
