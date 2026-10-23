---
name: c-conventions
description: "Use when writing or reviewing C: integer and expression pitfalls, memory and string safety, error and resource handling, threads and signals, the compiler hardening flags and sanitizers, headers and macros."
---

# c-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of C code, and carries the **hardening
and sanitizer section that `cpp-conventions` shares** (§5). Every rule below holds with the compiler alone:
the checks are compiler warnings, sanitizer runs and a code reading.

**Special status**: like `go-conventions`, no in-house production experience stands behind this block. The
content comes from a published secure-coding standard's rule list, an industry hardening guide for compiler
options and a kernel-style note, all read on 2026-10-02 (`references/origin.md`). It is a base to be
confronted with the first real C project, not proven doctrine. In a review, every rule here is a question
register until then.

**C is where a mistake becomes a vulnerability.** The compiler will not stop an out-of-bounds write, a
use-after-free or an integer wrap; the first four sections are about not writing them, the fifth about making
the build catch or contain the ones that slip through. Say which standard of C the project builds with before
applying a row, since several rules depend on it.

## When
As soon as C code is written or modified, during `code` (6) or `tdd` (5).

## Steps

**Read only the sections the task actually touches.** A section read is a section that has to be applied.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Integers, types and expressions | arithmetic on sizes or untrusted numbers, a conversion, a shift, an uninitialised or aliased object, a pointer cast | [`01-integers-types-expressions.md`](./references/01-integers-types-expressions.md) |
| 2 | Memory, arrays and strings | an allocation, an array index, a string copy, a pointer into a buffer, a flexible array member | [`02-memory-arrays-strings.md`](./references/02-memory-arrays-strings.md) |
| 3 | Errors, resources, I/O and the process | a library call can fail, a file or handle is opened, a format string is built, a shell or the environment is touched, cleanup spans several exits | [`03-errors-resources-process.md`](./references/03-errors-resources-process.md) |
| 4 | Threads and signals | a thread, a mutex, a condition variable, an atomic or a signal handler appears | [`04-threads-and-signals.md`](./references/04-threads-and-signals.md) |
| 5 | Hardening flags and sanitizers (shared with C++) | the build flags, a Makefile or CMake file, a CI job, a sanitizer or fuzz run, a function annotation changes | [`05-hardening-and-sanitizers.md`](./references/05-hardening-and-sanitizers.md) |
| 6 | Headers, macros and structure | a header, an include guard, a macro, a file layout is written | [`06-headers-macros-structure.md`](./references/06-headers-macros-structure.md) |

## Output / checkpoint
Code compliant with the sections above, built with the warning set of §5.2 without a new warning, and the
test suite run once under the memory sanitizer and once under the undefined-behaviour sanitizer (§5.9).
Where a sanitizer or a static analyser is not installed, the checkpoint says "not run" and names it; it never
reports a pass it did not observe. Checked by `gate` (7) and `review` (8).

## Guardrails
No comments in the code produced. Never silence a warning with a cast or a pragma to get a diff through, never
disable a sanitizer or a hardening flag to make a test pass: that is a project decision. These rules govern
**new** code; existing code stays until migrated deliberately, and a legacy build that cannot take the full flag
set follows the staged approach of §5.1. This block has not met a real C project: if a rule diverges from an
observed need, fix this block.

## Origin
Rules mined from a published secure-coding standard, an open-source security foundation's compiler hardening
and annotation guides and a kernel style note, rewritten in the house voice; the licences, pinned versions and
the list of what was left out are in [`references/origin.md`](./references/origin.md). Read it when checking
whether a rule is still current, not when applying one.
