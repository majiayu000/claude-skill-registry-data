---
name: framework-gap-analysis
version: "1.0.0"
description: Feed a framework control ID and threat scenario — receive the gap between what the control covers and what current TTPs require
triggers:
  - framework gap
  - control gap
  - nist gap
  - iso 27001 gap
  - soc 2 gap
  - pci gap
  - nis2 gap
  - compliance gap
  - why doesn't this control cover
data_deps:
  - atlas-ttps.json
  - cve-catalog.json
  - exploit-availability.json
  - global-frameworks.json
atlas_refs: []
attack_refs: []
framework_gaps: []
last_threat_review: "2026-09-28"
---

# Framework Gap Analysis

This skill analyzes the gap between what a compliance framework control was designed to address and what current attacker TTPs require. It is the meta-skill that underlies compliance-theater, global-grc, and policy-exception-gen.

## Frontmatter Scope

The `atlas_refs` and `attack_refs` arrays are intentionally empty. This skill is a meta-analysis: its subject is the *gap* between a control's design intent and the live TTP landscape, so its inputs are the TTP-to-control mappings already attached to every other playbook and skill rather than a fixed native TTP set. The specific techniques appear in the body where a given gap is illustrated; the authoritative TTP attachment lives on the skill or playbook that owns that detection. The `framework_gaps` reference set is the populated, authoritative declaration for this skill.

## Threat Context (mid-2026)

Compliance frameworks lag the threat environment by years. Most active controls in NIST 800-53, ISO 27001:2022, SOC 2, PCI DSS 4.0, NIS2, and DORA were drafted against assumptions (human-speed exploit development, persistent inventoriable assets, human-controlled accounts) that current attacker TTPs no longer respect. Three concrete mid-2026 instances anchor the lag:

- **CVE-2026-31431 (Copy Fail)** — CISA KEV-listed Linux kernel LPE, AI-discovered in roughly one hour, 732-byte deterministic public PoC, no race condition. NIST 800-53 SI-2 and ISO 27001:2022 A.8.8 patch-window language permits 30-day remediation, during which active exploitation is the documented condition. See `data/cve-catalog.json` for the full entry.
- **CVE-2025-53773** — GitHub Copilot YOLO-mode RCE, CVSS 7.8 (AV:L — local-vector through developer-side IDE interaction; the NVD-authoritative score was corrected from an initial 9.6 / AV:N). Bypasses SOC 2 CC6 and NIST 800-53 AC-2 because the action executes under the AI service account's authorized identity; the access control audit shows "passed."
- **CVE-2026-30615** — Windsurf MCP local-vector RCE, CVSS 8.0 / AV:L (NVD-authoritative; corrected from initial 9.8 / AV:N once the attack-vector reality — attacker controls HTML the MCP client processes — was confirmed). 150M+ combined downloads across MCP-capable assistants share the architectural surface. ISO 27001:2022 A.5.19 / A.5.20 vendor-management language treats MCP servers as SaaS tools, not third-party code executing in production developer environments.

This skill exists because every gap-analysis engagement encounters at least one control where a "compliant" auditor finding masks current-TTP exposure. The built-in gap catalog below is the codified evidence base.

## Framework Lag Declaration

This skill's entire purpose is to declare framework lag per analysis. The pre-analyzed lag declarations live in `## Built-In Gap Catalog` below — each entry states (a) what the control was designed for, (b) the specific current TTP it fails against, and (c) what a real control would require. When a user supplies a control ID and a threat scenario, the analysis procedure produces a new lag declaration in the same shape. The catalog is authoritative for the controls it lists; the procedure handles novel control/threat pairs. Universal lags that no current framework covers adequately are enumerated in `## Universal Gaps` near the end of this skill.

### Expanded jurisdictional cross-walk requirement (per `data/global-frameworks.json`)

The global-first requirement binds against the full expanded catalog, not the EU+UK+AU+ISO baseline. Every gap declaration produced by this skill must cross-walk the cited control against the equivalent obligations in the expanded jurisdiction set tracked in `data/global-frameworks.json`. The cross-walk set as of mid-2026:

