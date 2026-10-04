---
name: sota-c-cpp
description: >-
  State-of-the-art C and C++ engineering rules that Claude
  applies when writing or auditing C/C++. Covers modern idioms (RAII, value
  semantics, smart pointers, C++23), memory safety (lifetimes, bounds,
  sanitizers, hardening flags), undefined behavior, security (SEI CERT C/C++,
  MISRA, integer/buffer/format-string, injection), concurrency (C/C++ memory
  model, atomics, data races), build/tooling/CI (CMake, clang-tidy, cppcheck,
  ASan/UBSan/TSan, vcpkg/Conan, supply chain), and performance. Trigger keywords
  - C, C++, RAII, smart pointer, unique_ptr, shared_ptr, undefined
  behavior, UB, buffer overflow, use-after-free, sanitizer, ASan,
  UBSan, TSan, valgrind, CMake, clang-tidy, cppcheck, MISRA, CERT
  C, memory safety, std::thread, atomics, std::move. Use for BOTH building
  C/C++ libraries/systems and reviewing or auditing them. Owns firmware's LANGUAGE
  layer; does NOT own its SYSTEMS layer — ISRs, DMA coherency, MMIO, RTOS
  scheduling, priority inversion, WCET, linker scripts — unowned library-wide.
---

# SOTA C & C++ (2026)

Expert-level rules for producing and auditing production C and C++. C and C++
are *memory-unsafe by default*: the compiler will not stop you from reading
freed memory, overrunning a buffer, or invoking undefined behavior (UB) that
the optimizer then weaponizes. These rules exist to claw back the safety the
language doesn't give you — through RAII, the type system, sanitizers, hardened
build flags, and disciplined review. Baseline: C++23 (ISO/IEC 14882:2024) and
C17/C23; flag where a control needs a newer toolchain. C++26 is feature-complete
(DIS ballot 2026) — contracts, reflection, erroneous behavior for uninitialized
reads, and a standardized hardened standard library; the last is usable today
via libc++/libstdc++ hardening flags (`rules/02`). Every rule states the
*why*; every rules file ends with an audit checklist of grep/clang-tidy/
sanitizer patterns.

## Purpose

Two consumers, one source of truth:

- **BUILD mode** — generating new C/C++: follow the rules as defaults, not
  suggestions. Prefer C++ with RAII over raw C idioms unless the target is C.
  Deviate only with a comment justifying it.
- **AUDIT mode** — reviewing existing C/C++: hunt violations using the audit
  checklists, classify by severity, report in the finding format below. Memory-
  safety and UB findings are presumed exploitable until proven otherwise.

**What this skill covers about embedded work, and what it does not.** It carries the
safety-critical *coding* standards — MISRA C:2025 / C++:2023 and SEI CERT (`rules/04`),
freestanding builds with exceptions disabled (`rules/01` §7), banned APIs and hardened
build flags — so a firmware codebase gets real coverage of the language layer. It does
**not** cover the systems layer that makes embedded work its own discipline: interrupt
service routines and reentrancy, DMA buffer coherency, memory-mapped I/O and `volatile`
semantics against a peripheral, RTOS task scheduling and priority inversion, WCET and
timing analysis, or linker scripts and startup code. No skill in this library owns those
today. Say so when the task reaches them rather than generalising from the desktop rules —
guidance that sounds authoritative outside its scope is the failure `sota-skill-security`
exists to catch.

## BUILD mode

1. Before writing, read the rules files relevant to the task (see index). A
   parser handling untrusted bytes needs `02`, `03`, `04`; a threaded service
   needs `05`.
