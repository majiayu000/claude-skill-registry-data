---
name: ai-risk-management
version: "1.0.0"
description: AI governance and risk management for mid-2026 — ISO/IEC 23894 risk process, ISO/IEC 42001 management system, NIST AI RMF, EU AI Act high-risk obligations, AI impact assessments, AI red-team programs, AI incident lifecycle
triggers:
  - ai risk management
  - ai governance
  - ai impact assessment
  - aia
  - dpia ai
  - iso 23894
  - iso 42001
  - nist ai rmf
  - ai red team program
  - ai incident response
  - eu ai act high-risk
  - ai vendor risk
  - ai management system
data_deps:
  - atlas-ttps.json
  - cve-catalog.json
  - cwe-catalog.json
  - d3fend-catalog.json
  - exploit-availability.json
  - framework-control-gaps.json
  - global-frameworks.json
  - zeroday-lessons.json
atlas_refs:
  - AML.T0051
  - AML.T0096
  - AML.T0017
  - AML.T0013
attack_refs: []
framework_gaps:
  - ISO-IEC-42001-2023-clause-6.1.2
  - ISO-IEC-23894-2023-clause-7
  - NIST-AI-RMF-MEASURE-2.5
  - OWASP-LLM-Top-10-2025-LLM01
  - EU-AI-Act-Art-15
  - UK-CAF-A1
  - AU-Essential-8-App-Hardening
rfc_refs: []
cwe_refs:
  - CWE-1426
  - CWE-1039
d3fend_refs:
  - D3-IOPR
last_threat_review: "2026-05-15"
discovery_mode: "standalone"  # operator-reached via `exceptd brief ai-risk-management` or `exceptd ask`; not chained into any playbook's direct.skill_chain by design
---

# AI Risk Management (Governance Layer)

## Purpose

This is the governance-layer companion to `ai-attack-surface` (technical surface) and `threat-modeling-methodology` (methodology-agnostic). Where those skills tell you what the attacker can do and how to enumerate the threat, this skill tells you what programme structure must exist around AI use so that the enumerated threats are owned, treated, monitored, and re-assessed. It operationalises ISO/IEC 23894:2023, ISO/IEC 42001:2023, NIST AI RMF 1.0, and the EU AI Act high-risk obligations into a concrete set of artefacts and procedures.

This skill does not produce a technical control list — `defensive-countermeasure-mapping` does that. It produces the governance scaffolding without which technical controls are unowned, unmaintained, and unauditable.

---

## Threat Context (mid-2026)

AI governance moved from voluntary to mandatory between 2024 and 2026. The transition has three concrete dates that anchor the current state of the practice:

- **2023-08-22** — ISO/IEC 42001:2023 published as the first international standard for an AI Management System (AIMS). Certification bodies began offering accredited certification through 2024–2025; by Q2 2026 it is the de facto certification target for any organisation that builds or deploys AI at scale.
- **2023-12-15** — ISO/IEC 23894:2023 published, providing the AI risk management process that 42001 operationalises. The two standards are designed as a pair: 23894 is the *process*, 42001 is the *management system that runs the process*.
- **2024-08-01** to **2026-08-02** — EU AI Act (Regulation 2024/1689) staged entry into force. Prohibited-AI provisions effective 2025-02-02; GPAI obligations effective 2025-08-02; **high-risk AI system obligations under Art. 9 (risk management system), Art. 10 (data governance), Art. 12 (logging), Art. 14 (human oversight), and Art. 15 (accuracy, robustness, cybersecurity) become fully enforceable on 2026-08-02** — less than three months from the date stamped at the top of this skill.

The gap on the ground is severe and the same in every jurisdiction the maintainers have spot-checked through Q2 2026: most organisations deploying LLMs, agents, RAG pipelines, and AI-augmented developer tooling have **zero governance artefact specific to AI**. They assume general security policies, the existing risk register, the existing vendor management programme, and the existing incident response playbook cover AI by inheritance. They do not. Concretely:

- The risk register has no entry for prompt injection (AML.T0051), AI-as-C2 (AML.T0096), or AI-assisted exploit development against the organisation (AML.T0017).
- The vendor management programme treats AI providers as ordinary SaaS suppliers and accepts a SOC 2 Type II as evidence of AI-specific control adequacy — even though SOC 2 has no AI-specific criteria.
- The incident response playbook does not enumerate AI-specific incident classes (model exfiltration, training-data poisoning, agent compromise via MCP server, RAG corpus contamination, AI vendor breach affecting derived embeddings).
- The data inventory does not include vector embedding stores, model weights, or LLM prompt/response logs as classified data assets.
- There is no AI inventory. The organisation cannot list every model, API, agent, and MCP server it operates.

