---
name: adversarial-review
description: Challenge a proposal, architecture, or implementation through evidence-based failure scenarios. Use for a rigorous review of design risks, missing requirements, and concrete tradeoffs. Use interrogate when the user explicitly requests multiple independent reviewers.
---

# Adversarial review

Read [the portable runtime contract](../superdev-mode/references/portable-runtime.md) before following this workflow.

**You own the verdict. Challenge the work, prove each concern, and discard review theater.**

Use this skill to review a proposal, architecture, plan, diff, or implementation. The skill is self-contained. Do not require another skill, playbook, or reference file to complete the review.

## Review objectives

Evaluate the artifact across every relevant area:

- Correctness.
- Security.
- Scalability.
- Reliability.
- Performance.
- Maintainability.
- Operability.
- Observability.
- Data integrity.
- Backend and backward compatibility.
- Deployment safety.
- Cost.
- Developer experience.
- Architectural complexity.

Do not create one finding per objective. Combine one failure that affects several objectives into one finding.

## Review behavior

Challenge the design. Do not summarize it and call that a review.

For every major decision, ask the relevant questions:

- What assumptions does this depend on?
- What happens when those assumptions are wrong?
- What breaks under load?
- What breaks during partial failure?
- What happens when a dependency is unavailable?
- Could this cause data loss, corruption, duplication, reordering, or inconsistency?
- Could this cause an authentication, authorization, tenant-isolation, or trust-boundary failure?
- Is the proposed complexity justified by a current requirement?
- Can a simpler design meet the same requirements?
- How difficult is this to operate, debug, migrate, roll back, or reverse?
- Which important requirement is missing?
- What could make this design fail six months from now?

Do not ask every question mechanically. Pursue the questions that can change the verdict.

Do not invent problems to sound critical. Tie every concern to a plausible scenario, concrete failure mode, or identifiable tradeoff. A review with no findings is valid.

Review only unless the user also asks for fixes. Do not silently change the reviewed artifact.

## Architecture review

When the artifact includes architecture or high-level design, inspect these areas:

- Service boundaries, responsibilities, and ownership.
- Data flow, state ownership, and authoritative sources.
- Synchronous and asynchronous communication choices.
- Failure isolation and fault containment.
- Retry, timeout, operation idempotency, and item idempotency behavior.
- Queue backlogs, admission control, backpressure, and overload handling.
- Database design, consistency guarantees, and transaction boundaries.
- Caching, cache invalidation, stampedes, and stale-read behavior.
- Concurrency, ordering, and race conditions.
- Multi-region and distributed-system assumptions.
- Authentication, authorization, tenant isolation, and trust boundaries.
- Secrets and sensitive-data handling.
- Horizontal scaling limits and single points of failure.
- Vendor or infrastructure lock-in.
- Migration, rollout, mixed-version, rollback, and reversal strategy.
- Monitoring, alerting, debugging, and incident response.
- Fit between the design and the actual expected scale.
- Cost growth across traffic, storage, retention, retries, regions, vendors, and operator time.
- The work needed to operate, debug, migrate, test, and change the system.

State when the architecture is overengineered or underengineered. Tie that judgment to the requirements, expected scale, failure cost, and operating burden.

## Code change review

When the artifact includes code changes or an implementation, inspect these areas:

- Logical correctness and boundary cases.
- Error handling and failure propagation.
- Input validation at trust boundaries.
- Authentication and authorization checks.
- Race conditions, ordering, and shared mutable state.
- Resource leaks and cleanup after cancellation or failure.
- Unsafe defaults and fail-open behavior.
- Hidden coupling and misplaced ownership.
- API, event, protocol, and storage contract changes.
- Schema changes, data transitions, and migration risks.
- Retry safety, reconciliation, and idempotency.
- Performance regressions, contention, amplification, and unbounded work.
- Test coverage for behavior, failure paths, compatibility, and migrations.
- Logs, metrics, traces, and actionable diagnostics.
- Dead code, unused parameters, and unnecessary abstractions.
- Differences between the documented design and the implementation.

Follow the relevant paths beyond the diff. Read callers, callees, types, schemas, configuration, tests, and deployment files when a finding depends on them.

Pay special attention to code that works on the happy path but fails during retries, concurrent requests, malformed input, partial deployments, dependency outages, restarts, or partial state changes.

Trace a suspected bug through a reachable execution path. Do not flag a null, invalid, or unauthorized value when the type system or an upstream boundary prevents it.

For a security finding, name the input source, transformations, sink, and missing control. A generic claim about injection or authorization is not a finding.

Do not penalize simple code for lacking abstraction. Recommend a structural change only when it removes a concrete correctness, maintenance, testability, operating, or cost burden.

