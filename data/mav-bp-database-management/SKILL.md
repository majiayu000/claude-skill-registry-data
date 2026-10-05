---
name: mav-bp-database-management
description: Database and data management conventions for all projects using databases. Covers schema migrations, backup strategy, data lifecycle, index management, and connection pooling. Applied when designing, implementing, or reviewing database interactions.
user-invocable: false
disable-model-invocation: true
---

# Database & Data Management Standards

Maverick's hard rules for schema migrations, environment isolation, and data safety.

## Maverick's Rules

- **Forward-only in production** — never roll back a production migration manually; undo with a new forward migration.
- **Every migration is reversible** — each migration includes an up and a down operation, even if the down is only ever used in development.
- **Never edit an already-applied migration** — once applied to any shared environment, write a new migration instead.
- **No ad-hoc DDL against shared environments** — every schema change is a versioned migration file in version control.
- **Strict environment isolation** — dev, staging, and production databases are completely separate. Never connect to production from a local machine (bastion/audited admin tools only). Never copy production data to development — seed data or anonymised snapshots only.
- **Seed data is synthetic and idempotent** — never production data in seed files; re-running seeds produces the same result.
- **No speculative indexes** — index only columns appearing in actual query `WHERE`/`JOIN`/`ORDER BY`/`GROUP BY` clauses; remove unused indexes.
- **Connection pooling is mandatory** — never open a connection per request; configure connection and idle timeouts.
- **Stage destructive schema changes** — `DROP`/`RENAME`/type changes require the expand-backfill-contract pattern: deploy code that stops using the column first, then migrate.

## Project Implementation Lookup

Check for `docs/maverick/skills/database-management/SKILL.md`. If present, read it — it wins on specifics (library, config, conventions). If missing, proceed with these standards and note the gap in your summary.

## Detecting Database Issues in Code Review

When reviewing code, flag these patterns:

| Pattern                                            | Issue                              | Fix                                                    |
| -------------------------------------------------- | ---------------------------------- | ------------------------------------------------------ |
| Raw SQL without parameterised queries              | SQL injection risk                 | Use parameterised queries or ORM                       |
| Manual schema change (ad-hoc DDL)                  | Unreproducible, untracked change   | Create a migration file                                |
| Editing an already-applied migration               | Breaks migration history           | Write a new migration                                  |
| No index on columns used in WHERE/JOIN             | Performance degradation at scale   | Add appropriate index                                  |
| Opening connection per request (no pooling)        | Connection exhaustion              | Use connection pool                                    |
| Hardcoded connection string                        | Security risk, environment coupling| Use environment variables or secrets manager            |
| Missing down migration                             | Cannot revert in development       | Add reversible down operation                          |
| Production data in seed files                      | Data leak, privacy violation       | Use synthetic data only                                |
| `DROP TABLE` or `DROP COLUMN` without staged rollout| Breaks running application        | Stage the change: remove code references first         |
| No transaction wrapping for multi-step migration   | Partial application on failure     | Wrap in transaction where the database supports it     |

<!-- maverick-plugin-version: 4.0.2-dev -->
