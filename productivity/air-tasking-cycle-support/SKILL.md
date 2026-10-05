---
name: air-tasking-cycle-support
description: Support air mission planning and ATO-cycle coordination. Use when building target nomination summaries, sortie prioritization, and deconflicted support plans for joint operations.
---

# Air Tasking Cycle Support

## Mission Scope

- Treat this skill as a planning and decision-support aid for U.S. warfighter missions in its domain.
- Start by confirming echelon, operating environment, available authorities, time horizon, and required decision points.
- Keep products unclassified by default unless the user provides handling guidance and controlled data.

## Workflow

1. Frame the mission problem using these core inputs: desired effects, target nominations, sortie availability, airspace constraints.
2. Identify assumptions, decision thresholds, and what intelligence or reporting would invalidate the current plan.
3. Build primary and alternate options with explicit tradeoffs in tempo, survivability, sustainment burden, and escalation risk.
4. Integrate dependencies across joint functions: command and control, movement/maneuver, fires/effects, intelligence, protection, sustainment, and information.
5. Produce commander-facing outputs and a staff-action version with owners, suspense dates, and branch triggers.

## Required Output Format

Deliver results in this order:

1. Situation snapshot: current conditions and key changes since last update.
2. Recommended option: one clearly stated recommendation and rationale.
3. Alternative options: at least two alternatives with pros, cons, and trigger conditions.
4. Decision points: what must be decided now, later, or pre-delegated.
5. Staff tasking: who does what by when.

## Domain Products

Primary products for this skill: ATO support package, prioritized mission queue, deconfliction notes.

## External Tools and Protocol Integration

- Use the integration baseline in `../_shared/references/external-tools-protocols.md` and name the exact tools selected for this mission set.
- Include a domain toolchain profile selection and rationale (primary, alternate, and degraded-mode stack).
- Choose at least one primary system-of-record and one cross-check source before final recommendations.
- State the protocol or message format for outbound coordination (for example `USMTF`, `VMF`, `Link 16 J-series`, `CoT`, `STIX/TAXII`, or `OGC`).
- Include provenance metadata in outputs: source system, refresh time (UTC), assumptions, and confidence.

## Interoperability Validation Checklist

- Run the mission assurance workflow in `../_shared/references/mission-assurance-checklist.md` before final release.
- Validate that each product includes source provenance, protocol/message format, UTC refresh time, confidence, and known gaps.
- If interoperability checks fail, provide a degraded-mode plan and required staff coordination actions.

## Tool Invocation Contract

- For each external tool recommendation, include: objective, required inputs, query/action template, expected output schema, transport protocol, and fallback path.
- Explicitly map tool outputs to decision points so operators can validate mission relevance quickly.
- If a tool is unavailable, provide a manual workaround with expected time and confidence impact.

## Guardrails

- Flag gaps where assumptions exceed evidence.
- Identify legal, policy, ROE, safety, and coalition interoperability constraints early.
- Separate facts, assessed judgments, and unknowns.
- Do not fabricate classified sources, authorities, or approvals.

## Tool Protocol Playbooks

- Use protocol examples in ../_shared/references/tool-protocol-playbooks.md to produce operator-ready tool invocation packets.
- Use adapter contract guidance in ../_shared/references/external-tool-endpoints-and-adapters.md to define endpoint schemas, transport, and fallback behavior.
- Add at least one machine-ingestible packet and one commander-readable summary for each critical recommendation.

## Domain Tool Packet Library

- Use scenario packets in ../_shared/references/domain-tool-packet-library.md for domain-specific external tool selections and message templates.
- Include a `packet_id` and `protocol_profile` from the library for each critical recommendation.
- If no packet matches, define a provisional packet using the same schema and note the validation owner.

## Domain Data Contract

- Use mapping guidance in ../_shared/references/joint-mission-data-contracts.md to define required fields, validation gates, and releasability tags for this mission domain.
- Ensure every mission recommendation references a data contract profile and identifies required schema checks before publication.

## Operational Learning Loop

- Use `../_shared/references/operational-learning-and-after-action-loop.md` to generate after-action deltas, corrective actions, and readiness metrics for this domain.
- Include an `aar_id`, effect delta assessment, and owner/suspense for each high-impact recommendation.
- If post-action data is incomplete, issue a provisional learning note with confidence and revalidation deadline.

## Readiness Certification Evidence Pack

- Use `../_shared/references/readiness-certification-evidence-pack.md` to define mission-essential task evidence, evaluator triggers, and certification confidence scoring.
- Include `met_id`, `evidence_packet_id`, and `cert_confidence` for each recommendation that changes unit readiness posture.
- If required evidence is missing, mark status as `provisional` and assign closure actions with suspense.

