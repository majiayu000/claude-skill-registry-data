---
name: performance-benchmarking
description: >
  Use when evaluating, measuring, or comparing the performance of systems, functions,
  or services. This skill provides a framework for establishing baselines, measuring
  performance, and validating that changes meet performance requirements.
---

# Performance Benchmarking

## Overview
This skill defines how to systematically measure and track system performance. Without benchmarks, performance degradation goes unnoticed until it impacts users. Regular benchmarking ensures changes improve rather than degrade performance.

## When to Use
- Before launching any user-facing feature or service
- After making changes that could affect performance (algorithms, data access, queries)
- When users report slowness or degraded responsiveness
- Before committing to a technology or approach with performance implications
- As part of regular system health monitoring
- **Don't use when:** Performance is clearly not a concern (static content, one-time operations)

## Core Procedures

### Step 1: Define Metrics
Select relevant metrics for what's being measured:
- **Response Time:** p50, p90, p95, p99 latencies
- **Throughput:** Requests/operations per second
- **Resource Usage:** CPU, memory, disk I/O, network, database connections
- **Error Rate:** Percentage of failed operations
- **Scalability:** How metrics change as load increases

### Step 2: Establish Baseline
1. Define test scenario (load, data set, environment)
2. Run measurement under normal conditions
3. Record results as baseline
4. Ensure environment is stable and representative of production
5. Document test conditions for reproducibility

### Step 3: Execute Benchmark
1. Run test under defined conditions (same as baseline)
2. Run multiple iterations (minimum 5) for statistical significance
3. Record all metrics and environmental conditions
4. Save raw results for analysis

### Step 4: Compare and Analyze
- Did performance improve, degrade, or stay flat vs baseline?
- Are any metrics outside acceptable thresholds?
- If performance changed, identify WHAT changed (not just THAT it changed)
- For degradation: is the regression acceptable for the improvement gained?

### Step 5: Set Thresholds
Define acceptable ranges for each metric:
```
PERFORMANCE THRESHOLD
=====================
Metric: [response time, throughput, etc.]
Baseline: [typical value]
Warning: [degradation level that triggers investigation]
Critical: [degradation level that triggers rollback]
Target: [improvement goal]
```

## Quality Checklist
- [ ] Relevant metrics selected for system type
- [ ] Baseline established with documented conditions
- [ ] Tests run multiple times for statistical reliability
- [ ] Results compared against baseline
- [ ] Thresholds defined for ongoing monitoring
- [ ] Raw results saved for trend analysis

## Error Handling
- **Error:** Performance degrades significantly after change
  **Response:** Do NOT deploy, diagnose root cause, fix or revert
- **Error:** Results are inconsistent between runs
  **Response:** Investigate environmental factors, isolate variable, stabilize test conditions
- **Error:** No baseline data available
  **Response:** Measure current state as baseline, cannot assess change impact until next measurement

## Cross-Team Integration
**Related Skills:** testing-strategy, edge-case-analysis, incident-response, continuous-improvement
**Used By:** Performance testing engineers, developers, infrastructure teams, load testers, profiler agents