AI red-team activity has likewise shifted from voluntary research practice to governance obligation:

- EU AI Act Art. 72 mandates adversarial testing of GPAI models with systemic risk.
- NIST AI RMF MEASURE 2.5 expects organisations to assess AI risks during operation (`data/framework-control-gaps.json` → `NIST-AI-RMF-MEASURE-2.5`).
- OWASP LLM Top 10 2025 (LLM01: Prompt Injection — `data/framework-control-gaps.json` → `OWASP-LLM-Top-10-2025-LLM01`) is treated by auditors as the working operational checklist where ISO/IEC 42001 is silent on technical specifics.

The 2024–2026 disclosure record is unforgiving: vendor advisories from OpenAI, Anthropic, Google DeepMind, and Microsoft have published AI vulnerability disclosures spanning prompt-injection-driven RCE (CVE-2025-53773, CVSS 7.8 / AV:L), local-vector MCP supply-chain RCE (CVE-2026-30615, CVSS 8.0 / AV:L), agentic-pipeline compromise patterns, and indirect-injection via retrieved content. An organisation with no governance artefact mapping these classes to internal use cases is not in a position to act on any of them.

AI as adversary is now operational reality, not forecast: 41% of 2025 zero-days were AI-discovered (GTIG 2025 annual), the first documented AI-built in-the-wild zero-day surfaced 2026-05-11 (GTIG AI 2FA-bypass case), and Fragnesia (CVE-2026-46300, 2026-05-13) is the anchor case for autonomous agentic-AI discovery in load-bearing OSS — Zellic's agentic auditor surfaced an 18-year-old Linux kernel page-cache primitive. Risk registers, vendor questionnaires, and incident playbooks that omit AI-as-discovery-actor are out of currency. Align the AIMS to **CTID Secure AI v2 (2026-05-06)** — Secure AI v1 is superseded; Annex SL clause-by-clause mapping in `data/framework-control-gaps.json`.

---

## Framework Lag Declaration

AI governance lag is global and asymmetric. Regulatory expectation outruns operational capability everywhere except Israel and (provisionally) the EU. The comparison is global-first: it spans EU, UK, AU, JP, IL, ID, and US-state (NYDFS) frameworks alongside ISO and NIST.

