---
name: ot-ics-security
version: "1.0.0"
description: OT / ICS security for mid-2026 — NIST 800-82r3, IEC 62443-3-3, NERC CIP, IT/OT convergence risks, AI-augmented HMI threats, ICS-specific TTPs (ATT&CK for ICS)
triggers:
  - ot security
  - ics security
  - scada
  - plc security
  - operational technology
  - industrial control
  - iec 62443
  - nist 800-82
  - nerc cip
  - it ot convergence
  - hmi security
  - air gap
  - level 0
  - level 1
  - purdue
data_deps:
  - cve-catalog.json
  - d3fend-catalog.json
atlas_refs:
  - AML.T0010
attack_refs:
  - T1692.001
  - T0883
  - T1190
  - T1068
framework_gaps:
  - NIST-800-82r3
  - IEC-62443-3-3
  - NERC-CIP-007-6-R4
  - NIS2-Art21-patch-management
  - ISO-27001-2022-A.8.8
  - UK-CAF-B2
  - AU-Essential-8-App-Hardening
rfc_refs: []
cwe_refs:
  - CWE-287
  - CWE-798
  - CWE-306
  - CWE-1037
d3fend_refs: []
last_threat_review: "2026-09-18"
discovery_mode: "standalone"  # operator-reached via `exceptd brief ot-ics-security` or `exceptd ask`; not chained into any playbook's direct.skill_chain by design
---

# OT / ICS Security (mid-2026)

## Threat Context (mid-2026)

OT is no longer air-gapped. The "air gap" is a label on a Visio file, not a property of the production network. IT/OT convergence is a fait decompli at every Tier-1 operator and most Tier-2/3 manufacturers, utilities, and water authorities:

- **Production planning / MES / historian systems** routinely cross the IT/OT boundary. SAP, OSIsoft PI / AVEVA PI, Wonderware / AVEVA System Platform, GE Proficy — all collect from L2/L3 and surface to L4 enterprise reporting, often via cloud.
- **Remote-vendor maintenance access** is the operational norm. Siemens, Rockwell, Schneider Electric, ABB, GE Vernova, Emerson, Honeywell all ship remote-support tooling. A typical mid-size plant has 5–20 active vendor jump paths.
- **Cloud-hosted OT telemetry** is mainstream. AWS IoT SiteWise, Azure Industrial IoT, GCP Manufacturing Data Engine, plus vendor-specific clouds (Siemens Insights Hub, Rockwell FactoryTalk Hub, Schneider EcoStruxure) ingest L2 telemetry at scale.

**AI-augmented HMI is the new wrinkle.** Operators are increasingly fed LLM-generated summaries of plant state ("3 alarms in the last hour, two transient pressure-relief actuations on PT-204, one sustained temperature deviation on TIC-117 trending toward HH"). LLM-assisted engineering tools draft ladder logic, generate alarm-handling logic, propose setpoint adjustments. Prompt injection into an AI HMI assistant — via crafted historian tags, malicious vendor-document upload to an engineering workstation RAG, or polluted plant-state context — could lead to physical-process consequences: operator misled into ignoring a real alarm, engineering assistant inserting subtly wrong logic into a generated PLC routine, autonomous closed-loop adjustment of a setpoint outside safe range. The classical IEC 62443 zone-and-conduit model assumes deterministic data flows between trust zones; LLM-generated content is non-deterministic content sourced from a trust-conduit that does not exist in the standard.

**State-sponsored OT targeting is continuous, not episodic.** Volt Typhoon pre-positioning against US critical infrastructure (water, energy, transport) was confirmed by CISA/NSA/FBI in 2023–2024 and re-affirmed in 2025 joint advisories. Sandworm continues active operations against Ukrainian grid through 2025 (Industroyer2, Pipedream/Incontroller-derived tooling, and bespoke OT-aware wipers). 2025 saw the first publicly attributed AI-assisted OT reconnaissance campaign — adversaries using LLMs to triage exfiltrated engineering documents at scale.

**The exemption posture inverts vs. the ephemeral / AI-pipeline case.** The usual architectural-impossibility exemption is about ephemeral and AI-pipeline environments where some controls cannot run. OT is the opposite: OT systems are LONG-LIVED, often 10–30 year service lives. PLCs in service today were commissioned when Windows XP was current; HMIs running Windows 7 are routine; safety-instrumented systems (SIS) are deliberately frozen. The exemption that applies is reversed: "patch within 30 days" is architecturally impossible not because the workload is ephemeral but because the workload is fossilised, change-controlled, and physically dangerous to disturb. Recommendations must explicitly acknowledge multi-decade lifecycles and provide compensating-control paths (segmentation, allowlisting, unidirectional gateways, virtual patching at the L2/L3 boundary) rather than handwave "update the firmware."

