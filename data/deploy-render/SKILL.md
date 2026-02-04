---
name: deploy-render
description: Provides comprehensive Render.com deployment standards covering environment configuration, database migrations, cron jobs, health checks, log management, and production best practices for web services
---

# Render.com Deployment Standards

This skill provides complete guidelines for deploying applications to Render.com, covering all aspects from initial setup to production monitoring.

## Pre-Deployment Checklist

### Repository Requirements

- [ ] Code pushed to GitHub/GitLab/Bitbucket
- [ ] `package.json` with correct start script
- [ ] Build command configured (if using build step)
- [ ] `.gitignore` includes `.env`, `node_modules`, build artifacts
- [ ] Dependencies properly listed (not in devDependencies if needed for production)
- [ ] Database migrations ready (if applicable)
- [ ] Health check endpoint implemented

### Environment Preparation

- [ ] Production environment variables documented
- [ ] Secrets stored securely (not in repo)
- [ ] Database connection strings prepared
- [ ] Third-party API keys obtained
- [ ] Domain/subdomain configured (if using custom domain)

## Service Configuration

### Web Service Setup

**Basic Configuration:**

```yaml
# render.yaml (Infrastructure as Code - optional but recommended)
services:
  - type: web
    name: my-app
    env: node
    region: oregon
    plan: starter
    buildCommand: npm run build
    startCommand: npm start
    envVars:
      - key: NODE_ENV
        value: production
      - key: DATABASE_URL
        fromDatabase:
          name: my-postgres-db
          property: connectionString
      - key: API_KEY
        sync: false # Secret - set manually in dashboard
    healthCheckPath: /api/health
    autoDeploy: true
```

**Key Settings:**

| Setting | Recommended Value | Notes |
|---------|------------------|-------|
| Environment | Node, Docker, Python, etc. | Based on your stack |
| Region | oregon, frankfurt, singapore | Choose closest to users |
| Plan | starter → standard → pro | Scale based on traffic |
| Build Command | `npm run build` | Empty if no build step |
| Start Command | `npm start` | Must be defined |
| Auto-Deploy | `true` | Deploy on git push |
| Health Check | `/api/health` or `/health` | Critical for zero-downtime |

### Environment Variables

**Required Variables for Next.js:**

```bash
# Core
NODE_ENV=production
PORT=10000  # Render assigns this automatically

# Application
NEXT_PUBLIC_SITE_URL=https://your-app.onrender.com
NEXTAUTH_URL=https://your-app.onrender.com
NEXTAUTH_SECRET=your-secret-key-min-32-chars

# Database (if using Render PostgreSQL)
DATABASE_URL=${DATABASE_URL}  # Auto-populated from database connection

# Supabase (example)
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# External APIs
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
SENDGRID_API_KEY=SG...
```

**Setting Variables:**

**Via Dashboard:**
1. Go to your service → Environment
2. Add environment variables
3. Mark sensitive ones as "Secret"

**Via render.yaml:**
```yaml
envVars:
  - key: NODE_ENV
    value: production
  - key: DATABASE_URL
    fromDatabase:
      name: my-postgres-db
      property: connectionString
  - key: API_SECRET
    generateValue: true  # Auto-generate random value
  - key: STRIPE_KEY
    sync: false  # Must set manually (secret)
```

### Build & Start Commands

**Next.js:**
```yaml
buildCommand: npm install && npm run build
startCommand: npm start
```

**Vite/React:**
```yaml
buildCommand: npm install && npm run build
startCommand: npx serve -s dist -l $PORT
```

**Node.js/Express:**
```yaml
buildCommand: npm install
startCommand: npm start
```

**Docker:**
```yaml
dockerfilePath: ./Dockerfile
dockerCommand: npm start
```

**TypeScript:**
```yaml
buildCommand: npm install && npm run build
startCommand: node dist/index.js
```

## Database Configuration

### PostgreSQL Setup

**Create Database:**
1. Dashboard → New → PostgreSQL
2. Select region (same as web service)
3. Choose plan (Starter is free)
4. Database created with auto-generated credentials

**Connect to Web Service:**

