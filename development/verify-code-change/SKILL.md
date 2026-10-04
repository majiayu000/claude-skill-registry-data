---
name: verify-code-change
description: Verify an implemented code or config change with evidence scaled to risk and blast radius. Portable, language-agnostic. Use after an executable artifact changes, before claiming completion.
triggers:
  - verify code change
  - verify this change
  - did this change work
  - pre-merge verify
  - check before merge
  - is this ready to merge
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
  - run_command
---

<!-- Provenance: generic, portable. It names no fixed language or project toolchain. -->

# Verify Code Change

## Purpose

Collect enough evidence to determine whether the requested behavior appears satisfied within the executed scope, identify material regressions visible in that scope, and expose what remains uncertain.

This skill is the **portable, reasoning-driven** verifier. A repository may also provide a mechanical, project-bound verifier (for example `verify-change` tied to a `project-runtime.yaml` and a fixed report format). When one exists and the change is within its scope, prefer it for mechanical gates; use this skill when no project-specific contract applies, or for the reasoning, risk classification, and report it provides.

## Inputs

- requested behavior or definition of done;
- changed files or current diff, and the baseline (branch/commit/HEAD) to compare against;
- available test, lint, type-check, build, and runtime commands;
- known risks, constraints, and skipped checks;
- toolchain and dependency versions in effect (runtime, package manager, OS) when they differ from CI or production.

## Procedure

1. Confirm the exact scope (files, packages, modules) and the baseline. Without a baseline you cannot distinguish a change-caused failure from a pre-existing one.
2. Inspect the diff and identify the behavior that changed.
3. Separate evidence about **intended** behavior (requirements, definition of done) from evidence about **current** behavior (tests, logs, runtime). Treat tests and docs as evidence to reconcile, not infallible truth.
4. Map each material requirement to a verification target.
5. Classify the blast radius (see below).
6. Run the smallest check that covers an actual failure mode of the change first. Do not stop early simply because it is green; a green check that does not exercise the changed behavior proves nothing about this change.
7. Expand verification according to the blast radius. Each higher tier is required only when the change actually has that surface.
8. For meaningful bug fixes, prefer failing-before / passing-after evidence against the baseline, and confirm regression coverage when feasible.
9. When a test or build fails, reproduce against the baseline in the same environment before concluding the change is at fault: baseline-fails-too implies environmental or pre-existing; baseline-passes implies caused by the change. Continue with all remaining safe checks either way.
10. Record the toolchain and dependency versions in effect. A local pass under a different runtime than CI or production is weaker evidence; state the assumption as remaining risk when it applies.
11. Review the diff (and, at moderate or high blast radius, affected callers, callees, shared types, and contract/schema consumers - not just the changed lines) for unrelated changes, debug artifacts, missing error handling, unsafe assumptions, broadened behavior, and unnecessary complexity.
12. Treat a check that only proves the *mechanism* of the change (for example "unit tests pass") as a single point of evidence, never as proof of a broader claim (for example "so integration is fine"). Do not infer a higher-tier property from a lower-tier pass.

## Blast radius

Classify by what the change touches and who depends on it. The tier drives both test depth and review scope.

- **local** - a single function or module; no change to an exported or public contract; no persistence, concurrency, or external surface. Tests: focused unit + lint/type-check. Review scope: the diff.
- **moderate** - change to an exported symbol, shared package, API behavior, persistence, configuration consumed by others, or cross-module effect. Tests: local scope plus package or service test suite, contract-consumer checks, and integration where a consumer exists. Review scope: the diff plus callers and contract/schema consumers.
- **high** - security, privacy, authn/authz, data migrations, concurrency, infrastructure, destructive behavior, untrusted input handling, or broad compatibility impact. Tests: everything above plus broader validation, migration roll-forward/rollback where applicable, and at least one negative path per new guard. For infrastructure or config (IaC) changes, include plan/dry-run, policy as code, and a drift or diff against the deployed state instead of a unit test. Review scope: the diff plus transitive consumers; recommend independent review when available.

A check is **required** at a tier when it covers an actual failure mode created or widened by this change. If the change does not have a tier's surface, that tier's checks are not required - do not invent a gap.

## Verification ladder

Use only the levels justified by the change. The ladder is not automatically linear; choose checks that cover the actual failure modes of the change.

1. focused reproduction or unit test that exercises the changed lines;
2. diff-coverage: confirm the changed lines are actually reached by tests (via coverage tooling when available, otherwise by asserting a failing test before the change);
3. relevant lint, type-check, or static analysis;
4. package or service test suite;
5. build or integration test;
6. infrastructure/config validation (plan, policy as code, drift diff) for IaC or config changes;
7. broader validation for high-risk changes;
8. independent review when available and justified.

## Non-determinism and flakiness

A single green run is unreliable for order-, timing-, or concurrency-sensitive tests. When the change touches concurrency, retries, caching, or anything sensitive to ordering:

- re-run the relevant tests a bounded number of times or run the suite's concurrency/shuffle mode if one exists;
- treat a test that passes once and fails on retry as a failure to investigate, not as a pass;
- report non-determinism explicitly with the counts and the decisive failure, not a silent pass.

## Diff coverage

A green suite that never executes the changed lines proves nothing about this change. When the change adds or modifies executable behavior:

- prefer a coverage tool to show the changed lines are reached;
- when no coverage tool is practical, assert that a test fails against the baseline before the change and passes after it;
- a change that cannot be shown to be exercised by any test is remaining risk, not a clean pass.

