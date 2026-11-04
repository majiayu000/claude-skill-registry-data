---
name: profile
description: Performance profiling and bottleneck identification. Measures database statements and time per request on the running app, scans the code for bottleneck patterns, ranks findings by impact, and suggests specific optimizations. Use when user says "profile", "why is this slow", "find bottleneck", "performance issue", "slow query", "slow endpoint", "optimize", or needs to find what is causing poor performance. For benchmark comparisons, use /benchmark; for load testing, use /test perf; for general code review, use /review.
argument-hint: "/profile | /profile src/services/order.service.ts | /profile src/api --db"
allowed-tools: "Read, Grep, Glob, Bash"
---

## Overview

Performance profiling that measures what a slow request actually costs on the running app, scans the codebase for common bottleneck patterns, ranks findings by impact, and provides concrete fixes with code examples. A measured finding outranks a pattern match. Covers database queries, API latency, frontend loading, and algorithmic complexity.

## When to use

- When a specific endpoint, page, or operation is slow.
- When you need to find the highest-impact optimization targets before a release.
- When database query performance is degrading.
- When startup time or build time is unexpectedly long.

## When NOT to use

- For benchmark comparisons between implementations. Use `/benchmark` instead.
- For HTTP load testing with concurrent users. Use `/test perf` instead.
- For general code quality review. Use `/review` instead.
- For security scanning. Use `/audit` instead.

## Arguments

This skill accepts optional arguments after `/profile`:

- No arguments: scan the project for common bottleneck patterns across all categories.
- `<path>`: profile a specific file, directory, or module. Example: `/profile src/services/order.service.ts`.
- `--db`: focus exclusively on database query bottlenecks.
- `--api`: focus exclusively on API endpoint latency.
- `--frontend`: focus exclusively on frontend performance.
- `--startup`: focus on application startup time.

Flags can be combined with a path: `/profile src/api --db`.

## Steps

1. **Identify the performance concern.** If a specific path was provided, scope the analysis to that area. If a focus flag was passed, limit categories accordingly. Otherwise, scan all categories.

2. **Detect the tech stack.** Read package.json, go.mod, Cargo.toml, or equivalent to identify: the framework, the ORM, the database, the frontend framework, the bundler, and the test runner. This determines which patterns to search for.

3. **Measure statements per request on the running app.** A grep suspects a bottleneck; a measurement proves it. When the app runs locally, drive the slow path once with the ORM's query log on, such as Prisma `log: ['query']`, Drizzle `logger: true`, or Django `connection.queries`, or read the request's span list from the APM. Record `route`, `ms`, and `statements` for each request. Read the statement log for three shapes:
   - **Re-fetching data the caller already holds:** the same row read twice in one request, because a downstream function takes an ID and fetches what the caller already loaded. The fix passes the loaded object, typed as the minimal shape the callee reads.
   - **Per-row query loops:** a statement count that grows with the row count, such as 820 statements for one request. This is the runtime proof of the N+1 that step 4 only suspects.
   - **Independent reads run in sequence:** consecutive statements with no data dependency between them. The fix runs them concurrently with `Promise.all` or the framework's equivalent, bounded per [`rules/architecture-defaults.md`](../../rules/architecture-defaults.md).

   When the app cannot run, state that this step was skipped and why, and mark every static finding `unmeasured`.

4. **Scan for database bottlenecks.** Search the codebase for these patterns:
   - **N+1 queries:** ORM calls inside loops or `.map()` callbacks. Grep for query methods like `.findOne`, `.findUnique`, `.find`, `.get` inside `for`, `forEach`, `.map`, `.flatMap`. Each match is a potential N+1.
   - **Missing indexes:** read the schema or migration files. For each query that filters, sorts, or joins on a column, check if that column has an index. Cross-reference queries in service files with index definitions.
   - **Full table scans:** queries without a WHERE clause on large tables, or queries using `LIKE '%term%'` which cannot use indexes.
   - **Unnecessary eager loading:** ORM includes or joins that load relations not used by the calling code. Trace from the query to where its result is consumed.
   - **Missing connection pooling:** check database configuration for pool settings. If the ORM connects without a pool, flag it.
   - **Unbounded queries:** queries without LIMIT that could return thousands of rows. Check for missing pagination.

5. **Scan for API bottlenecks.** Search for these patterns:
   - **Sequential external calls:** multiple `await fetch()` or HTTP client calls that are independent but executed sequentially instead of with `Promise.all`.
   - **Missing caching:** repeated identical queries or computations per request without a cache layer. Look for pure functions called with the same arguments across requests.
   - **Unbounded response sizes:** API endpoints that return entire collections without pagination.
   - **Unnecessary serialization:** objects serialized and deserialized multiple times in the same request path.
   - **Synchronous I/O on request paths:** file reads, DNS lookups, or crypto operations blocking the event loop.
   - **Missing compression:** check if response compression middleware is configured.

