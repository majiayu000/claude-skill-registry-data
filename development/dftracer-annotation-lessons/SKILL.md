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
date: 2026-06-20
app: general
context: HDF5 1.10.x silently degrades optimization effectiveness — always use 1.14
error: |
  H5Pset_page_buffer_size() had no effect; H5Fcreate_async() fell back to sync;
  posix_close_ops_slope bottleneck could not be fully resolved despite correct hints.
root_cause: |
  HDF5 1.10.x (latest Debian/Ubuntu package at time of writing) does not support
  page buffering with the MPI-IO VFD and the async VOL is not available.
  Applications that call H5Pset_page_buffer_size on an MPIO fapl in 1.10.x get
  a silent no-op; H5Fcreate_async is a stub that falls through to synchronous create.
  This means several L2 optimizations compile and run without error but have zero effect.
fix: |
  Always build with HDF5 ≥ 1.14.x for parallel I/O projects.
  Install from source with --enable-parallel:
    wget https://github.com/HDFGroup/hdf5/releases/download/hdf5_1.14.4/hdf5-1.14.4.tar.gz
    tar xf hdf5-1.14.4.tar.gz && cd hdf5-1.14.4
    CC=mpicc ./configure \
      --prefix=<ws>/hdf5_1.14 --enable-parallel --enable-shared \
      --enable-build-mode=production --with-zlib=/usr
    make -j$(nproc) && make install
  Then rebuild the application with HDF5_DIR pointing at 1.14 install.
  Verify: h5cc -showconfig | grep "Version:"  → should show 1.14.x
tags: [hdf5, version, page-buffer, async-vol, parallel-io, best-practice]

---
date: 2026-06-20
app: https://github.com/hariharan-devarajan/h5bench (main)
context: clang_annotate_project / clang_add_braces corrupts assert() macro call-sites
error: |
  After brace insertion, assert(pconfig->version == 0) was split into:
    assert(pconfig->version ==
    {
    0)
    }
  Compiler: "error: expected ')' before '{' token"
root_cause: |
  glibc's assert(expr) expands to: if (expr) ; else __assert_fail(...)
  The Clang AST reports this IfStmt with a NullStmt then-body (the bare ";").
  _collect_braceless was treating the NullStmt as an unbraced body and inserting
  {/} at the macro call-site line, splitting multi-line macro arguments.
fix: |
  In source_parser.py _collect_braceless(), add a NullStmt guard:
    if kind == "IfStmt":
        _then_is_null = (len(inner) >= 2 and inner[1].get("kind") == "NullStmt")
        for i, child in enumerate(inner):
            if i == 0: continue  # condition
            if _then_is_null: continue  # assert()-style — skip ALL bodies
            ...
  When the then-body (child[1]) is a NullStmt, the entire IfStmt comes from a
  macro expansion like assert(). Skip adding braces to all bodies of that IfStmt.
tags: [c, clang, brace-insertion, assert, macro, mcp-tool-fix]

