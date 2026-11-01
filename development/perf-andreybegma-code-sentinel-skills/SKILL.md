---
name: cs-perf
description: Analyze code for performance issues — N+1 queries, unnecessary re-renders, memory leaks, bundle size problems
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, mcp__typescript__*
---

# Performance Analyzer

You are a performance optimization specialist. Analyze the codebase for common performance anti-patterns and inefficiencies.

## Inputs

`$ARGUMENTS` — optional scope:

- **Empty** — analyze high-risk areas across the project
- **Directory** — `src/api` — focus on that directory
- **File** — `src/services/user.service.ts` — analyze that file in depth
- **Category** — `queries` / `react` / `bundle` / `memory` — focus on specific category

## Step 1: Gather Context

Read `package.json` to identify framework, ORM, state management, and build tool. Read `CLAUDE.md` for performance-related conventions.

**Check TypeScript MCP** — if available, use it for accurate call chain analysis (`findAllReferences()` to trace which callers hit expensive paths). If not: `⚠️ TypeScript MCP not available. Call chain analysis will rely on grep patterns only.`

## Step 2: Database & Query Analysis

### N+1 Query Detection

Find files that contain ORM calls, then check if those calls are inside loops:

```bash
grep -rn "\.\(find\|findOne\|findMany\|findAll\|query\|execute\|aggregate\|count\)\b" src/ --include="*.ts" -l
```

For each file found, read it and check if ORM calls are nested inside a loop (`for`, `while`, `forEach`, `.map()`, `.reduce()`). Flag:

- `await Promise.all(items.map(item => repo.findOne(...)))` — N+1 even with Promise.all; should use `WHERE id IN (ids)`
- `for (const item of items) { await db.find(...) }` — sequential N+1
- GraphQL `@ResolveField` calling a service per-record without DataLoader

### Query Optimization Issues

```bash
# Unbounded queries (no pagination/limit)
grep -rn "findMany\b" src/ --include="*.ts" | grep -v "take:\|limit:\|skip:\|paginate\|cursor:"

# Potential SELECT * (full entity fetch without field selection)
grep -rn "findMany\|findAll\|find({" src/ --include="*.ts" | grep -v "select:\|fields:\|attributes:"
```

Flag:
- `findMany` without `take` or cursor pagination — unbounded list query
- `findMany` + in-memory `.filter()` instead of pushing condition to the query
- Check migration files for `CREATE TABLE` statements without a corresponding index on columns used in `WHERE`, `ORDER BY`, or `JOIN`

## Step 3: React Performance Analysis

### Unnecessary Re-renders

```bash
# Inline objects in JSX props (new reference every render)
grep -rn "style={{" src/ --include="*.tsx" | head -30

# Inline arrow functions in event handlers
grep -rn "on[A-Z][a-z]*={(" src/ --include="*.tsx" | head -30
grep -rn "on[A-Z][a-z]*={() =>" src/ --include="*.tsx" | head -30

# Expensive computations without memoization
grep -rn "useMemo\|useCallback" src/ --include="*.tsx" -l
```

For each file with inline props, read it to confirm the prop is not a stable reference. Flag:

- `style={{ ... }}` passed as prop — creates new object every render; extract to const or `useMemo`
- `onClick={() => fn(id)}` — creates new function every render; use `useCallback` when passed to memoized children
- Expensive array transforms (`filter`, `map`, `sort`) in render body without `useMemo`
- Fat context objects (user + theme + settings merged in one context) — split or use selectors

### State Issues

```bash
# Derived state stored in useState
grep -rn "useState" src/ --include="*.tsx" -A 1 | grep -E "filter|map|reduce|sort|find\b"
```

Flag:
- `useState` holding data that can be computed from other state/props — compute inline or with `useMemo`
- Duplicate `useQuery`/`useSWR` with the same key in multiple components — lift to shared provider

## Step 4: Memory Leak Detection

```bash
# useEffect that starts async resources — check for missing cleanup
grep -rn "useEffect" src/ --include="*.tsx" -A 15 | grep -B8 "setInterval\|setTimeout\|addEventListener\|\.subscribe\|\.connect\|EventSource\|WebSocket"
```

For each match, read the full `useEffect` block. Flag if the effect does **not** return a cleanup function:

```typescript
// BAD — timer never cleared
useEffect(() => {
  const id = setInterval(() => tick(), 1000)
}, [])

// GOOD
useEffect(() => {
  const id = setInterval(() => tick(), 1000)
  return () => clearInterval(id)
}, [])
```

Node.js:

```bash
# Event listeners without removal
grep -rn "\.on(" src/ --include="*.ts" | grep -v "\.off(\|removeListener\|once("
```

Flag:
- `EventEmitter.on()` without corresponding `off()` or `removeListener()`
- Streams not `.destroy()`ed after use
- In-memory caches or maps that grow without eviction (no max size, no TTL)

## Step 5: Bundle Size Analysis

```bash
# Heavy libraries with lighter alternatives
grep -rn "from 'moment'" src/ --include="*.ts" --include="*.tsx"
grep -rn "from 'lodash'" src/ --include="*.ts" --include="*.tsx"
grep -rn "^import _ from" src/ --include="*.ts" --include="*.tsx"
grep -rn "from 'axios'" src/ --include="*.ts" --include="*.tsx"
grep -rn "from 'uuid'" src/ --include="*.ts" --include="*.tsx"

# Dev-only packages imported in production code
grep -rn "from '@testing-library" src/ --include="*.ts" --include="*.tsx" | grep -v "\.spec\.\|\.test\."

# Missing 'import type' (causes runtime import of types)
grep -rn "^import {" src/ --include="*.ts" | grep -v "import type" | head -20
```

Flag heavy libraries and suggest lighter alternatives (e.g. `dayjs`/`date-fns` for `moment`, native `crypto.randomUUID()` for `uuid`, `fetch` for `axios`, named `lodash-es` imports for `lodash`).

Check for duplicate package versions:
```bash
npm ls --depth=1 2>/dev/null | grep " deduped\| — " | head -20
```

```bash
# Pages/routes without lazy loading
grep -rn "^import.*from.*pages/\|^import.*from.*views/" src/ --include="*.ts" --include="*.tsx" | grep -v "lazy\|dynamic\|React.lazy"
```

## Step 6: API & Network Performance

```bash
# Sequential awaits that could be parallelized
grep -rn "^\s*const .* = await" src/ --include="*.ts" -A 1 | grep -B1 "^\s*const .* = await" | head -40
```

For each file with consecutive `await` calls, read the function body and check if the awaited operations have no data dependency between them. Flag as `Promise.all` candidate:

```typescript
// BAD — sequential, 2x slower
const user = await getUser(id)
const org = await getOrg(orgId)  // doesn't use user

// GOOD
const [user, org] = await Promise.all([getUser(id), getOrg(orgId)])
```

Flag:
- Same API called in multiple places without caching (check for duplicate `useQuery` / `fetch` calls for the same resource)
- Fetching full objects when only an ID or one field is needed (over-fetching)
- Multiple round trips for related data that could be batched with `include` or a batch endpoint

## Output Format

Start with a summary table:

```
| Category    | Issues | Top Severity |
|-------------|--------|--------------|
| DB queries  | 2      | HIGH         |
| React       | 1      | MEDIUM       |
| Memory      | 0      | —            |
| Bundle      | 2      | MEDIUM       |
| API         | 1      | HIGH         |
```

Then list findings:

```
### [CRITICAL/HIGH/MEDIUM/LOW]: [Short title]
**Location:** file:line
**Impact:** [estimated cost — e.g., "100 queries per request instead of 1", "saves ~40KB gzip"]
**Fix:** [concrete fix — include code snippet if non-trivial]
```

End with:
- **Quick Wins** — low effort, high impact (fix in < 1 hour)
- **Medium Term** — higher effort but worth it

## Severity Levels

- **CRITICAL** — causes timeouts or crashes in production (unbounded queries, uncontrolled memory growth)
- **HIGH** — noticeable slowdown on normal usage (N+1 queries, memory leaks, sequential awaits on hot path)
- **MEDIUM** — unnecessary overhead affecting perceived performance (re-renders, large bundle, suboptimal patterns)
- **LOW** — micro-optimization

## Important

- Estimate the performance cost for every finding (queries saved, render cycles avoided, KB saved)
- If `$ARGUMENTS` is a specific category, run only the relevant Step (2 = queries, 3 = react, 4 = memory, 5 = bundle, 6 = api)
