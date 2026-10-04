---
name: researcher
version: "1.0.0"
description: Triage entry-point for raw threat intel — researches an input across all exceptd data catalogs, RWEP-scores it, and routes the operator to the right specialized skill(s)
triggers:
  - research this cve
  - what should I do about
  - new threat
  - new advisory
  - new exploit
  - triage threat
  - where do I start
  - which skill should I use
  - threat intel triage
  - exceptd research
data_deps:
  - atlas-ttps.json
  - cve-catalog.json
  - d3fend-catalog.json
  - exploit-availability.json
  - framework-control-gaps.json
  - global-frameworks.json
  - zeroday-lessons.json
atlas_refs: []
attack_refs: []
framework_gaps: []
last_threat_review: "2026-09-09"
discovery_mode: "standalone"  # operator-reached via `exceptd brief researcher` or `exceptd ask`; not chained into any playbook's direct.skill_chain by design
---

# Researcher — Threat Intel Triage and Dispatch

This skill is the front door to the exceptd library. Operators do not always arrive with a specific downstream skill name. They arrive with raw input: a CVE number from a vendor advisory, an ATLAS technique from a red-team report, a one-line incident description from a SOC analyst, a framework control ID from an auditor finding. The researcher skill takes that raw input, anchors it in the project's data catalogs, scores it with the Real-World Exploit Priority (RWEP) model, and routes the operator to the specialized skill(s) that will actually answer the question.

---

## Frontmatter Scope

The `atlas_refs`, `attack_refs`, and `framework_gaps` arrays are intentionally empty. This skill is a dispatch layer — it routes the operator to whichever specialised skill owns the relevant TTPs and framework gaps. The routed-to skill carries the authoritative reference set; duplicating those IDs here would create a divergence surface the next time a downstream skill's mappings change. The `data_deps` list is the complete dependency declaration: every catalog the researcher reads is enumerated there.

---

## Threat Context (mid-2026)

Most security teams in mid-2026 sit on a torrent of raw threat input: CISA KEV additions, vendor advisories, ATLAS updates, red-team reports, internal SIEM alerts, framework amendment bulletins, supply-chain notices. The two failure modes are symmetric and equally damaging.

**Over-triage.** Every CVE is treated to the same depth of analysis. A Medium-severity informational-disclosure bug in a backend library gets the same Jira workflow, the same patch-window negotiation, and the same compliance ticket as Copy Fail (CVE-2026-31431, RWEP 90, CISA KEV, AI-discovered, 732-byte deterministic root, blast radius all Linux since kernel 4.14). The team spends triage hours indiscriminately and exhausts attention before reaching the items that genuinely warrant emergency live-patch.

**Under-triage.** Every CVE gets the same baseline pipeline: open Jira, assign to platform team, follow the 30-day SLA. CISA-KEV-listed AI-discovered LPEs get the same handling as a Medium WAF rule update. The 4-hour live-patch window for Copy Fail is missed because the input never escaped the standard intake.

The researcher skill sits between raw input and the specialized analytical skills. It is not itself analysis — it is dispatch. Concrete examples from the project's catalogs:

- **CVE-2026-31431 (Copy Fail) drops.** Operator asks: "what should I do about CVE-2026-31431?" Researcher surfaces from `data/cve-catalog.json`: CISA KEV listed, AI-discovered, 732 bytes, deterministic (no race condition), blast radius = all Linux ≥ 4.14, live-patch available, RWEP 90, CVSS 7.8. Routes to `kernel-lpe-triage`. Flags that the standard 30-day SI-2 window is structurally inadequate — live-patch within 4 hours.
- **CVE-2026-30615 (Windsurf MCP, local-vector RCE, CVSS 8.0 / AV:L / RWEP 35).** Operator asks: "new MCP CVE, where do I start?" Researcher cross-joins to ATLAS AML.T0010 (ML supply chain compromise) and AML.T0096 (LLM integration abuse), surfaces 150M+ combined downloads across MCP-capable assistants, routes primary to `mcp-agent-trust` and secondary to `ai-attack-surface`. Flags the v0.12.9 catalog correction: NVD-authoritative CVSS is 8.0 / AV:L (local-vector), not the initially-cataloged 9.8 / AV:N.
- **SesameOp campaign report.** Operator asks: "we are seeing strange Azure OpenAI calls from a finance host — is this anything?" Researcher recognizes the AI-as-C2 pattern from `data/zeroday-lessons.json`, maps to AML.T0096, routes to `ai-c2-detection`.
- **NIST 800-53 Rev. 6 draft published.** Operator asks: "does our gap analysis change?" Researcher routes to `skill-update-loop` for currency review, then to `framework-gap-analysis` for the specific control deltas.

