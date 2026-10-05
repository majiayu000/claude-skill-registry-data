---
name: mission-risk-decision-support
description: Quantify and communicate mission risk for commander decisions. Use when comparing options under uncertainty and documenting risk acceptance with controls.
---

# Mission Risk Decision Support

## Mission Scope

- Treat this skill as a planning and decision-support aid for U.S. warfighter missions in its domain.
- Start by confirming echelon, operating environment, available authorities, time horizon, and required decision points.
- Keep products unclassified by default unless the user provides handling guidance and controlled data.

## Workflow

1. Frame the mission problem using these core inputs: COAs, threat likelihood/severity, control measures, commander risk tolerance.
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

Primary products for this skill: risk decision matrix, recommended controls, risk acceptance statement draft.

## Domain Tool Stack

Use these tool categories as the default stack for this skill: mission risk analytics boards, campaign dependency graph engines, cross-domain readiness dashboards.

## Protocol Profile

Preferred protocol families for this skill: USMTF, API/JSON, NATO APP-11/ADatP-3 aligned.

## Domain Toolchain Defaults

- Primary: `tool_suite_id=ts-strategic-deterrence-v1` with `protocol_stack_id=ps-joint-tactical-link-stack-v1`.
- Alternate: `tool_suite_id=ts-joint-c2-fusion-v1` with `protocol_stack_id=ps-cop-event-sharing-stack-v1`.
- Degraded: command-approved risk ledger with authenticated voice confirmation and UTC acknowledgment logging.

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

- Default packet IDs: `DPL-TELECOM-PRIORITY-001`, `DPL-AUTON-MAP-POISON-001`, `DPL-FINRAIL-PAYROLL-001`.
- If no packet fully matches, define a provisional packet and assign a validation owner before release.

## Domain Toolchain Override (2026-03-08)

- Prioritize `tool_suite_id=ts-telecom-priority-routing-v1` + `protocol_stack_id=ps-telecom-priority-routing-stack-v1` when commander risk hinges on communications continuity.
- Elevate `tool_suite_id=ts-autonomy-map-poisoning-detect-v1` + `protocol_stack_id=ps-autonomy-map-poisoning-stack-v1` when navigation trust is uncertain.
- If financial rail disruption affects force readiness, add `tool_suite_id=ts-financial-rail-payroll-v1` + `protocol_stack_id=ps-financial-rail-payroll-stack-v1` as a required cross-check branch.

## Domain Toolchain Override (2026-03-08, Timing and Sustainment Integrity Addendum)

- Add `tool_suite_id=ts-anti-jam-gps-epoch-recovery-v1` + `protocol_stack_id=ps-anti-jam-gps-epoch-stack-v1` when risk posture depends on synchronized timing in denied PNT conditions.
- Add `tool_suite_id=ts-denied-fuel-bladder-integrity-v1` + `protocol_stack_id=ps-denied-fuel-bladder-integrity-stack-v1` when sustainment reliability is vulnerable to fuel contamination or sabotage.
- Add `packet_id=DPL-LONG-RANGE-FIRES-LOT-001` for any recommendation that changes long-range fires allocation based on ammunition reliability assumptions.

## Operational Execution Hardening

- Enforce `ack_chain_status=verified` for all mission-critical tool exchanges before recommending posture changes.
- Require `trust_score >= 0.80` on each primary external dependency; if lower, elevate alternate stack and mark outputs `provisional`.
- Add explicit degraded-mode triggers: stale data beyond `refresh_sla_minutes`, missing cryptographic validation, or failed human approval gate.
- Include a final command-ready line: `GO`, `NO-GO`, or `GO-WITH-CONSTRAINTS` with rationale tied to authority and protocol checks.

## Domain Toolchain Override (2026-03-08, Signature and Data Integrity Addendum)

- Add `tool_suite_id=ts-electronic-signature-survivability-v1` + `protocol_stack_id=ps-electronic-signature-survivability-stack-v1` when risk posture depends on adversary sensing pressure.
- Add `tool_suite_id=ts-multi-cloud-mission-data-integrity-v1` + `protocol_stack_id=ps-multi-cloud-mission-data-integrity-stack-v1` when branch viability depends on cross-cloud data trust.
- Add `packet_id=DPL-PRIORITY-OF-LIFE-ROUTING-001` when force protection and civil continuity tradeoffs affect commander risk acceptance.

## Domain Toolchain Override (2026-03-09, Solar Storm and Counterfeit Supply Addendum)

- Add `tool_suite_id=ts-space-weather-solar-storm-mission-assurance-v1` + `protocol_stack_id=ps-space-weather-solar-storm-mission-assurance-stack-v1` when mission risk depends on timing, SATCOM, or grid fragility during geomagnetic disturbance.
- Add `tool_suite_id=ts-homeland-microelectronics-counterfeit-quarantine-v1` + `protocol_stack_id=ps-homeland-microelectronics-counterfeit-quarantine-stack-v1` when recommendation confidence depends on trusted military microelectronics pedigree.
- Add `packet_id=DPL-SPACE-WEATHER-SOLAR-STORM-MISSION-ASSURANCE-001` and `packet_id=DPL-HOMELAND-MICROELECTRONICS-COUNTERFEIT-QUARANTINE-001` for risk branches that change commander acceptance thresholds.

## Domain Toolchain Override (2026-03-10, Strategic Continuity and Countertargeting Expansion)

- Add `tool_suite_id=ts-nc3-resilience-and-order-integrity-v1` + `protocol_stack_id=ps-nc3-resilience-and-order-integrity-stack-v1` when mission risk depends on authenticated strategic command continuity.
- Add `tool_suite_id=ts-denied-pnt-timing-holdover-v1` + `protocol_stack_id=ps-denied-pnt-timing-holdover-stack-v1` when risk posture depends on synchronized timing under GNSS denial.
- Add `tool_suite_id=ts-precision-effects-weaponeering-ai-assurance-v1` + `protocol_stack_id=ps-precision-effects-weaponeering-ai-assurance-stack-v1` when risk recommendations rely on AI-assisted targeting effects.
- Add `tool_suite_id=ts-hyperscale-cloud-failover-command-continuity-v1` + `protocol_stack_id=ps-hyperscale-cloud-failover-command-continuity-stack-v1` when command continuity relies on contested cloud infrastructure.
- Add `packet_id=DPL-NC3-RESILIENCE-ORDER-INTEGRITY-001`, `packet_id=DPL-DENIED-PNT-TIMING-HOLDOVER-001`, and `packet_id=DPL-PRECISION-EFFECTS-WEAPONEERING-AI-ASSURANCE-001` for branches that can alter commander risk acceptance.

## Domain Toolchain Override (2026-03-10, Deepfake Orders, PNT Cross-Check, and AI Poisoning Addendum)

- Add `tool_suite_id=ts-deepfake-orders-auth-countersign-v1` + `protocol_stack_id=ps-deepfake-orders-auth-countersign-stack-v1` when commander risk depends on trusted command-path authentication under synthetic media pressure.
- Add `tool_suite_id=ts-quantum-navigation-pnt-cross-check-v1` + `protocol_stack_id=ps-quantum-navigation-pnt-cross-check-stack-v1` when mission risk thresholds depend on navigation and timing confidence under spoofing or jamming.
- Add `tool_suite_id=ts-adversarial-ai-model-poisoning-detection-v1` + `protocol_stack_id=ps-adversarial-ai-model-poisoning-detection-stack-v1` when risk decisions rely on mission AI outputs with uncertain provenance.
- Add `packet_id=DPL-DEEPFAKE-ORDERS-AUTH-COUNTERSIGN-001`, `packet_id=DPL-QUANTUM-NAV-PNT-CROSS-CHECK-001`, and `packet_id=DPL-ADVERSARIAL-AI-MODEL-POISONING-DETECTION-001` for branches that can materially alter commander risk acceptance.

## Domain Toolchain Override (2026-03-12, Expansion Wave XV Addendum)

- Add tool_suite_id=ts-strategic-homeland-port-fuel-terminal-cyber-physical-blackstart-cell-v1 + protocol_stack_id=ps-strategic-homeland-port-fuel-terminal-cyber-physical-blackstart-cell-stack-v1 when risk acceptance depends on fuel infrastructure restoration and cyber-safe blackstart sequencing.
- Add tool_suite_id=ts-strategic-deepfake-diplomatic-hotline-authentication-cell-v1 + protocol_stack_id=ps-strategic-deepfake-diplomatic-hotline-authentication-cell-stack-v1 when strategic decision confidence depends on authenticated crisis communication pathways.
- Add packet_id=DPL-HOMELAND-PORT-FUEL-BLACKSTART-001 and packet_id=DPL-DEEPFAKE-HOTLINE-AUTH-001 for branches that materially alter commander risk posture, escalation pathways, or continuity assumptions.


## Domain Toolchain Override (2026-03-12, Expansion Wave XVI Addendum)

- Add tool_suite_id=ts-strategic-grid-transformer-supply-sabotage-and-restoration-cell-v1 + protocol_stack_id=ps-strategic-grid-transformer-supply-sabotage-and-restoration-cell-stack-v1 when mission risk depends on power-grid transformer survivability, restoration timing, and sabotage confidence.
- Add tool_suite_id=ts-homeland-defense-satellite-timing-financial-clearing-fallback-cell-v1 + protocol_stack_id=ps-homeland-defense-satellite-timing-financial-clearing-fallback-cell-stack-v1 when commander risk acceptance depends on timing trust and financial-clearing continuity.
- Add packet_id=DPL-GRID-TRANSFORMER-RESTORE-001 and packet_id=DPL-SAT-TIMING-FINANCIAL-CLEARING-001 for branches that alter sustainment confidence, escalation posture, or force-readiness assumptions.

## Domain Toolchain Override (2026-03-12, Expansion Wave XIX Addendum)

- Add `tool_suite_id=ts-iamd-depletion-forecast-v1` + `protocol_stack_id=ps-iamd-depletion-forecast-stack-v1` when mission risk depends on interceptor endurance and defended-asset reprioritization under sustained salvos.
- Add `tool_suite_id=ts-contested-personnel-recovery-v1` + `protocol_stack_id=ps-contested-personnel-recovery-stack-v1` when commander risk posture depends on isolated personnel survival, authentication confidence, or contested recovery feasibility.
- Add `tool_suite_id=ts-jadc2-datalink-bridging-priority-v1` + `protocol_stack_id=ps-jadc2-datalink-bridging-priority-stack-v1` when risk acceptance depends on cross-link translation fidelity and message-priority acknowledgment integrity.
- Add `packet_id=DPL-IAMD-DEPLETION-001`, `packet_id=DPL-CONTESTED-PR-001`, and `packet_id=DPL-JADC2-BRIDGE-001` when these dependencies materially change commander GO/NO-GO decisions.

