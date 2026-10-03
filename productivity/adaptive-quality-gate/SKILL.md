---
name: adaptive-quality-gate
description: Use when work produces a deliverable, factual claim, dataset, code change, decision, publication, deployment, automation, or irreversible action whose failure would matter; when the user asks for a quality gate, acceptance criteria, QA, completeness, validation, audit, evidence, preflight, release readiness, or a definition of done; or before claiming completion on medium- or high-risk work. Automatically decide whether a formal gate is warranted, derive task-specific pass/fail criteria, gather evidence, and block unsupported completion. Make sure to use this skill even when the user does not say "quality gate" if consequential work needs acceptance criteria or completion evidence. Skip formal gating for trivial, reversible, low-impact requests.
---

# Adaptive Quality Gate

Set quality gates from the task's outcome and risk. Do not reuse a domain
checklist merely because it worked for a previous scraping, SEO, coding, or
content task.

## Core Contract

A gate is a decision rule backed by evidence. It is not a reminder to "check
quality."

For every material criterion, define:

- **Criterion**: the property that must be true.
- **Threshold**: the observable boundary between pass and fail.
- **Method**: how the property will be tested.
- **Evidence**: the artifact or result that proves the test ran.
- **Severity**: hard gate or advisory gate.
- **Failure action**: hold, repair and retest, request a decision, or accept a
  documented exception.

Apply gates before irreversible actions and before making a completion,
readiness, safety, or quality claim. Never convert missing evidence into a
pass.

## 1. Decide The Gate Level

Assess four factors:

- **Impact**: what happens if the result is wrong or incomplete?
- **Reversibility**: how easily can the action or artifact be corrected?
- **Uncertainty**: how much is unknown about inputs, requirements, or tools?
- **Exposure**: is the result private and provisional, or external,
  production-facing, regulated, or decision-driving?

Choose the smallest gate level that controls the material risk:

| Level | Use when | Typical gate size |
| --- | --- | --- |
| None | Trivial, easily reversible work with an obvious result | No formal table; perform a basic sanity check |
| Light | Low-impact deliverable with limited uncertainty | 1-3 focused checks |
| Standard | Material deliverable, multi-step workflow, or consequential claim | 3-6 hard or advisory gates |
| Strict | High-stakes, destructive, production, regulated, security-sensitive, or hard-to-reverse work | 5-8 gates plus independent or stronger verification where feasible |

For a `Standard` or `Strict` gate, state one concise sentence connecting the
chosen level to the material impact, reversibility, uncertainty, or exposure.
Do not expose a synthetic numeric risk score unless the task already has an
approved scoring model.

Use a formal gate when at least one of these is present:

- An external or decision-driving deliverable
- A factual, quantitative, completeness, freshness, or provenance claim
- A code, configuration, migration, release, or production change
- A destructive or difficult-to-reverse operation
- A multi-source data collection or transformation workflow
- Legal, medical, financial, privacy, security, or policy consequences
- An explicit request for QA, validation, acceptance criteria, audit, or a
  quality gate

Do not create gate theater for a simple explanation, brainstorming pass,
clearly provisional draft, or tiny reversible formatting change. State that a
formal gate is unnecessary when that decision is useful; otherwise just do the
sanity check.

## 2. Build The Task Contract

Before selecting checks, identify:

- Intended outcome and artifact
- Consumer or downstream action
- Explicit constraints and user-supplied acceptance criteria
- Material failure modes
- Unknowns and unavailable evidence
- The exact claim that would justify saying "done"

Use explicit requirements, specifications, policies, contracts, and user
constraints as the primary source of thresholds. Ask a concise question only
when the answer would materially change a hard threshold or authorize a risky
action. Otherwise, use a provisional gate and label the assumption.

## 3. Derive Task-Specific Gates

Select only dimensions that can change the release decision:

- **Correctness**: values, logic, calculations, or behavior match the source of
  truth.
- **Completeness**: required scope is covered against a defined denominator or
  inventory.
- **Evidence and provenance**: important claims trace to current, relevant
  sources or execution artifacts.
- **Functional behavior**: the artifact works in the target environment and
  important paths pass.
- **Safety and compliance**: destructive, security, privacy, legal, or policy
  constraints are respected.
