---
name: component-check-spec-translation
description: Cross-check a Certus component's nested Spec Kit `specs/**/spec.md` specifications against its generated implementation and tests, then summarize semantic translation mismatches with source evidence. Use when auditing whether generated code faithfully implements component requirements, acceptance scenarios, interfaces, defaults, constraints, errors, or success criteria; when checking implementation drift after generation or code changes; or when asked to compare a component spec with code. This is a read-only audit and does not reconcile or edit either side.
---

# Check Component Spec Translation

Compare specification intent with observable implementation semantics. Look for meaning that was lost, weakened, contradicted, or added during translation into code; do not rely on textual similarity alone.

## Resolve the Scope

1. Resolve the requested component name or path to one component directory. Prefer `components/<name>/`; accept an explicit component path elsewhere in the repository.
2. If no component is named, infer it only when the working directory is inside one component or the request identifies exactly one. Otherwise ask for the component.
3. Discover specifications with `rg --files <component>/specs` and select files whose path ends in `/spec.md`. Support both `specs/<feature>/spec.md` and deeper nesting.
4. Audit all discovered specs unless the user selects a feature/spec. Do not assume the highest numbered spec supersedes the others: specs can be additive. Record each spec's title, status, date, and any backfill or supersession notice.
5. Treat the component's checked-in source as the generated implementation. Include `Cargo.toml`, `src/`, `tests/`, `benches/`, `examples/`, and `build.rs` when present. Follow explicit spec references into shared interfaces, macros, app wiring, or another checked-in path when needed to determine behavior.
6. Exclude build output, dependencies, vendored code, logs, transcripts, and prior drift reports as implementation evidence. Prior reports may help locate code but never establish current alignment.

If no nested `spec.md` exists, stop and report the searched path. If the component path is ambiguous, do not combine candidates.

## Build the Specification Inventory

Read each selected `spec.md` completely. Extract every independently testable or observable claim from:

- functional and non-functional requirements, including IDs;
- acceptance scenarios, user stories, and edge cases;
- success criteria that constrain implementation;
- interfaces, entities, defaults, constants, limits, errors, and output formats;
- feature gates, lifecycle, concurrency, persistence, safety, and performance guarantees;
- explicit exclusions and prohibited behavior.

Split compound requirements when their clauses can align differently. Preserve the original identifier and add a clause suffix such as `FR-012.a`. Treat status labels such as `Implemented`, task completion, and named tests as claims to verify, not proof.

When specs overlap, compare each to code independently. Report an inter-spec conflict when two active specs prescribe incompatible behavior and no explicit supersession resolves it.

## Trace Claims into Code

For every inventory item:

1. Search first by requirement ID, domain terms, API names, constants, flags, errors, and test names.
2. Trace from public entry point to the behavior that satisfies the claim. Inspect configuration defaults, validation, branches, feature gates, error paths, state transitions, serialization, and shutdown behavior as relevant.
3. Follow shared interface definitions and repository macros when they determine the contract. Cite the checked-in macro invocation and definition rather than imagined expanded code.
4. Inspect tests for behavioral evidence and for assertions that encode semantics different from the spec. A test name, stub, mock, TODO, ignored test, or compile-only reference is not proof by itself.
5. Check all applicable build configurations named by the spec. Do not generalize behavior from one feature gate to another without evidence.
6. Use exact `path:line` references for both the specification claim and implementation evidence. Never mark a claim aligned solely because names resemble each other.

Run a focused existing test only when static inspection cannot settle a material claim and the test is practical in the current environment. Do not modify files, generate new tests, require unavailable hardware, or broaden into a full test suite. State which tests were run and separate runtime evidence from static evidence.

## Classify Translation Results

Assign exactly one primary result to each claim:

- **Aligned**: code and applicable tests substantively implement the full claim.
- **Partial**: some clauses or configurations are implemented, but required behavior is incomplete.
- **Contradiction**: implemented behavior, value, API, or test assertion directly conflicts with the spec.
- **Missing**: no implementation evidence exists after tracing the relevant paths.
- **Extra behavior**: code exposes material behavior or constraints absent from, or explicitly excluded by, the specs. Use this only for user-visible, contract, data, safety, or operational semantics—not routine implementation detail.
- **Unverifiable**: the claim needs hardware, runtime measurement, external state, or evidence unavailable to this audit. Do not count this as a mismatch.

Also flag stale spec annotations when a status such as `Implemented` disagrees with the evidence. Do not turn harmless naming, formatting, refactoring, or implementation-choice differences into translation mismatches.

Use these severities for non-aligned findings:

- **Critical**: data loss/corruption, safety/security violation, or unusable required contract.
- **High**: missing or contradictory core/user-visible behavior.
- **Medium**: incomplete edge case, default, validation, error, feature-gate, or test semantics with meaningful impact.
- **Low**: traceability or stale status issue with little runtime impact.

State confidence as high, medium, or low. Prefer `Unverifiable` or lower confidence over speculation.

## Summarize the Audit

Return the report in this shape:

```markdown
# Component Spec Translation Audit

Component: <path>
Specs: <paths or selected spec>
Evidence: static inspection; <tests run, or "no tests run">

## Summary

| Result | Count |
|---|---:|
| Aligned | N |
| Partial | N |
| Contradiction | N |
| Missing | N |
| Extra behavior | N |
| Unverifiable | N |

Verdict: <one-sentence assessment of translation fidelity and highest risk>

## Translation Mismatches

| ID | Severity | Result | Spec evidence | Code evidence | Mismatch and impact |
|---|---|---|---|---|---|
| FR-003 | High | Contradiction | `specs/.../spec.md:88` | `src/lib.rs:142` | Spec requires X; code does Y, causing Z. |

## Unverifiable Claims

- <claim and why it could not be established>

## Coverage by Spec

| Spec | Claims | Aligned | Mismatched | Unverifiable |
|---|---:|---:|---:|---:|

## Recommended Next Actions

1. <highest-value code or spec decision; identify which side likely needs review without editing it>
```

List findings by severity, then spec order. Include `Partial`, `Contradiction`, `Missing`, and `Extra behavior` in the mismatched total. Omit empty detail sections. Keep aligned claims summarized in counts unless the user requests the full traceability matrix. End with the total number of claims checked and mismatches found.

Remain read-only. Do not update the spec, implementation, tests, task files, or `.specify/sync` reports unless the user separately asks for remediation.
