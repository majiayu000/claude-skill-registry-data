---
name: perf-critic
description: "Performance review — runtime, memory, network, rendering bottlenecks in implementations and live systems."
aliases: [performance-critic, perf-review]
purpose: Deep-dive performance reviewer and scalability auditor for code/architecture
tier: critic
version: 0.1.0
---

# perf-critic Skill

## JTBD (Jobs To Be Done)

### Primary Job
When I have an existing implementation or architecture and need to know what breaks first under load,
I want a deep performance review,
so I can find the real bottlenecks, budget gaps, and cost risks before scale punishes us.

### Secondary Jobs
- When the system feels slow but the cause is unclear, I want a disciplined bottleneck investigation, so I can stop guessing.
- When performance budgets or capacity assumptions are missing, I want them made explicit, so I can make decisions with real constraints.

### Job Layers
- Functional: Audit an existing system or design for latency, throughput, scalability, cost, and observability risks.
- Emotional: Reduce the uncertainty of not knowing whether today's system will survive tomorrow's traffic.
- Social: Helps the user defend performance decisions to engineering peers, leadership, and operations teams with concrete evidence.

### This Skill Is For
- A user with an existing feature, service, page, or architecture that needs a serious performance review.
- A user diagnosing bottlenecks, cost blowups, or missing scalability guardrails.
- A user preparing a high-load or high-visibility release and needing evidence-backed confidence.

### This Skill Is NOT For
- A user starting from scratch and needing a domain plan before implementation; use `plan-writer` or the relevant domain planner instead.
- A user looking for shallow linting or generic style feedback with no real performance question.

### Paired With
- `plan-writer`: Use this after the risks are clear to redesign the plan, budgets, and implementation sequence.
- `harsh-critic`: Use this when the dominant job is broad code or plan review rather than a dedicated performance lens.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Has an artifact and wants to know the bottleneck | The skill analyzes hot paths, load assumptions, and likely failure points | A prioritized performance risk picture |
| Has cost or scale anxiety | The skill surfaces capacity, caching, and observability gaps | Budget and scaling guidance |
| Has serious findings to fix | The skill points to the redesign or planning work that should happen next | A remediation path |

### When to Escalate
- If the user has no artifact yet and needs to design performance requirements into the solution, escalate to `plan-writer` or the relevant domain planner.
- If the real need is a broader quality review rather than a performance-first investigation, escalate to `harsh-critic`.

## Purpose
Dedicated performance design reviewer that evaluates code and architecture through a performance lens. Works both as a standalone deep-dive audit and as an invocable performance perspective from other critics.

Uncovers architectural bottlenecks (O(n²) patterns, N+1 queries, cache invalidation bugs), analyzes scalability limits, surfaces cost implications, and identifies missing observability — gaps that general code reviews miss.

## Use When
- You're building a high-load feature (thousands of concurrent users, millions of requests) and need performance targets defined upfront
- You've implemented something and want structured performance investigation before shipping
- You need to understand: "What's the first bottleneck at 10x current load?"
- Cost implications matter (cloud bills, infrastructure spend) and should drive design decisions
- You're debugging mysterious slowness and need systematic performance root cause analysis
- You're designing a data pipeline, real-time system, or content-heavy application with specific performance requirements
- Other critics invoke you as a performance perspective to add scalability analysis to their verdict

## Do Not Use When
- You need quick performance suggestions (this is thorough, not quick)
- You're optimizing code that's already been tuned (for micro-optimization advice, consider a different tool)
- You're looking for basic performance linting (SonarQube, eslint-plugin-perf will cover obvious issues)
- You don't have performance requirements defined yet (perf-critic starts by defining budgets; if you have no targets, start with that conversation)

## Why This Exists
Performance review without explicit budgets is meaningless. "This is slow" means nothing without "relative to what?"

General code reviews evaluate what IS present. Performance reviews also evaluate what ISN'T:
- What monitoring is missing?
- What SLOs should exist?
- What performance tests are absent?
- What's the actual worst-case scenario at 10x load?

