---
name: dftracer-preload-run
description: >
  Reference for running applications with dftracer in PRELOAD or HYBRID mode.
  Covers correct environment variable setup, DATA_DIR rules, LD_PRELOAD wiring,
  MPI forwarding, and trace verification. Use before any session_run_with_dftracer
  call or when debugging missing trace categories (POSIX/HDF5/MPI).
---

# DFTracer PRELOAD and HYBRID Run Reference

Source: https://dftracer.readthedocs.io/en/latest/api.html

---

## Three Modes

| Mode     | When to use                                      | DFTRACER_INIT | Source annotations needed |
|----------|--------------------------------------------------|---------------|--------------------------|
| FUNCTION | App profiling only — no I/O interception        | `FUNCTION`    | DFTRACER_C_INIT + FINI + START/END macros |
| PRELOAD  | Transparent I/O capture without source changes  | `PRELOAD`     | None |
| HYBRID   | Function profiling AND I/O interception together | `HYBRID`      | DFTRACER_C_INIT + DFTRACER_C_FINI (both required) |

**HYBRID rule:** Use `DFTRACER_INIT=HYBRID` only when the annotated source
contains **both** `DFTRACER_C_INIT(...)` and `DFTRACER_C_FINI()`. If only one
is present, use `PRELOAD` instead (missing FINI leaves the trace open).

---

## Required Environment Variables

Set ALL of these before invoking the binary (PRELOAD or HYBRID):

```bash
# mandatory
export DFTRACER_ENABLE=1
export DFTRACER_INIT=PRELOAD          # or HYBRID — uppercase, exact string
export DFTRACER_LOG_FILE=/path/to/output/prefix
export DFTRACER_DATA_DIR=/path/to/watch:/another/path

# strongly recommended
export DFTRACER_INC_METADATA=1        # captures rank/file/comp metadata

# required for shared library resolution
export LD_LIBRARY_PATH=<session_venv>/lib/python3.12/site-packages/dftracer/lib:$LD_LIBRARY_PATH

# required to activate I/O interception
export LD_PRELOAD=<session_venv>/lib/python3.12/site-packages/dftracer/lib/libdftracer_preload.so
```

---

## DFTRACER_DATA_DIR Rules

`DFTRACER_DATA_DIR` is **case-sensitive** and must be a **real filesystem
path** or colon-separated list of paths. The string `"all"` is **not** valid
at the C++ layer (it is only understood by the Python helper layer and will
cause a `Code 2001` error at runtime).

| Goal                               | Correct value              |
|------------------------------------|----------------------------|
| Capture all I/O on any file        | `/` or leave empty¹        |
| Capture I/O under /tmp             | `DFTRACER_DATA_DIR=/tmp`   |
| Capture two specific data dirs     | `DFTRACER_DATA_DIR=/data:/scratch` |
| HDF5 + MPI-IO file in /tmp         | `DFTRACER_DATA_DIR=/tmp`   |

¹ Empty / unset → dftracer errors out with Code 2001. Always set an explicit path.

Use `/` to capture I/O on any path without knowing the exact location in advance.

---

## MPI Programs: Forwarding Environment Variables

`mpirun` does **not** automatically forward the shell environment to ranks.
You must **export** each variable AND pass it with `-x`:

```bash
# Export all vars first
export DFTRACER_ENABLE=1
export DFTRACER_INIT=PRELOAD
export DFTRACER_DATA_DIR=/tmp
export DFTRACER_LOG_FILE=/tmp/traces/myapp
export DFTRACER_INC_METADATA=1
export LD_LIBRARY_PATH=<dftracer_lib>:$LD_LIBRARY_PATH
export LD_PRELOAD=<dftracer_lib>/libdftracer_preload.so

# Forward every var to each rank with -x
mpirun --allow-run-as-root -np 4 \
  -x DFTRACER_ENABLE \
  -x DFTRACER_INIT \
  -x DFTRACER_DATA_DIR \
  -x DFTRACER_LOG_FILE \
  -x DFTRACER_INC_METADATA \
  -x LD_LIBRARY_PATH \
  -x LD_PRELOAD \
  ./my_app
```

Omitting `-x LD_PRELOAD` means ranks run without interception (no trace files).
Omitting `-x DFTRACER_DATA_DIR` causes Code 2001 on every rank.

---

## Expected Trace Categories

After a successful PRELOAD/HYBRID run, trace files (`<prefix>-<hash>-preload.pfw.gz`)
should contain these Chrome-tracing event categories:

| Category  | Source                          | Requires                    |
|-----------|---------------------------------|-----------------------------|
| `POSIX`   | POSIX open/read/write/close     | `DFTRACER_DATA_DIR` matches |
| `STDIO`   | fopen/fread/fwrite/fclose       | `DFTRACER_DATA_DIR` matches |
| `HDF5`    | H5Fcreate/H5Dwrite etc.         | dftracer built with HDF5    |
| `MPI`     | MPI_File_write/read etc.        | dftracer built with MPI¹    |
| `dftracer`| Init/Fini metadata events       | always present              |