## Domain Toolchain Override (2026-03-12, Expansion Wave XX Addendum)

- Add `tool_suite_id=ts-nuclear-command-auth-containment-v1` + `protocol_stack_id=ps-nuclear-command-auth-containment-stack-v1` when mission risk depends on trusted strategic order-path authentication or high-consequence incident containment.
- Add `tool_suite_id=ts-strategic-mobility-chokepoint-optimizer-v1` + `protocol_stack_id=ps-strategic-mobility-chokepoint-optimizer-stack-v1` when commander risk acceptance depends on rail-air-sealift throughput resilience.
- Add `tool_suite_id=ts-auton-target-human-override-assurance-v1` + `protocol_stack_id=ps-auton-target-human-override-assurance-stack-v1` when recommendations depend on autonomous targeting confidence and deterministic human override controls.
- Add `packet_id=DPL-NUCLEAR-AUTH-CONTAINMENT-001`, `packet_id=DPL-STRAT-MOBILITY-CHOKEPOINT-001`, and `packet_id=DPL-AUTON-TARGET-HUMAN-OVERRIDE-001` for branches that materially change GO/NO-GO posture.

## Domain Toolchain Override (2026-03-12, Expansion Wave XXIII Addendum)

- Add `tool_suite_id=ts-orbital-servicing-refuel-assurance-v1` + `protocol_stack_id=ps-orbital-servicing-refuel-assurance-stack-v1` when recommendations depend on contested space-logistics servicing continuity, custody confidence, or maneuver-safe refuel timing.
- Add `tool_suite_id=ts-denied-terrain-drone-resupply-nav-v1` + `protocol_stack_id=ps-denied-terrain-drone-resupply-nav-stack-v1` when branch viability depends on autonomous resupply route confidence through denied terrain.
- Add `tool_suite_id=ts-coalition-cable-landing-data-sovereignty-v1` + `protocol_stack_id=ps-coalition-cable-landing-data-sovereignty-stack-v1` when recommendations depend on sovereign data routing, coalition caveats, or cable-landing continuity.
- Add `tool_suite_id=ts-runway-ice-fog-autoland-assurance-v1` + `protocol_stack_id=ps-runway-ice-fog-autoland-assurance-stack-v1` when mission tempo is constrained by low-visibility runway conditions and autoland safety confidence.
- Add `packet_id=DPL-ORBITAL-SERVICING-REFUEL-001`, `packet_id=DPL-DENIED-TERRAIN-DRONE-RESUPPLY-001`, `packet_id=DPL-COALITION-CABLE-LANDING-SOVEREIGNTY-001`, and `packet_id=DPL-RUNWAY-ICE-FOG-AUTOLAND-001` for branches that materially alter commander GO/NO-GO posture.

## Domain Toolchain Override (2026-03-12, Expansion Wave XXIV Addendum)

- Add `tool_suite_id=ts-theater-llm-opsec-prompt-injection-defense-v1` + `protocol_stack_id=ps-theater-llm-opsec-prompt-injection-defense-stack-v1` when commander risk acceptance depends on trusted mission-AI outputs and prompt-injection containment.
- Add `tool_suite_id=ts-strategic-rare-gas-energetic-precursor-allocation-v1` + `protocol_stack_id=ps-strategic-rare-gas-energetic-precursor-allocation-stack-v1` when recommendation confidence depends on precursor sustainment availability.
- Add `packet_id=DPL-THEATER-LLM-OPSEC-INJECTION-001` and `packet_id=DPL-STRATEGIC-RAREGAS-ENERGETICS-001` for branches that materially alter GO/NO-GO posture.

## Domain Toolchain Override (2026-03-12, Expansion Wave XXV Addendum)

- Prioritize `tool_suite_id=ts-joint-cislunar-logistics-interdiction-reconstitution-v1` with `protocol_stack_id=ps-joint-cislunar-logistics-interdiction-reconstitution-stack-v1` when strategic space logistics, custody confidence, or cislunar maneuver assurance directly affect mission risk decisions.
- Add `tool_suite_id=ts-theater-underwater-datacenter-cooling-grid-defense-v1` with `protocol_stack_id=ps-theater-underwater-datacenter-cooling-grid-defense-stack-v1` when mission outcomes depend on underwater compute resilience, cooling continuity, or cyber-physical load restoration.
- Add `packet_id=DPL-CISLUNAR-LOGISTICS-INTERDICTION-001` and `packet_id=DPL-UNDERWATER-DATACENTER-COOLING-DEFENSE-001` for recommendations that alter mission posture, contingency branches, or strategic continuity authorities.

## Domain Toolchain Override (2026-03-14, Expansion Wave XLII Addendum)

- Add `tool_suite_id=ts-theater-mission-ai-confidence-early-warning-v1` + `protocol_stack_id=ps-theater-mission-ai-confidence-early-warning-stack-v1` when commander risk acceptance depends on trust in mission-AI outputs, drift warnings, or rollback timing.
- Add `tool_suite_id=ts-strategic-economic-coercion-logistics-warning-v1` + `protocol_stack_id=ps-strategic-economic-coercion-logistics-warning-stack-v1` when risk posture depends on fragile routes, carrier pressure, or adversary coercion against sustainment.
- Add `tool_suite_id=ts-theater-no-strike-geofence-integrity-v1` + `protocol_stack_id=ps-theater-no-strike-geofence-integrity-stack-v1` when protected-boundary drift could invalidate fires, maneuver, or civilian-risk assumptions.
- Add `packet_id=DPL-MISSION-AI-CONFIDENCE-001`, `packet_id=DPL-ECON-COERCION-LOGISTICS-001`, and `packet_id=DPL-NO-STRIKE-GEOFENCE-001` for branches that materially change commander GO, NO-GO, or GO-WITH-CONSTRAINTS decisions.

## Domain Toolchain Override (2026-03-14, Expansion Wave XLIII Addendum)

- Add `tool_suite_id=ts-joint-munition-dataload-crypto-fill-reconstitution-v1` + `protocol_stack_id=ps-joint-munition-dataload-crypto-fill-reconstitution-stack-v1` when commander risk posture depends on trusted weapon or EW mission-data reconstitution after compromise or relocation.
- Add `tool_suite_id=ts-coalition-neo-identity-fraud-suppression-v1` + `protocol_stack_id=ps-coalition-neo-identity-fraud-suppression-stack-v1` when evacuation legitimacy, family reunification, or coalition screening confidence materially affects risk acceptance.
- Add `tool_suite_id=ts-strategic-harbor-tug-pilotage-sealift-priority-v1` + `protocol_stack_id=ps-strategic-harbor-tug-pilotage-sealift-priority-stack-v1` when sealift timing, berth windows, or harbor-control scarcity becomes a decisive mission-risk driver.
- Add `packet_id=DPL-MUNITION-DATALOAD-CRYPTO-001`, `packet_id=DPL-NEO-IDENTITY-FRAUD-001`, and `packet_id=DPL-HARBOR-TUG-PILOTAGE-SEALIFT-001` for branches that materially change commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture.

## Domain Toolchain Override (2026-03-14, Expansion Wave XLIV Addendum)

- Add `tool_suite_id=ts-joint-airbase-arresting-gear-runway-cable-reconstitution-v1` + `protocol_stack_id=ps-joint-airbase-arresting-gear-runway-cable-reconstitution-stack-v1` when commander risk depends on sortie regeneration, arresting-gear integrity, or runway-end cable recovery at damaged airbases.
- Add `tool_suite_id=ts-joint-commercial-sat-imagery-retask-governance-v1` + `protocol_stack_id=ps-joint-commercial-sat-imagery-retask-governance-stack-v1` when risk decisions depend on trusted fallback ISR coverage after commercial imagery denial or political restrictions.
- Add `tool_suite_id=ts-joint-tactical-edge-dataset-provenance-rollback-v1` + `protocol_stack_id=ps-joint-tactical-edge-dataset-provenance-rollback-stack-v1` when commander risk acceptance depends on restoring trusted edge datasets or rolling back suspect model updates.
- Add `packet_id=DPL-ARRESTING-GEAR-RUNWAY-CABLE-001`, `packet_id=DPL-COMMERCIAL-SAT-IMAGERY-RETASK-001`, and `packet_id=DPL-TACTICAL-EDGE-DATASET-ROLLBACK-001` for branches that materially change commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture.

## Domain Toolchain Override (2026-03-14, Expansion Wave XLV Addendum)

- Add `tool_suite_id=ts-joint-civil-reserve-air-fleet-activation-v1` + `protocol_stack_id=ps-joint-civil-reserve-air-fleet-activation-stack-v1` when commander risk acceptance depends on reserve or commercial airlift closing deployment, evacuation, or sustainment gaps.
- Add `tool_suite_id=ts-theater-mission-sbom-emergency-patch-v1` + `protocol_stack_id=ps-theater-mission-sbom-emergency-patch-stack-v1` when risk posture depends on urgent software remediation, rollback assurance, or artifact trust across mission systems.
- Add `tool_suite_id=ts-joint-digital-order-watermark-recall-v1` + `protocol_stack_id=ps-joint-digital-order-watermark-recall-stack-v1` when commander confidence depends on authentic order distribution and rapid containment of spoofed or stale digital tasking.
- Add `packet_id=DPL-CIVIL-RESERVE-AIR-FLEET-001`, `packet_id=DPL-MISSION-SBOM-EMERGENCY-PATCH-001`, and `packet_id=DPL-DIGITAL-ORDER-WATERMARK-001` for branches that materially change commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture.

## Domain Toolchain Override (2026-03-15, Expansion Wave LIII Addendum)

- Add `tool_suite_id=ts-expeditionary-vector-control-field-epidemiology-v1` + `protocol_stack_id=ps-expeditionary-vector-control-field-epidemiology-stack-v1` when commander risk posture depends on vector-borne disease pressure, outbreak branching, or pesticide-release timing.
- Add `tool_suite_id=ts-joint-cold-injury-frostbite-rewarming-v1` + `protocol_stack_id=ps-joint-cold-injury-frostbite-rewarming-stack-v1` when exposure timelines, warming capacity, or cold-weather casualty routing materially alter GO or NO-GO posture.
- Add `tool_suite_id=ts-joint-blast-overpressure-breacher-readiness-v1` + `protocol_stack_id=ps-joint-blast-overpressure-breacher-readiness-stack-v1` when cumulative concussive exposure, breacher qualification status, or medical follow-up change acceptable risk.
- Add `packet_id=DPL-VECTOR-CONTROL-FIELD-EPI-001`, `packet_id=DPL-COLD-INJURY-REWARMING-001`, and `packet_id=DPL-BLAST-OVERPRESSURE-BREACHER-001` for branches that materially change commander risk acceptance, force-readiness confidence, or training tempo.

