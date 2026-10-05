---
name: performance-review
description: Profile performance, detect bottlenecks, analyze resource usage, caching strategies, and boundary conditions. Use when addressing performance issues.
---

# Code Review - Performance Review

Identify performance bottlenecks, caching issues, and optimization opportunities. This skill is **Phase 4** of the 6-phase code review methodology.

## When to Use This Skill

Use this skill when you need to:

- Identify performance bottlenecks
- Optimize critical code paths
- Reduce resource consumption
- Improve response times
- Address scalability concerns
- Profile memory and CPU usage
- Evaluate caching strategies

**Trigger phrases**: "performance review", "bottleneck", "slow code", "optimize", "profiling", "latency", "throughput", "memory usage", "caching"

## What This Skill Does

### Performance Dimensions

| Dimension | Metrics |
|-----------|---------|
| **Time** | Response time, latency, throughput |
| **Memory** | Heap usage, allocations, leaks |
| **CPU** | Utilization, hot paths |
| **I/O** | Database queries, network calls |
| **Concurrency** | Threading, async efficiency |
| **Caching** | Hit rate, TTL, invalidation |

### Severity Classification

| Level | Alias | Description |
|-------|-------|-------------|
| **P0** | CRITICAL | Production outages, severe degradation |
| **P1** | HIGH | Significant performance impact |
| **P2** | MEDIUM | Notable inefficiency |
| **P3** | LOW | Minor optimization opportunity |

## Instructions

### Step 1: Profile Application

```bash
# Python
python -m cProfile -s cumtime script.py
py-spy record -o profile.svg -- python script.py

# JavaScript/Node.js
node --prof app.js
clinic doctor -- node app.js

# Java
java -XX:+FlightRecorder -XX:StartFlightRecording=duration=60s,filename=app.jfr App
```

### Step 2: Identify Hot Paths

1. **CPU Profiling**
   - Functions with highest cumulative time
   - Frequent function calls
   - Complex algorithms

2. **Memory Analysis**
   - Large object allocations
   - Memory leaks
   - Garbage collection pressure
   - Event listener leaks (registered but never removed)

3. **I/O Analysis**
   - N+1 query patterns
   - Unoptimized database queries
   - Unnecessary network calls

### Step 3: Common Anti-Patterns

Reference: `references/code-quality-checklist.md` (Performance & Caching section)

| Anti-Pattern | Issue | Solution |
|--------------|-------|----------|
| N+1 Queries | Loop database calls | Batch queries, joins |
| Large Payloads | Excessive data transfer | Pagination, field selection |
| No Caching | Repeated computations | Add caching layer |
| Sync I/O | Blocking operations | Async/await |
| String Concatenation | Memory allocation in loops | StringBuilder/join |
| Missing Memoization | Same pure function called repeatedly | Add memoization |
| Over-fetching | `SELECT *` when only 2 columns needed | Select specific columns |
| No Pagination | Loading entire tables | LIMIT/OFFSET or cursor pagination |

### Step 4: Caching Strategy Analysis

| Issue | Risk | Diagnostic |
|-------|------|-----------|
| **Missing cache** | Repeated expensive computations | "Is this expensive operation called more than once with the same inputs?" |
| **Cache without TTL** | Stale data served indefinitely | "How long is cached data valid?" |
| **No invalidation strategy** | Cache and database drift | "When the source data changes, how is the cache updated?" |
| **Key collisions** | Different data overwriting each other | "Could two different inputs produce the same cache key?" |
| **User data cached globally** | Data leaks between users | "Does the cache key include user/tenant identity?" |
| **Cache stampede** | All caches expire simultaneously | "What happens when the cache expires under load?" |

### Step 5: Boundary Conditions Affecting Performance

Reference: `references/code-quality-checklist.md` (Boundary Conditions section)

| Condition | Performance Impact |
|-----------|-------------------|
| Unbounded collections | Lists/maps growing without limit, OOM risk |
| Large file loading | Reading entire files into memory instead of streaming |
| String concatenation in loops | O(n^2) memory allocation |
| Empty collection edge cases | `.reduce()` without initial value, `.sort()` on empty arrays |

### Step 6: Diagnostic Questions

Apply these questions to each module under review:

1. "What is the most expensive operation in the critical path? Can it be cached, batched, or deferred?"
2. "Are there any N+1 query patterns? (Loop that issues a query per iteration)"
3. "Is there any unbounded data structure that grows with input size?"
4. "For cached data, what is the TTL and invalidation strategy?"

### Step 7: Document Findings

```markdown
## Performance Finding

**File**: [path/to/file.py:42]
**Severity**: P1 (HIGH)
**Impact**: 500ms added latency per request
**Category**: Database Query

### Issue
N+1 query pattern in user loading

### Current Code
```python
users = User.query.all()
for user in users:
    orders = Order.query.filter_by(user_id=user.id).all()
```

### Optimized Code
```python
users = User.query.options(
    joinedload(User.orders)
).all()
```

### Expected Improvement
- Latency: 500ms -> 50ms
- Database queries: N+1 -> 1
```

## Language-Specific Tools

### Python
- cProfile, py-spy, memory_profiler
- line_profiler, tracemalloc

### JavaScript
- Chrome DevTools, Node.js profiler
- clinic.js, 0x

### Java
- JFR, VisualVM, async-profiler
- JMH for benchmarks

### Go
- pprof, trace
- benchmarks

### C# / .NET
- dotTrace, dotMemory
- BenchmarkDotNet

## Quality Checklist

- [ ] Application profiled
- [ ] Hot paths identified
- [ ] Database queries analyzed (N+1, missing indexes, over-fetching)
- [ ] Memory usage reviewed (leaks, unbounded collections)
- [ ] Caching strategy evaluated (TTL, invalidation, stampede)
- [ ] Boundary conditions checked
- [ ] Diagnostic questions applied to each module
- [ ] Findings documented with metrics and severity (P0-P3)

## Related Skills

- `context-analysis` - Context understanding (Phase 1)
- `code-quality` - Code quality + SOLID review (Phase 2)
- `security-review` - Security analysis (Phase 3)
- `performance-testing` - Load testing
- `testing-review` - Test assessment (Phase 5)
- `final-report` - Consolidated report (Phase 6)

---

**Version**: 2.0.0
**Last Updated**: February 2026
**Based on**: DevAI-Hub code review methodology + code-review-expert


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
