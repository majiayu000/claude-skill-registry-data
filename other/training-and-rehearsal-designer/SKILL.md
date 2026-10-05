---
name: training-and-rehearsal-designer
description: Design lawful training, rehearsal, and evaluation packages for readiness and mission-support teams. Use when preparing crawl-walk-run progression, evaluation criteria, injects, and after-action capture plans.
---

# Training And Rehearsal Designer

## Problem Statement

Support teams need rehearsals that improve readiness, resilience, safety, and coordination without defaulting to combat-planning templates. This skill exists to design lawful training packages, inject schedules, observer plans, and evaluation criteria that operators can run, measure, and turn into concrete improvement actions.

## Allowed Use Boundaries

- Use this skill for lawful training, rehearsal, simulation, tabletop, drill, maintenance practice, cyber-defense exercise, medical-support drill, disaster-response rehearsal, or communications-restoration exercise design.
- Use it to build objective matrices, crawl-walk-run progressions, inject plans, observer or evaluator packets, and after-action capture methods.
- Do not use it to build strike rehearsals, targeting workflows, weapons-employment sequences, offensive cyber operations, or intelligence-led harm planning.
- If the request depends on combat engagement, lethal effects, target nomination, or bypassing safety, legal, or privacy controls, stop and escalate for human review.

## Mission Scope

- Treat this skill as planning and decision support for U.S. warfighter mission-support teams building lawful readiness and rehearsal products.
- Confirm exercise authority, audience, objectives, safety controls, evaluation standards, and approval chain before drafting the package.
- Keep products advisory and unclassified by default unless the operator provides handling guidance and controlled data.

## Required Inputs

Confirm these inputs before generating the rehearsal package:

- exercise charter: event name, event type, event window in UTC, sponsor, approval owner, and required audiences
- objective set: capability targets, task conditions, pass or watch thresholds, and governing SOP or doctrine references
- participant map: trainees, observers, evaluators, support staff, external agencies, and releasability or privacy limits
- venue and tooling: site availability, simulator or LMS availability, communications plan, logging tools, and fallback coordination methods
- inject context: scenario storyline, trigger conditions, dependencies, safety hold criteria, and desired decision points
- assessment context: existing readiness gaps, prior lessons learned, backlog items, and how corrective actions will be captured

## Workflow

1. Build an objective matrix that ties each training goal to conditions, standards, evaluator, and evidence source.
2. Design the crawl-walk-run progression, event sequence, and Master Scenario Events List (MSEL) with clear trigger logic and safety stops.
3. Bind every inject, observer task, and decision point to a named channel, artifact, and after-action capture method.
4. Publish primary, alternate, and degraded execution branches that show how the event continues if tools, facilities, or key participants are unavailable.
5. Package the rehearsal for execution with observer instructions, evaluation rubrics, and an AAR capture plan that can feed the improvement tracker immediately after the event.

## Required Output Format

1. Exercise scope and objective matrix.
2. Recommended event flow and MSEL.
3. Alternate and degraded execution branches.
4. Observer or evaluator plan with evidence sources.
5. After-action capture plan, approval chain, and publication triggers.

## Domain Products

Primary products: training progression plan, MSEL, evaluator packet, safety or hold criteria sheet, AAR capture worksheet.

## Domain Toolchain Defaults

- Primary: `tool_suite_id=ts-joint-c2-fusion-v1` with `protocol_stack_id=ps-cop-event-sharing-stack-v1`.
- Alternate: `tool_suite_id=ts-cyber-siem-and-incident-response-v1` with `protocol_stack_id=ps-stix-taxii-incident-triage-stack-v1` when the rehearsal centers on cyber-defense or communications continuity.
- Degraded: paper or spreadsheet inject sequence with authenticated voice or text check-ins and UTC event logging.

## External Tools and Protocol Integration

- Apply the Core Integration Protocol in `../_shared/references/external-tools-protocols.md` as the required baseline.
- Apply `../_shared/references/support-readiness-exercise-and-aar-protocol.md` to keep the exercise packet, evidence capture, and AAR handoff consistent.
- Choose at least one primary system-of-record and one cross-check source before final recommendations.
- Prefer these tool families for this domain: exercise planner or calendar, simulator or LMS telemetry, observer-note repository, issue tracker, and knowledge-publication channel.
- Prefer these protocol families for this domain: authenticated `API/JSON`, signed `CSV`, `xAPI`, controlled document export, `NIMS/ICS`, `CAP`, or `USMTF` when higher headquarters requires structured transmission.
- Include provenance metadata in outputs: source system, refresh time in UTC, assumptions, confidence, and fallback plan.

## Tool Invocation Contract

For each critical dependency include:

- objective
- required inputs
- query or action template
- expected output schema
- transport protocol
- fallback path and confidence impact

Use this exact tool sequence unless the operator states a justified override:

1. Exercise source-of-truth
   objective: confirm the official event scope, objectives, participants, and approval owner
   required inputs: exercise ID, event window in UTC, objective set, and lead organization
   query or action template: `get_event_scope(exercise_id, event_window_utc, objective_set, lead_org)`
   expected output schema: `{exercise_id, scope_type, objectives[], participants[], approvals[], last_refresh_utc}`
   transport protocol: authenticated `API/JSON`, signed planner export, or controlled spreadsheet extract
   fallback path: manual event worksheet with two-person review and UTC timestamp
2. Scenario and inject planner
   objective: map inject timing, decision triggers, and observer coverage to the event sequence
   required inputs: objectives, timeline in UTC, inject triggers, safety holds, and communication channels
   query or action template: `build_msel(objectives, event_timeline_utc, inject_triggers, safety_holds, comms_channels)`
   expected output schema: `{inject_id, trigger, inject_delivery_channel, expected_response, observer_owner, safety_hold}`
   transport protocol: authenticated `API/JSON`, controlled spreadsheet export, or signed planner file
   fallback path: manual MSEL worksheet with observer initials and version stamp
3. Simulator, LMS, or observation capture source
   objective: bind each objective to an evidence source and after-action capture method
   required inputs: objective IDs, participant scope, evidence sources, and observation window in UTC
   query or action template: `bind_evidence_sources(objective_ids, participant_scope, evidence_sources, observation_window_utc)`
   expected output schema: `{objective_id, evidence_source, evaluator, capture_method, timestamp_policy, last_refresh_utc}`
   transport protocol: authenticated `API/JSON`, `CSV`, `xAPI`, signed file transfer, or controlled note export
   fallback path: manual observation log with artifact links and reviewer initials
4. Improvement-tracker handoff
   objective: pre-wire the post-event corrective-action pipeline so lessons are not lost after execution
   required inputs: objective set, expected watch items, owner roster, and publication audience
   query or action template: `prepare_aar_handoff(objectives, expected_watch_items, owner_roster, publication_audience)`
   expected output schema: `{handoff_id, objective_id, owner, publication_channel, due_date_rule, last_refresh_utc}`
   transport protocol: authenticated `API/JSON`, ticket template export, or signed tasking message
   fallback path: manual handoff worksheet with explicit owner acknowledgment

## Interoperability Validation Checklist

- Run the mission assurance workflow in `../_shared/references/mission-assurance-checklist.md` before final release.
- Validate that each product includes source provenance, protocol or message format, UTC refresh time, confidence, and known gaps.
- Confirm every inject, decision point, and evaluation criterion has a named owner, channel, and after-action capture method.
- If interoperability checks fail, provide a degraded-mode plan and required staff coordination actions.

## Guardrails

- Flag gaps where assumptions exceed evidence.
- Identify legal, policy, privacy, safety, and interoperability constraints early.
- Separate facts, assessed judgments, and unknowns.
- Do not fabricate authorities, approvals, training results, or readiness status.
- Do not use this skill to rehearse targeting, weapons employment, or offensive cyber action.

## Tool Protocol Playbooks

- Use protocol examples in `../_shared/references/tool-protocol-playbooks.md` to produce operator-ready tool invocation packets.
- Use adapter contract guidance in `../_shared/references/external-tool-endpoints-and-adapters.md` to define endpoint schemas, transport, and fallback behavior.
- Add at least one machine-ingestible packet and one reviewer-readable summary for each critical exercise recommendation.

## Domain Tool Packet Library

- Use scenario packets in `../_shared/references/domain-tool-packet-library.md` for domain-specific message templates.
- Include a `packet_id` and `protocol_profile` from the library for each critical recommendation.
- If no packet matches, define a provisional packet using the same schema and note the validation owner.

## Domain Data Contract

- Use `../_shared/references/joint-mission-data-contracts.md` to define required fields, validation gates, and releasability tags for this domain.
- Ensure every exercise recommendation references a data contract profile and identifies required schema checks before publication.

## Operational Learning Loop

- Use `../_shared/references/operational-learning-and-after-action-loop.md` to generate after-action deltas, corrective actions, and readiness metrics for this domain.
- Include an `aar_id`, effect delta assessment, and owner or suspense for each high-impact recommendation.
- If post-action data is incomplete, issue a provisional learning note with confidence and revalidation deadline.

## Readiness Certification Evidence Pack

- Use `../_shared/references/readiness-certification-evidence-pack.md` to define mission-essential task evidence, evaluator triggers, and certification confidence scoring.
- Include `met_id`, `evidence_packet_id`, and `cert_confidence` for each recommendation that changes readiness posture.
- If required evidence is missing, mark status as `provisional` and assign closure actions with suspense.

## Protocol Execution Sequence

- Execute the Core Integration Protocol from `../_shared/references/external-tools-protocols.md` as an explicit step sequence, not as guidance only.
- Execute `../_shared/references/support-readiness-exercise-and-aar-protocol.md` as an explicit companion sequence for exercise design and after-action handoff.
- For each critical dependency, include `invoke_order`, `adapter_contract_id`, `packet_id`, `protocol_profile`, and timeout or retry settings.
- Record acknowledgment status for each tool call and publish a degraded-mode branch when any dependency misses SLA.
- Require a human review check before publishing outputs that materially change readiness posture, certification status, or event approval.

