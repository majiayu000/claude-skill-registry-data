---
name: CA Lobby Vercel Deployment
description: Vercel deployment workflow for CA Lobby React app with Clerk auth and BigQuery backend. Use when deploying CA Lobby, troubleshooting Vercel, or user says "deploy". Ensures proper configuration and verification.
extends: generic-skills/cloud-deployment
version: 1.0.0
---

# CA Lobby Vercel Deployment

## CA Lobby Configuration

**Cloud Provider:** Vercel
**Build Command:** `npm run build`
**Deployment Config:** `vercel.json`
**Framework:** React (Create React App)

## Required Environment Variables

### Clerk Authentication
- `REACT_APP_CLERK_PUBLISHABLE_KEY` - Clerk public key

### BigQuery (Optional - for backend mode)
- `GOOGLE_APPLICATION_CREDENTIALS` - BigQuery credentials

### Mode Configuration
- `REACT_APP_USE_BACKEND_API` - Demo mode flag (default: false)

## CA Lobby Pre-Deployment Checklist

- [ ] All tests passing (`npm test`)
- [ ] Build succeeds locally (`npm run build`)
- [ ] Demo mode functional (default mode)
- [ ] Clerk authentication configured
- [ ] Environment variables set in Vercel dashboard
- [ ] No console.log in production code
- [ ] Bundle size acceptable (<500KB)

## Deployment Verification

- [ ] Application loads successfully
- [ ] Clerk authentication works
- [ ] Demo data displays correctly
- [ ] Search functionality works
- [ ] Organization profiles accessible
- [ ] Navigation functional
- [ ] No console errors

---

## Changelog
### Version 1.0.0 (2025-10-20)
- Initial CA Lobby implementation
- Vercel-specific configuration
- Clerk + demo mode verification

---

**End of Skill**
