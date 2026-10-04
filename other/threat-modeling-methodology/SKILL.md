---
name: threat-modeling-methodology
version: "1.0.0"
description: Threat modeling methodologies for mid-2026 — STRIDE, PASTA, LINDDUN (privacy), Cyber Kill Chain, Diamond Model, MITRE Unified Kill Chain, AI-system threat modeling, agent-based threat modeling
triggers:
  - threat model
  - threat modeling
  - stride
  - pasta
  - linddun
  - kill chain
  - diamond model
  - unified kill chain
  - attack tree
  - threat modeling methodology
  - data flow diagram
  - dfd
  - trust boundary
data_deps:
  - atlas-ttps.json
  - cve-catalog.json
  - cwe-catalog.json
  - d3fend-catalog.json
  - framework-control-gaps.json
  - zeroday-lessons.json
atlas_refs: []
attack_refs: []
framework_gaps:
  - ISO-27001-2022-A.8.28
  - ISO-IEC-23894-2023-clause-7
  - ISO-IEC-42001-2023-clause-6.1.2
  - NIST-800-218-SSDF
  - NIS2-Art21-incident-handling
  - UK-CAF-A1
  - AU-Essential-8-App-Hardening
rfc_refs: []
cwe_refs: []
d3fend_refs: []
forward_watch:
  - ISO/IEC 27005 revision integrating AI-system threats
  - OWASP Threat Modeling Manifesto v2 (post-2020)
  - MITRE ATLAS v6 publication and any methodology guidance attached
  - Unified Kill Chain successor revision (Pols, post-v3.0)
  - LINDDUN-GO and LINDDUN-PRO updates incorporating LLM privacy threats
  - PASTA v2 updates incorporating AI/ML application threats
last_threat_review: "2026-09-18"
discovery_mode: "standalone"  # operator-reached via `exceptd brief threat-modeling-methodology` or `exceptd ask`; not chained into any playbook's direct.skill_chain by design
---

# Threat Modeling Methodology

## Frontmatter Scope

The `atlas_refs` and `attack_refs` arrays are intentionally empty. This skill teaches the *method* for selecting and combining threat-modeling frameworks and mapping threats to techniques — it does not own a fixed TTP set. The specific TTPs cited in the body are illustrative of the method; the authoritative technique attachment lives on the domain skill or playbook that detects each threat. Duplicating those IDs here would create a divergence surface the next time a downstream mapping changes.

## Purpose

The companion skill `threat-model-currency` measures *when* a threat model is stale. This skill governs *how* a threat model is built. Currency without methodology yields opinion; methodology without currency yields a current-looking 2022 artefact. Both are required.

This skill is opinionated about methodology selection. There is no single methodology that covers technical threats, privacy threats, intrusion-analysis scenarios, full-lifecycle attack chains, and AI/agent-system threats simultaneously. Practitioners who try to force one methodology to do all five jobs produce thin coverage. The procedure below selects and combines methodologies deliberately.

---

## Threat Context

Most "threat models" in circulation in mid-2026 are STRIDE diagrams of 2018–2022 vintage. Their failure modes are concrete and current:

- **No AI agents as actors.** The actor inventory lists humans, services, and external systems. AI coding assistants, MCP servers, RAG retrievers, autonomous agents executing tool calls — none appear with their own trust boundaries. The Windsurf MCP local-vector RCE (CVE-2026-30615, CVSS 8.0 / AV:L) and the Copilot YOLO-mode RCE (CVE-2025-53773, CVSS 7.8 / AV:L) are not representable in a model whose actor schema predates the threat.
- **No MCP supply-chain RCE class.** Trust boundaries between developer workstations and "tool plugins" do not exist in pre-2024 threat models. The supply-chain chapter lists npm, Docker, and OS packages — not AI tool plugins, which now have an equal or greater attack surface across 150M+ assistant installs.
- **No AI-API as C2 channel.** The C2 chapter enumerates DGAs, beaconing, protocol anomalies. ATLAS AML.T0096 (AI Service API, covert C2, SesameOp pattern) is not on the diagram. The model cannot reason about a documented technique that is operationally indistinguishable from legitimate AI usage at the network layer.
- **Prompt injection mis-classified.** Pre-2024 STRIDE assigns prompt injection to "Tampering" or omits it entirely. Operationally it is an access-control bypass that achieves what spoofing achieves via the model's context window, with measured success rates above 85% against state-of-the-art defences.
- **Embedding store missing from crown jewels.** Data-classification work predates RAG. Vector embeddings of proprietary documents are treated as "metadata" rather than as a semantic projection of the underlying sensitive corpus.

