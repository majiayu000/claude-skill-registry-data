---
name: merge
description: Merge dev into main via PR with merge commit strategy
---

# /merge — Merge dev into main

**Invocation:** `/merge`

**Purpose:** Pulls the latest dev branch, opens (or reuses) a PR from dev → main, shows the diff, then asks for confirmation before performing the merge commit.

## Steps

Execute the following steps in order:

### 1. Switch to dev and pull latest

Run:
```bash
git checkout dev && git pull origin dev
```

Report the result. If this fails, stop and report the error.

### 2. Open PR (or find existing one)

Check if a PR from `dev` → `main` titled `merge/dev-main` already exists:
```bash
gh pr list --base main --head dev --json number,title,url
```

- If an open PR exists, note its number and URL.
- If no open PR exists, create one:
  ```bash
  gh pr create --base main --head dev --title "merge/dev-main" --body ""
  ```
  Note the new PR number and URL.

Report: `PR #<N>: <url>`

### 3. Show the diff

Display what will be merged — commits and full diff:
```bash
git log main..dev --oneline
git diff main...dev
```

Print both outputs for the user to review. The full diff shows all changes that will be merged.

### 4. Ask for confirmation

Use the AskUserQuestion tool to ask:

> Perform merge into main using merge commit strategy? (y / anything else to cancel)

Wait for the user's response.

### 5. Merge or abort

**If the user types exactly `y`:**

Merge the PR using the merge commit strategy. Use the PR title + number as the commit message:
```bash
gh pr merge <PR_NUMBER> --merge --subject "merge/dev-main (#<PR_NUMBER>)" --body ""
```

After merging, confirm success and print the PR URL.

**If the user types anything other than `y`:**

Print: `Merge cancelled.` and stop — do not merge.