---

## Framework Lag Declaration

| Framework | Control | Designed For | Fails Because |
|---|---|---|---|
| NIST 800-82r3 (Oct 2023) | Guide to OT Security | OT architecture and segmentation; converged IT/OT environments | Predates the AI-augmented-HMI threat class. Treats AI as "future consideration." No guidance on LLM-as-a-conduit between trust zones; no requirement that AI assistant integration appear in the zone/conduit drawing. |
| IEC 62443-3-3 (System Security Requirements) | SR 1–7 with Security Levels SL 1–4 | Industrial automation control system security, method-neutral | Method-neutral on AI integration — neither prohibits nor scopes LLM-assisted HMI, leaving SL claims silent on a real attack surface. Conduit definitions assume deterministic protocol-level flows; LLM-generated content is non-deterministic content over a conduit that the standard does not name. |
| NERC CIP-007-6 R4 (Security Event Monitoring) | BES Cyber Systems logging, alerting, response, retention | North-American bulk electric system (BES) High/Medium impact assets | R4 logging assumes a small, enumerable set of event sources. AI-assistant interactions (prompts, completions, tool calls) are neither in scope nor excluded — operators have no audit trail for AI-mediated operator decisions. Patch SLA in adjacent CIP-007-6 R2 is workable for IT, hard for OT firmware. |
| NIS2 Directive Art. 21 | Risk management measures for essential/important entities (energy, transport, water, manufacturing, food, waste, digital infra) | EU-wide cybersecurity baseline | Silent on OT-specific controls. "Appropriate measures" leaves Member State authorities to fill the OT gap unevenly. Patch-management language treats IT and OT identically — operationally indefensible for 25-year PLC fleets. |
| EU DORA + CRA | Financial-sector ICT resilience + product cybersecurity for digital elements | EU financial services; products with digital elements placed on EU market | DORA out of scope for most pure-OT operators (covers financial sector ICT). CRA applies to OT products placed on the EU market post-Dec 2027 — does not retroactively fix the deployed brownfield fleet. |
| UK NIS Regulations + CAF (Cyber Assessment Framework) | OES (Operators of Essential Services) including energy, transport, water | UK-equivalent of NIS2; outcome-focused | CAF outcomes are sound but lack specific OT-aware operational definitions; AI-assistant integration into HMI is not a CAF outcome. |
| AU SOCI Act 2018 (as amended 2022) + AESCSF | Security of Critical Infrastructure across 11 sectors; energy-sector cybersecurity maturity | AU critical infrastructure regulation; sector-specific maturity | AESCSF is OT-aware but its AI dimension is treated as monitoring scope, not as a new conduit type. SOCI risk-management programmes do not specifically require AI-HMI threat modelling. |
| JP NISC Critical Infrastructure Policy (14 sectors) | National critical-infrastructure cybersecurity policy | JP CI sectors | Policy-level; operational specifics defer to sector guidelines (METI for energy, MLIT for transport). AI-augmented OT not specifically addressed in current guidance. |
| IL INCD Critical Infrastructure Directives | National CI cyber directives | IL critical-infrastructure operators | OT-aware but does not yet codify AI-assistant integration as a regulated surface. |
| ID BSSN Critical Infrastructure Rules | National cybersecurity for vital information infrastructure | ID critical-infrastructure operators | Maturing framework; OT specifics evolving; AI integration not yet codified. |
| TW CSMA (Cyber Security Management Act) | National critical-infrastructure cyber-security management | TW critical infrastructure including semicon fabs and energy | Strong on segmentation and reporting; AI-assistant integration into operator workflows not specifically scoped. |
| ISO 27001:2022 + ISO/IEC 27019 (energy utilities) | Generic ISMS + energy-sector extension | Organisation-level ISMS | A.8.8 vulnerability management is IT-flavoured; ISO/IEC 27019 adds energy specifics but predates AI-augmented HMI. |

**Cross-jurisdiction posture (global-first, not US-centric):** Any OT/ICS gap analysis for a multi-jurisdiction operator must cite at minimum EU NIS2 + DORA + CRA, UK NIS+CAF, AU SOCI+AESCSF, JP NISC, IL INCD, ID BSSN, TW CSMA, alongside ISO 27001:2022 + ISO/IEC 27019. US-only (NIST 800-82r3, NERC CIP) is insufficient for any operator with multinational exposure.

---

## TTP Mapping

