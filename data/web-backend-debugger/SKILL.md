---
name: web-backend-debugger
description: Debug voicelite-web backend including Supabase PostgreSQL, Prisma ORM, license validation API, and Stripe webhooks. Activates when working in voicelite-web directory or debugging API/database issues.
---

# Web Backend Debugger

Specialized debugging for VoiceLite's Next.js web backend (voicelite-web).

## When This Skill Activates

- Working in `voicelite-web/` directory
- Keywords: "Supabase", "Prisma", "license validation", "Stripe webhook", "database"
- API errors: `/api/*` routes failing, 500 errors, database connection issues
- Database operations: Migrations, queries, schema changes
- License issues: "License not found", "Invalid license key", "Activation failed"

## Tech Stack Overview

- **Framework**: Next.js 15.5.4 (App Router)
- **Database**: Supabase PostgreSQL
- **ORM**: Prisma 6.1.0
- **Payments**: Stripe 18.5.0
- **Deployment**: Vercel
- **Rate Limiting**: Upstash Redis

## Quick Health Check

```bash
cd voicelite-web

# 1. Database connection
npx prisma db pull --dry-run
# Expected: "Database schema is up to date"

# 2. Environment variables
grep -E "DATABASE_URL|STRIPE_SECRET|NEXT_PUBLIC" .env.local > /dev/null && echo "✓ Env OK" || echo "✗ Missing secrets"

# 3. Supabase status
curl -s "https://lvocjzqjqllouzyggpqm.supabase.co/rest/v1/" \
  -H "apikey: [ANON_KEY]" | grep -q "200" && echo "✓ Supabase OK"

# 4. Check latest migrations
npx prisma migrate status

# 5. Test Stripe webhook locally
stripe listen --forward-to localhost:3000/api/webhook
```

## License Validation Debugging

### Common Issue: "License not found in database"

**Check license exists**:
```sql
-- In Prisma Studio or Supabase SQL Editor
SELECT *
FROM "License"
WHERE "licenseKey" = 'YOUR-LICENSE-KEY-HERE';

-- Check activation count
SELECT COUNT(*)
FROM "LicenseActivation"
WHERE "licenseId" = 'license-id-here';
-- Should be ≤ 3 (max 3 devices)
```

**Check license status**:
```sql
SELECT
  l."licenseKey",
  l."email",
  l."status",
  l."stripeCustomerId",
  COUNT(la."id") as "activationCount"
FROM "License" l
LEFT JOIN "LicenseActivation" la ON l."id" = la."licenseId"
WHERE l."licenseKey" = 'YOUR-KEY'
GROUP BY l."id";
```

### Common Issue: "Rate limit exceeded"

**Check Upstash Redis rate limit**:
```bash
# Rate limit key format: license:validate:${ip}
# Max: 5 requests per hour per IP

# Check current count (if you have redis-cli)
redis-cli -h [UPSTASH_HOST] -p [PORT] -a [PASSWORD] \
  GET "license:validate:192.168.1.1"

# Or check in code: app/api/licenses/validate/route.ts
# Look for ratelimit.limit() call
```

**Temporary bypass for testing**:
```typescript
// app/api/licenses/validate/route.ts
// Comment out for LOCAL TESTING ONLY
// const { success } = await ratelimit.limit(identifier);
// if (!success) {
//   return NextResponse.json({ error: 'Rate limit exceeded' }, { status: 429 });
// }
```

### Common Issue: "Invalid license key format"

**Validate format**:
```typescript
// Expected format: UUID v4
// Example: 550e8400-e29b-41d4-a716-446655440000

const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

if (!uuidRegex.test(licenseKey)) {
  console.error('Invalid license key format');
}
```

## Prisma Migration Workflow

### Safe Migration Process

```bash
# Development workflow
cd voicelite-web

# 1. Make schema changes in prisma/schema.prisma

# 2. Create migration
npx prisma migrate dev --name add_new_field
# This auto-generates migration SQL

# 3. Verify migration
cat prisma/migrations/[timestamp]_add_new_field/migration.sql

# 4. Format schema
npx prisma format

# 5. Validate schema
npx prisma validate

# 6. Generate Prisma Client
npx prisma generate

# 7. Test locally
npm run dev
# Test affected API routes

# 8. Deploy to production (Vercel auto-runs migrations)
git push origin master
# Or manually:
npx prisma migrate deploy
```

### View Database in GUI

```bash
# Open Prisma Studio
npx prisma studio
# Opens at http://localhost:5555

# View tables:
# - License
# - LicenseActivation
# - LicenseEvent
# - WebhookEvent
# - Feedback
```

## Stripe Webhook Debugging

### Test Webhook Locally

```bash
# Terminal 1: Start Next.js dev server
cd voicelite-web && npm run dev

# Terminal 2: Forward Stripe events
stripe listen --forward-to localhost:3000/api/webhook

# Terminal 3: Trigger test event
stripe trigger checkout.session.completed
```

### Common Issue: Webhook signature verification failed

