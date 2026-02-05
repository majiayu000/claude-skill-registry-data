---
name: deploy-rails-client
description: Deploy the shot-client-next frontend to Fly.io using RAILS BACKEND configuration (shot-client-next app). Use this skill ONLY when specifically deploying to the legacy Rails backend at shot-counter.fly.dev.
---

# Deploy Rails Frontend Client to Fly.io

## ⚠️ IMPORTANT: This deploys to the LEGACY RAILS backend configuration

This skill deploys the Next.js frontend configured to connect to the **Ruby on Rails backend** at `shot-counter.fly.dev`.

- **Fly.io App**: `shot-client-next`
- **Config File**: `fly.toml`
- **Backend**: Rails (shot-counter.fly.dev) - **LEGACY**
- **WebSocket**: ActionCable at `wss://shot-counter.fly.dev/cable`
- **Environment**: No `NEXT_PUBLIC_BACKEND_TYPE` (defaults to Rails)

## ⚠️ When NOT to Use This Skill

**DO NOT use this skill for:**
- Regular production deployments (use `deploy-phoenix-client` instead)
- User says "deploy the frontend" without specifying Rails
- User says "deploy to production"

**ONLY use this skill when:**
- User explicitly says "deploy to Rails client"
- User explicitly says "deploy with Rails backend"
- Testing Rails backend compatibility
- User specifically mentions shot-client-next app

## Quick Deployment

```bash
cd /Users/isaacpriestley/tech/isaacpriestley/chi-war/shot-client-next
./deploy_rails.sh
```

## Manual Deployment Steps

```bash
# Navigate to shot-client-next
cd /Users/isaacpriestley/tech/isaacpriestley/chi-war/shot-client-next

# Verify build succeeds
npm run build

# Deploy to Fly.io with Rails configuration
fly deploy --app shot-client-next -c fly.toml

# Monitor deployment
fly logs --app shot-client-next

# Verify health
curl https://shot-client-next.fly.dev
```

## Environment Variables (fly.toml)

These are configured in the build args:
- `NEXT_PUBLIC_API_BASE_URL=https://shot-counter.fly.dev`
- `NEXT_PUBLIC_SERVER_URL=https://shot-counter.fly.dev`
- `NEXT_PUBLIC_WEBSOCKET_URL=wss://shot-counter.fly.dev`
- **NO** `NEXT_PUBLIC_BACKEND_TYPE` (defaults to Rails)

## Post-Deployment Verification

After deployment, verify:
1. WebSocket connection uses ActionCable `/cable` endpoint
2. Check browser console for ActionCable connection messages
3. API calls go to `shot-counter.fly.dev`
4. Rails backend is running and responding

## Related Skills

- `deploy-phoenix-client` - Deploy frontend with Phoenix backend (PRIMARY/PRODUCTION)
- `deploy-shot-elixir` - Deploy the Phoenix/Elixir backend
