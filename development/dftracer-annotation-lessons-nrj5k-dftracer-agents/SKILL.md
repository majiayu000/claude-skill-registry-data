---
name: dftracer-annotation-lessons
description: >
  Lessons learned from dftracer annotation sessions — real errors, root causes,
  and exact fixes. Loaded by each per-file annotation subagent at startup.
  Updated by the pipeline recipe after every session (Step 8).
---

## How to use this file

Read this before annotating any file. For each lesson:
  1. Check if the `context` matches what you are about to do
  2. If so, apply the `fix` proactively — do not repeat the mistake

## How to add new entries

The pipeline recipe (Step 8) appends new entries after each session.
Entries follow this format:

```
---
date: YYYY-MM-DD
app: <git url>
context: <one-line description of what was being attempted>
error: |
  <exact error message or key excerpt>
root_cause: <why it happened>
fix: |
  <exact steps or rule that resolved it>
tags: [<language>, annotation, <error-keyword>]
---
```

Do not delete old entries. Entries accumulate as institutional memory.

---

## Standing rules (always apply, every session)

These are not lessons from failures — they are invariants that must hold:

R1  Read the lessons file before annotating any file (you are doing that now).

R2  Write the COMPLETE file when calling session_write_file. Never a partial.
    Verify: written line count > original line count.

R3  Run coverage verification after every file before moving to the next.
    START/decorator count must equal comp= count.

R4  Never annotate a forward declaration (C/C++: a line ending with ";").
    For any function name found twice, annotate only the definition (has body).

R5  Never annotate a header file (.h / .hpp).
    Put #include <dftracer/dftracer.h> in .c / .cpp files only.

R6  Lifecycle functions (*_init, *_final, *_initialize, *_finalize) are always
    annotated regardless of body length — never apply Rule 0 skip to them.

R7  Vendor filesystem functions (gpfs_*, beegfs_*, lustre_*, hdfs_*, ceph_*,
    daos_*) are always annotated as comp="io".

R8  If annotated code contains explicit DFTRACER_C_INIT() / DFTRACER_CPP_INIT()
    / DFTracer.initialize_log() calls, the environment must have DFTRACER_INIT=0
    when running the binary. Setting DFTRACER_INIT=1 with explicit INIT calls
    produces an empty trace file with no events.

---

## Session logs (appended by pipeline Step 8)

<!-- New entries are appended below this line by the pipeline recipe -->

---
date: 2026-06-17
app: https://github.com/llnl/ior (tag 4.0.0)
context: Inserting DFTRACER_C_FUNCTION_END into braceless single-line if (dryRun pattern)
error: |
  Inserting END made the early return unconditional — dryRun check bypassed.
  Or: compiler error "expected ';' before DFTRACER_C_FUNCTION_END"
root_cause: C braceless-if shares its body with the first following statement.
  END inserted before the return stole the if body, making return fall through always.
fix: |
  Grep for braceless early-exit lines before annotating each file:
    grep -n "if.*return\|if.*continue\|if.*break" <file.c> | grep -v "{" | grep -v "//"
  For each hit, add explicit braces FIRST, then insert END:
    // Before: if (dryRun) return NULL;
    // After:
    if (dryRun) {
      DFTRACER_C_FUNCTION_END();
      return NULL;
    }
tags: [c, annotation, braceless, if-body, dryRun, build-error]

---
date: 2026-06-17
app: https://github.com/llnl/ior (tag 4.0.0)
context: DFTRACER_C_FINI placed before ior_main() call — all backend spans missing from trace
error: |
  Trace contains only the main() span. No POSIX_Create, MPIIO_Open, HDF5_Close
  or any other backend spans appear even though those functions are annotated.
root_cause: |
  DFTRACER_C_FINI() was placed just before the final return in main(), BEFORE
  ior_main() had been called. dftracer finalized and stopped recording; all backend
  I/O that ran inside ior_main() was untraced.
fix: |
  FINI must appear AFTER the top-level benchmark function returns. Structure:
    int main(...) {
      MPI_Init(...);
      DFTRACER_C_INIT(NULL, NULL, NULL);
      DFTRACER_C_FUNCTION_START();
      ...
      ior_main(opts);           // ← real I/O happens here
      DFTRACER_C_FUNCTION_END();
      DFTRACER_C_FINI();        // ← AFTER ior_main, not before the benchmark call
      MPI_Finalize();
      return 0;
    }
  Before placing FINI, identify the "benchmark call" in main() — the call that
  does all the real work — and ensure FINI comes after it returns.
