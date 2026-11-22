---
name: cpp-safety
description: Review Yuzu C++ source changes for resource ownership, RAII, borrowed lifetimes, C ABI contexts, casts, process/syscall boundaries, callbacks, threads, and sanitizer coverage. Use for any governance Gate 3 review when C++ files change, paired with cpp-expert.
---

# C++ Safety

Use this skill for C++ ownership and lifetime proof. Pair it with `cpp-expert`, which covers general C++23 correctness and portability.

## Review Focus

- Load `docs/cpp-conventions.md` before reviewing C++ source changes.
- Verify every owning raw resource boundary in the Gate 1 Resource Ledger: fd, HANDLE, SOCKET, `FILE*`, SQLite, OpenSSL, BCrypt, allocated C string, mapped library, temp path, subprocess, callback context, and thread.
- Review broad mechanical hits such as `new`, `delete`, `malloc`, `free`, `release()`, `raw()`, casts, shell/process APIs, callback registration, and thread creation. Require ledger entries only when a hit creates, transfers, or releases ownership of an owning raw resource boundary.
- Flag leaks, double-release, early-return cleanup gaps, borrowed data escape, unsafe shell construction, ambiguous thread teardown, and undocumented cast assumptions.
- Require targeted ASan/UBSan/TSan or platform-specific validation when ownership, callbacks, shared state, or OS handles change.

## Output

Return findings first, with severity `BLOCKING`, `SHOULD`, or `NICE`, each grounded in `file:line` and a concrete fix. End with `Resource Ledger: complete/incomplete`, sanitizer coverage needed, and `PASS` or `BLOCKED`.
