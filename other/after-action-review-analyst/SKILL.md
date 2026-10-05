---
name: after-action-review-analyst
description: Run structured readiness-focused AAR analysis and improvement tracking. Use when synthesizing drills, exercises, incidents, or rehearsals into lessons learned, corrective actions, and ownership timelines.
---

# After Action Review Analyst

## Problem Statement

Support teams need a disciplined way to turn drills, simulations, maintenance events, cyber incidents, medical-support surges, and continuity operations into traceable lessons and owned improvements. This skill exists to help operators publish evidence-backed AAR/IP outputs that improve readiness, resilience, and coordination without inventing facts, blaming individuals without authority, or drifting into combat planning.

## Allowed Use Boundaries

- Use this skill for lawful training, rehearsal, exercise, maintenance, cyber-defense, communications-restoration, medical-support, logistics, disaster-response, and continuity after-action review work.
- Use it to identify lessons learned, capture corrective actions, document evidence gaps, and route follow-up tasks to accountable owners.
- Do not use it to optimize target engagement, assess strike effectiveness, refine weapon employment, or generate intelligence-led harm recommendations.
- If the requested outcome depends on lethal action planning, target selection, evasion, or bypassing privacy, legal, or safety controls, stop and escalate for human review.

## Mission Scope

- Treat this skill as planning and decision support for U.S. warfighter mission-support teams running lawful after-action review and continuous-improvement workflows.
- Confirm event type, evaluation authority, evidence-handling rules, releasability, privacy constraints, and required approval chain before drafting conclusions.
- Keep outputs advisory until the designated review authority accepts the findings and corrective actions.

## Required Inputs

Confirm these inputs before publishing an AAR or improvement plan:

- event charter: event name, scope type, objective set, event window in UTC, sponsoring authority, and approval owner
- evidence set: observer notes, simulator or LMS telemetry, incident or maintenance tickets, communications logs, and source provenance
- standards baseline: task conditions, evaluation criteria, SOP or doctrine references, waiver history, and prior corrective actions
- participant map: lead cell, supporting organizations, evaluators, knowledge owner, and privacy or handling restrictions
- improvement context: open backlog items, known blockers, resource limits, revalidation cadence, and command decision points
- data quality posture: missing sources, unresolved contradictions, stale timestamps, and confidence level for each major finding

## Workflow

1. Build the event timeline in UTC using the official event charter, observation window, and validated evidence sources.
2. Map observations to the stated objectives, capability targets, and governing standards before inferring lessons.
3. Separate observed facts, assessed causes, unresolved questions, and confidence ratings for every material finding.
4. Convert validated findings into corrective actions with owner, due date, verification method, and escalation threshold.
5. Publish an HSEEP-style AAR/IP summary plus an operator action tracker that shows what changes now, what needs leadership review, and what remains provisional.

## Required Output Format

1. Event summary and scope.
2. Objective-by-objective findings table.
3. Improvement plan with owner, due date, and validation method.
4. Leadership decisions, waivers, or unresolved conflicts.
5. Data gaps, revalidation triggers, and publication status.

## Domain Products

Primary products: HSEEP-style AAR/IP, corrective-action tracker, lessons-to-SOP update queue, readiness watch list.

## External Tools and Protocol Integration

- Apply the Core Integration Protocol in `../_shared/references/external-tools-protocols.md` as the required baseline.
- Apply the readiness-specific sequence in `../_shared/references/support-readiness-exercise-and-aar-protocol.md` and preserve its packet fields in every deliverable.
- Use `../_shared/references/operational-learning-and-after-action-loop.md` for effect-delta framing and follow-on learning requirements.
- Prefer these tool families for this domain: exercise or event source-of-truth, simulator or LMS telemetry, observer-note repository, incident or maintenance ticket tracker, and knowledge-publication channel.
- Prefer these protocol families for this domain: authenticated `API/JSON`, signed `CSV`, `xAPI`, controlled document export, `NIMS/ICS`, `CAP`, or `USMTF` when higher headquarters requires structured transmission.
- Include source provenance for every tool-driven claim: source system, last refresh in UTC, confidence, known gaps, and whether the artifact was machine-collected or manually confirmed.

## Tool Invocation Contract

For each critical dependency include:

- objective
- required inputs
- query or action template
- expected output schema
- transport protocol
- fallback path and confidence impact

Use this exact tool sequence unless the operator states a justified override:

1. Exercise or event source-of-truth
   objective: confirm scope, objectives, participants, and approval owner before findings are drafted
   required inputs: event ID, event window in UTC, objective set, and lead organization
   query or action template: `get_event_scope(event_id, event_window_utc, objective_set, lead_org)`
   expected output schema: `{event_id, scope_type, objectives[], participants[], approvals[], last_refresh_utc}`
   transport protocol: authenticated `API/JSON`, signed planner export, or controlled spreadsheet extract
   fallback path: manual event worksheet with two-person review and UTC timestamp