## Domain Toolchain Override (2026-03-15, Expansion Wave LIV Addendum)

- Add `tool_suite_id=ts-expeditionary-industrial-hygiene-occupational-exposure-v1` + `protocol_stack_id=ps-expeditionary-industrial-hygiene-occupational-exposure-stack-v1` when commander GO or NO-GO posture depends on occupational sampling confidence, PPE posture, or safe work continuation at expeditionary nodes.
- Add `tool_suite_id=ts-joint-aviation-physiology-hypoxia-life-support-v1` + `protocol_stack_id=ps-joint-aviation-physiology-hypoxia-life-support-stack-v1` when flight risk, hypoxia incidents, or life-support equipment restrictions materially change sortie or rescue viability.
- Add `tool_suite_id=ts-joint-dive-medicine-hyperbaric-routing-v1` + `protocol_stack_id=ps-joint-dive-medicine-hyperbaric-routing-stack-v1` when chamber scarcity, pressure injury, or undersea casualty routing changes commander risk acceptance.
- Add `tool_suite_id=ts-joint-substance-use-overdose-impaired-duty-v1` + `protocol_stack_id=ps-joint-substance-use-overdose-impaired-duty-stack-v1` when overdose stabilization, impaired-duty restrictions, or protected referral decisions materially affect command confidence and force availability.
- Add `tool_suite_id=ts-theater-sleep-recovery-shift-work-fatigue-restoration-v1` + `protocol_stack_id=ps-theater-sleep-recovery-shift-work-fatigue-restoration-stack-v1` when chronic sleep loss, unstable shifts, or protected-rest windows materially change risk acceptance across critical nodes.
- Add `packet_id=DPL-INDUSTRIAL-HYGIENE-OCCUPATIONAL-EXPOSURE-001`, `packet_id=DPL-AVIATION-PHYSIOLOGY-HYPOXIA-LIFE-SUPPORT-001`, `packet_id=DPL-DIVE-MEDICINE-HYPERBARIC-ROUTING-001`, `packet_id=DPL-SUBSTANCE-USE-OVERDOSE-IMPAIRED-DUTY-001`, and `packet_id=DPL-SLEEP-RECOVERY-SHIFT-WORK-FATIGUE-001` for branches that materially change commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture.

## Domain Toolchain Override (2026-03-15, Expansion Wave LV Addendum)

- Add `tool_suite_id=ts-joint-contested-ceasefire-hotline-escalation-control-v1` + `protocol_stack_id=ps-joint-contested-ceasefire-hotline-escalation-control-stack-v1` when commander risk posture depends on incident acknowledgment integrity, deconfliction speed, or escalation restraint.
- Add `tool_suite_id=ts-strategic-merchant-mariner-crewing-flag-sanctions-risk-v1` + `protocol_stack_id=ps-strategic-merchant-mariner-crewing-flag-sanctions-risk-stack-v1` when strategic mobility or sealift risk depends on crew availability, registry exposure, or sanctions friction.
- Add `tool_suite_id=ts-joint-deployed-finance-cash-payroll-disbursing-continuity-v1` + `protocol_stack_id=ps-joint-deployed-finance-cash-payroll-disbursing-continuity-stack-v1` when commander confidence depends on pay continuity, cash custody, or disbursing resilience during disruption.
- Add `tool_suite_id=ts-joint-robotic-casualty-extraction-human-override-safety-v1` + `protocol_stack_id=ps-joint-robotic-casualty-extraction-human-override-safety-stack-v1` when route denial, contamination, or fire makes casualty extraction risk hinge on autonomous override trust.
- Add `packet_id=DPL-CEASEFIRE-HOTLINE-ESCALATION-001`, `packet_id=DPL-MERCHANT-MARINER-FLAG-SANCTIONS-001`, `packet_id=DPL-DEPLOYED-FINANCE-DISBURSING-001`, and `packet_id=DPL-ROBOTIC-CASUALTY-EXTRACTION-001` for branches that materially change commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture.

## Domain Toolchain Override (2026-03-15, Expansion Wave LVI Gap-Closure Addendum)

- Add `tool_suite_id=ts-joint-signals-intelligence-emitter-geolocation-fusion-v1` + `protocol_stack_id=ps-joint-signals-intelligence-emitter-geolocation-fusion-stack-v1` when commander risk posture depends on emitter confidence, cross-cue latency, or adversary deception in contested sensing.
- Add `tool_suite_id=ts-joint-expeditionary-advanced-base-signature-management-v1` + `protocol_stack_id=ps-joint-expeditionary-advanced-base-signature-management-stack-v1` when risk acceptance depends on expeditionary base displacement timing, signature budget, or austere sustainment viability.
- Add `tool_suite_id=ts-joint-operational-law-judge-advocate-advisory-v1` + `protocol_stack_id=ps-joint-operational-law-judge-advocate-advisory-stack-v1` when commander confidence depends on authority basis, legal risk framing, or coalition caveat clarity.
- Add `tool_suite_id=ts-joint-orbital-warfare-effects-deconfliction-v1` + `protocol_stack_id=ps-joint-orbital-warfare-effects-deconfliction-stack-v1` when risk posture depends on protected-service continuity, conjunction confidence, or escalation control in orbit.
- Add `tool_suite_id=ts-joint-air-mobility-diplomatic-clearance-staging-v1` + `protocol_stack_id=ps-joint-air-mobility-diplomatic-clearance-staging-stack-v1` when commander GO or NO-GO posture depends on diplomatic-clearance speed, staging-node capacity, or contested lift continuity.
- Add `packet_id=DPL-SIGINT-EMITTER-GEOLOCATION-001`, `packet_id=DPL-EABO-SIGNATURE-MANAGEMENT-001`, `packet_id=DPL-JUDGE-ADVOCATE-OPLAW-001`, `packet_id=DPL-ORBITAL-WARFARE-DECONFLICTION-001`, and `packet_id=DPL-AIR-MOBILITY-DIPCLEAR-STAGING-001` for branches that materially change commander risk acceptance, authority gating, or mission continuity posture.

## Domain Toolchain Override (2026-03-15, Expansion Wave LXI Addendum)

- Add `tool_suite_id=ts-theater-aviation-fuel-lab-contamination-clearance-v1` + `protocol_stack_id=ps-theater-aviation-fuel-lab-contamination-clearance-stack-v1` when commander risk acceptance depends on trusted aviation fuel, contamination isolation, or sortie-release confidence.
- Add `tool_suite_id=ts-joint-offline-key-material-courier-compromise-v1` + `protocol_stack_id=ps-joint-offline-key-material-courier-compromise-stack-v1` when command confidence depends on disconnected key custody, courier delivery, or compromise containment.
- Add `tool_suite_id=ts-strategic-defense-industrial-workforce-clearance-assignment-v1` + `protocol_stack_id=ps-strategic-defense-industrial-workforce-clearance-assignment-stack-v1` when risk posture depends on cleared industrial labor availability across depots, shipyards, or missile plants.
- Add `tool_suite_id=ts-theater-electromagnetic-deception-confidence-countertargeting-v1` + `protocol_stack_id=ps-theater-electromagnetic-deception-confidence-countertargeting-stack-v1` when force-protection confidence depends on decoy credibility, emission control, or adversary countertargeting indicators.
- Add `packet_id=DPL-AVIATION-FUEL-LAB-CLEARANCE-001`, `packet_id=DPL-OFFLINE-KEY-MATERIAL-COURIER-001`, `packet_id=DPL-INDUSTRIAL-WORKFORCE-CLEARANCE-001`, and `packet_id=DPL-EM-DECEPTION-CONFIDENCE-001` for branches that materially alter commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture.

## Domain Toolchain Override (2026-03-15, Expansion Wave LXII Addendum)

- Add `tool_suite_id=ts-joint-nuclear-command-warning-delegation-safeguards-v1` + `protocol_stack_id=ps-joint-nuclear-command-warning-delegation-safeguards-stack-v1` when commander risk acceptance depends on warning authenticity, delegated-response safeguards, or acknowledgment integrity under degraded strategic communications.
- Add `tool_suite_id=ts-space-based-missile-warning-ground-truth-correlation-v1` + `protocol_stack_id=ps-space-based-missile-warning-ground-truth-correlation-stack-v1` when risk posture depends on corroborating ambiguous missile warning before changing alert status or dispersal posture.
- Add `tool_suite_id=ts-homeland-rail-evacuation-signaling-restoration-v1` + `protocol_stack_id=ps-homeland-rail-evacuation-signaling-restoration-stack-v1` when mission risk depends on protected homeland evacuation or force-flow continuity across damaged rail-control networks.
- Add `tool_suite_id=ts-strategic-rare-gas-cryogenic-supply-priority-v1` + `protocol_stack_id=ps-strategic-rare-gas-cryogenic-supply-priority-stack-v1` when readiness or industrial continuity depends on scarce cryogenic-gas allocation, purity confidence, or boil-off risk.
- Add `packet_id=DPL-NUCLEAR-WARN-DELEGATION-001`, `packet_id=DPL-MISSILE-WARNING-GT-CORR-001`, `packet_id=DPL-RAIL-EVAC-SIGNAL-001`, and `packet_id=DPL-RAREGAS-CRYO-001` for branches that materially change commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture.

## Domain Toolchain Override (2026-04-06, Expansion Wave LXX Addendum)