Without this skill, the operator either has to know the full inventory of 41 specialized skills downstream of the researcher (researcher itself is the 42nd) and pick the right one (cognitive load that does not scale) or default to a single catch-all skill (which produces shallow output). The researcher skill is the routing layer that makes the rest of the library usable under operational pressure.

---

## Framework Lag Declaration

No compliance framework prescribes a research-and-route step between intake and analysis. The frameworks define incident handling capacity but do not operationalize the triage-skill role this dispatcher fills.

| Framework | Control | Why It Does Not Cover Researcher's Role |
|---|---|---|
| NIST 800-53 | IR-4 (Incident Handling) | Defines incident handling phases (preparation, detection/analysis, containment, eradication, recovery). Does not prescribe a structured triage layer between raw intake and the analyst's chosen analytical procedure. A team can be IR-4 compliant while still applying the same depth to every CVE. |
| NIST 800-53 | RA-3 (Risk Assessment) | Requires risk assessments at defined intervals. The researcher problem is per-input dispatch, not periodic assessment. |
| NIST 800-53 | SI-5 (Security Alerts, Advisories, and Directives) | Requires the org to receive and disseminate advisories. Says nothing about the workflow between receiving the advisory and producing a prioritized action. |
| ISO 27001:2022 | A.5.24 (Incident management planning) | Requires planning and preparation. Does not specify a routing/dispatch step against an internal skill or runbook inventory. |
| ISO 27001:2022 | A.5.7 (Threat intelligence) | Requires collection, analysis, and use of threat intelligence. Does not prescribe a per-input triage gate that anchors each input in a structured catalog before action. |
| NIS2 | Art. 23 (Incident notification) | Mandates notification timelines (24h early warning, 72h incident notification, 30d final). Does not address how an org converts a raw input into a notification-worthy classification in the first place. |
| DORA | Art. 17 (ICT-related incident management) | Mirrors NIS2 for financial entities. Same gap: timelines without a triage gate. |
| SOC 2 | CC7.3 (Incident detection) | Requires incident detection and response procedures. Generic; does not require routing logic against a specialized analytical inventory. |
| CIS Controls v8 | 17 (Incident Response Management) | Plan, train, test. No structured triage layer specified. |

The framework lag here is structural: every framework assumes a generic incident handling pipeline. None assume the org has a curated inventory of 41 specialized analytical procedures and needs a router. The researcher skill is the routing layer the frameworks do not describe.

---

## TTP Mapping

This is a routing skill. The TTP coverage of any specific output equals the TTP coverage of the downstream skill(s) it routes to. The researcher itself does not pin to a specific MITRE ATLAS or ATT&CK technique class; it indexes across all of them.

| ATLAS / ATT&CK Class | Researcher Routes To |
|---|---|
| AML.T0010 (AI Supply Chain Compromise) | `mcp-agent-trust`, `ai-attack-surface` |
| AML.T0016 / AML.T0017 (Obtain Capabilities / Develop Capabilities, AI-assisted) | `ai-attack-surface`, `kernel-lpe-triage`, `exploit-scoring` |
| AML.T0013 (Discover AI Model Ontology) | `ai-attack-surface`, `mlops-security`, `api-security` |
| AML.T0018 (Manipulate AI Model) | `ai-attack-surface` |
| AML.T0020 (Training Data Poisoning) | `ai-attack-surface`, `rag-pipeline-security` |
| AML.T0043 (Craft Adversarial Data) / AML.T0054 (LLM Jailbreak) | `ai-attack-surface`, `rag-pipeline-security` |
| AML.T0051 (LLM Prompt Injection) | `ai-attack-surface`, `mcp-agent-trust` |
| AML.T0096 (AI Service API, C2) | `ai-c2-detection` |
| ATT&CK T1068 / T1548.001 (Privilege Escalation) | `kernel-lpe-triage` |
| ATT&CK T1195.001 (Supply Chain Compromise) | `mcp-agent-trust` |
| ATT&CK T1071 / T1102 (Application Layer / Web Service C2) | `ai-c2-detection` |
| ATT&CK T1566 / T1190 (Phishing / Exploit Public-Facing App) | `ai-attack-surface` |
| Cryptographic / PQC migration | `pqc-first` |
| Compliance framework control gaps | `framework-gap-analysis`, `compliance-theater`, `global-grc` |

