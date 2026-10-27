---
name: prisma-orm
description: "Prisma schema design, relation queries, migration safety, and eliminating hidden query bloat."
---

# Prisma ORM Protocol

1. Use select projections to load only necessary fields.
2. Avoid nested include statements that trigger massive relation joins.
3. Use prisma.$transaction for multi-operation ACID consistency.
