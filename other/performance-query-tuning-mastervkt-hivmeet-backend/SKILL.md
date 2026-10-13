---
name: performance-query-tuning
description: 'Diagnose and optimize backend performance in HIVMeet with query-focused tuning. Use for slow endpoints, N+1 patterns, indexing strategy, pagination cost control, and scalable ORM usage.'
argument-hint: 'Describe slow endpoint/query, observed latency, data volume context, and performance target.'
user-invocable: true
---

# Performance and Query Tuning

## Purpose
Improve backend response time and throughput with low-risk, measurable optimization steps.

## Use When
- Endpoint latency increases
- Database load spikes or timeouts appear
- N+1 query patterns are suspected
- Pagination/filter endpoints degrade under scale

## Mandatory Workflow

### 1. Baseline and Bottleneck Capture
- Measure current latency and query count on representative path
- Identify slow segments (DB, serializer, external calls, async waits)
- Define target metric before changes

### 2. Query Plan Review
- Inspect ORM patterns for N+1
- Apply select_related/prefetch_related where appropriate
- Reduce unnecessary fields and repeated queries

### 3. Endpoint-Level Efficiency
- Ensure deterministic ordering for paginated endpoints
- Enforce sane page_size defaults and limits
- Avoid expensive operations in list loops

### 4. Index and Schema Considerations
- Propose indexes for high-cardinality filters/sorts
- Validate write/read tradeoff before adding indexes
- Include migration impact in optimization plan

### 5. Safe Refactor Strategy
- Prefer small, measurable changes
- Re-measure after each optimization step
- Stop when target is reached or risk outweighs gains

### 6. Validation
- Confirm no behavior/contract regressions
- Confirm reduced query count and improved latency
- Validate unchanged permission and privacy behavior

### 7. Output Contract
1. Baseline metrics
2. Optimization changes and rationale
3. Before/after metrics
4. Tradeoffs and risks
5. Follow-up optimization opportunities

## Quality Gates
- No optimization merged without before/after evidence
- No query tuning that breaks endpoint contract or ordering semantics
- No performance gain accepted if it weakens security/privacy constraints