Reference `data/atlas-ttps.json` for the full attack-surface catalog. Reference `data/cve-catalog.json` for per-CVE TTP joins. The researcher's job is to produce the join, not to deepen any single dimension.

---

## Exploit Availability Matrix

The researcher's job is to PRODUCE this matrix from the local catalogs, not to consume a pre-computed one. For any input that resolves to a CVE, the researcher must emit:

| Factor | Source |
|---|---|
| CVSS score (for compatibility, never primary) | `data/cve-catalog.json` |
| RWEP score (primary priority signal) | `data/cve-catalog.json` (precomputed by `lib/scoring.js`) |
| CISA KEV listed? | `data/cve-catalog.json` and `data/exploit-availability.json` |
| Public PoC available? | `data/exploit-availability.json` |
| AI-accelerated discovery or weaponization? | `data/cve-catalog.json` (ai_discovered flag), `data/exploit-availability.json` |
| Active exploitation observed? | `data/cve-catalog.json`, `data/exploit-availability.json` |
| Live-patch available? | `data/cve-catalog.json` (live_patch field) |
| Reboot required to remediate? | `data/cve-catalog.json` |
| Blast radius (affected version range) | `data/cve-catalog.json` |
| Deterministic exploit (no race)? | `data/cve-catalog.json` |

If the input is not a CVE — for example, an ATLAS TTP, a vendor advisory without a CVE, or an incident narrative — the researcher emits a degenerate matrix: "N/A; this input is not a CVE. Map to ATLAS technique and downstream skill instead." No fabricated exploit availability data — theoretical-only intel is refused. If the catalog lacks the input, flag it as "not yet in catalog — propose adding" and route to `zeroday-gap-learn` for the catalog update procedure.

---

## Analysis Procedure

This is the longest section deliberately. The researcher skill is procedure-heavy by design.

### Step 1 — Classify the input

Apply string-shape rules in order. The first match wins.

- `/CVE-\d{4}-\d+/` → CVE. Canonical reference: the CVE ID.
- `/AML\.T\d{4}(\.\d{3})?/` → MITRE ATLAS TTP.
- `/^T\d{4}(\.\d{3})?$/` → MITRE ATT&CK technique.
- `/NIST-800-53-/`, `/ISO-27001-2022-/`, `/SOC2-/`, `/PCI-DSS-/`, `/NIS2-/`, `/DORA-/` → framework control ID.
- Vendor name (Cursor, Windsurf, Copilot, Anthropic, OpenAI, Linux kernel, OpenSSL) → vendor advisory. Capture the vendor and the affected technology.
- Otherwise → narrative input. Extract the technology, the attack pattern, and the impact from the prose.

Record the classification at the top of the output. Do not skip this — every downstream step depends on input class.

### Step 2 — Catalog lookup

Based on classification, search the corresponding data file:

- CVE → `data/cve-catalog.json`. If found, capture the full entry. If not found, flag as "not yet in catalog".
- ATLAS TTP → `data/atlas-ttps.json`.
- ATT&CK technique → search `attack_refs` across all skill frontmatter and `data/cve-catalog.json`.
- Framework control → `data/framework-control-gaps.json`. Pull the full gap entry.
- Vendor advisory → search `data/cve-catalog.json` for matching `vendor` or `product`, and search `data/exploit-availability.json` for live PoC references.
- Narrative → search `data/zeroday-lessons.json` for matching attack-vector keywords, and `data/atlas-ttps.json` for matching TTP descriptions.

Surface the full entry. Quote field values directly from the catalog. Do not paraphrase.

### Step 3 — RWEP scoring

