---
name: sector-financial
version: "1.0.0"
description: Financial services cybersecurity for mid-2026 — EU DORA TLPT, PSD2 RTS-SCA, SWIFT CSCF v2026, NYDFS 23 NYCRR 500, FFIEC CAT, MAS TRM, APRA CPS 234, IL BoI Directive 361, OSFI B-13; Threat-Led Pen Testing schemes TIBER-EU + CBEST + iCAST
triggers:
  - financial security
  - banking security
  - dora
  - psd2
  - psd3
  - sca
  - strong customer authentication
  - swift cscf
  - nydfs
  - 23 nycrr 500
  - ffiec
  - mas trm
  - apra cps 234
  - tiber-eu
  - cbest
  - icast
  - tlpt
data_deps:
  - cve-catalog.json
  - d3fend-catalog.json
  - dlp-controls.json
  - framework-control-gaps.json
atlas_refs:
  - AML.T0096
  - AML.T0013
attack_refs:
  - T1078
  - T1190
  - T1486
  - T1567
framework_gaps:
  - PSD2-RTS-SCA
  - SWIFT-CSCF-v2026-1.1
  - NIST-800-53-AC-2
  - SOC2-CC6-logical-access
  - NIS2-Art21-incident-handling
  - UK-CAF-A1
  - AU-Essential-8-MFA
rfc_refs:
  - RFC-8446
  - RFC-7519
  - RFC-8725
  - RFC-9421
cwe_refs:
  - CWE-287
  - CWE-862
  - CWE-863
  - CWE-798
  - CWE-352
d3fend_refs:
  - D3-MFA
  - D3-CBAN
  - D3-NTA
  - D3-IOPR
forward_watch:
  - PSD3 + PSR (Payment Services Regulation) trilogue and final adoption (expected 2026-2027); track agent-initiated payment treatment in final text
  - DORA Art. 26 TLPT first full cycle completion mid-2027; ESAs publishing aggregate findings under JC 2024/40 RTS
  - SWIFT CSCF v2027 (annual update cycle); track AI-mediated message generation controls
  - NYDFS 23 NYCRR 500 further amendments; track agentic-AI in CISO certification scope
  - FFIEC CAT replacement by CRI Profile v2 (Cyber Risk Institute) — US sector baseline migration
  - MAS Notice 655 / TRM Guidelines refresh tracking GenAI in financial services
  - HKMA CFI 3.0 cycle and iCAST scope expansion to AI/ML systems
  - APRA CPS 230 (Operational Risk Management) effective 2025-07-01 — operational resilience overlay on CPS 234
  - UK FCA / PRA operational resilience self-assessment cycle (SS1/21, SS2/21) and impact tolerances refresh post-2025
  - BCB Resolução BCB 85 (cyber policy for FIs) and Brazil PIX fraud-typology updates
  - OSFI B-13 (Technology and Cyber Risk Management) post-2024 examination findings
  - TIBER-EU framework v2.0 alignment with DORA TLPT RTS (JC 2024/40); cross-recognition with CBEST and iCAST
last_threat_review: "2026-09-18"
---

# Sector — Financial Services Cybersecurity (mid-2026)

## Threat Context (mid-2026)

Financial services is the most-regulated sector for cybersecurity globally and the regulation cadence is accelerating, not slowing. As of mid-2026 every Tier-1 bank, payments processor, broker-dealer, insurer, and significant financial-market infrastructure operates under multiple binding cyber regimes simultaneously. The threat landscape that drives those regimes has shifted materially since 2023.

**Regulatory state of play (mid-2026).**

- **EU DORA** has been in force since 2025-01-17. The first round of TLPT (Threat-Led Penetration Testing) under DORA Art. 26 + RTS JC 2024/40 is mid-cycle; designated financial entities run TLPT every 3 years. Register-of-information submissions under Art. 28 are operational. ESAs are issuing aggregated supervisory feedback. The TIBER-EU framework is the implementation vehicle for most jurisdictions; cross-recognition with UK CBEST and HK iCAST is partial.
- **PSD2** + RTS-SCA (Commission Delegated Regulation (EU) 2018/389) remains the binding payments security baseline. **PSD3 + PSR** (Payment Services Regulation) — trilogue concluded late-2025 with final text expected mid-to-late 2026 — extends scope to include non-bank payment service providers and tightens fraud-liability and SCA exemption rules. Agent-initiated payment treatment in PSD3/PSR is the open political question.
- **SWIFT CSCF v2026** (Customer Security Controls Framework, annual update) is the binding baseline for all SWIFT-connected institutions globally; v2026 introduced refinements to mandatory control 1.1 (SWIFT environment protection) and tightened audit-evidence requirements but did not address LLM-assisted operations on the secure zone.
- **NYDFS 23 NYCRR 500 Second Amendment** phased in through November 2025: enhanced CISO reporting, mandatory annual independent assessment, expanded incident reporting (24-hour cyber-event notification, 72-hour ransom-payment notification, written explanation within 30 days), Class A company designation with elevated controls.
- **FFIEC Cybersecurity Assessment Tool (CAT)** was sunset for new use in mid-2024; the **Cyber Risk Institute (CRI) Profile v2.x** built on NIST CSF 2.0 is becoming the de-facto US sector baseline. FFIEC IT Examination Handbook remains the binding supervisory reference.
- **MAS TRM Guidelines** (Singapore) most recent update 2021 with supplementary circulars 2024-2025; **MAS Notice 655** (Cyber Hygiene Notice) binds DSIBs and locally-incorporated banks since 2019. MAS 2-hour notification SLA is among the fastest in the world.
- **UK FCA + PRA operational resilience** (PS21/3, SS1/21, SS2/21) requires impact-tolerance setting for important business services; self-assessment cycle ongoing. **CBEST** is the BoE/PRA TLPT scheme for systemically-important UK financial entities.
- **AU APRA CPS 234** (Information Security) is the binding cyber prudential standard; **APRA CPS 230** (Operational Risk Management) effective 2025-07-01 layers operational-resilience requirements on top.
- **JP FISC Security Guidelines v9** series is the de-facto banking technical baseline referenced by JFSA; major banks operate against FISC v9.x as binding.
- **IL Bank of Israel Banking Supervision Directive 361** (2024 revision) is one of the world's strictest banking cyber regimes — Director-General-level accountability, prescriptive technical controls, cross-references INCD methodology.
- **CA OSFI B-13** (Technology and Cyber Risk Management, effective 2024-01-01) is the binding cyber/tech risk regime for federally-regulated financial institutions; sits alongside OSFI B-10 (third-party risk).
- **BR BCB** Resolução BCB 85 (2021) and successor circulars are the binding cyber regime for BCB-supervised institutions; Brazil's instant-payment system (PIX) has driven a parallel fraud-typology regulatory track.
- **FR ACPR + Banque de France**, **DE BaFin**, **ES Banco de España + AEPD** all operate national overlays beneath DORA — for example BaFin BAIT (Bankaufsichtliche Anforderungen an die IT) and VAIT (insurance), ACPR's cyber notification circulars, BdP's CMVM cyber requirements. DORA does not replace these national overlays; it stacks on top.