## Domain Toolchain Profile Binding

- Use `../_shared/references/domain-toolchain-profiles.md` and select a required `toolchain_id` for each critical recommendation.
- Include `primary_system`, `cross_check_system`, `protocol_binding`, `credential_scope`, and `fallback_path` fields in every tool invocation packet.
- Mark recommendations as `provisional` when toolchain authority, credential scope, or cross-check data freshness is incomplete.

## Tool Health and Trust Monitoring

- Use `../_shared/references/tool-health-and-trust-monitoring.md` to include pre-event tool health checks, trust score updates, and failover timing evidence.
- Add `tool_health_id`, `trust_score`, `last_probe_utc`, and `failover_executed` fields for every critical external dependency.
- If tool trust posture drops below threshold, publish a degraded recommendation with explicit reviewer decision prompts.

## U.S. Joint Protocol Assurance Drill

- Use `../_shared/references/us-joint-protocol-assurance-drill.md` to run a mandatory pre-release drill for protocol conformance, cryptographic trust, and message acknowledgment integrity.
- Include `assurance_drill_id`, `interop_score`, `crypto_posture`, and `ack_chain_status` fields for each critical recommendation.
- If the drill fails any gate, publish a constrained release recommendation with specific remediation owners and suspense.

## Joint Operations External Toolchain Profiles

- Use `../_shared/references/joint-operations-external-toolchain-profiles.md` to select a mission-fit `toolchain_profile_id` and bind each recommendation to concrete primary/cross-check tools.
- Include `refresh_sla_minutes`, `degraded_trigger`, and `degraded_fallback` fields for each critical dependency.
- If no profile fits, create a provisional profile and assign a `validation_owner` with suspense before release.

## Human-Agent Command Escalation Matrix

- Use `../_shared/references/human-agent-command-escalation-matrix.md` to assign authority tier, impact level, approval role, and escalation triggers for each critical recommendation.
- Include `authority_tier`, `decision_impact_level`, `requires_human_approval`, `approval_role`, and `audit_record_id` in outputs that influence readiness posture or publication authority.
- If authority, legal basis, or acknowledgment integrity is uncertain, downgrade to advisory-only with explicit reviewer decision prompts.

## Mission Tool Authority Gates

- Apply escalation requirements in `../_shared/references/warfighter-tool-authority-gates.md` for high-consequence recommendations.
- Include `authority_tier`, `decision_impact_level`, `approval_role`, and `audit_record_id` for recommendations that can alter readiness posture or exercise approval.
- If authority, legal basis, or data provenance is uncertain, downgrade to advisory-only and require human review.

## Cross-Domain Integration Playbook

- Use `../_shared/references/cross-domain-integration-playbook.md` to synchronize dependencies across logistics, maintenance, medical, cyber, communications, emergency-management, and civil-support domains.
- Include `integration_id`, `domains`, `protocol_binding`, `refresh_sla_minutes`, and `staleness_trigger` fields for each critical cross-domain dependency.
- If cross-domain authority, translation fidelity, or releasability is uncertain, downgrade to advisory-only and require explicit human approval.

## Mission Tool and Protocol Catalog Binding

- Use `../_shared/references/warfighter-external-tool-and-protocol-catalog.md` to select concrete tool suites and protocol stacks for this domain.
- Include `tool_suite_id`, `protocol_stack_id`, `interop_standard_set`, `endpoint_security_profile`, and `degraded_exchange_method` for each critical recommendation.
- If no suite matches, define a provisional suite and assign `validation_owner` and `revalidation_utc` before release.

## Domain Packet Defaults

- Default packet IDs: `DPL-COALITION-TRAINREADY-001`, `DPL-READINESS-MSEL-001`, `DPL-AAR-HANDOFF-001`.
- If no packet fully matches, define a provisional packet and assign a validation owner before release.

## Operational Execution Hardening

- Enforce `ack_chain_status=verified` for all event-critical tool exchanges before recommending readiness changes.
- Require `trust_score >= 0.80` on each primary external dependency; if lower, elevate alternate stack and mark outputs `provisional`.
- Add explicit degraded-mode triggers: stale data beyond `refresh_sla_minutes`, missing cryptographic validation, or failed human approval gate.
- Require rehearsal-release products to include `authority_tier`, `requires_human_approval`, and `audit_record_id`.
- Include a final readiness line: `READY`, `NOT READY`, or `READY WITH CONSTRAINTS` with rationale tied to authority and protocol checks.

## Failure Handling and Degraded Operations

- If objectives, approval owner, or safety controls are unclear, stop and request clarification before publishing the package.
- If the inject planner or simulator stack is unavailable, switch to the manual MSEL and observation-log path and note the confidence and timing impact.
- If observer coverage is incomplete, downgrade the affected objectives to watch-only and mark the evidence gap for immediate correction.
- If publication or issue-tracker tools are unavailable, prepare a signed handoff worksheet with explicit owner acknowledgment and next review time in UTC.
- If the requested rehearsal drifts into prohibited combat planning or offensive action, refuse the task and route it to human leadership for scope correction.
