---
name: sdd-verification-before-completion
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always. Also covers browser runtime, performance, production-telemetry, and spec-acceptance claims
disable-model-invocation: true
metadata:
    opencode/autoinvoke: false
---

# Verification Before Completion

## Overview

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

**Evidence must come from the environment the claim lives in.** Local green
supports "works locally"; a production claim needs production evidence. Claims
on other surfaces have their own standards: `browser-verification.md`,
`performance-verification.md`, `observability-verification.md`. Non-trivial
claims also get a falsification pass — see below.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

**Fresh means this verification cycle.** Evidence is fresh when it was produced
for this artifact in the current cycle and you inspected the actual output: a
command you ran, a recorded procedure you executed or observed, or captured
output you read at its stated path (a delegated run, a CI artifact, a test
report). It is stale when it predates the last change, when you infer it from
code, or when it is an assertion with no output behind it. Run the command
yourself whenever the claim requires independent execution — production claims,
agent success reports, anything you did not witness.

## Common Failures

| Claim                    | Requires                                                                                                                                                          | Not Sufficient                                 |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| Tests pass               | Test command output: 0 failures                                                                                                                                   | Previous run, "should pass"                    |
| Linter clean             | Linter output: 0 errors                                                                                                                                           | Partial check, extrapolation                   |
| Build succeeds           | Build command: exit 0                                                                                                                                             | Linter passing, logs look good                 |
| Bug fixed                | Test original symptom: passes                                                                                                                                     | Code changed, assumed fixed                    |
| Regression test works    | Red-green cycle verified                                                                                                                                          | Test passes once                               |
| Agent completed          | VCS diff shows changes                                                                                                                                            | Agent reports "success"                        |
| Requirements met         | Line-by-line checklist against the spec's Success Criteria, each criterion's command or recorded procedure run, no shipped behavior crossing an Out of Scope item | Tests passing, plan steps ticked               |
| UI works                 | Browser session: console clean, network correct, before/after comparison shows only intended changes                                                              | Unit tests passing, code "looks right"         |
| Optimization works       | Before/after measurements by the same method, delta beats run-to-run variance                                                                                     | "Obviously faster", one lucky run              |
| Works in production      | Post-deploy telemetry: real traffic exercised the path, RED metrics healthy, no new error class                                                                   | Pre-deploy induced-failure test, staging tests |
| End-to-end journey works | The journey run at the integration seam against the built artifact                                                                                                | Tests of its parts                             |

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- Browser-facing change never opened in a browser (or no recorded manual pass)
- Touched-path console noise left uninvestigated, or baseline noise accepted without recording it
- Performance claim with no before/after measurement
- "Works locally" standing in for a production claim
- Spec Success Criteria skipped in favor of plan checkboxes
- New behavior shipped that the spec's Out of Scope excluded
- Falsification reviewer handed the claim or the author's reasoning
- Any new falsification cycle on an unchanged artifact (the findings will not change; you are stalling)
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse                                   | Reality                                                                                                                    |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| "I'm confident"                          | Confidence ≠ evidence                                                                                                      |
| "Just this once"                         | No exceptions                                                                                                              |
| "Linter passed"                          | Linter ≠ compiler                                                                                                          |
| "Tests pass, so the spec is met"         | Tests check what was built; the spec checks what was promised. Run each Success Criterion's command or recorded procedure. |
| "It's obviously faster"                  | Unmeasured optimizations are complexity you maintain forever. Measure or revert.                                           |
| "Works locally, production will be fine" | Local evidence supports local claims. Production claims need telemetry.                                                    |
| "The extra feature was easy to add"      | Out of Scope is a promise too. Unrequested behavior is surface area, and a finding.                                        |
| "The reviewer agreed with me"            | The falsification reviewer never sees your claim. Classify its findings; don't collect its approval.                       |

## Key Patterns

**Tests:**

