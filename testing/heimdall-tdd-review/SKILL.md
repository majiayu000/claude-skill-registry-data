---
name: heimdall-tdd-review
description: Review the artifacts of the TDD workflow — TDD-context findings (behavior, conventions, test infrastructure), test-driven work-package evidence on the uncommitted tree, post-wave integration results, and each commit against the reviewed diffs it records — selecting the checklist by a Focus line in the brief; architecture-context findings, architecture documents, and their persisted form belong to the dedicated architecture-review skill.
---

# TDD Review

## Purpose

Independent verification at each gate of the TDD workflow. Four artifact shapes pass through this skill, one per dispatch, selected by the brief's `Focus:` line:

| `Focus:` | Artifact under review | The gate it guards |
| --- | --- | --- |
| `context` | a TDD-context report — current behavior, engineering conventions, test infrastructure with an executed baseline | no test is written and no criterion is checked against unproven behavior, and no session rediscovers the test command |
| `package` | one work package's red-green-refactor evidence block, its **uncommitted** diff against `HEAD`, and its tests | no behavior is accepted without proof it was observed failing first, and **nothing reaches history before this review** |
| `integration` | a post-wave integration pass on the uncommitted tree | no open seam and no red suite reaches the commit step |
| `commit` | one commit the commit session recorded, against the plan row and the reviewed diffs of its batch | nothing reaches history that a review did not pass, and nothing that passed is left out |

**Not for** architecture artifacts — the architecture-context Workfile (module boundaries, boundary interfaces, embodied concepts, the existing-documentation inventory), the arc42 document, its decision records, and its persisted form. All of them are reviewed by the dedicated architecture-review skill (`heimdall-architecture-review`), which owns every checklist for an architecture artifact. `Focus: context` here is the behavioral shape only; a structural context report briefed to this skill is routed there, not squeezed into the checklist below.

**Ground truth, not self-report.** Every verdict rests on files you read at review time, commands you executed yourself, and paths you resolved. A producing session's claim about its own output is the thing under review, never evidence for it.

**Verdict grammar.** One line, the first line of the review Workfile:

```text
Verdict: <PASS | PASS-WITH-NOTES | BLOCKED> — focus=<context|package|integration|commit>, artifact=<path>, <one-clause reason>
```

- **PASS** — the artifact meets its contract and the spot-checks this Focus names all resolved.
- **PASS-WITH-NOTES** — it meets its contract with non-blocking gaps, named and located; it may be consumed as it stands.
- **BLOCKED** — one of this Focus's blocking conditions holds. Name it, locate it, and state what re-establishes it.

The verdict is yours. What follows from it — resuming the session, re-dispatching it, or returning to the plan — belongs to the requesting agent.

## Boundaries

- Never edit the artifact under review, the code, or the tests. Findings go in the review Workfile; fixes belong to a producing session.
- Never fill in a missing evidence field, section, or test on the producer's behalf. An absent field is a finding, and supplying it destroys the very thing you were dispatched to check.
- Never re-do the producer's work: no re-investigating the codebase, no re-deciding the architecture, no re-implementing the package. You validate evidence and conformance.
- Never review from session memory. On a re-review after a fix, re-read every changed file live.
- Never apply more than the one Focus the brief names — and never fewer.
- Never soften a blocking finding to keep a wave moving, and never trade it for a promise to fix it afterwards.

## When to Use

- Dispatched by the requesting agent as a review gate of the TDD workflow, with a `Focus:` line naming exactly one of `context`, `package`, `integration`, `commit`.
- The brief also carries the originating session's brief or package contract, the paths of the artifacts to review, the pinned `HEAD`, the recorded baseline test run, and — for `package` and `integration` — the **reviewed-but-uncommitted paths** the brief lists as already in the tree from earlier packages of the same batch.
- When the reviewed session ran with `Phase:` and `Mode:` control lines, the brief echoes them: `Focus: package` covers a tests-only `Phase: red` session, a `Phase: green+refactor` session, and an integrated one alike.
- **Not for** an architecture-context Workfile, an architecture document, its decision records, or its persisted directory as a dispatch of their own: load `heimdall-architecture-review` for those.
- **Not for** deciding what should have been built, re-running the investigation, or pronouncing on a step whose artifact does not exist yet.

## Workflow

**Apply only the subsection the brief's Focus names.** Steps 0, 1, and 2 always run.

**Step 0 — Read the control line and pin the baseline.**

