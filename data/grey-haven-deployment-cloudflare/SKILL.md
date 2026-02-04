---
name: grey-haven-deployment-cloudflare
description: Deploy TanStack Start applications to Cloudflare Workers/Pages with GitHub Actions, Doppler, Wrangler, database migrations, and rollback procedures. Use when deploying Grey Haven applications.
# v2.0.43: Skills to auto-load for deployment work
skills:
  - grey-haven-code-style
  - grey-haven-observability-monitoring
# v2.0.74: Tools for deployment work
allowed-tools:
  - Read
  - Write
  - MultiEdit
  - Bash
  - Grep
  - Glob
  - TodoWrite
---

# Grey Haven Cloudflare Deployment

Deploy **TanStack Start** applications to Cloudflare Workers using GitHub Actions, Doppler for secrets, and Wrangler CLI.

## Deployment Architecture

### TanStack Start on Cloudflare Workers
- **SSR**: Server-side rendering with TanStack Start server functions
- **Edge Runtime**: Global deployment on Cloudflare's edge network
- **Database**: PostgreSQL (PlanetScale) with connection pooling
- **Cache**: Cloudflare KV for sessions, R2 for file uploads
- **Secrets**: Managed via Doppler, injected in GitHub Actions

### Core Infrastructure
- **Workers**: Edge compute (TanStack Start)
- **KV Storage**: Session management
- **R2 Storage**: File uploads and assets
- **D1 Database**: Edge data (optional)
- **Queues**: Background jobs (optional)

## Wrangler Configuration

### Basic `wrangler.toml`
```toml
name = "grey-haven-app"
main = "dist/server/index.js"
compatibility_date = "2025-01-15"
node_compat = true

[vars]
ENVIRONMENT = "production"
DATABASE_POOL_MIN = "2"
DATABASE_POOL_MAX = "10"

# KV namespace for session storage
[[kv_namespaces]]
binding = "SESSIONS"
id = "your-kv-namespace-id"
preview_id = "your-preview-kv-namespace-id"

# R2 bucket for file uploads
[[r2_buckets]]
binding = "UPLOADS"
bucket_name = "grey-haven-uploads"
preview_bucket_name = "grey-haven-uploads-preview"

# Routes
routes = [
  { pattern = "app.greyhaven.studio", zone_name = "greyhaven.studio" }
]
```

### Environment-Specific Configs
- **Development**: `wrangler.toml` with `ENVIRONMENT = "development"`
- **Staging**: `wrangler.staging.toml` with staging routes
- **Production**: `wrangler.production.toml` with production routes

## Doppler Integration

### Required GitHub Secrets
- `DOPPLER_TOKEN`: Doppler service token for CI/CD
- `CLOUDFLARE_API_TOKEN`: Wrangler deployment token

### Required Doppler Secrets (Production)
```bash
# Application
BETTER_AUTH_SECRET=<random-secret>
BETTER_AUTH_URL=https://app.greyhaven.studio
JWT_SECRET_KEY=<random-secret>

# Database (PlanetScale)
DATABASE_URL=postgresql://user:pass@host/db
DATABASE_URL_ADMIN=postgresql://admin:pass@host/db

# Redis (Upstash)
REDIS_URL=redis://user:pass@host:port

# Email (Resend)
RESEND_API_KEY=re_...

# OAuth Providers
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...

# Cloudflare
CLOUDFLARE_ACCOUNT_ID=...
CLOUDFLARE_API_TOKEN=...

# Monitoring (optional)
SENTRY_DSN=https://...@sentry.io/...
AXIOM_TOKEN=xaat-...
```

## GitHub Actions Deployment

### Production Deployment Flow
```yaml
# .github/workflows/deploy-production.yml
- Checkout code
- Setup Node.js 22 with cache
- Install dependencies (npm ci)
- Install Doppler CLI
- Run tests (doppler run --config test)
- Build (doppler run --config production)
- Run database migrations
- Deploy to Cloudflare Workers
- Inject secrets from Doppler
- Run smoke tests
- Rollback on failure
```

### Key Deployment Commands
```bash
# Build with Doppler secrets
doppler run --config production -- npm run build

# Run migrations before deployment
doppler run --config production -- npm run db:migrate

# Deploy to Cloudflare
npx wrangler deploy --config wrangler.production.toml

# Inject secrets into Workers
doppler secrets download --config production --format json > secrets.json
cat secrets.json | jq -r 'to_entries | .[] | "\(.key)=\(.value)"' | while read -r line; do
  key=$(echo "$line" | cut -d= -f1)
  value=$(echo "$line" | cut -d= -f2-)
  echo "$value" | npx wrangler secret put "$key"
done
rm secrets.json
```

## Database Migrations

### Drizzle Migrations (TanStack Start)
```typescript
// scripts/migrate.ts
import { drizzle } from "drizzle-orm/node-postgres";
import { migrate } from "drizzle-orm/node-postgres/migrator";
import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL_ADMIN,
});

const db = drizzle(pool);

async function main() {
  console.log("Running migrations...");
  await migrate(db, { migrationsFolder: "./drizzle/migrations" });
  console.log("Migrations complete!");
  await pool.end();
}

main().catch((err) => {
  console.error("Migration failed:", err);
  process.exit(1);
});
```

