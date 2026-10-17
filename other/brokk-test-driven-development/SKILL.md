---
name: brokk-test-driven-development
description: Implement a bounded work package by the red-green-refactor cycle — failing tests traced to acceptance criteria first, minimal implementation second, behavior-preserving refactor third — returning run evidence for each phase, stopping at a reviewed-ready, uncommitted tree; committing belongs to a separate step.
---

# Test-Driven Development

## Purpose

Execute one bounded work package test-first: every behavior is proven absent by a failing test before it is implemented, made present by the smallest sufficient change, then cleaned up without changing behavior. This skill owns **phase ordering**, **evidence capture**, **work-package and write-set discipline**, the **rules for running as one of several concurrent sessions in a shared working tree**, and the craft standards the cycle relies on. **It never commits**: the tree it leaves is reviewed uncommitted, and a separate commit step records it.

**Self-contained by design.** This skill is the complete method for the test-driven step and depends on no other skill. The test-craft, implementation, and refactoring standards the cycle needs are in § Craft Standards below. The package brief supplies the contracts and acceptance criteria — nothing else is imported. A gap in these standards is a report item, not a reason to reach elsewhere or improvise.

## When to Use

- Dispatched as the test-driven execution step of the TDD workflow, with one work package to implement.
- Implementing one package of a multi-package plan, alone or concurrently with sibling sessions.
- Implementing a single slice end-to-end when the plan produced exactly one package.
- The brief carries a `Phase:` and/or `Mode:` line (see Workflow) — those lines select the subsections below.
- Fixing a bug with a known or reproducible failure, where the reproduction must be captured as a test first.
- Building a shared scaffold (contracts, stubs, fixtures) that concurrent sessions will build against.
- **Not applicable to:** exploratory investigation with no behavior to verify, pure documentation changes, and packages whose acceptance criteria cannot be expressed as an observable outcome — report that rather than inventing a test.

## Workflow

**Step 0: Read the brief's control lines.**

- `Phase: full | red | green+refactor` — `full` runs Red → Green → Refactor in one session (default when absent); `red` writes failing tests only and stops; `green+refactor` starts from tests another session already wrote and a review already accepted.
- `Mode: solo | parallel` — `solo` means this is the only session touching the tree (default when absent); `parallel` means sibling sessions are working concurrently in the same tree on other packages (see *Parallel-context discipline*).

**Step 1: Consume the work package.**

1. **Extract the package contract.** Resolve each of: **scope / write set** (the files this session may create or change), **contracts and interfaces** to provide and consume (signatures, types, error and status contracts, schema changes), **owned acceptance criteria** with their IDs, **test seam and test command**, **dependencies** on other packages, and the **done criterion** — and, when the brief lists them, the **reviewed-but-uncommitted paths** of earlier packages in the same batch, which are read-only for this session exactly as in parallel mode.
2. **Know where each input comes from.** Interface and contract detail comes from the design document's blackbox interface specifications when a design step ran; acceptance criteria and quality scenarios come from the requirements document when an analysis step ran; when both steps were skipped, derive them from the request itself and **restate the derived list explicitly in the report** so the requesting agent can correct it.
3. **Report gaps instead of filling them.** A missing contract detail, an untestable acceptance criterion, or a contradiction between the request and the specified interface is a report item — and, if it blocks the first failing test, a consultation. Do not invent requirements to close the gap.
4. **Record the session header** before editing anything:

   ```text
   TDD session: package=<name>, phase=<full|red|green+refactor>, mode=<solo|parallel>, ACs=<IDs>, write set=<paths>, test command=<command>
   ```

5. **Capture the baseline.** Run the tests you are responsible for — the full suite in `solo` mode, your own subset in `parallel` mode — before changing any file, and keep the output verbatim. Failures already present in the baseline are pre-existing: report them unchanged; do not repair them unless the package owns them.

**Step 2: Slice the package into units of work.**

