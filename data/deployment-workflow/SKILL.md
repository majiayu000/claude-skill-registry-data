---
name: deployment-workflow
description: GitHub commits, Vercel deployments, PWA configuration, and rollback procedures.
---

# Deployment Workflow

Complete deployment workflow: GitHub → Vercel → Production.

## When to Use
- Ready to deploy to production
- Creating releases
- PWA updates
- Deployment verification

## Philosophy
**ONE CODEBASE, ALL PLATFORMS**
- Single Next.js app deployed to Vercel
- PWA on phones = the website
- Git push → Vercel auto-deploys → everyone auto-updates

## Quick Deploy
```bash
npm run build && npm version patch && git push origin main
```

## Pre-Deployment Checklist
- [ ] `npm run build` passes
- [ ] `npm run lint` passes
- [ ] Database migrations applied (`supabase db push`)
- [ ] Environment variables set in Vercel
- [ ] PWA icons exist (`ls public/*.png`)

## Version Bump
```bash
npm version patch   # Bug fixes: 1.0.0 → 1.0.1
npm version minor   # Features: 1.0.0 → 1.1.0
npm version major   # Breaking: 1.0.0 → 2.0.0
```

## Rollback Options
1. **Vercel Dashboard** (30s): Deployments → Promote old version
2. **Git Revert** (2min): `git revert HEAD && git push origin main`
3. **Hotfix** (5min): Create hotfix branch, fix, merge, push

## Branch Strategy
- `main` → Production (empathyledger.com)
- `develop` → Staging (preview URL)
- `feature/*` → Feature branches (preview URL)

## Reference Files
| Topic | File |
|-------|------|
| Full checklist | `refs/checklist.md` |

## Related Skills
- `local-dev-server` - Local development
- `supabase-deployment` - Database deployment
- `cultural-review` - Pre-deploy cultural check
