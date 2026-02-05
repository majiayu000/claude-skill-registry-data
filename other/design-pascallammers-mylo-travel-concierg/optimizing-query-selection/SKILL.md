---
name: optimizing-query-selection
description: Optimize queries by selecting only required fields and avoiding N+1 problems. Use when writing queries with relations or large result sets.
allowed-tools: Read, Write, Edit
version: 1.0.0
---

# Query Select Optimization

Optimize Prisma 6 queries through selective field loading and relation batching to prevent N+1 problems and reduce data transfer.

---

<role>
Optimize Prisma 6 queries by selecting required fields only, properly loading relations to prevent N+1 problems while minimizing data transfer and memory usage.
</role>

<when-to-activate>
- Writing user-facing data queries
- Loading models with relations
- Building API endpoints or GraphQL resolvers
- Optimizing slow queries; reducing database load
- Working with large result sets
</when-to-activate>

<workflow>
## Optimization Workflow

1. **Identify:** Determine required fields, relations to load, relation count needs, full vs. specific fields
2. **Choose:** `include` (prototyping, most fields) vs. `select` (production, API responses, performance-critical)
3. **Implement:** Use `select` for precise control, nest relations with `select`, use `_count` instead of loading all records, limit relation results with `take`
4. **Index:** Fields in `where` clauses, `orderBy` fields, composite indexes for filtered relations
5. **Validate:** Enable query logging for single-query verification, test with realistic data volumes, measure payload size and query duration
</workflow>

<core-principles>
## Core Principles

### 1. Select Only Required Fields

**Problem:** Fetching entire models wastes bandwidth and memory

```typescript
const users = await prisma.user.findMany()
```

**Solution:** Use `select` to fetch only needed fields

```typescript
const users = await prisma.user.findMany({
  select: {
    id: true,
    email: true,
    name: true,
  },
})
```

**Performance Impact:**
- Reduces data transfer by 60-90% for models with many fields
- Faster JSON serialization
- Lower memory usage
- Excludes sensitive fields by default

### 2. Include vs Select

**Include:** Adds relations to full model

```typescript
const user = await prisma.user.findUnique({
  where: { id: 1 },
  include: {
    posts: true,
    profile: true,
  },
})
```

**Select:** Precise control over all fields

```typescript
const user = await prisma.user.findUnique({
  where: { id: 1 },
  select: {
    id: true,
    email: true,
    posts: {
      select: {
        id: true,
        title: true,
        published: true,
      },
    },
    profile: {
      select: {
        bio: true,
        avatar: true,
      },
    },
  },
})
```

**When to Use:**
- `include`: Quick prototyping, need most fields
- `select`: Production code, API responses, performance-critical paths

### 3. Preventing N+1 Queries

**N+1 Problem:** Separate query for each relation

```typescript
const posts = await prisma.post.findMany()

for (const post of posts) {
  const author = await prisma.user.findUnique({
    where: { id: post.authorId },
  })
}
```

**Solution:** Use `include` or `select` with relations

```typescript
const posts = await prisma.post.findMany({
  include: {
    author: true,
  },
})
```

**Better:** Select only needed author fields

```typescript
const posts = await prisma.post.findMany({
  select: {
    id: true,
    title: true,
    content: true,
    author: {
      select: {
        id: true,
        name: true,
        email: true,
      },
    },
  },
})
```

### 4. Relation Counting

**Problem:** Loading all relations just to count them

```typescript
const user = await prisma.user.findUnique({
  where: { id: 1 },
  include: {
    posts: true,
  },
})

const postCount = user.posts.length
```

**Solution:** Use `_count` for efficient aggregation

```typescript
const user = await prisma.user.findUnique({
  where: { id: 1 },
  select: {
    id: true,
    name: true,
    _count: {
      select: {
        posts: true,
        comments: true,
      },
    },
  },
})
```

**Result:**
```typescript
{
  id: 1,
  name: "Alice",
  _count: {
    posts: 42,
    comments: 128
  }
}
```
</core-principles>

<quick-reference>
## Quick Reference

### Optimized Query Pattern

```typescript
const optimized = await prisma.model.findMany({
  where: {},
  select: {
    field1: true,
    field2: true,
    relation: {
      select: {
        field: true,
      },
      take: 10,
    },
    _count: {
      select: {
        relation: true,
      },
    },
  },
  orderBy: { field: 'desc' },
  take: 20,
  skip: 0,
})
```

### Key Takeaways

- Default to `select` for all production queries
- Use `include` only for prototyping
- Always use `_count` for counting relations
- Combine selection with filtering and pagination
- Prevent N+1 by loading relations upfront
- Select minimal fields for list views, more for detail views
</quick-reference>

<constraints>
## Constraints and Guidelines

**MUST:**
- Use `select` for all API responses
- Load relations in same query (prevent N+1)
- Use `_count` for relation counts
- Add indexes for filtered/ordered fields
- Test with realistic data volumes

**SHOULD:**
- Limit relation results with `take`
- Create reusable selection objects
- Enable query logging during development
- Measure performance improvements
- Document selection patterns

**NEVER:**
- Use `include` in production without field selection
- Load relations in loops (N+1)
- Fetch full models when only counts needed
- Over-fetch nested relations
- Skip indexes on commonly queried fields
</constraints>

---

## References

For detailed patterns and examples, see:

- [Nested Selection Patterns](./references/nested-selection.md) - Deep relation hierarchies and complex selections
- [API Optimization Patterns](./references/api-optimization.md) - List vs detail views, pagination with select
- [N+1 Prevention Guide](./references/n-plus-one-prevention.md) - Detailed anti-patterns and solutions
- [Type Safety Guide](./references/type-safety.md) - TypeScript types and reusable selection objects
- [Performance Verification](./references/performance-verification.md) - Testing and validation techniques
