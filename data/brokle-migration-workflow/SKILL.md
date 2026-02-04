---
name: brokle-migration-workflow
description: Use this skill when creating, running, or managing database migrations for PostgreSQL or ClickHouse. This includes creating new migrations, running migrations, checking migration status, rollback operations, seeding data, or troubleshooting migration issues.
---

# Brokle Migration Workflow Skill

Expert guidance for database migrations with PostgreSQL, ClickHouse, and seeding operations.

## Migration CLI Overview

**Location**: `cmd/migrate/main.go`

**Key Features**:
- Granular database control (`-db postgres|clickhouse|all`)
- Safety features (confirmation prompts, dry-run mode)
- Health monitoring with dirty state detection
- Supports both PostgreSQL and ClickHouse

## Quick Commands (Makefile)

```bash
# Run all database migrations
make migrate-up

# Rollback one migration
make migrate-down

# Check migration status
make migrate-status

# Create new migration
make create-migration DB=postgres NAME=add_users_table
make create-migration DB=clickhouse NAME=add_metrics_table

# Reset all databases (WARNING: destroys data)
make migrate-reset

# Seed with development data
make seed-dev

# Database shell access
make shell-db          # PostgreSQL
make shell-redis       # Redis CLI
make shell-clickhouse  # ClickHouse client
```

## Advanced CLI Commands

```bash
# Run migrations for specific databases
go run cmd/migrate/main.go -db postgres up
go run cmd/migrate/main.go -db clickhouse up
go run cmd/migrate/main.go up  # All databases

# Check detailed migration status
go run cmd/migrate/main.go -db postgres status
go run cmd/migrate/main.go -db clickhouse status
go run cmd/migrate/main.go status  # Both with health check

# Rollback migrations (requires confirmation)
go run cmd/migrate/main.go -db postgres down
go run cmd/migrate/main.go -db clickhouse down
go run cmd/migrate/main.go down  # Both databases

# Create new migrations
go run cmd/migrate/main.go -db postgres -name create_users_table create
go run cmd/migrate/main.go -db clickhouse -name create_metrics_table create

# Destructive operations (requires 'yes' confirmation)
go run cmd/migrate/main.go -db postgres drop
go run cmd/migrate/main.go -db clickhouse drop

# Granular step control
go run cmd/migrate/main.go -db postgres -steps 2 up      # Run 2 forward
go run cmd/migrate/main.go -db postgres -steps -1 down   # Rollback 1

# Force operations (DANGEROUS - use only when dirty)
go run cmd/migrate/main.go -db postgres -version 0 force
go run cmd/migrate/main.go -db clickhouse -version 5 force

# Information and debugging
go run cmd/migrate/main.go info
go run cmd/migrate/main.go -dry-run up  # Preview without executing
```

## Database Schema Guidelines

### PostgreSQL (Transactional Data)
- Users, authentication, sessions
- Organizations, projects, API keys
- Gateway configurations
- Billing and subscriptions

### ClickHouse (Analytics)

Primary tables in `migrations/clickhouse/`:

- **traces** - Distributed tracing data
- **spans** - LLM call spans with ZSTD compression
- **quality_scores** - Model performance metrics
- **blob_storage_file_log** - File storage metadata

**TTL**: All tables use 365-day retention
**Reference**: Check `migrations/clickhouse/*.up.sql` for exact schema, TTL configuration, and indexes

## Creating PostgreSQL Migration

```sql
-- migrations/000042_add_feature_table.up.sql
-- +migrate Up
CREATE TABLE IF NOT EXISTS feature_table (
    id VARCHAR(26) PRIMARY KEY,
    organization_id VARCHAR(26) NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_feature_table_organization_id ON feature_table(organization_id);
CREATE INDEX idx_feature_table_status ON feature_table(status);

-- +migrate Down
DROP INDEX IF EXISTS idx_feature_table_status;
DROP INDEX IF EXISTS idx_feature_table_organization_id;
DROP TABLE IF EXISTS feature_table;
```

## Creating ClickHouse Migration

```sql
-- migrations/clickhouse/000005_add_metrics_table.up.sql
-- +migrate Up
CREATE TABLE IF NOT EXISTS metrics (
    id String,
    organization_id String,
    project_id String,
    metric_name String,
    metric_value Float64,
    timestamp DateTime64(3),
    metadata String,  -- JSON stored as String
    created_at DateTime64(3) DEFAULT now64(3)
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (organization_id, project_id, timestamp)
TTL toDateTime(timestamp) + INTERVAL 365 DAY
SETTINGS index_granularity = 8192;

-- +migrate Down
DROP TABLE IF EXISTS metrics;
```