```yaml
# render.yaml
databases:
  - name: my-postgres-db
    plan: starter
    region: oregon
    databaseName: myapp_db
    user: myapp_user

services:
  - type: web
    name: my-app
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: my-postgres-db
          property: connectionString
```

**Manual Connection String:**
```
postgresql://user:password@host:port/database
```

### Redis Setup (for caching/sessions)

```yaml
# render.yaml
services:
  - type: redis
    name: my-redis
    plan: starter
    region: oregon
    maxmemoryPolicy: allkeys-lru
```

**Environment Variable:**
```bash
REDIS_URL=${REDIS_URL}  # Auto-populated
```

## Database Migrations

### Prisma Migration Strategy

**Option 1: Run migrations in build command (Recommended)**

```yaml
buildCommand: npm install && npx prisma generate && npx prisma migrate deploy && npm run build
```

**Option 2: Separate migration job**

```yaml
# render.yaml
services:
  - type: worker
    name: migration-runner
    env: node
    buildCommand: npm install && npx prisma generate
    startCommand: npx prisma migrate deploy && exit 0
    plan: starter
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: my-postgres-db
          property: connectionString
```

### Drizzle Migration

```yaml
buildCommand: npm install && npm run db:migrate && npm run build
```

**Migration script in package.json:**
```json
{
  "scripts": {
    "db:migrate": "drizzle-kit push:pg",
    "db:generate": "drizzle-kit generate:pg"
  }
}
```

### Manual Migrations

For complex migrations, use a separate job:

```bash
# In your repo, create migrate.js
const { Pool } = require('pg');
const fs = require('fs');

async function runMigrations() {
  const pool = new Pool({ connectionString: process.env.DATABASE_URL });
  const sql = fs.readFileSync('./migrations/001_initial.sql', 'utf8');
  await pool.query(sql);
  await pool.end();
  console.log('Migrations complete');
}

runMigrations();
```

```yaml
# render.yaml
jobs:
  - type: cron
    name: run-migrations
    schedule: "@manual"  # Run manually
    command: node migrate.js
```

## Cron Jobs & Background Tasks

### Cron Job Configuration

```yaml
# render.yaml
services:
  - type: cron
    name: daily-cleanup
    schedule: "0 2 * * *"  # Every day at 2 AM UTC
    env: node
    buildCommand: npm install
    startCommand: node scripts/cleanup.js
    region: oregon
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: my-postgres-db
          property: connectionString
```

**Common Cron Schedules:**

| Schedule | Expression | Description |
|----------|-----------|-------------|
| Every hour | `0 * * * *` | At minute 0 |
| Every 6 hours | `0 */6 * * *` | At 00:00, 06:00, 12:00, 18:00 |
| Daily at 2 AM | `0 2 * * *` | Every day at 2:00 AM UTC |
| Weekly (Monday) | `0 0 * * 1` | Monday at midnight |
| Monthly (1st) | `0 0 1 * *` | 1st of month at midnight |

**Cron Expression Format:**
```
* * * * *
│ │ │ │ │
│ │ │ │ └─── Day of week (0-7, 0 and 7 = Sunday)
│ │ │ └───── Month (1-12)
│ │ └─────── Day of month (1-31)
│ └───────── Hour (0-23)
└─────────── Minute (0-59)
```

### Background Workers

```yaml
# render.yaml
services:
  - type: worker
    name: email-worker
    env: node
    buildCommand: npm install
    startCommand: node workers/email-processor.js
    plan: starter
    envVars:
      - key: REDIS_URL
        fromService:
          type: redis
          name: my-redis
          property: connectionString
```

**Example Worker (Bull Queue):**

```typescript
// workers/email-processor.js
import Queue from 'bull';

const emailQueue = new Queue('email', process.env.REDIS_URL);

emailQueue.process(async (job) => {
  const { to, subject, body } = job.data;
  // Send email logic
  console.log(`Sending email to ${to}`);
});

console.log('Email worker running...');
```

## Health Checks

### Implementation

**Express.js:**