tags: [c, annotation, fini, main, empty-trace, benchmark-wrapper]

---
date: 2026-06-17
app: https://github.com/llnl/ior (tag 4.0.0)
context: HDF5 stray END inserted because grep matched forward declaration instead of definition
error: |
  HDF5_Create had a DFTRACER_C_FUNCTION_END() inserted before DFTRACER_C_FUNCTION_START()
  — compile error or incorrect trace span.
root_cause: |
  grep matched the forward declaration of HDF5_Create (which ends with ';')
  and inserted an END there, then also annotated the real definition.
fix: |
  Always filter grep results to definitions only:
    grep -n "HDF5_Create" file.c | grep -v ";$"
  The definition has a body ({...}); the forward declaration ends with ';'.
  Annotate ONLY the definition line, never the declaration.
tags: [c, annotation, forward-declaration, stray-end, hdf5]

---
date: 2026-06-17
app: https://github.com/llnl/ior (tag 4.0.0)
context: dftracer built without MPI/HDF5 support — MPIIO and HDF5 annotation not captured
error: |
  Trace files exist but contain only POSIX events. MPIIO_* and HDF5_* annotated
  function spans are missing even though the annotations compiled correctly.
root_cause: |
  dftracer was installed without -DDFTRACER_ENABLE_MPI=ON and -DDFTRACER_ENABLE_HDF5=ON.
  The config header shows DFTRACER_MPI_ENABLE 0. Without MPI support, dftracer
  cannot intercept MPI-IO paths and MPI-aware annotations produce no events.
fix: |
  Rebuild dftracer with backend flags:
    cmake -DCMAKE_INSTALL_PREFIX=<prefix> \
          -DDFTRACER_ENABLE_MPI=ON \
          -DDFTRACER_ENABLE_HDF5=ON \
          -DDFTRACER_ENABLE_FTRACING=ON <src>
    make -j4 install
  Verify: grep DFTRACER_MPI_ENABLE <prefix>/include/dftracer/core/dftracer_config.hpp
  Expected output: #define DFTRACER_MPI_ENABLE 1
  Then do a clean rebuild of the annotated project against the new dftracer install.
tags: [c, dftracer-install, mpi, hdf5, missing-spans, dftracer_config]

---
date: 2026-06-17
app: https://github.com/llnl/ior (tag 4.0.0)
context: IOR autotools configure silently ignored new --with-hdf5 flag due to stale state
error: |
  ./configure --with-hdf5 completed without error but config.h showed USE_HDF5_AIORI=0.
  The HDF5 backend was not compiled in.
root_cause: |
  Stale .deps/, config.status, and autom4te.cache from a previous ./configure run
  caused autotools to skip re-detection of HDF5. The new --with-hdf5 flag was
  effectively ignored.
fix: |
  Before reconfiguring after any flag change:
    make distclean
    rm -rf .deps src/.deps autom4te.cache config.status config.log Makefile
  Then set HDF5 paths via env and use bare --with-hdf5 (no path argument):
    export CPPFLAGS="-I${HDF5_PREFIX}/include"
    export LDFLAGS="-L${HDF5_PREFIX}/lib -Wl,-rpath,${HDF5_PREFIX}/lib"
    export LIBS="-lhdf5 -lz"
    ./configure --with-hdf5 --prefix=<install_prefix> ...
  Verify: grep USE_HDF5_AIORI config.h → should show 1
tags: [autotools, hdf5, stale-config, configure, ior, distclean]

---
date: 2026-06-17
app: https://github.com/llnl/ior (tag 4.0.0)
context: OpenMPI refuses to run as root in a container environment
error: |
  --------------------------------------------------------------------------
  There are components in the Open MPI that should not be run as root.
  --------------------------------------------------------------------------
root_cause: |
  The container runs as uid=0. OpenMPI's default policy refuses to launch
  as root as a safety measure.
fix: |
  Add --allow-run-as-root to mpirun and set the two confirm env vars:
    OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1 \
      mpirun -np 1 --allow-run-as-root ./src/ior -a MPIIO ...
  When using session_run_with_dftracer, pass via env_extra:
    {"OMPI_ALLOW_RUN_AS_ROOT": "1", "OMPI_ALLOW_RUN_AS_ROOT_CONFIRM": "1"}