**Threat reality driving the rule-making.**

The financial sector ransomware position has shifted. 2024-2026 saw ransomware actors throttle direct attacks on the largest banks (operational-resilience controls, segmentation, faster IR) and pivot to two more productive vectors:

1. **Financial supply chain compromise.** Snowflake customer-credential abuse (2024) hit AT&T, Ticketmaster, Santander; CDK Global ransomware (2024) shut down a third of US auto-dealer financing; MOVEit (2023) cascaded into hundreds of financial-services downstream. Pure-play financial-targeted supply-chain attacks: ION Trading (LockBit, 2023), Ivanti VPN exploitation in financial sector (2024), and continuing 2025-2026 targeting of fintech-adjacent SaaS (loan-origination platforms, KYC verification services, payment gateways).
2. **AI-augmented fraud against retail and commercial banking.** Voice-cloning + deepfake video defeating remote KYC: Hong Kong UOB deepfake-CFO wire transfer (USD 25.6M, January 2024) is the public reference case; documented at scale through 2025 against private-banking onboarding, business-email-compromise wire transfers, and account-takeover via help-desk social engineering. Deepfake-resistant liveness detection is supplier-fragmented.

**Agentic AI is the emerging structural problem.** Banking copilots — both bank-supplied (Erica, Eno, Alexa-for-Bank-of-America-class assistants) and customer-supplied (operator's own ChatGPT/Copilot/Gemini agents acting on behalf of the customer) — are now initiating transactions. RTS-SCA contemplates two principals: the customer and the PISP (payment initiation service provider, regulated). It does not contemplate an autonomous AI agent acting under loosely-scoped delegated authority. Mid-2026 sees three real cases in production:

- bank-supplied conversational interfaces with transaction-initiation tool-use (read balance → propose transfer → execute on SCA confirmation)
- customer-supplied autonomous agents (LangChain / OpenAI Assistants / Anthropic computer-use class) that hold session credentials and initiate transactions
- enterprise-treasury AI agents initiating B2B payments under delegated CFO authority, frequently across SWIFT or domestic RTGS rails

In all three, the SCA evidence chain (the customer's authenticated session, the bank-side audit trail of MT/MX message origin) is fully compliant on paper. **Injected intent — prompt injection that causes an agent to send a payment the customer did not want — produces a SCA-compliant audit trail.** RTS-SCA, SWIFT CSCF v2026, MAS Notice 655, NYDFS 500.12, APRA CPS 234 paragraph 27 — all are silent on this failure mode.

**Threat-Led Penetration Testing convergence.** TIBER-EU (the EU's TLPT framework, formally adopted by ECB 2018, now the implementation vehicle for DORA Art. 26), UK CBEST, HK iCAST, AU AESCSF red-team activities, and DORA TLPT proper (JC 2024/40 RTS) are converging methodologically. Mutual recognition is the political objective for 2026-2027; mid-2026 reality is that a multinational bank may need to run TIBER-EU once per primary EU jurisdiction, CBEST once for UK, iCAST once for HK, and bilateral pen-tests for AU/JP/SG — same scope, different documentation, different supervisors. Skill `attack-surface-pentest` covers method; this skill scopes the regulatory mapping.

---

## Framework Lag Declaration

| Framework | Control | Designed For | Fails Because |
|---|---|---|---|
| EU DORA + RTS JC 2024/40 (TLPT) | Threat-Led Penetration Testing every 3 years for designated entities (Art. 26) | Pen testing against current adversary TTPs for systemically-important financial entities | Scenario libraries lag adversary capability 12-18 months. Agent-initiated payment threats are not in TIBER-EU TT&Ps inventory as of mid-2026. AI-augmented social engineering (voice clone, deepfake video) scenarios exist but rule-of-engagement constraints often exclude them as "out of scope for technical TLPT." Frequency (every 3 years) is well-matched to deep red-team; mismatched to rapid AI-driven TTP evolution. |
| EU PSD2 RTS-SCA (Reg. 2018/389) | Two-of-three-factor Strong Customer Authentication for electronic payments | Customer + PISP transaction initiation | Silent on agent-as-initiator. Captured in `data/framework-control-gaps.json#PSD2-RTS-SCA`. Prompt-injection-induced transactions present a fully SCA-compliant audit trail because the customer's session authenticated; injected intent is invisible to the SCA evidence chain. PSD3/PSR draft does not yet close this; final text expected 2026-2027. |
| SWIFT CSCF v2026 | Mandatory and advisory controls for SWIFT-connected institutions; control 1.1 (SWIFT Environment Protection) is the secure-zone foundation | Messaging integrity + operator authentication | Captured in `data/framework-control-gaps.json#SWIFT-CSCF-v2026-1.1`. Silent on LLM-assisted MT/MX drafting, AI-API egress from administrative jump zones, and AI-mediated reconciliation/sanctions tooling. SWIFT publishes annually; AI-on-CSCF guidance is forward-watched. |
| US NYDFS 23 NYCRR 500 (Second Amendment, phased to Nov 2025) | Comprehensive cybersecurity program for NY-regulated financial entities (banks, insurers, broker-dealers) | Risk-based cybersecurity program + CISO accountability + incident reporting (24h cyber event, 72h ransom payment) | Method-neutral on penetration testing under 500.5; does not name agentic-AI as a covered system. Class A designation thresholds capture size but not AI-pipeline complexity. CISO annual certification is paper-attested unless paired with independent technical evidence. Privileged-access requirements (500.7) cover human accounts; AI-agent service accounts are treated as conventional service accounts when they are not. |
| US FFIEC IT Examination Handbook + CRI Profile v2.x | Examiner reference for US banks; risk-based maturity profile mapped to NIST CSF 2.0 | Comprehensive IT/cyber examination across US banking sector | FFIEC CAT sunset 2024; CRI Profile is voluntary maturity self-assessment. Examiners increasingly cite CRI Profile but it is not binding. No AI-specific dimension; AI risk treated under existing NIST CSF 2.0 Govern / Identify pillars without sector-specific TTPs. |
| MAS TRM Guidelines (2021) + MAS Notice 655 (Cyber Hygiene) + Notice 644 | Technology risk management and cyber hygiene baseline for SG-regulated financial institutions | Mature, prescriptive technical baseline for SG FIs | TRM 2021 predates GenAI deployment at scale; MAS supervisory circulars 2024-2025 fill some gaps but TRM main document is stale on agentic AI. 2-hour notification SLA is operationally tight; tabletop-tested rarely. |
| UK FCA + PRA operational resilience (PS21/3, SS1/21, SS2/21) | Important Business Service mapping, impact tolerance setting, severe-but-plausible scenario testing | Cross-firm operational resilience post-2021 | Severe-but-plausible scenarios in mid-2026 still over-index on classical IT outage; AI-supply-chain or agentic-AI-mediated fraud scenarios under-represented. CBEST scenarios (the TLPT layer) close some of this for systemic entities. |
| AU APRA CPS 234 + CPS 230 (effective 2025-07-01) | Information security obligations + operational risk and resilience | AU-regulated prudential entities (banks, insurers, super funds) | CPS 234 information-security control objectives are sound; AI-system classification under "information assets" is undocumented. CPS 230 layers operational resilience but is silent on AI-specific operational scenarios. 72-hour APRA notification (para 26) is reasonable but does not require AI-channel disclosure in the notification structure. |
| JP FISC Security Guidelines v9.x | Detailed technical security guidelines for JP banks and financial institutions | JP financial-sector technical baseline; de-facto JFSA-referenced | Most prescriptive sector guideline globally on conventional IT but slow on AI integration. FISC v9 supplementary materials cite AI under outsourcing/third-party risk; no AI-specific cyber control set. |
| IL Bank of Israel Banking Supervision Directive 361 (2024 revision) | Cyber defense management for IL banks | IL banking sector; cross-references INCD methodology | One of the strictest banking cyber regimes globally; AI-specific extension references INCD AI guidance without Directive-361-native AI controls. |
| CA OSFI B-13 (effective 2024-01-01) | Technology and Cyber Risk Management for federally-regulated financial institutions | CA FRFI cyber/tech risk regime | Principle-based; specifies expectations but leaves operationalisation to the FRFI. AI/ML model risk is in B-13 scope as a technology risk; cyber controls specifically for AI agents are not yet articulated. |
| BR BCB Resolução BCB 85 + Resolução CMN 4893 (cyber policy) | BR-regulated FI cyber policy and incident reporting | BR banking and payments sector; PIX-fraud-typology overlay | BR cyber policy is principle-based; PIX-specific fraud-typology rules (Circular 3978 AML overlay) close some retail-payments gaps. Agentic-AI in PIX initiation is forward-watched. |
| FR ACPR + Banque de France | National financial-cyber overlay beneath DORA | FR FIs under ACPR supervision | DORA stacks on top; ACPR retains national notification and supervisory authority. Operational under DORA from 2025-01-17. |
| DE BaFin BAIT + VAIT | Bankaufsichtliche Anforderungen an die IT (banks) / Versicherungsaufsichtliche (insurance) | DE financial-cyber baseline | DORA-aligned but retains national specificity; BaFin examinations cite BAIT/VAIT alongside DORA. |
| HK HKMA CFI 2.0 + iCAST + TM-G-1 | HK Authorized Institution cyber baseline + intelligence-led red-team | HK banking sector | C-RAF 2.0 maturity assessment + iCAST red-team is substantive and tier-calibrated; AI cyber specifics gap noted in HKMA GenAI Circular 2024. |
| NZ RBNZ BS11 / RBNZ guidance | NZ-regulated FI outsourcing and cyber | NZ banking sector | Outsourcing-focused; cyber-specific guidance is principle-based and trails AU APRA. |
| AE CBUAE Cyber + UAE SCA + DFSA + FSRA | UAE federal banking cyber + free-zone (DIFC/ADGM) financial-cyber regimes | UAE conventional, DIFC, and ADGM financial sectors | Fragmented across federal + free-zone regimes; AE NESA Information Assurance Standards apply alongside. |
| SA SAMA Cyber Security Framework (CSF) | KSA-regulated FI cyber baseline; tier-calibrated maturity | KSA banking and insurance sectors | SAMA CSF is prescriptive technically; AI-specific extension forward-watched. |
| IN SEBI Cybersecurity and Cyber Resilience Framework + RBI Master Direction (IT, Cyber Security) | IN-regulated capital markets (SEBI) and banks (RBI) | IN financial sector | Recently strengthened (RBI Master Direction April 2024); AI-specific provisions limited. |
| ISO 27001:2022 + ISO/IEC 27017 (cloud) + ISO/IEC 27018 (cloud PII) | Generic ISMS for financial entities | Organisation-level ISMS | A.5.16 (identity management) and A.8.5 (secure authentication) cross-walk to SCA but do not name agent-initiation. A.5.23 (cloud services) generic; financial-sector cloud risk not specifically addressed. |
| SOC 2 Trust Services Criteria (CC6 logical access) | Service-organisation logical access controls | Audit attestation for service organisations | Captured in `data/framework-control-gaps.json#SOC2-CC6-logical-access`. Logical-access criteria treat the authenticated session as the access boundary; injected intent within an authenticated AI-agent session is invisible. |

**Cross-jurisdiction posture (global-first, not US-centric).** Any financial-sector gap analysis for a multi-jurisdiction institution must cite at minimum: EU DORA + PSD2 (transitioning to PSD3/PSR) + RTS-SCA + national overlays (BaFin BAIT/VAIT, ACPR, BdP, Banca d'Italia, AEPD, ENISA), UK FCA + PRA operational resilience + CBEST, AU APRA CPS 234 + CPS 230 + AESCSF, JP FISC v9 + JFSA, SG MAS TRM + Notice 655 + Notice 644, HK HKMA CFI 2.0 + iCAST + TM-G-1, IL BoI Directive 361 + INCD, CA OSFI B-13 + B-10, BR BCB Resolução 85, AE CBUAE + DFSA + FSRA, SA SAMA CSF, IN SEBI + RBI Master Direction, NZ RBNZ BS11, alongside SWIFT CSCF v2026, NYDFS 23 NYCRR 500 (for any NY-connected entity), ISO 27001:2022 + ISO/IEC 27017/27018, and SOC 2. US-only (FFIEC, NYDFS, NIST CSF) is incomplete.

---

## TTP Mapping

| Surface | TTP | Matrix | Variant in mid-2026 | Gap Flag |
|---|---|---|---|---|
| Customer account credential reuse → ATO | T1078 — Valid Accounts | ATT&CK Enterprise | Snowflake-class credential database compromise; help-desk social-engineering with deepfake-voice | PSD2 RTS-SCA covers payment SCA; account-takeover via help-desk channel bypasses SCA entirely. CWE-287 (Improper Authentication) and CWE-863 (Incorrect Authorization) are the underlying weakness classes. |
| Internet-banking / treasury portal exploit | T1190 — Exploit Public-Facing Application | ATT&CK Enterprise | Ivanti VPN, MOVEit-class file-transfer, web-portal SSRF, JWT validation flaws (RFC 8725 best-current-practice violations) | DORA Art. 6-15 ICT risk-management requirements general; CWE-862 (Missing Authorization) and CWE-352 (CSRF) common findings; SWIFT CSCF v2026 covers SWIFT zone, not customer-facing portals |
| Ransomware against banking infrastructure | T1486 — Data Encrypted for Impact | ATT&CK Enterprise | LockBit-class, BlackBasta, ALPHV/BlackCat residuals 2024-2026; double-extortion + regulatory-threat-of-disclosure | NYDFS 500.17 ransom-payment notification (72h) + DORA major-incident reporting (Art. 19, 24h initial) + APRA CPS 234 para 26 (72h) — notification cadences harmonising slowly; ransom-payment legality fragmented (NYDFS reporting only, OFAC sanctions-screening, EU sanctions overlay) |
| Data exfiltration including LLM-channel | T1567 — Exfiltration Over Web Service | ATT&CK Enterprise | LLM API egress (OpenAI, Anthropic, Google) as covert channel; AI-coding-assistant context leaks; KYC-document upload to consumer-grade AI | DLP controls in `data/dlp-controls.json` apply; SWIFT CSCF v2026 1.1 segregation assumption violated when AI-API egress crosses administrative jump zone |
| AI-as-covert-C2 in trading / treasury systems | AML.T0096 — Use AI for C2 Communications | ATLAS v2026.09 | Steganographic encoding in trading-assistant prompts; LLM response decodes operator instructions; multi-agent covert relay in market-making bots | No ATT&CK Enterprise mapping; ATLAS v2026.09 names the technique but no financial-sector-specific detection. SOC tooling rarely monitors trading-system AI tool-use. |
| Fraud-detection model extraction | AML.T0013 (Discover AI Model Ontology) | ATLAS v2026.09 | Adversarial probing of card-not-present fraud models; chargeback-pattern fingerprinting; transaction-monitoring threshold discovery via test transactions | Fraud-model lifecycle governance under MAS TRM / OSFI B-13 / NYDFS 500.13 (asset management) — model-extraction probes are not classified as a cyber event in most institutions |
| Hard-coded credentials in financial mobile / API clients | CWE-798 | CWE | Mobile-banking apps shipping API keys; partner-integration API tokens checked into Git; treasury-management-system local config | PSD2 RTS-SCA covers customer SCA, silent on partner-API credential hygiene; SWIFT CSCF 5.1/5.2 covers credential management for SWIFT users only |
| Agent-initiated payment via prompt injection | (No native TTP — closest: T1078 + AML.T0051) | ATT&CK + ATLAS | LLM agent with payment-initiation tool-use receives injected instruction via email / document / web content; transaction executes under customer's authenticated session | RTS-SCA evidence chain is fully compliant; injected intent invisible. Captured in `data/framework-control-gaps.json#PSD2-RTS-SCA`. |
| AI-generated SWIFT MT/MX message draft poisoning | (No native TTP — closest: T1565 + AML.T0051) | ATT&CK + ATLAS | LLM-assisted operator drafting tool produces subtly-wrong beneficiary BIC or amount; reviewer fatigue lets it pass 4-eyes principle | Captured in `data/framework-control-gaps.json#SWIFT-CSCF-v2026-1.1`. |
| Deepfake-mediated SCA bypass / KYC bypass | T1556 — Modify Authentication Process (closest) | ATT&CK Enterprise | Voice-clone defeating remote-KYC liveness; deepfake-video defeating high-value-transaction step-up | RTS-SCA "inherence" factor (biometric) implementation-dependent; liveness-detection vendor-fragmented. CWE-287 underlying weakness. |

**Note on TTP coverage.** ATT&CK Enterprise does not yet have a financial-sector matrix (unlike ATT&CK for ICS). ATLAS v2026.09 covers AI-specific techniques. The gap between (a) the customer's authenticated session and (b) the AI agent's injected intent within that session is not currently named in either matrix — this is a tracked gap in `forward_watch`.

---

## Exploit Availability Matrix

| Surface / CVE Class | CVSS | RWEP | CISA KEV | PoC Public | AI-Discovered | Active Exploitation | Patch Available | Live-Patchable | Sector-Aware Detection |
|---|---|---|---|---|---|---|---|---|---|
| Financial supply-chain credential abuse (Snowflake / similar SaaS) | n/a (config-class) | high (operationally exploited 2024-2026) | n/a | Documented at scale | n/a | Confirmed mass exploitation | Configuration hardening (MFA enforcement, network policy) | n/a | Vendor-side telemetry; CSPM if integrated |
| Web-facing financial portal CVEs (Ivanti / MOVEit class) | varies (often 9.0+) | varies (KEV-listed entries high) | Multiple entries (Ivanti 2024, MOVEit 2023, Citrix NetScaler 2023) | Yes | Increasing | Confirmed in financial-sector breaches | Yes — vendor patches | Limited — appliance reboot windows constrained | EDR + WAF + network telemetry |
| AI-augmented BEC / deepfake-voice wire fraud | n/a (social engineering) | high (USD 25.6M HK UOB case 2024 as public reference) | n/a | Demonstrated at scale | n/a (AI is the weapon) | Confirmed ongoing 2024-2026 | Mitigation only — out-of-band callback, AI-channel-aware liveness | n/a | Specialised liveness vendors; fragmented |
| Agent-initiated payment via prompt injection | n/a (design class) | risk-modelled, not CVSS | n/a | Demonstrated in 2025 research and red-team engagements | n/a | Suspected in 2025-2026 advanced campaigns; under-reported due to SCA-compliant audit trail | Mitigation only — agent-scope tokens, out-of-band confirmation, AI-channel audit | n/a | LLM-aware fraud telemetry — almost never deployed |
| Fraud-detection model extraction | n/a | risk-modelled | n/a | Research demonstrations | n/a | Suspected; difficult to detect | Mitigation only — query-rate-limiting, output perturbation, model-watermarking | n/a | Model-monitoring telemetry — vendor-fragmented |
| SWIFT CSCF v2026 1.1 violations via AI-API egress | n/a | risk-modelled | n/a | Demonstrated in 2025 red-team | n/a | Suspected | Mitigation — DLP on jump-zone egress, AI-API explicit deny | n/a | DLP + egress telemetry |
| HMI / treasury-workstation Linux LPE (Copy Fail CVE-2026-31431) where deployed | 7.8 | 90 | Yes (2026-05-01, due 2026-05-15) | Yes — 732-byte script | Yes | Confirmed | Yes | Yes (kpatch/livepatch) on supported distros | EDR if deployable |

**Honest gap statement (catalog coverage is not exhaustive).** Vendor-specific financial-sector CVEs (core-banking platform CVEs, payment-gateway CVEs, broker-dealer trading-platform CVEs, SWIFT Alliance Access CVEs) are not exhaustively inventoried in `data/cve-catalog.json`. The authoritative sources are: vendor advisories (Temenos, Finastra, FIS, Fiserv, Jack Henry, Murex, Calypso, Bloomberg, Refinitiv, SWIFT KB), CISA KEV for cross-sector exposure, and sector-specific intel feeds (FS-ISAC, FI-ISAC EU). Forward-watched.

---

## Analysis Procedure

This procedure threads the three foundational design principles (defense in depth, least privilege, zero trust) through every step.

**Defense in depth.** Multi-layer authentication for high-value transactions: AAL3 / FIDO2 device-bound passkey at customer layer (skill `identity-assurance`); 4-eyes principle on payment release; SWIFT CSCF 4.1/4.2 password management plus 5.1 logical access; CSCF 1.1 secure-zone segregation; network segmentation (D3-NI) between internet-banking, core-banking, treasury, SWIFT zone, fraud-detection; transaction monitoring (D3-NTA) at multiple layers (host, network, application, payment-message); model-output review for AI-mediated transactions; out-of-band confirmation for any AI-agent-initiated payment above scoped threshold.

**Least privilege.** Per-service-account scoping (CWE-863 default-permissive role assignments are the dominant failing); SWIFT 4-eyes principle on every payment release; vendor-API tokens scoped to specific operations + amounts + counterparties + time windows; AI-agent transaction tokens scope-limited per delegated-authority attestation (PSD3/PSR forward-looking — see `data/framework-control-gaps.json#PSD2-RTS-SCA`); admin accounts on SWIFT secure zone segregated from administrative jump zone; fraud-detection model query-rate-limiting per-principal.

**Zero trust.** Every transaction re-authenticated, not session-trusted; agentic-AI-initiated payments require ENHANCED authentication (out-of-band confirmation), not relaxed authentication; vendor remote access per-action verified (just-in-time credentialing); AI-assistant outputs treated as untrusted content until cross-checked against deterministic source (transaction-confirmation channel, customer step-up); fraud-model decisions logged with explanation for post-hoc review.

### Step 1 — DORA Art. 26 TLPT scoping (where applicable)

For EU-regulated entities designated under DORA Art. 26 (and TIBER-EU jurisdictions):

- Confirm designation status with the lead competent authority (per Member State).
- Pull last TLPT report; identify scope (which critical or important functions tested), threat-intelligence provider, red-team provider, replay/rerun gates.
- Validate against JC 2024/40 RTS scope: critical or important functions, all critical ICT third-party service providers in scope.
- Flag if last TLPT predates major AI integration (banking copilot, agentic payments, AI fraud detection model swap) — scope is stale.
- Cross-walk to CBEST (UK), iCAST (HK), AESCSF red-team (AU) if entity is multi-jurisdictional. Mutual recognition is partial; do not assume one report satisfies all.

### Step 2 — PSD2 RTS-SCA evidence audit + agent-initiation gap

For all payment-related entities:

- Pull RTS-SCA compliance evidence per payment channel (card, account-to-account, instant payment, treasury initiation).
- Validate SCA element pairing: knowledge + possession + inherence two-of-three; biometric implementation per RFC-grade or vendor-attested standard.
- Validate dynamic linking (RTS Art. 5) on every transaction: amount + payee bound into the SCA confirmation; replay-resistant.
- Run the **agent-initiation question**: which transaction channels accept input from AI agents (bank copilot, customer-supplied agent, treasury-management automation)? For each, what is the delegated-authority attestation? Per `data/framework-control-gaps.json#PSD2-RTS-SCA`, document the absence of an agent-initiation construct as an open finding even if RTS-SCA evidence is otherwise complete.
- Cross-walk to UK FCA SCA-RTS and AU CDR authentication where applicable.

### Step 3 — SWIFT CSCF v2026 self-attestation gap analysis

For SWIFT-connected institutions:

- Pull the most recent KYC-SA (Know Your Customer - Security Attestation) submission.
- Validate mandatory controls 1.1, 1.2, 2.1, 2.2, 2.3, 4.1, 4.2, 5.1, 5.4, 6.4, 7.1, 7.2 as a minimum (CSCF v2026 mandatory baseline; advisory controls assessed separately).
- Per `data/framework-control-gaps.json#SWIFT-CSCF-v2026-1.1`: audit AI-API egress from SWIFT secure zone or administrative jump zone, LLM-assisted MT/MX drafting tools, AI reconciliation/sanctions tools. Document each AI integration's trust boundary.
- Flag any "100% compliant" attestation that does not name AI integrations as a theater risk (see Theater Test 3).

### Step 4 — NYDFS 23 NYCRR 500 Class A / standard institution check

For NY-regulated entities:

- Identify Class A designation status (Section 500.1(d) — 1B+ in revenue from NY business + 20K+ employees globally, broadly).
- Validate CISO annual certification (Section 500.17): independent assessment, identified risk-based areas of non-compliance, remediation plan.
- Validate 24-hour cyber-event notification + 72-hour ransom-payment notification readiness.
- Audit privileged access (500.7) coverage of AI-agent service accounts — most institutions classify AI service accounts as conventional service accounts, which is structurally insufficient.

### Step 5 — Ransomware resilience tabletop (multi-jurisdictional notification)

- Tabletop a ransomware scenario hitting a critical-or-important function (DORA term) / important business service (UK FCA term) / critical ICT service (APRA, MAS term).
- Time every regulator-notification clock: DORA Art. 19 (24h initial classification, 72h initial report, 1-month final), NYDFS 500.17 (24h cyber event, 72h ransom payment), APRA CPS 234 para 26 (72h material incident), MAS Notice 644/655 (1h notification of relevant cyber incident; 24h system unavailability), HKMA (within 24h), OSFI B-13 (24h significant incident), FCA (without delay), BoI Directive 361 (defined by impact).
- Document ransom-payment decision authority pre-incident; map OFAC + EU + UK sanctions screening obligations on the payment processor.
- Validate IR playbook against `data/cve-catalog.json` entries with ransomware-precursor relevance (Copy Fail CVE-2026-31431 LPE, Dirty Frag CVE-2026-43284, MOVEit-class file-transfer, Ivanti VPN, Citrix NetScaler).

### Step 6 — Fraud-detection model adversarial-resilience audit

- Pull current fraud-detection model architecture, training data refresh cadence, drift-monitoring posture.
- Per AML.T0013 (Discover AI Model Ontology): test the institution's ability to detect model-probing — incremental test transactions, threshold-discovery patterns, chargeback-pattern fingerprinting. If detection is "manual review of false-positive rate trends only," the model is functionally undefended against probing.
- Validate model retraining cadence: monthly or faster for high-velocity surfaces (card-not-present); quarterly is theater for any adversary-evolving surface (see Theater Test 4).
- Cross-walk to OSFI E-23 (Enterprise-Wide Model Risk Management) and SR 11-7 equivalents.

### Step 7 — Agentic-AI transaction policy audit

- Enumerate every AI integration that can directly or indirectly initiate a transaction:
  - bank-supplied conversational interface with payment tool-use
  - customer-supplied agents (third-party AI agents holding session credentials)
  - enterprise treasury AI agents under delegated CFO authority
  - vendor-supplied AI features inside core-banking / treasury-management / trading platforms
- For each, document: delegated-authority attestation, scope token (amount, counterparty, frequency, time window), out-of-band confirmation gate, prompt + completion + tool-call logging, kill switch.
- If no policy exists, this is the single largest open structural gap in mid-2026 financial cyber.

### Step 8 — Deepfake / voice-clone fraud-channel audit

- Inventory remote-KYC + step-up-authentication channels using biometric inherence (voice, face).
- Validate liveness detection vendor + version + last false-accept-rate / false-reject-rate test against adversarial generation tooling.
- Help-desk social-engineering channel: validate out-of-band callback policy + voice-channel deepfake-resistant verification + transaction-history-question fallback.

### Step 9 — Third-party / supply-chain risk per DORA Art. 28-30 and equivalents

- Pull register of information per DORA Art. 28 (ICT third-party service providers supporting critical or important functions); validate completeness against actual third-party landscape.
- Validate critical-ICT-TPP classification + concentration risk + exit strategy.
- Cross-walk to OSFI B-10, APRA CPS 234 + CPS 230 (operational risk management), MAS TRM third-party section.
- Use companion skill `supply-chain-integrity` for technical SBOM/SLSA/CSAF evidence; this skill scopes the regulatory mapping.

### Step 10 — Compliance Theater Check (see dedicated section below for concrete tests)

---

## Output Format

The skill produces a Financial Sector Cybersecurity Posture Assessment covering EU DORA Art. 6-15 + RTS coverage, UK FCA / PRA SS2/21, US NYDFS 23 NYCRR 500 (Nov 2025 amended), AU APRA CPS 234 + CPG 235, SG MAS TRM, HK HKMA SA-2 / TM-G-1, JP FISC, BR BCB, and the BEC / wire-fraud exposure. The shape below is consumed downstream by `incident-response-playbook` (for the DORA 4h initial-notification clock), by `email-security-anti-phishing` (for BEC exposure), and by `global-grc` (for cross-jurisdictional financial rollup). Preserve the per-regulator obligation rows verbatim — they are the auditable evidence for incident-classification timing.

Produce this structure verbatim:

```
## Financial Sector Cybersecurity Posture Assessment

**Assessment Date:** YYYY-MM-DD
**Institution / Entity:** [name]
**Regulatory exposure:** [EU DORA / UK FCA+PRA / US NYDFS / AU APRA / SG MAS / HK HKMA / IL BoI / CA OSFI / JP FISC / BR BCB / ...]
**Critical or important functions in scope:** [list per DORA Art. 8 / equivalent]

### DORA Register of Information Snapshot (where applicable)
| ICT Third-Party | Service | Critical/Important Function Supported | Concentration Risk | Exit Strategy | Last Assessment |

### PSD2 RTS-SCA Evidence Pack
| Payment Channel | SCA Elements | Dynamic Linking | Exemption Use | Agent-Initiation Policy | Gap (per framework-control-gaps#PSD2-RTS-SCA) |

### SWIFT CSCF v2026 Self-Attestation Gaps
| Control | Mandatory/Advisory | Attested Compliant | Evidence Currency | AI-Integration Conduit Documented | Gap (per framework-control-gaps#SWIFT-CSCF-v2026-1.1) |

### NYDFS 23 NYCRR 500 CISO Certification Readiness
| Section | Class A Applicable | Evidence Status | Independent Assessment Currency | AI-Agent Service Accounts in Scope |

### FFIEC / CRI Profile v2.x Scorecard (US examined entities)
| NIST CSF 2.0 Function | CRI Profile Score | Examiner Finding History | AI Dimension Documented |

### TLPT Status (TIBER-EU / DORA Art. 26 / CBEST / iCAST / AESCSF red-team)
| Jurisdiction | Scheme | Last Test Date | Scope | Threat Provider | Red Team Provider | Mutual Recognition Status |

### Multi-Jurisdiction Notification SLA Matrix
| Regulator | Notification SLA | Last Tabletop Date | Pre-Decision Authority Documented |

### Agentic-AI Transaction Surface Inventory
| AI Surface | Bank-Supplied / Customer / Treasury / Vendor | Transaction Authority Scope | Delegated-Authority Attestation | Out-of-Band Confirmation | Kill Switch |

### Fraud-Detection Model Adversarial-Resilience Posture
| Model | Retraining Cadence | Drift Monitoring | Probing Detection | Last Adversarial Test |

### Deepfake / Voice-Clone Channel Defense
| Channel | Liveness Vendor / Version | Last FAR/FRR Test | Out-of-Band Fallback |

### Cross-Jurisdiction Framework Gap Summary
[Per-jurisdiction reconciliation — EU DORA + national overlays + UK + AU + SG + HK + IL + CA + JP + BR + AE + SA + IN + NZ + ISO 27001 + SOC 2 + SWIFT CSCF]

### Compliance Theater Findings
[Outcome of the four tests in the Compliance Theater Check section]

### Defensive Countermeasure Plan (D3FEND)
[D3-MFA, D3-CBAN, D3-NTA, D3-IOPR — concrete control placements by surface]

### Priority Remediation Actions
1. ...
2. ...
3. ...

### RWEP-Prioritised CVE Exposure
[Financial-sector-relevant CVEs ranked by RWEP, not CVSS; see `exploit-scoring` skill for recalculation]
```

---

## Compliance Theater Check

Run all four tests. Any "fail" is a theater finding documented with the evidence (or absence thereof).

**Theater Test 1 — TIBER-EU / CBEST / iCAST scenario currency.**
Ask: "Show me the TLPT scenario from your last cycle, the threat-intelligence inputs, the red-team report, and the remediation tracker."

- If the answer is "we did a TIBER-EU in 2022 and we're due in 2025-2026": the test pre-dates banking copilot deployment, agentic payment surfaces, and 2024-2026 supply-chain TTPs. Scope is stale.
- If the scenario library does not include AI-augmented social engineering (voice clone, deepfake video) or agent-initiated payment via prompt injection: scope is incomplete against current adversary capability.
- If the remediation tracker is "all closed" but the next TLPT has not started: closure validation against re-exploitation is theater.
- Acceptable: TLPT within the last 3 years, scenario library refreshed against current AI-augmented TTPs, remediation tracker explicitly retests closed findings before claiming closure.

**Theater Test 2 — PSD2 SCA evidence for AI-agent-initiated transactions.**
Ask: "What is your PSD2 SCA evidence for transactions initiated by an AI agent acting on behalf of the customer — whether your own conversational interface or a third-party agent holding the customer's session?"

- If the answer is "all transactions go through SCA so they're compliant": this is the dominant theater answer. RTS-SCA evidence is fully satisfied by the customer's authenticated session; injected intent is invisible. Per `data/framework-control-gaps.json#PSD2-RTS-SCA`, document this as an open finding.
- If the answer is "we don't allow AI agents to initiate transactions": validate against the actual product surface. Conversational interfaces with transfer tool-use exist at most large retail banks in mid-2026. The policy "no AI initiation" without the technical control is theater.
- Acceptable: documented agent-initiation policy with scoped delegated-authority tokens, out-of-band confirmation for any agent-initiated payment above a threshold (the threshold itself documented and defensible), AI-channel audit indicator on every agent-mediated transaction.

**Theater Test 3 — SWIFT CSCF v2026 attestation completeness.**
Ask: "Show me your SWIFT CSCF v2026 self-attestation. For each control attested compliant, name the AI integrations that touch the SWIFT secure zone or its administrative jump zone — LLM-assisted message drafting, AI reconciliation, AI sanctions screening, vendor copilot features in SWIFT Alliance Access or Alliance Web Platform."

- If the answer is "100% compliant" but no AI integrations are named: per `data/framework-control-gaps.json#SWIFT-CSCF-v2026-1.1`, the attestation is silent on a real attack surface. The "100% compliant" claim is paper completeness, not actual coverage.
- If AI-API egress from administrative jump zones is allowed without explicit allowlist + DLP + monitoring: CSCF 1.1 segregation assumption is violated regardless of attestation.
- Acceptable: attestation explicitly names AI integrations, documents their trust boundaries, names the DLP control on jump-zone egress, and includes the AI-mediated message-drafting review gate before MT/MX release.

**Theater Test 4 — Fraud-detection model retraining cadence vs adversary capability.**
Ask: "What is your fraud-detection model retraining cadence, drift-monitoring cadence, and adversarial-testing cadence? When did adversaries last successfully evade your model in production?"

- If the answer is "quarterly retraining, manual drift review, no adversarial testing": this is theater against any AI-augmented fraud adversary. Mid-2026 adversary capability evolves on a 2-4 week cycle for AI-augmented BEC and on a continuous cycle for card-not-present fraud-pattern adaptation.
- If "we don't know when adversaries last successfully evaded": detection of evasion is the missing control. Successful evasions show up as chargeback-volume drift weeks later, not as fraud-system alerts.
- Acceptable: monthly-or-faster retraining for high-velocity surfaces, continuous drift monitoring with alerting, scheduled adversarial-resilience testing (AML.T0013 detection), retrospective audit of evasion patterns from chargeback / customer-complaint signal.

---

## Defensive Countermeasure Mapping

Maps financial-sector offensive findings to MITRE D3FEND IDs from `data/d3fend-catalog.json`, with explicit defense-in-depth layer position, least-privilege scope, zero-trust posture, and AI-pipeline applicability.

| D3FEND ID | Technique | Layer Position | Least-Privilege Scope | Zero-Trust Posture | AI-Pipeline Applicability |
|---|---|---|---|---|---|
| D3-MFA | Multi-Factor Authentication | Customer-facing channel (AAL3 / FIDO2 device-bound passkey for high-value); employee-facing channel (FIDO2 for SWIFT operator, treasury, admin); vendor remote access | Per-principal MFA enrolment; phishing-resistant factors mandatory for any payment-authority principal | Every authentication event verified, not session-trusted; step-up for high-value and AI-agent-initiated transactions | Applicable to human principals. AI-agent service accounts need a distinct attestation construct (scope token + delegated-authority assertion) — D3-MFA conceptually extends but PSD2 RTS-SCA does not yet name it (see framework gap). |
| D3-CBAN | Credential-Based Authentication | Application + API layer for customer credentials; SWIFT secure-zone operator credentials; vendor-API tokens; AI-agent service-account credentials | Per-credential scope (amount, counterparty, time window) for agent tokens; per-operator-role for SWIFT operators; CWE-798 prohibition on hard-coded credentials in code | Credential issuance just-in-time where feasible; credential rotation per documented cadence; credential leakage detection at egress and on public-code-search surfaces | Applicable. AI-agent credentials need scope-token construct beyond conventional CBAN; PSD3/PSR forward-looking. |
| D3-NTA | Network Traffic Analysis | Network boundary (internet ↔ customer-facing portal); inter-zone boundary (customer-facing ↔ core-banking); SWIFT secure-zone boundary; administrative jump zone egress; AI-API egress | Operator alerting scoped to operator's zone; SOC aggregated visibility | Network-hostile-until-proven posture; AI-API egress explicitly allowlisted at administrative jump zone | Applicable. AI-API egress monitoring is the specific gap: DLP-aware NTA is required to detect AI-channel exfiltration (T1567) per `data/dlp-controls.json`. |
| D3-IOPR | Input / Output Pattern Recognition | Application layer (transaction monitoring); fraud-detection model layer; AI-channel inspection (prompt + completion + tool-call) | Transaction-pattern detection per customer; model-probing detection per principal; AI-channel inspection per integration | Every transaction pattern verified against historical norm and against adversary-known patterns; AI-channel outputs treated as untrusted until cross-checked | Critical for AI-pipeline applicability. AI-channel I/O inspection is the primary defensive control against prompt injection mediating agent-initiated payments and AI-mediated SWIFT message drafting. Almost never deployed at mid-2026; this is the dominant defensive gap. |

**AI-pipeline-specific posture.** Conventional D3-MFA cannot apply to autonomous AI agents acting on behalf of a customer — there is no agent-side biometric inherence factor, and possession factors are reduced to API-key custody. The AI-pipeline-appropriate construct is: scoped delegated-authority attestation (PSD3/PSR forward-looking) + out-of-band confirmation for any transaction above scoped threshold + AI-channel I/O recording (D3-IOPR) sufficient to support post-hoc dispute resolution and forensic reconstruction. Skill `identity-assurance` covers AAL/IAL/FAL constructs and is the companion for human-side authentication; this skill covers the sector-regulatory framing of the agent-side gap.

---

## Hand-Off / Related Skills

After producing the financial-sector posture assessment, chain into the following skills.

- **`identity-assurance`** — for AAL3 / FIDO2 / WebAuthn customer-side SCA implementation detail, IAL2/IAL3 for high-value onboarding, FAL constructs for federation, and the deep cryptographic posture (RFC 8446 TLS 1.3, RFC 7519 JWT, RFC 8725 JWT BCP, RFC 9421 HTTP Message Signatures) that PSD2 RTS-SCA and SWIFT CSCF reference but do not specify.
- **`attack-surface-pentest`** — for DORA Art. 26 TLPT methodology, TIBER-EU rules of engagement, CBEST scope-setting, iCAST tier calibration, and AESCSF red-team execution. This skill scopes the regulatory mapping; `attack-surface-pentest` covers the test mechanics.
- **`supply-chain-integrity`** — for DORA Art. 28-30 ICT third-party risk technical evidence (SBOM, SLSA, CSAF VEX, in-toto attestation, Sigstore verification), APRA CPS 230 third-party operational dependencies, OSFI B-10 outsourcing posture, and MAS TRM third-party section.
- **`dlp-gap-analysis`** — for financial PII and customer-data egress controls, AI-channel egress (LLM API calls) from SWIFT secure zone administrative jump zones, KYC document leakage into consumer AI tools, and the DLP-aware NTA construct named in D3-NTA above. Per `data/dlp-controls.json`.
- **`compliance-theater`** — to extend the four theater tests above with general-purpose theater detection across the wider GRC posture (DORA register completeness, CISO certification independence, SWIFT KYC-SA evidence currency).
- **`coordinated-vuln-disclosure`** — for DORA Art. 19 major-incident reporting (24h initial / 72h follow-up / 1-month final), NYDFS 500.17 24h cyber event + 72h ransom payment, APRA CPS 234 para 26 72h material incident, MAS Notice 644/655 1h notification, HKMA 24h, OSFI B-13 24h, and the multi-regulator notification orchestration when a single incident triggers multiple clocks.
- **`framework-gap-analysis`** — for any multi-jurisdiction institution, to produce the per-jurisdiction reconciliation called for in Output Format "Cross-Jurisdiction Framework Gap Summary."
- **`global-grc`** — alongside framework-gap-analysis when EU DORA + national overlays (BaFin BAIT/VAIT, ACPR, BdP, Banca d'Italia, AEPD), UK FCA + PRA, AU APRA + AESCSF, SG MAS, HK HKMA, IL BoI 361, CA OSFI, JP FISC, BR BCB, AE CBUAE + DFSA + FSRA, SA SAMA, IN SEBI + RBI all apply.
- **`ai-attack-surface`** and **`mcp-agent-trust`** — when banking copilot, agentic-payment surface, or AI-mediated SWIFT drafting is in scope; `ai-attack-surface` for prompt-injection and model-extraction threats, `mcp-agent-trust` for tool-use governance on copilots with write access to payment, transfer, or message-creation surfaces.
- **`policy-exception-gen`** — to generate defensible exceptions for financial-sector controls that cannot be met within stated SLAs (e.g., legacy core-banking platforms where 30-day patch SLA is operationally infeasible; documented compensating-control programme is the exception evidence).

**Forward watch (per skill-format spec).** PSD3 + PSR final text and agent-initiated-payment treatment; DORA TLPT first-cycle aggregate findings from ESAs; SWIFT CSCF v2027 annual update and AI-mediated-message-generation controls; NYDFS 23 NYCRR 500 further amendments and agentic-AI scope; CRI Profile v2 migration as US sector baseline replacing FFIEC CAT; MAS Notice 655 / TRM Guidelines refresh for GenAI; HKMA CFI 3.0 and iCAST AI/ML scope; APRA CPS 230 effective-date operational findings; UK FCA / PRA operational resilience self-assessment cycle; BCB Resolução BCB 85 PIX-fraud-typology updates; OSFI B-13 post-2024 examination findings; TIBER-EU v2.0 cross-recognition with CBEST and iCAST.