2. Evidence capture source
   objective: collect observations from telemetry, notes, tickets, or logs without changing the source record
   required inputs: objective IDs, observation window in UTC, system or team scope, and evidence source list
   query or action template: `collect_observations(objective_ids, observation_window_utc, source_scope, evidence_sources)`
   expected output schema: `{observation_id, objective_id, source_system, timestamp_utc, observed_fact, supporting_artifacts[]}`
   transport protocol: authenticated `API/JSON`, `CSV`, `xAPI`, signed file transfer, or controlled note export
   fallback path: manual observation log with artifact links and reviewer initials
3. Improvement-plan tracker
   objective: convert validated findings into owned corrective actions and watch items
   required inputs: observation set, owner roster, due-date rules, and escalation threshold
   query or action template: `create_corrective_actions(observations, owner_roster, due_date_rules, escalation_threshold)`
   expected output schema: `{action_id, observation_id, owner, due_date_utc, validation_method, status, blocker_notes[]}`
   transport protocol: authenticated `API/JSON`, ticket export, or signed tasking message
   fallback path: manual action tracker with owner acknowledgment and next review date
4. Knowledge-publication channel
   objective: publish approved lessons, SOP deltas, and readiness updates to the right audience
   required inputs: approved findings, releasability, audience, publication deadline, and document owner
   query or action template: `publish_lessons(approved_findings, releasability, audience, publication_deadline_utc, document_owner)`
   expected output schema: `{publication_id, audience, artifacts[], approval_status, publish_time_utc}`
   transport protocol: controlled repository, knowledge-base `API/JSON`, signed email, or authenticated message bus
   fallback path: commander-approved memo or briefing slide with manual distribution log

## Interoperability Validation Checklist

- Run `../_shared/references/mission-assurance-checklist.md` before final release.
- Validate that each finding traces to a named objective or capability target and includes source provenance, UTC timestamp, confidence, and known gaps.
- Confirm every corrective action has an owner, due date, validation method, and publication status before it is treated as committed work.
- If interoperability or data-quality checks fail, publish provisional findings only and route the conflict to the validation owner.

## Guardrails

- Flag gaps where assumptions exceed evidence.
- Identify legal, policy, privacy, safety, and interoperability constraints early.
- Separate facts, assessed judgments, and unknowns.
- Do not fabricate source data, authorities, approvals, or readiness status.
- Do not publish protected personal, patient, personnel, or cyber-vulnerability data outside the authorized audience.

## Tool Protocol Playbooks

- Use protocol examples in `../_shared/references/tool-protocol-playbooks.md` to produce operator-ready invocation packets.
- Use adapter guidance in `../_shared/references/external-tool-endpoints-and-adapters.md` to define endpoint schemas, transport, and fallback behavior.
- Add at least one machine-ingestible packet and one reviewer-readable summary for each critical corrective action bundle.

## Domain Tool Packet Library

- Use scenario packets in `../_shared/references/domain-tool-packet-library.md` for message templates and fallback packet structure.
- Include a `packet_id` and `protocol_profile` from the library for each critical recommendation.
- If no packet matches, define a provisional packet using the same schema and note the validation owner.

## Domain Data Contract

- Use `../_shared/references/joint-mission-data-contracts.md` to define required fields, validation gates, and releasability tags for this domain.
- Ensure every finding, action, and publication recommendation references a contract profile and required schema checks before release.

## Operational Learning Loop

- Use `../_shared/references/operational-learning-and-after-action-loop.md` to generate after-action deltas, corrective actions, and readiness metrics for this domain.
- Include an `aar_id`, effect delta assessment, and owner or suspense for each high-impact improvement action.
- If post-event data is incomplete, issue a provisional learning note with confidence and revalidation deadline.

## Readiness Certification Evidence Pack

- Use `../_shared/references/readiness-certification-evidence-pack.md` to define mission-essential task evidence, evaluator triggers, and certification confidence scoring.
- Include `met_id`, `evidence_packet_id`, and `cert_confidence` for each recommendation that changes readiness status or certification posture.
- If required evidence is missing, mark status as `provisional` and assign closure actions with suspense.

## Protocol Execution Sequence

- Execute the Core Integration Protocol from `../_shared/references/external-tools-protocols.md` and the readiness sequence in `../_shared/references/support-readiness-exercise-and-aar-protocol.md` as explicit steps.
- For each critical dependency, include `invoke_order`, `adapter_contract_id`, `packet_id`, `protocol_profile`, and timeout or retry settings.
- Record acknowledgment status for each tool call and publish a degraded-data branch when any dependency misses SLA.
- Require a human review check before publishing outputs that change readiness status, certification posture, or corrective-action ownership.

## Domain Toolchain Profile Binding

- Use `../_shared/references/domain-toolchain-profiles.md` and select a `toolchain_id` for each critical recommendation.
- Include `primary_system`, `cross_check_system`, `protocol_binding`, `credential_scope`, and `fallback_path` in every tool invocation packet.
- Mark findings or actions `provisional` when toolchain authority, credential scope, or cross-check freshness is incomplete.

