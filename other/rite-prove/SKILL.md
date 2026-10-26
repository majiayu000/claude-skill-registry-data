---
name: rite-prove
description: Prove a completed feature with tests and the full test suite, build/typecheck/lint, end-to-end/browser evidence, screenshots, commands, and outputs for seal. Not for single-slice proof.
argument-hint: "[feature-slug]"
user-invocable: true
---

<!-- loads: {"always":["devrites-lib/reference/standards/core.md","devrites-lib/reference/candidate-integrity.md","devrites-lib/reference/standards/testing.md","devrites-lib/reference/standards/spec-grammar.md","devrites-lib/reference/standards/test-proof-checklist.md","devrites-lib/reference/standards/agents.md","devrites-lib/reference/standards/gates.md","devrites-lib/reference/standards/verification-methods.md","rite-prove/reference/acceptance-proof.md","rite-prove/reference/proof-ladder.md","rite-prove/reference/failure-triage.md","rite-prove/reference/test-command-discovery.md","rite-prove/reference/anti-patterns.md","rite-build/reference/checkpoint.md"],"triggers":{"applicability":["devrites-lib/reference/standards/repository-topology.md","devrites-lib/reference/standards/data-integrity.md","devrites-lib/reference/standards/integration-reliability.md"],"browser":["devrites-lib/reference/standards/browser-proof-checklist.md","rite-prove/reference/browser-proof.md"],"devex":["devrites-lib/reference/standards/developer-experience.md"],"dod":["devrites-lib/reference/standards/definition-of-done.md"],"observability":["devrites-lib/reference/standards/observability.md"],"one-shot":["devrites-lib/reference/standards/one-shot-actions.md"],"performance":["devrites-lib/reference/standards/performance.md"],"workflow-artifacts":["devrites-lib/reference/standards/workflow-artifacts.md"]},"workspace":["brief.md","spec.md","state.md","decisions.md","assumptions.md","questions.md","decision-coverage.md","architecture.md","plan.md","tasks.md","traceability.md","eng-review.md","test-plan.md","gates.md","evidence.md","touched-files.md","browser-evidence.md"],"workspaceByRole":{"proof-runner":["spec.md","test-plan.md","tasks.md","gates.md","evidence.md","touched-files.md","browser-evidence.md","state.md"],"spec-reviewer":["brief.md","spec.md","decision-coverage.md","questions.md","decisions.md","assumptions.md","state.md"]},"rootOnly":["rite-build/reference/checkpoint.md","devrites-lib/reference/standards/workflow-artifacts.md"]} -->
> Read-set manifest: `devrites-engine context <slug> --phase prove` bundles every file named below into one deduplicated read. Trigger names map to the conditional rules in the sections that follow.


# /rite-prove: prove the completed feature

