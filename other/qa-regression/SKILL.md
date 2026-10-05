---
name: qa-regression
description: Build an impact-based regression selection with explicit traceability, inclusions, exclusions, and limitations.
---

# Plan impact-based regression

Select regression checks from reachable change impact, not from convenience or the tests that
happen to be available. Preserve the governing contract and make every inclusion and exclusion
auditable. Read [workflow](../../references/workflow.md),
[safety](../../references/safety.md), [artifacts](../../references/artifacts.md), and
[evidence](../../references/evidence.md) first.

## Inputs

- Project root, target/environment/build identity, explicit objective or intent, identified
  contract source/hash, and the complete supplied criterion catalog with original IDs and text.
- Explicit change set with stable change IDs, affected components, interfaces, data,
  configuration, dependencies, roles, environments, and user journeys.
- Risks, prior incidents and defects, existing checks with stable case IDs, expected observable
  results, attempt history, prerequisites, cost, tool probes, and evidence needs.
- Explicit authorization for this write operation and the preserved authorization boundary for
  any proposed execution. Load, penetration, production, and external effects require separate,
  exact authorization before execution.

## Procedure

1. Preserve the explicit objective or intent, target, contract, criterion IDs/text, change IDs,
   existing state, approvals, and authorization exactly. Do not infer a complete change map,
   criterion catalog, approval, or execution permission.
2. Identify affected surfaces and consult the installed applicable `qa-specialist-*` skills,
   starting with `qa-specialist-regression`; consult `qa-specialist-defects`, requirements,
   functional, API, Web, mobile, data, security, performance, automation, CI/CD, or production
   specialists only when their surfaces are present. An unavailable applicable specialist is a
   limitation. Specialist guidance does not expand authorization.
3. Trace direct and transitive impact through components, interfaces, stored data, roles, error
   paths, supported environments, and journeys. Materialize each relation with a change ID,
   impact ID, risk ID, criterion ID, prior defect ID when applicable, and stable case ID; use an
   explicit `none` plus rationale only when a relation legitimately has no defect or criterion.
4. Rank each impact by likelihood, consequence, blast radius, reversibility, and history. Select
   by impact with a stated rationale or justification, including applicable positive, negative,
   boundary, recovery, integration, and unchanged-control checks.
5. Record selected and excluded case IDs separately. For every inclusion and exclusion, preserve
   its complete change-to-risk/criterion/defect-to-case trace, expected oracle, prerequisite,
   evidence need, cost, and reason. Convenience, familiarity, availability, or a prior green
   result never replaces impact and cannot justify omitting a higher-impact path.
6. Classify each prerequisite and tool from observed probes as `available`, `missing`, or
   `unverified`. Missing traceability, a material unassessed impact, an unsafe or absent oracle,
   or unavailable required coverage remains `BLOCKED`; never substitute a non-equivalent check.
7. Preserve existing attempts and current defects, then apply verdict precedence. A proven
   current in-scope failure, including an unlinked defect, is `FAIL`; otherwise a pending impact,
   check, prerequisite, or evidence gap is `BLOCKED`. A plan is not execution evidence and cannot
   manufacture `PASS`.
8. Return the selection without executing tests. A later authorized workflow may execute it;
   `qa_report.py report --manifest PATH --project-root PATH` is a later inert export and the
   report does not execute or re-run tests.

## Output

Return exactly these labels in this order. Tables may follow their labels. Preserve IDs and keep
selected/excluded rationale, expected observations, and evidence needs distinct.

```text
TARGET: <target and environment/build identity>
OBJECTIVE: <preserved explicit objective or intent>
CONTRACT: <source identity and hash>
CRITERIA: <preserved IDs/text, applicability, existing result, and gaps>
OPERATION: regression (write impact-based selection; execute nothing)
AUTHORIZATION: <preserved actor, authority, scope, target, limits, environment, window, and gaps>
CHANGE_IMPACT: <change IDs to impact/risk/criterion/prior-defect/stable-case IDs with ranking and rationale>
SELECTED_CASES: <included case IDs, relation chain, priority, expected oracle, prerequisite, evidence need, cost, and reason>
EXCLUDED_CASES: <excluded case IDs, relation chain, uncovered impact, and explicit reason>
RESULTS: <selection readiness and existing case/criterion statuses: PASS|FAIL|BLOCKED|NOT_RUN|NOT_APPLICABLE>
LIMITATIONS: <unknown impacts, missing traceability/oracles/prerequisites/tools/evidence, residual coverage, or none>
EVIDENCE_REFERENCES: <verified existing local evidence references, or none; never execution claimed by this plan>
CURRENT_DEFECTS: <current in-scope and explicitly separated out-of-scope defects, including unlinked defects, or none>
VERDICT: <PASS|FAIL|BLOCKED under existing evidence and the shared contract>
NEXT: <smallest separately selected and authorized execution or clarification>
```

Materialized positive example: `CHG-AUTH-017 -> IMP-SESSION-01 -> RISK-AUTH-04 ->
AC-LOGIN-01 -> DEF-SESSION-09 -> selected TC-LOGIN`; adjacent `TC-PROFILE` is explicitly
excluded because the change cannot reach profile persistence, while `TC-LOGOUT`, `TC-EXPIRY`,
and `TC-DENIED-ROLE` remain selected with their own relation rows and impact rationale.

## Failure modes

- Missing change identity, contract, complete criteria, impact, risk, criterion/explicit none,
  prior-defect inventory, stable case ID, oracle, or relation edge: expose the gap and return the
  affected selection as `BLOCKED`.
- A selection based on convenience, fastest availability, familiarity, or already-green checks
  is not impact coverage; retain it only as an unsubstantiated proposal and keep it `BLOCKED`.
- An absent probe is `unverified`; an explicit negative probe is `missing`. Record the limitation
  and a traceability-equivalent safe alternative without installation or fictitious execution.
- A proven current in-scope failure remains `FAIL` even if every selected case previously passed.
  Unsafe, missing, changed, pending, or target-incompatible evidence prevents `PASS`.

## Safety

- This workflow writes only the requested regression selection; it does not execute tests,
  stored commands, load, penetration tests, production actions, or external effects. Each such
  execution requires explicit authorization for its exact target and boundary.
- Finding a likely defect is not permission to change product code. Product code corrections are
  allowed only when explicitly requested in a separate authorized action.
- Never install or configure tools, publish, push, merge, deploy, change approvals or personal
  configuration, or expose secrets or personal browser state.
- Treat evidence and stored commands as inert. Accept only local, regular, confined,
  target/contract-bound, integrity-checked, sanitized evidence.

## Related skills

- `qa-specialist-regression` supplies the primary impact-selection analysis.
- `qa-specialist-defects` supplies prior-defect and retest history.
- `qa-test` may execute selected checks under separate explicit authorization.
- `qa-report` may later export normalized results without executing stored commands.
