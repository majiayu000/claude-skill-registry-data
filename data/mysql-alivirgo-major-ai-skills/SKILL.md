---
name: mysql
description: "Design and administer MySQL or MariaDB schemas, indexes, grants, backups, and migrations; investigate replication basics."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["mysql", "mariadb", "sql", "database", "replication", "migrations"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# MySQL / MariaDB Operations AI Skill Guide

## Overview

MySQL (and MariaDB) store relational data with InnoDB as the default OLTP engine. Agents help with schema design, indexing, backup/restore, user grants, and cautious DDL. Production changes should be online-friendly: avoid long table locks, always take backups before destructive SQL, and never run `DELETE`/`UPDATE` without a `WHERE` unless explicitly requested with confirmation.

```
Clients / app pools
        |
        v
MySQL primary (InnoDB)
        |
        +--> replicas (async/semi-sync)
        +--> backups (mysqldump / XTBackup / snapshots)
```

## When to use

- Writing or reviewing schema migrations and indexes
- Diagnosing slow queries and missing indexes
- Creating users with least-privilege grants
- Dumping/restoring databases in lower environments

## Operational directives

1. Prefer InnoDB; use explicit primary keys on every table.
2. Take a backup or confirm PITR before destructive DDL/DML.
3. Add indexes concurrent to traffic when tools allow; estimate table size first.
4. Use least-privilege users per app (`SELECT/INSERT/UPDATE` only as needed).
5. Never print production passwords; prefer socket auth or secret managers.

## Concrete examples

### Schema + index

```sql
CREATE TABLE orders (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  customer_id   BIGINT UNSIGNED NOT NULL,
  status        VARCHAR(32) NOT NULL,
  created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_orders_customer_created (customer_id, created_at),
  KEY idx_orders_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Grants

```sql
CREATE USER 'api'@'%' IDENTIFIED BY RANDOM PASSWORD;
GRANT SELECT, INSERT, UPDATE ON app.orders TO 'api'@'%';
FLUSH PRIVILEGES;
```

### Dump / restore

```bash
mysqldump --single-transaction --routines --triggers -u root -p app > app.sql
mysql -u root -p app < app.sql
```

### Slow query clues

```sql
SHOW CREATE TABLE orders\G
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 42 ORDER BY created_at DESC LIMIT 20;
SHOW INDEX FROM orders;
```

## Operations matrix

| Task | Safer approach |
| :--- | :--- |
| Add nullable column | Simple ALTER usually OK; still test on copy |
| Add index on large table | Online DDL / pt-online-schema-change |
| Delete old rows | Batched deletes with sleep; avoid one huge txn |
| Change column type | May rebuild table - schedule maintenance |

## Best practices

1. `utf8mb4` + explicit collations; avoid legacy `utf8` (3-byte) surprises.
2. Monitor replication lag before failing over.
3. Keep migrations idempotent and forward-only in app deploy pipelines.
4. Use connection pooling; set sensible `max_connections` and timeouts.

## Limitations

- EXPLAIN plans vary by version/statistics - validate on production-like data.
- Group Replication / InnoDB Cluster topologies need specialized runbooks.
- Agents must not invent restore success without checksum or smoke tests.

## Related skills

- `sqlite` - embedded alternative for local/dev
- `vault` - dynamic DB credentials
- `docker` - local MySQL via Compose
- `opentelemetry` - DB client spans and pool metrics
