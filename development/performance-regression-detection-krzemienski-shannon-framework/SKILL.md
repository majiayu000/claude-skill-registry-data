---
name: performance-regression-detection
description: |
  Track performance benchmarks and detect regressions exceeding 10% threshold. Analyze historical trends and alert on degradation. Calculate regression score (0.00-1.00) for performance health. Integrate with Serena for continuous monitoring. Use when: monitoring performance, detecting regressions, analyzing performance trends, optimizing slow components, validating performance fixes.

skill-type: MONITORING
shannon-version: ">=5.6.0"

mcp-requirements:
  recommended:
    - name: serena
      purpose: Performance metric tracking, alerting, trend analysis
    - name: benchmark-js
      purpose: JavaScript/TypeScript benchmarking
    - name: criterion
      purpose: Rust benchmarking
    - name: pytest-benchmark
      purpose: Python performance testing

allowed-tools: All
---

# Performance Regression Detection - Quantified Speed

## Purpose

Establish baseline performance metrics, detect regressions >10%, and analyze historical trends. Calculates regression score (0.00-1.00) showing performance health. Integrates with Serena MCP for continuous alerting and trend visualization.

## When to Use

- Detecting performance regressions before deployment
- Tracking performance improvements over time
- Comparing performance across branches
- Identifying slow components needing optimization
- Setting performance SLAs and monitoring compliance
- Alerting on regressions >10% threshold

## Core Metrics

**Regression Score:**
```
Score = Current / Baseline × 1.0 (capped at 1.00)
- 1.00 = same or better than baseline (green)
- 0.95 = 5% slower (acceptable)
- 0.90 = 10% slower (warning threshold)
- 0.80 = 20% slower (critical)
```

**Benchmark Tracking Example:**
```
Component: API Request Handler
├─ Baseline (main): 45ms
├─ Current (feature): 48ms (6.7% slower) → Score: 0.97
├─ Threshold: >50ms regression
├─ Trend: Stable (+0.1% vs last week)
└─ Status: ✅ Pass (within tolerance)

Component: Database Query
├─ Baseline: 120ms
├─ Current: 132ms (10% slower) → Score: 0.90
├─ Trend: +4% slower over 2 weeks (regressing)
└─ Status: ⚠️ Warning (at threshold, monitor)
```

## Workflow

### Phase 1: Baseline Establishment
1. **Establish baseline**: Benchmark main branch performance
2. **Sample size**: Run ≥10 iterations for stability
3. **Record stats**: Store mean, std dev, min, max
4. **Push to Serena**: Create historical baseline

### Phase 2: Continuous Monitoring
1. **Run benchmarks**: On each commit/PR
2. **Compare to baseline**: Calculate regression percentage
3. **Calculate score**: 0.00-1.00 metric
4. **Alert if >10%**: Trigger warning/critical notifications
5. **Push to Serena**: Send metrics for tracking

**Serena Push Format:**
```json
{
  "metric_type": "performance_regression",
  "project": "task-app",
  "component": "api_handler",
  "baseline_ms": 45,
  "current_ms": 48,
  "regression_percent": 6.7,
  "regression_score": 0.97,
  "status": "PASS",
  "timestamp": "2025-11-20T12:00:00Z"
}
```

### Phase 3: Trend Analysis
1. **Track history**: 30-day regression score trend
2. **Detect patterns**: Consistent degradation vs spikes
3. **Correlate with commits**: Identify which changes caused regression
4. **Forecast**: Predict if trends continue
5. **Alert on trajectory**: Flag if regressing >0.02/week

**Trend Analysis Example:**
```
Performance Trend (30 days)
1.00 ┤     ╭─────────────┐
0.95 ┤    ╱               ╲     ↓ Regression detected
0.90 ┤───╱                 ╰──── Commit 3f7d2c added 15% overhead
0.85 ┤                          Optimized in 4f9a1e, back to 0.97
     └────────────────────────
       7d   14d   21d   28d

Action: Optimization identified regressor, restored health
```

## Real-World Impact

**Web Application Response Time:**
- Baseline: 150ms p95
- Regression detected: 170ms (13% slower, score 0.87)
- Serena alert triggered, investigation found N+1 query
- Fixed in 2 hours, restored to 152ms (score 0.99)
- Prevented customer-facing slowdown

**Mobile App Load Time:**
- Tracking 5 key paths (Launch, Login, Dashboard, Search, Checkout)
- Regression detected in Search: 450ms → 540ms (score 0.83)
- Trend analysis showed gradual 2-week degradation
- Root cause: Missing cache invalidation in recent refactor
- Fix deployed, score back to 1.02 (10% faster!)

## Success Criteria

✅ Baseline established for critical paths
✅ Regression score ≥0.90 maintained
✅ Serena alerts fire within 5 min of regression
✅ Historical trend shows improvement or stability
✅ No unexplained spikes >0.05 score variance
✅ All regressions >10% investigated and documented
