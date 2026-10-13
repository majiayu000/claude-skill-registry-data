---
name: omc-gh-triage
description: "Triage GitHub: open issues, PRs needing review, failing CI, and security alerts for a project health overview. Not for PR code review (omc-gh-review) or project boards. ADO projects → omc-ado-triage."
---

# OMC GitHub Triage

Perform a full GitHub triage cycle for the current project. Reads `.omg/config.json` for connection settings, queries all relevant GitHub surfaces (issues, PRs, Actions, Dependabot), and presents a prioritized summary with recommended actions.

**When this skill is invoked, immediately execute the workflow below. Do not only restate or summarize these instructions back to the user.**

## Trigger Patterns

- "gh triage"
- "github triage"
- "triage issues"
- "github status"
- "project health"
- "omc-gh-triage"

---

## Step 1: Load Configuration

Read `.omg/config.json`:

```bash
node -e "const f=require('fs');try{process.stdout.write(f.readFileSync('.omg/config.json','utf8'))}catch{console.log('NOT_FOUND')}"
```

Extract from the `github` key:
- `owner` — GitHub owner (org or user)
- `repo` — repository name
- `defaultBranch` — default branch name
- `labelTriage` — triage label filter (optional)

If config is NOT_FOUND or missing the `github` key: tell the user to run `/oh-my-copilot:omc-gh-setup` first and stop.

---

## Step 2: Gather Triage Data

Run all data-gathering queries in parallel (they are independent).

### 2a. Open Issues Assigned to Me

```bash
gh issue list --repo {owner}/{repo} --assignee @me --state open --json number,title,labels,createdAt,milestone --limit 20 2>&1
```

### 2b. Untriaged Issues

Issues matching the triage label (if configured) or issues with no labels:

```bash
gh issue list --repo {owner}/{repo} --label "{labelTriage}" --state open --json number,title,createdAt --limit 20 2>&1
```

If `labelTriage` is not configured, query issues with no labels:

```bash
gh issue list --repo {owner}/{repo} --state open --json number,title,labels,createdAt --limit 30 --jq '[.[] | select(.labels | length == 0)]' 2>&1
```

### 2c. PRs Needing My Review

```bash
gh pr list --repo {owner}/{repo} --search "review-requested:@me" --state open --json number,title,author,createdAt,reviewDecision --limit 20 2>&1
```

### 2d. PRs I Authored (status check)

```bash
gh pr list --repo {owner}/{repo} --author @me --state open --json number,title,reviewDecision,statusCheckRollup --limit 10 2>&1
```

### 2e. Failing CI on Default Branch

```bash
gh run list --repo {owner}/{repo} --branch {defaultBranch} --status failure --limit 5 --json databaseId,displayTitle,conclusion,headBranch,updatedAt 2>&1
```

### 2f. Dependabot / Security Alerts

```bash
gh api repos/{owner}/{repo}/dependabot/alerts --jq '[.[] | select(.state=="open")] | length' 2>&1
```

If this fails (Dependabot not enabled or insufficient permissions), skip this section and note "Dependabot not enabled or insufficient permissions."

---

## Step 3: Render Triage Summary

Present results using the following structured format. Omit sections that have 0 items (but keep the header with a "(0)" count so the user knows the query ran).

```
## GitHub Triage Summary
Repository: {owner}/{repo} | Branch: {defaultBranch}
Generated: {timestamp}

---

### My Open Issues ({N})
| # | Title | Labels | Milestone | Age |
|---|-------|--------|-----------|-----|
| #42 | Fix login timeout | bug, p1 | v2.0 | 3d |

### Untriaged Issues ({N})
| # | Title | Created |
|---|-------|---------|
| #55 | New feature request | 2026-03-28 |

### PRs Needing My Review ({N})
| # | Title | Author | Age | Decision |
|---|-------|--------|-----|----------|
| #38 | Add retry logic | alice | 3d | Pending |

### My Open PRs ({N})
| # | Title | Review Status | CI Status |
|---|-------|--------------|-----------|
| #40 | Refactor auth | Changes requested | Passing |

### CI Status — {defaultBranch}
| Workflow | Last Run | Result |
|----------|----------|--------|
| CI | 2026-03-31 08:14 | failed |
| Deploy | 2026-03-30 17:02 | succeeded |

### Security Alerts
Dependabot: {N} open alerts

---

### Recommended Actions
1. [Priority] Action description
2. [Priority] Action description
...
```

### Recommended Actions Logic

Build the action list using this priority order:

| Condition | Action |
|-----------|--------|
| CI failing on default branch | Fix failing workflow: `{workflow name}` |
| Dependabot alerts > 0 | Address `{N}` open Dependabot alerts |
| PR with `CHANGES_REQUESTED` I authored | Respond to review feedback on `#{id}` |
| PR review requested from me | Review PR `#{id}` — `{title}` |
| Untriaged issues > 0 | Triage `{N}` issues — assign labels and milestone |
| PR age > 5 days with no reviews | Ping reviewers on stale PR `#{id}` |

---

## Step 4: Optional — Delegate Actions

After presenting the summary, ask the user (via AskUserQuestion):

**Question:** "Would you like me to take action on any of these items?"

**Options:**
1. Fix failing CI — delegate to `build-fixer` agent
2. Address PR feedback — open the PR diff and summarize changes needed
3. Triage issues — walk through untriaged issues one by one
4. Review a PR — delegate to `/oh-my-copilot:omc-gh-review`
5. Show details for a specific item — enter issue or PR number
6. No action needed — exit triage

---

## Error Handling

| Error | Action |
|-------|--------|
| `.omg/config.json` missing | Tell user to run `/oh-my-copilot:omc-gh-setup` first |
| `gh auth` required | Prompt user to authenticate; do not abort — skip that section |
| Dependabot not enabled | Skip security alerts section, note it in summary |
| Query returns 0 results | Show the section with count "(0)" — do not omit the header |
| Rate limit / 403 | Wait 2 seconds and retry once; if still failing, note the section as unavailable |
