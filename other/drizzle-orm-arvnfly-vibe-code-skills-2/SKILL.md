---
name: drizzle-orm
description: "Drizzle ORM schema modeling, type-safe SQL queries, zero-overhead migrations, and relation queries."
---

# Drizzle ORM Protocol

1. Define schemas with drizzle-orm/pg-core or mysql-core with explicit type safety.
2. Use db.query for relation-heavy lookups and db.select for optimized raw SQL projections.
3. Run migrations via drizzle-kit migrate in CI.
