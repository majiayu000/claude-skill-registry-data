---
name: age-gates-child-safety
version: "1.0.0"
description: Age-related gates and child online safety for mid-2026 — COPPA + CIPA + California AADC + GDPR Art. 8 + DSA Art. 28 + UK Online Safety Act + UK Children's Code + AU Online Safety Act + IN DPDPA child provisions + KOSA pending; age verification standards (IEEE 2089-2021, OpenID Connect age claims); AI product age policies
triggers:
  - age gate
  - age gates
  - age verification
  - age assurance
  - child safety
  - child online safety
  - children's online safety
  - youth safety
  - coppa
  - cipa
  - california aadc
  - children's code
  - uk online safety act
  - kosa
  - gdpr article 8
  - dsa article 28
  - parental consent
  - csam
  - ofcom
  - esafety
data_deps:
  - cwe-catalog.json
  - d3fend-catalog.json
  - framework-control-gaps.json
atlas_refs: []
attack_refs:
  - T1078
  - T1567
framework_gaps:
  - ISO-27001-2022-A.8.30
  - NIST-800-53-AC-2
  - SOC2-CC6-logical-access
  - NIS2-Art21-incident-handling
  - UK-CAF-B2
  - AU-Essential-8-MFA
rfc_refs: []
cwe_refs:
  - CWE-200
  - CWE-287
  - CWE-862
d3fend_refs:
  - D3-MFA
  - D3-IOPR
  - D3-CSPP
forward_watch:
  - KOSA (Kids Online Safety Act) federal enactment status — reintroduced 2024-2025 with bipartisan support; if enacted, duty-of-care + safest-defaults + age-appropriate-design obligations become US federal floor
  - Ofcom UK Online Safety Act child-safety codes — illegal-content codes live July 2025; child-safety codes phasing through 2026 with iterative enforcement guidance
  - California AADC (AB-2273) — Sept 2023 federal injunction (NetChoice v. Bonta), 2024 partial revival; track Ninth Circuit / SCOTUS posture and state legislative response
  - AU social media under-16 ban — Online Safety Amendment (Social Media Minimum Age) Act 2024 passed Nov 2024; implementation deferred to late 2025; age-assurance method finalisation pending
  - EU CSAM Regulation ("chat control") — Commission proposal 2022, contested through 2024-2025; if adopted, automated detection on encrypted communications becomes mandatory with significant fundamental-rights challenge
  - NIST IR on Age Assurance — pending publication; will operationalise age-assurance levels for US federal procurement
  - euCONSENT pilot outcomes — EU age-verification interoperability scheme; if scaled, becomes the de facto Member State age-verification reference architecture
  - AI product age policy enforcement — Character.ai litigation (2024 child-suicide complaint) testing duty-of-care for AI companion apps; ChatGPT / Claude / Gemini under-13 / under-18 enforcement evolving via FTC + state AG actions
  - France SREN (Securing and Regulating the Digital Space) Act 2024 — ARCOM age-verification referential for adult content services; double-anonymity model under deployment
  - US state adult-site age-verification laws — 19+ states by mid-2026 (TX HB 18 upheld by SCOTUS June 2025 in Free Speech Coalition v. Paxton); track ongoing challenges in remaining states
last_threat_review: "2026-09-18"
discovery_mode: "standalone"  # operator-reached via `exceptd brief age-gates-child-safety` or `exceptd ask`; not chained into any playbook's direct.skill_chain by design
---

# Age Gates and Child Online Safety (mid-2026)

## Threat Context (mid-2026)

The age-related regulatory wave that began with the UK Children's Code (in force Sept 2021) and California AADC (signed Sept 2022) crested in 2023-2025 and is in active enforcement entering mid-2026. The compliance surface for any consumer-facing product reachable by users under 18 is now approximately twenty-five overlapping jurisdictional regimes plus emerging AI-specific obligations, with enforcement asymmetry that punishes "we don't track children" as ignorance, not exemption.

Live-enforcement developments through mid-2026:

- **UK Online Safety Act 2023** — Ofcom's illegal-content codes of practice came into force March 2025; child-safety codes (highly effective age assurance for pornography, suicide / self-harm / eating-disorder content) phasing through July 2025 onward. Ofcom can fine up to GBP 18M or 10% of global turnover; senior-manager criminal liability for repeated failure. Ofcom's "highly effective age assurance" standard explicitly rejects self-declaration as a control.
- **California AADC (AB-2273)** — issued Sept 2023 federal preliminary injunction in NetChoice v. Bonta on First Amendment grounds; Ninth Circuit Aug 2024 partially reversed (severing the Data Protection Impact Assessment provisions from the speech-restricting provisions). DPIA + high-privacy-default + dark-pattern-prohibition pieces have an evolving enforcement posture into 2026; the Attorney General has begun targeted inquiries on products likely accessed by children.
- **EU Digital Services Act Art. 28** — VLOP / VLOSE (>45M EU monthly active users) obligations live since Feb 2024 for designated services; Commission has opened formal proceedings against multiple platforms in 2024-2025 on minor-protection grounds. Art. 28(2) prohibits targeted advertising based on profiling of children.
- **AU Online Safety Amendment (Social Media Minimum Age) Act 2024** — passed November 2024, mandating under-16 social-media ban; implementation deferred to late 2025 with age-assurance trial (administered by ACMA / eSafety, results delivered mid-2025) informing the technical method. The trial deliberately tested multi-vendor stacks (Yoti, age-estimation, document-based, vouching) under realistic conditions.
- **US adult-content age verification** — SCOTUS upheld Texas HB 18 in Free Speech Coalition v. Paxton (June 2025), 6-3, finding rational-basis applies to age-verification statutes targeting commercial pornography. By mid-2026, 19+ US states have enacted comparable laws (TX, LA, MT, MS, UT, AR, VA, NC, KY, FL, AL, TN, KS, OK, IN, NE, ID, GA, SD, plus more in late-2025 sessions). Multiple still face state-court challenges.
- **France SREN 2024** — ARCOM's age-verification "double anonymity" referential for adult-content services took effect with mid-2025 enforcement; non-compliant services face geo-blocking orders.
- **KOSA (Kids Online Safety Act)** — US federal; Senate passed 91-3 in July 2024; House did not advance before 119th Congress reset; reintroduced 2025. If enacted: duty of care to children, safest defaults on by default for under-17 accounts, age-appropriate design, opt-out from algorithmic recommendation, parental tools. Enforcement by FTC and state AGs.
- **AI-product age dimension** — ChatGPT terms-of-service minimum age 13 (with parental consent for 13-18 under enterprise / consumer variants), Claude.ai 18+ (with limited consumer-tier exceptions through enterprise admin), Google Gemini 13+ (with Google Workspace for Education k-12 carve-outs), Meta AI 18+. None of these vendors deploys robust age verification — age is self-attested at signup. Character.ai litigation (multiple 2024 complaints, including a Florida wrongful-death suit alleging companion-chatbot influence on minor suicide) is testing duty-of-care theory for AI-companion services. CSAM dimension: AI-generated CSAM is reportable to NCMEC CyberTipline under 18 U.S.C. §2258A and is criminal under existing US obscenity / child-pornography statutes; the EU CSAM Regulation proposal would require automated detection on hosting + interpersonal-communication services, contested through 2024-2025 on encryption-undermining grounds.

