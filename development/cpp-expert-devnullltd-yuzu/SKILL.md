---
name: cpp-expert
description: Review Yuzu C++ source changes for C++23 correctness, idiomatic standard-library use, ABI boundaries, threading primitives, and cross-compiler portability across GCC, Clang, MSVC, and Apple Clang. Use for any governance Gate 3 review when `.cpp`, `.hpp`, or `.h` files change.
---

# C++ Expert

Use this skill for general C++ language review. Pair it with `cpp-safety` for ownership and lifetime proof; this skill covers correctness, idiom, portability, and ABI shape.

## Review Focus

- Load `docs/cpp-conventions.md` before reviewing C++ source changes.
- Check `std::expected`, `std::string_view`, `std::span`, `std::format`, templates, concepts, move semantics, and concurrency primitives for correct C++23 use.
- Check plugin ABI boundaries: no C++ types, exceptions, or unstable ownership contracts cross `sdk/include/yuzu/plugin.h`.
- Check cross-compiler behavior against the supported matrix: GCC 13+, Clang 18+, MSVC 19.38+, and Apple Clang 15+.
- Flag undefined behavior, use-after-move, ODR hazards, narrowing conversions, missing includes, non-portable extensions, and unnecessary copies on hot paths.

## Output

Return findings first, with severity `BLOCKING`, `SHOULD`, or `NICE`, each grounded in `file:line` and a concrete fix. End with `PASS` or `BLOCKED`.
