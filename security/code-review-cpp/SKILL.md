---
name: code-review-cpp
description: >
  Security review of C / C++ code — memory-safety and the classic unsafe-API sinks. Load when
  reviewing C/C++ source/PR, on .c/.cc/.cpp/.h in scope, or "review this C code". Signals:
  Makefile/CMakeLists, strcpy/sprintf/memcpy, malloc/free, raw pointers, format strings, parsers.
domain: code-review
type: reference
stability: learning
modes: [defense, pentest, bugbounty]
severity: info
cwe: [CWE-119, CWE-787, CWE-416, CWE-134, CWE-190, CWE-78]
tools: [clang-analyzer, cppcheck, semgrep, asan, valgrind]
schema_version: 1
---

# C / C++ source review

## When it applies
Reviewing native C/C++ (a service, a parser, a library). The bugs are overwhelmingly memory safety —
the highest-impact, most exploitable class — plus the handful of unsafe APIs that cause them.

## Why it works
C/C++ has no bounds checking: a length mistake, a lifetime mistake, or attacker-controlled format
string becomes a memory-corruption primitive. Most of these trace to a small, greppable set of APIs
and patterns, and sanitizers/fuzzing confirm the ones static reading only suspects.

## Sinks & patterns (grep, then reason about lengths and lifetimes)
- **Buffer overflow**: `strcpy`, `strcat`, `sprintf`, `gets`, `scanf("%s")`, `memcpy`/`memmove` with
  an unchecked or attacker-influenced length; fixed stack buffers filled from input.
- **Format string**: `printf(user)`, `fprintf(f, user)`, `syslog(user)` — user data as the format arg.
- **Integer issues**: size/length arithmetic that can overflow or go negative and then feeds an
  allocation or copy (`malloc(n*size)`, `len-1`); signed/unsigned confusion in bounds checks.
- **Use-after-free / double-free**: `free` then use; ownership unclear across functions; dangling
  pointers after realloc; C++ iterator invalidation, dangling references, `std::move` misuse.
- **Off-by-one / OOB**: `<=` in loop bounds, missing NUL terminator, `strncpy` not null-terminating.
- **Command/path**: `system`/`popen`/`exec*` with concatenated input; unchecked `../` in path handling.
- **C++ specifics**: unchecked `.at()` vs `[]`, unsafe `reinterpret_cast`, deserialization of
  untrusted data into objects, `std::string`↔C-string length mistakes.

## Method
1. Run `clang --analyze`/`cppcheck` and `semgrep`; treat as leads.
2. `rg 'strcpy|strcat|sprintf|gets|memcpy|system\(|printf\s*\([^"]'` and, for each, trace the size and
   the source of the data.
3. For every allocation/copy, check the length's origin and arithmetic for overflow.
4. Where reachable with input, confirm with a fuzzer + ASan (`libFuzzer`/AFL++) — a crash under ASan
   is proof; escalate to `exploit-memory-corruption` for exploitability.

## Gotchas
- A crash isn't automatically exploitable, but under ASan it's a real memory-safety bug worth reporting.
- Modern C++ (`std::span`, `std::string_view`, smart pointers) reduces but doesn't remove these —
  raw buffers and FFI boundaries are where they persist.
- `strncpy`/`snprintf` are safer but have their own truncation/termination traps — read the lengths.

## References
CERT C/C++ Coding Standard; OWASP C-Based Toolchain hardening; ASan/libFuzzer docs.
