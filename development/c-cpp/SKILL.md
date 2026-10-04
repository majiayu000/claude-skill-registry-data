---
name: c-cpp
description: "Applies C/C++ rules for resource safety, ownership, ABI, builds, tests, and validation."
---

# Skill: c-cpp

## Purpose

Apply the shared engineering style to C and C++ projects while respecting safety, ABI, build configuration, resource ownership, and platform constraints.

## Inspect First

Before changing C/C++ code, inspect relevant files when present:

- `CMakeLists.txt`
- `Makefile`
- build scripts
- compiler flags
- toolchain files
- `compile_commands.json`
- formatter/linter config
- existing headers/source/tests
- target platform constraints

Infer:

- C/C++ standard;
- compiler/toolchain;
- warning policy;
- memory ownership style;
- test framework;
- embedded constraints if relevant.

Do not assume language standard or ABI expectations.

## General Rules

- Preserve ABI when relevant.
- Avoid undefined behavior.
- Keep ownership explicit.
- Keep headers minimal and stable.
- Avoid unnecessary dynamic allocation.
- Avoid global mutable state.
- Prefer small translation units with cohesive responsibility.
- Do not create giant headers full of unrelated code.

## C++ Rules

- Prefer RAII.
- Avoid raw owning pointers.
- Use `const` correctly.
- Prefer value semantics when appropriate.
- Use smart pointers only when ownership requires them.
- Avoid inheritance unless polymorphism is real.
- Prefer composition over inheritance.
- Avoid exceptions if the project forbids them; otherwise follow project convention.
- Do not use modern features unsupported by configured standard.

## C Rules

- Make ownership and lifetime explicit in names/docs.
- Check allocation and I/O failures.
- Avoid buffer overflows.
- Prefer bounded operations.
- Keep error paths correct.
- Do not hide resource ownership in vague helper functions.

## Embedded / Firmware Awareness

When code may run on constrained hardware:

- avoid blocking critical loops;
- avoid unbounded allocation;
- consider stack usage;
- consider ISR constraints;
- avoid unsafe boot states;
- preserve watchdog behavior;
- be careful with volatile/hardware registers;
- isolate platform-specific code.

## Tests and Validation

Use existing build/test system.

Common commands, only when configured or clearly available:

```bash
cmake --build <build-dir>
ctest --test-dir <build-dir>
make
make test
ninja
```

Report exact commands and results.
## Shared Cross-Ecosystem Style


Apply the shared engineering style from:

- `../../engineering/05_design_principles.md`
- `../../engineering/06_responsibility_model.md`
- `../../engineering/07_complexity_budget.md`
- `../../engineering/12_naming_bible.md`

Language-specific idioms control syntax and ecosystem details, but they must not weaken the core rules: small cohesive units, explicit boundaries, honest validation, no dumping grounds, and no fake placeholders.