If the input is a CVE present in `data/cve-catalog.json`, the RWEP score is already computed. Surface it. The CVSS score is reported alongside for compatibility (see `lib/scoring.js`), never as the primary signal.

If the input is a CVE not yet in catalog, compute RWEP per `lib/scoring.js` formula and flag the entry for addition to `data/cve-catalog.json`. The formula factors: CISA KEV (0.25), public PoC (0.20), AI-assisted weaponization (0.15), active exploitation (0.20), patch availability (-0.15), live-patch availability (-0.10), blast radius (0.15). Output the RWEP score with the factor breakdown so the operator can audit the score.

If the input is not a CVE, RWEP is not applicable. State that explicitly: "RWEP is a per-CVE score; this input is a [TTP / framework control / narrative] and RWEP does not apply directly."

### Step 4 — Cross-catalog joins

For a CVE, perform these joins:

- Related ATLAS TTPs via the `atlas_refs` field on the CVE entry. Pull the technique descriptions from `data/atlas-ttps.json`.
- Related framework gaps via the `framework_gaps` field on the CVE entry. Pull the full gap rationale from `data/framework-control-gaps.json`.
- Corresponding zero-day lessons entry in `data/zeroday-lessons.json` (keyed by CVE ID). If present, surface the full attack-vector → control-gap → framework-gap → new-control-requirement chain. If absent, flag that the zero-day learning loop has not yet been run for this CVE and route to `zeroday-gap-learn`.
- Live exploit availability in `data/exploit-availability.json` (PoC URLs, weaponization status, last_verified date).

For an ATLAS TTP, perform the reverse join: which CVEs in `data/cve-catalog.json` reference this TTP, and which skills declare it in `atlas_refs`.

For a framework control, perform: which CVEs in `data/cve-catalog.json` reference this control as a gap, and which skills declare it in `framework_gaps`.

### Step 5 — Global-jurisdiction surface

Every threat must be evaluated against at least the following jurisdictions (global-first, not US-centric): EU (NIS2, DORA, EU AI Act, EU CRA), UK (NCSC CAF, Cyber Essentials Plus), Australia (ISM, ASD Essential 8, APRA CPS 234), and ISO 27001:2022. Look up the jurisdiction-specific obligations in `data/global-frameworks.json`. Surface:

- EU: which NIS2 / DORA / EU AI Act / EU CRA articles apply, and what notification timelines they impose.
- UK: which CAF outcome the threat maps to.
- Australia: which Essential 8 mitigation strategy is in scope, and whether APRA CPS 234 is triggered for regulated entities.
- ISO 27001:2022: which Annex A control IDs are relevant.
- US (NIST 800-53, NIST AI RMF, NIST CSF 2.0): for completeness, not as the primary jurisdiction.

If the operator's organization operates only in one jurisdiction, surface that jurisdiction first but never omit the others. US-only analysis is incomplete.

### Step 6 — Route to specialized skill(s)

Use this mapping. Pick one primary route and zero-or-more secondary routes.

