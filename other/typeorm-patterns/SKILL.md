---
name: typeorm-patterns
description: "TypeORM entity modeling, query builder patterns, transaction managers, and lazy loading avoidance."
---

# TypeORM Architecture Protocol

1. Avoid lazy relations; use explicit relations: ['item'] in find options.
2. Use SelectQueryBuilder for complex joins and aggregations.
3. Always execute mutations through queryRunner to guarantee transaction rollback on errors.
