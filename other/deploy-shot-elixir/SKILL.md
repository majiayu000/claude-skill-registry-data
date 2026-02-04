---
name: deploy-shot-elixir
description: Deploy the shot-elixir Elixir/Phoenix application to Fly.io. Use this skill when deploying backend changes, updating environment variables, or releasing new versions to production.
---

# Deploy shot-elixir to Fly.io

## Instructions

1. Navigate to the shot-elixir directory
2. Verify all changes are committed to git
3. Check that tests are passing (optional but recommended)
4. Execute the deployment using `fly deploy`
5. Monitor the deployment logs for errors
6. Verify the application is running on https://shot-elixir.fly.dev/
7. Test critical API endpoints after deployment

## Deployment Steps

```bash
# Navigate to shot-elixir
cd /Users/isaacpriestley/tech/isaacpriestley/chi-war/shot-elixir

# Verify git status
git status

# Deploy to Fly.io
fly deploy

# Monitor deployment
fly logs

# Verify health
curl https://shot-elixir.fly.dev/api/v2/health
```

## Examples

- User: "Deploy the latest changes to shot-elixir"
- User: "Release shot-elixir to production"
- User: "Push the backend changes to Fly.io"
- User: "Deploy elixir"
- User: "Update the production backend"

## Guidelines

- Always verify commits before deploying
- Check that environment variables are properly set on Fly.io
- Monitor deployment logs for errors
- Test critical endpoints after deployment (auth, campaigns, characters)
- Update documentation if configuration changes
- Deployment typically takes 2-3 minutes

## Post-Deployment Checks

- Test user authentication
- Verify WebSocket connections work
- Check database migrations applied successfully
- Test AI image generation endpoints
- Verify ActionCable/Phoenix Channels connectivity

## Troubleshooting

If deployment fails:

- Check `fly logs` for error messages
- Verify database connection with `fly ssh console`
- Check environment variables with `fly secrets list`
- Review recent git commits for breaking changes
- Rollback if needed: `fly releases rollback`