**Check webhook secret**:
```bash
# Get signing secret from Stripe CLI
stripe listen --print-secret

# Update .env.local
STRIPE_WEBHOOK_SECRET=whsec_...

# Or get from Stripe Dashboard:
# Developers → Webhooks → [your endpoint] → Signing secret
```

### Verify Webhook Event Stored

```sql
-- Check WebhookEvent table for deduplication
SELECT *
FROM "WebhookEvent"
WHERE "stripeEventId" = 'evt_...'
ORDER BY "createdAt" DESC
LIMIT 10;
```

## API Route Debugging

### Test License Validation Endpoint

```bash
# Test POST /api/licenses/validate
curl -X POST http://localhost:3000/api/licenses/validate \
  -H "Content-Type: application/json" \
  -d '{
    "licenseKey": "550e8400-e29b-41d4-a716-446655440000",
    "machineId": "test-machine-123"
  }'

# Expected response:
# {
#   "valid": true,
#   "email": "user@example.com",
#   "activationsRemaining": 2
# }
```

### Test Stripe Checkout

```bash
# Test POST /api/checkout
curl -X POST http://localhost:3000/api/checkout \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com"
  }'

# Expected: Stripe checkout session URL
```

## Database Query Optimization

### Find Slow Queries

```sql
-- Enable query logging in Supabase
-- Settings → Database → Query Performance

-- Check license validation performance
EXPLAIN ANALYZE
SELECT *
FROM "License" l
LEFT JOIN "LicenseActivation" la ON l."id" = la."licenseId"
WHERE l."licenseKey" = 'YOUR-KEY'
  AND l."status" = 'active';
```

### Add Index if Slow

```sql
-- Already indexed in schema.prisma:
-- @@index([licenseKey])
-- @@index([email])

-- Verify indexes exist
SELECT
  tablename,
  indexname,
  indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename = 'License';
```

## Environment Variables Checklist

```bash
# .env.local (NEVER commit!)

# Database
DATABASE_URL="postgresql://..."          # Supabase connection string
DIRECT_URL="postgresql://..."            # Direct connection (for migrations)

# Supabase
NEXT_PUBLIC_SUPABASE_URL="https://..."
NEXT_PUBLIC_SUPABASE_ANON_KEY="eyJ..."
SUPABASE_SERVICE_ROLE_KEY="eyJ..."       # Server-side only

# Stripe
STRIPE_SECRET_KEY="sk_..."               # Server-side only
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY="pk_..."
STRIPE_WEBHOOK_SECRET="whsec_..."

# Upstash Redis (rate limiting)
UPSTASH_REDIS_REST_URL="https://..."
UPSTASH_REDIS_REST_TOKEN="..."

# App
NEXT_PUBLIC_APP_URL="https://voicelite.app"
```

## Common Errors & Solutions

### Error: "Prisma Client not generated"

**Fix**:
```bash
npx prisma generate
```

### Error: "Cannot connect to database"

**Check**:
1. DATABASE_URL correct in .env.local
2. Supabase project not paused
3. IP whitelisted (if using IP restrictions)

**Fix**:
```bash
# Test connection
npx prisma db pull

# If fails, verify connection string format:
# postgresql://[user]:[password]@[host]:[port]/[database]?[params]
```

### Error: "Migration failed"

**Rollback**:
```bash
# View migration status
npx prisma migrate status

# Reset database (DESTRUCTIVE - local only!)
npx prisma migrate reset

# Re-apply migrations
npx prisma migrate deploy
```

## Production Deployment (Vercel)

### Deploy to Production

```bash
# Commit changes
git add .
git commit -m "fix: license validation bug"
git push origin master

# Vercel auto-deploys from master branch

# Or manual deploy
cd voicelite-web
vercel deploy --prod
```

### Check Production Logs

```bash
# View deployment logs
vercel logs --follow

# Or in Vercel Dashboard:
# Project → Deployments → [latest] → Function Logs
```

### Environment Variables in Vercel

```bash
# Set via CLI
vercel env add DATABASE_URL production

# Or in Vercel Dashboard:
# Project → Settings → Environment Variables
```

## Useful Prisma Commands

```bash
# View current database schema
npx prisma db pull

# Reset database (DESTRUCTIVE!)
npx prisma migrate reset

# Deploy pending migrations
npx prisma migrate deploy

# Create migration from schema changes
npx prisma migrate dev --name change_description

# Generate Prisma Client
npx prisma generate

# Open Prisma Studio (GUI)
npx prisma studio

# Validate schema
npx prisma validate

# Format schema file
npx prisma format
```

## Security Checklist

- [ ] NEVER commit `.env.local` (add to .gitignore)
- [ ] Use SUPABASE_SERVICE_ROLE_KEY only server-side
- [ ] Validate webhook signatures (Stripe, Supabase)
- [ ] Rate limit public endpoints (license validation)
- [ ] Sanitize SQL inputs (Prisma does this automatically)
- [ ] Use environment variables for all secrets
- [ ] Enable Row Level Security (RLS) in Supabase (if needed)
