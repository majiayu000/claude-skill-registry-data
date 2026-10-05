---
name: dftracer-annotate-process
description: The complete dftracer manual annotation process — 5 passes, coverage requirements, annotation_logs format, build prep, and mandatory Pass 5 review
---

## Manual Annotation Process (gradual, iterative)

`session_annotate_source` returns a **plan** — it does NOT write files.
Annotate manually using `session_read_file` + `session_write_file`.

---

## Coverage Requirement

**All storage backend functions MUST be annotated. Skipping due to difficulty is not acceptable.**

A function may only be permanently skipped if it qualifies under **Rule 0**
(trivial — getter/setter, ≤5 lines, no I/O, no data movement). Every other
function, regardless of complexity, MUST eventually be annotated.

**Storage backends that always require full annotation:**
- `aiori-POSIX.c` — POSIX_Create, POSIX_Open, POSIX_Xfer, POSIX_Close, POSIX_Delete,
  POSIX_Rename, POSIX_Fsync, POSIX_Sync, POSIX_GetFileSize, POSIX_Mknod
- `aiori-MPIIO.c` — MPIIO_Open, MPIIO_Xfer, MPIIO_Close, MPIIO_Delete, MPIIO_Fsync,
  MPIIO_GetFileSize
- `aiori-HDF5.c`, `aiori-NCMPI.c`, `aiori-DFS.c`, `aiori-S3*.c` — all I/O functions
- Any other `aiori-*.c` file — treat every non-trivial function as mandatory
- **Lifecycle functions always included:** `*_init`, `*_final`, `*_initialize`, `*_finalize`,
  `*_Sync`, `*_Fsync`, `*_Delete`, `*_Rename` — even if the body is short

**Mandatory POSIX backend function list:**
- `POSIX_Create`, `POSIX_Open`, `POSIX_Xfer`, `POSIX_Close`, `POSIX_Delete`
- `POSIX_Fsync`, `POSIX_Sync`, `POSIX_GetFileSize`, `POSIX_Mknod` (even if "deprecated")
- `POSIX_Rename`, `POSIX_Initialize`, `POSIX_Finalize`
- `gpfs_free_all_locks`, `gpfs_access_start`, `gpfs_access_end`, `gpfs_fineGrainWriteSharing`, `gpfs_fineGrainReadSharing`
- `beegfs_getStriping`, `beegfs_compatibleFileExists`, `beegfs_createFilePath`, `beegfs_isOptionSet`
- `lustre_disable_file_locks`

**Backend annotation order:**
1. POSIX / simplest reference backend
2. Wrapper backends (MMAP, AIO)
3. MPI-based backends (MPIIO, NCMPI)
4. High-level library backends (HDF5, NetCDF)
5. Distributed / cloud (HDFS, DFS, S3, CEPHFS, RADOS)
6. Specialized / research backends last

---

## annotation_logs/ Folder (mandatory — create before Pass 1)

```
workspaces/<run_id>/annotation_logs/
  annotation_process.log   ← running log of every action taken (append-only)
  annotation_status.md     ← per-function status table (update after every function)
  annotation_report.md     ← final summary (written after all passes complete)
```

### annotation_process.log format

```
[PASS1] src/ior.c — added INIT/FINI/START/END — build: SUCCESS
[PASS2] src/aiori-POSIX.c — POSIX_Create — START+END×2+UPDATE×2 — build: SUCCESS
[PASS2] src/aiori-MPIIO.c — MPIIO_Xfer — attempt 1 FAILED: data_fn undeclared
[PASS2] src/aiori-MPIIO.c — MPIIO_Xfer — attempt 2 — fixed END order — build: SUCCESS
[SKIP]  src/aiori-POSIX.c — POSIX_options — Rule 0: trivial, no I/O
[ERROR] src/aiori-MPIIO.c — MPIIO_Open — FAILED 2× — kept include-only — PENDING RETRY
```

### annotation_status.md format

```markdown
# Annotation Status — <run_id>

## Storage Backends (mandatory coverage)

| File | Function | Status | comp | Traced in Test | Attempts | Notes |
|------|----------|--------|------|----------------|----------|-------|
| aiori-POSIX.c | POSIX_Create | ✅ DONE | io | ✅ 2 events | 1 | START+END×2+UPDATE |
| aiori-POSIX.c | gpfs_access_start | ✅ DONE | io | ⚠️ no GPFS | 1 | #ifdef guarded |
| aiori-MPIIO.c | MPIIO_Open | ⚠️ PENDING | — | — | 2 | complex control flow |

## Skipped (Rule 0 — permanent)

| File | Function | Reason |
|------|----------|--------|
| aiori-POSIX.c | POSIX_options | Trivial option helper, no I/O |
```

Status values:
- `✅ DONE` — annotated and build passes
- `⚠️ PENDING` — not yet annotated or annotation failed; MUST be retried
- `❌ INCLUDE-ONLY` — only `#include` added; annotation failed and was reset; MUST retry
- `⏭️ SKIPPED (Rule 0)` — permanently exempt

---

## Build Prep — BEFORE Pass 1 (Makefile patching)

```bash
INSTALL_ANN=<workspace>/install_ann

# Patch src/Makefile (not just the top-level)
sed -i "s|^CFLAGS = |CFLAGS = -I${INSTALL_ANN}/include |" annotated/src/Makefile
sed -i "s|^LIBS = |LIBS = -ldftracer_core -lcpp-logger -lbrahma |" annotated/src/Makefile
sed -i "s|^LDFLAGS = |LDFLAGS = -L${INSTALL_ANN}/lib -Wl,-rpath,${INSTALL_ANN}/lib |" annotated/src/Makefile

# Clean stale dependency files — ALWAYS after a Makefile patch
rm -rf annotated/.deps annotated/src/.deps && make -C annotated clean
```

