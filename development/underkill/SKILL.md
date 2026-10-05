---
name: "underkill"
description: "Use when writing or modifying code — implementing features, refactoring, or fixing bugs — to prevent over-engineering: unrequested abstractions, options, config, dependencies, and defensive code. Build exactly what was asked, nothing more."
---

# underkill

<!-- Generated from rules.md by scripts/build-dist.ts. Do not edit by hand. -->

Your job is to build exactly what was asked — nothing more. Extra abstraction,
options, and defensive code look thorough but are scope you were not given.
Follow these rules when writing or changing code.

1. **Scope lock.** Implement only what was requested. Ideas for more go in a
   short "Suggestions" note at the end of the task, never in the code.

2. **Rule of three.** Do not create a helper, base class, generic, or interface
   until there are 3+ real call sites in this diff. Two duplicates: copy-paste.

3. **No unrequested surface.** No config files, option arguments, env vars, CLI
   flags, exported symbols, or dependencies that the request did not ask for.
   "It might be nice to have" is not a reason to add.

4. **Boundary-only validation.** Validate at system boundaries (user input,
   external APIs) only. Trust internal code and framework guarantees. No error
   handling or fallbacks for cases that cannot occur.

5. **Declare the diff budget.** Before writing code, state the expected size
   (e.g. "~2 files, ~40 LOC"). If the real diff exceeds 1.5×, stop, say in one
   line what grew the scope, and re-scope to the minimum. When running
   non-interactively, do not wait for a reply — report the overrun and proceed
   with the smallest version yourself.

6. **Simplify pass.** Before calling it done, make one pass to delete anything
   the request and tests do not require — comments, abstractions, defensive
   code included. When there is nothing left to cut, you are done.
