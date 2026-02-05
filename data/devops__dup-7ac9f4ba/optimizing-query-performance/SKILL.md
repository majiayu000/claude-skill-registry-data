---
name: optimizing-query-performance
description: Optimize queries with indexes, batching, and efficient Prisma operations for production performance.
allowed-tools: Read, Write, Edit, Bash
version: 1.0.0
---

<overview>
Query optimization requires strategic indexing, efficient batching, and monitoring to prevent common production anti-patterns.

Key capabilities: Strategic index placement (@@index, @@unique) · Efficient batch operations (createMany, transactions) · Query analysis & N+1 prevention · Field selection optimization & cursor pagination
</overview>

<workflow>
**Phase 1 — Identify:** Enable query logging; analyze patterns/execution times; identify missing indexes, N+1 problems, or inefficient batching

**Phase 2 — Optimize:** Add indexes for filtered/sorted fields; replace loops with batch operations; select only needed fields; use cursor pagination for large datasets

**Phase 3 — Validate:** Measure execution time before/after; verify index usage with EXPLAIN ANALYZE; monitor connection pool under load
</workflow>

## Quick Reference

**Index Strategy:**

| Scenario              | Index Type                          | Example                        |
| --------------------- | ----------------------------------- | ------------------------------ |
| Single field filter   | `@@index([field])`                  | `@@index([status])`            |
| Multiple field filter | `@@index([field1, field2])`         | `@@index([userId, status])`    |
| Sort + filter         | `@@index([filterField, sortField])` | `@@index([status, createdAt])` |

**Batch Operations:**

| Operation | Slow (Loop)            | Fast (Batch)   |
| --------- | ---------------------- | -------------- |
| Insert    | `for...await create()` | `createMany()` |
| Update    | `for...await update()` | `updateMany()` |
| Delete    | `for...await delete()` | `deleteMany()` |

**Performance Gains:** Indexes (10-100x) · Batch ops (50-100x for 1000+ records) · Cursor pagination (constant vs O(n))

<constraints>
**MUST:** Add indexes for WHERE/ORDER BY/FK fields with frequent queries; use createMany for 100+ records; cursor pagination for deep pagination; select only needed fields; monitor query duration in production

**SHOULD:** Test indexes with production data; chunk 100k+ batches into smaller sizes; use `@@index([field1, field2])` for multi-field filters; remove unused indexes

**NEVER:** Add indexes without performance measurement; offset pagination beyond page 100 on large tables; fetch all

fields when only needing few; loop with individual creates/updates; ignore slow query warnings
</constraints>

<validation>
**Measure Performance:**
```typescript
const start = Date.now()
const result = await prisma.user.findMany({ ... })
console.log(`Query took ${Date.now() - start}ms`)
```
Expected: 50-90% improvement for indexed queries, 50-100x for batch operations

**Verify Index Usage:** Run EXPLAIN ANALYZE; confirm "Index Scan" vs "Seq Scan"

**Monitor Production:** Track P95/P99 latency; expect reduced slow query frequency

**Check Write Performance:** Writes may increase 10-30% per index if rarely-used; consider removal
</validation>

## References

- **Index Strategy**: `references/index-strategy.md` — indexing patterns and trade-offs
- **Batch Operations**: `references/batch-operations.md` — bulk operations and chunking
- **Query Monitoring**: `references/query-monitoring.md` — logging setup and slow query analysis
- **Field Selection**: `references/field-selection.md` — select vs include patterns and N+1 prevention
- **Optimization Examples**: `references/optimization-examples.md` — real-world improvements
- **Next.js Integration**: Next.js plugin for App Router-specific patterns
- **Serverless**: CLIENT-serverless-config skill for connection pooling