ATT&CK for ICS is a separate matrix from Enterprise. Many IT-rooted SOCs do not track ICS TTPs — that gap alone is a finding.

| Surface | TTP | Matrix | Variant in mid-2026 | Gap Flag |
|---|---|---|---|---|
| Internet-exposed control-system asset | T0883 — Internet Accessible Device | ATT&CK for ICS | HMI/PLC reachable via Shodan/Censys; default-cred VNC; vendor remote-support tooling exposed | IEC 62443-3-3 SR 5.1 (network segmentation) presumes a perimeter that does not exist for vendor-mediated remote access |
| Unauthorized control command | T1692.001 — Unauthorized Command Message | ATT&CK for ICS | Modbus/TCP, DNP3, S7, EtherNet/IP write to coil/register without authentication | CWE-306 (Missing Authentication) and CWE-287 (Improper Authentication) baked into protocols; IEC 62443-3-3 SR 1.1/1.2 (identification & authentication) cannot be enforced at L1 protocol layer |
| Lateral movement within OT | T0867 — Lateral Tool Transfer | ATT&CK for ICS | Engineering workstation → HMI → PLC programming-software pivot | NIST 800-82r3 segmentation guidance does not specify L2/L1 micro-segmentation; AESCSF MIL-1 tolerates flat L2 |
| OT scripting | T0853 — Scripting | ATT&CK for ICS | PowerShell on engineering workstation; vendor-tool macro; LLM-generated PLC code reviewed only by overworked engineer | No framework requires diff-review of AI-generated control logic |
| IT-side initial access pivoting to OT | T1190 — Exploit Public-Facing Application | ATT&CK Enterprise | Historian (PI Vision), MES web UI, vendor remote-portal web app | NIST 800-53 SC-7 perimeter assumption does not address IT→OT pivot chain |
| HMI host LPE | T1068 — Exploitation for Privilege Escalation | ATT&CK Enterprise | Windows 7/10 HMI host; un-rebootable; Copy Fail (CVE-2026-31431) on any Linux HMI; Print Spooler / win32k LPE family on Windows HMIs | IT patch SLAs (30 day) inapplicable to HMI hosts; no compensating-control baseline in NIST 800-82r3 |
| Hard-coded / shared credentials | CWE-798 | CWE | Vendor default creds on PLC web UI; shared "operator" account across HMI fleet | IEC 62443-3-3 SR 1.5 (authenticator management) cannot land on devices that lack per-user accounts; NERC CIP-007-6 R5 password-management partially addresses but exempts cyber-asset classes lacking user-account features |
| Firmware-image integrity | CWE-1037 (Processor Optimization Removal or Modification of Security-Critical Code) and CWE-345 family (insufficient verification of data authenticity, captured via cve-catalog supply-chain entries) | CWE | Unsigned firmware accepted by L1 device; vendor-side build pipeline compromise | NERC CIP-010 baseline-change management does not require firmware-image signature verification at install time |
| AI-assistant prompt injection in HMI/engineering workflow | AML.T0010 — AI Supply Chain Compromise (closest existing ATLAS entry) | ATLAS v2026.09 | Crafted historian tag value or vendor PDF poisons context; LLM proposes unsafe setpoint or misleads operator | No ATT&CK for ICS technique for AI-mediated operator deception; no IEC 62443 control on AI conduit; NIST 800-82r3 silent |

**Note on ATT&CK for ICS ID format.** ATT&CK for ICS uses `T0xxx` IDs (e.g., T1692.001, T0883, T0867). The linter regex `^T\d{4}(\.\d{3})?$` accepts this shape. For IT/OT convergence techniques (the IT side of the pivot), ATT&CK Enterprise IDs (T1190, T1068, T1078) are cited alongside.

**Note on ATLAS coverage.** AML.T0010 (AI Supply Chain Compromise) is the closest current ATLAS v2026.09 mapping for AI-augmented-HMI threats; it does not specifically cover prompt-injection-as-operator-deception in a control room. This is a tracked ATLAS gap — see `forward_watch`.

---

## Exploit Availability Matrix