- **EU:** GDPR, NIS2 (Directive 2022/2555), DORA (Regulation 2022/2554), EU AI Act (Regulation 2024/1689), EU CRA (Regulation 2024/2847).
- **UK:** UK GDPR / DPA 2018, NCSC CAF, Cyber Essentials / CE+.
- **AU:** Privacy Act 1988 / APP, ASD ISM, Essential 8, APRA CPS 234.
- **Singapore:** MAS TRM, CSA CCoP (CII), PDPA.
- **Japan (expanded):** APPI, METI Cybersecurity Framework, NISC Basic Policy, FISC Security Guidelines.
- **India:** CERT-In Directions (Apr 2022), DPDPA 2023, SEBI Cyber Resilience Framework.
- **Canada:** OSFI B-10, PIPEDA, Quebec Law 25.
- **Israel (IL):** Privacy Protection Law Amendment 13 (2024), INCD Cyber Defense Methodology v2.0.
- **Switzerland (CH):** revFADP (in force 2023-09-01), FINMA Circulars (2023/1 operational risks, 2018/3 outsourcing).
- **Hong Kong (HK):** PDPO + PCPD 2024 cross-border guidance, HKMA SA-2 / TM-G-1 / TM-E-1.
- **Taiwan (TW):** PDPA TW, Cyber Security Management Act (2018), FSC sector guidance.
- **Indonesia (ID):** UU PDP (2022, in force 2024-10-17), BSSN guidance.
- **Vietnam (VN):** Cybersecurity Law 2018 + Decree 53/2022/ND-CP, BCY cryptographic-product certification.
- **South Korea (KR):** PIPA, Network Act, KISA / K-CSAP / KCMVP.
- **China (CN):** PIPL, DSL, CSL, Cybersecurity Review Measures (2022).
- **Brazil (BR):** LGPD + ANPD guidance.
- **Saudi Arabia (KSA):** PDPL + SDAIA Implementing Regulation 2023.
- **Global standards:** ISO 27001:2022 / 27002:2022, ISO/IEC 42001:2023, CSA CCM v4, CIS Controls v8, MITRE ATLAS v2026.09.
- **US sub-national:** NYDFS 23 NYCRR 500 (amended Nov 2023, phased through Nov 2025); state privacy laws (CA CCPA/CPRA, CO CPA, CT CTDPA, IL BIPA, NY SHIELD, TX DPSA, VA CDPA).

A gap declaration that closes section 6 (Global coverage check) without referencing at least the EU, UK, AU, ISO, and a representative selection from {IL, CH, HK, TW, ID, VN, JP-expanded, KR, CN, BR, NYDFS} for any org operating in those jurisdictions is incomplete: a global-first analysis must cover every applicable jurisdiction, not a US-centric subset. The exact set required depends on the org's footprint — but the analyst must consult `data/global-frameworks.json` to enumerate it rather than defaulting to the legacy four-jurisdiction shorthand.

## TTP Mapping (MITRE ATLAS v2026.09 and ATT&CK)

This skill maps framework controls to attacker TTPs on demand rather than statically. The authoritative TTP catalog is `data/atlas-ttps.json` (pinned to MITRE ATLAS v2026.09, September 2026) supplemented by MITRE ATT&CK Enterprise IDs for non-AI threats. The mapping convention used in every gap declaration this skill produces:

