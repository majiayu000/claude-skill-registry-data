---
name: contested-logistics-sustainment
description: Plan sustainment under contested conditions. Use when designing resupply methods, pre-positioning, and distribution resilience for degraded or denied environments.
---

# Contested Logistics Sustainment

## Mission Scope

- Treat this skill as a planning and decision-support aid for U.S. warfighter missions in its domain.
- Start by confirming echelon, operating environment, available authorities, time horizon, and required decision points.
- Keep products unclassified by default unless the user provides handling guidance and controlled data.

## Workflow

1. Frame the mission problem using these core inputs: consumption rates, route threats, stock levels, transport assets.
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

Primary products for this skill: sustainment posture plan, resupply branch options, critical-shortfall forecast.

## Domain Tool Stack

Use these tool categories as the default stack for this skill: movement and distribution control systems, stockpile and consumption analytics, convoy and route risk dashboards.

## Protocol Profile

Preferred protocol families for this skill: USMTF, API/JSON, OGC.

## Domain Toolchain Defaults

- Primary: `tool_suite_id=ts-logistics-distribution-v1` with `protocol_stack_id=ps-joint-tactical-link-stack-v1`.
- Alternate: `tool_suite_id=ts-maritime-undersea-v1` with `protocol_stack_id=ps-geo-maritime-stack-v1`.
- Degraded: mission-essential sustainment board with manual reconciliation and scheduled command confirmations.

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

## Domain Packet Defaults

- Default packet IDs: `DPL-PORT-REPAIR-001`, `DPL-INTERMODAL-RAIL-AIR-001`, `DPL-FUEL-LEAK-ATTRIB-001`.
- If no packet fully matches, define a provisional packet and assign a validation owner before release.

## Operational Execution Hardening

- Enforce `ack_chain_status=verified` for all mission-critical tool exchanges before recommending posture changes.
- Require `trust_score >= 0.80` on each primary external dependency; if lower, elevate alternate stack and mark outputs `provisional`.
- Add explicit degraded-mode triggers: stale data beyond `refresh_sla_minutes`, missing cryptographic validation, or failed human approval gate.
- Include a final command-ready line: `GO`, `NO-GO`, or `GO-WITH-CONSTRAINTS` with rationale tied to authority and protocol checks.

## Logistics Continuity Addendum (2026-03-08)

- For Arctic or littoral denial scenarios, bind `tool_suite_id=ts-under-ice-resupply-v1` with `protocol_stack_id=ps-under-ice-resupply-stack-v1`.
- For strategic sealift availability stress, add `tool_suite_id=ts-maritime-insurance-reconstitution-v1` with `protocol_stack_id=ps-maritime-insurance-reconstitution-stack-v1`.
- For sustainment plans with life-support dependencies, include `packet_id=DPL-RARE-BLOOD-MATCH-001` as a mandatory medical-logistics cross-check.

## Logistics Continuity Addendum (2026-03-08, Fuel and Critical Cargo Integrity)

- Add `tool_suite_id=ts-denied-fuel-bladder-integrity-v1` + `protocol_stack_id=ps-denied-fuel-bladder-integrity-stack-v1` for forward fuel-storage reliability and sabotage detection.
- Add `packet_id=DPL-CRITICAL-MINERAL-SHIPPING-001` when sustainment courses of action depend on strategic material flow continuity.
- Add `packet_id=DPL-MICROREACTOR-EMPLOY-001` when expeditionary power constraints materially change sustainment branch feasibility.

## Logistics Continuity Addendum (2026-03-08, Signature and Feedstock Integrity)

- Add `tool_suite_id=ts-logistics-signature-masking-v1` + `protocol_stack_id=ps-logistics-signature-masking-stack-v1` when convoy detectability is a primary sustainment risk.
- Add `packet_id=DPL-ADDITIVE-FEEDSTOCK-AUTH-001` for sustainment plans that rely on additive repair or microfactory throughput.
- Add `packet_id=DPL-SEMICONDUCTOR-FAB-CONTINGENCY-001` when strategic electronics shortages can cascade into theater sustainment delays.

## Logistics Continuity Addendum (2026-03-10, Port Recovery and Rail Priority Merge)

- Add `tool_suite_id=ts-port-crane-cyber-physical-recovery-v1` + `protocol_stack_id=ps-port-crane-cyber-physical-recovery-stack-v1` when sustainment throughput depends on contested port crane restoration and OT safety controls.
- Add `tool_suite_id=ts-civil-rail-evac-priority-merge-v1` + `protocol_stack_id=ps-civil-rail-evac-priority-merge-stack-v1` when military sustainment movement must be synchronized with life-safety rail evacuation demand.
- Add `packet_id=DPL-PORT-CRANE-CYBER-PHYSICAL-RECOVERY-001` and `packet_id=DPL-CIVIL-RAIL-EVAC-PRIORITY-MERGE-001` for sustainment branches that alter port unloading cadence, rail throughput, or distribution sequencing.