Methodology choice is not cosmetic — it determines what is representable in the model:

- **STRIDE** (Microsoft, formalised 1999; SDL adoption 2002) under-represents privacy threats. LINDDUN exists because Spoof/Tamper/Repudiate/InfoDisclose/DoS/EoP cannot cleanly express linkability, identifiability, non-repudiation-of-data-subjects, detectability, disclosure-of-information-with-purpose-mismatch, unawareness, and non-compliance.
- **PASTA** (Process for Attack Simulation and Threat Analysis, Tony UcedaVélez, 2012; book 2015) over-represents app-layer threats. It is excellent for a single application's threat surface and weak for systemic AI risks crossing multiple AI services, agents, and pipelines.
- **LINDDUN** (KU Leuven, original 2010; LINDDUN-GO 2020; LINDDUN-PRO 2022) is the canonical privacy methodology and the appropriate input to a GDPR / LGPD / PIPL / DPDPA DPIA workflow.
- **Trike** (Saitta, Larcom, Eddington, 2005) is requirements-driven and asset-centric; it survives in regulated environments but has had limited public revision.
- **OCTAVE** / **OCTAVE Allegro** (SEI / Carnegie Mellon, OCTAVE 2001, Allegro 2007) is enterprise-risk shaped, useful for organisation-wide asset prioritisation, and ill-suited to component-level technical modelling.
- **Cyber Kill Chain** (Lockheed Martin, Hutchins/Cloppert/Amin, 2011) is linear, intrusion-stage shaped, biased toward APT-style attacks, and weak for cloud-native and ephemeral compute.
- **Diamond Model of Intrusion Analysis** (Caltagirone, Pendergast, Betz, 2013) gives IR / SOC analysts an adversary–capability–infrastructure–victim frame that ATT&CK alone does not, and pivots naturally to attribution and campaign tracking.
- **MITRE Unified Kill Chain** (Pols, 2017; v3.0 published 2024) integrates Lockheed Kill Chain with MITRE ATT&CK across 18 stages, extending coverage to cover initial access through impact in cloud-native and AI-augmented environments.
- **AI-system threat modeling** (Microsoft AI/ML STRIDE-ML, MITRE ATLAS methodology guidance, OWASP ML Top 10) and **agent-based threat modeling** are not unified into a single accepted framework as of mid-2026. The procedure below treats them as a composite of STRIDE-ML + ATLAS TTPs + an explicit actor-inventory amendment.

Skipping methodology selection is itself a methodology. The most common pattern in industry is "we talked about threats in a sprint planning meeting" — which produces no artefact, no review trail, and no input to currency assessment. The pre-ship test for this skill: an artefact exists, lives next to the system it models, and is versioned.

---

## Framework Lag Declaration

No major risk-assessment, secure-development, or AI-management framework prescribes a specific threat-modeling methodology. The gap is global, not US-specific.

