---
name: sector-energy
version: "1.0.0"
description: Electric power + oil & gas + water/wastewater + renewable-integration cybersecurity for mid-2026 — NERC CIP v6/v7, NIST 800-82r3, TSA Pipeline SD-2021-02C, AWWA cyber, EU NIS2 energy + NCCS-G (cross-border electricity), AU AESCSF + SOCI, ENISA energy sector
triggers:
  - energy security
  - electric grid security
  - oil gas cyber
  - pipeline cyber
  - water utility cyber
  - nerc cip
  - tsa sd-2021
  - awwa cyber
  - aescsf
  - nccs-g
  - grid resilience
  - renewable cyber
  - inverter security
  - der security
  - smart meter security
data_deps:
  - cve-catalog.json
  - d3fend-catalog.json
atlas_refs: []
attack_refs:
  - T1692.001
  - T0883
  - T1190
  - T1078
framework_gaps:
  - NERC-CIP-007-6-R4
  - NIST-800-82r3
  - IEC-62443-3-3
  - NIS2-Art21-patch-management
  - ISO-27001-2022-A.8.8
  - UK-CAF-D1
  - AU-Essential-8-Backup
rfc_refs: []
cwe_refs:
  - CWE-287
  - CWE-798
  - CWE-306
  - CWE-1037
d3fend_refs:
  - D3-NI
  - D3-NTPM
  - D3-NTA
  - D3-EAL
  - D3-PSEP
