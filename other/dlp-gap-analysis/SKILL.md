---
name: dlp-gap-analysis
version: "1.0.0"
description: DLP gap analysis for mid-2026 — legacy DLP misses LLM prompts, MCP tool args, RAG retrievals, embedding-store exfil, and code-completion telemetry. Audit channels, classifiers, protected surfaces, enforcement actions, and evidence trails against modern threat reality and cross-jurisdictional privacy regimes
triggers:
  - dlp
  - data loss prevention
  - data leak
  - egress
  - exfiltration
  - data classification
  - llm dlp
  - prompt dlp
  - rag exfil
  - copilot data leak
  - data exfiltration
  - mcp tool arg dlp
  - embedding store exfil
  - clipboard ai paste
data_deps:
  - cve-catalog.json
  - cwe-catalog.json
  - d3fend-catalog.json
  - dlp-controls.json
  - framework-control-gaps.json
  - global-frameworks.json
atlas_refs:
  - AML.T0096
  - AML.T0024
  - AML.T0051
attack_refs:
  - T1567
  - T1530
  - T1213
  - T1041
framework_gaps:
  - NIST-800-53-SC-7
  - ISO-27001-2022-A.8.16
  - ISO-IEC-42001-2023-clause-6.1.2
  - HIPAA-Security-Rule-164.312(a)(1)
  - SOC2-CC7-anomaly-detection
  - NIST-800-53-SC-28
  - NIS2-Art21-incident-handling
  - UK-CAF-C1
  - AU-Essential-8-App-Hardening
rfc_refs:
  - RFC-8446
  - RFC-9458
forward_watch:
  - EU AI Office secondary legislation under EU AI Act Art 10 / Art 15 that may operationalise inference-time data-flow controls
  - ISO/IEC 42001 amendments expected 2026-2027 likely to add prescriptive data-flow guidance for AI systems
  - Microsoft Purview AI Hub, Nightfall, Netskope GenAI, Cloudflare AI Gateway feature deltas — SDK-level prompt capture coverage is the differentiator
  - MCP gateway / proxy standardisation (Anthropic enterprise MCP gateway, Portkey MCP) — tool-call argument inspection is the missing primary control
  - Quebec Law 25, India DPDPA, KSA PDPL enforcement actions naming AI-tool prompt data as in-scope personal information
cwe_refs:
  - CWE-1426
  - CWE-200
d3fend_refs:
  - D3-CSPP
  - D3-EAL
  - D3-IOPR
  - D3-NTA
  - D3-NTPM
last_threat_review: "2026-09-18"
---

# DLP Gap Analysis

## Threat Context (mid-2026)

DLP's protected surface inverted between 2024 and 2026. Crown-jewel data is no longer "rows in this database" — it is "anything that crosses an LLM context window." Legacy DLP (outbound email, web upload, USB removable media) is solved in the sense that every commercial DLP suite covers those channels and every prescriptive framework cites them. The compliance-relevant exfiltration channels of 2026 are different: free-form LLM prompts, file attachments and RAG retrievals placed into model context, MCP tool-call arguments, code-completion context windows, IDE and dev-tool telemetry, and clipboard-to-AI-tool paste. See `data/dlp-controls.json` channel entries — `DLP-CHAN-LLM-PROMPT`, `DLP-CHAN-LLM-CONTEXT`, `DLP-CHAN-MCP-TOOL-ARG`, `DLP-CHAN-CLIPBOARD-AI`, `DLP-CHAN-CODE-COMPLETION`, `DLP-CHAN-IDE-TELEMETRY` — for the catalog of modern channels.

The dominant real-world exfil pattern: an engineer pastes proprietary code, customer data, or a draft contract into an AI tool; the vendor stores the content for abuse monitoring under the published retention policy (Anthropic 30 days for trust-and-safety, OpenAI 30 days on the API, Google Workspace and Gemini Enterprise variants, Microsoft 365 Copilot retention tied to tenant settings, Meta Llama API variants); the data crosses jurisdictions. Under GDPR Art 44 (transfers to third countries), LGPD Art 33, DPDPA 2023 §16, KSA PDPL Art 29, and Quebec Law 25 §17 this is a regulated transfer, not just an internal policy issue. Microsoft Purview AI Hub, Nightfall AI, Netskope GenAI, Forcepoint AI Security, and Cloudflare AI Gateway emerged 2024-2025 to address SDK-level and gateway-level prompt egress; coverage as of mid-2026 is uneven, with the largest gaps at: (a) MCP tool-call argument inspection, (b) RAG retrieval-time classification, (c) embedding-store membership-inference and similarity exfil, (d) clipboard-to-native-AI-app paste on unmanaged devices.

41% of 2025 zero-days were AI-discovered and the same AI capability that accelerates exploit development accelerates exfil targeting — see the `ai-c2-detection` skill for PROMPTSTEAL pattern, which uses an LLM as a live intelligence analyst to prioritise what to exfiltrate. DLP cannot treat AI as a future channel: AI is the dominant 2026 channel for unstructured proprietary content.

---

## Framework Lag Declaration

