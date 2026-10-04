---
name: simplify
description: Read-only review for overengineering and avoidable complexity. Use when Charlie asks what can be deleted, whether code is overengineered, or requests a simplification review. Do not use for an ordinary implementation request that merely uses the word simplify.
license: MIT
metadata:
  source: adapted from ponytail-review (github.com/DietrichGebert/ponytail)
---

# Simplify

Review the requested artifact for complexity that can be removed without changing the intended outcome. Do not edit unless a later request asks for the accepted changes.

Default scope is the current branch against its merge base plus uncommitted changes. Use the fixed point or files Charlie names when supplied.

A finding must name what disappears and what replaces it. Label its provenance as `branch`, `made-obsolete`, or `pre-existing` so the user can decide whether it belongs in the current change. Look for:

1. Dead code, unused options, and speculative extension points. Before calling code unused, trace its callers, entry points, and runtime selection. A documentation label alone is not evidence for deletion.
2. A custom helper that the standard library, platform, dependency, or current codebase already provides.
3. An abstraction with one caller and no concrete second variation.
4. Parallel representations of the same fact.
5. A refactor that moved complexity without reducing the concepts a maintainer must hold.
6. Branches or fallbacks that hide an unclear model.

Use one line per finding:

`path:line: <tag> [<provenance>]: <what to remove>. <replacement>.`

Tags are `delete`, `reuse`, `stdlib`, `native`, `yagni`, and `shrink`.

Do not report correctness, security, or performance defects as simplification findings. Do not flag a focused smoke test or assertion merely because it adds lines. Avoid line count theater. When useful, end with a clearly labeled rough estimate of code that could disappear, not a claimed exact total.

When Charlie explicitly asks for an unusually strict maintainability pass, also load [`references/strict-maintainability.md`](references/strict-maintainability.md).

If nothing material can be removed, return `Lean already.` and name the main surfaces checked.