- One unit = one acceptance criterion, or one distinct behavior within an acceptance criterion that needs its own test. Order units so the earliest ones establish the contract surface and the later ones add branches, error paths, and edge cases.
- Enumerate the edge cases per unit from the **edge-case catalog** in § Craft Standards.
- **Test-level selection for the cycle** (levels defined in § Craft Standards; what follows is the TDD choice rule): for each unit, write the test at the **innermost level that can still observe the acceptance criterion** — fast, specific failures make red evidence legible and keep green minimal. Add exactly one test at the package's declared test seam per acceptance criterion so the criterion is provably covered end-to-end at that seam, and keep the remaining branch and edge-case coverage at unit level. Do not raise the level to compensate for a missing seam; report the missing seam.
- Units are small: if a single red step requires more than one behavior to go green, split it.

### Phase: Red — write the failing test

Run when `Phase` is `full` or `red`. Skip entirely when `Phase` is `green+refactor`.

1. **Name the behavior** in the test name: scenario plus expected outcome, referencing the acceptance criterion ID in the name or an adjacent comment so traceability survives refactoring.
2. **Write the smallest test that fails** for the current unit. Introduce only the interface elements needed for the test to compile and execute — taken from the specified contract, never improvised beyond it. Stubs may exist, but must not satisfy the assertion.
3. **Run it and capture the output verbatim.** This is the red evidence; a paraphrase is not evidence.
4. **Confirm it fails for the intended reason.** The failure must be the assertion you wrote, not a syntax error, missing import, misconfigured harness, or unresolved dependency. An infrastructure failure means the red is not yet established — fix the harness, re-run, re-capture.
5. **Handle an immediately-green test explicitly.** Never accept it silently. Either the behavior already exists (stop, report it, and ask whether the acceptance criterion is already satisfied) or the assertion is too weak (strengthen it until it fails). Record which of the two it was.
6. **Stop here when `Phase: red`.** Deliver the test files plus the red evidence and hand over; write no implementation, and state which units are covered and which remain.

### Phase: Green — minimal implementation

Run when `Phase` is `full` or `green+refactor`.

1. **When starting from another session's tests** (`green+refactor`): re-run them yourself first and capture the red output as this session's phase baseline. The handed-over tests are **read-only** — a test you believe is wrong is a report item or a consultation, never a silent edit, and never a weakened assertion.
2. **Write the simplest code that turns the current red green.** Honor the specified contract exactly; stay strictly inside the write set; apply the **green-phase implementation standards** in § Craft Standards.
3. **Run the tests and capture the green output verbatim.** The target test passes and no previously passing test in your responsibility regresses.
4. **Add nothing the current test does not demand.** Anticipated behavior, extra configuration knobs, and speculative abstractions belong to a later red — or to no one.
5. **Loop** back to Red for the next unit until every owned acceptance criterion has at least one passing test that was observed failing first.

### Phase: Refactor — behavior-preserving cleanup

Run when `Phase` is `full` or `green+refactor`, and only from a fully green state.

1. **Never refactor on red.** Return to green first, by fixing or reverting.
2. **Scope the cleanup to the code this package touched** — naming, duplication, over-long functions, tangled conditionals, test readability. Apply the **refactoring moves** in § Craft Standards; adjacent code outside the write set is out of scope.
3. **Re-run after each discrete change** and keep the final output. A refactor step that goes red is reverted rather than debugged forward, unless the cause is a genuine defect the tests just exposed — which becomes a new red/green cycle, reported as such.
4. **Change no behavior and add no public surface.** An edge case discovered while refactoring is not patched in place: write it as a new failing test first.

### Evidence block

Return this to the requesting agent at the end of every session; it is what the review session verifies against.

```text
TDD session: package=<name>, phase=<…>, mode=<…>
Baseline:    <command> → <verbatim result tail>
Red:         <command> → <verbatim failing assertion(s)>, one line per unit/AC
Green:       <command> → <verbatim pass summary>
Final:       <command> → <verbatim pass summary>   (full-suite line too, in solo mode)
AC coverage: table of | AC ID | test name | file:line | status |
Files changed: <paths>   Write-set deviation: <none | path + reason>
Would-fail check: <how it was confirmed the tests fail without the implementation>
Commits: none
Gaps / concerns reported: <contract gaps, untestable ACs, pre-existing failures>
```