| Built-in gap | Primary TTP(s) | Gap flag |
|---|---|---|
| NIST 800-53 SI-2 vs. deterministic LPE | T1068 (Exploitation for Privilege Escalation), T1548.001 | Patch SLA permits active exploitation window |
| NIST 800-53 SC-8/SC-28 vs. Dirty Frag | T1190 (Exploit Public-Facing Application) via IPsec subsystem | Cryptographic control is the attack surface |
| NIST 800-53 SI-2 vs. Fragnesia (Dirty Frag sequel) | T1068 (Exploitation for Privilege Escalation) via XFRM ESP-in-TCP skb coalesce | Patch SLA assumes patches close bug families; the Dirty Frag patch introduced this sibling bug |
| NIST 800-53 AC-2 vs. prompt injection | AML.T0051 (LLM Prompt Injection), AML.T0054 | Authorized identity executes attacker intent |
| NIST 800-53 SI-3 vs. AI-generated malware | AML.T0016 (adversary Obtain Capabilities, payload generation), AML.T0018 | Signature-based detection has zero coverage |
| ISO 27001 A.8.8 vs. CISA KEV class | T1068, T1203 | "Appropriate timescales" undefined for AI-accelerated weaponization |
| SOC 2 CC6 vs. prompt injection | AML.T0051 | Authorization model has no prompt-level granularity |
| PCI DSS 6.3.3 vs. AI-accelerated weaponization | T1068, T1190 | One-month window predates AI-assisted exploit development |
| NIS2 Art. 21 vs. AI pipeline integrity | AML.T0020 (Training Data Poisoning), AML.T0010 | No AI-specific control surface |
| All frameworks vs. ephemeral inventory | T1610, T1525 | Asset-inventory assumption invalid on serverless/container |

For any gap analysis this skill produces, every cited control must be paired with at least one ATLAS or ATT&CK ID drawn from `data/atlas-ttps.json`. Controls without a mapped TTP are orphaned controls and are rejected — every control recommendation must map to a real ATLAS or ATT&CK TTP.

## Exploit Availability Matrix

This skill consumes the matrix produced upstream by the exploit-scoring skill. The authoritative source is `data/exploit-availability.json`; CVE-specific fields (CVSS, RWEP, KEV status, PoC availability, AI-discovery flag, live-patch availability, active exploitation) come from `data/cve-catalog.json`. Every gap declaration must carry the matrix row for the evidence CVE so the "what a real control requires" output is RWEP-justified rather than CVSS-only.

| CVE | CVSS | RWEP | KEV | Public PoC | AI-accelerated | Live-patchable | Active exploitation |
|---|---|---|---|---|---|---|---|
| CVE-2026-31431 (Copy Fail) | 7.8 | 90 | Yes (2026-05-01) | Yes (732 bytes, deterministic) | Yes (AI-discovered) | Yes (kpatch/livepatch) | Confirmed |
| CVE-2026-43284 (Dirty Frag) | 8.8 | 53 | No | Yes (chain component) | Yes (AI-assisted discovery) | Limited (kpatch RHEL-only) | Suspected |
| CVE-2026-46300 (Fragnesia) | 7.8 | 35 (60 if KEV-listed) | No (candidate) | Yes (one-liner vs /usr/bin/su) | Yes (AI-assisted discovery) | Yes (kpatch / canonical-livepatch / KernelCare) | None observed |
| CVE-2025-53773 (Copilot YOLO-mode RCE) | 7.8 | 30 | No | Yes (demonstrated) | Yes (AI tooling enables) | Yes (SaaS push / IDE update) | Suspected |
| CVE-2026-30615 (Windsurf MCP local-vector RCE) | 8.0 | 35 | No | Yes | No | Yes (IDE update) | Suspected |

When a gap analysis cites a CVE not in this matrix, the analyst must populate the row from `data/cve-catalog.json` before producing the declaration. A declaration without an evidence row is incomplete.

## Built-In Gap Catalog

The following gaps are documented with evidence. When a control from this list is referenced, apply the pre-analyzed gap rather than reconstructing the analysis from first principles.

---

### NIST 800-53 SI-2 — Flaw Remediation vs. Deterministic LPE

**Control intent:** Identify, report, and correct system flaws; apply security patches within organizationally defined time periods.

**Designed for:** Network-centric environments (2013), early cloud (Rev 4), where the assumption was human-speed exploit development and patch deployment cycles measured in weeks.