| Jurisdiction | Framework | Control | What it misses |
|---|---|---|---|
| US | NIST SP 800-53 Rev. 5 | RA-3 (Risk Assessment) | Process-only — mentions threat sources and threat events; specifies no methodology, no DFD/attack-tree requirement, no actor inventory standard. A STRIDE-from-2018 model is RA-3-compliant in 2026. |
| US | NIST SP 800-218 SSDF v1.1 | PW.1 (Design Software to Meet Security Requirements), PW.4 (Reuse Existing, Well-Secured Software) | PW.1 calls for "threat modelling and risk assessment" without specifying methodology. PW.4 has no representation for AI-assistant-generated code as a distinct supply-chain class. Listed in `data/framework-control-gaps.json` as `NIST-800-218-SSDF`. |
| US | NIST AI RMF 1.0 | MAP-2.1, MAP-3.1 | Requires categorising AI-system risks; does not require a specific threat model methodology, does not require trust-boundary articulation for AI agents, does not cross-walk to ATLAS. |
| EU | EU AI Act | Art. 9 (Risk Management System for high-risk AI) | "Continuous iterative" risk management; provides no methodology, no required cross-walk to ATLAS, no requirement that AI agents be modelled as actors with trust boundaries. |
| EU | NIS2 Directive (2022/2555) | Art. 21(2)(a) — Risk analysis policies | Mandates risk analysis as a measure; silent on threat-model methodology. National competent authority guidance (mid-2026) has not bound any methodology. |
| EU | DORA (Regulation 2022/2554) | Art. 6 — ICT risk management framework | "Ongoing" risk identification; undefined methodology. |
| EU | EU Cyber Resilience Act (Regulation 2024/2847) | Annex I, Part I — Essential cybersecurity requirements | Requires risk assessment over the product lifecycle; does not specify methodology, does not name AI components or agent supply chain as a required model element. |
| UK | NCSC | Cyber Assessment Framework Principle A2 (Risk Management); NCSC Threat Modelling guidance (2024 update) | Principle-based. NCSC's 2024 threat-modelling guidance recommends STRIDE-like decomposition but does not mandate AI-agent actor representation. |
| AU | ASD | ISM-1238 (threat modelling in the software development life cycle) and ISM-2039 (threat model review); ISM AI annex (2025) | The ISM requires threat modelling for software development and a review that tracks changes to the threat environment, but binds no threat-modeling methodology. The 2025 AI annex names ATLAS but does not require methodology-level integration. |
| JP | NISC / IPA | Cybersecurity Management Guidelines v3.0 (2023) | Requires risk identification process; methodology-neutral; no AI-actor requirement. |
| IL | INCD | Cyber Defence Methodology 2.0 (2024) | Risk-based but methodology-neutral; AI-system threat modelling not yet integrated as of mid-2026. |
| SG | CSA Singapore | Cybersecurity Code of Practice (CCoP 2.0, 2022); Model AI Governance Framework v2 (2024) | CCoP requires risk assessment; AI governance framework is principle-based; neither binds a methodology. |
| Global | ISO | ISO/IEC 27001:2022 A.5.7 (Threat Intelligence), A.8.28 (Secure Coding) | Listed in `data/framework-control-gaps.json` as `ISO-27001-2022-A.8.28`. Silent on methodology; prompt-injection-as-RCE is outside the scope of "secure coding". |
| Global | ISO | ISO/IEC 27005:2022 (Information security risk management) | Process guidance; methodology-neutral; predates current AI threat catalogue. |
| Global | ISO | ISO/IEC 42001:2023 (AI Management System), clause 6.1.2 | Listed as `ISO-IEC-42001-2023-clause-6.1.2`. AI risk assessment as periodic activity; no runtime threat-surface methodology; cross-jurisdiction obligations not enumerated. |
| Global | ISO | ISO/IEC 23894:2023 (AI Risk Management Guidance) clause 7 | Process-level lifecycle guidance; no specific methodology binding. |
| Global | ISO | ISO 31000:2018 (Risk management) | Enterprise-risk umbrella; no operational methodology. |
| Global | COSO | ERM Framework | Enterprise risk; no operational threat-modelling methodology. |
| Privacy | EU / global | GDPR Art. 35 (DPIA); LGPD Art. 38 (RIPD); PIPL Art. 55; India DPDPA 2023 | Require impact assessments but bind no methodology. LINDDUN is the de facto privacy threat-modeling methodology; none of these regulations name it. |

The recurring failure across all of the above: every framework treats threat modelling as a process to perform, not as a methodology to select on the basis of what is representable. This skill is the missing methodology selector.