Capture run output verbatim (trimmed to the informative tail), never summarized into prose. `Commits:` is always `none`: this session never commits, in any mode, and a reviewer treats any other value as blocking.

### Parallel-context discipline (`Mode: parallel`)

Concurrent sessions share one working tree, so isolation is a discipline, not a guarantee. The no-commit rule is not parallel-specific — see § No Commits — so it is not repeated here.

1. **Scaffold before fan-out.** Shared surfaces — interface and contract declarations, dependency-injection and registration tables, route tables, migrations, dependency manifests and lockfiles, generated code, and shared test fixtures or harness setup — belong to a **sequential scaffold session that completes and is reviewed before any concurrent package starts**, and are frozen for the duration of the wave. If this session *is* the scaffold: create only the shared surface (declarations, fixtures, and stubs that fail loudly), implement no package internals, and report the frozen contract surface explicitly so the concurrent sessions can build against it.
2. **No cross-package edits.** Files outside your write set — including the scaffold — are read-only. A required change there is a report item or a consultation; never an edit, and never a local workaround that duplicates the shared surface.
3. **Run only your own test subset.** Sibling packages are mid-flight, so their failures are expected and are not yours. Do not investigate them, do not "fix" them, and never skip-mark, disable, or delete a failing test to get a clean run.
4. **No tree-wide side effects.** No dependency installation or upgrade, no repository-wide formatter or codegen run, no lockfile regeneration, no schema/migration application — those are scaffold or integration duties.
5. **Report the seam.** State the write set actually touched, any contract detail you needed that the scaffold did not provide, and anything the integration session must reconcile.

**Solo mode** relaxes only these: baseline and final runs use the full suite, and shared surfaces may be created in-session as ordinary units of work.

### No Commits

This session never records a commit, in any phase and in any mode, whether or not the brief mentions one. You stop at a refactored green state and hand the uncommitted tree to review; the TDD workflow's commit step (`brokk-tdd-commit`) records it afterwards, by the plan, once the review has passed. A brief that asks this session to commit is a defect in the brief: report it and leave the work uncommitted.

### Craft Standards

The standards the cycle runs on. Apply them; do not re-derive them, and do not expand them into a general playbook.

**Edge-case catalog.** Before writing a unit's tests, walk this list and name which entries apply to the unit and which do not: empty or absent input; null/undefined; boundary values (minimum, maximum, off-by-one on each side); oversized input; invalid type or format; duplicate submission and idempotency; ordering and sort stability; concurrency or re-entrancy where the unit can be entered twice; error and timeout paths of every contract the unit consumes; permission or authorization denial; and the negative of the happy path. An entry you exclude is excluded on the record, not by omission.

**Test levels.** *Unit* — one building block in isolation, consumed contracts replaced by fakes; the default. *Integration* — real collaborators across one seam (database, HTTP, filesystem, message bus); use it when the behavior *is* the seam. *End-to-end* — the whole path through the package's declared test seam; use it once per acceptance criterion for provable coverage, never as a substitute for a unit test you could write instead.

**Test structure.** One behavior per test. Independent: no shared mutable state, no dependence on execution order, no reliance on another test's side effects. Deterministic: inject time, seed or stub randomness, never touch the live network. Named descriptively: scenario plus expected outcome plus the acceptance-criterion ID. Assert specifically enough that a plausible regression fails the test. Prefer fakes over mocks of internals, and assert on observable behavior, never on implementation structure.

**Bug fixes and uncovered code.** A bug fix starts with a test that reproduces the failure and fails for that reason; only then write the fix. Before refactoring code that has no coverage, write **characterization tests** that pin the current behavior as it actually is — run them as ordinary red steps, expect them to be immediately green, and classify them as such in the evidence block so they are not mistaken for proven-absent behavior.

**Green-phase implementation standards.** Honor the specified contract exactly — signatures, types, and error and status contracts are part of the interface. Keep the behavior under test separate from transport and framework glue so it stays unit-testable. Make errors explicit and informative; never swallow one. Add no unrequested behavior and no speculative generality — no configuration knob, abstraction, field, or extension point that no current test demands. Hold the security basics inside the write set: parameterized queries, input validated at trust boundaries, no hardcoded secrets, no debug endpoints. If the package owns a migration, make it reversible and exercise it with a test.