**Fails for:**
- CVE-2026-31431 (Copy Fail): CISA KEV, 732-byte public PoC, deterministic, no race condition. The "organizationally defined time period" is typically 30 days for High, 7 days for Critical. With a public PoC and CISA KEV, any unpatched system is being actively exploited during that window. SI-2 frames patching as remediation; for this class it must be framed as incident response.
- AI-discovered vulnerabilities: The 1-hour discovery-to-weaponization timeline means vulnerability windows are defined by AI capability, not human patch cycles.

**What a real control requires:** A tiered response with time bounds indexed to: (1) CISA KEV status, (2) PoC public availability, (3) live-patch availability, (4) blast radius. For CISA KEV + public PoC + live-patch available: deploy live patch within 4 hours or document compensating controls. Not "within 30 days."

---

### NIST 800-53 SC-8/SC-28 — Transmission/Data at Rest Protection vs. Dirty Frag

**Control intent:** Implement cryptographic mechanisms to prevent unauthorized disclosure during transmission (SC-8) and at rest (SC-28).

**Designed for:** Network-centric environments where IPsec, TLS, and disk encryption are reliable cryptographic controls for data protection.

**Fails for:**
- CVE-2026-43284/CVE-2026-43500 (Dirty Frag): The exploit runs through the IPsec implementation. A system using IPsec to satisfy SC-8 compliance cannot claim IPsec as a compensating control for Dirty Frag — the control is the attack surface.
- CVE-2026-46300 (Fragnesia): Same class as Dirty Frag — page-cache corruption via XFRM ESP-in-TCP skb coalescing. Introduced by the Dirty Frag patch. SC-8 IPsec-based compliance is invalidated identically; operators who removed the Dirty Frag `blacklist esp4 / esp6 / rxrpc` mitigation when that patch landed re-opened the IPsec attack surface for Fragnesia.

**What a real control requires:** Cryptographic controls for SC-8/SC-28 compliance must include integrity assurance for the cryptographic subsystem itself, not just assurance that the subsystem is configured. Kernel subsystem integrity monitoring (eBPF-based, read-only kernel text verification) as a compensating layer. When a CVE patch lands in a cryptographic subsystem, retain the pre-patch compensating controls until the patched code has soaked — the Fragnesia precedent demonstrates the sibling-bug risk.

---

### NIST 800-53 AC-2 — Account Management vs. Prompt Injection

**Control intent:** Manage system accounts, group memberships, privileges, and access authorization throughout the account lifecycle.

**Designed for:** Human user accounts, service accounts, and machine identities in traditional IAM systems.

**Fails for:**
- Prompt injection (CVE-2025-53773 class): An attacker who successfully injects a prompt into an AI assistant causes the AI to take actions using the AI's service account. The service account is properly managed under AC-2 — it's authorized, monitored, and within least-privilege scope. The unauthorized access is happening through the model's context window, not through account compromise. AC-2 audit trails show the service account performing the action. The attacker's identity is absent from all access logs.

**What a real control requires:** Agent identity controls distinct from service account identity: who authorized this specific model invocation, what context was provided, what tools were authorized for this invocation, what did the model actually do. Session-level authorization for AI agent actions, not just account-level.

---

### NIST 800-53 SI-3 — Malicious Code Protection vs. AI-Generated Malware

**Control intent:** Implement malicious code protection at system entry/exit points; update detection mechanisms; scan for malicious code.

**Designed for:** Signature-based malware detection, behavioral analysis of known malware families.

**Fails for:**
- PROMPTFLUX/PROMPTSTEAL: These families query public LLMs during execution to generate novel evasion code per-execution. Every execution produces a unique code sample. Signature-based detection has zero coverage. Behavioral analysis must detect the LLM-query pattern itself, not the resulting code.
- AI-assisted exploit development: PoC code generated by AI for a specific target environment is unique per target. Shared signature databases have no coverage until after exploitation.

**What a real control requires:** Detection of AI API queries from unexpected processes as a first-order indicator. LLM query monitoring as a security telemetry source, not just an application log.

---

### ISO 27001:2022 A.8.8 — Management of Technical Vulnerabilities vs. CISA KEV