| Surface / CVE Class | CVSS | RWEP | CISA KEV | PoC Public | AI-Discovered | Active Exploitation | Patch Available | Live-Patchable | OT-Aware Detection |
|---|---|---|---|---|---|---|---|---|---|
| IT/OT bridge — HMI Linux host hit by Copy Fail (CVE-2026-31431) | 7.8 | 90 | Yes (2026-05-01, due 2026-05-15) | Yes — 732-byte script | Yes | Confirmed | Yes | Yes (kpatch/livepatch/kGraft) on supported distros; rare in OT brownfield | Partial — auditd/eBPF rules apply if deployable on HMI host |
| IT/OT bridge — HMI Windows host LPE (Print Spooler / win32k family) | varies | varies | Some entries KEV-listed | Yes | Mixed | Confirmed | Yes for in-support; out-of-support HMIs are exposed permanently | No — Windows live-patch is limited to Hotpatch on supported builds | EDR if deployable; many OT EDR carve-outs |
| Vendor-side OT CVEs (Siemens, Rockwell, Schneider, ABB, GE Vernova) | varies | varies | Several KEV listings 2024–2026 | Mixed — vendor disclosures only sometimes accompanied by PoC | Increasing AI-assisted RE | Targeted exploitation by Sandworm-aligned and Volt Typhoon-aligned actors | Vendor-dependent — typical lag 60–180 days; deploy lag 1–5 years | No — firmware updates require change windows | ICS-aware IDS (Claroty, Nozomi, Dragos, Tenable OT) detection signature lag varies |
| AI-HMI prompt injection (no CVE-class yet) | n/a | risk-modelled, not CVSS | n/a | Demonstrated in research and 2025 incident-response engagements | n/a (vector is the AI conduit itself) | Suspected in 2025 advanced campaigns | Mitigation only — design-time controls on the AI integration | n/a | Requires LLM-aware telemetry — almost never present |

**Honest gap statement (declare what the catalog does not yet cover).** This project's `data/cve-catalog.json` does not yet contain an exhaustive inventory of vendor-side OT CVEs (Siemens SSAs, Rockwell SD advisories, Schneider Electric Security Notifications, ABB CSAs, GE Vernova advisories). The authoritative source for current OT/ICS CVEs is the CISA ICS-CERT advisory feed at https://www.cisa.gov/news-events/cybersecurity-advisories/ics-advisories — captured in `forward_watch` for inclusion in the catalog as part of the next data refresh. Do not invent CVE IDs to fill this matrix.

---

## Analysis Procedure

This procedure threads the three foundational design principles (defense in depth, least privilege, zero trust) through every step.

**Defense in depth.** Purdue Enterprise Reference Architecture layers (L0 physical I/O → L1 PLC/RTU/BPCS → L2 SCADA/HMI → L3 site operations/MES → L3.5 IDMZ → L4 enterprise → L5 cloud/enterprise edge). Controls required at every layer, with the IDMZ (L3.5) acting as the policy-enforcement boundary between OT and IT. Network segmentation (D3-NI), unidirectional gateways for OT→IT data egress, ICS-aware IDS at L2/L3 boundary (D3-NTA), signed-firmware enforcement at L1 where vendor supports it, executable allowlisting (D3-EAL) on engineering workstations and HMI hosts.

**Least privilege.** Engineering-workstation privileges strictly separate from HMI operator. Vendor remote access scoped to specific assets, specific actions, and specific time windows (jump host with session recording; no standing VPN). AI HMI assistants run with read-only context by default; any tool-use that writes to historian, setpoint, alarm-suppression list, or PLC must require explicit operator approval with non-AI-mediated confirmation. SIS engineering workstations are not the same workstation as BPCS engineering, and neither has internet egress.

**Zero trust.** Never assume the OT network is trustworthy because it sits behind a firewall. Identity-bind every command — Modbus write, DNP3 control, S7 download — through an authenticated proxy where the protocol does not natively support it. Every vendor-remote-access session verified per-action, not per-session. AI-assistant outputs treated as untrusted content from a non-enumerable producer until cross-checked against a deterministic source (historian raw data; SIS independent reading).

### Step 1 — Inventory OT assets per Purdue level

Capture (ideally from a passive ICS-aware sensor such as Claroty CTD / Nozomi Guardian / Dragos Platform / Tenable OT; failing that, from a documented walkdown):

- L0 (sensors, actuators, field instruments): count, vendor, communication protocol (4–20 mA, HART, Profinet, EtherCAT, IO-Link).
- L1 (PLCs, RTUs, BPCS controllers, SIS logic solvers): vendor, model, firmware version, last firmware update date, network address, supported protocols.
- L2 (SCADA front-ends, HMIs, engineering workstations, OPC servers, alarm servers): host OS + patch level, application + version, account model, exposed services.
- L3 (site MES, historians, batch managers): host OS, application + version, exposed services, data flows into and out of the zone.
- L3.5 (IDMZ): all assets, all conduits, all data flows enumerated.
- L4 (enterprise integration points): all systems that pull from L3 or push to L3.

### Step 2 — Classify each zone against IEC 62443-3-3 Security Levels