- **Operational readiness**: backup, rollback, observability, ownership, and
  failure handling are adequate.
- **Usability and format**: the consumer can read, open, navigate, or act on the
  result as intended.
- **Freshness**: time-sensitive inputs and conclusions are current enough for
  the decision.

Do not automatically use every dimension. A gate that cannot affect acceptance
adds noise and weakens attention to the real risks.

### Threshold Rules

Prefer thresholds in this order:

1. Explicit user requirement, contract, policy, or specification
2. Deterministic test, schema, reference artifact, or authoritative source
3. Established project baseline, service level, or historical control limit
4. A clearly labeled provisional qualitative criterion with human review

Do not invent a percentage, sample size, zero-defect promise, or coverage
denominator. If the population is unknown, gate the inventory method and source
coverage instead of claiming an unsupported completeness percentage.

## 4. Place Gates At Decision Boundaries

Use gates where a failure can still change the action:

- **Entry gate**: inputs, scope, permissions, and prerequisites are sufficient.
- **Process gate**: intermediate results reveal drift before expensive work
  continues.
- **Release gate**: final evidence supports delivery, publication, deployment,
  deletion, or a completion claim.

Most tasks need only a release gate. Add entry or process gates when later
rework would be expensive, destructive, or misleading.

Mark each criterion as:

- **Hard**: failure blocks the action or completion claim.
- **Advisory**: failure is disclosed but may be accepted without misrepresenting
  the result.

## 5. Execute And Record Evidence

Use the strongest relevant validator already available in the environment:
tests, parsers, schema checks, static analysis, visual inspection, source
reconciliation, dry runs, checksums, sampling, or independent review.

For each result, record one status:

- `PASS`: current evidence meets the threshold.
- `PASS WITH EXCEPTION`: the threshold is missed but an authorized, documented
  exception permits release.
- `FAIL`: evidence shows the threshold is not met.
- `BLOCKED`: a prerequisite or external dependency prevents evaluation or
  repair.
- `NOT EVALUATED`: required evidence is unavailable or the check did not run.
- `NOT APPLICABLE`: the dimension does not apply, with a short reason when not
  obvious.

Use these overall decisions:

- `RELEASE`: all hard gates pass.
- `RELEASE WITH EXCEPTIONS`: hard-gate exceptions are explicit, authorized, and
  traceable.
- `HOLD`: any hard gate fails, remains blocked, or is not evaluated without an
  accepted risk decision.

An exit code, file existence check, or confident narrative is not sufficient
evidence unless it directly tests the criterion. Verify the actual artifact and
the important claims it contains.

## 6. Adapt During The Task

Revise the gate contract when scope, inputs, implementation, or risk changes.
Do not silently lower a threshold to make the result pass. Record:

- What changed
- Why the existing gate no longer fits
- Who or what authorized the new threshold
- Which evidence must be rerun

When evidence is insufficient, report known facts, candidate hypotheses,
verification paths, and temporary mitigation. Mark unverified conclusions.

## Reporting

Keep the report proportional to the task. For standard or strict gates, use:

```markdown
Gate level: <Light | Standard | Strict>
Decision: <RELEASE | RELEASE WITH EXCEPTIONS | HOLD>

| Gate | Severity | Threshold | Method and evidence | Status |
| --- | --- | --- | --- | --- |
| ... | Hard/Advisory | ... | ... | ... |

Gaps or exceptions:
- ...

Next action:
- ...
```

For a light gate, a short checklist or one-sentence decision is enough. Do not
make the gate report larger than the deliverable it protects.

## Anti-Patterns

- Reusing one fixed checklist for unrelated tasks
- Measuring what is easy instead of what controls acceptance
- Claiming completeness without a defined denominator
- Treating missing, stale, or indirect evidence as a pass
- Inventing numeric thresholds to make a gate look objective
- Running every available validator regardless of relevance
- Allowing an advisory issue to silently become a hard failure, or vice versa
- Declaring success before the release gate has run

This skill orchestrates quality decisions; it does not replace domain expertise
or domain-specific validators. Use relevant tools and skills to produce the
evidence, then apply this gate contract to decide whether the result can ship.
