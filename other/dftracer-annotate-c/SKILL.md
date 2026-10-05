---
name: dftracer-annotate-c
description: Complete C annotation rules for dftracer — START/END placement, comp types, linker setup, coverage verification, and the full checklist
---

## C Annotation Rules (dftracer)

> **Before reading the detail rules below, check the `dftracer-cheatsheet` skill** for
> the five critical rules (C1–C5), seven corner cases (CC1–CC7), and the top-10
> known mistakes (M1–M10). The rules below provide the full explanation and examples.

### C Rule 1 — Include and one START per function, at the very top

Add the include after all existing `#include` lines in the .c file (never in a header):
```c
#include <dftracer/dftracer.h>
```

Then for each selected function:
```c
return_type function_name(params) {
  DFTRACER_C_FUNCTION_START();   // ← FIRST statement after {, nothing before it
  ...
}
```

- **One and only one** START per function body.
- START goes **after** the opening `{`, never before it.
- It must be the **first executable statement** — no variable declarations, no assignments before it.
- **Never** place START inside a control-flow block (`if`, `else`, `for`, `while`,
  `switch`, `do`). Control-flow blocks are NOT functions.
- **Never** annotate: struct/union/enum definitions, typedefs, macro bodies,
  `#ifdef` guard blocks, forward declarations, or function pointer declarations.

### C Rule 2 — DFTRACER_C_FUNCTION_END before every exit point

```c
return_type function_name(params) {
  DFTRACER_C_FUNCTION_START();
  ...
  if (error) {
    DFTRACER_C_FUNCTION_END();   // ← before early return
    return -1;
  }
  ...
  DFTRACER_C_FUNCTION_END();     // ← before normal return
  return 0;
}
```

- Place END **immediately before every `return` statement** (on its own line, same indent as return).
- For **void functions** that fall off the end (no explicit `return`), place END
  as the **last statement before the closing `}`**:
  ```c
  void helper(int x) {
    DFTRACER_C_FUNCTION_START();
    do_work(x);
    DFTRACER_C_FUNCTION_END();   // ← last statement, void function
  }
  ```
- Every function with a START **must** have a corresponding END at every exit path.
- Never place END after a `return` (it would be unreachable).
- END indentation must match the surrounding block — not at column 0.

### C Rule 3 — DFTRACER_C_FINI in main before every exit; order around MPI

**Without MPI** — INIT goes right after the opening `{` of main:

```c
int main(int argc, char **argv) {
  DFTRACER_C_INIT(NULL, NULL, NULL);   // ← first, before anything else
  DFTRACER_C_FUNCTION_START();
  ...
  DFTRACER_C_FUNCTION_END();
  DFTRACER_C_FINI();
  return 0;
}
```

**With MPI** — INIT must come AFTER `MPI_Init`/`MPI_Init_thread`, and FINI must
come BEFORE `MPI_Finalize`. dftracer uses MPI internals; initialising before MPI
is ready causes crashes, and finalising after MPI shuts down loses trace data:

```c
int main(int argc, char **argv) {
  MPI_Init(&argc, &argv);              // ← MPI first
  DFTRACER_C_INIT(NULL, NULL, NULL);   // ← dftracer after MPI_Init
  DFTRACER_C_FUNCTION_START();
  ...
  if (bad) {
    DFTRACER_C_FUNCTION_END();         // ← END first
    DFTRACER_C_FINI();                 // ← dftracer FINI before MPI_Finalize
    MPI_Finalize();                    // ← MPI last
    return 1;
  }
  ...
  DFTRACER_C_FUNCTION_END();
  DFTRACER_C_FINI();                   // ← dftracer FINI before MPI_Finalize
  MPI_Finalize();
  return 0;
}
```

- Scan main for `MPI_Init` or `MPI_Init_thread` before placing `DFTRACER_C_INIT`.
  If found, place INIT on the line immediately after the `MPI_Init(...)` call.
- Scan every `return` path and every `MPI_Finalize()` call in main. Place
  `DFTRACER_C_FUNCTION_END()` then `DFTRACER_C_FINI()` immediately **before**
  each `MPI_Finalize()`.
- The full order at every exit from an MPI main:
  `FUNCTION_END → DFTRACER_C_FINI → MPI_Finalize → return`
- Also place FINI before any **process-exit call** (`exit()`, `_exit()`, `abort()`,
  `quick_exit()`) that bypasses `MPI_Finalize`.
- `DFTRACER_C_FINI()` must appear **in the same function as `DFTRACER_C_INIT()` (i.e., main).
- INIT/FINI summary: `MPI_Init → DFTRACER_C_INIT → ... → DFTRACER_C_FINI → MPI_Finalize`

### C Rule 4 — Classify every annotated function with comp=TYPE