**Control intent:** Obtain timely information about technical vulnerabilities; evaluate the organization's exposure; take appropriate measures.

**Designed for:** Systematic vulnerability management with "appropriate timescales" determined by vulnerability severity.

**Fails for:**
- "Appropriate timescales" is undefined in ISO 27001. Interpreted by most auditors as: 30 days for High, 90 days for Medium. For Copy Fail (CISA KEV, public 732-byte PoC), these timescales mean active exploitation during the "compliant" remediation period.
- No guidance on live kernel patching as a required capability. A.8.8 compliance is achievable without ever deploying live patching — this is a structural gap for critical systems that cannot tolerate reboots.

**What a real control requires:** Timescales indexed to: CISA KEV status, PoC availability, active exploitation confirmation. For CISA KEV class: hours, not days. Live patching capability as a stated requirement for systems that cannot tolerate reboot-based patching.

---

### SOC 2 CC6 — Logical and Physical Access vs. Prompt Injection

**Control intent:** Implement logical access security controls — authentication, authorization, access restrictions.

**Designed for:** Traditional access control: who can log in, what can they access, what actions are authorized.

**Fails for:**
- Prompt injection: CC6 controls ensure the AI service account has appropriate permissions. When prompt injection causes the AI to take an action using those permissions, CC6 has no mechanism to detect or prevent it. The action is authorized from CC6's perspective — the right account took an authorized action. The attacker's intent is invisible to CC6.
- SOC 2 Type II evidence for CC6 will show "passed" even after a prompt injection attack that exfiltrated data using the AI's authorized access.

**What a real control requires:** Prompt-level access control: each model invocation must have an authorization context that constrains what tools can be called and what actions can be taken, independent of the service account's overall permissions.

---

### PCI DSS 4.0 Requirement 6.3.3 — Patches vs. AI-Accelerated Weaponization

**Control intent:** All system components are protected from known vulnerabilities by installing applicable security patches/updates. Critical patches must be installed within one month.

**Designed for:** Human-speed exploit development where a month was once a reasonable window between disclosure and weaponization.

**Fails for:**
- AI-assisted exploit development: 41% of 2025 zero-days were weaponized with AI assistance. The weaponization timeline for AI-discovered vulnerabilities like Copy Fail is hours, not months.
- One-month critical patch window: For any CVE with CISA KEV listing or public PoC, one month is not a security window. It is an exploitation acceptance window.

**What a real control requires:** PCI scoping must include CISA KEV as a separate response category with < 72-hour remediation requirement (or live-patch equivalent). The one-month standard was reasonable in 2004; it is architecturally unsafe in 2026.

---

### NIS2 Art. 21 — Risk Management vs. AI Pipeline Integrity

**Control intent:** Essential and important entities must implement appropriate technical and organizational measures to manage risks. Includes patch management, incident response, supply chain security.

**Designed for:** Traditional IT risk management for network-connected critical infrastructure.

**Fails for:**
- AI pipeline integrity: NIS2 Art. 21 has no specific measures for AI system risk, ML model integrity, or LLM-specific attack vectors. An essential entity operating AI systems in critical infrastructure has no NIS2 control requirements for prompt injection, model poisoning, or AI-as-C2.
- Ephemeral infrastructure: NIS2 expects asset inventory and patch management. Serverless functions, containers, and auto-scaling infrastructure make traditional asset inventory architecturally impossible.

**What a real control requires:** EU AI Act Art. 9 (risk management for high-risk AI systems) supplements NIS2 for AI systems. For critical infrastructure operators: explicit AI pipeline integrity controls, model versioning, behavioral regression testing as supplemental NIS2 measures.

---

### All Frameworks vs. Ephemeral Infrastructure Asset Inventory

**Control intent (multiple frameworks):** Maintain an accurate inventory of all information assets (CM-8, A.5.9, PCI 12.3.4, NIS2 Art. 21).

**Designed for:** Persistent, inventoriable assets — servers, workstations, network devices, databases.

