---
name: omc-gh-setup
description: "Set up or troubleshoot the GitHub integration for this project (.omg/config.json connection). Not for issue triage, project boards, PR review, or Azure DevOps setup (omc-ado-setup)."
role: config-writer
scope: .omg/**
---

# OMC GitHub Setup

Configure GitHub integration for the current project. Detects the owner and repo from the git remote URL, verifies `gh` authentication, and writes `.omg/config.json` with all required settings.

**When this skill is invoked, immediately execute the workflow below. Do not only restate or summarize these instructions back to the user.**

## Trigger Patterns

- "gh setup"
- "github setup"
- "configure github"
- "connect to github"
- "omc-gh-setup"

## Prerequisites

Before running the main workflow, verify all prerequisites are present. If any fail, report the issue and stop with actionable remediation steps.

### Check 1: gh CLI installed

```bash
gh --version 2>&1 | head -1
```

If this fails: tell the user to install the GitHub CLI from https://cli.github.com/.

### Check 2: gh authentication status

```bash
gh auth status 2>&1
```

If this fails or shows "not logged in": tell the user to run `gh auth login` and retry.

### Check 3: Token scopes

```bash
gh auth status 2>&1 | grep -i "token scopes"
```

The token must include the `repo` scope for full access. If scopes are insufficient, suggest: `gh auth refresh -s repo`.

---

## Step 1: Detect GitHub Remote

Inspect the git remote URL to determine if the repo is hosted on GitHub.

```bash
git remote -v 2>&1
```

GitHub remote URLs follow these patterns:
- `https://github.com/{owner}/{repo}.git`
- `https://github.com/{owner}/{repo}`
- `git@github.com:{owner}/{repo}.git`

Parse the remote URL to extract:
- `owner` — the GitHub organization or user
- `repo` — the repository name (strip trailing `.git` if present)

If no GitHub remote is detected, inform the user and ask whether they want to configure manually (prompt for owner, repo values).

---

## Step 2: Probe Existing Configuration

Check if `.omg/config.json` already exists:

```bash
node -e "const f=require('fs');try{process.stdout.write(f.readFileSync('.omg/config.json','utf8'))}catch{console.log('NOT_FOUND')}"
```

If it exists and contains `github` settings, ask the user whether to update or keep the existing configuration (use AskUserQuestion).

---

## Step 3: Verify GitHub Access

Confirm the detected owner/repo are accessible with the current authentication:

```bash
gh repo view {owner}/{repo} --json name,defaultBranchRef,isPrivate,owner 2>&1
```

Extract:
- `defaultBranch` — the default branch name (e.g. `main`, `dev`, `master`)
- `isPrivate` — whether the repo is private (informational)

If this fails, the user may need to re-authenticate or the repo may not exist:

```bash
gh auth login
```

---

## Step 4: Discover Optional Settings

Ask the user (via AskUserQuestion) for optional configuration. Defaults are shown in brackets.

### Triage Label

```bash
gh label list --repo {owner}/{repo} --json name --jq '.[].name' 2>&1
```

Show available labels and ask the user which label (if any) should mark untriaged issues. Default: none (skip).

---

## Step 5: Write `.omg/config.json`

Create or update the config file. Preserve any existing keys (e.g. `ado`).

First, ensure the `.omg/` directory exists:

```bash
node -e "require('fs').mkdirSync('.omg',{recursive:true});console.log('Ensured .omg/')"
```

Write `.omg/config.json` using the Write (or Edit) tool. The schema is:

```json
{
  "github": {
    "owner": "{owner}",
    "repo": "{repo}",
    "defaultBranch": "main",
    "labelTriage": "",
    "configuredAt": "{ISO timestamp}"
  }
}
```

### Configuration Schema Reference

| Key | Type | Description |
|-----|------|-------------|
| `github.owner` | `string` | GitHub owner (organization or user) |
| `github.repo` | `string` | Repository name |
| `github.defaultBranch` | `string` | Default branch name (e.g. `main`) |
| `github.labelTriage` | `string?` | Label used to identify untriaged issues (optional) |
| `github.configuredAt` | `string` | ISO 8601 timestamp of when setup ran |

### Example output

```json
{
  "github": {
    "owner": "RobinNorberg",
    "repo": "oh-my-copilot",
    "defaultBranch": "dev",
    "labelTriage": "needs-triage",
    "configuredAt": "2026-04-01T12:00:00Z"
  }
}
```

---

## Step 6: Verify Connection

Run a smoke test by listing the most recent 5 issues:

```bash
gh issue list --repo {owner}/{repo} --limit 5 --json number,title,state 2>&1
```

If the query returns results: report success and show the items.
If the query fails with an auth error: suggest `gh auth login`.
If the query returns 0 items: that is normal — confirm setup is complete.

---

## Step 7: Report and Next Steps

Report a summary of what was configured:

```
GitHub Setup Complete

Owner        : {owner}
Repository   : {repo}
Default Branch: {defaultBranch}
Triage Label : {labelTriage or "none"}
Config file  : .omg/config.json

Next steps:
  /oh-my-copilot:omc-gh-triage   — run a full triage of issues, PRs, and CI
  /oh-my-copilot:omc-gh-review   — review open pull requests
```

---

## Error Reference

| Error | Likely cause | Fix |
|-------|-------------|-----|
| `gh: command not found` | GitHub CLI not installed | Install from https://cli.github.com/ |
| `not logged in` | Not authenticated | Run `gh auth login` |
| `Could not resolve to a Repository` | Wrong owner/repo | Verify the remote URL and re-run |
| `HTTP 403` | Insufficient token scopes | Run `gh auth refresh -s repo` |
| `HTTP 404` | Repo not found or private | Ensure token has `repo` scope for private repos |
