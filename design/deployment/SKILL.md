---
name: deployment
description: >
  Deployment and DevOps for EFT-Tracker using Coolify, Docker, and Nixpacks.
  Covers 3-tier validation, pre-push hooks, and production deployment.
  Activates when user mentions: deploy, deployment, Docker, Coolify,
  production, staging, nixpacks, build, CI/CD, pre-push, webhook.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Deployment Skill

## Deployment Flow

```
feature/* → PR → CI checks → merge to master → Coolify auto-deploy
```

**Production URL:** `https://learntotarkov.com`
**Deployment time:** ~3 minutes from merge to live

## 3-Tier Validation System

Pre-push hooks catch 95%+ of deployment failures locally:

### Tier 1: Quick Validation (~15-30s) - ALWAYS RUNS

- Nixpacks configuration valid
- No test packages in build (Chromium, Playwright)
- Required env vars documented
- Standalone build structure valid

### Tier 2: Full Validation (~2-3 min) - IF TYPESCRIPT CHANGED

- TypeScript type checking
- ESLint / Prettier
- All unit tests pass
- Prisma client generation

### Tier 3: Docker Build (~2-4 min) - IF DEPLOYMENT FILES CHANGED

Triggers if these files change:

- `nixpacks.toml`, `Dockerfile`, `package.json`
- `next.config.ts`, `pnpm-lock.yaml`, `.dockerignore`

Tests:

- Docker image builds
- Container starts
- Health checks pass

## Manual Validation Commands

```bash
# Tier 1: Quick checks only
bash scripts/test-coolify-build.sh --quick

# Tier 2: Nixpacks plan validation
bash scripts/test-coolify-build.sh --plan

# Tier 3: Full Docker build test
bash scripts/test-coolify-build.sh

# Force rebuild without cache
bash scripts/test-coolify-build.sh --no-cache
```

## Coolify Auto-Deployment

### How It Works

1. Code merged to `master`
2. GitHub webhook triggers Coolify
3. Coolify validates webhook signature
4. Deployment queued and executed:
   - Clone at commit SHA
   - Build Docker image
   - Run healthcheck
   - Rolling update (zero downtime)
   - Remove old container

### Webhook Configuration

- **URL:** `http://95.217.155.28:8000/webhooks/source/github/events/manual`
- **Events:** Push to master only
- **Secret:** HMAC-SHA256 signed

### Monitoring Deployments

**Coolify Dashboard:** `http://95.217.155.28:8000/`
Navigate: Projects → EFT-Tracker → Deployments

**Programmatic Monitoring:**

```typescript
import { getCoolifyAPIClient } from "@eft-tracker/utils";

const client = getCoolifyAPIClient();
const deployment = await client.getDeployment("uuid");
// Status: 'queued' | 'in_progress' | 'finished' | 'failed' | 'cancelled'
```

**API Routes:**

- `GET /api/deployment/status?deploymentId=<uuid>`
- `GET /api/deployment/logs?deploymentId=<uuid>`

## Common Issues

### Tier 1: "Sentry packages found"

```bash
cd apps/web && pnpm install
```

### Tier 1: "Standalone output not found"

```bash
cd apps/web && npm run build
```

### Tier 3: "Docker not running"

Start Docker Desktop. Only needed for Tier 3.

### Windows: EPERM errors on build

Enable Developer Mode in Windows Settings → Privacy & Security → For developers

Or let CI handle it - pre-push hook detects Windows and relies on CI.

## Files Reference

| File | Purpose |
| ---- | ------- |
| `scripts/test-coolify-build.sh` | Main testing script |
| `.husky/pre-push` | 3-tier validation hook |
| `nixpacks.toml` | Coolify build configuration |
| `.nixpacksignore` | Excludes test files from build |
| `.coolify-build/` | Temp build artifacts (git-ignored) |

## Environment Variables

**Required for deployment monitoring:**

- `COOLIFY_API_URL` - `http://95.217.155.28:8000/api/v1`
- `COOLIFY_API_TOKEN` - Bearer token (read-only)

## Deployment Checklist

### Before Merging

- [ ] All CI checks pass
- [ ] Pre-push validation passed
- [ ] No deployment-critical file changes without Tier 3 test
- [ ] Smoke tests ready to verify

### After Deployment

- [ ] Check Coolify dashboard for success
- [ ] Verify production URL responds
- [ ] Run smoke tests: `gh workflow run smoke-tests.yml`
- [ ] Monitor for errors in first 30 minutes

## Troubleshooting

### Deployment Failed in Coolify

1. Check Coolify logs (Dashboard → Deployments → View logs)
2. Common causes:
   - Missing env vars
   - Docker build failure
   - Healthcheck timeout
   - Port conflict

### Rollback

1. Go to Coolify Dashboard
2. Navigate to Deployments
3. Find last successful deployment
4. Click "Redeploy" on that commit

### Manual Deployment

If webhooks aren't working:

1. Coolify Dashboard → EFT-Tracker
2. Click "Redeploy" button
3. Wait for build (~3 min)

## Performance Notes

**Before (with Sentry):** 25+ min deployments
**After (Sentry removed):** ~3 min deployments

Local validation catches issues before the 3+ minute deployment cycle.