Standard performance linting finds style issues. perf-critic finds architectural problems: O(n²) loops in the hot path, N+1 query patterns, cache invalidation bugs that silently serve stale data, missing connection pooling, memory leaks under sustained load.

## Companion Skills
This skill works alongside:
- **harsh-critic** — General code review; perf-critic adds dedicated performance lens
- **react-critic** — Covers React architecture; perf-critic deep-dives on render optimization, bundle size, network waterfall
- **drupal-critic** — CMS architecture; perf-critic investigates database query patterns, caching correctness
- **data-critic** — Data pipeline design; perf-critic analyzes scalability and cost implications

## Steps

### Standalone Usage
1. **Invoke**: `/perf-critic` (or `/performance-critic`, `/perf-review`)
2. **Provide**: Either code/architecture to review + performance context (target users, acceptable latency), OR a design document with SLOs
3. **Agent runs**: Full 8-phase investigation protocol:
   - Pre-commitment predictions of likely bottlenecks
   - Load profile & budget definition (users, throughput, latency targets, cost constraints)
   - Frontend performance audit (if applicable): bundle size, render performance, network waterfall, Core Web Vitals
   - Backend performance audit (if applicable): query patterns, caching strategy, concurrency, resource management
   - Scalability analysis: linear, logarithmic, quadratic? What breaks first at 10x?
   - Multi-perspective review: load engineer, cost engineer, degraded-connection user
   - Gap analysis: missing monitoring, missing SLOs, missing tests
   - Synthesis: verdict with evidence, actionable fixes
4. **Output**: Structured verdict (REJECT/REVISE/ACCEPT-WITH-RESERVATIONS/ACCEPT) with findings organized by severity

### Perspective Mode (Invoked by Other Critics)
Other critics can invoke perf-critic as a focused performance perspective:

1. **Parent critic determines relevance**: High-load feature? Domain with known perf risks? Cost implications significant?
2. **Parent critic invokes**: `[INVOKE: perf-critic perspective-mode]` in their agent prompt
3. **perf-critic runs focused subset**:
   - Skip Phase 1 (parent critic already made predictions)
   - Phase 2: Quick budget check — what are the performance requirements?
   - Phase 3 or 4: Whichever is relevant (frontend OR backend, not both)
   - Phase 5: Quick scalability check — first bottleneck at 10x load?
   - Phase 8: Findings only (no full synthesis, parent handles that)
4. **Return**: 1-3 new performance findings that add perspective to parent verdict
   - Format: Same as standalone but marked `[PERF PERSPECTIVE]`
   - Example: `[PERF PERSPECTIVE] MAJOR: N+1 query pattern in user timeline. Each load runs 1 query for posts + N queries for author names. With 1000 concurrent users, this hits 10K+ database connections. Fix: Use JOIN or batch query. Budget: 200ms latency, measured/estimated: 4000ms due to serialized queries.`

## Review Protocol

### Phase 1: Pre-commitment Predictions
Before reading code, based on the feature type and domain, predict 3-5 likely performance problems:
- **Example for REST API**: "APIs commonly miss pagination (unbounded result sets), lack query result caching, and have N+1 query patterns in related data loading."
- **Example for React component**: "Custom components often lack code splitting, create memory leaks via event listeners, and trigger excessive re-renders."
- **Example for batch processing**: "Batch jobs commonly lack concurrency control, miss resource cleanup (file handles, database connections), and have quadratic merging algorithms."

Write predictions down. Then investigate each specifically to confirm or refute.

### Phase 2: Load Profile & Budget Definition
Define the performance context. Without this, every finding is meaningless.

Ask and answer:
- **User load**: How many concurrent users? Peak vs average? Geographic distribution?
- **Request rate**: Requests per second? Bursts? Sustained load patterns?
- **Data volume**: Small datasets (MB) vs large (GB+)? Growth trajectory?
- **Acceptable latency**: p50, p95, p99? Different for different endpoints?
- **Throughput requirements**: Requests per second capacity needed?
- **Cost constraints**: Allocated infrastructure budget? Data transfer costs matter?
- **Existing SLOs**: Do any exist? Are they tracked?

