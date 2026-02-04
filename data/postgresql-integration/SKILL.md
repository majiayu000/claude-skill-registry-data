---
name: postgresql-integration
description: Guide developers through PostgreSQL setup, connection configuration, query patterns, and best practices
license: Complete terms in LICENSE.txt
---

# PostgreSQL Integration
**Version:** 0.17.0

## When to Use
- Setting up PostgreSQL connection
- Implementing database operations
- Configuring connection pooling
- Handling transactions
- Troubleshooting PostgreSQL issues

## Connection Setup

### Connection String
```
postgresql://[user[:password]@][host][:port][/dbname][?param=value]
```

### Security
**NEVER hardcode credentials.** Use:
1. Environment variables: `DATABASE_URL=postgresql://...`
2. Config files (not in version control)
3. Secret management services

### SSL Modes
| Mode | Description |
|------|-------------|
| disable | No SSL |
| require | Require SSL, no verification |
| verify-ca | SSL with CA verification |
| verify-full | SSL with full verification |

## Query Patterns

### Parameterized Queries (Required)
```sql
-- CORRECT
SELECT * FROM users WHERE id = $1

-- WRONG (SQL injection vulnerable)
SELECT * FROM users WHERE id = {user_id}
```

### Common Operations
```sql
-- SELECT
SELECT col1, col2 FROM table WHERE condition ORDER BY col1 LIMIT 100;

-- INSERT with returning
INSERT INTO table (col1) VALUES ($1) RETURNING id;

-- UPDATE
UPDATE table SET col1 = $1, updated_at = NOW() WHERE id = $2 RETURNING *;

-- DELETE
DELETE FROM table WHERE id = $1 RETURNING id;
```

## Transaction Handling

### Isolation Levels
| Level | Dirty Read | Non-repeatable | Phantom |
|-------|:----------:|:--------------:|:-------:|
| READ COMMITTED (default) | No | Yes | Yes |
| REPEATABLE READ | No | No | Yes |
| SERIALIZABLE | No | No | No |

### Best Practices
- Keep transactions short
- Handle errors with rollback
- Never wait for user input mid-transaction

### Savepoints
```sql
BEGIN;
INSERT INTO table1 ...;
SAVEPOINT my_savepoint;
INSERT INTO table2 ...;  -- might fail
ROLLBACK TO SAVEPOINT my_savepoint;
COMMIT;
```

## Connection Pooling

### Why Pool?
Opening connections is expensive (TCP, auth, memory). Pools maintain open connections for reuse.

### Key Parameters
| Parameter | Purpose |
|-----------|---------|
| min_connections | Minimum to maintain |
| max_connections | Maximum allowed |
| connection_timeout | Wait time for connection |
| idle_timeout | Close idle after |

### Sizing
```
max_connections = core_count * 2  (SSD systems)
```

## Error Handling

### Common Errors
| Error | Cause |
|-------|-------|
| ECONNREFUSED | Server not running |
| authentication failed | Wrong credentials |
| relation does not exist | Table not found |
| duplicate key | Unique constraint violation |

### Retry Strategy
1. Exponential backoff
2. Max 3 attempts
3. Log each retry
4. Fail after max

## Performance Tips

### Indexing
```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);
```

### Query Analysis
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
```
Look for: Sequential scans on large tables, high cost estimates

---

**End of PostgreSQL Integration Skill**
