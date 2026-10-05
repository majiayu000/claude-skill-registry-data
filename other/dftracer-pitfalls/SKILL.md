---
name: dftracer-pitfalls
description: Annotation pitfalls — real mistakes that caused build failures or missing trace data, with root causes and exact fixes
---

## Annotation Pitfalls (lessons learned)

> **Quick navigation:** For the top-10 most common mistakes and critical rules,
> see the `dftracer-cheatsheet` skill first. This file contains the full detail for
> every pitfall, organized in the order they were discovered.

These are real mistakes that caused build failures or missing trace data in actual
annotation sessions. Check pitfalls matching your current file type before writing.

**Standing instruction — update `.goose/hints/02-annotation-pitfalls.md` in two situations:**

1. **Immediately after any fix during annotation** — the moment you fix a build error
   or annotation mistake, append a new entry.
2. **At end of every session (Pass 5, Step 2)** — scan `annotation_process.log` and
   add entries for every pattern not yet covered.

When you encounter ANY error during annotation, build, or run that is not already
covered, and you fix it, you MUST immediately append a new entry using the format:

```
---
context: <one-line description of what was being attempted>
error: |
  <exact error message or key excerpt>
root_cause: <why it happened>
fix: |
  <exact rule or steps that resolved it>
tags: [<language>, annotation, <error-keyword>, ...]
---
```

---

**Pitfall: `{` inside a string literal**

context: Macro injected into fprintf multi-line string
error: `aiori-MPIIO.c:241: error: missing terminating " character`
fix: Verify the `{` is a real function body opener: must follow a closing `)`, be last on its line, and NOT be inside a string. If the line contains `"..."` or is inside `fprintf`, it is NOT a function body.

---

**Pitfall: Macro inside `#define` body**

error: `'data_fn' undeclared — DFTRACER_C_FUNCTION_END expanded inside a macro`
fix: Never annotate `#define` macro bodies, inline lambdas, or function-like macros. Only annotate real C function definitions.

---

**Pitfall: Macro inside block comment**

error: START inside `/* ... */` — no compile error but function is silently never traced.
fix: Skip any line where `{` appears after `/*` with no intervening `*/`.

---

**Pitfall: START inside a control-flow block**

error: Multiple START macros per function when `if(...) {` or `for(...) {` matched as function openers.
fix: Reject any match where the "function name" is: `if`, `else`, `for`, `while`, `do`, `switch`, `case`, `return`, `sizeof`, `typeof`, `namespace`, `class`, `struct`, `union`, `enum`, `template`, `catch`, `try`.

---

**Pitfall: Forward declaration annotated**

error: `DFTRACER_C_FUNCTION_START injected after a semicolon-terminated prototype`
fix: A function DEFINITION must have `{` (not `;`) after the parameter list. Never annotate a line ending with `;`.

---

**Pitfall: struct/union/enum annotated as function**

error: `DFTRACER_C_FUNCTION_START() inserted after "struct IOR_param_t {"`
fix: Reject any match where the return-type token is `struct`, `union`, `enum`, `typedef`, `class`, or `namespace`.

---

**Pitfall: File truncated during write**

error: `ior.c went from 1869 lines to 960 lines after session_write_file`
fix: Always write the COMPLETE file. Read the original, build the full annotated content in memory, verify line count is ≥ original, then write in one call.

---

**Pitfall: Annotating header files (.h/.hpp)**

error: `DFTRACER_C_FUNCTION_START injected into inline function in header included by many TUs — redeclaration or scope errors`
fix: Do NOT annotate header files. Only annotate .c/.cpp/.cxx source files. Add `#include <dftracer/dftracer.h>` to the .c file, not the header.

---

**Pitfall: UPDATE uses parameter name from declaration, not definition**

error: `aiori-POSIX.c:687:50: error: 'count' undeclared`
fix: Always locate the function DEFINITION (with `{` body) to read exact parameter names. The forward declaration often omits or changes names. Use: `grep -n "POSIX_Xfer" file.c` to find both, then use names from the definition.

---

**Pitfall: START placed before `{` instead of after it**

