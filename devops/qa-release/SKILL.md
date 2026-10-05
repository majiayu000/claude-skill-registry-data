---
name: qa-release
description: Produce an evidence-backed release readiness opinion while keeping the human release decision separate.
---

# Assess release readiness

Produce a QA opinion for an identified release target, with explicit failures and pending items.
This workflow recommends; it does not approve, publish, merge, push, deploy, or otherwise perform
the release. Read [workflow](../../references/workflow.md),
[safety](../../references/safety.md), [artifacts](../../references/artifacts.md), and
[evidence](../../references/evidence.md) first.

## Inputs

- Project root, target/environment/build/change identity, explicit objective or intent, identified
  contract source/hash, and the complete supplied criterion catalog with exact IDs/text,
  applicability, results, cases, attempts, expected/observed values, and evidence references.
- Complete current-defect inventory, including unlinked defects, scope decisions, owners,
  resolution and terminal retest state, plus prior QA review findings.
- Risks, mitigations, residual exposure, prerequisites, limitations, missing capabilities,
  unsafe or insufficient evidence, pending work, and release-entry/exit gates.
- Existing human release and risk decisions, each with actor, authority, scope, rationale, and
  timestamp, or an explicit missing record. These decisions are inputs, not QA results.
- Explicit authorization boundary for this consultative assessment and for any separately
  proposed production or external action. No release action is authorized by this workflow.

## Procedure

1. Preserve the explicit objective or intent, target, build, contract, criterion IDs/text,
   results, findings, risks, limitations, approvals, human decisions, and authorization exactly.
   Do not infer a missing decision, applicability, waiver, risk acceptance, or execution right.
2. Identify affected surfaces and consult the installed applicable `qa-specialist-*` skills,
   starting with `qa-specialist-readiness`; consult requirements, defects, regression, metrics,
   functional, API, Web, mobile, data, accessibility, security, performance, automation, CI/CD,
   or production specialists only when their surfaces apply. An unavailable applicable
   specialist is a limitation. Specialist guidance cannot expand authorization.
3. Confirm catalog completeness and evaluate every criterion. Preserve justified
   `NOT_APPLICABLE` items and their reasons. Zero applicable criteria is `BLOCKED`; unknown or
   partial applicability is pending, never silently excluded.
4. Inventory every current in-scope defect independently of criterion links. A proven current
   failure, including an unlinked defect, is `FAIL` and takes precedence over waivers, risk
   acceptance, severity, priority, or incomplete pending work.
5. List failures and pending items separately. Evaluate terminal retests, evidence safety and
   sufficiency, review findings, release gates, tools/capabilities, risks, mitigations, residual
   exposure, owners, and next actions. Without a proven failure, any missing, unsafe,
   insufficient, unresolved, or pending item makes the verdict `BLOCKED`.
6. Keep every human release or risk decision separate from the QA verdict. Record actor,
   authority, scope, rationale, and timestamp without changing either the decision or underlying
   results. Risk acceptance cannot turn `FAIL` or `BLOCKED` into `PASS`; a required missing or
   incomplete human decision remains pending.
7. Apply verdict precedence exactly: `PASS` requires all applicable criteria `PASS`, no current
   in-scope defects, no pending work, no pending risk, no pending limitation, no pending evidence,
   no pending gate, no pending required decision, no proven failure, and a complete catalog. A
   proven current in-scope failure is `FAIL`; otherwise any pending item or zero applicable
   criteria is `BLOCKED`.
8. Recommend release only for `PASS`, recommend against release for `FAIL`, and identify the
   exact owner/blocker for `BLOCKED`. The release owner makes the human decision separately.
9. Return the opinion without release effects. Production access and external effects may occur
   only in a separately selected operation with explicit authorization for the exact target,
   environment, limits, window, owner, stop conditions, and cleanup. This workflow never
   publishes, pushes, merges, deploys, or executes stored commands.
10. A later inert export may use `qa_report.py report --manifest PATH --project-root PATH`; the
    report does not run or re-run tests and its exit code does not replace the QA verdict.

## Output

Return exactly these labels in this order. Tables may follow their labels. Never combine the QA
verdict, recommendation, and human decision into one field.

```text
TARGET: <target, environment, build, and change identity>
OBJECTIVE: <preserved explicit objective or intent>
CONTRACT: <source identity and hash>
CRITERIA: <complete preserved applicable/non-applicable IDs/text, reasons, results, and gaps>
OPERATION: release (consultative QA opinion; perform no release effect)
AUTHORIZATION: <preserved actor, authority, scope, target, limits, environment, window, and gaps>
FAILURES: <proven current in-scope failures with criterion/case/defect/evidence IDs, or none>
PENDING: <unresolved gates, work, findings, retests, evidence, capabilities, risks, decisions, owners, and next actions, or none>
RISKS: <risks, mitigations, residual exposure, acceptance records, and gaps>
HUMAN_DECISION: <separate release/risk decision with actor, authority, scope, rationale, timestamp, or missing>
RESULTS: <case, criterion, defect, gate, and readiness statuses: PASS|FAIL|BLOCKED|NOT_RUN|NOT_APPLICABLE>
LIMITATIONS: <missing catalog, scope, tools, capabilities, evidence, decisions, or none>
EVIDENCE_REFERENCES: <verified local evidence IDs, paths, hashes, target/contract binding, or none>
CURRENT_DEFECTS: <all current in-scope defects and explicitly separated out-of-scope defects, including unlinked defects, or none>
VERDICT: <PASS|FAIL|BLOCKED under the shared contract>
RECOMMENDATION: <recommend release only for PASS; recommend against for FAIL; exact blocker/owner for BLOCKED>
NEXT: <human decision or smallest separately selected and explicitly authorized follow-up>
```

## Failure modes

- Missing, partial, or zero-applicable criterion catalog is `BLOCKED`; never infer `PASS` from
  an empty denominator or from available tests alone.
- Missing current-defect inventory, unlinked-defect review, risk inventory, release gates,
  limitations, or required decision record is `BLOCKED` unless valid evidence proves a current
  in-scope failure, which is `FAIL`.
- A current proven failure remains `FAIL` regardless of waiver, accepted risk, criterion linkage,
  severity, priority, or human preference.
- A human decision missing actor, authority, scope, rationale, or timestamp is incomplete and
  pending. Do not repair, approve, or execute it.
- A release request beyond the recorded authorization stops before any effect and identifies the
  exact missing authority and owner.

## Safety

- This workflow never releases, deploys, publishes, pushes, merges, changes approvals, or grants
  production or external-effect authorization.
- Load testing, penetration testing, production access, and external effects require explicit
  authorization for their exact bounded operation; this assessment performs none of them.
- Never install or configure tools, execute stored commands, alter personal configuration, expose
  secrets or personal browser state, or treat a QA recommendation as a human decision.
- Product code corrections are only allowed when explicitly requested in a separate authorized
  operation. Evidence remains inert, local, regular, confined, target/contract-bound,
  integrity-checked, and reviewed for sanitization.

## Related skills

- `qa-specialist-readiness` supplies the primary readiness analysis.
- `qa-review` supplies a read-only requirements and coverage review.
- `qa-specialist-defects` assesses whether defects remain current after terminal retests.
- `qa-status` may later summarize the recorded opinion without mutation.
- `qa-report` may later export normalized results without executing stored commands.