## Logistics Continuity Addendum (2026-03-12, Arctic Rescue, Munitions Safety, and Coalition Cascade Response)

- Add `tool_suite_id=ts-arctic-sar-medical-auth-v1` + `protocol_stack_id=ps-arctic-sar-medical-auth-stack-v1` when sustainment plans include contested Arctic personnel recovery and hypothermia-driven casualty routing.
- Add `tool_suite_id=ts-munitions-energetics-dispersal-v1` + `protocol_stack_id=ps-munitions-energetics-dispersal-stack-v1` when munitions safety compatibility and depot dispersal timing drive sustainment feasibility.
- Add `tool_suite_id=ts-coalition-infra-cyber-kinetic-cascade-v1` + `protocol_stack_id=ps-coalition-infra-cyber-kinetic-cascade-stack-v1` when sustainment continuity depends on coalition infrastructure restoration after cyber-kinetic shocks.
- Add `packet_id=DPL-ARCTIC-SAR-MEDAUTH-001`, `packet_id=DPL-MUNITIONS-ENERGETICS-DISPERSAL-001`, and `packet_id=DPL-COALITION-CYBER-KINETIC-CASCADE-001` for branches that materially change throughput confidence, life-support posture, or mission sustainment viability.

## Domain Toolchain Override (2026-03-12, Expansion Wave XXIV Addendum)

- Add `tool_suite_id=ts-theater-autonomous-fortification-print-farm-v1` + `protocol_stack_id=ps-theater-autonomous-fortification-print-farm-stack-v1` when contested sustainment must prioritize distributed fortification and engineer support output.
- Add `tool_suite_id=ts-strategic-rare-gas-energetic-precursor-allocation-v1` + `protocol_stack_id=ps-strategic-rare-gas-energetic-precursor-allocation-stack-v1` when sustainment feasibility depends on energetic precursor flow assurance.
- Add `packet_id=DPL-THEATER-FORTIFICATION-PRINTFARM-001` and `packet_id=DPL-STRATEGIC-RAREGAS-ENERGETICS-002` for logistics branches that hinge on industrial throughput confidence.

## Domain Toolchain Override (2026-03-12, Expansion Wave XXV Addendum)

- Prioritize `tool_suite_id=ts-joint-cislunar-logistics-interdiction-reconstitution-v1` with `protocol_stack_id=ps-joint-cislunar-logistics-interdiction-reconstitution-stack-v1` when strategic space logistics, custody confidence, or cislunar maneuver assurance directly affect mission risk decisions.
- Add `tool_suite_id=ts-theater-underwater-datacenter-cooling-grid-defense-v1` with `protocol_stack_id=ps-theater-underwater-datacenter-cooling-grid-defense-stack-v1` when mission outcomes depend on underwater compute resilience, cooling continuity, or cyber-physical load restoration.
- Add `packet_id=DPL-CISLUNAR-LOGISTICS-INTERDICTION-001` and `packet_id=DPL-UNDERWATER-DATACENTER-COOLING-DEFENSE-001` for recommendations that alter mission posture, contingency branches, or strategic continuity authorities.

## Domain Toolchain Override (2026-03-13, Expansion Wave XL Addendum)

- Add `tool_suite_id=ts-coalition-merchant-marine-crew-vetting-sealift-assurance-v1` + `protocol_stack_id=ps-coalition-merchant-marine-crew-vetting-sealift-assurance-stack-v1` when sustainment viability depends on merchant crew trust, sanctions compliance, or coalition sealift release timing.
- Add `tool_suite_id=ts-strategic-contested-lng-bunker-fleet-fuel-allocation-v1` + `protocol_stack_id=ps-strategic-contested-lng-bunker-fleet-fuel-allocation-stack-v1` when contested maritime fuel access and bunkering confidence determine sustainment feasibility.
- Add `tool_suite_id=ts-strategic-commercial-port-crane-firmware-rollback-sealift-recovery-v1` + `protocol_stack_id=ps-strategic-commercial-port-crane-firmware-rollback-sealift-recovery-stack-v1` when port OT recovery and berth release directly constrain theater throughput.
- Add `tool_suite_id=ts-theater-rapid-temporary-bridge-uas-inspection-release-v1` + `protocol_stack_id=ps-theater-rapid-temporary-bridge-uas-inspection-release-stack-v1` when force-flow branches depend on rapid bridge release and structural-confidence restoration.
- Add `packet_id=DPL-COALITION-MERCHANT-MARINE-CREW-VETTING-SEALIFT-001`, `packet_id=DPL-STRATEGIC-LNG-BUNKER-FLEET-FUEL-ALLOCATION-001`, `packet_id=DPL-STRATEGIC-PORT-CRANE-FIRMWARE-ROLLBACK-SEALIFT-001`, and `packet_id=DPL-THEATER-TEMPORARY-BRIDGE-UAS-RELEASE-001` for sustainment branches that materially alter throughput confidence or mission feasibility.