Every annotated function MUST include a `comp` classification UPDATE immediately
after `DFTRACER_C_FUNCTION_START()`. This tags functions in the trace so analysis
tools can group and filter by operation type.

**The four types:**

| Type | When to use | Typical functions |
|------|------------|-------------------|
| `"io"` | File system I/O: open, read, write, close, fsync, stat, delete, rename, getfilesize, mknod | POSIX_Create, POSIX_Xfer, POSIX_Fsync, POSIX_Close, POSIX_Delete, HDF5_Xfer, MMAP_Open |
| `"mem"` | Memory operations: large memcpy, mmap region setup, buffer alloc/free, data copy between memory regions | MMAP_Xfer (memcpy path), any malloc/free of large buffers |
| `"cpu"` | Compute: checksums, compression, encryption, hash, data encoding, format conversion | Any function that transforms data without doing file I/O |
| `"comm"` | Communication: MPI sends/recvs, network I/O, REST API calls, distributed FS ops | MPIIO_Xfer, NCMPI_Xfer, HDFS_Xfer, S3_Xfer, RADOS ops, DFS ops, any MPI_File_* wrapper |

**Usage — always the first UPDATE after START:**

```c
// File I/O function
aiori_fd_t *POSIX_Create(char *testFileName, int flags, aiori_mod_opt_t *param)
{
  DFTRACER_C_FUNCTION_START();
  DFTRACER_C_FUNCTION_UPDATE_STR("comp", "io");            // ← type first
  DFTRACER_C_FUNCTION_UPDATE_STR("filename", testFileName); // then params
  DFTRACER_C_FUNCTION_UPDATE_INT("flags", flags);
  ...
}
```

**Classification guide for common patterns:**
- `Create`, `Open`, `Close`, `Fsync`, `Sync`, `Delete`, `Rename`, `GetFileSize`, `Mknod` → `"io"`
- `Xfer` in POSIX, MMAP, HDF5, NCMPI where data goes to/from a file → `"io"`
- `Xfer` in MPIIO, S3, HDFS, RADOS, DFS, CEPHFS where a network/RPC call is made → `"comm"`
- `Xfer` in MMAP where the transfer is a `memcpy` into the mmap region → `"mem"`
- `init`, `final`, `initialize`, `finalize` for any backend → `"io"` (I/O stack lifecycle)
- Functions doing checksums, compression, encryption, hashing → `"cpu"`

### C Rule 5 — Track important I/O metadata with FUNCTION_UPDATE (after comp=TYPE)

```c
ssize_t my_read(const char *filename, void *buf, size_t count, off_t offset) {
  DFTRACER_C_FUNCTION_START();
  DFTRACER_C_FUNCTION_UPDATE_STR("filename", filename);   // string params
  DFTRACER_C_FUNCTION_UPDATE_INT("count",    (int)count); // numeric params
  DFTRACER_C_FUNCTION_UPDATE_INT("offset",   (int)offset);
  ...
  DFTRACER_C_FUNCTION_END();
  return result;
}
```

- **String params** (`const char *`): use `DFTRACER_C_FUNCTION_UPDATE_STR("name", ptr)`
- **Numeric params** (`size_t`, `off_t`, `int`, `long`): use `DFTRACER_C_FUNCTION_UPDATE_INT("name", (int)val)`
- The variable name in the UPDATE call **must exactly match** the parameter name in
  the function definition — otherwise you get `undeclared identifier` compile errors.
- **Opaque handle typedefs** (`MPI_File`, `hid_t`, `ncid`, `hsize_t`) use `UPDATE_INT` with `(int)` cast.

### C Rule 5 — Error-checking macros that embed early exits

```c
ssize_t my_write(...) {
  DFTRACER_C_FUNCTION_START();
  ...
  DFTRACER_C_FUNCTION_END();          // ← before macro that may return/goto
  NCMPI_CHECK(ncmpi_put_vara(...), "write failed");
  ...
  DFTRACER_C_FUNCTION_END();          // ← before normal return
  return 0;
err:
  DFTRACER_C_FUNCTION_END();          // ← before goto-target fallthrough
  return -1;
}
```

For **`goto`-based error handling** (HDF5):
```c
ssize_t hdf5_write(...) {
  DFTRACER_C_FUNCTION_START();
  ...
  if ((fid = H5Fcreate(...)) < 0) goto done;
  ...
done:
  DFTRACER_C_FUNCTION_END();   // ← place END at the goto label, not before each goto
  return ret;
}
```

### C Rule 7 — Forward declarations vs definitions: only annotate definitions

```c
// ❌ DO NOT annotate — forward declaration (no body, no param names)
static IOR_offset_t POSIX_Xfer(int, aiori_fd_t *, IOR_size_t *,
                               IOR_offset_t, IOR_offset_t, aiori_mod_opt_t *);

// ✅ Annotate this one — definition with named params and body
static IOR_offset_t POSIX_Xfer(int access, aiori_fd_t *file, IOR_size_t *buffer,
                               IOR_offset_t length, IOR_offset_t offset,
                               aiori_mod_opt_t *param)
{
  DFTRACER_C_FUNCTION_START();
  ...
}
```