| Jurisdiction | Framework | Control / Article | What it misses for AI governance |
|---|---|---|---|
| Global | ISO | ISO/IEC 42001:2023 clause 6.1.2 (AI risk treatment) — gap key `ISO-IEC-42001-2023-clause-6.1.2` | Mandates an AIMS but is **process-focused**. Specifies neither prompt-injection-resistant context boundaries, nor MCP server trust posture, nor AI-as-C2 detection. Certification is achievable without any of these technical controls. |
| Global | ISO | ISO/IEC 23894:2023 clause 7 (AI risk management process) — gap key `ISO-IEC-23894-2023-clause-7` | Details a generic risk-management process for AI; does not enumerate AI-specific threat classes, does not bind to ATLAS, does not require an AI red-team cadence. |
| US | NIST | AI RMF 1.0 — MEASURE 2.5 — gap key `NIST-AI-RMF-MEASURE-2.5` | "Measure AI risks and impacts" is a function; provides no schedule, no minimum test set, no requirement to map findings to ATLAS or to a defensive-countermeasure catalogue. NIST AI RMF MAP-3.1 (categorisation) is similarly process-only. |
| Global | OWASP | LLM Top 10 (2025) — LLM01 Prompt Injection — gap key `OWASP-LLM-Top-10-2025-LLM01` | Operational checklist treated by auditors as a substitute for binding control language. Helpful for engineers, not legally binding, and does not address ISO/IEC 42001 management-system obligations. |
| EU | EU AI Office | EU AI Act (Regulation 2024/1689) Art. 9 (Risk Management System, high-risk AI) | Mandatory **continuous iterative** RMS for high-risk AI systems from 2026-08-02. Silent on internal-use AI tooling (Copilot-for-office-workers, internal coding assistants) where staff productivity AI doubles as data exfiltration surface. |
| EU | EU AI Office | EU AI Act Art. 15 (accuracy, robustness, cybersecurity) | "Cybersecurity" requirement for high-risk AI is undefined at the technical level. Prompt injection not addressed in Art. 15 or implementing measures (per `data/global-frameworks.json` → EU.EU_AI_ACT.framework_gaps). |
| EU | EU AI Office | EU AI Act Art. 72 (GPAI adversarial testing) | Adversarial testing required for GPAI with systemic risk; no specification of test methodology, no required ATLAS coverage, no signing/attestation requirement for adversarial-test results. |
| UK | DSIT / NCSC | UK AI Regulation White Paper (2023) — sectoral, principles-based approach | Five cross-sectoral principles (safety/security, transparency, fairness, accountability, contestability). **Non-statutory.** No central AI authority equivalent to the EU AI Office. NCSC's 2024 AI security guidance is sectoral and voluntary. |
| AU | DISR / NAIC | AU Voluntary AI Safety Standard (2024) + ASD ISM AI annex (2025) | Voluntary standard; ten guardrails patterned on EU AI Act but **non-binding**. ISM AI annex (2025) names ATLAS but does not bind methodology. |
| JP | Cabinet Office | AI Strategy Council Human-Centric AI Society Principles + AI Guidelines for Business v1.0 (2024-04) + Hiroshima AI Process Code of Conduct (2023-10) — per `data/global-frameworks.json` → JP.AI_STRATEGY_COUNCIL | **Entire regime non-binding** as of 2026-05. No statutory AI law; LDP/Cabinet discussions on a Japanese AI Act ongoing. No mandatory adversarial testing equivalent to EU Art. 72. |
| IL | INCD | Cyber Defense for AI Systems guidance (2024) under INCD Cyber Defense Methodology v2.1 — per `data/global-frameworks.json` → IL.INCD_METHODOLOGY | Explicit AI-systems guidance: adversarial ML threat modelling, prompt injection, training-data integrity, model supply chain. The most operationally-specific national AI-security guidance available in mid-2026. Voluntary for private sector; mandatory for designated essential service providers via INCD directives. |
| ID | Komdigi / BSSN | UU PDP (Law 27/2022) Art. 35; no dedicated AI law as of 2026-05 — per `data/global-frameworks.json` → ID.PDP_LAW | UU PDP general security obligation extends to AI by inheritance; no AI-specific risk-management requirement, no AI inventory obligation, no adversarial-testing duty. |
| US sub-national | NYDFS | 23 NYCRR Part 500 — Cybersecurity Requirements for Financial Services Companies; 2024 NYDFS letter on AI cybersecurity risks — per `data/global-frameworks.json` → US_NYDFS.NYDFS_PART_500 | Part 500 second amendment (2023) is not AI-specific; the 2024 NYDFS AI letter is **interpretive guidance**, not a regulation, but applies Part 500 risk-assessment, vendor-management, and access-control obligations to AI systems. Functions as a de facto financial-sector AI risk-management baseline for any entity holding a New York banking, insurance, or financial-services licence (including non-US institutions). |

Recurring failure across the table: every framework treats AI governance as a process duty to discharge, not as a structured obligation to inventory, classify, assess, treat, test, monitor, and incident-respond per use case. This skill is the missing operational scaffold.

---

## TTP Mapping

Governance failure surfaces as exploitable threat. The TTPs below are the diagnostic markers for the absence of governance controls — the items a red-team or auditor reaches for when asking "is there a governance programme behind this AI deployment?"

| ATLAS ID | Technique | Governance failure that exposes it | Where the gap appears in the AIMS |
|---|---|---|---|
| AML.T0051 | LLM Prompt Injection | No prompt/response logging, no semantic monitoring, no AI use-case-level risk treatment decision | ISO/IEC 23894 clause 7 risk treatment register has no entry; OWASP LLM01 control unowned. CWE-1426 (improper validation of generative AI output) is the root-cause class. |
| AML.T0096 | AI Service API (covert C2) | No baseline of normal AI API traffic per principal; AI API egress treated as trusted internal traffic | NIST AI RMF MEASURE 2.5 not operationalised; SesameOp-class detection absent from SOC playbooks. |
| AML.T0013 | Discover AI Model Ontology: adversary reconnaissance of deployed model family / guardrails | No inference-API rate / shape baseline; model-registry RBAC absent; system-prompt extraction queries undetected | NIST AI RMF MEASURE 2.5 not requiring per-identity inference monitoring; AIMS lacks a probing-detection control. |
| AML.T0017 | Develop Capabilities (adversary AI-assisted exploit / payload development) | No threat-intelligence ingestion path for AI-discovered vulnerabilities; patch SLAs sized for human-speed exploit development | EU AI Act Art. 9 RMS not iterating on the input that 41% of 2025 zero-days are AI-discovered (per `ai-attack-surface` and `zeroday-lessons.json`). |