## Domain Toolchain Override (2026-03-14, Expansion Wave XLI Addendum)

- Add `tool_suite_id=ts-strategic-domestic-transport-chokepoint-reroute-v1` + `protocol_stack_id=ps-strategic-domestic-transport-chokepoint-reroute-stack-v1` when homeland transport failures materially alter theater sustainment timelines or reception and onward movement confidence.
- Add `tool_suite_id=ts-expeditionary-autonomous-sustainment-routing-drift-governance-v1` + `protocol_stack_id=ps-expeditionary-autonomous-sustainment-routing-drift-governance-stack-v1` when convoy viability depends on autonomy trust, telemetry confidence, or route drift containment.
- Add `tool_suite_id=ts-strategic-shipyard-drydock-power-water-cyber-restoration-v1` + `protocol_stack_id=ps-strategic-shipyard-drydock-power-water-cyber-restoration-stack-v1` when fleet repair throughput and maritime sustainment depend on drydock utilities and OT recovery.
- Add `tool_suite_id=ts-theater-river-port-dredge-barge-roro-sustainment-v1` + `protocol_stack_id=ps-theater-river-port-dredge-barge-roro-sustainment-stack-v1` when inland-waterway cargo flow, channel depth, or transload timing drives sustainment feasibility.
- Add `packet_id=DPL-STRATEGIC-DOMESTIC-TRANSPORT-CHOKEPOINT-REROUTE-001`, `packet_id=DPL-EXPEDITIONARY-AUTONOMOUS-SUSTAINMENT-ROUTING-DRIFT-001`, `packet_id=DPL-STRATEGIC-SHIPYARD-DRYDOCK-RESTORATION-001`, and `packet_id=DPL-THEATER-RIVER-PORT-DREDGE-BARGE-RORO-001` for sustainment branches that materially alter throughput confidence or mission feasibility.

## Domain Toolchain Override (2026-03-14, Expansion Wave XLII Addendum)

- Add `tool_suite_id=ts-coalition-allied-depot-sabotage-wargame-v1` + `protocol_stack_id=ps-coalition-allied-depot-sabotage-wargame-stack-v1` when sustainment viability depends on depot survivability, stock relocation, or host-nation recovery branches.
- Add `tool_suite_id=ts-strategic-economic-coercion-logistics-warning-v1` + `protocol_stack_id=ps-strategic-economic-coercion-logistics-warning-stack-v1` when route, carrier, supplier, or insurer coercion indicators can fracture distribution plans before physical disruption is visible.
- Add `tool_suite_id=ts-strategic-launch-counterfeit-microelectronics-v1` + `protocol_stack_id=ps-strategic-launch-counterfeit-microelectronics-stack-v1` when logistics confidence depends on trusted electronics pedigree for critical launch, C2, or sustainment systems.
- Add `packet_id=DPL-DEPOT-SABOTAGE-WARGAME-001`, `packet_id=DPL-ECON-COERCION-LOGISTICS-001`, and `packet_id=DPL-LAUNCH-COUNTERFEIT-MICRO-001` for branches that materially alter throughput, reconstitution timing, or commander risk acceptance.

## Domain Toolchain Override (2026-03-14, Expansion Wave XLIII Addendum)