**Comments.** Code is self-explanatory by default — carry the meaning in names, decomposition, and explicit control flow rather than in prose beside it. There is no general need to comment: add none merely to restate what the code already says, and delete such comments from the code this package touches. Write a comment only where it is truly necessary or genuinely helpful — a *why* the code cannot express, a caveat or constraint invisible from the syntax, or the acceptance-criterion ID a test carries in an adjacent comment for traceability.

**Refactoring moves (from green only).** Rename for intent. Extract a function or method to remove duplication or shorten an over-long one. Inline needless indirection. Simplify conditionals with guard clauses and early returns. Replace magic values with named constants. One move at a time; run the tests after each; revert any move that goes red rather than debugging forward. Stay inside the package's write set.

## Quality Criteria

- **Red before green, with proof.** Every owned acceptance criterion has at least one test whose failure was observed and captured before the implementation existed.
- **Red evidence is genuine.** Each captured failure is the intended assertion, not a harness, import, or configuration error, and is quoted verbatim.
- **Green is minimal.** No behavior, abstraction, or configuration exists that no test demanded.
- **Refactor is behavior-preserving** and was performed only from green; the final run is green.
- **Traceability is explicit.** The AC → test table maps every owned criterion to a named test at a file location.
- **Reversion sensitivity is confirmed.** The report states how it was established that the tests fail without the implementation.
- **Boundaries held.** Files changed are a subset of the declared write set; any deviation is named with a reason.
- **Contracts honored exactly** as specified; every divergence is reported rather than silently adopted.
- **Baseline honesty.** The pre-change run is captured, and pre-existing failures are reported unchanged.
- **Tree left uncommitted.** `HEAD` is unchanged from the session's start, and the evidence block reads `Commits: none`.
- **Parallel invariants held** when in `parallel` mode: no cross-package edits, own subset only, no tree-wide side effects.
- **Handover integrity** in `green+refactor`: the reviewed tests are unmodified.
- **Test craft standards** — independence, determinism, one behavior per test, assertions specific enough to catch a regression — hold as defined in § Craft Standards.
- **Evidence block complete** and in the given schema.

## Anti-Patterns

- **Implementation-first with back-filled tests** — writing code then tests that describe it; the tests can no longer fail for the right reason.
- **Fitting tests to the implementation** — asserting on internals, mirroring the code's structure, or relaxing an assertion until it passes.
- **Silently accepting an immediately-green test** — the strongest signal that the test is weak or the work is already done, discarded.
- **Giant red** — one failing test that demands a whole package, or many behaviors, to go green.
- **Skip-marking, disabling, or deleting failing tests** to reach a clean run.
- **Editing the reviewed tests in a `green+refactor` session** instead of reporting the problem.
- **Refactoring on red** — cleaning up while the suite is failing, so the cause of the next failure is ambiguous.
- **Write-set creep** — improving adjacent code, renaming across the tree, or touching shared surfaces outside the package.
- **Chasing sibling failures in parallel mode** — debugging another package's mid-flight state, or committing to "stabilize" the tree.
- **Fan-out before the scaffold is fixed** — starting concurrent packages while shared contracts, fixtures, or registrations are still in motion.
- **Fabricated or paraphrased evidence** — reporting "tests pass" without the captured run output.
- **Inventing requirements** to close a contract or acceptance-criterion gap instead of reporting it.
- **Test-level inflation** — reaching for an end-to-end test where a unit test proves the behavior, making red slow and failures vague.
- **Committing.** Any commit from this session — "to checkpoint progress", "because the brief allowed it", "because the tree is green" — bypasses the review that gates history; the commit step exists for exactly that.
- **Reaching outside this skill for method** — expecting another skill to supply test craft or implementation standards; this skill is complete for the test-driven step, and a gap in it is a report item, not a reason to improvise.
- **Restating a comprehensive general testing playbook** — re-deriving edge-case catalogs, level definitions, or refactoring technique at length instead of applying the Craft Standards this skill defines.
