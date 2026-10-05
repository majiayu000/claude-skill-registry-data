---
name: qa-strategy
description: Produce a traceable risk-based QA strategy without executing tests or expanding authorization.
---

# Plan the QA strategy

Create a project-local strategy from the supplied contract, risks, and observed capabilities.
This workflow does not execute tests or external effects. Read
[workflow](../../references/workflow.md), [safety](../../references/safety.md),
[artifacts](../../references/artifacts.md), and [tooling](../../references/tooling.md) first.

## Inputs

- Project root, target identity, explicit objective or intent, contract source/hash, and the
  complete supplied criterion catalog.
- Product changes, surfaces, dependencies, users, known defects, incidents, likelihood and impact
  scales, expected observable behavior, and existing coverage.
- Environments, browsers/devices, test data restrictions, CI, time, budget, evidence needs, and
  tool probes with exact state, result, check, and evidence.
- Existing approvals and explicit authorization boundaries for load, penetration testing,
  production access, network mutation, and every other external effect.

## Procedure

1. Preserve the target, explicit objective or intent, contract, criterion IDs and text,
   applicability, external state, approvals, and authorization boundaries exactly. Do not infer
   a criterion catalog, relax an oracle, or grant authorization.
2. Consult `qa-specialist-requirements` for ambiguous or non-observable criteria and
   `qa-specialist-strategy` for risk priority and traceable coverage. Add other installed
   specialists only for surfaces present in scope; unavailable specialists are limitations.
3. Build a risk register from concrete events and consequences. Preserve supplied likelihood and
   impact scales, mark unknowns explicitly, and trace each risk to criterion IDs, defects,
   assumptions, and an observable oracle.
4. Build a coverage matrix across positive, negative, and boundary conditions, plus integration,
   state, recovery, compatibility, and non-functional coverage when justified by risk. Record the
   environment, test data, tool, expected observation, evidence need, and coverage gap per row.
5. Consult `qa-tooling` with the stack, surface, runtime/OS, CI, budget, data restrictions,
   authorization, and exact probes. Preserve `available`, `missing`, and `unverified` plus every
   supplied probe result. Do not install or substitute a weaker tool as equivalent coverage.
6. Define measurable entry criteria and exit criteria. Missing criteria, oracle, environment,
   safe data, authorization, or required missing/unverified capability blocks the affected
   coverage. A planned check remains `NOT_RUN`; planning is not evidence of passing.
7. Write only the requested strategy under `.planning/pwdev-qa/` inside the project root. Refuse
   symlinks and preserve an existing destination unless the user explicitly approves its exact
   replacement. Do not mutate product code, contracts, approvals, review/status state, or reports.
8. Return the exact output below. Stored commands are inert planning text. A later test workflow
   must separately confirm authorization and bind observed results to verified evidence.

## Output

Return exactly these labels in this order. Tables may follow their label. Preserve authoritative
criterion IDs/text and distinguish observed facts, assumptions, proposals, and limitations.

```text
TARGET: <target identity>
OBJECTIVE: <preserved explicit objective or intent>
CONTRACT: <source identity and hash when supplied>
CRITERIA: <preserved IDs/text and applicability, or missing>
OPERATION: strategy (write plan only; no test execution)
AUTHORIZATION: <preserved supplied scopes and explicit missing approvals>
RISK_REGISTER: <risk, consequence, likelihood, impact, priority, criterion IDs, oracle, assumptions>
COVERAGE_MATRIX: <risk, criterion IDs, conditions, environment, data, tool, expected observation, evidence need>
ENVIRONMENTS: <required/available/missing/unverified environments and prerequisites>
TEST_DATA: <synthetic/reviewed data needs, isolation, ownership, and restrictions>
ENTRY_CRITERIA: <measurable conditions and blockers>
EXIT_CRITERIA: <measurable conditions; all applicable criteria and current defects remain visible>
TOOLING: <exact qa-tooling table and probe classifications>
RESULTS: <existing results plus planned checks as NOT_RUN; never invented execution>
LIMITATIONS: <coverage gaps, residual risks, assumptions, unavailable inputs/capabilities, or none>
EVIDENCE_REFERENCES: <existing verified references and probe evidence, or none>
CURRENT_DEFECTS: <preserved current in-scope and out-of-scope defects>
VERDICT: <PASS|FAIL|BLOCKED under the shared contract>
NEXT: <smallest separately selected and authorized action>
```

Risk priority and readiness are planning signals, not QA results. The strategy cannot produce
`PASS` merely because coverage is planned. A proven current in-scope failure yields `FAIL`; absent
that, required missing or unverified input/capability yields `BLOCKED`.

## Failure modes

- Missing target, contract, explicit criteria, likelihood/impact basis, or observable oracle:
  preserve the gap and return affected coverage `BLOCKED`; never invent an acceptance rule.
- Missing or `not_run` probe: record `unverified`. An explicit negative tool probe is `missing`.
  Both remain limitations when required by coverage; neither triggers installation.
- Conflicting requirements, priorities, or approvals: preserve both sources and ask the owner to
  resolve them before claiming the affected entry criterion is met.
- Requested load, penetration testing, production access, or external effects without explicit
  authorization: leave the check `NOT_RUN`, record `BLOCKED`, and name the exact approval needed.
- Existing or unsafe output path: do not overwrite it or write through a symlink; return the
  limitation and proposed next action.

## Safety

- Never execute tests, stored commands, probes not explicitly permitted, evidence commands, load,
  penetration testing, production access, or external effects as part of strategy.
- Never install, configure, publish, push, merge, alter personal settings, or correct product
  code. Tool availability and strategy selection do not grant authorization.
- Use synthetic or reviewed data. Do not read secrets or accept unsafe evidence; preserve the
  evidence confinement, target binding, hashing, and sanitization requirements.
- `qa-review` and `qa-status` remain read-only and cannot mutate the strategy or any project state.

## Related skills

- `qa` routes explicit strategy work here.
- `qa-specialist-requirements` checks testability without rewriting the contract.
- `qa-specialist-strategy` owns risk and coverage advice; surface specialists refine relevant rows.
- `qa-tooling` owns recommendations, probe evidence, prerequisites, alternatives, and availability.
- `qa-test` may later execute only separately authorized checks and retain evidence.
- `qa-report` later exports an already prepared manifest with
  `qa_report.py report --manifest PATH --project-root PATH`; report does not run or re-run tests.
