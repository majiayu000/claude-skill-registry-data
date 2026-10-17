---
name: cross-framework-audit-synthesis
description: Synthesizes accessibility, Universal Design, usability, Nielsen heuristic, and Norman interaction review outputs into one evidence-based audit report and dependency-aware remediation backlog. Use when specialist audit findings must be contract-validated, deduplicated by root cause, reconciled without losing valid framework mappings, separated by evidence status, prioritized across critical user flows, or converted into a unified verification plan.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository or audit-artifact access. Requires the shared finding contract from inclusive-interface-audit-orchestrator to claim contract-valid synthesis.
metadata:
  category: research-synthesis
  task_type: research
  audience: accessibility-ux-product-and-engineering-teams
  tags:
    - accessibility
    - wcag
    - universal-design
    - usability
    - nielsen-heuristics
    - norman-principles
    - audit-synthesis
    - evidence
    - remediation-backlog
  status: draft
  side_effects: none
---

# Cross-Framework Audit Synthesis

## Purpose

Combine specialist accessibility, Universal Design, usability, Nielsen heuristic, and Norman interaction findings into one traceable audit report. Validate every source finding, consolidate repeated symptoms only when they share a root cause, preserve every supported framework mapping, expose disagreement, and produce a prioritized remediation and verification plan without multiplying issue counts by framework.

This skill synthesizes completed review outputs. It does not perform the missing specialist audits, change the audited interface, certify WCAG conformance, or silently repair incomplete evidence.

## When to use this skill

Use this skill when:

- Several specialist reviews cover the same interface, component, flow, state, or user problem.
- Accessibility conformance evidence must be reported separately from heuristic or inclusive-design observations.
- Duplicate findings must be merged without losing source traceability, occurrences, affected users, or valid mappings.
- Audit results must be organized into critical-flow risks, remediation phases, unresolved tests, and closure evidence.
- Conflicting root-cause claims, statuses, severities, mappings, or recommendations need explicit adjudication.
- Stakeholders need one issue count and backlog rather than a sum of framework observations.

Do not use this skill when:

- No specialist outputs or evidence are available.
- The task is to plan which audits to run; use `inclusive-interface-audit-orchestrator`.
- The user wants a narrow WCAG evidence map or one specialist review only.
- The user expects legal advice, certification, or an unqualified conformance claim.
- The request is to implement fixes rather than synthesize evidence.

## Inputs to inspect

Inspect the smallest complete evidence set:

- The `inclusive-interface-audit-orchestrator` output and its shared finding contract.
- Every specialist report, including source skill, audit date, target version, scope, exclusions, sample, methods, and environment.
- Finding-level evidence references such as URLs, routes, component or story IDs, states, screenshots, recordings, code locations, tool output, test logs, and manual notes.
- Critical user flows, task criticality, affected user groups, roles, platforms, locales, breakpoints, and supported assistive-technology combinations.
- Existing issue IDs, accepted-risk decisions, remediation owners, dependencies, and prior closure evidence.
- The named WCAG version and level, plus any versions or labels used for Universal Design, Nielsen, Norman, or organizational frameworks.

Do not infer a pass from silence. Do not treat missing evidence as evidence of absence.

## Non-negotiable synthesis rules

- Keep one canonical finding per distinct root problem, not one finding per framework mapping or specialist.
- Preserve original source records and IDs even when a normalized finding supersedes them for reporting.
- Preserve every valid WCAG criterion, Universal Design principle, Nielsen heuristic, Norman concept, and local-policy mapping with its rationale and evidence references.
- Keep WCAG criterion results separate from heuristic and inclusive-design observations.
- Do not convert a heuristic observation into a WCAG failure without criterion-specific conformance evidence.
- Do not convert a WCAG failure into violations of every concept that could describe the symptom.
- Keep unsupported mappings in the conflict ledger, not in the validated mapping set.
- Base severity and priority on user and task risk, not on the number of framework mappings or the WCAG conformance level.
- Never let `accepted-risk` erase the evidence status or remove the finding from traceability.
- Never silently choose between conflicting specialist conclusions.