tags: [mpi, openmpi, root, container, smoke-test]

---
date: 2026-06-17
app: general
context: Running dftracer trace collection — always use DFTRACER_DATA_DIR=all and start dftracer_service daemon
error: |
  (not an error — a standing best-practice from IOR session experience)
root_cause: |
  Using a scoped DFTRACER_DATA_DIR (e.g., workspace/source) silently drops I/O events
  on /tmp, /scratch, or other paths where benchmarks actually write data.
  Not running dftracer_service means only inline annotation spans are captured,
  missing system-level I/O that the daemon would have recorded.
fix: |
  In the pipeline trace run (Step 7):
  1. Always pass data_dir="all" to session_run_with_dftracer.
     This sets DFTRACER_DATA_DIR=all so no I/O path is excluded.
  2. Start dftracer_service before the run and stop it after:
       SERVICE_BIN=<WS>/install_ann/bin/dftracer_service
       SERVICE_LOG=<WS>/traces/service
       mkdir -p "$SERVICE_LOG"
       DFTRACER_ENABLE=1 DFTRACER_LOG_FILE=<WS>/traces/<RUN_ID> \
         DFTRACER_DATA_DIR=all DFTRACER_TRACE_INTERVAL_MS=1000 \
         "$SERVICE_BIN" start "$SERVICE_LOG"
       # ... run application ...
       "$SERVICE_BIN" stop "$SERVICE_LOG"
  If $SERVICE_BIN is missing, skip service start/stop (service not compiled in).
tags: [dftracer, data_dir, service, daemon, trace, best-practice]

---
date: 2026-06-18
app: https://github.com/llnl/ior (tag 4.0.0)
context: session_split_traces fails because pfw files are in a subdirectory of traces/
error: |
  {"status": "error", "message": "No .pfw or .pfw.gz files found in <workspace>/traces"}
root_cause: |
  When run_id contains a slash (e.g., "ior/20260617_185032"), dftracer's LOG_FILE is
  set to <workspace>/traces/<run_id>, so it writes:
    <workspace>/traces/ior/20260617_185032-<hash>-app.pfw.gz
  The subdirectory traces/ior/ must be created before the run, AND the split tool
  looks only in traces/ directly (not subdirectories), so files must be copied up.
fix: |
  Before calling session_run_with_dftracer, create the subdirectory:
    mkdir -p <workspace>/traces/<run_id_prefix>   # e.g., traces/ior
  After the run, copy pfw files to the parent traces/ directory before splitting:
    cp <workspace>/traces/ior/*.pfw.gz <workspace>/traces/
  Then call session_split_traces normally.
tags: [dftracer, traces, split, run_id, subdirectory, pfw]

---
date: 2026-06-18
app: general
context: DFTRACER_INIT=0 prevents the POSIX interceptor from capturing syscall-level events
error: |
  dfanalyzer reports "Total Files: 0" and no POSIX-layer events in trace despite
  application running and C_APP annotations recording correctly.
root_cause: |
  Setting DFTRACER_INIT=0 disables the dftracer constructor, which prevents the
  POSIX LD_PRELOAD interceptor from initializing. The current values are FUNCTION (default and recommended), PRELOAD (is no annotation is done), and HYBRID. Only C_APP (application-level)
  annotations are recorded; open/read/write/close syscalls are never hooked.
  dfanalyzer's posix preset requires POSIX-layer events to compute file I/O metrics.
fix: |
  Do NOT set DFTRACER_INIT=0 when you want POSIX-layer tracing. It can be FUNCTION (RECOMMENDED), PRELOAD (when no applictaion annotation is done), or HYBRID (both preload is set and applictaion annotaion is done), but not 0.
  Even when the annotated source has explicit DFTRACER_C_INIT() calls, leave
  DFTRACER_INIT unset (defaults to FUNCTION). The auto-init and explicit C_INIT() coexist
  without conflict — C_INIT() is idempotent when dftracer is already initialized.
  Only set DFTRACER_INIT=0 if you explicitly do NOT want POSIX-level tracing.
tags: [dftracer, DFTRACER_INIT, posix, interceptor, dfanalyzer]
