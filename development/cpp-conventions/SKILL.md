---
name: cpp-conventions
description: "Use when writing or reviewing C++: types and initialisation, ownership and RAII, errors and exceptions, class design, concurrency, headers and build structure, templates, performance and the shared compiler hardening."
---

# cpp-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of C++ code. The compiler hardening flags
and the sanitizers are **not repeated here**: they are `c-conventions` §5, shared by both languages. Every rule
below holds with the compiler, its warnings and its sanitizers alone.

**Special status**: like `go-conventions`, no in-house production experience stands behind this block. The
content comes from the language's committee-backed core guidelines and from one large organisation's style
guide, read on 2026-10-02 (`references/origin.md`); both are licensed so that **only the mechanisms were
taken, never the wording**. Treat it as a base to be confronted with the first real C++ project.

**Two sources disagree on exceptions, and the block does not pick for you.** The core guidelines build error
handling on exceptions and RAII; the style guide bans exceptions for its own code base. A project is already
on one side, by its build flags and the libraries it links. §3 states both and the rule for choosing: follow
the project's existing choice, and never mix a library that throws into a code base built without them.

## When
As soon as C++ code is written or modified, during `code` (6) or `tdd` (5). Say which language standard the
project builds with before applying a row (concepts, `std::span`, `std::expected`, modules depend on it).

## Steps

**Read only the sections the task actually touches.** A section read is a section that has to be applied.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Types, initialisation and conversions | a variable, an enum, a cast, a string or span parameter, a signed/unsigned mix, a literal null | [`01-types-and-initialisation.md`](./references/01-types-and-initialisation.md) |
| 2 | Resources and ownership | a `new`, a raw pointer in a signature, a smart pointer, a resource that must be released, a lock | [`02-resources-and-ownership.md`](./references/02-resources-and-ownership.md) |
| 3 | Errors and exceptions | a function can fail, a `throw`, a `catch`, `noexcept`, an error code | [`03-errors-and-exceptions.md`](./references/03-errors-and-exceptions.md) |
| 4 | Classes and hierarchies | a class, a constructor, a destructor, copy and move, a virtual function, an operator, a union | [`04-classes-and-hierarchies.md`](./references/04-classes-and-hierarchies.md) |
| 5 | Concurrency | a thread, a mutex, a condition variable, a task, a coroutine, an atomic | [`05-concurrency.md`](./references/05-concurrency.md) |
| 6 | Headers, namespaces and structure | a header, an include, a macro, a namespace, a source layout | [`06-headers-and-structure.md`](./references/06-headers-and-structure.md) |
| 7 | Hardening pointer, templates, functions and performance | build flags, a template or concept, a function signature, an optimisation | [`07-hardening-templates-performance.md`](./references/07-hardening-templates-performance.md) |

## Output / checkpoint
Code compliant with the sections above, built with the warning set and the library precondition checks of
`c-conventions` §5, and the test suite run under the address and undefined-behaviour sanitizers (and the
thread sanitizer for threaded code). A sanitizer or analyser that is not installed is recorded as "not run",
never reported as a pass. Checked by `gate` (7) and `review` (8).

## Guardrails
No comments in the code produced. Never silence a warning with a cast or a pragma, never disable a sanitizer
or a hardening flag to make a test pass: that is a project decision. Rules govern **new** code; legacy code
stays until migrated deliberately, and a rule that the project's standard cannot express is skipped, not
emulated with a macro. This block has not met a real C++ project: if a rule diverges from an observed need,
fix this block.

## Origin
Rules mined from the core guidelines and one style guide for large code bases plus the shared hardening
guide, rewritten in the house voice; licences, pinned versions and the arbitration between the sources are in
[`references/origin.md`](./references/origin.md). Read it when checking whether a rule is still current, not
when applying one.