Prove the assembled feature once. No workspace: use `/verify` or `/run`;
pending tasks: stop for `/rite-build`.
Never assert unobserved passes. After Polish/Review edits, repeat affected
criteria/dependencies and bind under
[evidence validity](../devrites-lib/reference/candidate-integrity.md#evidence-validity).
Initial full feature proof and required mutable observations still run.

## Rules

Read the applicable standards: [`testing.md`](../devrites-lib/reference/standards/testing.md), [`test-proof-checklist.md`](../devrites-lib/reference/standards/test-proof-checklist.md),
[`browser-proof-checklist.md`](../devrites-lib/reference/standards/browser-proof-checklist.md) for UI, [`spec-grammar.md`](../devrites-lib/reference/standards/spec-grammar.md), [`performance.md`](../devrites-lib/reference/standards/performance.md),
[`observability.md`](../devrites-lib/reference/standards/observability.md), topology/data/integration rules named by the plan,
[`developer-experience.md`](../devrites-lib/reference/standards/developer-experience.md), [`definition-of-done.md`](../devrites-lib/reference/standards/definition-of-done.md), [`one-shot-actions.md`](../devrites-lib/reference/standards/one-shot-actions.md), and
[`workflow-artifacts.md`](../devrites-lib/reference/standards/workflow-artifacts.md). Developer surfaces require an observed flow, measured
TTHW, and exact signal-bearing errors; never assert DX (trigger `devex`).

- Each claim needs an executed positive, discriminating assertion and decisive
  signal; green commands alone are unproven. Methods must be genuinely distinct
  and coverage counted against an explicit denominator — apply
  [`verification-methods.md`](../devrites-lib/reference/standards/verification-methods.md).
- Follow [`candidate-integrity.md`](../devrites-lib/reference/candidate-integrity.md). Prove owns proof binding, not candidate
  grammar/hashing. Spec Drift Guard owns revealed contract drift.
- Root runs vetted gates/browser and records immutable evidence; proof runner
  validates it. Only the bounded wright fixes product source/tests.
- **Prove remains the controlling caller** during technical backtracking. Save
  its cursor; run Plan repair, Recovery Vet, remediation, and re-proof inline;
  consume nested boundaries; resume the failed rung. A strategy is spent after
  three no-progress attempts on the exact same fingerprint; escalate it per the
  [retry contract](../devrites-lib/reference/standards/afk-hitl.md#retry-cap-no-progress-loops-and-self-resolve)
  instead of stopping. Closing one or exposing a distinct
  Critical/Important invariant is progress, not a reason to hand work off.
<!-- workflow-artifact-adapter: {"module":"devrites-lib/reference/standards/workflow-artifacts.md","entry":"Prove consumes installed Workflow Artifact or CLEANED rerun","action":"VERIFY_EXISTING or admitted proof path ending PROVE_AND_RETURN","return":"saved Prove cursor; stop before real action"} -->
## Released-workspace refresh

Only an admitted `/rite-upgrade` assessment proving a released-format candidate
defect enters. Require legacy touched-file scope, live diff, tasks, and traceability agree unambiguously
on every candidate path/state. Missing or
ambiguous scope stops; never guess from Git. Preserve unrelated manifest content
and refresh only the strict manifest from observed bytes.

Discard old passes. Run all current approved real proof from scratch. Establish
pre-proof and post-proof engine digest with `devrites-engine check candidate
<slug>` and require equality, then write one fresh exact binding in evidence and
browser evidence. Current failure blocks; Upgrade does not authorize source or
test changes.

## Workflow

1. **Orient.** Read core, resolve active slug, require `state.md`, and read its
   cursor. On blocked Prove cold resume, reconcile retained consumptive evidence
   and no-progress corrections before accepting terminal none; a distinct
   fingerprint below cap resumes offline triage without another real action.
2. **Freeze scope.** Read spec, tasks, state, test plan, and full diff. Require
   every slice built except a [deferred slice](../rite-plan/reference/slicing.md#deferred-slice). Missing `test-plan.md` returns to Vet inline (Prove stays the controlling
   caller) and resumes here; it never authorizes ad hoc proof.
3. **Approve commands.** If absent, use
   [test-command-discovery](reference/test-command-discovery.md) over repository
   manifests/CI. Discovery is evidence only: `test-plan.md` is the sole approved runtime
   command list. A newly found command must return to the current Vet contract,
   refresh readiness, then resume without user handoff.
4. **Execute a frozen candidate.** Run `devrites-engine check candidate <slug>` and retain its digest.
   The root runs only commands declared by `test-plan.md`, with exact approved
   command, cwd, prerequisites, exit, and sanitized
   decisive output, plus the test selector, runner counts
   (collected/ran/passed/failed/skipped), and attempt number with first-attempt
   outcome; output and exit come from one execution. Run relevant suite plus build/typecheck/lint,
   concurrently when they share no build directory, port, or lock. Recheck the
   candidate and require identical digest/no source mutation. Reject substituted
   commands, malformed manifests, zero-test/skipped/filtered behavioral claims,
   exit-status-only claims, status-masking forms, and source drift. A retry-only
   pass is `flaky` per [`testing.md`](../devrites-lib/reference/standards/testing.md#determinism-no-flaky-tests),
   never green. Static gates prove only their named
   static criterion.
   Run the acceptance ledger with `--transcripts`: `devrites-engine gates run <slug>
   --transcripts` executes every unmet runnable gate against the same approved
   preflight rows, records definition-bound evidence, and writes one redacted,
   candidate-bound transcript per gate under `references/gates/<gate-id>/`;
   `gates reverify <slug> --transcripts` re-executes all of them when any prior
   pass is in doubt. Hand the proof runner those transcripts, never hand-built
   logs. Attest manual gates with `gates attest
   <slug> <id> <note>` only against observed judgment whose note cites the
   human's own words or source; placeholder notes are unmet and an AFK run never
   self-attests. Only gates manual at Vet are attested; runnable-to-manual
   conversion, EXPECT loosening, or CHECK/CWD/row change here is Plan repair plus
   re-Vet ([`gates.md`](../devrites-lib/reference/standards/gates.md)). An impossible outcome
   is `gates abandon` plus a handoff, never a deleted row or a false pass.
   `gates status <slug>` must reduce to `all-met` before Prove records green.
5. **Gate consumptive actions.** Immediately before execution, apply
   [`one-shot-actions.md`](../devrites-lib/reference/standards/one-shot-actions.md): current retained identity, bounds/sanitization,
   injective boundary map, per-seam fault fixtures, collision mutant, terminal
   fixtures, and cleanup-survival proof must be green. Missing/stale/disposable-
   only evidence returns to Vet without spending an attempt. Record the admitted artifact identity before execution.
   After failure, retained evidence is the
   reproduction; never rerun for diagnosis. Spent authorization blocks another
   action, but when action budget is zero it does not exhaust a newly identified
   offline fingerprint.
6. **Prove UI when applicable.** Use design brief/references, browser harness,
   allowed scratch path, [proof ladder](reference/proof-ladder.md), and
   [browser proof](reference/browser-proof.md): routes, viewports, opened and
   described screenshots, console/network, interaction, target comparisons, and
   every required state. Material mismatch fails.
7. **Independent validation.** Fresh read-only `devrites-proof-runner` and
   `devrites-spec-reviewer`, in one parallel wave, judge the same candidate/commands/evidence/acceptance map.
   Neither runs commands; reject missing/stale, invented-ID, label-only or self-attested reports.
8. **Map proof.** Reconcile verdicts under [acceptance-proof.md](reference/acceptance-proof.md).
   Every criterion/scenario/interaction/key link needs discriminating evidence or a
   blocker, including critical-path, observability, developer and wiring branches.
9. **Recover red.** Use [failure triage](reference/failure-triage.md) and Debug
   Recovery. Reconcile reproduction; send accepted in-scope source/test correction
   to the sole wright; update actual manifest; rerun affected proof, both candidate
   checks, and fresh proof runner. Recheck affected acceptance with the exact spec
   reviewer; reconcile both validators under evidence validity. Scope growth blocks.

   Agent-owned durable-plan errors run Spec Drift Guard, Plan, and Vet inline,
   preserving Prove as origin. Consumptive failures use retained fixtures, repair,
   and Vet, then stop for fresh GO after changed conditions. Ambiguous retained
   evidence does not prove that no safe future acquisition design exists: treat
   an in-scope discriminator as diagnostic-amplification Plan gap, repair its
   finite map/collision proof, narrow-Vet, then seek fresh GO before one evidence
   attempt. Never guess the runtime fix or reuse old GO.
10. **Record.** Root updates `evidence.md`, optional `browser-evidence.md`,
    traceability, and state, with exactly one observed candidate binding.
    After independent validators are green, checkpoint remaining candidate
    diffs per [`checkpoint.md`](../rite-build/reference/checkpoint.md). A wright
    correction during Recover red does not commit on control until this step.

> Do not claim an unobserved pass, skip browser proof, or proceed with pending
> slices. Load `reference/anti-patterns.md` when tempted to do so.

## Phase exit

**Complete when:** every criterion in `acceptance-proof.md` has discriminating
evidence bound to the current candidate digest, `gates status` reduces to
`all-met` with no handoffs, both independent validators admit
accounts, and `state.md` records Prove complete with no open `cannot_verify` rows.

**Failing case:** narrative "all tests passed" without `evidence.md` binding and
proof-runner admission → phase not complete; Seal blocks.
