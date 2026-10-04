---
name: coordinated-vuln-disclosure
version: "1.0.0"
description: Coordinated Vulnerability Disclosure for mid-2026 — ISO 29147 (disclosure) + ISO 30111 (handling) + VDP + bug bounty + CSAF 2.0 advisories + security.txt + EU CRA / NIS2 regulator-mandated disclosure + AI vulnerability classes
triggers:
  - cvd
  - coordinated vulnerability disclosure
  - vdp
  - vulnerability disclosure program
  - bug bounty
  - responsible disclosure
  - iso 29147
  - iso 30111
  - csaf
  - security.txt
  - 90-day disclosure
  - project zero
data_deps:
  - cve-catalog.json
  - atlas-ttps.json
  - framework-control-gaps.json
  - zeroday-lessons.json
  - rfc-references.json
  - cwe-catalog.json
  - d3fend-catalog.json
atlas_refs: []
attack_refs: []
framework_gaps:
  - NIST-800-218-SSDF
  - ISO-27001-2022-A.8.8
  - SOC2-CC9-vendor-management
  - NIS2-Art21-incident-handling
  - UK-CAF-D1
  - AU-Essential-8-Patch
rfc_refs:
  - ISO-29147
  - ISO-30111
  - RFC-9116
  - CSAF-2.0
cwe_refs:
  - CWE-1357
d3fend_refs: []
forward_watch:
  - EU CRA Art. 11 implementing regulations and ENISA single-reporting-platform rollout (target operational 2026-09; first manufacturer notifications due 2027-12 per CRA transition timeline)
  - ISO/IEC 29147 and ISO/IEC 30111 revisions expected post-CRA to align "method-neutral" language with EU 24h-notification reality
  - CSAF 2.1 draft (CISA + OASIS working group) — VEX status profile extensions for AI/ML components and SBOM-aligned advisory shape
  - Forthcoming IETF work on AI vulnerability disclosure (proposed BoF under SECDISPATCH) and any update to RFC 9116 (security.txt) covering AI/model artifact disclosure endpoints
  - UK NCSC Vulnerability Disclosure Toolkit revisions and AU ISM CVD guidance updates
  - NYDFS 23 NYCRR 500 amendments potentially adding explicit CVD program requirements
last_threat_review: "2026-09-18"
---

# Coordinated Vulnerability Disclosure

Coordinated Vulnerability Disclosure (CVD) is the public-side mirror of the zero-day learning loop. `zeroday-gap-learn` consumes finished CVEs; `coordinated-vuln-disclosure` runs the upstream pipeline that turns a researcher's email, a bug-bounty report, or a regulator notification into a finished CVE with an advisory the rest of the ecosystem can act on. If the upstream pipeline is broken, the learning loop has nothing to learn from.

This skill operationalizes ISO/IEC 29147:2018 (Vulnerability disclosure), ISO/IEC 30111:2019 (Vulnerability handling processes), and the post-2024 layer of regulator-mandated CVD (EU CRA Art. 11, NIS2 Art. 12, NYDFS 500.17 incident-reporting overlap), plus the publication layer that downstream consumers actually parse (CSAF 2.0 advisories, security.txt per RFC 9116, CVE Records). It also handles the dimension that the ISO standards predate: AI vulnerabilities — model-weight tampering, training-data poisoning, prompt-injection classes — most of which do not fit the versioned-software shape that 29147/30111 assume.

---

## Threat Context (mid-2026)

CVD is no longer optional, and "we have a security@ alias" is no longer a program.

- **EU CRA Article 11** (Cyber Resilience Act, in force since December 2024; manufacturer obligations triggering through 2027) requires every manufacturer placing a product with digital elements on the EU market to operate a CVD process and to notify ENISA and the relevant CSIRT of any *actively exploited vulnerability* within **24 hours** of awareness (early warning), followed by an intermediate report within 72 hours and a final report within 14 days. ENISA's single reporting platform is rolling out 2026-2027; manufacturers without a wired-in CVD pipeline will miss the 24h clock at scale.
- **NIS2 Directive Article 12** mandates EU-wide coordinated vulnerability disclosure with a designated CSIRT acting as coordinator and requires Member States to operate a single point of contact. National implementations vary in maturity but the obligation is binding on essential and important entities from late 2024.
- **NYDFS 23 NYCRR 500.17** (covered entities in NY financial services) requires 72-hour notification for cybersecurity events, which intersects CVD when a disclosed vulnerability becomes a confirmed exploitation. The mapping between "received a researcher report" and "covered cybersecurity event" is ambiguous and most covered entities have not wired it.
- **US**: CISA Binding Operational Directive 20-01 requires federal agencies to publish a VDP; the broader voluntary CISA VDP guidance, the 2021 Executive Order 14028, and NIST 800-218 SSDF v1.1 (PW.4/PS.3/RV.1) push CVD into procurement. UK NCSC publishes a Vulnerability Disclosure Toolkit; AU ISM has CVD guidance in the OFFICIAL/PROTECTED tiers; JP IPA runs the early-warning partnership with JPCERT/CC; SG CSA publishes a Coordinated Vulnerability Disclosure framework; IL INCD operates a national CVD program; the EU's ENISA CSIRTs Network coordinates cross-border.
- **The AI dimension breaks the ISO model.** Anthropic publishes a responsible disclosure policy for Claude (prompt injection, jailbreaks, harmful-output regressions), OpenAI runs a bug bounty for ChatGPT, Microsoft runs an AI bug bounty including Copilot. None of these fit the ISO 29147/30111 assumption that a vulnerability has: (a) a versioned product, (b) a discrete patch shipped at a release boundary, (c) a CVE-shaped advisory. Model-weight vulnerabilities ship as serving-side weight updates without a CVE. Training-data poisoning has no patch — it has a re-training cycle. Prompt-injection classes (per `ai-attack-surface` and `rag-pipeline-security`) are class-level architectural facts, not bugs. The industry has no consensus on how to advertise these, score them, or notify regulators about them.
- **Disclosure cadence is the new CVSS.** Google Project Zero's 90-day-then-disclose policy, CISA's KEV-time disclosure, EU CRA's 24h-clock — each pushes exploit availability earlier in the lifecycle. A CVD program that runs on quarterly engineering cycles is structurally incompatible with the 24h regulatory clock; a CVD program with no intake page (no security.txt, no published policy) does not exist by the EU CRA definition.

