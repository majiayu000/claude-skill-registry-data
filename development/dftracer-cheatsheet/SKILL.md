---
name: dftracer-cheatsheet
description: Critical annotation rules, corner cases, and top-10 known mistakes for dftracer — read this before every annotation session
---

## Annotation Quick Reference — Critical Rules, Corner Cases, Known Mistakes

Read this first. Every item here is drawn from a real session failure or a
rule that is commonly missed. Details and code examples are in the topic files.

---

## CRITICAL — Violations cause build failures or silent empty traces

| # | Rule | What breaks | Detail |
|---|------|-------------|--------|
| C1 | `DFTRACER_C_FUNCTION_START()` must be the **first statement after `{`**, never before it | Syntax error | C Rule 1 |
| C2 | `DFTRACER_C_FUNCTION_END()` must be **before every `return`**, never after it | Unreachable code / missing span | C Rule 2 |
| C3 | `DFTRACER_C_FUNCTION_UPDATE_STR("comp", "<type>")` is **mandatory immediately after START** — never skip it | Trace analysis can't group functions | C Rule 4, Pitfall: comp= |
| C4 | **Never annotate a forward declaration** — only the definition with a `{...}` body | Syntax error | C Rule 7, Pitfall: POSIX_Xfer |
| C5 | If code has `DFTRACER_C_INIT()`, **do NOT set `DFTRACER_INIT=1`** in the environment | Empty trace file | Standing Order 6, Pitfall: INIT conflict |

---

## CORNER CASES — Non-obvious patterns that need special handling

### CC1: Two occurrences of the same function name
A C file may have a forward declaration near the top and the real definition further
down. Both have the same name but only the definition has a `{...}` body.

```bash
grep -n "POSIX_Xfer" aiori-POSIX.c
# 115: static IOR_offset_t POSIX_Xfer(int, aiori_fd_t *, ...);   ← SKIP (fwd decl, ends with ;)
# 735: static IOR_offset_t POSIX_Xfer(int access, aiori_fd_t *file, ...) ← ANNOTATE (definition)
```
Quick filter — shows only definitions: `grep -n "FN_NAME" file.c | grep -v ";$"`

### CC2: Error-checking macros hide early returns (Rule E)
`MPI_CHECK(...)`, `NCMPI_CHECK(...)`, `HGOTO_ERROR(...)` expand to `if (rc != 0) { ... return; }`.
These are invisible exit points. Do NOT place `END` before them — only place `END` before
**visible** `return` and `throw` statements in the source.

For **goto-based cleanup** (HDF5): place a single `END` at the `done:` / `err:` label,
not before each individual `goto`. See C Rule 5 (error macros) and 01-annotation-rules-general.md Rule E.

### CC3: Multi-line function signatures
When a function signature spans multiple lines the `{` appears alone on a line below the last
parameter. Scan **upward** from the `{` to find the signature start before placing START:
```c
static IOR_offset_t POSIX_Xfer(int access, aiori_fd_t *file,
                               IOR_size_t *buffer, IOR_offset_t length,
                               IOR_offset_t offset, aiori_mod_opt_t *param)
{                         ← START goes here, after this brace
  DFTRACER_C_FUNCTION_START();
```

### CC4: Vendor filesystem functions guarded by `#ifdef`
`gpfs_*`, `beegfs_*`, `lustre_*` functions are compiled only when `HAVE_GPFS_FCNTL_H`
etc. are defined. Annotate them anyway — they will appear in traces when the binary
is built against those libraries and run on the corresponding filesystem.
If they don't appear in a basic smoke test, that is **expected, not a bug**.

### CC5: Internal helper functions with non-obvious names
After annotating the public API functions (`POSIX_Create`, `POSIX_Xfer`, etc.) always
scan the **entire file** for unannotated definitions. Any helper that calls a syscall
or filesystem API is an I/O function regardless of its name:

```bash
# List all annotated functions
awk '/^[a-zA-Z_].*\(/ {func=NR": "$0} /DFTRACER_C_FUNCTION_START/ {print func}' file.c

# Find definitions that may be missing
grep -n "^[a-zA-Z_].*(.*)$" file.c | grep -v ";"
```

**Triggers that make a helper mandatory to annotate:**
- Calls `open()`, `read()`, `write()`, `close()`, `mknod()`, `mkstemp()`, `stat()`, `ioctl()`
- Calls `cuFileHandleRegister()`, `cuFileRead/Write()` (GPU Direct)
- Calls `gpfs_fcntl()`, `beegfs_*()`, `llapi_*()` (vendor filesystem APIs)
- Creates, opens, reads, writes, or deletes any file
- Returns a file descriptor

