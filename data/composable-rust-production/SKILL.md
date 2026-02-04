---
name: composable-rust-production
description: Expert knowledge for deploying and operating Composable Rust applications in production. Use when setting up database migrations, configuring connection pools, implementing backup/restore procedures, tuning performance, setting up monitoring and observability, or handling operational concerns like disaster recovery and production database management.
---

# Composable Rust Production Operations Expert

Expert knowledge for production deployment and operations of Composable Rust applications - database migrations, connection pooling, backup/restore, performance tuning, monitoring, and operational excellence.

## When to Use This Skill

Automatically apply when:
- Setting up database migrations or schema changes
- Configuring connection pools for production
- Implementing backup and restore procedures
- Performance tuning PostgreSQL or application code
- Setting up monitoring, metrics, or observability
- Implementing disaster recovery procedures
- Production database operations
- Troubleshooting production issues

## Database Migrations (sqlx)

### Running Migrations

**Option 1: Helper Function (Deployment Scripts)**

```rust
use composable_rust_postgres::run_migrations;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let database_url = std::env::var("DATABASE_URL")?;

    // Run migrations during startup
    run_migrations(&database_url).await?;

    println!("Database ready!");
    Ok(())
}
```

**Option 2: EventStore Method (When Store Exists)**

```rust
use composable_rust_postgres::PostgresEventStore;

let store = PostgresEventStore::new(&database_url).await?;
store.run_migrations().await?;
```

**Option 3: sqlx CLI (Development)**

```bash
# Install CLI
cargo install sqlx-cli --no-default-features --features postgres

# Run migrations
sqlx migrate run --database-url postgres://localhost/mydb

# Revert last migration
sqlx migrate revert --database-url postgres://localhost/mydb
```

### Creating Migrations

**Step 1: Create SQL file with sequential number**

```bash
# migrations/003_add_user_context.sql
```

**Step 2: Write idempotent SQL**

```sql
-- Add user_context column to events table
ALTER TABLE events
ADD COLUMN IF NOT EXISTS user_context JSONB;

-- Add index
CREATE INDEX IF NOT EXISTS idx_events_user_context
ON events USING GIN (user_context);
```

**Critical Rules:**
- ✅ **Always use `IF NOT EXISTS`** for idempotency
- ✅ **One logical change per migration**
- ✅ **Test on production data copy first**
- ❌ **Never edit existing migrations** (create new one)
- ❌ **Never delete migrations** (breaks version tracking)

### Migration Best Practices

```sql
-- ✅ GOOD: Idempotent
CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY,
    customer_id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ✅ GOOD: Safe column addition
ALTER TABLE orders
ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'pending';

-- ❌ BAD: Not idempotent
CREATE TABLE orders (...);  -- Fails on second run

-- ❌ BAD: Destructive
DROP TABLE old_orders;  -- Can't be undone
```

## Connection Pooling

### Production Pool Configuration

```rust
use sqlx::postgres::PgPoolOptions;
use std::time::Duration;

let pool = PgPoolOptions::new()
    // Connection limits
    .max_connections(20)                  // Max concurrent
    .min_connections(5)                   // Keep warm

    // Timeouts
    .acquire_timeout(Duration::from_secs(10))   // Wait for conn
    .idle_timeout(Duration::from_secs(600))     // 10min idle
    .max_lifetime(Duration::from_secs(1800))    // 30min recycle

    // Health
    .test_before_acquire(true)            // Validate conn

    .connect(&database_url)
    .await?;

let store = PostgresEventStore::from_pool(pool);
```

### Sizing Guidelines

**Formula**: `max_connections = (req/sec × conn_time) / req_time + buffer`

**Example**:
- Load: 1000 req/sec
- Request time: 50ms
- Connection hold: 10ms
- Calculation: `(1000 × 0.010) / 0.050 + 5 = 25 connections`

**Recommendations by Load:**

| Environment | Max Connections | Use Case |
|-------------|-----------------|----------|
| Development | 5 | Minimal overhead |
| Staging | 10-20 | Simulate production |
| Low traffic | 20-50 | < 100 req/sec |
| Medium traffic | 50-100 | 100-1000 req/sec |
| High traffic | 100-200 | > 1000 req/sec |

**PostgreSQL Limits:**

```ini
# postgresql.conf
max_connections = 200  # Reserve some for admin/monitoring
```

### Pool Monitoring

```rust
// Check pool health
let size = pool.size();           // Current connections
let idle = pool.num_idle();       // Available connections

tracing::info!(
    pool_size = size,
    pool_idle = idle,
    "Connection pool status"
);

// Metrics to track:
// - pool.size() < max_connections (not exhausted)
// - pool.num_idle() > 0 (connections available)
// - Acquire time < 100ms (fast acquisition)
// - Connection errors ≈ 0 (healthy pool)
```

## Backup and Restore

### Full Database Backup