## ClickHouse Best Practices

### OTEL-Native Schema Pattern

```sql
CREATE TABLE spans (
    -- Core fields
    id String,
    trace_id String,

    -- OTEL-native: All attributes in one field with namespace prefixes
    attributes String,  -- {"brokle.model": "gpt-4", "brokle.tokens": 150}

    -- OTEL metadata
    metadata String,  -- {"resourceAttributes": {...}, "instrumentationScope": {...}}

    -- Timestamps
    start_time DateTime64(3),
    end_time Nullable(DateTime64(3)),

    -- ZSTD compression for large fields
    input Nullable(String) CODEC(ZSTD),
    output Nullable(String) CODEC(ZSTD),

    -- Application version for A/B testing
    version Nullable(String),

    created_at DateTime64(3) DEFAULT now64(3)
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(start_time)
ORDER BY (trace_id, start_time)
TTL start_time + INTERVAL 90 DAY
SETTINGS index_granularity = 8192;
```

### Performance Patterns

1. **Partitioning**: `PARTITION BY toYYYYMM(timestamp)` for time-series
2. **Ordering**: `ORDER BY` for query optimization
3. **TTL**: `TTL toDateTime(timestamp) + INTERVAL 365 DAY` for automatic retention
4. **Compression**: `CODEC(ZSTD)` for large text fields (78% cost reduction)
5. **Index Granularity**: `index_granularity = 8192` for optimal performance
6. **Engine**: `ReplacingMergeTree(event_ts, is_deleted)` for soft-delete support

### Data Types

- **IDs**: `String` (not UUID)
- **Timestamps**: `DateTime64(3)` for millisecond precision
- **JSON**: `String` (store as JSON string, query with JSON functions)
- **Optional**: `Nullable(Type)`

## Seeding Data

### Seed File Structure (`seeds/`)

```yaml
# seeds/dev.yaml
organizations:
  - id: 01H4XJZQX3EXAMPLE
    name: "Acme Corp"
    slug: "acme-corp"
    plan: "pro"

users:
  - id: 01H4XJZQX3USER001
    email: "admin@acme.com"
    name: "Admin User"
    password_hash: "$2a$10$..."

projects:
  - id: 01H4XJZQX3PROJECT1
    organization_id: 01H4XJZQX3EXAMPLE
    name: "Production API"
    environment: "production"
```

### Running Seeds

```bash
make seed-dev     # Load development data
make seed-demo    # Load demo data
make seed-test    # Load test data

# Or directly
go run cmd/migrate/main.go seed -file seeds/dev.yaml
```

## Migration Safety Checklist

### Before Creating Migration

- [ ] Check existing schema with `make migrate-status`
- [ ] Review similar migrations in `migrations/`
- [ ] Plan rollback strategy (Down migration)
- [ ] Consider data migration needs
- [ ] Test locally first

### Migration Best Practices

- [ ] Always include both Up and Down
- [ ] Use `IF NOT EXISTS` / `IF EXISTS`
- [ ] Add appropriate indexes
- [ ] Consider foreign key constraints
- [ ] Use transactions where appropriate
- [ ] Test rollback functionality

### After Migration

- [ ] Verify schema with `\d table_name` (psql)
- [ ] Check indexes are created
- [ ] Test application functionality
- [ ] Monitor performance
- [ ] Document breaking changes

## Troubleshooting

### Dirty State Recovery

```bash
# Check status
go run cmd/migrate/main.go -db postgres status

# Force clean state (DANGEROUS)
go run cmd/migrate/main.go -db postgres -version 0 force

# Re-run migrations
go run cmd/migrate/main.go -db postgres up
```

### Common Issues

1. **Migration fails mid-way**: Use force command to reset, then fix migration
2. **Schema mismatch**: Drop and recreate (dev only)
3. **Performance issues**: Check indexes and partitioning
4. **TTL not working**: Verify ClickHouse TTL settings

## Database Shell Commands

```bash
# PostgreSQL
make shell-db
\d                # List tables
\d table_name     # Describe table
\di               # List indexes

# ClickHouse
make shell-clickhouse
SHOW TABLES;
DESCRIBE TABLE table_name;
SELECT * FROM table_name LIMIT 10;

# Redis
make shell-redis
KEYS *
GET key_name
```

## References

- `CLAUDE.md` - Migration CLI section
- Migration files in `migrations/` and `migrations/clickhouse/`
- Seed files in `seeds/`
