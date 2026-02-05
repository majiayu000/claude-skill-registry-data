---
name: vercel-deploy-debug
description: Debug Vercel deployment issues for the CoinSite Astro project. Use this skill when deployments fail, when checking deployment status after pushing to GitHub, or when investigating runtime errors on the deployed site. Provides CLI-based debugging workflow for Astro + Vercel SSR deployments.
---

# Vercel Deploy Debug

## Overview

This skill provides a systematic workflow for debugging Vercel deployment issues specific to the CoinSite project (Astro 5 with SSR, @astrojs/vercel adapter, Astro DB with Turso).

## CRITICAL: Deployment Method

**GitHub auto-deploys to Vercel on every `git push`.** Each push = one deployment.

### NEVER use manual Vercel CLI deploys:
```bash
# WRONG - Creates duplicate deployments
vercel deploy --prod
vercel --prod
```

### Minimize deployments with this workflow:

The bd git hooks automatically flush beads changes to JSONL on `git commit`, so you don't need separate `bd sync` calls.

**Optimized single-deployment workflow:**
```bash
# 1. Work on the issue (claim, code, close)
bd update <id> --status=in_progress
# ... make code changes ...
bd close <id>

# 2. Stage EVERYTHING (code + beads) in one commit
git add -A
git commit -m "Your message"

# 3. ONE push = ONE deployment
git push
```

**Why this works:**
- `bd update` and `bd close` modify the local database
- The pre-commit hook flushes these to `.beads/issues.jsonl`
- `git add -A` stages both code AND beads changes
- Single `git push` triggers exactly one Vercel deployment

**Avoid these patterns (cause multiple deployments):**
```bash
# BAD: Calling bd sync separately pushes to git
bd sync  # <-- This pushes, triggering a deployment!
git push # <-- This ALSO pushes, another deployment!

# BAD: Multiple commits with pushes between
git commit && git push  # deployment 1
bd sync                 # deployment 2
```

### End-of-session checklist:
```bash
git status                    # Check what changed
bd close <ids>                # Close completed issues
git add -A                    # Stage everything
git commit -m "..."           # Commit (hooks flush beads)
git push                      # ONE deployment
```

## When To Use This Skill

- After pushing changes to GitHub when deployment fails
- When the deployed site shows 500 errors or unexpected behavior
- When Vercel build logs show errors
- To verify deployment status and configuration

## Automated Health Check

Run the comprehensive health check script to automatically:
1. Fetch the latest Vercel deployment
2. Check deployment status (Ready/Error/Building)
3. Scan build logs for errors
4. Scan runtime logs for errors
5. Test key pages on lordmarcovan.com for HTTP errors

```bash
npx tsx .claude/skills/vercel-deploy-debug/scripts/deployment-health-check.ts
```

Optionally pass a specific deployment URL:
```bash
npx tsx .claude/skills/vercel-deploy-debug/scripts/deployment-health-check.ts https://coinsite-xxx.vercel.app
```

## Manual Diagnostic Workflow

### Step 1: Check Deployment Status

List recent deployments to see current state:

```bash
vercel ls
```

This shows deployment URLs, status (Ready, Error, Building), and timestamps.

### Step 2: Inspect Specific Deployment

Get detailed info about a deployment:

```bash
vercel inspect <deployment-url>
```

Shows build output, function regions, and configuration details.

### Step 3: View Build/Runtime Logs

Check logs for a specific deployment:

```bash
vercel logs <deployment-url>
```

Add `--follow` to stream logs in real-time during builds.

### Step 4: Check Environment Variables

Verify environment variables are set correctly:

```bash
vercel env ls
```

For Astro DB with Turso, ensure these are set in Vercel:
- `ASTRO_DB_REMOTE_URL` - Turso database URL
- `ASTRO_DB_APP_TOKEN` - Turso auth token

## Common Errors and Solutions

### NoAdapterInstalled Error

**Symptom**: Build fails with "NoAdapterInstalled" or adapter not found.

**Causes**:
1. `astro.config.mjs` is gitignored and not deployed
2. Wrong import path for adapter version

**Diagnostic**:
```bash
# Check if astro.config.mjs is tracked
git ls-files astro.config.mjs

# Check .gitignore for problematic patterns
grep -E "^\*\.mjs|astro" .gitignore
```

**Fix**:
- Ensure `astro.config.mjs` is NOT in .gitignore
- For @astrojs/vercel v8.x, use: `import vercel from '@astrojs/vercel/serverless'`
- For @astrojs/vercel v9.x, use: `import vercel from '@astrojs/vercel'`

### libsql Native Module Error

**Symptom**: Runtime 500 errors with "Could not locate libsql native module".

**Cause**: Deploying prebuilt output from macOS to Vercel's Linux environment.

**Fix**: Always use Vercel's remote build (default). Do NOT use:
```bash
# WRONG - builds locally then deploys
vercel build --prod && vercel deploy --prebuilt
```

Instead push to GitHub and let Vercel build remotely.

### Cached Prebuilt Artifacts

**Symptom**: Vercel uses old prebuilt output instead of building fresh.

**Diagnostic**:
```bash
vercel inspect <url>
# Look for "Using prebuilt output" in logs
```

**Fix**:
1. Delete `.vercel/output` directory locally
2. In Vercel dashboard: Settings > Git > "Clear Build Cache & Redeploy"
3. Or set environment variable: `VERCEL_FORCE_NO_BUILD_CACHE=1`

### SSL Certificate Issues

**Symptom**: Some browsers show certificate errors or different issuer.

**Diagnostic**:
```bash
# Check certificate chain
curl -v https://your-domain.vercel.app 2>&1 | grep -A 5 "SSL certificate"

# Detailed SSL check
openssl s_client -connect your-domain.vercel.app:443 -servername your-domain.vercel.app </dev/null 2>/dev/null | openssl x509 -noout -issuer -subject
```

**Note**: Vercel uses Let's Encrypt certificates. If you see a different issuer (e.g., NordVPN), it's client-side TLS interception by VPN/security software, not a server issue.

## Project-Specific Configuration

### Current Setup (CoinSite)

- **Framework**: Astro 5 with SSR (`output: 'server'`)
- **Adapter**: `@astrojs/vercel` v8.2.7 (use `/serverless` import)
- **Database**: Astro DB with Turso (requires `--remote` flag for builds)
- **Build command**: `astro build --remote`

### astro.config.mjs Template

```javascript
import db from '@astrojs/db';
import vercel from '@astrojs/vercel/serverless';  // v8.x path
import { defineConfig } from 'astro/config';

export default defineConfig({
  output: 'server',
  adapter: vercel(),
  integrations: [db()],
});
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `npx tsx ...health-check.ts` | Run automated health check |
| `vercel ls` | List deployments |
| `vercel inspect <url>` | Deployment details |
| `vercel logs <url>` | View logs |
| `vercel env ls` | List env vars |
| `vercel env pull` | Pull env vars to local .env |
| `git push` | Deploy to production (auto-triggers Vercel) |

## Resources

- `scripts/deployment-health-check.ts` - Automated health check script
- `references/common-errors.md` - Detailed error messages and stack traces