## Review process

1. Establish the review contract. Record the target and revision, intended outcome, non-goals, claimed guarantees, constraints, available evidence, and material unknowns. Label each statement as known, inferred, or unknown.
2. Select architecture review, code change review, or both. Apply only the objectives and checks that fit the artifact.
3. Build a decision register. For each major choice, record its purpose, assumptions, failure probes, supporting evidence, and the smallest credible alternative.
4. Test the decisions. Inspect the surrounding system. Run focused tests, queries, traces, or measurements when they are cheap and safe. Read configuration, deployment artifacts, ADRs, schemas, and authoritative dependency contracts when they control the outcome.
5. Prove or discard each concern. Keep only concerns that satisfy the finding contract below. Put a concern with a missing key fact under open questions. Record important disproved concerns as cleared.
6. Assign severity and confidence.
7. Choose the verdict.
8. Write the report with the required format below.

## Finding contract

A reportable finding needs every item below:

1. A plausible precondition grounded in the artifact or its environment.
2. A trigger such as a request pattern, outage, retry, rollout step, malformed input, or concurrent action.
3. A causal path from the trigger to the failure.
4. A concrete impact on users, data, security, operations, cost, or future changes.
5. Evidence and a way to verify or falsify the concern.

Prefer evidence in this order:

1. A runtime reproduction, focused test, query, trace, or measurement.
2. A reachable code path, schema constraint, configuration value, or deployment manifest.
3. An explicit design statement, requirement, ADR, or authoritative dependency contract.
4. A reasoned scenario based on documented behavior and known constraints.

If a key fact is unknown, report the fact under open questions. Do not promote the concern to a finding. If evidence disproves the concern, record it under cleared concerns when the check matters to the verdict.

## Severity and confidence

Assign one severity to each finding:

- `blocker` means a realistic path violates a core requirement, security boundary, data guarantee, or safe deployment condition.
- `high` means expected conditions expose a likely or costly incident, outage, compatibility break, or operating failure.
- `medium` means a bounded design, maintenance, performance, cost, or diagnostic risk has a concrete failure mode.
- `low` means a small but real problem has a specific cost. Cosmetic nits do not qualify.

Assign one confidence level to each finding:

- `high confidence` requires direct evidence or a fully traced path.
- `medium confidence` allows one unverified environmental fact in an otherwise concrete path.
- Prefer an open question over a low-confidence finding.

## Verdicts

Use one verdict:

- `approve` when no material finding remains.
- `approve with conditions` when bounded risks have explicit owners or gates.
- `revise` when material changes are required before implementation or release.
- `reject` when a foundational choice conflicts with the requirements and a local correction cannot repair it.
- `insufficient evidence` when missing artifacts or operating facts prevent a responsible verdict.

## Required output

Produce a structured report with this format:

```markdown
# Adversarial review report

## Verdict

[Verdict and the one or two facts that control it.]

## Review contract

[Target, intent, requirements, constraints, evidence, and material unknowns.]

## Decision register

| Decision | Purpose | Assumptions | Failure probes | Evidence | Simpler alternative |
| --- | --- | --- | --- | --- | --- |
| [Choice] | [Requirement served] | [What must remain true] | [Load, outage, concurrency, retry, or migration cases] | [Supporting or contradicting evidence] | [Smallest option that still meets the requirements] |

## Findings

### AR-01. [Concrete failure]

| Field | Detail |
| --- | --- |
| Severity | [Blocker, High, Medium, or Low] |
| Confidence | [High or Medium] |
| Objectives | [Affected review objectives] |
| Decision or assumption | [The choice under challenge] |
| Scenario | [Precondition, trigger, causal path, and failure] |
| Evidence | [Files, lines, tests, metrics, design text, or dependency contract] |
| Impact | [User, data, security, operations, cost, or change impact] |
| Recommendation | [Smallest credible correction or simpler design] |
| Verification | [How to prove the correction or falsify the concern] |

## Missing requirements

[Requirements whose absence creates a concrete decision or assurance gap.]

## Open questions

[Unknown facts that can change the verdict. Name the evidence needed.]

## Cleared concerns

[Important failure modes checked and disproved, with evidence.]

## Coverage and limits

[Review modes and objectives applied, artifacts inspected, checks run, and areas not assessed.]
```

Sort findings by severity and failure impact. Omit the findings, missing requirements, open questions, or cleared concerns section when it is empty. Never omit the verdict, review contract, decision register, or coverage and limits.

Do not add praise, a prose walkthrough, generic best practices, or concerns that fail the finding contract.

**Reply:** the report above, with every concern proven, bounded as an open question, or discarded.
