---
name: detect-n-plus-one
description: Detect N+1 query patterns in the codebase. Finds loops that contain database or API calls that should be batched. Works across all languages. Use when user asks to find performance issues or N+1 patterns.
allowed-tools: mcp__miller__fast_search, mcp__miller__get_symbols, mcp__miller__trace_call_path, mcp__miller__fast_refs, Read
---

# N+1 Query Pattern Detection

## Activation Announcement

**IMPORTANT**: When this skill activates, ALWAYS start your response with:

```
🔍 **N+1 Pattern Detection Scan**
Scanning codebase for loop + query anti-patterns...
```

This provides a visual indicator to the user that systematic detection is running.

## What is N+1?

An N+1 query problem occurs when code:
1. Fetches a list of N items
2. Then makes 1 additional query per item in a loop

Instead of 1 batch query, you get N+1 queries. For 100 items = 101 DB roundtrips.

## Detection Strategy

### Phase 1: Semantic Search for Loop + Query Patterns

Run these searches to find suspicious code:

```
fast_search("for loop database query execute", method="semantic", limit=30)
fast_search("foreach await repository find", method="semantic", limit=30)
fast_search("loop api call fetch request", method="semantic", limit=30)
fast_search("iterate collection query each", method="semantic", limit=30)
```

### Phase 2: Pattern Search for Language-Specific Idioms

```
# C# / Entity Framework
fast_search("foreach await context", method="text", limit=20)
fast_search("for var in FirstOrDefault", method="text", limit=20)

# TypeScript / Prisma / TypeORM
fast_search("for of await prisma findUnique", method="text", limit=20)
fast_search("forEach await fetch", method="text", limit=20)

# Python / SQLAlchemy / Django
fast_search("for in session query", method="text", limit=20)
fast_search("for in objects get filter", method="text", limit=20)

# General patterns
fast_search("for each get by id", method="semantic", limit=20)
```

### Phase 3: Trace Suspicious Functions

For each suspicious result, trace the call path:

```
trace_call_path(symbol_name="<function_name>", direction="downstream", max_depth=3)
```

Look for paths that lead to:
- Database access (repository, context, connection, cursor)
- HTTP calls (fetch, axios, http client)
- Cache lookups without batching

### Phase 4: Verify with Code Inspection

```
get_symbols(file_path="<file>", target="<function>", mode="full")
```

Confirm the pattern by checking:
- Is there a loop construct (for, foreach, while, map)?
- Is there a query/fetch inside the loop body?
- Could this be batched into a single query?

## Output Format

**IMPORTANT**: Always present findings in this structured format:

```
## N+1 Pattern Detection Results

### Summary
- Files scanned: X
- Potential N+1 patterns found: Y
- Confidence: High/Medium/Low

### Findings

#### 1. [HIGH] file/path.ts:42 - `processOrders`
**Pattern**: foreach loop with individual DB fetch
**Code**:
```typescript
for (const order of orders) {
    const customer = await db.customers.findUnique({ where: { id: order.customerId }});
}
```
**Fix**: Batch fetch all customers upfront with `findMany({ where: { id: { in: customerIds }}})`

#### 2. [MEDIUM] file/path.cs:128 - `LoadUserDetails`
**Pattern**: LINQ with lazy loading inside loop
...

### Recommendations
1. Replace individual queries with batch operations
2. Use Include/ThenInclude for eager loading (EF Core)
3. Consider caching for frequently accessed data
```

## Red Flags to Look For

### High Confidence Indicators
- `await` inside `for`/`foreach`/`for...of` with DB method name
- Loop variable used as query parameter
- `.Find()`, `.Get()`, `.FirstOrDefault()`, `.findUnique()` inside loops
- Multiple queries returning single items in sequence

### Medium Confidence Indicators
- Lazy loading patterns (accessing navigation properties in loops)
- `.Select()` with async operations
- Nested loops with any data access

### Language-Specific Patterns

| Language | High-Risk Patterns |
|----------|-------------------|
| C# | `foreach` + `await context.X.FindAsync()` |
| TypeScript | `for...of` + `await prisma.x.findUnique()` |
| Python | `for x in` + `session.query().filter().first()` |
| Java | `for` + `repository.findById()` |
| Go | `for range` + `db.Query()` or `db.QueryRow()` |

## Success Criteria

This skill succeeds when:
- Clear visual announcement at start
- Systematic search across semantic + pattern modes
- Findings presented with file:line locations
- Confidence levels assigned to each finding
- Actionable fix suggestions provided
- Results are language-appropriate
