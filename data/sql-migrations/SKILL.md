---
name: sql-migrations
description: Manage Azure SQL Server migrations and schema changes for the FinOps platform
---

# SQL Migrations

Use this skill to:
- Create new migrations
- Apply migrations to local/dev/prod environments
- Rollback migrations
- Manage schema changes across databases (control, ingest, finops, allocation, ai, reporting)
- Generate migration status reports

## Database Structure
The platform uses 6 databases:
- **control** — Application configuration and metadata
- **ingest** — Raw cost ingestion staging
- **finops** — Normalized FOCUS cost data
- **allocation** — Cost allocation rules and results
- **ai** — AI/ML analysis results
- **reporting** — Power BI reporting views and metadata

## Common Tasks

### Create New Migration
```bash
npm run migrate:create -- --name "add_new_table"
```

### Apply Migrations
```bash
npm run migrate:up              # All databases
npm run migrate:up:finops       # Specific database
```

### Rollback Migration
```bash
npm run migrate:down            # Last migration
npm run migrate:down -- --steps 3  # Last 3 migrations
```

### Check Migration Status
```bash
npm run migrate:status
```
