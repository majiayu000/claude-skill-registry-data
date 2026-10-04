---
name: threat-model-currency
version: "1.0.0"
description: Score how current an org's threat model is against 2026 reality — 14-item checklist, currency percentage, prioritized update roadmap
triggers:
  - threat model currency
  - update threat model
  - threat model review
  - is our threat model current
  - threat model gap
  - threat intelligence gap
data_deps:
  - atlas-ttps.json
  - cve-catalog.json
  - global-frameworks.json
atlas_refs: []
attack_refs: []
framework_gaps: []
forward_watch:
  - New AI attack classes as ATLAS v6 publishes
  - Post-quantum adversary capability timeline
  - New CISA KEV entries in kernel/AI/supply chain categories
  - New MCP or agent protocol security disclosures
  - Emerging malware families using AI for evasion
last_threat_review: "2026-09-28"
discovery_mode: "standalone"  # operator-reached via `exceptd brief threat-model-currency` or `exceptd ask`; not chained into any playbook's direct.skill_chain by design
---

# Threat Model Currency Assessment

## Frontmatter Scope

The `atlas_refs`, `attack_refs`, and `framework_gaps` arrays are intentionally empty. This skill is a meta-assessment of *every* threat model — its job is to surface gaps against the full 14-class mid-2026 landscape that downstream skills enumerate. Pinning a fixed TTP or framework-gap subset here would understate the assessment's actual coverage (every ATLAS / ATT&CK ID and every framework gap any other skill maps becomes an in-scope currency check). The 14 threat classes are listed in the body; each one references the downstream skill that carries the authoritative TTP and framework-gap IDs.

## Purpose

Most organizational threat models were last substantially revised 2–4 years ago. They describe the threat landscape of 2021–2022: ransomware, supply chain (SolarWinds-era), cloud misconfiguration, credential phishing using template emails. This is not the 2026 threat landscape.

This skill produces a currency score and a specific update roadmap. Currency is measured against 14 threat classes that define the mid-2026 threat reality. Each unchecked item is a specific gap, not a generic "keep monitoring" recommendation.

---

## The 14 Threat Class Checklist

### Class 1: AI-Discovered Kernel Vulnerabilities

**2026 reality:** AI systems discovered Copy Fail (CVE-2026-31431) in approximately one hour. The vulnerability class — page-cache write primitives enabling deterministic LPE — had existed in every major Linux distribution since 2017. Human researchers did not find it in 9 years.

**Currency check questions:**
- Does the threat model include AI-accelerated vulnerability discovery as a threat actor capability?
- Does the threat model acknowledge that AI-discovered vulnerabilities may be weaponized faster than human-speed patch cycles?
- Does the patch management policy differentiate CISA KEV + public PoC from non-exploited High CVEs?

**If unchecked:** The threat model assumes human-speed exploit development. This assumption fails for Copy Fail class vulnerabilities.

**ATLAS/ATT&CK ref:** T1068 (Exploitation for Privilege Escalation)

---

### Class 2: Deterministic Kernel LPE (No Race Condition)

**2026 reality:** Copy Fail is deterministic. Previous privilege escalation class vulnerabilities (Dirty COW, etc.) had race conditions that introduced unreliability and noise. Copy Fail has none. A 732-byte script reliably escalates to root on every attempt.

**Currency check questions:**
- Does the threat model distinguish deterministic LPEs from probabilistic ones?
- Does the incident response plan treat a confirmed exploitation of a deterministic LPE as an immediate full-system compromise, not a "potential" compromise?

**If unchecked:** IR playbooks may underestimate the reliability and speed of privilege escalation on unpatched systems.

---

### Class 3: IPsec Subsystem Exploitation (Network Control Bypass)

**2026 reality:** Dirty Frag (CVE-2026-43284/43500) exploits the IPsec implementation itself. Fragnesia (CVE-2026-46300, disclosed 2026-05-13) is the sibling page-cache-corruption bug introduced by the Dirty Frag patch — same primitive class, same XFRM ESP-in-TCP code path, same `blacklist esp4 / esp6 / rxrpc` mitigation. Network segmentation controls that rely on IPsec cannot be claimed as compensating controls for unpatched systems. Threat intel decays in days, not quarters: Dirty Frag and Fragnesia landed two weeks apart in the same primitive class.

