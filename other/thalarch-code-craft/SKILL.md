---
name: thalarch-code-craft
description: >
  Universal coding-quality overlay for implementation and review across languages. Use on
  meaningful code changes to keep the solution idiomatic, minimal, repository-native, incrementally
  verifiable, and evidence-backed while preventing common agent mistakes such as invented APIs,
  speculative abstractions, broad exception swallowing, dependency bloat, and fake-success behavior.
---

# Thalarch Code Craft

This is the universal coding layer. Language skills add syntax, tooling, and runtime-specific
judgment on top of it.

## Priority order

**Correctness → clarity → required robustness → maintainability → concision → micro-optimization.**

Never compress code at the expense of correctness, security, or human readability.

## Repository-native first

Before writing meaningful code:

- read the exact file to change;
- inspect at least one nearby implementation of the same kind when available;
- read applicable repository rules;
- identify the actual compiler/runtime/framework/dependency versions;
- discover the project's real formatter, linter, type checker, test runner, and build commands;
- reuse existing error types, logging, dependency injection, serialization, HTTP, database,
  and test patterns unless the requested change intentionally replaces them.

Project conventions beat generic style preferences unless they violate the task or a real
correctness/security contract.

## Minimal correct shape

Before editing, identify the smallest code surface that satisfies the acceptance contract.

Avoid:

- speculative configuration;
- single-use abstraction layers without a real domain benefit;
- duplicate wrappers around existing helpers;
- unrelated cleanup;
- extra files or dependencies that are not needed;
- compatibility shims for versions the repository does not support.

A changed line should be explainable by the requested behavior, required regression protection, or
a direct consequence of the change.

## Incremental evidence slices

For multi-file or uncertain work, do not maximize code written before feedback. Split the work into
the smallest slices that can produce new evidence.

Choose the slicing strategy that best reduces risk:

- **vertical** — one complete user/system path through the required layers;
- **contract-first** — stabilize a shared API/schema/interface before independent producers/consumers;
- **risk-first** — prove the most uncertain integration, lifecycle, protocol, migration, or performance
  assumption before building dependent work;
- **behavior-first** — create the regression/invariant proof before changing implementation.

After a slice that changes behavior:

1. run the smallest repository-native check that can falsify the slice;
2. inspect the result rather than treating command execution as proof;
3. keep the repository in a coherent state before expanding the next slice;
4. if evidence disproves the approach, revise before more files depend on it.

Do not create commits automatically unless the user authorized commits. A clean evidence checkpoint
is valuable even when Git mutation is outside scope.

Re-running the same successful check with no relevant mutation in between adds little evidence. Run
it again after a change that can invalidate it, and require fresh final verification after the last
relevant mutation.

## Verify APIs instead of remembering them

Never write an external-library call merely because it looks plausible.

When an API matters:

1. inspect the version actually installed or declared;
2. inspect existing call sites, generated types, source, local docs, or current primary docs;
3. confirm signature, nullability/error behavior, ownership/lifecycle, and version support;
4. only then implement.

For load-bearing version-sensitive framework decisions, route through `thalarch-source-grounding`
when available.

If the API cannot be confirmed, mark that point `UNVERIFIED` rather than silently inventing it.

## Boundary discipline

Validate at trust boundaries:

- network/request input;
- deserialized data;
- file/process boundaries;
- database/external-service responses where contracts are not trusted;
- user-controlled paths, identifiers, URLs, or commands.

Inside a proven typed/internal contract, do not scatter defensive checks for states the contract
excludes. Defensive noise can hide the real invariant.

## Error discipline

- Catch only errors the current layer can handle, translate, enrich, or recover from.
- Preserve cancellation/interruption semantics for the runtime in use.
- Do not catch broad exceptions just to log and return an empty/success value.
- Do not replace a real operation with canned success data.
- Do not weaken, skip, delete, or rewrite a test merely to make a change appear green.

## Names, comments, and structure

- Names should carry domain intent rather than generic `data`, `result`, `helper`, or `manager`
  unless the surrounding API genuinely makes the meaning obvious.
- Comments explain non-obvious reasons, constraints, protocols, or hazards — not syntax.
- Extract a helper when it creates a meaningful concept, isolates a testable rule, removes real
  duplicated knowledge, or reduces difficult control flow. Do not extract merely to hit an arbitrary
  line-count target.
- Prefer standard-library/framework primitives when they make the code clearer and are compatible
  with the repository version.

## Dependencies

Before adding one:

1. check standard library/runtime support;
2. check dependencies already present;
3. determine whether local code would reimplement dangerous or substantial complexity;
4. inspect maintenance/security/version implications;
5. add the dependency only when it owns meaningful complexity.

Do not add a dependency to save a handful of obvious lines.

## Shortcut defenses

Reject common agent rationalizations:

- "I'll test at the end" — wrong assumptions compound across slices.
- "While I'm here, I'll clean this up" — unrelated cleanup increases review and regression surface.
- "This abstraction will help later" — future requirements are not current evidence.
- "This API is standard" — standard-looking is not version proof.
- "The build passed once" — an earlier result does not prove code changed afterward.
- "More defensive code is safer" — redundant checks inside a proven contract can obscure the real
  boundary and failure mode.

## Completion guard

Before handing work to review:

- inspect the diff for unrelated changes;
- remove imports/symbols made dead by this change;
- confirm new external APIs actually exist in the project version;
- run the language/project-native targeted checks after the final relevant mutation;
- state what was proved and what remains unverified.

The implementer does not self-certify final completion.

## Design heritage

This skill synthesizes public patterns from surgical coding guidance, idiomatic language overlays,
incremental/risk-first implementation, clean-code guardrails, and independent review practice. It
intentionally avoids universal numeric rules that are not valid across every codebase.