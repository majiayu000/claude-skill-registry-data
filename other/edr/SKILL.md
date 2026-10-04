---
name: edr
description: "Expert routing agent for Endpoint Detection & Response (EDR). Routes to platform-specific agents for CrowdStrike, Defender for Endpoint, SentinelOne, Carbon Black, Cortex XDR, Elastic Defend, Sophos, and Wazuh. Covers cross-platform EDR concepts, detection methodology, and platform selection. WHEN: \"EDR\", \"endpoint detection\", \"endpoint protection\", \"behavioral detection\", \"IOC\", \"IOA\", \"MITRE ATT&CK\", \"threat hunting\", \"endpoint telemetry\", \"XDR\". Do NOT use for platform-specific questions -- use the `crowdstrike`, `defender-endpoint`, `sentinelone`, `carbon-black`, `cortex-xdr`, `elastic-defend`, `sophos`, or `wazuh` skill."
license: MIT
---

# Endpoint Detection & Response (EDR)

This skill covers Endpoint Detection & Response (EDR) platforms. It provides broad knowledge across all major EDR solutions and deep expertise in cross-platform EDR concepts, detection methodology, and platform selection. Read the platform-specific sibling skill for detailed technical work.

## How to Approach Tasks

When you receive a request:

1. **Identify the platform** — Determine which EDR platform the user is working with. If clear, read the appropriate sibling skill immediately. If unclear or multi-platform, handle at this level.

2. **Classify the request type:**
   - **Platform selection / comparison** — Handle here using the comparison table and concepts reference
   - **Detection engineering** — Load `references/concepts.md` for methodology, then read the appropriate sibling skill
   - **Incident response** — Read the appropriate sibling skill for tool-specific response actions
   - **Threat hunting** — Read the appropriate sibling skill for query language specifics
   - **Architecture / deployment** — Read the appropriate sibling skill's architecture reference
   - **Tuning / false positive reduction** — Read the appropriate sibling skill's best-practices reference

3. **Load context** — For cross-platform questions, read `references/concepts.md`. For platform-specific questions, read the appropriate sibling skill.

4. **Analyze** — Apply EDR-specific reasoning. Understand the difference between detection and prevention, behavioral vs. signature-based approaches, and the tradeoffs between alert fidelity and coverage.

5. **Recommend** — Provide actionable guidance. For platform-specific queries, include platform-native syntax and tooling.

## Platform Routing

Read the appropriate sibling skill based on the platform:

| Platform | Agent | Trigger Keywords |
|---|---|---|
| CrowdStrike Falcon | `crowdstrike` | Falcon, CrowdStrike, RTR, Threat Graph, OverWatch, Charlotte AI, CQL |
| Microsoft Defender for Endpoint | `defender-endpoint` | MDE, Defender for Endpoint, ASR rules, KQL advanced hunting, AIR, Defender XDR |
| SentinelOne | `sentinelone` | SentinelOne, Singularity, Storyline, Deep Visibility, Purple AI, Ranger |
| Carbon Black | `carbon-black` | Carbon Black, CB Defense, CB Response, VMware Carbon Black, Broadcom EDR |
| Cortex XDR | `cortex-xdr` | Cortex XDR, Palo Alto XDR, XQL, BIOC, XSIAM, Causality View |
| Elastic Defend | `elastic-defend` | Elastic Defend, Elastic Security, Elastic Agent, Fleet, ECS |
| Sophos Intercept X | `sophos` | Sophos, Intercept X, CryptoGuard, Sophos Central, Deep Learning |
| Wazuh | `wazuh` | Wazuh, OSSEC, open-source EDR, FIM, SCA, Wazuh indexer |

## EDR Platform Comparison

### Feature Matrix

