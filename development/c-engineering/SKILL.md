---
name: c-engineering
description: Write production C — memory discipline, undefined-behavior avoidance, warning-clean builds, and boundary testing.
version: 1
triggers: c programming, c code, write c, memory bugs, undefined behavior
category: Engineering & code
blurb: Write production C — memory discipline, no undefined behaviour, warning-clean builds, boundary tests.
archetype: knowledge
example: Review this C code for memory and undefined-behaviour traps.
---

# C Engineering

C is the sharpest tool in the shop: small, fast, everywhere — and unforgiving. Write it like the memory matters, because it does.

## When to use
- Systems code, embedded, performance-critical paths, native extensions.
- Reviewing or hardening existing C.

## Method
1. **Memory discipline**: one clear owner per allocation; free on the same path as allocation; document ownership in headers. Prefer caller-supplied buffers over hidden allocations.
2. **No undefined behavior**: mind integer overflow, strict aliasing, uninitialized reads, signed shifts, sequence-point traps. No UB shortcuts.
3. **Warnings are errors**: build `-Wall -Wextra -Werror` (MSVC `/W4 /WX`); zero warnings maintained, not "later".
4. **Bounds and strings**: never `strcpy`/`sprintf`/`gets`; use sized APIs (`snprintf`, checked `memcpy`); validate every length crossing a boundary.
5. **Sanitizers in dev**: ASan + UBSan in test builds; Valgrind for leaks; fuzz parsers (libFuzzer/AFL).
6. **Static analysis**: clang-tidy + compiler analyzer in the loop; findings are bugs until proven otherwise.
7. **Portability**: fixed-width types (`stdint.h`); isolate compiler extensions; test on target platforms.
8. **Build & test**: Make/CMake pinned; unit tests at function boundaries; integration tests at the edges.

## Quality gates
- [ ] Warning-clean with `-Werror` on target compilers.
- [ ] ASan/UBSan clean on the suite.
- [ ] No unbounded string/mem operations in the diff.
- [ ] Ownership documented for pointers that outlive their function.

## Red lines
- No `gets`, `strcpy`, `sprintf`, unchecked `scanf` — ever.
- No UB "because it works on my machine".

## Related
`cpp-engineering` · `testing-strategy` · `dependency-governance`.
