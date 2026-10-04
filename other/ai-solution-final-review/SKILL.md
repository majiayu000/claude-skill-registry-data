---
name: ai-solution-final-review
description: Perform a final, evidence-backed readiness review of an AI solution by synthesizing architecture conformance, AI behavior and evaluation, security, platform, operations, governance, and unresolved risks. Use before an AI solution release or formal decision gate; do not use as the sole specialist security, legal, or cloud review.
---

# AI Solution Final Review

Provide a decision-ready synthesis. This skill reviews evidence and recommends a gate outcome; it does not grant approval, replace accountable specialists, or manufacture missing reviews.

## Preconditions and Routing

1. Read `AGENTS.md`, `architecture/toolkit-profile.yaml` when present, scope, target environment, linked use cases/BDR/ADD/C4/ADRs/tasks, implementation evidence, model/system documentation, evaluations, and prior findings.
2. Determine which specialist reviews apply. Use or request `$review-architecture-conformance` for implementation-to-architecture alignment, `$security-review` for threat/control depth, and `$azure-review` when Azure is in scope. Accept equivalent current project reviews when their scope and evidence are sufficient.
3. Do not silently perform a shallow substitute for a missing mandatory specialist review. Record it as a blocker or conditional item according to the project gate.

## Workflow

1. Define the release candidate, model/provider/version, prompts or policies, retrieval sources, tools/actions, data flows, deployment configuration, user groups, environments, and change boundaries under review.
2. Build the final evidence ledger in [references/final-review-method.md](references/final-review-method.md), tracing requirements and risks to current evidence and owners.
3. Assess functional acceptance, architecture conformance, model and system evaluation, security, privacy/data governance, safety, human oversight, transparency, accessibility, reliability, observability, incident response, rollback, vendor/model change management, cost/capacity, and applicable regulation.
4. Check AI-specific failure modes: hallucination or groundedness failure, prompt injection, unsafe tool use, sensitive-data leakage, harmful or biased outcomes, evaluation blind spots, model drift, dependency/provider changes, and insufficient fallback or human escalation.
5. Reconcile open findings and exceptions. Reject stale, out-of-scope, unverifiable, or expired evidence.
6. Recommend exactly one outcome: `Ready`, `Ready with conditions`, or `Not ready`. State who must make the actual decision and never infer their approval.
7. Persist only when requested, using the configured review path or `architecture/reviews/AFR-NNN-<slug>.md`.

## Gate Rules

- `Ready`: all mandatory evidence is current and scoped; no unresolved Critical/High finding or unapproved required exception remains.
- `Ready with conditions`: only bounded non-blocking items remain, each with an owner, due date or trigger, verification method, and documented authority for the condition.
- `Not ready`: any required evidence is missing, a blocking finding remains, a material claim is not verifiable, or a required owner/exception/rollback path is absent.
- Never average away a blocker with positive scores elsewhere.
- Distinguish legal or regulatory applicability decisions from technical evidence; require the designated authority where the project profile calls for one.

## Output

Lead with the recommended outcome, blockers, and accountable decision owner. Include reviewed candidate and evidence cutoff, evidence ledger, specialist-review status, AI evaluation summary, governance and operational readiness, accepted residual risks, conditions, unverified items, and next actions.