- Add `tool_suite_id=ts-theater-bulk-industrial-gas-oxygen-priority-v1` + `protocol_stack_id=ps-theater-bulk-industrial-gas-oxygen-priority-stack-v1` when sustainment viability depends on bulk gas purity, refill capacity, or contested transport to medical and maintenance nodes.
- Add `tool_suite_id=ts-strategic-harbor-tug-pilotage-sealift-priority-v1` + `protocol_stack_id=ps-strategic-harbor-tug-pilotage-sealift-priority-stack-v1` when tug and pilotage scarcity becomes the limiting factor for sealift throughput.
- Add `tool_suite_id=ts-homeland-defense-specialty-lubricant-hydraulic-fluid-allocation-v1` + `protocol_stack_id=ps-homeland-defense-specialty-lubricant-hydraulic-fluid-allocation-stack-v1` when specialty-fluid shortages or contamination directly constrain mission-capable rates and depot output.
- Add `packet_id=DPL-INDUSTRIAL-GAS-OXYGEN-PRIORITY-001`, `packet_id=DPL-HARBOR-TUG-PILOTAGE-SEALIFT-001`, and `packet_id=DPL-LUBRICANT-HYDRAULIC-ALLOCATION-001` for branches that materially alter sustainment throughput, life-support posture, or commander risk acceptance.

## Domain Toolchain Override (2026-03-14, Expansion Wave XLIV Addendum)

- Add `tool_suite_id=ts-strategic-photonics-laser-optics-allocation-v1` + `protocol_stack_id=ps-strategic-photonics-laser-optics-allocation-stack-v1` when sustainment feasibility depends on scarce EO materials for sensors, laser systems, or electro-optical repair.
- Add `tool_suite_id=ts-homeland-rail-hazmat-military-priority-deconfliction-v1` + `protocol_stack_id=ps-homeland-rail-hazmat-military-priority-deconfliction-stack-v1` when rail dispatch must reconcile military throughput with hazardous-material controls and civil emergency constraints.
- Add `tool_suite_id=ts-joint-airbase-arresting-gear-runway-cable-reconstitution-v1` + `protocol_stack_id=ps-joint-airbase-arresting-gear-runway-cable-reconstitution-stack-v1` when airbase sustainment, sortie recovery, or runway-end cable integrity becomes the bottleneck for operational tempo.
- Add `packet_id=DPL-PHOTONICS-LASER-OPTICS-ALLOCATION-001`, `packet_id=DPL-RAIL-HAZMAT-MILPRIORITY-DECONFLICTION-001`, and `packet_id=DPL-ARRESTING-GEAR-RUNWAY-CABLE-001` for branches that materially alter sustainment throughput, sortie regeneration, or commander risk acceptance.

## Domain Toolchain Override (2026-03-14, Expansion Wave XLVI Addendum)

- Add `tool_suite_id=ts-strategic-fuel-additive-adulteration-interdiction-v1` + `protocol_stack_id=ps-strategic-fuel-additive-adulteration-interdiction-stack-v1` when sustainment viability depends on trusted fuel-additive pedigree, contamination quarantine, or substitute blending decisions.
- Add `tool_suite_id=ts-expeditionary-high-latitude-battery-thermal-survivability-v1` + `protocol_stack_id=ps-expeditionary-high-latitude-battery-thermal-survivability-stack-v1` when cold-soaked batteries, charging windows, or low-insolation power limits threaten logistics nodes and autonomous sustainment.
- Add `tool_suite_id=ts-autonomous-breach-soil-bearing-route-classification-v1` + `protocol_stack_id=ps-autonomous-breach-soil-bearing-route-classification-stack-v1` when engineer or heavy-vehicle throughput depends on trusted soil-bearing classifications before route release.
- Add `packet_id=DPL-FUEL-ADDITIVE-ADULTERATION-001`, `packet_id=DPL-HIGH-LATITUDE-BATTERY-THERMAL-001`, and `packet_id=DPL-BREACH-SOIL-BEARING-001` for branches that materially alter sustainment throughput, energy continuity, or route-release confidence.

## Domain Toolchain Override (2026-03-14, Expansion Wave XLVIII Addendum)

- Add `tool_suite_id=ts-theater-autonomous-decoy-economy-inventory-governance-v1` + `protocol_stack_id=ps-theater-autonomous-decoy-economy-inventory-governance-stack-v1` when sustainment survivability depends on pacing decoy expenditure, regeneration, or deception coverage across logistics nodes.
- Add `tool_suite_id=ts-coalition-fuel-energy-water-nexus-anomaly-adjudication-v1` + `protocol_stack_id=ps-coalition-fuel-energy-water-nexus-anomaly-adjudication-stack-v1` when contested sustainment depends on distinguishing sabotage, utility cascade, or distribution failure across fuel, power, and water systems.
- Add `tool_suite_id=ts-joint-aerial-port-battery-hazmat-pallet-integrity-v1` + `protocol_stack_id=ps-joint-aerial-port-battery-hazmat-pallet-integrity-stack-v1` when throughput depends on safe release of battery cargo, hazmat consignments, or palletized sustainment loads.
- Add `packet_id=DPL-AUTONOMOUS-DECOY-ECONOMY-001`, `packet_id=DPL-FEW-NEXUS-ANOMALY-001`, and `packet_id=DPL-AERIAL-PORT-HAZMAT-PALLET-001` for branches that materially alter sustainment survivability, utility continuity, or air-logistics throughput.