- `Focus: context | package | integration | commit`. Missing or ambiguous → ask the requesting agent. Do not guess, and do not hedge by applying all four. A brief naming `architecture` names no Focus this skill has: route it to `heimdall-architecture-review` and say so rather than improvising a checklist.
- Under `Focus: context`, confirm the artifact is a **behavioral** TDD-context report before applying the checklist below. A Workfile whose sections are an area map, boundary interfaces, embodied cross-cutting concepts, or an architecture-document inventory is the architecture shape: stop, route it to `heimdall-architecture-review` `Focus: context`, and report that rather than blocking it for the test-infrastructure facts it was never contracted to carry.
- Resolve every artifact path the brief names. A named path that does not exist is a blocking finding by itself.
- Pin the reference: `HEAD` — verify it equals the brief's pinned value, because a moved `HEAD` under `package` or `integration` is a commit by a session that may not commit, blocking by itself; the recorded baseline run; and the reviewed-but-uncommitted list. A modified path in neither the write set nor that list is a write-set breach.
- Re-read the artifacts from disk now. Session memory of an earlier draft is not the artifact.

**Step 1 — Common checks (every Focus).**

- The named artifacts exist, are complete against their own declared output contract, and are the version the brief points at.
- The originating brief was honored: the inputs it named were used, its scope was not exceeded, and gaps were reported rather than invented.
- Every claim your verdict rests on is verified against ground truth — a resolved path, an executed command, or a line you quote from the live file.
- Every finding carries a location (`path:line`, section number, criterion ID) plus the evidence that establishes it and the change that would clear it.

### Focus: context

The artifact is the TDD-context Workfile: what the touched paths do today, the conventions the new code will sit beside, and the test infrastructure a test-first session will drive — with the baseline actually executed.

- **Scope declaration.** A preamble restates the objective and carries the **touched-path list** with its source declared — the ratified work packages' write sets and consumed contracts, or the objective itself when no architecture document exists — plus what was deliberately excluded and why. Without it, you cannot distinguish a thin report from a narrow one. An undeclared source is a finding: a path list said to come from a design that does not exist is the one claim here that cannot be spot-checked later.
- **Output contract complete.** Scope with the touched-path list; entry points and call paths for those paths; the interfaces the tests will call; current behavior of the touched paths; engineering conventions; test infrastructure with an executed baseline run; the test-runner and runtime dependencies those paths use; and an explicit not-examined list. A missing part is a finding; a missing test-infrastructure part on a code-touching objective is blocking.
- **Every finding proven.** `path:line`, or a command plus its captured output. "The service layer", "tests live under `test/`", "validation happens somewhere in the handler" are vague citations, not proofs.
- **Fact-rich, framing-poor.** No recommendation, no prioritization, no "should", no proposed design. Framing content is blocking: downstream steps must inherit facts to decide from, not conclusions already drawn for them.
- **Resolve at least two proofs yourself**, chosen from the most load-bearing findings — the interfaces the tests will call, the current behavior a criterion depends on, the test command. The path exists, the line numbers are accurate, and a quoted signature matches the live file character for character.
- **Run the recorded test command.** It exists, it executes, and the recorded baseline result reproduces — or the difference is explained. A baseline reported as executed that does not reproduce is fabricated evidence, not a stale note.
- **Signatures quoted, not summarized.** A paraphrased signature cannot be tested against.
- **`[UNVERIFIED]` discipline.** Each carries the reason verification was not possible, and they are at most a quarter of the findings.
- **Not checked here:** the area map, boundary interfaces, cross-cutting concepts as embodied, the existing architecture-document and decision-record inventory, and the current-state view. This shape carries none of them by contract; their absence is never a finding and never blocking.
- **BLOCKED on:** a proof that does not resolve or names a nonexistent path; a recorded baseline run that does not reproduce; recommendation or prioritization content; absent test-infrastructure facts for a code-touching objective; unverified findings above a quarter of the total.

### Focus: package

**(a) Evidence block.** The central claim is that every behavior was observed failing before it was implemented, and that claim is worth exactly as much as the captured output supports.

