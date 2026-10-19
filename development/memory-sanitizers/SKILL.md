---
name: memory-sanitizers
description: >
  Find and interpret memory, undefined-behavior and data-race bugs in C and C++ programs with
  Clang/GCC sanitizers (AddressSanitizer, LeakSanitizer, UndefinedBehaviorSanitizer,
  ThreadSanitizer, MemorySanitizer): choose the right sanitizer, build correctly, read the
  report, and avoid invalid combinations. Use when a native program crashes with heap corruption,
  use-after-free, uninitialized reads, intermittent segfaults, leaks, signed overflow or data
  races, or when adding sanitizer jobs to CI. Not for general C/C++ style (use c-development or
  cpp-development), CPU/time profiling (use performance-profiling), Rust or managed languages, or
  kernel sanitizers (KASAN) and exploit development.
compatibility: >
  Clang (all five sanitizers on Linux; MSan not on macOS) and GCC (ASan, UBSan, TSan, LSan; no
  MemorySanitizer). Verified against Clang documentation and local Apple clang 21. Needs the
  ability to rebuild the program with instrumentation.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "sanitizers, asan, ubsan, tsan, msan, c, cpp, memory-safety, debugging"
  topics: "software-development, debugging"
---

# Memory and Concurrency Sanitizers (C/C++)

Sanitizers are compiler instrumentation plus a runtime that turns silent corruption into a precise report at the first detectable violation. They find bugs that tests did not crash on. Each sanitizer detects a **different bug class** and they **cannot all be combined**, so the skill is mostly about choosing, building and interpreting, not flags.

Boundaries: language conventions are `c-development` / `cpp-development`; reproducing and narrowing bugs generally is `debugging-workflow`; profiling is `performance-profiling`; exploiting a bug is out of scope. Sanitizer builds are for development and CI, not for shipping.

## Non-negotiable rules

1. **Sanitizers are test builds.** Do not ship them to production: they increase memory and time substantially, ASan/MSan runtimes widen attack surface and print memory addresses, and some options (like `ASAN_OPTIONS` environment settings) change behavior. Use a separate build directory.
2. **Treat reports as bugs until proven otherwise.** First fix the real defect; suppress only with a written justification and an owner. A suppression file entry hides evidence for everyone downstream.
3. **One sanitizer family per build.** Plan separate builds: (ASan [+LSan] [+UBSan]), TSan, MSan.
4. **Do not run untrusted inputs with sanitizers on shared infrastructure** without isolation; reports can expose stack and heap contents. Do not paste reports containing secrets (heap dumps in report shadow bytes are small but stack frames and strings can leak) into public issues without review.
5. **Do not "fix" by silencing**: no `-fno-sanitize=...` on the failing file, no `__attribute__((no_sanitize))`, and no `halt_on_error=0` to reach green, unless the user approves and the reason is recorded.

## Choosing the sanitizer (decision table)

| Symptom / goal | Sanitizer | Flag | Combine with |
|---|---|---|---|
| Heap/stack/global buffer overflow, use-after-free, double free, use-after-return/scope | AddressSanitizer | `-fsanitize=address` | LSan (included by default on Linux), UBSan |
| Leaks at exit | LeakSanitizer | on by default inside ASan on Linux; `-fsanitize=leak` standalone | ASan, UBSan; not TSan |
| Signed overflow, bad shifts, null deref, misaligned access, invalid enum/bool, etc. | UndefinedBehaviorSanitizer | `-fsanitize=undefined` | ASan |
| Data races, lock-order issues in threaded code | ThreadSanitizer | `-fsanitize=thread` | Not with ASan/LSan |
| Reads of uninitialized memory | MemorySanitizer (Clang only) | `-fsanitize=memory` | Not with ASan or TSan; see below |

Hard facts:

- `-fsanitize=address` with `-fsanitize=thread` is rejected by the driver; verified locally with Apple clang 21 ("not allowed with"). GCC documents that address cannot combine with thread or hwaddress, and thread cannot combine with address or leak.
- **MemorySanitizer is incompatible with ASan** in practice (separate shadow memory designs); build it separately. It is Clang-only, Linux/FreeBSD/NetBSD per the Clang docs; Apple clang here reported `-fsanitize=memory` unsupported on arm64-darwin. GCC has no MSan.
- **MSan requires every piece of code to be instrumented**, including C++ standard library and any third-party library you link, otherwise you get false reports. Prefer an MSan-built libc++, or the project's documented MSan build. Inline assembly that writes memory may need replacement. This is the usual reason MSan adoption fails.
- ASan: static linking of executables is not supported; ASan reserves very large virtual address space on 64-bit, which can collide with `ulimit -v`.
- LSan on Linux needs `ptrace`; inside containers without that permission it can fail at exit. Do not widen container privileges without approval; run ASan with `detect_leaks=0` and run leak checks where ptrace is available.

## Workflow

### 1. Reproduce and pick

