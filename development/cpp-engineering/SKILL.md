---
name: cpp-engineering
description: Write modern C++ — RAII, value semantics, STL-first design, sanitizers and static analysis in the loop.
version: 1
triggers: c++, cpp, modern c++, raii, stl, sanitizers
category: Engineering & code
blurb: Write modern C++ — RAII, value semantics, STL-first design, sanitizers and static analysis in the loop.
archetype: knowledge
example: Modernize this C++ code to RAII and value semantics.
---

# C++ Engineering

Modern C++ done deliberately: resources managed by construction, types that carry meaning, and tooling that catches what eyes miss.

## When to use
- C++ services, tooling, game/perf code, cross-platform libraries.
- Modernizing legacy C++ toward C++17/20/23.

## Method
1. **RAII everywhere**: resources (memory, files, sockets, locks) owned by objects; destructors clean up; no manual pairing.
2. **Value semantics first**: prefer values, `const`, and references; move semantics where copies are expensive; follow the Rule of Zero (write special members only when you must).
3. **Smart pointers with intent**: `unique_ptr` default; `shared_ptr` only for real shared ownership; `weak_ptr` to break cycles. No raw owning pointers in new code.
4. **STL-first**: algorithms over hand loops; containers matched to access patterns; ranges where available.
5. **Exceptions policy**: pick one per codebase (exceptions on/off), document it, and be consistent.
6. **Tooling gates**: clang-tidy + clang-format; ASan/UBSan/TSan test builds; warnings as errors.
7. **Templates sparingly**: for real genericity, not vanity; keep error messages readable.
8. **ABI discipline**: for libraries: stable interfaces, pimpl where needed, versioned symbols.

## Quality gates
- [ ] clang-tidy clean on the diff; warnings-as-errors build green.
- [ ] Sanitizer-clean test run.
- [ ] No raw owning pointers or manual `new`/`delete` in new code.
- [ ] Rule of Zero honored (special members only when justified).

## Red lines
- No dangling references across async boundaries.
- No macros where language features exist.

## Related
`c-engineering` (FFI boundaries) · `rust-engineering` (when rewriting hot paths) · `testing-strategy`.
