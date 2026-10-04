---
name: con-artist
description: Audit whether tests detect broken behavior by tracing assertions and running narrow controlled mutations in an isolated workspace; use for test-quality reviews, not routine test execution.
---

# Con Artist

> Your mock is very impressed with itself.

## Check what the test actually buys

Trace the requested assertions far enough to establish the actual exercised effect
and select a reachable fault. Follow unresolved bindings, mocks and relevant setup;
reading every intermediate wrapper is not itself evidence. Reuse known instructions,
runner and source context. Keep discovery inside the permitted project root; a
broad suite need not become a reading list of unrelated tests.

Use the evidenced runner and configuration; reuse a valid correct-code baseline.
Choose one meaningful fault at the requested boundary, such as acknowledging
without persisting. Preserve originals and compilation/binding context through
project isolation, disposable module/package copies or a valid substitution;
restore substitutions in reused processes. A wrong binding, rewritten simulation,
syntax error or equivalent mutation cannot establish test sensitivity.

Before adding an assertion, identify the required observable contract. Object
identity (including exception or traceback identity) needs an explicit identity
requirement; propagation or unwinding alone does not imply it. Reuse existing
neighboring controls when they cover the required boundary. Check the proposed
assertion on correct code before interpreting its failure on faulty code.

Inspect each phase's actual assertion and exit, not just a green baseline or a
nonzero mutant status. Runner errors/warnings can indicate broken assertion
plumbing, not a detected production fault. Establish provenance through copied
imports, traced bindings and defect-specific observations. Add instrumentation for
required or unresolved dispatch, not duplicate evidence; a separate import-only
process does not prove what the test process loads.

## Use support only where it helps

- Nearby known files: read relevant source/configuration directly. For scattered
  Python context, [the collector](references/python-context.md) locates definitions,
  ancestor instructions and fixtures. Select known bodies directly; indexes are
  navigation, not reviewed bodies or execution. Don't recollect equivalent context.
- Existing Python test improvements: consider [the complete four-check recipe](references/existing-tests.md)
  when they remove custom copy/run/cleanup plumbing. One recipe checks original
  and proposed tests against correct/faulty code with the native runner and fixtures;
  Native `python -B -m unittest` uses the same single recipe with
  `"invocation": "module"`; one fault’s original/stronger phases do not need
  the batch guide. Localized changes can use an exact edit instead of a complete
  replacement file.
  Applying the verified edit remains separate. No helper is needed for a simpler
  native workflow or an already-completed audit.
- Several independent Python faults or required test selections: choose the matching runner.
  For pytest, use the [common CLI contract](references/python-audit.md) with
  [batch fields](references/python-audit-batch.md), `"runner": "pytest"` and the default
  bootstrap invocation; `"invocation": "module"` is unittest-only.
  For required `python -B -m unittest`, the [native unittest batch recipe](references/native-unittest-batch.md)
  provides actual `python -B -m unittest` execution, same-process binding prechecks,
  copy cleanup and reusable correct observations without writing your own startup script.
  Consider it when those facilities remove needed orchestration. One fault's
  correct/mutant and stronger-assertion phases do not alone need a batch: the
  [single-audit contract](references/python-audit.md) supports them, as well as
  pytest and inline probes.
  Prefer existing project support or a simpler native check when sufficient;
  don't restart a completed audit to adopt a helper. It checks selected files by
  default; enable `guard_project` for required, authorized whole-project inventories.
  Inspect implementation for a concrete trust/adaptation question.
- Unexpected Python runner errors/warnings: [diagnostics](references/python-audit-advanced.md#diagnostics-and-incomplete-evidence)
  covers false-pass assertion helpers and incomplete checks. It is not routine setup.

If tests survive, distinguish demonstrating the gap from verifying a repair.
For a proposal-only review, give a concrete assertion and label it unexecuted
unless checked; demonstrating the requested fault still requires execution.
For requested test improvements or a claim that an assertion closes the gap,
verify it on correct and faulty code: pass the former, fail the latter for the
intended effect, not merely success or container size. If killed, identify the
detecting assertion or warning policy; this protects that fault, not every lifecycle path.

## Deliver and stop

Give decisive commands/results and the gap/proposed assertion or detecting check.
Distinguish executions from comparisons: one correct run used against several
faults is reused evidence even in a custom harness. Label that reuse and count
the run once, not once per comparison.
Keep a harness/report only for requested reuse or delivery. Without isolated
execution, label the concern static. Apply test improvements only when requested,
never the deliberate fault; an audit does not authorize publication.

Stop when the scoped claim and requested improvements are verified. Add faults
only for distinct material boundaries, not to fish for survivors, chase a global
mutation score or remove every mock. Preserve user changes and explicit requirements.