- Kernel CVE / LPE / page-cache exploit / live-patch question → `kernel-lpe-triage`
- AI / LLM / model CVE or attack / prompt injection / RAG / model poisoning / phishing AI-acceleration → `ai-attack-surface`
- MCP / agent-trust CVE / tool manifest signing / IDE coding assistant security → `mcp-agent-trust`
- RAG / vector store / embedding attack / retrieval filter bypass → `rag-pipeline-security`
- LLM-API-as-C2 / SesameOp / PROMPTFLUX / PROMPTSTEAL / covert channel via AI API → `ai-c2-detection`
- Cryptographic algorithm / PQC concern / ML-KEM / ML-DSA / SLH-DSA / HNDL / crypto migration → `pqc-first`
- Compliance framework control gap question → `framework-gap-analysis`
- "Are we compliant but exposed?" / audit-passing-but-vulnerable question → `compliance-theater`
- RWEP / prioritization / CVSS-band question / "is this a real risk" → `exploit-scoring`
- Multi-jurisdiction GRC question / NIS2 / DORA / EU AI Act / CRA / CAF / Essential 8 / MAS TRM / CERT-In → `global-grc`
- Zero-day learning loop runner / "what control gap enabled this" → `zeroday-gap-learn`
- Ephemeral / serverless / AI pipeline exception / ZTA / no-reboot patching exception → `policy-exception-gen`
- "Is our threat model current?" / threat model currency review → `threat-model-currency`
- Implementation roadmap question / MVP-Practical-Overkill tiers / "where do we start" → `security-maturity-tiers`
- Skills currency / ATLAS update / CISA KEV update / framework amendment → `skill-update-loop`
- Pen-test / attack-surface / red-team / TIBER-EU / DORA TLPT scoping question → `attack-surface-pentest`
- Fuzz / fuzzing / OSS-Fuzz / syzkaller / AI-augmented fuzz / continuous-fuzz compliance question → `fuzz-testing-strategy`
- DLP / data-leak / LLM-prompt-egress / RAG-exfil / clipboard-AI / code-completion-leak / cross-border-data-processing-via-AI question → `dlp-gap-analysis`
- Supply chain / SBOM / SLSA / VEX / CSAF / Sigstore / in-toto / AI-codegen provenance / model-weight integrity question → `supply-chain-integrity`
- "What controls counter this attack?" / D3FEND mapping / defensive coverage / defense-in-depth audit / least-privilege validation / zero-trust posture audit → `defensive-countermeasure-mapping`
- Identity assurance / authentication / federation / passkey / NIST 800-63 / AAL question / agent-as-principal identity question → `identity-assurance`
- OT / ICS / SCADA / PLC / NIST 800-82 / IEC 62443 / NERC CIP / IT-OT convergence / AI-augmented HMI question → `ot-ics-security`
- CVD / VDP / bug bounty / ISO 29147 / ISO 30111 / CSAF advisory / security.txt / regulator-mandated disclosure (EU CRA / NIS2) question → `coordinated-vuln-disclosure`
- Threat model question / STRIDE / PASTA / LINDDUN / Kill Chain / Diamond Model / Unified Kill Chain / AI-system threat model question → `threat-modeling-methodology`
- Web application security / OWASP Top 10 / OWASP ASVS / web vulnerability class question (CSRF, SSRF, SQLi, XSS, path traversal, command injection) / AI-generated webapp code question → `webapp-security`
- AI governance / AI risk management / ISO 23894 process / ISO 42001 management system / NIST AI RMF / EU AI Act high-risk obligation / AI impact assessment question → `ai-risk-management`
- Healthcare cyber / HIPAA / HITRUST / HL7 FHIR / medical device cyber / FDA SaMD / EU MDR cyber / PHI in LLM / AI clinical decision support question → `sector-healthcare`
- Financial cyber / banking cyber / DORA TLPT / PSD2 SCA / SWIFT CSCF / NYDFS 23 NYCRR 500 / FFIEC / MAS TRM / APRA CPS 234 / TIBER-EU / CBEST question → `sector-financial`
- Federal cyber / government cyber / FedRAMP / CMMC / EO 14028 / NIST 800-171 CUI / FISMA / M-22-09 Zero Trust / OMB M-24-04 AI / CISA BOD/ED question → `sector-federal-government`
- Energy cyber / electric grid cyber / NERC CIP / TSA pipeline / AWWA water / EU NCCS-G / AESCSF / DER cyber / inverter security / smart meter cyber question → `sector-energy`
- Telecom / 5G core / Salt Typhoon / Volt Typhoon / SS7 / Diameter / GTP / lawful intercept / CALEA / FCC CPNI / O-RAN / GSMA NESAS / 3GPP TS 33.501 question → `sector-telecom`
- API security / OWASP API Top 10 / BOLA / BFLA / mass assignment / GraphQL / gRPC / WebSocket / API gateway / rate limit policy question → `api-security`
- Cloud security / CSPM / CWPP / CNAPP / CSA CCM / AWS / Azure / GCP / shared responsibility / workload identity / cloud IAM question → `cloud-security`
- Container security / Kubernetes / CIS K8s Benchmark / Pod Security Standards / Kyverno / Gatekeeper / Falco / Tetragon / admission policy / NetworkPolicy question → `container-runtime-security`
- MLOps security / training data integrity / model registry / model signing / drift detection / MLflow / Kubeflow / Vertex AI / SageMaker / Hugging Face question → `mlops-security`
- Incident response / IR playbook / PICERL / NIST 800-61 / ISO 27035 / breach notification / BEC incident / AI-class incident handling question → `incident-response-playbook`
- Ransomware incident / encryption event / LockBit / ALPHV / Akira / RansomHub / Hunters International / ransom payment / OFAC sanctions screening / decryptor availability question → `ransomware-response`
- Cloud-IAM incident / AWS account takeover / GCP service-account compromise / Azure managed-identity replay / access-key leak / IAM role-assumption abuse / cross-account assume-role / IMDS SSRF / CloudTrail anomaly question → `cloud-iam-incident`
- IdP incident / Okta / Entra ID / Auth0 / Ping / OneLogin tenant compromise / federated-trust abuse / OAuth consent abuse / SAML-OIDC token forgery / Midnight Blizzard / Scattered Spider question → `idp-incident-response`
- Email security / anti-phishing / SPF / DKIM / DMARC / BIMI / ARC / MTA-STS / BEC / vishing / deepfake / AI-augmented phishing question → `email-security-anti-phishing`
- Age gate / age verification / age assurance / child online safety / COPPA / CIPA / California AADC / UK Children's Code / KOSA / GDPR Art. 8 / DSA Art. 28 / parental consent / CSAM detection question → `age-gates-child-safety`