For each zone identified in Step 1, determine target SL (1–4) based on consequence of compromise:

- SL 1: protection against casual or coincidental violation
- SL 2: protection against intentional violation using simple means
- SL 3: protection against intentional violation using sophisticated means
- SL 4: protection against intentional violation using sophisticated means with extended resources

SIS and HIPPS zones target SL 3 or SL 4. BPCS typically SL 2 minimum, SL 3 if process consequence is severe.

Score actual SL achieved against target across all seven Foundational Requirements (FR 1–7). Document deltas.

### Step 3 — Map IT/OT convergence surfaces

Enumerate every IT→OT and OT→IT data flow:

- Historian/MES ↔ ERP/SAP
- Engineering workstation ↔ vendor cloud / patch server
- Vendor remote-support paths (jump host, VPN, vendor-cloud-mediated)
- Cloud-OT telemetry pipelines
- Operator workstation ↔ enterprise email, browsing, document collaboration (a frequent finding: HMI used as a general workstation)
- Backup pipelines into the OT environment
- AV/EDR signature update paths

For each, identify the conduit, the policy enforcement point, the authentication model, the audit/logging coverage.

### Step 4 — Audit AI-assistant integration with HMI / engineering workflow

Specifically ask:

- Is there an LLM-generated content surface visible to operators (alarm summary, shift report, plant-state synopsis)? If yes — what is the source data, what is the prompt template, who controls the model endpoint, where are prompts and completions logged?
- Is there an engineering assistant generating or suggesting PLC code, ladder logic, function-block diagrams, alarm-handler logic, or setpoint adjustments? If yes — what is the review gate, who signs off, is the diff visible to the SIS team?
- Is there a control-room copilot with tool-use access (read/write to historian, alarm-suppression list, OT-asset registry, PLC programming software)? If yes — what are the writable tools, what is the approval workflow, what is the kill switch?
- Is there a vendor-supplied AI feature in the HMI software itself (Siemens Industrial Copilot, Rockwell FactoryTalk Optix AI extensions, Schneider EcoStruxure assistant)? If yes — what is the data-residency posture, what is the trust boundary, who has prompt-injection liability?

If "no AI integration" is the answer but operators have ChatGPT / Copilot / Gemini open on the same workstation: that is a shadow-AI integration, not the absence of one. Cross-reference with `mcp-agent-trust` and `ai-attack-surface`.

### Step 5 — Verify network segmentation (D3-NI + D3-NTPM)

- Produce the network diagram with Purdue levels, zones, conduits, and IDMZ explicitly drawn.
- Verify conduit enforcement: is the L3↔L3.5 firewall ruleset readable, current, and audited?
- Verify directional flow at the IDMZ: are unidirectional gateways used for OT→IT export of historian data where feasible (Waterfall, Owl, Siemens ScalanceLPE-RUGGEDCOM, Hirschmann Tofino)?
- Are vendor remote-support paths terminated at a jump host inside the IDMZ with session recording, or do they tunnel directly to L2/L1? Direct tunnels into L2/L1 violate the zone-and-conduit model regardless of how the firewall is configured.

### Step 6 — Audit vendor remote access (zero-trust application)

- Maintain a vendor-access ledger: vendor, contracted scope, technical scope, account model, MFA enforcement, session-recording, time-window restrictions, last actual access.
- Each session per-action verified (jump-host command policy, just-in-time credential issuance) rather than per-session (open VPN tunnel with vendor-side credential).
- Confirm vendor accounts deprovisioned within 24h of contract termination.

### Step 7 — Audit patch posture against NERC CIP-007 (where applicable) and SLAs against OT reality

For BES Cyber Systems subject to NERC CIP-007-6 R2:

- 35-day evaluation requirement: when did the entity last evaluate available patches against current installed software?
- Patch source identification documented and current.
- Mitigation plan filed for patches not yet applied within 35 days, with target installation date.

For non-NERC OT assets, document the actual OT-realistic patch SLA (often quarterly during planned shutdowns, sometimes annual). If the documented IT SLA is 30 days but OT reality is 365+ days, the IT SLA is theater for the OT assets and a separate documented compensating-control programme is required (segmentation, allowlisting D3-EAL, ICS-IDS detection, virtual patching D3-PSEP at the boundary).

### Step 8 — Build OT-aware incident response