## Protocol Execution Sequence

- Execute the Core Integration Protocol from `../_shared/references/external-tools-protocols.md` as an explicit step sequence, not as guidance only.
- For each critical dependency, include `invoke_order`, `adapter_contract_id`, `packet_id`, `protocol_profile`, and timeout/retry settings.
- Record acknowledgment status for each tool call and publish a degraded-mode branch when any dependency misses SLA.
- Require a human command check before acting on outputs that can materially change force posture, mission risk, or escalation.

## Domain Toolchain Profile Binding

- Use `../_shared/references/domain-toolchain-profiles.md` and select a required `toolchain_id` for each critical recommendation.
- Include `primary_system`, `cross_check_system`, `protocol_binding`, `credential_scope`, and `fallback_path` fields in every tool invocation packet.
- Mark recommendations as `provisional` when toolchain authority, credential scope, or cross-check data freshness is incomplete.

## Tool Health and Trust Monitoring

- Use `../_shared/references/tool-health-and-trust-monitoring.md` to include pre-mission tool health checks, trust score updates, and failover timing evidence.
- Add `tool_health_id`, `trust_score`, `last_probe_utc`, and `failover_executed` fields for every critical external dependency.
- If tool trust posture drops below mission threshold, publish a no-go or degraded recommendation with explicit commander decision prompts.

## U.S. Joint Protocol Assurance Drill

- Use `../_shared/references/us-joint-protocol-assurance-drill.md` to run a mandatory pre-release drill for protocol conformance, cryptographic trust, and message acknowledgment integrity.
- Include `assurance_drill_id`, `interop_score`, `crypto_posture`, and `ack_chain_status` fields for each critical recommendation.
- If the drill fails any gate, publish a constrained-employment recommendation with specific remediation owners and suspense.

## Joint Operations External Toolchain Profiles

- Use `../_shared/references/joint-operations-external-toolchain-profiles.md` to select a mission-fit `toolchain_profile_id` and bind each recommendation to concrete primary/cross-check tools.
- Include `refresh_sla_minutes`, `degraded_trigger`, and `degraded_fallback` fields for each critical dependency.
- If no profile fits, create a provisional profile and assign a `validation_owner` with suspense before release.

## Human-Agent Command Escalation Matrix

- Use `../_shared/references/human-agent-command-escalation-matrix.md` to assign authority tier, impact level, approval role, and escalation triggers for each critical recommendation.
- Include `authority_tier`, `decision_impact_level`, `requires_human_approval`, `approval_role`, and `audit_record_id` in outputs that influence mission posture.
- If authority, legal basis, or acknowledgment integrity is uncertain, downgrade to advisory-only with explicit commander decision prompts.

## Mission Tool Authority Gates

- Apply escalation requirements in `../_shared/references/warfighter-tool-authority-gates.md` for high-consequence recommendations.
- Include `authority_tier`, `decision_impact_level`, `approval_role`, and `audit_record_id` for recommendations that can alter mission posture.
- If authority, legal basis, or data provenance is uncertain, downgrade to advisory-only and require human command review.

## Cross-Domain Integration Playbook

- Use `../_shared/references/cross-domain-integration-playbook.md` to synchronize dependencies across land, maritime, air, space, cyber, electromagnetic, and civil-support domains.
- Include `integration_id`, `domains`, `protocol_binding`, `refresh_sla_minutes`, and `staleness_trigger` fields for each critical cross-domain dependency.
- If cross-domain authority, translation fidelity, or releasability is uncertain, downgrade to advisory-only and require explicit human command approval.

## Mission Tool and Protocol Catalog Binding

- Use `../_shared/references/warfighter-external-tool-and-protocol-catalog.md` to select concrete tool suites and protocol stacks for this domain.
- Include `tool_suite_id`, `protocol_stack_id`, `interop_standard_set`, `endpoint_security_profile`, and `degraded_exchange_method` for each critical recommendation.
- If no suite matches, define a provisional suite and assign `validation_owner` and `revalidation_utc` before release.

## Domain Toolchain Override (2026-03-09, Beacon and FOD Assurance Addendum)