6. **Scan for frontend bottlenecks.** Search for these patterns:
   - **Large bundle size:** check build output size. Look for large dependencies imported entirely when only a small part is used.
   - **Unoptimized images:** images served without width/height, missing lazy loading, or served in non-modern formats.
   - **Blocking resources:** synchronous scripts in `<head>`, render-blocking CSS, missing `async` or `defer` on scripts.
   - **Excessive re-renders:** components that re-render on every parent render due to missing `memo`, `useMemo`, or `useCallback`. Look for object or array literals created inline as props.
   - **Missing code splitting:** large route components imported statically instead of with `React.lazy` or dynamic `import()`.

7. **Scan for general algorithmic bottlenecks.** Search for these patterns:
   - **O(n^2) algorithms:** nested loops over the same or related collections. `.find()` inside `.map()` or `.filter()`. Array includes checks inside loops where a Set would be O(1).
   - **Unnecessary allocations in loops:** creating new arrays, objects, or strings inside tight loops that could be pre-allocated or computed once.
   - **Missing pagination:** iterating over unbounded collections from the database or API.
   - **Redundant computations:** the same expensive computation performed multiple times when the result could be cached or memoized.

8. **For each bottleneck found, produce a finding.**

   Each finding includes:
   - **File and line:** exact location.
   - **Category:** database, API, frontend, or algorithmic.
   - **Issue:** what the problem is in one sentence.
   - **Impact estimate:** rough time cost or resource waste. Use qualitative levels: critical, high, medium, low. Critical means seconds of latency or orders of magnitude waste. Low means milliseconds in uncommon paths.
   - **Measured:** the `ms` and `statements` from step 3 for the request that hits this code, or `unmeasured`.
   - **Fix:** concrete code change with a before/after example.

9. **Rank findings by estimated impact.** Critical first, then high, medium, low. Within the same level, order by frequency of execution.

10. **Present the report.** Use this format:

    ````markdown
    ## Bottleneck Report

    **Scope:** <path or "full project">
    **Stack:** <detected stack summary>
    **Findings:** N total (X critical, Y high, Z medium, W low)

    ---

    ### Critical

    #### 1. N+1 query in order listing
    **File:** src/services/order.service.ts:45
    **Issue:** `findUnique` called inside a loop for each order's customer.
    **Impact:** For 100 orders, this executes 101 queries instead of 2.
    **Measured:** `GET /orders`, 101 statements, 840 ms
    **Fix:**

    Before:

    ```ts
    for (const order of orders) {
      order.customer = await prisma.customer.findUnique({ where: { id: order.customerId } });
    }
    ```

    After:

    ```ts
    const orders = await prisma.order.findMany({
      include: { customer: true },
    });
    ```

    ### High

    ...

    ### Medium

    ...

    ### Low

    ...

    ---

    ### Summary

    Top 3 actions by impact:
    1. Fix the N+1 query in order listing. Critical
    2. Add pagination to the products endpoint. High
    3. Replace sequential API calls with Promise.all in checkout. High
    ````

## Rules

- Focus on measurable impact, not code style. A function that violates naming conventions but runs in O(1) is not a performance finding.
- Quantify wherever possible. "This is slow" is not a finding. "This executes 101 queries instead of 2" is.
- A measured finding outranks a pattern match at the same impact level, and the report names which findings were measured.
- Suggest only fixes that preserve existing behavior. A performance fix that changes semantics is a bug.
- Read the actual code before flagging. A loop that runs over 3 items is not a performance problem even if the pattern looks like O(n^2).
- When the scope is a specific path, still check its callers and callees one level deep. A bottleneck might be in the calling code.
- Do not suggest premature optimization. Only flag patterns that matter at the project's actual or expected scale.
- When unsure about impact, classify as low rather than inflating severity.

## Common Rationalizations

- "A `.find()` inside `.map()` is O(n^2), so it is a finding": read the code first. A loop over three items is not a bottleneck at any scale the project reaches.
- "Memoizing every component is a free win": flag only patterns that matter at the project's actual or expected scale, with a fix that preserves behavior.
- "It feels slow, so it is critical": critical means seconds of latency or orders of magnitude of waste. Without a number, classify it as low.
- "The path I was given is where the problem lives": check the callers and callees one level deep, since the cost often sits in the calling code.
- "This function name is confusing, worth listing": naming and style are not performance findings.

## Red Flags

- Stop and downgrade to low when the impact has no number and no execution frequency behind it.
- Stop and trace the consumer when flagging eager loading before reading where the query result is used.
- Stop and read the schema or migration files when flagging a missing index without having read them.
- Stop and drop the fix when it changes ordering, error behavior, or any other observable result.
- Stop and remove the finding when it is about naming or style.

## Verification

- Every finding carries a file and line, a category, a one-sentence issue, an impact level, and a before and after fix.
- Every flagged location was read in this run.
- Every finding carries its step 3 measurement or the word `unmeasured`, and a skipped step 3 is stated with its reason.
- Findings run critical to low, and ties are ordered by execution frequency.
- The counts in the report header match the findings listed.
- The top three actions in the summary are the three highest-ranked findings.

## Related skills

- `/test perf` - HTTP load testing with concurrent users and latency percentiles.
- `/review` - General code review covering correctness, security, and quality.
- `/benchmark` - Compare latency, bundle size, and query time against saved baselines once a fix lands.