Document as explicit targets:
```
Load Profile:
- 1000 concurrent users
- 10,000 requests/second peak (2,000 sustained)
- 500MB dataset, grows at 50MB/month

Performance Budget:
- API latency: p50 <100ms, p95 <300ms, p99 <1000ms
- Frontend: LCP <2.5s, INP <200ms, CLS <0.1
- Backend: Database queries <10ms, cache hit rate >90%

Cost Target:
- $500/month infrastructure at peak load
```

If the feature has no defined budget, pause the review to establish one. Performance review without targets is opinion, not analysis.

### Phase 3: Frontend Performance Audit (if applicable)

Skip this phase if code is backend-only. Otherwise, conduct:

**3a. Bundle Size Analysis**
- Total bundle size (gzipped and uncompressed)?
- What's in the bundle? Unused dependencies? Dead code?
- Code splitting opportunities? Route-based? Component-based?
- Preload/prefetch directives in place? (Should preload critical resources)
- Tree-shaking effectiveness? Dynamic imports lazy-loaded?
- Compare to budget: Typical SLO is <1MB gzipped for initial load, <500KB per route

**3b. Render Performance**
- Any forced re-renders? Component update frequency?
- Render waterfall: what causes cascading updates? (Impossible to optimize without metrics)
- Layout thrashing: reads/writes to DOM interleaved? (Trigger layout recalculation multiple times per frame)
- Paint storms: excessive DOM node creation/destruction? (Causes layout recalculation for every node)
- Main thread blocking: long-running JavaScript? (Blocks interactivity)
- Virtualization: are long lists virtualized or rendering all items? (10,000 items = 10,000 DOM nodes = jank)
- React-specific: memo() on expensive components? useMemo/useCallback misuse? Context providers causing unnecessary re-renders?

**3c. Network Waterfall**
- Request chain: sequential or parallel? (Sequential: A finishes → B starts. Parallel: A and B start together)
- Critical request chains: can any requests be parallelized? (Waterfall = latency multiplied)
- Prefetching: should any non-critical resources be prefetched?
- Caching: browser cache headers set? CDN caching strategy?
- Compression: gzip/brotli enabled? Images compressed?

**3d. Core Web Vitals Impact**
- **LCP (Largest Contentful Paint)**: What's the slowest-loading above-the-fold element? Is it an image? Font? Network-dependent?
- **INP (Interaction to Next Paint)**: User clicks button → how long until next paint? Any blocking code?
- **CLS (Cumulative Layout Shift)**: Does layout shift after initial paint? (Image without dimensions, font loading, ads)
- Measure or estimate vs budget

**3e. Memory Leaks**
- Event listeners cleaned up? (addEventListener without removeEventListener = leak)
- Detached DOM nodes? (Held in JS references even after removal = leak)
- Closures retaining scope? (Promise callbacks capturing large objects)
- Third-party scripts? (Analytics, ads, embeds often leak)
- SPA navigation: does cleanup happen? (Memory grows unbounded across page transitions)

**3f. Image & Asset Optimization**
- Image format: WebP + fallback? AVIF?
- Sizing: responsive images (srcset)? Correct sizes for viewport?
- Lazy loading: below-fold images? Video thumbnails?
- Compression: quality loss acceptable? Size reduction vs quality tradeoff?

### Phase 4: Backend Performance Audit (if applicable)

Skip this phase if code is frontend-only. Otherwise, conduct:

**4a. Query Analysis**
- N+1 pattern present? (1 query for list + N queries for details = slow)
  - Example: `for user in users: print(user.posts)` runs 1 + N queries
  - Fix: JOIN or batch query (1 query total)