**Currency check questions:**
- Does the threat model include exploitation of cryptographic subsystems as a bypass for network isolation controls?
- Are IPsec-dependent network controls flagged for review when kernel CVEs affecting IPsec are published?
- Does the threat model treat a CVE patch as opening a soak window during which the pre-patch compensating controls remain active? (Fragnesia precedent — Dirty Frag patch introduced a sibling bug in the same primitive class.)

**If unchecked:** Network segmentation controls may be claimed as compensating controls when they are actually part of the attack surface. "Patch landed therefore safe" misses sibling-bug introductions.

---

### Class 4: Prompt Injection as Enterprise RCE

**2026 reality:** CVE-2025-53773 demonstrated prompt injection in a production developer tool (GitHub Copilot) coercing the agent into flipping `chat.tools.autoApprove: true` and converting subsequent tool calls into shell execution. CVSS 7.8 / AV:L (NVD-authoritative; the local-vector reflects developer-side IDE interaction, not network reach). This is not a research demo. It is a real CVE in a tool used by hundreds of millions of developers. Attack success rates against SOTA defenses exceed 85%.

**Currency check questions:**
- Does the threat model include prompt injection as an RCE vector (not just a chatbot annoyance)?
- Is prompt injection included in application threat models for any system with an LLM component?
- Are AI coding assistants in scope for the threat model?

**If unchecked:** Prompt injection is classified as a "trust and safety" issue, not a security control failure. The shipped CVE (CVSS 7.8 / AV:L) says otherwise.

---

### Class 5: MCP Supply Chain RCE

**2026 reality:** CVE-2026-30615 (Windsurf MCP) demonstrated local-vector RCE via the MCP tool ecosystem (CVSS 8.0 / AV:L — attacker controls HTML the client processes). 150M+ combined downloads across MCP-capable assistants. Every major AI coding assistant has the same architectural attack surface.

**Currency check questions:**
- Does the threat model include AI tool supply chain as an attack surface?
- Are MCP servers treated as third-party code with supply chain risk?
- Is developer workstation compromise via AI tool plugins in scope?

**If unchecked:** Supply chain threat model covers npm packages, Docker images, and cloud providers — but not AI tool plugins, which now have an equal or greater attack surface.

---

### Class 6: AI-Assisted Exploit Development (Attacker-Side)

**2026 reality:** 41% of 2025 zero-days involved AI-assisted reverse engineering on the attacker side. AI has compressed the weaponization timeline from weeks to hours for a significant class of vulnerabilities.

**Currency check questions:**
- Does the threat model account for AI-compressed exploit development timelines?
- Do patch SLAs reflect that "critical patch in 30 days" is now an exploitation window, not a safety window?
- Is AI-assisted vulnerability research by threat actors included in the threat actor capability section?

**If unchecked:** Risk assessments assume historical exploit development timelines. These timelines are broken.

---

### Class 7: AI as Covert C2 (SesameOp Pattern)

**2026 reality:** Adversaries are using legitimate AI API endpoints as covert C2 channels (ATLAS AML.T0096). Traffic is indistinguishable from legitimate AI usage. Traditional C2 detection (DGA, beaconing, protocol anomalies) has zero coverage.

**Currency check questions:**
- Does the threat model include AI APIs as potential C2 channels?
- Is AI API behavioral monitoring included in the detection architecture?
- Is there a detection control that would fire for a SesameOp-style C2 pattern?

**If unchecked:** The C2 detection architecture has a complete blind spot for a confirmed, documented threat technique.

---

### Class 8: AI-Generated Malware Evasion (PROMPTFLUX Pattern)

**2026 reality:** PROMPTFLUX queries public LLMs in real-time to generate novel evasion code. Every execution produces a unique sample. Signature-based detection has zero coverage.

**Currency check questions:**
- Does the threat model include AI-generated dynamic malware evasion?
- Does the detection architecture go beyond signature matching for malware detection?
- Is behavioral detection the primary malware detection mechanism?

