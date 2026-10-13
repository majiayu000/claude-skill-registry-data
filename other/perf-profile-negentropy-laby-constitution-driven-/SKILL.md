---
name: perf-profile
description: "Structured performance profiling workflow. Identifies bottlenecks, measures against budgets, and generates optimization recommendations with priority rankings. Game: CPU/GPU/frame-time. Product: API latency, DB queries, memory, throughput."
argument-hint: "[system-name or 'full']"
user-invocable: true
agent: performance-analyst
allowed-tools: Read, Glob, Grep, Bash
---

## User Guide

- When to use: Structured performance profiling workflow. Identifies bottlenecks, measures against budgets, and generates optimization recommendations with priority rankings. Game: CPU/GPU/frame-time. Product: API latency, DB queries, memory, throughput.
- Inputs: Command arguments: `/perf-profile [system-name or 'full']`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Detection

**Required Read before domain-dependent routing:** read `CLAUDE.md` and
`standards/technical-preferences.md`, the existing explicit domain decision for
the current scope, and any existing `design/cdd/game-concept.md` or
`design/cdd/product-concept.md` bodies. Read actual configuration before deciding
what the absence of a concept means. Filenames, copied templates, placeholders
and shared file extensions do not establish a domain.

In technical preferences, read populated legacy Product sections as valid aliases:
`Language & Framework` supplies language/framework/runtime choices;
`Platform & Deployment` supplies targets/deployment; `Agent Routing`, including
its `File Extension Routing`, supplies specialist routing in its owning domain.
Compare their actual values with `Product Stack` and applicable concept/decision
evidence. A missing parallel section does not erase valid configured facts or
require relocating them. Conflicting values block the affected route.

Classify the current scope after these reads:

- **Game**: consistent substantive Game concept/decision evidence, or actual
  configured engine/domain plus Game behavior evidence, supports `[Game]` paths.
- **Product**: consistent substantive Product concept/decision evidence or actual
  configured Product facts supports `[Product]` paths. Populated legacy
  TypeScript/Bun API/CLI targets and Product specialist routing, for example,
  remain Product without a concept or a new `Product Stack` section.
- **Unknown**: evidence is insufficient, conflicting or mixed without a concrete
  governing scope. Resolve Game or Product using an existing scoped decision or
  confirmation from the user/configured project lead before dependent branches.
  Both concept filenames do not select a branch; independent neutral reporting
  continues while the affected domain-specific work waits.

Record the chosen domain and the actual source sections/values supporting it.
Never silently default to Game. Missing/inaccessible required configuration or
branch inputs leaves the affected check Incomplete; domain selection alone does
not prove runtime availability, test execution, readiness or completion.

---

## Phase 1: Determine Scope

Read the argument:

- System name → focus profiling on that specific system
- `full` → run a comprehensive profile across all systems

---

## Phase 2: Load Performance Budgets

Check for existing performance targets in design docs or CLAUDE.md.

**[Game]** Performance budgets:
- Target FPS (e.g., 60fps = 16.67ms frame budget)
- Memory budget (total and per-system)
- Load time targets
- Draw call budgets
- Network bandwidth limits (if multiplayer)

**[Product]** Performance budgets:
- API latency (p50/p95/p99 targets)
- Memory budget (total and per-service)
- Cold start time target
- Throughput (requests/sec, events/sec)
- Database query time budget
- Network bandwidth limits (if applicable)

---

## Phase 3: Analyze Codebase

### [Game] Game Profiling Targets

**CPU Profiling Targets:**
- `_process()` / `Update()` / `Tick()` functions — list all and estimate cost
- Nested loops over large collections
- String operations in hot paths
- Allocation patterns in per-frame code
- Unoptimized search/sort over game entities
- Expensive physics queries (raycasts, overlaps) every frame