Quick filter to find only definitions: `grep -n "FUNCTION_NAME" file.c | grep -v ";$"`

### C Rule 8 — Vendor-specific filesystem functions are I/O functions

| Prefix | Filesystem | Examples |
|--------|-----------|---------|
| `gpfs_*` | IBM GPFS/Spectrum Scale | `gpfs_free_all_locks`, `gpfs_access_start` |
| `beegfs_*` | BeeGFS | `beegfs_getStriping`, `beegfs_createFilePath` |
| `lustre_*` | Lustre | `lustre_disable_file_locks` |
| `hdfs_*` | Hadoop HDFS | Any HDFS JNI wrapper |
| `ceph_*` | Ceph | Any libcephfs wrapper |
| `daos_*` | DAOS | Any DAOS API wrapper |

### C Rule 9 — Coverage verification: scan all definitions after each file

```bash
# Check 1 — list every annotated function
awk '/^[a-zA-Z].*\(/ {func=$0} /DFTRACER_C_FUNCTION_START/ {print NR": "func}' \
    annotated/src/foo.c

# Check 2 — verify comp=TYPE present in every annotated function
grep -c "DFTRACER_C_FUNCTION_START"          annotated/src/foo.c
grep -c 'DFTRACER_C_FUNCTION_UPDATE_STR.*comp' annotated/src/foo.c
# Both counts must be equal
```

### C Rule 10 — Header include and linker setup

#### 10a — Header placement
Add `#include <dftracer/dftracer.h>` as the **last `#include`** in each `.c`/`.cpp` file.
**Never add it to a `.h` header file.**

#### 10b — Linker flags

**Makefile/autotools:**
```makefile
CFLAGS  += -I$(DFTRACER_PREFIX)/include
LDFLAGS += -L$(DFTRACER_PREFIX)/lib -Wl,-rpath,$(DFTRACER_PREFIX)/lib
LIBS    += -ldftracer_core
```

**CMake:**
```cmake
target_link_libraries(${MY_TARGET} PRIVATE dftracer::dftracer_core)
target_include_directories(${MY_TARGET} PRIVATE ${DFTRACER_PREFIX}/include)
```

**pip/venv install** — library lives inside the Python package tree:
```bash
DFTRACER_SITE=$(python3 -c \
    "import importlib.util, pathlib; \
     p=importlib.util.find_spec('dftracer'); \
     print(pathlib.Path(p.origin).parent)")
DFTRACER_INC="${DFTRACER_SITE}/include"
DFTRACER_LIB="${DFTRACER_SITE}/lib"
# → <venv>/lib/python<ver>/site-packages/dftracer/lib/libdftracer_core.so
```

#### 10c — Transitive deps (if linker reports undefined symbols)
```makefile
LIBS += -ldftracer_core -lcpp-logger -lbrahma
```

#### 10d — Verify build setup before annotating any source
```bash
echo '#include <dftracer/dftracer.h>' >> annotated/src/one_file.c
make -C annotated/src 2>&1 | grep -i "error\|cannot find"
```

### C Quick checklist

- [ ] **Build setup verified before first annotation** (Rule 10d)
- [ ] `#include <dftracer/dftracer.h>` added to every annotated `.c`/`.cpp` — last include, never in `.h`
- [ ] Linker flags: `-ldftracer_core -L<prefix>/lib -Wl,-rpath,<prefix>/lib`
- [ ] ALL non-trivial functions annotated — skip only pure getters/setters/formatters
- [ ] START is the first statement after `{` (not before `{`)
- [ ] START is in the definition body, not a forward declaration (Rule 7)
- [ ] `DFTRACER_C_FUNCTION_UPDATE_STR("comp", "<type>")` is FIRST UPDATE after every START
- [ ] `comp` type is one of: `"io"`, `"mem"`, `"cpu"`, `"comm"`
- [ ] Parameter names in UPDATE match the definition, not the declaration
- [ ] END placed before every VISIBLE `return` (same indentation level)
- [ ] Error-checking macros (MPI_CHECK, NCMPI_CHECK): END before them if they wrap a return
- [ ] goto-based error handling: single END at the label, not before each goto
- [ ] Void functions: END placed as last statement before `}`
- [ ] END indentation is not at column 0
- [ ] main: MPI_Init (if present) → DFTRACER_C_INIT → ... → DFTRACER_C_FINI → MPI_Finalize → return
- [ ] Vendor-specific functions (gpfs_*, beegfs_*, lustre_*) annotated as comp="io"
- [ ] Coverage verified: START count == comp count; no missed functions