¹ MPI-IO tracing via brahma requires that the dftracer wheel was built with
`DFTRACER_ENABLE_MPI=ON` AND that the runtime MPI shared library matches the
version dftracer was compiled against. Verify with:
```bash
strings libdftracer_core.so | grep "openmpi/include"
# must match the mpi.h path on the system
```

Rank-level metadata (MPI rank, hostname) appears as `PR` (process rank),
`HH` (hostname hash), `FH` (file hash) events in the trace metadata.

---

## Verification Checklist

After running, verify:

```bash
# 1. Trace files exist and are non-empty
ls -lh <DFTRACER_LOG_FILE>*.pfw.gz

# 2. Categories visible in each file
for f in <prefix>*.pfw.gz; do
  zcat "$f" | python3 -c "
import sys, json
cats = set()
for line in sys.stdin:
    l = line.strip().rstrip(',')
    if l in ('[',']') or not l: continue
    try: cats.add(json.loads(l).get('cat',''))
    except: pass
print('$(basename $f):', sorted(cats))
"
done

# 3. MPI rank metadata present
zcat <any>.pfw.gz | python3 -c "
import sys, json
for line in sys.stdin:
    l = line.strip().rstrip(',')
    try:
        e = json.loads(l)
        if e.get('name') == 'rank': print('rank =', e['args']['value'])
    except: pass
"
```

---

## Common Errors and Fixes

| Error                                          | Cause                              | Fix                                      |
|------------------------------------------------|------------------------------------|------------------------------------------|
| `Code 2001: Data dirs not defined`             | `DFTRACER_DATA_DIR` not forwarded or set to `"all"` | Set to a real path, forward with `-x` |
| No trace files written                         | `DFTRACER_INIT` not uppercase or not forwarded | Use `PRELOAD` (uppercase), add `-x` |
| Empty trace files (0 bytes)                    | Library loaded but no I/O in `DATA_DIR` | Expand `DATA_DIR` or use `/`          |
| `HDF5` events missing                          | dftracer not built with `DFTRACER_ENABLE_HDF5=ON` | Reinstall with `HDF5_ROOT` set        |
| `MPI` events missing                           | MPI headers at build time don't match runtime lib | Reinstall with matching OpenMPI       |
| `DFTRACER_INIT=hybrid` → no function events    | String is case-sensitive; lowercase ignored | Use `HYBRID` (uppercase)              |
| Ranks crash with DFTRACER errors               | `LD_PRELOAD` not forwarded to MPI ranks | Add `-x LD_PRELOAD` to mpirun        |

---

## Quick Reference: session_run_with_dftracer

When using the MCP tool, pass these in `env_extra`:

```python
# PRELOAD mode (no source annotations)
session_run_with_dftracer(
    run_id  = RUN_ID,
    command = "mpirun --allow-run-as-root -np 4 -x DFTRACER_ENABLE -x DFTRACER_INIT -x DFTRACER_DATA_DIR -x DFTRACER_LOG_FILE -x DFTRACER_INC_METADATA -x LD_LIBRARY_PATH -x LD_PRELOAD ./myapp",
    data_dir = "/tmp",          # real path, not "all"
    env_extra = json.dumps({
        "DFTRACER_INIT": "PRELOAD",
        "LD_PRELOAD": "<venv>/lib/python3.12/site-packages/dftracer/lib/libdftracer_preload.so",
        "LD_LIBRARY_PATH": "<venv>/lib/python3.12/site-packages/dftracer/lib"
    })
)

# HYBRID mode (source has DFTRACER_C_INIT + DFTRACER_C_FINI)
session_run_with_dftracer(
    run_id  = RUN_ID,
    command = "mpirun --allow-run-as-root -np 4 -x DFTRACER_ENABLE -x DFTRACER_INIT -x DFTRACER_DATA_DIR -x DFTRACER_LOG_FILE -x DFTRACER_INC_METADATA -x LD_LIBRARY_PATH -x LD_PRELOAD ./myapp_annotated",
    data_dir = "/tmp",
    env_extra = json.dumps({
        "DFTRACER_INIT": "HYBRID",
        "LD_PRELOAD": "<venv>/lib/python3.12/site-packages/dftracer/lib/libdftracer_preload.so",
        "LD_LIBRARY_PATH": "<venv>/lib/python3.12/site-packages/dftracer/lib"
    })
)
```

The `data_dir` parameter to `session_run_with_dftracer` maps to `DFTRACER_DATA_DIR`.
When the tool says `data_dir="all"` in its docstring, that is a shorthand interpreted
by the tool itself — the C++ library still receives a real path.
