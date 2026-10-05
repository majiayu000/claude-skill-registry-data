---
name: dftracer-pipeline
description: >
  Interactive dftracer annotation pipeline.
  Clones the app, builds it, annotates all source files using the
  clang-based MCP annotation tools (clang_annotate_project /
  clang_annotate_file + clang_syntax_check + clang_lint_annotations),
  builds the annotated version, runs a smoke test, collects traces,
  and produces optimization proposals.
---

Lessons file: /workspaces/dftracer-agents/.agents/skills/dftracer-annotation-lessons/SKILL.md

Read the lessons file before doing anything else. Apply every lesson that
matches the current app or language.

══════════════════════════════════════════════════════════════════════
!! ANNOTATION MODE — MANDATORY RULE (READ BEFORE ANY OTHER STEP) !!
══════════════════════════════════════════════════════════════════════

ALWAYS annotate using MCP clang tools. NEVER do manual annotation.

  CORRECT flow:
    1. clang_annotate_project()         ← primary: annotates all files at once
    2. clang_syntax_check() per file    ← validation
    3. clang_lint_annotations() per file← validation
    4. If check/lint FAILS for a specific function → call clang_annotate_file()
       with that function excluded or with comp_overrides to correct it.
       This is "manual correction" — targeted, single-function only.

  FORBIDDEN at all times (do NOT do these, ever):
    ✗ Read a source file → manually compose macros → Write/Edit the file
    ✗ Use Bash gcc/g++ -fsyntax-only to check annotations
    ✗ Call session_annotate_c_file / session_annotate_cpp_file (deprecated)
    ✗ Rewrite or re-annotate an entire file with Edit/Write tools
    ✗ Fall back to "manual mode" when an MCP call fails — instead, re-call
      clang_annotate_file() for only the failing function with overrides.

  If clang_annotate_project itself fails to run (tool error, not annotation
  error): diagnose the tool error, do NOT switch to manual annotation.
  Report the tool failure to the user and stop.

══════════════════════════════════════════════════════════════════════

══════════════════════════════════════════════════════════════════════
STEP 1 — GATHER INPUTS  (if not supplied via arguments)
══════════════════════════════════════════════════════════════════════

If the user invoked this with named arguments (run_id=…, url=…, etc.),
use those directly. Otherwise ask one question at a time and wait:

  Q1: "What is the Git URL of the application you want to annotate?"
      → Store as APP_URL.

  Q2: "Which branch or tag? (default: main)"
      → Store as REF (use "main" if blank).

  Q3: "Smoke test command? (leave blank to auto-detect)"
      → Store as SMOKE_CMD.

  Q4: "Extra CMake/configure build flags? (leave blank to skip)"
      → Store as EXTRA_FLAGS.

If a run_id was supplied skip Q1–Q4 and jump to Step 3.

Print: "Starting pipeline for <APP_URL> @ <REF>"


══════════════════════════════════════════════════════════════════════
STEP 2 — SESSION SETUP  (MCP tools)
══════════════════════════════════════════════════════════════════════

2a. Create session and build the original source:

    session_create(url=APP_URL, ref=REF)
    → store RUN_ID, WS (workspace path)

2b. Validate HDF5 version (only if project uses HDF5):

    h5cc --version 2>/dev/null || h5dump --version 2>/dev/null || \
      pkg-config --modversion hdf5 2>/dev/null

    dftracer-compatible HDF5 versions (exact series only):
      1.8.23  |  1.10.5  |  1.12.3  |  1.14.5 (preferred)

    If the system HDF5 is NOT in one of these series:
      - Build HDF5 1.14.5 from source into <WS>/hdf5_1.14/ (see dftracer-install skill)
      - Add "-DHDF5_DIR=<WS>/hdf5_1.14" to EXTRA_FLAGS for all cmake steps
      - Set HDF5_DIR and LD_LIBRARY_PATH in every subsequent shell command

    The MCP session_detect tool reports hdf5_system.compatible=true/false and
    hdf5_system.recommended with the preferred patch release for the detected series.

2c. Configure + build the original source:

    session_configure(run_id=RUN_ID, extra_cmake_flags=EXTRA_FLAGS)
    session_build_install(run_id=RUN_ID)

2c. Install dftracer into the session (cmake mode, with MPI + HDF5
    auto-detected from the project source):

    session_install_dftracer(run_id=RUN_ID)

    On failure → print the cmake/pip error and stop.

