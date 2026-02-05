---
name: encore-vercel-deploy
description: Automates deployment of Encore.ts backend and Next.js frontend to Encore Cloud and Vercel. Use this skill when deploying the full-stack application, setting up new environments, or troubleshooting deployment issues.
---

# Encore + Vercel Deployment Skill

Automates the deployment of full-stack applications with Encore.ts backend and Next.js frontend.

## When to Use This Skill

Use this skill when:
- Deploying backend to Encore Cloud and frontend to Vercel
- Setting up a fresh Encore app after git/deployment issues
- Configuring environment variables and secrets
- Connecting frontend to deployed backend
- Troubleshooting deployment failures

## Prerequisites

Before deployment, verify:
- Encore CLI installed and authenticated (`encore auth whoami`)
- Vercel CLI installed and authenticated (`vercel whoami`)
- Git repository with proper structure (no broken submodules)
- OpenAI API key available for agent services

## Deployment Process

### Step 1: Verify Git Structure

Ensure backend is NOT a git submodule:

```bash
# Check if backend is tracked properly
cd /path/to/project
git ls-tree HEAD backend
```

**If output shows mode `160000`** → Backend is a broken submodule. Fix it:

```bash
# Remove submodule reference
git rm --cached backend

# Add backend files properly
git add backend

# Commit
git commit -m "fix: properly add backend to git"
```

### Step 2: Create or Link Encore App

**Option A: Create New App (if starting fresh)**

```bash
cd /path/to/project
encore app create your-app-name

# Update backend/encore.app with new app ID
# Copy the app ID from output (e.g., your-app-name-xyz123)
```

Update `backend/encore.app`:
```json
{
  "id": "your-app-name-xyz123",
  "lang": "typescript",
  "global_cors": {
    "allow_origins_without_credentials": [
      "http://localhost:3000",
      "https://your-app.vercel.app",
      "https://your-app-*.vercel.app"
    ]
  }
}
```

**Option B: Link Existing App**

```bash
cd backend
encore app init  # Interactive linking
```

### Step 3: Configure Git Remote for Encore

```bash
# Remove old remote if exists
git remote remove encore 2>/dev/null

# Add Encore remote (use encore:// protocol)
git remote add encore encore://your-app-id

# Verify
git remote -v
```

### Step 4: Set Required Secrets

All agent services require `OpenAIApiKey`:

```bash
cd backend
encore secret set --type prod,dev OpenAIApiKey
# Paste your OpenAI API key when prompted
```

For additional secrets, repeat the command with different names.

### Step 5: Deploy Backend to Encore

```bash
# From project root
git add -A
git commit -m "feat: deploy to encore"
git push encore main:main
```

**Expected output:**
```
remote: main: triggered deploy https://app.encore.cloud/your-app-id/deploys/staging/...
```

**Deployment will be at:**
- Staging: `https://staging-your-app-id.encr.app`
- Dashboard: `https://app.encore.cloud/your-app-id`

### Step 6: Deploy Frontend to Vercel

**Set environment variable:**

```bash
cd frontend

# Add API URL (updates existing or creates new)
echo "https://staging-your-app-id.encr.app" | vercel env add NEXT_PUBLIC_API_URL production

# Or if variable exists, update via dashboard:
# https://vercel.com/your-team/your-project/settings/environment-variables
```

**Deploy:**

```bash
# Remove old project link if redeploying
rm -rf .vercel

# Deploy
vercel --prod --yes
```

**Alternative:** Push to GitHub if Vercel GitHub integration is configured.

### Step 7: Verify Deployment

**Backend health check:**
```bash
curl https://staging-your-app-id.encr.app/hello/World
# Should return: {"message":"Hello World!"}
```

**Frontend check:**
```bash
curl -I https://your-app.vercel.app
# Should return: 200 OK
```

**Test integration:**
- Open frontend URL
- Try sending a chat message
- Verify backend responds via SSE stream

