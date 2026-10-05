---
name: optimize
description: Performance optimization workflow -- profile, identify bottlenecks, apply targeted improvements, verify gains
layer: hub
category: workflow
triggers:
  - "/optimize"
  - "optimize this"
  - "make this faster"
  - "improve performance"
  - "reduce load time"
  - "this is too slow"
inputs:
  - target: Code, feature, page, or endpoint to optimize
  - metric: What to optimize for (latency, throughput, memory, bundle size, render time, etc.)
  - baseline: Current performance measurement (optional, will attempt to measure)
  - budget: Performance target/budget (optional)
outputs:
  - profileReport: Analysis of current performance with identified bottlenecks
  - optimizations: List of applied optimizations with measured impact
  - beforeAfter: Performance comparison showing improvement
  - tradeoffs: What was traded for performance (complexity, memory, readability)
linksTo:
  - scout
  - test
  - code-review
  - refactor
linkedFrom:
  - cook
  - team
  - ship
preferredNextSkills:
  - test
  - code-review
fallbackSkills:
  - scout
  - research
riskLevel: medium
memoryReadPolicy: selective
memoryWritePolicy: selective
sideEffects:
  - Modifies source code files
  - May run performance benchmarks
  - May add caching layers or change data structures
---

# Optimize Skill

## Purpose

Systematically identify and resolve performance bottlenecks using a measure-first approach. This skill prevents the most common optimization mistake: guessing where the problem is and optimizing the wrong thing.

**The law of optimization**: Measure first. Optimize the bottleneck. Measure again. Repeat.

Never optimize based on intuition alone. Developers are notoriously bad at predicting where performance problems live.

## Workflow

### Phase 1: Define the Target

1. **Identify what to optimize** -- Be specific:
   - API endpoint response time
   - Page load / Time to Interactive
   - Database query performance
   - Build / bundle size
   - Memory consumption
   - Throughput (requests/sec, items/sec)
   - Render performance (FPS, re-render count)

2. **Set the performance budget** -- What is "good enough"?
   - If the user provides a target, use that
   - If not, use industry standards:
     - API: < 200ms p95
     - Page load (LCP): < 2.5s
     - Interaction (INP): < 200ms
     - Bundle size: < 200KB (initial JS)
     - Database query: < 50ms

3. **Establish the baseline** -- Measure current performance before changing anything. Record exact numbers, not impressions.

### Phase 2: Profile and Analyze

4. **Identify the profiling approach** based on the target:

   | Target | Profiling Approach |
   |--------|-------------------|
   | API latency | Add timing logs, trace request lifecycle |
   | Database | Analyze query plans (EXPLAIN), check indexes |
   | Frontend load | Analyze bundle (webpack-bundle-analyzer), check network waterfall |
   | Render perf | Check component re-renders, identify expensive renders |
   | Memory | Heap snapshots, allocation tracking |
   | Build time | Build profiling, dependency analysis |

5. **Read the code** in the hot path -- the execution path that matters for the target metric.

6. **Identify bottlenecks** -- Look for these common performance problems:

   **Backend / General**:
   - N+1 database queries (loop of individual queries instead of batch)
   - Missing database indexes
   - Synchronous operations that could be parallel (`Promise.all`)
   - Unbounded data fetching (no pagination, no limits)
   - Expensive computation in hot paths (should be cached or precomputed)
   - Redundant work (computing the same thing multiple times)
   - Blocking I/O on the main thread
   - Missing caching for stable data
   - Oversized payloads (returning more data than needed)

   **Frontend specific**:
   - Unnecessary re-renders (missing memo, unstable references)
   - Large bundle imports (importing entire library for one function)
   - Render-blocking resources (sync scripts, unoptimized fonts)
   - Layout thrashing (reading then writing DOM in loops)
   - Unoptimized images (no lazy loading, wrong format, no srcset)
   - Missing code splitting (everything in one bundle)
   - Client-side computation that should be server-side

7. **Rank bottlenecks by impact** -- Which bottleneck, if resolved, would produce the largest improvement? Start there.

### Phase 3: Apply Optimizations

8. **Apply optimizations one at a time**, measuring after each:

   **Common optimization patterns**:

   | Problem | Optimization | Trade-off |
   |---------|-------------|-----------|
   | N+1 queries | Batch query / JOIN | Query complexity |
   | Missing index | Add database index | Write performance, storage |
   | Sequential I/O | `Promise.all` / parallel | Error handling complexity |
   | Redundant computation | Memoization / caching | Memory, staleness |
   | Large payload | Field selection, pagination | API complexity |
   | Large bundle | Dynamic import, tree-shaking | Loading states, code complexity |
   | Unnecessary re-renders | `React.memo`, `useMemo`, `useCallback` | Code complexity |
   | Unoptimized images | Next/Image, WebP, lazy loading | Build complexity |
   | No caching | HTTP cache, in-memory cache, CDN | Invalidation complexity |
   | Blocking computation | Web Worker, server-side | Architecture complexity |