## Domain Toolchain Override (2026-03-14, Expansion Wave XLIX Addendum)

- Add `tool_suite_id=ts-strategic-undersea-cable-repair-ship-escort-priority-v1` + `protocol_stack_id=ps-strategic-undersea-cable-repair-ship-escort-priority-stack-v1` when sustainment C2, reroute authority, or distribution continuity depends on restoring contested cable infrastructure.
- Add `tool_suite_id=ts-theater-offshore-energy-platform-blackstart-defense-v1` + `protocol_stack_id=ps-theater-offshore-energy-platform-blackstart-defense-stack-v1` when sustainment viability depends on offshore power, fuel, or maritime energy-node restart sequencing.
- Add `packet_id=DPL-CABLE-REPAIR-SHIP-ESCORT-001` and `packet_id=DPL-OFFSHORE-ENERGY-BLACKSTART-001` for branches that materially alter distribution confidence, energy continuity, or commander sustainment risk acceptance.

## Domain Toolchain Override (2026-03-15, Expansion Wave LI Addendum)

- Add `tool_suite_id=ts-theater-property-book-sensitive-item-recapture-v1` + `protocol_stack_id=ps-theater-property-book-sensitive-item-recapture-stack-v1` when sustainment feasibility depends on recovering or denying compromised vehicles, weapons, optics, crypto, or other accountable materiel.
- Add `packet_id=DPL-PROPERTY-BOOK-SENSITIVE-ITEM-RECAPTURE-001` for branches that materially alter accountability confidence, reissue timing, or commander acceptance of compromise risk.

## Domain Toolchain Override (2026-03-15, Expansion Wave LII Addendum)

- Add `tool_suite_id=ts-homeland-tsunami-port-closure-sealift-regeneration-v1` + `protocol_stack_id=ps-homeland-tsunami-port-closure-sealift-regeneration-stack-v1` when sustainment feasibility depends on regenerating sealift throughput after tsunami-driven berth or channel loss.
- Add `tool_suite_id=ts-coalition-host-nation-rail-signaling-manual-block-reversion-v1` + `protocol_stack_id=ps-coalition-host-nation-rail-signaling-manual-block-reversion-stack-v1` when rail dispatch degradation, host-nation signaling loss, or manual-block reversion drive force-flow risk.
- Add `packet_id=DPL-TSUNAMI-PORT-SEALIFT-REGEN-001` and `packet_id=DPL-RAIL-SIGNALING-MANUAL-BLOCK-001` for branches that materially alter throughput confidence, inland transload posture, or coalition movement timing.

## Domain Toolchain Override (2026-03-15, Expansion Wave LIII Addendum)

- Add `tool_suite_id=ts-theater-reproductive-health-contraception-sti-readiness-v1` + `protocol_stack_id=ps-theater-reproductive-health-contraception-sti-readiness-stack-v1` when sustainment feasibility depends on protected pharmacy continuity, diagnostic kit flow, or privacy-safe reproductive-health support.
- Add `tool_suite_id=ts-expeditionary-barracks-hvac-mold-indoor-air-quality-v1` + `protocol_stack_id=ps-expeditionary-barracks-hvac-mold-indoor-air-quality-stack-v1` when housing habitability, barracks relocation, or respiratory-risk controls materially affect force availability and throughput.
- Add `tool_suite_id=ts-joint-foot-health-trench-foot-load-bearing-readiness-v1` + `protocol_stack_id=ps-joint-foot-health-trench-foot-load-bearing-readiness-stack-v1` when boot or sock resupply, march endurance, or immersion-foot risk directly changes force-flow confidence.
- Add `packet_id=DPL-REPRODUCTIVE-HEALTH-STI-READINESS-001`, `packet_id=DPL-BARRACKS-HVAC-MOLD-IAQ-001`, and `packet_id=DPL-FOOT-HEALTH-TRENCH-FOOT-001` for branches that materially alter protected-medical sustainment, housing posture, or movement endurance.

## Domain Toolchain Override (2026-03-15, Expansion Wave LV Addendum)