error: `data_fn undeclared or duplicate-START errors`
fix: START must go on the FIRST LINE AFTER the opening `{`, not before it.

---

**Pitfall: END at column 0**

error: Indentation mismatch — END at column 0 while surrounding code is indented.
fix: END indentation must match the line it precedes. Check the `return` or `}` indentation and use the same leading whitespace.

---

**Pitfall: Duplicate STARTs or misplaced ENDs from iterative annotation**

fix: Always restore from the original unannotated source before re-running any annotation script: `cp source/src/foo.c annotated/src/foo.c`. Never annotate a file that already contains dftracer macros.

---

**Pitfall: END placed after return statement in MPI-IO functions**

error: `aiori-MPIIO.c: error: 'data_fn' undeclared — DFTRACER_C_FUNCTION_END placed after a return`
fix: For functions with complex control flow, manually trace EVERY exit path. List all returns with `grep -n "return" file.c`. Place END immediately BEFORE each return, same indentation. For switch/case: place END before `break` or `return` in each case.

---

**Pitfall: Duplicate END macros**

error: `conflicting types for 'finalize_region'` — two consecutive END macros.
fix: Before inserting any END, check the 3 lines above the return: `awk "NR>=$(( LINE-3 )) && NR<$LINE" file.c | grep -c "DFTRACER_C_FUNCTION_END"`. If count is already 1, skip the insertion.

---

**Pitfall: DFTRACER_INIT=1 is incorrect value**

error: Trace file is empty (0 bytes or 580 bytes with no events).
fix: NEVER set `DFTRACER_INIT=1` when source already contains explicit `DFTRACER_C_INIT()` calls. Pass `env_extra='{"DFTRACER_INIT": "FUNCTION"}'`. Heuristic: `grep -r "DFTRACER_C_INIT" annotated/` — if matches found, set `DFTRACER_INIT=FUNCTION`.

---

**Pitfall: .deps missing separator after Makefile patching**

error: `.deps/IOR-aiori-DUMMY.Po:1: *** missing separator. Stop.`
fix: Always purge .deps before rebuilding after a Makefile patch: `rm -rf .deps src/.deps && make clean && make -j4`.

---

**Pitfall: dftracer.h not found / linker undefined references**

error: `fatal error: dftracer/dftracer.h: No such file or directory` + `undefined reference to 'initialize_main'`
fix: Patch the build system BEFORE annotating any file:
1. Add `-I<install_ann>/include` to CFLAGS
2. Add `-L<install_ann>/lib -Wl,-rpath,<install_ann>/lib` to LDFLAGS
3. Add `-ldftracer_core -lcpp-logger -lbrahma` to LIBS
For autotools: patch `src/Makefile` (not just the top-level). Then: `rm -rf .deps src/.deps && make -j4`.

---

**Pitfall: Smoke test binary not found (return code 127)**

error: `./ior: not found (return code 127)`
fix: Always use the FULL ABSOLUTE PATH to the binary. Find it first: `find <workspace> -name "ior" -type f -not -path "*/source/*"`.

---

**Pitfall: Error-checking macro (MPI_CHECK, NCMPI_CHECK, H5EPRINT) hides early return**

error: Traces show START with no corresponding END — span imbalance, no compile error.
fix: Before annotating any function, grep for all error-checking macro calls and place END immediately before them. Verify after annotation: count of END >= count of (return + CHECK_MACROS) in the function.

---

**Pitfall: goto-based error handling — END before goto vs at label**

error: N duplicate END macros when a function has N `goto done` statements.
fix: Place a SINGLE END at the goto label, not before each goto: `done: DFTRACER_C_FUNCTION_END(); ... return ret;`

---

**Pitfall: Multi-line function signature not matched**

error: MPIIO_Xfer annotation skipped / START placed inside wrong line.
fix: Treat any `{` on its own line as a potential function-body opener. Look UPWARD from that `{` to find the function signature — scan back until you find a line ending with `)`.

---

**Pitfall: MPI-IO backend annotation fails and must be reset**