- Add `toolchain_id=TC-DSC-258`, `tool_suite_id=ts-homeland-dual-status-command-authority-integration-v1`, and `protocol_stack_id=ps-homeland-dual-status-command-authority-integration-stack-v1` when commander risk posture depends on Title 10 versus Title 32 force-status alignment, dual-status command designation timing, or domestic unity-of-command confidence.
- Add `toolchain_id=TC-GOVRFF-260`, `tool_suite_id=ts-homeland-governor-request-for-forces-mission-assignment-v1`, and `protocol_stack_id=ps-homeland-governor-request-for-forces-mission-assignment-stack-v1` when risk acceptance depends on governor demand legitimacy, mission-assignment speed, or sourcing sufficiency.
- Add `toolchain_id=TC-EOCFUSE-262`, `tool_suite_id=ts-homeland-emergency-manager-cop-fusion-v1`, and `protocol_stack_id=ps-homeland-emergency-manager-cop-fusion-stack-v1` when commander risk framing depends on fragmented domestic reporting, local confirmation lag, or confidence-scored common operating pictures.
- Add `toolchain_id=TC-FISCAL-264`, `tool_suite_id=ts-homeland-dsca-reimbursement-funding-authority-v1`, and `protocol_stack_id=ps-homeland-dsca-reimbursement-funding-authority-stack-v1` when recommendation viability depends on fiscal legitimacy, reimbursement timing, or auditability of DSCA actions.
- Add `packet_id=DPL-DUAL-STATUS-COMMAND-001`, `packet_id=DPL-GOV-RFF-MISSION-ASSIGNMENT-001`, `packet_id=DPL-EMERGENCY-MANAGER-COP-FUSION-001`, and `packet_id=DPL-DSCA-FUNDING-AUTHORITY-001` for branches that materially alter commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture during homeland response.

## Domain Toolchain Override (2026-04-06, Expansion Wave LXXII Materialization Addendum)

- Add `toolchain_id=TC-COMPENSATION-243`, `tool_suite_id=ts-joint-military-financial-liability-and-compensation-continuity-v1`, and `protocol_stack_id=ps-joint-military-financial-liability-and-compensation-continuity-stack-v1` when commander risk posture depends on compensation legitimacy, claims continuity, or fraud-safe interim relief.
- Add `toolchain_id=TC-PUBCOMMS-244`, `tool_suite_id=ts-joint-incident-command-post-public-communications-and-media-contingency-v1`, and `protocol_stack_id=ps-joint-incident-command-post-public-communications-and-media-contingency-stack-v1` when risk framing depends on public-warning timing, message approval integrity, or media-driven escalation pressure.
- Add `toolchain_id=TC-HNMANDATE-245`, `tool_suite_id=ts-joint-host-nation-legislative-liaison-and-mandate-alignment-v1`, and `protocol_stack_id=ps-joint-host-nation-legislative-liaison-and-mandate-alignment-stack-v1` when commander confidence depends on host-nation mandate stability, waiver speed, or coalition caveat alignment.
- Add `toolchain_id=TC-ESSENTIAL-247`, `tool_suite_id=ts-theater-essential-services-contractor-strike-and-continuity-v1`, and `protocol_stack_id=ps-theater-essential-services-contractor-strike-and-continuity-stack-v1` when risk posture depends on labor-action continuity, safe service rationing, or contractor-driven operational choke points.
- Add `toolchain_id=TC-WORKFORCEFAM-249`, `tool_suite_id=ts-strategic-defense-industrial-workforce-family-stabilization-v1`, and `protocol_stack_id=ps-strategic-defense-industrial-workforce-family-stabilization-stack-v1` when strategic risk depends on critical-worker family stability, industrial surge confidence, or defense-production continuity.
- Add `packet_id=DPL-COMPENSATION-CONTINUITY-001`, `packet_id=DPL-ICP-PUBLIC-COMMS-001`, `packet_id=DPL-HOST-NATION-MANDATE-001`, `packet_id=DPL-ESSENTIAL-SERVICES-CONTINUITY-001`, and `packet_id=DPL-WORKFORCE-FAMILY-STABILIZATION-001` for branches that materially alter commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture.

## Domain Toolchain Override (2026-04-07, Expansion Wave LXXII Addendum)

- Add `toolchain_id=TC-PHLAB-274`, `tool_suite_id=ts-homeland-public-health-laboratory-surge-specimen-chain-v1`, and `protocol_stack_id=ps-homeland-public-health-laboratory-surge-specimen-chain-stack-v1` when commander risk posture depends on diagnostic confidence, specimen-custody integrity, or outbreak-reporting speed.
- Add `toolchain_id=TC-CORR-276`, `tool_suite_id=ts-homeland-corrections-facility-evacuation-guard-force-relief-v1`, and `protocol_stack_id=ps-homeland-corrections-facility-evacuation-guard-force-relief-stack-v1` when risk acceptance depends on lawful custody evacuation, receiving-site confidence, or guard-force exhaustion.
- Add `toolchain_id=TC-COOL-277`, `tool_suite_id=ts-homeland-cooling-center-load-shedding-generator-priority-v1`, and `protocol_stack_id=ps-homeland-cooling-center-load-shedding-generator-priority-stack-v1` when extreme-heat life-safety depends on cooling-center uptime, generator allocation, or blackout triage.
- Add `toolchain_id=TC-FERRY-278`, `tool_suite_id=ts-homeland-ferry-evacuation-island-resupply-priority-v1`, and `protocol_stack_id=ps-homeland-ferry-evacuation-island-resupply-priority-stack-v1` when isolated-population support or maritime evacuation timing becomes a decisive commander-risk driver.
- Add `toolchain_id=TC-WASTE-279`, `tool_suite_id=ts-homeland-wastewater-overflow-force-health-waterway-protection-v1`, and `protocol_stack_id=ps-homeland-wastewater-overflow-force-health-waterway-protection-stack-v1` when contamination spread, responder exposure, or downstream waterway impacts change GO or NO-GO posture.
- Add `toolchain_id=TC-ANIMAL-280`, `tool_suite_id=ts-homeland-animal-disease-quarantine-food-system-defense-v1`, and `protocol_stack_id=ps-homeland-animal-disease-quarantine-food-system-defense-stack-v1` when commander confidence depends on zoonotic containment, agricultural disruption, or food-system continuity.
- Add `packet_id=DPL-PUBLIC-HEALTH-LAB-CHAIN-001`, `packet_id=DPL-CORRECTIONS-EVAC-GUARDFORCE-001`, `packet_id=DPL-COOLING-CENTER-GENERATOR-001`, `packet_id=DPL-FERRY-ISLAND-RESUPPLY-001`, `packet_id=DPL-WASTEWATER-OVERFLOW-WATERWAY-001`, and `packet_id=DPL-ANIMAL-DISEASE-FOOD-DEFENSE-001` for branches that materially change commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture during domestic response.

## Domain Toolchain Override (2026-04-07, Expansion Wave LXXIII Addendum)

- Add `toolchain_id=TC-LEGALAID-282`, `tool_suite_id=ts-homeland-military-legal-assistance-identity-document-reissuance-v1`, and `protocol_stack_id=ps-homeland-military-legal-assistance-identity-document-reissuance-stack-v1` when commander risk posture depends on legal-aid sufficiency, identity-document recovery, or family entitlement continuity.
- Add `toolchain_id=TC-PROTECT-283`, `tool_suite_id=ts-homeland-protective-order-domestic-violence-safe-housing-continuity-v1`, and `protocol_stack_id=ps-homeland-protective-order-domestic-violence-safe-housing-continuity-stack-v1` when victim protection, safe-housing reliability, or protective-order continuity changes acceptable risk.
- Add `toolchain_id=TC-POSTPARTUM-284`, `tool_suite_id=ts-homeland-postpartum-lactation-infant-formula-diaper-continuity-v1`, and `protocol_stack_id=ps-homeland-postpartum-lactation-infant-formula-diaper-continuity-stack-v1` when maternal-infant care continuity, lactation support, or formula and diaper sustainment alter commander confidence.
- Add `toolchain_id=TC-SPOUSE-287`, `tool_suite_id=ts-strategic-military-spouse-licensure-employment-pcs-continuity-v1`, and `protocol_stack_id=ps-strategic-military-spouse-licensure-employment-pcs-continuity-stack-v1` when spouse employment collapse, licensure barriers, or PCS disruption materially affect readiness risk.
- Add `toolchain_id=TC-DEPENDENTCARE-288`, `tool_suite_id=ts-reserve-component-single-parent-childcare-eldercare-mobilization-bridge-v1`, and `protocol_stack_id=ps-reserve-component-single-parent-childcare-eldercare-mobilization-bridge-stack-v1` when dependent-care failure, eldercare gaps, or mobilization deferral pressure change GO or NO-GO posture.
- Add `toolchain_id=TC-COURT-289`, `tool_suite_id=ts-homeland-installation-courthouse-custody-hearing-family-law-continuity-v1`, and `protocol_stack_id=ps-homeland-installation-courthouse-custody-hearing-family-law-continuity-stack-v1` when court access, custody-hearing delay, or family-law instability alters commander risk framing.
- Add `packet_id=DPL-LEGAL-AID-ID-REISSUE-001`, `packet_id=DPL-PROTECTIVE-ORDER-SAFE-HOUSING-001`, `packet_id=DPL-POSTPARTUM-LACTATION-FORMULA-001`, `packet_id=DPL-SPOUSE-LICENSURE-PCS-001`, `packet_id=DPL-SINGLE-PARENT-ELDERCARE-MOB-001`, and `packet_id=DPL-COURTHOUSE-CUSTODY-FAMILY-LAW-001` for branches that materially change commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture across military communities.

## Domain Toolchain Override (2026-04-07, Expansion Wave LXXV Addendum)

- Add `toolchain_id=TC-ARCMSG-295`, `tool_suite_id=ts-joint-emergency-leave-american-red-cross-message-command-approval-v1`, and `protocol_stack_id=ps-joint-emergency-leave-american-red-cross-message-command-approval-stack-v1` when commander risk posture depends on verified emergency leave, compassionate travel, or credible family-emergency message provenance.
- Add `toolchain_id=TC-EFMP-296`, `tool_suite_id=ts-joint-efmp-respite-medical-device-power-continuity-v1`, and `protocol_stack_id=ps-joint-efmp-respite-medical-device-power-continuity-stack-v1` when force availability depends on EFMP fragility, power-dependent medical devices, or respite collapse within military households.
- Add `toolchain_id=TC-RELIEF-300`, `tool_suite_id=ts-joint-relief-society-hardship-grant-zero-interest-loan-bridge-v1`, and `protocol_stack_id=ps-joint-relief-society-hardship-grant-zero-interest-loan-bridge-stack-v1` when readiness or retention risk depends on hardship stabilization, emergency-assistance timing, or unpaid travel or lodging burdens.
- Add `packet_id=DPL-EMERGENCY-LEAVE-ARC-001`, `packet_id=DPL-EFMP-RESPITE-POWER-001`, and `packet_id=DPL-RELIEF-SOCIETY-HARDSHIP-001` for branches that materially alter commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture across military-community continuity decisions.

## Domain Toolchain Override (2026-04-07, Expansion Wave LXXVII Addendum)

