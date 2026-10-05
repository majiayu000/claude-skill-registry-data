---
name: dftracer-smoke-test
description: Smoke test rules for dftracer — single-process only, environment variables, DFTRACER_INIT conflict warning, and trace file paths
---

## Smoke Test Rules

**Always run smoke tests as a single process — never with MPI or any parallelism.**

- `session_run_smoke_test` automatically strips MPI launchers (`mpirun`, `mpiexec`,
  `srun`, `jsrun`, `aprun`, `flux run`) and their flags (`-np`, `-n`, `--ntasks`, etc.)
  from the command before running.
- Never use `-j N` (parallel make) inside a smoke test command.
- Never use `OMP_NUM_THREADS > 1` or `GOMP_SPINCOUNT` in smoke test env vars.
- If the application requires at least one MPI rank to start (e.g., calls
  `MPI_Init` unconditionally), run it with `mpirun -np 1 <binary> <args>` so the
  tool strips it to a single rank — NOT with multiple ranks.
- The smoke test command should exercise the minimal happy path: one input file,
  one iteration, smallest possible data size, no checksum or verification flags.

**Example for IOR:**
```
# Good — single process, minimal run
./src/ior -a POSIX -b 1m -t 1m -s 1 -F -C -o /tmp/ior_smoke_test

# Bad — MPI multi-process
mpirun -np 4 ./src/ior -a POSIX -b 1m -t 1m -s 1 -F -C -o /tmp/ior_smoke_test
```

## Key DFTracer Environment Variables (for session_run_with_dftracer)

`session_run_with_dftracer` sets all of these automatically — **do not pass them
in `env_extra` unless you have a specific override reason**:

| Variable | Value set by the tool | Purpose |
|---|---|---|
| `DFTRACER_ENABLE` | `1` | Activate tracing (required) |
| `DFTRACER_INC_METADATA` | `1` | Include process/thread metadata |
| `DFTRACER_LOG_FILE` | `workspaces/<run_id>/traces/<run_id>` | Trace file prefix |
| `DFTRACER_DATA_DIR` | `workspaces/<run_id>/source` | Directory to monitor for I/O events |
| `DFTRACER_INIT` | `FUNCTION` *(see note below)* | Auto-initialise without an explicit API call |

**DFTRACER_INIT conflict warning:** If the annotated source already contains explicit
`DFTRACER_C_INIT()` / `DFTRACER_CPP_INIT()` calls (added during Pass 1), do NOT set
`DFTRACER_INIT=1`. Both active simultaneously causes double-init, producing an empty
or corrupted trace file. Pass `env_extra='{"DFTRACER_INIT":"FUNCTION"}'` in that case.

Heuristic: `grep -r "DFTRACER_C_INIT\|DFTRACER_CPP_INIT" annotated/` — if any matches,
set `DFTRACER_INIT=FUNCTION`.

**`DFTRACER_LOG_FILE` must always be an absolute path inside the workspace run directory.**
Trace files land at `workspaces/<run_id>/traces/<run_id>.<pid>.pfw`.

**Never set `DFTRACER_LOG_FILE` to `/tmp/` or any path outside the workspace.**

If running the application manually outside the MCP tool:
```bash
export DFTRACER_ENABLE=1
export DFTRACER_INC_METADATA=1
export DFTRACER_LOG_FILE=/absolute/path/to/workspaces/<run_id>/traces/<run_id>
export DFTRACER_DATA_DIR=/absolute/path/to/workspaces/<run_id>/source
export DFTRACER_INIT=PRELOAD  # or FUNCTION if explicit init calls are in the code
```
