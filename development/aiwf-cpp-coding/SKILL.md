---
name: aiwf-cpp-coding
description: Use for C++ source, CMake, compiler flags, ABI, ownership, templates, concurrency, and ISO C++ compatibility work.
---

# AIWF C++ Coding

## Core Rule

Match the project's configured C++ standard, compiler, ABI, and build system before editing. Prefer idiomatic C++ that fits the local codebase: RAII for ownership, explicit lifetimes at boundaries, and narrow changes that preserve tests and binary contracts.

## Workflow

1. Inspect `CMakeLists.txt`, presets, package manager files, CI, compiler flags, `CMAKE_CXX_STANDARD`, `target_compile_features`, exported headers, and library boundaries.
2. Confirm whether the project targets C++17, C++20, C++23, or another level. Do not introduce newer library or language features unless the target allows them.
3. Identify ownership and ABI surfaces before changing signatures, templates, inline functions, virtual methods, exported symbols, exception behavior, RTTI usage, or allocator behavior.
4. Patch with local style: smart pointers where ownership is real, references where non-null borrowing is clear, spans/views only when supported, and `const` correctness without churn.
5. Build and test with the repo-native command. For template/header changes, run the broadest practical compile surface because failures may appear in downstream translation units.

## C++ Guardrails

- Prefer RAII over manual cleanup. If raw pointers remain, make ownership and nullability explicit in naming, docs, or types.
- Avoid broad template metaprogramming, concepts, coroutines, modules, or ranges unless the project already uses them.
- Keep exception and error-code strategy consistent. Do not add thrown exceptions in no-exception or C-style boundary code.
- Protect ABI: public struct layout, enum values, virtual method order, inline function changes, and exported names can break consumers.
- For concurrency, prefer existing primitives and document synchronization ownership. Avoid detached threads unless the project already has a lifecycle pattern.
- Treat C interop as a boundary: no C++ names, templates, exceptions, or STL types in C ABI headers.

## Validation Defaults

Prefer existing commands. Useful fallbacks:

```powershell
cmake --build <build-dir> --config Debug
ctest --test-dir <build-dir> --output-on-failure
clang++ -std=c++20 -Wall -Wextra -Wpedantic -c <file.cpp>
g++ -std=c++20 -Wall -Wextra -Wpedantic -c <file.cpp>
```

Use the project target standard in fallback commands; do not assume C++20.

## Primary Source Anchors

- ISO C++ standard status: https://isocpp.org/std/the-standard
- C++ Core Guidelines: https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines

When compiler/library support matters, verify the current compiler documentation or CI target before claiming support.