9. **For each optimization**:
   - **Describe what is being changed and why**
   - **Apply the change** using Edit tool
   - **Measure the result** -- Did it improve? By how much?
   - **Assess the trade-off** -- Was the added complexity worth the gain?
   - **Decide: keep or revert** -- If the gain is minimal and the trade-off is significant, revert.

10. **Stop when the budget is met** or when remaining optimizations have diminishing returns.

### Phase 4: Verification

11. **Run the full test suite** -- Optimizations must not break functionality.

12. **Measure final performance** -- Compare against baseline.

13. **Check for regressions in other dimensions**:
    - Did optimizing speed increase memory usage?
    - Did optimizing bundle size break functionality?
    - Did caching introduce staleness bugs?

14. **Produce the optimization report** using the template below.

## Optimization Report Template

```markdown
# Optimization Report

## Target
**Metric**: [what was optimized]
**Baseline**: [measurement before]
**Budget**: [target]
**Result**: [measurement after]
**Improvement**: [percentage or absolute]

## Bottlenecks Identified
| # | Bottleneck | Impact | Location |
|---|-----------|--------|----------|
| B1 | [description] | [estimated impact] | [file:line] |
| B2 | [description] | [estimated impact] | [file:line] |

## Optimizations Applied
### O1: [Name]
**Bottleneck**: B1
**Change**: [description]
**Before**: [measurement]
**After**: [measurement]
**Trade-off**: [what was given up]
**Files changed**: [list]

### O2: [Name]
...

## Optimizations Considered but Not Applied
- [optimization]: [reason -- diminishing returns, too complex, etc.]

## Performance Summary
| Metric | Baseline | After | Change |
|--------|----------|-------|--------|
| [primary metric] | [value] | [value] | [improvement] |
| [secondary metric] | [value] | [value] | [change] |

## Verification
- [ ] All tests pass
- [ ] No regressions in other metrics
- [ ] Performance gains verified in representative conditions

## Maintenance Notes
[Any ongoing considerations -- cache invalidation, index maintenance, etc.]
```

## Usage

### General optimization
```
/optimize The /api/users endpoint takes 3 seconds to respond
```

### Frontend performance
```
/optimize Reduce the initial page load time -- Lighthouse score is 45
```

### Specific metric
```
/optimize Reduce the JavaScript bundle size below 150KB
```

### Database optimization
```
/optimize The product search query is slow with 1M+ rows
```

## Examples

### Example: API endpoint optimization

**Baseline**: `/api/orders` responds in 2.3s
**Profiling**: Found N+1 query -- fetching customer for each order individually
**Optimization**: Replace loop of `findCustomer(order.customerId)` with single `findCustomers(customerIds)` using IN clause
**Result**: Response time dropped to 180ms (92% improvement)
**Trade-off**: Slightly more complex query code

### Example: Bundle size optimization

**Baseline**: Initial JS bundle is 450KB
**Profiling**: `moment.js` (300KB) used for one `formatDate()` call
**Optimization**: Replace with `date-fns/format` (2KB) or native `Intl.DateTimeFormat`
**Result**: Bundle reduced to 155KB (66% reduction)
**Trade-off**: None meaningful

### Example: Render optimization

**Baseline**: List of 500 items causes 2s freeze on filter change
**Profiling**: Every item re-renders on filter change because list component re-creates item objects
**Optimization**: Virtualize the list (react-window), memoize item components, stabilize references
**Result**: Filter change is instant, only visible items render
**Trade-off**: Added dependency, slightly more complex list component

## Guidelines

- **Measure before and after EVERY change** -- Intuition is wrong more often than right.
- **Optimize the bottleneck, not the fast path** -- Making a 1ms operation 0.5ms is irrelevant if a 500ms operation exists.
- **One optimization at a time** -- Otherwise you cannot attribute improvements to specific changes.
- **Simplicity is a feature** -- If two optimizations give similar results, prefer the simpler one.
- **Do not sacrifice correctness for speed** -- A fast wrong answer is worse than a slow right answer.
- **Consider the 80/20 rule** -- 80% of improvement usually comes from 20% of the optimizations. Stop when returns diminish.
- **Document trade-offs** -- Every optimization has a cost. Make the cost visible for future maintainers.
- **Premature optimization is real** -- Only optimize code that is demonstrably too slow, not code that might be slow someday.
- **Caching solves most problems and creates new ones** -- If you add caching, think carefully about invalidation.