- OT incident response playbook must explicitly answer: "is process shutdown the safe response to a suspected compromise, or is it the dangerous response?" The answer is process-dependent — for some processes shutdown is the safest available action; for others (continuous-cracker chemical processes, certain power-generation modes, blast furnaces, certain water treatment phases) an unplanned shutdown is catastrophically worse than the suspected compromise.
- Pre-decision authority: who, in advance, has authority to direct OT-side response? (Plant manager? OT lead? SIS engineer? Process safety?)
- IR playbooks reviewed and exercised against ICS-specific scenarios (Sandworm-style, Volt Typhoon-style pre-positioning, ransomware that hit the IT side and is approaching the IDMZ).

### Step 9 — Compliance Theater Check (see dedicated section below for the concrete tests)

### Step 10 — Cross-jurisdiction output reconciliation

For each jurisdiction the operator is exposed to (EU, UK, AU, JP, IL, ID, TW, US, and sector-specific equivalents), produce a single mapping of the same control findings to that jurisdiction's regulatory language. Disparate findings for the same control deficiency across jurisdictions are themselves a finding.

---

## Output Format

The skill produces an OT / ICS Security Posture Assessment covering Purdue-model zone inventory, IEC 62443 zone-and-conduit posture, NERC CIP / TSA-pipeline coverage, AI-augmented threat exposure (NIST IR 8504 ICS-AI), and the prioritized roadmap for safety-system isolation. The shape below is consumed downstream by `sector-energy` (which inherits the NERC CIP rows), by `incident-response-playbook` (which scopes IR with the Purdue-zone affected-asset list), and by `compliance-theater` (which compares the deployed segmentation against IEC 62443 / NERC CIP claims). Preserve the per-zone safety-system field verbatim — it is the auditable safety-isolation evidence.

Produce this structure verbatim:

```
## OT / ICS Security Posture Assessment

**Assessment Date:** YYYY-MM-DD
**Site / Operator:** [name]
**Process(es) in scope:** [e.g., crude distillation unit; 500kV substation; water treatment Train A]
**Regulatory jurisdictions:** [US/NERC, EU/NIS2, UK/CAF, AU/SOCI+AESCSF, ...]

### Purdue-Level Asset Inventory
| Level | Assets (count + class) | OS / Firmware Range | Avg Age (years) | Patch Posture |
|-------|------------------------|---------------------|-----------------|----------------|
| L0    | ...                    | ...                 | ...             | n/a            |
| L1    | ...                    | ...                 | ...             | ...            |
| L2    | ...                    | ...                 | ...             | ...            |
| L3    | ...                    | ...                 | ...             | ...            |
| L3.5  | ...                    | ...                 | ...             | ...            |

### IEC 62443-3-3 SL Scorecard (per zone)
| Zone | Target SL | Actual SL | FR Deltas (FR1–FR7) | Notes |

### IT/OT Bridge Inventory
| Source | Destination | Conduit | Auth Model | Logging | Risk |

### AI-HMI Integration Audit
| Surface | Vendor / Model | Read or Write | Approval Gate | Prompt + Completion Logging | Kill Switch |

### Network Segmentation Map
[Diagram or textual representation of Purdue zones, conduits, IDMZ, vendor jump paths]

### Vendor Remote-Access Ledger
| Vendor | Scope | Account Model | MFA | Session Recording | Time Window | Last Access |

### NERC CIP / NIS2 / SOCI / CAF Mappings
[Per-jurisdiction control-status matrix]

### Compliance Theater Findings
[Outcome of the four tests in the Compliance Theater Check section]

### Defensive Countermeasure Plan (D3FEND)
[D3-NI, D3-NTPM, D3-NTA, D3-EAL, D3-PSEP — concrete control placements by Purdue layer]

### Priority Remediation Actions
1. ...
2. ...
3. ...

### RWEP-Prioritised CVE Exposure
[IT/OT bridge CVEs ranked by RWEP, not CVSS; see `exploit-scoring` skill for recalculation]
```

---

## Compliance Theater Check

Run all four tests. Any "fail" is a theater finding documented with the evidence (or absence thereof).

**Theater Test 1 — Network diagram and conduit enforcement.**
Ask: "Show me the network diagram with Purdue levels and the conduits between them, dated within the last 12 months."

- If no diagram exists: zone enforcement cannot be claimed; IEC 62443-3-3 SR 5.1 evidence is fabricated.
- If diagram exists but is older than the most recent IT/OT change (new vendor remote path, new cloud telemetry pipeline, new AI assistant integration): the segmentation claim covers a network that no longer exists.
- If diagram exists and is current but no conduit policy artifact (firewall ruleset, allowlist, signed-conduit-policy document) corresponds to each conduit: drawing is documentation theater, not control.

**Theater Test 2 — HMI host patch posture.**
Ask: "What is the time-since-last-patch for each HMI Windows / Linux host, and what is the documented compensating control set for those that cannot be patched within the corporate SLA?"

