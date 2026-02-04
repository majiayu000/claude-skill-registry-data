---
name: dqmc-dev
description: Workflow for modifying DQMC C code, adding new measurements, and running tests. Use when editing source code, implementing new observables, debugging, or validating code changes.
---

# Code Development

## Build & Test

```bash
# Build
make               # -> build/dqmc
make clean         # remove build/

# Test
cd test && make && ./test_greens
```

## Smoke Test

After any code change:
```bash
dqmc-util gen Nx=4 Ny=4 U=4 dt=0.1 L=20 n_sweep_warm=50 n_sweep_meas=100
build/dqmc sim_0.h5
dqmc-util summary sim_0.h5
```

## Adding New Measurements

1. **Add to X-macro list** in `src/rc/sim_types.h`:
   ```c
   // Add to MEAS_EQLT_LIST (or MEAS_UNEQLT_LIST for unequal-time)
   #define MEAS_EQLT_LIST \
       /* ... */ \
       X(my_meas, num_ij)  // pick an appropriate size expression
   ```

2. **Implement measurement kernel** in `src/rc/meas.c`

3. **Add analysis function** in `dqmc_util/analyze_hub.py` (and update reshaping/symmetrization if needed):
   ```python
   @observable(
       description="my new observable",
       requires=("meas_eqlt/n_sample", "meas_eqlt/sign", "meas_eqlt/my_meas"),
   )
   def _my_meas(ctx):
       return core.jackknife_noniid(
           ctx.data["meas_eqlt/n_sample"],
           ctx.data["meas_eqlt/sign"],
           ctx.data["meas_eqlt/my_meas"],
       )
   ```

## Key Code Patterns

**Dual compilation:** Files in `src/rc/` compile twice. Use `RC(name)` macro for real/complex dispatch.

**Memory:** Use `my_calloc()` for 64-byte aligned allocations.

**Profiling:** Wrap with `profile_begin(name)` / `profile_end(name)`.

## Definition of Done

- [ ] `make` succeeds without warnings
- [ ] `cd test && make && ./test_greens` passes
- [ ] Smoke run completes
- [ ] If touching measurements: verify via `dqmc-util summary`
