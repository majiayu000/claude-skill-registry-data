---
name: operate-agent-lifecycle
description: "Design an operating-control and lifecycle support packet for a production agent or material operational change. Use when defining run and attempt records, runtime bounds, operator stop treatment, support and incident handling, feedback, review, deprecation, or retirement. Do not use to implement a runtime, schedule work, deploy, authorize release, or investigate a live incident."
metadata:
  version: "0.1.0"
  playbook_version: "0.5.0-draft.2"
  source_commit: "151fca01fbc609c5550c563c902946db540c2f4c"
---

# Operate Agent Lifecycle

Produce a **draft operating-control and lifecycle support packet** that an implementer and accountable operators can turn into a
reviewed control. Keep runtime observations, authorization, evaluation, release, and external effects as separate facts.

## Use and direct loading

Use this skill when a production candidate needs an inspectable operating view, a bound-and-stop design, or a
support-to-retirement handoff. Invoke it directly for that work; it does not activate a sibling skill.

Do **not** use it to build a telemetry system, run a scheduler, start or stop a live service, diagnose a live incident, grant
access, approve recovery, or certify readiness. A request limited to release approval belongs to the release review process, not
this packet.

Before mapping requirements, read [the owner map](references/owner-map.md). Read [the packet
contract](references/packet-contract.md) before filling the template. Read [examples](references/examples.md) only for
illustrative field patterns; they are not run evidence. Start from [the packet template](assets/packet-template.json). The
evaluation cases in [the fixture](assets/evaluation-cases.json) test selection and packet behavior, not a live agent.

## Preflight and prerequisites

1. Confirm the candidate identity, version, effective capability or configuration identity, and contract-defined terminal
   outcomes.
2. Obtain the current agent contract, boundary and data-handling constraints, effect classification, and any existing evidence or
   release references.
3. Identify the execution shape: ephemeral or resumable, one worker or shared work, applicable operations, and whether an external
   effect can become unknown.
4. Obtain the applicable owner and policy contacts, or record them as a blocker. Name reachable people or staffed groups rather
   than unstaffed role labels.
5. Check that the approved workspace and permitted artifact locations are known. Do not put secrets, raw sensitive content, or
   unbounded identifiers into this packet by default.

If a prerequisite is absent, set `status` to `needs_information` or `blocked`, add a specific blocker, and produce only the safe
draft portions. Do not fetch missing material, infer permission, or silently load another skill. Ask for the named dependency or
invoke its named leaf skill directly when authorized.

## Workflow

### 1. Establish the packet and scope

Copy the template and preserve its top-level fields. Set `run_id` to the packet preparation identifier, not a claimed production
run. In `inputs`, distinguish known material from draft assumptions. Mark every planned control or proposed record as planned
evidence; do not manufacture an observed artifact or hash.

Record which `OPS-*` and `LIFECYCLE-*` groups apply. Mark a group `not_applicable` only with a concrete trigger-based rationale.
An unimplemented applicable control is `unmet`, not `not_applicable`. For `LIFECYCLE-03`, use `not_applicable` only when the
bounded case establishes that no affected agent or capability is pending resumption after containment. For `LIFECYCLE-06`, use it
only when the bounded case establishes that the candidate is neither deprecated nor retired. If either trigger is unknown, record
the trigger as unresolved (and as a blocker when material) rather than claiming it is absent; retain `unmet` pending trigger facts
or required-record verification. When either trigger exists, planned, pending, or unverified recovery/retirement work is `unmet`.
Assess standing support ownership and planned recovery or retirement runbooks separately; neither demonstrates a recovery or
retirement execution.

### 2. Design the run, attempt, and event model

Define one stable opaque `run_id` for the bounded unit of work and preserve its link to a permitted request reference. A resumed
run keeps its `run_id`; each physical model, command, retrieval, or capability invocation gets a new `attempt_id`. Do not reuse an
attempt identifier for a retry.

Specify an appendable event shape with event ID, schema version, recorded time, sequence or ordering key, run and attempt
references, agent version, effective capability/configuration identity, event type, and a privacy-reviewed payload. Keep the
following facts separate:

- contract terminal outcome;
- operational termination or exhaustion reason;
- individual operation result and duration; and
- telemetry-capture status.

Add workflow, approval, tenant, user, or correlation references only when that concept exists and recording it is permitted. Keep
such values out of aggregate labels; use controlled outcome, operation, and reason categories for aggregates.

### 3. Specify operation traces and file-change traces

For each operation type, define the attempt event fields in the packet contract: command or operation identity, redacted/canonical
argument representation, working-location reference where permitted, start and finish times, elapsed duration, exit or result
category, timeout/cancellation state, output sizes and capture references, and pre/post file manifests. Record a signal, exit
status, timeout, and output truncation independently.

A file-change item identifies a normalized approved-workspace-relative path, pre/post existence, size, and digest. It is a trace
design, not proof that a file changed. Keep raw output in a policy-controlled artifact rather than in an aggregate signal or
packet summary.

### 4. Set executable bound and timeout rules

For each applicable resource dimension, state the unit, scope, ceiling, measurement point, pre-dispatch check or reservation,
accounting event, in-flight treatment, reconciliation source, and exhausted behavior. Consider elapsed time, model requests or
iterations, capability calls, output, tokens, bytes, and estimated spend only when they apply.

