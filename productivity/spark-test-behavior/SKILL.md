---
name: spark-test-behavior
description: Use when adding or repairing Spark regression tests for asynchronous ownership, cancellation, persistence, restart recovery, or cross-surface projections. Not a coverage campaign, performance benchmark, source-text policy check, or full delivery review.
---

# Spark behavior tests

Turn a concrete failure into a test that distinguishes the intended contract
from the faulty behavior. Use the existing owner and test lane rather than
adding another harness or copying repository policy.

## Choose the observation and owner

Identify the triggering input or event order, the expected observable result,
and the production path that must enforce it. Consult
[the package inventory](../../../architecture/packages.json) and
[test architecture](../../notes/contracts/test-architecture.md) to locate the
owner, nearest tests, and appropriate lane.

Keep package behavior in its package. Root integration tests are for behavior
that crosses owners; source-process, browser, and packed-product tests prove
different boundaries. Read the owning manifest and Vitest configuration before
choosing a command. A green root suite does not establish that a package-local,
process, or browser test was discovered.

Where a contract suite already exists, bind the affected implementation to it.
For example, [Loop store contracts](../../../apps/spark-daemon/src/store/loops.contract.ts)
exercise store semantics; they do not replace daemon startup or drain tests.
Do not move a case to the root suite just to reuse setup.

## Make the bad ordering observable

For a stale result, cancellation, or replacement defect, identify the exact
suspension boundary. Hold the dependency there with a controllable fake or
barrier, wait until it is entered, cause the competing event, then release it.
Assert the observable result and the remaining tasks, resources, or committed
state. When the real dependency can finish after cancellation, the fake must
allow that completion too.

For retry delay policy, follow the contract's fake-timer guidance. Retain real
timers and the necessary scheduler or process boundary when testing actual
deadlines, cancellation, or drain. Bound waits and release resources even if
an assertion fails; do not repair ordering by adding sleeps or blind retries.

Distinguish accepted, committed, projected, and drained work. Hold persistence
at the relevant boundary when verifying publication order. Observe projections
through the owner API or real adapter; prompt text, transcript wording, and
frontend timers cannot serve as execution-state oracles.

## Keep the boundary that can fail

Use real temporary files, SQLite reopen, sockets, or child processes when that
is the contract being changed. Reuse the existing isolated test environment
instead of pointing at the user's Spark state. Check failures after partial
effects and reconnect or restart only when relevant to the reported defect.

For transport or schema changes, exercise the consumer's acceptance, rejection,
or normalization. For UI interaction, use the browser lane when focus or DOM
events matter. An in-memory store, mock process, SSR render, or snapshot proves
only its own boundary.

Try the regression against the faulty behavior in an isolated reproduction,
then against the repair. If a red run is unavailable, explain which assertion
would detect the defect and mark the result as unverified rather than inventing
a red/green history. Do not test source, prompt, or documentation fragments to
prove runtime behavior.

## Run and report

Select the focused command from
[CONTRIBUTING.md](../../../CONTRIBUTING.md#validation), confirm it discovered
and executed the intended case, then run the relevant broader gate.
Preserve explicit skips and missing native prerequisites in the result.

Report the contract, owner, controlled ordering, observed outcome, exact
commands and limitations. Performance conclusions belong to benchmarks;
publication readiness belongs to the existing delivery workflow.