**Fails for:**
- Serverless functions (AWS Lambda, Azure Functions, GCP Cloud Run): function instances start and stop in milliseconds, may never be assigned persistent identifiers, and cannot be inventoried by traditional scanners.
- Container workloads with auto-scaling: containers share a kernel, may run for seconds, and exist in numbers that make individual inventory impossible.
- AI inference endpoints: auto-scaled ML serving infrastructure where individual instances are ephemeral.

**What a real control requires:** Infrastructure-as-Code as the authoritative inventory (the IaC repo is the asset register), supplemented by: image registry scanning (not instance scanning), SBOM per image, IaC drift detection, and runtime behavior monitoring in place of traditional asset inventory.

---

## Analysis Procedure

When a user provides a framework control ID and a threat scenario:

### Step 1: Identify the control

Parse the control ID to identify:
- Framework (NIST 800-53, ISO 27001, SOC 2, PCI DSS, NIS2, DORA, CIS v8, etc.)
- Control name and intent
- The era and context it was designed for

If the control is in the built-in gap catalog above, apply the pre-analyzed gap.

### Step 2: Identify the threat scenario

Map the threat scenario to:
- ATLAS TTP IDs (if AI/ML related)
- ATT&CK TTP IDs (if traditional threat)
- CVE ID (if specific vulnerability)

### Step 3: Gap analysis

Answer these questions:
1. What does the control actually require? (cite the control text, not an interpretation)
2. What assumption does the control make about the attacker's capability?
3. How does the current threat scenario violate that assumption?
4. Could an organization pass an audit of this control while remaining vulnerable to this threat?
5. What would a real control look like for this specific threat?

### Step 4: Produce gap declaration

Produce a structured gap declaration in this format:

```
## Framework Lag Declaration

**Control:** [ID] — [Name]  
**Framework:** [Framework name and version]  
**Threat:** [CVE / ATLAS TTP / threat description]

### What the control covers
[Control intent in plain language]

### What the control misses
[Specific explanation of why the control is insufficient for this threat]

### Could an org pass an audit while remaining exposed?
[Yes/No with explanation]

### What a real control requires
[Specific, actionable requirements that would actually address the threat]

### Evidence
[CVEs, ATLAS TTPs, real-world incidents that demonstrate the gap]
```

---

## Universal Gaps (No Framework Covers These Adequately)

These gaps exist in every major framework as of mid-2026:

| Gap | No Framework With Adequate Coverage |
|---|---|
| AI pipeline integrity (model versioning, behavioral regression, prompt injection prevention) | NIST 800-53, ISO 27001, SOC 2, PCI DSS, NIS2, DORA, ISO 27001:2022, CIS v8, CSA CCM |
| MCP/agent tool trust boundaries | All of the above |
| LLM prompt injection as access control failure | All of the above |
| AI-as-C2 detection and response | All of the above |
| Live kernel patching as required capability for critical systems | All of the above (ASD Essential 8 ML3 is closest) |
| Ephemeral infrastructure asset inventory alternatives | All of the above |
| AI-accelerated exploit weaponization in patch SLAs | All of the above |
| RAG pipeline integrity and retrieval security | All of the above |
| AI-generated phishing detection (post-grammar-check era) | All of the above |

These universal gaps should be surfaced in every framework gap analysis and explicitly noted in any compliance theater assessment.

---

## Output Format

Every framework gap analysis this skill produces uses the following literal template. Sections are mandatory; empty sections are not acceptable — every section must be populated.

