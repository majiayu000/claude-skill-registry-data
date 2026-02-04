---
name: dqmc-analyze
description: Extract physical observables with error estimates from completed DQMC simulations. Use when computing density, double occupancy, spin correlations, structure factors, or any measured quantity from simulation data.
---

# Analyze Results

## Inputs

- Directory containing `bin_*.h5` files (completed simulations)
- Observable names (see table below)

## Outputs

- Dictionary with parameters and `(mean, stderr)` tuples for each observable

## Procedure

**Basic analysis:**
```python
from dqmc_util import analyze_hub

data = analyze_hub.get("data/run/", "sign", "den", "zzr")

print(f"sign = {data['sign'][0]:.4f} +/- {data['sign'][1]:.4f}")
print(f"density = {data['den'][0]:.4f} +/- {data['den'][1]:.4f}")
```

**Available observables:**

| Name | Description | Requires |
|------|-------------|----------|
| `sign` | Fermion sign | - |
| `den` | Density <n> | - |
| `docc` | Double occupancy <n_up n_down> | - |
| `gr`, `gk` | Green's function (real/k-space) | - |
| `nnr`, `nnq` | Density correlator / structure factor | - |
| `zzr`, `zzq` | Spin-z correlator / structure factor | - |
| `xxr` | Spin-x correlator | - |
| `swq0` | S-wave pair structure factor | - |
| `nnrw0`, `zzrw0` | Zero-freq susceptibilities | `period_uneqlt > 0` |
| `dwq0t` | D-wave pair susceptibility | `period_uneqlt > 0` |

**Collect from multiple directories:**
```python
import os

def collect_results(base_dir, observables):
    results = []
    for subdir in sorted(os.listdir(base_dir)):
        path = os.path.join(base_dir, subdir)
        if os.path.isdir(path):
            try:
                results.append(analyze_hub.get(path + "/", *observables))
            except Exception as e:
                print(f"Skipping {path}: {e}")
    return results
```

**Compute derived quantities:**
```python
# Magnetic moment squared from spin correlator
path = "data/run/"
data = analyze_hub.get(path, "zzr")
mz2 = 4 * data["zzr"][0][0, 0]       # [0] = mean, shape (Ny, Nx)
mz2_err = 4 * data["zzr"][1][0, 0]   # [1] = stderr
```

## Validation

- [ ] Errorbar on sign is significantly less than mean. Otherwise, sign problem is too severe.
- [ ] Errorbars on observable are reasonable (not >> mean)

## Failure Modes

| Symptom | Cause | Recovery |
|---------|-------|----------|
| KeyError for observable | Observable not computed | Check `period_uneqlt` setting |
| "No files found" | Wrong path or no `bin_*.h5` | Verify directory structure |
| Large error bars | Insufficient statistics | Run more sweeps or bins |