| Framework | Control | What It Covers | What It Misses For AI-Era DLP |
|---|---|---|---|
| NIST 800-53 r5 SC-7 | Boundary Protection | Egress allowlisting and inspection at network boundaries. | AI provider domains (`api.openai.com`, `api.anthropic.com`, `generativelanguage.googleapis.com`, `*.openai.azure.com`, `bedrock-runtime.*.amazonaws.com`) are uniformly allowlisted; SC-7 boundary inspection cannot see prompt content under TLS 1.3 (RFC 8446) and is blind to Oblivious HTTP relays (RFC 9458). SC-7 as written does not require SDK-level prompt logging or per-identity sanctioned-business-reason allowlist entries. The real_requirement is recorded under `NIST-800-53-SC-7` in `data/framework-control-gaps.json`. |
| NIST 800-53 r5 SI-12 (referenced from `DLP-CHAN-LLM-CONTEXT`, `DLP-CHAN-IDE-TELEMETRY`) | Information Handling and Retention | Handling rules for information at rest and in transit. | Silent on retrieval-time classification enforcement against RAG corpora and silent on inference-time prompt content. |
| NIST 800-53 r5 SC-28 | Protection of Information at Rest | Encryption of stored information. | Operationalised for disks, object stores, and databases — silent on RAG corpora, embedding stores, and model-context caches that hold protected content at rest inside AI pipelines. Engineer-pasted prompts cached by the AI vendor are an at-rest surface SC-28 does not name. |
| NIST AI RMF MAP-4.1 / MEASURE-2.10 (referenced from `DLP-CHAN-LLM-PROMPT`, `DLP-CHAN-LLM-CONTEXT`) | AI risk identification and measurement | Identifies AI system risks and measurement criteria. | Voluntary, not auditable. Does not operationalise DLP at the prompt or retrieval boundary. |
| ISO 27001:2022 A.8.16 | Monitoring Activities | Monitoring of networks, systems, and applications. | Channel-agnostic in language; every implementation guide cites email/web/endpoint. No guidance for SDK-level prompt logging, MCP tool-call argument capture, or RAG retrieval audit. |
| ISO 27001:2022 A.5.34 (referenced from `DLP-CHAN-LLM-CONTEXT`, `DLP-CHAN-IDE-TELEMETRY`) | Privacy and Protection of PII | PII handling. | Does not address retrieval-time classification of PII in RAG corpora. |
| ISO/IEC 42001:2023 clause 6.1.2 | AI Risk Treatment Planning | Requires the org to plan treatments for AI risks. | Non-prescriptive on prompt-egress DLP. Auditors accept policy documents in lieu of control evidence — a compliance-theater risk. The real_requirement is recorded under `ISO-IEC-42001-2023-clause-6.1.2` in `data/framework-control-gaps.json`. |
| EU AI Act (Reg. 2024/1689) Art 10 / Art 15 | Data governance and accuracy/robustness/cybersecurity for high-risk AI | Training data governance, robustness, and cybersecurity for high-risk AI systems. | Inference-time prompt data flows are not enumerated. Cross-border transfer of prompt content interacting with EU-resident personal data is governed by GDPR Art 44, not by AI Act technical controls. |
| EU GDPR Art 44 | International transfers | Cross-border personal-data transfers require adequacy, SCCs, or BCRs. | Operationalised in DPIAs as "transfers to processors" — engineer-pastes-into-LLM is treated as an unsanctioned use, not as a measurable DLP event. Without prompt-egress evidence the org cannot answer a Subject Access Request asking "has my data been processed by AI." |
| UK Data Protection Act 2018 / UK GDPR + ICO AI guidance (Oct 2023, updated 2025) | UK transfers and AI accountability | Equivalent to EU GDPR; ICO has issued AI-specific guidance. | Same blind spot as GDPR Art 44; ICO guidance is non-statutory. |
| HIPAA Security Rule §164.312(a)(1) | Technical access controls | Access controls to ePHI. | Does not operationalise PHI flowing into LLM context windows. OCR enforcement guidance as of 2026 treats engineer-pastes-PHI-into-LLM as a reportable breach under §164.408 if the vendor lacks a BAA — but no technical DLP requirement is named. |
| Brazil LGPD Art 33 | International transfers | Cross-border data transfers. | Same operational gap as GDPR Art 44. ANPD has signalled enforcement interest in AI tools but has issued no DLP-specific guidance as of mid-2026. |
| India DPDPA 2023 §16 | Cross-border transfer | Transfer to notified countries. | DPDP Rules (draft Jan 2025, expected final 2026) name no AI-specific DLP control. |
| KSA PDPL Art 29 + Implementing Regulation 2023 | Cross-border transfer of personal data | Requires Saudi Data and AI Authority (SDAIA) approval or specified safeguards. | AI prompt content is in scope if it contains personal data; SDAIA has not issued AI-specific DLP technical guidance. |
| China PIPL Art 38-42 | Cross-border data transfer | CAC security assessment, certification, or standard contract. | LLM prompt data is in scope; PIPL enforcement against AI tools is active (2025 multi-vendor enforcement) but framed as transfer compliance, not DLP. |
| Quebec Law 25 §17 (CFR-1Q-25) | Disclosure outside Quebec | Requires Privacy Impact Assessment and notification. | CAI has issued non-binding AI guidance (2024). PIA documentation is not a DLP technical control. |
| Australia Privacy Act 1988 / APP 8 + Essential Eight (ASD ISM 2026) | Cross-border disclosure / mitigation strategies | APP 8 governs disclosure; Essential Eight names application control, restrict admin privileges, patch applications/OS. | Essential Eight does not name AI-tool egress as a mitigation. ASD ISM 2026 control set adds AI guidance but does not prescribe SDK-level prompt logging. |
| SOC 2 CC7 (anomaly detection) | System operations | Anomaly detection, incident handling. | AI API traffic typically sits in the SaaS anomaly-detection blind spot — see `SOC2-CC7-anomaly-detection` gap. |
| PCI-DSS 4.0 §3.4 | Cardholder-data rendering | PAN must be rendered unreadable. | Silent on PAN appearing in LLM prompts; payment org operational reality is that engineers paste prod queries containing PAN-shaped data into AI tools for debugging. |
| US DTSA / EU Trade Secrets Directive 2016/943 | Trade secret protection | Misappropriation remedies. | "Reasonable measures to keep secret" is the eligibility test. Pasting trade secrets into a third-party LLM that retains them for abuse monitoring can disqualify trade-secret status in subsequent litigation. No technical control named — purely a downstream legal-eligibility risk. |