**Apply Rule 0 (skip) only if:** the function is a pure getter/setter ≤5 lines, a
string formatter, or an arithmetic helper with no filesystem calls.

Examples from `aiori-POSIX.c`:
| Function | Decision | Reason |
|----------|----------|--------|
| `init_cufile` | ✅ Annotate `comp="io"` | Calls `cuFileHandleRegister()` — GPU Direct I/O setup |
| `mkTempInDir` | ✅ Annotate `comp="io"` | Calls `mkstemp()` + `unlink()` — creates and deletes a file |
| `POSIX_Mknod` | ✅ Annotate `comp="io"` | Calls `mknod()` syscall |
| `POSIX_xfer_hints` | ❌ Skip (Rule 0) | 2-line setter, no filesystem call |
| `POSIX_check_params` | ❌ Skip (Rule 0) | Pure parameter validation, no filesystem call |
| `cuFileGetErrorString` | ❌ Skip (Rule 0) | Trivial error string formatter |

### CC6: Lifecycle functions that look too short to annotate
Backend `*_Initialize` and `*_Finalize` functions often have short bodies (sometimes
just an `#ifdef` block). **Always annotate them** — they mark the backend entry/exit
point in traces and are never skipped under Rule 0.

### CC7: `beegfs_isOptionSet`-style END-after-return bug
When a function has a single-expression return like `return opt != -1;`, it is easy
to place `END` after the `return` by accident, making it unreachable:
```c
// ❌ Wrong — END after return is dead code
bool beegfs_isOptionSet(int opt) {
  DFTRACER_C_FUNCTION_START();
  return opt != -1;
  DFTRACER_C_FUNCTION_END();   // ← unreachable, span never closed
}

// ✅ Correct — END before return
bool beegfs_isOptionSet(int opt) {
  DFTRACER_C_FUNCTION_START();
  DFTRACER_C_FUNCTION_UPDATE_STR("comp", "io");
  DFTRACER_C_FUNCTION_END();   // ← before the return
  return opt != -1;
}
```

---

## KNOWN MISTAKES — Top recurring errors from real annotation sessions

| # | Mistake | Symptom | Fix |
|---|---------|---------|-----|
| M1 | **comp= not added** after completing a file | `grep -c START` ≠ `grep -c comp=` | Add `UPDATE_STR("comp","<type>")` immediately after every bare START |
| M2 | **Forward declaration annotated** instead of definition | `syntax error: expected ';'` before `{` | Check both occurrences; annotate only the one with a body |
| M3 | **Vendor functions skipped** (gpfs_*, beegfs_*, lustre_*) | Coverage gap found in post-annotation awk scan | These are I/O functions — always annotate |
| M4 | **Lifecycle functions skipped** (Initialize, Finalize) | Functions missing from trace | Never apply Rule 0 to lifecycle functions |
| M5 | **Internal helpers missed** (init_cufile, mkTempInDir, etc.) | Coverage gap | Run the awk scan after the named functions; check every definition against the syscall trigger list |
| M6 | **`.deps missing separator`** after Makefile edit | Build fails immediately | `rm -rf .deps src/.deps && make clean` — always after any Makefile change |
| M7 | **END indented at column 0** | Compiles, but hard to read / wrong indentation | END must match the indentation of the surrounding `return` |
| M8 | **`DFTRACER_INIT=1` with explicit INIT call** | Empty `.pfw` trace file | Pass `env_extra='{"DFTRACER_INIT":"0"}'` when source has explicit `DFTRACER_C_INIT()` |
| M9 | **Missing `rm -rf .deps`** after annotating a file that affects the Makefile | `.deps missing separator` on next build | Standard cleanup before every `make` after Makefile touch |
| M10 | **Completing annotation without verifying coverage** | Missed functions discovered late | Always run the two-count check and awk scan at end of every file |

---

## Coverage Verification Commands (run after every file)

```bash
FILE=annotated/src/aiori-POSIX.c

# 1. START count must equal comp= count
grep -c "DFTRACER_C_FUNCTION_START"               $FILE
grep -c 'DFTRACER_C_FUNCTION_UPDATE_STR.*"comp"'  $FILE

# 2. List all annotated function signatures
awk '/^[a-zA-Z_].*\(/ {func=NR": "$0} /DFTRACER_C_FUNCTION_START/ {print func}' $FILE

# 3. List all definitions (compare against #2 to find gaps)
grep -n "^[a-zA-Z_].*(.*)$" $FILE | grep -v ";"
```

Both counts from step 1 must match. Any definition in step 3 not in step 2 is a
candidate for annotation (check the body for syscalls before deciding to skip).