- Add `toolchain_id=TC-DEERS-307`, `tool_suite_id=ts-joint-deers-id-card-eligibility-reconciliation-v1`, and `protocol_stack_id=ps-joint-deers-id-card-eligibility-reconciliation-stack-v1` when commander risk posture depends on sponsor-dependent eligibility integrity, blocked medical access, or family-support restoration for critical personnel.
- Add `toolchain_id=TC-MEBPEB-308`, `tool_suite_id=ts-joint-medical-evaluation-board-physical-evaluation-board-va-claim-continuity-v1`, and `protocol_stack_id=ps-joint-medical-evaluation-board-physical-evaluation-board-va-claim-continuity-stack-v1` when risk acceptance depends on trusted disability disposition, medical-board timing, or wounded-warrior transition legitimacy.
- Add `toolchain_id=TC-CLEAR-311`, `tool_suite_id=ts-joint-security-clearance-foreign-contact-record-correction-continuity-v1`, and `protocol_stack_id=ps-joint-security-clearance-foreign-contact-record-correction-continuity-stack-v1` when assignment viability or force availability depends on clearance integrity, foreign-contact adjudication, or record-correction speed.
- Add `packet_id=DPL-DEERS-ID-ELIGIBILITY-001`, `packet_id=DPL-MEB-PEB-VA-CLAIM-001`, and `packet_id=DPL-CLEARANCE-RECORD-CORRECTION-001` for branches that materially alter commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture across support-readiness decisions.

## Domain Toolchain Override (2026-04-07, Expansion Wave LXXVIII Addendum)

- Add `toolchain_id=TC-DD93BEN-315`, `tool_suite_id=ts-joint-dd93-sgli-tsgli-beneficiary-estate-readiness-continuity-v1`, and `protocol_stack_id=ps-joint-dd93-sgli-tsgli-beneficiary-estate-readiness-continuity-stack-v1` when commander risk posture depends on trusted DD93 or beneficiary integrity, casualty-notification readiness, or estate-document confidence for key personnel.
- Add `toolchain_id=TC-SKILLBRIDGE-316`, `tool_suite_id=ts-joint-skillbridge-career-skills-apprenticeship-employer-fellowship-continuity-v1`, and `protocol_stack_id=ps-joint-skillbridge-career-skills-apprenticeship-employer-fellowship-continuity-stack-v1` when retention, transition timing, or recovery posture depends on SkillBridge or employer-fellowship continuity for separating or recovering warfighters.
- Add `toolchain_id=TC-VAHOME-317`, `tool_suite_id=ts-joint-va-home-loan-guaranty-foreclosure-avoidance-housing-stability-v1`, and `protocol_stack_id=ps-joint-va-home-loan-guaranty-foreclosure-avoidance-housing-stability-stack-v1` when mission risk depends on preventing housing collapse, foreclosure pressure, or PCS or transition instability tied to the VA home-loan pipeline.
- Add `toolchain_id=TC-PROMO-318`, `tool_suite_id=ts-joint-promotion-board-evaluation-report-record-brief-continuity-v1`, and `protocol_stack_id=ps-joint-promotion-board-evaluation-report-record-brief-continuity-stack-v1` when force availability or assignment confidence depends on accurate board files, evaluation-report continuity, or record-brief integrity.
- Add `packet_id=DPL-DD93-SGLI-TSGLI-ESTATE-001`, `packet_id=DPL-SKILLBRIDGE-CSP-001`, `packet_id=DPL-VA-HOME-LOAN-HOUSING-001`, and `packet_id=DPL-PROMOTION-BOARD-RECORD-BRIEF-001` for branches that materially alter commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture across warfighter support-readiness decisions.

## Domain Toolchain Override (2026-04-07, Expansion Wave LXXIX Addendum)

- Add `toolchain_id=TC-PRIV-319`, `tool_suite_id=ts-joint-clinical-privileging-credentialing-deployment-readiness-v1`, and `protocol_stack_id=ps-joint-clinical-privileging-credentialing-deployment-readiness-stack-v1` when commander risk posture depends on deployable-provider legitimacy, scope-of-practice trust, or privileging friction inside medical formations.
- Add `toolchain_id=TC-GTCC-320`, `tool_suite_id=ts-joint-government-travel-charge-card-mission-travel-continuity-v1`, and `protocol_stack_id=ps-joint-government-travel-charge-card-mission-travel-continuity-stack-v1` when risk posture depends on restoring lawful official travel after card delinquency, suspended accounts, or reimbursement backlog.
- Add `toolchain_id=TC-PAYINC-321`, `tool_suite_id=ts-joint-special-pay-bah-cola-incentive-continuity-v1`, and `protocol_stack_id=ps-joint-special-pay-bah-cola-incentive-continuity-stack-v1` when mission confidence depends on location-based pay trust, bonus continuity, or special-pay certification for key personnel.
- Add `packet_id=DPL-CLINICAL-PRIVILEGING-DEPLOYMENT-001`, `packet_id=DPL-GTCC-MISSION-TRAVEL-001`, and `packet_id=DPL-SPECIAL-PAY-BAH-COLA-INCENTIVE-001` for branches that materially alter commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture across support-readiness decisions.

## Domain Toolchain Override (2026-04-07, Expansion Wave LXXXI Addendum)

- Add `toolchain_id=TC-CMDSP-323`, `tool_suite_id=ts-joint-command-sponsorship-overseas-screening-no-fee-passport-continuity-v1`, and `protocol_stack_id=ps-joint-command-sponsorship-overseas-screening-no-fee-passport-continuity-stack-v1` when commander risk posture depends on lawful overseas family movement, no-fee passport continuity, or command-sponsorship legitimacy for critical personnel.
- Add `toolchain_id=TC-POV-324`, `tool_suite_id=ts-joint-pov-shipment-driver-license-registration-continuity-v1`, and `protocol_stack_id=ps-joint-pov-shipment-driver-license-registration-continuity-stack-v1` when household transport breakdown, POV shipment delay, or driving-legality friction starts to change readiness risk.
- Add `toolchain_id=TC-CDCFEE-325`, `tool_suite_id=ts-joint-child-development-center-fee-assistance-duty-shift-continuity-v1`, and `protocol_stack_id=ps-joint-child-development-center-fee-assistance-duty-shift-continuity-stack-v1` when childcare collapse, fee-assistance loss, or shift-coverage strain changes GO or NO-GO posture.
- Add `toolchain_id=TC-STULOAN-326`, `tool_suite_id=ts-joint-federal-student-loan-deferment-fafsa-college-reentry-continuity-v1`, and `protocol_stack_id=ps-joint-federal-student-loan-deferment-fafsa-college-reentry-continuity-stack-v1` when education-finance instability, missed FAFSA deadlines, or student-loan protection failures materially affect retention or household resilience.
- Add `packet_id=DPL-CMD-SPONSOR-OVERSEAS-SCREEN-001`, `packet_id=DPL-POV-SHIPMENT-LICENSE-REG-001`, `packet_id=DPL-CDC-FEE-SHIFT-CONTINUITY-001`, and `packet_id=DPL-STUDENT-LOAN-FAFSA-REENTRY-001` for branches that materially alter commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture across American-warfighter support decisions.

## Domain Toolchain Override (2026-04-07, Expansion Wave LXXXII Addendum)

- Add `toolchain_id=TC-TBHEALTH-327`, `tool_suite_id=ts-joint-telebehavioral-health-burnout-suicide-risk-continuity-v1`, and `protocol_stack_id=ps-joint-telebehavioral-health-burnout-suicide-risk-continuity-stack-v1` when commander risk posture depends on remote behavioral-health continuity, burnout mitigation, or suicide-risk escalation for key personnel or families.
- Add `toolchain_id=TC-HOMELESS-328`, `tool_suite_id=ts-joint-military-homelessness-prevention-transitional-housing-bridge-v1`, and `protocol_stack_id=ps-joint-military-homelessness-prevention-transitional-housing-bridge-stack-v1` when household displacement, unsafe shelter, or homelessness risk begins to alter force availability or recovery confidence.
- Add `toolchain_id=TC-BANKR-329`, `tool_suite_id=ts-joint-bankruptcy-consumer-protection-clearance-financial-distress-v1`, and `protocol_stack_id=ps-joint-bankruptcy-consumer-protection-clearance-financial-distress-stack-v1` when debt distress, bankruptcy pressure, or creditor action changes clearance confidence, assignment viability, or travel readiness.
- Add `toolchain_id=TC-DOXX-330`, `tool_suite_id=ts-joint-family-online-harassment-doxxing-protective-escalation-v1`, and `protocol_stack_id=ps-joint-family-online-harassment-doxxing-protective-escalation-stack-v1` when targeted harassment, swatting risk, or doxxing creates a force-protection branch that should alter commander risk acceptance.
- Add `toolchain_id=TC-COMPASS-331`, `tool_suite_id=ts-joint-compassionate-reassignment-hardship-discharge-humanitarian-transfer-v1`, and `protocol_stack_id=ps-joint-compassionate-reassignment-hardship-discharge-humanitarian-transfer-stack-v1` when family crisis, caregiving burden, or hardship may require compassionate personnel routing rather than ordinary retention or leave assumptions.
- Add `packet_id=DPL-TELEBEHAVIORAL-BURNOUT-SUICIDE-001`, `packet_id=DPL-HOMELESSNESS-TRANSITIONAL-HOUSING-001`, `packet_id=DPL-BANKRUPTCY-CLEARANCE-DISTRESS-001`, `packet_id=DPL-FAMILY-ONLINE-HARASSMENT-DOXXING-001`, and `packet_id=DPL-COMPASSIONATE-REASSIGNMENT-HARDSHIP-001` for branches that materially alter commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture across American-warfighter human-readiness decisions.

## Domain Toolchain Override (2026-04-07, Expansion Wave LXXXIII Addendum)

