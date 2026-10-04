---
name: deploy-staging
description: Deploys specified app(s) to Vercel staging environment with build verification, smoke tests, and multi-channel notifications. This skill should be used when the user wants to deploy to staging, test a staging deployment, or push changes to the v2 branch staging environment.
---

# Deploy Staging

This skill automates the deployment of KStoryBridge apps to Vercel staging environments with comprehensive validation and notifications.

## When to Use This Skill

- Deploying apps to staging for testing
- Testing changes before production PR
- Verifying builds work in staging environment
- Running smoke tests on staging URLs

## Supported Apps

| App | Staging URL | Vercel Project |
|-----|-------------|----------------|
| dashboard | dashboard-staging.kstorybridge.com | dashboard-staging |
| creator | creator-staging.kstorybridge.com | creator-staging |
| website | kstorybridge.com (staging) | kstorybridge-website |

## Commands

```
/deploy-staging dashboard        # Deploy dashboard only
/deploy-staging creator          # Deploy creator only
/deploy-staging all              # Deploy all apps
/deploy-staging dashboard --skip-tests  # Skip smoke tests
```

## Deployment Workflow

When triggered, execute the following steps:

### Step 1: Pre-flight Checks

Verify the environment is ready for deployment:

```bash
# Verify on v2 branch
git branch --show-current

# Check for uncommitted changes
git status --porcelain

# Ensure latest changes are pulled
git pull origin v2
```

If not on v2 branch, warn the user and ask to confirm before proceeding.

### Step 2: Build Verification

Run a local build to catch errors before deploying:

```bash
# For single app
npm run build:[app]  # e.g., npm run build:dashboard

# For all apps
npm run build
```

If build fails, stop and report the error. Do not proceed to deployment.

### Step 3: Deploy to Vercel

Deploy using Vercel CLI:

```bash
# Change to app directory and deploy
cd apps/[app]
vercel --yes

# Capture the deployment URL from output
# Example: https://dashboard-staging-xxx.vercel.app
```

For deploying all apps, run deployments in sequence:
1. dashboard
2. creator
3. website

### Step 4: Smoke Tests (unless --skip-tests)

After deployment, verify the app is working:

```bash
# Wait for deployment to be ready (poll status)
# Then run basic health checks

# For dashboard
curl -s -o /dev/null -w "%{http_code}" https://[deployment-url]/

# For creator
curl -s -o /dev/null -w "%{http_code}" https://[deployment-url]/
```

Basic checks:
- HTTP 200 response from root
- Page loads without JavaScript errors
- Auth routes accessible (redirect to signin expected)

### Step 5: Report Results

Generate a deployment summary:

```
## Staging Deployment Summary

**App**: dashboard
**Branch**: v2
**Commit**: abc1234 - feat: Add new feature
**Deploy URL**: https://dashboard-staging-xxx.vercel.app
**Production URL**: https://dashboard-staging.kstorybridge.com
**Status**: SUCCESS
**Build Time**: 45s
**Deploy Time**: 1m 23s

### Smoke Tests
- Root page: PASS (200)
- Auth redirect: PASS (302 → /signin)
- Static assets: PASS

### Next Steps
1. Test your changes at the staging URL
2. When ready, run /pr-production to create a PR to main
```

## Notification Channels

### Console Output

Always show progress and results in terminal with clear formatting:

```
Deploying to staging...

[1/4] Pre-flight checks
      Branch: v2
      Clean: Yes

[2/4] Building dashboard...
      Build time: 23s

[3/4] Deploying to Vercel...
      URL: https://dashboard-staging-xxx.vercel.app

[4/4] Running smoke tests...
      Root: PASS
      Auth: PASS

Deployment successful!
```

### Slack Notification (if SLACK_WEBHOOK_URL set)

Post to Slack with deployment summary:

```bash
# Check if Slack webhook is configured
if [ -n "$SLACK_WEBHOOK_URL" ]; then
  curl -X POST -H 'Content-type: application/json' \
    --data '{"text":"Staging deployed: dashboard\nURL: https://...\nStatus: SUCCESS"}' \
    "$SLACK_WEBHOOK_URL"
fi
```

### GitHub PR Comment (if PR exists)

If there's an open PR for the current branch, add a comment:

```bash
# Find open PR for current branch
PR_NUMBER=$(gh pr list --head v2 --json number --jq '.[0].number')

if [ -n "$PR_NUMBER" ]; then
  gh pr comment $PR_NUMBER --body "## Staging Deployment\n\n..."
fi
```

## Error Handling

### Build Failures

If build fails:
1. Show the error message clearly
2. Suggest checking the specific file/line causing the issue
3. Do NOT proceed to deployment

### Deployment Failures

If Vercel deployment fails:
1. Check Vercel logs: `vercel logs [deployment-url]`
2. Report the failure with log excerpt
3. Suggest checking Vercel dashboard for more details

### Smoke Test Failures

If smoke tests fail:
1. Report which tests failed
2. The deployment is still live (user can investigate)
3. Suggest checking browser console for errors

## Environment Variables

Required for full functionality:

| Variable | Purpose | Required |
|----------|---------|----------|
| VERCEL_TOKEN | Vercel CLI authentication | Yes (or logged in) |
| SLACK_WEBHOOK_URL | Slack notifications | No |
| GITHUB_TOKEN | GitHub PR comments | No (uses gh CLI) |

## Tips

- Run `/deploy-staging dashboard --skip-tests` for faster iteration when testing minor changes
- Use `/deploy-staging all` before creating a production PR to verify all apps work together
- Check Vercel dashboard if deployment seems stuck
- If you get rate-limited, wait a few minutes and try again

## Related Skills

- `/pr-production` - Create a PR from v2 to main after staging testing
- `/deploy-functions` - Deploy Supabase edge functions
- `/test-e2e` - Run comprehensive E2E tests