The mid-2026 reality: CVD is now infrastructure, not paperwork. An org without a wired CVD pipeline is non-compliant with EU CRA, blind to its own zero-day learning loop, and a single tweet away from a public disclosure with no internal triage clock running.

---

## Framework Lag Declaration

CVD obligations now span four layers — process (ISO 29147/30111), software development (NIST SSDF), governance (SOC 2 vendor management, ISO 27001 vulnerability management), and regulator-mandated reporting (EU CRA, NIS2, NYDFS). Each layer is partially covered; none is sufficient alone.

| Framework / Jurisdiction | Control | What It Says | Why It Fails as a CVD Program Spec |
|---|---|---|---|
| ISO/IEC 29147:2018 | Vulnerability disclosure | Method-neutral guidance on receiving reports, coordinating fixes, publishing advisories. | Predates EU CRA 24h clock, predates AI vulnerabilities, predates CSAF 2.0. "Coordinate disclosure timeline" with no specified clock is incompatible with the 24h regulatory clock. |
| ISO/IEC 30111:2019 | Vulnerability handling processes | Internal handling lifecycle (triage, root cause, remediation). | Same lag: no AI-vuln class, no live-patch concept, no bug-bounty operations guidance, no regulator-notification step. |
| NIST 800-218 SSDF v1.1 | RV.1 (Identify and confirm vulnerabilities) + RV.2 (Assess, prioritize, and remediate) | Producers must receive and act on vulnerability reports. | Per `framework-control-gaps.json` NIST-800-218-SSDF: AI-generated code provenance and model-level vulnerability reports (jailbreaks, prompt-injection regressions, embedding inversion) are not treated on equal footing with code CVEs in PW.4 / PS.3 / RV.1. SSDF is silent on bug-bounty operations, CSAF publication, or regulator-notification clocks. |
| ISO/IEC 27001:2022 | A.8.8 Technical vulnerability management | "Information about technical vulnerabilities shall be obtained, the organization's exposure evaluated, and appropriate measures taken." | Per `framework-control-gaps.json` ISO-27001-2022-A.8.8: "appropriate measures" and "appropriate timescales" are undefined. The control does not require an external-facing CVD intake, does not require CSAF publication, does not require regulator notification, and is silent on AI vulnerability classes. |
| SOC 2 | CC9.2 Vendor management / CC7 (System operations — incident management) | Trust services criteria for vendor risk and incident handling. | Per `framework-control-gaps.json` SOC2-CC9-vendor-management: CC9.2 evaluates vendor controls at procurement-time but does not require evidence of vendor CVD program existence (security.txt, published policy, bug bounty), does not require continuous re-evaluation of vendor disclosure performance, and ignores AI-vendor model-weight disclosure entirely. |
| EU Cyber Resilience Act (Regulation 2024/2847) | Art. 11 — vulnerability handling and reporting | 24h early warning to ENISA/CSIRT for actively exploited vulnerabilities; 72h intermediate; 14d final. Manufacturer CVD process required. Annex I §2 lists vulnerability handling as essential requirement. | The legal obligation is concrete but the operationalization is left to the manufacturer. No prescribed advisory format (CSAF 2.0 is recommended, not mandated). The 24h clock is incompatible with quarterly release cycles. AI products are in scope as "products with digital elements"; the regulation does not yet resolve how model-weight vulnerabilities are reported. |
| EU NIS2 Directive (Directive 2022/2555) | Art. 12 — coordinated vulnerability disclosure; Art. 21 — risk management | Member States designate a CSIRT as CVD coordinator. Essential/important entities must operate CVD. | Member State implementations vary; coordinator-of-coordinators problem unsolved. Essential entities running legacy ISO 29147 programs without CSAF/security.txt are formally compliant but operationally invisible. |
| EU AI Act (Regulation 2024/1689) | Art. 73 — serious incident reporting (high-risk AI) | Providers of high-risk AI systems must report serious incidents to market surveillance authorities. | Defines "serious incident" but not "AI vulnerability." Overlap with CRA Art. 11 is unresolved — a single jailbreak in a high-risk AI system may need to be reported under both, on different clocks, to different authorities. |
| UK NCSC | Vulnerability Disclosure Toolkit | Practical CVD program guidance for UK orgs. | Guidance, not requirement. UK Product Security and Telecommunications Infrastructure Act (PSTI, 2022) requires security update policy publication for consumer connectable products but does not require a full CVD program. |
| AU ISM (OFFICIAL/PROTECTED) | ISM-1616 (vulnerability disclosure program) | Government entities should operate a CVD program. | "Should" not "must" at OFFICIAL; tighter at PROTECTED. Does not specify CSAF, does not specify AI-vuln handling. AU SOCI Act 2018 reporting (12h significant cyber incident) interacts with CVD when disclosure produces a confirmed compromise. |
| JP IPA / JPCERT/CC | Information Security Early Warning Partnership | National coordination scheme for product vulnerability disclosure. | Voluntary partnership, not regulatory mandate. Strong for traditional software vendors, weak for AI/SaaS where there is no product-version boundary. |
| SG CSA | Coordinated Vulnerability Disclosure Framework | National CVD framework for Singapore. | Voluntary. SG Cybersecurity Act 2018 (CCoP for CII operators) requires incident reporting but does not specify CVD program structure. |
| IL INCD | National CVD program | National coordinator. | National-scope coordinator. Defence-sector orgs operate under separate classified processes. |
| NYDFS 23 NYCRR 500.17 | Cybersecurity event notification | 72h notification of cybersecurity events to NYDFS. | Notification-only, not a CVD program spec. The intersection with CVD — "we received a researcher report; is that a cybersecurity event?" — is unresolved in practice. Covered entities without an explicit decision tree default to under-reporting. |