- Add `toolchain_id=TC-TAMPHC-332`, `tool_suite_id=ts-joint-transitional-healthcare-tamp-chcbp-pharmacy-bridge-v1`, and `protocol_stack_id=ps-joint-transitional-healthcare-tamp-chcbp-pharmacy-bridge-stack-v1` when commander risk posture depends on preserving treatment access, pharmacy continuity, or lawful medical coverage during separation, demobilization, or medical transition.
- Add `toolchain_id=TC-VACARE-333`, `tool_suite_id=ts-joint-va-caregiver-support-program-stipend-training-respite-continuity-v1`, and `protocol_stack_id=ps-joint-va-caregiver-support-program-stipend-training-respite-continuity-stack-v1` when recovery confidence depends on caregiver sustainment, respite viability, or stipend continuity for key wounded-warrior households.
- Add `toolchain_id=TC-VREIL-334`, `tool_suite_id=ts-joint-vre-independent-living-adaptive-employment-continuity-v1`, and `protocol_stack_id=ps-joint-vre-independent-living-adaptive-employment-continuity-stack-v1` when long-tail force-management, retention, or transition risk depends on adaptive employment, vocational-rehabilitation routing, or independent-living support.
- Add `toolchain_id=TC-SAHAA-335`, `tool_suite_id=ts-joint-specially-adapted-housing-automobile-allowance-home-accessibility-benefit-bridge-v1`, and `protocol_stack_id=ps-joint-specially-adapted-housing-automobile-allowance-home-accessibility-benefit-bridge-stack-v1` when recovery risk depends on adaptive-housing execution, vehicle mobility, or home-accessibility benefit legitimacy.
- Add `toolchain_id=TC-MEDHOLD-336`, `tool_suite_id=ts-joint-convalescent-leave-limited-duty-medical-hold-continuity-v1`, and `protocol_stack_id=ps-joint-convalescent-leave-limited-duty-medical-hold-continuity-stack-v1` when commander acceptance depends on lawful recovery orders, convalescent leave, medhold continuity, or limited-duty legitimacy.
- Add `packet_id=DPL-TRANSITIONAL-HEALTHCARE-TAMP-CHCBP-001`, `packet_id=DPL-VA-CAREGIVER-STIPEND-RESPITE-001`, `packet_id=DPL-VRE-INDEPENDENT-LIVING-001`, `packet_id=DPL-SAH-AUTOMOBILE-HOME-ACCESS-001`, and `packet_id=DPL-CONVALESCENT-LEAVE-MEDHOLD-001` for branches that materially alter commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture across wounded-warrior recovery and transition decisions.

## Domain Toolchain Override (2026-04-07, Expansion Wave LXXXV Addendum)

- Add `toolchain_id=TC-PARENTAL-343`, `tool_suite_id=ts-joint-parental-leave-pregnancy-postpartum-profile-duty-modification-continuity-v1`, and `protocol_stack_id=ps-joint-parental-leave-pregnancy-postpartum-profile-duty-modification-continuity-stack-v1` when commander risk posture depends on lawful parental leave, pregnancy or postpartum profile legitimacy, or safe duty-modification branches.
- Add `toolchain_id=TC-NEWBORN-344`, `tool_suite_id=ts-joint-newborn-birth-certificate-deers-tricare-travel-document-bridge-v1`, and `protocol_stack_id=ps-joint-newborn-birth-certificate-deers-tricare-travel-document-bridge-stack-v1` when readiness risk depends on newborn documentation, DEERS or TRICARE enrollment, or family-travel legitimacy during PCS, deployment, or OCONUS assignment.
- Add `toolchain_id=TC-IGEO-345`, `tool_suite_id=ts-joint-inspector-general-equal-opportunity-reprisal-complaint-safeguard-v1`, and `protocol_stack_id=ps-joint-inspector-general-equal-opportunity-reprisal-complaint-safeguard-stack-v1` when protected reporting, reprisal pressure, or command-climate risk changes acceptable commander risk.
- Add `toolchain_id=TC-LODPAY-346`, `tool_suite_id=ts-joint-line-of-duty-incapacitation-pay-duty-status-continuity-v1`, and `protocol_stack_id=ps-joint-line-of-duty-incapacitation-pay-duty-status-continuity-stack-v1` when injury-driven duty status, incapacitation pay, or legal availability becomes a mission-risk driver.
- Add `toolchain_id=TC-AWARDS-347`, `tool_suite_id=ts-joint-awards-decorations-valor-board-record-protection-v1`, and `protocol_stack_id=ps-joint-awards-decorations-valor-board-record-protection-stack-v1` when recognition integrity, morale, or board-record trust materially affects retention or assignment confidence.
- Add `toolchain_id=TC-FINALOUT-348`, `tool_suite_id=ts-joint-final-out-processing-cif-ocie-medical-dental-separation-clearance-v1`, and `protocol_stack_id=ps-joint-final-out-processing-cif-ocie-medical-dental-separation-clearance-stack-v1` when DD214 timing, separation legitimacy, or final-out friction changes force-flow or transition risk.
- Add `packet_id=DPL-PARENTAL-LEAVE-PREG-POSTPARTUM-001`, `packet_id=DPL-NEWBORN-DEERS-TRICARE-DOCS-001`, `packet_id=DPL-IG-EO-REPRISAL-SAFEGUARD-001`, `packet_id=DPL-LOD-INCAP-PAY-DUTY-STATUS-001`, `packet_id=DPL-AWARDS-DECORATIONS-BOARD-001`, and `packet_id=DPL-FINAL-OUT-CIF-SEPARATION-001` for branches that materially alter commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture across personnel-lifecycle readiness decisions.

## Domain Toolchain Override (2026-04-11, Expansion Wave LXXXVI Addendum)

- Add `toolchain_id=TC-NJPSEP-349`, `tool_suite_id=ts-joint-nonjudicial-punishment-letter-of-reprimand-administrative-separation-continuity-v1`, and `protocol_stack_id=ps-joint-nonjudicial-punishment-letter-of-reprimand-administrative-separation-continuity-stack-v1` when adverse-action timelines, rebuttal windows, or separation exposure materially change commander risk acceptance.
- Add `toolchain_id=TC-CMART-350`, `tool_suite_id=ts-joint-court-martial-defense-counsel-discovery-expert-witness-travel-continuity-v1`, and `protocol_stack_id=ps-joint-court-martial-defense-counsel-discovery-expert-witness-travel-continuity-stack-v1` when defense-support logistics, discovery delay, or witness access materially alter readiness and family-stability risk.
- Add `toolchain_id=TC-UIFGOMOR-351`, `tool_suite_id=ts-joint-unfavorable-information-file-gomor-board-record-rebuttal-continuity-v1`, and `protocol_stack_id=ps-joint-unfavorable-information-file-gomor-board-record-rebuttal-continuity-stack-v1` when adverse-record integrity or board-file contamination distorts mission-risk assumptions about assignment, retention, or promotion trust.
- Add `toolchain_id=TC-SORCLR-352`, `tool_suite_id=ts-joint-security-clearance-suspension-revocation-statement-of-reasons-response-v1`, and `protocol_stack_id=ps-joint-security-clearance-suspension-revocation-statement-of-reasons-response-stack-v1` when clearance suspension, revocation risk, or statement-of-reasons deadlines change acceptable access and force-posture risk.
- Add `toolchain_id=TC-DRBBCMR-353`, `tool_suite_id=ts-joint-discharge-review-board-bcmr-character-of-service-va-eligibility-bridge-v1`, and `protocol_stack_id=ps-joint-discharge-review-board-bcmr-character-of-service-va-eligibility-bridge-stack-v1` when discharge-redress friction, character-of-service disputes, or VA-eligibility loss materially affect long-tail readiness and recovery.
- Add `toolchain_id=TC-A138-354`, `tool_suite_id=ts-joint-article-138-congressional-casework-record-preservation-escalation-v1`, and `protocol_stack_id=ps-joint-article-138-congressional-casework-record-preservation-escalation-stack-v1` when protected escalation, congressional casework, or evidence-preservation failures alter command-trust risk.
- Add `packet_id=DPL-NJP-LOR-ADMINSEP-001`, `packet_id=DPL-COURT-MARTIAL-DEFENSE-001`, `packet_id=DPL-UIF-GOMOR-BOARD-001`, `packet_id=DPL-CLEARANCE-SOR-SUSP-REVOCATION-001`, `packet_id=DPL-DRB-BCMR-CHARACTER-VA-001`, and `packet_id=DPL-ARTICLE-138-CONGRESSIONAL-001` for branches that materially alter commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture across administrative-justice and redress decisions.

## Domain Toolchain Override (2026-04-11, Expansion Wave LXXXVII Addendum)

- Add `toolchain_id=TC-IMR-332`, `tool_suite_id=ts-joint-individual-medical-readiness-immunization-pha-dental-continuity-v1`, and `protocol_stack_id=ps-joint-individual-medical-readiness-immunization-pha-dental-continuity-stack-v1` when commander risk posture depends on IMR evidence, immunization status, PHA completion, or dental deployability for key personnel.
- Add `toolchain_id=TC-LODINCAP-333`, `tool_suite_id=ts-reserve-component-line-of-duty-incapacitation-pay-medical-hold-continuity-v1`, and `protocol_stack_id=ps-reserve-component-line-of-duty-incapacitation-pay-medical-hold-continuity-stack-v1` when mobilization or recovery risk depends on LOD legitimacy, incapacitation-pay continuity, or medical-hold status.
- Add `toolchain_id=TC-TAPBRIDGE-334`, `tool_suite_id=ts-joint-transition-assistance-vre-dol-federal-hiring-bridge-v1`, and `protocol_stack_id=ps-joint-transition-assistance-vre-dol-federal-hiring-bridge-stack-v1` when TAP milestones, VR&E continuity, or federal-hiring readiness materially change transition-risk assumptions.
- Add `toolchain_id=TC-FAMNET-335`, `tool_suite_id=ts-joint-family-readiness-group-ombudsman-key-spouse-communication-v1`, and `protocol_stack_id=ps-joint-family-readiness-group-ombudsman-key-spouse-communication-stack-v1` when verified household communication, volunteer-network health, or rumor-control posture changes family-readiness risk.
- Add `toolchain_id=TC-ONESOURCE-336`, `tool_suite_id=ts-joint-military-onesource-nonmedical-counseling-peer-support-v1`, and `protocol_stack_id=ps-joint-military-onesource-nonmedical-counseling-peer-support-stack-v1` when non-medical counseling or peer-support availability materially changes stress-driven readiness loss risk.
- Add `toolchain_id=TC-COOLMAP-337`, `tool_suite_id=ts-joint-cool-usmap-credentialing-pathway-continuity-v1`, and `protocol_stack_id=ps-joint-cool-usmap-credentialing-pathway-continuity-stack-v1` when credential-path continuity, apprenticeship-hour capture, or voucher legitimacy affects retention, recovery, or transition confidence.
- Add `packet_id=DPL-IMR-PHA-DENTAL-001`, `packet_id=DPL-LOD-INCAP-MEDHOLD-001`, `packet_id=DPL-TAP-VRE-FEDHIRE-001`, `packet_id=DPL-FRG-OMBUDSMAN-KEY-SPOUSE-001`, `packet_id=DPL-ONESOURCE-PEER-SUPPORT-001`, and `packet_id=DPL-COOL-USMAP-CREDPATH-001` for branches that materially alter commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture across support-readiness and transition-continuity decisions.

