---
name: smoke-test-database
description: Smoke-test the database — connectivity/auth, query performance vs SLA, data integrity, backup/restore.
when_to_use: Reach for this to validate the database layer only (can connect, queries meet SLA, integrity intact). For the full release suite use smoke-test-runner; for HTTP endpoints use smoke-test-api; for third-party APIs use smoke-test-external-services; for auth flows use smoke-test-auth; for user journeys use smoke-test-critical-paths.
allowed-tools: Read, Bash, Grep, Glob
---

# Smoke Test Database Skill

**Quick Reference** - Load this first for fast context (~3KB)

## Mission

Execute comprehensive database smoke tests to validate connectivity, query performance, data integrity, and backup/restore operations during release workflows.

## Core Capabilities

- **Connection Testing**: Validate database connectivity and authentication
- **Query Performance**: Test read/write operations against SLA targets
- **Schema Validation**: Verify database schema matches expected structure
- **Data Integrity**: Check critical data constraints and relationships
- **Replication Health**: Validate primary/replica synchronization
- **Backup Validation**: Verify backup operations and restore capability

## When to Use This Skill

Use this skill when:
- Executing pre-release smoke tests (verify database readiness)
- Validating post-deployment health (after migrations)
- Testing canary deployments (database connection pooling)
- Verifying rollback success (schema rollback validation)
- Running scheduled health checks (monitoring integration)

## Quick Start

### 1. Load Skill in Agent

```yaml
skills:
  - name: smoke-test-database
    path: skills/smoke-test-database/SKILL.md
```

### 2. Execute Database Tests

```javascript
const { SmokeTestDatabase } = require('./scripts/test-connectivity.js');

const tester = new SmokeTestDatabase({
  type: 'postgresql',  // or 'mysql', 'mongodb', 'redis'
  host: 'localhost',
  port: 5432,
  database: 'staging_db',
  username: 'app_user',
  password: process.env.DB_PASSWORD
});

const result = await tester.executeTests({
  environment: 'staging',
  tests: ['connectivity', 'query-performance', 'schema-validation']
});

if (result.passed) {
  console.log('✅ Database smoke tests passed');
} else {
  console.error('❌ Database smoke tests failed');
}
```

### 3. Configuration Template

```yaml
environment: staging
database:
  type: postgresql
  host: staging-db.example.com
  port: 5432
  database: app_staging
  username: app_user
  password: ${DB_PASSWORD}
  ssl: true
  poolSize: 10
tests:
  - connectivity
  - query-performance
  - schema-validation
  - data-integrity
```

## Database Smoke Test Categories

### 1. Connectivity Tests
- Primary connection: Connect to primary database
- Replica connection: Connect to read replica
- Connection pooling: Validate pool size and idle connections
- SSL/TLS validation: Verify encrypted connections
- Authentication: Test credentials and permissions

### 2. Query Performance Tests
- Simple query: `SELECT 1` (target: ≤10ms)
- Table query: `SELECT * FROM users LIMIT 1` (target: ≤50ms)
- Join query: Multi-table join (target: ≤200ms)
- Index usage: Verify indexes are used (EXPLAIN analysis)
- Write operations: INSERT/UPDATE/DELETE (target: ≤100ms)

### 3. Schema Validation
- Table existence: Verify all required tables exist
- Column validation: Check columns, types, constraints
- Index validation: Verify indexes exist and are valid
- Foreign key constraints: Check referential integrity
- Migration status: Verify all migrations applied

### 4. Data Integrity Tests
- Record counts: Validate expected data volume
- Constraint validation: Check NOT NULL, UNIQUE, CHECK constraints
- Referential integrity: Validate foreign key relationships
- Critical data: Verify essential configuration records
- Data consistency: Check for orphaned or duplicate records

### 5. Replication Health
- Replication lag: Measure primary-replica lag (target: ≤1s)
- Replica status: Verify replicas are connected and healthy
- Data consistency: Compare row counts across replicas
- Failover readiness: Test replica promotion capability

### 6. Backup Validation
- Backup recency: Verify last backup timestamp (target: ≤24h)
- Backup integrity: Validate backup file checksums
- Point-in-time recovery: Test PITR capability
- Backup restoration: Verify restore to test environment

## Performance SLAs