---

## Pass 1 — INIT and FINI in main (entry files only)

1. Read the file with `session_read_file`
2. Add `#include <dftracer/dftracer.h>` after the last existing `#include`
3. Check for `MPI_Init` or `MPI_Init_thread`:
   - **No MPI**: `DFTRACER_C_INIT(NULL, NULL, NULL);` as first statement after `{` of main
   - **Has MPI**: `DFTRACER_C_INIT(NULL, NULL, NULL);` immediately AFTER the `MPI_Init(...)` call
4. Before every `return` in main AND before any `exit()`/`abort()`/`MPI_Abort()`:
   - C (no MPI): `DFTRACER_C_FINI();`
   - C (with MPI): `DFTRACER_C_FINI();` then `MPI_Finalize();` then `return`
5. **If code has explicit DFTRACER_C_INIT(), do NOT set DFTRACER_INIT=1 in the env**
6. Write the file, build, fix errors, log to `annotation_process.log`.

---

## Pass 2 — FUNCTION_START and FUNCTION_END

For each backend file, work through ALL I/O functions — start with the simplest:

1. Read the file.
2. For each function: apply Rule D (skip only pure getters/setters ≤5 lines with no I/O).
3. Determine `comp` type BEFORE writing any macro: `"io"`, `"mem"`, `"cpu"`, or `"comm"`.
4. Annotate the function:
   a. Count VISIBLE `return` statements: `grep -n "return" <function_lines>`
   b. Identify multi-line signatures by scanning upward from `{`
   c. Insert `DFTRACER_C_FUNCTION_START();` as FIRST statement after `{`
   d. Insert `DFTRACER_C_FUNCTION_UPDATE_STR("comp", "<type>");` immediately after START
   e. Insert `DFTRACER_C_FUNCTION_END();` before every VISIBLE `return`
   f. For goto-based error handling: single END at the goto label
   g. For void functions: END as last statement before `}`
5. Write the file, run `rm -rf .deps src/.deps` if Makefile was touched, then build.
6. **On failure**: do NOT reset and skip. Fix the specific macro. Only after 3 attempts should you reset to include-only.
7. Log every attempt to `annotation_process.log`.
8. Update `annotation_status.md` (including `comp` column) after every function.
9. **After every file** — run coverage verification:
   ```bash
   grep -c "DFTRACER_C_FUNCTION_START"               annotated/src/foo.c
   grep -c 'DFTRACER_C_FUNCTION_UPDATE_STR.*"comp"'  annotated/src/foo.c
   # Counts must be equal
   ```

---

## Pass 3 — FUNCTION_UPDATE for I/O metadata

For functions with meaningful I/O parameters:
- `DFTRACER_C_FUNCTION_UPDATE_STR("name", param)` for `const char *` params
- `DFTRACER_C_FUNCTION_UPDATE_INT("name", (int)param)` for numeric params
- Always read parameter names from the **definition**, not a forward declaration.

---

## Pass 4 — Retry PENDING / INCLUDE-ONLY functions

1. Read the function carefully — treat it as a fresh annotation.
2. For complex control flow (switch/case, nested MPI error checks, multi-return):
   - List every exit path before writing any macro
   - For `switch`: place END before each `case`'s `break` or `return`
3. Build after each retry.
4. If it passes: update status to `✅ DONE`.
5. If it fails again: ask the user for guidance, then add a pitfall entry.

---

## Key safety rules for every pass

- Verify line count: annotated file must have MORE lines than original
- Work one function at a time — build after every function in complex files
- After Makefile changes: always `rm -rf .deps src/.deps` before rebuilding
- Never move to the next function while the current file has compile errors
- Update `annotation_status.md` after every function — do not batch updates

---

## After all passes — mandatory artifacts

```bash
diff -urN source/ annotated/ > workspaces/<run_id>/annotation.patch
```

Also write `annotation_logs/annotation_report.md` with:
- Total files modified, lines added, macros inserted
- Per-pass build history
- Table of annotated functions (file, function, macros, notes)
- Table of skipped functions (file, function, reason — Rule 0 only)
- Table of INCLUDE-ONLY functions with retry plan

---

## Pass 5 — Review, Confirm, and Extract Rules (MANDATORY — do not skip)

### Step 1 — Present the coverage summary to the user

Show the user these three tables from `annotation_status.md` inline:
1. **Coverage Summary table**
2. **Annotated functions table** — all rows with ✅ DONE
3. **Skipped/Rule-0 table**

Ask explicitly:
> "Annotation complete. Please review:
> - Are there any functions in the Skipped list that you think should be annotated?
> - Are any functions in the Annotated list incorrect (wrong comp type, wrong macros)?
> Reply 'confirmed' to proceed, or tell me what to fix."

**Do not proceed to Step 2 until the user replies 'confirmed'.**

### Step 2 — Extract new rules from the session log

Read `annotation_logs/annotation_process.log` and extract every pattern that meets ANY criterion:
- A function was initially skipped/missed and had to be added later
- A build failed and required a specific fix
- A comp type was wrong and had to be corrected
- A macro was placed wrong
- A new function category was discovered
- A user correction during the review step

For each extracted pattern, add a pitfall entry to `.goose/hints/02-annotation-pitfalls.md`.

### Step 3 — Update the cheatsheet coverage verification commands

Check whether the coverage verification commands in `00-critical-cheatsheet.md`
would have caught the new pattern. If not, add a new check command.

### Step 4 — Write the rule-update log

```
[RULES] <date> — extracted N new rules from session
  - pitfalls added: <list>
  - mandatory list updates: <functions added>
  - cheatsheet updates: <section updated>
```

**The session is not complete until Steps 1–4 are done.**
