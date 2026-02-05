---
name: deploying-production-migrations
description: Deploy migrations to production safely using migrate deploy in CI/CD. Use when setting up production deployment pipelines.
allowed-tools: Read, Write, Edit, Bash
---

# MIGRATIONS-production

## Overview

Production database migrations require careful orchestration to prevent data loss and downtime. This covers safe migration deployment using `prisma migrate deploy` in CI/CD pipelines, failure handling, and rollback strategies.

## Production Migration Commands

### Safe Command

**prisma migrate deploy**: Applies pending migrations only; records history in `_prisma_migrations`; neither creates migrations nor resets database.

```bash
npx prisma migrate deploy
```

### Prohibited Commands

**prisma migrate dev**: Creates migrations, can reset database (development-only)  
**prisma migrate reset**: Drops/recreates database, deletes all data  
**prisma db push**: Bypasses migration history, no rollback capability, risks data loss

## CI/CD Integration

```yaml
# GitHub Actions
name: Deploy to Production
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npx prisma generate
      - run: npx prisma migrate deploy
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
      - run: npm run deploy
```

```yaml
# GitLab CI
deploy-production:
  stage: deploy
  image: node:20
  only: [main]
  environment:
    name: production
  before_script:
    - npm ci && npx prisma generate
  script:
    - npx prisma migrate deploy
    - npm run deploy
  variables:
    DATABASE_URL: $DATABASE_URL_PRODUCTION
```

```dockerfile
# Docker
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY prisma ./prisma
RUN npx prisma generate
COPY . .
CMD ["sh", "-c", "npx prisma migrate deploy && npm start"]
```

## Handling Failed Migrations

\*\*Check status

\*\*: `npx prisma migrate status` (identifies pending, applied, failed migrations, and schema drift)

**Resolution options**:

- **Temporary failure**: `npx prisma migrate resolve --applied <name> && npx prisma migrate deploy`
- **Partially reverted**: `npx prisma migrate resolve --rolled-back <name>`
- **Buggy migration**: Create new migration to fix: `npx prisma migrate dev --name fix_previous_migration`, then deploy

**Manual rollback**: Create down migration (SQL to revert changes), apply via `npx prisma migrate dev --name rollback_* --create-only`

## Production Deployment Checklist

**Pre-Deployment**: All migrations tested in staging; backup created; rollback plan documented; downtime window scheduled; team notified

**Deployment**: Maintenance mode enabled (if needed); run `npx prisma migrate deploy`; verify status; run smoke tests; monitor logs

**Post-Deployment**: Verify all migrations applied; check functionality; monitor database performance; disable maintenance mode; document issues

## Database Connection Best Practices

**Connection pooling**: `DATABASE_URL="postgresql://user:pass@host:5432/db?connection_limit=10&pool_timeout=20"`

**Security**: Never commit DATABASE_URL; use environment variables, CI/CD secrets, or secret management tools (Vault, AWS Secrets Manager)

**Read replicas**: Separate migration connection from app connections; migrations always target primary database:

```env
DATABASE_URL="postgresql://primary:5432/db"
DATABASE_URL_REPLICA="postgresql://replica:5432/db"
```

## Zero-Downtime Migrations

**Expand-Contract Pattern**:

1. **Expand** (add new column, keep old): `ALTER TABLE "User" ADD COLUMN "email_new" TEXT;` Deploy app writing to both.
2. **Migrate data**: `UPDATE "User" SET "email_new" = "email"

WHERE "email_new" IS NULL;`3. **Contract** (remove old):`ALTER TABLE "User" DROP COLUMN "email"; ALTER TABLE "User" RENAME COLUMN "email_new" TO "email";`

**Backwards-compatible**: Make columns optional first, enforce constraints in later migration.

## Monitoring and Alerts

**Duration tracking**: `time npx prisma migrate deploy`; set alerts for migrations exceeding expected duration

**Failure alerts**:

```yaml
- run: npx prisma migrate deploy
- if: failure()
  run: curl -X POST $SLACK_WEBHOOK -d '{"text":"Production migration failed!"}'
```

**Schema drift detection**: `npx prisma migrate status` fails if schema differs from migrations

## Common Production Issues

| Issue                   | Cause                                                  | Solution                                                                                                     |
| ----------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| Migration hangs         | Long-running query, table locks                        | Identify blocking queries; run during low-traffic window; use `SET statement_timeout = '30s';` in PostgreSQL |
| Migration fails midway  | Constraint violation, data type mismatch               | Check migration status; mark as applied if data correct; create fix migration if needed                      |
| Out-of-order migrations | Multiple developers creating migrations simultaneously | Merge conflicts in migration files; regenerate if needed; enforce linear history                             |

## Configuration

**Shadow Database** (Prisma 6): Not needed for `migrate deploy`, only `migrate dev`

```env
DATABASE_URL="postgresql://..."
SHADOW_DATABASE_URL="postgresql://...shadow"
```

**Multi-Environment Strategy**:

- Development: `npx prisma migrate dev`
- Staging: `npx prisma migrate deploy` (test production process)
- Production: `npx prisma migrate deploy` (apply only, never create)

## References

[Prisma Migrate Deploy Documentation](https://www.prisma.io/docs/orm/prisma-migrate/workflows/deploy) | [Production Best Practices](https://www.prisma.io/docs/orm/prisma-migrate/workflows/production) | [Troubleshooting Migrations](https://www.prisma.io/docs/orm/prisma-migrate/workflows/troubleshooting)