**package.json scripts**:
```json
{
  "scripts": {
    "db:migrate": "tsx scripts/migrate.ts",
    "db:migrate:production": "doppler run --config production -- tsx scripts/migrate.ts"
  }
}
```

## Rollback Procedures

### Wrangler Rollback
```bash
# List recent deployments
npx wrangler deployments list --config wrangler.production.toml

# Rollback to previous deployment
npx wrangler rollback --config wrangler.production.toml

# Rollback to specific deployment ID
npx wrangler rollback --deployment-id abc123 --config wrangler.production.toml
```

### Database Rollback
```bash
# Drizzle - rollback last migration
doppler run --config production -- drizzle-kit migrate:rollback

# Alembic - rollback one migration
doppler run --config production -- alembic downgrade -1
```

### Emergency Rollback Playbook
1. **Identify issue**: Check Cloudflare Workers logs, Sentry
2. **Rollback Workers**: `npx wrangler rollback`
3. **Rollback database** (if needed): `drizzle-kit migrate:rollback`
4. **Verify rollback**: Run smoke tests
5. **Notify team**: Update Linear issue
6. **Root cause analysis**: Create postmortem

## Cloudflare Resources Setup

### KV Namespace (Session Storage)
```bash
# Create KV namespace
npx wrangler kv:namespace create "SESSIONS" --config wrangler.production.toml
npx wrangler kv:namespace create "SESSIONS" --preview --config wrangler.production.toml

# List KV namespaces
npx wrangler kv:namespace list
```

### R2 Bucket (File Uploads)
```bash
# Create R2 bucket
npx wrangler r2 bucket create grey-haven-uploads
npx wrangler r2 bucket create grey-haven-uploads-preview

# List R2 buckets
npx wrangler r2 bucket list
```

## Monitoring

### Wrangler Tail (Real-time Logs)
```bash
# Stream production logs
npx wrangler tail --config wrangler.production.toml

# Filter by status code
npx wrangler tail --status error --config wrangler.production.toml
```

### Sentry Integration (Error Tracking)
```typescript
import * as Sentry from "@sentry/browser";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.ENVIRONMENT,
  tracesSampleRate: 1.0,
});
```

## Local Development

### Wrangler Dev (Local Workers)
```bash
# Run Workers locally with Doppler
doppler run --config dev -- npx wrangler dev

# Run with remote mode (uses production KV/R2)
doppler run --config dev -- npx wrangler dev --remote
```

## Supporting Documentation

All supporting files are under 500 lines per Anthropic best practices:

- **[examples/](examples/)** - Complete deployment examples
  - [github-actions-workflow.md](examples/github-actions-workflow.md) - Full CI/CD workflows
  - [wrangler-config.md](examples/wrangler-config.md) - Complete wrangler.toml examples
  - [doppler-secrets.md](examples/doppler-secrets.md) - Secret management patterns
  - [migrations.md](examples/migrations.md) - Database migration examples
  - [INDEX.md](examples/INDEX.md) - Examples navigation

- **[reference/](reference/)** - Deployment references
  - [rollback-procedures.md](reference/rollback-procedures.md) - Rollback strategies
  - [monitoring.md](reference/monitoring.md) - Monitoring and alerting
  - [troubleshooting.md](reference/troubleshooting.md) - Common issues and fixes
  - [INDEX.md](reference/INDEX.md) - Reference navigation

- **[templates/](templates/)** - Copy-paste ready templates
  - [wrangler.toml](templates/wrangler.toml) - Basic wrangler config
  - [deploy-production.yml](templates/deploy-production.yml) - GitHub Actions workflow

- **[checklists/](checklists/)** - Deployment checklists
  - [deployment-checklist.md](checklists/deployment-checklist.md) - Pre-deployment validation

## When to Apply This Skill

Use this skill when:
- Deploying TanStack Start to Cloudflare Workers
- Setting up CI/CD with GitHub Actions
- Configuring Doppler multi-environment secrets
- Running database migrations in production
- Rolling back failed deployments
- Setting up KV namespaces or R2 buckets
- Troubleshooting deployment failures
- Configuring monitoring and alerting

## Template Reference

These patterns are from Grey Haven's production templates:
- **cvi-template**: TanStack Start + Cloudflare Workers
- **cvi-backend-template**: FastAPI + Python Workers

## Critical Reminders

1. **Doppler for ALL secrets**: Never commit secrets to git
2. **Migrations BEFORE deployment**: Run `db:migrate` before `wrangler deploy`
3. **Smoke tests AFTER deployment**: Validate production after deploy
4. **Automated rollback**: GitHub Actions rolls back on failure
5. **Connection pooling**: Match wrangler.toml pool settings with database
6. **Environment-specific configs**: Separate wrangler files per environment
7. **KV/R2 bindings**: Configure in wrangler.toml, create with CLI
8. **Custom domains**: Use Cloudflare Proxy for DDoS protection
9. **Monitoring**: Set up Sentry + Axiom + Wrangler tail
10. **Emergency playbook**: Know how to rollback both Workers and database
