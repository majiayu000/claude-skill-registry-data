---
name: deployment-workflows
description: CI/CD pipelines, zero-downtime deployments, infrastructure as code, and production deployment strategies
triggers: [deploy, deployment, CI/CD, pipeline, production, infrastructure, docker, kubernetes, vercel]
version: 1.0.0
agents: [devops-deployment-engineer, solutions-architect, security-specialist]
context_levels:
  minimal: Core deployment checklist and quick commands
  detailed: Complete CI/CD pipeline configurations
  full: Deployment scripts and IaC templates
---

# Deployment Workflows Skill

## Overview
This skill provides comprehensive deployment strategies including CI/CD pipelines, zero-downtime deployments, and infrastructure as code patterns for production-ready applications.

## When to Use This Skill
- Setting up deployment pipelines
- Configuring production infrastructure
- Implementing zero-downtime deployments
- Disaster recovery procedures
- Monitoring and alerting setup

## Pre-Deployment Checklist (Level 1 - Always Loaded)

### 🚀 Production Readiness Checklist

**Before deploying to production:**
- [ ] All tests passing (unit, integration, E2E)
- [ ] Test coverage ≥ 80%
- [ ] Security scan passed (no critical vulnerabilities)
- [ ] No hardcoded secrets
- [ ] Environment variables documented
- [ ] Database migrations tested
- [ ] Monitoring configured
- [ ] Logging implemented
- [ ] Error tracking setup (Sentry/equivalent)
- [ ] Rate limiting enabled
- [ ] HTTPS enforced
- [ ] Backup strategy defined
- [ ] Rollback plan documented
- [ ] Performance tested under load
- [ ] Documentation updated

## Zero-Downtime Deployment Strategy

### Blue-Green Deployment
```yaml
# Deploy new version (green) alongside old version (blue)
# Switch traffic once green is verified healthy

steps:
  1. Deploy new version (green) to separate infrastructure
  2. Run smoke tests on green environment
  3. Switch 10% of traffic to green (canary)
  4. Monitor metrics for 10 minutes
  5. If metrics healthy, switch 100% traffic to green
  6. Keep blue running for 1 hour (quick rollback if needed)
  7. Decommission blue environment
```

### Rolling Deployment
```yaml
# Update instances one at a time

steps:
  1. Remove instance from load balancer
  2. Deploy new version to instance
  3. Run health checks
  4. Add instance back to load balancer
  5. Repeat for next instance
  6. Monitor error rates between updates
```

### Database Migration Strategy
```typescript
// Safe migration pattern (zero-downtime)

// Step 1: Add new column (deploy v1.1)
// Migration: Add column with nullable constraint
ALTER TABLE users ADD COLUMN email_verified BOOLEAN;

// Application code: Write to both old and new schema
async function updateUser(userId: string, data: any) {
  // Write to new column if provided
  if (data.emailVerified !== undefined) {
    await db.query(
      'UPDATE users SET email_verified = $1 WHERE id = $2',
      [data.emailVerified, userId]
    );
  }
}

// Step 2: Backfill data (background job)
async function backfillEmailVerified() {
  // Migrate existing data in batches
  await db.query(`
    UPDATE users
    SET email_verified = false
    WHERE email_verified IS NULL
  `);
}

// Step 3: Make column non-nullable (deploy v1.2)
ALTER TABLE users ALTER COLUMN email_verified SET NOT NULL;

// Step 4: Remove old code paths (deploy v1.3)
```

## CI/CD Pipeline Configuration

### GitHub Actions Example
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

env:
  NODE_VERSION: '20.x'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run type check
        run: npm run type-check

      - name: Run tests
        run: npm test -- --coverage

      - name: Security scan
        run: npm audit --audit-level=high

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}

      - name: Build application
        run: npm run build

      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build
          path: dist/

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          name: build

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'

      - name: Run smoke tests
        run: npm run test:smoke -- --url=https://production-url.com

      - name: Notify deployment
        if: success()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: '✅ Deployed to production successfully'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## Environment Configuration

### Environment Variables Management
```bash
# .env.example (check into git)
# Document all required environment variables

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# API Keys (NEVER commit actual values)
API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here

# App Configuration
NODE_ENV=production
PORT=3000
LOG_LEVEL=info

# External Services
REDIS_URL=redis://localhost:6379
SENTRY_DSN=your_sentry_dsn_here
```

### Secrets Management
```typescript
// Runtime validation of required environment variables
import { z } from 'zod';

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  API_KEY: z.string().min(32),
  SECRET_KEY: z.string().min(32),
  NODE_ENV: z.enum(['development', 'production', 'test']),
  PORT: z.string().regex(/^\d+$/).transform(Number),
});

export const env = envSchema.parse(process.env);

// Type-safe environment variables
// Fails at startup if any required variable is missing
```

## Docker Configuration