---

## TTP Mapping

Threat-modelling methodologies are *consumers* of the TTP catalog, not contributors. The mapping below shows what each methodology pulls from `data/atlas-ttps.json`, `data/cve-catalog.json`, and the ATT&CK references inside `data/cve-catalog.json` entries.

| Methodology | Native input | TTP pull pattern | Gap if methodology used alone |
|---|---|---|---|
| STRIDE / STRIDE-per-element | Trust boundaries on a DFD | Per boundary: enumerate Spoof / Tamper / Repudiate / InfoDisclose / DoS / EoP; map each to ATT&CK or ATLAS TTPs from `data/atlas-ttps.json` | Privacy threats (linkability, identifiability) compressed into "InfoDisclose" lose specificity; LINDDUN required to surface them. |
| STRIDE-ML (Microsoft, 2020) | DFD with ML training/inference/feedback elements | Per ML element: adversarial ML threats from ATLAS (AML.T0010 ML Supply Chain, AML.T0020 Poison Training Data, AML.T0043 Craft Adversarial Data, AML.T0051 LLM Prompt Injection, AML.T0054 LLM Jailbreak, AML.T0096 AI Service API) | Agent-as-actor still missing; needs the actor-inventory amendment described in the Analysis Procedure. |
| PASTA | App-centric attack trees with business-impact rooting | Per app component: pull CVE-level threats from `data/cve-catalog.json` (e.g. CVE-2025-53773 prompt-injection RCE in app-integrated AI assistants) and ATLAS TTPs at the app boundary | Systemic AI risks crossing services (cross-agent prompt injection, shared embedding contamination) sit outside any one app. |
| LINDDUN / LINDDUN-PRO | DFD plus privacy threat tree | Per data flow: Linkability, Identifiability, Non-repudiation, Detectability, Disclosure-of-Information, Unawareness/Unintervenability, Non-compliance; cross-walk to GDPR Art. 5 / Art. 32 obligations | Technical threats (memory corruption, kernel LPE) not represented. |
| Trike | Requirements model + implementation model | Per actor-action pair: authorised vs. unauthorised actions; pull ATT&CK TTPs that bridge the gap | Limited recent revision; weaker fit for AI-agent actors. |
| OCTAVE Allegro | Asset profiles | Per critical asset: areas-of-concern; cross-walk to ATLAS/ATT&CK | Component-level technical threats missing. |
| Cyber Kill Chain | Linear 7-stage intrusion timeline | Per stage: ATT&CK TTPs | Cloud-native / serverless / AI-pipeline scenarios fit the timeline poorly; lateral movement assumptions break in ephemeral compute. |
| Diamond Model | Adversary–capability–infrastructure–victim diamond | Per intrusion event: TTPs become adversary capabilities; pivot to other diamonds | Built for IR / SOC, not for design-phase threat modelling — pair with STRIDE/PASTA during design and Diamond during operate phase. |
| MITRE Unified Kill Chain (v3.0, 2024) | 18 phases spanning initial access through objectives | Per phase: ATLAS and ATT&CK TTPs assigned to phases that cover both classical and AI-augmented attacks | Most comprehensive single methodology, but weak on privacy threats — pair with LINDDUN. |
| AI-system threat modeling (composite) | Augmented DFD with AI actors and AI trust boundaries | Full ATLAS v2026.09 catalogue (every `AML.T*` key in `data/atlas-ttps.json`) | Methodology not yet standardised — this skill operationalises it. |
| Agent-based threat modeling | Actor graph with autonomous agents, MCP plugins, tool-call boundaries | CVE-2026-30615 (MCP RCE), CVE-2025-53773 (prompt-injection RCE), AML.T0051, AML.T0096 | Methodology not yet standardised — this skill operationalises it. |

The truth set for any composite model is: every `AML.T*` key in `data/atlas-ttps.json`, plus every `attack_refs` entry across every CVE in `data/cve-catalog.json`, plus the CWE root-cause classes in `data/cwe-catalog.json`. A model that does not address each, or document a reasoned exclusion for each, is non-current by construction (and should be re-run through `threat-model-currency`).