error: `error: 'data_fn' undeclared (first use in this function)` — file reset to include-only.
fix: Annotate MPI-IO style backends LAST and one function at a time. Pick the simplest first (MPIIO_Close, MPIIO_Delete). Read the entire function body before writing a single macro. Build after every single function.

---

**Pitfall: POSIX_Xfer forward declaration annotated instead of definition**

fix: Before annotating ANY function, search for ALL occurrences of its name: `grep -n "POSIX_Xfer" file.c`. If two hits: the one with no param names and trailing `;` is the forward declaration — DO NOT ANNOTATE. Annotate only the one with named parameters and a `{` body.

---

**Pitfall: Vendor-specific functions (gpfs_*, beegfs_*, lustre_*) not annotated**

error: Coverage check found gpfs_free_all_locks, beegfs_getStriping, etc. unannotated.
fix: After annotating named backend functions, always scan the ENTIRE file: `grep -n "^[a-zA-Z].*(.*)$\|^static.*(.*)$" file.c | grep -v ";" | grep -v "DFTRACER"`. These are I/O operations — annotate with `comp="io"`.

---

**Pitfall: Lifecycle functions skipped because body is short**

error: POSIX_Initialize and POSIX_Finalize not annotated (bodies only contain `#ifdef` blocks).
fix: Backend lifecycle functions (*_Initialize, *_Finalize) are ALWAYS annotated regardless of body size. Never apply Rule 0 to lifecycle functions.

---

**Pitfall: Sync and rename functions missed**

error: POSIX_Sync and POSIX_Rename not annotated — not "read/write" functions.
fix: The mandatory list includes: Create, Open, Xfer, Close, Delete, Fsync, Sync, Rename, GetFileSize, Mknod, Initialize, Finalize.

---

**Pitfall: Skipping POSIX_Mknod because "deprecated"**

fix: Never skip a function solely because it is described as "deprecated" or not called in the basic smoke test. Only skip under Rule 0 (pure getter/setter ≤5 lines, no I/O).

---

**Pitfall: comp= not added to any function in a pass**

error: grep for comp= finds zero results but grep for START finds 21.
fix: After annotating a file, always run: `grep -c "DFTRACER_C_FUNCTION_START" file.c` vs `grep -c 'DFTRACER_C_FUNCTION_UPDATE_STR.*comp' file.c`. If different, find each bare START: `grep -A2 "DFTRACER_C_FUNCTION_START" file.c | grep -v "comp"`.

---

**Pitfall: dftracer header added to a .h file instead of .c file**

error: `fatal error: dftracer/dftracer.h: No such file or directory` in files that never include dftracer themselves.
fix: Move `#include <dftracer/dftracer.h>` into each .c/.cpp file that contains annotation macros. Never add it to a .h header.

---

**Pitfall: Linker fails with "undefined reference to dftracer_*"**

error: `/usr/bin/ld: foo.o: undefined reference to 'dftracer_init'`
fix: Add to src/Makefile: `LDFLAGS += -L$(DFTRACER_PREFIX)/lib -Wl,-rpath,$(DFTRACER_PREFIX)/lib` and `LIBS += -ldftracer_core`. If dftracer installed via pip/venv, use: `DFTRACER_LIB=$(python3 -c "import importlib.util, pathlib; p=importlib.util.find_spec('dftracer'); print(pathlib.Path(p.origin).parent / 'lib')")`.

---

**Pitfall: Binary links but crashes — dftracer .so not found at runtime**

error: `./myprogram: error while loading shared libraries: libdftracer_core.so: cannot open shared object file`
fix: Add `-Wl,-rpath,$(DFTRACER_PREFIX)/lib` to LDFLAGS. Or export `LD_LIBRARY_PATH=$(DFTRACER_PREFIX)/lib` before running.

---

**Pitfall: Vendor-specific functions not appearing in trace**

error: gpfs_access_start, beegfs_getStriping annotated but not in trace output.
fix: This is EXPECTED — they are guarded by `#ifdef HAVE_GPFS_FCNTL_H` etc. and only invoked on those filesystems. Report as "annotated, not traced (filesystem not available in test environment)".