| Capability | CrowdStrike | Defender MDE | SentinelOne | Carbon Black | Cortex XDR | Elastic Defend | Sophos | Wazuh |
|---|---|---|---|---|---|---|---|---|
| Deployment model | Cloud-native | Cloud (M365) | Cloud/on-prem | Cloud/on-prem | Cloud | Cloud/self-hosted | Cloud (Central) | Self-hosted |
| Agent footprint | ~25MB, lightweight | Built-in Windows | Light | Moderate | Moderate | Via Elastic Agent | Moderate | Lightweight |
| NGAV prevention | Yes | Yes | Yes | Yes | Yes | Yes | Yes (Deep Learning) | Limited |
| Behavioral EDR | Yes (IOA) | Yes (E5) | Yes (Storyline) | Yes | Yes (BIOC) | Yes | Yes | Yes (rules) |
| Threat hunting | CQL / Falcon Insight | KQL Advanced Hunting | Deep Visibility | Solr/CB Search | XQL | Kibana / EQL | Sophos Central | OpenSearch |
| Auto-response | Yes (RTR) | Yes (AIR) | Yes (1-click rollback) | Yes (Live Response) | Yes (Live Terminal) | Yes (response actions) | Yes (AAP) | Yes (active response) |
| MITRE ATT&CK mapping | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| XDR / SIEM integration | Falcon LogScale | Sentinel / Defender XDR | Singularity Data Lake | SIEM connectors | Cortex XSIAM | Elastic SIEM | Sophos MDR | Built-in SIEM |
| Managed service | OverWatch / Complete MDR | Microsoft Threat Experts | Vigilance MDR | CB TAU | Unit 42 MXDR | N/A | Sophos MDR | N/A |
| Open source | No | No | No | No | No | Partial (EL2.0) | No | Yes (GPLv2) |
| Licensing model | Module tiers | M365 E3/E5 | Core/Control/Complete | Standard/Enterprise | Varies | Subscription | Central-based | Free (support paid) |

### Deployment Decision Guide

**Choose CrowdStrike when:**
- Cloud-native architecture is required with no on-premises infrastructure
- Managed threat hunting (OverWatch) is a priority
- Large enterprise with strict sensor footprint requirements
- CrowdStrike's Threat Graph AI correlation is valued

**Choose Defender for Endpoint when:**
- Organization is Microsoft-centric (M365 E5 or E3)
- Integration with Azure AD, Intune, Sentinel, and the full Defender XDR suite is needed
- Want built-in vulnerability management (Plan 2)
- Windows-heavy environment with ASR rules for hardening

**Choose SentinelOne when:**
- Autonomous response without cloud connectivity is required
- 1-click rollback capability is a priority for ransomware recovery
- Strong macOS and Linux coverage is needed
- Natural language threat hunting (Purple AI) is appealing

**Choose Carbon Black when:**
- Deep process-level forensic visibility is required
- Full endpoint recording (continuous data capture) is needed
- Existing VMware/Broadcom infrastructure
- Note: Evaluate roadmap carefully post-Broadcom acquisition (2023)

**Choose Cortex XDR when:**
- Palo Alto NGFW and Prisma Cloud are already deployed (native integration)
- Cross-domain correlation (endpoint + network + cloud + identity) is the priority
- Built-in SOAR capabilities (XSOAR integration) are needed

**Choose Elastic Defend when:**
- Already running ELK/Elastic stack for SIEM
- Open-source/cost-sensitive environment
- Custom detection rule development is a core requirement
- Flexibility in data pipeline is needed

**Choose Sophos Intercept X when:**
- SMB or mid-market organization
- Deep learning malware detection without behavioral overhead is preferred
- Integrated MDR service (Sophos MDR) is attractive
- Simple central management via Sophos Central

**Choose Wazuh when:**
- Open-source (GPLv2) is a hard requirement
- Combined HIDS + FIM + SCA + SIEM in one platform is needed
- Regulatory compliance automation (PCI DSS, HIPAA, GDPR) is required
- On-premises or air-gapped deployment is mandatory

## Cross-Platform EDR Concepts

### Detection Methodology Framework

EDR detection operates across multiple layers:

**1. Signature-based (IOC)**
- Matches known-bad file hashes, IP addresses, domains
- Pros: Low false positive rate, fast, deterministic
- Cons: Blind to novel threats, evaded by simple obfuscation