```javascript
const SLA_TARGETS = {
  connectivity: 1000,     // Connection: ≤1000ms
  simpleQuery: 10,        // SELECT 1: ≤10ms
  tableQuery: 50,         // Table scan: ≤50ms
  joinQuery: 200,         // Multi-table join: ≤200ms
  writeOperation: 100,    // INSERT/UPDATE/DELETE: ≤100ms
  replicationLag: 1000,   // Replication lag: ≤1000ms
  timeout: 30000          // Global timeout: ≤30000ms
};
```

## Pass/Fail Criteria

**Pass**: All smoke tests must pass
- ✅ Database connections established successfully
- ✅ All query performance SLAs met
- ✅ Schema matches expected structure
- ✅ Data integrity constraints satisfied
- ✅ Replication lag within acceptable limits
- ✅ Recent backup exists and is valid

**Fail**: Any smoke test failure blocks deployment
- ❌ Connection failures or authentication errors
- ❌ Query performance exceeds SLA targets
- ❌ Missing tables, columns, or indexes
- ❌ Data integrity violations detected
- ❌ Replication lag exceeds threshold
- ❌ Backup missing, stale, or corrupted

## Execution Points

Database smoke tests are executed at these points in the release workflow:

1. **Pre-Release** (before staging deployment): Validate database readiness and migrations
2. **Post-Staging** (after staging deployment): Verify database health after deployment
3. **Canary 5%** (5% traffic): Test database connection pooling with minimal load
4. **Canary 25%** (25% traffic): Validate database performance under moderate load
5. **Canary 100%** (100% traffic): Test database at full production load
6. **Post-Production** (after production deployment): Verify production database health
7. **Post-Rollback** (after rollback): Validate rollback database state and schema

## Common Patterns

### Pattern 1: Simple Connectivity Test

```javascript
const result = await tester.testConnectivity({
  timeout: 5000,
  retries: 2
});
```

### Pattern 2: Query Performance Test

```javascript
const result = await tester.testQueryPerformance({
  queries: [
    { sql: 'SELECT 1', sla: 10 },
    { sql: 'SELECT * FROM users LIMIT 1', sla: 50 }
  ]
});
```

### Pattern 3: Schema Validation

```javascript
const result = await tester.validateSchema({
  tables: ['users', 'products', 'orders'],
  checkIndexes: true,
  checkConstraints: true
});
```

### Pattern 4: Data Integrity Check

```javascript
const result = await tester.validateDataIntegrity({
  checks: [
    { table: 'users', expected: { min: 100, max: 1000000 } },
    { table: 'products', constraint: 'price > 0' },
    { query: 'SELECT COUNT(*) FROM orders WHERE user_id NOT IN (SELECT id FROM users)', expected: 0 }
  ]
});
```

## Output Format

```javascript
{
  passed: true,
  details: {
    totalTests: 6,
    passed: 6,
    failed: 0,
    executionTime: 1234
  },
  reason: 'Database smoke tests passed: All 6 tests passing',
  metrics: {
    testsPassed: 6,
    testsFailed: 0,
    averageQueryTime: 45,
    maxQueryTime: 198,
    executionTime: 1234
  },
  results: [
    {
      test: 'connectivity',
      category: 'Connection',
      passed: true,
      duration: 234,
      sla: 1000
    },
    {
      test: 'query-performance',
      category: 'Performance',
      passed: true,
      duration: 45,
      sla: 50,
      details: {
        queries: 5,
        averageTime: 45,
        maxTime: 198
      }
    }
  ]
}
```

## Database Type Support

### PostgreSQL
- Connection: `pg` driver with connection pooling
- Schema validation: `information_schema` queries
- Performance: `EXPLAIN ANALYZE` for query plans
- Replication: `pg_stat_replication` monitoring

### MySQL
- Connection: `mysql2` driver with connection pooling
- Schema validation: `INFORMATION_SCHEMA` queries
- Performance: `EXPLAIN` for query plans
- Replication: `SHOW SLAVE STATUS` monitoring

### MongoDB
- Connection: `mongodb` driver with connection pooling
- Schema validation: Collection and index validation
- Performance: `explain()` for query plans
- Replication: Replica set status monitoring

### Redis
- Connection: `redis` client with connection pooling
- Operations: GET, SET, INCR, EXPIRE tests
- Performance: Response time validation
- Replication: Master-replica lag monitoring

## Need More Detail?

For comprehensive documentation including:
- Advanced testing patterns (transactions, deadlock detection, connection pooling)
- Multi-database configurations (sharding, read replicas)
- Integration with monitoring systems (Datadog, Prometheus)
- Custom validation rules and migration testing
- Performance optimization strategies

**Load**: `skills/smoke-test-database/REFERENCE.md` (~15KB)