```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**Regression test validation (after the fix is in):**

```
✅ Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without falsification)
```

This validates that an existing regression test catches the bug. It never
substitutes for the implementer's BUILD-stage RED→GREEN evidence.

**Runtime (UI), performance, production (companions above):**

```
✅ UI: console clean, network correct, only intended visual changes | Performance: same-method before/after, delta beats variance, tests green | Production: post-deploy telemetry shows the path exercised and healthy
❌ Unit tests for a DOM claim / "obviously faster" / staging or local evidence for production
```

**Spec acceptance (requirements):**

```
✅ Re-read the spec's Confirmed Intent + Success Criteria → checklist keyed to each criterion → run each criterion's command or recorded procedure → confirm no shipped behavior crosses an Out of Scope item → report gaps
❌ "Tests pass, phase complete" / plan steps ticked
A criterion with no runnable command or recorded procedure is a finding, not a pass — name the missing evidence source.
```

## Falsification Pass (Non-Trivial Claims)

A claim is **non-trivial** when at least one of these is true:

- It introduces or modifies branching logic
- It crosses a module or service boundary
- It asserts a property the compiler cannot check (idempotence, ordering,
  thread safety, invariants)
- Its correctness depends on context the future reader cannot see
- Its blast radius is irreversible (deploy, migration, public API, data loss)

For those claims, run a disproof pass before the claim stands:

1. **Extract.** Write the smallest reviewable unit — the diff, the proposal,
   the assertion — with the contract it must satisfy, and cite the contract's
   source (spec section, plan task, requirement line). Strip your reasoning. A
   contract that cannot cite a source is itself a finding.
2. **Withhold the claim.** The reviewer must not see your conclusion or your
   reasoning: handing them over biases the review toward agreement.
3. **Dispatch where no scheduled review already covers the claim.** In SDD,
   the task review covers task-scope correctness, the final review covers
   branch integration, and the plan review covers plan-shape decisions — do
   not dispatch a falsification pass over the same artifact. The pass is for
   claims in the gaps (a controller ruling, an accepted trade-off, an
   "is safe / is reversible" assertion) and for inline or human sessions.
   Dispatch the `sdd-falsifier` agent — fresh context and an adversarial
   prompt; a separate model is ideal. A scheduled seat counts only if it is
   claimless and issues-only. No
   fresh context available? Do not stall on a human: run the pass on yourself
   as a **degraded** substitute (rewrite artifact + contract as a fresh
   self-prompt, keep the issues-only framing), label the result degraded, and
   record the pass as a ledger ruling where a ledger exists. In SDD, a
   subagent that runs the pass — or cannot run one — names the outcome in
   its report as a concern; the controller ledgers the ruling.
4. **Reconcile.** Findings are data, not verdict. Re-read the artifact against
   each finding, first matching class wins: **contract misread** (correct the
   contract _against its cited source_ — never weaken it — and re-run) →
   **actionable** (change the artifact, re-check) → **valid trade-off**
   (document it) → **noise** (note why it does not apply). If the source
   itself is ambiguous, that is a ledger ruling, not a contract rewrite. You
   decide; the reviewer lacks your context.
5. **Bound it.** Stop when a cycle returns only trivial or already-considered
   findings, the artifact has not changed since the last cycle, after 3
   cycles, or when the human partner says ship. Three unresolved cycles is
   information about the artifact: do not grind a fourth. Actionable findings
   route into the normal fix loop — in SDD, the task's five-round gate;
   falsification cycles are not fix rounds. Under SDD the outcome is a
   ledgered ruling and execution continues — a stop here is a decision, not a
   checkpoint. Escalate to the human partner only when one of SDD's four stop
   conditions applies.

Adversarial prompt:

```text
Adversarial review. Find what is wrong with this artifact.
Assume the author is overconfident. Look for:
- unstated assumptions
- edge cases not handled
- hidden coupling or shared state
- ways the contract could be violated
- failure modes under unexpected input

Do NOT validate. Do NOT summarize. Find issues, or state
explicitly that you cannot find any after thorough examination.

ARTIFACT: <artifact>
CONTRACT: <contract>
```

## When To Apply

Before any success, satisfaction, or completion claim — including commits, PRs,
task completion, agent delegation, and the surface claims routed to the
companions above (UI, performance, production). The rule covers exact phrases,
paraphrases, implications, and any communication suggesting completion.
