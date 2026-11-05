---
name: gateway-database
description: Route database tasks to the right library skill. Covers migrations, query optimization, ORM, transactions.
type: gateway
tier: core
domains: [database, sql, orm]
trigger: "SQL, PostgreSQL, MySQL, MongoDB, Redis, Prisma, Drizzle, TypeORM, migration, query, schema, transaction"
---

## Purpose

You are the Database Gateway. Route database tasks to specialized library skills.

## Intent Detection → Skill Routing

| Intent Keywords | Load Skill |
|---|---|
| `migration`, `schema change`, `alter table`, `column` | `skills/library/database/safe-migrations/SKILL.md` |
| `index`, `query optimize`, `explain`, `slow query` | `skills/library/database/query-optimization/SKILL.md` |
| `transaction`, `acid`, `rollback`, `savepoint` | `skills/library/database/transactions/SKILL.md` |
| `prisma`, `drizzle`, `typeorm`, `orm`, `sequelize` | `skills/library/database/orm-patterns/SKILL.md` |
| `seed`, `fixture`, `initial data`, `populate` | `skills/library/database/data-seeding/SKILL.md` |
| `backup`, `restore`, `disaster recovery`, `dump` | `skills/library/database/backup-strategies/SKILL.md` |

## Output Format

```
GATEWAY_DATABASE:
Domain: database
Skills to load:
  - [absolute/path/to/SKILL.md]

Instructions: Read the above skill files before proceeding with your task.
```
