---
name: deploy-vercel
description: Provides comprehensive Vercel deployment standards optimized for Next.js applications, covering environment configuration, edge functions, serverless architecture, database integration, cron jobs, and production best practices
---

# Vercel Deployment Standards

This skill provides complete guidelines for deploying applications to Vercel, with specific focus on Next.js optimizations and serverless architecture patterns.

## Pre-Deployment Checklist

### Repository Requirements

- [ ] Code pushed to GitHub/GitLab/Bitbucket
- [ ] Next.js project properly configured
- [ ] `package.json` with build scripts
- [ ] `.gitignore` includes `.env`, `.vercel`, `node_modules`
- [ ] Dependencies correctly categorized
- [ ] Database migrations strategy defined
- [ ] API routes follow serverless best practices

### Vercel-Specific Requirements

- [ ] `vercel.json` configured (optional but recommended)
- [ ] Environment variables documented
- [ ] Build output optimized
- [ ] Edge runtime considered for performance-critical routes
- [ ] ISR/SSG strategy defined

## Initial Setup

### Connect Repository

**Via Dashboard:**
1. Go to [vercel.com](https://vercel.com)
2. Click "Add New" → "Project"
3. Import Git Repository
4. Select repository
5. Configure project settings
6. Deploy

**Via CLI:**
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel

# Production deploy
vercel --prod
```

### Project Configuration

**vercel.json:**

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "rewrites": [
    { "source": "/api/:path*", "destination": "/api/:path*" }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ],
  "regions": ["iad1", "sfo1"],
  "crons": [
    {
      "path": "/api/cron/daily-cleanup",
      "schedule": "0 0 * * *"
    }
  ]
}
```

## Environment Variables

### Configuration

**Via Dashboard:**
1. Project Settings → Environment Variables
2. Add variables for each environment:
   - Production
   - Preview
   - Development

**Via CLI:**
```bash
# Add environment variable
vercel env add DATABASE_URL production

# Pull environment variables locally
vercel env pull .env.local
```

### Required Variables for Next.js

```bash
# Core Next.js
NODE_ENV=production  # Auto-set by Vercel
NEXT_PUBLIC_VERCEL_URL=${VERCEL_URL}  # Auto-provided

# Application URLs
NEXT_PUBLIC_SITE_URL=https://yourdomain.com
NEXTAUTH_URL=https://yourdomain.com
NEXTAUTH_SECRET=your-secret-min-32-chars

# Database (Vercel Postgres / Supabase / PlanetScale)
DATABASE_URL=postgresql://...
POSTGRES_URL=postgresql://...
POSTGRES_PRISMA_URL=postgresql://...  # For Prisma
POSTGRES_URL_NON_POOLING=postgresql://...  # For migrations

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...

# External Services
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
SENDGRID_API_KEY=SG...
OPENAI_API_KEY=sk-...

# Storage (Vercel Blob)
BLOB_READ_WRITE_TOKEN=vercel_blob_...

# KV (Vercel KV - Redis)
KV_REST_API_URL=https://...
KV_REST_API_TOKEN=...
KV_REST_API_READ_ONLY_TOKEN=...

# Edge Config (Feature flags)
EDGE_CONFIG=https://edge-config.vercel.com/...
```

### Environment Variable Types

**Public (Client-Side):**
- Must start with `NEXT_PUBLIC_`
- Exposed to browser
- Embedded at build time

**Private (Server-Side Only):**
- No prefix needed
- Available in API routes and Server Components
- Never exposed to client

**System Variables (Auto-provided by Vercel):**
- `VERCEL_URL` - Deployment URL
- `VERCEL_ENV` - production | preview | development
- `VERCEL_GIT_COMMIT_SHA` - Git commit hash
- `VERCEL_GIT_COMMIT_REF` - Git branch name

## Build Configuration

### Next.js Optimization

**next.config.js:**

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Production optimizations
  reactStrictMode: true,
  swcMinify: true,
  
  // Image optimization
  images: {
    domains: ['yourdomain.com', 'images.unsplash.com'],
    formats: ['image/avif', 'image/webp'],
  },
  
  // Headers
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on'
          },
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=63072000; includeSubDomains; preload'
          }
        ]
      }
    ]
  },
  
  // Redirects
  async redirects() {
    return [
      {
        source: '/old-page',
        destination: '/new-page',
        permanent: true,
      }
    ]
  },
  
  // Experimental features
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
}