Write down the symptom, the input, and the hypothesis class ("heap overflow in parser" -> ASan; "flaky result under threads" -> TSan; "value depends on stack garbage" -> MSan). A symptom that depends on uninitialized memory is often *also* caught by UBSan only partially, so choose deliberately.

### 2. Build in a separate tree

Common baseline (Clang or GCC):

```bash
cc -g -O1 -fno-omit-frame-pointer -fsanitize=address,undefined \
   -fno-sanitize-recover=undefined -o app_asan main.c
```

- `-g` gives symbolized stacks; `-O1` is the documented minimum for sensible speed; `-fno-omit-frame-pointer` improves traces; `-fno-optimize-sibling-calls` gives more precise frames at a small cost.
- `-fno-sanitize-recover=undefined` makes UBSan abort so failures fail CI (default is to print and continue).
- Link with the same flags; use the compiler driver (not bare `ld`) so the runtime is linked.
- For MSan add `-fsanitize=memory -fsanitize-memory-track-origins=2` (origin tracking shows where the uninitialized value was created, at roughly 1.5-2x extra slowdown) and build all dependencies with it.
- Keep optimization consistent with the failing build when reproducing; some bugs vanish at `-O0`.

### 3. Run and read the report

Runtime options are environment variables: `ASAN_OPTIONS`, `UBSAN_OPTIONS`, `LSAN_OPTIONS`, `TSAN_OPTIONS`, `MSAN_OPTIONS`. The Clang docs state ASan parses LSan/UBSan options from their own variables, not `ASAN_OPTIONS`. Useful: `UBSAN_OPTIONS=print_stacktrace=1`, `ASAN_OPTIONS=detect_stack_use_after_return=1` (already the default on Linux with Clang 15+ via runtime mode), `help=1` to list flags for your runtime version.

Read an ASan report in this order:
1. **Error type and access** (`heap-buffer-overflow ... READ of size 4`): classifies the bug.
2. **Top stack frame in your code**: where the bad access happened.
3. **"is located N bytes after/inside a region ... allocated by"**: the object and its allocation site.
4. **"freed by"** (for use-after-free): the other half of the story; the bug is the lifetime mismatch between the two stacks.
5. **Shadow bytes**: rarely needed after steps 1-4.

TSan reports show two conflicting accesses and the threads/mutexes involved; fix by establishing a happens-before relation (lock, atomic with correct ordering), not by adding sleeps. MSan reports "use-of-uninitialized-value" with an origin only if origin tracking is on.

### 4. Fix, then lock in the regression

Add the minimal reproducing input as a test; keep a sanitizer CI job (ASan+UBSan on every change; TSan for threaded code; MSan nightly if you can afford the instrumented dependencies).

## Worked example

Symptom: intermittent crash in `parse_header`. Hypothesis: heap overflow.

```c
#include <stdlib.h>
#include <string.h>
int main(int argc, char **argv) {
    (void)argv;
    char *p = malloc(8);
    memset(p, 0, 8 + (size_t)argc);   /* argc >= 1: writes past the allocation */
    int r = p[0];
    free(p);
    return r;
}
```

Built with `cc -g -O1 -fno-omit-frame-pointer -fsanitize=address,undefined -fno-sanitize-recover=undefined`, ASan (Apple clang 21, arm64 macOS) reported `heap-buffer-overflow ... WRITE of size 9`, "located 0 bytes after 8-byte region", with the allocation site at the `malloc` line. The fix is `memset(p, 0, 8)`. Lesson from authoring: a first version that never used `p` afterwards was optimized away at `-O1` and reported nothing, so a clean run proves little unless the code path survives optimization. Report wording varies by compiler version and platform.

## Anti-patterns

- Combining ASan with TSan or MSan "to save CI time".
- Enabling MSan without instrumenting libc++/dependencies, then dismissing the false positives (and the real ones).
- Merging a suppression to get green without root-causing.
- Running a sanitizer build with the production allocator preloaded (`LD_PRELOAD` of another allocator conflicts with ASan's interceptors).
- Interpreting only the top frame; for use-after-free the free stack is half the evidence.
- Declaring a program "clean" after one run: sanitizers only find bugs on executed paths. Pair with fuzzing or broader tests.
- Shipping or benchmarking sanitized binaries.

## Verification checklist

- [ ] Sanitizer chosen to match the bug class; no invalid combination (ASan with TSan/MSan).
- [ ] Separate sanitizer build with `-g` and frame pointers; same flags at link.
- [ ] UBSan configured to fail (`-fno-sanitize-recover`) in CI.
- [ ] For MSan: all dependencies instrumented, origin tracking on.
- [ ] Root cause fixed; regression test added; any suppression justified and owned.
- [ ] Reports reviewed for sensitive data before sharing.

## References

- [references/flags-and-options.md](references/flags-and-options.md): flag, environment variable and compatibility tables.
- [references/scenarios.md](references/scenarios.md): scenarios.
- [references/sources.md](references/sources.md): sources and provenance.