**Bottom line:** no compliance framework operationalises LLM-prompt, MCP-tool-arg, RAG-retrieval, embedding-store, or code-completion-context DLP as a required, auditable, technically prescriptive control. Compliance evidence based purely on legacy SC-7, AC-2, A.8.16, or §164.312 for AI-era DLP is theater.

### Expanded jurisdictional coverage (per `data/global-frameworks.json`)

DLP via AI is fundamentally cross-jurisdictional — pasting a customer record into an AI tool transports that record across borders the moment it leaves the endpoint. The EU/UK/AU/ISO baseline is no longer sufficient; the following regimes each impose distinct cross-border data-export controls that the engineer-pastes-into-LLM pattern violates:

- **China (PIPL Art. 38-42 + DSL):** Cross-border PI export requires CAC Security Assessment (mandatory above thresholds — CII operators, processors of >1M individuals, or sensitive PI of >10k), CAC-accredited Certification, or filed Standard Contract Clauses. Prompt content containing CN-resident PI sent to a non-CN AI endpoint is in scope; the PIPL Security Assessment is the strictest triad-member globally.
- **Israel (Privacy Protection Law Amendment 13, in force 2024):** Expanded sensitive-data definitions (genetic, biometric, mental-health) and a strict adequacy-equivalent expectation for transfers. INCD methodology cross-walks to PPL for technical safeguards.
- **Switzerland (revFADP, in force 2023-09-01):** Cross-border transfer rules under FADP Art. 16-17 require recognised adequacy (FDPIC list), standard contractual clauses, or BCRs. Prompt-data export to a US-hosted AI tool requires FDPIC-aligned safeguards.
- **Japan (APPI cross-border consent Art. 28 + anonymized-information rules):** Cross-border transfer of personal data requires consent unless the recipient country is on the PPC adequacy list or maintains PPC-aligned safeguards. APPI also imposes leak notification for anonymized information that is re-identifiable — directly relevant to LLM prompts containing pseudonymised customer records.
- **South Korea (PIPA cross-border consent + Network Act):** PIPA requires explicit consent for cross-border PI transfer; PIPC has actively enforced against AI tools accepting Korean PI without consent infrastructure.
- **Hong Kong (PDPO + PCPD 2024 cross-border guidance):** Section 33 historically un-commenced; PCPD's 2024 guidance operationalises cross-border restrictions and treats AI-tool prompt processing as a transfer event for high-risk personal data.
- **Taiwan (PDPA TW):** Agency-imposed cross-border restrictions per data category; financial PI under FSC oversight has the tightest restrictions.
- **Indonesia (UU PDP 2022, in force 2024-10-17):** 72-hour breach notification + cross-border adequacy or BCR-equivalent safeguards; pasting Indonesian-resident PI into an AI tool without lawful basis is a reportable event.
- **Vietnam (Decree 53/2022/ND-CP):** Data-localization for "important data" — affects DLP rule design because in-country storage may preclude any cross-border AI tool processing of certain categories.
- **Hong Kong (HKMA TM-G-1 / SA-2):** Banking-sector data-handling requirements layer on top of PDPO; AI-tool use in financial services is subject to HKMA supervisory expectations.
- **Brazil (LGPD Art. 33-35):** Cross-border transfer requires ANPD adequacy decision, SCCs, BCRs, certifications, or specific consent. ANPD has signalled active enforcement interest in AI-tool prompt content.
- **US sub-national — NYDFS 23 NYCRR 500.15 (Encryption of NPI) + 500.11 (TPSP):** Covered entities must encrypt nonpublic information in transit and apply third-party service-provider security policies — AI-tool vendors processing NPI for covered entities are TPSPs under 500.11 and prompt content is NPI in transit under 500.15. NYDFS is the most prescriptive US sub-national regime on AI-tool data handling for financial covered entities.

A DLP gap analysis that maps only to NIST 800-53 SC-7, ISO 27001:2022 A.8.16, HIPAA §164.312, and EU GDPR Art. 44 is incomplete for any covered entity with CN, IL, CH, JP, KR, HK, TW, ID, VN, BR resident data or NYDFS covered-entity status.

---

## TTP Mapping (MITRE ATLAS v2026.09 + MITRE ATT&CK)