module.exports = nextConfig
```

### Build Performance

**Optimize Build Times:**

```json
// package.json
{
  "scripts": {
    "build": "next build",
    "postbuild": "next-sitemap"
  }
}
```

**Turbopack (Faster Builds):**
```bash
# Use Turbopack for builds
next build --turbo
```

## Serverless Functions

### API Routes Configuration

**Function Config:**

```typescript
// app/api/users/route.ts
import { NextResponse } from 'next/server'

export const runtime = 'edge'  // or 'nodejs' (default)
export const maxDuration = 60  // seconds (Pro plan: 300s)
export const dynamic = 'force-dynamic'  // Disable caching

export async function GET(request: Request) {
  // Your logic here
  return NextResponse.json({ users: [] })
}
```

**Runtime Options:**

| Runtime | Use Case | Execution Time | Cold Start |
|---------|----------|----------------|------------|
| `edge` | Low-latency, simple logic | 30s (Hobby), 900s (Pro) | ~5ms |
| `nodejs` | Complex logic, libraries | 10s (Hobby), 300s (Pro) | ~100ms |

### Edge Functions

**When to Use Edge:**
- Authentication checks
- Geolocation-based routing
- A/B testing
- Bot detection
- Simple data fetching

**Example:**

```typescript
// app/api/geo/route.ts
export const runtime = 'edge'

export async function GET(request: Request) {
  const geo = request.headers.get('x-vercel-ip-country') || 'unknown'
  
  return new Response(JSON.stringify({ country: geo }), {
    headers: { 'content-type': 'application/json' }
  })
}
```

## Database Integration

### Vercel Postgres

**Setup:**
1. Dashboard → Storage → Create Database → Postgres
2. Automatically provisions connection strings
3. Environment variables auto-added

**Environment Variables (Auto-provided):**
```bash
POSTGRES_URL="postgresql://..."
POSTGRES_PRISMA_URL="postgresql://..."  # With pgBouncer
POSTGRES_URL_NON_POOLING="postgresql://..."  # Direct connection
```

**Connection:**

```typescript
// lib/db.ts
import { Pool } from '@vercel/postgres'

export const db = new Pool({
  connectionString: process.env.POSTGRES_URL,
})

// Usage
const { rows } = await db.query('SELECT * FROM users')
```

### Prisma Integration

**Prisma Setup:**

```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const prisma = globalForPrisma.prisma ?? new PrismaClient()

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma
```

**Database Migrations:**

```json
// package.json
{
  "scripts": {
    "postinstall": "prisma generate",
    "db:migrate": "prisma migrate deploy",
    "vercel-build": "prisma generate && prisma migrate deploy && next build"
  }
}
```

**Vercel Build Settings:**
```bash
# Build Command
npm run vercel-build

# This ensures migrations run before build
```

### Supabase Integration

```typescript
// lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)
```

## Cron Jobs

### Configuration

**vercel.json:**

```json
{
  "crons": [
    {
      "path": "/api/cron/daily-cleanup",
      "schedule": "0 0 * * *"
    },
    {
      "path": "/api/cron/send-reminders",
      "schedule": "0 9 * * *"
    },
    {
      "path": "/api/cron/weekly-report",
      "schedule": "0 10 * * 1"
    }
  ]
}
```

**Cron API Route:**

```typescript
// app/api/cron/daily-cleanup/route.ts
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  // Verify cron secret
  const authHeader = request.headers.get('authorization')
  if (authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  try {
    // Run cleanup logic
    await cleanupOldData()
    
    return NextResponse.json({ success: true })
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }
}

async function cleanupOldData() {
  // Your cleanup logic
  console.log('Running daily cleanup...')
}
```

**Cron Schedule Format:**

```
* * * * *
│ │ │ │ │
│ │ │ │ └─ Day of week (0-7)
│ │ │ └─── Month (1-12)
│ │ └───── Day of month (1-31)
│ └─────── Hour (0-23)
└───────── Minute (0-59)
```

**Examples:**
- Every hour: `0 * * * *`
- Daily at 2 AM: `0 2 * * *`
- Every Monday: `0 0 * * 1`
- First of month: `0 0 1 * *`

## Static & Dynamic Rendering

### Rendering Strategies

**Static Generation (SSG):**
```typescript
// app/blog/[slug]/page.tsx
export async function generateStaticParams() {
  const posts = await getPosts()
  return posts.map((post) => ({ slug: post.slug }))
}