- Add `tool_suite_id=ts-expeditionary-hydrogen-production-storage-blast-safety-v1` + `protocol_stack_id=ps-expeditionary-hydrogen-production-storage-blast-safety-stack-v1` when sustainment posture depends on hydrogen-enabled power continuity, standoff controls, or explosive-safety limits at forward nodes.
- Add `tool_suite_id=ts-joint-deployed-finance-cash-payroll-disbursing-continuity-v1` + `protocol_stack_id=ps-joint-deployed-finance-cash-payroll-disbursing-continuity-stack-v1` when cash handling, payroll continuity, or disbursing resilience directly affects sustainment labor and contractor throughput.
- Add `tool_suite_id=ts-theater-battle-damage-contracting-vendor-vetting-payment-v1` + `protocol_stack_id=ps-theater-battle-damage-contracting-vendor-vetting-payment-stack-v1` when sustainment recovery depends on rapid local contracting, fraud-resistant payment, or vendor trust under battle damage.
- Add `packet_id=DPL-HYDROGEN-PRODUCTION-BLAST-SAFETY-001`, `packet_id=DPL-DEPLOYED-FINANCE-DISBURSING-001`, and `packet_id=DPL-BATTLE-DAMAGE-CONTRACTING-VENDOR-001` for branches that materially alter energy continuity, sustainment labor confidence, or recovery throughput.

## Domain Toolchain Override (2026-03-15, Expansion Wave LVII Addendum)

- Add `tool_suite_id=ts-expeditionary-prime-power-generator-load-balance-v1` + `protocol_stack_id=ps-expeditionary-prime-power-generator-load-balance-stack-v1` when sustainment feasibility depends on generator repair tempo, load-balance discipline, or priority-circuit continuity.
- Add `tool_suite_id=ts-joint-sling-load-external-lift-certification-v1` + `protocol_stack_id=ps-joint-sling-load-external-lift-certification-stack-v1` when throughput depends on external-lift release confidence for austere resupply or obstacle-bypassing movement.
- Add `tool_suite_id=ts-joint-small-craft-riverine-maintenance-spares-v1` + `protocol_stack_id=ps-joint-small-craft-riverine-maintenance-spares-stack-v1` when inland-waterway or littoral sustainment depends on scarce watercraft spares and maintenance recovery.
- Add `tool_suite_id=ts-joint-cold-weather-clothing-frostbite-discipline-v1` + `protocol_stack_id=ps-joint-cold-weather-clothing-frostbite-discipline-stack-v1` when force endurance, exposure control, or cold-weather issue posture materially constrains sustainment output.
- Add `packet_id=DPL-PRIME-POWER-GENERATOR-LOAD-BALANCE-001`, `packet_id=DPL-SLING-LOAD-EXTERNAL-LIFT-001`, `packet_id=DPL-SMALL-CRAFT-RIVERINE-MAINT-SPARES-001`, and `packet_id=DPL-COLD-WEATHER-CLOTHING-FROSTBITE-001` for branches that materially alter throughput, power continuity, inland-waterway reach, or cold-weather sustainment confidence.

## Domain Toolchain Override (2026-03-15, Expansion Wave LVIII Addendum)

- Add `tool_suite_id=ts-theater-heavy-drop-platform-rigging-retrograde-recovery-v1` + `protocol_stack_id=ps-theater-heavy-drop-platform-rigging-retrograde-recovery-stack-v1` when sustainment viability depends on heavy-drop release confidence, extraction-system health, or contested recovery of outsized cargo.
- Add `tool_suite_id=ts-joint-ammunition-surveillance-lot-serviceability-v1` + `protocol_stack_id=ps-joint-ammunition-surveillance-lot-serviceability-stack-v1` when throughput depends on trusted ammunition issue posture, defect adjudication, or lot quarantine discipline.
- Add `tool_suite_id=ts-expeditionary-ribbon-bridge-maintenance-raft-launch-v1` + `protocol_stack_id=ps-expeditionary-ribbon-bridge-maintenance-raft-launch-stack-v1` when wet-gap sustainment depends on bridge-bay serviceability, raft-launch cadence, or current-sensitive maintenance recovery.
- Add `tool_suite_id=ts-expeditionary-flightline-ground-support-equipment-readiness-v1` + `protocol_stack_id=ps-expeditionary-flightline-ground-support-equipment-readiness-stack-v1` when air sustainment nodes depend on scarce AGE, cart dispatch, or cross-servicing to maintain sortie throughput.
- Add `packet_id=DPL-HEAVY-DROP-PLATFORM-RIGGING-001`, `packet_id=DPL-AMMUNITION-SURVEILLANCE-LOT-001`, `packet_id=DPL-RIBBON-BRIDGE-RAFT-LAUNCH-001`, and `packet_id=DPL-FLIGHTLINE-GSE-READINESS-001` for branches that materially alter airdrop capacity, ammunition availability, wet-gap throughput, or expeditionary air-node sustainment confidence.

