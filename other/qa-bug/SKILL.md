---
name: qa-bug
description: Record a reproducible defect, independent triage, immutable attempts, and evidence-backed retest state.
---

# Record and reassess a defect

Record defect facts without changing the product. Preserve reproduction, triage, scope, evidence,
attempt history, and retest semantics under the governing contract. Read
[workflow](../../references/workflow.md), [safety](../../references/safety.md),
[artifacts](../../references/artifacts.md), and [evidence](../../references/evidence.md) first.

## Inputs

- Project root, target/environment/build/change identity, explicit objective or intent,
  identified contract source/hash, and the complete supplied criterion catalog with exact IDs,
  text, applicability, and current results.
- Stable defect ID, summary, prerequisites, exact reproduction steps and data, frequency,
  expected and observed behavior, affected surface, in-scope/out-of-scope decision, and local
  target-bound evidence.
- Severity and priority proposals with separate rationales, owner, current state, linked
  criterion IDs or an explicit unlinked reason, related risks, and complete current-defect inventory.
- Stable logical case ID, original failure and all retest attempts with unique attempt IDs,
  increasing attempt numbers, supersession links, evidence, and explicit authorization for this
  write operation or any separately requested retest execution.

## Procedure

1. Preserve the explicit objective or intent, target, environment/build, contract, criterion
   IDs/text, defect identity, existing attempts, approvals, and authorization exactly. Do not
   infer expected behavior, applicability, resolution, risk acceptance, or execution permission.
2. Identify affected surfaces and consult the installed applicable `qa-specialist-*` skills,
   starting with `qa-specialist-defects`; consult requirements, functional, API, Web, mobile,
   data, security, performance, automation, CI/CD, regression, or production specialists only
   when their surfaces apply. An unavailable applicable specialist is a limitation. Specialist
   guidance cannot expand authorization.
3. Materialize reproduction with prerequisites, ordered steps/actions, safe data, environment and
   build, frequency, expected oracle, observed mismatch, scope and rationale, criterion links or
   explicit unlinked reason, risk links, and verified evidence references. Insufficient
   reproduction or evidence is `BLOCKED`; never manufacture certainty.
4. Assess severity from product/user impact and blast radius. Assess priority independently from
   delivery order, urgency, dependencies, and scheduling. Record both rationales, owners, and
   scope; neither value rewrites the other, the defect status, or the QA result.
5. Preserve the original failure and every retest as immutable history. Use one stable logical
   case ID, unique attempt IDs, strictly increasing attempt numbers, the same target, and a
   linear `supersedes` chain. Never delete a failure, branch/cycle history, or rerun until green.
6. Record a retest result only from an explicitly authorized `qa-test` execution and valid local,
   confined, target/contract-bound, integrity-checked, sanitized evidence. This write workflow
   does not itself execute a stored command or product correction.
7. Mark this defect resolved only when the referenced terminal retest attempt is `PASS` with
   valid current evidence; a blocked/failed terminal attempt never falls back to an older pass.
   Return global `PASS` only after the terminal retest is valid and has valid current evidence,
   all applicable criteria are `PASS`, no pending work or limitations remain, and no other current
   in-scope defects remain. Missing criteria or defect inventory is `BLOCKED`; another proven
   current in-scope defect is `FAIL`.
8. Apply verdict precedence: any proven current in-scope failure, including an unlinked defect,
   is `FAIL`; without such proof, missing reproduction, evidence, retest, or complete inventories
   is `BLOCKED`. `qa_report.py report --manifest PATH --project-root PATH` is a later inert export
   and the report does not execute or re-run tests.

## Output

Return exactly these labels in this order. Tables may follow their labels; keep expected,
observed, evidence, severity, priority, scope, and history separate.

```text
TARGET: <target, environment, build, and change identity>
OBJECTIVE: <preserved explicit objective or intent>
CONTRACT: <source identity and hash>
CRITERIA: <preserved IDs/text, applicability/results, links, or explicit unlinked reason>
OPERATION: bug (write defect and supplied retest state; execute no product correction)
AUTHORIZATION: <preserved actor, authority, scope, target, limits, environment, window, and gaps>
DEFECT: <stable ID, summary, state, owner, scope/rationale, criterion/risk links, and current decision>
REPRODUCTION: <prerequisites, ordered steps/data, environment/build, frequency, expected, observed, and evidence IDs>
TRIAGE: <severity/impact rationale and priority/delivery rationale recorded independently>
ATTEMPT_HISTORY: <stable case ID, all unique attempt IDs/numbers, supersedes, target, expected, observed, status, evidence IDs>
RETEST: <referenced terminal attempt, authorization/source, evidence validity, and resolution decision>
RESULTS: <defect, attempt, case, and criterion statuses: PASS|FAIL|BLOCKED|NOT_RUN|NOT_APPLICABLE>
LIMITATIONS: <missing reproduction/criteria/inventory/authorization/tools/evidence, ambiguous scope, or none>
EVIDENCE_REFERENCES: <verified local original/retest evidence IDs, paths, hashes, target/contract binding, or none>
CURRENT_DEFECTS: <this defect plus every other current in-scope defect and separated out-of-scope defects, or none>
VERDICT: <PASS|FAIL|BLOCKED under the shared contract>
NEXT: <smallest separately selected and authorized follow-up>
```

Valid resolution example: `DEF-LOGIN-01` links `AC-LOGIN-01` and logical
`CASE-LOGIN-LOCK`; original `ATT-LOGIN-01` is `FAIL`, terminal `ATT-LOGIN-02` supersedes it and
is `PASS` with valid retest evidence. This closes only `DEF-LOGIN-01`. Global `PASS` additionally
requires the complete applicable catalog (including `AC-LOGIN-01`) to be `PASS` and an explicit
inventory showing no other current in-scope defect.

## Failure modes

- Missing target, environment/build, scope, reproduction, expected/observed distinction, valid
  evidence, or severity rationale: preserve the finding and return `BLOCKED` unless valid current
  evidence already proves an in-scope failure, which is `FAIL`.
- Severity copied into priority, or priority used to weaken severity/status: keep them separate
  and request the missing rationale without changing the recorded result.
- `resolved` without a terminal valid `PASS` retest and evidence keeps the defect current. Never
  fall back to an older pass after a terminal `FAIL` or `BLOCKED` attempt.
- Missing, branched, cyclic, cross-target, or non-increasing attempt history invalidates the
  resolution conclusion; preserve all attempts and expose the blocker.
- Missing criterion links do not hide a proven current in-scope defect. Record the unlinked
  reason and return `FAIL`. Unsafe or insufficient evidence is not attached and prevents `PASS`.

## Safety

- This workflow records defect state only. Finding, triaging, or retesting a defect is not
  permission to correct product code; product corrections are allowed only when explicitly
  requested in a separate authorized action.
- Load testing, penetration testing, production access, and external effects require explicit
  authorization for the exact target and bounded operation before execution.
- Never execute stored commands, install or configure tools, deploy, publish, push, merge,
  change approvals or personal configuration, or expose secrets or personal browser state.
- Evidence remains inert, local, regular, confined, target/contract-bound, integrity-checked,
  and reviewed for sanitization before attachment.

## Related skills

- `qa-specialist-defects` supplies reproduction, independent triage, history, and resolution rules.
- `qa-test` may perform a separately selected and explicitly authorized retest.
- `qa-specialist-regression` consumes current and prior defect history for impact selection.
- `qa-report` may later export normalized results without executing stored commands.