- If the answer is "we don't patch HMI" with no compensating-control documentation: patch-management policy compliance is theater for the OT subset.
- If the answer references "segmentation" without specifying which segmentation (L2 VLAN? L3 firewall? Unidirectional gateway? Air-gap that is not actually air?) and without an executable allowlist (D3-EAL) and ICS-IDS detection (D3-NTA) as joint compensating controls: the compensating-control claim is theater.
- Acceptable answer: "HMI hosts patched at next planned shutdown (Q3); in the interim D3-EAL deployed via [tool], D3-NTA via [ICS-IDS], host-based network restriction to specific L1 conduit only."

**Theater Test 3 — AI-assistant integration disclosure.**
Ask: "Is there any AI assistant integration with any HMI, engineering workstation, or operator workflow — including shadow IT?"

- If "no" is the answer, ask the follow-up: "Do operators or engineers have ChatGPT / Copilot / Gemini / vendor-AI tooling open on the same workstation they use for HMI or PLC programming?"
- If the follow-up answer is "yes" but the original answer was "no": shadow-AI integration is the actual state; the formal "no AI in HMI" claim is theater.
- If formal AI integration exists but is not documented in the IEC 62443-3-3 zone-and-conduit diagram: the AI conduit is an unmapped trust path — the diagram is theater for AI risk.

**Theater Test 4 — Asset inventory currency.**
Ask: "Show me the SOCI / NIS2 / NERC CIP / CAF evidence for OT asset inventory, with the source-of-truth and the date of last reconciliation against the actual network."

- If asset inventory source-of-truth is a Visio file last edited 18 months ago: regulatory asset-inventory evidence is theater.
- If asset inventory comes from a passive ICS-aware sensor (Claroty / Nozomi / Dragos / Tenable OT) but the reconciliation between sensor view and the formal regulatory submission is unscheduled or absent: the regulatory submission is theater.
- Acceptable: passive ICS-aware sensor is the source of truth; reconciliation against regulatory submission documented quarterly; deltas explained.

---

## Defensive Countermeasure Mapping

Maps OT/ICS offensive findings to MITRE D3FEND IDs from `data/d3fend-catalog.json`, with explicit defense-in-depth layer position, least-privilege scope, zero-trust posture, and the inverted ephemeral/AI-pipeline applicability (long-lived OT inverts the usual architectural-impossibility exemption).

| D3FEND ID | Technique | Purdue Layer Position | Least-Privilege Scope | Zero-Trust Posture | OT-Realistic Applicability |
|---|---|---|---|---|---|
| D3-NI | Network Isolation | L3.5 IDMZ as the primary policy-enforcement boundary; secondary L2↔L1 micro-segmentation | Per-zone, per-conduit; no flat L2 between BPCS and SIS | Conduit policy applied per-flow, not per-VLAN; default-deny conduit posture | Universally applicable; the foundational OT control. Brownfield retrofit constrained by L1 device limits — supplement with L2.5 enforcement points where L1 cannot enforce. |
| D3-NTPM | Network Traffic Policy Mapping | L3.5 IDMZ; L2/L3 boundary; vendor-jump-host conduits | Conduit-level allowlist of source/destination/protocol/port/direction | Continuous verification of conduit conformance; deviation → alert | Applicable. Requires ICS-protocol-aware policy expression (Modbus function codes, S7 PDU types, DNP3 object groups) not just TCP/UDP. |
| D3-NTA | Network Traffic Analysis | Passive sensor at L2/L3 span ports; L3.5 IDMZ choke; L1 where feasible (some devices, some protocols) | Operator-visible alerts scoped to that operator's zone; SOC-visible aggregated | Detection assumes the network is hostile until proven otherwise per-flow | Applicable. ICS-aware IDS (Claroty CTD, Nozomi Guardian, Dragos Platform, Tenable OT, SCADAfence) is the deployed control; signature/anomaly lag is a tracked metric. |
| D3-EAL | Executable Allowlisting | L2 HMI hosts; L2 engineering workstations; L3 historian/MES hosts | Per-host allowlist of signed executables; vendor-tooling exceptions explicit | Default-deny execution; only enumerated binaries run | Applicable to Windows/Linux HMI and engineering workstation hosts. Cannot apply directly to L1 PLC/RTU devices — for those, signed-firmware enforcement (where vendor supports) is the analogue. |
| D3-PSEP | Process Segment Execution Prevention | L2 HMI hosts; L2 engineering workstations | Per-process memory-execution policy; non-exec data segments | Memory regions and process behaviour continuously verified at execution time | Applicable where host OS supports modern memory protections. Brownfield Windows 7 / WinCC older versions have weaker support — compensating control: tighter D3-EAL + D3-NTA. |