Supporting weakness classes consumed from `data/cwe-catalog.json`:
- **CWE-1426** — improper validation of generative AI output. The governance correlate: every AI use case must declare what output validation is performed and who owns it.
- **CWE-1039** — automated recognition mechanism with inadequate detection or handling of adversarial input perturbations. Governance correlate: model robustness is a risk-treatment decision, not an implementation accident.

Defensive technique consumed from `data/d3fend-catalog.json`:
- **D3-IOPR** (Input / Output Profiling) — the closest D3FEND-mapped defensive technique to "AI prompt / response governance". Governance does not implement D3-IOPR — it *commissions and audits* the implementation done by `defensive-countermeasure-mapping`.

Threats with no TTP attachment are escalated to `zeroday-gap-learn` (the zero-day learning loop, so no threat is left orphaned without a mapped technique).

---

## Exploit Availability Matrix

Adversary capability versus organisational governance maturity is the relevant axis. CVE-style live-patch decisions are not the unit of analysis here — programme-level readiness is.

| Adversary capability | Low-governance org (no AIMS, no AI inventory) | Medium-governance org (AI inventory + risk register only) | High-governance org (full ISO/IEC 42001 AIMS + AI red-team + AI incident playbook) |
|---|---|---|---|
| Low (off-the-shelf prompt injection per AML.T0051) | Exploitable today. Bypass rates >85% against SOTA defences (per `ai-attack-surface`). No detection. | Exploitable. Risk register names the threat; no detection or response capability deployed. | Detection latency: minutes-to-hours. Response playbook bound to incident class. |
| Medium (AI-as-C2 per AML.T0096, SesameOp pattern) | Exploited last quarter by definition — no AI API logging, no baseline. | Detection-blind: AI traffic logged but no behavioural baseline. | Behavioural baseline + correlation with host activity per `ai-attack-surface` Step 4. |
| High (AI-assisted exploit development per AML.T0017, Copy Fail-class) | Patch SLA structurally inadequate; live-patch capability absent. | Patch SLA sized for human-speed exploit development. | RWEP-driven prioritisation (`lib/scoring.js`), live-patch SLA <4h for KEV+PoC+AI-discovered class. |
| Frontier (training pipeline poisoning, supply-chain compromise of model weights — AML.T0020 catalogue) | No AI supplier risk register; vendor SOC 2 accepted as adequate. | AI vendor register exists; no 4th-party (AI-of-AI) coverage. | EU AI Act Art. 10 data governance + Art. 72 adversarial testing operationalised; vendor adversarial-test attestations required contractually. |

Reference incident inputs to the matrix: vendor advisories from Anthropic, OpenAI, Google DeepMind, Microsoft across 2024–2026; the emergent agentic-attack patterns observed through 2025–2026 disclosed in coordinated-vulnerability programmes per `coordinated-vuln-disclosure`; the AI-as-C2 evidence base referenced in `ai-c2-detection`; the prompt-injection-RCE and MCP-RCE CVE evidence referenced in `ai-attack-surface`.

KEV / PoC / live-patch availability of the underlying CVEs is tracked in `data/cve-catalog.json` and `data/exploit-availability.json`. The governance question is whether the AIMS can *consume* that data; the CVE catalogue itself is the responsibility of the technical-surface skills.

---

## Analysis Procedure

Every AI risk-management exercise must explicitly thread three foundational design principles. They are not optional considerations — they are the structure of the programme.