**Memory Profiling Targets:**
- Large data structures and their growth patterns
- Texture/asset memory footprint estimates
- Object pool vs instantiate/destroy patterns
- Leaked references (objects that should be freed but aren't)
- Cache sizes and eviction policies

**Rendering Targets (if applicable):**
- Draw call estimates
- Overdraw from overlapping transparent objects
- Shader complexity
- Unoptimized particle systems
- Missing LODs or occlusion culling

**I/O Targets:**
- Save/load performance
- Asset loading patterns (sync vs async)
- Network message frequency and size

### [Product] Product Profiling Targets

**API Profiling Targets:**
- Endpoint handlers — list all and estimate latency
- Middleware chain cost (auth, logging, validation)
- Serialization/deserialization overhead (JSON, protobuf)
- N+1 query patterns in request handlers
- Unbounded result sets (missing pagination)

**Database Profiling Targets:**
- Missing indexes on query WHERE/JOIN columns
- Slow queries (full table scans, unoptimized joins)
- Connection pool utilization and wait time
- Transaction scope (too broad = lock contention)

**Memory Profiling Targets:**
- Large in-memory caches without eviction policies
- Unbounded collections (growing lists, maps)
- Memory retained across requests (stateful singletons)
- Leaked connections (database, HTTP, message queue)

**I/O Targets:**
- Blocking I/O on async/event-loop threads
- File read/write patterns (buffer sizes, streaming vs full load)
- Network call timeout and retry configuration
- Third-party API call latency and failure modes

---

## Phase 4: Generate Profiling Report

### [Game] Game Profiling Report

```markdown
## Performance Profile: [System or Full]
Generated: [Date]

### Performance Budgets
| Metric | Budget | Estimated Current | Status |
|--------|--------|-------------------|--------|
| Frame time | [16.67ms] | [estimate] | [OK/WARNING/OVER] |
| Memory | [target] | [estimate] | [OK/WARNING/OVER] |
| Load time | [target] | [estimate] | [OK/WARNING/OVER] |
| Draw calls | [target] | [estimate] | [OK/WARNING/OVER] |

### Hotspots Identified
| # | Location | Issue | Estimated Impact | Fix Effort |
|---|----------|-------|------------------|------------|

### Optimization Recommendations (Priority Order)
1. **[Title]** — [Description]
   - Location: [file:line]
   - Expected gain: [estimate]
   - Risk: [Low/Med/High]
   - Approach: [How to implement]

### Quick Wins (< 1 hour each)
- [Simple optimization 1]

### Requires Investigation
- [Area that needs actual runtime profiling to confirm impact]
```

### [Product] Product Profiling Report

```markdown
## Performance Profile: [System or Full]
Generated: [Date]

### Performance Budgets
| Metric | Budget | Estimated Current | Status |
|--------|--------|-------------------|--------|
| API latency (p95) | [target] | [estimate] | [OK/WARNING/OVER] |
| Memory (RSS) | [target] | [estimate] | [OK/WARNING/OVER] |
| Cold start | [target] | [estimate] | [OK/WARNING/OVER] |
| Throughput | [target] | [estimate] | [OK/WARNING/OVER] |
| DB query time (p95) | [target] | [estimate] | [OK/WARNING/OVER] |

### Hotspots Identified
| # | Location | Issue | Estimated Impact | Fix Effort |
|---|----------|-------|------------------|------------|

### Optimization Recommendations (Priority Order)
1. **[Title]** — [Description]
   - Location: [file:line]
   - Expected gain: [estimate]
   - Risk: [Low/Med/High]
   - Approach: [How to implement]

### Quick Wins (< 1 hour each)
- [Simple optimization 1]

### Requires Investigation
- [Area that needs actual runtime profiling to confirm impact]
```

Output the report with a summary: top 3 hotspots, estimated headroom vs budget, and recommended next action.

---

## Phase 5: Scope and Timeline Decision

Activate this phase only if any hotspot has Fix Effort rated M or L.

Present significant-effort items and ask the user to choose for each:

- **A) Implement the optimization** (proceed with fix now or schedule it)
- **B) Reduce feature scope** (run `/scope-check [feature]` to analyze trade-offs)
- **C) Accept the performance hit and defer to Polish phase** (log as known issue)
- **D) Escalate to technical-director for an architectural decision** (run `/architecture-decision`)

**[Game]** If multiple items are deferred to Polish (choice C), record them under `### Deferred to Polish`.
**[Product]** If multiple items are deferred (choice C), record them under `### Deferred Performance Items`.

This skill is read-only — no files are written. Verdict: **COMPLETE** — performance profile generated.

---

## Phase 6: Next Steps

- If bottlenecks require architectural change: run `/architecture-decision`.
- If scope reduction is needed: run `/scope-check [feature]`.
- To schedule optimizations: run `/sprint-plan update`.

### Rules
- Never optimize without measuring first — gut feelings about performance are unreliable
- Recommendations must include estimated impact — "make it faster" is not actionable
- **[Game]** Profile on target hardware, not just development machines
- **[Product]** Profile under realistic load, not just single-request benchmarks
- Static analysis (this skill) identifies candidates; runtime profiling confirms