```bash
# Backup with compression
pg_dump -h localhost -U postgres -d mydb \
    --format=custom \
    --compress=9 \
    --file=backup_$(date +%Y%m%d_%H%M%S).dump

# Restore
pg_restore -h localhost -U postgres \
    --clean --create \
    --dbname=postgres \
    backup_20250110_143022.dump
```

### Events-Only Backup (Faster)

```bash
# Backup events table (source of truth)
pg_dump -h localhost -U postgres -d mydb \
    --table=events \
    --format=custom \
    --file=events_backup_$(date +%Y%m%d_%H%M%S).dump

# Restore
pg_restore -h localhost -U postgres \
    --dbname=mydb \
    --table=events \
    events_backup_20250110_143022.dump
```

### Automated Backup Script

```bash
#!/bin/bash
# daily-backup.sh

set -e

BACKUP_DIR="/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="mydb"
RETENTION_DAYS=30

# Create backup
pg_dump -h localhost -U postgres -d $DB_NAME \
    --format=custom --compress=9 \
    --file=$BACKUP_DIR/backup_$DATE.dump

# Upload to S3 (optional)
aws s3 cp $BACKUP_DIR/backup_$DATE.dump \
    s3://my-backups/postgres/backup_$DATE.dump

# Delete old backups
find $BACKUP_DIR -name "backup_*.dump" \
    -mtime +$RETENTION_DAYS -delete

echo "Backup completed: backup_$DATE.dump"
```

**Cron Schedule:**

```cron
# Daily at 2 AM
0 2 * * * /usr/local/bin/daily-backup.sh >> /var/log/backup.log 2>&1
```

### Testing Backups

**Critical**: Test restoration monthly!

```bash
# 1. Create test database
createdb -h localhost -U postgres mydb_test

# 2. Restore backup
pg_restore -h localhost -U postgres \
    --dbname=mydb_test \
    backup_latest.dump

# 3. Verify data
psql -h localhost -U postgres -d mydb_test \
    -c "SELECT COUNT(*) FROM events;"

# 4. Cleanup
dropdb -h localhost -U postgres mydb_test
```

## Performance Tuning

### PostgreSQL Configuration

**For Event Sourcing Workloads (postgresql.conf):**

```ini
# Memory (assume 16GB RAM server)
shared_buffers = 4GB              # 25% of RAM
effective_cache_size = 12GB       # 75% of RAM
work_mem = 64MB                   # Per-operation memory

# Write Performance
wal_buffers = 16MB
checkpoint_completion_target = 0.9
max_wal_size = 4GB
min_wal_size = 1GB

# Query Performance (SSDs)
random_page_cost = 1.1            # Default 4.0 for HDDs
effective_io_concurrency = 200

# Logging
log_min_duration_statement = 1000 # Log queries > 1s
log_checkpoints = on
```

### Index Optimization

**Default Event Store Indexes:**

```sql
-- Primary key (automatic)
PRIMARY KEY (stream_id, version)

-- Query by time
CREATE INDEX idx_events_created ON events(created_at);

-- Query by type
CREATE INDEX idx_events_type ON events(event_type);
```

**Custom Indexes for Your Workload:**

```sql
-- Query by metadata fields
CREATE INDEX idx_events_user_id
ON events ((metadata->>'user_id'));

-- Query by correlation ID
CREATE INDEX idx_events_correlation
ON events ((metadata->>'correlation_id'));

-- Partial index for recent events
CREATE INDEX idx_events_recent
ON events(created_at)
WHERE created_at > NOW() - INTERVAL '30 days';
```

### Table Maintenance

```bash
# Regular maintenance
psql -c "VACUUM ANALYZE events;"

# Full vacuum (locks table - maintenance window)
psql -c "VACUUM FULL events;"

# Reindex if bloated
psql -c "REINDEX TABLE events;"
```

**Automate with autovacuum (postgresql.conf):**

```ini
autovacuum = on
autovacuum_vacuum_scale_factor = 0.1
autovacuum_analyze_scale_factor = 0.05
```

## Monitoring and Observability

### Health Check Endpoint

```rust
use axum::{Json, extract::State};
use serde::Serialize;

#[derive(Serialize)]
struct HealthStatus {
    status: String,
    database: String,
    event_count: i64,
}

async fn health_check(
    State(store): State<Arc<PostgresEventStore>>,
) -> Json<HealthStatus> {
    // Test database connectivity
    let db_status = match sqlx::query("SELECT 1")
        .execute(store.pool())
        .await
    {
        Ok(_) => "healthy",
        Err(_) => "unhealthy",
    };

    // Get event count
    let event_count: (i64,) = sqlx::query_as("SELECT COUNT(*) FROM events")
        .fetch_one(store.pool())
        .await
        .unwrap_or((0,));

    Json(HealthStatus {
        status: if db_status == "healthy" { "ok" } else { "error" }.into(),
        database: db_status.into(),
        event_count: event_count.0,
    })
}
```

### Key Metrics to Track