| ID | Source | Technique | DLP Relevance | Gap Flag — Which DLP Control Fails |
|---|---|---|---|---|
| AML.T0096 | ATLAS v2026.09 | AI Service API | Direct: prompt and completion bodies as covert exfil. The same SesameOp pattern that is a C2 channel is also a DLP exfil channel — prompts encode payloads against allowlisted AI provider domains. Cross-references `DLP-CHAN-LLM-PROMPT` and `DLP-CHAN-LLM-CONTEXT` in `data/dlp-controls.json`. | Legacy email/web/USB DLP (`DLP-CHAN-EMAIL-OUT`, `DLP-CHAN-WEB-UPLOAD`, `DLP-CHAN-USB-REMOVABLE`) sees nothing. AI-aware DLP (`DLP-CHAN-LLM-PROMPT`) is the only effective control category. SC-7 boundary controls allowlist the AI provider domain — no protocol or destination anomaly fires. |
| AML.T0024 | ATLAS v2026.09 | Exfiltration via AI Inference API | Indirect but DLP-relevant: model inversion and membership-inference attacks against embedding stores and fine-tuned models extract training-corpus content (which is itself a protected surface — see `DLP-SURFACE-TRAINING-DATA`, `DLP-SURFACE-EMBEDDING-STORE`). | No legacy DLP control category exists. Modern controls: embedding-similarity classification at retrieval boundary (`DLP-CLASS-EMBEDDING-MATCH`), differential-privacy fine-tuning, query-rate limits on inference APIs. None of these are named in any compliance framework. |
| AML.T0051 | ATLAS v2026.09 | LLM Prompt Injection | Direct: prompt-injection-induced data extraction. A malicious document in a RAG corpus or a poisoned tool output (MCP) coerces the model into emitting protected content in a subsequent response. Cross-references `DLP-CHAN-LLM-CONTEXT` and `DLP-CHAN-MCP-TOOL-ARG`. | Egress-side classification on model output catches some cases but is fundamentally retroactive. Retrieval-time classification (`DLP-SURFACE-RAG-CORPUS`) and MCP tool-call argument inspection (`DLP-CHAN-MCP-TOOL-ARG`) are the primary controls. No compliance framework names either. |
| T1567 | ATT&CK | Exfiltration Over Web Service | LLM and AI API endpoints are exactly the "legitimate web service used for exfil" pattern, pre-allowlisted in nearly every enterprise. | SC-7 sees only the destination domain (allowlisted). SDK-level prompt logging with identity binding is the only practical control. |
| T1530 | ATT&CK | Data from Cloud Storage Object | Includes vector stores and model registries — embedding stores (Pinecone, Weaviate, Qdrant, pgvector, Vertex AI Matching Engine) and model artifacts in cloud object stores are 2026's high-value crown-jewel surface. See `DLP-SURFACE-EMBEDDING-STORE` and `DLP-SURFACE-TRAINING-DATA`. | Cloud DLP scanning of object stores is mature for files but not for vector indexes — index payloads are not classifiable as files. Vector-store-native ACL audit is the practical control. |
| T1213 | ATT&CK | Data from Information Repositories | RAG corpora are exactly information repositories (SharePoint, Confluence, GitHub, Drive) ingested into vector indexes. Cross-cleared retrieval is a confused-deputy exfil channel. See `DLP-SURFACE-RAG-CORPUS`. | Repository-side ACL enforcement does not propagate to RAG context. Retrieval-time classification with user-clearance check is required (`DLP-CHAN-LLM-CONTEXT`). |
| T1041 | ATT&CK | Exfiltration Over C2 Channel | Where the C2 channel is itself an AI API (AML.T0096 overlap), exfil and C2 are the same flow. | Same gap as T1567 — boundary inspection cannot distinguish exfil from legitimate prompt content under TLS. |

---

## Exploit Availability Matrix

DLP gaps in this skill are misuse patterns and architectural blind spots, not single-vendor CVEs. No entries map to `data/cve-catalog.json`. The evidence base is incident disclosures, regulator enforcement actions, and vendor abuse-policy publications.

| Channel × Pattern | CVE? | Public Incident Reporting | KEV? | AI-Accelerated? | Vendor DLP Coverage (mid-2026) | Regulator Action To Date |
|---|---|---|---|---|---|---|
| Engineer pastes proprietary code into ChatGPT / Claude / Gemini (`DLP-CHAN-CLIPBOARD-AI`, `DLP-CHAN-LLM-PROMPT`) | No | Samsung 2023 (three reported incidents leading to internal ban); follow-on disclosures across financial services, law firms, healthcare 2024-2025; routine in incident-response retainers as of 2026 | N/A | Yes — AI-accelerated targeting (PROMPTSTEAL pattern from `ai-c2-detection` skill) | Microsoft Purview AI Hub (GA mid-2025), Nightfall, Netskope GenAI, Forcepoint AI Security ship clipboard-to-AI policy; coverage is endpoint-agent-dependent, unmanaged BYOD is a structural blind spot | EU AI Office / ICO published prompt-data-handling guidance Q4 2024; CNIL (FR) 2025 enforcement against an undisclosed insurer for engineer-pasted-PII; ANPD (BR) 2025 advisory on AI prompt content under LGPD; SDAIA (KSA) 2025 inquiry under PDPL Art 29 |
| RAG corpus cross-clearance retrieval (`DLP-CHAN-LLM-CONTEXT`, `DLP-SURFACE-RAG-CORPUS`) | No | Multiple 2024-2025 disclosures: Glean, Microsoft Copilot for M365, Notion AI — over-permissive SharePoint/Drive ACLs surfaced through enterprise search; documented in vendor security bulletins and customer post-incident reviews | N/A | Yes — RAG amplifies prior over-permissioning | Microsoft Purview Information Protection label propagation to Copilot context; Glean trust-and-permissions enforcement; Notion AI permission inheritance — feature parity uneven | OCR (HHS) opened guidance review 2025 on PHI in Copilot for healthcare tenants |
| MCP tool-call argument exfil (`DLP-CHAN-MCP-TOOL-ARG`) | No vendor CVE; see CVE-2026-30615 class in `data/cve-catalog.json` for MCP inbound trust surface | Red-team disclosures across the MCP ecosystem 2025-2026; agent observability platforms (LangSmith, Langfuse, Helicone) ship traces showing protected content in tool args | N/A | Yes — agentic workflows scale exfil automatically | Emerging only: Portkey MCP support, Anthropic enterprise MCP gateway preview, Cloudflare AI Gateway tool-arg rules. Most enterprises run MCP without any DLP gateway. | None published as of 2026-05; expected to follow EU AI Office secondary legislation |
| Code-completion context exfil (`DLP-CHAN-CODE-COMPLETION`) | No | GitHub Copilot vendor disclosures on content exclusion bypass 2024; secret-in-source telemetry 2024-2025 across Copilot, Cursor, Codeium | N/A | Yes — context windows grew 8x-32x 2024-2026 | Vendor-side: Copilot Business content exclusions, Cursor Privacy Mode, Codeium enterprise context filtering. Network-side DLP cannot see the request body under TLS pinning. | None published; trade-secret eligibility risk under US DTSA and EU Directive 2016/943 — see `data/global-frameworks.json` |
| Embedding-store membership inference (`DLP-SURFACE-EMBEDDING-STORE`) | No | Academic and red-team work 2023-2025 demonstrating membership inference against Pinecone / Weaviate / Qdrant indexes built from sensitive corpora | N/A | Yes — AI-assisted query optimisation accelerates inference attacks | None — no commercial DLP product addresses this. Mitigations are architectural (DP-SGD fine-tuning, query rate limits, k-anonymity at retrieval). | None |
| IDE / dev-tool telemetry leak (`DLP-CHAN-IDE-TELEMETRY`) | No | JetBrains / VS Code / Visual Studio crash-dump and error-report leakage cases 2022-2025 | N/A | Partial — AI-extension telemetry includes prompt previews | GPO/MDM telemetry suppression; SWG egress block on telemetry domains | None |

