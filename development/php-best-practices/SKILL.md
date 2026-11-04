---
name: php-best-practices
description: Implement, refactor, debug, or review PHP with explicit runtime compatibility, precise contracts, and framework-aware validation. Use for substantive PHP engineering work; simple conceptual questions do not require this workflow.
---

# BeautifulPHP

Produce clear, idiomatic PHP that satisfies the requested behaviour on the project's supported runtimes. Follow repository instructions and established framework conventions. Keep changes scoped; introduce dependencies and abstractions only when they solve a concrete problem.

## Establish the target and contract

Read affected code, tests, Composer manifests, analysis configuration, and any existing CI, container, or deployment settings. Establish the supported PHP range, required extensions, framework version, and actual execution environment. Distinguish a library's consumer compatibility promise from an application's deployment target. A local interpreter or lockfile alone does not establish either.

Reconcile conflicting version evidence before compatibility-sensitive edits. If the target is unresolved, state the uncertainty and ask for the missing decision while continuing independent work. Do not silently raise the minimum version, narrow the supported range, or bypass platform requirements. Check syntax, built-in APIs, dependencies, and deprecations against the full promised range. Read [compatibility](references/compatibility.md) when establishing a target, upgrading PHP, or using version-sensitive features.

Before refactoring, identify observable contracts: return values, exceptions, side effects, ordering, serialization, and public signatures. Preserve them unless the request authorises changes. Documenting a difference does not authorise it. Add focused regression coverage for demonstrated bugs and fragile boundaries.

## Implement deliberately

- Prefer cohesive functions and objects with clear names and explicit dependencies. Use interfaces for real substitution or public contracts, not one per class. Avoid speculative layers, service locators, global mutable state, and unmeasured optimisation; respect established framework mechanisms.
- Express meaningful constraints with native parameter, return, and property types supported by the target. Use PHPDoc for additional information such as generics and array shapes. Validate external data before treating it as a domain value; casts and type annotations are not validation.
- Distinguish missing keys, null, false, zero, and empty strings. Choose comparisons and presence checks by semantics. Consider array-key coercion, list versus map shape, byte versus character operations, and JSON representation. Read [types and contracts](references/types-and-contracts.md) when these boundaries or public APIs change.
- Apply strict typing deliberately. Scalar argument strictness depends on the calling file; adding declarations or narrower types can change accepted inputs. Do not present strict typing as sanitisation or apply it mechanically during compatibility-preserving refactors.
- Use exceptions for failures according to project contracts, preserving useful context and previous causes. Distinguish normal absence from failure. Catch at a recovery or translation boundary; do not swallow Throwable, suppress diagnostics, or return a success-shaped fallback after failure. Release resources with appropriate cleanup and transactions.
- Treat final, readonly, constructor promotion, enums, and property hooks as design choices with version and compatibility costs. Check inheritance, named arguments, reflection, serialization, and framework hydration before changing exposed structures.
- Keep untrusted data separate from executable commands and queries. Enforce authorisation at the operation boundary, encode output for its destination, and bound resource use. Read [security and boundaries](references/security-and-boundaries.md) for HTTP, persistence, filesystem, process, or external-service changes.
- Document contracts types cannot convey: failure modes, units, encoding, side effects, and meaningful ordering or lifecycle constraints. Prefer examples that exercise realistic failure handling over comments that repeat the code.

## Validate and review

Run validation locally using the project's available formatter, analyser, and test commands. CI is optional; use the existing provider when present. Do not require GitHub Actions or introduce CI unless requested. Follow existing PHPStan or Psalm configuration rather than imposing a new tool or maximum level. Preserve baseline debt without hiding new diagnostics. Follow the existing style; when none exists, use a target-compatible PHP-FIG PER Coding Style configuration. Do not reformat unrelated files.

Read [testing and tooling](references/testing-and-tooling.md) when selecting checks or changing validation configuration. Lint and run focused tests on the minimum supported PHP runtime and other relevant supported versions when available. Compatibility scanning and static analysis supplement runtime tests; they do not replace them. Verify required extensions and dependency platform requirements on the real execution environment.

Test behaviour with independent expectations and relevant boundary inputs. For bug fixes, demonstrate that the regression check fails before the fix when practical. Inspect the final diff for accidental contract changes, unsupported features, hidden warnings, and unrelated edits.

For review-only requests, report actionable findings with locations, triggers, and consequences; do not rewrite code unless asked. Distinguish demonstrated defects from preferences. For all work, report checks actually run, runtime versions, existing failures, and material verification gaps. Never claim compatibility or model effectiveness from packaging checks alone.

## Sources and inspiration

Original guidance inspired by [Morgan Linton's BeautifulRust](https://github.com/morganlinton/BeautifulRust) approach. [Compatibility](references/compatibility.md), [types and contracts](references/types-and-contracts.md), [security and boundaries](references/security-and-boundaries.md), and [testing and tooling](references/testing-and-tooling.md) link the authoritative sources behind these summaries. Load only the references relevant to the task.