## Workflow

### 1. Establish synthesis scope

1. Record the target version, audit period, requested frameworks, in-scope and out-of-scope surfaces, representative sample, critical flows, and decision the synthesis must support.
2. Record each source report's scope, method, date, environment, evidence limits, and known omissions.
3. Create stable source IDs for reports and evidence artifacts without rewriting their original finding IDs.
4. Mark stale, mismatched, partial, or inaccessible inputs before using them.

### 2. Validate the shared finding contract

Read the shared finding contract from `inclusive-interface-audit-orchestrator` before normalizing any finding. Treat that contract as authoritative when it differs from this skill's summary.

At minimum, require each incoming finding to contain:

| Field | Validation |
|---|---|
| `id` | Present and unique within its source |
| `target` | Identifies the relevant route, component, flow, state, role, environment, and occurrence |
| `evidence` | States evidence type, method, reference, environment, and reproducible observation |
| `user_impact` | Identifies affected users, task effect, consequence, and workaround |
| `status` | One of `confirmed`, `provisional`, `needs-validation`, `not-reproduced`, `resolved`, or `accepted-risk` |
| `severity` | One of `critical`, `high`, `medium`, `low`, or `advisory`, with user-impact rationale |
| `confidence` | One of `high`, `medium`, or `low`, with reason and missing evidence |
| `framework_mappings` | Contains zero or more mappings with framework, identifier, label or version when supplied, rationale, and evidence |
| `recommendation` | Describes the desired outcome, constraints, and responsible surface |
| `verification` | Defines retest steps, expected result, method, environment, and closure evidence |

Allow `source_skill`, `related_ids`, and `root_cause` when present.

Create an intake result for every source finding:

- `valid`: satisfies the contract and is supported by its cited evidence.
- `normalizable`: can satisfy the contract through lossless formatting, explicit field mapping, or added source traceability.
- `invalid`: lacks information required to interpret the claim safely.
- `conflicting`: contains internally inconsistent fields or contradicts another supported finding.

Do not invent missing evidence, affected users, mappings, or test results. Log every normalization. If the orchestrator contract is unavailable, return an intake-gap report or a clearly labeled provisional synthesis; never call the output contract-valid.

### 3. Normalize evidence disposition

Preserve the source `status`, `confidence`, and lifecycle decision. Add one mutually exclusive `synthesis_disposition`:

| Disposition | Use when |
|---|---|
| `confirmed` | Reproducible direct evidence establishes the scoped problem or result in the named environment |
| `probable` | Credible implementation, prior-audit, or indirect evidence supports the claim, but decisive reproduction is incomplete |
| `unverified` | Evidence is missing, stale, contradictory, out of scope, or too weak to support the claim |
| `not-applicable` | The criterion or lens genuinely does not apply to the scoped target, with a recorded rationale |
| `manual-test` | The claim cannot be resolved from current artifacts and requires a named expert, browser, device, input, or assistive-technology test |

Apply these rules:

- Usually map source `confirmed` to `confirmed` only after its evidence passes validation.
- Usually map `provisional` to `probable`.
- Map `needs-validation` to `manual-test` when a concrete manual method is required; otherwise use `unverified`.
- Map `not-reproduced` to `unverified` unless retained evidence proves a version-specific historical defect.
- Treat `resolved` as a lifecycle state. Confirm closure only when retest evidence meets the original verification requirement.
- Treat `accepted-risk` as a product decision. Preserve the independently supported evidence disposition.
- Use `not-applicable` only for scoped coverage accounting. Do not count it as an issue or place it in the remediation backlog.
- Move a `manual-test` item to another disposition only after recording the test environment, method, result, and evidence.

Normalize common specialist result labels without losing their originals:

| Specialist result | Synthesis treatment |
|---|---|
| Confirmed failure or evidence-backed defect | `confirmed` active finding |
| Probable issue or provisional concern | `probable` active finding |
| Unavailable evidence or unsupported claim | `unverified` evidence-gap record |
| Manual-test requirement or not-verifiable behavior | `manual-test` record with an executable method |
| Not applicable | `not-applicable` coverage record |
| Scoped pass | WCAG or coverage result, not an active finding or issue count |
| Heuristic strength | Framework observation to preserve, not an active issue unless it is part of a mixed finding |

### 4. Separate conformance results from observations

For each canonical finding, maintain distinct mapping collections:

- `wcag_results`: criterion, WCAG version, level when relevant, applicability, result, evidence, and rationale.
- `universal_design_observations`: principle, observation, rationale, and evidence.
- `nielsen_observations`: heuristic, observation, rationale, and evidence.
- `norman_observations`: concept, observation, rationale, and evidence.
- `other_inclusive_design_observations`: named framework or local policy, observation, rationale, and evidence.

Use WCAG results such as `fail`, `pass`, `inconclusive`, `not-tested`, or `not-applicable` only at criterion-and-scope level. A `pass` requires affirmative evidence for the tested scope; an absent failure is not a pass.

Use heuristic observations such as `concern`, `strength`, `mixed`, `not-observed`, or `not-applicable`. Heuristic results provide design insight, not conformance status.

Deduplicate identical mapping tuples, but retain all distinct rationales, evidence references, versions, scopes, and source IDs.

### 5. Build candidate root-cause clusters

Group source findings into a candidate cluster only when they refer to:

1. The same user-observable symptom or task consequence.
2. The same target behavior and relevant state.
3. The same supported root cause.
4. The same remediation locus and materially compatible verification method.

Merge the cluster into one canonical finding when all four conditions hold. Preserve:

- Every source report and source finding ID.
- Every occurrence, target, state, user group, and affected flow.
- Every valid mapping and rationale.
- The strongest reproducible evidence and all material evidence limits.
- Minority severity, status, root-cause, or recommendation views as conflicts when they remain supported.

Do not merge findings merely because they share a WCAG criterion, heuristic, screen, component, severity, or recommendation wording. Keep findings separate when causes, fixes, owners, dependencies, or verification methods differ. When the root cause is only suspected, link the findings with a `candidate_cluster_id` and keep separate issue counts until confirmed.

Name canonical findings for the user-facing problem and root cause, not for a framework label.

### 6. Detect and adjudicate disagreement

Create a conflict record when specialists disagree about:

- Whether a finding exists, reproduces, or has been resolved.
- The affected target, state, user group, flow, or environment.
- The root cause or whether two findings are duplicates.
- Severity, confidence, user impact, workaround, reach, or task criticality.
- A WCAG, Universal Design, Nielsen, Norman, or local-policy mapping.
- The remediation outcome, owner, dependency, or verification method.

Resolve a conflict only when the evidence supports a documented decision rule. Never resolve by majority vote, source prestige alone, or the most severe phrasing. Otherwise preserve both positions, set the canonical disposition no stronger than the evidence permits, and add a targeted unresolved test.

Record unsupported findings separately with the missing contract field, unsupported claim, evidence gap, consequence for synthesis, and required next step. Do not delete them or mix them into confirmed totals.

### 7. Prioritize validated canonical findings

Score each active canonical finding from 0 to 4 on:

| Factor | 0 | 2 | 4 |
|---|---|---|---|
| User impact (`I`) | No demonstrated task effect | Material friction or degraded access | Exclusion, serious harm, unsafe or irreversible outcome |
| Likelihood (`L`) | Not expected in supported use | Plausible or intermittent | Reproducible or expected in ordinary use |
| Task criticality (`C`) | Optional or decorative | Important but recoverable | Essential, regulated, safety-sensitive, financial, or irreversible |
| Reach (`R`) | One rare occurrence | Several users, states, or components | Shared pattern affecting many users, flows, or surfaces |
| Remediation dependency (`D`) | Independent leaf fix | Some sequencing value | Foundational fix that blocks or unlocks several remediations |

