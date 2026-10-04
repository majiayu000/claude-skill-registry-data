---
name: modern-cpp
description: Write, review, and modernize C++ with repository-compatible language features, precise interfaces, RAII, explicit ownership, safe concurrency, and measured hardening. Use for C++ implementation, refactoring, API design, or safety review; do not use for pure C or build-system-only work.
---

# Modern C++

Write the smallest clear C++ that fits the repository. Inspect the configured language standard, supported compilers, ABI constraints, formatter, warning policy, error model, and nearby code before choosing an idiom. Repository constraints and user requirements take precedence over newer syntax.

Keep changes focused. Do not upgrade the language standard, replace a project-wide error strategy, or modernize unrelated code unless the task requires it.

## Design baseline

- Make ownership, lifetime, nullability, units, valid states, and failure behavior visible in types and interfaces.
- Prefer value semantics, deterministic cleanup, ordinary control flow, and standard-library facilities.
- Use RAII for every resource, including files, handles, locks, mappings, sockets, and transactions.
- Prefer scoped objects and `std::unique_ptr`. Use `std::shared_ptr` only for genuine shared lifetime. Raw pointers and references are normally non-owning.
- Initialize objects before use. Apply `const` when a value should remain stable and doing so clarifies the design; do not force immutability when localized mutation better represents the algorithm.
- Preserve public behavior and ABI unless the requested change requires otherwise.
- Comment invariants, ownership exceptions, synchronization rules, ABI constraints, and non-obvious tradeoffs. Do not narrate the code.

For interface, function, class, ownership, error-handling, concurrency, template, and source-file decisions, read [core-guidelines.md](./references/core-guidelines.md).

## Feature selection

Use a feature only when the project's selected standard and supported toolchains implement it well.

| Need | Prefer when available | Important boundary |
|---|---|---|
| Non-owning contiguous input | `std::span` | The source must outlive the view. |
| Non-owning text input | `std::string_view` | Do not retain a view into temporary or mutable storage. |
| Optional value | `std::optional` | A pointer can still be clearer for optional object identity. |
| Closed alternatives | `std::variant` | C unions may still be required at ABI or hardware boundaries. |
| Typed expected failure | `std::expected` | Follow the repository's established exception, status, or result model. |
| Constrained generic code | concepts and `requires` | Requires C++20; do not add templates without a useful abstraction. |
| Thread with owned lifetime | `std::jthread` | Requires C++20 and does not replace a clear shutdown protocol. |
| Multiple mutex acquisition | `std::scoped_lock` | Define the protected invariant and lock scope first. |
| Type-safe formatting | `std::format` or `std::print` | Confirm library support and preserve logging facilities. |
| Type punning | `std::bit_cast` | Types must satisfy its size and trivial-copyability requirements. |

Read the version-specific reference only when that version is available or under consideration:

- [cpp20-features.md](./references/cpp20-features.md)
- [cpp23-features.md](./references/cpp23-features.md)
- [cpp26-features.md](./references/cpp26-features.md)

Use [anti-patterns.md](./references/anti-patterns.md) to evaluate a legacy replacement. Treat the table as options, not mechanical rewrite rules: C APIs, embedded targets, kernels, allocators, stable ABIs, and older toolchains often require lower-level representations.

## Safety and hardening

For security-sensitive or boundary-heavy code, read [safe-idioms.md](./references/safe-idioms.md). Check sizes, conversions, bounds, iterator validity, lifetime, partial operations, cleanup after failure, and concurrency invariants.

For compiler and CI hardening, read [compiler-hardening.md](./references/compiler-hardening.md). Select flags by compiler, platform, build type, dependency policy, and measured overhead. Do not apply `-Werror`, sanitizer settings, linker flags, or a standard-library hardening mode universally without checking compatibility.

## Review

Before finishing:

- Confirm the code builds under the repository's actual standard and supported toolchains.
- Check that ownership and borrowed lifetimes remain valid across every exit path.
- Check narrowing, signedness, overflow, bounds, invalid states, and ignored failures at affected boundaries.
- Check Rule of Zero/Five and polymorphic destruction when special members or inheritance are involved.
- Check lock scope, wait predicates, callbacks under locks, cancellation, and shutdown when concurrency is involved.
- Run the repository formatter and the narrowest relevant build, tests, static analysis, or sanitizers.
- Keep performance claims tied to equivalent benchmarks or a clear complexity result.

## Loading in Oh My Pi

Relative paths in this skill (`references/…`, `scripts/…`) resolve against the skill's own directory. Read them with `skill://modern-cpp/<relative-path>`. When a shell command needs a real filesystem path, that directory is `<OMP_HOME>/skills/modern-cpp/` — `~/.omp/agent/skills/modern-cpp/` by default. Invoking `/skill:modern-cpp` also prints the resolved location.
