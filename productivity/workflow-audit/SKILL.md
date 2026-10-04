---
name: workflow-audit
description: Use when manual work, prior sessions, or an operator interview must be audited for repeatable skill, automation, or bounded-loop candidates.
metadata:
  version: "8.1.0"
  updated: "2026-08-20"
  profile: "one-shot"
  assumes: "The operator supplies bounded text, Markdown, or JSON evidence and the promotion authority is explicit."
  conflicts_with: "Invented run history, autonomous policy mutation, unbounded scheduling, or treating demo evidence as authority."
---

# Workflow Audit

<skill_contract>
  <input>Bounded manual notes, prior-session evidence, or interview answers describing work, repetition, decisions, and constraints.</input>
  <output>A deterministic audit with mode, evidence-bounded candidates, skill/automation/loop decisions, permissions, and a typed handoff.</output>
  <done>Every recommendation points to supplied evidence, remains within the input bound, and has an explicit supervised promotion decision.</done>
  <non_goals>Editing skills, changing schedules, mutating Vault state, inventing metrics, or executing an unapproved external action.</non_goals>

## Usage Template

Provide: objective, evidence source, mode (`manual`, `session`, or `interview`), size bound, candidate limit, operator/approval owner, and desired handoff.

## Workflow

<intake>
Classify the source as manual notes, prior-session history, or an operator interview. Preserve its hash and provenance. Infer a mode only when the text contains a clear session or interview signal; otherwise use `manual`.
</intake>

<unknowns_gate>
Separate observed repetition from a proposed improvement. Missing frequency, owner, verifier, permission, or stop condition makes a candidate review-only; it does not justify a schedule or autonomous loop.
</unknowns_gate>

<execute>
Extract a bounded list of distinct work candidates. For each candidate, decide:

- `SKILL_CANDIDATE` when the work has a reusable procedure or multiple steps; otherwise `KEEP_MANUAL`.
- `AUTOMATION_CANDIDATE` only when repetition or a clear trigger is evidenced; otherwise `HOST_REQUIRED_REVIEW`.
- `LOOP_CANDIDATE` only when retry, monitoring, polling, follow-up, or a repeat-until condition is evidenced; otherwise `NO_LOOP`.

Record the evidence snippet, approval owner, verifier, stop condition, and side-effect expectation. Promotion is a separate supervised action with a receipt and rollback path.
</execute>

<evaluate>
Reject recommendations that rely on an unbounded input, an inferred external permission, a fluent success claim, or a video/demo as authority. Check candidate count, source hash, evidence linkage, and `side_effect_count: 0`.
</evaluate>

## Failure Protocol

Return `NEEDS_INPUT` for missing evidence or a required authority decision, `INSUFFICIENT_EVIDENCE` when repetition cannot be supported, and `VERIFY_FAILED` when a recommendation cannot be traced to the supplied source. Preserve the audit receipt and do not promote.

## Output Contract

Return `status`, `result`, `evidence`, `unknowns`, and `next_action`. The result includes mode, source hash, bounded candidates, skill/automation/loop decisions, approval, verifier, stop condition, and side-effect count.

## Edge Cases

- A quiet prior session is not proof that a workflow is eligible for automation; record `INSUFFICIENT_EVIDENCE` or request a frequency probe.
- A recurring task that writes to a shared Vault remains a supervised staged-write candidate even when the extraction itself is deterministic.

## Success Metrics

- Source provenance and candidate bounds are preserved.
- Every decision is evidence-linked and independently checkable.
- No skill, schedule, external service, or Vault file is changed by the audit.

## Quality Gates

- [ ] Mode is explicit or conservatively inferred.
- [ ] Unknown permissions, verifiers, and stop conditions are surfaced.
- [ ] Promotion is supervised and receipt-backed.
- [ ] `side_effect_count` is zero.

</skill_contract>