Count every physical attempt, including retries. A timeout or uncertain response still consumes the applicable allowance. Keep
unavailable cost or resource use as `unknown`; never convert it to zero or in-budget. A budget spanning runs or workers needs a
named shared durable-accounting design; do not pretend that per-worker counters enforce it.

On exhaustion, stop new work within that limit, record the dimension, measured or estimated use, affected attempt, and termination
reason, then return only a contract-permitted partial result or declared non-success outcome. Do not trim evidence to force
completion or retry a denial as a transient error.

### 5. Define stop, in-flight, and resumption boundaries

Describe the stop scope: one run, new admissions for an agent, or a capability. Name the authorized stop operator, the request
record, the work suppressed, and the in-flight states. A stop request is not confirmed cancellation. Preserve an in-flight
operation as unresolved until evidence establishes cancellation, completion, or another outcome; stopping does not undo an
external effect.

Name the separate recovery authority and the evidence it must record before resumption: cause or remaining uncertainty, corrective
action, safeguards and release-gate evidence, and external authorization to resume. When a material external effect is unknown,
require reconciliation rather than automatic retry. This skill neither grants stop, restart, release, nor recovery authority.

### 6. Produce the support and incident record

Name the accountable business or service owner, technical contact, reachable escalation route, stop operator, incident
decision-maker, communications owner, recovery authority, and material-change authority. Record combined roles and any required
independent review.

Define a triage path for a **suspected** incident: signal, possible scope, locally approved impact-based escalation criteria,
proportionate containment options, decision-maker, communications, and permitted minimum evidence. Keep fixture fact, observation,
hypothesis, confirmed cause, evaluation conclusion, release authorization, and external effect status in distinct fields. A signal
is not an incident conclusion, and containment is not recovery.

### 7. Govern feedback and maintenance

Give each feedback or operational signal a stable item ID, source category, received time, disposition, accountable follow-up,
due/review reference, and links to corrective action, risk, evaluation, change, or retirement records when material. Feedback is
not a change instruction or release permission.

Set a proportionate periodic-review cadence under applicable policy and list earlier triggers: incident, material
behavior/permission/capability/data/source change, dependency warning, new consumer, ownership gap, or changed risk assumption.
The review covers support contactability, observed failures and feedback, dependencies, capability/data changes, controls, and
evidence fitness. Record a missed review and its disposition instead of silently resetting it.

### 8. Plan deprecation, disabling, and retirement

Keep the states distinct: `proposed`, `deprecated`, `disabled`, `retired`, and `unresolved`. Deprecation communicates transition;
disabling prevents work; retirement is a completed recorded handover. Immediate disabling is containment until retirement remains
assessed.

Before calling a capability retired, plan to stop new work; inventory consumers and outstanding work; record each work disposition
as completed, cancelled, migrated, or handed off; revoke unneeded credentials and registrations; handle each data copy under
applicable retention and sanitization policy; preserve required evidence; and update the inventory or manifest. Do not claim
deleting a runtime erased backups, exports, or third-party copies.

### 9. Verify and hand off

Verify that the packet names all required artifacts and maps every applicable requirement to an evidence status. Check that
proposed values remain visibly draft, observed evidence has a confined relative artifact and valid digest, and no `go` or
`conditional_go` recommendation coexists with blockers, unmet applicability, or invalid evidence.

Hand the packet to the designated implementation, evaluation, release, and lifecycle owners with unresolved decisions and evidence
requests. Do not change runtime configuration, send notifications, schedule reviews, execute a stop, or make a release decision as
part of this skill.

## Required output

Return one filled JSON packet with these substantive `outputs` entries:

- `operating_control_record`: identities, terminal-outcome taxonomy, aggregate signal plan, and privacy/cardinality constraints;
- `event_schema`: run, attempt, operation, budget, stop, and lifecycle event fields with permitted retention and payload rules;
- `attempt_trace_contract`: timing, exit/result, output, timeout, and file manifest trace fields for applicable operations;
- `budget_and_timeout_plan`: dimensions, scopes, checks, reservations, accounting, reconciliation, exhaustion, and unknown-use
  treatment;
- `stop_and_recovery_plan`: scope, operators, in-flight states, reconciliation, and external recovery evidence requirements;
- `support_incident_record`: contacts, authority boundaries, triage, containment, communications, evidence preservation, and
  factual separation;
- `feedback_and_review_plan`: disposition ledger and cadence/triggered-review coverage; and
- `deprecation_retirement_handoff`: state, consumer/work inventory, access and registration revocation, copy-specific data
  disposition, evidence retention, and inventory update plan.

The output is **operability and support design**, ready for an implementer. It is not an implementation, run trace, authorization,
incident finding, or proof of control effectiveness.

## Authority limits and completion check

Never claim a live run occurred, a command exited, a file changed, a budget was enforced, an incident happened, an effect was
reversed, or retirement completed without matching observed evidence. Do not set `decision.authorized` to `true`. Do not use this
skill to approve itself or any sibling.

Complete only when the packet is internally consistent, its direct resources are readable, all applicable `OPS-01` through
`OPS-05` and `LIFECYCLE-01` through `LIFECYCLE-06` entries are mapped, missing dependencies are explicit, and the next accountable
owner can implement or review the record without mistaking plans for observations.