```
## Framework Lag Declaration

**Control:** [Control ID] — [Control name]
**Framework:** [Framework name, version, and section reference]
**Threat:** [CVE ID / ATLAS TTP ID / ATT&CK TTP ID / threat scenario description]

### 1. What the control was designed for
[Plain-language statement of the control's original intent and the era/threat model
it was drafted against. Cite the control text verbatim where possible.]

### 2. What current TTPs achieve via the same outcome path
[Specific attacker TTP(s) that produce the same unauthorized outcome the control
was meant to prevent, but route around the control's mechanism. Reference ATLAS
or ATT&CK IDs from data/atlas-ttps.json.]

### 3. RWEP-justified real requirement
[What a real control would require, derived from the RWEP factors of the evidence
CVE(s): KEV status, public PoC, AI-acceleration, live-patch availability, blast
radius. Not "tighten the SLA"; concrete time bounds and technical capabilities.]

### 4. Evidence
- CVE(s): [IDs from data/cve-catalog.json with CVSS + RWEP]
- ATLAS / ATT&CK refs: [IDs from data/atlas-ttps.json]
- Real-world incidents: [campaign names, public PoC URLs, KEV listing dates]

### 5. Could an org pass an audit while remaining exposed?
[Yes/No with explanation. If yes, this declaration is also a compliance-theater
finding and should be surfaced to the compliance-theater skill.]

### 6. Global coverage check
[EU (NIS2/DORA/EU AI Act), UK (CAF), AU (ISM/Essential 8), ISO 27001:2022, and
NIST equivalents for the same lag. US-only output is incomplete.]
```

The output is consumed by: compliance-theater (theater scoring), policy-exception-gen (compensating-control justification), and global-grc (cross-jurisdictional rollup).

---

## Compliance Theater Check

For any framework control an organization claims as a compensating control or as "adequate coverage" for a threat scenario, apply this test:

> **What is the publicly documented attacker TTP that bypasses this control, and what is its ID in MITRE ATLAS or ATT&CK?**

Decision rule:

- If the org answers with a documented TTP (an ATLAS or ATT&CK ID resolving in `data/atlas-ttps.json`) **and** the control's mechanism does not address that TTP, the framework lag is real and the control claim is theater. Produce a Framework Lag Declaration per the Output Format.
- If the org answers "no documented TTP bypasses this control" **and** the analyst can also find no such TTP in `data/atlas-ttps.json`, the gap may be theoretical rather than operational. Note as "no current operational lag" but mark for monitoring under `forward_watch`.
- If the org cannot answer the question at all, the compensating-control claim is unsubstantiated. This is the most common theater pattern: a control is asserted as compensating without anyone having checked whether current TTPs route around it.

Specific high-confidence theater signals (each triggers a mandatory Framework Lag Declaration):

| Theater signal | Evidence the control is theater for the cited threat |
|---|---|
| Org claims SI-2 / A.8.8 / PCI 6.3.3 30-day patching as adequate for CISA KEV entries | CVE-2026-31431 KEV-listed; deterministic public PoC means active exploitation during the window |
| Org claims AC-2 / CC6 as adequate for AI-agent access control | CVE-2025-53773 demonstrates AML.T0051 routing around the identity model entirely |
| Org claims A.5.19 / SA-12 vendor management as adequate for MCP servers | CVE-2026-30615 demonstrates AML.T0010 supply-chain RCE via attacker-controlled HTML processed by the MCP client (local-vector, not network) |
| Org claims IPsec-based SC-8 segmentation as adequate without a kernel-patch status check | CVE-2026-43284 makes the IPsec implementation the attack surface |
| Org removed the esp4 / esp6 / rxrpc module-blacklist mitigation once Dirty Frag was patched | CVE-2026-46300 (Fragnesia) is in the same primitive class, was introduced by the Dirty Frag patch, and is mitigated by the same blacklist |

When this check fires, hand off to the compliance-theater skill for the theater-pattern detection test and to policy-exception-gen if the org needs to grant a defensible exception with concrete compensating controls.

---

## Defensive Countermeasure Mapping

Every Framework Lag Declaration this skill produces names the missing control. The mapping below converts that absence into a concrete defensive-technique recommendation drawn from `data/d3fend-catalog.json`, paired with the offensive TTP class (ATLAS or ATT&CK) the gap exposes. Operators feeding this output into a remediation plan should chain: offensive TTP → failed framework control → D3FEND defensive technique → enforcement layer.