```typescript
// routes/health.ts
app.get('/api/health', async (req, res) => {
  try {
    // Check database connection
    await db.query('SELECT 1');
    
    // Check Redis (if applicable)
    await redis.ping();
    
    res.status(200).json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      database: 'connected',
      redis: 'connected'
    });
  } catch (error) {
    res.status(503).json({
      status: 'unhealthy',
      error: error.message
    });
  }
});
```

**Next.js API Route:**

```typescript
// app/api/health/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // Basic health check
    return NextResponse.json({
      status: 'healthy',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    return NextResponse.json(
      { status: 'unhealthy', error: error.message },
      { status: 503 }
    );
  }
}
```

**Configuration in Render:**

```yaml
healthCheckPath: /api/health
```

Or via Dashboard:
- Service Settings → Health Check
- Path: `/api/health`
- Render will ping every 30 seconds
- 3 failed checks = service marked unhealthy

## Logging & Monitoring

### Structured Logging

```typescript
// utils/logger.ts
const logger = {
  info: (message: string, meta?: any) => {
    console.log(JSON.stringify({
      level: 'info',
      message,
      timestamp: new Date().toISOString(),
      ...meta
    }));
  },
  error: (message: string, error?: Error, meta?: any) => {
    console.error(JSON.stringify({
      level: 'error',
      message,
      error: error?.message,
      stack: error?.stack,
      timestamp: new Date().toISOString(),
      ...meta
    }));
  },
  warn: (message: string, meta?: any) => {
    console.warn(JSON.stringify({
      level: 'warn',
      message,
      timestamp: new Date().toISOString(),
      ...meta
    }));
  }
};

export default logger;
```

**Usage:**

```typescript
logger.info('User logged in', { userId: user.id });
logger.error('Database connection failed', error);
```

### Viewing Logs

**Via Dashboard:**
1. Go to your service
2. Click "Logs" tab
3. View real-time logs
4. Filter by date/time

**Via CLI:**
```bash
# Install Render CLI
npm install -g @render/cli

# Login
render login

# View logs
render logs my-app --tail
render logs my-app --since 1h
```

### Log Aggregation (Advanced)

**Integration with LogDNA/Datadog:**

```typescript
// Log forwarding
const logForwarder = require('logdna-winston');

const logger = winston.createLogger({
  transports: [
    new logForwarder({
      key: process.env.LOGDNA_KEY,
      app: 'my-app',
      env: process.env.NODE_ENV
    })
  ]
});
```

## Custom Domains

### Setup Steps

1. **Add domain in Render:**
   - Service Settings → Custom Domain
   - Enter your domain (e.g., `app.yourdomain.com`)

2. **Configure DNS:**
   - Add CNAME record pointing to Render

   ```
   Type: CNAME
   Name: app (or www)
   Value: your-app.onrender.com
   TTL: 3600
   ```

3. **SSL Certificate:**
   - Automatically provisioned by Render (Let's Encrypt)
   - Takes 5-10 minutes after DNS propagation

### Apex Domain (yourdomain.com)

```
Type: ALIAS or ANAME (if provider supports)
Name: @
Value: your-app.onrender.com

Or use A records (provided by Render in dashboard)
```

### Force HTTPS

```typescript
// middleware.ts (Next.js)
export function middleware(request: NextRequest) {
  const proto = request.headers.get('x-forwarded-proto');
  
  if (proto !== 'https') {
    return NextResponse.redirect(
      `https://${request.headers.get('host')}${request.nextUrl.pathname}`,
      301
    );
  }
}
```

## Scaling Configuration

### Horizontal Scaling

```yaml
# render.yaml
services:
  - type: web
    name: my-app
    scaling:
      minInstances: 1
      maxInstances: 10
      targetMemoryPercent: 80
      targetCPUPercent: 70
