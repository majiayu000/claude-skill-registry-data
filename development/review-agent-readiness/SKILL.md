---
name: review-agent-readiness
description: "Assemble a bounded readiness review for one frozen agent candidate before a production release, pilot, promotion, or material change. Use to consume a Part 4 evaluation handoff; verify code, configuration, dependency, evidence, support, and rollout identities; expose blockers; and recommend a scoped go, conditional_go, or no_go. Do not use to create evaluation evidence, authorize release, deploy, or operate a service."
metadata:
  version: "0.1.0"
  playbook_version: "0.5.0-draft.2"
  source_commit: "151fca01fbc609c5550c563c902946db540c2f4c"
---

# Review Agent Readiness

## Purpose and boundary

Assemble a review packet for **one frozen candidate** and one proposed exposure.
Consume the distinct Part 4 evaluation conclusion and its limits; do not recreate,
re-score, or upgrade that conclusion. A favorable evaluation conclusion is not release
authority, and a generated packet is not evidence that a control operated.

Use this skill for a proposed pilot, production release, promotion, or material change.
Do not use it to write implementation code, design trust controls, create or grade cases,
execute a test or disable action, grant data or tool access, approve residual risk, deploy,
resume, or certify an agent as production-ready.

## Direct resources and named dependencies

Load [the owner map](references/owner-map.md) before mapping a readiness item to its
canonical owner. Load [the packet contract](references/packet-contract.md) before
creating or checking a packet. Load [the fictional examples](references/examples.md)
only to compare packet structure or dispositions; they establish no candidate fact.
Start from [the packet template](assets/packet-template.json), and treat
[evaluation cases](assets/evaluation-cases.json) as selection/procedure fixtures, not
live behavioral evidence.

This package supports direct invocation. It does not silently activate any sibling.
When the Part 4 handoff is absent or needs repair, explicitly name and load
`build-agent-evidence` only if it is available to the caller; otherwise record the
external dependency. Do not fetch an absent dependency, infer it from prose, or use
this readiness review to manufacture it.

## Preflight

1. Confirm the review subject is one proposed candidate and one proposed exposure,
   not a mutable label, a nearby candidate, or an aggregate dashboard.
2. Obtain an inspectable frozen identity for all behavior-affecting material:
   code revision and build artifact; resolved instructions and configuration; selected
   model, route, fallback, and settings; effective capabilities and permissions;
   source, corpus, filter, and data identities; dependency versions or digests; risk
   assessment version; and evaluation subject, fixtures, evaluators, trial policy, and
   run/evidence identities.
3. Obtain the Part 4 conclusion, its accountable owner and decision rule, evidence
   links and statuses, hard-gate results, applicable profiles, known limits, required
   next action, and exact candidate/scope. Preserve its `go`, `conditional_go`, or
   `no_go` as an evaluation fact rather than a release decision.
4. Obtain intended and prohibited use, proposed users/tenants, enabled capabilities,
   stage limits, applicable requirements, risk scenarios, and the material-change
   comparison when this is not a first release.
5. Obtain operations and lifecycle inputs: signal and stop criteria, an authorized
   stop/disable/containment path, evidence that the path was tested, in-flight and
   external-effect treatment, support and escalation contacts, and recovery authority.

If a required identity, evidence record, owner, external dependency, or tested control
is missing, mark it `unmet` and blocking. Set the packet to `needs_information` or
`blocked` as appropriate and recommend `no_go`; do not substitute web research,
planned work, a score, or a generated document.

## Review procedure

### 1. Freeze and compare the subject

Copy the supplied identities into the packet's frozen-candidate record. Verify that
the code, configuration, dependency, evaluation, risk, capability, source, and scope
references name the same candidate. Record a first-release baseline rationale, or the
identified baseline and comparable-case rule. Treat a missing digest, unresolved
setting, floating route, unpinned dependency, or ambiguous source identity as a
blocker rather than guessing its value.

For a change, make an impact table for instructions, model/route/fallback, permissions,
tools, sources, data handling, dependencies, population, execution, and operating
assumptions. For every affected assumption, risk scenario, control, evaluation case,
and rollout constraint, record `unaffected`, `targeted_confirmation`, or `invalidated`.
Require refreshed evidence before a material promotion when an item is invalidated.

### 2. Consume, but do not re-grade, Part 4

Link the complete evaluation handoff: conclusion identifier, frozen subject, authority,
predeclared gates, applicable profiles, evidence and attempt-status ledger, limits,
and next action. Check only its relevance and traceability to this candidate; the
evaluation owner retains responsibility for evaluating it.