export default async function BlogPost({ params }: { params: { slug: string } }) {
  const post = await getPost(params.slug)
  return <Article post={post} />
}
```

**Incremental Static Regeneration (ISR):**
```typescript
// app/products/[id]/page.tsx
export const revalidate = 3600  // Revalidate every hour

export default async function ProductPage({ params }: { params: { id: string } }) {
  const product = await getProduct(params.id)
  return <Product data={product} />
}
```

**Server-Side Rendering (SSR):**
```typescript
// app/dashboard/page.tsx
export const dynamic = 'force-dynamic'  // Always SSR

export default async function Dashboard() {
  const session = await getSession()
  const data = await getUserData(session.userId)
  return <DashboardView data={data} />
}
```

## Vercel KV (Redis)

### Setup

1. Dashboard → Storage → Create Database → KV
2. Select region
3. Environment variables auto-added

**Usage:**

```typescript
// lib/kv.ts
import { kv } from '@vercel/kv'

// Set value
await kv.set('user:123', { name: 'John' })

// Get value
const user = await kv.get('user:123')

// Set with expiration
await kv.setex('session:abc', 3600, { userId: '123' })

// Delete
await kv.del('user:123')

// Increment
await kv.incr('page:views')
```

**Rate Limiting Example:**

```typescript
// app/api/protected/route.ts
import { kv } from '@vercel/kv'
import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  const ip = request.headers.get('x-forwarded-for') || 'unknown'
  const key = `ratelimit:${ip}`
  
  const requests = await kv.incr(key)
  
  if (requests === 1) {
    await kv.expire(key, 60)  // 60 second window
  }
  
  if (requests > 10) {
    return NextResponse.json(
      { error: 'Too many requests' },
      { status: 429 }
    )
  }
  
  // Process request
  return NextResponse.json({ success: true })
}
```

## Vercel Blob (File Storage)

### Setup & Usage

```typescript
// Upload file
import { put } from '@vercel/blob'

export async function POST(request: Request) {
  const form = await request.formData()
  const file = form.get('file') as File
  
  const blob = await put(file.name, file, {
    access: 'public',
    token: process.env.BLOB_READ_WRITE_TOKEN,
  })
  
  return Response.json({ url: blob.url })
}

// List files
import { list } from '@vercel/blob'

const { blobs } = await list()

// Delete file
import { del } from '@vercel/blob'

await del(url)
```

## Monitoring & Logs

### Real-Time Logs

**Via Dashboard:**
- Project → Logs
- Filter by function, status, time range
- Search logs

**Via CLI:**
```bash
# Stream logs
vercel logs my-app --follow

# Logs from specific deployment
vercel logs my-app --deployment dpl_xxx

# Filter by function
vercel logs my-app --function /api/users
```

### Analytics

**Web Analytics (Built-in):**
- Dashboard → Analytics
- Page views, unique visitors
- Top pages, referrers
- Real-time data

**Speed Insights:**
- Core Web Vitals
- Performance metrics
- Real user monitoring

**Enable in next.config.js:**
```javascript
module.exports = {
  experimental: {
    webVitalsAttribution: ['CLS', 'LCP', 'FCP', 'FID', 'TTFB']
  }
}
```

### Error Tracking

**Integrate Sentry:**

```typescript
// sentry.config.ts
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.VERCEL_ENV,
  tracesSampleRate: 1.0,
})
```

## Custom Domains

### Setup

**Add Domain:**
1. Project Settings → Domains
2. Enter domain name
3. Choose domain type (apex or subdomain)

**Configure DNS:**

**For subdomain (www, app, etc.):**
```
Type: CNAME
Name: www
Value: cname.vercel-dns.com
TTL: 3600
```

**For apex domain (yourdomain.com):**
```
Type: A
Name: @
Value: 76.76.21.21

