---
name: deploy-shot-client-next
description: Deploy the shot-client-next Next.js frontend application to Fly.io. Use this skill when deploying UI changes, updating environment variables, or releasing new versions to production.
---

# Deploy shot-client-next to Fly.io

## Instructions

1. Navigate to the shot-client-next directory
2. Run `npm run build` to verify the build succeeds locally
3. Verify all changes are committed to git
4. Execute the deployment using `fly deploy`
5. Monitor the deployment logs for build or startup errors
6. Verify the application is running on Fly.io
7. Test critical user flows in production (login, campaign management, fight creation)

## Deployment Steps

```bash
# Navigate to shot-client-next
cd /Users/isaacpriestley/tech/isaacpriestley/chi-war/shot-client-next

# Verify build succeeds
npm run build

# Verify git status
git status

# Deploy to Fly.io
fly deploy

# Monitor deployment
fly logs

# Verify health
curl https://[your-app-name].fly.dev
```

## Examples

- User: "Deploy the latest frontend changes"
- User: "Release the new UI updates to Fly.io"
- User: "Push the Next.js updates to production"
- User: "Deploy the client"
- User: "Update the production frontend"
- User: "Deploy shot-client-next"

## Guidelines

- Always verify the build succeeds locally before deploying
- Ensure API endpoint URLs are correct for production environment
- Monitor deployment logs for build or startup errors
- Test responsive design and critical flows after deployment
- Clear browser cache when testing UI changes
- Verify WebSocket connections work properly
- Deployment typically takes 3-5 minutes (includes Docker build)

## Pre-Deployment Checklist

- [ ] All changes committed to git
- [ ] `npm run build` succeeds locally
- [ ] No TypeScript errors
- [ ] Environment variables configured in Fly.io
- [ ] API base URL points to correct backend

## Post-Deployment Checks

- Test user login/registration
- Verify campaign switching works
- Test WebSocket real-time updates
- Check fight creation and management
- Test character creation with AI image generation
- Verify autocomplete components work
- Test drawer forms and modals
- Check responsive design on mobile

## Environment Variables

Ensure these are set on Fly.io:

- `NEXT_PUBLIC_API_URL` - Backend API URL (https://shot-elixir.fly.dev)
- `NEXT_PUBLIC_WS_URL` - WebSocket URL
- Any other required environment variables

## Troubleshooting

If deployment fails:

- Check `fly logs` for build errors
- Verify Next.js build succeeds locally
- Check environment variables with `fly secrets list`
- Review recent git commits for breaking changes
- Test API connectivity from production environment
- Rollback if needed: `fly releases rollback`

## Docker Build Notes

- Uses Node.js 18+ base image
- Multi-stage build for optimized image size
- Production build with `npm run build`
- Deployment process caches layers for faster rebuilds