Use `priority_score = 2I + L + 2C + R + D` and retain the factor evidence beside the score.

Assign:

- `P0` for 23–28 when impact and criticality are each at least 3 and the disposition is `confirmed` or `probable`.
- `P1` for 17–22.
- `P2` for 10–16.
- `P3` for 1–9.
- `P4` for zero-impact advisory strengths, documentation notes, or inactive historical records.

Use the score as a transparent sorting aid, not a substitute for judgment. Elevate or lower at most one band for a documented safety, legal-policy, workaround, or dependency reason.

Do not put `not-applicable` records in the backlog. Give `unverified` and `manual-test` records a test urgency based on the same factors, but do not present their provisional score as a confirmed remediation priority. Keep `probable` remediation explicitly provisional when validation could materially change the fix.

### 8. Build dependency-aware remediation phases

Organize work into:

1. **Evidence closure and containment:** Resolve conflicts and high-urgency manual tests; add temporary safeguards where credible severe harm may continue.
2. **Critical-flow restoration:** Fix confirmed or probable P0/P1 barriers in essential tasks, beginning with prerequisites.
3. **Shared foundations:** Correct root causes, primitives, content patterns, or design-system behavior that unlock multiple dependent findings.
4. **Broad interaction and inclusion improvements:** Address remaining P1/P2 accessibility, Universal Design, usability, Nielsen, and Norman concerns.
5. **Lower-risk polish and documentation:** Address P3/P4 issues without delaying higher-impact work.
6. **Regression and closure:** Run canonical verification, affected-flow regression, criterion-specific checks, and cross-framework acceptance review.

Allow independent phases to overlap only when their dependencies, target files or surfaces, evidence environments, and acceptance gates do not conflict. Give each phase entry criteria, exit criteria, findings, owners when known, dependencies, verification evidence, and residual risk.

### 9. Design the verification plan

For every active canonical finding:

- Define an observable acceptance result tied to the root cause and affected user task.
- Reuse the strongest applicable source verification requirement.
- Cover every merged occurrence or define a justified representative regression sample and expansion trigger.
- Separate automated, expert manual, assistive-technology, participant, design-review, and documentation checks.
- Name the environment, browser, platform, device, viewport, zoom, input, role, locale, state, data, and assistive technology when relevant.
- Recheck every retained framework mapping; closing one mapping does not automatically prove all others.
- Require retained evidence and a closure decision of `resolved`, `partially-resolved`, `not-resolved`, or `accepted-risk`.
- Return changed or failed behavior to the ledger as new evidence rather than erasing the previous result.

## Output format

Return the synthesis using this structure:

```md
# Cross-Framework Audit Synthesis

## Executive summary

- Target, version, scope, and audit period:
- Decision supported:
- Canonical active findings by disposition:
- Source observations / canonical findings / valid mappings:
- Highest critical-flow risks:
- Cross-cutting root causes:
- Evidence confidence and major limitations:
- Conformance disclaimer:

## Intake and contract validation

| Source | Scope and method | Findings received | Valid | Normalizable | Invalid | Conflicting | Evidence limitations |
|---|---|---:|---:|---:|---:|---:|---|

## Consolidated finding ledger

| Canonical ID | Problem and root cause | Occurrences and affected flows | Users and impact | Disposition | Evidence | WCAG results | UD / Nielsen / Norman observations | I/L/C/R/D | Priority | Phase | Source IDs |
|---|---|---|---|---|---|---|---|---|---|---|---|

## Critical-flow risks

| Flow and step | Users | Canonical findings | Disposition | Worst credible consequence | Workaround or containment | Required decision |
|---|---|---|---|---|---|---|

## Framework coverage

### WCAG conformance results

| Criterion and scope | Result | Evidence | Canonical findings | Remaining test |
|---|---|---|---|---|

### Heuristic and inclusive-design observations

| Framework and principle or heuristic | Observation | Evidence | Canonical findings | Design implication |
|---|---|---|---|---|

## Conflicts and unsupported findings

| Conflict ID | Sources or findings | Disagreement or unsupported claim | Evidence on each side | Synthesis treatment | Resolution test or decision |
|---|---|---|---|---|---|

## Remediation phases

### Phase N — Name

- Entry criteria:
- Canonical findings:
- Dependencies:
- Remediation outcomes:
- Owner or responsible surface:
- Verification and exit criteria:
- Residual risk:

## Unresolved tests

| Test ID | Related findings | Question | Urgency factors | Method and environment | Expected evidence | Blocking decision |
|---|---|---|---|---|---|---|

## Verification plan

| Canonical finding | Acceptance result | Method | Coverage and environment | Evidence to retain | Regression scope | Closure gate |
|---|---|---|---|---|---|---|

## Count reconciliation and limitations

- Source finding count:
- Canonical active finding count:
- Duplicate observations merged:
- Candidate clusters not merged:
- Valid framework mapping count:
- Not-applicable coverage records:
- Invalid or unsupported source findings:
- Untested scope and remaining uncertainty:
```

Count canonical active findings once. Report source observations, occurrences, mappings, conflicts, inactive resolved records, and not-applicable coverage separately.

## Quality bar

The task is complete only when:

- Every input finding has a contract-validation result and source traceability.
- Every canonical finding has one evidence disposition and preserves the original source status.
- Confirmed, probable, unverified, not-applicable, and manual-test records are separated.
- WCAG criterion results are separate from heuristic and inclusive-design observations.
- Duplicate findings are merged only with supported root-cause and remediation equivalence.
- Every valid WCAG, Universal Design, Nielsen, Norman, and local-policy mapping is retained with rationale.
- Conflicting and unsupported specialist findings are visible and have a resolution path.
- Issue totals count canonical findings rather than framework mappings.
- Priority records user impact, likelihood, task criticality, reach, remediation dependency, and supporting evidence.
- Critical-flow risks, remediation phases, unresolved tests, and a finding-level verification plan are present.
- No unsupported pass, compliance, certification, or universal user-experience claim is made.

## Edge cases

- **Contract unavailable:** Return a contract dependency failure and intake gaps. Produce only a labeled provisional synthesis if the user explicitly wants one.
- **Mixed audit dates or product versions:** Do not merge across versions without compatibility evidence. Preserve historical findings separately.
- **Framework version omitted:** Preserve the mapping text, mark the version gap, and avoid version-specific conclusions.
- **One symptom, unknown cause:** Link candidate duplicates but keep separate canonical IDs and counts.
- **One cause, several symptoms:** Merge only when one remediation and verification plan covers the materially distinct impacts; otherwise use related canonical findings under one root-cause theme.
- **One criterion, several independent failures:** Keep separate canonical findings.
- **Heuristic strength and WCAG failure coexist:** Preserve both without treating the strength as a conformance pass or the failure as proof that every heuristic is violated.
- **Accepted risk:** Keep the issue, evidence, decision owner, rationale, review date, expiry or revisit trigger, and residual impact visible.
- **Resolved source finding:** Require closure evidence and regression scope before excluding it from the active backlog.
- **Representative samples:** State what the sample represents, what remains untested, and what triggers sample expansion.
- **User research absent:** Do not present expert review as proof of lived experience.

## Related skills

- `inclusive-interface-audit-orchestrator`
- `inclusive-task-flow-review`
- `universal-design-interface-review`
- `norman-interaction-principles-review`
- `semantic-structure-accessibility-audit`
- `forms-errors-accessibility-audit`
- `accessibility-validation-planner`
- `wcag-evidence-mapper`
- `interface-state-coverage-review`