**2. Behavioral (IOA)**
- Detects patterns of behavior regardless of specific file or hash
- Examples: process injection, credential dumping patterns, lateral movement
- Pros: Catches novel threats, obfuscation-resistant
- Cons: Requires tuning, can generate false positives

**3. Machine learning / heuristics**
- Statistical models trained on malicious and benign samples
- Pros: Generalize to new variants
- Cons: Model quality varies, explainability challenges

**4. Threat intelligence correlation**
- Enriches detections with external context (actor attribution, campaign tracking)
- Used by Threat Graph (CrowdStrike), Threat Analytics (MDE), Unit 42 (Palo Alto)

### MITRE ATT&CK Integration

All major EDR platforms map detections to the MITRE ATT&CK framework:
- **Tactics**: High-level adversary goals (Initial Access, Execution, Persistence, etc.)
- **Techniques**: Methods used to achieve tactics (T1059.001 = PowerShell)
- **Sub-techniques**: Specific implementations

When evaluating EDR coverage:
1. Run ATT&CK evaluations (MITRE publishes annual EDR evaluations)
2. Map your threat model to relevant ATT&CK techniques
3. Validate platform coverage for those specific techniques
4. Do not rely solely on vendor ATT&CK coverage claims

### Telemetry vs. Detection

**Telemetry** = raw endpoint event data collected (process starts, file writes, network connections, registry changes, DNS queries)
**Detection** = alert generated from telemetry matching a detection rule or ML model

Key distinction: An EDR may collect telemetry for an event without generating a detection. This matters for:
- Threat hunting (searching telemetry for IOCs after-the-fact)
- Forensic investigation (reconstructing attack timelines)
- Compliance (demonstrating data was collected)

Telemetry retention varies by platform:
- CrowdStrike Falcon Insight: 90 days (default)
- Defender MDE: 30 days (Advanced Hunting)
- SentinelOne Deep Visibility: 90 days (Complete tier)
- Elastic: Configurable (limited by cluster storage)
- Wazuh: Configurable (limited by indexer storage)

### EDR vs. XDR

**EDR (Endpoint Detection & Response):** Focused on endpoint telemetry — processes, files, registry, network connections from the host perspective.

**XDR (Extended Detection & Response):** Cross-domain correlation across endpoint + network + cloud + identity + email. Reduces alert fatigue through correlated incidents.

True XDR platforms: Cortex XDR (Palo Alto), Defender XDR (Microsoft), Singularity (SentinelOne with Data Lake).
EDR-first platforms with XDR evolution: CrowdStrike (Falcon platform), Elastic Security.

### Response Action Taxonomy

| Action | Description | Platforms |
|---|---|---|
| Host isolation | Cut off all network except EDR comms | All major platforms |
| Process kill | Terminate a running process | All major platforms |
| File quarantine | Remove and vault a suspicious file | All major platforms |
| Rollback / remediation | Reverse attacker changes (registry, files) | SentinelOne (1-click), MDE (AIR), CrowdStrike (RTR) |
| Remote shell | Live interactive session on endpoint | RTR (CrowdStrike), Live Response (CB), Live Terminal (Cortex) |
| Memory forensics | Dump process memory for analysis | CrowdStrike RTR, CB Live Response, Elastic response |
| Network containment | Block specific IPs/domains without full isolation | Varies by platform |

## Reference Files

Load these for cross-platform deep knowledge:

- `references/concepts.md` — EDR fundamentals: behavioral detection, IOA vs. IOC, MITRE ATT&CK methodology, telemetry architecture, detection engineering lifecycle. Read for conceptual and methodology questions.

For platform-specific deep knowledge, read the appropriate sibling skill and its references:
- `crowdstrike` (plus its own `references/`)
- `defender-endpoint` (plus its own `references/`)
- `sentinelone` (plus its own `references/`)
- `carbon-black`
- `cortex-xdr`
- `elastic-defend`
- `sophos`
- `wazuh` (plus its own `references/`)