**Database Metrics:**

```sql
-- Active connections
SELECT count(*) FROM pg_stat_activity WHERE state = 'active';

-- Database size
SELECT pg_size_pretty(pg_database_size('mydb'));

-- Table size
SELECT pg_size_pretty(pg_total_relation_size('events'));

-- Slow queries (requires pg_stat_statements)
SELECT query, calls, total_exec_time, mean_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

**Application Metrics:**

```rust
use metrics::{counter, histogram, gauge};

// Track reducer execution time
let start = Instant::now();
let effects = reducer.reduce(&mut state, action, &env);
histogram!("reducer_duration_ms").record(start.elapsed().as_millis() as f64);

// Track effect execution
counter!("effects_executed_total").increment(effects.len() as u64);

// Track store state
gauge!("store_state_size_bytes").set(state_size as f64);
```

### Alert Thresholds

Set up alerts for:

- **Connection pool exhausted**: `pool.num_idle() == 0` for > 1 minute
- **High query latency**: p99 > 1 second
- **Disk space low**: < 20% free
- **Replication lag**: > 60 seconds (if using replication)
- **Failed backups**: Last successful backup > 24 hours ago
- **Error rate**: > 1% of requests failing

## Disaster Recovery

### Recovery Time Objective (RTO)

**Target**: < 4 hours to full recovery

**Steps**:
1. Provision new PostgreSQL instance (30 min)
2. Restore from backup (1-2 hours, depends on size)
3. Verify data integrity (30 min)
4. Reconfigure applications (30 min)

### Recovery Point Objective (RPO)

**Target**: < 1 hour of data loss

**Strategies**:
- **Tier 1** (No data loss): Continuous WAL archiving + PITR
- **Tier 2** (< 1 hour): Hourly backups
- **Tier 3** (< 24 hours): Daily backups

### Disaster Recovery Runbook

**Step 1: Assess the situation**

```bash
# Check PostgreSQL logs
tail -100 /var/log/postgresql/postgresql.log

# Check disk space
df -h

# Check system resources
top
iostat
```

**Step 2: Attempt quick recovery**

```bash
# Restart PostgreSQL
systemctl restart postgresql

# Verify
systemctl status postgresql
psql -c "SELECT 1"
```

**Step 3: If restart fails, restore from backup**

```bash
# Stop application
systemctl stop myapp

# Restore latest backup
pg_restore -h localhost -U postgres \
    --clean --create --dbname=postgres \
    /backups/postgres/backup_latest.dump

# Run migrations
./myapp migrate

# Start application
systemctl start myapp
```

**Step 4: Verify recovery**

```bash
# Check event count
psql -c "SELECT COUNT(*) FROM events;"

# Check application health
curl http://localhost:8080/health
```

## Production Checklist

Before deploying to production, verify:

- [ ] Migrations automated in deployment pipeline
- [ ] Connection pool sized for expected load
- [ ] Daily automated backups configured
- [ ] Backup restoration tested (within last 30 days)
- [ ] Monitoring and alerting set up
- [ ] Performance tuning applied (postgresql.conf)
- [ ] Disaster recovery runbook documented and tested
- [ ] Database access secured (SSL, firewall, strong passwords)
- [ ] High availability configured (if needed: replication, failover)
- [ ] Resource limits set (connection limits, rate limiting)

## Troubleshooting Guide

### Connection Pool Exhausted

**Symptom**: "Timeout acquiring connection from pool"

**Diagnosis**:
```rust
let size = pool.size();
let idle = pool.num_idle();
tracing::error!(size, idle, "Pool exhausted");
```

**Solutions**:
1. Increase `max_connections` in pool config
2. Reduce connection hold time (optimize queries)
3. Add connection timeout handling
4. Scale horizontally (more app instances)

### Slow Queries

**Symptom**: High latency on database operations

**Diagnosis**:
```sql
-- Enable query logging
SET log_min_duration_statement = 100;

-- Check slow queries
SELECT query, mean_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC;
```

**Solutions**:
1. Add missing indexes
2. Optimize query patterns
3. Use EXPLAIN ANALYZE
4. Consider read replicas for queries

### High Memory Usage

**Symptom**: PostgreSQL using excessive memory

**Diagnosis**:
```sql
SELECT pg_size_pretty(pg_database_size('mydb'));
SELECT pg_size_pretty(pg_total_relation_size('events'));
```

**Solutions**:
1. Run VACUUM ANALYZE
2. Reduce `shared_buffers` if too high
3. Optimize `work_mem` for query complexity
4. Archive old events to separate table

## See Also

- **Architecture**: See `composable-rust-architecture` skill for core patterns
- **Event Sourcing**: See `composable-rust-event-sourcing` skill for event design
- **Testing**: See `composable-rust-testing` skill for integration tests
- **Documentation**: `docs/production-database.md` (800+ lines)
- **Observability**: `docs/observability.md` for tracing and metrics
