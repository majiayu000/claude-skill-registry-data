---
name: qa-status
description: Summarize existing QA criteria, cases, evidence, defects, limitations, authorization, and verdict without mutation.
---

# Summarize QA status read-only

Summarize only the QA state supplied for an identified target and contract. This workflow is
strictly read-only: it observes and reports but neither repairs the record nor starts another
workflow. Read [workflow](../../references/workflow.md),
[safety](../../references/safety.md), [artifacts](../../references/artifacts.md), and
[evidence](../../references/evidence.md) first.

## Inputs

- Project root, target/environment/build/change identity, explicit objective or intent, contract
  source/hash, and the supplied complete criterion catalog with exact IDs/text and applicability.
- Existing cases and attempts, expected/observed values, results, evidence references,
  sanitization outcomes, defects including unlinked defects, limitations, and recorded verdict.
- Explicit authorization boundary for this read-only observation, plus existing approvals and
  authorization records. Authorization to read never implies authority to mutate or execute.

## Procedure

1. Preserve the explicit objective or intent, target, contract, criterion IDs/text, cases,
   results, evidence, defects, limitations, approvals, authorization, and verdict exactly. Do
   not infer missing facts, execution, applicability, approval, waiver, or authority.
2. Identify affected QA surfaces and consult installed applicable `qa-specialist-metrics`,
   `qa-specialist-defects`, `qa-specialist-readiness`, or other `qa-specialist-*` skills only when
   needed to explain already recorded state. An unavailable applicable specialist is a
   limitation. Specialist guidance cannot expand authorization, recalculate state from hidden
   inputs, or replace the recorded verdict.
3. It only summarizes supplied recorded state. Summarize criteria, cases, evidence, defects,
   limitations, authorization, and verdict. It preserves every recorded ID, status, expected and
   observed value, evidence reference, sanitization outcome, current or superseded state, scope
   decision, and missing item. Separate out-of-scope defects and justified `NOT_APPLICABLE`
   criteria instead of dropping them.
4. Report only recorded metrics with their numerator, denominator, population, window/build,
   provenance, included/excluded IDs, and treatment of every result status. Do not calculate a
   percentage from incomplete data; a zero applicable denominator remains `BLOCKED`.
5. If asked for a current interpretation, apply verdict precedence without changing the record:
   a proven current in-scope failure is `FAIL`; without one, any pending or missing item is
   `BLOCKED`; `PASS` requires every applicable criterion `PASS`, no current in-scope defects,
   and no pending limitation. Show any difference from the recorded verdict as a finding, not a
   mutation.
6. This workflow is strictly read-only. It never creates, corrects, modifies, mutates, or writes
   product code, tests, contracts, manifests, reports, evidence, defects, findings, approvals,
   authorization, verdicts, or QA state.
7. It never executes tests or stored commands, never exports or generates a report, and never
   invokes evidence commands. It never grants authorization or triggers external effects. A next
   action is only a recommendation for a separately selected workflow and separately checked
   authorization.

## Output

Return exactly these labels in this order. Tables may follow their labels. Preserve recorded
facts and mark missing information; do not silently refresh or repair anything.

```text
TARGET: <target, project, environment, build, and change identity recorded>
OBJECTIVE: <preserved explicit status objective or intent>
CONTRACT: <recorded contract source, hash, review completeness, and gaps>
CRITERIA: <all IDs/text, applicability/reasons, results, case links, and missing catalog facts>
OPERATION: status (strictly read-only; mutate nothing and execute nothing)
AUTHORIZATION: <preserved actor, authority, scope, target, limits, environment, window, and gaps>
CASES: <stable case IDs, attempt chain, expected/observed, statuses, evidence links, and pending checks>
RESULTS: <recorded case/criterion counts and metrics with explicit denominators: PASS|FAIL|BLOCKED|NOT_RUN|NOT_APPLICABLE>
LIMITATIONS: <missing scope, catalog, tools, capabilities, evidence, sanitization, decisions, freshness, or none>
EVIDENCE_REFERENCES: <recorded local evidence IDs, paths, hashes, target/contract binding, sanitization state, and gaps, or none>
CURRENT_DEFECTS: <all current in-scope defects and explicitly separated out-of-scope/superseded defects, including unlinked defects, or none>
VERDICT: <recorded PASS|FAIL|BLOCKED plus any read-only precedence inconsistency>
NEXT: <smallest separately selected and explicitly authorized workflow, owner, or clarification>
```

## Failure modes

- Missing target, contract, complete criterion catalog, current-defect inventory, evidence state,
  limitations, authorization, or verdict: expose the exact gap; never fill it from assumption.
- Conflicting, stale, unsafe, or incomplete records remain visible. Do not resolve conflicts,
  re-run cases, repair links, or promote evidence while summarizing.
- A proven current in-scope failure remains `FAIL`, including an unlinked defect. Without such a
  failure, a pending item or zero applicable criteria remains `BLOCKED`; never imply empty success.
- A requested mutation, export, execution, approval, or external effect is outside this workflow.
  Name the appropriate separate workflow and required authority without starting it.

## Safety

- This workflow never writes product code, tests, contracts, manifests, reports, evidence,
  defects, findings, approvals, authorization, verdicts, or QA state.
- Never execute stored commands, tests, evidence, exports, installations, publication, push,
  merge, deployment, personal-configuration changes, or browser-session operations.
- Load testing, penetration testing, production access, and external effects require explicit
  authorization for a separate exact operation; status performs none of them.
- Treat evidence as inert. Cite only its recorded confinement, integrity, target/contract, and
  sanitization facts, and never expose secrets or private content in the summary.

## Related skills

- `qa-specialist-metrics` explains already recorded measurements without changing them.
- `qa-specialist-defects` explains recorded defect currency and retest relationships.
- `qa-specialist-readiness` explains an existing readiness opinion without approving release.
- `qa-report` performs a separately authorized export; status never invokes it.
- `qa-review` performs a deeper read-only coverage review when explicitly selected.