## Domain Toolchain Override (2026-03-15, Expansion Wave LX Addendum)

- Add `tool_suite_id=ts-theater-ammunition-yard-fire-compatibility-v1` + `protocol_stack_id=ps-theater-ammunition-yard-fire-compatibility-stack-v1` when sustainment feasibility depends on ammunition-yard survivability, emergency separation, or alternate issue-point activation.
- Add `packet_id=DPL-AMMUNITION-YARD-FIRE-COMPATIBILITY-001` for branches that materially alter munitions availability, force-protection posture, or depot throughput.

## Domain Toolchain Override (2026-03-15, Expansion Wave LXI Addendum)

- Add `tool_suite_id=ts-theater-aviation-fuel-lab-contamination-clearance-v1` + `protocol_stack_id=ps-theater-aviation-fuel-lab-contamination-clearance-stack-v1` when sustainment viability depends on trusted aviation fuel, contamination quarantine, or sortie-support release timing.
- Add `tool_suite_id=ts-joint-arctic-ice-pilotage-mariner-fatigue-v1` + `protocol_stack_id=ps-joint-arctic-ice-pilotage-mariner-fatigue-stack-v1` when high-latitude sustainment routes depend on ice pilotage confidence, fatigue controls, or convoy release timing.
- Add `tool_suite_id=ts-homeland-port-war-risk-insurance-claims-v1` + `protocol_stack_id=ps-homeland-port-war-risk-insurance-claims-stack-v1` when sustainment throughput depends on insurer trigger logic, cargo claims routing, or restored commercial confidence at strategic ports.
- Add `packet_id=DPL-AVIATION-FUEL-LAB-CLEARANCE-001`, `packet_id=DPL-ARCTIC-ICE-PILOTAGE-FATIGUE-001`, and `packet_id=DPL-PORT-WAR-RISK-CLAIMS-001` for branches that materially alter throughput confidence, convoy timing, or air-logistics availability.

## Domain Toolchain Override (2026-03-15, Expansion Wave LXIV Addendum)

- Add `tool_suite_id=ts-joint-reefer-container-cold-chain-denied-port-restoration-v1` + `protocol_stack_id=ps-joint-reefer-container-cold-chain-denied-port-restoration-stack-v1` when sustainment continuity depends on reefer power, berth restoration, or temperature-sensitive cargo survival.
- Add `tool_suite_id=ts-joint-littoral-hydrographic-survey-beach-lane-recertification-v1` + `protocol_stack_id=ps-joint-littoral-hydrographic-survey-beach-lane-recertification-stack-v1` when over-the-shore distribution depends on refreshed bathymetry, lane certification, or connector draft confidence.
- Add `tool_suite_id=ts-strategic-cash-vault-disconnected-pay-agent-anti-diversion-v1` + `protocol_stack_id=ps-strategic-cash-vault-disconnected-pay-agent-anti-diversion-stack-v1` when sustainment labor or contractor availability depends on emergency payroll, cash custody, or anti-diversion controls.
- Add `tool_suite_id=ts-coalition-ration-dietary-compliance-allergen-assurance-v1` + `protocol_stack_id=ps-coalition-ration-dietary-compliance-allergen-assurance-stack-v1` when sustainment legitimacy depends on compliant feeding plans, allergen traceability, or coalition ration substitutions.
- Add `packet_id=DPL-REEFER-COLD-CHAIN-001`, `packet_id=DPL-HYDRO-BEACH-LANE-001`, `packet_id=DPL-CASH-VAULT-ANTIDIVERSION-001`, and `packet_id=DPL-RATION-ALLERGEN-001` for branches that materially alter throughput confidence, over-the-shore access, sustainment labor stability, or coalition feeding viability.

## Domain Toolchain Override (2026-03-15, Expansion Wave LXII Addendum)

