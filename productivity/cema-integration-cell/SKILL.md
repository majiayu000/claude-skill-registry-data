---
name: cema-integration-cell
description: Integrate cyber and electromagnetic activities into joint operations. Use when synchronizing cyber effects, EW actions, and information actions with maneuver and fires.
---

# CEMA Integration Cell

## Mission Scope

- Treat this skill as a planning and decision-support aid for U.S. warfighter missions in its domain.
- Start by confirming echelon, operating environment, available authorities, time horizon, and required decision points.
- Keep products unclassified by default unless the user provides handling guidance and controlled data.

## Workflow

1. Frame the mission problem using domain-specific inputs and command objectives.
2. Identify assumptions, decision thresholds, and what reporting would invalidate the current plan.
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

Primary products for this skill: CEMA synchronization matrix, effects-to-objectives crosswalk, cyber-EW deconfliction plan.

## External Tools and Protocol Integration

- Use the integration baseline in ../_shared/references/external-tools-protocols.md and name the exact tools selected for this mission set.
- Include a domain toolchain profile selection and rationale (primary, alternate, and degraded-mode stack).
- Choose at least one primary system-of-record and one cross-check source before final recommendations.
- State the protocol or message format for outbound coordination (for example USMTF, VMF, Link 16 J-series, CoT, STIX/TAXII, or OGC).
- Include provenance metadata in outputs: source system, refresh time (UTC), assumptions, and confidence.

## Interoperability Validation Checklist

- Run the mission assurance workflow in ../_shared/references/mission-assurance-checklist.md before final release.
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

## Domain Toolchain Override (2026-03-15, Expansion Wave LII Addendum)

- Add `tool_suite_id=ts-theater-sdr-waveform-key-hopset-emergency-reconstitution-v1` + `protocol_stack_id=ps-theater-sdr-waveform-key-hopset-emergency-reconstitution-stack-v1` when CEMA synchronization depends on rapid rekey, hopset regeneration, or trusted waveform restoration after compromise.
- Add `tool_suite_id=ts-joint-directed-energy-airspace-reflection-safety-v1` + `protocol_stack_id=ps-joint-directed-energy-airspace-reflection-safety-stack-v1` when electromagnetic or directed-energy branches depend on beam safety, airspace release, or reflective-surface hazard control.
- Add `packet_id=DPL-SDR-WAVEFORM-KEY-HOPSET-001` and `packet_id=DPL-DIRECTED-ENERGY-AIRSPACE-REFLECTION-SAFETY-001` for branches that materially alter spectrum posture, beam release, or tactical-network trust.

## Domain Toolchain Override (2026-03-15, Expansion Wave LVI Gap-Closure Addendum)

- Add `tool_suite_id=ts-joint-signals-intelligence-emitter-geolocation-fusion-v1` + `protocol_stack_id=ps-joint-signals-intelligence-emitter-geolocation-fusion-stack-v1` when CEMA synchronization depends on emitter-confidence adjudication, cross-cue speed, or geolocation uncertainty management.
- Add `tool_suite_id=ts-joint-expeditionary-advanced-base-signature-management-v1` + `protocol_stack_id=ps-joint-expeditionary-advanced-base-signature-management-stack-v1` when electromagnetic survivability depends on expeditionary emissions discipline, decoy timing, or base displacement windows.
- Add `tool_suite_id=ts-joint-orbital-warfare-effects-deconfliction-v1` + `protocol_stack_id=ps-joint-orbital-warfare-effects-deconfliction-stack-v1` when space-control branches materially affect CEMA timing, SATCOM continuity, or escalation-safe effects integration.
- Add `packet_id=DPL-SIGINT-EMITTER-GEOLOCATION-001`, `packet_id=DPL-EABO-SIGNATURE-MANAGEMENT-001`, and `packet_id=DPL-ORBITAL-WARFARE-DECONFLICTION-001` for branches that materially alter emitter-control posture, expeditionary emissions discipline, or cross-domain timing trust.

## Domain Toolchain Override (2026-03-15, Expansion Wave LXI Addendum)

- Add `tool_suite_id=ts-joint-offline-key-material-courier-compromise-v1` + `protocol_stack_id=ps-joint-offline-key-material-courier-compromise-stack-v1` when cyber-electromagnetic branches depend on disconnected cryptographic key delivery, custody integrity, or compromise containment.
- Add `tool_suite_id=ts-theater-electromagnetic-deception-confidence-countertargeting-v1` + `protocol_stack_id=ps-theater-electromagnetic-deception-confidence-countertargeting-stack-v1` when CEMA synchronization depends on trusted decoy effects, blue-force signature confidence, or adversary countertargeting drift.
- Add `packet_id=DPL-OFFLINE-KEY-MATERIAL-COURIER-001` and `packet_id=DPL-EM-DECEPTION-CONFIDENCE-001` for branches that materially alter release authority, blue-force survivability, or command-path trust.

## Domain Toolchain Override (2026-03-15, Expansion Wave LXII Addendum)