The dominant 2026 reality: any consumer product likely accessed by children needs an age-assurance posture that survives scrutiny across at minimum US (COPPA, AADC, KOSA-if-enacted, state adult-content laws), EU (GDPR Art. 8, DSA Art. 28, AVMSD, CSAM Regulation if adopted), UK (Online Safety Act + Children's Code), AU (Online Safety Act + under-16 social-media regime), and a long tail of national regimes (IN DPDPA, BR LGPD, CN Minors Protection Law, SG, JP). Self-declaration is not a control under any 2026 jurisdiction's "highly effective" / "verifiable parental consent" / "appropriate" standard.

---

## Framework Lag Declaration

Classical security and privacy frameworks (NIST 800-53 r5, ISO/IEC 27001:2022, SOC 2, PCI-DSS) make essentially no provision for age-cohort-specific data handling beyond generic access control and lawful-basis language. They are channel-agnostic in language and child-blind in implementation guidance. Children's-specific regimes layer on top, with different age thresholds, different consent rules, and different "appropriate" technical-assurance bars per jurisdiction.

| Framework / Regime | Control / Instrument | Designed For | What It Misses For Child Online Safety in mid-2026 |
|---|---|---|---|
| NIST 800-53 r5 AC-2 | Account Management | Generic account lifecycle. | No age-cohort attribute model. Does not name verifiable parental consent (VPC), age-assurance levels (IEEE 2089-2021 style), age-attribute provisioning, or under-13 / under-16 / under-18 cohort gating. AC-2 recorded gap in `data/framework-control-gaps.json` covers generic AI-service-principal lifecycle but is silent on child identities. |
| ISO/IEC 27001:2022 A.8.30 | Outsourced Development | Outsourced software development controls. | Silent on child-specific data minimisation and age-appropriate-design requirements imposed on suppliers. Catalog gap entry exists; needs explicit "age-cohort handling" extension when in scope. |
| ISO/IEC 27001:2022 A.5.34 | Privacy and Protection of PII | PII handling. | Channel-agnostic; no cohort-specific defaults; no DPIA-on-child-product requirement. |
| SOC 2 CC6 (logical access) | Logical and Physical Access | TSC logical-access controls. | No age-cohort dimension; auditors accept self-declared-age signup as access control. SOC 2 CC6 gap entry in `data/framework-control-gaps.json` does not capture age-attribute requirement. |
| US COPPA (Children's Online Privacy Protection Act, 15 U.S.C. §§6501-6506; FTC Rule 16 CFR Part 312; 2025 Rule update) | Under-13 personal-information collection by operators of websites or online services directed to children, or with actual knowledge of under-13 use | US protection of under-13 children | Threshold-and-knowledge model — "directed to children" + "actual knowledge" lets operators argue ignorance. 2025 FTC Rule update adds biometric to personal-information definition, restricts third-party disclosures, raises VPC operationalisation bar — but VPC methods still include the historically-permissive "credit card + transaction" and "knowledge-based authentication" channels that are inadequate against motivated children. Behavioral advertising prohibited but ad-tech operator inheritance of "actual knowledge" is contested. |
| US CIPA (Children's Internet Protection Act, 47 U.S.C. §254) | E-Rate / LSTA-funded schools and libraries | Internet filtering for school / library children | Eligibility-conditioned, not a general obligation; covers technology-protection-measure baseline only. Silent on generative-AI exposure in K-12. |
| California AADC (AB-2273, Cal. Civ. Code §§1798.99.28-1798.99.40) | "Online service, product, or feature likely to be accessed by children" (under 18 in CA framing) | Operators serving CA users likely-accessed-by-children | "Likely to be accessed" is broader than COPPA's "directed to" — operationally captures most general-audience platforms. DPIA + high-privacy-default + dark-pattern-prohibition under partial enforcement after 2023 injunction + 2024 Ninth Circuit ruling severing speech-restricting from non-speech-restricting provisions. Implementation is service-by-service; auditor capacity is the rate-limiting step. |
| California CCPA / CPRA children | Cal. Civ. Code §§1798.120(c), 1798.135 | Sale / sharing of personal information of CA children | Opt-IN required for under-13 (parent) and 13-15 (the child); opt-OUT otherwise. CPRA Reg modifications 2023-2024 tightened operationalisation. "Actual knowledge" pivot remains. |
| NY SAFE for Kids Act (S7694A, 2024) | Operators of "addictive feeds" reaching New York children | NY-resident children | Restricts algorithmic feeds + push notifications between 12am-6am for child accounts. Age determination obligation triggers age-verification posture per NY AG rulemaking (2025). |
| KOSA (proposed) | Duty of care, safest defaults, age-appropriate design | US federal | Not yet enacted (reintroduced 2025). If enacted: duty of care to prevent specified harms (mental-health, sexual exploitation, online bullying, sextortion), safest defaults on by default for under-17 accounts, age-appropriate design, opt-out from algorithmic recommendation, parental tools. Section 230 carve-out is part of the policy fight. |
| EU GDPR Article 8 | Age of digital consent for information-society services offered directly to children | EU/EEA + UK (under UK GDPR) | Member-state discretion sets age 13-16: UK = 13, IE = 16, DE = 16, FR = 15, ES = 14, IT = 14, NL = 16, PL = 16, BE = 13, SE = 13, FI = 13, etc. Multi-jurisdictional operators must apply the highest applicable threshold per audience or per Member State. Operationalisation of VPC under Art. 8 mirrors COPPA infirmities. EDPB Guidelines 5/2020 on consent provide non-binding interpretive guidance. |
| EU Digital Services Act Art. 28 (Reg. 2022/2065) | Online platforms accessible to children — heightened minor protection; VLOPs / VLOSEs Art. 28(2) ban on profiling-based advertising to children | EU users | Live enforcement since Feb 2024 for designated VLOPs; Commission has opened multiple formal proceedings (TikTok, X, Instagram on minor-protection grounds 2024-2025). Art. 28(2) profiling-ads ban operationalisation: "reasonable certainty" the recipient is a minor — operator inference burden, contested. |
| EU AVMSD (Dir. 2010/13/EU as amended) Art. 6a + Art. 28b | Video-sharing platforms — age verification for adult content; appropriate measures for minor protection | EU video-sharing platforms | Implementation is per-Member-State; UK has transposed via OSA; FR via SREN ARCOM referential; DE via JMStV (Jugendmedienschutz-Staatsvertrag); IT via AGCOM; ES via CNMC. Cross-border consistency is patchy. |
| EU CSAM Regulation (proposed, COM(2022) 209) | Hosting and interpersonal-communications services — detection, reporting, removal of CSAM and grooming | EU-served services | Not adopted as of mid-2026. Contested through 2024-2025 on encryption-integrity and fundamental-rights grounds (EDPS / EDPB joint opinion 2022). If adopted, would require automated detection — fundamental-rights case law via CJEU likely to follow. |
| UK Online Safety Act 2023 (c. 50) | User-to-user services, search services, services publishing pornographic content | UK users | Live enforcement: Ofcom illegal-content codes live March 2025; child-safety codes phasing from July 2025. "Highly effective age assurance" standard (s.81 + Ofcom guidance) explicitly rejects self-declaration; lists methods including age estimation, photo-ID, open-banking-derived, credit-reference-derived, mobile-network-operator-derived. Penalties: GBP 18M or 10% of qualifying worldwide revenue; senior-manager criminal liability under s.110. |
| UK Age-Appropriate Design Code ("Children's Code", ICO) | Information Society Services likely to be accessed by children in the UK | UK users — under 18 framing per UNCRC | In force since Sept 2021. 15 standards: best-interests-of-child, DPIA, age-appropriate application, transparency, detrimental use of data, policies and community standards, default settings high-privacy, data minimisation, data sharing, geolocation, parental controls, profiling, nudge techniques, connected toys, online tools. Standard 3 (Age-Appropriate Application) requires either age verification or design-as-if-children. ICO enforcement: TikTok fine GBP 12.7M (April 2023) for under-13 processing without consent; Snap Inc. preliminary enforcement notice (Oct 2023, withdrawn after remediation 2024); ongoing audit programme 2025-2026. |
| AU Online Safety Act 2021 + 2024 amendments | Australian users — Basic Online Safety Expectations + designated industry codes | AU users | eSafety Commissioner enforcement. Basic Online Safety Expectations (BOSE) Determination 2022 + 2024 amendments require minimum age-assurance measures for class-1 and class-2 material. Industry codes / standards (Class 1A / Class 1B / Class 1C / Phase 2) impose specific obligations on relevant electronic services, social media services, designated internet services. Under-16 social-media ban (Online Safety Amendment (Social Media Minimum Age) Act 2024) — implementation deferred to late 2025; eSafety age-assurance trial 2024-2025 informed technical method. Penalties up to AUD 49.5M per breach. |
| IN DPDPA 2023 + Draft DPDP Rules 2025 | Personal data of children (under 18) and persons with disabilities | IN data principals | Default verifiable parental consent for under-18 (s.9). Prohibits tracking, behavioural monitoring, and targeted advertising directed at children. Draft DPDP Rules Jan 2025 propose VPC mechanisms; final rules expected late 2026. Highest cohort threshold globally — IN treats under-18 as the protected cohort, not under-13 / under-16. |
| BR LGPD Art. 14 + ANPD Resolution CD/ANPD No. 4/2023 + Best-Practices Guide on processing of children's and adolescents' personal data (2024) | Children's (0-12) and adolescents' (12-17) personal data | BR data subjects | "Best interests" standard plus specific parental-consent regime for children. ANPD Resolution + Guide articulate technical-and-organisational expectations including DPIA, data minimisation, age-appropriate communication. ANPD enforcement action against TikTok (2023-2024) set the operational tone. |
| CN Minors Protection Law (2020 rev., chapter on network protection) + PIPL child provisions (Art. 31 — sensitive PI category) + CAC Provisions on Protection of Minors in Cyberspace (2023) + CAC Provisions on Minors Mode (2024) | Online services accessed by children in China | CN children (under 18) | Child PI is sensitive personal information under PIPL Art. 31 — requires separate consent, DPIA, encryption, access control. Minors Mode requirement (CAC 2024, in force 2024-2025) imposes platform-wide age-cohort UX with time limits + content restrictions + spending limits. Gaming time limits (NPPA 2021) — under-18 limited to 1 hour on Fri/Sat/Sun/holidays. Real-name identification effectively pre-existing; age verification is operationally robust by global standards. |
| SG Online Safety (Miscellaneous Amendments) Act 2022 + IMDA Code of Practice for Online Safety + 2024 designated services obligations | Designated social-media services serving SG users | SG users — under 18 | Code obliges designated services to implement community guidelines, content-moderation, child-safety measures, age-assurance, user-reporting. IMDA designation criteria + enforcement evolving. |
| JP Act on Establishment of Enhanced Environment for Youth's Safe and Secure Internet Use (2008, updated through 2024) + per-prefecture youth-protection ordinances + APPI special-care-required PI rules | Youth (under 18) internet protection | JP children | Filtering-software default-installation obligation on mobile carriers and ISP retail; per-prefecture content ordinances vary. APPI sensitive-PI rules apply where child data overlaps with health, criminal, biometric. JP framework is filter-heavy, age-verification-light. |
| KR Network Act (Act on Promotion of Information and Communications Network Utilization and Information Protection) + PIPA child-PI provisions + Youth Protection Act + Act on Sound Game Culture (game shutdown law repealed 2021, replaced with parental choice) | Under-14 PI requires legal-guardian consent under PIPA Art. 22-2 | KR data subjects | PIPA threshold under-14 (post-2023 amendment from under-15). Real-name verification for some services (i-PIN, mobile-carrier-based) is technically robust. PIPC enforcement against AI services accepting KR child PI without consent infrastructure active 2024-2025. |
| Quebec Law 25 (Act respecting the protection of personal information in the private sector, amended 2021-2024) | Under 14 cannot consent without parent / tutor; high-privacy defaults for children | QC residents | Operationalised by CAI; cross-border transfers require PIA per s.17. AI-tool processing of child PI captured. |
| US sub-national — adult content age-verification laws (TX HB 18, LA, MT, MS, UT SB 287, AR, VA, NC, KY, FL, AL, TN, KS, OK, IN, NE, ID, GA, SD plus more in 2025 sessions) | Operators of websites with substantial portion (typically >33%) sexual material | State residents | "Reasonable age-verification" standard (varies by state — typically excludes self-declaration); SCOTUS Free Speech Coalition v. Paxton (June 2025) upheld TX HB 18 under rational-basis review. Multiple still face state-court challenges. |
| France SREN (Loi visant à sécuriser et réguler l'espace numérique, Loi n° 2024-449) | Adult-content services serving France | FR users | ARCOM "référentiel" for age-verification (double-anonymity model) enforceable mid-2025; non-compliant services subject to geo-blocking orders. |
| ISO / IEC standards — IEEE 2089-2021 (Age-Appropriate Digital Services Framework) + ISO/IEC 27566 (Age assurance systems, draft) + BSI PAS 1296:2018 (Age checking — code of practice) + emerging NIST IR on age assurance | Age-appropriate design + age-assurance assurance levels | Multi-jurisdiction technical reference | IEEE 2089-2021 is the canonical framework reference cited by UK ICO, Ofcom, and AADC implementation guidance. ISO/IEC 27566 still in draft (parts 1-4 progressing 2024-2026). PAS 1296 is referenced in UK Ofcom guidance for age-check effectiveness. NIST IR on age assurance pending — will set US federal procurement baseline. |
| AI-vendor age policies (OpenAI 13+ w/ parental consent for under-18, Anthropic 18+ consumer / age-gated, Google Gemini 13+ w/ Workspace Edu carve-outs, Meta AI 18+, Character.ai 13+ then 17+ for chat post-2024 settlement) | Vendor terms-of-service age minimums | Self-declared | None of the major frontier AI vendors deploys verifiable age assurance at signup as of mid-2026. Terms-of-service are post-hoc liability shields, not technical controls. Character.ai litigation (FL wrongful-death suit 2024, additional complaints 2024-2025) is the leading-edge test of duty-of-care theory for AI companion services. |
| NCMEC CyberTipline (18 U.S.C. §2258A) + EU CSAM Regulation (proposed) | CSAM reporting obligation for US electronic-service-providers; (proposed) EU detection / reporting obligation | US ESPs (mandatory); EU services (if Regulation adopted) | §2258A is a reporting obligation, not a detection obligation — but operational reality is that hash-matching (PhotoDNA, NCMEC hash, Apple NeuralHash family) is the de facto detection layer. AI-generated CSAM is criminal under existing US obscenity / child-pornography law and is reportable under §2258A as apparent CSAM. EU CSAM Regulation contested; if adopted, expands detection mandate. |

**Cross-jurisdiction posture (global-first, not US-centric).** Any age-gate / child-online-safety posture for a multi-jurisdiction operator must explicitly enumerate the regulator and primary instrument for: US (FTC for COPPA + AADC + KOSA-if-enacted; state AGs for state laws), EU (each Member State DPA + Commission for DSA + national audiovisual regulators for AVMSD), UK (ICO + Ofcom), AU (eSafety Commissioner + OAIC), IN (Data Protection Board, when operational, + MeitY for DPDP Rules), BR (ANPD), CN (CAC + MIIT for industry-specific obligations), SG (IMDA + PDPC), JP (PPC + per-prefecture authorities), KR (PIPC + KCC), CA / QC (CAI), and US-state (CA AG + NY AG plus comparable). ISO/IEC 27001:2022 + IEEE 2089-2021 + (when published) ISO/IEC 27566 + NIST IR on age assurance form the technical-reference layer. US-only (COPPA + state laws) is incomplete for any multinational service likely-accessed-by-children.

---

## TTP Mapping

This skill is primarily a compliance + privacy-engineering skill rather than a technical-exploit skill. There are no ATLAS-catalogued AI-attack TTPs that are child-specific as of v2026.09, and most relevant attacker activity intersects general ATT&CK techniques rather than child-targeted novel TTPs. The relevant mapping is therefore narrower and explicitly flagged as such — `atlas_refs` is empty by design, not omission.

| ID | Source | Technique | Child-Safeguarding Relevance | Gap Flag |
|---|---|---|---|---|
| T1078 | ATT&CK Enterprise | Valid Accounts | Account takeover targeting child accounts (compromised parental controls; sextortion via stolen accounts; grooming via account hijack) — child accounts are under-protected because MFA roll-out lags adult user populations. | NIST 800-53 AC-2 + COPPA / AADC / Children's Code silent on MFA-for-child requirement; the AC-2 gap entry in `data/framework-control-gaps.json` covers AI-service-principals not child identities. Hand off to `identity-assurance` for AAL2+ on child accounts where vendor terms permit. |
| T1567 | ATT&CK Enterprise | Exfiltration Over Web Service | Child PI exfiltrated via AI-tool / SaaS egress — additional liability under COPPA (no behavioral-ad use of under-13 PI), AADC (DPIA failure), GDPR Art. 8 (no lawful basis), DPDPA (default-VPC bypass), CN PIPL Art. 31 (child PI = sensitive PI requiring separate consent). | Hand off to `dlp-gap-analysis` for child-PI as a protected data class; COPPA / AADC / Children's Code do not name DLP technical controls; the SOC2-CC7 anomaly-detection gap entry applies. |
| AI-generated CSAM creation / distribution | Not catalogued in ATLAS or ATT&CK as of v2026.09 | Generative-AI image / video synthesis depicting children | Direct criminal exposure under 18 U.S.C. §§2251, 2252, 2252A, 2256 (Protect Act / Mash-Up Act framework); mandatory NCMEC reporting per §2258A. Multiple 2024-2025 prosecutions (US v. Anderegg WD-Wis 2024 — first federal AI-CSAM prosecution; UK National Crime Agency campaign 2024-2025). | No formal TTP class. Evidence stream: NCMEC CyberTipline reports + EU IWF reports. Hand off to `ai-attack-surface` for generative-model content-policy red-team and to `incident-response-playbook` for reporting workflow. |
| AI chatbot grooming / harmful-content engagement with children | Not catalogued | Long-context AI chatbot interactions with children steering toward harm | Research and litigation evidence: Character.ai litigation 2024 (FL wrongful-death suit alleging companion-chatbot contribution to minor suicide; additional 2024-2025 complaints); UK NCA campaign 2024 documenting grooming attempts via AI chatbots; ESRC / RAND research 2024-2025. | No formal TTP class. EU DSA Art. 28 + UK OSA + AU OSA + KOSA-if-enacted all frame this as a platform duty-of-care obligation. Hand off to `ai-risk-management` for AI-product age policy enforcement. |

**Honest scope statement (no fabricated TTP IDs).** This skill does not invent TTP IDs to fill gaps in the ATLAS or ATT&CK matrices. AI-generated CSAM and AI-chatbot-mediated harm to children are real-world threat classes documented through prosecution records, NCMEC / IWF reporting, and litigation — not novel ATLAS techniques. Citation is to the evidence stream, not to a TTP ID.

---

## Exploit Availability Matrix

For this skill, "exploit availability" maps to "what child-exposure violations have happened recently, with what regulator outcome." This is the precedent base that an analysis must score against — paper-compliance language is theatre if these patterns are present without controls.

| Pattern | CVE? | Public Incident / Enforcement Reporting | KEV? | AI-Accelerated? | Vendor / Platform Coverage (mid-2026) | Regulator Action To Date |
|---|---|---|---|---|---|---|
| Self-declared-age signup as the only age control | No | YouTube / Google COPPA settlement (USD 170M, Sept 2019, FTC + NY AG, In re YouTube In re YouTube LLC) — canonical COPPA enforcement precedent for "directed-to-children" content treated under standard ad model. Epic Games COPPA + dark-patterns settlement (USD 520M, Dec 2022, FTC) — largest COPPA penalty to date; default-on voice/text chat for under-13 + dark-pattern purchase flows. TikTok ICO fine (GBP 12.7M, April 2023) for processing under-13 PI without consent. Multiple 2024-2025 FTC actions on educational-tech operators. | N/A | Yes — AI age-estimation lowers verification friction but is rarely deployed | Microsoft / Apple / Google account-age inference improving but voluntary; consumer-AI vendors (OpenAI, Anthropic, Google, Meta) effectively zero | FTC COPPA Rule 2025 update tightens VPC + adds biometric to PI; ICO Children's Code audit programme; CA AG AADC inquiries; ANPD (BR) action vs. TikTok 2023-2024 |
| Behavioral advertising to under-13 / children | No | YouTube / Google 2019 settlement specifically named behavioral ads on directed-to-children content. Multiple ad-tech operator follow-on actions 2020-2025. DSA Art. 28(2) profiling-ads ban for children live since Feb 2024 — Commission formal proceedings against multiple VLOPs 2024-2025. | N/A | Yes — AI-driven targeting amplifies efficiency | Major ad-tech platforms deploy content-classifier-based "made for kids" treatment; "actual knowledge" inheritance to upstream advertisers remains contested | EU Commission formal proceedings 2024-2025; FTC COPPA 2025 Rule tightens third-party disclosures |
| Cross-clearance retrieval / child PI in RAG corpus | No | M365 Copilot / Glean / Notion AI over-permissioning disclosures 2024-2025 — applies to schools and child-serving organisations where teacher / staff Copilot retrieves child records due to broken SharePoint ACL inheritance | N/A | Yes — RAG amplifies pre-existing over-permissioning | Microsoft Purview Information Protection label propagation to Copilot context evolving; school-tenant configuration is the operator's responsibility | OCR (HHS) guidance review 2025 on PHI in Copilot for healthcare overlaps with education; ICO Children's Code applies to educational ISS likely accessed by children |
| AI companion chatbot interaction harms with children | No | Character.ai litigation Oct 2024 (Garcia v. Character Technologies, MD-FL — alleging AI-companion contribution to 14-year-old's suicide) + additional 2024-2025 complaints; Texas SB 976 child-AI-companion bill 2025; UK NCA campaign 2024 on AI grooming risk | N/A | Yes — large language model intrinsic | Character.ai 2024 settlement-driven changes: 17+ chat for some features, parental controls, safe-prompt guardrails. OpenAI / Anthropic / Google content policies + child-cohort guardrails | None final yet; KOSA-if-enacted creates duty-of-care; UK OSA child-safety codes phasing through 2026 |
| AI-generated CSAM | No CVE; criminal-statute violations | US v. Anderegg WD-Wis 2024 — first federal AI-CSAM prosecution; UK NCA 2024-2025 enforcement; multiple EU national prosecutions; NCMEC CyberTipline AI-CSAM reports doubled 2023-2024 (NCMEC 2024 annual reporting) | N/A | Yes — AI is the threat capability | OpenAI / Anthropic / Google / Stability AI / Midjourney deploy content classifiers + reporting infrastructure; open-weight model ecosystems are structural blind spot | NCMEC CyberTipline mandatory reporting in effect; EU CSAM Regulation contested but pressure rising; multiple Stable-Diffusion-derived prosecutions 2024-2025 |
| Adult content served without age verification (US state laws) | No | Pornhub geo-blocked TX 2023 + LA 2023 + MT + UT + VA + MS + AR + NC + KY + AL + KS + OK + IN + NE 2023-2024-2025 rather than implement; SCOTUS upheld TX HB 18 in Free Speech Coalition v. Paxton June 2025 6-3; Aylo state-AG enforcement actions; XHamster + similar smaller operators face state AG actions 2024-2025 | N/A | N/A | AgeChecked, Yoti, VerifyMy, Incode, Persona, Jumio, OnFido provide commercial age-verification stacks; coverage uneven | TX, LA, MT, MS, UT, AR, VA, NC, KY, FL, AL, TN, KS, OK, IN, NE, ID, GA, SD active enforcement 2024-2025 |
| EU AVMSD age-verification non-compliance for adult video content | No | DE BzKJ enforcement against adult-content services 2023-2025; FR ARCOM enforcement 2024-2025 culminating in geo-blocking orders under SREN | N/A | N/A | Member-state per-stack age-verification ecosystem (FR ARCOM referential, DE KJM-acceptable systems) | Per-member-state continuous enforcement |
| UK Online Safety Act child-safety failure | No | Ofcom illegal-content code enforcement live March 2025; child-safety codes in force July 2025; Ofcom has launched 80+ investigations into adult sites and issued its first OSA fine (£1M for failure to implement highly effective age assurance); Ofcom 2026-27 priorities document confirms continued child-protection focus, AI-generated-harm enforcement, and categorised-services register publication July 2026 | N/A | N/A | Major platforms deploying age-assurance stacks pre-emptively (Yoti, Persona, internal age-estimation) | Ongoing OSA investigations; risk-assessment records due from notified providers April 2026; provider risk-assessment summary publication deadline November 2026; categorised-services register July 2026 |
| AU social-media-under-16 non-compliance | No | Act entered force 10 December 2025; >4.7M underage accounts deactivated / restricted by mid-January 2026; eSafety Commissioner opened formal investigations into Facebook, Instagram, Snapchat, TikTok and YouTube on 31 March 2026 — first formal compliance assessment under the regime | N/A | N/A | Age-assurance trial concluded mid-2025; eSafety regulatory guidance published Feb 2026; implementation method evolving | eSafety civil penalty regime active (up to A$49.5M); investigation outcomes for the five named platforms pending; expect first civil penalty proceedings H2 2026 |
| CN Children-Mode non-compliance + gaming time-limit non-compliance | No | CAC + NPPA enforcement against multiple platforms 2022-2025; real-name + age-verification operationally robust by global standards | N/A | N/A | Tencent / NetEase / ByteDance Children-Mode + real-name-based time limits comprehensive | CAC + MIIT active enforcement; NPPA gaming-time-limit enforcement continuous |
| BR LGPD Art. 14 violations (child data processing without VPC) | No | ANPD TikTok proceeding 2023-2024; ANPD Best-Practices Guide 2024 set operational tone | N/A | N/A | Major Brazilian + multinational platforms aligning to ANPD 2024 Guide | ANPD continuing enforcement |
| IN DPDPA child-provisions non-compliance | No | DPDP Rules not yet final (draft Jan 2025; final expected late 2026); Data Protection Board not yet operational | N/A | N/A | None — Rules not final, Board not operational | None — Rules pending |

**Interpretation.** Age-gate failures are predominantly civil-regulatory and litigation patterns, not vendor CVEs. The exception is AI-generated CSAM, where the failure mode is criminal-statute exposure for the operator and (potentially) for upstream model providers depending on training-data and content-policy posture. Mitigation is architectural (age-assurance stack, age-cohort UX, content-classifier + reporting infrastructure, parental-consent flow) plus contractual (vendor terms-of-service alignment) plus operational (DPIA, AAL2 on child accounts where feasible, parental tools, transparency reporting).

---

## Analysis Procedure

The procedure threads the three foundational design principles — defense in depth, least privilege, zero trust — through every step before stepping through the audit.

### Principle 1 — Defense in depth

Age-related gating cannot be a single-layer control. The required ladder, weakest to strongest:

1. **Layer 1 — Age declaration (self-attestation).** Operationally the floor and explicitly insufficient under every 2026 jurisdiction's "highly effective" / "verifiable" / "reasonable" standard. Acceptable only as the entry point to subsequent layers.
2. **Layer 2 — Age verification (document-based or hard-identity).** Photo-ID + biometric-match (Yoti, OnFido, Jumio, Persona, Incode); credit-reference-derived (VerifyMy, Veriff); mobile-network-operator-derived (UK MEF Personal Data & Trust Framework); open-banking-derived (UK / EU PSD2-based); national-eID-derived (eIDAS in EU, IndiaStack Aadhaar where lawful, GOV.UK One Login). Highest assurance; highest friction; per-jurisdiction lawfulness varies.
3. **Layer 3 — Age estimation (biometric / behavioural).** Facial-age-estimation (Yoti FaceMatch, Privately, Incode), voice-age-estimation, account-age + interaction-pattern. Lower friction; lower assurance; bias considerations under EU AI Act high-risk + UK Equality Act. UK Ofcom and France ARCOM accept facial-age-estimation within defined error bands.
4. **Layer 4 — Verifiable parental consent (VPC) flow.** COPPA-acceptable methods: government-ID-and-photo, credit-card-with-transaction, knowledge-based-authentication, video-conference, signed-form + return, plus 2025 FTC Rule expansions. India DPDPA, BR LGPD, Quebec Law 25, AU OSA each have parallel VPC operationalisations. Required wherever the cohort threshold sets it (under-13 universally; under-14 in KR, QC; under-15 in FR; under-16 in DE, IE, NL, IT, ES, others; under-18 in IN, BR-adolescents-with-best-interests-overlay).
5. **Layer 5 — Age-appropriate design (default settings).** UK Children's Code 15 standards; AADC high-privacy-default + dark-pattern-prohibition; DSA Art. 28 minor-protection; KOSA-if-enacted safest-defaults. Geolocation off, profiling off, friends-of-friends visibility off, nudging-design absent, time-of-day restrictions where required (NY SAFE).
6. **Layer 6 — Behavioral & content gating per cohort.** Under-13 default to no tracking, no behavioral ads, scoped feature set; under-16 / under-18 expanded but still scoped; AI-chatbot scoped capabilities + safety filtering + crisis-detection (self-harm, eating-disorder, sextortion classifiers).
7. **Layer 7 — AI-content moderation & CSAM detection.** Hash-matching against PhotoDNA + NCMEC + IWF hash sets; classifier-based CSAM detection (Thorn Safer, Microsoft PhotoDNA AI extensions); generative-model content-policy enforcement (prompt classifiers, output classifiers, reporting infrastructure); operator NCMEC CyberTipline reporting workflow.

Each layer fails differently. Layer 1 alone = compliance theater. Layer 2 alone = friction failure + privacy maximalism. Layer 4 alone = adult-cohort-served-as-child failure. Layer 7 absent = criminal-statute exposure on AI-generated CSAM.

### Principle 2 — Least privilege

Per identity × cohort × feature granularity. Children get the minimum-data-collection scope by default — not as an after-the-fact consent option. Advertising / profiling / personalization disabled by default for under-13 (universal) and for under-16 / under-18 per jurisdiction. AI chatbots for children get scoped capabilities (no romantic / companion mode, no self-harm topics without crisis-routing, no purchase capability without parental approval), safety filtering enabled, and crisis-detection wired to escalation. Parental-consent state is per-cohort, per-feature — not blanket. Educational-tech tenants get school-as-controller, vendor-as-processor model with strict purpose-limitation; teacher / staff accounts are not authorised to use child PI outside the educational purpose.

### Principle 3 — Zero trust

Never trust self-declared age. Verify or estimate at every high-risk action (account creation, purchase, content access, AI interaction with sensitive topics, friend-request approval, location-sharing toggle, livestream initiation). Re-verify periodically (annual + on flagged-anomaly). Verify parental consent through multiple channels — the "verifiable" in COPPA-VPC is the qualifier — and re-verify on material change (new feature, new data category, vendor change). Treat vendor age-claim attestations as compensating contractual controls, not as primary technical controls — verify with audit logs.

### Step-by-step audit

**Step 1 — Inventory products / services likely-accessed-by-children per jurisdiction.**

Pull the product / service catalog. For each, score "directed to children" (COPPA-style), "likely to be accessed by children" (AADC + UK Children's Code-style), "designated service" (AU OSA-style), "service offered directly to children" (GDPR Art. 8-style), "addictive feed reaching children" (NY SAFE-style), VLOP / VLOSE (DSA Art. 28-style), "online service likely to be accessed by adolescents" (BR LGPD-style), "designated MZ service" (CN Children-Mode-style). The breadth is intentional — products often qualify under multiple frameworks simultaneously. Document the rationale, not just the conclusion; "we're a general audience platform" is rebuttable.

**Step 2 — DPIA per California AADC + UK Children's Code + GDPR Art. 35 + DSA Art. 28 obligations.**

For each product from Step 1, produce or refresh the Data Protection Impact Assessment / Children's Impact Assessment. Required elements: data flows, age cohorts served, lawful basis per cohort (Art. 6 + Art. 8 + Art. 9 if applicable + Art. 28 DSA + COPPA-VPC + AADC-DPIA + DPDPA-VPC + LGPD Art. 14), profiling / advertising / personalisation posture per cohort, default settings, dark-pattern audit, parental-tool inventory, crisis-detection inventory for AI-mediated features. The DPIA artefact is the primary regulator-facing evidence — its absence is per-se theater under AADC + Children's Code.

**Step 3 — Age-verification posture per jurisdiction and per service.**

For each (jurisdiction × service) intersection, document the age-assurance posture against the applicable standard:

- UK Ofcom "highly effective age assurance" (HEAA) — self-declaration ruled out; document the HEAA method and the technical-effectiveness evidence (vendor assurance report; bias testing; error-band evidence).
- France ARCOM "double-anonymity" referential — verifier-attribute-provider separation evidence.
- US state adult-content laws — "reasonable age verification" per statute (varies; many specifically exclude self-declaration).
- AU eSafety age-assurance method (post-trial; finalising late 2025).
- EU AVMSD per-Member-State implementation.
- IEEE 2089-2021 assurance-level claim (where the operator references it as a framework anchor).

Map to the age-assurance vendor stack in use (Yoti, Persona, OnFido, Jumio, Incode, VerifyMy, AgeChecked, Privately, Veriff, others). Document the fallback for users who cannot complete a given method (lawful basis for refusal, alternate route, accessibility / equality considerations).

**Step 4 — Parental consent (VPC) flow per applicable cohort.**

COPPA-VPC method audit: government-ID-and-photo + photo-match, credit-card + transaction, knowledge-based authentication, video-conference, signed-form + return, plus 2025-Rule additions. DPDPA VPC operationalisation (draft Rules 2025; final 2026). LGPD Art. 14 parental-consent + best-interests-of-child evidence. Quebec Law 25 parental-tutor consent. UK Children's Code parental-control posture. AU OSA parental-consent under the under-16 ban (when in force). For each: re-verification cadence, evidence retention (consistent with data-minimisation), parental-revocation mechanism, dispute / fraud handling, accessibility for non-resident or non-citizen parents.

**Step 5 — Data-collection minimization per cohort.**

For each cohort (under-13, under-16, under-18) per service, enumerate:

- What PI / sensitive PI is collected, and the lawful basis per jurisdiction (COPPA-permitted limited categories for under-13; PIPL Art. 31 sensitive-PI handling for CN under-18; APPI special-care-required for JP; PIPA child-PI for KR; AADC + Children's Code data-minimisation; DPDPA prohibition on tracking children).
- Retention per category per cohort.
- Sharing / disclosure / transfer per category per cohort, including cross-border treatment under GDPR Art. 44, LGPD Art. 33, DPDPA s.16, PIPL Art. 38-42, KSA PDPL Art. 29, Quebec Law 25 s.17.
- Onward use (training, analytics, advertising) restrictions per cohort.

Hand off to `dlp-gap-analysis` for the child-PI channel-and-surface matrix; child PI is a protected data class throughout.

**Step 6 — AI-product age policy enforcement.**

For each AI service the operator provides or uses:

- Terms-of-service age minimum and whether it is enforced (signup gate + verification posture).
- Per-cohort capability gating (no companion mode for under-18, no romantic / explicit content, no purchase capability without parental approval, scoped self-harm / eating-disorder / sextortion topic handling with crisis-detection + safe-routing).
- Content-policy + classifier coverage on prompt and output (PhotoDNA + NCMEC hash matching for image surfaces; CSAM classifier on generative image / video; grooming / sextortion conversation classifier on chat).
- Child data in training corpus: provenance, consent, opt-out, deletion-on-request mechanism.
- Crisis-detection and routing: self-harm signals routed to crisis-line referral with human-in-the-loop where feasible; sextortion / grooming signals routed to safety team + NCMEC where US-jurisdictional.
- Vendor-side commitments: enterprise terms requiring vendor age-policy adherence; child-safety-by-design evidence.

Hand off to `ai-risk-management` for AI product age policy frameworks and to `ai-attack-surface` for red-team posture on the safety filtering.

**Step 7 — Algorithmic-feed transparency and gating (DSA Art. 28 + NY SAFE + KOSA-if-enacted).**

For each algorithmic feature reaching children: feed transparency disclosure, non-personalised option availability, opt-out from algorithmic recommendation for children, push-notification time-of-day restrictions per NY SAFE (12am-6am child accounts), addictive-design audit per AADC + DSA Art. 28 + UK Children's Code Standard 13 (Nudge Techniques). Document the inputs to the algorithmic system, the available controls, and the operationalisation of child-specific gating.

**Step 8 — Advertising-to-children policy audit.**

COPPA prohibits behavioral advertising to under-13. AADC restricts dark-pattern monetisation. DSA Art. 28(2) prohibits profiling-based targeted advertising to children. ANPD 2024 Guide imposes parallel restrictions on adolescent-targeted advertising in BR. For each ad-serving surface reaching children: audit the cohort-detection (technically robust? operator-controlled vs. ad-tech-inherited?), the ad-stack treatment (made-for-kids classification; contextual-only fallback; no-profile inheritance through DSP / SSP chain), the upstream advertiser inheritance of "actual knowledge" status.

**Step 9 — CSAM detection coverage and reporting workflow.**

For each surface accepting user-generated or AI-generated content reaching distribution:

- Hash-matching coverage (PhotoDNA + NCMEC + IWF + per-platform internal hashes) on upload and on retrieval.
- Classifier coverage for novel / AI-generated CSAM (Thorn Safer; commercial CSAM-classifier vendors).
- Reporting workflow: NCMEC CyberTipline (US ESPs mandatory under 18 U.S.C. §2258A), IWF (UK), Internet Watch Foundation referrals (EU), per-country National Center referrals; investigation queue with content-preservation per 18 U.S.C. §2258A(h) (preserve 90 days, extension on law-enforcement request).
- Generative-model content-policy: prompt-side prevention (refuse generation), output-side detection (classifier on output before delivery), creator-side attribution (C2PA / watermarking where feasible), distributed-weight model gap (open-weight models that the operator does not control).

Hand off to `incident-response-playbook` for the operational reporting workflow.

**Step 10 — Incident response for child-online-safety incidents.**

Pre-position the multi-jurisdiction breach / harm notification matrix:

- COPPA: no statutory breach-clock specific to under-13 PI; FTC settlement precedent treats child-PI breach as enhanced harm.
- AADC: notification to CA AG aligned to CCPA / California breach-notification timing.
- GDPR Art. 33: 72 hours to supervisory authority for personal-data breaches; child-PI breach is high-severity by default per EDPB guidance.
- UK ICO: 72 hours under UK GDPR.
- AU OAIC: as soon as practicable under Notifiable Data Breaches.
- LGPD: 72 hours indicative.
- DPDPA: 72 hours upon awareness once Rules final.
- CN PIPL: immediate notification to CAC for sensitive PI involving children.
- NCMEC CyberTipline: prompt reporting (no fixed clock but operational expectation is 24 hours from operator awareness) for apparent CSAM under §2258A.
- AU eSafety Commissioner: cyber-bullying / image-based-abuse / class-1 material reporting under OSA.
- UK Ofcom: significant non-compliance with safety duties triggers information-notice + investigation pathway.

Tabletop the AI-chatbot-child-harm scenario (Character.ai-class): notification matrix + parent notification + crisis-line referral + content preservation + regulator engagement. Hand off to `incident-response-playbook` for full workflow.

**Step 11 — Compliance Theater Check.**

Apply the tests in the Compliance Theater Check section below.

**Step 12 — Cross-jurisdiction output reconciliation.**

Produce a single per-control mapping across all in-scope jurisdictions; disparate findings for the same control deficiency across jurisdictions are themselves a finding (reconcile to one consolidated per-control row).

---

## Output Format

The skill produces an Age Gates and Child-Safeguarding Posture Assessment covering US COPPA / CIPA, California AADC, UK Children's Code (ICO), Ireland Fundamentals for a Child-Oriented Approach, EU DSA Art. 28 (online platforms), KOSA (US, where enacted), GDPR Art. 8, AU Online Safety Act + eSafety Basic Online Safety Expectations, and emerging KSA / SG / IN child-protection guidance. The shape below is consumed downstream by `dlp-gap-analysis` (for child-data flow detection), by `incident-response-playbook` (for child-data breach notification clocks), and by `global-grc` (for cross-jurisdictional rollup). Preserve the per-jurisdiction obligation rows verbatim — they are the auditable evidence for regulator inquiries.

Produce this structure verbatim:

```
## Age Gates and Child-Safeguarding Posture Assessment

**Assessment Date:** YYYY-MM-DD
**Entity:** [operator name]
**Scope:** [products / services in scope; cohorts served; jurisdictions]
**Regulatory jurisdictions:** [US COPPA + CIPA + AADC + state laws + KOSA-if-enacted; EU GDPR Art. 8 + DSA Art. 28 + AVMSD + CSAM-Regulation-pending; UK OSA + Children's Code; AU OSA + under-16; IN DPDPA; BR LGPD; CN Minors Protection Law + PIPL Art. 31; SG OSA; JP youth protection; KR PIPA; QC Law 25]

### Likely-Accessed-By-Children Inventory (Step 1)
| Product / Service | COPPA "Directed To" | AADC / UK Children's Code "Likely Accessed" | DSA VLOP / VLOSE | AU Designated | NY SAFE Reach | Other Triggers | Rationale |

### Per-Jurisdiction Compliance Scorecard (Step 2-9)
| Jurisdiction | Regime | Instrument | Operator Obligation | Current Posture | Gap | Theater Risk |
| US | COPPA | 16 CFR Part 312 (2025 Rule) | ... | ... | ... | ... |
| US | CIPA | 47 U.S.C. §254 (E-Rate) | ... | ... | ... | ... |
| US-CA | AADC | Cal. Civ. Code §§1798.99.28-40 | ... | ... | ... | ... |
| US-CA | CCPA / CPRA children | §§1798.120(c), 1798.135 | ... | ... | ... | ... |
| US-NY | SAFE for Kids | S7694A | ... | ... | ... | ... |
| US-states (adult content) | Per-state | TX HB 18 / LA / MT / MS / UT / AR / VA / NC / KY / FL / AL / TN / KS / OK / IN / NE / ID / GA / SD | ... | ... | ... | ... |
| US-fed (pending) | KOSA | Senate-passed 2024; reintroduced 2025 | ... | ... | ... | ... |
| EU | GDPR Art. 8 | Reg. 2016/679 | ... | ... | ... | ... |
| EU | DSA Art. 28 | Reg. 2022/2065 | ... | ... | ... | ... |
| EU | AVMSD Art. 6a + 28b | Dir. 2010/13/EU as amended | ... | ... | ... | ... |
| EU (proposed) | CSAM Regulation | COM(2022) 209 | ... | ... | ... | ... |
| FR | SREN | Loi 2024-449 + ARCOM référentiel | ... | ... | ... | ... |
| UK | Online Safety Act | c. 50 + Ofcom codes | ... | ... | ... | ... |
| UK | Children's Code | ICO 15 standards | ... | ... | ... | ... |
| AU | OSA + under-16 | Online Safety Act 2021 + 2024 amendment | ... | ... | ... | ... |
| IN | DPDPA child provisions | DPDPA s.9 + Draft Rules 2025 | ... | ... | ... | ... |
| BR | LGPD Art. 14 + ANPD Guide | LGPD Art. 14 + Resolution CD/ANPD No. 4/2023 | ... | ... | ... | ... |
| CN | Children Protection + PIPL Art. 31 + Minors Mode | 2020 rev. + CAC 2023 + 2024 Provisions | ... | ... | ... | ... |
| SG | Online Safety + IMDA Code | 2022 amendment + Code of Practice | ... | ... | ... | ... |
| JP | Youth Internet Safety | 2008 Act + per-prefecture | ... | ... | ... | ... |
| KR | PIPA + Network + Youth Protection | PIPA Art. 22-2 + Network Act | ... | ... | ... | ... |
| QC | Law 25 | s.17 + CAI guidance | ... | ... | ... | ... |

### Age-Verification Posture Matrix (Step 3)
| Service | Jurisdiction | Required Assurance | Method In Use | Vendor | IEEE 2089-2021 Level (claimed) | Bias / Equality Evidence | Fallback Route |

### Parental-Consent (VPC) Flow Audit (Step 4)
| Cohort | Jurisdiction | VPC Method | Re-Verification Cadence | Revocation Path | Evidence Retention |

### Data-Collection Minimisation by Cohort (Step 5)
| Cohort | Service | PI Collected | Lawful Basis | Retention | Cross-Border Treatment | Onward Use Restrictions |

### AI-Product Age-Policy Audit (Step 6)
| AI Service | TOS Age Min | Verification | Per-Cohort Capability Gating | Content-Policy Coverage | Crisis Detection / Routing | Child Data in Training |

### Algorithmic-Feed Transparency & Gating (Step 7)
| Service | Feed Type | Non-Personalised Option | Push-Notification Window | Addictive-Design Audit |

### Advertising-to-Children Posture (Step 8)
| Surface | Cohort Detection | Ad-Stack Treatment | Behavioral Ad Blocked? | "Actual Knowledge" Inheritance |

### CSAM Detection Coverage & Reporting Workflow (Step 9)
| Surface | Hash-Match Coverage | Classifier Coverage | Reporting Channel | Preservation Workflow | Generative-Model Policy |

### Incident-Response Readiness for Child-Safeguarding (Step 10)
| Scenario | Notification Matrix | Tabletop Date | Lessons-Learned Status |

### DPIA / Children's Impact Assessment Library (per service × cohort)
| Service | Cohort | DPIA Date | Frameworks Addressed | Outstanding Gaps |

### Compliance Theater Findings (Step 11)
[Outcome of the five tests in the Compliance Theater Check section]

### Defensive Countermeasure Plan (D3FEND)
[D3-MFA, D3-IOPR, D3-CSPP — concrete control placements by layer; see Defensive Countermeasure Mapping]

### Priority Remediation Actions
1. ...
2. ...
3. ...
```

---

## Compliance Theater Check

Apply all five tests. Any failing test inverts the audit outcome — claimed framework coverage is theater regardless of policy documentation, regardless of attestations, regardless of auditor sign-off.

**Test 1 — DPIA / Children's Impact Assessment existence and currency.**

Ask: "Show me your Data Protection Impact Assessment (or Children's Impact Assessment) for every product or feature likely to be accessed by users under 18, dated within the last 12 months, addressing the UK Children's Code 15 standards, AADC obligations, GDPR Art. 35 + Art. 8, DSA Art. 28 where applicable, and DPDPA child provisions where applicable."

- If the answer is "we don't track that audience" or "we're a general-audience platform so we don't have one": ignorance is not exemption under AADC ("likely to be accessed") or UK Children's Code ("likely to be accessed by children"). Theater.
- If a DPIA exists but does not address AI-mediated features (chatbots, ambient features, recommendation): the assessment covers a network that no longer exists. Theater.
- Acceptable: DPIA current within 12 months; per-cohort treatment; AI features assessed; DSA Art. 28 obligations addressed for VLOPs / VLOSEs; ICO Standard 2 (DPIA) evidence current; AADC §1798.99.31 DPIA evidence current.

**Test 2 — Age-verification posture vs. the applicable jurisdictional standard.**

Ask: "For each service in scope, what is your age-verification posture against (a) UK Ofcom 'highly effective age assurance' for any in-scope content under OSA child-safety codes, (b) US state adult-content laws per state of operation, (c) FR ARCOM SREN référentiel for adult video content, (d) AU eSafety age-assurance method under the under-16 social-media regime?"

- If the answer is "we self-declare" or "we have a checkbox for 'I am over X'": that is not Reasonable Verification under any of those statutes. Each named regime explicitly excludes self-declaration. Theater.
- If the answer relies on payment-method age inference alone: insufficient under UK HEAA and most US state laws. Theater.
- If the answer is "we use [vendor]" without effectiveness evidence (vendor assurance report, bias / equality testing, error-band evidence, fallback for users who cannot complete the primary method): partial — the technical-effectiveness evidence is the regulator-facing artefact.
- Acceptable: per-service age-assurance stack documented, vendor-effectiveness evidence retained, fallback documented, IEEE 2089-2021 level claim grounded, bias / equality testing on file, fallback route for users unable to complete the primary method.

**Test 3 — COPPA verifiable parental consent (VPC) flow operationalisation.**

Ask: "Show me your COPPA Verifiable Parental Consent flow end-to-end. For each under-13 user, what method establishes parental status, what evidence is retained, and how is revocation handled?"

- If the answer is "we ask 'are you over 13?' at signup with click-through": that is not VPC. The FTC has settled multiple cases on exactly this pattern (YouTube 2019, Epic 2022). Theater.
- If the answer is a single-method VPC with no fraud detection: the method is potentially valid but the operational gate is weak.
- If 2025 FTC Rule expansions are not reflected (biometric in PI; restricted third-party disclosures; ad-tech inheritance handling): the posture is pre-2025 — partial.
- Acceptable: per-COPPA-permitted-method evidence, fraud-detection on parental-status verification, retention consistent with data-minimisation, revocation path operational, 2025 Rule updates reflected.

**Test 4 — AI chatbot child-online-safety policy and operationalisation.**

Ask: "For each AI chatbot or AI-companion feature reachable by users under 18, show me (a) the per-cohort capability gating, (b) the self-harm / eating-disorder / sextortion / grooming classifier coverage on conversation flow, (c) the crisis-detection routing to human-in-the-loop or crisis-line referral, (d) the child-data-in-training-corpus posture, (e) the parental-tools surface."

- If the answer is "we have a terms-of-service age minimum": post-Character.ai litigation, that is liability shield language, not control. Theater.
- If the answer is "we have content classifiers" without per-cohort gating or crisis-routing: the harm surface is partially covered.
- If child-data-in-training is "we don't separate it" or "opt-out exists but is hard to find": consent-and-control failure.
- Acceptable: per-cohort capability gating documented; classifier coverage + measured precision / recall on conversation flow; crisis-detection routing with operational human-in-the-loop or external referral; child-data-in-training-corpus separation + opt-out + deletion-on-request operational; parental-tools surface available with documented effectiveness.

**Test 5 — Behavioral-advertising-to-children prohibition operationalisation.**

Ask: "Under COPPA, AADC, DSA Art. 28(2), and ANPD 2024 Guide, behavioural advertising to children is prohibited. For each ad-serving surface reaching users under 18, show me the cohort-detection mechanism, the ad-stack treatment (made-for-kids classification + contextual-only fallback + no-profile inheritance through DSP / SSP chain), and the upstream-advertiser 'actual knowledge' inheritance handling."

- If the answer is "we mark made-for-kids content" without per-user cohort detection: surface-level only, not user-level. Theater for any general-audience surface where children create accounts.
- If the answer is "we don't profile children" without evidence in the ad-tech stack: the contractual claim does not survive ad-stack audit. Theater unless the SDP / SSP / DSP chain is gated.
- If the answer relies on age-attribute provisioned from self-declaration: under-detection guaranteed.
- Acceptable: per-user cohort detection at sign-in (with refresh on age-assurance updates), ad-stack treatment propagated through the DSP / SSP chain, contextual-only fallback, "actual knowledge" inheritance documented, transparency reporting available to regulators.

---

## Defensive Countermeasure Mapping

Maps the offensive findings of this skill to MITRE D3FEND v1.3.0+ countermeasure references from `data/d3fend-catalog.json`, with explicit defense-in-depth layer position, least-privilege scope, zero-trust posture, and AI-pipeline applicability (controls that are architecturally impossible in serverless / ephemeral / AI-pipeline contexts must name an explicit scoped alternative).

| D3FEND ID | Technique | Child-Safeguarding Layer Position | Least-Privilege Scope | Zero-Trust Posture | AI-Pipeline Applicability |
|---|---|---|---|---|---|
| D3-MFA | Multi-Factor Authentication | Verifiable Parental Consent (VPC) flow as multi-channel verification — government-ID + photo-match, credit-card + transaction, knowledge-based + return-channel, video-conference, signed-form + return; child-account MFA at signup and on high-risk actions (purchase, friend-request, location-share, livestream initiate); parental-tool access bound to a separate parental identity with its own MFA. | Per-cohort × per-feature: parental identity distinct from child identity; school-tenant teacher identity distinct from child-student identity; AI-companion feature gated to over-18 cohort or to parental-approved over-13 cohort. | Every cohort-sensitive action re-verifies; cohort attribute provisioned by the verifier with limited lifetime; cohort attribute revocable on parental-revocation. | VPC flow applies to AI products whose terms-of-service require under-18 parental approval; for ephemeral / serverless AI-product backends, the VPC verification point is the identity-provider gateway, not the ephemeral compute — never recommend host-agent-only VPC for ephemeral AI workloads. |
| D3-IOPR | Input / Output Profiling | AI chatbot input / output profiling for child-online-safety content moderation including CSAM detection on generative-image output, grooming / sextortion / self-harm / eating-disorder conversation classifier on chat flow, and crisis-detection routing. | Per-cohort classifier sensitivity; under-13 strictest; 13-17 cohort-appropriate; over-18 standard; per-feature scope (companion-mode classifiers stricter than information-mode). | Default-deny on generative output until classifier verdict; conversation continuously profiled with classifier decision logged; vendor-side and operator-side classifier evidence both required (do not rely on vendor attestation alone). | Required for every AI feature reachable by children. For serverless / API-only AI integrations, the profiling point is the API-gateway sidecar layer, not the ephemeral inference compute. |
| D3-CSPP | Client-Server Payload Profiling | Client-server payload profiling for harmful-content detection at the platform boundary: hash-matching (PhotoDNA + NCMEC + IWF) on upload + retrieval; classifier-based CSAM detection on generative-image / video; behavioural-ad payload profiling at ad-stack ingress to enforce no-profile-inheritance for child cohorts. | Per-surface × per-cohort: upload surface vs. retrieval vs. distribution; per-cohort ad-stack treatment with contextual-only fallback; per-tenant treatment for educational deployments. | Continuous verification at the platform boundary, not at the client; classifier verdicts logged with operator-controlled retention; vendor-side ad-stack attestations cross-checked against operator-side profiling. | At AI-API-gateway egress for generated content reaching distribution; at LLM-gateway ingress for prompts originating from child-cohort accounts. For serverless backends the CSPP layer is the gateway, not the ephemeral function. |

Cross-cutting:

- **D3-MFA** is the irreplaceable control for VPC operationalisation. The COPPA-VPC methods are MFA-shaped: a primary verifier + an out-of-band attestation. Without D3-MFA-style multi-channel verification, VPC reduces to single-factor parental-status attestation — the failure mode the FTC has prosecuted repeatedly.
- **D3-IOPR** is the primary content-layer defence for AI-mediated child online safety. Maps directly to the Character.ai-class duty-of-care theory and to KOSA-if-enacted safest-defaults obligations. The required surface is bidirectional (prompt + output) and per-cohort-tuned.
- **D3-CSPP** is the primary gateway-layer defence for CSAM detection on distribution surfaces and for behavioral-ad payload profiling. Maps to the COPPA behavioral-ad prohibition, the DSA Art. 28(2) profiling-ads ban for children, and the NCMEC reporting workflow.

Underlying weakness classes from `data/cwe-catalog.json`: CWE-200 (Exposure of Sensitive Information to an Unauthorized Actor) applies to child PI flowing to advertising / training / cross-border destinations without lawful basis per cohort. CWE-287 (Improper Authentication) applies to the VPC flow — single-channel self-attested parental status is improper authentication for the parental claim. CWE-862 (Missing Authorization) applies to per-cohort × per-feature capability gating that is absent or inconsistent (companion-mode reachable by under-18 cohort; behavioural-ad reachable by under-13 cohort; geolocation toggle defaulting on for child accounts).

---

## Hand-Off / Related Skills

After producing the age-gate / child-online-safety posture assessment, chain into the following skills.

- **`global-grc`** — for jurisdictional regulatory mapping baseline across US (FTC + state AGs), EU (Commission + Member State DPAs + audiovisual regulators), UK (ICO + Ofcom), AU (eSafety + OAIC), IN (DPB + MeitY), BR (ANPD), CN (CAC + MIIT), SG (IMDA + PDPC), JP (PPC + per-prefecture), KR (PIPC + KCC), QC (CAI). The cross-jurisdiction reconciliation step in this skill consumes the global-grc baseline.
- **`dlp-gap-analysis`** — child PI is a protected data class throughout this skill. Hand off for the channel-and-surface DLP matrix when child PI is reaching LLM context windows, MCP tool arguments, RAG corpora, embedding stores, code-completion context, or IDE telemetry. The cross-border treatment (GDPR Art. 44, LGPD Art. 33, DPDPA s.16, PIPL Art. 38-42, KSA PDPL Art. 29, Quebec Law 25 s.17) overlap is identical.
- **`identity-assurance`** — age claims as identity attributes via OpenID Connect age claim extensions (`age_over_13`, `age_over_18`, `age_over_21`); eIDAS / IndiaStack / GOV.UK One Login age-attribute provisioning; child-account MFA posture; parental identity as a distinct identity with its own lifecycle. AAL2 minimum on child accounts where vendor terms permit; AAL3 on parental-tool access for privileged settings.
- **`ai-risk-management`** — AI product age policies (vendor terms-of-service alignment, per-cohort capability gating, content-policy coverage); child data in training corpus (consent, opt-out, deletion-on-request); EU AI Act high-risk classification for AI features serving children; NIST AI RMF + ISO/IEC 42001 child-cohort overlay.
- **`ai-attack-surface`** — red-team coverage on safety filtering for child-relevant topics (self-harm, eating-disorder, grooming, sextortion, CSAM generation); jailbreak resilience on per-cohort capability gating; prompt-injection scenarios that bypass child-cohort controls.
- **`incident-response-playbook`** — multi-jurisdiction breach + harm notification matrix specific to child-online-safety incidents; NCMEC CyberTipline reporting workflow under 18 U.S.C. §2258A; preservation requirements per §2258A(h); AU eSafety reporting; UK Ofcom information-notice pathway; parental notification operationalisation.
- **`coordinated-vuln-disclosure`** — researcher-reported child-safety vulnerabilities (age-gate bypass, parental-tool bypass, content-classifier evasion against child-cohort surfaces, CSAM-detection bypass on generative model) have special handling — coordinated reporting with safety researchers, NCMEC / IWF, and platform safety teams. Vulnerability handling timelines may need to compress relative to standard CVD because of ongoing-harm risk.
- **`compliance-theater`** — extends the five tests above with general-purpose theater detection on the entity's wider GRC posture (auditor sign-off vs. control evidence; multi-jurisdiction reconciliation; vendor attestation vs. operator-side verification).
- **`framework-gap-analysis`** — for multi-jurisdiction reconciliation in Step 12 of the analysis procedure (US + EU + UK + AU + IN + BR + CN + SG + JP + KR + QC + per-state).
- **`sector-healthcare`** — overlap when child PHI reaches AI clinical tools (paediatric ambient-documentation, paediatric decision-support, parent-portal AI features); HIPAA + AADC + Children's Code + GDPR Art. 9 (health data) + Art. 8 (child) stacking on a single product is the operationally hardest cell.

**Sector-education acknowledgment.** A `sector-education` skill does not yet exist in the repository. The K-12 + edtech subset of child online safety — CIPA E-Rate filtering, FERPA + Protection of Pupil Rights Amendment overlap, state student-data-privacy laws (CA SB 1177 SOPIPA + 100+ comparable state laws), DfE UK guidance on edtech, AU national framework for the protection of children, CN MOE guidance on AI in education — would naturally live in that skill. This skill currently covers the cross-cutting age-gates layer that applies to general-audience services and to AI products reaching children. When `sector-education` is created, the K-12-specific obligations move there; the cross-cutting age-gate / VPC / age-assurance / child-cohort-design surface remains here.

---
