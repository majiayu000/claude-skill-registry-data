---
name: qa-review
description: Review requirements, coverage, results, evidence, and findings without changing the product or recorded state.
---

# Review QA coverage read-only

Assess whether the supplied QA record covers the governing requirements and supports its stated
results. This is a read-only review: it reports gaps and findings without changing product code,
tests, contracts, approvals, evidence, or recorded state. Read
[workflow](../../references/workflow.md), [safety](../../references/safety.md),
[artifacts](../../references/artifacts.md), and [evidence](../../references/evidence.md) first.

## Inputs

- Project root, target/environment/build/change identity, explicit objective or intent, identified
  contract source/hash, and the complete supplied criterion catalog with exact IDs, text,
  applicability, and current results.
- Risks, planned and executed cases, stable case/attempt IDs, expected and observed values,
  exclusions, prerequisites, limitations, and verified local evidence references.
- Complete current-defect inventory, including unlinked and out-of-scope defects, retest history,
  findings already accepted or deferred, and the recorded QA verdict.
- Explicit authorization boundary for this read-only review and any separately proposed follow-up.
  Load, penetration, production, and external effects require separate exact authorization.

## Procedure

1. Preserve the explicit objective or intent, target, contract, criterion IDs/text, existing
   results, findings, limitations, approvals, and authorization exactly. Never infer missing
   criteria, applicability, approval, execution permission, or risk acceptance.
2. Identify affected surfaces and consult the installed applicable `qa-specialist-*` skills,
   starting with `qa-specialist-requirements`; use functional, API, Web, mobile, data,
   accessibility, security, performance, automation, CI/CD, regression, defects, metrics, or
   production specialists only when their surfaces apply. An unavailable applicable specialist
   is a limitation. Specialist guidance does not expand authorization.
3. Review requirements first: confirm catalog completeness, preserve each ID and text, and assess
   applicability, clarity, consistency, testability, observable oracle, source identity, and
   traceability. Ambiguity or contradiction remains `BLOCKED`; proposed wording is never an
   authoritative correction.
4. Review coverage against each applicable requirement and risk. Trace inclusions, exclusions,
   cases, attempts, environments, data, positive/negative/boundary/recovery paths, expected and
   observed results, evidence, and defects. A hash proves integrity, not semantic completeness.
5. Report findings with stable IDs, affected requirement/risk/case/defect IDs, severity and
   rationale, supporting evidence or explicit evidence gap, owner, and smallest valid follow-up.
   Keep proven failures, coverage gaps, limitations, and editorial observations distinct.
6. Apply verdict precedence to the supplied facts without mutating them: a proven current
   in-scope failure, including an unlinked defect, is `FAIL`; otherwise any missing criterion,
   coverage, evidence, prerequisite, capability, decision, or unresolved finding is `BLOCKED`.
   `PASS` requires every applicable criterion `PASS`, no current in-scope defects, no pending
   item or limitation, and a complete review scope. Zero applicable criteria is `BLOCKED`.
7. Return the review read-only. It never corrects, modifies, or mutates the product, tests,
   contracts, approvals, evidence, findings, or state. Product code corrections are only allowed
   when explicitly requested in a separate authorized operation.
8. A later inert export may use `qa_report.py report --manifest PATH --project-root PATH`; the
   report does not run or re-run tests and does not resolve findings.

## Output

Return exactly these labels in this order. Tables may follow their labels. Preserve requirement
text and distinguish reviewed facts from reviewer findings.

```text
TARGET: <target, environment, build, and change identity>
OBJECTIVE: <preserved explicit objective or intent>
CONTRACT: <source identity and hash>
CRITERIA: <complete preserved IDs/text, applicability, results, and gaps>
OPERATION: review (read-only; mutate nothing)
AUTHORIZATION: <preserved actor, authority, scope, target, limits, environment, window, and gaps>
REQUIREMENTS_REVIEW: <completeness, clarity, consistency, testability, oracles, and traceability by criterion ID>
COVERAGE_REVIEW: <criterion/risk to cases, attempts, environments, data, expected/observed, evidence, defects, and exclusions>
FINDINGS: <stable finding IDs, severity/rationale, affected IDs, evidence or gap, owner, and follow-up>
RESULTS: <reviewed case, criterion, finding, and coverage statuses: PASS|FAIL|BLOCKED|NOT_RUN|NOT_APPLICABLE>
LIMITATIONS: <missing scope, criteria, traceability, tools, capabilities, evidence, decisions, or none>
EVIDENCE_REFERENCES: <verified local evidence IDs, paths, hashes, target/contract binding, or none>
CURRENT_DEFECTS: <all current in-scope defects and explicitly separated out-of-scope defects, including unlinked defects, or none>
VERDICT: <PASS|FAIL|BLOCKED under the shared contract>
NEXT: <smallest separately selected and authorized clarification or correction request>
```

## Failure modes

- Missing target, contract, complete criterion catalog, risk/coverage inventory, current defects,
  or review boundary: record the exact gap and return `BLOCKED` unless valid evidence already
  proves a current in-scope failure, which returns `FAIL`.
- Requirement ambiguity, untraceable exclusion, missing oracle, uncovered material risk, or
  unsafe/insufficient evidence is a finding, never an inferred pass or silent correction.
- A proven current in-scope failure remains `FAIL` even if all linked criteria appear green or
  the defect has no criterion association.
- Requested correction or mutation is outside this workflow. Report it under `NEXT` and require
  a separately selected, explicitly authorized operation.

## Safety

- This workflow is read-only and never writes product code, tests, contracts, evidence, findings,
  approvals, or QA state.
- Load testing, penetration testing, production access, and external effects require explicit
  authorization for their exact target and bounded operation; this review performs none of them.
- Never install or configure tools, execute stored commands, publish, push, merge, deploy, alter
  personal configuration, or expose secrets or personal browser state.
- Product code corrections are only permitted when explicitly requested outside this review.
  Evidence remains inert, local, regular, confined, target/contract-bound, integrity-checked, and
  reviewed for sanitization.

## Related skills

- `qa-specialist-requirements` supplies the primary requirement analysis.
- Applicable `qa-specialist-*` skills assess their surfaces without expanding authority.
- `qa-bug` may record an accepted defect in a separate authorized write operation.
- `qa-release` may consume the completed review without treating it as release approval.
- `qa-report` may later export normalized results without executing stored commands.