2d. Copy source to annotated/ workspace:

    session_copy_annotated(run_id=RUN_ID)

2e. Baseline annotated build (no macros yet — verifies the build
    system patch works before any annotation):

    session_build_annotated(run_id=RUN_ID,
      extra_cmake_flags=<same flags as 2b>)

    On failure → show cmake/make errors and stop.

Print: "Setup complete. RUN_ID=<RUN_ID>  Baseline build PASSED."


══════════════════════════════════════════════════════════════════════
STEP 3 — WHOLE-PROJECT ANNOTATION  (clang MCP tools)
══════════════════════════════════════════════════════════════════════

The preferred path is a single project-level call that discovers all
C/C++ files, determines entry points, filters trivial functions by AST
cost, and inserts macros in bottom-to-top line order:

    clang_annotate_project(
      run_id      = RUN_ID,
      language    = "c",          # or "cpp" for C++ projects
      init_args   = "NULL, NULL, NULL",
      exclude_patterns = ["test/", "tests/", "vendor/", "third_party/"]
    )

This call:
  • Discovers every .c / .cpp / .cxx / .cc under annotated/
  • Skips files matching exclude_patterns (plus the always-excluded
    /CMakeFiles/, /.git/ paths)
  • Annotates library/inner files first (is_entry=False)
  • Annotates entry-point files last (is_entry=True) so INIT/FINI land
    around main()
  • For each file, internally calls clang_extract_functions to get an
    authoritative function map, then clang_estimate_function_cost per
    function to decide annotate vs. skip (score ≥ 20 or lifecycle rule)
  • Inserts macros in a single in-memory pass (no intermediate writes)
  • Writes each file exactly once via clang_write_annotated_file

Print the result: number of files annotated, functions annotated vs skipped.

### When to use per-file annotation instead

If clang_annotate_project reports errors for specific files, OR if you
need comp= overrides for particular functions, switch to per-file mode
for those files only:

    # 1. Extract the function map
    clang_extract_functions(run_id=RUN_ID, filepath=<file>)

    # 2. For any function where you want to override the auto comp:
    clang_estimate_function_cost(run_id=RUN_ID, filepath=<file>,
      function_name=<name>)
    # → review the cost_info and decide comp= category manually

    # 3. Annotate the file with optional overrides
    clang_annotate_file(
      run_id         = RUN_ID,
      filepath       = <file>,
      is_entry       = <True if file contains main()>,
      language       = "c",        # or "cpp"
      init_args      = "NULL, NULL, NULL",
      comp_overrides = '{"fn_name": "comm", "other_fn": "io"}'
    )
    # clang_annotate_file writes the file in one in-memory pass;
    # call clang_write_annotated_file only if the tool says it is
    # needed to flush (check the response).

Do NOT manually read files, insert macros with Edit/Write, or run
shell `gcc -fsyntax-only` commands. All of that is handled by the
MCP tools.


══════════════════════════════════════════════════════════════════════
STEP 4 — PER-FILE VALIDATION  (clang MCP tools)
══════════════════════════════════════════════════════════════════════

After annotation (project-level or per-file), validate every annotated
C/C++ file using the two MCP validation tools. Run both for each file:

    clang_syntax_check(run_id=RUN_ID, filepath=<file>)
    clang_lint_annotations(run_id=RUN_ID, filepath=<file>)

clang_syntax_check rules:
  • Uses the real gcc/g++ front-end with a dftracer stub header and
    the session's MPI + dftracer include paths — no manual -I flags needed.
  • PASS → move to next file.
  • FAIL → fix ONLY the exact lines named in the compiler error output:
      - Extract function name and line number from "error:" lines.
      - Call clang_annotate_file again for ONLY that function using
        comp_overrides (e.g. to skip it or override the comp= value).
      - NEVER rewrite the whole file manually. NEVER touch functions
        that already pass syntax check.
      - Retry clang_syntax_check. Max 2 targeted fixes per file.
      - On 2nd failure: strip the single failing function's macros by
        re-calling clang_annotate_file with that function excluded, then
        mark it as PENDING in a comment. Move on.

