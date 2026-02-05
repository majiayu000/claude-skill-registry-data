---
name: performance-patterns
description: Use when user asks about N+1 queries, performance optimization, query optimization, reduce API calls, improve render performance, fix slow code, optimize database, or reduce bundle size. Provides guidance on identifying and fixing performance anti-patterns across database, backend, frontend, and API layers.
allowed-tools: Read, Grep, Glob
---

# Performance Anti-Patterns Reference

## N+1 Query Problem

The N+1 problem occurs when code executes N additional queries to fetch related data for N items from an initial query.

**Identification:**
- Queries inside loops
- Lazy loading of associations during iteration
- GraphQL resolvers fetching per-item

**Fix Strategies:**
1. **Eager Loading**: Load related data in initial query
2. **Batching**: Collect IDs, fetch all at once
3. **DataLoader**: For GraphQL, batch and cache per-request
4. **Denormalization**: Store computed/related data together

**Severity**: HIGH - Scales linearly with data size, causes exponential slowdown

## Over-Fetching

Retrieving more data than needed from API or database.

**Identification:**
- SELECT * queries
- API endpoints returning full objects
- No field selection support
- Loading nested relations by default

**Fix Strategies:**
1. **Field Selection**: Only query needed columns
2. **Sparse Fieldsets**: Support `?fields=id,name` parameter
3. **GraphQL**: Let clients specify exact fields
4. **DTOs**: Map to response-specific objects

**Severity**: MEDIUM - Increases bandwidth, memory, serialization time

## Under-Fetching

Requiring multiple requests to get needed data.

**Identification:**
- Waterfall requests (request depends on previous)
- Multiple endpoints for related data
- No include/expand support

**Fix Strategies:**
1. **Compound Endpoints**: `/users?include=orders`
2. **GraphQL**: Single query for nested data
3. **BFF Pattern**: Backend aggregates for frontend
4. **Parallel Requests**: When dependencies allow

**Severity**: MEDIUM - Increases latency, connection overhead

## Missing Pagination

Returning unbounded result sets.

**Identification:**
- List endpoints without limit
- `findAll()` without pagination
- No cursor for large datasets

**Fix Strategies:**
1. **Offset Pagination**: `?page=1&limit=20`
2. **Cursor Pagination**: `?cursor=abc&limit=20` (better for large sets)
3. **Default Limits**: Always apply max limit server-side
4. **Streaming**: For very large exports

**Severity**: HIGH - Can crash server/client with large data

## Inefficient Algorithms

O(n²) or worse complexity where better solutions exist.

**Identification:**
- Nested loops on collections
- Repeated array.find/includes in loops
- String concatenation in loops
- Sort inside loops

**Fix Strategies:**
1. **Use Maps/Sets**: O(1) lookup instead of O(n)
2. **Single Pass**: Combine operations
3. **Pre-compute**: Calculate once, reuse
4. **Better Algorithms**: Binary search for sorted data

**Severity**: HIGH - Becomes unusable with large data

## Unnecessary Re-renders (Frontend)

Components re-rendering when their output hasn't changed.

**Identification:**
- Inline objects/arrays in JSX
- Inline function handlers
- Missing React.memo/useMemo/useCallback
- Context changes affecting all consumers

**Fix Strategies:**
1. **Memoization**: React.memo for components
2. **Stable References**: useMemo for objects, useCallback for functions
3. **Context Splitting**: Separate frequently-changing state
4. **Selectors**: Only subscribe to needed state slices

**Severity**: MEDIUM-HIGH - Causes janky UI, especially on lists

## Sequential Async Operations

Running async operations one-by-one when parallel is possible.

**Identification:**
- Sequential await statements
- Waterfall promises
- Loop with await inside

**Fix Strategies:**
1. **Promise.all**: Run independent operations in parallel
2. **Promise.allSettled**: When some can fail
3. **Batching**: Group operations efficiently
4. **Pipelining**: Stream processing

**Severity**: MEDIUM - Multiplies latency

## Quick Reference by Layer

### Database
| Issue | Detect | Fix |
|-------|--------|-----|
| N+1 queries | Query in loop | Eager load / batch |
| Missing index | Slow WHERE/JOIN | Add index |
| SELECT * | No column list | Specify columns |
| No LIMIT | Unbounded query | Add pagination |

### Backend
| Issue | Detect | Fix |
|-------|--------|-----|
| O(n²) loop | Nested iteration | Use Set/Map |
| Sequential await | await in sequence | Promise.all |
| Sync I/O | fs.readFileSync | Use async version |
| No caching | Repeated computation | Memoize |

### Frontend
| Issue | Detect | Fix |
|-------|--------|-----|
| Re-renders | Inline objects/functions | Memoize |
| Bundle size | Large imports | Tree-shake/split |
| Memory leak | No cleanup | useEffect cleanup |
| Layout thrash | Read+write DOM | Batch DOM ops |

### API
| Issue | Detect | Fix |
|-------|--------|-----|
| Over-fetching | All fields returned | Field selection |
| Under-fetching | Multiple requests | Include/expand |
| No pagination | Unbounded lists | Add limit/cursor |
| N+1 calls | Fetch in loop | Batch endpoint |
