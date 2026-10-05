---
name: dftracer-build-run
description: Annotation-build-run iteration loop for dftracer — manual mode for when the pipeline exhausts retries or you are working interactively
---

## Annotation-Build-Run Iteration (manual mode)

The pipeline automatically retries build + run up to 3 times and fixes dftracer macro
errors in the affected files. When the pipeline exhausts its retries or you are working
interactively, follow this manual loop:

**Goal:** maximize dftracer coverage — `DFTRACER_C_FUNCTION_START/END` on every function,
`DFTRACER_C_FUNCTION_UPDATE_STR/INT` for important I/O parameters (filenames, sizes,
offsets, fds). Do NOT add `DFTRACER_C_REGION_START/END` — function-level macros are enough.

**Iteration loop:**

```
repeat until both build and run succeed:

  1. Read <workspace>/artifacts/10_session_build_annotated*.log
     → find which files have compile errors

  2. For each failing file:
     a. session_read_file(run_id, "annotated/src/foo.c")
     b. Identify the bad macro insertion (wrong scope, inside struct, missing START, etc.)
     c. session_write_file(run_id, "annotated/src/foo.c", corrected_content)
        Rules:
        - Every non-trivial C function needs DFTRACER_C_FUNCTION_START() as first statement
        - DFTRACER_C_FUNCTION_END() before every return (not before closing brace of void fns)
        - DFTRACER_C_FUNCTION_UPDATE_STR("name", value) for const char* params (filename, path…)
        - DFTRACER_C_FUNCTION_UPDATE_INT("name", value) for size_t/off_t/int params (size, fd…)
        - Do NOT annotate: struct definitions, typedefs, macro bodies, #ifdef guards
        - C++ uses DFTRACER_CPP_FUNCTION() (RAII, no END needed) + DFTRACER_CPP_FUNCTION_UPDATE

  3. session_build_annotated(run_id)
     → check artifacts/10_session_build_annotated.log

  4. If build succeeds: session_run_with_dftracer(run_id, command="<smoke_test_command>")
     → check artifacts/11_session_run_with_dftracer.log

  5. If run fails due to a runtime crash in annotated code:
     → read the failing file, remove the offending macro, rebuild, rerun

  6. Once run succeeds: session_split_traces → session_analyze_traces
```

**Prefer manual edits over tool calls when failing:** if `session_annotate_source`
produces errors on the same file across two attempts, use `session_read_file` +
`session_write_file` to hand-annotate that file rather than re-running the tool.

**Coverage check:** after a successful run, check how many functions in the annotated
source contain `DFTRACER_C_FUNCTION_START`. A file with zero START calls was either
skipped (header-only) or had its macros stripped during error recovery — re-annotate it
manually.
