---
name: Deploy to Production
description: Deploy current develop branch to production. Use when user says /deploy, "deploy to production", "push to heroku", "release to production", "deploy changes", "ship it", or "release changes". Commits changes, pushes develop, merges to main, creates version tag, pushes to GitHub and Heroku, then returns to develop branch.
---

# Deploy to Production Skill

This skill automates the full deployment workflow for Northwest Custom Apparel's Pricing Index project.

## What This Skill Does

Executes a complete deployment pipeline:
1. Commits any uncommitted changes (auto-generated message)
2. Pushes develop branch to GitHub
3. Merges develop into main
4. Creates a version tag (e.g., v2025.12.23.1)
5. Pushes main to GitHub and Heroku
6. Returns to develop branch

## When to Use This Skill

Use this skill when the user says:
- "/deploy"
- "deploy to production"
- "push to heroku"
- "release to production"
- "deploy changes"
- "ship it"
- "release changes"

## Implementation

Execute these steps in order. **Stop immediately if any step fails.**

### Step 1: Check Current Branch and Status

```bash
# Verify we're on develop branch
git branch --show-current
```

If not on develop, inform the user and stop.

```bash
# Check for uncommitted changes
git status --porcelain
```

### Step 2: Commit Changes (if any)

Only run if there are uncommitted changes from Step 1:

```bash
# Stage all changes
git add -A

# Get list of changed files for commit message
git diff --cached --name-only
```

Generate commit message based on changed files:
- Format: `Deploy: updated X files (file1.js, file2.css, ...)`
- If more than 3 files, show first 3 with "... and X more"

```bash
# Create commit with auto-generated message
git commit -m "Deploy: updated X files (file1, file2, ...)"
```

### Step 3: Push Develop to GitHub

```bash
git push origin develop
```

### Step 4: ASK FOR CONFIRMATION (REQUIRED)

**CRITICAL: You MUST ask the user for confirmation before proceeding to production.**

Display a summary and ask:
```
READY TO DEPLOY TO PRODUCTION?

Summary so far:
- Branch: develop
- Committed: X files
- Pushed to: GitHub (develop branch)

Next steps will:
- Merge develop → main
- Create version tag
- Push to GitHub (main) and Heroku (PRODUCTION)

Are you ready to proceed?
```

Use the AskUserQuestion tool to get explicit confirmation. **DO NOT proceed without user approval.**

If user says no or wants to stop, return to develop branch and stop.

### Step 5: Switch to Main Branch

```bash
git checkout main
```

### Step 6: Pull Latest Main (Safety Check)

```bash
git pull origin main
```

### Step 7: Merge Develop into Main

```bash
git merge develop --no-edit
```

**CRITICAL: If merge fails due to conflict:**
1. Run `git merge --abort`
2. Run `git checkout develop`
3. Display error message to user:
   ```
   DEPLOY ABORTED: Merge conflict detected!

   Please resolve conflicts manually:
   1. git checkout main
   2. git merge develop
   3. Resolve conflicts in your editor
   4. git add . && git commit
   5. Run /deploy again

   You are back on develop branch.
   ```
4. **STOP** - do not continue with remaining steps

### Step 8: Create Version Tag

Generate tag in format: `vYYYY.MM.DD.N` where N is sequence number for the day.

```bash
# Get today's date
date +%Y.%m.%d

# Check for existing tags today to determine sequence number
git tag -l "v$(date +%Y.%m.%d).*"
```

If no tags exist for today, use `.1`. Otherwise increment the last sequence number.

```bash
# Create annotated tag
git tag -a v2025.12.23.1 -m "Production deploy"
```

### Step 9: Push Main to GitHub (with tags)

```bash
git push origin main --tags
```

### Step 10: Push Main to Heroku

```bash
git push heroku main
```

### Step 11: Return to Develop Branch

```bash
git checkout develop
```

### Step 12: Display Success Message

```
DEPLOY SUCCESSFUL!

Summary:
- Committed: X files
- Version tag: v2025.12.23.1
- Pushed to: GitHub (develop + main) and Heroku

Main branch is now live at:
https://caspio-pricing-proxy-ab30a049961a.herokuapp.com
```

## Error Handling

| Error | Action |
|-------|--------|
| Not on develop branch | Stop, inform user |
| Merge conflict | Abort merge, return to develop, show manual resolution steps |
| Push fails | Show error, suggest `git pull` first |
| Heroku push fails | Show error, suggest checking Heroku login status |

## Example Output

```
Starting deployment...

[1/12] Checking branch... develop
[2/12] Committing changes... 3 files staged
       Commit: "Deploy: updated 3 files (calculator.js, styles.css, index.html)"
[3/12] Pushing develop to GitHub... done

[4/12] CONFIRMATION REQUIRED...

       READY TO DEPLOY TO PRODUCTION?

       Summary so far:
       - Branch: develop
       - Committed: 3 files
       - Pushed to: GitHub (develop branch)

       Next steps will:
       - Merge develop → main
       - Create version tag
       - Push to GitHub (main) and Heroku (PRODUCTION)

       [User confirms: Yes, proceed]

[5/12] Switching to main... done
[6/12] Pulling latest main... already up to date
[7/12] Merging develop into main... done
[8/12] Creating version tag... v2025.12.23.1
[9/12] Pushing main to GitHub... done
[10/12] Pushing to Heroku... done
[11/12] Returning to develop... done

DEPLOY SUCCESSFUL! Version v2025.12.23.1 is now live.
```

## Important Notes

- Always verify you're on develop branch before starting
- Never force push - if push fails, investigate why
- Version tags provide rollback points: `git checkout v2025.12.23.1`
- If Heroku fails but GitHub succeeds, you can manually run `git push heroku main`
