---
name: dqmc-run
description: Execute DQMC Monte Carlo sweeps on HDF5 simulation files. Use when running simulations, checkpointing long runs, using the queue system for multiple files, or checking simulation status.
---

# Run Simulations

## Inputs

- HDF5 simulation file(s) from the dqmc-generate and dqmc-parameter-scans skills
- Binary at `build/dqmc`, worker utility from `dqmc-util worker`

## Outputs

- Updated HDF5 files with measurements in `/meas_eqlt/` (and `/meas_uneqlt/` if enabled)

## Decision Rules (single vs queue)

- **Exactly 1 file**: run it directly with `build/dqmc sim_0.h5`.
- **2+ files**: use the **queue/worker system** (`dqmc-util enqueue` + `dqmc-util worker`) even on a local workstation.
  - This avoids ad-hoc shell loops, makes restarts/checkpointing consistent, and scales to parallel execution safely.

## Procedure

**Single file:**
```bash
build/dqmc sim_0.h5
```

**With checkpointing (long runs):**
```bash
build/dqmc -s 300 -t 3600 sim_0.h5  # checkpoint every 300 seconds, max runtime 3600 seconds
```

**Multiple files (queue system):**
```bash
# 1. Add files to queue/ (globs are expanded by Python, so quote them)
dqmc-util enqueue queue 'data/run/bin_*.h5'

# 2. Start workers
dqmc-util worker queue ./build/dqmc -n 8 -s 300 -t 3600  # 8 parallel workers
```

**Multiple files (local temperature scan example):**
```bash
# enqueue all bins across temperatures
dqmc-util enqueue queue 'runs/pi_pi_U8_6x6/T*/bin_*.h5'

# run N workers in parallel (pick N for your machine)
dqmc-util worker queue ./build/dqmc -n 8 -s 300 -t 3600
```

## Validation (single file)
```bash
dqmc-util summary sim_0.h5
```

**For multiple files:**
```bash
dqmc-util print-n data/run/   # directory paths should end with '/'
```

## Failure Modes

| Symptom | Cause | Recovery |
|---------|-------|----------|
| "opening... failed" | File doesn't exist | Check path |
| NaN in output | Numerical instability | Reduce dt and/or n_matmul. Check parameters |
| Killed by scheduler | Exceeded time limit | Use `-t` flag, checkpoint enabled |
| Large errorbars | Sign problem | Add more sweeps and/or bins |

## Do Not

- Kill running simulations without checkpointing (`-s` flag)
- Run multiple workers on the same file
- Use manual shell loops for 2+ files (prefer `dqmc-util enqueue` + `dqmc-util worker`)