**If unchecked:** Malware detection architecture is primarily signature-based. For PROMPTFLUX class, signature-based detection is bypassed by design.

---

### Class 9: RAG Data Exfiltration

**2026 reality:** Attackers can manipulate vector embeddings to force RAG retrieval mechanisms to surface and exfiltrate proprietary data. No framework covers this. Organizations deploying RAG for sensitive data have zero control guidance.

**Currency check questions:**
- Does the threat model include RAG pipeline attacks if the organization uses RAG?
- Are vector stores classified as sensitive data assets requiring access controls?
- Is retrieval behavior monitored for anomalous patterns?

**If unchecked:** RAG systems are deployed with the same security model as traditional databases (perimeter + access control), which doesn't account for semantic retrieval attacks.

---

### Class 10: Model Poisoning of Decision Systems

**2026 reality:** Training pipeline targeting has moved to biasing ML models used in decision systems (logistics, classification, fraud detection). The attack is subtle — the model performs normally on most inputs but produces adversary-favorable decisions on specific inputs.

**Currency check questions:**
- Does the threat model include model poisoning for any ML system used in consequential decisions?
- Is model integrity verification (behavioral testing, output monitoring) in place?
- Is the ML training pipeline in scope for supply chain security?

**If unchecked:** ML decision systems are treated as software (covered by standard SDLC security) without accounting for ML-specific attacks on model behavior.

---

### Class 11: AI-Speed Reconnaissance

**2026 reality:** AI-assisted reconnaissance is observed at 36,000 probes per second per campaign. Rate-based detection thresholds set for human-speed reconnaissance (hundreds to low thousands of probes per second) don't fire until significant intelligence has already been gathered.

**Currency check questions:**
- Do network monitoring thresholds account for AI-speed reconnaissance rates?
- Is asset exposure to the internet minimized given the AI-speed enumeration baseline?
- Are external attack surface management tools in place?

**If unchecked:** Reconnaissance detection thresholds allow complete infrastructure mapping before an alert fires.

---

### Class 12: AI-Generated Credential Phishing

**2026 reality:** 82.6% of phishing emails contain AI-generated content. AI-generated phishing is indistinguishable from legitimate emails by grammar/style analysis. Credential theft via AI-assisted phishing increased 160% in 2025.

**Currency check questions:**
- Does the threat model reflect AI-generated phishing as the baseline phishing capability (not an advanced technique)?
- Are phishing detection controls updated for AI-generated content?
- Is MFA phishing-resistant (passkeys/hardware keys)? SMS/TOTP remains vulnerable to real-time AI-assisted phishing.

**If unchecked:** Phishing threat model is built on detection of human-generated templates. 82.6% of actual phishing bypasses these detectors.

---

### Class 13: MITRE ATLAS v2026.09 Coverage

**2026 reality:** MITRE ATLAS (September 2026, v2026.09) is the primary AI threat framework. Most SOC detection engineering programs are built on ATT&CK, not ATLAS. AI-specific TTPs have zero detection coverage in ATT&CK-only programs.

**Currency check questions:**
- Is MITRE ATLAS v2026.09 incorporated into the threat model?
- Are ATLAS TTPs mapped to detection controls?
- What is the current ATLAS version in use? (Current: 2026.09, September 2026)

**If unchecked:** AI-specific threat techniques are not covered by the detection architecture. The SOC has no alerts for ATLAS TTPs.

---

### Class 14: Post-Quantum Adversary Timeline

**2026 reality:** NIST has standardized ML-KEM (FIPS 203), ML-DSA (FIPS 204), and SLH-DSA (FIPS 205). CISA and NSA have recommended PQC migration timelines. Harvest-now-decrypt-later attacks against encrypted traffic are ongoing. The "decrypt later" timeline is shortening.

**Currency check questions:**
- Does the threat model include quantum adversary capability timelines?
- Is there a PQC migration roadmap?
- Are long-lived sensitive communications (data with > 10-year sensitivity requirement) protected with post-quantum cryptography?

