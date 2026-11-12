---
name: database-query-optimization
description: When addressing slow application endpoints, high database CPU usage, or standardizing data access patterns.
version: 2.0.0
category: backend
tags: [backend, database, performance, sql, optimization]
skill_type: workflow
author: skiLLM
license: MIT
compatible_agents: [claude-code, cursor, copilot, codex]
estimated_context_tokens: 2000
dangerous: true
requires_review: true
security_level: review-required
dependencies: []
triggers: [slow query, n+1, database performance, sql optimization]
permissions:
  filesystem: { read: true, write: true }
  network: { outbound: true }
  shell: { execute: true }
input_requirements: [slow query, orm code, database schema]
output_contract: [no select *, no n+1 queries, indexes on where/join columns]
failure_conditions: [database unavailable, lack of query profiling data, migration cannot be rolled back]
last_updated: 2026-05-15
---

# Database Query Optimization

## Purpose
Slow databases kill applications. This skill replaces guesswork with systematic performance analysis, using EXPLAIN plans and profiling to eliminate N+1 queries, eliminate unnecessary scans, and add targeted indexes so the database bears the computational load, not the application.

## When to use
- Writing complex SQL queries or ORM access functions
- Resolving performance bottlenecks on read-heavy endpoints
- Designing schema migrations for growing datasets
- Refactoring loops that make repeated database calls

## When NOT to use
- Schema design (different concern)
- Database selection (architectural decision)
- Caching strategies (use Caching Strategies skill)
- Application-level performance (profilers, algorithms)

## Inputs required
- Slow query logs or endpoint metrics
- ORM code accessing the database
- Database schema (tables, columns, indexes)
- EXPLAIN ANALYZE capability (test environment)

## Workflow
1. **Profile the Bottleneck**: Run EXPLAIN ANALYZE on slow queries to identify sequential scans and high-cost operations
2. **Identify N+1**: Locate loops making repetitive database calls for the same entity type
3. **Measure Selectivity**: Analyze WHERE clause filters and add indexes to highly selective columns
4. **Replace Loops**: Replace N+1 with single IN queries or ORM eager-loading (JOINs)
5. **Remove Over-Fetching**: Replace SELECT * with explicit column names
6. **Add Indexes**: Add B-Tree indexes to WHERE, JOIN, and ORDER BY columns in slow queries
7. **Paginate**: Enforce LIMIT and OFFSET (or cursor pagination) on all collection queries
8. **Verify Performance**: Re-run EXPLAIN ANALYZE and benchmark end-to-end latency

## Rules
- MUST explicitly define selected columns (NEVER use SELECT * in production)
- MUST NEVER have database operations inside loops
- MUST perform filtering and aggregation in the database, not application memory
- MUST enforce LIMIT and OFFSET on collection queries
- MUST EXPLAIN before adding indexes (verify they reduce cost)
- MUST rollback indexes if they degrade INSERT/UPDATE performance
- MUST NOT over-index (each index has maintenance cost)

## Anti-patterns
- **The N+1 Problem**: Fetching 50 users, then making 50 individual queries to fetch each user's profile
- **Over-Indexing**: Adding an index to every single column (degrades INSERT/UPDATE performance)
- **Application-Side Filtering**: Fetching 10,000 rows from DB and using `filter()` in JavaScript
- **SELECT * in Production**: Fetching all columns including BLOBs when needing only `id` and `name`
- **Unbounded Queries**: Collection endpoints without LIMIT/OFFSET returning millions of rows
- **Ignoring Selectivity**: Adding indexes to low-cardinality columns (gender, status)

## Failure conditions
- Database unavailable for profiling
- No query metrics/logs available
- EXPLAIN ANALYZE not supported by database
- Migration lacks rollback strategy
- Index changes cause lock timeouts on large tables

## Validation checklist
- [ ] EXPLAIN ANALYZE shows acceptable query cost (< 1000 for simple queries)
- [ ] No sequential scans on large tables (use indexes)
- [ ] SELECT explicitly lists columns (no SELECT *)
- [ ] No loops making repeated database calls
- [ ] N+1 problems replaced with JOIN or ORM eager-load
- [ ] WHERE/JOIN/ORDER BY columns are indexed
- [ ] Collection queries enforce LIMIT and OFFSET
- [ ] No unused indexes (maintenance burden)
- [ ] Low-cardinality columns (gender, status) are NOT indexed
- [ ] Benchmark shows latency improvement (confirm end-to-end)

## Output format
- **SQL format**: ANSI standard, explicitly selecting columns, using parameterized queries
- **ORM calls**: Using eager-load or relationship methods (not loops)
- **Schema changes**: Migration files with forward and rollback steps
- **Indexes**: B-Tree on high-selectivity columns, documented in schema
- **Validation**: EXPLAIN ANALYZE output showing acceptable costs

## Security considerations
- All user input MUST be parameterized (prevent SQL injection)
- Query results MUST be accessible by user (respect permissions)
- Large result sets MUST be paginated (prevent DOS)
- Timing attacks: ensure query timing doesn't leak existence of data

## Agent execution notes
- Agent MAY: Add indexes, create ORM relationships, replace loops with joins, add LIMIT/OFFSET
- Agent MUST NEVER: Use SELECT *, create loops with queries, add untested indexes, bypass pagination
- Agent MUST ASK: Before dropping existing indexes, before major query rewrites, before schema changes
- Agent MUST VALIDATE: EXPLAIN ANALYZE shows improvement, no N+1 remaining, pagination enforced

## Example

**❌ Anti-pattern (N+1, SELECT *, no pagination, missing indexes):**
```javascript
// N+1 problem: 1 query for users + 50 queries for posts
const users = await User.findAll(); // SELECT * (over-fetching)
for (const user of users) {
  const posts = await Post.find({ userId: user.id }); // 50 individual queries
  console.log(user, posts);
}

// Application-side filtering
const allUsers = await User.find({});
const filtered = allUsers.filter(u => u.status === 'active');
```

**✅ Correct pattern (Join, eager-load, explicit columns, paginated):**
```javascript
// Single optimized query with JOIN and explicit columns
const usersWithPosts = await User.findAll({
  attributes: ['id', 'username', 'email'],
  include: [{
    model: Post,
    attributes: ['id', 'title', 'createdAt'],
    required: true
  }],
  limit: 20,
  offset: 0,
  order: [['createdAt', 'DESC']]
});

// Or raw SQL with pagination
const query = `
  SELECT u.id, u.username, p.id, p.title
  FROM users u
  LEFT JOIN posts p ON u.id = p.user_id
  WHERE u.status = $1
  ORDER BY u.created_at DESC
  LIMIT $2 OFFSET $3
`;
const result = await db.query(query, ['active', 20, 0]);

// Indexes created
// CREATE INDEX idx_posts_user_id ON posts(user_id);
// CREATE INDEX idx_users_status ON users(status) WHERE status = 'active';
```
