---
name: performance
description: Measure and optimize runtime latency, algorithmic efficiency, memory footprints, and bundle size.
---

# Performance Engineering

## Optimization Targets
- **Frontend:** Code splitting, tree shaking, asset compression, avoidance of unnecessary re-renders, bundle size inspection (<500kB chunks).
- **Backend:** Connection pooling, async concurrency, sub-millisecond in-memory lookups, zero redundant I/O.
- **Database:** Query explain plans, index tuning, batch inserts, and selective column projection.
- **ML / Forecasting:** Vectorized NumPy/Pandas operations, lightweight gradient boosted trees or linear baselines, avoiding multi-second inference blocking.
