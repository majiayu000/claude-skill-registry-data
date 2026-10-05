---
name: deploy-backend
description: Deploy a backend branch via GitHub Actions. Use when user says "deploy", "lanza el pipeline", "despliega", or "/deploy". Accepts optional branch and operation arguments.
user_invocable: true
---

# Deploy Backend Skill

Triggers the "Disparar Backend Pipeline en .private" GitHub Actions workflow for the current repository.

## Usage

```
/deploy-backend              → deploy current branch
/deploy-backend feature/foo  → deploy specific branch
/deploy-backend compile      → compilation only (no deploy)
```

## Instructions

When invoked, follow these steps:

1. **Determine the repository** — Run `basename $(git remote get-url origin) .git` to get the repo name, and extract the org from the remote URL.

2. **Determine the branch** — If the user provided a branch argument, use it. Otherwise run `git branch --show-current` and use the current branch.

3. **Determine the operation** — If the user said "compile" or "compilation", use `compilation (no deploy)`. Otherwise default to `deploy`. Valid operations:
   - `compilation (no deploy)`
   - `deploy`
   - `feature`
   - `release`
   - `close release`
   - `close release and deploy master`
   - `hotfix`
   - `close hotfix`

4. **Execute the workflow** — Run:
   ```bash
   gh workflow run "Disparar Backend Pipeline en .private" -R <org>/<repo> --ref master -f operations="<operation>" -f branch="<branch>"
   ```

5. **Confirm to the user** — Show what was triggered: repo, operation, and branch.

6. **Optionally check status** — If the user asks, run:
   ```bash
   gh run list -R <org>/<repo> --branch <branch> --limit 1
   ```