- **Complete before assessed.** Session header (package, phase, mode, criterion IDs, write set, test command); the baseline run; the red run; the green run; the final run; the criterion-to-test coverage table; files changed with any write-set deviation and its reason; the would-fail check; `Commits: none`; and the gaps or concerns reported. A missing field is a finding — never fill it in for the author.
- **Verbatim or absent.** Real output names the runner, the test, and the failing assertion. "Tests failed as expected" is prose, and prose is not evidence: treat a paraphrased phase as a missing phase.
- **Red plausibility, per unit.** The failing test names appear in the diff; the output matches the project's real runner format; the failure is the assertion that was written, not a missing import, a syntax error, or a misconfigured harness. Infrastructure noise is not red evidence.
- **Resolve the coverage table, do not read it.** Open each cited `file:line`, confirm the test exists there, and confirm it asserts the criterion it is mapped to. An entry naming a test absent from the diff, or pointing at a test that already existed, voids red-before-green for that criterion.
- **Verify the would-fail check.** Its claim is that reverting the implementation alone would make the new tests fail again. Confirm it by reverting or stubbing the implementation and re-running when that is cheap; otherwise read each new test against the implementation and name the assertion that would break. State which method you used.
- **Distrust a frictionless narrative.** No red phase at all; every unit green on the first attempt; red captures identical in shape across distinct units; a red output that never mentions the behavior under test; a would-fail check described in generalities. Each signal is a reason to resolve *more* of the coverage table, not fewer.
- **Immediately-green tests** are legitimate only when the report says so and classifies them — already-implemented behavior, or a weak assertion that was then strengthened. An unclassified one is a finding.
- **Baseline honesty.** Failures already present at the pinned baseline are reported unchanged, neither quietly repaired nor hidden.

**(b) Code correctness.** Every owned criterion is implemented and behaves as the criterion states. Contracts conform exactly — signatures, types, error and status contracts match the specified blackbox interface or the codebase's existing signature, because a silent divergence breaks a sibling package that was built against the same contract. The edge, error, boundary, and permission cases the criteria name are handled. The code runs: run it. Nothing exists that no test demanded — no speculative abstraction, no unused configuration knob.

**(c) Test quality.** One behavior per test. Assertions on observable behavior, not internals. Deterministic and order-independent, with time, randomness, and network controlled. Assertion strength — would this fail on a plausible regression, or would it pass either way? No mocking so heavy that the test verifies its own fakes. Negative and boundary criteria have their own tests rather than a branch inside the happy-path test. Test structure that mirrors the implementation's structure is a sign of tests fitted to the code.

**(d) Discipline.** Files changed — `git status` and `git diff HEAD`, minus the reviewed-but-uncommitted list the brief gave you — are a subset of the declared write set, with any deviation named and reasoned; compare the path lists yourself. **`HEAD` is unchanged since the brief's pinned value: no commit by the session, in any mode; verify with `git log`, not with the report.** In `Phase: green+refactor`, the handed-over tests are unchanged; a reviewed test edited by the implementing session is blocking. In `Mode: parallel`, verify against the diff and the version-control history rather than the report: no edits outside the write set including the shared scaffold, own test subset only, no tree-wide side effects (dependency installs, lockfile regeneration, repository-wide codegen or formatting), and no sibling failure skip-marked, disabled, or deleted to reach a clean run.

**(e) `Phase: red` sessions only.** No production code beyond the scaffolding the tests need to compile and execute; stubs may exist but must not satisfy an assertion; each test fails for its intended reason; and the handover states which units are covered and which remain.

**BLOCKED on:** a fabricated, paraphrased, or unresolvable red; tests back-filled after the implementation; a reviewed test modified in a `green+refactor` session; a write-set breach; any commit since the pinned `HEAD`; an owned criterion with no test that was observed failing first. A broken cycle cannot be reconstructed after the fact, so the remedy is re-establishing it from a reverted state, not a note in the review.

### Focus: integration

- **Run the full suite yourself**, never a package subset, from the live tree. It is green, and no test that passed at the pinned baseline now fails. Baseline failures still present are reported unchanged.
- **Seams resolved.** Every seam the concurrent sessions reported is closed: no shared surface duplicated into two packages' local copies, no dangling stub the scaffold left behind, no consumed contract still unimplemented.
- **Write sets and history.** Against the wave's cumulative **uncommitted** diff: no file was touched by two packages; nothing landed outside the union of the declared write sets plus the integration package's own; `HEAD` is unchanged since the wave began, verified with `git log`; and no transient workspace content was modified, staged, or committed.
- **BLOCKED on:** a red suite or any regression against the baseline; a cross-package write-set violation; an open seam; any commit since the pinned `HEAD`.

### Focus: commit

Inputs are the plan Workfile with the batch row, the commit record, and the gating review Workfiles. You verify that history received exactly what the reviews passed — nothing more, nothing less.

