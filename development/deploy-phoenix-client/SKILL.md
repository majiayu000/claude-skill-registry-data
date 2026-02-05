---
name: deploy-phoenix-client
description: Deploy the shot-client-next frontend to Fly.io using PHOENIX BACKEND configuration (shot-client-phoenix app). Use this skill when deploying the production frontend that connects to the Elixir/Phoenix backend at shot-elixir.fly.dev.
---

# Deploy Phoenix Frontend Client to Fly.io

## ⚠️ IMPORTANT: This deploys to the PHOENIX backend configuration

This skill deploys the Next.js frontend configured to connect to the **Elixir/Phoenix backend** at `shot-elixir.fly.dev`.

- **Fly.io App**: `shot-client-phoenix`
- **Config File**: `fly-phoenix.toml`
- **Backend**: Phoenix/Elixir (shot-elixir.fly.dev)
- **WebSocket**: Phoenix Channels at `wss://shot-elixir.fly.dev/socket`
- **Environment**: `NEXT_PUBLIC_BACKEND_TYPE=phoenix`

## Quick Deployment

```bash
cd /Users/isaacpriestley/tech/isaacpriestley/chi-war/shot-client-next
./deploy_phoenix.sh
```

## Manual Deployment Steps

```bash
# Navigate to shot-client-next
cd /Users/isaacpriestley/tech/isaacpriestley/chi-war/shot-client-next

# Verify build succeeds
npm run build

# Deploy to Fly.io with Phoenix configuration
fly deploy --app shot-client-phoenix -c fly-phoenix.toml

# Monitor deployment
fly logs --app shot-client-phoenix

# Verify health
curl https://shot-client-phoenix.fly.dev
```

## When to Use This Skill

Use this skill when:
- Deploying frontend changes to **production** (Phoenix backend is primary)
- User says "deploy to production"
- User says "deploy the frontend" or "deploy the client"
- User says "deploy Phoenix client"
- Releasing UI updates to the live application

## Environment Variables (fly-phoenix.toml)

These are configured in the build args:
- `NEXT_PUBLIC_API_BASE_URL=https://shot-elixir.fly.dev`
- `NEXT_PUBLIC_SERVER_URL=https://shot-elixir.fly.dev`
- `NEXT_PUBLIC_WEBSOCKET_URL=wss://shot-elixir.fly.dev`
- `NEXT_PUBLIC_BACKEND_TYPE=phoenix` ← **Critical for Phoenix channels**

## Post-Deployment Verification

After deployment, verify:
1. WebSocket connection uses Phoenix Channels (not Rails ActionCable `/cable`)
2. Check browser console for: `[PhoenixChannelClient] Socket connection opened`
3. NO errors about `/cable` endpoint
4. Factions dropdown doesn't spin endlessly
5. Real-time fight updates work correctly

## Troubleshooting

**WebSocket connects to `/cable` instead of `/socket`:**
- Verify `NEXT_PUBLIC_BACKEND_TYPE=phoenix` is set in `fly-phoenix.toml`
- Check build logs show Phoenix backend configuration
- Clear browser cache and hard reload

**Build fails:**
- Check `npm run build` succeeds locally
- Review TypeScript errors
- Check `fly logs --app shot-client-phoenix`

## Related Skills

- `deploy-rails-client` - Deploy frontend with Rails backend (legacy)
- `deploy-shot-elixir` - Deploy the Phoenix/Elixir backend
