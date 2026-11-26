---
name: snx-code-quality
description: "RFC #142's C rules: strict ISO C99, no redundant state, indices not pointer chains, one allocation per owner, atomics apart, no stored pointers, one global struct per file. Use when writing or reviewing C in src/."
---

# Code quality (#142)

Write strict ISO C: C99, as the driver builds (`-std=c99 -pedantic-errors`), unless the target needs more.
C99 is the baseline, so use what it has: `static inline` functions, `<stdint.h>` types (`SnxU32`/`SnxU64` in the
driver), 64-bit literals as `0x...ull` (not `UINT64_C`, not two halves), `SIZE_MAX` in size checks
(`n > SIZE_MAX / size`), `%zu` for a `size_t`, `%llu`/`%llx` through `(unsigned long long)` for a 64-bit value
(never `(unsigned long)`: `long` is 32 bits on Windows), `bool` or `int` flags, `strtoull`, `snprintf`. A
declaration may follow statements and open a `for`; comments stay `/* */`, as the code has them. In place of C11
and C23: `__atomic_*` builtins on plain integers, a `char` padding array, a negative-size array typedef as the static
assert. A file's build flags plus `-std=c99 -pedantic` list what is not. A local that starts zeroed is declared
`= {0}`, not zeroed by a `memset` after its declaration; a `memset` stays for an object reached through a pointer.
`strdup` is not C99: `snx_strdup` (common.h) is, and fails the way the rest of the code does when memory runs out.

1. **No state another value already says.** A NULL pointer is absent: no `is_present` beside it.
   Not when NULL means something itself, or the flag says something else.
2. **Indices, not pointer chains.** Objects in one array, linked by `u32` index; 0 is none, so slot 0
   is never an object. Not when the index can outlive its array.
3. **One allocation per owner.** An owner's arrays come from one block carved by offsets (each at a
   multiple of its type's size), sizes checked against `(size_t)-1`, one `free`. Not for an array that
   grows on its own, or parts that live apart.
4. **Atomics apart.** Atomics that different threads write get a cache line each (a `char` pad between).
   Not when one thread writes them all, or for many per-object atomics.
5. **No stored pointers in data.** Data refers to its parts by index or offset, so a copy or a file
   holds together. Handles (`FILE*`, SDL, Vulkan) stay in a runtime struct beside it.
6. **One global per file.** A file's mutable state (every variable of static duration, function-local
   `static`s included) is the members of one struct in one global, `g_<file>`, not loose globals. What
   other files read is declared once, in the header beside it, through the struct or a function. Not
   for `const` tables (they are data, not state), or for `_Thread_local`.
   **In `src/nx/hle/`** the HLE's state is one global for the whole subsystem: each file's state struct is a
   member of `g_hle` (`hle/hle.h`), its type and initializer declared in the header beside the file, and the
   objects it makes and frees come from bounded pools in it (an all-zero slot is free, `pool_take` searches on
   from the last slot taken and asserts when full). No file there defines a variable of static duration.

Review: `python3 .claude/skills/snx-code-quality/check.py FILES` lists candidates for 1, 3, 4 and 6 (a
candidate is not a finding until the code is read); read the diff for 2 and 5. Report `file:line`, the
rule and the fix. A rule that does not apply is not a finding. Wrong and right C for each rule:
[examples.md](examples.md).