---

## Exploit Availability Matrix

Methodologies are catalog consumers, not catalog producers. The matrix shows the catalog dependency for each.

| Methodology | Consumes | KEV-bound? | PoC-bound? | AI-accelerated input? | Live-patch decisions in scope? |
|---|---|---|---|---|---|
| STRIDE | Generic threat categories per boundary | No — threat categories are pre-CVE | No | No | No (model is design-time) |
| STRIDE-ML | STRIDE categories + ATLAS TTPs | Indirectly via CVEs mapped to TTPs | Yes (when a TTP has a public PoC, that strengthens the threat) | Yes (AML.T0016 Obtain Capabilities and AML.T0017 Develop Capabilities, AI on attacker side) | No |
| PASTA | App-centric attack trees consuming CVE-level primitives from `data/cve-catalog.json` | Yes (KEV entries elevate tree-branch priority) | Yes | Yes | Possible — PASTA stage VI (Vulnerability and Weakness Analysis) names live-patch as a control class |
| LINDDUN | Privacy threat tree | No — privacy threats are policy-bound, not exploit-bound | No | No | No |
| Trike | Authorised/unauthorised action gaps | Indirectly | Indirectly | No | No |
| OCTAVE Allegro | Asset areas-of-concern | Indirectly | No | No | No |
| Cyber Kill Chain | Intrusion phases | Yes (KEV common in initial-access phase) | Yes | Yes | No |
| Diamond Model | Adversary–capability–infrastructure–victim | Yes (capabilities include live CVEs) | Yes | Yes (campaigns increasingly use AI-developed capabilities — AI-assisted attack development is current operational reality) | Yes (Diamond pivots into IR and IR drives live-patch decisions) |
| MITRE Unified Kill Chain v3.0 | Full ATLAS + ATT&CK across 18 phases | Yes | Yes | Yes | Yes (phases 14–18 include impact stages where live-patch SLAs are decisive) |
| AI-system composite | Full ATLAS catalogue | Yes (CVE-2025-53773 prompt-injection RCE, CVE-2026-30615 MCP RCE, both in `data/cve-catalog.json`) | Yes | Yes | Yes (CVE-2025-53773 is SaaS live-patchable; CVE-2026-30615 is IDE-update live-patchable) |
| Agent-based composite | ATLAS subset (AML.T0010, AML.T0051, AML.T0096) + MCP-class CVEs | Yes | Yes | Yes | Yes |

None of these methodologies directly consume the CVE catalog as a primary input. All of them must be *informed* by `data/cve-catalog.json` for currency — which is what makes `threat-model-currency` the natural companion skill.

---

## Analysis Procedure

Every threat-modelling exercise must explicitly thread three foundational principles. None is optional.

- **Defense in depth.** Methodology selection itself is a defense-in-depth question. Use STRIDE-ML for technical threats *plus* LINDDUN for privacy *plus* Diamond Model for operate-phase IR scenarios *plus* MITRE Unified Kill Chain v3.0 for end-to-end lifecycle coverage. No single methodology is sufficient. The model must show, per threat, at least two control layers (prevent + detect, or prevent + contain).
- **Least privilege.** Every actor in the model — human, service, AI agent, MCP plugin, RAG retriever, tool-call target — must be documented with a trust boundary and a minimum-scope authorisation statement. The model surfaces excess privilege as a finding, not as an implicit assumption.
- **Zero trust.** Trust boundaries are explicit. Every boundary crossing requires verification (mutual auth, signed input, capability-scoped token, prompt-injection-resistant context boundary). The model must answer, for each boundary, *what is verified and how* — not "the network is internal".

For ephemeral / serverless / AI-pipeline contexts, classical STRIDE-per-element applies poorly: there is no persistent attack surface to decompose. Use the modified procedure: model the *invocation lifecycle* (cold-start → execution → state externalisation → teardown) as the unit of analysis, attach trust boundaries to invocation-context inputs (event payload, IAM-scoped role, retrieved secrets, AI model context window), and treat the absence of persistent state as a control to be verified, not assumed.

