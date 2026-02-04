---
name: implementing-query-pagination
description: Implement cursor-based or offset pagination for Prisma queries. Use for datasets 100k+, APIs with page navigation, or infinite scroll/pagination mentions.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
version: 1.0.0
---

# QUERIES-pagination: Efficient Pagination Strategies

Teaches correct Prisma 6 pagination patterns with guidance on cursor vs offset trade-offs and performance implications.

<role>
Implement cursor-based or offset-based Prisma pagination strategies, choosing based on dataset size, access patterns, and performance requirements.
</role>

<when-to-activate>
Activates when: user mentions "pagination," "page," "infinite scroll," "load more"; building APIs with page navigation/list endpoints; optimizing large datasets (100k+) or slow queries; implementing table/feed views.
</when-to-activate>

<overview>
**Cursor-based pagination** (recommended): Stable performance regardless of size; efficient for infinite scroll; handles real-time changes gracefully; requires unique sequential ordering field.

**Offset-based pagination**: Simple; supports arbitrary page jumps; degrades significantly on large datasets (100k+); prone to duplicates/gaps during changes.

\*\*Core principle: Default to cursor. Use offset only for

small (<10k), static datasets requiring arbitrary page access.\*\*
</overview>

<workflow>
## Pagination Strategy Workflow

**Phase 1: Choose Strategy**

- Assess dataset size: <10k (either), 10k–100k (prefer cursor), >100k (require cursor)
- Assess access: sequential (cursor); arbitrary jumps (offset); infinite scroll (cursor); traditional pagination (cursor)
- Assess volatility: frequent inserts/deletes (cursor); static (either)

**Phase 2: Implement**

- **Cursor**: select unique ordering field (id, createdAt+id); implement take+cursor+skip; return next cursor; handle edges
- **Offset**: implement take+skip; calculate total pages if needed; validate bounds; document limitations

**Phase 3: Optimize & Validate**

- Add indexes on ordering field(s); test with realistic dataset size; measure performance; document pagination metadata in response
  </workflow>

<decision-matrix>
## Pagination Strategy Decision Matrix

| Criterion                | Cursor            | Offset          | Winner     |
| ------------------------ | ----------------- | --------------- | ---------- |
| Dataset > 100k           | Stable O(n)       | O(skip+n)       | **Cursor** |
| Infinite scroll          | Natural           | Poor            | **Cursor** |
| Page controls (1,2,3...) | Workaround needed | Natural         | Offset     |
| Jump to page N           | Not supported     | Supported       | Offset     |
| Real-time data           | No duplicates     | Duplicates/gaps | **Cursor** |
| Total count needed       | Extra query       | Same query      | Offset     |
| Complexity               | Medium            | Low             | Offset     |
| Mobile feed              | Natural           | Poor            | **Cursor** |
| Admin table (<10k)       | Overkill          | Simple          | Offset     |
| Search results           | Good              | Acceptable      | **Cursor** |

**Guidelines:** (1) Default cursor for user-facing lists; (2) Use offset only for small admin tables, total-count requirements, or arbitrary page jumping in internal tools; (3) Never use offset for feeds, timelines, >100k datasets, infinite scroll, real-time data.
</decision-matrix>

<cursor-pagination>
## Cursor-Based Pagination

Cursor pagination uses a pointer to a specific record as the starting point for the next page.

### Basic Pattern

```typescript
async function getPosts(cursor?: string, pageSize: number = 20) {
  const posts = await prisma.post.findMany({
    take: pageSize,
    skip: cursor ? 1 : 0,
    cursor: cursor ? { id: cursor } : undefined,
    orderBy: { id: 'asc' },
  });

  return {
    data: posts,
    nextCursor: posts.length === pageSize ? posts[posts.length - 1].id : null,
  };
}
```

### Composite Cursor for Non-Unique Ordering

For non-unique fields (createdAt, score), combine with unique field:

```typescript
async function getPostsByDate(cursor?: { createdAt: Date; id: string }, pageSize: number = 20) {
  const posts = await prisma.post.findMany({
    take: pageSize,
    skip: cursor ? 1 : 0,
    cursor: cursor ? { createdAt_id: cursor } : undefined,
    orderBy: [{ createdAt: 'desc' }, { id: 'asc' }],
  });

  const lastPost = posts[posts.length - 1];
  return {
    data: posts,
    nextCursor:
      posts.length === pageSize ? { createdAt: lastPost.createdAt, id: lastPost.id } : null,
  };
}
```

**Schema requirement:**

```prisma
model Post {
  id        String   @id @default(cuid())
  createdAt DateTime @default(now())
  @@index([createdAt, id])
}
```

### Performance

- **Time complexity**: O(n) where n=pageSize (independent of total dataset size); first and subsequent pages identical
- **Index requirement**: Critical; without index causes full table scan
- **Memory**: Constant (only pageSize records)
- **Data changes**: No duplicates/missing records across pages; new records appear in correct position

</cursor-pagination>

<offset-pagination>
## Offset-Based Pagination

Offset pagination skips a numeric offset of records.

### Basic Pattern

```typescript
async function getPostsPaged(page: number = 1, pageSize: number = 20) {
  const skip = (page - 1) * pageSize;
  const [posts, total] = await Promise.all([
    prisma.post.findMany({ skip, take: pageSize, orderBy: { createdAt: 'desc' } }),
    prisma.post.count(),
  ]);

  return {
    data: posts,
    pagination: { page, pageSize, totalPages: Math.ceil(total / pageSize), totalRecords: total },
  };
}
```

### Performance Degradation

**Complexity**: Page 1 O(pageSize); Page N O(N×pageSize)—linear degradation

**Real-world example** (1M records, pageSize 20):

- Page 1 (skip 0): ~5ms
- Page 1,000 (skip 20k): ~150ms
- Page 10,000 (skip 200k): ~1,500ms
- Page 50,000 (skip 1M): ~7,500ms

Database must scan and discard skipped rows despite indexes.

### When Acceptable

Use only when: (1) dataset <10k OR deep pages rare; (2) arbitrary page access required; (3) total count needed; (4) infrequent data changes. Common cases: admin tables, search results (rarely past page 5), static archives.
</offset-pagination>

<validation>
## Validation

1. **Index verification**: Schema has index on ordering field(s); for cursor use `@@index([field1, field2])`; run `npx prisma format`

2. **Performance testing**:

   ```typescript
   console.time('First page');
   await getPosts(undefined, 20);
   console.timeEnd('First page');
   console.time('Page 100');
   await getPosts(cursor100, 20);
   console.timeEnd('Page 100');
   ```

   Cursor: both ~similar (5–50ms); Offset: verify acceptable for your use case

3. **Edge cases**: first page, last page (<pageSize results), empty results, invalid cursor/page, concurrent modifications

4. **API contract**: response includes pagination metadata; nextCursor null when done; hasMore accurate; page numbers

validated (>0); consistent ordering across pages; unique fields in composite cursors
</validation>

<constraints>
**MUST**: Index cursor field(s); validate pageSize (max 100); handle empty results; return pagination metadata; use consistent ordering; include unique fields in composite cursors

**SHOULD**: Default cursor for user-facing lists; limit offset to <100k datasets; document pagination strategy; test realistic sizes; consider caching total count

**NEVER**: Use offset for >100k datasets, infinite scroll, feeds/timelines, real-time data; omit indexes; allow unlimited pageSize; use non-unique sole cursor; modify ordering between requests
</constraints>

---

## References

- [Bidirectional Pagination](./references/bidirectional-pagination.md) — Forward/backward navigation
- [Complete API Examples](./references/api-implementation-examples.md) — Full endpoint implementations with filtering
- [Performance Benchmarks](./references/performance-comparison.md) — Detailed performance data, optimization guidance
- [Common Mistakes](./references/common-mistakes.md) — Anti-patterns and fixes
- [Data Change Handling](./references/data-change-handling.md) — Managing duplicates and gaps