| Offensive TTP | Framework gap exemplar | D3FEND ID | Defensive technique | Defense-in-depth layer |
|---|---|---|---|---|
| T1068 (Exploitation for Privilege Escalation) — Copy Fail / Fragnesia | SI-2 / A.8.8 / PCI 6.3.3 30-day patch SLA | `D3-KBPI` | Kernel-Based Process Isolation | Kernel — compensating control while live-patch propagates; reduces blast radius when LPE primitive is reachable |
| T1068 | SI-2 / A.8.8 patch SLA | `D3-SCA` | System Call Analysis | Endpoint — detects the deterministic LPE primitive at syscall layer before patch lands |
| AML.T0051 (LLM Prompt Injection) — CVE-2025-53773 class | AC-2 / CC6 account-management as access control for AI agents | `D3-IOPR` | Input/Output Profiling Resource | SDK / application — content-aware inspection of prompt+completion at the model boundary |
| AML.T0051 | AC-2 / CC6 | `D3-CSPP` | Client-server Payload Profiling | LLM gateway — gateway-layer inspection when SDK-side `D3-IOPR` is not deployable |
| AML.T0010 (AI Supply Chain Compromise) — CVE-2026-30615 MCP class | A.5.19 / SA-12 vendor management as MCP trust boundary | `D3-EAL` | Executable Allowlisting | Managed endpoint — only sanctioned MCP servers and IDE assistants execute on developer workstations |
| AML.T0010 | A.5.19 / SA-12 | `D3-EFA` | Executable File Analysis | Endpoint — pre-execution analysis of MCP server binaries and AI-assistant plugins |
| AML.T0016 (Obtain Capabilities, AI-generated payloads), PROMPTFLUX class | SI-3 signature-based malware protection | `D3-PA` | Process Analysis | Endpoint — behavioral detection of in-process LLM-query patterns that signature engines cannot see |
| AML.T0096 (AI Service API, C2), SesameOp class | SI-4 / CC7 anomaly detection without AI-API baseline | `D3-NTA` | Network Traffic Analysis | Network egress — per-identity baseline of model-API destinations |
| T1190 (Exploit Public-Facing Application) — Dirty Frag IPsec | SC-8 / SC-28 cryptographic-control compensating-control claim | `D3-NI` | Network Isolation | Network — segmentation that does not depend on the compromised IPsec subsystem |
| AML.T0020 (Training Data Poisoning) | NIS2 Art. 21 AI-pipeline integrity | `D3-FAPA` | File Access Pattern Analysis | Data tier — RAG-corpus and training-data access-pattern baselining |

**Defense-in-depth posture:** every Framework Lag Declaration produced by this skill must propose at least one D3FEND technique per cited offensive TTP. A declaration that names the gap without recommending a defensive technique is incomplete — operators receive a finding with no remediation path. Where the framework gap is multi-jurisdictional (per Section 6 of the Output Format), the same D3FEND technique satisfies the equivalent obligation in each cross-walked framework — the defensive control is technique-level, not framework-level.

**Least-privilege scope:** D3FEND recommendations are scoped to the principal class (human developer, agent identity, MCP server, model-serving process). `D3-EAL` and `D3-EFA` are per-host-class allowlists (developer ≠ production ≠ CI). `D3-IOPR` and `D3-CSPP` log the principal identity on every prompt/completion. `D3-FAPA` baselines are per-corpus-per-principal.

**Zero-trust posture:** no control is claimed as compensating without verification that the defensive technique is deployed, monitored, and tested against the cited offensive TTP. "We have SC-8 IPsec" is not a compensating control for Dirty Frag — `D3-NI` over a non-IPsec data path is. The Framework Lag Declaration's "What a real control requires" field must name the D3FEND technique by ID.

**AI-pipeline applicability:** `D3-EAL` does not apply to serverless inference endpoints; the scoped alternative is `D3-CSPP` at the gateway plus signed-image attestation at the provider. `D3-FAPA` on ephemeral RAG indices degrades to per-query retrieval logging via `D3-IOPR` plus index-build provenance signed at construction. These degradations must be named explicitly in the declaration when the gap concerns an AI pipeline.