### Step 1 — Scope the system and inventory actors (including AI agents)

List every actor with a trust boundary and an authorisation scope:

- Human actors (end users, operators, developers, admins, contractors).
- Service actors (microservices, batch jobs, cron tasks, queues).
- External-system actors (third-party APIs, identity providers, SaaS).
- **AI actors** — AI coding assistants, MCP servers, LLM endpoints, agent runtimes, autonomous workflows. Every AI actor is named, with trust boundary, with minimum-scope authorisation, with an explicit answer to "what does this agent decide on its own and what does it escalate?"
- Data actors — vector embedding stores, RAG corpora, training data manifests, model weight artefacts. Treated as crown-jewel data even when they appear as "metadata" elsewhere.

### Step 2 — Choose methodology or methodology mix

Apply the selection rule:

- Technical threats only, single app, design phase → STRIDE-per-element (or STRIDE-ML if any AI/ML element exists).
- Privacy / DPIA in scope (GDPR / LGPD / PIPL / DPDPA) → add LINDDUN-PRO.
- Multi-service / app-centric with business-impact rooting → PASTA, with STRIDE-ML inside each app-component decomposition.
- Operate-phase / SOC / IR scenarios → Diamond Model, fed by ATLAS+ATT&CK.
- End-to-end lifecycle, cloud-native, AI-augmented → MITRE Unified Kill Chain v3.0 as the spine, with STRIDE-ML and LINDDUN as per-phase decomposition tools.
- AI agents present → composite AI-system + agent-based amendments to whichever spine is chosen.

Document the methodology choice and rationale at the top of the artefact. Methodology choice is reviewable.

### Step 3 — Draw the model

Per chosen methodology:

- STRIDE / STRIDE-ML / LINDDUN / PASTA → Data Flow Diagram with explicit trust boundaries and explicit AI actors. Where ephemeral compute is in scope, the DFD models invocation lifecycle, not server topology.
- Trike → requirements model and implementation model side by side.
- OCTAVE Allegro → asset profile sheets.
- Cyber Kill Chain → linear stage diagram.
- Diamond Model → adversary–capability–infrastructure–victim diamonds per intrusion event.
- MITRE Unified Kill Chain v3.0 → 18-phase grid with applicable TTPs at each phase.
- Agent-based → actor graph with directed edges representing tool-call authorisations.

### Step 4 — Enumerate threats per methodology

For STRIDE: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege. For STRIDE-ML add: Model Stealing, Model Poisoning, Adversarial Input, Prompt Injection, Membership Inference. For LINDDUN: Linkability, Identifiability, Non-repudiation (of data subjects), Detectability, Disclosure of Information, Unawareness/Unintervenability, Non-compliance. For PASTA: complete the seven stages (Define Objectives → Define Technical Scope → App Decomposition → Threat Analysis → Vulnerability & Weakness Analysis → Attack Modelling → Risk & Impact Analysis).

### Step 5 — Map threats to ATLAS + ATT&CK

For each enumerated threat, attach at least one `AML.T*` ID from `data/atlas-ttps.json` or one ATT&CK `T*` ID. Threats with no TTP attachment are either (a) novel — and require an entry into the zero-day learning loop via `zeroday-gap-learn` — or (b) over-broad and need decomposition.

### Step 6 — Cross-walk to CWE root causes

For each technical threat, attach the relevant CWE class from `data/cwe-catalog.json`. CWE is the design-defect view that complements ATT&CK's behavioural view. A model whose threats cross-walk only to TTPs is operationally complete but architecturally thin.

### Step 7 — Score known CVEs per RWEP

For each threat that maps to a known CVE in `data/cve-catalog.json`, score per RWEP (`lib/scoring.js`) — not CVSS alone (CVSS-only risk scoring is prohibited; report CVSS alongside RWEP, never alone). RWEP outputs feed prioritisation in step 8.