**Interpretation:** no patch applies because there is no vendor CVE for the *architectural* DLP gaps above. Mitigation is architectural — defense-in-depth across SDK, gateway, browser-isolation, endpoint, and egress NTA. Vendor-side contractual controls (zero retention enterprise tiers, BAAs for HIPAA, EU data residency for GDPR Art 44) are necessary but technically un-verifiable; treat as compensating controls, not primary.

### Adjacent CVE — LLM-Gateway Credential Exfiltration

**CVE-2026-42208** — BerriAI LiteLLM Proxy authorization-header SQL injection (CVSS 9.8 / CVSS v4 9.3 / CISA KEV-listed 2026-05-08, federal due 2026-05-29; in-wild exploitation confirmed). LiteLLM is the open-source LLM-API gateway used in front of agent stacks, MCP-server fronts, and multi-model proxy deployments — exactly the egress path this skill treats as the credential boundary for hosted-model use. The proxy concatenated an attacker-controlled `Authorization` header value into a SQL query in the error-logging path, so a curl-able POST against `/chat/completions` with a SQL-injection payload returns the managed-credentials DB content without prior auth. Patched in 1.83.7+; temporary workaround `general_settings: disable_error_logs: true`. DLP relevance: a compromised LiteLLM gateway hands the adversary every downstream model-provider credential plus the per-tenant routing config — every subsequent prompt/response pair routes through attacker-known credentials and the *exfiltration* channel becomes the legitimate AI-API egress that the DLP architectures above are designed to monitor. Any organisation whose DLP scope treats the LLM gateway as "just a reverse proxy" misses that the gateway is the credential-and-routing boundary that determines whether outbound LLM traffic is trustworthy at all.

---

## Analysis Procedure

The procedure threads three foundational principles before stepping through the audit.

### Principle 1 — Defense in depth

DLP for AI-era channels cannot be a single-layer control. Required layers:

1. **SDK-level prompt and completion logging with identity binding.** You cannot DLP what you cannot see. Anthropic, OpenAI, Google, Azure, and Bedrock SDKs all support audit logging; enterprise gateway products (Portkey, LiteLLM-proxy, Cloudflare AI Gateway) capture this at the wire layer. Without this layer, every downstream layer is reasoning from absence. Maps to `DLP-CHAN-LLM-PROMPT` and `DLP-CHAN-LLM-CONTEXT`.
2. **LLM / MCP gateway with policy enforcement.** Inline content classification on prompt, retrieval context, and tool-call arguments. Maps to `DLP-CHAN-MCP-TOOL-ARG` and `DLP-CHAN-LLM-PROMPT`.
3. **Managed-browser / browser-isolation prompt inspection.** Catches the paste-into-web-UI channel that bypasses the SDK. Island, Talon, Menlo, Chrome Enterprise Premium, Edge for Business. Maps to `DLP-CHAN-CLIPBOARD-AI`.
4. **Endpoint DLP with clipboard awareness and AI-tool process awareness.** Microsoft Purview Endpoint DLP, Trellix, Forcepoint. Maps to `DLP-CHAN-CLIPBOARD-AI` and `DLP-CHAN-CODE-COMPLETION`.
5. **Egress network traffic analysis (NTA) with AI-domain classification.** Detects traffic to AI provider domains and Oblivious HTTP relays. Maps to D3-NTA in `data/d3fend-catalog.json`. Detects pattern, not content.
6. **Enterprise data classification feeding all of the above.** Microsoft Purview Information Protection labels, Google Workspace classification, custom sensitivity taxonomies — propagated to RAG corpora, embedding stores, and DLP classifier dictionaries. Maps to `DLP-CLASS-REGEX-PII`, `DLP-CLASS-ML-CLASSIFIER`, `DLP-CLASS-EMBEDDING-MATCH`.

Each layer fails differently. Missing any layer is a DLP gap. Layer 1 absent = structural zero coverage on the primary AI channel. Layer 3 absent = paste-bypass on every unmanaged device.

### Principle 2 — Least privilege