**If unchecked:** Adversaries conducting harvest-now-decrypt-later operations against sensitive traffic are not in the threat model.

---

## Threat Context

Most organizational threat models in circulation today are 2022–2024 vintage. They were written before the operational reality of mid-2026:

- **AI-discovered LPEs.** Copy Fail (CVE-2026-31431) was found by an AI system in roughly one hour in a code path that had been in every major Linux distribution for nine years. A threat model that does not name "AI-assisted vulnerability discovery" as an attacker capability cannot reason about Copy Fail-class exposure.
- **Local-vector MCP RCE.** CVE-2026-30615 (Windsurf, CVSS 8.0 / AV:L) demonstrated that a malicious MCP server can drive an AI coding assistant to execute code in the developer's user context once installed. 150M+ combined downloads of MCP-capable assistants share the same architectural surface. A threat model that lists "third-party software" but not "AI tool plugins" is no longer comprehensive.
- **AI-API C2 (SesameOp).** Adversaries are using legitimate AI API endpoints (ATLAS AML.T0096) as covert command-and-control channels. Traffic is indistinguishable from legitimate usage at the network layer. A threat model whose C2 chapter still lists only DGAs, beaconing, and protocol anomalies has a documented blind spot.
- **AI-accelerated weaponization.** 41% of 2025 zero-days involved AI-assisted reverse engineering on the attacker side. The window between disclosure and reliable exploitation has compressed from weeks to hours for a meaningful class of CVEs.
- **AI-generated phishing as baseline.** 82.6% of phishing in 2025 contained AI-generated content. Threat models that treat AI-generated phishing as an "emerging" or "advanced" capability are scoring below the actual median attacker.

Currency is the gap. The threat-model document is rarely "wrong" — it is usually correct *for 2022*. This skill measures the delta.

---

## Framework Lag Declaration

No major risk-assessment or threat-intelligence framework defines a currency metric or mandates a refresh cadence indexed to current TTPs. The gap is global, not US-specific.

| Framework | Control | What it misses |
|---|---|---|
| NIST | SP 800-30 Rev. 1 (Guide for Conducting Risk Assessments) | Process-only. Requires identifying threats, vulnerabilities, likelihood, impact — defines no metric for the *currency* of the threat catalog used. A 2022 threat model can be SP 800-30-compliant in 2026. |
| NIST | SP 800-39 / SP 800-37 (Risk Management Framework) | Mandates ongoing risk assessment but not threat-model refresh cycles tied to KEV/ATLAS updates. |
| NIST | AI RMF MAP-2.1 | Requires categorising AI-system risks; does not require the categorisation be re-run when new ATLAS TTPs publish. |
| ISO | 27005:2022 (Information security risk management) | Same shape as SP 800-30 — process guidance with no currency requirement. |
| ISO | 27001:2022 A.5.7 (Threat intelligence) | Requires collection and analysis of threat intelligence. Defines no recency requirement, no metric for "current", no test that distinguishes current threat intel from a 2022 PDF on a shelf. |
| EU | NIS2 Art. 21(2)(a) (Risk analysis and information system security policies) | Mandates risk analysis as a measure; is silent on threat-model age or refresh trigger. National competent authorities have not (mid-2026) issued binding guidance on threat-model currency. |
| EU | DORA Art. 6 (ICT risk management framework) | Requires identification of ICT risks "on an ongoing basis"; "ongoing" is undefined and unmetered. |
| EU | EU AI Act Art. 9 (Risk Management System for high-risk AI) | Mandates "continuous iterative" risk management; provides no currency test, no mapping to ATLAS, no required refresh trigger. |
| UK | NCSC CAF Principle A2 (Risk Management) | Principle-based, leaves currency to the assessor. No threat-class checklist, no minimum refresh cadence. |
| AU | ISM-1238 and ISM-2039 | Require threat modelling in the software development life cycle, and a review that keeps the model current with the as-built software and the threat environment. Neither sets a review cadence, and neither applies to threat models outside software development. |
| Global | COSO ERM / ISO 31000 | Enterprise risk frameworks treat cyber as one risk category; no operational threat-currency requirement. |