### Step 8 — Produce mitigations (hand off to defensive-countermeasure-mapping)

Mitigations are out of scope for this skill. Every enumerated threat is handed to `defensive-countermeasure-mapping`, which produces D3FEND IDs from `data/d3fend-catalog.json`. The cross-walk handoff is described in section "Defensive Countermeasure Mapping" below.

### Step 9 — Integrate findings to threat-model-currency

The output of this skill feeds `threat-model-currency` as the model under test. Currency assessment runs against this artefact, not against a separately-maintained PDF.

### Step 10 — Re-run on cadence

Under the external-data version-pinning discipline: when ATLAS, ATT&CK, NIST 800-218 SSDF, ISO/IEC 42001, or any data-dep version pin advances, re-run the model. Currency triggers also include: any new CVE in scope (`data/cve-catalog.json` change), any new zero-day lesson (`data/zeroday-lessons.json` change), any change to actor inventory (new agent, new MCP server, new RAG corpus).

---

## Output Format

The skill produces a structured Threat Model per system covering the chosen methodology composite (STRIDE-ML + LINDDUN + Diamond, or Unified Kill Chain v3.0, or a domain-specific composite), the data-flow diagram, identified threats with ATLAS / ATT&CK mapping, mitigations with D3FEND ID, and the currency-trigger list that schedules re-runs. The shape below is consumed downstream by `threat-model-currency` (which scores the model against the 14-class checklist), by `framework-gap-analysis` (which converts each unmitigated threat into a Framework Lag Declaration), and by `policy-exception-gen` (for any threat accepted as residual risk). Preserve the methodology-rationale field verbatim — it is the auditable justification for the chosen composite.

```
## Threat Model — <system name>
**Date:** YYYY-MM-DD
**Methodology:** <STRIDE-ML + LINDDUN + Diamond | Unified Kill Chain v3.0 | composite ...>
**Methodology rationale:** <why this combination, not others>
**Currency triggers:** <list of upstream changes that will require re-run>

### 1. Scope and Actor Inventory
| Actor | Type (human/service/AI/data) | Trust boundary | Minimum-scope authorisation | Notes |
|---|---|---|---|---|

### 2. AI / Agent Inventory (required if any AI actor present)
| Agent | Runtime | Tool-call surface | Plugins / MCP servers | Decides on its own | Escalates to |
|---|---|---|---|---|---|

### 3. Data Flow Diagram / Attack Tree / Kill Chain Grid
<diagram or structured representation per methodology choice>

### 4. Threat Enumeration
| # | Methodology | Element / Phase | Threat | ATLAS / ATT&CK TTP | CWE | CVE (if any) | RWEP |
|---|---|---|---|---|---|---|---|

### 5. ATLAS / ATT&CK Cross-Walk
<aggregated TTP list against atlas-ttps.json and ATT&CK; flag uncovered TTPs>

### 6. CWE Root-Cause Cross-Walk
<aggregated CWE list against cwe-catalog.json>

### 7. Mitigation Roadmap (hand-off)
<refer each threat to defensive-countermeasure-mapping output; do not enumerate D3FEND here>

### 8. Currency Triggers
<list specific external events that invalidate this model and require re-run via threat-model-currency>

### 9. Methodology Limitations
<explicit per-methodology gap statement; e.g., "STRIDE-ML does not surface privacy threats; LINDDUN-PRO addendum at section 4b">
```

---

## Compliance Theater Check

Apply each test. A "no" on any of (a)–(e) means the threat-model is paper.

(a) **Currency.** "Show me your current threat model." If the response is "we did one two years ago" or "let me find it in SharePoint", theater — the model is not an operational artefact.

(b) **Co-location with the system.** "Is your threat model checked into the same Git repository as the system it models, with a `CODEOWNERS` rule that requires security review on changes?" If it lives in a SharePoint, Confluence wiki, or shared drive disconnected from the codebase, theater — there is no enforced review on system changes that invalidate the model.