clang_lint_annotations rules check:
  L1 — DFTRACER_C_INIT before DFTRACER_C_FUNCTION_START in main()
  L2 — comp= UPDATE_STR within 3 lines after every START
  L3 — DFTRACER_C_FINI before MPI_Finalize in main()
  L4 — no END immediately before MPI_CHECK / NCMPI_CHECK
  L5 — no END at global scope

  LINT violations → use clang_insert_line to fix ONLY the reported line;
  never re-annotate the whole file. Then re-lint to verify.

Print per-file status: ✓ <file>  (<n> functions annotated, lint PASSED)


══════════════════════════════════════════════════════════════════════
STEP 5 — BUILD ANNOTATED VERSION  (MCP tools)
══════════════════════════════════════════════════════════════════════

5a. Detect explicit INIT usage to determine DFTRACER_INIT mode:

    INIT_COUNT=$(grep -r "DFTRACER_C_INIT\|DFTRACER_CPP_INIT\|DFTracer.initialize_log" \
      <WS>/annotated/ 2>/dev/null | wc -l)
    FINI_COUNT=$(grep -r "DFTRACER_C_FINI\|DFTRACER_CPP_FINI\|dftracer.finalize_log" \
      <WS>/annotated/ 2>/dev/null | wc -l)

    INIT_COUNT > 0 AND FINI_COUNT > 0 → DFTRACER_INIT_ENV = {"DFTRACER_INIT": "HYBRID"}
      (source has both INIT and FINI: function profiling + I/O interception)

    INIT_COUNT > 0 AND FINI_COUNT == 0 → DFTRACER_INIT_ENV = {"DFTRACER_INIT": "PRELOAD"}
      (missing FINI — HYBRID would leave traces open; fall back to preload-only)

    INIT_COUNT == 0 → DFTRACER_INIT_ENV = {"DFTRACER_INIT": "PRELOAD"}
      (no annotations — preload-only I/O interception)

    Important: NEVER set DFTRACER_INIT=0 — it disables POSIX-level
    tracing. Valid values: HYBRID (annotated source with both INIT+FINI),
    PRELOAD (transparent I/O only, no annotations), FUNCTION (annotations only,
    no I/O interception). All values are CASE-SENSITIVE uppercase strings.

5b. Build and install annotated version:

    session_build_annotated(run_id=RUN_ID,
      extra_cmake_flags=<same flags as 2b>)

    On failure:
      1. Extract failing function(s) from the compiler error.
      2. Re-annotate only those files using clang_annotate_file with
         the failing function excluded (add it to comp_overrides with
         a sentinel, or use exclude).
      3. Re-run syntax check + lint for the fixed file.
      4. Retry session_build_annotated. Max 2 retries.
      5. If still failing → escalate to user with exact error lines.

5c. Run smoke test:

    session_run_smoke_test(run_id=RUN_ID, command=SMOKE_CMD,
      subfolder="build_ann")

    MPI/OpenMPI as root? Add env:
      OMPI_ALLOW_RUN_AS_ROOT=1, OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

    On failure: if DFTRACER symbols in error → re-annotate + retry.
    Otherwise ask: "Smoke test failed (non-annotation issue). Continue? [yes/stop]"


══════════════════════════════════════════════════════════════════════
STEP 6 — ANNOTATION REPORT + USER CONFIRMATION
══════════════════════════════════════════════════════════════════════

    session_annotation_report(run_id=RUN_ID)

Print:
  ┌─────────────────────────────────────────────────────────┐
  │  ANNOTATION REPORT — <RUN_ID>                           │
  │  Files:     <n> annotated                               │
  │  Functions: <annotated> / <eligible>  skipped: <n>      │
  │  comp:  io=<n>  comm=<n>  mem=<n>  cpu=<n>             │
  │  Build: PASSED   Smoke test: PASSED                     │
  │  Annotated source: workspaces/<RUN_ID>/annotated/       │
  └─────────────────────────────────────────────────────────┘

Ask: "Proceed with dftracer trace run? [yes / no / fix <file> <feedback>]"

  "no"  → stop, print artifact location.
  "fix <file> <feedback>" → re-annotate that file using clang_annotate_file
           with comp_overrides derived from the feedback, re-run lint +
           syntax check, rebuild, re-run smoke test, show updated report,
           ask again.
  "yes" → continue to Step 7.


══════════════════════════════════════════════════════════════════════
STEP 7 — TRACE COLLECTION + ANALYSIS  (MCP tools)
══════════════════════════════════════════════════════════════════════