## Domain Toolchain Override (2026-04-11, Expansion Wave LXXXVIII Addendum)

- Add `toolchain_id=TC-RESRET-355`, `tool_suite_id=ts-reserve-component-retirement-points-sanctuary-nonregular-retirement-continuity-v1`, and `protocol_stack_id=ps-reserve-component-retirement-points-sanctuary-nonregular-retirement-continuity-stack-v1` when reserve-force availability, sanctuary exposure, or long-horizon retention trust materially changes commander risk acceptance.
- Add `toolchain_id=TC-TRSRES-356`, `tool_suite_id=ts-reserve-component-tricare-reserve-select-retired-reserve-dental-eligibility-bridge-v1`, and `protocol_stack_id=ps-reserve-component-tricare-reserve-select-retired-reserve-dental-eligibility-bridge-stack-v1` when commander risk posture depends on preserving Reserve family healthcare continuity during duty-status change or demobilization.
- Add `toolchain_id=TC-EFMPSL-357`, `tool_suite_id=ts-joint-efmp-enrollment-assignment-coordination-school-liaison-continuity-v1`, and `protocol_stack_id=ps-joint-efmp-enrollment-assignment-coordination-school-liaison-continuity-stack-v1` when special-needs family movement, school continuity, or assignment coordination materially changes readiness assumptions.
- Add `toolchain_id=TC-GITEB-358`, `tool_suite_id=ts-joint-post-9-11-gi-bill-transferability-dependent-education-yellow-ribbon-continuity-v1`, and `protocol_stack_id=ps-joint-post-9-11-gi-bill-transferability-dependent-education-yellow-ribbon-continuity-stack-v1` when family education portability or service-obligation trust materially changes retention or transition risk.
- Add `toolchain_id=TC-MYCAA-359`, `tool_suite_id=ts-strategic-military-spouse-mycaa-portable-training-career-reentry-v1`, and `protocol_stack_id=ps-strategic-military-spouse-mycaa-portable-training-career-reentry-stack-v1` when spouse training restart or career reentry materially changes household stability and warfighter retention confidence.
- Add `toolchain_id=TC-PMHOUS-360`, `tool_suite_id=ts-joint-privatized-military-housing-tenant-rights-bah-recertification-claims-v1`, and `protocol_stack_id=ps-joint-privatized-military-housing-tenant-rights-bah-recertification-claims-stack-v1` when unsafe housing, BAH recertification friction, or unresolved claims materially changes readiness risk.
- Add `toolchain_id=TC-HUMREAD-361`, `tool_suite_id=ts-joint-command-team-human-readiness-case-conference-escalation-v1`, and `protocol_stack_id=ps-joint-command-team-human-readiness-case-conference-escalation-stack-v1` when fragmented support lanes or unresolved household strain materially changes mission-risk posture.
- Add `packet_id=DPL-RESERVE-RETIREMENT-SANCTUARY-001`, `packet_id=DPL-TRS-TRR-DENTAL-ELIGIBILITY-001`, `packet_id=DPL-EFMP-ASSIGNMENT-SCHOOL-001`, `packet_id=DPL-GI-BILL-TEB-YELLOW-RIBBON-001`, `packet_id=DPL-MYCAA-TRAINING-CAREER-001`, `packet_id=DPL-PRIVATIZED-HOUSING-BAH-CLAIMS-001`, and `packet_id=DPL-HUMAN-READINESS-CASE-CONFERENCE-001` for branches that materially alter commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture across reserve-lifecycle and household-portability decisions.

## Domain Toolchain Override (2026-04-11, Expansion Wave LXXXIX Addendum)

- Add `toolchain_id=TC-UATOUR-362`, `tool_suite_id=ts-joint-unaccompanied-tour-family-separation-allowance-deferred-travel-continuity-v1`, and `protocol_stack_id=ps-joint-unaccompanied-tour-family-separation-allowance-deferred-travel-continuity-stack-v1` when commander risk posture depends on separated-family legitimacy, unaccompanied-tour order integrity, or deferred-travel confidence for key personnel.
- Add `toolchain_id=TC-TAXDOM-363`, `tool_suite_id=ts-joint-state-tax-domicile-residency-withholding-continuity-v1`, and `protocol_stack_id=ps-joint-state-tax-domicile-residency-withholding-continuity-stack-v1` when household tax conflict, double-withholding exposure, or legal-residence uncertainty materially changes retention or availability risk.
- Add `toolchain_id=TC-SCHTRN-364`, `tool_suite_id=ts-joint-military-child-school-transfer-transcript-graduation-continuity-v1`, and `protocol_stack_id=ps-joint-military-child-school-transfer-transcript-graduation-continuity-stack-v1` when dependent school-transfer friction, transcript loss, or graduation-risk pressure changes acceptable commander risk.
- Add `toolchain_id=TC-AUTOFIN-365`, `tool_suite_id=ts-joint-consumer-auto-loan-repossession-insurance-gap-transportation-continuity-v1`, and `protocol_stack_id=ps-joint-consumer-auto-loan-repossession-insurance-gap-transportation-continuity-stack-v1` when household transport collapse, repossession exposure, or uninsured mobility materially changes reporting confidence or family stability.
- Add `packet_id=DPL-UNACCOMP-FSA-DEFER-001`, `packet_id=DPL-STATE-TAX-DOMICILE-001`, `packet_id=DPL-SCHOOL-TRANSFER-GRAD-001`, and `packet_id=DPL-AUTO-REPO-TRANSPORT-001` for branches that materially alter commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture across separated-family, tax-legitimacy, dependent-school, and transport-continuity decisions.

## Domain Toolchain Override (2026-04-11, Expansion Wave XC Addendum)

- Add `toolchain_id=TC-MYPAY-366`, `tool_suite_id=ts-joint-mypay-les-allotment-payroll-access-continuity-v1`, and `protocol_stack_id=ps-joint-mypay-les-allotment-payroll-access-continuity-stack-v1` when commander risk posture depends on payroll self-service legitimacy, LES correction speed, or broken allotments for key personnel.
- Add `toolchain_id=TC-REENLIST-367`, `tool_suite_id=ts-joint-reenlistment-selective-retention-bonus-career-field-reclassification-continuity-v1`, and `protocol_stack_id=ps-joint-reenlistment-selective-retention-bonus-career-field-reclassification-continuity-stack-v1` when retention confidence, billet fill, or lawful availability depends on reenlistment windows, SRB legitimacy, or reclassification routing.
- Add `toolchain_id=TC-BARRDORM-368`, `tool_suite_id=ts-joint-barracks-dorm-work-order-bah-exception-emergency-relocation-continuity-v1`, and `protocol_stack_id=ps-joint-barracks-dorm-work-order-bah-exception-emergency-relocation-continuity-stack-v1` when unsafe living quarters, delayed work orders, or BAH-exception routing materially changes commander risk acceptance.
- Add `toolchain_id=TC-KITISS-369`, `tool_suite_id=ts-joint-initial-issue-cif-ocie-clothing-record-mobilization-kitting-continuity-v1`, and `protocol_stack_id=ps-joint-initial-issue-cif-ocie-clothing-record-mobilization-kitting-continuity-stack-v1` when reporting reliability or deployment timing depends on missing issue, clothing-record drift, or substitute-kit legitimacy.
- Add `toolchain_id=TC-LEAVE-370`, `tool_suite_id=ts-joint-leave-carryover-special-leave-accrual-sell-back-continuity-v1`, and `protocol_stack_id=ps-joint-leave-carryover-special-leave-accrual-sell-back-continuity-stack-v1` when use-or-lose exposure, SLA failure, or leave-balance drift materially changes recovery or retention risk.
- Add `toolchain_id=TC-PROFILE-371`, `tool_suite_id=ts-joint-duty-limiting-profile-accommodation-nondeployable-code-continuity-v1`, and `protocol_stack_id=ps-joint-duty-limiting-profile-accommodation-nondeployable-code-continuity-stack-v1` when stale profiles, missing accommodations, or wrong nondeployable codes materially distort deployability assumptions.
- Add `packet_id=DPL-MYPAY-LES-ALLOTMENT-001`, `packet_id=DPL-REENLISTMENT-SRB-RECLASS-001`, `packet_id=DPL-BARRACKS-DORM-BAH-RELOCATE-001`, `packet_id=DPL-INITIAL-ISSUE-KITTING-001`, `packet_id=DPL-LEAVE-SLA-SELLBACK-001`, and `packet_id=DPL-PROFILE-NONDEPLOY-CODE-001` for branches that materially alter commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture across payroll legitimacy, retention continuity, housing safety, kitting readiness, leave correctness, and profile-driven availability decisions.

## Domain Toolchain Override (2026-04-11, Expansion Wave XCII Addendum)

- Add `toolchain_id=TC-AVPAY-378`, `tool_suite_id=ts-joint-aviation-incentive-pay-aeronautical-order-gate-month-continuity-v1`, and `protocol_stack_id=ps-joint-aviation-incentive-pay-aeronautical-order-gate-month-continuity-stack-v1` when commander risk posture depends on trusted aeronautical-order validity, gate-month evidence, or aviation-pay legitimacy for critical aircrew.
- Add `toolchain_id=TC-HAZPAY-379`, `tool_suite_id=ts-joint-hazardous-duty-jump-dive-special-duty-pay-certification-continuity-v1`, and `protocol_stack_id=ps-joint-hazardous-duty-jump-dive-special-duty-pay-certification-continuity-stack-v1` when hazardous-duty certification, jump or dive currency, or special-duty pay legitimacy materially changes deployability assumptions.
- Add `toolchain_id=TC-PME-380`, `tool_suite_id=ts-joint-professional-military-education-school-seat-waiver-promotion-prerequisite-continuity-v1`, and `protocol_stack_id=ps-joint-professional-military-education-school-seat-waiver-promotion-prerequisite-continuity-stack-v1` when school-seat loss, waiver delay, or prerequisite drift changes command confidence in promotion-timed billet fill.
- Add `toolchain_id=TC-POLY-381`, `tool_suite_id=ts-joint-security-clearance-polygraph-continuous-vetting-readiness-v1`, and `protocol_stack_id=ps-joint-security-clearance-polygraph-continuous-vetting-readiness-stack-v1` when polygraph delay, vetting-alert backlog, or mission-access uncertainty materially changes acceptable commander risk.
- Add `toolchain_id=TC-LANG-382`, `tool_suite_id=ts-joint-foreign-language-proficiency-bonus-dlpt-linguist-readiness-continuity-v1`, and `protocol_stack_id=ps-joint-foreign-language-proficiency-bonus-dlpt-linguist-readiness-continuity-stack-v1` when expired language qualification, DLPT backlog, or FLPB friction degrades mission-language coverage for key personnel.
- Add `toolchain_id=TC-BROADEN-383`, `tool_suite_id=ts-joint-advanced-civil-schooling-fellowship-broadening-assignment-continuity-v1`, and `protocol_stack_id=ps-joint-advanced-civil-schooling-fellowship-broadening-assignment-continuity-stack-v1` when schooling, fellowship, or broadening-assignment drift changes retention confidence, mid-career talent-development timing, or command succession assumptions.
- Add `packet_id=DPL-AVIATION-PAY-AERO-ORDER-001`, `packet_id=DPL-HAZDUTY-JUMP-DIVE-CERT-001`, `packet_id=DPL-PME-SCHOOL-SEAT-PREREQ-001`, `packet_id=DPL-POLYGRAPH-CONTINUOUS-VETTING-001`, `packet_id=DPL-FLPB-DLPT-LINGUIST-001`, and `packet_id=DPL-ACS-FELLOWSHIP-BROADENING-001` for branches that materially alter commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture across career-readiness, mission-access, and deliberate talent-management decisions.