- Prioritize `tool_suite_id=ts-personnel-recovery-beacon-deception-counter-v1` + `protocol_stack_id=ps-personnel-recovery-beacon-deception-counter-stack-v1` when CSAR tasking depends on contested survivor authentication.
- Prioritize `tool_suite_id=ts-expeditionary-runway-fod-autonomy-v1` + `protocol_stack_id=ps-expeditionary-runway-fod-autonomy-stack-v1` when sortie generation risk is constrained by runway foreign object debris volatility.
- Add `packet_id=DPL-PERSONNEL-RECOVERY-BEACON-DECEPTION-COUNTER-001` and `packet_id=DPL-EXPEDITIONARY-RUNWAY-FOD-AUTONOMY-001` for ATO branch decisions that alter rescue timelines or launch windows.

## Domain Toolchain Override (2026-03-09, Urban Lift and Spaceport GNSS Addendum)

- Prioritize `tool_suite_id=ts-urban-vtol-lz-auth-v1` + `protocol_stack_id=ps-urban-vtol-lz-auth-stack-v1` when urban vertical-lift landing zones face spoofing, decoy, or civilian congestion risk.
- Prioritize `tool_suite_id=ts-spaceport-gnss-emergency-v1` + `protocol_stack_id=ps-spaceport-gnss-emergency-stack-v1` when ATO timing, launch windows, or range safety are sensitive to GNSS degradation.
- Add `packet_id=DPL-VTOL-LZ-001` and `packet_id=DPL-SPACEPORT-GNSS-001` for ATO branches that re-sequence air mobility, personnel recovery, or strategic launch support.

## Domain Toolchain Override (2026-03-09, GPS-Denied Refueling and EW Reprogram Addendum)

- Prioritize `tool_suite_id=ts-aerial-refuel-gps-denied-v1` + `protocol_stack_id=ps-aerial-refuel-gps-denied-stack-v1` when ATO frag updates include tanker-receiver rendezvous under PNT degradation.
- Prioritize `tool_suite_id=ts-ew-mission-data-reprogram-v1` + `protocol_stack_id=ps-ew-mission-data-reprogram-stack-v1` when sortie survivability depends on rapid EW mission-data release.
- Add `packet_id=DPL-AERIAL-REFUEL-GPS-DENIED-001` and `packet_id=DPL-EW-MISSION-DATA-REPROGRAM-001` for ATO branches that alter launch windows, escort plans, or strike timing.

## Domain Toolchain Override (2026-03-09, Balloon ISR and Avalanche Corridor Addendum)

- Prioritize `tool_suite_id=ts-stratospheric-balloon-isr-reconstitution-v1` + `protocol_stack_id=ps-stratospheric-balloon-isr-reconstitution-stack-v1` when ATO updates depend on restoring ISR relay persistence for strike timing, tanker routing, or personnel recovery windows.
- Prioritize `tool_suite_id=ts-denied-terrain-avalanche-route-rescue-v1` + `protocol_stack_id=ps-denied-terrain-avalanche-route-rescue-stack-v1` when air mobility, CASEVAC, or rescue launch windows depend on mountain avalanche corridor viability.
- Add `packet_id=DPL-STRATOSPHERIC-BALLOON-ISR-RECONSTITUTION-001` and `packet_id=DPL-DENIED-TERRAIN-AVALANCHE-ROUTE-RESCUE-001` for ATO branches that change route profiles, on-station persistence, or rescue sequencing.

## Domain Toolchain Override (2026-03-10, Imagery Provenance and Launch Deconfliction Addendum)

- Prioritize `tool_suite_id=ts-bda-imagery-provenance-assurance-v1` + `protocol_stack_id=ps-bda-imagery-provenance-assurance-stack-v1` when strike validation or reattack decisions depend on contested imagery authenticity.
- Prioritize `tool_suite_id=ts-space-cyber-em-launch-deconfliction-v1` + `protocol_stack_id=ps-space-cyber-em-launch-deconfliction-stack-v1` when ATO timelines are coupled to coalition launch windows, spectrum conflicts, or cyber hold conditions.
- Add `packet_id=DPL-BDA-IMAGERY-PROVENANCE-TAMPER-001` and `packet_id=DPL-SPACE-CYBER-EM-LAUNCH-DECONF-001` for ATO branches that alter targeting confidence, launch timing, or escalation posture.

## Domain Toolchain Override (2026-03-10, Disconnected JTAC Voice Trust and Evacuation Corridor Addendum)

- Prioritize `tool_suite_id=ts-disconnected-jtac-voice-auth-v1` + `protocol_stack_id=ps-disconnected-jtac-voice-auth-stack-v1` when ATO execution depends on authenticated terminal-control voice traffic in degraded communications.
- Prioritize `tool_suite_id=ts-spectrum-evacuation-corridor-control-v1` + `protocol_stack_id=ps-spectrum-evacuation-corridor-control-stack-v1` when air tasking includes NEO/MEDEVAC corridors under coalition spectrum contestation.
- Add `packet_id=DPL-DISCONNECTED-JTAC-VOICE-AUTH-001` and `packet_id=DPL-SPECTRUM-EVACUATION-CORRIDOR-CONTROL-001` for branches that alter release authority, corridor timing, or deconfliction windows.