Cross-cutting gap: **no framework treats AI vulnerability disclosure as a first-class category**. ISO 29147/30111, SSDF, ISO 27001, SOC 2, and the regulator regimes all assume versioned-software shape. Model-weight tampering, training-data poisoning, prompt-injection classes, and embedding-space attacks have no native disclosure shape across any of the above. The org-level workaround is to extend the CVD program scope explicitly; the framework-level fix is pending.

---

## TTP Mapping

This skill is meta — it is the upstream input pipeline that feeds the downstream CVE catalog. It does not pin to specific TTPs. Frontmatter `atlas_refs` and `attack_refs` are intentionally empty.

| Input / Output Catalog | Role in the CVD Pipeline |
|---|---|
| `data/cve-catalog.json` | **Downstream product.** Every CVE in this catalog is the output of a CVD process (someone's, somewhere). When this org receives a report covering one of its own products, the resulting CVE enters this catalog via the same schema. |
| `data/zeroday-lessons.json` | **Downstream consumer.** Every disclosed CVE feeds the zero-day learning loop run by `zeroday-gap-learn`. A CVD program with no entries here is not learning from its own disclosures. |
| `data/atlas-ttps.json` (MITRE ATLAS v2026.09) | **Lookup for AI-class disclosures.** When a report covers an AI vulnerability, map the attack mechanism to an ATLAS TTP (e.g., AML.T0051 LLM Prompt Injection, AML.T0110 AI Agent Tool Poisoning) for advisory tagging. |
| `data/framework-control-gaps.json` | **Lookup for regulator-notification routing.** Each disclosure intersects one or more framework controls; this skill writes new gaps when a disclosure exposes one. |
| `data/cwe-catalog.json` | **Required taxonomy for advisories.** Per CVE-Numbering-Authority practice, every CVE advisory cites a CWE. `CWE-1357 Reliance on Insufficiently Trustworthy Component` is invoked for supply-chain disclosures (MCP servers, AI dependencies); other CWEs per the specific class. |
| `data/d3fend-catalog.json` | **Defensive mapping for advisory recommendations.** Advisories that recommend mitigations should cite D3FEND IDs so blue teams can map the recommendation to existing control surfaces. See Defensive Countermeasure Mapping section. |
| `data/rfc-references.json` | **Lookup for protocol-related disclosures.** RFC 9116 (security.txt) is the publication endpoint for CVD intake; it is not currently in `data/rfc-references.json` (cited in prose throughout this skill). The catalog is consulted when a disclosure concerns an RFC-defined protocol (IPsec, TLS, etc.). |

Per `framework-gap-analysis` and `compliance-theater`: a CVD program that exists on paper but produces zero entries in `data/cve-catalog.json` (or its org-internal equivalent) is a process artifact without learning output.

---

## Exploit Availability Matrix

Unlike technical-vulnerability skills, the "availability" question for CVD is about disclosure cadence — how the choice of disclosure clock affects exploit weaponization speed downstream.

| Disclosure Model | Clock | Effect on Exploit Availability | When It Fits | When It Breaks |
|---|---|---|---|---|
| Google Project Zero | 90 days from vendor notification; +14 day grace; **0-day disclosure for actively exploited bugs** | Forces patch availability within 90 days; weaponization typically follows within 7-30 days of disclosure | High-volume vendor with mature CVD; researcher leverage needed | Small vendor / open-source maintainer overwhelmed by 90-day clock; AI vendors without versioned releases |
| CISA KEV-time | Disclosure aligned with KEV listing (active exploitation already confirmed) | Exploit availability is *prior* — disclosure is catching up to reality. RWEP spikes immediately. | Confirmed-exploited CVEs (e.g., CVE-2026-31431 Copy Fail) | Pre-exploitation vulnerabilities; class-level AI findings |
| EU CRA Art. 11 | **24h early warning** to ENISA for actively exploited; 72h intermediate; 14d final | Earliest formal regulator notification clock currently in force globally. Limits weaponization-vs-detection asymmetry. | EU manufacturers in scope; products with digital elements | Non-EU vendors not yet wired into ENISA platform; AI vendors with non-versioned products |
| NIS2 Art. 12 (per Member State CSIRT) | Coordinator-mediated; clock varies | Slower than CRA but broader scope (essential / important entities). | Member State entities | Cross-border coordination friction; coordinator-of-coordinators problem |
| NYDFS 500.17 | 72h | Notification-only; no public advisory implied | NY-licensed financial services | Pre-confirmation reports; AI/SaaS vendor incidents |
| ISO 29147 default | "Coordinate" — no specific clock | Researcher and vendor negotiate. Historically months to years. | Mature vendor + cooperative researcher | Public PoC drops mid-coordination; CRA-regulated products (clock incompatible) |
| Bug bounty (HackerOne / Bugcrowd / Intigriti / Anthropic / OpenAI / Microsoft AI) | Per program — typically 90-180d resolution SLA | Incentivized pre-disclosure pipeline. Weaponization deferred while researchers prioritize bounty payout over public disclosure. | Vendors with funded program; well-scoped attack surface | Critical bugs that exceed bounty ceiling; AI class-level findings that don't fit "specific bug" reward shape |
| AI-vendor responsible disclosure (Anthropic / OpenAI / Microsoft / Google / Meta) | Per program — no industry standard | Disclosure → model-update or serving-update, often **without a CVE or versioned advisory** | Prompt-injection, jailbreak, harmful-output regressions | Customers and regulators who expect CSAF/CVE-shaped output get a blog post instead |

For AI vulnerabilities specifically, the lifecycle is structurally different from software:
- A "patch" is a model retraining or a serving-side update — often without a version identifier the customer can pin.
- A "vulnerability" may be class-level (an entire prompt-injection technique applicable to a family of models) rather than instance-level.
- A "user" of the AI may be a deploying organization rather than an end user, complicating advisory routing.
- Disclosure of prompt-injection class techniques may itself enable copycat exploitation against other AI vendors — the disclosure-as-weaponization asymmetry is amplified.

Translation: the disclosure-clock choice is itself a security decision with downstream RWEP consequences. See `exploit-scoring` for RWEP scoring of disclosed CVEs.

---

## Analysis Procedure

Before stepping through the disclosure-program assessment, thread the three foundational design principles (defense in depth, least privilege, zero trust):

**Defense in depth — disclosure intake as multi-layer pipeline.** A CVD program is not one channel; it is a stack:
- **Layer 1 — public VDP intake**: security.txt (RFC 9116), `/security` web page, published policy, public security@ alias. The minimum visible surface; tested by every script-kiddie scanner before they email the CEO.
- **Layer 2 — incentivized bug bounty**: HackerOne / Bugcrowd / Intigriti / Anthropic / OpenAI / Microsoft program. Pays researchers to come to you instead of dropping on Twitter or selling on a broker market.
- **Layer 3 — internal security testing including fuzz**: hand off to `fuzz-testing-strategy`. Continuous fuzzing (OSS-Fuzz, syzkaller, libfuzzer, AI-assisted fuzz harnesses) finds bugs before researchers do; failure to run this layer is a precondition for the bug bounty being overwhelmed.
- **Layer 4 — third-party pen testing and red-team exercises**: hand off to `attack-surface-pentest`. TIBER-EU style scope, periodic, deliberately targeting the assets the VDP/bounty does not attract researchers to.
- **Layer 5 — customer-driven CVE reports and regulator-routed reports**: ENISA single platform, national CSIRT routing under NIS2 Art. 12, NYDFS notifications, customer enterprise-security teams reporting via account managers.

An org that runs only one layer is brittle. The brittleness pattern: bug bounty without VDP (no public intake for non-bounty-scope reports), VDP without bug bounty (no incentive for high-skill researchers), bounty + VDP without internal fuzzing (third-party finds dominate; signal-to-noise ratio in intake collapses), internal testing only (researchers go elsewhere or sell).

**Least privilege — triage scope is per-report, not org-wide.** Researcher communications channel through a single security@ alias or VDP intake; reproducer assets stored with sealed access; not every engineer needs full pipeline access. The triage role sees all reports; product engineers see only their product's reports; regulator-notification authority is held by a named officer per CRA Art. 11 / NIS2 Art. 12 / NYDFS 500.17. Researchers receive scoped acknowledgment, not internal product detail. Bug-bounty platform admin scope is held by the security team, not engineering managers.

**Zero trust — assume every disclosure is real until proven otherwise.** Do not dismiss researchers based on report writing quality, reputation, or claimed affiliation. Reproduce in isolated environment (D3-RPA — Remote Process Analysis). Treat the researcher's reproducer as adversarial input — it may itself contain payloads targeting the triage environment. Verify reproducer behavior in a sandbox before broad internal distribution. Do not trust the report's classification or severity claim — re-score under RWEP independently (hand-off to `exploit-scoring`). Do not assume the researcher's disclosure window will hold without explicit written agreement.

Then run the program assessment steps:

### Step 1 — Public intake surface (the "do you exist as a CVD target" check)

Test the externally visible CVD surface:
- Fetch `https://<domain>/.well-known/security.txt`. RFC 9116 requires `Contact`, `Expires` (must be in the future; many orgs let this lapse), and recommends `Encryption`, `Policy`, `Acknowledgments`, `Preferred-Languages`, `Canonical`. Without a valid security.txt, the org is not discoverable as a CVD target — an EU-CRA-regulated manufacturer in this state is in early non-compliance.
- Test the `Contact:` channel — does email to it route to a triaged queue? Does it auto-respond with an acknowledgment SLA?
- Fetch the linked `Policy:` URL — does it match an ISO 29147-shaped policy (scope, safe harbor, response times, coordination expectations, public-acknowledgment terms)?
- Verify `Encryption:` URL serves a current PGP key (or modern equivalent — age, signify) if encrypted intake is offered.

### Step 2 — Policy content (the ISO 29147 conformance check)

Audit the published CVD policy:
- **Scope**: what products/services/AI systems are in scope? Out-of-scope assets named?
- **Safe harbor**: explicit good-faith research authorization. Without it, researchers may decline to report or take legal precautions that delay disclosure.
- **Submission expectations**: report shape, reproducer expectations, communication channel.
- **Vendor response SLAs**: initial acknowledgment (target 24-72h), validation (target 5-10 days), remediation timeline (severity-banded), public disclosure timing.
- **Coordination preferences**: disclosure-deadline policy (90-day default? CRA Art. 11 24h for actively exploited?), credit/acknowledgment terms, embargo expectations.
- **Out-of-scope behaviors**: social engineering employees, physical attacks, DoS, etc.
- **AI-system handling**: explicit scope statement for model behavior, prompt-injection classes, training-data concerns, RAG corpus issues — or explicit statement that the policy does not cover these (preferable to silent ambiguity).

### Step 3 — Handling lifecycle (the ISO 30111 conformance check)

Walk the internal handling pipeline:
- **Intake → triage**: how does a report move from VDP queue to product team? Is there a SLA? Is there a named owner per product?
- **Validation**: who reproduces? In what isolated environment (D3-RPA)? What is the false-positive rate?
- **Severity scoring**: CVSS for legacy compatibility, RWEP per `lib/scoring.js` for actual prioritization. CVSS-only scoring fails — never rank disclosures on CVSS alone.
- **Remediation routing**: how does a confirmed vulnerability become a fix? What is the engineering SLA per RWEP band?
- **Verification**: how is the fix confirmed? Researcher re-verification? Internal regression test?
- **Disclosure preparation**: who drafts the advisory? Who approves? When does CVE assignment happen (request from CVE.org or via a CNA partner)?

### Step 4 — Regulator-notification wiring (the EU CRA / NIS2 / NYDFS check)

For each in-scope jurisdiction, verify the notification pipeline:
- **EU CRA Art. 11** (manufacturer in scope): is there a 24h-clock-aware process? Who is the named notification officer? Is there a direct channel to ENISA / national CSIRT? Is the CRA "actively exploited" criterion operationalized — what triggers the clock?
- **EU NIS2 Art. 12** (essential / important entity in scope): which national CSIRT is the designated CVD coordinator? What is the routing? Cross-border coordination plan?
- **EU AI Act Art. 73** (high-risk AI system provider): serious-incident reporting to market surveillance authority. How does this interact with CRA Art. 11 reporting? Same officer? Same clock?
- **NYDFS 500.17** (covered NY financial entity): 72h cybersecurity event notification. Decision tree: when does a received vulnerability report cross into "cybersecurity event" requiring notification?
- **AU SOCI Act** (critical infrastructure): 12h significant cyber incident notification — does an exploited disclosure trigger this?
- **UK NCSC reporting**, **SG CSA reporting**, **JP IPA early-warning partnership**, **IL INCD coordination**: per-jurisdiction routing checked.

### Step 5 — Bug bounty operations (the incentive-layer check)

Audit the bounty program (if operated):
- **Platform**: HackerOne / Bugcrowd / Intigriti / self-hosted? Anthropic / OpenAI / Microsoft AI bounty for AI vendors.
- **Scope clarity**: which assets in scope; out-of-scope explicit. AI-vendor: which models, which surfaces (chat UI, API, plugins/MCP, fine-tuning, embeddings).
- **Severity → payout matrix**: aligned with RWEP, not CVSS alone.
- **Response SLAs**: triage time, payout time, resolution time. Public metrics?
- **Duplicate handling, signal-to-noise ratio**.
- **AI-class submissions**: how are prompt-injection / jailbreak / harmful-output regressions / training-data findings rewarded? Most programs under-pay class-level findings versus single bugs; the structural incentive misalignment pushes class-level AI findings into the academic-paper pipeline instead of the bounty pipeline.

### Step 6 — Learning-loop integration (the `zeroday-gap-learn` hand-off)

For every disclosed vulnerability against an org product:
- The CVE entry in `data/cve-catalog.json` triggers a corresponding entry in `data/zeroday-lessons.json` (every disclosed CVE feeds the zero-day learning loop).
- The CVD program is the source of these entries. If the CVD program is operating but learning-loop entries are not being produced, the hand-off is broken.
- The internal control gap exposed by each disclosure is the input to `framework-gap-analysis` — is the org's own framework coverage missing this control class?

### Step 7 — Advisory publication (the CSAF 2.0 / VEX check)

For each disclosed vulnerability, verify advisory output:
- **CSAF 2.0 advisory** (OASIS CSAF v2.0, published 2022; CSAF 2.1 draft in flight 2026): machine-readable advisory in JSON form, published at `/.well-known/csaf/`. CSAF is the de facto cross-jurisdiction format — CISA, ENISA, BSI, NCSC-NL all consume it.
- **VEX statement** (Vulnerability Exploitability eXchange, CSAF profile): per-product exploitability status. Hand off to `supply-chain-integrity` for SBOM-aligned VEX integration.
- **CVE Record**: filed via CNA (or via CVE.org if no CNA partner). CVE ID assignment timing matters for regulator-notification (CRA Art. 11 references a specific vulnerability identifier).
- **Plain-language advisory**: customer-facing version. Translation of CSAF/VEX into operator action.
- **AI-vendor advisory equivalent**: where the disclosure does not fit CSAF/CVE shape (model-weight class, prompt-injection class), publish a structured advisory using the org's documented AI-vuln-advisory format — and acknowledge in the policy that this format is non-standard.

### Step 8 — Disclosure timeline operations

Operate the disclosure clock per the agreed model:
- **Active-exploitation case**: CRA Art. 11 24h-clock starts at awareness. Notification pipeline runs in parallel with internal triage.
- **Pre-exploitation case**: standard ISO 29147 coordination clock. Default 90-day disclosure unless researcher and vendor agree otherwise.
- **Researcher disclosure-window enforcement**: if the researcher will disclose at day 90 regardless, advisory must be ready at day 89. Vendor cannot extend unilaterally.
- **Embargo break handling**: if disclosure leaks (researcher tweet, broker market, public PoC drop), pivot to immediate-disclosure mode and notify regulators if exploitation evidence emerges.

### Step 9 — Acknowledgment and credit

- Hall-of-fame / acknowledgments page per RFC 9116 `Acknowledgments:` field.
- Researcher credit in advisory, CVE Record, CSAF document `acknowledgments` block.
- Bug-bounty platform payout reconciled with public credit.

### Step 10 — Program metrics and continuous improvement

Per ISO 30111 §5 (continual improvement) and NIST 800-218 SSDF RV.2 (assess, prioritize, remediate):
- Time-to-acknowledge, time-to-validate, time-to-fix (banded by severity / RWEP).
- Disclosure-to-CVE-publication latency.
- Researcher-satisfaction signal (re-disclosure rate, public researcher feedback).
- Regulator-notification on-time rate (24h / 72h / 14d milestones for CRA; 72h for NYDFS; per-jurisdiction).
- Class-level findings vs instance-level findings (AI-vendor relevance).
- Hand off to `framework-gap-analysis` whenever metrics show a control class repeatedly absent from intake.

**Ephemeral / serverless / AI-pipeline reality:** CVD is largely org-process, not infrastructure, so the "is this control architecturally possible in a serverless / AI-pipeline environment" question does not apply in the usual sense. The honest version of the question for THIS skill is: **does your AI / agent pipeline have CVD scope?** Most orgs running production agentic systems do not. The org has a CVD policy covering its web application, its API, and its enterprise software — and silently excludes the LangChain orchestrator, the RAG corpus, the agent toolchain, the MCP-server installations, the model-serving infrastructure, and the fine-tuning pipeline. That silent exclusion is the gap. The fix is to make scope explicit in the published policy: list AI/agent assets in scope or list them as explicitly out-of-scope. Silence is not a posture.

---

## Output Format

The skill produces seven artifacts per program assessment: an ISO 29147-shaped CVD policy text, a `security.txt` file, an ISO 30111-mapped triage workflow, a CSAF 2.0 advisory template, the safe-harbor language, the bug-bounty scope statement, and the jurisdiction-specific disclosure-clock table (EU CRA / NIS2, US, UK, AU, JP, SG). Each artifact is consumed by a different downstream operator: legal review for safe harbor, vendor PSIRT for CSAF, web ops for `security.txt`, executive risk owner for the disclosure-clock table.

### 1. CVD Policy Text (ISO 29147 template)

```
# Coordinated Vulnerability Disclosure Policy — <Organization>

## Scope
In scope: <list of products / services / AI systems>
Out of scope: <list of assets / behaviors>
AI-systems statement: <explicit scope for model behavior, prompt-injection classes,
training-data, RAG corpora, agent toolchains — or explicit exclusion>

## Safe Harbor
We will not pursue legal action for security research conducted in good faith
within the scope and rules below. Specifically: ...

## How to Report
Contact: security@<domain> (also see /.well-known/security.txt)
Encrypted reports: <PGP fingerprint / age recipient>
Bug bounty: <platform URL if any>

## Vendor Response SLAs
Acknowledgment: within <24 / 48 / 72>h
Initial validation: within <5 / 10> business days
Remediation target (RWEP-banded): RWEP 90+ <4h–7d>; 70–89 <30d>; 40–69 <90d>; <40 <next release>
Public disclosure: <90 days> by default; <24h regulator notification> for actively exploited

## Coordination Preferences
Disclosure deadline: 90 days (extensions by mutual agreement)
Embargo: <terms>
Credit / acknowledgment: <terms; opt-in / opt-out>

## Out of Scope Behavior
Social engineering of employees, physical attacks, denial of service, …

## Regulator-Notification Statement
EU CRA Art. 11: actively-exploited vulnerabilities will be reported to ENISA
within 24 hours of confirmation. Where customer notification overlaps with
regulator notification, we will coordinate timing with affected customers
where feasible without delaying the regulatory clock.
```

### 2. Bug Bounty Scope Document

```
# Bug Bounty — <Organization> — Scope

In-scope assets:
  - <domain1> + subdomains
  - <product-API endpoint>
  - <AI system> — surfaces: chat UI, API, plugins/MCP, fine-tuning, embeddings
  - <mobile app bundle IDs>

Out of scope:
  - Marketing sites, third-party SaaS, social engineering, physical, DoS

Severity → payout matrix (USD):
  RWEP 90+ Critical: $<X>
  RWEP 70–89 High:   $<X>
  RWEP 40–69 Medium: $<X>
  RWEP <40 Low:      $<X>
  AI class-level finding (prompt-injection class / training-data class):
    $<X> — flat-rate for class-level discovery regardless of instance count

Duplicate handling: first valid report wins; subsequent dupes get a goodwill credit.
AI / model-weight reports: see additional handling in policy.
```

### 3. security.txt Content (RFC 9116)

```
Contact: mailto:security@<domain>
Contact: https://<domain>/.well-known/security-report
Expires: <ISO date — keep at least 12 months in the future; renew quarterly>
Encryption: https://<domain>/security.asc
Acknowledgments: https://<domain>/security/hall-of-fame
Preferred-Languages: en, <others>
Canonical: https://<domain>/.well-known/security.txt
Policy: https://<domain>/security/policy
Hiring: https://<domain>/security/jobs
```

### 4. CSAF 2.0 Advisory Skeleton

```json
{
  "document": {
    "category": "csaf_security_advisory",
    "csaf_version": "2.0",
    "publisher": {
      "category": "vendor",
      "name": "<Organization>",
      "namespace": "https://<domain>"
    },
    "title": "<Advisory title>",
    "tracking": {
      "id": "<vendor-advisory-id>",
      "initial_release_date": "<ISO timestamp>",
      "current_release_date": "<ISO timestamp>",
      "status": "final",
      "version": "1.0",
      "revision_history": []
    },
    "distribution": { "tlp": { "label": "WHITE" } }
  },
  "product_tree": { "branches": [] },
  "vulnerabilities": [
    {
      "cve": "CVE-YYYY-NNNNN",
      "cwe": { "id": "CWE-1357", "name": "Reliance on Insufficiently Trustworthy Component" },
      "scores": [{ "cvss_v3": {}, "products": [] }],
      "remediations": [],
      "acknowledgments": [{ "names": ["<researcher>"], "organization": "<affiliation>" }]
    }
  ]
}
```

VEX status profile fields (per CSAF VEX profile): `product_status.known_affected`, `known_not_affected`, `fixed`, `under_investigation` — populated per product variant.

### 5. EU CRA / NIS2 Regulator-Notification Template

```
TO: <ENISA single reporting platform> AND <Member State CSIRT>
SUBJECT: CRA Art. 11 Early Warning — <vendor> — <advisory-id>
TIMESTAMP: <ISO timestamp, <24h from awareness>

1. Manufacturer identity: <name, address, contact, EU representative if applicable>
2. Product affected: <name, versions, CPE if available>
3. Vulnerability summary: <2-3 sentences, no exploitation detail>
4. Awareness timestamp: <when did manufacturer become aware>
5. Active exploitation evidence: <basis for "actively exploited" determination>
6. Affected user population estimate: <count or range>
7. Mitigation status: <available / in development / not yet available>
8. Coordination point of contact: <named officer, email, phone>
9. Next milestone: 72h intermediate report at <ISO timestamp>
```

For NYDFS 500.17 / AU SOCI / UK / SG / JP / IL: parallel templates per jurisdiction; the same disclosure event may trigger several in parallel.

### 6. Intake-to-Disclosure Timeline Tracker

| Phase | Event | Target SLA | Actual | Owner |
|---|---|---|---|---|
| T+0 | Report received via VDP / bounty / direct | — | — | Triage |
| T+24h | Acknowledgment sent to reporter | 24h | — | Triage |
| T+5d | Validation complete; RWEP scored | 5d | — | Product + Security |
| T+24h (parallel, if exploited) | EU CRA Art. 11 early warning sent | 24h from awareness | — | Named officer |
| T+72h (parallel, if exploited) | Intermediate regulator report | 72h | — | Named officer |
| T+30d (RWEP-banded) | Patch shipped | per band | — | Engineering |
| T+14d (parallel, if exploited) | Final regulator report | 14d | — | Named officer |
| T+disclosure-day | CSAF advisory published; CVE record live; researcher acknowledged | per agreed window | — | Security + Comms |
| T+disclosure+1d | Entry filed in `data/zeroday-lessons.json` (zero-day learning loop) | 1d | — | Security |

### 7. Program Metrics Report

```
Window: <Q-N>
Reports received: <N>
Median time-to-acknowledge: <Xh>
Median time-to-validate: <Xd>
Median time-to-fix (RWEP 90+): <Xh / Xd>
Disclosure-to-CVE-publication latency: <Xd>
EU CRA Art. 11 24h on-time rate: <X%>
NIS2 / NYDFS / SOCI / IL / SG / JP / UK on-time rate per jurisdiction: <X%>
AI class-level findings: <N> (flat-rate paid: <$X>)
Hall-of-fame entries added: <N>
zeroday-lessons.json entries filed: <N>
framework-control-gaps.json entries added or updated: <N>
```

---

## Compliance Theater Check

Four concrete tests distinguish a real CVD program from CVD theater. Run them in order — each filters out a tier of paper compliance.

> **Test 1 — Publish your security.txt URL right now.** Fetch `https://<domain>/.well-known/security.txt`. If it 404s, the org has no public CVD intake — which means no compliance with EU CRA Art. 11 (manufacturers must operate a CVD process; "operate" requires discoverability), no NIS2 Art. 12 coordinator wiring, no RFC 9116 conformance, and the next researcher who finds something will email the CEO or drop on social media. The org will discover this when a Reuters reporter calls. If security.txt exists but `Expires:` is in the past, the org once had a program and stopped operating it — same outcome, with the additional signal that internal ownership has lapsed.

> **Test 2 — Show me your last 12 months of received disclosures and time-to-fix per severity band.** If the answer is "we don't track that," there is no program — only a queue. If the answer is "we track it, here are the numbers," compare time-to-fix against RWEP bands: median time-to-fix for RWEP 90+ must be measured in hours-to-days, not weeks. CVSS-banded SLAs alone are insufficient. If the org cannot produce metrics, the org cannot demonstrate continuous improvement per ISO 30111 §5 or NIST 800-218 RV.2, so the formal compliance with those controls is theater regardless of policy text.

> **Test 3 — Show me a single CSAF 2.0 advisory you've published, with a CVE ID, in the last 12 months.** If the answer is "we publish blog posts" or "we wait for the CVE to appear in NVD" or "our security advisories are PDF attachments," downstream consumers (customers, regulators, automated patch-management systems) cannot ingest the disclosures. The org's disclosure posture is theater for the machine-readable era. Under EU CRA Art. 11, the advisory format is left to the manufacturer but consumers and regulators are converging on CSAF 2.0; an org that has never published one is not operating in the de facto downstream ecosystem.

> **Test 4 — What is your AI vulnerability disclosure handling?** Three failure modes signal theater: (a) "same as software CVEs" — the org has not engaged with the class-level reality and the lack of versioned-patch shape; (b) "we don't run AI systems" — verify against actual product surface (most orgs do, often via embedded Copilot / Claude / ChatGPT integrations, RAG features, internal agentic workflows); (c) "we have a separate process but it's not published" — the published policy must state AI scope or explicitly exclude it. Silence is the failure. If the org operates a high-risk AI system under EU AI Act Art. 73 with no serious-incident notification pipeline, that is a regulatory failure on top of the disclosure-posture failure.

A program passing all four tests is operating CVD as infrastructure. A program failing any one is operating CVD as paperwork — and the next disclosure will expose the gap publicly.

---

## Defensive Countermeasure Mapping

Maps this skill's findings to MITRE D3FEND IDs from `data/d3fend-catalog.json` with explicit defense-in-depth layer position, least-privilege scope, zero-trust posture, and AI-pipeline applicability.

CVD is process infrastructure, not a single technical control — the D3FEND mapping is therefore thin and concentrated at the triage and post-disclosure boundaries.

| D3FEND ID | Where It Applies in CVD | Defense-in-Depth Layer | Least-Privilege Scope | Zero-Trust Posture | AI-Pipeline Applicability |
|---|---|---|---|---|---|
| **D3-RPA** (Remote Process Analysis) | Reproducer execution and triage. Researcher-submitted reproducers are adversarial input; execute in isolated environment with telemetry. | Triage layer (between intake and validation). | Triage analysts only; product engineers receive reproduced findings, not raw researcher payloads. | Verify reproducer behavior in sandbox; do not trust the report's classification or the researcher's environment claims. | Applies — AI-vuln reproducers (jailbreak prompts, training-data poisoning payloads) must run in isolated model-serving environments. The reproducer prompt may itself be designed to exfiltrate triage-environment data. |
| **D3-NTA** (Network Traffic Analysis) | Post-disclosure exploitation monitoring. Once an advisory ships, attacker weaponization typically follows within days; egress monitoring detects active exploitation against unpatched customers. | Detection layer (post-disclosure, downstream of CVD output). | Detection scoped to known exploit indicators from disclosed CVE; not all-traffic surveillance. | Assume disclosed CVEs will be exploited; verify exploitation evidence per advisory IOCs. | Limited direct applicability — AI exploitation traffic often blends with legitimate AI API usage (see `ai-c2-detection`); D3-NTA on its own is insufficient. |
| **D3-EAL** (Executable Allowlisting) | Post-disclosure blocking of known weaponized exploits. When a public PoC ships with the advisory, allowlisting blocks the exploit binary class from execution on patched/unpatched endpoints alike. | Prevention layer (post-disclosure, downstream of CVD output). | Endpoint scope; allowlist administered by endpoint-security team, not application teams. | Default-deny; verify executable signatures and allowlist membership per execution. | Limited — AI exploits are typically prompt-class, not binary-class. D3-EAL applies to traditional-software exploits derived from CVD output, not AI-class disclosures. |

**Explicit statement (no orphaned controls)**: CVD itself is process infrastructure. The technical defensive layers it *feeds* are the D3FEND techniques above plus the broader cross-walk in `defensive-countermeasure-mapping`. A CVD program with no downstream defensive-control hand-off is producing advisories that no operator action follows — which is the post-disclosure equivalent of compliance theater.

**AI-pipeline statement**: D3FEND's current coverage of AI-vulnerability defenses is sparse. Mid-2026 D3FEND additions (per `data/d3fend-catalog.json` forward-watch) are extending into AI-system telemetry; the gap until then is filled by `ai-attack-surface`, `rag-pipeline-security`, and `ai-c2-detection` skill-specific recommendations.

Reference `defensive-countermeasure-mapping` for the full cross-walk; reference `framework-gap-analysis` for the regulatory-control gaps each defensive layer leaves open.

---

## Hand-Off / Related Skills

CVD sits at the upstream end of several skill pipelines. Route to the following on the indicated trigger:

- **`zeroday-gap-learn`** — *downstream consumer of CVD reports.* Every disclosed CVE against an org product triggers a learning-loop entry. If CVD output is not producing `data/zeroday-lessons.json` entries, the hand-off is broken. Run `zeroday-gap-learn` for every advisory shipped.
- **`exploit-scoring`** — *RWEP scoring of disclosed CVEs.* CVSS alone is insufficient; route every confirmed-validated disclosure through RWEP scoring before regulator notification (the "actively exploited" determination depends on it).
- **`supply-chain-integrity`** — *CSAF VEX integration with SBOM.* When the disclosure affects a product component shipped to downstream consumers, the CSAF advisory's VEX status profile must align with the SBOM produced under SLSA / CycloneDX / SPDX. Hand off for the supply-chain-shaped output.
- **`framework-gap-analysis`** — *CVD failures often expose framework gaps.* When a disclosure shows that an existing control (SI-2, A.8.8, CC9.2, SSDF RV.1) was insufficient to prevent or detect the vulnerability, file the gap under the appropriate framework entry per `data/framework-control-gaps.json`.
- **`compliance-theater`** — *publish-no-VDP theater test.* The four compliance theater checks in this skill compose with the broader theater detection across frameworks; run `compliance-theater` after this skill when the org is claiming SOC 2 / ISO 27001 / NIST CSF maturity that the CVD test results contradict.
- **`fuzz-testing-strategy`** — *Layer 3 of defense-in-depth.* Continuous fuzzing pre-empts external disclosure; weak fuzzing makes the bug-bounty intake overwhelmed by findings the org should have found internally.
- **`attack-surface-pentest`** — *Layer 4 of defense-in-depth.* TIBER-EU-style red team exercises target the assets that VDP/bounty does not attract researchers to.
- **`defensive-countermeasure-mapping`** — *full D3FEND cross-walk* beyond the three IDs cited in the Defensive Countermeasure Mapping section above.
- **`global-grc`** — *cross-jurisdiction routing* when the disclosure intersects multiple regulator regimes (EU CRA + NIS2 + AI Act + NYDFS + AU SOCI + IL INCD + SG CSA + JP IPA + UK NCSC), which is the common case for multi-jurisdictional organizations.
