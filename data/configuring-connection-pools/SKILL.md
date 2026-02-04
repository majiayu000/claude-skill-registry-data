---
name: configuring-connection-pools
description: Configure connection pool sizing for optimal performance. Use when configuring DATABASE_URL or deploying to production.
allowed-tools: Read, Write, Edit
---

# Connection Pooling Performance

Configure Prisma Client connection pools for optimal performance and resource utilization.

## Pool Sizing Formula

**Standard environments:** `connection_limit = (num_cpus × 2) + 1`

Examples: 4 CPU → 9, 8 CPU → 17, 16 CPU → 33 connections

**Configure in DATABASE_URL:**

```
DATABASE_URL="postgresql://user:pass@host:5432/db?connection_limit=9&pool_timeout=20"
```

**Configure in schema.prisma:**

```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider        = "prisma-client-js"
  previewFeatures = ["metrics"]
}
```

## Serverless Environments

**Always use `connection_limit=1` per instance**: Serverless platforms scale horizontally; total connections = instances × limit. Example: 100 Lambda instances × 1 = 100 DB connections (safe) vs. 100 × 10 = 1,000 (exhausted).

**AWS Lambda / Vercel / Netlify:**

```
DATABASE_URL="postgresql://user:pass@host:5432/db?connection_limit=1&pool_timeout=0&connect_timeout=10"
```

**Additional optimizations:**

- `pool_timeout=0`: Fail fast instead of waiting for connections
- `connect_timeout=10`: Timeout initial DB connection
- `pgbouncer=true`: Use PgBouncer transaction mode

## PgBouncer for High Concurrency

**Deploy external pooler when:** >100 application instances, unpredictable serverless scaling, multiple apps sharing one database, connection exhaustion, frequent P1017 errors

**Configuration:**

```ini
[databases]
mydb = host=postgres.internal port=5432 dbname=production

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
reserve_pool_size = 5
reserve_pool_timeout = 3
```

\*\*Prisma with

PgBouncer:\*\*

```
DATABASE_URL="postgresql://user:pass@pgbouncer:6432/db?pgbouncer=true&connection_limit=10"
```

**Avoid in transaction mode:** Prepared statements (disabled with `pgbouncer=true`), persistent SET variables, LISTEN/NOTIFY, advisory locks, temporary tables

## Bottleneck Identification

**P1017 Error (Connection pool timeout)**: "Can't reach database server at `localhost:5432`"

Causes: connection_limit too low, slow queries holding connections, missing cleanup, database at max_connections limit

**Diagnosis:**

```typescript
import { Prisma } from '@prisma/client';

const prisma = new Prisma.PrismaClient({
  log: [{ emit: 'event', level: 'query' }],
});

prisma.$on('query', (e) => {
  console.log('Query duration:', e.duration);
});

const metrics = await prisma.$metrics.json();
console.log('Pool metrics:', metrics);
```

**Check pool status:**

```sql
SELECT count(*) as connections, state, wait_event_type, wait_event
FROM pg_stat_activity WHERE datname = 'your_database'
GROUP BY state, wait_event_type, wait_event;

SHOW max_connections;
SELECT count(*) FROM pg_stat_activity;
```

## Pool Configuration Parameters

| Parameter          | Standard         | Serverless    | PgBouncer | Notes                                                |
| ------------------ | ---------------- | ------------- | --------- | ---------------------------------------------------- |
| `connection_limit` | num_cpus × 2 + 1 | 1             | 10–20     | Total connections = instances × limit                |
| `pool_timeout`     | 20–30 sec        | 0 (fail fast) | —         | Wait time for available connection                   |
| `connect_timeout`  | 5 sec            | 10 sec        | —         | Initial connection timeout; 15–30 for network issues |

**Complete URL example:**

```
postgresql://user:pass@host:5432/db?connection_limit=9&pool_timeout=20&connect_timeout=10&socket_timeout=0&statement_cache_size=100
```

## Production Deployment Checklist

- [ ] Calculate `connection_limit` based on CPU/instance count
- [ ] Set `pool_timeout` appropriately for environment
- [ ] Enable query logging to identify

slow queries

- [ ] Monitor P1017 errors
- [ ] Set up database connection monitoring
- [ ] Configure PgBouncer if serverless/high concurrency
- [ ] Load test with realistic connection counts
- [ ] Document pool settings in runbook

**Environment-specific settings:**

| Environment               | URL Pattern                                                                   |
| ------------------------- | ----------------------------------------------------------------------------- |
| Traditional servers       | `postgresql://user:pass@host:5432/db?connection_limit=17&pool_timeout=20`     |
| Containers with PgBouncer | `postgresql://user:pass@pgbouncer:6432/db?pgbouncer=true&connection_limit=10` |
| Serverless functions      | `postgresql://user:pass@host:5432/db?connection_limit=1&pool_timeout=0`       |

## Common Mistakes

**Default limit in serverless**: Each Lambda instance uses ~10 connections, exhausting DB with 50+ concurrent functions. **Fix:** `connection_limit=1`

**High pool_timeout in serverless**: Functions wait 30s for connections, hitting timeout. **Fix:** `pool_timeout=0`

**No PgBouncer with high concurrency**: 200+ application instances with direct connections = exhaustion. **Fix:** Deploy PgBouncer with transaction pooling.

**Connection_limit exceeds database max_connections**: Setting `connection_limit=200` when DB max is 100. **Fix:** Use PgBouncer or reduce limit below database maximum.