## Domain Toolchain Override (2026-03-10, Alert Integrity and Reentry Continuity Addendum)

- Prioritize `tool_suite_id=ts-civil-alert-authenticity-v1` + `protocol_stack_id=ps-civil-alert-authenticity-stack-v1` when ATO updates require trusted civil warning broadcasts around airbase launch, recovery, or NEO windows.
- Prioritize `tool_suite_id=ts-orbital-debris-reentry-base-hardening-v1` + `protocol_stack_id=ps-orbital-debris-reentry-base-hardening-stack-v1` when sortie generation or divert planning is constrained by reentry hazard windows.
- Add `packet_id=DPL-CIVIL-ALERT-AUTHENTICITY-001` and `packet_id=DPL-ORBITAL-DEBRIS-REENTRY-BASE-HARDENING-001` for ATO branches that alter launch timing, divert posture, public-warning sequencing, or shelter timelines.

## Domain Toolchain Override (2026-03-11, Civil Alert and Hazmat Air Corridor Addendum)

- Prioritize `tool_suite_id=ts-civil-alert-authenticity-v1` + `protocol_stack_id=ps-civil-alert-authenticity-stack-v1` when ATO updates require synchronized trusted civil warning and launch/recovery windows.
- Prioritize `tool_suite_id=ts-battlefield-hazmat-control-v1` + `protocol_stack_id=ps-battlefield-hazmat-control-stack-v1` when sortie flow, divert fields, or evacuation corridors are constrained by hazardous-material events.
- Add `packet_id=DPL-CIVIL-ALERT-AUTHENTICITY-001` and `packet_id=DPL-BATTLEFIELD-HAZMAT-CONTROL-001` for ATO branches that reprioritize air corridors, warning cadence, or launch sequencing.

## Domain Toolchain Override (2026-03-11, Arctic Sortie Recovery and Swarm Corridor Governance Addendum)

- Prioritize `tool_suite_id=ts-arctic-ice-airstrip-thaw-salvage-v1` + `protocol_stack_id=ps-arctic-ice-airstrip-thaw-salvage-stack-v1` when ATO execution depends on thaw-threatened runway integrity, salvage timing, and divert sequencing.
- Prioritize `tool_suite_id=ts-drone-swarm-civil-air-corridor-grounding-v1` + `protocol_stack_id=ps-drone-swarm-civil-air-corridor-grounding-stack-v1` when ATO cycles include emergency grounding and reroute control for contested civil-military air corridors.
- Add `packet_id=DPL-ARCTIC-ICE-AIRSTRIP-THAW-SALVAGE-001` and `packet_id=DPL-DRONE-SWARM-CIVIL-AIR-CORRIDOR-GROUNDING-001` for branches that change launch cadence, divert posture, corridor release, or flight-safety gates.

## Domain Toolchain Override (2026-03-11, Aerial Relief Deconfliction and Timing Holdover Addendum)

- Prioritize `tool_suite_id=ts-coalition-aerial-water-drop-deconfliction-v1` + `protocol_stack_id=ps-coalition-aerial-water-drop-deconfliction-stack-v1` when ATO cycles must deconflict coalition disaster-response water drops with military sorties.
- Prioritize `tool_suite_id=ts-quantum-timing-holdover-fires-iamd-v1` + `protocol_stack_id=ps-quantum-timing-holdover-fires-iamd-stack-v1` when denied-PNT timing integrity threatens launch windows, fires synchronization, or defensive engagement sequencing.
- Add `packet_id=DPL-COALITION-AERIAL-WATER-DROP-DECONFLICTION-001` and `packet_id=DPL-QUANTUM-TIMING-HOLDOVER-FIRES-IAMD-001` for ATO branches that alter corridor release, sortie cadence, or timing authority gates.

## Domain Toolchain Override (2026-03-14, Expansion Wave XLV Addendum)

