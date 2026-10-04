---
name: spec-ship
description: >
  Push the current branch to GitHub and create a pull request. Use this skill when the user says
  "ship it", "ship this", "push to github", "create a pr", "open a pull request", "send for review",
  "get this reviewed", or wants to push their work and open a PR. Also use when the user says
  "/spec-ship" (or their host's equivalent invocation syntax). This skill handles prerequisites,
  branching, pushing, and PR creation — it does not commit or run quality checks (use
  spec-checkpoint for that first).
license: MIT
---

# Ship It

Push your work to GitHub and open a pull request — handling prerequisites, branch creation, pushing, and PR generation automatically.

This skill complements `spec-checkpoint`. Use `spec-checkpoint` to commit locally (with quality gates), then `spec-ship` to get the code to GitHub for review.

## Instructions

### Step 0: Prerequisites

Verify tooling before doing anything else.

1. **GitHub CLI installed?**
   ```bash
   gh --version
   ```
   If the command fails (not found):
   - Detect the platform and attempt to install:
     - **Windows:** `winget install --id GitHub.cli`
     - **macOS:** `brew install gh`
     - **Linux (Debian/Ubuntu):** follow the official apt instructions
   - If auto-install fails, tell the user what to install and stop.

2. **GitHub CLI authenticated?**
   ```bash
   gh auth status
   ```
   If not authenticated, tell the user:
   ```
   GitHub CLI is not logged in. Please run this in the prompt:
     ! gh auth login
   Then re-run /spec-ship.
   ```
   Stop here — do not proceed until auth is confirmed.

3. **Git remote exists?**
   ```bash
   git remote -v
   ```
   If no remote named `origin` exists, stop and tell the user:
   ```
   No git remote found. Add one with:
     git remote add origin https://github.com/{user}/{repo}.git
   ```

### Step 1: Detect the Environment

Run these commands to understand the current state:

1. `git branch --show-current` — get the current branch name
2. Detect the default branch:
   ```bash
   gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'
   ```
3. `git status --porcelain` — check for uncommitted changes

If there are uncommitted changes, stop and tell the user:
```
You have uncommitted changes. Run /spec-checkpoint first to commit them, then /spec-ship to push.
```

Store the default branch name for use throughout the remaining steps.

### Step 2: Check for Unpushed Commits

Determine if there are commits that haven't been pushed yet.

**If on a feature branch with a remote tracking branch:**
```bash
git log @{upstream}..HEAD --oneline
```

**If on a feature branch with no remote tracking branch, or on the default branch:**
```bash
git log origin/{default_branch}..HEAD --oneline
```

If there are **no unpushed commits**, stop and tell the user:
```
Nothing to ship — all commits are already pushed.
```

Save the list of unpushed commit messages for use in later steps.

### Step 3: Handle Branching

**If already on a feature branch** (not the default branch):
- Stay on it. No branching needed.
- Skip to Step 4.

**If on the default branch:**
- Generate a branch name from the unpushed commit messages:
  - Read the commit subjects
  - Derive a kebab-case branch name with a conventional prefix: `feat/`, `fix/`, `refactor/`, `chore/`, `docs/` based on the commit content
  - Keep it short (3-5 words max after the prefix), e.g., `feat/add-user-auth`, `fix/login-redirect-loop`
  - Strip special characters, lowercase everything
- Create and switch to the new branch:
  ```bash
  git checkout -b {branch_name}
  ```
- Tell the user: `Created branch {branch_name}`

### Step 4: Confirm Before Pushing

Pushing and opening a PR are visible to others and not easily undone — confirm with the user
before proceeding, even if your host would otherwise run this skill non-interactively without
prompting. Show:

```
About to push and open a PR:
  Branch: {branch_name}
  Remote: origin
  Commits:
    {list of unpushed commit subjects, from Step 2}

Proceed? (yes/no)
```

Wait for an explicit yes. If the user declines or doesn't respond affirmatively, stop here —
do not push.

### Step 5: Push to Origin

```bash
git push -u origin {branch_name}
```

If the branch already has a remote tracking branch, a regular `git push` is fine.

### Step 6: Check for Existing PR

Before creating a new PR, check if one already exists for this branch:

```bash
gh pr view --json number,url,title,state 2>/dev/null
```

If a PR already exists and is **open**:
- Do NOT create a new one
- Skip to Step 8 and report the existing PR with a note that new commits were pushed.

If no PR exists (or it is closed/merged), proceed to Step 7.

### Step 7: Create the Pull Request

Generate the PR title and body from the unpushed commits:

- **Title**: concise summary under 70 chars. If single commit, use its subject. If multiple, synthesize a short summary. Imperative mood.
- **Body**: TL;DR of the changes in 2-4 bullet points max, plus a footer naming whichever
  agent/model actually generated the PR — never hardcode a specific vendor or model name, since
  this skill runs under many different hosts. Omit the footer entirely if your host has no clean
  way to identify itself.

```bash
gh pr create --base {default_branch} --head {branch_name} --title "{title}" --body "$(cat <<'EOF'
## Summary
{2-4 bullet points}

---
Generated by {agent name}
EOF
)"
```

### Step 8: Report

Display the result clearly:

```
Shipped to GitHub:
  Branch: {branch_name}
  PR: #{number} — {title}
  URL: {url}
```

## Important

- Do NOT run lint, type-check, or build — that is spec-checkpoint's job
- Do NOT commit anything — only push existing commits and create a PR
- If the user has uncommitted changes, tell them to run /spec-checkpoint first
- Keep the PR body short — a TL;DR, not an essay
- Always check for an existing open PR before creating a new one to avoid duplicates
- Detect the default branch dynamically — do not hardcode `main` or `master`
- When creating a branch from the default branch, use conventional prefixes (`feat/`, `fix/`, etc.) with kebab-case names
- Never run destructive git operations (no `--force`, no `reset --hard`)
- If `gh` is not installed or authenticated, help the user get set up before proceeding
- Always get explicit user confirmation before pushing or opening a PR (Step 4) — do this even
  if your host would otherwise let the skill run non-interactively, since pushing and opening a
  PR are visible to others and not easily undone