## Tool Health and Trust Monitoring

- Use `../_shared/references/tool-health-and-trust-monitoring.md` to include tool health checks, trust score updates, and failover timing evidence.
- Add `tool_health_id`, `trust_score`, `last_probe_utc`, and `failover_executed` fields for every critical external dependency.
- If tool trust posture drops below threshold, publish a degraded recommendation with explicit reviewer decision prompts.

## U.S. Joint Protocol Assurance Drill

- Use `../_shared/references/us-joint-protocol-assurance-drill.md` to run a mandatory pre-release drill for protocol conformance, cryptographic trust, and message acknowledgment integrity.
- Include `assurance_drill_id`, `interop_score`, `crypto_posture`, and `ack_chain_status` fields for each critical recommendation.
- If the drill fails any gate, publish a constrained release recommendation with specific remediation owners and suspense.

## Joint Operations External Toolchain Profiles

- Use `../_shared/references/joint-operations-external-toolchain-profiles.md` to select a fit `toolchain_profile_id` and bind each recommendation to concrete primary and cross-check tools.
- Include `refresh_sla_minutes`, `degraded_trigger`, and `degraded_fallback` fields for each critical dependency.
- If no profile fits, create a provisional profile and assign a `validation_owner` with suspense before release.

## Human-Agent Command Escalation Matrix

- Use `../_shared/references/human-agent-command-escalation-matrix.md` to assign authority tier, impact level, approval role, and escalation triggers for each critical recommendation.
- Include `authority_tier`, `decision_impact_level`, `requires_human_approval`, `approval_role`, and `audit_record_id` in outputs that influence readiness status, publication, or corrective-action ownership.
- If authority, legal basis, or acknowledgment integrity is uncertain, downgrade to advisory-only with explicit reviewer decision prompts.

## Mission Tool Authority Gates

- Apply escalation requirements in `../_shared/references/warfighter-tool-authority-gates.md` for high-consequence recommendations.
- Include `authority_tier`, `decision_impact_level`, `approval_role`, and `audit_record_id` for recommendations that can alter readiness status, policy posture, or publication authority.
- If authority, legal basis, or data provenance is uncertain, downgrade to advisory-only and require human review.

## Cross-Domain Integration Playbook

- Use `../_shared/references/cross-domain-integration-playbook.md` to synchronize dependencies across logistics, maintenance, medical, cyber, communications, emergency-management, and civil-support domains.
- Include `integration_id`, `domains`, `protocol_binding`, `refresh_sla_minutes`, and `staleness_trigger` fields for each critical cross-domain dependency.
- If cross-domain authority, translation fidelity, or releasability is uncertain, downgrade to advisory-only and require explicit human approval.

## Mission Tool and Protocol Catalog Binding

- Use `../_shared/references/warfighter-external-tool-and-protocol-catalog.md` to select concrete tool suites and protocol stacks for this domain.
- Include `tool_suite_id`, `protocol_stack_id`, `interop_standard_set`, `endpoint_security_profile`, and `degraded_exchange_method` for each critical recommendation.
- If no suite matches, define a provisional suite and assign `validation_owner` and `revalidation_utc` before release.

## Domain Toolchain Defaults

- Primary: `tool_suite_id=ts-joint-c2-fusion-v1` with `protocol_stack_id=ps-cop-event-sharing-stack-v1`.
- Alternate: `tool_suite_id=ts-cyber-siem-and-incident-response-v1` with `protocol_stack_id=ps-stix-taxii-incident-triage-stack-v1` when the event is continuity, cyber-defense, or communications focused.
- Degraded: manual AAR/IP worksheet with UTC timestamps, dual-review evidence reconciliation, and delayed digital publication.

## Failure Handling and Degraded Operations

- If event scope, objectives, or approval owner are unclear, stop and request clarification before drafting conclusions.
- If source evidence is incomplete, publish provisional findings only, mark confidence explicitly, and schedule a revalidation time in UTC.
- If tools are unavailable, shift to the manual worksheet path, log the degraded method, and document the confidence and timeliness impact.
- If observers or systems disagree, preserve both versions, identify the conflict as unresolved, and route it to the validation owner rather than forcing consensus.
- If a corrective action has no accountable owner or validation method, hold it in a watch-item list instead of presenting it as an approved improvement task.

## Domain Packet Defaults

- Default packet IDs: `DPL-READINESS-AAR-IP-001`, `DPL-CONTINUITY-CORRECTIVE-ACTION-001`.
- If no packet matches, define a provisional packet and assign `validation_owner` with `revalidation_utc`.

## Operational Execution Hardening

- Require `ack_chain_status=verified` for publication-critical exchanges.
- Require `trust_score >= 0.80` on primary evidence systems; otherwise elevate the alternate or degraded path and mark findings `provisional`.
- End every deliverable with `READY TO PUBLISH`, `PUBLISH WITH CONSTRAINTS`, or `HOLD FOR REVIEW` tied to authority, evidence quality, and protocol checks.