Multiple routes are common and expected. A new MCP CVE routes to `mcp-agent-trust` (primary), `ai-attack-surface` (secondary, for the broader surface impact), and `exploit-scoring` (secondary, if the RWEP needs explanation). State primary vs. secondary explicitly in the output.

### Trigger collisions and dispatch fan-out

Several triggers in `manifest.json` legitimately resolve to more than one skill. The researcher does not pick one and discard the other — it emits an ordered dispatch list. The policy:

- **PROMPTSTEAL / PROMPTFLUX** route to BOTH `ai-attack-surface` AND `ai-c2-detection`. This is intentional fan-out, not a collision to resolve. `ai-attack-surface` produces the attack-class analysis (the offensive characterization, the prompt-injection mechanics, the LLM-integration abuse surface per AML.T0051 / AML.T0096); `ai-c2-detection` produces the detection-engineering response (the telemetry signatures, the egress patterns, the SIEM/EDR rule shape). The researcher emits BOTH skills as the answer to a PROMPTSTEAL/PROMPTFLUX query, ordered by the phase of the operator's question — analysis-first if the operator is scoping the threat, detection-first if the operator is hunting active intrusion. Multi-jurisdiction note: PROMPTSTEAL-class C2 over commercial AI APIs implicates EU NIS2 Art. 23 notification, DORA Art. 17 for financial entities, and ICO / CNIL guidance on AI-API data egress under GDPR Art. 32.
- **"compliance gap"** routes primary to `framework-gap-analysis` (the analytical depth: which control, which version, which jurisdiction, which gap). `compliance-theater` is the natural secondary if the gap analysis reveals the control exists on paper but is structurally inadequate for current TTPs. Researcher emits `framework-gap-analysis` FIRST and recommends `compliance-theater` as the secondary when the operator's framing is "we 'comply' but..." (the scare quotes are the tell). Global-first applies: gap analysis always spans EU + UK + AU + ISO 27001:2022 alongside US references.
- **"defense in depth"** routes primary to `defensive-countermeasure-mapping` (the structural D3FEND mapping: which defensive technique on which layer, which least-privilege scope, which zero-trust verification gate). `security-maturity-tiers` is the secondary if the operator is asking "where on the MVP-Practical-Overkill maturity curve does this control sit?" — `defensive-countermeasure-mapping` first to establish the structural mapping, `security-maturity-tiers` second to place it on the maturity axis. EU CRA Annex I essential-cybersecurity-requirements framing is relevant for product-side defense-in-depth questions; NIST CSF 2.0 Protect function and ISO 27001:2022 A.8.* controls are the cross-jurisdiction anchors.
- **"zero trust"** disambiguates the same way: `defensive-countermeasure-mapping` for "what verification controls implement ZT for this attack class?", `policy-exception-gen` for "we cannot implement full ZT in our ephemeral/serverless/AI-pipeline environment — how do we document the exception with compensating controls for an environment where some controls are architecturally impossible?". The first question is structural, the second is exception-management. Researcher routes by which framing the operator used. Cross-jurisdiction note: NIST SP 800-207 is the US ZT anchor; UK NCSC ZT design principles and EU ENISA ZTA guidance are the parallel references and must be surfaced if the operator's jurisdiction is non-US.