- **Defense in depth (programme layering, not just technical layering).** Governance ≠ technical defence. The AIMS is a *defence-in-depth scaffold for the technical defences*. Programme layers:
  - Layer 1 — **AI inventory** (every model, every API, every agent, every MCP server, every RAG corpus, every fine-tuning artefact).
  - Layer 2 — **AI impact assessment per use case** (ISO/IEC 23894 clause 7 process; EU AI Act AIA + GDPR DPIA crosswalk for high-risk and personal-data-processing cases).
  - Layer 3 — **AI risk-treatment register** (acceptable / mitigated / transferred / avoided, with owner and review cadence per use case).
  - Layer 4 — **AI incident response playbook** (incident classes, declaration thresholds, regulatory notification timelines per jurisdiction).
  - Layer 5 — **AI red-team programme** (continuous adversarial testing on a documented cadence, with findings routed to the risk register and to `defensive-countermeasure-mapping`).
  - Layer 6 — **AI vendor / 4th-party risk** (AI providers as suppliers whose own AI dependencies are 4th-party risk; contractual adversarial-test attestations).
- **Least privilege (per principal, per use case).** Every AI use case is scoped to the least data and least authority required. Agentic systems get the narrowest action set required, never the model's full tool-call surface. Every agent's service-account permissions are an explicit risk-treatment decision recorded in the register.
- **Zero trust (AI vendors and internal AI tooling are untrusted suppliers).** AI vendor data-retention claims require contractual *and* technical verification (vendor-side audit log access, encryption-in-transit verification, zero-data-retention attestation tied to specific endpoints, not the vendor's marketing page). Internal AI tooling (Copilot, Cursor, Windsurf, Claude Code, agent runtimes, internal RAG) receives the same posture: traffic is logged, principals are authenticated, capabilities are scoped, trust boundaries are explicit.

For ephemeral / serverless / AI-pipeline contexts, governance applies to the *use case*, not to the runtime — the AI inventory entry is per use case, the impact assessment is per use case, and the risk treatment is per use case, regardless of whether the underlying runtime is a long-lived server, a serverless function, or an ephemeral agent invocation.

### Step 1 — Build the AI inventory ledger

Enumerate every AI-touching element with these required columns: name, owner, runtime (SaaS / self-hosted / on-device / edge), data sensitivity tier, EU AI Act risk tier (prohibited / high-risk / limited-risk / minimal-risk / GPAI-with-systemic-risk / GPAI-without-systemic-risk / out-of-scope), processing personal data (yes/no, jurisdictions), tool-call surface (none / read-only / read-write / code-execution), MCP servers attached, dependencies (foundation model, fine-tuning data, RAG corpus, embeddings).

The completeness test is concrete: every model API key issued by the org, every agent runtime installed on a developer workstation, every MCP server entry in `~/.cursor/mcp.json` / `~/.vscode/mcp.json` / equivalent appears as an inventory row. Absence of an inventory row is the governance equivalent of an undocumented production system.

### Step 2 — Classify each use case per EU AI Act risk tier

Use the EU AI Act high-risk categories from `data/global-frameworks.json` → EU.EU_AI_ACT.high_risk_categories as the authoritative list. For each use case classified high-risk, attach the Art. 9 RMS obligation, the Art. 10 data-governance obligation, the Art. 12 logging obligation, the Art. 14 human-oversight obligation, and the Art. 15 cybersecurity obligation, with named owners and operational evidence references.

For organisations operating outside the EU, the classification is still useful as a *structural taxonomy*: every jurisdiction in scope (per `data/global-frameworks.json`) inherits some subset of these obligations through equivalent mechanisms (UK sectoral guidance, AU voluntary guardrails, IL INCD AI guidance, JP AI Guidelines for Business, NYDFS Part 500 + 2024 AI letter, UU PDP for personal-data-processing AI in ID).

### Step 3 — Run AI impact assessment per ISO/IEC 23894

For each inventory row above the minimal-risk threshold, run the ISO/IEC 23894 clause 7 risk-management process: context establishment → risk identification (cross-walking to ATLAS via `data/atlas-ttps.json`) → risk analysis → risk evaluation → risk treatment. For personal-data-processing AI use cases, integrate with the GDPR Art. 35 DPIA, LGPD Art. 38 RIPD, PIPL Art. 55, India DPDPA, Indonesia UU PDP Art. 35 obligations as a combined AIA+DPIA. Hand off the threat-enumeration step to `threat-modeling-methodology` (LINDDUN for privacy, STRIDE-ML for technical, composite for AI-agent systems).

### Step 4 — Log every risk-treatment decision

The risk-treatment register is the artefact auditors and regulators ask for first. Every entry: risk identifier (linked to the ATLAS TTP and any relevant CVE in `data/cve-catalog.json`), treatment decision (accept / mitigate / transfer / avoid), owner, residual-risk justification (cross-walked to RWEP per `lib/scoring.js`, never CVSS alone), review cadence, last review date.

Acceptance decisions require sign-off from the risk-accepting authority. Acceptance without sign-off is theatre (Compliance Theater Check (c) below).

### Step 5 — Set up an AI red-team cadence

Continuous adversarial testing is the operational expression of EU AI Act Art. 72 and NIST AI RMF MEASURE 2.5. Programme requirements:
- Minimum quarterly cadence for high-risk AI use cases; semi-annually for limited-risk.
- ATLAS-coverage minimum: every AML.T* in `data/atlas-ttps.json` applicable to the use case is tested or has a documented exclusion.
- Adversarial-test results feed both `defensive-countermeasure-mapping` (for D3FEND mitigation production) and the risk-treatment register (for residual-risk re-evaluation).
- For GPAI vendors: contractual right to require adversarial-test attestations; reject SOC 2 alone as adequate evidence.

### Step 6 — Integrate AI vulnerability intake with coordinated disclosure

Hand off to `coordinated-vuln-disclosure`: AI-specific vulnerabilities (prompt-injection chains, model-extraction primitives, MCP supply-chain compromises) need a defined intake path that does not flatten them into ordinary CVE workflow. The AIMS owns the policy; CVD owns the procedure.

### Step 7 — Integrate threat modelling per use case

Every inventory row above limited-risk triggers a `threat-modeling-methodology` invocation, with the composite AI-system / agent-based methodology selected when AI agents are in scope. The threat model is the input to the risk-treatment register, not a separate artefact.

### Step 8 — Integrate data-flow controls per AI use case

Hand off to `dlp-gap-analysis`: AI use cases routinely move sensitive data across trust boundaries (developer workstation → SaaS LLM endpoint; internal RAG corpus → LLM context window → user-visible output). The AIMS commissions the DLP analysis; DLP returns control coverage by use case.

### Step 9 — Integrate identity for AI-as-principal

Hand off to `identity-assurance`: every AI agent that takes action requires its own principal identity, AAL/IAL/FAL determination, and authentication mechanism. Reusing a service account across multiple agents collapses the audit trail and is a least-privilege violation (Step 0 principle).

### Step 10 — Build the AIMS per ISO/IEC 42001

The above steps are the operational inputs to the AIMS. Per ISO/IEC 42001 the management system also requires: AI policy, leadership commitment, roles/responsibilities, competence/training records, communication, documented information, operational planning, performance evaluation (internal audit, management review), improvement (corrective actions, continual improvement). The AIMS is the meta-artefact that contains all of the above as evidence.

Re-run cadence: when ATLAS, EU AI Act implementing measures, ISO/IEC 42001, ISO/IEC 23894, NIST AI RMF, or any data-dep version pin advances, re-run the affected layers. The minimum cadence is annual for the AIMS as a whole; quarterly for the risk-treatment register; per-use-case-change for inventory; per-incident for the incident playbook.

---

## Output Format

The skill produces a structured AI Risk Management Programme assessment scoring the org against ISO/IEC 42001:2023, ISO/IEC 23894:2023, NIST AI RMF 1.0, EU AI Act (Regulation 2024/1689) high-risk-system obligations, and the jurisdiction-specific AI frameworks tracked in `data/global-frameworks.json`. The shape below is consumed downstream by `compliance-theater` (which compares the AI-RM policy against deployed controls), by `ai-attack-surface` (which inherits the AI-system inventory), and by `global-grc` (for cross-jurisdictional AI rollup). Preserve the per-standard control-coverage rows verbatim — they are the auditable derivation of the programme score.

```
## AI Risk Management Programme — <organisation / scope>
**Assessment Date:** YYYY-MM-DD
**Standards in scope:** ISO/IEC 42001:2023 | ISO/IEC 23894:2023 | NIST AI RMF 1.0 | EU AI Act (2024/1689) | <jurisdiction-specific frameworks>
**EU AI Act enforcement reference date:** 2026-08-02 (high-risk system obligations fully enforceable)

### 1. AI Inventory Ledger
| ID | Name | Owner | Runtime | Data tier | EU AI Act risk tier | Personal data? | Tool-call surface | MCP servers | Dependencies |
|---|---|---|---|---|---|---|---|---|---|

### 2. AI Impact Assessment Register
| Use case ID | EU AI Act tier | ISO/IEC 23894 risk ID | ATLAS TTPs in scope | CWE root-cause classes | DPIA / RIPD / PIPIA needed | LINDDUN privacy threats | Status |
|---|---|---|---|---|---|---|---|

### 3. AI Risk Treatment Register
| Risk ID | ATLAS / CVE link | Treatment (accept/mitigate/transfer/avoid) | Owner | Residual-risk RWEP | Acceptance sign-off (if applicable) | Review cadence | Last review |
|---|---|---|---|---|---|---|---|

### 4. AI Red-Team Programme Charter
- Cadence: <per risk tier>
- ATLAS coverage minimum: <list of AML.T* IDs in scope per use case>
- Findings routing: `defensive-countermeasure-mapping` + risk treatment register
- Last red-team round: YYYY-MM-DD
- Top findings (summary, full report linked)

### 5. AI Incident Response Playbook
- Incident classes (model exfiltration, training-data poisoning, agent compromise via MCP, RAG corpus contamination, AI vendor breach, AI-as-C2 detection, prompt-injection-as-RCE)
- Declaration thresholds per class
- Regulatory notification timelines: GDPR 72h, NIS2 24h/72h/30d, DORA major-incident, EU AI Act Art. 73 serious incident, NYDFS 72h, jurisdiction-specific per `data/global-frameworks.json`
- IR roles, escalation matrix, communications template

### 6. AI Vendor / 4th-Party Risk Register
| Vendor | AI service | Vendor's AI dependencies (4th party) | Adversarial-test attestation status | Zero-data-retention contractual basis | Last assurance | Next review |
|---|---|---|---|---|---|---|

### 7. ISO/IEC 42001 Audit-Readiness Matrix
| 42001 clause | Evidence artefact | Owner | Status (in place / partial / gap) | Notes |
|---|---|---|---|---|

### 8. EU AI Act Compliance Evidence Pack (for high-risk systems)
| Article | Obligation | Evidence reference | Owner | Status |
|---|---|---|---|---|

### 9. Cross-Jurisdiction Obligations Summary
<per jurisdiction in scope, the binding and non-binding AI obligations attached, hand-off to `global-grc`>

### 10. Hand-Off Register
<every threat enumerated above linked to its consuming skill: `defensive-countermeasure-mapping`, `threat-modeling-methodology`, `dlp-gap-analysis`, `identity-assurance`, `coordinated-vuln-disclosure`, `ai-attack-surface`, `mcp-agent-trust`, `rag-pipeline-security`, `global-grc`>
```

---

## Compliance Theater Check

Apply each test. A "no" on any of (a)–(e) means the AI governance posture is paper.

(a) **Show me your AI inventory ledger.** If there is no list of every model + API + agent + MCP server + RAG corpus, the governance claim is theatre. ISO/IEC 42001 cannot be implemented over an unknown surface. The test is concrete: ask for the inventory; if the response is "we use OpenAI for some things" or "let me check with the AI team", the inventory does not exist.

(b) **Show me your most recent AI impact assessment for a high-risk EU AI Act use case.** Per the 2026-08-02 enforcement date, any high-risk use case in production requires a documented Art. 9 RMS output before that date. If none exist for a deployed high-risk use case, the organisation is non-compliant with the upcoming deadline — and the governance programme is paper. If the response is "we don't think any of our use cases are high-risk" without a documented classification exercise referencing EU AI Act Annex III, that *is* the theatre.

(c) **What is your AI red-team cadence and last finding?** If the answer is "we haven't tested" or "we ran a red-team exercise in 2023", the red-team programme is theatre. The pattern auditors look for in 2026: a documented cadence, ATLAS-coverage matrix, last-test date within the cadence window, findings routed to the risk-treatment register, and at least one residual-risk re-evaluation triggered by a red-team finding.

(d) **Show me your AI vendor 4th-party risk register.** If the response is "we trust the SOC 2 Type II report from our AI vendor", that is theatre for the AI-specific risk class. SOC 2 has no AI-specific criteria. The test: ask which of the vendor's own AI dependencies (model weights, training data, MCP servers the vendor exposes) are covered by their SOC 2 report. Almost universally, none are.

(e) **Show me your acceptance sign-off for the prompt-injection residual risk.** Per AML.T0051 and the bypass rates >85% against SOTA defences (per `ai-attack-surface`), every organisation deploying LLMs with tool-call capability is operating with non-trivial residual prompt-injection risk. That residual must be a *signed-off acceptance decision* by the risk-accepting authority — not a silent assumption that prompt-injection classifiers handle it. If the residual is not documented, the AIMS is missing its highest-priority risk treatment.

(f) **Show me the framework-gap declaration for ISO/IEC 42001 in your AIMS.** The AIMS must explicitly declare what ISO/IEC 42001 controls are insufficient for current TTPs (framework lag is first-class). If the AIMS implies that 42001 certification is adequate evidence of AI security posture, the framework-lag rule is breached. Hand-off to `framework-gap-analysis` is then required.

---

## Defensive Countermeasure Mapping

AI risk management is a process-not-technical discipline; its D3FEND mapping is therefore indirect. The closest technical correlate to *governance-of-prompt/response-flows* is **D3-IOPR** (Input / Output Profiling) from `data/d3fend-catalog.json`. The AIMS does not implement D3-IOPR — it *commissions, audits, and re-prioritises* the D3-IOPR implementation that `defensive-countermeasure-mapping` is responsible for.

For each governance finding produced by this skill that maps to a technical risk class (prompt injection, AI-as-C2, model extraction, training-data poisoning, RAG exfiltration, MCP compromise), hand off to `defensive-countermeasure-mapping` to produce the D3FEND ID set with the four-axis annotation prescribed there:
- **Defense-in-depth layer position** — the AIMS audits that every accepted residual has at least two defensive layers, or a signed acceptance for the shallow-defence position.
- **Least-privilege scope** — the AIMS verifies that every AI principal's authorisation surface is the minimum required and is recorded in the risk-treatment register.
- **Zero-trust posture** — the AIMS verifies that every boundary crossing in the AI inventory has a stated verification primitive.
- **AI-pipeline applicability** — the AIMS rejects governance recommendations that are architecturally infeasible for the runtime in question and requires an explicitly scoped alternative or an "accept residual or redesign" entry.

Per the broader `defensive-countermeasure-mapping` cross-walk, the AIMS is the place where D3FEND coverage gaps are *owned*: a missing D3FEND layer is not a defect the technical team carries alone — it is a residual-risk entry the risk-accepting authority owns.

---

## Hand-Off / Related Skills

- **`threat-modeling-methodology`** — per-use-case threat models. Every AI inventory row above limited-risk triggers a threat-model invocation; the resulting threat enumeration feeds the risk-treatment register.
- **`ai-attack-surface`** — technical AI attack surface. Provides the TTP-to-CVE evidence base the AIMS classifies and treats.
- **`mcp-agent-trust`** — MCP server and agent-plugin trust posture. Every MCP server in the AI inventory ledger triggers an `mcp-agent-trust` invocation; results inform the vendor / 4th-party register.
- **`rag-pipeline-security`** — RAG corpus and vector embedding store assessment. Every RAG corpus in the inventory triggers this skill.
- **`dlp-gap-analysis`** — data-flow controls for AI use cases. Receives use-case data flows from this skill; returns DLP coverage gaps to be entered into the risk-treatment register.
- **`identity-assurance`** — AI-as-principal identity, authentication mechanism, AAL/IAL/FAL determination. Receives the agent inventory; returns identity posture for each principal.
- **`coordinated-vuln-disclosure`** — AI vulnerability intake. The AIMS owns the policy; CVD owns the procedure. AI-specific vulnerabilities flow through CVD; the AIMS consumes the resulting evidence.
- **`global-grc`** — cross-jurisdictional obligations. The AIMS produces a jurisdictional obligation summary (section 9 of Output Format); `global-grc` is the canonical comparator for the cross-jurisdiction matrix.
- **`framework-gap-analysis`** — invoked when an AI use case is not adequately covered by ISO/IEC 42001 / 23894 / NIST AI RMF / EU AI Act. Runs the EU+UK+AU+ISO+IL+JP+ID+NYDFS comparison.
- **`zeroday-gap-learn`** — receives any threat enumerated in the impact-assessment register that has no ATLAS or ATT&CK TTP attachment, feeding the zero-day learning loop.
- **`compliance-theater`** — runs the broader theatre detection against the AIMS as a whole when an audit cycle approaches.