### Dockerfile (Multi-stage Build)
```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 3: Production
FROM node:20-alpine AS runner
WORKDIR /app

# Security: Run as non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy only necessary files
COPY --from=deps --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
COPY --from=builder --chown=nextjs:nodejs /app/package.json ./

USER nextjs

EXPOSE 3000

ENV NODE_ENV production
ENV PORT 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js || exit 1

CMD ["node", "dist/server.js"]
```

### Docker Compose (Local Development)
```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_DB: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## Monitoring & Alerting

### Health Check Endpoint
```typescript
// /health endpoint for load balancers
app.get('/health', async (req, res) => {
  const checks = {
    uptime: process.uptime(),
    timestamp: Date.now(),
    status: 'healthy',
  };

  try {
    // Check database connection
    await db.raw('SELECT 1');
    checks.database = 'connected';

    // Check Redis connection
    await redis.ping();
    checks.redis = 'connected';

    res.status(200).json(checks);
  } catch (error) {
    checks.status = 'unhealthy';
    checks.error = error.message;
    res.status(503).json(checks);
  }
});

// Readiness check (for Kubernetes)
app.get('/ready', async (req, res) => {
  // Additional checks before accepting traffic
  const isReady = await checkDatabaseMigrations();

  if (isReady) {
    res.status(200).send('Ready');
  } else {
    res.status(503).send('Not ready');
  }
});
```

### Error Tracking Setup
```typescript
import * as Sentry from '@sentry/node';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1, // 10% of transactions for performance monitoring
  beforeSend(event, hint) {
    // Filter out sensitive data
    if (event.request) {
      delete event.request.cookies;
      delete event.request.headers?.Authorization;
    }
    return event;
  },
});

// Error handler middleware
app.use(Sentry.Handlers.errorHandler());
```

## Rollback Procedures

### Quick Rollback Steps
```bash
# 1. Identify last known good version
git log --oneline -10

# 2. Revert to previous deployment
# For Vercel
vercel rollback [deployment-url]

# For Kubernetes
kubectl rollout undo deployment/myapp

# For Docker
docker service update --rollback myapp

# 3. Verify rollback successful
curl https://myapp.com/health

# 4. Monitor error rates
# Check Sentry/Datadog for error spike reduction

# 5. Investigate root cause
# Review logs, error traces, recent changes
```

## Performance Optimization

### CDN Configuration
```typescript
// Cache-Control headers for static assets
app.use('/static', express.static('public', {
  maxAge: '1y', // 1 year for immutable assets
  immutable: true,
}));

// API response caching
app.get('/api/products', cacheMiddleware(300), async (req, res) => {
  // Cache for 5 minutes
  const products = await getProducts();
  res.json(products);
});
```

### Load Balancer Configuration
```nginx
# nginx.conf
upstream backend {
    least_conn; # Route to server with fewest connections
    server backend1:3000 max_fails=3 fail_timeout=30s;
    server backend2:3000 max_fails=3 fail_timeout=30s;
    server backend3:3000 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name myapp.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name myapp.com;

    # SSL configuration
    ssl_certificate /etc/ssl/certs/myapp.crt;
    ssl_certificate_key /etc/ssl/private/myapp.key;
    ssl_protocols TLSv1.2 TLSv1.3;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    location /api/ {
        limit_req zone=api burst=20;
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Deployment Checklist Summary

**Pre-deployment:**
- [ ] Tests pass
- [ ] Security scan clear
- [ ] Environment variables configured
- [ ] Database migrations ready

**During deployment:**
- [ ] Deploy to staging first
- [ ] Run smoke tests
- [ ] Monitor error rates
- [ ] Check performance metrics

**Post-deployment:**
- [ ] Verify health checks passing
- [ ] Monitor logs for errors
- [ ] Check user-facing functionality
- [ ] Keep previous version ready for rollback

**If issues occur:**
- [ ] Rollback immediately
- [ ] Investigate root cause
- [ ] Fix and redeploy

## Detailed CI/CD Patterns (Level 2 - Load on Request)

See companion files:
- `kubernetes-deployment.md` - K8s manifests and strategies
- `monitoring-setup.md` - Complete observability stack
- `disaster-recovery.md` - Backup and recovery procedures

## Deployment Scripts (Level 3 - Load When Needed)

See scripts directory:
- `scripts/deploy.sh` - Production deployment script
- `scripts/rollback.sh` - Quick rollback automation
- `scripts/smoke-test.sh` - Post-deployment validation

## Integration with Agents

**devops-deployment-engineer:**
- Primary agent for deployment tasks
- Uses this skill for CI/CD pipeline setup
- Implements monitoring and alerting

**solutions-architect:**
- Uses this skill for infrastructure design
- References patterns for scalability

**security-specialist:**
- Uses this skill to validate deployment security
- Reviews secret management and access controls

---

*Version 1.0.0 | Zero-Downtime Ready | Production Tested*
