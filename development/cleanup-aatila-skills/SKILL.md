---
name: cleanup
description: Contract-first cleanup of a PR, branch, files, or feature — removes unnecessary complexity while preserving behaviour and regression coverage. Review-only by default; pass `implement` to apply.
disable-model-invocation: true
---

# Behaviour-preserving cleanup

**Acceptance standard:** a smaller, clearer implementation whose tests still reject realistic regressions while letting equally correct implementations pass. Measure the gain by what disappears (concepts, branches, responsibilities, maintenance obligations), aiming for one clear current-state implementation.

A **contract** is anything callers or users rely on: domain results, emitted events, persisted records, boundary interactions, and lifecycle guarantees, including temporal ones (intermediate publications, ordering, cancellation, supersession, exactly-once completion, persistence, shutdown). Everything else is implementation, free to change.

**Invocation:** `/cleanup <scope> [implement]`, where scope is a PR, branch diff, files, or feature. When no scope is given, ask for one.

**Modes.** Review-only (default): steps 1–3, then list the checks step 5 would need; edit nothing. Implement: all steps. In both modes, preserve unrelated working-tree changes, and commit, push, or post external comments only when explicitly asked.

## Steps

### 1. Map contracts and baseline

Read the scope in full: complete surrounding functions, callers, tests, and repo guidance or plan/spec. Sort what you find into contract, implementation, and incidental (obsolete scaffolding; unrelated pre-existing defects, which you note and leave). Run the relevant checks before any edit and record the results as the baseline.

**Done when** every affected flow has a written contract line and the baseline is recorded (or noted as unavailable).

### 2. Collect candidates

Check the scope against every category in [Smells](#smells). Treat each removal as a Chesterton's fence: confirm usages across callers and build configurations, and for a repeated-looking check, confirm its invariant cannot change between checks (suspension points, lifecycle transitions).

**Done when** every Smells category has been checked against the scope. "Already minimal" is a valid result once that holds.

### 3. Decide each candidate

Write a **candidate record**:

- **Disappears**: the concept, branch, responsibility, dependency, state, or obligation eliminated (relocated code eliminates nothing)
- **Why**: unnecessary, redundant, or overcoupled, and the evidence
- **Contract**: what must stay true
- **Check**: the test or observation that will show it holds afterwards
- **Verdict**: `change` (well-supported, in scope) · `uncertain` (name the missing evidence) · `scope decision` (needs an approved requirement or boundary changed; raise it separately)

When a candidate touches tests, apply [Test audit](#test-audit).

**Done when** every candidate has a record and a verdict.

### 4. Apply (implement mode)

Make the `change` verdicts only. Prefer deletion or an existing mechanism; keep a few straightforward cases inline rather than building a configurable framework.

### 5. Validate

Rerun the baseline checks and separate pre-existing failures from new ones. Cover affected callers and build configurations, especially conditional compilation, internal API requirements, and shared test helpers. When you change regression-test instrumentation, run a **mutation check**: inject the original failure (or an equivalent controlled fault), confirm the test goes red on a behavioural assertion rather than a timeout or fixture error, then remove the fault. A green suite is necessary evidence, not proof.

**Done when** every record's Check has run, or is reported as not run with the reason.

## Reference

### Smells

- Unused state, fields, counters, parameters, hooks, wrappers, abstractions.
- Duplicate execution paths, especially DEBUG/test paths that diverge from release behaviour.
- Optional inputs or defaults that silently substitute behaviour when a caller omits required information.
- Checks a stronger type, constructor, parser, or state transition would make redundant.
- Speculative compatibility paths and fallbacks without a demonstrated requirement.
- Test orchestration, diagnostics, setup, or helper layers grown beyond what the scenario needs to observe.

Validation at trust, security, authorization, and persistence boundaries is load-bearing: keep it.

### Test audit

For every test or assertion you change, answer:

1. What realistic regression does it catch?
2. Is its **oracle** independent, drawn from requirements, explicit examples, invariants, or externally meaningful outcomes rather than the production logic or a copy of its algorithm?
3. Would an equally correct implementation pass it? If not, it is structure-sensitive: it reads source text, private representation, helper names, internal call sequences, or incidental call counts.
4. Is its coverage unique?

Interaction assertions count as behavioural when the interaction is the contract (exactly-once completion; no persistence write after authorization fails). Architecture checks belong where structure is the policy; keep them apart from correctness tests. A short input/output test can have an independent oracle: judge independence, not length.

Replace weak tests that guard a real contract with behavioural ones. Delete tests with no unique value, and name the coverage that remains. Keep temporal tests temporal: a transient wrong selection, stale publication, or late write is a regression even when the final state looks right.

### Test seams

Exercise the real path. A seam observes or controls a boundary while the behaviour under test runs for real: a hook reporting a real completed event is coverage; a hook bypassing the behaviour is not.

Each asynchronous test needs a **completion witness**: deterministic ordering and bounded failure. Sleeps, repeated yields, manually invoking the expected result, and eventual-state polling are not witnesses.

Sort DEBUG/test code before cutting it: diagnostic payload (cut) · synchronization a completion witness needs (keep, minimal) · lifecycle or safety logic (keep). Move recorders, expectations, deadlines, and orchestration into test support when that lightens production classes. Keep cleanup of observers, tasks, gates, and fixtures. Simplify custom test machinery before removing the tests that rely on it.

## Output

- **Changes made / recommended**: candidate records with verdict `change`.
- **Contracts preserved**: each important contract and the check that still guards it; removed or replaced assertions, with the coverage that remains.
- **Validation**: exactly what ran, results against the baseline, and limitations.
- **Left unchanged**: worthwhile `uncertain` and `scope decision` records, with the reason.