- Add `tool_suite_id=ts-strategic-cable-landing-station-sanctions-bypass-hunt-v1` + `protocol_stack_id=ps-strategic-cable-landing-station-sanctions-bypass-hunt-stack-v1` when CEMA planning depends on landing-station OT defense, sanctions-evasion detection, or strategic telecom continuity.
- Add `tool_suite_id=ts-space-based-missile-warning-ground-truth-correlation-v1` + `protocol_stack_id=ps-space-based-missile-warning-ground-truth-correlation-stack-v1` when cyber-electromagnetic actions must be synchronized with warning confidence, false-track adjudication, or alert-release timing.
- Add `tool_suite_id=ts-joint-loitering-munition-fratricide-envelope-assurance-v1` + `protocol_stack_id=ps-joint-loitering-munition-fratricide-envelope-assurance-stack-v1` when CEMA release timing affects loitering-munition deconfliction, blue-force position confidence, or jamming-driven fratricide risk.
- Add `tool_suite_id=ts-theater-disconnected-additive-repair-intent-validation-v1` + `protocol_stack_id=ps-theater-disconnected-additive-repair-intent-validation-stack-v1` when contested repair networks require digital-pedigree assurance before fielded cyber or EW equipment returns to service.
- Add `packet_id=DPL-CABLE-LANDING-SANCTIONS-001`, `packet_id=DPL-MISSILE-WARNING-GT-CORR-001`, `packet_id=DPL-LM-FRATRICIDE-ENVELOPE-001`, and `packet_id=DPL-ADDITIVE-INTENT-VALIDATION-001` for branches that materially change mission timing, telecom resilience, force protection, or trusted reconstitution posture.

## Domain Toolchain Override (2026-03-15, Expansion Wave LXIII Addendum)

- Add `tool_suite_id=ts-theater-offline-mission-planning-malware-quarantine-v1` + `protocol_stack_id=ps-theater-offline-mission-planning-malware-quarantine-stack-v1` when CEMA synchronization depends on trusted offline planning nodes, removable-media custody, or clean rebuild timing after malware suspicion.
- Add `tool_suite_id=ts-theater-electronic-attack-iff-track-confidence-recovery-v1` + `protocol_stack_id=ps-theater-electronic-attack-iff-track-confidence-recovery-stack-v1` when cyber-electromagnetic branches depend on jamming-aware track trust, IFF restoration, or release-veto timing.
- Add `packet_id=DPL-OFFLINE-MISSION-PLANNING-MALWARE-001` and `packet_id=DPL-EA-IFF-TRACK-CONFIDENCE-001` for branches that materially change command-path trust, air-defense deconfliction, or cross-domain timing integrity.

## Domain Toolchain Override (2026-03-15, Expansion Wave LXVI Addendum)

- Add `tool_suite_id=ts-theater-denied-firmware-attestation-loader-sanitization-v1` + `protocol_stack_id=ps-theater-denied-firmware-attestation-loader-sanitization-stack-v1` when cyber-electromagnetic synchronization depends on trusted firmware pedigree, sanitized field loaders, or safe return-to-service of EW or network nodes.
- Add `tool_suite_id=ts-coalition-ai-foreign-disclosure-guardrail-v1` + `protocol_stack_id=ps-coalition-ai-foreign-disclosure-guardrail-stack-v1` when CEMA branches depend on coalition AI access boundaries, model provenance, or guardrail enforcement across shared decision aids.
- Add `tool_suite_id=ts-tactical-weather-denial-baro-altimetry-cross-check-v1` + `protocol_stack_id=ps-tactical-weather-denial-baro-altimetry-cross-check-stack-v1` when jamming or spoofing degrades weather confidence and sortie or fires release depends on alternate barometric cross-checks.
- Add `packet_id=DPL-DENIED-FIRMWARE-ATTESTATION-001`, `packet_id=DPL-COALITION-AI-GUARDRAILS-001`, and `packet_id=DPL-WEATHER-DENIAL-BARO-CROSSCHECK-001` for branches that materially change cyber trust, partner-access posture, or release timing under sensor denial.

## Domain Toolchain Override (2026-04-06, Expansion Wave LXVII Addendum)

- Add `tool_suite_id=ts-joint-seabed-sensor-grid-cable-sabotage-hunt-v1` + `protocol_stack_id=ps-joint-seabed-sensor-grid-cable-sabotage-hunt-stack-v1` when CEMA synchronization depends on seabed sensor continuity, undersea cable trust, or repair-security timing.
- Add `tool_suite_id=ts-sof-clandestine-resupply-signature-budget-v1` + `protocol_stack_id=ps-sof-clandestine-resupply-signature-budget-stack-v1` when cyber-electromagnetic branches depend on low-signature SOF sustainment, cache exposure, or adversary sensor avoidance.
- Add `tool_suite_id=ts-joint-arctic-under-ice-polynya-routing-v1` + `protocol_stack_id=ps-joint-arctic-under-ice-polynya-routing-stack-v1` when low-probability communications, navigation confidence, or Arctic recovery timing materially affect CEMA release decisions.
- Add `packet_id=DPL-SEABED-SABOTAGE-HUNT-001`, `packet_id=DPL-SOF-RESUPPLY-SIGNATURE-001`, and `packet_id=DPL-UNDER-ICE-POLYNYA-ROUTING-001` for branches that materially change undersea sensing trust, clandestine exposure posture, or Arctic command-path timing.