(c) **AI agents as actors.** "Did your latest threat model include AI agents as actors with their own trust boundaries and minimum-scope authorisation statements? Name them." If the actor inventory does not name AI coding assistants, MCP servers, agent runtimes, or RAG retrievers, the model is 2022-vintage regardless of its date stamp.

(d) **Right methodology for privacy.** "For your privacy threats, did you use STRIDE or LINDDUN?" STRIDE for privacy is the wrong methodology — InfoDisclose compresses seven LINDDUN categories into one. If the DPIA / RIPD / PIPIA referenced this model and it used STRIDE alone for privacy, the privacy assessment is theater.

(e) **Cross-jurisdiction.** "Did your model include cross-jurisdiction threats — EU AI Act high-risk categorisation, NIS2 incident-reporting timelines, DORA ICT third-party register, UK CAF B4, AU ISM AI annex, IL INCD methodology, JP NISC, SG CCoP 2.0?" Global-first, not US-centric: a model citing only US frameworks does not meet the bar.

(f) **Methodology rationale.** "Why did you choose this methodology mix?" If the answer is "because that's what we always do" or "because STRIDE is the standard", the methodology choice was not reviewed. Document the rationale or it is theater.

---

## Defensive Countermeasure Mapping

Threat modelling produces an enumerated threat set; mitigations come from the `defensive-countermeasure-mapping` skill. Every threat in the Threat Enumeration table (section 4 of Output Format) is handed off as an input to that skill, which produces D3FEND IDs from `data/d3fend-catalog.json` along with the explicit four-axis annotation:

- **Defense-in-depth layer position.** Each D3FEND mapping is annotated with its layer (network, host, identity, application, data, agent context). Threats that map to only one layer are flagged for additional layering.
- **Least-privilege scope.** Each mapping is annotated with the principal whose privilege is being scoped (human user, service identity, agent, plugin). Mappings that do not narrow privilege are flagged as monitoring-only.
- **Zero-trust posture.** Each mapping declares the verification primitive at the boundary it covers (mutual auth, signed input, prompt-injection-resistant context boundary, capability-scoped token).
- **AI-pipeline applicability.** Each mapping declares whether it is architecturally feasible for serverless / containerised / AI-pipeline targets. Mappings that are infeasible are paired with an explicitly scoped alternative or marked "no compensating control available — accept residual or redesign".

For each threat enumerated in this skill's output, the receiving `defensive-countermeasure-mapping` invocation must produce at least one D3FEND ID at two distinct defense-in-depth layers (per "Defense in depth" in Analysis Procedure step 0). Threats with only one layer of D3FEND coverage are flagged as defense-shallow and routed back to design.

---

## Hand-Off / Related Skills

- **`threat-model-currency`** — runs after this skill to score the produced model against 14 currency classes. The two skills are companion artefacts: methodology builds the model, currency keeps it fresh.
- **`defensive-countermeasure-mapping`** — receives the threat enumeration from section 4 of Output Format and produces D3FEND mitigations. Mandatory hand-off for any shipped threat model.
- **`researcher`** — dispatcher for "what skill addresses this specific threat I just enumerated?" Use when a threat in section 4 does not have an obvious skill home.
- **`zeroday-gap-learn`** — receives any threat enumerated in section 4 that has no ATLAS or ATT&CK TTP attachment. New threats feed back into the zero-day learning loop.
- **`framework-gap-analysis`** — receives any threat enumerated in section 4 that is not addressed by an existing framework control. The model exposes framework gaps as a natural by-product of cross-walk; framework-gap-analysis then runs the global EU+UK+AU+ISO+IL+JP+SG comparison.
- **`ai-attack-surface`** — runs alongside this skill when the actor inventory includes any AI agent. Produces the AI-specific TTP set that feeds the threat enumeration.
- **`mcp-agent-trust`** — runs alongside this skill when the actor inventory includes any MCP server or agent plugin. Produces the trust-boundary specification for MCP edges.
- **`rag-pipeline-security`** — runs alongside this skill when the data inventory includes any RAG corpus or vector embedding store.