When the researcher emits a fan-out or a primary/secondary pair, the Output Format's "Routed to" block lists Primary first, then each Secondary on its own line with its one-line rationale. Operators run skills in the emitted order unless they have a specific reason to deviate.

### Step 7 — Synthesize

Produce the Output Format below. Keep it to one page. The point of the researcher is to compress the catalog evidence into a routable summary, not to reproduce the downstream skills' depth.

---

## Output Format

The skill produces a Researcher Triage Report that converts a free-form research query (CVE ID, threat-actor name, framework reference, RFC number, vendor advisory) into a structured triage: canonical identifier, threat-currency assessment, the skill(s) that own follow-on analysis, and the suggested next operator action. The shape below is consumed downstream by `exceptd dispatch` (which routes to matching skills) and by the operator's investigation queue. Preserve the canonical-reference field verbatim — it is the load-bearing field for downstream skill chaining.

```
# Researcher Triage Report — <input>

## What this is
<one-line classification + canonical reference>
Example: "CVE — Linux kernel LPE. Canonical: CVE-2026-31431 (Copy Fail)."

## RWEP-anchored priority
RWEP: <score> / 100   CVSS: <score> (for compatibility, not primary)
Drivers: <CISA KEV: yes/no> | <Public PoC: yes/no> | <AI-discovered/AI-accelerated: yes/no> | <Blast radius: scope> | <Live-patch: available/unavailable> | <Reboot required: yes/no>
Determinism: <deterministic / probabilistic with race> | Exploit size: <bytes or LOC if known>
Catalog status: <full entry present | partial | not yet in catalog — propose adding>

## Exploit availability matrix
| Factor                       | Value |
|------------------------------|-------|
| CVSS                         | <x.y> |
| RWEP                         | <0-100> |
| CISA KEV                     | <yes/no, listing date if yes> |
| Public PoC                   | <yes/no, source if yes> |
| AI-assisted                  | <yes/no, dimension if yes> |
| Active exploitation          | <yes/no/suspected> |
| Patch available              | <yes/no, date if yes> |
| Live-patch available         | <yes/no, vehicle if yes> |
| Reboot required              | <yes/no> |
| Blast radius                 | <affected version range> |

## Cross-catalog joins
- ATLAS TTPs: <AML.Txxxx list with one-line descriptions>
- ATT&CK techniques: <Txxxx list>
- Framework gaps: <control IDs with one-line gap descriptions>
- Zero-day lessons entry: <present in zeroday-lessons.json | absent — must run zeroday-gap-learn>

## Routed to
Primary: skills/<name> — <one-line reason>
Also relevant: skills/<name>, skills/<name> — <one-line reasons>

## Global jurisdiction angle
EU: <NIS2 / DORA / EU AI Act / EU CRA articles + notification timelines>
UK: <NCSC CAF outcome + Cyber Essentials Plus relevance>
AU: <Essential 8 strategy + APRA CPS 234 trigger if regulated>
ISO 27001:2022: <Annex A control IDs>
US (for context): <NIST 800-53 control IDs + NIST AI RMF function if AI-related>

## Next actions
1. Invoke <primary skill> with input <canonical reference>.
2. If the catalog lacks this entry, open a data update PR following the project's "Adding a New CVE" procedure.
3. <Operator-specific action: live-patch within 4h / disable feature / update detection rules / etc.>
4. If notification thresholds tripped (NIS2 24h early warning, DORA, etc.), start the regulatory clock now.
```

The report fits on one page when rendered. Anything longer belongs in the downstream specialized skill's output, not here.

---

## Defensive Countermeasure Mapping

The researcher skill is dispatch, not analysis — but every dispatched finding lands in a downstream skill where a defensive countermeasure must be selected. The mapping below names the D3FEND techniques the researcher recommends the downstream skill include in its output. Each entry pulls from `data/d3fend-catalog.json`.