---
date: 2026-06-20
app: https://github.com/hariharan-devarajan/h5bench (main)
context: clang_add_braces inserts standalone "{" before "else if", producing illegal C
error: |
  After brace insertion, else-if chains became:
    } else
    {
    if (condition) {
  Compiler: "error: expected expression before '{' token"
root_cause: |
  In _collect_braceless, when an IfStmt's else-body (index >= 2) is itself an
  IfStmt (the else-if case), _maybe_add was wrapping it. This inserted a standalone
  "{" line BEFORE the "else" keyword — producing "{ else if (...)" which is
  illegal C syntax.
fix: |
  In source_parser.py _collect_braceless(), add an else-if guard:
    if i >= 2 and child.get("kind") == "IfStmt":
        continue  # else-if: skip wrapping; recursion handles inner IfStmt
  The recursion already visits the inner IfStmt's own bodies; wrapping the outer
  else-body is never needed and always breaks else-if chains.
tags: [c, clang, brace-insertion, else-if, mcp-tool-fix]

---
date: 2026-06-20
app: https://github.com/hariharan-devarajan/h5bench (main)
context: DFTRACER_C_INIT(NULL, NULL, -1) causes segfault — third arg must be NULL not -1
error: |
  Segmentation fault in initialize_main() at fgets call immediately after startup.
  Stack: main → read_config_from_file → fgets → SIGSEGV
root_cause: |
  DFTRACER_C_INIT macro passes its third argument directly to initialize_main(log,
  dirs, int *process_id). Passing the integer -1 is implicitly cast to (int*)0xffffffffffffffff,
  which initialize_main then dereferences → immediate segfault.
fix: |
  Always use NULL (not -1 or any integer) for the process_id argument:
    DFTRACER_C_INIT(NULL, NULL, NULL)
  NULL is a valid int* meaning "auto-detect PID". The pipeline skill init_args
  default was updated from "NULL, NULL, -1" to "NULL, NULL, NULL".
tags: [c, dftracer-init, segfault, init-args, pipeline-skill]

---
date: 2026-06-20
app: https://github.com/hariharan-devarajan/h5bench (main)
context: CMake library name mismatch — dftracer installs as libdftracer_core.so not libdftracer.so
error: |
  /usr/bin/ld: cannot find -ldftracer: No such file or directory
root_cause: |
  dftracer's installed library filename is libdftracer_core.so (not libdftracer.so).
  session_install_dftracer patches CMake to link -ldftracer, but the actual soname
  is dftracer_core. This causes linker failure on all targets.
fix: |
  After session_install_dftracer completes, patch both CMakeCache.txt and all
  generated link.txt files:
    sed -i 's/-ldftracer\b/-ldftracer_core/g' build_ann/CMakeCache.txt
    find build_ann/CMakeFiles -name "link.txt" \
      -exec sed -i 's/-ldftracer\b/-ldftracer_core/g' {} \;
  Verify: grep -r "ldftracer[^_]" build_ann/ → should return nothing
  Note: session_build_annotated should be updated to auto-apply this fix.
tags: [c, cmake, linker, dftracer-install, libdftracer_core]

---
date: 2026-06-20
app: https://github.com/hariharan-devarajan/h5bench (main)
context: -ldftracer_core on its own line in link.txt causes cmake_link_script to ignore it
error: |
  All -ldftracer_core flags were silently dropped; linker still reported undefined
  reference to initialize_region after the fix was applied.
root_cause: |
  When appending -ldftracer_core to link.txt using "echo -n >> file", the file
  already had a trailing newline, so the flag ended up on its own line.
  cmake -E cmake_link_script executes each line as a separate command; a line
  containing only " -ldftracer_core" is not a valid command and is silently ignored.
fix: |
  When patching link.txt, join the flag to the SAME line as the cc command:
    # Remove from current position first, then re-append properly:
    find build_ann/CMakeFiles -name "link.txt" | while read f; do
      sed -i 's/ -ldftracer_core / /g' "$f"
      # Remove trailing newline from last line, append flag, add newline
      content=$(head -n -1 "$f" | tr -d '\n')  # if on its own line
      echo "${content} -ldftracer_core" > "$f"
    done
tags: [cmake, link-order, link-txt, cmake_link_script, dftracer_core]

---
date: 2026-06-20
app: https://github.com/hariharan-devarajan/h5bench (main)
context: Link order error — -ldftracer_core before .o files causes undefined references
error: |
  undefined reference to `initialize_region'
  undefined reference to `update_metadata_string'
  undefined reference to `finalize_region'
  (symbols DO exist in libdftracer_core.so per nm)
root_cause: |
  The linker processes libraries left-to-right. When -ldftracer_core appears BEFORE
  the .o object files that need it, no symbols are requested yet so the linker
  skips pulling them in. When the .o files are processed later, the library is
  already past and symbols are not found.
fix: |
  Ensure -ldftracer_core appears AFTER all .o files in the link command.
  When CMake places it before the objects (via CMAKE_EXE_LINKER_FLAGS), patch
  the generated link.txt files to move the flag to the end:
    sed -i 's/ -ldftracer_core//g' link.txt
    # append at end of the line (see lesson above about same-line appending)
tags: [c, cmake, linker, link-order, undefined-reference, dftracer_core]

---
date: 2026-06-20
app: https://github.com/hariharan-devarajan/h5bench (main)
context: Patching CMakeCache.txt triggers cmake re-run that loses MPI detection
error: |
  CMake re-ran configure after CMakeCache.txt was edited; MPI was not found:
  "Could NOT find MPI_C" / "Could NOT find MPI_CXX"
root_cause: |
  Modifying CMakeCache.txt causes cmake's cmake_check_build_system to re-run
  configure. The re-run could not find MPI because it looked for mpich/openmpi
  in the wrong place in a container environment.
fix: |
  After editing CMakeCache.txt, also add these entries to skip MPI re-detection:
    MPI_C_WORKS:BOOL=TRUE
    MPI_CXX_WORKS:BOOL=TRUE
  This tells cmake that MPI was already verified and prevents the re-check.
tags: [cmake, mpi, cmake-cache, re-configure, container]

---
date: 2026-06-20
app: https://github.com/hariharan-devarajan/h5bench (main)
context: h5bench_write expects an INI key=value config file, not the JSON sample files
error: |
  Passing samples/sync-write-1d-contig-contig.json as the config file caused a
  segfault inside fgets() — the JSON was parsed as INI and file handle was corrupted.
root_cause: |
  The JSON files in h5bench/samples/ are for the h5bench Python runner (h5bench.py),
  which reads them and generates a temporary key=value INI file. h5bench_write itself
  only accepts a simple KEY=VALUE text file (one pair per line, no sections).
fix: |
  Create a minimal INI-style config directly:
    cat > /tmp/h5bench.cfg << 'EOF'
    MEM_PATTERN=CONTIG
    FILE_PATTERN=CONTIG
    TIMESTEPS=3
    DELAYED_CLOSE_TIMESTEPS=0
    COLLECTIVE_DATA=NO
    COLLECTIVE_METADATA=NO
    NUM_DIMS=1
    DIM_1=1048576
    DIM_2=1
    DIM_3=1
    EOF
    mpirun -np 2 ./h5bench_write /tmp/h5bench.cfg /tmp/test.h5
  The h5bench.py runner auto-generates this file from JSON; to invoke h5bench_write
  directly, create the INI file manually.
tags: [h5bench, config, ini, json, segfault, smoke-test]

---
date: 2026-06-20
app: https://github.com/hariharan-devarajan/h5bench (main)
context: Missing DFTRACER_DATA_DIR=all silently drops I/O events outside the workspace dir
error: |
  Trace files written but dfanalyzer shows low or zero file I/O event count;
  events for /tmp and other non-workspace paths are missing.
root_cause: |
  dftracer's DFTRACER_DATA_DIR defaults to watching only specific directories.
  When benchmarks write to /tmp, /scratch, or any path outside the default scope,
  those events are silently excluded from the trace.
fix: |
  Always pass DFTRACER_DATA_DIR=all when collecting traces:
    DFTRACER_ENABLE=1 DFTRACER_DATA_DIR=all DFTRACER_INC_METADATA=1 \
      DFTRACER_LOG_FILE=<prefix> DFTRACER_INIT=FUNCTION ./binary ...
  This ensures ALL file paths are traced regardless of location.
  Applies to both session_run_with_dftracer (pass data_dir="all") and manual runs.
tags: [dftracer, data_dir, trace-missing, DFTRACER_DATA_DIR, best-practice]

---
date: 2026-06-20
app: general
context: Missing DFTRACER_INC_METADATA=1 omits metadata events from trace
error: |
  Trace events are missing process/thread name metadata and custom key=value fields
  set via DFTRACER_C_FUNCTION_UPDATE_STR even though the annotations compiled fine.
root_cause: |
  dftracer's metadata events (process name, thread name, custom key=value pairs
  set via UPDATE_STR/UPDATE_INT) are only recorded when DFTRACER_INC_METADATA=1
  is set in the environment. Without it, only timing events are captured.
fix: |
  Always set DFTRACER_INC_METADATA=1 alongside other dftracer env vars:
    DFTRACER_ENABLE=1 DFTRACER_DATA_DIR=all DFTRACER_INC_METADATA=1 \
      DFTRACER_LOG_FILE=<prefix> DFTRACER_INIT=FUNCTION ./binary ...
  The comp=, filename=, count= etc. metadata set via UPDATE_STR will not appear
  in the trace without this flag — the span start/end timestamps will be there
  but the custom attributes won't.
tags: [dftracer, metadata, DFTRACER_INC_METADATA, UPDATE_STR, best-practice]

---
date: 2026-06-20
app: https://github.com/hariharan-devarajan/h5bench (main)
context: DFTRACER_ENABLE=1 is required when explicit DFTRACER_C_INIT() calls are used
error: |
  No trace files written to DFTRACER_LOG_FILE path after h5bench_write run.
  Application completed successfully but /tmp/h5bench_trace* was empty.
root_cause: |
  When the annotated code contains explicit DFTRACER_C_INIT() calls, dftracer's
  default initialization mode (without DFTRACER_ENABLE=1) may not write traces
  unless explicitly enabled via the environment.
fix: |
  Always set both DFTRACER_ENABLE=1 and DFTRACER_LOG_FILE when running:
    DFTRACER_ENABLE=1 DFTRACER_LOG_FILE=/tmp/my_trace \
      DFTRACER_INIT=FUNCTION ./h5bench_write cfg out.h5
  Trace files are written as: <LOG_FILE>-<hash>-app.pfw.gz
tags: [dftracer, DFTRACER_ENABLE, trace-missing, h5bench, smoke-test]

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

---

## General Pitfalls (PG)

These apply to all languages (C, C++, Python).

PG1  File truncated
     Written lines < original line count → re-read the file, rewrite the complete file.

PG2  Header file annotated
     Macros placed in a .h or .hpp file → move all macros to the .c or .cpp source file.

PG3  comp= missing
     Annotation count does not equal comp= count → find and fix each gap before reporting DONE.

PG4  Lifecycle function skipped
     A *_init, *_finalize, or similar lifecycle function has a short body and was skipped via
     Rule 0 → always annotate lifecycle functions regardless of body length (see ALWAYS_ANNOTATE).

PG5  Vendor function skipped
     gpfs_*, beegfs_*, lustre_*, hdfs_*, ceph_*, daos_* functions were skipped →
     always annotate with comp="io".

PG6  Re-annotating a dirty file
     The annotated copy already contains dftracer macros from a previous run → restore the
     original (unannotated) copy first, then re-annotate from scratch.

PG7  Coverage check skipped
     Reported DONE without running the coverage verification step → always run Step 6 before
     reporting DONE. START/decorator count must equal comp= count.

PG8  UPDATE uses forward-declaration parameter name
     'param' undeclared error in UPDATE_STR/UPDATE_INT → read parameter names from the
     function definition body, not from a forward declaration.

PG9  Wrong tool name (-32002 Tool not found)
     Dot notation is not valid for MCP tools in this environment. Use the correct names:
       WRONG                        CORRECT
       todo.todoWrite               todo__todo_write
       read_file                    load
       session_read_file            dftracer__session_read_file
       session_write_file           dftracer__session_write_file
       clang_add_braces             dftracer__clang_add_braces
       clang_extract_functions      dftracer__clang_extract_functions

PG10 Revert-all on build error
     A syntax or build error caused the entire annotated file to be reverted → do NOT
     revert the whole file. Strip macros from the FAILING FUNCTION ONLY, mark it PENDING
     with a reason, and continue annotating the remaining functions. Write the new pitfall
     to lessons-learned immediately.

---

## C-Specific Pitfalls (PC)

PC1  END after return
     DFTRACER_C_FUNCTION_END() was placed AFTER the return statement (dead code) →
     swap order: END must PRECEDE the return.

PC2  END at column 0
     DFTRACER_C_FUNCTION_END() was emitted at column 0 with no indentation →
     match the indentation of the return statement it precedes; never at column 0.

PC3  START before opening brace
     DFTRACER_C_FUNCTION_START() was placed before the opening '{' → syntax error.
     Move START to the first line INSIDE the body, after '{'.

PC4  Error macro hides exit
     MPI_CHECK / NCMPI_CHECK / H5EPRINT / HGOTO_ERROR macros internally expand to a
     hidden return or goto → do NOT add END before these macros. Only add END before
     explicit visible return statements that follow in the source.

PC5  goto: END before each goto
     Adding END before every goto statement that jumps to a shared exit label results
     in duplicate END calls → place a SINGLE END at the exit label instead, not before
     each individual goto.

PC6  Forward declaration annotated
     Annotated a line ending with ';' (a forward declaration) instead of the definition
     with a body → filter grep results to definitions only; annotate ONLY the definition.

PC7  Wrong DFTRACER_INIT value
     DFTRACER_INIT=1 is not a valid value. Valid values are:
       FUNCTION  — default and recommended (annotation-based tracing)
       PRELOAD   — use when no application annotation is done; requires LD_PRELOAD set
                   to dftracer_preload.so
       HYBRID    — both LD_PRELOAD and application annotation active
     Using an invalid value silently disables tracing.

---

## C++-Specific Pitfalls (CP)

CP1  Used DFTRACER_C_* macros in a .cpp file
     C macros do not compile in C++ translation units → replace every DFTRACER_C_*
     macro with its DFTRACER_CPP_* equivalent.

CP2  Used DFTRACER_CPP_FUNCTION() in main()
     RAII guard fires after DFTRACER_CPP_FINI(), producing a use-after-finalize span →
     replace with DFTRACER_CPP_REGION_START / REGION_END in main().

CP3  Used DFTRACER_CPP_REGION_* in a regular (non-main) function
     REGION macros are only for main() → replace with DFTRACER_CPP_FUNCTION() which
     uses the RAII pattern.

CP4  Added manual DFTRACER_CPP_FUNCTION_END() after DFTRACER_CPP_FUNCTION()
     There is no END macro for the CPP RAII guard; the destructor fires automatically on
     scope exit → remove the manual END calls.

CP5  Used UPDATE_INT in C++
     There is no DFTRACER_CPP_FUNCTION_UPDATE_INT in the C++ API → either omit the
     numeric parameter or convert it to a string before passing to FUNCTION_UPDATE.

CP6  Added #include to a .hpp header file
     dftracer includes in header files get compiled into every translation unit that
     includes the header → move the #include <dftracer/dftracer.h> to the .cpp/.cxx
     source file only.

CP7  comp= UPDATE missing
     DFTRACER_CPP_FUNCTION() count does not equal the DFTRACER_CPP_FUNCTION_UPDATE("comp",...)
     count → add a comp= UPDATE immediately after each DFTRACER_CPP_FUNCTION() call.

CP8  REGION_END missing before a return in main()
     main() has a return path that lacks DFTRACER_CPP_REGION_END before it → add
     REGION_END (and FINI if applicable) before every return statement in main().

---

## Python-Specific Pitfalls (PP)

PP1  Missing import
     ImportError at runtime: dftracer_fn or DFTracer not found →
     add: from dftracer.logger import dftracer_fn, DFTracer

PP2  comp= keyword missing from decorator
     @dftracer_fn decorator count does not equal comp= count →
     add comp="<type>" to every @dftracer_fn call.

PP3  Inconsistent cat= names across the file
     Mixed "io" / "IO" / "file" cat= values → standardise to a single consistent
     convention per file (e.g., "IO", "Compute", "MPI", "Data", "Init").

PP4  initialize_log missing from entry point
     Empty or missing trace file → add DFTracer.initialize_log(...) to every entry
     point file (top of if __name__ == "__main__" or the entry function body).

PP5  finalize_log missing
     Trace file is truncated or missing final events → add DFTracer.finalize_log()
     before every sys.exit() call and before MPI.Finalize().

PP6  @dftracer_fn placed above other decorators
     When stacked with other decorators, @dftracer_fn must be CLOSEST to the def
     statement (i.e., the last decorator before def) → move it below all other
     decorators.

PP7  @property method decorated with @dftracer_fn
     Applying @dftracer_fn to a @property accessor conflicts with the property
     descriptor protocol → skip all @property methods.

PP8  Wrong DFTRACER_INIT value when calling DFTracer.initialize_log()
     If the Python code calls DFTracer.initialize_log() explicitly, set
     DFTRACER_INIT=0 in the environment so the C-level auto-init does not double-
     initialize. Leaving DFTRACER_INIT unset while using explicit initialize_log()
     can produce duplicate or empty traces.

---

## Core Annotation Rules

### ALWAYS_ANNOTATE (never apply Rule 0 skip to these)

These function categories must always be annotated, regardless of body length or
perceived complexity:

  - Lifecycle:   *_init, *_final, *_initialize, *_finalize
  - Sync/flush:  *_fsync, *_flush, *_sync
  - File ops:    *_delete, *_rename, *_stat, *_mknod, *_getfilesize
  - Vendor FS:   gpfs_*, beegfs_*, lustre_*, hdfs_*, ceph_*, daos_*

### Rule 0 — Skip criterion

Apply Rule 0 (skip without annotation) ONLY when ALL of the following are true:
  1. The function is a pure getter or setter with no more than 5 lines
  2. It returns a single field
  3. It performs no I/O, no data movement, and no syscalls

Every Rule 0 skip must be justified by function name in the per-file report.

### comp= Classification Table

  "io"   — file I/O (POSIX open/read/write/close/stat/mmap), HDF5, NCMPI,
            backend lifecycle (init/final/initialize/finalize), vendor FS helpers
  "comm" — MPI wrappers, network I/O, distributed FS clients (S3, HDFS, RADOS, DFS)
  "mem"  — memcpy, large buffer alloc/free, mmap region setup, tensor copies
  "cpu"  — checksums, compression, encryption, hashing

C note:   transfer to/from a file (POSIX/MMAP/HDF5/NCMPI) → "io";
          transfer via network/MPI → "comm"; memcpy into mmap → "mem"
C++ note: MPI calls wrapped in C++ → "comm"; std::filesystem / fstream → "io"
Python:   comp= classification uses the same table

### Per-Function Incremental Annotation Loop (Step 1.5 rule)

Annotate ONE function at a time. After each function:

  a. Write the full file (never a partial):
       dftracer__session_write_file(run_id=..., filepath=..., content=<FULL FILE>,
         subfolder="annotated")

  b. Run the language-specific syntax check:
       C:      gcc -include /tmp/dftracer_stub.h -fsyntax-only -w -x c <file> 2>&1
       C++:    g++ -include /tmp/dftracer_stub.h -fsyntax-only -w -std=c++14 <file> 2>&1
       Python: python3 -c "import ast; ast.parse(open('<file>').read())" 2>&1

  c. PASS → mark function annotated, move to the next function.

  d. FAIL →
       i.   Identify the exact line and macro from the error message.
      ii.   Fix ONLY that macro — do not touch functions that already passed.
     iii.   Write the file and re-check (max 2 retries for this function).
      iv.   After 2 failed retries: strip macros from THIS function only,
            mark it PENDING with reason, and continue to the next function.
       v.   Write the new pitfall to the lessons file IMMEDIATELY (not at the end).

Rules that must never be broken during the loop:
  - NEVER revert annotations from functions that already passed their syntax check.
  - NEVER fix an error by reverting the whole file.
  - NEVER skip the syntax check step — it catches placement errors before the full build.
  - If BUILD ERROR MODE is active (build_errors param is set): process only the
    functions named in the errors first, then continue with unannotated functions.