2. Apply the **top-10 non-negotiables** (below) unconditionally.
3. New projects: CMake (≥3.20) with `-Wall -Wextra -Wpedantic` (`-Werror` in CI, not in distributed sources), the
   [OpenSSF hardening flags](https://best.openssf.org/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.html)
   (`rules/04`), a debug build wired to ASan+UBSan, clang-tidy + clang-format
   configs, and CI running all of it from day one (`rules/06`).
4. Prefer the standard library and RAII types over hand-rolled
   allocation/ownership. Every `new`/`malloc`/`fopen`/`mutex.lock()` should be
   owned by a destructor (`unique_ptr`, container, `lock_guard`), not a manual
   matching call you can forget on an early return or exception.
5. Treat warnings as errors. A clean `-Wall -Wextra` build is the floor, not
   the goal — also run a static analyzer and the sanitizers (`rules/06`).
6. When you must use a sharp tool (raw pointer arithmetic, `reinterpret_cast`,
   `unsafe` C interop, manual lifetime), leave a `// NOTE(sota):` comment
   explaining the invariant you're upholding so auditors don't flag it blind.

## AUDIT mode

Work through each relevant rules file's audit checklist against the target.
Run the listed grep/clang-tidy/sanitizer commands; confirm each hit manually
(greps are recall-oriented). Where feasible, build with `-fsanitize=address,
undefined` and run the test suite — a sanitizer abort is ground truth.

### Severity conventions

| Severity | Meaning | Examples |
|---|---|---|
| **CRITICAL** | Exploitable memory corruption or guaranteed UB on reachable input | Heap/stack buffer overflow on attacker data, use-after-free, double-free, OOB write, format-string with user-controlled fmt, `system()` with interpolated input, data race on a pointer |
| **HIGH** | Likely corruption, crash, or security weakness | Unchecked `malloc`/`new` size from input, integer overflow feeding an allocation or index, missing bounds check, `strcpy`/`sprintf`/`gets`, TOCTOU on a path, missing RAII so a leak/UB occurs on the exception path |
| **MEDIUM** | Correctness/maintainability hazard, latent bug | Raw owning pointers, manual `new`/`delete` pairs, C-style casts, narrowing conversions, `memcpy` where a typed copy fits, missing `override`/`= delete`, signed/unsigned comparison |
| **LOW** | Idiom/perf debt, works but wrong shape | Pass-by-value of large objects, needless copies instead of `std::move`, `using namespace std` in headers, macros where `constexpr`/`inline` fits |
| **INFO** | Style/doc/hygiene | clang-format drift, naming, missing `[[nodiscard]]`, include hygiene |

### Finding format

```
[SEVERITY] file.cpp:LINE — short title
  Rule: rules/NN-name.md § section
  Evidence: the offending line(s), verbatim
  Impact: one sentence — what corrupts/leaks/races, under what input
  Fix: concrete replacement code or action
  Effort: trivial | small | medium | large
```

Group findings by severity, CRITICAL first. End with: counts per severity, the
three highest-leverage fixes, and which checklists/sanitizers were run.

## Rules index

| File | Read this when... |
|---|---|
| `rules/01-idioms.md` | Writing/reviewing any C++: RAII and the rule of zero/five, ownership with `unique_ptr`/`shared_ptr`, value semantics and move, `const`/`constexpr`, references vs pointers, casts, `enum class`, error handling (exceptions vs `std::expected` vs error codes), **in-band sentinels (absence encoded as `-1`/`0`/`""`)** incl. **`EOF` in a `char` — broken only where `char` is unsigned**, C-vs-C++ idiom choices |
| `rules/02-memory-safety.md` | Anything touching pointers, buffers, lifetimes, or allocation: bounds, use-after-free/return, dangling references and views (`string_view`/`span`), iterator invalidation, ownership discipline, sanitizers (ASan/MSan), `_FORTIFY_SOURCE`/`_GLIBCXX_ASSERTIONS`, Clang Safe Buffers (`-Wunsafe-buffer-usage`) |
| `rules/03-undefined-behavior.md` | Reasoning about UB and the optimizer: integer overflow, strict aliasing, uninitialized reads, null/misaligned access, signed shifts, data races as UB, `unsigned` arithmetic, overflow checks the optimiser deletes (`-fno-strict-overflow`/`-fwrapv` in production, never instead of a checked `ckd_*`), C++26 `std::saturating_*`, C++26 erroneous behaviour and its limits (`[[indeterminate]]`, heap), union `= {0}` on GCC 15+, UBSan, TypeSanitizer, **C++26 contracts are not input validation** (evaluation semantics), why "it worked in debug" proves nothing |
| `rules/04-security.md` | Any input crossing a trust boundary: CERT C/C++ + MISRA, banned functions (`gets`/`strcpy`/`sprintf`/`system`), integer-overflow-to-allocation, format strings, path traversal/TOCTOU, command injection, SSRF through libcurl (connect-time address check, redirects, protocol allowlist), regex as a control (escaping, full-match anchoring, backtracking `std::regex`/PCRE2 vs linear-time RE2), deserialization/parsers, dynamic code evaluation (embedded Lua/Python interpreters, `dlsym` by input name), app-set cookie attributes (Drogon, Crow, cpp-httplib), CSPRNG, secret wiping (`memset_explicit`), the OpenSSF hardening flag set (plus inert flags, `-strong` vs `-all` canaries, retpoline thunks), hardening opt-out macros (`-U_FORTIFY_SOURCE`, `_CRT_SECURE_NO_WARNINGS`), Windows/MSVC binary hardening (`/sdl`, `/guard:cf`, `/CETCOMPAT`, BinSkim, process mitigations), a shipped debug/sanitizer build refused at compile time |
| `rules/05-concurrency.md` | Anything with threads, atomics, or shared state: the C++ memory model, data races, `std::atomic` and memory orders, `mutex`/`lock_guard`/`scoped_lock`, deadlock ordering, condition variables, `std::jthread`/stop tokens, request-scoped state in `thread_local` or a logging MDC on reused threads and across `co_await`, TSan |
| `rules/06-build-tooling-ci.md` | Setting up or auditing builds/CI: CMake hygiene, pinning the C/C++ dialect (GCC 15/16 moved the defaults), `-fpermissive` as a finding, Debug/Release configurations and the NDEBUG/DEBUG guard, flags that never reach a unit (stale objects, overridden `CFLAGS`, vendored libraries), warning flags (periodic `-Weverything`, per-site suppression), clang-tidy/clang-format, static analysis (clang-analyzer, cppcheck, Coverity), sanitizer CI matrix and the trap-mode UBSan subset that may ship, fuzzing (libFuzzer/OSS-Fuzz), dependencies and supply chain (vcpkg/Conan, pinning, SBOM, selecting a new dependency and overriding its insecure defaults, dependency code that runs at configure/build time). **Test *strategy* lives in `sota-testing`; this file owns C/C++ build/test mechanics.** |
| `rules/07-performance.md` | Latency/throughput/memory work: profiling (perf, VTune, Callgrind), allocation reduction and custom allocators, move/copy elision, cache locality and data-oriented layout, `<algorithm>` over hand loops, LTO/PGO, micro-benchmarking pitfalls |

## Top-10 non-negotiables

1. **Every resource is owned by a destructor (RAII).** No `new`/`delete` or
   `malloc`/`free` pairs you have to match by hand; no bare owning pointers.
   Use `unique_ptr`, containers, `lock_guard`/`scoped_lock`, RAII wrappers.
   A leak or UB on the exception/early-return path is the default failure mode
   of manual cleanup. (`rules/01`, `rules/02`)
2. **No buffer touches memory it doesn't own.** Bounds-check every index/
   length derived from input; use `std::span`/`std::string`/containers and
   `.at()` or explicit checks, never raw pointer + length you assume. Overflow
   on attacker input is CRITICAL. (`rules/02`)
3. **No use-after-free / dangling.** A pointer, reference, iterator,
   `string_view`, or `span` must not outlive its storage. Never return a
   reference/view to a local or to a temporary. (`rules/02`)
4. **Undefined behavior is a bug even if it "works".** Signed integer
   overflow, strict-aliasing violations, uninitialized reads, OOB, data races
   are UB the optimizer may exploit. Build with UBSan; treat any UBSan
   diagnostic as CRITICAL/HIGH. (`rules/03`)
5. **Integers feeding an allocation, index, or `memcpy` size are
   overflow-checked and the right signedness.** Validate ranges before use;
   prefer unsigned for sizes, check for wrap. Overflow-to-undersize-alloc is a
   classic RCE primitive. (`rules/03`, `rules/04`)
6. **Banned functions are banned.** No `gets`, `strcpy`/`strcat`/`sprintf`
   (use bounded forms or `std::string`/`std::format`), no `system()` with
   interpolated input (use `posix_spawn`/`exec*` with an argv array). (`rules/04`)
7. **Build hardened, by default.** `-Wall -Wextra` (`-Werror` in CI; OpenSSF: not blanket
   in distributed sources) plus the OpenSSF set (`-D_FORTIFY_SOURCE=3 -D_GLIBCXX_ASSERTIONS
   -fstack-protector-strong -fstack-clash-protection -Wl,-z,relro,-z,now`, and
   `-fcf-protection=full` on x86_64 or `-mbranch-protection=standard` on AArch64). Missing
   hardening on a network-facing binary is a HIGH finding. (`rules/04`,
   `rules/06`)
8. **Shared mutable state is synchronized; data races are CRITICAL.** Guard
   with a `mutex`/`scoped_lock` or use `std::atomic` with a justified memory
   order. A `-fsanitize=thread` failure is not flaky noise. (`rules/05`)
9. **Sanitizers and a static analyzer gate CI.** A debug/test job runs
   ASan+UBSan (and TSan for threaded code); clang-tidy + cppcheck run on every
   PR. Untrusted-input parsers get a fuzz target. (`rules/06`)
10. **Prefer the type system to convention.** `enum class` over macros,
    `constexpr`/`inline` over `#define`, `gsl::span`/`std::span` over pointer+
    length, `[[nodiscard]]` on must-check returns, `explicit` on single-arg
    constructors, `override`/`final`. Make misuse fail to compile. (`rules/01`)