## Domain Toolchain Override (2026-04-11, Expansion Wave XCIII Addendum)

- Add `toolchain_id=TC-ARTCARE-384`, `tool_suite_id=ts-joint-assisted-reproductive-care-fertility-preservation-cryostorage-continuity-v1`, and `protocol_stack_id=ps-joint-assisted-reproductive-care-fertility-preservation-cryostorage-continuity-stack-v1` when commander risk posture depends on preserving ART access, fertility-preservation timing, or cryostorage integrity for key warfighters and families.
- Add `toolchain_id=TC-SURRO-385`, `tool_suite_id=ts-joint-surrogacy-parentage-newborn-documentation-dependent-enrollment-continuity-v1`, and `protocol_stack_id=ps-joint-surrogacy-parentage-newborn-documentation-dependent-enrollment-continuity-stack-v1` when family-formation legality, newborn-document continuity, or dependent-enrollment delay changes acceptable commander risk.
- Add `toolchain_id=TC-MEPS-386`, `tool_suite_id=ts-joint-meps-medical-waiver-moral-screening-ship-date-continuity-v1`, and `protocol_stack_id=ps-joint-meps-medical-waiver-moral-screening-ship-date-continuity-stack-v1` when accession throughput, waiver delay, or ship-date drift materially changes force-generation assumptions.
- Add `toolchain_id=TC-COMMISSION-387`, `tool_suite_id=ts-joint-rotc-service-academy-ocs-ots-commissioning-file-continuity-v1`, and `protocol_stack_id=ps-joint-rotc-service-academy-ocs-ots-commissioning-file-continuity-stack-v1` when commissioning-file drift, qualification gaps, or delayed appointments materially change future billet-fill confidence.
- Add `toolchain_id=TC-IET-388`, `tool_suite_id=ts-joint-initial-entry-training-holdover-recycle-family-separation-continuity-v1`, and `protocol_stack_id=ps-joint-initial-entry-training-holdover-recycle-family-separation-continuity-stack-v1` when trainee holdovers, recycle decisions, or family-separation friction materially change acceptable risk in the training pipeline.
- Add `toolchain_id=TC-SCHOOLHOUSE-389`, `tool_suite_id=ts-joint-high-attrition-schoolhouse-selection-recycle-medhold-follow-on-orders-continuity-v1`, and `protocol_stack_id=ps-joint-high-attrition-schoolhouse-selection-recycle-medhold-follow-on-orders-continuity-stack-v1` when special-duty schoolhouse attrition, medhold delay, or follow-on-orders drift materially changes talent-retention or readiness assumptions.
- Add `packet_id=DPL-ART-CRYOSTORAGE-001`, `packet_id=DPL-SURROGACY-PARENTAGE-001`, `packet_id=DPL-MEPS-WAIVER-SHIP-001`, `packet_id=DPL-COMMISSIONING-FILE-001`, `packet_id=DPL-IET-HOLDOVER-RECYCLE-001`, and `packet_id=DPL-SCHOOLHOUSE-RECYCLE-MEDHOLD-001` for branches that materially alter commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture across family-building and force-generation decisions.

## Domain Toolchain Override (2026-04-11, Expansion Wave XCIV Addendum)

- Add `toolchain_id=TC-DUALMIL-390`, `tool_suite_id=ts-joint-dual-military-colocation-career-field-alignment-dependent-care-continuity-v1`, and `protocol_stack_id=ps-joint-dual-military-colocation-career-field-alignment-dependent-care-continuity-stack-v1` when commander risk posture depends on dual-military assignment stability, co-location feasibility, or dependent-care sufficiency for key personnel.
- Add `toolchain_id=TC-SOFA-391`, `tool_suite_id=ts-joint-overseas-spouse-work-authorization-host-nation-banking-driver-license-continuity-v1`, and `protocol_stack_id=ps-joint-overseas-spouse-work-authorization-host-nation-banking-driver-license-continuity-stack-v1` when acceptable risk depends on whether a moved family can lawfully work, bank, drive, and remain stable overseas.
- Add `toolchain_id=TC-TELEHEALTH-392`, `tool_suite_id=ts-joint-cross-state-telehealth-licensure-compact-specialty-access-continuity-v1`, and `protocol_stack_id=ps-joint-cross-state-telehealth-licensure-compact-specialty-access-continuity-stack-v1` when readiness or retention depends on timely specialty care that can only be preserved through remote-state telehealth routing.
- Add `toolchain_id=TC-SPECIALMED-393`, `tool_suite_id=ts-joint-diver-submariner-pressure-qualification-special-duty-medical-continuity-v1`, and `protocol_stack_id=ps-joint-diver-submariner-pressure-qualification-special-duty-medical-continuity-stack-v1` when undersea or special-duty medical qualification materially changes force availability, sea-duty legitimacy, or mission confidence.
- Add `toolchain_id=TC-ENOTARY-394`, `tool_suite_id=ts-joint-remote-notary-digital-signature-emergency-legal-document-execution-v1`, and `protocol_stack_id=ps-joint-remote-notary-digital-signature-emergency-legal-document-execution-stack-v1` when commander confidence depends on trusted emergency document execution for POA, guardianship, ballot cure, or casualty-preparation actions.
- Add `toolchain_id=TC-CDLHAZ-395`, `tool_suite_id=ts-joint-military-driver-qualification-cdl-hazmat-convoy-license-continuity-v1`, and `protocol_stack_id=ps-joint-military-driver-qualification-cdl-hazmat-convoy-license-continuity-stack-v1` when sustainment viability depends on legally qualified drivers with current CDL, hazmat, or convoy credentials.
- Add `packet_id=DPL-DUAL-MIL-COLOCATION-001`, `packet_id=DPL-SPOUSE-WORKAUTH-BANK-DRIVER-001`, `packet_id=DPL-TELEHEALTH-LICENSURE-SPECIALTY-001`, `packet_id=DPL-DIVER-SUBMARINER-MEDQUAL-001`, `packet_id=DPL-REMOTE-NOTARY-DOCEXEC-001`, and `packet_id=DPL-MIL-DRIVER-CDL-HAZMAT-001` for branches that materially alter commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture across household stability, medical access, legal execution, and sustainment force flow.

## Domain Toolchain Override (2026-04-12, Expansion Wave XCV Addendum)

- Add `toolchain_id=TC-DLATLE-396`, `tool_suite_id=ts-joint-dislocation-allowance-temporary-lodging-expense-temporary-lodging-allowance-continuity-v1`, and `protocol_stack_id=ps-joint-dislocation-allowance-temporary-lodging-expense-temporary-lodging-allowance-continuity-stack-v1` when commander risk posture depends on whether lodging-cost shocks or delayed reimbursement will break PCS execution or reporting reliability.
- Add `toolchain_id=TC-OHA-397`, `tool_suite_id=ts-joint-overseas-housing-allowance-utility-reconciliation-lease-continuity-v1`, and `protocol_stack_id=ps-joint-overseas-housing-allowance-utility-reconciliation-lease-continuity-stack-v1` when overseas assignment stability depends on lawful lease posture, utility continuity, or housing-allowance trust.
- Add `toolchain_id=TC-OCOLA-398`, `tool_suite_id=ts-joint-overseas-cola-post-allowance-currency-shock-continuity-v1`, and `protocol_stack_id=ps-joint-overseas-cola-post-allowance-currency-shock-continuity-stack-v1` when acceptable commander risk depends on whether exchange-rate shock or locality-lag will destabilize key overseas households.
- Add `toolchain_id=TC-BASMESS-399`, `tool_suite_id=ts-joint-basic-allowance-for-subsistence-meal-card-messing-debt-continuity-v1`, and `protocol_stack_id=ps-joint-basic-allowance-for-subsistence-meal-card-messing-debt-continuity-stack-v1` when food access, BAS accuracy, or messing-debt drift materially changes household stability or retention confidence.
- Add `toolchain_id=TC-SPACEA-400`, `tool_suite_id=ts-joint-space-available-travel-emergency-leave-nonmedical-attendant-priority-continuity-v1`, and `protocol_stack_id=ps-joint-space-available-travel-emergency-leave-nonmedical-attendant-priority-continuity-stack-v1` when bedside or family-crisis travel timing materially changes command risk acceptance for affected personnel.
- Add `toolchain_id=TC-GEOBACH-401`, `tool_suite_id=ts-joint-geographic-bachelor-housing-exception-separate-rations-continuity-v1`, and `protocol_stack_id=ps-joint-geographic-bachelor-housing-exception-separate-rations-continuity-stack-v1` when split-household strain, housing-exception delay, or separate-rations drift materially changes lawful availability assumptions.
- Add `packet_id=DPL-DLA-TLE-TLA-001`, `packet_id=DPL-OHA-LEASE-UTILITY-001`, `packet_id=DPL-OCOLA-POST-CURRENCY-001`, `packet_id=DPL-BAS-MEALCARD-MESS-001`, `packet_id=DPL-SPACEA-EMERGENCY-ATTENDANT-001`, and `packet_id=DPL-GEOBACH-SEPRATS-001` for branches that materially alter commander GO, NO-GO, or GO-WITH-CONSTRAINTS posture across housing, overseas-cost, subsistence, compassionate-travel, and split-household continuity.
