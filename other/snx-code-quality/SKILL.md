---
name: snx-code-quality
description: "The C rules of RFC #142: strict ISO C99, no redundant state and indices in place of pointer chains. Also one allocation per owner, atomics apart, no stored pointers and one global struct per file. Use it when you write or review C in src/."
---

# Code quality (#142)

Write strict ISO C: C99, as the driver builds (`-std=c99 -pedantic-errors`), unless the target needs more. C99 is the
baseline, so use what it has:
- `static inline` functions.
- `<stdint.h>` types (`SnxU32`/`SnxU64` in the driver).
- 64-bit literals as `0x...ull` (not `UINT64_C`, not two halves).
- `SIZE_MAX` in size checks (`n > SIZE_MAX / size`).
- `%zu` for a `size_t`.
- `%llu`/`%llx` through `(unsigned long long)` for a 64-bit value. Never use `(unsigned long)`: `long` is 32 bits on
  Windows.
- `bool` or `int` flags, `strtoull` and `snprintf`.

Keep comments as `/* */`, as the code has them. In place of C11 and C23, use `__atomic_*` builtins on plain integers
and a `char` padding array. Use a negative-size array typedef as the static assert. The build flags of a file with
`-std=c99 -pedantic` show what is not C99.

`strdup` is not C99. Use `snx_strdup` (common.h), which is C99. When memory runs out, it fails the same way as the rest
of the code.

No C89 workarounds. Declare a local where it first gets its value, together with that assignment. Declare it in the
innermost block that uses it, and a loop counter in its `for`. Do not put a block of bare declarations at the top of a
function. A local stays above a forward `goto` whose label reads it.

Language semantics over library calls. Declare a local that starts at zero with `= {0}`, not with a `memset` after its
declaration. Zero an object behind a pointer with `*p = (T){0};`. Copy a struct by assignment (`a = b;`,
`*dst = *src;`), not with `memcpy`. `memset` and `memcpy` stay where the bytes matter or the types differ:
- Bytes that the code hashes, compares with `memcmp`, uses as a key, or writes to a file, guest memory, a GPU buffer
  or the wire. An initializer or an assignment leaves padding unspecified.
- Byte ranges.
- Fills that are not zero.
- Copies between different types. That `memcpy` is how the code keeps strict aliasing.
- Objects over about a kilobyte. A compound literal can be a stack temporary of that size. Thus the code clears the
  100 KB `SnxCtrPica` of the 3DS with `memset`.

One implementation of each helper. Before you write a small helper, look in `common/utilities/`:
- `ascii.h`: character classes, hex digits, case, path separators, locale-free.
- `bits.h`: align, clamp, min/max, FNV-1a, qsort comparators.
- `endian.h`: little- and big-endian loads and stores at a byte address.
- `common.h`: paths, files, strings.

Put a helper that two files need there, or in a header beside the two files. Never make a second copy.

1. **No state that another value already says.** A NULL pointer means absent: do not put an `is_present` beside it.
   The rule does not apply when NULL itself means something, or when the flag says something else.
2. **Indices, not pointer chains.** Put objects in one array, and link them by `u32` index. Index 0 is none, so slot
   0 is never an object. The rule does not apply when the index can outlive its array.
3. **One allocation per owner.** The arrays of an owner come from one block that offsets divide. Each array is at a
   multiple of the size of its type. Check the sizes against `(size_t)-1`. Use one `free`. The rule does not apply to
   an array that grows on its own, or to parts that live apart.
4. **Atomics apart.** Atomics that different threads write get a cache line each, with a `char` pad between them.
   The rule does not apply when one thread writes them all, or to many atomics per object.
5. **No stored pointers in data.** Data refers to its parts by index or offset, so a copy or a file holds together.
   Handles (`FILE*`, SDL, Vulkan) stay in a runtime struct beside it.
6. **One global per file.** The mutable state of a file is the members of one struct in one global, `g_<file>`, not
   loose globals. That state is every variable of static duration, and also function-local `static`s. Declare what
   other files read one time, in the header beside the file, through the struct or a function. The rule does not
   apply to `const` tables (they are data, not state), or to `_Thread_local`.

   **In `src/nx/hle/`**, the state of the HLE is one global for the whole subsystem. The state struct of each file is
   a member of `g_hle` (`hle/hle.h`). The header beside the file declares its type and initializer. The objects that
   the file makes and frees come from bounded pools in that struct (an all-zero slot is free). `pool_take` searches
   on from the last slot that it took, and asserts when the pool is full. No file there defines a variable of static
   duration.

Review: `python3 .claude/skills/snx-code-quality/check.py FILES` lists candidates for rules 1, 3, 4 and 6. A candidate
is not a finding until you read the code. Read the diff for rules 2 and 5. Report `file:line`, the rule and the fix. A
rule that does not apply is not a finding. Wrong and right C for each rule: [examples.md](examples.md).