forward_watch:
  - NERC CIP v7 final FERC order (anticipated 2026–2027) — additions for low-impact BES Cyber Systems, supply chain, and INSM (internal network security monitoring)
  - CISA + EPA joint guidance evolution for water/wastewater following the 2023 Unitronics campaign and the 2024 EPA enforcement memorandum
  - TSA Pipeline Security Directive renewal cadence — SD Pipeline-2021-02F effective 3 May 2025, expires 2 May 2026; next reissue (anticipated 02G) overdue as of mid-May 2026, expected H2 2026; track for renewed performance-based requirements and any inclusion of agentic-AI / supply-chain extensions
  - EU NCCS-G (Network Code on Cybersecurity for Cross-Border Electricity Flows, Reg. (EU) 2024/1366) phased compliance milestones through 2027 for ENTSO-E, EU DSO Entity, and impact-tier classified operators
  - AESCSF 2025 refresh by AEMO with renewable/DER specific maturity indicators
  - UL 2941 (DER cybersecurity) and IEEE 1547.3-2023 (DER cyber) adoption into US state PUC interconnection rules
  - MadIoT-class research on consumer-IoT-driven grid frequency manipulation moving from proof-of-concept to attributed campaigns
  - ICS-CERT advisory feed (https://www.cisa.gov/news-events/cybersecurity-advisories/ics-advisories) for vendor CVEs in Siemens, Rockwell, Schneider Electric, ABB, GE Vernova, Hitachi Energy, AVEVA / OSIsoft PI
last_threat_review: "2026-09-18"
discovery_mode: "standalone"  # operator-reached via `exceptd brief sector-energy` or `exceptd ask`; not chained into any playbook's direct.skill_chain by design
---

# Sector — Energy (Electric Power, Oil & Gas, Water/Wastewater, Renewables) — mid-2026

This skill extends `ot-ics-security` with energy-sector-specific regulatory, market, and grid-stability layers. The OT mechanics (Purdue model, IEC 62443 zones/conduits, ICS-IDS, vendor remote access, AI-augmented HMI risk) are inherited from `ot-ics-security`. Energy-specific overlays added here: balancing-authority awareness, telecontrol protocol authentication (IEC 62351), substation automation (IEC 61850), AMI/smart meter exposure, distributed-energy-resource (DER) cyber per UL 2941 / IEEE 1547.3-2023, pipeline-specific SD-2021-02C compliance, water-sector AWWA guidance, and cross-border electricity-flow controls under EU NCCS-G.

## Threat Context (mid-2026)

State-sponsored targeting of energy infrastructure has escalated, not plateaued.

- **Sandworm (GRU Unit 74455)** continued operations against Ukrainian grid infrastructure through 2025. Tooling lineage: BlackEnergy (2015) → CrashOverride/Industroyer (2016) → Industroyer2 (2022) → 2023–2025 bespoke OT-aware wipers and IEC-104 / IEC-61850 abusing payloads. Documented capability to send unauthorized control messages over IEC 60870-5-104, IEC 61850 MMS, and OPC DA — direct mapping to ATT&CK for ICS T1692.001.
- **Volt Typhoon (PRC-attributed)** pre-positioning in US energy, water, and transport ICS networks was confirmed by joint CISA / NSA / FBI advisories 2023–2024 and re-affirmed in 2025 sustainment advisories. The TTPs are living-off-the-land on the IT side (LOLBins, valid-account abuse, native admin tooling) bridged to OT engineering workstations — no off-the-shelf malware signature exists, defeating the entire IT-side EDR signature paradigm. ATT&CK Enterprise T1078 (Valid Accounts) is the dominant pivot.
- **CyberAv3ngers (IRGC-linked)** targeted Unitronics Vision-series PLCs at US, EU, and IL water utilities in late 2023, defacing HMIs and in some cases stopping treatment processes. The shared pattern: internet-exposed Unitronics device (T0883 — Internet Accessible Device), default credential (CWE-798), Modbus or vendor-protocol command (T1692.001). Re-tooled campaigns continued in 2024–2025 against other vendor lines. The 2023 EPA enforcement memorandum on Section 1433 of the Safe Drinking Water Act (Sanitary Survey cyber inclusion) was a direct response.
- **CIP-violating ransomware crossover**: Colonial Pipeline (2021) remains the canonical pivot case — IT-side ransomware drove an OT-side precautionary shutdown despite no OT-side compromise. Multiple 2024–2025 ransomware crews (BlackCat/ALPHV successors, RansomHub, Akira) have hit oil & gas, refining, and midstream operators; the operational pattern is consistent — IT compromise drives OT shutdown due to inability to bill, dispatch, or maintain situational awareness.

**Renewable energy and DER expansion brings new attack surface that classical NERC CIP scoping does not reach.**

- **Distributed energy resources** (rooftop solar, behind-the-meter storage, EV chargers, microgrid controllers) communicate over IEEE 2030.5 (CSIP), IEC 61850-7-420, SunSpec Modbus, and OpenADR. Most aggregator-DER and DER-DSO links use TLS with vendor-managed CAs; per-device authentication varies widely. UL 2941 (released 2023) and IEEE 1547.3-2023 are the emerging DER cyber standards; adoption into state PUC interconnection rules is uneven across the US, with CA Rule 21, HI Rule 14H, and NY Standardized Interconnection Requirements ahead of most others.
- **EV charging infrastructure** (EVSE) using OCPP 1.6J / 2.0.1 has been demonstrated vulnerable to backend impersonation, plug-and-charge ISO 15118 certificate abuses, and side-channel attacks on the V2G interface. Public-charger networks (ChargePoint, EVgo, Electrify America, Tesla Superchargers, BP Pulse, Ionity, Fastned, EVie) span jurisdictions and threat models.
- **Virtual power plants / DER aggregation platforms** consolidate command authority over thousands to millions of small DER. The control plane (cloud SaaS) is an IT-style attack surface with OT-grade consequence; pure-NERC-CIP scoping treats this as out of scope because no individual DER meets the BES Cyber System threshold.
- **MadIoT-class attacks** (manipulation of demand via IoT) have moved from PoC research (Soltan et al., 2018; subsequent academic follow-ups through 2024) to credible threat-model entries in TSO/DSO risk registers. A coordinated attack on 1–10 million high-wattage consumer IoT devices (water heaters, HVAC, EV chargers) can perturb grid frequency outside acceptable bands.

**AI-augmented operations in energy.**

- **AI-assisted dispatch and forecasting** (load forecasting, renewables forecasting, congestion management, unit commitment optimization) is widely deployed at ISOs / RTOs / TSOs. ML pipelines ingest weather feeds, market signals, telemetry — every input is a poisoning surface (ATLAS AML.T0020 / AML.T0043).
- **AI-augmented HMI / control-room copilots** are arriving in substation automation suites (Siemens Industrial Copilot, GE Vernova, Hitachi Energy, AVEVA). The risk inversion vs. classical NERC CIP is the same as in `ot-ics-security`: LLM-generated content is non-deterministic content over a conduit that the standards do not name.
- **AI-assisted reverse engineering of vendor firmware** dropped exploit-development time for vendor-specific OT vulnerabilities in 2025 (per multiple vendor security advisory acknowledgements). The implication: vendor advisory-to-PoC latency is shrinking from months to weeks.

**Inverted ephemerality (the usual architectural-impossibility exemption, reversed — see `ot-ics-security`).** Energy infrastructure is among the longest-lived OT in existence. Substation relays from the 1980s remain in service. Transmission RTUs commissioned in the 1990s carry IEC 60870-5-101 / -104 traffic today. Pipeline SCADA running on Windows XP / Server 2003 hosts remains operationally common. Recommendations assuming patch-fast or rebuild-on-change are operationally indefensible without an explicit compensating-control programme.

---

## Framework Lag Declaration

| Framework | Control | Designed For | Fails Because |
|---|---|---|---|
| NERC CIP v6 (currently in force) | CIP-002 through CIP-014 covering BES Cyber System identification, segmentation, personnel, physical, electronic perimeter, system management, recovery, vulnerability assessment, supply chain, INSM (CIP-015 added for medium/high impact), physical security | North American Bulk Electric System operators (BAs, TOs, GOs, GOPs, RCs) | (a) Low-impact BES Cyber Systems have minimal applicability — DER aggregators below the impact thresholds are unscoped. (b) CIP-007-6 R4 logging assumes enumerable event sources; AI-assistant interactions and DER aggregation control planes are not enumerated. (c) CIP-007-6 R2 patch SLA (35-day evaluation) is workable for evaluation but does not address the install backlog for substation relay firmware. (d) CIP-013-2 supply chain is procurement-focused; does not address run-time vendor remote-access enforcement (Unitronics-pattern risk on non-CIP-scoped utility assets). |
| NERC CIP v7 (proposed; FERC review) | Adds INSM (CIP-015) for high and medium impact BES, expands low-impact requirements, hardens supply chain, refines virtualization and cloud applicability | Same scope as v6, with expanded coverage | Even v7 does not scope DER aggregation control planes, EV charging networks, or AI-assisted dispatch ML pipelines. Final FERC order timing slips repeatedly; planning to "wait for v7" is itself a gap. |
| NIST 800-82r3 (October 2023) | OT security guidance, IT/OT convergence, segmentation, vendor remote access | OT broadly across all critical-infrastructure sectors | Predates AI-augmented HMI threat class; treats AI as future consideration. No specific operationalization for DER cyber or AMI. See `ot-ics-security` for the foundational gap analysis. |
| TSA SD Pipeline-2021-02C (reissued 2025-07; current as of mid-2026) | Cybersecurity for TSA-designated critical hazardous-liquid and natural-gas pipeline owners/operators | US pipeline operators on TSA's critical list | (a) Performance-based requirements still allow significant operator interpretation on segmentation; (b) does not address LNG export facility cyber specifically; (c) does not name AI-assistant integration or DER-adjacent pipeline-attached assets (e.g., compressor station microgrid controllers); (d) annual cybersecurity assessment is calendar-driven, not threat-driven. |
| AWWA Cybersecurity Guidance and Tool (current 2023 revision) | Risk and responsibility model for water/wastewater utilities | US water/wastewater sector | Guidance is non-binding; adoption uneven. Section 1433 of SDWA requires risk assessment to include cyber but EPA enforcement authority on cyber-specific findings was challenged in court and remains operationally weak. The 2024 EPA enforcement memorandum operationalized Sanitary Survey cyber inclusion but does not specify minimum controls. Unitronics pattern is the canonical gap case. |
| IEC 62443-3-3 (System Security Requirements) | SR 1–7 with Security Levels SL 1–4 | Industrial automation control system security, method-neutral | Inherited from `ot-ics-security`: method-neutral on AI integration; conduit definitions assume deterministic protocol-level flows. Energy-specific extension: IEC 61850-90-4 / -90-12 (substation cybersecurity informative annexes) and IEC 62351 (telecontrol protocol authentication) are the energy-specific cousins; both are aspirational rather than deployed at most utilities. |
| IEC 62351 (Telecontrol security) | Authentication, integrity, confidentiality for IEC 60870-5-104, IEC 61850, DNP3 | Energy-sector telecontrol protocols | Designed for; deployment is the gap. Most installed IEC 60870-5-104 and IEC 61850 MMS traffic at brownfield utilities is unauthenticated — IEC 62351-3/-5/-6 retrofit is operationally hard. Sandworm/Industroyer2 exploited exactly this gap. |
| EU NIS2 Directive Art. 21 + Annex I (energy sector — electricity, district heating/cooling, oil, gas, hydrogen) | Risk management measures for essential/important entities | EU energy operators | Silent on OT-specific controls; "appropriate measures" leaves Member State authorities to fill the energy-OT gap unevenly. Patch-management language identical for IT and OT — operationally indefensible for substation relay fleets. See generic NIS2 gap in `ot-ics-security`. |
| EU NCCS-G — Network Code on Cybersecurity for Cross-Border Electricity Flows (Reg. (EU) 2024/1366, entry into force 2024-07) | Binding cybersecurity requirements for entities affecting cross-border electricity flows: TSOs, DSOs, NEMOs, RCCs, ENTSO-E, EU DSO Entity | EU electricity sector cross-border operators | First binding sector-specific cyber regulation for EU electricity; phased compliance through 2027. Gaps: (a) impact tier assignment (high vs critical) under negotiation, (b) ECCM (ENTSO-E Cybersecurity Cost-Benefit-Method) for minimum cybersecurity controls still being elaborated, (c) does not yet specifically address AI-assisted dispatch, (d) interaction with NIS2 transposition uneven across Member States. |
| EU CER Directive 2022/2557 (Critical Entities Resilience) | Physical and operational resilience for critical entities in 11 sectors including energy | EU critical entities | Resilience-focused; cyber overlaps NIS2. Sector-specific operationalization is at Member State authority discretion. |
| UK NIS Regulations 2018 + NCSC CAF (Cyber Assessment Framework v3.2) for ESN (Essential Services Network — energy) | OES designation includes electricity, oil, gas; CAF outcomes are sector-tailored via NCSC guidance | UK energy operators | CAF outcomes are sound but lack specific operational definitions for DER, AMI, AI-HMI; reliance on CA/CAA professional judgement at audit time. Energy Emergencies Executive Committee (E3C) coordinates cyber-induced emergency response — playbook integration with operator IR is uneven. |
| AU SOCI Act 2018 (as amended 2022) + AESCSF 2024 (Australian Energy Sector Cyber Security Framework, AEMO-published) | Security of Critical Infrastructure across 11 sectors; energy-sector cybersecurity maturity model | AU energy operators (electricity, gas, liquid fuels) | AESCSF is OT-aware and energy-specific; its AI dimension is treated as monitoring scope, not as a new conduit type. SOCI risk-management programmes (RMP) do not specifically require DER-aggregation cyber or AI-HMI threat modelling. 2025 AESCSF refresh anticipated to add renewable/DER maturity indicators (in forward_watch). |
| JP NISC Critical Infrastructure Policy (14 sectors, including electricity, gas, water) + METI energy cybersecurity guidelines | National critical-infrastructure cybersecurity policy with sector specifics from METI for energy | JP energy operators | Policy-level; operational specifics defer to METI sector guidelines. AI-augmented dispatch and DER cyber not specifically addressed in current METI guidance. |
| IL INCD Critical Infrastructure Directives (energy directives) | National CI cyber directives, energy-sector specific | IL energy operators | OT-aware but does not yet codify AI-assistant integration or DER-aggregation as a regulated surface. The post-2023 CyberAv3ngers incidents drove INCD energy-sector advisory updates; codification trails. |
| US CISA ICS Joint Working Group (ICSJWG) output | Coordinated US ICS guidance across sectors | Voluntary guidance for US CI | Non-binding; high-quality but adoption uneven. The ICS-CERT advisory cadence is the most actionable output. |
| ISO 27001:2022 + ISO/IEC 27019:2017 (energy utilities sector extension) | Generic ISMS + energy-sector extension | Organisation-level ISMS for energy | ISO/IEC 27019 predates AI-augmented HMI (2017 publication). A.8.8 vulnerability management is IT-flavoured; 27019 adds energy specifics but no AI conduit treatment. |

**Cross-jurisdiction posture (global-first, not US-centric):** Any energy-sector gap analysis for a multi-jurisdiction operator must cite at minimum US NERC CIP v6/v7 + TSA SD (if pipeline) + AWWA (if water) + NIST 800-82r3, EU NIS2 + NCCS-G + CER Directive, UK NIS+CAF for ESN, AU SOCI+AESCSF, JP NISC + METI, IL INCD, alongside ISO 27001:2022 + ISO/IEC 27019. US-only analysis is insufficient for any operator with European, Australian, or Asian footprint.

---

## TTP Mapping

Energy-sector TTPs span ATT&CK for ICS, ATT&CK Enterprise (for the IT side of the pivot), and ATLAS for the AI overlay.

| Surface | TTP | Matrix | Energy-specific Variant in mid-2026 | Gap Flag |
|---|---|---|---|---|
| Internet-exposed energy control asset | T0883 — Internet Accessible Device | ATT&CK for ICS | Substation gateways with IEC 60870-5-104 over public IPv4 (legacy MPLS replacement projects exposing previously private addressing); Unitronics PLCs at water utilities; SunSpec / Modbus-exposed solar combiners; OCPP-exposed EV chargers | IEC 62443-3-3 SR 5.1 presumes perimeter; vendor-mediated remote access and DER aggregator backplanes lack one. NERC CIP electronic security perimeter (ESP) does not scope DER aggregator cloud control planes. |
| Unauthorized control command (grid command injection) | T1692.001 — Unauthorized Command Message | ATT&CK for ICS | IEC 60870-5-104 select/operate without IEC 62351-5 authentication; IEC 61850 MMS file transfer / control / report; DNP3 select/operate without DNP3-SA; Modbus/TCP write to coil; SunSpec inverter setpoint write | CWE-306 / CWE-287 baked into protocol deployments. IEC 62443-3-3 SR 1.1/1.2 cannot be enforced at L1 where protocols and devices do not natively support authentication. Industroyer2 / CrashOverride were exactly this. |
| Compromised vendor remote access | T1078 — Valid Accounts | ATT&CK Enterprise | Vendor jump-host credentials phished or replayed (Volt Typhoon pattern); shared vendor "engineer" account on engineering workstation; vendor-managed cloud control plane (EcoStruxure, FactoryTalk Hub, Insights Hub, Hitachi Energy Lumada) credential abuse | NERC CIP-005 / CIP-007 R5 cover personnel and password management but assume utility-managed identity; vendor-cloud-mediated identity is a delegated surface. NIS2 Art. 21(2)(d) supply chain measures are procurement-focused. |
| IT-side initial access pivoting to OT | T1190 — Exploit Public-Facing Application | ATT&CK Enterprise | Energy MES, market-bidding web application, customer-portal pivoting to AMI head-end, vendor remote-portal web app, EV charging back-end exposed REST/GraphQL | NIST 800-53 SC-7 perimeter assumption does not address IT→OT pivot chain. Colonial Pipeline (2021) was the canonical case. |
| Substation lateral movement | T0867 — Lateral Tool Transfer | ATT&CK for ICS | Engineering workstation → station HMI → bay-level IED via IEC 61850 file transfer or vendor engineering tool (Hitachi Energy PCM600, Siemens DIGSI, GE Enervista, SEL AcSELerator) | NIST 800-82r3 segmentation guidance does not specify L2/L1 micro-segmentation at substations; flat process bus is common. |
| AMI / smart-meter compromise | T0883 + T1692.001 | ATT&CK for ICS | AMI head-end compromise enables disconnect command at scale; meter firmware vulnerability classes (ANSI C12.18 / C12.22, DLMS/COSEM); 802.15.4 mesh attacks (Itron, Landis+Gyr, Sensus deployments) | NERC CIP does not scope AMI (distribution-side asset); state PUCs vary in cyber-specific requirements; ENISA smart-grid recommendations are non-binding. |
| DER aggregation control plane abuse | T1078 + T1190 | ATT&CK Enterprise | Compromise of VPP / DER aggregator cloud control plane enables coordinated DER curtailment, ramp manipulation, or trip; IEEE 2030.5 (CSIP) and OpenADR identity model varies | UL 2941 / IEEE 1547.3-2023 are emerging standards; deployment lag is wide. Not in any binding regulation as of mid-2026. |
| MadIoT-class demand manipulation | T1078 + T1692.001 | ATT&CK Enterprise + ICS | Compromise of consumer IoT (HVAC thermostats, water heaters, EV chargers, smart appliances) at scale enables coordinated demand perturbation outside grid frequency tolerance | No framework treats consumer IoT as an energy-sector threat surface. ENISA, NIST, and AESCSF treat as research-stage. |
| Engineering-workstation host LPE on substation engineering host | T1068 — Exploitation for Privilege Escalation | ATT&CK Enterprise | Windows 7 / 10 engineering workstation hosts running vendor tooling (PCM600, DIGSI, AcSELerator); often un-patchable due to vendor tool compatibility constraints; Copy Fail (CVE-2026-31431) on any Linux engineering host | IT 30-day patch SLA inapplicable to vendor-tool engineering hosts; cross-reference `kernel-lpe-triage`. |
| Hard-coded / shared / default credentials in energy assets | CWE-798 | CWE | Vendor default credentials on PLC, RTU, smart inverter, smart meter, EVSE, OCPP back-end; shared substation operator accounts | NERC CIP-007 R5 partially addresses but exempts asset classes lacking user-account features; AWWA guidance non-binding for water |
| Firmware-image integrity at L1 | CWE-1037 + CWE-345 family (insufficient verification of data authenticity) | CWE | Unsigned firmware accepted by relay, RTU, smart inverter; vendor build-pipeline compromise propagating to substation fleet | NERC CIP-010 baseline-change management does not require firmware-image signature verification at install time; signed-firmware support varies by vendor and product line |
| Authentication weakness in energy protocols | CWE-287 + CWE-306 | CWE | IEC 60870-5-104 and IEC 61850 MMS deployed without IEC 62351 authentication retrofit; DNP3 deployed without DNP3-SA; Modbus/TCP without any authentication layer | IEC 62443-3-3 SR 1.1/1.2 unenforceable at protocol layer for installed brownfield; retrofit cost and operational risk routinely defer indefinitely |
| AI-pipeline poisoning in dispatch / forecasting | (closest ATLAS mapping addressed in `ai-attack-surface`) | ATLAS v2026.09 | ML-poisoning of load forecast inputs, renewables forecast inputs, congestion model training data, or unit-commitment optimization features | No ATT&CK for ICS technique for AI-mediated market or dispatch manipulation; NERC CIP-007 R4 silent on AI event sources; NIST 800-82r3 silent. Cross-reference `ai-attack-surface`, `rag-pipeline-security`. |

**Note on ATT&CK for ICS ID format.** ATT&CK for ICS uses `T0xxx` IDs (T1692.001, T0883, T0867). The linter regex `^T\d{4}(\.\d{3})?$` accepts this shape. ATT&CK Enterprise IDs (T1190, T1078, T1068) are cited alongside for IT/OT pivot.

**Note on ATLAS coverage.** `atlas_refs: []` in this skill's frontmatter is deliberate — ATLAS AI overlay is owned by `ai-attack-surface`. This skill cross-references rather than duplicates ATLAS mappings.

---

## Exploit Availability Matrix

| Surface / CVE Class | CVSS | RWEP | CISA KEV | PoC Public | AI-Discovered | Active Exploitation | Patch Available | Live-Patchable | OT-Aware Detection |
|---|---|---|---|---|---|---|---|---|---|
| Engineering / HMI Linux host hit by Copy Fail (CVE-2026-31431) | 7.8 | 90 | Yes (2026-05-01, due 2026-05-15) | Yes — 732-byte script | Yes | Confirmed | Yes | Yes (kpatch/livepatch/kGraft) on supported distros; rare in energy brownfield | Partial — auditd / eBPF if deployable |
| Engineering / HMI Windows host LPE (Print Spooler / win32k family) | varies | varies | Several entries KEV-listed | Yes | Mixed | Confirmed | Yes for in-support; out-of-support engineering hosts exposed permanently | Hotpatch on supported builds only | EDR if OT-deployable; many OT EDR carve-outs |
| Unitronics Vision-series PLC (CyberAv3ngers pattern) | varies — vendor advisories | high RWEP where internet-exposed | Yes (some) — see CISA ICSA-23-353-01 and successors | Yes — public PoCs since late 2023 | Mixed | Confirmed against US/EU/IL water utilities | Yes | No | ICS-aware IDS signatures available (Claroty CTD, Nozomi Guardian, Dragos, Tenable OT) |
| Vendor-side energy-OT CVEs (Siemens SIPROTEC / SCALANCE, Rockwell ControlLogix / FactoryTalk, Schneider Electric Modicon / EcoStruxure, ABB RTU / SDM, GE Vernova Multilin / Mark VIe, Hitachi Energy MicroSCADA / RTU500, AVEVA / OSIsoft PI System) | varies | varies | Multiple KEV listings 2024–2026 | Mixed — vendor disclosure cadence | Increasing AI-assisted RE (2025 trend) | Targeted by Sandworm-aligned and Volt Typhoon-aligned actors | Vendor-dependent; typical install lag 1–5 years | No — firmware updates require change windows | ICS-aware IDS signature lag varies |
| IEC 60870-5-104 / IEC 61850 protocol abuse (Industroyer / Industroyer2 class) | n/a — design-level | risk-modelled | n/a | Demonstrated in attributed campaigns | n/a | Confirmed (Ukraine grid, 2016 and 2022) | Mitigation only (IEC 62351 retrofit; conduit segmentation) | n/a | ICS-aware IDS with energy protocol decoders detects unusual control-block patterns; signatures for Industroyer2 are widely deployed |
| DER inverter firmware / smart-inverter setpoint manipulation | emerging research; limited public CVEs | risk-modelled | n/a | Demonstrated in academic research | Mixed | Suspected in 2025 advanced campaigns; attribution incomplete | Vendor-dependent | No | Aggregator-side telemetry analytics; D3-NTA at DER aggregator boundary |
| AMI / smart-meter mesh attacks | varies | varies | Limited KEV coverage | Some academic PoCs | n/a | Suspected; rarely attributed | Vendor-dependent firmware updates over the mesh | No | Vendor head-end analytics; weak external detection |
| OCPP / V2G / ISO 15118 attack surface (EV charging) | varies | varies | Limited KEV coverage | Yes — research community publishes | Mixed | Demonstrated in research; opportunistic abuse confirmed | Vendor / charge-point-operator dependent | No | Charge-point-operator side analytics; weak external detection |
| AI-dispatch / AI-forecast poisoning (no CVE class) | n/a | risk-modelled | n/a | Demonstrated in research and 2025 incident-response engagements | n/a | Suspected | Mitigation only — design-time controls on ML pipeline | n/a | Requires ML-pipeline telemetry; almost never present at utilities |

**Honest gap statement (declare what the catalog does not yet cover).** This project's `data/cve-catalog.json` does not yet contain an exhaustive inventory of vendor-side energy-OT CVEs (Siemens SSAs, Rockwell SD advisories, Schneider Electric Security Notifications, ABB CSAs, GE Vernova advisories, Hitachi Energy advisories, AVEVA advisories). The authoritative source for current energy-OT CVEs is the CISA ICS-CERT advisory feed at https://www.cisa.gov/news-events/cybersecurity-advisories/ics-advisories — captured in `forward_watch` for inclusion in the catalog as part of the next data refresh. Do not invent CVE IDs to fill this matrix.

---

## Analysis Procedure

This procedure inherits the OT foundation (Purdue model, IEC 62443 zone/conduit, vendor remote access, AI-HMI audit) from `ot-ics-security` and adds energy-sector overlays. Defense in depth, least privilege, and zero trust are threaded explicitly.

**Defense in depth.** Purdue layers L0–L5 (inherited from `ot-ics-security`) plus energy-specific overlays: substation process bus (IEC 61850 station and process bus separation), control-center to substation conduits (IEC 60870-5-104 or IEC 61850 R-GOOSE / R-SV), market-systems isolation (ISO/RTO bidding interfaces, settlements), AMI head-end segmentation, DER aggregator control-plane isolation. Physical-security defense in depth at substations (Metcalf 2013 lesson — physical sabotage of substations preceded the cyber threat era and remains a parallel risk). Unidirectional gateways (Waterfall, Owl, Hirschmann Tofino, Siemens SCALANCE) at the IT/OT and SIS/BPCS boundaries where the data-flow is naturally OT→IT only.

**Least privilege.** Substation engineering tooling separated from operator HMI; vendor remote access scoped per-asset, per-action, per-time-window with session recording (post-Unitronics, post-Colonial; same pattern as `ot-ics-security`). Market-systems user access strictly separated from operations user access. DER aggregator control plane: every aggregator action that affects more than a documented impact threshold of DER capacity requires multi-party authorization. AI-assistant tooling (operator copilot, engineering copilot, dispatch optimization assistant) runs read-only by default; any write to setpoint, breaker, alarm-suppression, or market bid requires non-AI-mediated human confirmation.

**Zero trust.** Assume every smart meter, smart inverter, EVSE, and DER controller is hostile. Authenticate every command at the aggregator-to-DER boundary using IEEE 2030.5 / OpenADR identity model; authenticate every IEC 60870-5-104 and IEC 61850 control message using IEC 62351-5/-6 where retrofit is feasible. Never assume the OT network is trustworthy because it sits behind a firewall (inherited from `ot-ics-security`). Vendor remote-access sessions verified per-action via jump host; cloud-mediated vendor control planes treated as external network regardless of vendor's TLS termination.

### Step 1 — Identify sector(s) and asset class scope

Confirm which energy sub-sector(s) the operator is in: electric power (transmission, distribution, generation, market operations); oil & gas (upstream, midstream pipeline, downstream refining, LNG); water/wastewater; renewables/DER aggregation; EV charging network. Each sub-sector pulls in different regulatory layers — record the applicable set for Step 9 cross-jurisdiction reconciliation.

### Step 2 — Inventory OT assets per Purdue level, with energy overlay

Inherit the L0–L5 inventory from `ot-ics-security` Step 1. Add energy-specific overlays:

- **Substations**: bay-level IEDs (relays, merging units, switches), station HMI, station gateway, time synchronization (PTP / IRIG-B / GPS). Capture protocol mix (IEC 60870-5-101 / -104, IEC 61850 MMS / GOOSE / SV / R-GOOSE / R-SV, DNP3, Modbus). Capture IEC 62351 deployment status per conduit.
- **Control centers**: SCADA front-end, EMS / DMS / ADMS, historian, alarm management. Capture EMS vendor and version (Siemens Spectrum Power, GE / Vernova ADMS, Hitachi Energy MicroSCADA Pro, OATI webSmartGrid, etc.).
- **Market systems**: bidding interface, settlement, congestion management, capacity market. (For ISOs/RTOs and market participants.)
- **AMI**: meter population, meter vendor(s), head-end version, communication layer (RF mesh, PLC, cellular). Capture meter firmware signing posture.
- **DER**: behind-the-meter and front-of-meter inventory; aggregator(s) and communication standard (IEEE 2030.5 CSIP, IEC 61850-7-420, SunSpec, OpenADR); UL 2941 / IEEE 1547.3-2023 conformance claims.
- **EV charging**: charger inventory if operator-owned; OCPP version (1.6J vs 2.0.1); ISO 15118 plug-and-charge deployment status; back-end identity model.
- **Pipeline / midstream (oil & gas)**: SCADA front-end, RTU population, leak detection systems (CPM and external), valve operators, compressor / pump station SCADA, custody-transfer metering. Capture TSA SD-2021-02C applicability.
- **Water/wastewater**: treatment SCADA, SCADA-attached chemical dosing, lift-station and distribution SCADA, AMI water-meter overlap. Capture AWWA guidance adoption.

### Step 3 — Determine regulatory applicability

For each asset/system, determine applicability under each regulatory framework relevant to the operator's jurisdictional footprint. Build a single applicability matrix with rows = assets, columns = frameworks, cells = applicable control set.

- **NERC CIP**: per BES Cyber System impact tier (high/medium/low); per asset role (BCA, EACMS, PACS, PCA). For non-BES utility assets (DER aggregation, distribution-side, AMI), document explicit out-of-scope.
- **TSA SD-2021-02C**: per pipeline asset on TSA's critical list.
- **AWWA**: per water/wastewater utility size and service population.
- **EU NIS2 + NCCS-G**: per Member State transposition; impact-tier classification under NCCS-G (high vs critical) where applicable.
- **AU SOCI + AESCSF**: per AESCSF maturity indicator level (MIL-1 to MIL-3 across 11 domains).
- **UK NIS + CAF**: per Operator of Essential Services designation; CAF outcomes A1–D2.
- **JP NISC + METI**: per critical-infrastructure sector tier.
- **IL INCD energy directives**: per asset class designation.

### Step 4 — Inherit OT analysis from `ot-ics-security`

Run the full `ot-ics-security` Analysis Procedure (Steps 2–8) on the OT estate. This skill does not duplicate that procedure; it adds energy-sector overlays in subsequent steps. Specifically inherit:

- IEC 62443-3-3 SL scorecard per zone
- IT/OT bridge inventory
- AI-HMI integration audit
- Network segmentation map (D3-NI + D3-NTPM)
- Vendor remote-access ledger (post-Unitronics application of zero trust)
- Patch posture audit
- OT-aware incident response

### Step 5 — Telecontrol-protocol authentication audit (IEC 62351)

For each operational conduit carrying IEC 60870-5-104, IEC 61850 MMS, IEC 61850 R-GOOSE / R-SV, or DNP3:

- Is IEC 62351 deployed at all? (Most brownfield: no.)
- If yes: which parts — 62351-3 (TLS for TCP/IP), -4 (MMS auth), -5 (IEC 60870-5-7 auth), -6 (IEC 61850 GOOSE/SV auth)?
- If no: what compensating control protects the conduit from T1692.001 unauthorized command injection? (Network isolation alone is insufficient where vendor remote access or operator workstation compromise places an attacker on the conduit.)
- Are there any internet-bridged 104 / 61850 conduits without VPN/TLS termination at trusted endpoints? If yes — that is a Sandworm-class exposure documented in the finding.

### Step 6 — DER aggregation and AMI cyber audit

- DER aggregator cloud control plane: identity model, MFA enforcement, multi-party authorization on bulk DER actions (curtailment, ramp, trip), session recording, integration with operator SOC.
- IEEE 2030.5 / OpenADR / SunSpec / IEC 61850-7-420 deployment per aggregator: TLS configuration, mutual auth, certificate lifecycle, revocation.
- DER device firmware signing posture per vendor (Tesla, Enphase, SolarEdge, Sungrow, Huawei FusionSolar, Fronius, SMA, Generac, EcoFlow, etc.); UL 2941 / IEEE 1547.3-2023 conformance claims.
- AMI head-end: identity model for utility users, vendor users, third-party users (DER providers reading meter data); disconnect/reconnect command authorization; mass-action throttling.
- Connection between AMI head-end and DER aggregator (if any): conduit identification, authentication.

### Step 7 — EV charging / V2G cyber audit (if operator-owned)

- OCPP version, OCPP-Security profile usage (Profile 1 / 2 / 3), back-end TLS configuration, mutual auth.
- ISO 15118 plug-and-charge: PKI design, certificate provisioning, V2G-specific risks.
- Charge-point-operator (CPO) cloud control plane identity model; payment-system isolation; mass-action throttling.
- Aggregated load impact of charger fleet: is it large enough to factor into grid-frequency threat model?

### Step 8 — Pipeline-specific (if oil & gas midstream)

- TSA SD-2021-02C measure-by-measure compliance: cybersecurity coordinator designation, vulnerability assessment cadence, cybersecurity assessment plan, cybersecurity implementation plan, network segmentation, access control, continuous monitoring and detection, application of patches and updates, cybersecurity training.
- Leak detection system isolation (independent of SCADA where possible).
- Custody-transfer metering integrity (regulatory and contractual implications of cyber-mediated metering manipulation).

### Step 9 — Water-specific (if water/wastewater)

- Sanitary Survey cyber inclusion per 2024 EPA enforcement memorandum.
- AWWA Cybersecurity Risk and Responsibility tool: assessment recency, completeness, board reporting.
- Unitronics-pattern audit: any Vision-series PLC anywhere in the estate, internet-exposed (any plant, any pump station, any lift station). Cross-reference vendor advisory CISA ICSA-23-353-01 and successors.
- Chemical dosing system isolation (operator-induced overdose is the canonical worst-case for water; corresponding underdose is the silent worst-case).

### Step 10 — Market-systems isolation audit (if ISO/RTO or market participant)

- Market-bidding interface isolated from operations SCADA? Compromise of bidding does not trivially pivot to operations.
- Settlement and revenue isolation from operations.
- Congestion management and security-constrained-economic-dispatch (SCED) model integrity: ML inputs and outputs treated as integrity-critical?

### Step 11 — Cross-jurisdiction reconciliation

For each jurisdiction the operator is exposed to, produce a per-jurisdiction mapping of the same control findings to that jurisdiction's regulatory language. Disparate findings for the same deficiency across jurisdictions are themselves a finding (per `ot-ics-security` Step 10).

### Step 12 — Grid-stability / aggregate-impact threat-model overlay

For operators with material aggregate consumer-IoT or DER influence (TSOs, large DSOs, large DER aggregators, large EV charging networks, large smart-appliance OEMs with cloud control planes):

- Quantify aggregate controllable load and aggregate controllable generation under the operator's or aggregator's control.
- Quantify worst-case coordinated swing as a fraction of regional grid load.
- Threat-model MadIoT-class scenarios against the regional balancing authority's frequency tolerance bands.
- Document the cyber-physical compensating controls (rate-limiting on bulk DER actions, ramping limits, frequency-responsive disconnect logic at DER, regional protective relaying).

### Step 13 — Compliance Theater Check (see dedicated section below)

---

## Output Format

The skill produces an Energy-Sector Cybersecurity Posture Assessment covering NERC CIP v6 / v7 coverage, TSA Pipeline Security Directives, IEC 62443 zone-and-conduit posture, ENISA EECSP, ASD Essential 8 + AESCSF (AU), CER NIS2 transposition (EU), and the AI-augmented OT threat exposure. The shape below is consumed downstream by `ot-ics-security` (which inherits the Purdue-zone analysis), by `incident-response-playbook` (for the FERC / NERC EOP-004 incident-classification clock), and by `global-grc` (for cross-jurisdictional energy rollup). Preserve the per-substation / per-pipeline asset rows verbatim — they are the auditable evidence for regulator reporting.

Produce this structure verbatim:

```
## Energy-Sector Cybersecurity Posture Assessment

**Assessment Date:** YYYY-MM-DD
**Operator / Site:** [name]
**Sub-sector(s):** [electric T&D / generation / market ops / pipeline / water / DER aggregation / EV charging]
**Regulatory jurisdictions:** [US/NERC + TSA + AWWA + state PUCs; EU/NIS2 + NCCS-G + CER; UK/CAF; AU/SOCI+AESCSF; JP/NISC+METI; IL/INCD; other]

### Asset Class Inventory (Purdue + Energy Overlay)
| Class | Count | Vendor Mix | Protocol Mix | IEC 62351 Status | Avg Age (years) | Patch Posture |
|-------|-------|------------|--------------|-------------------|-----------------|----------------|
| Substation IEDs                | ... | ... | ... | ... | ... | ... |
| Station gateways / RTUs        | ... | ... | ... | ... | ... | ... |
| EMS/DMS/ADMS                   | ... | ... | ... | n/a | ... | ... |
| Pipeline SCADA/RTUs            | ... | ... | ... | n/a | ... | ... |
| Water treatment SCADA          | ... | ... | ... | n/a | ... | ... |
| AMI head-end + meters          | ... | ... | ... | n/a | ... | ... |
| DER + aggregator               | ... | ... | ... | n/a | ... | ... |
| EVSE + CPO back-end            | ... | ... | ... | n/a | ... | ... |

### Regulatory Applicability Matrix
| Asset Class | NERC CIP | TSA SD | AWWA | NIS2 | NCCS-G | UK CAF | AESCSF | METI | INCD | ISO 27019 |

### IEC 62351 Deployment Audit
| Conduit | Protocol | Endpoint A | Endpoint B | 62351 Part | Status | Compensating Control |

### DER / AMI / EV Cyber Audit
| Surface | Standard Cited | Identity Model | MFA | Multi-Party Auth (bulk actions) | Aggregator-Side Telemetry |

### IT/OT Bridge Inventory (energy-specific)
| Source | Destination | Conduit | Auth Model | Logging | Risk |

### AI-Assistant / AI-Dispatch Integration Audit
| Surface | Vendor / Model | Read or Write | Approval Gate | Prompt + Completion Logging | Kill Switch |

### Vendor Remote-Access Ledger
| Vendor | Scope | Account Model | MFA | Session Recording | Time Window | Last Access |

### NERC CIP / TSA / AWWA / NIS2 / NCCS-G / CAF / AESCSF / METI / INCD Mappings
[Per-jurisdiction control-status matrix]

### Compliance Theater Findings
[Outcome of the four tests in the Compliance Theater Check section]

### Defensive Countermeasure Plan (D3FEND)
[D3-NI, D3-NTPM, D3-NTA, D3-EAL, D3-PSEP — concrete control placements by Purdue layer and energy overlay]

### Grid-Stability Aggregate-Impact Posture (if applicable)
[Aggregate controllable load / generation; worst-case coordinated swing; MadIoT-class compensating controls]

### Priority Remediation Actions
1. ...
2. ...
3. ...

### RWEP-Prioritised Energy-OT CVE Exposure
[Energy-OT CVEs ranked by RWEP, not CVSS; see `exploit-scoring` skill for recalculation]
```

---

## Compliance Theater Check

Run all four tests. Any "fail" is a theater finding documented with the evidence (or absence thereof).

**Theater Test 1 — NERC CIP-007 patch evidence.**
Ask: "Show me your NERC CIP-007 R2 patch evaluation evidence for the last four 35-day cycles for each HIGH and MEDIUM impact BES Cyber System, including (a) the patch source identified, (b) the evaluation outcome per applicable cyber asset, (c) the installation timeline or filed mitigation plan with target date."

- If the answer is "we patch quarterly" without per-35-day evidence: documented violation, not theater. Compliance theater is when the paperwork exists but the underlying patches do not.
- If the answer is "we have an evaluation log" but no per-asset outcome and no mitigation plan for un-installed patches: theater — the regulator's expectation is per-asset traceability with mitigation accountability for any patch not installed.
- If the answer references "compensating controls" without naming the specific D3FEND techniques deployed (D3-NI conduit policy, D3-EAL allowlist, D3-NTA ICS-IDS detection coverage) and the change window for installation: theater.
- Acceptable answer: per-asset evaluation log for last four cycles + mitigation plans for un-installed patches with target dates + compensating-control programme documented by D3FEND technique.

**Theater Test 2 — Vendor remote access enforcement (post-Unitronics).**
Ask: "Walk me through how a vendor support engineer initiates a session to a Modicon / SIPROTEC / ControlLogix / Mark VIe / Multilin / MicroSCADA on day one of a quarter, and on the last day of the contract, end-to-end. Show me the access ledger entry, the session recording, and the post-session command log."

- If the answer is "we have a VPN": that is a credential, not enforcement; theater per the Unitronics pattern (which started with vendor-credential-on-VPN).
- If the answer references jump-host MFA but no per-action / per-asset / per-time-window scope and no session recording: theater.
- If contract-end deprovisioning is "we send an email to IT": theater. Acceptable: deprovisioning automation linked to the contract repository.
- Acceptable: per-vendor ledger entry, jump-host MFA with just-in-time credential issuance, per-asset / per-action scope encoded as a jump-host policy, session recording with searchable command log, contract-end automated deprovisioning within 24 hours.

**Theater Test 3 — DER cyber inventory.**
Ask: "Show me your DER cyber inventory: every behind-the-meter and front-of-meter DER under operator or aggregator control, by vendor, by firmware version, by communication standard, by UL 2941 / IEEE 1547.3-2023 conformance claim."

- If "no, DER is out of NERC CIP scope" is the answer: misses that aggregate DER influence is the threat surface, not individual DER NERC-impact. Theater — the regulatory scope is not the threat scope.
- If "yes — the aggregator has it" without operator-side aggregation, cross-aggregator total, and aggregate-impact threat modelling: theater for the operator's own visibility.
- If the inventory exists but stops at the aggregator boundary (no per-DER firmware / conformance data): partial; document as a gap that grows daily as DER penetration increases.
- Acceptable: aggregated per-DER inventory, per-vendor firmware signing posture, per-standard conformance, aggregate-impact threat-model entry in the risk register with a quantified worst-case swing and compensating controls.

**Theater Test 4 — OT-aware incident response (process-shutdown ≠ always safe).**
Ask: "Walk me through your IR playbook for a confirmed compromise of [pick one: substation engineering workstation / pipeline SCADA primary / water treatment SCADA / AMI head-end]. Tell me who has the authority to direct OT-side response, what the decision tree looks like for shutdown vs. keep-running, and how you handle the case where shutdown is the dangerous response."

- If the playbook is a copy-paste from the IT IR playbook: dangerous theater. IT IR defaults to isolate-and-rebuild; OT IR has cases where isolate causes more harm than the suspected compromise (continuous-cracker, certain power-generation modes, blast furnaces, certain water-treatment phases, ongoing pipeline flow, in-progress switching).
- If the playbook does not name pre-decided authority for the OT-side response: theater. In a real incident the authority question is the bottleneck — pre-decide it.
- If the playbook does not include process-safety engagement (the SIS / safety team participates in the IR decision, not just IT/OT cyber): theater for processes where safety is the controlling consideration.
- Acceptable: per-asset-class IR playbook with explicit shutdown-vs-keep-running decision tree, pre-decided authority, process-safety integration, and tabletop-exercise evidence within the last 12 months including ICS-specific scenarios (Sandworm-style, Volt Typhoon-style, ransomware-approaching-IDMZ).

---

## Defensive Countermeasure Mapping

Maps energy-sector offensive findings to MITRE D3FEND IDs from `data/d3fend-catalog.json`, with explicit defense-in-depth layer position, least-privilege scope, zero-trust posture, and the inverted ephemeral/AI-pipeline applicability (long-lived OT inverts the usual architectural-impossibility exemption).

| D3FEND ID | Technique | Purdue Layer + Energy Overlay | Least-Privilege Scope | Zero-Trust Posture | Energy-Realistic Applicability |
|---|---|---|---|---|---|
| D3-NI | Network Isolation | L3.5 IDMZ as primary; substation L2/L1 micro-segmentation (station bus vs process bus per IEC 61850-90-4); control-center to substation conduit isolation; AMI head-end isolation; DER aggregator cloud control plane treated as external network | Per-zone, per-conduit; no flat L2 between BPCS, SIS, and substation bays | Conduit policy applied per-flow; default-deny | Universally applicable. Brownfield retrofit constrained by L1 device limits at substations — supplement with L2.5 enforcement points (managed switches with ACLs, conduit-level firewalls) where L1 cannot enforce. |
| D3-NTPM | Network Traffic Policy Mapping | L3.5 IDMZ; substation conduit; AMI head-end conduit; DER aggregator boundary; market-systems boundary | Per-conduit allowlist with energy-protocol-aware policy expression (IEC 60870-5-104 ASDU types, IEC 61850 MMS service types, DNP3 object groups, Modbus function codes) | Continuous verification; deviation → alert | Applicable. Requires ICS-protocol-aware policy expression — generic L4 firewall rules are insufficient for energy protocols. |
| D3-NTA | Network Traffic Analysis | Passive sensor at L2/L3 span ports; substation span ports; control-center to substation conduits; AMI head-end; DER aggregator boundary | SOC-visible aggregated; operator-visible scoped to that operator's zone; substation engineer visibility scoped to that substation | Detection assumes the network is hostile until proven otherwise per-flow | Applicable. ICS-aware IDS with energy protocol decoders (Claroty, Nozomi, Dragos, Tenable OT, SCADAfence, Cisco Cyber Vision) is the deployed control. Industroyer2-class signatures widely deployed; bespoke campaign signatures lag. |
| D3-EAL | Executable Allowlisting | L2 station HMI hosts; L2 engineering workstations (PCM600, DIGSI, AcSELerator, etc.); L3 historian/MES hosts; AMI head-end servers; market-systems servers | Per-host allowlist of signed executables; vendor-tooling exceptions explicit and audited | Default-deny execution; only enumerated binaries run | Applicable to Windows/Linux engineering and HMI hosts. Cannot apply directly to L1 IEDs, smart meters, smart inverters — for those, signed-firmware enforcement (where vendor supports) is the analogue; signed-firmware support varies widely across energy vendors. |
| D3-PSEP | Process Segment Execution Prevention | L2 station HMI hosts; L2 engineering workstations; control-center operator hosts | Per-process memory-execution policy; non-exec data segments | Memory regions verified at execution time | Applicable where host OS supports modern memory protections. Brownfield Windows 7 / Windows Server 2008 hosts have weaker support — compensating control: tighter D3-EAL + D3-NTA + isolated network. Substation engineering hosts often locked to vendor-tool-supported OS versions, constraining options. |

**Inverted ephemerality posture (the usual architectural-impossibility exemption, reversed — extended from `ot-ics-security`).** Energy infrastructure is among the longest-lived OT in existence. Substation relays from the 1980s remain in service; transmission RTUs from the 1990s carry IEC 60870-5-104 today; pipeline SCADA hosts running Windows XP / Server 2003 remain operationally common. Controls assuming rapid patching are unrealistic; controls assuming rebuild-on-change are catastrophic for grid stability. The energy-appropriate posture: virtual patching at L3.5 / L2 boundaries, executable allowlisting on engineering and HMI hosts, ICS-IDS detection with energy-protocol decoders as the primary control where prevention is architecturally unavailable, signed-firmware enforcement where supported, and explicit documentation of multi-decade compensating-control programmes. Recommendations that read "patch the substation relay firmware" without specifying the change window (often an annual outage), the vendor's signed-firmware support status, the protective-relay coordination re-test plan, and the rollback plan are operationally indefensible.

---

## Hand-Off / Related Skills

After producing the energy-sector posture assessment, chain into the following skills.

- **`ot-ics-security`** — the OT foundation this skill extends. Run the `ot-ics-security` Analysis Procedure on the OT estate before applying energy-specific overlays. The IEC 62443-3-3 SL scorecard, AI-HMI audit, Purdue-level inventory, and the inverted ephemerality framing all originate there.
- **`supply-chain-integrity`** — for vendor-supplied firmware (Siemens, Rockwell, Schneider Electric, ABB, GE Vernova, Hitachi Energy, AVEVA, Itron, Landis+Gyr, Sensus, Tesla, Enphase, SolarEdge, Sungrow, SMA, Fronius), engineering software, AI dispatch features. SLSA-style provenance, SBOMs (CycloneDX or SPDX), signed-firmware verification, in-toto attestations, Sigstore verification. The energy supply chain is heterogeneous and maturity varies widely.
- **`identity-assurance`** — engineering workstation AAL3, vendor remote-access account model post-Unitronics, jump-host MFA, just-in-time credentialing, separation of engineering vs. operator vs. market-user identities. DER aggregator identity model.
- **`attack-surface-pentest`** — energy-aware pen-test with explicit safety scoping. Rules of engagement must spell out: no production-effecting actions on live grid / pipeline / treatment, no PLC writes outside isolated test bench, no DoS testing on operational conduits, presence of an OT-aware authoriser with stop-test authority, explicit identification of SIS-adjacent / SIL-rated assets out of scope, and substation physical-access carve-outs. TIBER-EU / DORA TLPT (if EU regulated), CBEST (if UK financial overlap on energy trading), AESCSF red-team activities (AU).
- **`coordinated-vuln-disclosure`** — energy-vendor advisory cycle via CISA ICS-CERT (https://www.cisa.gov/news-events/cybersecurity-advisories/ics-advisories), ENISA EU-CSIRT, AU ACSC, UK NCSC. Energy vendor advisory cadence and quality varies widely; ISO/IEC 29147 + 30111 expectations are not uniformly met.
- **`compliance-theater`** — extend the four theater tests above with general-purpose theater detection.
- **`framework-gap-analysis`** — per-jurisdiction reconciliation called for in Analysis Procedure Step 11.
- **`global-grc`** — alongside framework-gap-analysis when EU NIS2 + NCCS-G + CER, UK NIS+CAF, AU SOCI+AESCSF, JP NISC+METI, IL INCD all apply.
- **`ai-attack-surface`** — when AI-assisted dispatch, AI-augmented HMI, or AI-augmented forecasting is in scope. ATLAS AML.T0020 / AML.T0043 poisoning surfaces.
- **`rag-pipeline-security`** — when engineering knowledge-base RAG, vendor-document RAG, or operator-assistant RAG is in scope.
- **`mcp-agent-trust`** — for tool-use governance on copilots with write access to setpoint / breaker / market-bid surfaces.
- **`kernel-lpe-triage`** — for every L2/L3 Linux engineering / historian / HMI host, run kernel-lpe-triage to score Copy Fail (CVE-2026-31431) and Dirty Frag (CVE-2026-43284 / -43500) exposure.
- **`policy-exception-gen`** — to generate defensible exceptions for energy-OT assets where corporate IT SLAs (30-day patch) are architecturally infeasible. The exception evidence is the documented compensating-control programme: D3-NI conduit policy, D3-EAL allowlist, D3-NTA detection coverage, change-window patch schedule (often annual outage), vendor support status.