- Add `tool_suite_id=ts-theater-disconnected-additive-repair-intent-validation-v1` + `protocol_stack_id=ps-theater-disconnected-additive-repair-intent-validation-stack-v1` when sustainment viability depends on trusted field manufacturing, disconnected work-order pedigree, or emergency part substitutions.
- Add `tool_suite_id=ts-strategic-rare-gas-cryogenic-supply-priority-v1` + `protocol_stack_id=ps-strategic-rare-gas-cryogenic-supply-priority-stack-v1` when industrial or missile-support sustainment depends on cryogenic gas purity, boil-off control, or allocation authority.
- Add `tool_suite_id=ts-coalition-arctic-bulk-fuel-blending-freeze-point-assurance-v1` + `protocol_stack_id=ps-coalition-arctic-bulk-fuel-blending-freeze-point-assurance-stack-v1` when cold-weather sustainment depends on verified blend integrity, additive compatibility, or freeze-point release confidence.
- Add `packet_id=DPL-ADDITIVE-INTENT-VALIDATION-001`, `packet_id=DPL-RAREGAS-CRYO-001`, and `packet_id=DPL-ARCTIC-FUEL-FREEZE-001` for branches that materially alter repair release, industrial sustainment confidence, or Arctic distribution feasibility.

## Domain Toolchain Override (2026-03-15, Expansion Wave LXVI Addendum)

- Add `tool_suite_id=ts-coalition-civil-port-labor-strike-sealift-continuity-v1` + `protocol_stack_id=ps-coalition-civil-port-labor-strike-sealift-continuity-stack-v1` when sustainment viability depends on commercial-port labor posture, berth throughput, or coalition reroute timing.
- Add `tool_suite_id=ts-homeland-coastal-storm-surge-fuel-farm-saltwater-intrusion-v1` + `protocol_stack_id=ps-homeland-coastal-storm-surge-fuel-farm-saltwater-intrusion-stack-v1` when fuel continuity depends on storm-surge contamination control, verified clean stock, or coastal distribution recovery.
- Add `tool_suite_id=ts-strategic-aviation-spares-airworthiness-trust-v1` + `protocol_stack_id=ps-strategic-aviation-spares-airworthiness-trust-stack-v1` when sustainment recovery depends on trusted aviation-spares pedigree, cannibalization discipline, or safe release of reclaimed parts.
- Add `packet_id=DPL-PORT-LABOR-SEALIFT-CONTINUITY-001`, `packet_id=DPL-FUEL-FARM-SALTWATER-INTRUSION-001`, and `packet_id=DPL-AVIATION-SPARES-AIRWORTHINESS-001` for branches that materially alter sealift throughput, fuel confidence, or fleet-sustainment viability.

## Domain Toolchain Override (2026-04-06, Expansion Wave LXVIII Addendum)

- Add `tool_suite_id=ts-theater-evacuation-route-humanitarian-logistics-traffic-priority-v1` + `protocol_stack_id=ps-theater-evacuation-route-humanitarian-logistics-traffic-priority-stack-v1` when sustainment feasibility depends on mixed evacuation and resupply traffic, corridor control, or humanitarian throughput.
- Add `tool_suite_id=ts-joint-civil-works-emergency-permitting-right-of-entry-v1` + `protocol_stack_id=ps-joint-civil-works-emergency-permitting-right-of-entry-stack-v1` when sustainment recovery depends on emergency site access, dig permits, or right-of-entry for repair and clearance crews.
- Add `tool_suite_id=ts-theater-essential-services-contractor-strike-continuity-v1` + `protocol_stack_id=ps-theater-essential-services-contractor-strike-continuity-stack-v1` when logistics viability depends on contracted utilities, sanitation, transport, or warehousing labor continuity.
- Add `tool_suite_id=ts-theater-allied-civilian-contractor-readiness-force-protection-v1` + `protocol_stack_id=ps-theater-allied-civilian-contractor-readiness-force-protection-stack-v1` when throughput depends on vetted contractor access, protected convoy movement, or contested base-service support.
- Add `packet_id=DPL-EVAC-HUMLOG-TRAFFIC-001`, `packet_id=DPL-EMERGENCY-PERMIT-ENTRY-001`, `packet_id=DPL-ESSENTIAL-SERVICES-STRIKE-001`, and `packet_id=DPL-CONTRACTOR-READINESS-FP-001` for branches that materially alter throughput confidence, repair timing, or sustainment labor viability.

## Domain Toolchain Override (2026-04-11, Expansion Wave XCIV Addendum)

- Add `toolchain_id=TC-CDLHAZ-395`, `tool_suite_id=ts-joint-military-driver-qualification-cdl-hazmat-convoy-license-continuity-v1`, and `protocol_stack_id=ps-joint-military-driver-qualification-cdl-hazmat-convoy-license-continuity-stack-v1` when sustainment feasibility depends on enough legally qualified drivers with current CDL, hazmat, or convoy credentials to move fuel, ammunition, or priority cargo.
- Add `packet_id=DPL-MIL-DRIVER-CDL-HAZMAT-001` for branches that materially alter force-flow confidence, cargo-release timing, or commander trust in convoy execution.