**Inverted ephemerality posture (the usual architectural-impossibility exemption, reversed).** OT assets are long-lived (10–30 year service lives). Controls that assume rapid patching are unrealistic; controls that assume rebuild-on-change are catastrophic. The OT-appropriate posture: virtual patching at L3.5 / L2 boundaries, executable allowlisting on hosts that cannot be re-imaged, ICS-IDS detection as the primary control where prevention is architecturally unavailable, signed-firmware enforcement where supported, and explicit documentation of multi-decade compensating-control programmes where the device itself cannot be hardened. Recommendations that read "patch the PLC firmware" without specifying the change window, the vendor's signed-firmware support status, and the rollback plan are operationally indefensible.

---

## Hand-Off / Related Skills

After producing the OT/ICS posture assessment, chain into the following skills.

- **`kernel-lpe-triage`** — for every L2/L3 Linux HMI / historian / engineering-workstation host, run kernel-lpe-triage to score Copy Fail (CVE-2026-31431) and Dirty Frag (CVE-2026-43284 / -43500) exposure. The HMI host class is the most operationally constrained patch surface in the enterprise; the live-patch-vs-reboot decision tree applies with the additional constraint that reboot during continuous operation is often unacceptable.
- **`supply-chain-integrity`** — for vendor-supplied firmware, engineering software, and AI features. SLSA-style provenance, SBOMs (CycloneDX or SPDX), signed-firmware verification, in-toto attestations, and Sigstore verification all apply to OT vendors with widely varying maturity. The OT supply chain is the single most under-controlled surface in most operators.
- **`identity-assurance`** — engineering workstation privileges, vendor remote-access account model, jump-host MFA, just-in-time credentialing, and the separation of engineering vs. operator identities. This is where least-privilege gets concrete; many OT operators have a single shared "Engineer" account on the engineering workstation, which is identity theater.
- **`attack-surface-pentest`** — OT-scoped pen-test with explicit safety boundaries. The pen-test rules of engagement must spell out: no production-effecting actions on live processes, no PLC writes outside an isolated test bench, no DoS testing on live conduits, presence of an OT-aware authoriser with stop-test authority, and explicit identification of any SIS-adjacent or SIL-rated asset that is out of scope. TIBER-EU / DORA TLPT for EU financials, CBEST for UK financial sector, and AESCSF red-team activities for AU energy all need OT-specific carve-outs.
- **`defensive-countermeasure-mapping`** — to deepen the D3FEND mapping above into a layered remediation plan rather than a single-control patch ticket; the OT-realistic compensating-control programme typically combines five or more D3FEND techniques in a defence-in-depth stack.
- **`compliance-theater`** — to extend the four theater tests above with general-purpose theater detection on the operator's wider GRC posture.
- **`framework-gap-analysis`** — for any multi-jurisdiction operator, to produce the per-jurisdiction reconciliation called for in Analysis Procedure Step 10.
- **`global-grc`** — alongside framework-gap-analysis when EU NIS2 + DORA + CRA, UK NIS+CAF, AU SOCI+AESCSF, JP NISC, IL INCD, ID BSSN, TW CSMA all apply.
- **`ai-attack-surface`** and **`mcp-agent-trust`** — when AI-HMI integration is in scope; ai-attack-surface for prompt-injection and operator-deception threats, mcp-agent-trust for tool-use governance on copilots with write access to historian / alarm-suppression / setpoint surfaces.
- **`policy-exception-gen`** — to generate defensible exceptions for OT assets where corporate IT SLAs (30-day patch) are architecturally infeasible. The exception evidence is the documented compensating-control programme: D3-NI conduit policy, D3-EAL allowlist, D3-NTA detection coverage, change-window patch schedule, and vendor support status.

**Forward watch (per skill-format spec).** ATT&CK for ICS coverage expansion to LLM-mediated operator deception; ATLAS additions covering control-system AI integration; CISA ICS-CERT advisory feed (https://www.cisa.gov/news-events/cybersecurity-advisories/ics-advisories) for OT vendor CVE inclusion in `data/cve-catalog.json`; IEC 62443-4-2 SR refinements for AI-integrated components; NIST 800-82r4 (in development) for AI-augmented HMI guidance; vendor signed-firmware roadmaps (Siemens, Rockwell, Schneider Electric, ABB, GE Vernova) for D3-EAL-analogue coverage at L1.
