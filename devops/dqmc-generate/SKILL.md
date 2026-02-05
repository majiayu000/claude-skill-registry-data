---
name: dqmc-generate
description: Create HDF5 simulation files for DQMC with specified physical parameters. Use when setting up new simulations, specifying lattice size, interaction strength U, chemical potential mu, temperature (via dt and L), or number of Monte Carlo sweeps.
---

# Generate Simulation Files

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `Nx`, `Ny` | No | 8 | Lattice dimensions |
| `U` | No | 6.0 | On-site interaction strength |
| `mu` | No | 0.0 | Chemical potential |
| `tp` | No | 0.0 | Next-nearest neighbor hopping |
| `dt` | No | 0.1 | Imaginary time step |
| `L` | No | 40 | Number of time slices (beta = L*dt) |
| `n_sweep_warm` | No | 200 | Warmup sweeps |
| `n_sweep_meas` | No | 2000 | Measurement sweeps |
| `Nfiles` | No | 1 | Number of independent bins |
| `prefix` | No | `sim` | Output path prefix |
| `period_uneqlt` | No | 0 | Unequal-time period (0=disabled) |

## Outputs

- `{prefix}_0.h5`, `{prefix}_1.h5`, ... - HDF5 simulation files
- `{prefix}.h5.params` - common params HDF5 file

## Procedure

**Option A: CLI (simple cases)**
```bash
dqmc-util gen Nx=6 Ny=6 U=4.0 mu=0.0 dt=0.1 L=50 Nfiles=4 prefix=data/run/bin
```

**Option B: Python (parameter scans)**
```python
from dqmc_util import gen_1band_hub

gen_1band_hub.create_batch(
    prefix="data/run/bin", Nfiles=4,
    Nx=6, Ny=6, U=4.0, mu=0.0, tp=0.0, dt=0.1, L=50
)
```

**Choosing dt and L for a target temperature T:**
```python
import numpy as np
T = 0.25  # target temperature
U = 4.0
beta = 1.0 / T
dt = min((0.05/U)**0.5, beta / 10)  # Trotter error constraint
L = int(np.ceil(beta / dt / 5) * 5)  # L must be divisible by n_matmul and period_eqlt (defaults: 5)
dt = beta / L  # recalculate exact dt
```

## Validation

- [ ] Files created: `ls {prefix}_*.h5 {prefix}.h5.params`
- [ ] Trotter error check: `U * dt^2 <= 0.05`

## Failure Modes

| Symptom | Cause | Recovery |
|---------|-------|----------|
| "File exists" error | Previous files not cleaned | Remove old files or use overwrite=1 argument |
| ValueError: L must be divisible ... | L must be multiple of n_matmul and period_eqlt | Adjust value of L and dt, keeping their product (beta) constant |

## Do Not

- Overwrite existing simulation files without confirmation
- Ignore the Trotter error bound (`U * dt^2 <= 0.05`)