The recurring failure across all of the above: every framework treats threat modelling as a process to perform, not a knowledge artefact to keep fresh against external TTP catalogs. The 14-class checklist in this skill is the missing currency metric.

---

## TTP Mapping

The 14-class checklist above *is* the TTP map. Each class is a coverage requirement against the canonical sources of truth: `data/atlas-ttps.json` (MITRE ATLAS v2026.09) and the ATT&CK techniques referenced in `data/cve-catalog.json`. A current threat model must address — explicitly or by reasoned exclusion — every TTP below.

| Class | Primary TTP | Catalog source | Gap if absent |
|---|---|---|---|
| 1 — AI-discovered kernel LPE | T1068 (Exploitation for Privilege Escalation) | cve-catalog.json: CVE-2026-31431 | Threat model assumes human-speed exploit discovery |
| 2 — Deterministic LPE | T1068 | cve-catalog.json: CVE-2026-31431 | IR plan treats LPE as probabilistic |
| 3 — IPsec subsystem LPE | T1068 | cve-catalog.json: CVE-2026-43284 / CVE-2026-43500 / CVE-2026-46300 | Network-segmentation claimed as compensating control for the attack surface itself; patch-landed-therefore-safe assumes patches close bug families (Fragnesia disproved this in days) |
| 4 — Prompt injection RCE | AML.T0051 (LLM Prompt Injection), AML.T0054 (LLM Jailbreak) | atlas-ttps.json + CVE-2025-53773 | Prompt injection treated as T&S, not security |
| 5 — MCP supply chain RCE | AML.T0010 (AI Supply Chain Compromise), T1190 (Exploit Public-Facing Application) | atlas-ttps.json + CVE-2026-30615 | AI plugin ecosystem out of supply-chain scope |
| 6 — AI-assisted weaponization | AML.T0017 (Develop Capabilities) | atlas-ttps.json | Patch SLAs sized for 2019 attacker speed |
| 7 — AI as covert C2 | AML.T0096 (AI Service API, C2) | atlas-ttps.json | C2 detection architecture has total blind spot |
| 8 — AI-generated malware evasion | AML.T0016 (Obtain Capabilities, payload generation) | atlas-ttps.json | Detection stack signature-bound; PROMPTFLUX bypasses by design |
| 9 — RAG exfiltration | AML.T0043 (Craft Adversarial Data) | atlas-ttps.json | Vector store treated as database, not as semantic exfil surface |
| 10 — Model poisoning | AML.T0020 (Training Data Poisoning) | atlas-ttps.json | ML decision systems treated as standard software |
| 11 — AI-speed reconnaissance | T1595 (Active Scanning), T1190 | ATT&CK | Rate-based detection thresholds calibrated for human-speed scans |
| 12 — AI-generated phishing | AML.T0016 (Obtain Capabilities, payload crafting via public AI APIs), T1566 (Phishing) | atlas-ttps.json + ATT&CK | Detection rules tuned for 2021 phishing |
| 13 — ATLAS coverage | All AML.T* in atlas-ttps.json | atlas-ttps.json `_meta.atlas_version` | SOC detection programs are ATT&CK-only |
| 14 — Post-quantum adversary | T1557 (harvest-now-decrypt-later context) | global-frameworks.json (PQC standards) | Long-lived sensitive traffic captured today, decrypted later |

The truth set: every `AML.T*` key in `data/atlas-ttps.json` (excluding `_meta`) and every `attack_refs` entry across every CVE in `data/cve-catalog.json`. A threat model that does not address each, or document a reasoned exclusion for each, is non-current by construction.

---

## Exploit Availability Matrix

A threat model is "current" only if it accounts for every `data/cve-catalog.json` entry with RWEP >= 50 — with either a deployed mitigation or a documented, accepted residual risk. As of the frontmatter `last_threat_review`:

| CVE | Name | CVSS | RWEP | KEV | PoC | AI factor | Live-patchable | Required threat-model treatment |
|---|---|---|---|---|---|---|---|---|
| CVE-2026-31431 | Copy Fail | 7.8 | 90 | Yes (2026-05-01, due 2026-05-15) | Yes — 732-byte deterministic | AI-discovered | Yes (kpatch / canonical-livepatch / kGraft) | Must name as named threat. Patch SLA must reflect KEV + deterministic class — live-patch within hours, not 30 days. |
| CVE-2025-53773 | Copilot YOLO-mode RCE | 7.8 | 30 | No | Yes — demonstrated | AI-weaponized | Yes (SaaS vendor patch / IDE update) | Must include prompt-injection-driven YOLO-mode escalation as RCE vector if any developer uses Copilot. |
| CVE-2026-30615 | Windsurf MCP local-vector RCE | 8.0 | 35 | No | Yes | No | Yes (IDE update) | Must include MCP supply chain if any developer uses any MCP-capable assistant. |
| CVE-2026-43284 | Dirty Frag (ESP/IPsec) | 8.8 | 53 | No | Yes — chain component | AI-assisted discovery | No | Required if IPsec-based controls are claimed as compensating. |
| CVE-2026-43500 | Dirty Frag (RxRPC) | 7.6 | 47 | No | Yes — chain component | AI-assisted discovery | No | Required when chained with CVE-2026-43284 in IR scenario planning. |
| CVE-2026-46300 | Fragnesia | 7.8 | 35 (60 if KEV-listed) | No (candidate) | Yes — one-liner vs /usr/bin/su | AI-assisted discovery (Zellic's agentic auditing tool) | Yes (kpatch / canonical-livepatch / KernelCare) | Required when the threat model claims patches close bug families — Fragnesia is the sibling bug introduced by the Dirty Frag patch; the same `blacklist esp4 / esp6 / rxrpc` mitigation covers both. Treat as the canonical "today" example of threat-intel decay measured in days, not quarters. |

The hard rule for currency scoring: every CVE in the catalog with RWEP >= 50 (query `data/cve-catalog.json` for the current set) must appear in the threat model under its named threat or its CVE ID. RWEP 40–49 entries should appear if the org uses the affected technology. Sub-40 entries appear by exception.

Run `node lib/scoring.js` to recompute RWEP if `data/cve-catalog.json` has been updated since `last_threat_review`.

---

## Compliance Theater Check

Apply this single test to any "yes, we have a threat model" claim:

> "What was the publish or last-revision date of the version of the threat model that is currently authoritative inside your organisation? Now list every CISA KEV addition since that date that affects any technology in your stack (Linux kernel, AI coding assistants, MCP servers, identity providers, edge appliances). For each, point to the line in the threat model that addresses it, or the dated risk-acceptance memo. If the answer is 'we'll update it at next review' and the next review is more than 30 days out, the threat model is a compliance artefact, not an operational document. The control is documented; it is not operational."

A complementary test for AI surfaces:

> "Open `data/atlas-ttps.json`. Pick any three `AML.T*` IDs at random. For each, show where in your threat model the technique is named or where the equivalent attack is described. If the threat model has zero ATLAS IDs and the org operates any LLM-integrated system, the AI section is theater — the document predates the threat catalog that defines AI threats."

A complementary test for global orgs:

> "Your org is subject to DORA (4h initial incident notification). When did your threat model last refresh its incident-classification taxonomy against DORA's RTS on classification of major ICT-related incidents? If the answer is 'before January 2025', the threat model cannot drive DORA-compliant classification decisions — by definition, the taxonomy predates the regulation."

---

## Scoring

For each class, score:
- **2 points:** Explicitly addressed in threat model with specific controls
- **1 point:** Mentioned in threat model but without specific controls
- **0 points:** Not addressed

**Total: 28 points maximum**

| Score | Currency Rating |
|---|---|
| 25–28 | Current (≥ 89%) |
| 20–24 | Mostly current — 2–3 gaps |
| 14–19 | Partially current — systematic AI/modern threat gaps |
| 7–13 | Significantly stale — 2022 threat model |
| 0–6 | Critically stale — 2019-era threat model |

---

## Analysis Procedure

### Step 1: Obtain the current threat model

Request or locate:
- Most recent threat model document
- Date of last substantive update (not just cosmetic/formatting)
- Which threat actors are in scope
- Which attack classes are documented

### Step 2: Score each of the 14 classes

For each class:
1. Is it explicitly in the threat model? If yes, with specific controls?
2. Score 0/1/2

### Step 3: Identify top gaps

Prioritize unchecked classes by RWEP impact:
1. Classes where a real, exploited CVE (Copy Fail, Windsurf MCP) means current exposure
2. Classes where detection architecture has zero coverage (AI C2, PROMPTFLUX)
3. Classes that affect future risk posture (PQC, AI reconnaissance speed)

### Step 4: Generate update roadmap

For each gap, produce a specific, actionable update:
- What text to add to the threat model
- What ATLAS/ATT&CK TTP to reference
- What control to add or update

---

## Output Format

The skill produces a structured Threat Model Currency Assessment that scores the threat model against each of the 14 threat classes, computes a currency percentage, and emits a priority update roadmap. The shape below is consumed downstream by `framework-gap-analysis` (which converts per-class gaps into Framework Lag Declarations), by `policy-exception-gen` (which generates defensible exceptions for any class the operator cannot remediate immediately), and by `global-grc` (which rolls up the currency score across EU/UK/AU/ISO jurisdictions for global-first coverage). Preserve the per-class scoring rows verbatim — they are the auditable derivation of the currency percentage.

```
## Threat Model Currency Assessment

**Date:** YYYY-MM-DD
**Threat Model Version:** [document version / last update date]

### Currency Score: [X / 28] = [percentage]%
**Rating:** [Current / Mostly current / Partially current / Significantly stale / Critically stale]

### Class-by-Class Scoring
| # | Threat Class | Score | Finding |
|---|---|---|---|
| 1 | AI-Discovered Kernel Vulnerabilities | 0/1/2 | [specific gap or confirmation] |
| 2 | Deterministic Kernel LPE | 0/1/2 | |
| 3 | IPsec Subsystem Exploitation | 0/1/2 | |
| 4 | Prompt Injection as Enterprise RCE | 0/1/2 | |
| 5 | MCP Supply Chain RCE | 0/1/2 | |
| 6 | AI-Assisted Exploit Development | 0/1/2 | |
| 7 | AI as Covert C2 | 0/1/2 | |
| 8 | AI-Generated Malware Evasion | 0/1/2 | |
| 9 | RAG Data Exfiltration | 0/1/2 | |
| 10 | Model Poisoning | 0/1/2 | |
| 11 | AI-Speed Reconnaissance | 0/1/2 | |
| 12 | AI-Generated Credential Phishing | 0/1/2 | |
| 13 | MITRE ATLAS v2026.09 Coverage | 0/1/2 | |
| 14 | Post-Quantum Adversary Timeline | 0/1/2 | |

### Priority Update Roadmap
[Ordered by current exposure risk: specific additions for each gap]

### ATLAS Version Check
Current reference: MITRE ATLAS v2026.09 (September 2026)
Threat model references: [version cited in document]
Gap: [if different]
```

---

## Defensive Countermeasure Mapping

A threat model is current only when each of the 14 threat classes above has a named defensive control. The mapping below converts each class to the D3FEND defensive technique that disrupts its offensive TTP. A currency assessment that scores a class as "addressed" without naming the corresponding D3FEND technique is under-specified — the threat model identifies the threat but does not commit to a defence.

| Class | Offensive TTP | D3FEND ID | Defensive technique | Defense-in-depth layer |
|---|---|---|---|---|
| 1 — AI-discovered kernel LPE (Copy Fail) | T1068 | `D3-KBPI` | Kernel-Based Process Isolation | Kernel — compensating control during the AI-compressed weaponization window |
| 2 — Deterministic LPE | T1068 | `D3-SCA` | System Call Analysis | Endpoint — detect the deterministic primitive at syscall layer |
| 3 — IPsec subsystem LPE (Dirty Frag / Fragnesia) | T1190 | `D3-NI` | Network Isolation (non-IPsec data path) | Network — segmentation independent of the compromised cryptographic subsystem |
| 4 — Prompt injection RCE | AML.T0051, AML.T0054 | `D3-IOPR` | Input/Output Profiling | SDK / application — content-aware prompt+completion inspection |
| 4 — Prompt injection RCE (gateway tier) | AML.T0051 | `D3-CSPP` | Client-server Payload Profiling | LLM gateway — when SDK-side instrumentation is not deployable |
| 5 — MCP supply chain RCE | AML.T0010 | `D3-EAL` | Executable Allowlisting | Managed endpoint — only sanctioned MCP servers and IDE assistants execute |
| 5 — MCP supply chain RCE | AML.T0010 | `D3-EFA` | Executable File Analysis | Endpoint — pre-execution analysis of MCP-server binaries |
| 6 — AI-assisted weaponization | AML.T0017 | `D3-NTA` | Network Traffic Analysis | Network egress — detect attacker-side AI-API queries from compromised tooling |
| 7 — AI as covert C2 (SesameOp) | AML.T0096 | `D3-NTA` | Network Traffic Analysis | Network egress — per-identity baseline of model-API destinations |
| 8 — AI-generated malware evasion (PROMPTFLUX) | AML.T0016 | `D3-PA` | Process Analysis | Endpoint — behavioral detection of in-process LLM-query patterns |
| 9 — RAG exfiltration | AML.T0043 | `D3-FAPA` | File Access Pattern Analysis | Data tier — RAG-corpus retrieval-pattern baselining |
| 10 — Model poisoning | AML.T0020 | `D3-FAPA` | File Access Pattern Analysis | Data tier — training-corpus access-pattern baselining |
| 11 — AI-speed reconnaissance | T1595 | `D3-NTA` | Network Traffic Analysis | Network ingress — recalibrated thresholds for AI-speed probe rates |
| 12 — AI-generated phishing | T1566, AML.T0016 | `D3-MFA` | Multi-factor Authentication (passkey class) | Identity — remove the credential-disclosure win condition AI phishing optimizes for |
| 12 — AI-generated phishing (gateway tier) | T1566 | `D3-CSPP` | Client-server Payload Profiling | Email gateway — stylometric drift detection for LLM-generated lures |
| 13 — ATLAS coverage | All AML.T* | `D3-IOPR` + `D3-NTA` | Input/Output Profiling + Network Traffic Analysis | SDK + network — the two-layer minimum for AI TTP detection |
| 14 — Post-quantum adversary | T1557 (harvest-now-decrypt-later) | `D3-MENCR` | Message Encryption (PQC-hybrid TLS) | Network — ML-KEM / X25519 hybrid key agreement for long-lived sensitive traffic |

**Defense-in-depth posture:** the 14-class currency score (per the Scoring section above) is upgraded from "addressed" to "operationally addressed" only when each class names at least one deployed D3FEND technique from the table. A threat model that scores 28/28 on knowledge of threats but cites zero D3FEND techniques is paper-current — the document is updated, the defence is not.

**Least-privilege scope:** the D3FEND techniques in this table are technique-level; their per-principal scoping is owned by the downstream skill cited in each class (e.g. `ai-attack-surface` owns `D3-IOPR` scoping for AI principals, `kernel-lpe-triage` owns `D3-KBPI` scoping for kernel-class assets). The threat-model currency assessment cites the technique by ID; the scoping document lives in the downstream skill.

**Zero-trust posture:** every class above is verified in production before the currency score credits it. A class scored as "addressed" with a D3FEND technique that is policy-approved but not deployed, or deployed but not monitored, or monitored but not tested against the cited TTP, is over-credited. The Priority Update Roadmap field (per the Output Format) must list verification tests alongside the technique deployment plan.

**AI-pipeline applicability:** Classes 4, 5, 7, 8, 9, 10, 11, 12, 13 are AI-pipeline-applicable. `D3-EAL` does not apply to serverless inference endpoints; the scoped alternative is `D3-CSPP` at the gateway plus signed-image attestation at the provider. `D3-FAPA` on ephemeral RAG indices degrades to per-query retrieval logging via `D3-IOPR` plus index-build provenance signed at construction. The currency assessment must record these degradations explicitly when scoring AI-pipeline classes.