```

**Manual Scaling (via Dashboard):**
- Service Settings → Scaling
- Adjust instance count
- Immediate effect

### Vertical Scaling

**Upgrade Plan:**
- Starter (512 MB RAM, 0.5 CPU)
- Standard (2 GB RAM, 1 CPU)
- Pro (4 GB RAM, 2 CPU)
- Pro Plus (8 GB RAM, 4 CPU)

## Zero-Downtime Deployments

### Strategy

Render performs zero-downtime deployments automatically:

1. New version built
2. Health check passes on new instance
3. Traffic gradually shifted to new instance
4. Old instance terminated after drain period

**Ensure zero-downtime:**
- [ ] Health check endpoint returns 200
- [ ] Database migrations are backwards-compatible
- [ ] No breaking API changes

### Rollback

**Via Dashboard:**
1. Service → Deploys
2. Find previous successful deploy
3. Click "Rollback to this version"

**Via render.yaml:**
```bash
# Revert git commit and push
git revert HEAD
git push origin main
```

## Deployment Triggers

### Auto-Deploy

**Enable:**
```yaml
services:
  - type: web
    name: my-app
    autoDeploy: true  # Deploy on every push to main
    branch: main
```

**Manual Deploy:**
```yaml
autoDeploy: false
```

Deploy manually via:
- Dashboard → "Manual Deploy"
- CLI: `render deploy my-app`

### Deploy Hooks

**Webhook URL:**
- Service Settings → Deploy Hook
- Copy webhook URL
- Trigger deploys via HTTP POST

```bash
curl -X POST https://api.render.com/deploy/srv-xxx?key=xxx
```

**Use cases:**
- CI/CD pipelines
- Automated workflows
- External monitoring systems

## Production Best Practices

### Security

- [ ] Use environment secrets for sensitive data
- [ ] Enable HTTPS (automatic with Render)
- [ ] Set secure headers (helmet.js for Node)
- [ ] Implement rate limiting
- [ ] Use CORS properly
- [ ] Keep dependencies updated
- [ ] Run security audits (`npm audit`)

### Performance

- [ ] Enable compression (gzip/brotli)
- [ ] Implement caching (Redis, CDN)
- [ ] Optimize database queries (indexes, connection pooling)
- [ ] Use CDN for static assets
- [ ] Monitor response times
- [ ] Set appropriate timeouts

### Reliability

- [ ] Implement health checks
- [ ] Set up error tracking (Sentry, Rollbar)
- [ ] Configure alerting
- [ ] Test deployments in staging first
- [ ] Document rollback procedures
- [ ] Monitor resource usage (CPU, memory)

### Cost Optimization

- [ ] Use starter plan for low-traffic services
- [ ] Scale down non-production environments
- [ ] Use suspending services for dev/staging
- [ ] Optimize build times (caching)
- [ ] Monitor bandwidth usage

## Troubleshooting

### Common Issues

**Build Fails:**
```bash
# Check logs for error
# Common causes:
- Missing dependencies in package.json
- Build command incorrect
- Out of memory (upgrade plan)
```

**Service Won't Start:**
```bash
# Verify:
- Start command is correct
- Port binding: app.listen(process.env.PORT || 10000)
- Environment variables set correctly
```

**Database Connection Fails:**
```bash
# Check:
- DATABASE_URL is set
- Database is in same region
- IP allowlist (not needed on Render)
- Connection pool limits
```

**Health Check Fails:**
```bash
# Verify:
- /api/health endpoint exists
- Returns 200 status
- Responds within 10 seconds
- No dependencies fail (DB, Redis)
```

## Monitoring Checklist

- [ ] Health check endpoint responding
- [ ] Logs streaming properly
- [ ] Deployment notifications configured
- [ ] Error tracking integrated (Sentry, etc.)
- [ ] Database performance monitored
- [ ] Uptime monitoring (UptimeRobot, Pingdom)
- [ ] SSL certificate valid
- [ ] Custom domain resolving correctly
- [ ] Backup strategy in place (database)
- [ ] Disaster recovery plan documented

## Resources

- [Render Documentation](https://render.com/docs)
- [render.yaml Reference](https://render.com/docs/yaml-spec)
- [Deploy Hooks](https://render.com/docs/deploy-hooks)
- [Health Checks](https://render.com/docs/health-checks)

---

**Critical Reminder:** Always test deployments in a staging environment before pushing to production. Keep deployment scripts and documentation updated as your application evolves.