7a. Create the trace output subdirectory before running:

    mkdir -p <WS>/traces/<app_name>

    (where app_name = first component of RUN_ID before "/")

7b. Run with dftracer:

    session_run_with_dftracer(run_id=RUN_ID, command=SMOKE_CMD,
      subfolder="build_ann",
      env_extra={**DFTRACER_INIT_ENV,
                 "DFTRACER_ENABLE": "1",
                 "DFTRACER_INC_METADATA": "1"},
      data_dir="all")

    Always use data_dir="all" so no I/O path is excluded from tracing.
    Always set DFTRACER_INC_METADATA=1 so UPDATE_STR/UPDATE_INT metadata
    (comp=, filename=, count=) is captured in the trace events.
    Always set DFTRACER_ENABLE=1 to ensure trace files are written.

7c. Copy trace files up to the parent traces/ dir if needed
    (run_id subdirectory layout):

    cp <WS>/traces/<app_name>/*.pfw.gz <WS>/traces/ 2>/dev/null || true

7d. Split and analyze:

    APP_NAME = first component of RUN_ID
    session_split_traces(run_id=RUN_ID, app_name=APP_NAME)
    session_analyze_traces(run_id=RUN_ID, query_type="summary")


══════════════════════════════════════════════════════════════════════
STEP 8 — OPTIMIZATION PIPELINE  (MCP tools)
══════════════════════════════════════════════════════════════════════

Ask: "Generate optimization proposals? [yes / no]"

If yes:

8a. Run the baseline iteration loop (profiling + diagnosis + literature search):

    session_optimization_iteration(run_id=RUN_ID, command=SMOKE_CMD,
      app_name=APP_NAME, data_dir="all",
      env_extra=DFTRACER_INIT_ENV,
      optimization_applied="baseline", rebuild=False)

    This runs the benchmark, splits traces, diagnoses bottlenecks AND
    searches arXiv/Semantic Scholar for papers relevant to each bottleneck.
    Repeat for each optimization iteration.

8b. Generate citation-backed proposals from the iteration results:

    session_generate_optimization_proposals(run_id=RUN_ID, iteration=-1)

    This maps each diagnosed bottleneck to concrete L1/L2/L3 proposals
    backed by papers found in 8a.

    CRITICAL: Every optimization proposal MUST be backed by a paper citation.
    Papers are not rejected by age but are scored and ranked — the
    highest-ranked paper for each bottleneck becomes the citation.

8b-i. PAPER RELEVANCE SCORING

    For every candidate paper, compute a composite relevance score (0–100):

      score = bottleneck_score + system_score + recency_score

    Component definitions:

      bottleneck_score (0–50):
        How directly does the paper address the specific bottleneck metric?
        • 50 — paper directly studies this metric or the exact I/O pattern
                (e.g., paper on "POSIX close latency in HDF5 timestep writes")
        • 35 — paper addresses the broader I/O category
                (e.g., "collective metadata performance in parallel I/O")
        • 20 — paper addresses an adjacent technique that indirectly applies
                (e.g., "MPI-IO collective buffering" for a metadata bottleneck)
        •  0 — paper is topically unrelated to the bottleneck

      system_score (0–30):
        How well does the paper match the target system/software stack?
        • 30 — same library/runtime (e.g., paper uses HDF5 + ROMIO on MPI)
        • 20 — same storage tier or middleware class (e.g., parallel filesystem,
                object store, two-phase I/O)
        • 10 — same application domain (e.g., scientific HPC I/O, checkpoint)
        •  0 — different system class (e.g., cloud-only, database, in-memory)

      recency_score (0–20):
        age_years = current_year - publication_year
        • 20 — age_years ≤ 2
        • 15 — age_years ≤ 5
        • 10 — age_years ≤ 10
        •  5 — age_years ≤ 15
        •  0 — age_years > 15

    Rank all candidate papers by score descending.
    Use the top-ranked paper (highest score) as the primary citation for each
    bottleneck. If the top paper scores < 20 total, add a second search pass
    before accepting it.

8b-ii. PAPER SEARCH PROCEDURE

    If session_generate_optimization_proposals returns empty or unsupported
    bottlenecks, search manually:

      dftracer__search_arxiv / dftracer__search_semantic_scholar with queries:
        - Bottleneck metric name + I/O domain
          (e.g., "posix close latency HDF5 parallel I/O")
        - Broader technique synonyms
          (e.g., "collective buffering MPI-IO", "metadata caching HDF5")
        - System-specific terms from the stack
          (e.g., "ROMIO two-phase I/O", "Lustre striping checkpoint")

      Score every result using the rubric above.
      If top score < 20 after 3 searches → state:
        "Best available citation scores <N>/100 for this bottleneck
         (title: <title>, year: <year>). Proceeding with caveat."
      NEVER propose an optimization with zero candidate papers.

8c. Present proposals in this format (one per bottleneck, top-ranked citation):

    ┌─────────────────────────────────────────────────────────────┐
    │  OPTIMIZATION PROPOSAL — <bottleneck> (<severity>)          │
    ├─────────────────────────────────────────────────────────────┤
    │  Evidence: <paper title>, <authors>, <year>                 │
    │  URL: <arxiv or doi url>                                    │
    │  Relevance score: <N>/100  (bottleneck=N, system=N, age=N) │
    ├─────────────────────────────────────────────────────────────┤
    │  L1 (application):  <specific code/config change>           │
    │  L2 (middleware):   <library/runtime tuning>                │
    │  L3 (filesystem):   <storage/system config change>          │
    └─────────────────────────────────────────────────────────────┘

8d. ITERATIVE OPTIMIZATION LOOP  (max 10 iterations)

    Run up to 10 full optimization cycles. Each cycle applies ALL THREE
    layers (L1 → L2 → L3) then re-profiles to discover new bottlenecks.
    Stop early only if the termination conditions in 8f are met.

    Maintain a loop state table across iterations:

      ITER  | applied_opts          | new_bottlenecks | resolved | raw_rate
      ------|-----------------------|-----------------|----------|----------
      0     | baseline              | <list>          | —        | <val>
      1     | <L1+L2+L3 changes>    | <list>          | <list>   | <val>
      ...

    For each iteration i = 1 … 10:

    8d-i.  Apply all three layers in sequence:

        session_optimize_l1_app(run_id=RUN_ID)
        session_optimize_l2_software(run_id=RUN_ID)
        session_optimize_l3_filesystem(run_id=RUN_ID)

        If any layer reports "no applicable optimizations", record that
        layer as exhausted for this iteration but still run the remaining
        layers. Do NOT skip the re-profile step.

    8d-ii. Re-profile with the applied changes:

        session_optimization_iteration(run_id=RUN_ID, command=SMOKE_CMD,
          app_name=APP_NAME, data_dir="all",
          env_extra=DFTRACER_INIT_ENV,
          optimization_applied="iter-<i>: L1+L2+L3",
          rebuild=True)

        This rebuilds the annotated binary, runs the benchmark, splits
        traces, diagnoses bottlenecks, and searches for new papers.
        Store the trace path for this iteration as TRACE_ITER_<i>.

    8d-iii. Compare this iteration against the previous one using the
        dftracer comparator MCP tool:

        comparator(
          trace_a = TRACE_ITER_<i-1>,   # previous iteration's trace path
          trace_b = TRACE_ITER_<i>       # current iteration's trace path
        )

        The comparator output includes per-metric deltas (improved /
        regressed / unchanged) and a ranked list of changes. Use this
        output — not manual arithmetic — as the authoritative source for:
          • Which bottlenecks were resolved between iterations
          • Which metrics worsened (regression check for 8e)
          • The raw rate and observed completion time delta to show in
            the loop state table

        For the baseline comparison (i = 1), use TRACE_ITER_0 as trace_a.

    8d-iv. Generate updated proposals for newly surfaced bottlenecks:

        session_generate_optimization_proposals(run_id=RUN_ID, iteration=i)

        Score and rank candidate papers per 8b-i. Present any new
        proposals using the format in 8c. Skip bottlenecks that were
        already fully addressed in a prior iteration (no new proposals
        means no proposal box for that bottleneck).

    8d-v. Update the loop state table and print a one-line delta summary
        derived from the comparator output:

        "Iter <i>: resolved=<n> bottlenecks, new=<m>, raw_rate <before>→<after> GB/s (comparator: <overall verdict>)"

8e. Check termination conditions after each iteration:

    Stop the loop early (before reaching 10 iterations) if ANY of:

      EXHAUSTED  — All three layers report "no applicable optimizations"
                   for every active bottleneck in this iteration.
      CONVERGED  — No new bottlenecks surfaced AND no resolved bottlenecks
                   changed severity compared to the previous iteration.
      REGRESSED  — The comparator reports that raw write rate or observed
                   completion time worsened by > 5% versus the previous
                   iteration. Use the comparator's metric delta output as
                   the authoritative source — do not recompute manually.
                   (Roll back the last iteration's changes, mark as
                   "regressed", and stop.)
      MAX_ITERS  — 10 iterations completed.

    On stopping, print the reason:
      "Optimization loop ended after <i> iterations: <reason>"

8f. Final all-layers summary after the loop:

    Print the completed loop state table (all iterations).
    Identify the iteration with the best raw write rate as the
    "recommended configuration" and note which optimizations it includes.


══════════════════════════════════════════════════════════════════════
STEP 9 — UPDATE LESSONS LEARNED
══════════════════════════════════════════════════════════════════════

Append any new pitfalls discovered this session to the lessons file.
Format:

  ---
  date: YYYY-MM-DD
  app: <APP_URL>
  context: <one-line description>
  error: |
    <exact error or key excerpt>
  root_cause: <why it happened>
  fix: |
    <exact steps or rule>
  tags: [c|cpp|python, annotation, <keyword>]
  ---

Do not duplicate entries already present.


══════════════════════════════════════════════════════════════════════
STEP 10 — SESSION REPORT
══════════════════════════════════════════════════════════════════════

Generate a Markdown session report and write it to
<WS>/session_report.md using the Write tool.

The report MUST follow this exact structure:

---

# DFTracer Session Report — <RUN_ID>

**Application:** <APP_URL> @ <REF>  
**Date:** <YYYY-MM-DD>  
**Platform:** <OS / arch / HPC system>

---

## What Ran Correctly (Pipeline Flow)

Document each step that succeeded as a numbered flow:

1. **Session setup** — cloned <URL>, built with <build_tool>
2. **dftracer install** — version <X.Y.Z>, installed to <path>
3. **Source copy** — <N> files copied to annotated/
4. **Annotation** — <N> files annotated (<M> functions), <K> skipped
5. **Build** — annotated binary built successfully at <path>
6. **Smoke test** — ran `<command>`, completed in <time>
7. **Trace collection** — <N> trace files, <M> events, <K> KB
8. **Trace analysis** — bottlenecks found: <list>
9. **Optimization loop** — <N> iterations (stopped: <reason>); best speedup at iter <K>

Include the full iteration table:

| Iter | L1 applied | L2 applied | L3 applied | New bottlenecks | Resolved | Raw rate |
|------|-----------|-----------|-----------|-----------------|----------|----------|
| 0    | baseline  | baseline  | baseline  | <list>          | —        | <val>    |
| 1    | <change>  | <change>  | <change>  | <list>          | <list>   | <val>    |
| …    |           |           |           |                 |          |          |

For each iteration's applied optimizations, include a sub-section:

### Iteration <N> — <L1/L2/L3 summary>
- **L1 (app):** <code or config change>
- **L2 (middleware):** <library/runtime tuning>
- **L3 (filesystem):** <storage/system config>
- **Evidence:** <paper title>, <authors>, <year>, score=<N>/100 — <URL>
- **Result:** Before: <metric=val>, After: <metric=val>, Δ = <pct>%
- **Stop reason (if last iter):** <EXHAUSTED / CONVERGED / REGRESSED / MAX_ITERS>

---

## Lessons Learned (Pitfalls)

For each pitfall encountered, include a sub-section:

### Pitfall: <short title>
- **Step:** <which pipeline step this occurred in>
- **Error:** (verbatim excerpt from compiler/linker/runtime output)
  ```
  <error text>
  ```
- **Root cause:** <one paragraph explaining why it happened>
- **Fix:** <exact commands or code changes that resolved it>
- **Lesson added to:** <path to lessons file> as tag `<tag>`

---

## Summary

| Category | Value |
|---|---|
| Files annotated | <N> |
| Functions annotated | <N> |
| Bottlenecks diagnosed | <N> (high: N, medium: N) |
| Optimization iterations | <N> (max 10, stopped: <reason>) |
| Optimizations applied | <N> (L1=N, L2=N, L3=N) |
| Raw write rate improvement | <pct>% |
| Observed completion improvement | <pct>% |
| Papers cited (avg relevance score) | <N> (avg <X>/100) |
| Pitfalls resolved | <N> |

---

## Artifacts

| Artifact | Path |
|---|---|
| Annotated source | workspaces/<RUN_ID>/annotated/ |
| Annotated build | workspaces/<RUN_ID>/build_ann/ |
| Trace files | workspaces/<RUN_ID>/traces/ |
| Split traces | workspaces/<RUN_ID>/traces_split/ |
| Session report | workspaces/<RUN_ID>/session_report.md |

---

After writing session_report.md, print its path and a one-line summary
of the key result (e.g., "Raw write rate improved X% via collective I/O
and ROMIO collective buffering — see <path> for full report").


══════════════════════════════════════════════════════════════════════
TOOL REFERENCE
══════════════════════════════════════════════════════════════════════

| Purpose                          | MCP Tool                        |
|----------------------------------|---------------------------------|
| Create session + clone           | session_create                  |
| Configure original build         | session_configure               |
| Build + install original         | session_build_install           |
| Install dftracer (C/C++ cmake)   | session_install_dftracer        |
| Copy source → annotated/         | session_copy_annotated          |
| Annotate entire project at once  | clang_annotate_project          |
| Annotate one file (with overrides)| clang_annotate_file            |
| Extract function map + line #s   | clang_extract_functions         |
| Estimate per-function cost       | clang_estimate_function_cost    |
| Compiler syntax check            | clang_syntax_check              |
| Lint macro ordering              | clang_lint_annotations          |
| Flush in-memory buffer to disk   | clang_write_annotated_file      |
| Build annotated version          | session_build_annotated         |
| Run smoke test                   | session_run_smoke_test          |
| Annotation coverage report       | session_annotation_report       |
| Run with dftracer tracing        | session_run_with_dftracer       |
| Split trace files                | session_split_traces            |
| Analyze traces                   | session_analyze_traces          |
| Search optimization papers       | session_search_optimization_papers |
| Generate optimization proposals  | session_generate_optimization_proposals |
| Apply L1 app optimizations       | session_optimize_l1_app         |
| Apply L2 software optimizations  | session_optimize_l2_software    |
| Apply L3 filesystem optimizations| session_optimize_l3_filesystem  |
| Compare two trace runs           | comparator                      |

NEVER use:
  • Read / Write / Edit tools to manually insert macros into source files
  • Bash `gcc -fsyntax-only` — use clang_syntax_check instead
  • session_annotate_c_file / session_annotate_cpp_file — superseded by
    clang_annotate_file and clang_annotate_project


══════════════════════════════════════════════════════════════════════
ANNOTATION RULES QUICK REFERENCE
══════════════════════════════════════════════════════════════════════

These are enforced automatically by clang_annotate_file/project but
apply when you use comp_overrides:

  comp= "io"   — POSIX I/O, HDF5, NetCDF, MPI-IO file ops, lifecycle fns
  comp= "comm" — MPI wrappers, network, S3, HDFS, RADOS, DFS
  comp= "mem"  — memcpy, malloc/free of large buffers, mmap setup
  comp= "cpu"  — checksums, compression, encryption, hashing

  ALWAYS annotate (never apply score filter):
    • Lifecycle: *_init, *_final, *_initialize, *_finalize
    • Sync/flush: *_fsync, *_flush, *_sync
    • File ops:   *_delete, *_rename, *_stat, *_mknod, *_getfilesize
    • Vendor FS:  gpfs_*, beegfs_*, lustre_*, hdfs_*, ceph_*, daos_*

  Score ≥ 20 (from clang_estimate_function_cost) → annotate
  Score < 20 and not lifecycle/vendor → skip

  INIT/FINI placement in main() (enforced by is_entry=True):
    DFTRACER_C_INIT(NULL, NULL, NULL)  ← before FUNCTION_START
    DFTRACER_C_FUNCTION_START()
    DFTRACER_C_FUNCTION_UPDATE_STR("comp", "cpu")
    ... benchmark work ...
    DFTRACER_C_FUNCTION_END()
    DFTRACER_C_FINI()                 ← after all benchmark work
    MPI_Finalize();                   ← FINI must precede MPI_Finalize