This applies to executable code. For changes that are validated rather than executed - infrastructure/config (IaC), policy as code, declarative manifests - the required evidence is a plan, dry-run, policy evaluation, or drift diff, not line coverage. Do not force such changes to PARTIAL for lacking line execution; the plan/dry-run that passed IS the evidence for that surface.

## Test quality

Tests that exercise the changed lines still prove little if they assert nothing meaningful. For the tests that carry this change's verification weight, check:

- each asserts observable behavior (got/want on outputs, state, or errors), not merely that no error occurred or that a mock was called;
- the unit under test is real where the risk is real - a test that mocks the very behavior being verified proves only the mock;
- for guard, reject, or boundary logic, at least one test fails if the guard is removed or inverted. When this is cheap to check directly (temporarily weaken the condition, observe the named test fail, revert), that spot check is stronger than inspection and worth reporting;
- new tests would have failed before the change (the RED half of failing-before / passing-after).

A suite that reaches the changed lines but would pass with the change's logic inverted is remaining risk, not coverage.

## Negative paths

For new behavior that accepts input, branches on a condition, or enforces a rule, confirm at least one error, boundary, or negative case is exercised. This matches the "missing error handling" concern in diff review but makes it concrete: the test must demonstrate the guard fires. A guard with no failing test is remaining risk.

### Interrupted paths

The happy path and the rejected path are not the only paths. Work that stops part-way
escapes most suites, because the tests drive the operation to completion. When the
change touches long-running work, durable state, cancellation, retry, or resume,
confirm the interrupted paths are exercised as well:

- **Cancellation mid-operation.** Cancel at each phase the operation has, not only at
  the start. Confirm the partial result survives, that it is marked partial, and that
  the error reaches the caller instead of being replaced by a clean status.
- **Failure of one attempt inside a retry.** Confirm the attempt's error is recorded
  before the next attempt starts, and that the retry does not erase it.
- **Restart between two durable writes.** Confirm the recovery path handles the state
  at each gap, and that a repeated recovery run produces the same result as one run.
- **Loss of a resource the stopped work depends on.** Confirm the resume refuses
  instead of continuing without it.

A change to durable or long-running behavior whose interrupted paths have no test is
remaining risk, whatever the coverage number says.

### Bound and sentinel values

When the change adds or moves a numeric bound, confirm a test pins what the bound's
sentinel value means, at the layer the caller reaches. Confirm the resolved value is
the value the runtime reads: a bound that a later layer replaces with a default is a
bound the caller cannot set, and no test of the resolver will show it.

## Result semantics

- `PASS` - the checks required at the change's blast radius were executed and passed, the change was shown to be exercised (for executable code) or validated (for IaC/config), and no material issue was found within that scope.
- `PARTIAL` - a check required at the change's blast radius is unavailable, incomplete, or blocked; or the diff review surfaced a material concern the executed checks did not resolve; or the changed executable lines could not be shown to be exercised by any test; or a check failed but causal attribution was impossible because no baseline was available.
- `FAIL` - a required check executed and failed, the implementation does not satisfy the requirement, or a material regression was found.

Choosing between PARTIAL and FAIL when the diff review finds a defect: if the defect is confirmed (a concrete failure path exists, or a required check fails against the change), the result is `FAIL`. If the concern is real but unconfirmed (a suspected issue the executed checks neither proved nor disproved), the result is `PARTIAL` with the concern and the confirmation needed stated as remaining risk.

- `NOT_RUN` - verification could not begin (no scope, no environment, plan only).

Two symmetric guards on `PASS`:

- Do **not** downgrade a verified change to `PARTIAL` by citing higher-tier checks that were not required for its scope.
- Do **not** upgrade to `PASS` by skipping a required check and relabeling it "not required." If a check was required and could not run, the result is `PARTIAL`.

`PASS` does not prove that no defect exists; it describes the executed scope only. When the diff review finds a material defect in the change itself (for example a silently swallowed error or an untested broadened behavior), the result is `PARTIAL` or `FAIL`, not a clean `PASS`.

## Failure handling

- If a check fails, report the command or method, the decisive failure, and the practical consequence.
- Distinguish change-caused from environmental failures using the baseline reproduction in step 9.
- If the failure is caused by the change, return the task to implementation.
- If the failure is unrelated or environmental, provide the evidence and continue with all remaining safe checks.
- If required verification cannot run, do not declare the task complete.
- For high-risk work, identify the exact approval or validation still required before release.

## Report shape

When a resource catalogue and its scoped reader are available, load
`report-template` before producing the verification report. Without that
capability, use the inline report shape below.

### Verification result

`PASS`, `PARTIAL`, `FAIL`, or `NOT_RUN`.

### Scope

- behavior and files covered;
- blast-radius classification and what drove it;
- baseline and toolchain/dependency versions in effect.

### Checks executed

- exact command or method (with exit status);
- summarized result, not full successful output;
- requirement or risk covered;
- list a check as not run only if it was required at the change's blast radius and could not be executed; do not record higher-tier checks that were not required for the change as not run, since that invents a gap and muddies the result.

### Diff coverage

- how the changed lines were shown to be exercised (coverage tool and result, or failing-before/passing-after), or remaining risk if they were not.

### Diff review

- material findings, or `No material issues found within the reviewed diff`.

### Negative paths

- the error/boundary case(s) exercised for new behavior, or remaining risk if none could be shown.

### Test quality

- what the load-bearing tests assert and whether they would fail if the changed logic were inverted, or the specific weakness (assertion-free, mock-of-unit, guard untested) as remaining risk.

### Remaining risk

- skipped checks, unresolved uncertainty, non-determinism, toolchain mismatch, or `None identified within the executed scope`.

Keep the report concise. Do not paste complete successful logs.
