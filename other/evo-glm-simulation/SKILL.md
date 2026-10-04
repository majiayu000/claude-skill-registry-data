---
name: evo-glm-simulation
description: Run the General Lake Model (GLM v3) for Lake Mendota — edit glm3.nml, execute the GLM binary, parse NetCDF output (depth = z_surface - z_layer), match to field observations, compute RMSE, and iteratively calibrate Kw, sw_factor, wind_factor, coef_mix_hyp to achieve RMSE < 2°C.
---

# evo-glm-simulation

End-to-end workflow for running and calibrating GLM for Lake Mendota.

## Directory contract
- `/root/glm3.nml` — namelist (working dir is `/root/`)
- `/root/bcs/*.csv` — meteo, inflow (yahara, pheasant), outflow
- `/root/field_temp_oxy.csv` — field obs (columns: datetime, depth, temp, OXY_oxy)
- `/root/output/output.nc` — required output

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-glm-simulation/scripts')
from utils import (read_glm_nml, update_glm_nml, verify_bcs, run_glm,
                   process_glm_netcdf, load_field_observations,
                   calculate_rmse, calibrate_parameters)

# 1) Verify boundary files
assert verify_bcs() == []

# 2) Run GLM once
ok, so, se = run_glm('/root/')

# 3) Read NetCDF & compute RMSE
sim = process_glm_netcdf('/root/output/output.nc')
obs = load_field_observations('/root/field_temp_oxy.csv')
rmse, n = calculate_rmse(sim, obs)

# 4) Calibrate to RMSE < 2.0
best, history = calibrate_parameters(target_rmse=1.95, max_iters=30)
```

## Key concepts

**Depth conversion**: GLM `z` is height-from-bottom. Convert with
`depth = z_layer_top_max - z_layer`. Use dynamic z_surface per timestep
(max layer height at that timestep) rather than static `lake_depth`.

**NS variable**: number of active layers at each timestep — slice arrays
to `[:NS[t]]` to drop padded/masked entries.

**Time units**: GLM NetCDF time uses `hours since <start>` — parse from
the variable's `units` attribute (fallback: 2009-01-01 12:00:00).

**RMSE matching**: GLM saves daily (nsave=24); group obs by date, build
a 1D interpolator over sim depths, look up obs depth, compute RMSE on
matched (obs, sim) pairs.

## Calibration levers (Mendota)

| Param | Block | Range | Notes |
|---|---|---|---|
| `Kw` | `&light` | 0.3–0.6 | Higher = darker water, cooler deep |
| `sw_factor` | `&meteorology` | 0.9–1.05 | Shortwave scaling |
| `wind_factor` | `&meteorology` | 0.9–1.1 | Surface mixing |
| `coef_mix_hyp` | `&mixing` | 0.3–0.7 | Deep mixing |

Default baseline gives ~2.01 °C RMSE for Mendota; a small grid search
typically lands in 1.4–1.9 °C.

## Pitfalls
- DO NOT use `lake_depth` (25 m) statically — surface fluctuates. Use
  per-timestep `z_surface = z[t,:NS[t]].max()`.
- `f90nml.write(...,force=True)` then atomic replace to avoid partial writes.
- GLM aborts if `start`/`stop` lie outside meteo file range.
- The skill assumes GLM binary `glm` is on PATH.
