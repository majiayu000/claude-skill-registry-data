---
name: pink-review
description: Review the current repository changes for evidence-backed defects and high-value behavior-preserving refactoring or simplification opportunities. Use when the user explicitly invokes /pink-review.
disable-model-invocation: true
effort: high
metadata:
  short-description: One-command evidence-based code review
---

# Pink Review

Review the current repository changes with no setup questions and no command options. Determine the review scope automatically, inspect enough surrounding context to verify each concern, and perform two passes: first for defects and regression risks, then for behavior-preserving structural simplification.

## User Experience

- The user only needs to invoke `/pink-review`.
- Always perform both the risk pass and the refactoring/simplification pass; the user does not need to select a mode.
- Do not ask the user to choose a base branch, review mode, path, severity threshold, or output format.
- Keep the review read-only. Do not edit files, create commits, install dependencies, rewrite lockfiles, or change repository state.
- Use English for the review.
- Treat a review with no evidence-backed findings as a valid successful result.
- Never claim that a file was reviewed or a check passed unless it actually was reviewed or run.
- Do not make network calls merely to complete the review.

## Automatically Determine the Scope

1. Confirm that the current directory belongs to a Git repository and read applicable repository instructions, including files such as `AGENTS.md`, `CONTRIBUTING.md`, and documented validation guidance.
2. Identify the current branch and its configured upstream when available.
3. For committed branch changes, compare the current branch with the merge-base of its upstream. When no upstream is configured, use the repository's remote default branch when it can be determined reliably, then a clearly established local default branch.
4. Also include staged, unstaged, and untracked local changes.
5. Avoid reviewing the same effective change twice when committed and local scopes overlap.
6. If a reliable base branch cannot be identified, review all local changes that can be established safely and disclose the limitation instead of asking the user to configure a mode.
7. If there are no reviewable changes, state that clearly and stop.
8. For a very large change set, prioritize the highest-risk files and behaviors, then disclose any files or areas that received only shallow coverage.
9. Treat generated, vendored, binary, snapshot, migration, configuration, and lock files according to their effect on delivery and behavior; do not criticize their generated style.

## Build Context Before Judging

Before reporting a concern:

- Read the complete changed function, method, class, module, query, configuration section, or manifest entry.
- Inspect the callers, callees, types, schemas, tests, feature flags, migrations, and error paths needed to understand the behavior.
- Infer intended behavior from the user's request, commit messages, tests, public interfaces, and nearby implementation. Do not invent requirements.
- Search for existing guards, canonical helpers, invariants, and repository conventions that could make the concern invalid.
- Trace a concrete execution path to the suspected failure.
- Distinguish a problem introduced or materially worsened by the current changes from pre-existing code.

A diff hunk is evidence of a change, not sufficient context by itself.

## Review in Risk Order

### Correctness and Data Integrity

Check results, edge cases, state transitions, ordering assumptions, retries, idempotency, partial updates, concurrency, stale state, null and empty inputs, units, time handling, resource cleanup, and failure recovery.

### Security and Privacy

Check authorization separately from authentication. Examine trust boundaries, validation, injection, path traversal, unsafe execution or deserialization, secret handling, sensitive logging, tenant isolation, data exposure, and excessive permissions.

### Compatibility and Delivery Safety

Check public APIs, serialization, schemas, migrations, configuration defaults, feature flags, rolling deployment, rollback, cache formats, command-line behavior, and mixed-version operation.

### Error Handling, Tests, and Observability

Check swallowed errors, misleading fallback behavior, cancellation, timeouts, retry storms, missing regression coverage, assertions that miss the real failure mode, and whether production failures can be diagnosed.

### Performance and Resource Use

Check unbounded work, repeated input/output, N+1 access, blocking in asynchronous paths, avoidable sequential work, memory growth, leaked resources, and expensive operations on hot paths. Do not report unsupported micro-optimizations.

### Maintainability and Architecture

Check duplicated policy, scattered special cases, growing branching complexity, unclear ownership, weak type boundaries, unnecessary wrappers, misplaced logic, and abstractions that add concepts without simplifying behavior.

Actively look beyond local cleanup. Search for behavior-preserving “code judo” moves that make the change materially smaller or more inevitable: fewer states, branches, flags, layers, conversions, duplicated flows, or concepts a reader must hold at once. Prefer deleting complexity over moving it, and prefer existing canonical mechanisms over new parallel abstractions.

Do not use file length by itself as evidence. Recommend decomposition only when a cohesive responsibility can be separated and doing so reduces coupling, branching, or cognitive load.

### Style

Report style only when an explicit repository rule is violated, the code becomes ambiguous, or the style materially increases defect risk. Do not spend review attention on cosmetic preferences.

## Structural Simplification Pass

After the risk review, deliberately re-read every meaningful changed area from a simplification perspective.

1. Inventory the concepts introduced or expanded by the diff: flags, modes, nullable states, branches, wrappers, adapters, helper layers, conversions, duplicated sequences, ownership boundaries, and orchestration steps.
2. Ask whether the same behavior can be expressed with fewer concepts or a stronger invariant.
3. Search the repository for an existing type, helper, primitive, policy owner, state model, or extension point that makes the new mechanism unnecessary.
4. Prefer, in this order:
   - deleting states, flags, branches, fallbacks, or layers;
   - making one canonical path handle the normal and edge cases;
   - moving policy to the module that already owns the concept;
   - collapsing duplicated flows into one direct implementation;
   - strengthening a type or boundary so downstream conditionals disappear;
   - removing pass-through wrappers and speculative abstractions;
   - separating orchestration from business logic when that clearly reduces coupling;
   - making related updates atomic, or independent work concurrent, when that is both safer and simpler;
   - splitting a cohesive responsibility into a focused module when it materially improves comprehension and testing.