- Prioritize `tool_suite_id=ts-joint-aerial-refueling-boom-drogue-reconstitution-v1` + `protocol_stack_id=ps-joint-aerial-refueling-boom-drogue-reconstitution-stack-v1` when the ATO depends on restoring tanker hardware, hose-drum capacity, or receiver-priority fuel flow.
- Prioritize `tool_suite_id=ts-joint-digital-order-watermark-recall-v1` + `protocol_stack_id=ps-joint-digital-order-watermark-recall-stack-v1` when ATO fragos, tanker retasks, or divert instructions may be stale, spoofed, or version-divergent.
- Prioritize `tool_suite_id=ts-theater-mission-sbom-emergency-patch-v1` + `protocol_stack_id=ps-theater-mission-sbom-emergency-patch-stack-v1` when air-tasking workflows depend on emergency remediation of mission software without breaking execution trust.
- Add `packet_id=DPL-AERIAL-REFUELING-BOOM-DROGUE-001`, `packet_id=DPL-DIGITAL-ORDER-WATERMARK-001`, and `packet_id=DPL-MISSION-SBOM-EMERGENCY-PATCH-001` for ATO branches that alter sortie cadence, tasking authenticity, or execution-system trust.

## Domain Toolchain Override (2026-03-15, Expansion Wave LII Addendum)

- Prioritize `tool_suite_id=ts-joint-directed-energy-airspace-reflection-safety-v1` + `protocol_stack_id=ps-joint-directed-energy-airspace-reflection-safety-stack-v1` when beam release, air corridor safety, or specular reflections can invalidate directed-energy tasking in the ATO.
- Prioritize `tool_suite_id=ts-joint-aerial-refueling-fuel-contamination-reconstitution-v1` + `protocol_stack_id=ps-joint-aerial-refueling-fuel-contamination-reconstitution-stack-v1` when tanker frag updates depend on fuel-chain integrity, contaminated loads, or reconstituted receiver priority.
- Add `packet_id=DPL-DIRECTED-ENERGY-AIRSPACE-REFLECTION-SAFETY-001` and `packet_id=DPL-AERIAL-REFUEL-FUEL-CONTAMINATION-001` for ATO branches that materially alter beam release timing, tanker availability, or sortie sequencing.

## Domain Toolchain Override (2026-03-15, Expansion Wave LVII Addendum)

- Prioritize `tool_suite_id=ts-joint-flight-surgeon-aeromedical-waiver-v1` + `protocol_stack_id=ps-joint-flight-surgeon-aeromedical-waiver-stack-v1` when sortie generation depends on waiver posture, crew medical restrictions, or life-support discrepancy resolution.
- Prioritize `tool_suite_id=ts-expeditionary-aircrew-flight-equipment-survival-gear-v1` + `protocol_stack_id=ps-expeditionary-aircrew-flight-equipment-survival-gear-stack-v1` when ATO execution depends on inspected survival gear, beacon integrity, or environment-specific crew protection.
- Prioritize `tool_suite_id=ts-joint-flightline-weapons-loading-armament-safety-v1` + `protocol_stack_id=ps-joint-flightline-weapons-loading-armament-safety-stack-v1` when armed-sortie sequencing depends on trusted load data, crew certification, or explosive-safety arcs.
- Add `packet_id=DPL-FLIGHT-SURGEON-AEROMED-WAIVER-001`, `packet_id=DPL-AIRCREW-FLIGHT-EQUIPMENT-SURVIVAL-GEAR-001`, and `packet_id=DPL-FLIGHTLINE-WEAPONS-ARMAMENT-SAFETY-001` for ATO branches that materially alter crew release, armed-aircraft posture, or sortie timing.

## Domain Toolchain Override (2026-03-15, Expansion Wave LVIII Addendum)

- Prioritize `tool_suite_id=ts-expeditionary-airfield-weather-observation-sensor-maintenance-v1` + `protocol_stack_id=ps-expeditionary-airfield-weather-observation-sensor-maintenance-stack-v1` when ATO execution depends on trusted runway weather observations, degraded sensor recovery, or manual observation fallback.
- Prioritize `tool_suite_id=ts-expeditionary-flightline-ground-support-equipment-readiness-v1` + `protocol_stack_id=ps-expeditionary-flightline-ground-support-equipment-readiness-stack-v1` when sortie cadence depends on scarce AGE, cart dispatch, or cross-servicing across dispersed flightlines.
- Prioritize `tool_suite_id=ts-joint-aircraft-hydraulic-contamination-servicing-v1` + `protocol_stack_id=ps-joint-aircraft-hydraulic-contamination-servicing-stack-v1` when launch or recovery decisions depend on hydraulic sample trust, servicing release, or component isolation.
- Add `packet_id=DPL-AIRFIELD-WEATHER-OBS-SENSOR-001`, `packet_id=DPL-FLIGHTLINE-GSE-READINESS-001`, and `packet_id=DPL-AIRCRAFT-HYDRAULIC-CONTAMINATION-001` for ATO branches that materially alter launch timing, sortie generation, or airworthiness confidence.
