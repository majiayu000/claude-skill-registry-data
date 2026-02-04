---
name: dqmc-advanced
description: Advanced DQMC features including unequal-time measurements, analytic continuation, and queue system internals. Use when enabling dynamical correlations, performing MaxEnt continuation, or understanding HDF5 data structure.
---

# Advanced Topics

## Unequal-Time Measurements

Enable by setting `period_uneqlt > 0` during file generation:

```bash
dqmc-util gen period_uneqlt=8 ...
```

Required for:
- `nnrw0`, `zzrw0` - Zero-frequency susceptibilities
- `dwq0t` - D-wave pair susceptibility
- Any time-dependent correlation functions

**Note:** Unequal-time measurements significantly increase runtime and memory usage.

## Analytic Continuation

Use maximum entropy for continuing imaginary-time data to real frequencies:

```python
from dqmc_util import maxent

# Solve G = K A given:
# - G: binned data, shape (nbin, ntau)
# - K: kernel, shape (ntau, nw)
# - m: default model, shape (nw,)
A_omega = maxent.calc_A(G, K, m)
```

## HDF5 File Structure

```
/metadata/     # Model info (mu, Nx, Ny, beta)
/params/       # Simulation parameters, precomputed matrices
/state/        # RNG state, sweep number, aux field config
/meas_eqlt/    # Equal-time measurements (n_sample, sign, den, ...)
/meas_uneqlt/  # Unequal-time measurements (optional)
```

## Queue System Internals

The sharded queue uses:
- 128 shards to avoid lock contention on distributed filesystems
- Atomic `rename()` operations for task claiming
- Symlinks moved: `todo/` -> `running/` -> `done/`
- Checkpointed jobs returned to `todo/` for resumption