Type: AAAA (IPv6)
Name: @
Value: 2606:4700:4700::1111
```

**SSL Certificate:**
- Automatically provisioned
- Free via Let's Encrypt
- Auto-renewal

## Performance Optimization

### Image Optimization

```typescript
// Use Next.js Image component
import Image from 'next/image'

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority  // For above-the-fold images
  placeholder="blur"  // Better UX
/>
```

**next.config.js:**
```javascript
module.exports = {
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  }
}
```

### Edge Config (Feature Flags)

```typescript
// lib/feature-flags.ts
import { get } from '@vercel/edge-config'

export async function isFeatureEnabled(flag: string): Promise<boolean> {
  try {
    return await get(flag) || false
  } catch {
    return false
  }
}

// Usage
const newUIEnabled = await isFeatureEnabled('new-ui')
```

### Bundle Analysis

```bash
# Analyze bundle size
npm install -D @next/bundle-analyzer

# next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

module.exports = withBundleAnalyzer({
  // Your config
})

# Run analysis
ANALYZE=true npm run build
```

## Deployment Strategies

### Preview Deployments

**Automatic:**
- Every push to non-production branch creates preview
- Unique URL: `my-app-git-branch-username.vercel.app`
- Test changes before merging

**Comments on PRs:**
- Vercel bot comments with preview URL
- QA team can review
- Automatic updates on new commits

### Production Deployments

**Automatic:**
- Push to `main` branch triggers production deploy
- Alias to custom domain

**Manual:**
```bash
# Deploy to production
vercel --prod

# Rollback to previous deployment
vercel rollback
```

### Environment-Specific Builds

```typescript
// lib/config.ts
const config = {
  apiUrl: process.env.VERCEL_ENV === 'production'
    ? 'https://api.yourdomain.com'
    : process.env.VERCEL_ENV === 'preview'
    ? 'https://api-staging.yourdomain.com'
    : 'http://localhost:3001',
}
```

## Deployment Checklist

### Pre-Deployment

- [ ] All environment variables set
- [ ] Database migrations tested
- [ ] Build passes locally (`npm run build`)
- [ ] No console errors or warnings
- [ ] Images optimized
- [ ] API routes tested
- [ ] Authentication working
- [ ] Third-party integrations configured

### Post-Deployment

- [ ] Custom domain resolving correctly
- [ ] SSL certificate active
- [ ] Health check endpoint responding
- [ ] Database connection working
- [ ] Cron jobs running (check logs)
- [ ] Analytics tracking
- [ ] Error tracking configured
- [ ] Performance metrics monitored
- [ ] SEO meta tags correct
- [ ] Social share previews working

## Troubleshooting

### Build Errors

```bash
# Common issues:
- Missing dependencies → Check package.json
- TypeScript errors → Run tsc --noEmit
- Environment variable missing → Set in dashboard
- Out of memory → Upgrade plan or optimize build
```

### Runtime Errors

```bash
# Check:
- Function logs in dashboard
- Environment variables in deployment
- Database connection
- External API availability
```

### Performance Issues

```bash
# Investigate:
- Bundle size (use bundle analyzer)
- Slow database queries
- Unoptimized images
- Blocking server-side operations
- Cold starts (consider edge runtime)
```

## Best Practices

### Security

- [ ] Use environment secrets
- [ ] Implement CSRF protection
- [ ] Rate limit API routes
- [ ] Validate all inputs
- [ ] Sanitize user content
- [ ] Use secure headers
- [ ] Keep dependencies updated

### Performance

- [ ] Use ISR for dynamic content
- [ ] Implement edge caching
- [ ] Optimize images with next/image
- [ ] Minimize JavaScript bundle
- [ ] Use compression
- [ ] Lazy load components
- [ ] Prefetch critical routes

### Cost Optimization

- [ ] Use Edge functions where possible (cheaper)
- [ ] Implement proper caching strategies
- [ ] Optimize serverless function duration
- [ ] Use ISR instead of SSR when possible
- [ ] Monitor bandwidth usage
- [ ] Clean up unused deployments

## Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Documentation](https://nextjs.org/docs)
- [Vercel CLI Reference](https://vercel.com/docs/cli)
- [Edge Functions](https://vercel.com/docs/functions/edge-functions)
- [Serverless Functions](https://vercel.com/docs/functions/serverless-functions)

---

**Pro Tip:** Use preview deployments aggressively for QA. Every PR should have a working preview URL before merging to production.