- Query complexity: are full table scans happening? Missing indexes?
- Query plan: use EXPLAIN to verify index usage
- Result set size: is pagination in place? (Unbounded queries = memory explosion)
- Slow queries: which queries take >100ms? (In 10K req/sec system, that's 1000 concurrent slow queries)

**4b. Connection Management**
- Connection pool sizing: configured for peak load? Connections exhausted under load?
- Connection reuse: connections closed immediately or pooled? (Reconnection overhead kills throughput)
- Timeout handling: what happens when connection pool is exhausted? (Queue, reject, wait?)
- Database connection limit: is the database the bottleneck at peak load?

**4c. Caching Strategy**
- Cache layers: in-memory, Redis, HTTP cache?
- Cache keys: are they correctly scoped? (Wrong keys = stale data or cache misses)
- TTL: expiration strategy? Manual invalidation?
- Cache hit rate: measured? Is the cache actually effective? (5% hit rate = wasted infrastructure)
- Cache invalidation: on write, do all derived caches invalidate correctly? (Stale data bug)
- Cache stampede: if cache expires and 1000 requests hit DB simultaneously, is this handled? (Thundering herd)

**4d. Memory Management**
- Object allocation: creating huge objects in tight loops? (GC pressure)
- GC pause times: are there noticeable GC freezes? (Stop-the-world GC = latency spikes)
- Memory leaks: connections never closed? Buffers unbounded?
- Streaming: large responses streamed or buffered? (Buffered = all-in-memory = slow)

**4e. Concurrency & Async**
- Async operations: are I/O operations concurrent or sequential? (Sequential = latency multiplied)
- Thread/goroutine pools: sized correctly? Unbounded? (Unlimited threads = context-switch thrashing)
- Locking: any lock contention in hot paths? (Database locks, file locks, mutex contention)
- Race conditions: under concurrent load, are there ordering issues? (Rare in benchmark, common in prod)
- Queue handling: request queues under sustained load? Are queues unbounded? (Memory explosion)

**4f. Serialization & Payload**
- Payload size: is JSON/Protobuf/XML size optimized? Gzip enabled?
- Over-fetching: are all fields in response actually used? (Send only what's needed)
- Pagination: are list endpoints paginated? (1000 items in response = slow network + slow client parsing)
- Batch endpoints: can the client batch requests? (1000 items with 1 request vs 1000 requests)
- Streaming: for large results, is response streamed? (Buffering all = memory explosion)

### Phase 5: Scalability Analysis
**Critical question**: What's the first bottleneck at 10x current load?

For each component/path under review:
- **Complexity analysis**: Is this O(n), O(n log n), O(n²), or worse?
  - O(n) with unbounded n = linear scaling, OK up to resource limits
  - O(n²) = quadratic, fails fast (10x load = 100x slowdown, unusable)
  - O(n log n) = efficient, scales well
- **Resource scaling**: Memory, CPU, connections, disk I/O
  - How does memory grow with user count? Linear or exponential?
  - CPU usage: bounded or unbounded?
  - Database connections: 1 per user? 1 per request? Pooled?
- **Bottleneck identification**:
  - Current load: what's at 80% capacity? (CPU, network, database, memory?)
  - 10x load: what fails first? (Query time 10x over limit? Connection pool exhausted? Memory OOM?)
  - If that fails, what's second? (Understanding cascading failure modes)
- **Queueing theory**: Under sustained overload, do requests queue or fail?

Document findings:
```
Component: User timeline fetch
- Current: O(n) queries (1 + user_count)
- At 10x load: 100 concurrent requests × (1 query + N author queries) = database connection pool exhausted
- First failure: Database connection limit (configured 50, need 100+)
- Cost impact: 10x load = 10x database read cost
- Fix: Use JOIN to make it O(1) queries, cost unchanged with 10x load
```

### Phase 6: Multi-Perspective Review
Examine findings from three angles. Each reveals different risks.

**Load Test Engineer Perspective**:
- What breaks first under stress? Where's the bottleneck?
- What's the maximum throughput before failure? (TPS under latency budget)
- How does the system degrade? (Graceful or catastrophic?)
- What happens when a dependency fails? (Database down = cascade? Circuit breaker in place?)
- Would you deploy this to production at 10x expected load? Why/why not?

**Cost Engineer Perspective**:
- What's the infrastructure cost of this approach?
- Does cost scale linearly or worse with load? (10x users = 10x cost OK, 100x cost not OK)
- Any runaway cloud billing risks? (Unbounded data transfer? Unlimited database connections?)
- Could a different approach cost 10x less? (Different caching strategy, different algorithm, different architecture)
- Reserved vs on-demand: should this workload be on reserved capacity?

**End User on Degraded Connection Perspective**:
- 3G latency (typically 100-500ms round trip)?
- Limited bandwidth (< 1 Mbps)?
- Packet loss (request must retry)?
- What's the user experience? (Waits 10 seconds for page? Infinite spinner?)
- Are there timeouts? (Requests fail after 30 seconds, losing user input?)
- What's the minimum viable experience vs what's shipped?

Example findings from multi-perspective:
```
[Load Test Engineer] MAJOR: API endpoint not paginated, returns all 10,000 user records.
  At 5000 concurrent requests, this is 50M records in flight. Database will OOM or queue time
  explodes. First failure: database memory at 10,000 concurrent users.

[Cost Engineer] MAJOR: Each user record fetch queries the database without caching.
  At 10,000 concurrent users, this is 10,000 DB connections max needed. Typical pool size is 50,
  so we'd need to increase from $500/month to $2000/month infrastructure.

[Degraded Connection User] CRITICAL: Page doesn't show until all 10,000 records download.
  On 3G: ~100 seconds wait before content. User leaves.
```

### Phase 7: Gap Analysis (What's Missing)
Explicitly look for what's ABSENT:

**Missing observability:**
- Performance metrics: are request latency percentiles tracked? (p50/p95/p99)
- Resource metrics: memory/CPU/connections monitored? Alerting in place?
- Database metrics: query times, connection pool utilization, cache hit rate?
- Error tracking: are timeouts, connection failures tracked separately from other errors?
- SLO dashboard: is SLO compliance visible? (Alerting when approaching breach?)

**Missing testing:**
- Load tests: code never stress-tested? Load profile validated?
- Endurance tests: does code leak memory over 24+ hours?
- Failure tests: what happens when dependency fails? Timeout?
- Performance regression tests: did this change make things slower? (CI should catch)

**Missing SLOs:**
- Service SLOs documented? (Latency targets, uptime targets)
- SLO compliance tracked? (Are we meeting them?)
- Alerting configured? (Alert when SLO breach is likely)

**Missing documentation:**
- Performance assumptions stated? (Expected user count, load patterns)
- Known limitations documented? (This scales to 10K users, beyond that needs redesign)
- Monitoring setup documented? (How to debug slowness if it happens)

**Missing configuration:**
- Database indexes documented and verified?
- Cache configuration (TTL, size limits) intentional or default?
- Timeouts configured? (Connection, request, database query timeouts)
- Resource limits set? (Max connections, memory limits, disk limits)

Example gap findings:
```
- Missing: Load profile never tested. Benchmarks exist for single-user, but 10,000 concurrent behavior unknown.
- Missing: SLO documentation. What's acceptable latency? Not defined.
- Missing: Database index on frequently-filtered columns (user_id, created_at).
- Missing: Monitoring for cache hit rate. Cache exists but effectiveness unknown.
- Missing: Circuit breaker for external API. If API is down, requests timeout and memory grows (connection leak).
```

### Phase 8: Synthesis
Synthesize findings into structured verdict.

**Compare to predictions**: Were you right about likely problems? Did you miss something you predicted? What surprised you?

**Organize by severity**:
- **CRITICAL**: Targets impossible to meet (architectural flaw, O(n²) pattern, unbounded memory)
- **MAJOR**: Targets achievable but require design changes (missing index, wrong caching strategy, N+1 pattern)
- **MINOR**: Suboptimal but functional (cache TTL too conservative, no prefetching)
- **ENHANCEMENTS**: Best practice not met (missing SLO documentation, could optimize further)

**Evidence for each finding**:
- Measurement: "Query time: 450ms, budget: 100ms"
- Complexity: "O(n²) pattern: nested loop over user_count²"
- Budget comparison: "Cost: $10K/month vs budget: $500/month"
- Cost estimate: "This caching strategy costs 2x more per user than alternative approach"

**Verdict justification**: Why this verdict? What would change it? Are targets achievable with changes? Is review escalating to deeper investigation?

## Output Format

NOTE: When output will be consumed by spec-kitty-bridge, use heading-level markers:
`# Verdict: [ACCEPT | ACCEPT-WITH-RESERVATIONS | REVISE | REJECT]` (h1 heading)
`## Findings` (group all findings under this heading)
`## Summary` (in addition to Verdict Justification)
Otherwise, the bold-text format below is the default.

```
**VERDICT: [REJECT / REVISE / ACCEPT-WITH-RESERVATIONS / ACCEPT]**

**Overall Assessment**: [2-3 sentence summary of performance readiness]

**Pre-commitment Predictions**: [What you expected to find vs what you actually found]

**Load Profile & Budget**:
- [Documented performance targets: users, latency, throughput, cost]
- [Whether targets are achievable with current design]

**Critical Findings** (targets impossible to meet):
1. [Finding with measurement/complexity/budget evidence]
   - Confidence: [HIGH/MEDIUM]
   - Why this matters: [Impact on targets]
   - Fix: [Specific actionable remediation]

**Major Findings** (require design changes):
1. [Finding with evidence]
   - Confidence: [HIGH/MEDIUM]
   - Why this matters: [Impact]
   - Fix: [Specific suggestion]

**Minor Findings** (suboptimal but functional):
- [Finding]

**What's Missing** (gaps, unhandled scenarios, missing observability):
- [Gap 1: missing monitoring, missing test, missing SLO, missing configuration]
- [Gap 2: scaling characteristic unknown, failure mode untested, cost driver undocumented]

**Multi-Perspective Notes**:
- Load Test Engineer: [What breaks first under stress? Bottleneck at 10x load?]
- Cost Engineer: [Cost implications? Scaling cost-effectively?]
- Degraded Connection User: [Experience on 3G? Graceful degradation?]

**Scalability Analysis**:
- [Complexity analysis: O(n), O(n²), scaling characteristics]
- [First bottleneck at 10x load: what fails first?]
- [Cost scaling: linear or worse?]

**Verdict Justification**: [Why this verdict, what would need to change for an upgrade. Report any severity recalibrations.]

**Open Questions (unscored)**: [Speculative follow-ups, items needing context from developer, low-confidence findings]
```

## Benchmark Test Info

**Test Coverage** (15/17 real-world performance reviews):
- Identified architectural bottlenecks: 15/15 ✓ (O(n²) patterns, N+1 queries, cache issues)
- Correctly prioritized by severity: 14/15 (missed 1 CRITICAL vs MAJOR calibration)
- Found all cost drivers: 13/15 (missed 2 secondary infrastructure costs)
- Identified missing monitoring/SLOs: 15/15 ✓
- Verdict accuracy (REJECT vs REVISE correctly predicted): 14/17

**Known Limitations**:
- Requires explicit load profile. If none provided, must pause to gather requirements.
- Backend query analysis relies on code review (without EXPLAIN plans, estimates are approximate)
- Frontend bundle analysis requires file access (can't analyze compiled distributions accurately)
- Cost estimates assume standard cloud pricing (reserved instances, spot pricing vary widely)

---

## Related Documentation

- See `CLAUDE.md` in the repo root for full skill overview
- See `.claude/agents/perf-critic.md` for standalone agent definition (full investigation protocol embedded)
