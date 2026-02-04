---
name: tsh-deploy
description: |
  Vercel deployment workflow for TSH Clients Console. Use when:
  (1) Deploying changes to production or staging
  (2) Checking deployment status
  (3) Troubleshooting deployment issues
  (4) Setting up environment variables
  (5) Managing domains and DNS
  (6) Running cache revalidation after deployment
---

# TSH Deployment

## Quick Deploy

```bash
# Deploy to PRODUCTION
cd "/Users/khaleelal-mulla/General/ Projects/tsh-clients-console"
vercel --prod --yes
```

## URLs

| Environment | URL |
|-------------|-----|
| **Production** | https://www.tsh.sale |
| **Staging** | https://staging.tsh.sale |
| **Vercel Default** | https://tsh-clients-console.vercel.app |

## Deployment Workflow

### 1. Pre-deployment Checks
```bash
# Run type check
npm run build

# Check for lint errors
npm run lint

# Verify environment variables
vercel env ls
```

### 2. Deploy to Staging (Optional)
```bash
vercel --yes
# Verify at staging.tsh.sale
```

### 3. Deploy to Production
```bash
vercel --prod --yes
```

### 4. Post-deployment
```bash
# Revalidate caches
curl "https://www.tsh.sale/api/revalidate?tag=all&secret=tsh-revalidate-2024"

# Verify site is up
curl -I https://www.tsh.sale
```

## Environment Variables

### Required Variables (Vercel Dashboard)

```bash
# Zoho OAuth
ZOHO_CLIENT_ID=<client_id>
ZOHO_CLIENT_SECRET=<client_secret>
ZOHO_REFRESH_TOKEN=<refresh_token>
ZOHO_ORGANIZATION_ID=748369814

# Upstash Redis (CRITICAL for token caching)
UPSTASH_REDIS_REST_URL=https://fine-mole-41883.upstash.io
UPSTASH_REDIS_REST_TOKEN=<token>

# NextAuth
NEXTAUTH_URL=https://www.tsh.sale
NEXTAUTH_SECRET=<secret>

# Email
RESEND_API_KEY=<api_key>
EMAIL_FROM=TSH <noreply@tsh.sale>
```

### Managing Variables
```bash
# List all variables
vercel env ls

# Add variable
vercel env add VARIABLE_NAME production preview

# Remove variable
vercel env rm VARIABLE_NAME production preview
```

## Domain Configuration

DNS Records (Namecheap):
```
www      CNAME   cname.vercel-dns.com
staging  CNAME   cname.vercel-dns.com
_vercel  TXT     <verification>
```

## Common Issues

### "Contact for price" after deploy
- Upstash Redis env vars missing
- Solution: Verify `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN`

### Stock/prices not updating
- Cache needs revalidation
- Solution: `curl "https://www.tsh.sale/api/revalidate?tag=all&secret=tsh-revalidate-2024"`

### Build fails
- Type errors
- Solution: Run `npm run build` locally first

### OAuth errors
- Token expired
- Solution: Generate new refresh token in Zoho API Console

## Vercel Dashboard

- **Project**: https://vercel.com/tsh-03790822/tsh-clients-console
- **Deployments**: Check deployment logs
- **Settings**: Environment variables, domains

## Rollback

```bash
# List recent deployments
vercel ls

# Promote previous deployment
vercel promote <deployment-url>
```

## Cache Revalidation

```bash
# All caches
curl "https://www.tsh.sale/api/revalidate?tag=all&secret=tsh-revalidate-2024"

# Specific tags
curl "https://www.tsh.sale/api/revalidate?tag=products&secret=tsh-revalidate-2024"
curl "https://www.tsh.sale/api/revalidate?tag=price-lists&secret=tsh-revalidate-2024"
```

## Deployment Checklist

- [ ] Run `npm run build` locally
- [ ] Fix any type/lint errors
- [ ] Commit all changes
- [ ] Deploy: `vercel --prod --yes`
- [ ] Wait for deployment to complete
- [ ] Verify site: `curl -I https://www.tsh.sale`
- [ ] Revalidate caches if needed
- [ ] Test critical pages (shop, login, dashboard)
