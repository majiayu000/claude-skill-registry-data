---
name: production-deploy
description: Production deployment checklist and procedures for Medellin Spark. Use when deploying to production, performing releases, or setting up production infrastructure.
version: 1.0.0
---

# Production Deploy Skill

## Purpose
Complete production deployment checklist ensuring security, performance, and reliability. This skill guides you through the entire deployment lifecycle.

---

## Quick Navigation

Choose the stage you need:

### 🔍 Pre-Deployment
**Before you deploy** - Quality, security, and verification checks
- See [PRE-DEPLOY.md](PRE-DEPLOY.md) for complete checklist
- Code quality, security verification, database checks

### 🚀 Deployment
**Actual deployment steps** - Frontend, backend, database
- See [DEPLOY.md](DEPLOY.md) for step-by-step guide
- Release commits, tagging, platform deployment

### ✅ Post-Deployment
**After deployment** - Verification and validation
- See [POST-DEPLOY.md](POST-DEPLOY.md) for verification steps
- Smoke tests, E2E tests, performance checks

### 📊 Monitoring
**Ongoing operations** - Logs, alerts, performance
- See [MONITORING.md](MONITORING.md) for setup guide
- Supabase logs, error tracking, monitoring setup

### 🔄 Rollback
**Emergency procedures** - When things go wrong
- See [ROLLBACK.md](ROLLBACK.md) for rollback steps
- Frontend, database, and Edge Function rollbacks

---

## Quick Commands

### Pre-Deploy Check (5 min)
```bash
pnpm tsc && pnpm lint && pnpm build && npx playwright test
```
✅ All must pass before deployment

### Deploy All (10 min)
```bash
# Frontend
netlify deploy --prod

# Edge Functions
supabase functions deploy chat && \
supabase functions deploy pitch-deck-assistant && \
supabase functions deploy generate-pitch-deck

# Migrations
supabase db push
```

### Post-Deploy Verify (5 min)
```bash
# Check deployment
curl -I https://your-domain.com

# Check Edge Functions
supabase functions list

# Check database
supabase db diff
```

---

## Production Readiness Checklist

### Pre-Deploy ✓
- [ ] Code compiles: `pnpm tsc --noEmit`
- [ ] Build succeeds: `pnpm build`
- [ ] Tests pass: `npx playwright test`
- [ ] No secrets in git
- [ ] RLS enabled
- [ ] Edge Functions deployed
- [ ] See [PRE-DEPLOY.md](PRE-DEPLOY.md) for details

### Deploy ✓
- [ ] Create release commit
- [ ] Tag release
- [ ] Deploy frontend
- [ ] Deploy Edge Functions
- [ ] Apply migrations
- [ ] See [DEPLOY.md](DEPLOY.md) for details

### Post-Deploy ✓
- [ ] Smoke test passes
- [ ] E2E tests pass
- [ ] Performance check
- [ ] Security verification
- [ ] Monitoring configured
- [ ] See [POST-DEPLOY.md](POST-DEPLOY.md) for details

---

## Success Criteria

✅ **Code Quality**: TypeScript compiles, build succeeds, tests pass
✅ **Security**: No secrets exposed, RLS enabled, HTTPS active
✅ **Performance**: Load time < 2s, Lighthouse 90+
✅ **Functionality**: All features work as expected
✅ **Monitoring**: Logs configured, alerts setup

---

## Emergency Contacts

**Supabase Support**: support@supabase.com
**Project Lead**: [Your contact]
**Deployment Platform**: [Netlify/Vercel support]

---

## Workflow Overview

```
Pre-Deploy Checks
    ↓
Create Release
    ↓
Deploy Frontend
    ↓
Deploy Backend
    ↓
Apply Migrations
    ↓
Post-Deploy Verification
    ↓
Setup Monitoring
    ↓
✅ Production Live
```

**For emergency rollback**: See [ROLLBACK.md](ROLLBACK.md)

---

*This skill ensures production deployments are secure, performant, and reliable. Start with [PRE-DEPLOY.md](PRE-DEPLOY.md) for your first deployment.*
