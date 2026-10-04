---
name: performance-optimization
description: >
  Systematic performance optimization with measurement-first methodology.
  Use when performance issues are identified, during review phase, or
  when building performance-critical features. Profile before optimizing.
version: 1.0.0
permissions:
  - fs.read
  - fs.write
  - shell.exec
  - browser.inspect
triggers:
  - context: "performance issue"
  - context: "slow response times"
  - context: "optimization needed"
  - command: "/review"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
dependencies:
  - test-driven-development@^1.0.0
author: codehands-core
signed: true
tier: 2
---

## Overview

Performance optimization follows one iron rule: **measure first, optimize second.** Never optimize based on intuition. Profile, identify the bottleneck, fix it, measure again. Premature optimization is the root of all evil — but measured optimization is engineering.

## When to Use

- When profiling reveals a measurable performance problem
- During `/review` phase for performance-sensitive code
- When building features with explicit performance requirements
- NOT speculatively ("this might be slow someday")

## Process

### 1. Measure Current Performance

Before ANY optimization:
```bash
# Backend: Response time
time curl -s http://localhost:3000/api/endpoint

# Frontend: Lighthouse
npx lighthouse http://localhost:3000 --output=json

# Database: Query time
EXPLAIN ANALYZE SELECT ...;
```

Record the baseline. Without a baseline, you can't prove improvement.

### 2. Identify the Bottleneck

- Is it CPU? Memory? I/O? Network? Database?
- Use profiling tools appropriate to the stack
- The bottleneck is ONE thing. Find it before fixing anything.

### 3. Optimize the Bottleneck

Apply the fix with the smallest possible change. Common optimizations:

| Problem | Solution |
|---|---|
| N+1 queries | Eager loading, DataLoader, batch queries |
| Missing index | Add database index on query columns |
| Unbounded query | Add LIMIT, implement pagination |
| Full table scan | Add WHERE clause, use index |
| Unnecessary re-renders | Memoization (React.memo, useMemo) |
| Large bundle | Code splitting, tree shaking, lazy loading |
| Uncompressed responses | Enable gzip/brotli compression |
| Synchronous blocking | Move to async/background job |

### 4. Measure Again

Same measurement as Step 1. Compare to baseline. If improvement < 10%, reconsider whether the optimization is worth the complexity.

### 5. Document the Change

```markdown
## Performance Optimization: [What]
- Baseline: 450ms p99 response time
- After: 85ms p99 response time
- Improvement: 5.3x faster
- Change: Added index on users.email column
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I know this will be slow" | You don't — measure it. Developers are notoriously bad at predicting bottlenecks. |
| "Premature optimization is bad, so I shouldn't think about performance" | Premature optimization of the wrong thing is bad. Choosing an O(n²) algorithm when O(n) exists isn't "premature" — it's a mistake. |
| "The optimization is obvious, I don't need to measure" | Obvious optimizations sometimes make things worse (e.g., caching adding overhead for small datasets). Measure. |

## Red Flags

- Optimizing without a baseline measurement
- Optimizing code that isn't the bottleneck
- Adding caching without understanding the access pattern
- Micro-optimizing at the cost of readability
- No measurement after the change

## Verification

- [ ] Baseline performance measured before optimization
- [ ] Bottleneck identified via profiling (not guessing)
- [ ] Optimization targets the actual bottleneck
- [ ] Performance measured after optimization (improvement confirmed)
- [ ] No regression in functionality (all tests pass)
- [ ] Optimization documented with before/after metrics

## See Also

- `references/performance-checklist.md` — Quick-scan checklist
- `codehands:frontend-ui-engineering` — Frontend-specific performance
- `codehands:code-simplification` — When simplification improves performance