| D3FEND Technique | Researcher Trigger | Defense-in-Depth Layer | Rationale |
|---|---|---|---|
| **D3-IOPR** (Input/Output Profiling Resource) | Input is a CVE / advisory describing AI-API surface, RAG retrieval, MCP tool response, or prompt-injection path. | Detect | Per-call inspection of model inputs and outputs is the foundational signal for prompt-injection class findings the researcher routes to `ai-attack-surface` or `rag-pipeline-security`. Without IOPR baseline, downstream skills have no source for their detection rules. |
| **D3-NTA** (Network Traffic Analysis) | Input is an AI-API anomaly, SesameOp-class C2 narrative, or any AML.T0096 reference. | Detect | The egress baseline the dispatcher recommends `ai-c2-detection` build first. Per-identity model-API and MCP-server egress profiling is the prerequisite for every downstream AI-as-C2 finding. |
| **D3-CAA** (Credential Access Auditing) | Input mentions an MCP server, OAuth-flow CVE, agent bearer-token reuse, or AML.T0010 supply chain. | Detect | The post-hoc evidence stream when the dispatcher routes to `mcp-agent-trust`, `identity-assurance`, or `supply-chain-integrity`. Without CAA, the downstream skill cannot reconstruct what a compromised credential touched. |
| **D3-EHB** (Executable Hash-based Allowlist) | Input is a supply-chain CVE / advisory (npm worm, PyPI malware, model-registry compromise). | Harden | Hash-pinning is the canonical counter to the AML.T0010 / T1195.001 pattern across `supply-chain-integrity`, `mcp-agent-trust`, and `mlops-security`. The dispatcher names it so the downstream skill does not re-derive the harden layer from first principles. |
| **D3-PA** (Process Analysis) | Input is a kernel LPE, container-escape, or post-exploitation narrative. | Detect | The auditd / eBPF / EDR layer that `kernel-lpe-triage`, `container-runtime-security`, and `incident-response-playbook` all depend on. RWEP-90 LPE inputs route here before live-patch consideration. |

Defense-in-depth posture: the researcher's job is to recommend the **first** D3FEND layer the downstream skill should produce evidence against. Subsequent layers are the downstream skill's responsibility. No orphaned controls: every D3FEND mapping above resolves to a real ATLAS or ATT&CK TTP enumerated in the TTP Mapping section.

---

## Compliance Theater Check

The compliance theater test for the researcher skill is itself a meta-test: does the operator's existing triage process treat all inputs at the same depth, anchored on CVSS bands?

> "Pull your last 30 days of vulnerability and threat-intel tickets. Bucket them by your current triage outcome: Critical, High, Medium, Low. Now overlay each one with the corresponding RWEP score from `data/cve-catalog.json` and the CISA KEV status and the AI-discovery flag. How many of your 'Critical' tickets are RWEP ≥ 85 and CISA KEV listed? How many of your 'Medium' tickets are RWEP ≥ 85 and CISA KEV listed but happened to land at CVSS 7.x? If any Medium-bucket ticket is a CISA-KEV-listed AI-discovered LPE, your triage process is CVSS-band theater. The control nominally exists (you triage every input) but the prioritization is anchored on a severity metric, not a risk metric. CVSS is severity, not risk."

A second, complementary test:

> "Open your incident response runbook and your security skills inventory. When a new CVE drops, what is the documented step between 'CVE arrives in inbox' and 'analyst starts work'? If the answer is 'analyst reads the CVE and decides', the routing is implicit and varies by analyst. If the answer is 'analyst runs the researcher skill, gets a routed dispatch report, then runs the named downstream procedure', the routing is explicit and reproducible. The former is IR-4-compliant theater. The latter is operational."

An org running structured RWEP-based triage with documented routing to a curated analytical inventory is not in theater. An org running "every CVE gets a Jira ticket, severity equals CVSS band, SLA equals 30 days" is in theater for any CISA-KEV-listed AI-discovered LPE in its environment — the control exists on paper, the prioritization mechanism is structurally inadequate for the threat class. The researcher skill is the corrective. The compliance theater check is whether the operator is using it (or an equivalent) or relying on a CVSS-band shortcut that misses the inputs that matter most.
