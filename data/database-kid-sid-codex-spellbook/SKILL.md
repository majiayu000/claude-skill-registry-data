---
name: database
description: Database guidance for schema naming, safe migrations, indexing, N+1 detection, transaction scope, and soft-delete versus hard-delete tradeoffs. Use when designing schemas, writing migrations, or tuning persistence behavior.
---

# Database

Model schemas for clarity, migrate in safe increments, and optimize queries around real access patterns rather than guesswork.

## When to Activate

- Design a new schema or table
- Add or review a migration
- Diagnose slow queries or query explosions
- Decide whether an index is warranted
- Refactor a transaction boundary
- Choose data deletion semantics
- Review ORM usage for N+1 issues

## Naming and Migrations

| Object | Convention |
| --- | --- |
| Tables | plural `snake_case` |
| Columns | singular `snake_case` |
| Primary keys | `id` |
| Foreign keys | `<table>_id` |
| Join tables | alphabetical plural pair, e.g. `roles_users` |

| Change | Safe Pattern | Avoid |
| --- | --- | --- |
| Drop column | add replacement, backfill, dual-read, dual-write, drop later | destructive one-step drop |
| Rename column | add new column and migrate gradually | instant rename in hot path |
| Add constraint | backfill invalid rows first | applying constraint to dirty data |

BAD

```sql
ALTER TABLE users DROP COLUMN full_name;
```

GOOD

```sql
ALTER TABLE users ADD COLUMN display_name text;
UPDATE users SET display_name = full_name WHERE display_name IS NULL;
```

## Indexing and Query Shape

| Query Pattern | Index |
| --- | --- |
| Equality on foreign key | single-column btree |
| Filter + sort | composite index ordered by filter then sort |
| Case-insensitive search | functional index matching query function |

| Signal | Fix |
| --- | --- |
| One query per row in a list view | eager load or batch fetch |
| Repeated lookup in serializer loop | prefetch related data |
| ORM debug logs showing repeated shapes | consolidate access path |

## Transactions and Deletion

| Preferred | Avoid |
| --- | --- |
| Short transaction around consistent write set | Holding transaction open across network calls |
| Retry on known transient conflicts | Blind retries on all DB errors |

| Use Soft Delete When | Use Hard Delete When |
| --- | --- |
| Audit or recovery matters | Regulation or retention requires full erasure |
| References must remain historically intact | Data is ephemeral and unreferenced |

## Checklist

- [ ] Tables and columns use consistent `snake_case` naming
- [ ] Migrations are additive before destructive cleanup
- [ ] New indexes match real query patterns
- [ ] N+1 risks were checked on list and detail endpoints
- [ ] Transactions exclude network calls and long-running work
- [ ] Delete strategy is chosen intentionally per dataset
- [ ] Rollout works across mixed old and new application versions