DLP enforcement is at the granularity of identity × tool × data-class. Not every engineer needs to paste production data into an LLM. Not every agent needs RAG access to every corpus. Privilege scope is a control surface — record per-identity sanctioned AI-tool list, per-tool sanctioned data classes, per-agent RAG corpus allowlist with cross-clearance enforcement. The SC-7 real_requirement in `data/framework-control-gaps.json` names per-identity business-reason allowlist entries; reuse that language for the AI-tool inventory.

### Principle 3 — Zero trust

Every prompt is hostile until proven otherwise. Trust that AI vendors do not retain data is a contractual control: Anthropic, OpenAI, Google, Microsoft all publish enterprise-tier zero-retention or limited-retention terms. Technical zero-trust assumes retention until verified. Apply the same posture to MCP tool arguments, RAG retrievals, and embedding-store queries — verify with audit logs and vendor attestations, do not assume.

### Step-by-step audit

**Step 1 — Inventory AI tools in use, including Shadow AI.**

Pull from the SWG / CASB shadow-IT discovery report all destinations matching the "Generative AI" URL category for the last 90 days. Cross-reference against the sanctioned AI-tool list. Every unsanctioned destination is a finding. Specifically enumerate at minimum: `chat.openai.com`, `claude.ai`, `gemini.google.com`, `copilot.microsoft.com`, `chat.deepseek.com`, `chat.mistral.ai`, `huggingface.co/chat`, `poe.com`, `you.com`, plus any IDE-AI marketplace (Cursor, Windsurf, Codeium, Cline, Replit Agent, JetBrains AI Assistant), code-review AI (CodeRabbit, Greptile, Qodo), meeting-AI (Otter, Fireflies, Read), and any internal AI gateway.

**Step 2 — Enumerate egress channels per tool.**

For each tool from Step 1, identify which channels in `data/dlp-controls.json` apply: web UI paste (`DLP-CHAN-CLIPBOARD-AI`), API/SDK (`DLP-CHAN-LLM-PROMPT`), file attachment (`DLP-CHAN-LLM-CONTEXT`), MCP tool calls (`DLP-CHAN-MCP-TOOL-ARG`), IDE context (`DLP-CHAN-CODE-COMPLETION`), telemetry (`DLP-CHAN-IDE-TELEMETRY`). Record the matrix tool × channel.

**Step 3 — Classify protected surfaces.**

Enumerate which protected data classes can reach each tool × channel intersection: source code (and within source, secrets and proprietary algorithms), PHI, customer PII, financial / cardholder data, contract drafts, M&A materials, internal incident data, RAG corpora (which themselves contain mixed classifications), embedding stores, model weights, training datasets. Map each class to its governing regime: GDPR (EU personal data), CCPA/CPRA (CA personal info), LGPD (BR personal data), DPDPA (IN personal data), PIPL (CN personal info), KSA PDPL (KSA personal data), Quebec Law 25 (QC personal info), HIPAA (US PHI), PCI-DSS (cardholder data), DTSA + EU Directive 2016/943 (trade secrets).

**Step 4 — Map each channel × surface intersection to existing DLP controls.**

For each cell of the channel × surface matrix from Steps 2 and 3, identify which DLP controls from `data/dlp-controls.json` apply: which channel control (`DLP-CHAN-*`), which classifier (`DLP-CLASS-*`), which surface-level control (`DLP-SURFACE-*`), which enforcement action (`DLP-ENFORCE-*`), which evidence trail (`DLP-EVIDENCE-*`). Record which controls are deployed, which are deployed but not tuned for AI content, which are absent.

**Step 5 — Score gaps.**

A gap exists where:
- A channel × surface cell has no deployed control (structural zero).
- A control is deployed but `ai_pipeline_applicability` in `data/dlp-controls.json` says "not applicable" or "partial" (legacy DLP on AI channel).
- A control depends on SDK-level prompt logging that is not enabled (cascading dependency failure).
- A control depends on retrieval-time classification on a RAG corpus where labels have not propagated (cascading dependency failure).

Score each gap using the RWEP model in `lib/scoring.js`. Inputs: KEV / known-exploitation evidence (use the Exploit Availability Matrix above), AI-acceleration flag (yes for every modern channel), blast radius (per-identity vs. enterprise-wide), patch availability (architectural — not patchable, only mitigable). Output RWEP per gap. Never report a gap with CVSS alone — RWEP is the prioritization signal, with CVSS reported alongside but never as the sole input.

**Step 6 — Propose layered controls per the defense-in-depth ladder.**

For each gap, propose controls from each of the five layers in Principle 1. Do not propose a single-layer fix for a multi-layer problem. If the org cannot deploy a layer (BYOD without endpoint agent, for example), document the compensating control and the residual risk.

**Step 7 — Enforce least privilege per identity × tool × data class.**

For each sanctioned tool from Step 1, produce a per-identity entitlement: which identities are authorised, for which data classes, with what enforcement. Unsanctioned identity × tool combinations become Step-1-style policy violations. Record the entitlement in the same format as the SC-7 per-identity business-reason allowlist.

**Step 8 — Build zero-trust verifications.**

For each AI vendor in scope, verify rather than assume:
- Enterprise-tier zero-retention terms in effect (contract clause cited).
- Data residency configured per GDPR Art 44 / LGPD / PIPL / DPDPA / KSA PDPL / Quebec Law 25 requirements.
- BAA in effect for any PHI-touching tool (HIPAA).
- DPA in effect for any EU personal data (GDPR Art 28).
- SDK-level prompt logging enabled, identity-bound, 90+ day retention, SIEM-forwarded.
- MCP tool calls inspected at gateway with content policy.
- RAG retrievals logged with user clearance vs. document sensitivity-label decision recorded.