5. Reject a proposed refactor when it merely renames, relocates, or redistributes the same complexity; adds another abstraction without deleting concepts; requires a broad rewrite for a small payoff; or depends on product assumptions not established by the repository.
6. Describe the smallest safe transformation boundary and how behavior would be verified. Do not edit the code.

Prioritize opportunities that delete whole categories of incidental complexity. Limit the final review to at most three high-value refactoring opportunities so they do not drown out defects.

## Defect Finding Admission Gate

Report a finding only when all of the following are available:

1. The current changes introduced or materially worsened the problem.
2. The finding points to an accurate file and the smallest useful line range.
3. A concrete input, state, sequence, deployment condition, or execution path triggers it.
4. The impact is observable and meaningful.
5. The evidence is grounded in the implementation and repository contracts.
6. A practical correction or validation step can be described.
7. Nearby guards, callers, tests, and invariants have been checked in an attempt to disprove the finding.

Do not report the item as a defect when one of these elements is missing. A useful but unresolved uncertainty may appear under questions or residual risks, with the uncertainty stated explicitly.

Do not create findings for personal naming preferences, purely theoretical possibilities, unaffected pre-existing issues, generic requests for more tests, subjective architecture taste without a demonstrated cost, or multiple symptoms of the same root cause.

## Refactoring Opportunity Admission Gate

A refactoring or simplification opportunity does not need a runtime failure trigger, but it must satisfy all of the following:

1. It is tied to code introduced or materially expanded by the current changes.
2. The current complexity can be named precisely, such as duplicated policy, extra states, scattered branching, boundary leakage, or an abstraction that does not earn its cost.
3. The proposed target structure is concrete enough to understand without writing a replacement implementation.
4. It removes or consolidates meaningful complexity rather than moving it elsewhere.
5. Its payoff is explicit: fewer concepts, branches, states, duplicated paths, ownership crossings, or testing surfaces.
6. A behavior-preserving migration boundary and validation approach can be described.
7. Nearby architecture and canonical helpers have been checked so the recommendation is not speculative.

Keep these opportunities separate from defect findings. They are non-blocking by themselves and must not change the verdict unless the same structural issue also satisfies the defect admission gate with a demonstrated correctness, safety, compatibility, or material maintenance risk.

Do not force a refactoring comment. When no opportunity clears this gate, say so briefly.

## Severity and Confidence

Use severity based on impact and likelihood:

- **P0:** credible catastrophic impact, such as broad compromise, irreversible data loss, or systemic outage.
- **P1:** a high-impact or likely regression that should block merging.
- **P2:** a real localized defect, important test gap, or material operational or performance problem.
- **P3:** a non-blocking maintainability, clarity, or design improvement with a demonstrated cost.

Use high confidence when the issue follows directly from code, a test, or a deterministic path. Use medium confidence only when the evidence is strong but depends on an explicitly stated environment or caller assumption. Do not emit low-confidence speculation as a finding.

## Verification

Run the smallest safe and relevant checks allowed by the repository and environment. Prefer focused tests for the changed behavior, then targeted type checking, linting, builds, or static analysis. Do not install missing tooling or run destructive operations.

Record exactly what ran and what did not. When a check cannot run, state the reason and adjust confidence when necessary.

Before finalizing, re-read every proposed finding and actively try to invalidate it. Remove findings that depend on an incorrect path, a hidden guard, an impossible state, an unsupported requirement, or behavior unchanged by the diff.

## Output

Use this order:

### 1. Defect Findings

Put evidence-backed defects first, ordered by severity and confidence. Use one root cause per finding. For each finding include:

- severity and confidence;
- precise file and line range;
- a concise title;
- trigger;
- impact;
- evidence;
- the smallest practical fix;
- a focused verification or regression-test suggestion.

When no defect clears the admission gate, state: `No evidence-backed defects.`

### 2. Refactoring and Simplification Opportunities

Report at most three opportunities, highest expected payoff first. For each include:

- precise file and line range;
- the current source of complexity;
- the simpler target structure;
- what concepts, branches, states, duplication, or layers it removes;
- the smallest safe transformation boundary;
- how to verify behavior is preserved.

Prefer recommendations that delete complexity rather than create a more elaborate abstraction. When none clears the refactoring gate, state: `No high-value simplification opportunity identified.`

### 3. Review Summary

Include:

- verdict;
- scope reviewed, including the automatically selected base when one was found;
- checks run and their results;
- unreviewed or shallowly reviewed areas;
- questions or residual risks.

Use `request changes` when a credible P0 or P1 defect exists. Use `comment` for non-blocking defects, incomplete verification, or refactoring opportunities. Use `approve` only when no evidence-backed defect remains and scope and verification are sufficient. Refactoring opportunities alone never require `request changes`.

Do not manufacture either a defect or a refactoring suggestion to avoid an empty section.