## Common Issues & Solutions

### Issue: "repository not found" when pushing to Encore

**Cause:** Wrong git remote format or app not created

**Fix:**
```bash
# Verify app exists
encore auth whoami

# Recreate remote with encore:// protocol
git remote remove encore
git remote add encore encore://your-app-id
```

### Issue: "secret key(s) not defined: OpenAIApiKey"

**Cause:** Secrets not set before deployment

**Fix:**
```bash
cd backend
encore secret set --type prod,dev OpenAIApiKey
# Trigger redeploy
git commit --allow-empty -m "chore: redeploy after secrets"
git push encore main:main
```

### Issue: Backend showing old services (auth/portfolio instead of chat-gateway)

**Cause:** Backend was never properly pushed to git/Encore

**Fix:**
```bash
# Verify backend files are in git
git ls-files backend | head -20

# If empty or showing "backend" only → fix submodule issue
git rm --cached backend
git add backend
git commit -m "fix: add backend files"
git push origin main
git push encore main:main
```

### Issue: CORS errors between frontend and backend

**Cause:** Frontend domain not in `backend/encore.app` CORS config

**Fix:**

Update `backend/encore.app`:
```json
{
  "global_cors": {
    "allow_origins_without_credentials": [
      "http://localhost:3000",
      "https://your-actual-domain.vercel.app",
      "https://your-actual-domain-*.vercel.app"
    ]
  }
}
```

Then redeploy backend:
```bash
git add backend/encore.app
git commit -m "fix: update CORS for frontend"
git push encore main:main
```

### Issue: Vercel project named "frontend" instead of app name

**Fix:**
1. Go to Vercel project settings
2. Rename project to match desired domain
3. New URL will be `https://your-project-name.vercel.app`

## Quick Reference

### Encore Commands

```bash
# Check auth status
encore auth whoami

# Create new app
encore app create app-name

# List secrets
encore secret list

# View logs
encore logs --env=staging

# Get API URL
echo "https://staging-$(cat backend/encore.app | grep '"id"' | cut -d'"' -f4).encr.app"
```

### Vercel Commands

```bash
# Check auth
vercel whoami

# List projects
vercel list

# Set env var
vercel env add VAR_NAME production

# Deploy
vercel --prod

# Rollback
vercel rollback
```

### Git Commands

```bash
# Check for submodules
git ls-tree HEAD | grep 160000

# View remotes
git remote -v

# Push to multiple remotes
git push origin main
git push encore main:main
```

## Environment URLs

After successful deployment:

| Environment | Backend URL | Frontend URL |
|-------------|-------------|--------------|
| Local | `http://localhost:4000` | `http://localhost:3000` |
| Staging | `https://staging-{app-id}.encr.app` | `https://{project}.vercel.app` |
| Production | `https://prod-{app-id}.encr.app` | `https://{project}.vercel.app` |

## Security Notes

- Never commit `.env.local` or `.env.production` files
- Rotate OpenAI API keys regularly
- Use Encore's secret management for all sensitive values
- Enable Vercel password protection for preview deployments if needed

## Success Checklist

- [ ] Backend git structure verified (no broken submodules)
- [ ] Encore app created/linked with correct ID
- [ ] Git remote configured: `encore://app-id`
- [ ] OpenAI secret set in Encore
- [ ] Backend deployed successfully to Encore
- [ ] Frontend NEXT_PUBLIC_API_URL points to Encore staging
- [ ] Frontend deployed to Vercel
- [ ] CORS configured correctly in backend/encore.app
- [ ] Health check endpoints responding
- [ ] Frontend can communicate with backend

## Related Documentation

- Encore Deployment: https://encore.dev/docs/deploy/deploying
- Encore Secrets: https://encore.dev/docs/primitives/secrets
- Vercel CLI: https://vercel.com/docs/cli
- Vercel Environment Variables: https://vercel.com/docs/projects/environment-variables