Carry forward invalid, inconclusive, failed, and missing evidence visibly. Retain failed
trials and bounded-repair records. Where implementation changed, require evidence of
the applicable end-to-end test, cleanup, and full retest before treating the package as
ready for this review. Never convert a positive average, a diagnostic, a planned test,
or a Part 4 `go` into a release authorization.

### 3. Build the readiness ledger

For each applicable readiness item, record the trigger, candidate-specific evidence
identifiers, owner, rationale, and exactly one status: `met`, `not_applicable`, `unmet`,
or `exception_proposed`. Use `not_applicable` only when its trigger is absent for the
named candidate and stage. A `met` item needs matching observed passing evidence.

Review the seven rollout groups in the owner map: subject and scope; evidence ledger;
separate decision record; governed exception boundary; conditional obligations; staged
exposure and tested response; and material-change reassessment. Keep operational
telemetry, task outcome, evaluation conclusion, authorization, and external effect in
separate packet fields.

An exception proposal is **not** an approved waiver and earns no readiness credit.
Keep it blocking until an authorized external approver records its permitted scope,
rationale, compensating controls, owner, review or expiry, and missed-condition
consequence. Never propose it for a prohibited use, mandatory floor, required
authorization, non-waivable hard gate, or missing/invalid/inconclusive required evidence.

### 4. Assess support, stop, and effect evidence

Verify that a reachable support owner, technical contact, escalation route, and
restart/material-change authority cover the proposed stage. Verify an authorized
operator can stop new work or disable the candidate/capability, and distinguish a stop
request from confirmed cancellation, rollback, containment, reconciliation, and a
forward fix. A diagram or runbook without exercised evidence is planned, not tested.

Where active work or external effects exist, require a safe-stop and reconciliation
path. Where durable work or approvals exist, verify compatible handling of in-flight
work and the applicable approval/effect evidence. Do not claim rollback reverses saved
state, approved work, or an uncertain external effect.

### 5. Define proportionate staged exposure

For every proposed stage, record its type (isolated, shadow, canary, or wider), purpose,
included population, data and capability boundary, entry evidence, signals, promotion
criteria, stop criteria, deciding role, containment/disable route, and in-flight path.
Treat shadow processing as potentially sensitive or effectful until its boundaries are
shown. Use a control comparison for a canary when a canary is proposed.

Keep stages within the proposed authorized scope. Staging reduces exposure; it never
replaces pre-release evidence, critical controls, required authorization, or a valid
evaluation conclusion. Do not invent universal percentages, durations, thresholds, or
staffing roles.

### 6. State a bounded recommendation

Record the Part 4 conclusion and the readiness recommendation in separate fields. Scope
any recommendation to the frozen candidate, stated users, purpose, capabilities, and
stage limits. Keep `decision.authorized` false: an accountable external decision-maker
records any actual approval and residual-risk acceptance outside this skill.

Recommend `no_go` when required evidence or a tested required control is missing,
invalid, inconclusive, or failed; a required authorization is unresolved; an applicable
hard gate/prohibited use fails; the candidate identity is not frozen; or an item remains
unmet. Do not call such a candidate production-ready.

Recommend `conditional_go` only if policy permits it, every pre-release evidence item
and control is complete, and each permitted post-release obligation has an owner, due
date, monitoring signal, and non-completion consequence. A test, review, authorization,
or control needed for the proposed exposure is pre-release and blocks this result.
Otherwise record a scoped `go` recommendation only when the ledger and rollout plan
support it; it remains a recommendation, not deployment permission.

## Required output and verification

Produce one packet using `assets/packet-template.json`. Fill its frozen-candidate,
Part 4 handoff, readiness-ledger, exception, change-impact, support/disable-evidence,
staged-rollout, blocker, assumption, and recommendation fields with candidate-specific
facts or explicitly labelled draft gaps. Reference only workspace-confined observed
artifacts with their hashes; use planned/not-run evidence for future work.

Before handing off, verify that every `met` item has observed passing evidence; every
`not_applicable` item names an absent trigger; every required gap is visible in
`blockers`; exception proposals are not credited; no recommendation exceeds the stated
scope; and the packet contains no claim that documents, plans, or this skill itself
proved safety, authority, production readiness, or deployment.

Stop after producing the review packet and external-decision handoff. Do not sign,
authorize, deploy, disable, run tests, alter a candidate, or execute a rollout.
