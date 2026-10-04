---
name: pr-production
description: Creates a streamlined pull request from v2 (staging) to main (production) with change summary, affected apps detection, and deployment checklist. This skill should be used when ready to deploy staging changes to production, creating a production PR, or promoting v2 branch to main.
---

# PR Production

This skill streamlines the process of creating a pull request from v2 (staging) to main (production) with comprehensive change tracking and deployment verification.

## When to Use This Skill

- After testing changes in staging environment
- Ready to deploy to production
- Creating a production release PR
- Promoting v2 changes to main branch

## Commands

```
/pr-production                                    # Create PR with auto-generated title
/pr-production --title="Feature: New chatbot"     # Create PR with custom title
/pr-production --draft                            # Create as draft PR
/pr-production --check                            # Check readiness without creating PR
```

## Prerequisites

Before creating a production PR:

1. **Changes tested in staging** - All changes deployed and tested
2. **CI passing on v2** - All tests green
3. **No uncommitted changes** - Clean working directory
4. **v2 branch up to date** - Synced with remote

## PR Creation Workflow

### Step 1: Pre-flight Checks

Verify readiness for production:

```bash
# Ensure on v2 branch
git branch --show-current
# Expected: v2

# Check for uncommitted changes
git status --porcelain
# Expected: empty

# Ensure v2 is up to date
git fetch origin
git status -uno
# Expected: up to date with origin/v2

# Check if v2 has commits ahead of main
git log main..v2 --oneline
# Expected: list of commits to merge
```

### Step 2: Gather Change Information

Collect data for PR body:

```bash
# Get commits since last main merge
COMMITS=$(git log main..v2 --oneline)

# Get files changed
FILES_CHANGED=$(git diff --name-only main..v2)

# Count changes by app
DASHBOARD_CHANGES=$(git diff --name-only main..v2 | grep "^apps/dashboard" | wc -l)
CREATOR_CHANGES=$(git diff --name-only main..v2 | grep "^apps/creator" | wc -l)
WEBSITE_CHANGES=$(git diff --name-only main..v2 | grep "^apps/website" | wc -l)
FUNCTIONS_CHANGES=$(git diff --name-only main..v2 | grep "^supabase/functions" | wc -l)
MIGRATIONS_CHANGES=$(git diff --name-only main..v2 | grep "^supabase/migrations" | wc -l)

# Check for breaking changes (look for migrations, type changes)
BREAKING_CHANGES=$(git diff --name-only main..v2 | grep -E "(migration|types\.ts)" | wc -l)
```

### Step 3: Generate PR Title

Auto-generate title based on changes:

```
# If single feature/fix (most common)
feat: Add new mandate matcher improvements

# If multiple changes
chore: Merge v2 staging changes (dashboard, creator)

# If hotfix
fix: Resolve authentication timeout issue
```

### Step 4: Generate PR Body

Create comprehensive PR body:

```markdown
## Summary

This PR promotes staging (v2) changes to production (main).

### Changes Included

**Commits**: [X] commits since last production deploy

<details>
<summary>Click to expand commit list</summary>

- abc1234 feat: Add mandate matcher v2
- def5678 fix: Resolve auth timeout
- ghi9012 chore: Update dependencies
...

</details>

### Affected Apps

| App | Files Changed | Will Auto-Deploy |
|-----|---------------|------------------|
| Dashboard | X files | Yes |
| Creator | X files | Yes |
| Website | X files | Yes |

### Database Changes

| Type | Count | Notes |
|------|-------|-------|
| Migrations | X | [List migration names] |
| Edge Functions | X | [List functions] |

### Deployment Checklist

Pre-merge:
- [ ] All staging tests passed
- [ ] Staging URLs tested manually
- [ ] Database migrations tested in staging
- [ ] No breaking API changes (or clients updated)

Post-merge:
- [ ] Monitor Vercel deployment status
- [ ] Verify production URLs after deploy
- [ ] Check error monitoring for new issues
- [ ] Notify team of deployment

### Testing Evidence

**Staging URLs Tested**:
- Dashboard: https://dashboard-staging.kstorybridge.com
- Creator: https://creator-staging.kstorybridge.com

**Test Results**:
- E2E Tests: PASS
- Build: PASS
- Lint: PASS

### Rollback Plan

If issues detected after deployment:

1. Revert this PR via GitHub
2. Force push main to previous commit
3. Notify team in Slack

---

Generated with [Claude Code](https://claude.com/claude-code)
```

### Step 5: Create PR

Use GitHub CLI to create PR:

```bash
# Create PR with generated body
gh pr create \
  --base main \
  --head v2 \
  --title "[TITLE]" \
  --body "[GENERATED_BODY]"

# Get PR URL
PR_URL=$(gh pr view --json url --jq '.url')
```

### Step 6: Report Results

Output PR creation summary:

```
## Production PR Created

**PR**: #123
**URL**: https://github.com/creepyblues/kstorybridge-integrated/pull/123
**Title**: feat: Add mandate matcher improvements

### Summary

- Commits: 5
- Files changed: 23
- Apps affected: dashboard, creator

### Affected Apps (Will Auto-Deploy)

- Dashboard: 15 files
- Creator: 8 files

### Next Steps

1. Review the PR at the URL above
2. Get approval from reviewer
3. Merge when ready
4. Monitor Vercel deployments after merge

### CI Status

Waiting for CI checks to complete...
Run `/pr-production --check` to see status.
```

## Check Mode (--check)

When using `--check`, analyze without creating PR:

```
## Production Readiness Check

**Branch**: v2
**Target**: main
**Status**: READY

### Changes Summary

- Commits ahead of main: 5
- Files changed: 23
- Apps affected: dashboard (15), creator (8)

### CI Status

| Check | Status |
|-------|--------|
| Build | PASS |
| Lint | PASS |
| Unit Tests | PASS |
| E2E Tests | PASS |

### Staging Verification

- [ ] Dashboard staging tested
- [ ] Creator staging tested

### Recommendations

Ready to create PR.
Run `/pr-production` to proceed.
```

## Notifications

### Console Output

```
Creating production PR...

[1/5] Pre-flight checks
      Branch: v2
      Clean: Yes
      Up to date: Yes

[2/5] Analyzing changes
      Commits: 5
      Files: 23
      Apps: dashboard, creator

[3/5] Generating PR body
      Title: feat: Add mandate matcher improvements
      Body: Generated (245 words)

[4/5] Creating PR
      PR #123 created

[5/5] Post-creation tasks
      CI status: Pending

PR created successfully!
URL: https://github.com/creepyblues/kstorybridge-integrated/pull/123
```

### Slack Notification

```json
{
  "text": "Production PR Created",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Production PR Created*\n<https://github.com/.../pull/123|PR #123: feat: Add mandate matcher>"
      }
    },
    {
      "type": "section",
      "fields": [
        {"type": "mrkdwn", "text": "*Commits*\n5"},
        {"type": "mrkdwn", "text": "*Files*\n23"},
        {"type": "mrkdwn", "text": "*Apps*\ndashboard, creator"},
        {"type": "mrkdwn", "text": "*Status*\nPending review"}
      ]
    }
  ]
}
```

### GitHub Comment

After CI completes, add status comment:

```markdown
## CI Status Update

All checks passed! Ready for review.

| Check | Status | Duration |
|-------|--------|----------|
| Build | PASS | 2m 15s |
| Lint | PASS | 45s |
| Unit Tests | PASS | 1m 30s |
| E2E Tests | PASS | 4m 20s |

This PR is ready to merge.
```

## Error Handling

### Not on v2 Branch

```
ERROR: Not on v2 branch

Current branch: feature/new-feature

To create a production PR, first merge your changes to v2:
  git checkout v2
  git merge feature/new-feature
  git push origin v2

Then run /pr-production again.
```

### Uncommitted Changes

```
ERROR: Uncommitted changes detected

Modified files:
- apps/dashboard/src/App.tsx
- apps/creator/src/pages/Home.tsx

Commit or stash changes before creating PR:
  git add .
  git commit -m "..."
  # or
  git stash
```

### v2 Behind main

```
WARNING: v2 is behind main

v2 is 3 commits behind main.

Rebase v2 on main before creating PR:
  git fetch origin
  git rebase origin/main
  git push origin v2 --force-with-lease

Or merge main into v2:
  git merge origin/main
  git push origin v2
```

### No Changes

```
ERROR: No changes to merge

v2 is up to date with main.

Nothing to deploy. Make changes to v2 first.
```

## Tips

- Use `--check` before `--create` to preview the PR
- Add custom title with `--title` for clarity
- Use `--draft` if you want review before marking ready
- Check Vercel deployment status after merging
- Keep PRs focused - consider smaller, more frequent releases

## Related Skills

- `/deploy-staging` - Deploy to staging before creating PR
- `/test-e2e` - Run E2E tests before creating PR
- `/push` - Existing skill for committing and pushing changes