**Step 9 — Cross-jurisdictional exposure assessment.**

For every gap, identify which jurisdictions are exposed based on where personal data originates and where the AI vendor processes it. Produce a per-jurisdiction exposure note: EU (GDPR Art 44 + EU AI Act Art 10/15), UK (UK GDPR + ICO AI guidance), AU (Privacy Act APP 8 + ASD ISM 2026), IN (DPDPA §16), BR (LGPD Art 33), KSA (PDPL Art 29), CN (PIPL Art 38-42), QC (Law 25 §17), US sectoral (HIPAA, PCI-DSS, state laws CA/CO/CT/IL/NY/TX/VA).

**Step 10 — Run the compliance theater check.**

Apply the three concrete tests in the Compliance Theater Check section. Any failing test inverts the audit outcome: the framework-control claim is unsupported regardless of paper coverage.

---

## Output Format

The skill produces a DLP Gap Analysis covering per-channel coverage (email, web, endpoint, cloud-storage, LLM-prompt, RAG-retrieval), policy enforcement evidence, and the prioritized roadmap to close LLM/RAG exfiltration channels that traditional DLP misses. The shape below is consumed downstream by `ai-attack-surface` (which integrates the LLM-prompt and RAG-retrieval gaps), by `email-security-anti-phishing` (which inherits the email-egress channel findings), and by `compliance-theater` (which compares the deployed DLP channels against the org's claimed data-protection compliance). Preserve the per-channel coverage rows verbatim — they are the auditable map of where DLP enforcement actually fires.

```
## DLP Gap Analysis

**Date:** YYYY-MM-DD
**Scope:** [org units, tenants, network segments assessed]
**Frameworks in scope:** [list, including jurisdictions]

### AI Tool Inventory (Step 1)
| Tool | Sanctioned? | Identities Using | First Seen | Channel(s) |
|---|---|---|---|---|

### Channel × Surface × Control Matrix (Steps 2–4)
For each tool × channel × protected surface intersection: which DLP control applies (ID from `data/dlp-controls.json`), deployment state (Deployed / Deployed-untuned-for-AI / Absent), residual risk note.

### Gap Register (Step 5)
| Gap ID | Channel × Surface | Missing Control | RWEP | CVSS-equivalent (if used elsewhere) | Affected Identities | Affected Jurisdictions |
|---|---|---|---|---|---|---|

### Identity × Tool × Data-Class Entitlement Ledger (Step 7)
| Identity | Tool | Data Classes Permitted | Enforcement Layer | Last Reviewed |
|---|---|---|---|---|

### Zero-Trust Verification Status (Step 8)
| Vendor | Zero-retention contract? | Data residency? | BAA / DPA? | SDK prompt logging on? | MCP gateway inspection? | RAG retrieval audit? |
|---|---|---|---|---|---|---|

### Jurisdictional Exposure (Step 9)
| Jurisdiction | Regime | Exposure | Required Action |
|---|---|---|---|
| EU | GDPR Art 44 + EU AI Act Art 10/15 | … | … |
| UK | UK GDPR + ICO AI guidance | … | … |
| AU | Privacy Act APP 8 + ASD ISM 2026 + Essential Eight | … | … |
| IN | DPDPA §16 | … | … |
| BR | LGPD Art 33 | … | … |
| KSA | PDPL Art 29 | … | … |
| CN | PIPL Art 38-42 | … | … |
| QC | Law 25 §17 | … | … |
| US-HIPAA | §164.312(a)(1) + §164.408 | … | … |
| US-PCI | PCI-DSS 4.0 §3.4 | … | … |

### Prioritised Remediation Roadmap
| Priority | Gap ID | Layer (1-5) | Control to Deploy | Owner | Target Date | Compensating Control If Blocked |
|---|---|---|---|---|---|---|

### Compliance Theater Findings (Step 10)
Three test outcomes (Shadow AI inventory, sample LLM-prompt DLP event, DSAR AI-processing answer). Pass / Fail each, with evidence.

### Framework Gap Declaration
Per framework (NIST 800-53 SC-7, ISO 27001:2022 A.8.16, ISO/IEC 42001:2023 6.1.2, HIPAA §164.312(a)(1), SOC 2 CC7, plus all jurisdictional regimes above): what control exists on paper, why it does not address AI-era DLP, what real_requirement applies from `data/framework-control-gaps.json`.
```

---

## Compliance Theater Check

Apply all three tests. Any failing test inverts the audit outcome — claimed framework coverage for AI-era DLP is theater, regardless of policy documentation, regardless of attestations, regardless of auditor sign-off.

**Test 1 — Shadow AI inventory completeness.**

Ask: "List every AI tool your engineers, salespeople, marketers, recruiters, lawyers, and executives use, including the ones you have not sanctioned." If the answer is a list of sanctioned tools only — "we sanction Microsoft 365 Copilot and GitHub Copilot Business" — the answer is theater. Cross-check by pulling the SWG / CASB shadow-IT report from Step 1 of the Analysis Procedure. Every destination in the Generative AI URL category that is not on the sanctioned list is a counter-example. A 2026 enterprise typically discovers 15-40 AI tools in this gap; a "we sanction two" answer with no shadow-IT data is failing.

**Test 2 — Sample LLM-prompt DLP event existence.**

Ask: "Show me a sample DLP event from the last 90 days where an LLM prompt contained proprietary code, PII, PHI, cardholder data, contract draft, or M&A materials." If no such events exist, one of two conditions holds: (a) nothing has leaked to AI tools in 90 days at an org with engineering or sales staff — extraordinary and unlikely; (b) the org has no SDK-level or gateway-level visibility into prompt content — structural zero coverage. The 2026 baseline at any org with >50 engineers and any AI tool sanctioned is non-zero events per month. Zero events for 90 days with no visibility infrastructure is failing; zero events for 90 days with visibility infrastructure and a sample query failing to return content is also failing.

**Test 3 — DSAR / data-subject answer for AI processing.**

Ask: "A customer files a Data Subject Access Request under GDPR Art 15, LGPD Art 18, DPDPA §11, KSA PDPL Art 4, or Quebec Law 25 §27. The request asks 'has my personal data been processed by an AI tool, and if so which tools, for what purpose, with what cross-border transfer, and what is your legal basis under Art 44 / Art 33 / §16 / Art 29 / §17?' Show me the answer you would deliver in 30 days (GDPR) / 15 days (DPDPA) / 30 days (KSA) / 30 days (Quebec)." If the answer is "we cannot track that" or "we would tell the customer their data is not processed by AI" without an audit log proving it, the cross-border compliance posture is theater. The technical prerequisite is SDK-level prompt logging with identity binding from Step 5 of the Analysis Procedure — without it, no DSAR answer is defensible.

---

## Defensive Countermeasure Mapping

D3FEND v1.3.0+ countermeasure references from `data/d3fend-catalog.json`. Indicates which D3FEND defenses are the primary control category for each DLP channel.

| DLP Channel | Primary D3FEND Defense | Secondary D3FEND Defenses | Notes |
|---|---|---|---|
| `DLP-CHAN-LLM-PROMPT` | D3-IOPR (Input/Output Profiling) — SDK-level prompt inspection | D3-CSPP (Client-server Payload Profiling) — gateway-based inspection; D3-NTA (Network Traffic Analysis) — egress NTA | D3-IOPR is the irreplaceable control; without it no other layer has content visibility |
| `DLP-CHAN-LLM-CONTEXT` | D3-IOPR — retrieval-time content inspection | D3-CSPP — gateway-level context inspection; D3-FAPA (File Access Pattern Analysis) on RAG source documents | RAG retrieval-time classification with user clearance check |
| `DLP-CHAN-MCP-TOOL-ARG` | D3-CSPP — MCP gateway payload inspection on tool-call args | D3-IOPR — agent observability traces; D3-NTA — egress NTA on MCP server destinations | Emerging vendor coverage; most enterprises have no D3-CSPP equivalent on MCP today |
| `DLP-CHAN-CLIPBOARD-AI` | D3-IOPR — endpoint clipboard inspection | D3-EAL (Executable Allowlisting) — restrict which AI-tool executables can paste; D3-CSPP — managed-browser paste inspection | Endpoint agent or managed browser required; unmanaged BYOD is structural blind spot |
| `DLP-CHAN-CODE-COMPLETION` | D3-CSPP — proxy-based inspection where TLS termination feasible | D3-EAL — restrict which code-assistant binaries run; D3-IOPR — IDE-side context filtering | TLS pinning in IDE assistants makes D3-CSPP often infeasible; vendor-side contractual controls fill the gap |
| `DLP-CHAN-IDE-TELEMETRY` | D3-NTPM (Network Traffic Policy Mapping) — block telemetry domains at egress | D3-NTA — observe telemetry destinations; D3-EAL — extension allowlisting | GPO/MDM controls feed D3-NTPM allowlists |
| `DLP-CHAN-EMAIL-OUT` (legacy, for completeness) | D3-MENCR (Message Encryption) + content classification | D3-CSPP — SMTP gateway DLP | Solved domain; keep for compliance, do not over-invest |
| `DLP-CHAN-WEB-UPLOAD` (legacy, for completeness) | D3-CSPP — SWG / CASB inspection | D3-NTPM — domain allowlist; D3-NTA — flow observation | Tuned for file uploads, not free-form prompt text |
| `DLP-CHAN-USB-REMOVABLE` (legacy, for completeness) | D3-PHRA (Process Hardware Resource Access) — endpoint device control | D3-EAL — restrict process access to removable media | Solved domain |

Cross-cutting controls:

- **D3-NTA** is the primary egress defense for distinguishing AI-API destinations and Oblivious HTTP (RFC 9458) relays from generic SaaS traffic. Pair with `DLP-LAG-LEGACY-SCOPE` review — if NTA is observing only legacy categories, AI-era egress is invisible.
- **D3-NTPM** is the primary allowlist control surface. Implements the SC-7 real_requirement (per-identity sanctioned-business-reason entries) when wired to identity context.
- **D3-IOPR** is the primary content-layer defense and the single most important missing control at the typical 2026 enterprise. Maps to SDK-level prompt and completion logging.
- **D3-CSPP** is the primary gateway-layer defense. Maps to LLM gateway and MCP gateway products.
- **D3-EAL** restricts which AI-tool binaries can run on managed endpoints — the prerequisite to clipboard-DLP and code-completion controls being meaningful.

Underlying weakness classes from `data/cwe-catalog.json`: CWE-200 (Exposure of Sensitive Information to an Unauthorized Actor) is the canonical class for every AI-era DLP gap in this skill — the AI tool is the unauthorized actor either contractually (no zero-retention term), jurisdictionally (cross-border without lawful basis), or by clearance (RAG cross-clearance retrieval). CWE-1426 (Improper Validation of Generative AI Output) compounds CWE-200 in the prompt-injection-driven extraction case (AML.T0051).

---
