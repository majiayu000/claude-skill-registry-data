---
name: kit-overengineering-review
description: Review code or a diff specifically for unnecessary complexity, including speculative abstractions, single-implementation interfaces, reinvented standard library or platform features, unneeded dependencies, dead configuration, and indirection that adds no value, and report what to delete or simplify with the simpler replacement. Use when the user asks whether code is over-engineered, what can be deleted or simplified, or for a YAGNI, simplicity, or complexity review. Do not use for correctness or security review (use kit-code-review or kit-security-audit), or for carrying out the simplification (use kit-refactoring); this skill reports and does not edit code.
---

# Over-engineering review

Report findings without modifying code unless the user asks.

## 1. Determine the scope

Review the files, module, or diff the user named; otherwise the uncommitted changes and the current branch against its base. Read the call sites and tests so each finding reflects how the code is actually used, and read project instructions for conventions that justify structure.

## 2. Look for

- **Speculative generality:** interfaces, abstract classes, factories, or strategy patterns with one implementation; plugin systems with one plugin; parameters and options no caller passes; configuration for values that never change.
- **Reinvention:** hand-written code for what the standard library, the platform (database constraints, HTTP framework features, CSS), or an already-installed dependency provides.
- **Unneeded dependencies:** packages used for a few lines of code the project could own, or that duplicate another installed package.
- **Indirection:** wrappers that only forward calls, layers that pass data through unchanged, deep inheritance, events or queues where a function call would do.
- **Dead weight:** unused exports, flags, branches, compatibility shims for versions no longer supported, and commented-out code.
- **Premature optimization:** caches, pools, or concurrency without a measured need, especially where they add invalidation or race risks.

Keep structure that has a concrete reason: a second implementation in tests is not enough on its own, but a real second backend, a published API contract, or a documented extension point is. Respect language idioms, such as small Go interfaces declared by the consumer as test seams.

## 3. Report

For each finding, give `file:line`, what to delete or simplify, the simpler replacement (named function, built-in, or inline code), and the estimated lines removed. Order by payoff. Note what was checked and kept on purpose. If the code is already simple, say so.

## Examples

- Use: "Is this module over-engineered?" "What can we delete from src/services?" "YAGNI review of my branch."
- Skip: "Review this PR for bugs." (kit-code-review) "Simplify this module." (kit-refactoring, which makes the change)