- **(a) One commit, right parent.** `git log --oneline <pinned>..HEAD` lists exactly one commit, and its parent is the pinned reference. No ref was rewritten.
- **(b) Branch.** The current branch equals the plan row's and carries a `feature/`, `fix/`, or `refactor/` prefix.
- **(c) Path set.** `git show --stat --name-status HEAD` equals the union of the batch's evidence-block `Files changed`, computed by **you** from the gating reviews — nothing extra (no `.yggdrasil-workspace/` path), nothing missing.
- **(d) Message.** `<type>: <subject>` equals the plan row verbatim; the type is one of `feat:`, `fix:`, `refactor:`, `test:`; and the type is consistent with the diff's shape.
- **(e) Green at `HEAD`.** Run the full suite yourself: green, or the baseline's failures unchanged.
- **(f) Leftovers.** `git status --porcelain` shows only the plan's recorded baseline-dirty paths.
- **(g) Gate honored.** Each gating review Workfile's first line reads PASS or PASS-WITH-NOTES.
- **BLOCKED on:** a path-set mismatch; red at `HEAD`; a non-conforming branch; more than one commit or a rewritten ref; workspace content committed; a gating review that did not pass.

A blocked commit is already history and this workflow never rewrites it: name the corrective commit that clears the finding.

**Step 2 — Write the review Workfile.**

Write to the path the brief names, following the pattern `NN-review-<focus>-<name>.md` — `NN-review-context-tdd-<area>.md`, `NN-review-package-<name>.md`, `NN-review-integration.md`, `NN-review-commit-<n>.md` — in this order:

1. The verdict line.
2. **Blocking findings**, worst first: location, the evidence that establishes each, and the change that clears it.
3. **Notes** — non-blocking gaps, explicitly marked as not blocking consumption.
4. **Verification method** — what you checked by execution (the commands and their results), what you checked by reading, and what you could not verify and why.

Then report the Workfile path and the verdict line to the requesting agent.

## Quality Criteria

- Exactly one Focus was applied, and the verdict line names it.
- Every finding has a location and the evidence that establishes it, and states what would clear it — the producing session knows precisely what to change.
- Ground truth beat self-report: at least the spot-checks this Focus names were actually executed, and the review distinguishes what was verified by execution from what was verified by reading.
- The joint to the previous stage was checked rather than assumed. The workflow is one traceability chain — acceptance criteria → building blocks and decision records → TDD-context facts → plan → work packages → tests → the integrated suite → commits — and each Focus owns one link plus the seam behind it.
- Blocking findings are separated from notes, so the requesting agent can tell a re-dispatch from a nicety.
- The producer's work was validated, not repeated: no re-investigation, no re-design, and no re-implementation appears in the review.
- An artifact that could not be verified is reported as unverifiable with the reason. An unresolved check is never rounded up to PASS.

## Anti-Patterns

- **Rubber-stamping**: passing because the artifact looks complete and the session sounded confident.
- **Format-only evidence review**: confirming an evidence block has all its fields without resolving a single test location or running a single command.
- **Trusting paraphrase**: accepting "all tests pass" or "failed as expected" in place of captured run output.
- **Reviewing from session memory**: re-reviewing a corrected artifact against what you remember of it instead of the file as it now stands.
- **Applying every checklist at once**: four Focus passes crammed into one dispatch produce a long review that verifies none of them properly.
- **Re-doing the producer's work**: investigating the codebase yourself, redesigning the architecture, or fixing the code you were dispatched to review.
- **Reviewing a structural context report against this checklist**: blocking an architecture-context Workfile for a missing baseline run or behavior characterization. It is contracted to carry neither; it belongs to the architecture-review skill's own `Focus: context`.
- **Filling the gap you found**: writing the missing evidence field, section, or test, and then passing the artifact that lacked it.
- **Nitpicking as a verdict**: a page of style notes with the write-set breach or the fabricated red unmentioned.
- **Negotiating a blocker**: downgrading BLOCKED to a note because the wave is nearly finished — the cost of a broken cycle or a corrupted tree lands later and larger.
- **Passing a commit by its message**: the subject matches the plan row, so the path set is never diffed against the reviewed evidence.
- **Reviewing the tree as the commit**: confirming green on the working tree without confirming that the tree beyond `HEAD` holds only the planned leftovers.
- **Deferring to method that lives elsewhere**: this skill is the complete review method for these four gates, and it names no external checklist; an architecture artifact is routed to `heimdall-architecture-review`, never reviewed here. A gap anywhere else is a report item to the requesting agent, not license to improvise from an unrelated checklist.
