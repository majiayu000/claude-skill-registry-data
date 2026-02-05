---
name: tzurot-deployment
description: Railway deployment operations for Tzurot v3 - Service management, log analysis, environment variables, health checks, and troubleshooting. Use when deploying, debugging production issues, or managing Railway infrastructure.
lastUpdated: '2025-12-20'
---

# Deployment Skill - Tzurot v3

**Use this skill when:** Deploying to Railway, checking logs, managing env vars, debugging production, or verifying service health.

## Quick Reference

```bash
# Check service status
railway status

# View logs
railway logs --service api-gateway --tail 50

# Health check
curl https://api-gateway-development-83e8.up.railway.app/health

# Set env variable
railway variables set KEY=value --service service-name
```

> **IMPORTANT**: Consult `docs/reference/RAILWAY_CLI_REFERENCE.md` for accurate Railway CLI 4.5.3 commands.

## Deployment Workflow

### Standard Process

1. **Merge PR to develop** (auto-deploys):

   ```bash
   gh pr merge <PR-number> --rebase
   ```

2. **Monitor deployment**:

   ```bash
   railway status --service api-gateway
   railway logs --service api-gateway --tail 100
   ```

3. **Verify health**:
   ```bash
   curl https://api-gateway-development-83e8.up.railway.app/health
   ```

### Rollback

```bash
# Revert last commit
git revert HEAD
git push origin develop
# Railway auto-deploys the revert
```

## Core Operations

### Viewing Logs

```bash
# Tail specific service
railway logs --service bot-client --tail 50

# Search for errors
railway logs --service api-gateway | grep "ERROR"

# Trace request across services
railway logs | grep "requestId:abc123"
```

### Environment Variables

```bash
# List all
railway variables --service api-gateway

# Set variable
railway variables set OPENROUTER_API_KEY=sk-or-v1-... --service ai-worker

# Delete variable
railway variables delete OLD_VAR_NAME --service ai-worker
```

### Database Operations

```bash
# Run migrations
railway run npx prisma migrate deploy

# Check migration status
railway run npx prisma migrate status

# Open Prisma Studio (local)
npx prisma studio
```

### Service Restart

```bash
railway restart --service bot-client
```

## Troubleshooting

| Symptom            | Check                           | Solution                    |
| ------------------ | ------------------------------- | --------------------------- |
| Service crashed    | `railway logs --tail 100`       | Check for missing env vars  |
| Slow responses     | `railway logs \| grep duration` | Check DB/Redis connection   |
| Bot not responding | `bot-client` logs               | Verify DISCORD_TOKEN        |
| Migration failed   | `prisma migrate status`         | Apply with `migrate deploy` |

### Service Won't Start

1. Check logs: `railway logs --service <name> --tail 100`
2. Verify env vars: `railway variables --service <name>`
3. Check DATABASE_URL and REDIS_URL are set

### Discord Bot Not Responding

1. Check bot-client logs
2. Verify health endpoint
3. Verify DISCORD_TOKEN is set
4. Check bot permissions in Discord server

## Railway Patterns

### Private Networking

```typescript
// ✅ Use Railway-provided URLs
const GATEWAY_URL = process.env.GATEWAY_URL; // Internal

// ❌ Don't use public URLs for internal calls
const GATEWAY_URL = 'https://api-gateway-xxx.up.railway.app';
```

### Connection Retry on Startup

```typescript
for (let attempt = 1; attempt <= 5; attempt++) {
  try {
    await prisma.$connect();
    break;
  } catch {
    await new Promise(r => setTimeout(r, 2000 * attempt));
  }
}
```

## Deployment Checklist

**Before**:

- [ ] Tests passing (`pnpm test`)
- [ ] Linting passing (`pnpm lint`)
- [ ] PR merged to `develop`

**After**:

- [ ] Services show "Running" status
- [ ] Health endpoint returns 200
- [ ] No ERROR logs in first 5 minutes
- [ ] Bot responds to test command

## Related Skills

- **tzurot-observability** - Log analysis and correlation IDs
- **tzurot-security** - Secret management
- **tzurot-git-workflow** - Deployment triggers

## References

- Railway CLI: `docs/reference/RAILWAY_CLI_REFERENCE.md`
- Railway deployment: `docs/deployment/RAILWAY_DEPLOYMENT.md`
- Railway docs: https://docs.railway.app/
