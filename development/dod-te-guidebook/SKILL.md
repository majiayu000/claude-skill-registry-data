---
name: dod-te-guidebook
description: "Knowledge base from the DoD Test & Evaluation Enterprise Guidebook (OUSD R&E, August 2022). Use for DoD test and evaluation (T&E) across the Adaptive Acquisition Framework — the four test communities (contractor testing, developmental DT&E, operational OT&E, live-fire LFT&E); the five operational events (Operational Demonstration, EOA, OA, IOT&E, FOT&E) and the OTRR gate; the T&E Strategy / TEMP and its IDSK, with the upstream documents that feed it and the test plans that decompose it; the T&E organizations and oversight roles (USD(R&E), DOT&E, TRMC, the Service Executives and OTAs, the T&E WIPT, CDT); and pathway-specific T&E for all six acquisition pathways (Urgent Capability, Middle Tier, Major Capability, Software, Defense Business Systems). Statutory anchors include 10 U.S.C. §4171 (IOT&E) and §4172 (LFT&E/FUSL). This is guidance, not policy: it points outward to DoDI 5000.89 and the DoDI 5000-series for binding detail, and is thin on detailed test statistics/design-of-experiments methodology, cost estimating, the Acquisition of Services pathway, and any CUI/CAC-gated companion guides."
---

<!-- argument-hint: [test type (DT&E/OT&E/LFT&E/CT), operational event (EOA/OA/IOT&E/FOT&E/ops demo), OTRR, T&E Strategy/TEMP/IDSK, FUSL waiver, T&E organization/role (DOT&E/USD(R&E)/TRMC/OTA/T&E WIPT), acquisition pathway (UCA/MTA/MCA/Software/DBS), chapter number] -->

# DoD Test & Evaluation Enterprise Guidebook (OUSD R&E, August 2022)
**Source**: US Department of Defense (OUSD R&E) — US Government work, public domain; Distribution A | **Chapters**: 8

## When to use
Use this skill when you need to apply, explain, or assess the DoD's test and evaluation approach for defense acquisition: distinguishing the four test communities (contractor, developmental, operational, live-fire) and the five operational events; building or reviewing a T&E Strategy / TEMP and its IDSK; tracing how upstream acquisition documents feed the Strategy and how test plans decompose it; identifying who approves what (USD(R&E), DOT&E, the Service Executives and OTAs, the T&E WIPT) and how the T&E Oversight List changes the approval chain; or planning T&E for any of the six Adaptive Acquisition Framework pathways. This is the OUSD(R&E) companion to the T&E policy in **DoDI 5000.89**; it is **guidance, not policy** — programs tailor it, and binding requirements live in the DoDI 5000-series and Title 10.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below for an overview of the test types, operational events, the T&E Strategy/IDSK, the organizations, and the six pathways.
- **With a topic** — ask about a test type (e.g., "DT&E vs OT&E", "LFT&E and the FUSL waiver"), an operational event (e.g., "IOT&E requirements", "OTRR"), the planning artifacts (e.g., "what goes in a TEMP", "IDSK"), an organization/role (e.g., "what does TRMC do", "DOT&E authority"), or a pathway (e.g., "T&E in the Software pathway", "DBS ATP gates").
- **With a chapter** — ask for `ch01` (test fundamentals & types), `ch02` (T&E Strategy & documentation), `ch03` (organizations, oversight & roles), or a pathway chapter (`ch04` UCA, `ch05` MTA, `ch06` MCA, `ch07` Software, `ch08` DBS).

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### The Four Test Communities

T&E is organized around four test "communities" or types that the Guidebook directs to be **integrated, streamlined, automated, and reused** so one event can feed several evaluations — without letting collaboration replace any dedicated event:

1. **Contractor Testing (CT)** — testing performed by the contractor; government testers leverage it rather than duplicating it.
2. **Developmental Test & Evaluation (DT&E)** — the disciplined generation of substantiated knowledge about a system's capabilities and limitations. Verifies critical technical parameters and KPPs, manages development risk, finds cyber vulnerabilities early, and judges readiness for operational test. Criteria come from the CONOPS/OMS/MP, capabilities documents, and technical/contractual requirements.
3. **Operational Test & Evaluation (OT&E)** — evaluation of how units equipped with the system perform under realistic operational conditions and threats, to judge **operational effectiveness, suitability, and survivability** (10 U.S.C. §4171; DoDI 5000.89).
4. **Live Fire Test & Evaluation (LFT&E)** — characterizes **survivability** (avoid/withstand/recover from combat threats) and **lethality** (defeat expected targets) against likely combat threats (10 U.S.C. §4172).

> **Test ≠ evaluate.** Testing produces data under identified conditions; evaluation interprets that data against criteria. A single test can support multiple evaluations — "collect once, answer many" is the efficiency lever.

### The Five Operational Events (a maturity ladder)

**Operational Demonstration** (characterize maturity/interoperability/risk) → **Early Operational Assessment (EOA)** (early, largely analytical risk read) → **Operational Assessment (OA)** (more realism; risk reduction before IOT&E) → **Initial OT&E (IOT&E)** (statutory; production-representative articles, end-to-end, realistic combat conditions; gates full-rate production) → **Follow-on OT&E (FOT&E)** (confirm fixes, evaluate untested aspects, assess modifications). The **Operational Test Readiness Review (OTRR)** gates entry into operational events by verifying reliability, maintainability, supportability, and hazard/ESOH/software-safety manageability.

### The T&E Strategy / TEMP and the IDSK

The **T&E Strategy** is the principal, pathway-agnostic planning deliverable — and primarily a **stakeholder agreement** on tasks, roles, resources, and responsibilities, not just a document. It appears under several names (TEMP, SAMP, "test strategy") depending on pathway. It must be written early enough to inform the contract and kept as a **living document**. Its central device is the **Integrated Decision Support Key (IDSK)** (required by DoDI 5000.89): a table correlating the **decisions** to be made → the **data** they require → the **sources** (CT/DT/LFT/OT/M&S) that produce it. The Strategy is woven from upstream acquisition documents (JCIDS, AoA, VOLT, Acquisition Strategy, SEP, PPP, cybersecurity/RMF artifacts, APB, CARD, LCSP, ISP, LMDP, RFP) and decomposed downstream into per-event **test plans**.

> **Oversight is a gating switch.** Whether a program is on the **T&E Oversight List** (a joint DOT&E + USD(R&E) product) flips both the Strategy's approval authority (DOT&E vs. Component) and the operational-test-plan regime (DOT&E approval, advance submission, concurrence-before-deviation). Read oversight status first.

### The T&E Organizations (independence by design)

The enterprise deliberately separates those who **develop** a system from those who **judge** it. Two OSD principals split the work by test type: **USD(R&E)** owns DT&E and the test infrastructure (approving the DT&E plan in the TEMP and preparing MS B/C DT&E sufficiency assessments for MDAPs); **DOT&E** owns OT&E and LFT&E policy and approves strategies/plans on the oversight list, reporting independently to the Secretary of Defense and Congress. **TRMC** is the infrastructure landlord (MRTFB, CTEIP, JMETC, NCRC, TENA). Each Service mirrors the pattern: a **T&E Executive** (policy) plus an independent **OTA** (ATEC, OPTEVFOR, MCOTEA, AFOTEC, JITC). At program level the **PM** charters the **T&E WIPT** and names a **Chief Developmental Tester (CDT)**, Lead DT&E Organization, and Lead OTA.

### The Six Acquisition Pathways

T&E adapts to each Adaptive Acquisition Framework pathway, sharing common building blocks (T&E WIPT, IDSK, shared body of evidence, FUSL waiver) tuned to each pathway's clock:
- **Urgent Capability (UCA, DoDI 5000.81)** — 2-year fielding window; parallel phases; tailored Strategy inside the Acquisition Strategy; first unit equipped is the test unit.
- **Middle Tier (MTA, DoDI 5000.80)** — 5-year cap; Rapid Prototyping (ops demo) vs. Rapid Fielding (production tests + IOT&E/OA/ops demo).
- **Major Capability (MCA, DoDI 5000.85)** — deliberate five phases (MSA→TMRR→EMD→P&D→O&S); milestone TEMP at A/B/C/FRP; ITRA/TRA/DTSA/DTA risk stack; IOT&E and FUSL.
- **Software Acquisition (DoDI 5000.87)** — continuous, automated, embedded test; MVP (not operational) → MVCR (triggers IOT&E); BDD/ATDD (Given-When-Then); risk-informed OT&E after MVCR.
- **Defense Business Systems (DBS, DoDI 5000.75)** — five-phase BCAC gated by ATP decisions; COTS/GOTS still needs independent government T&E.
- **Acquisition of Services** — noted in the source as under review; not covered as a chapter here.

### LFT&E and the FUSL Waiver

Live-fire testing runs across the program (component → sub-system → system), culminating in **Full-Up System-Level (FUSL)** testing of a combat-equipped, production-representative system, early enough to fix design deficiencies before going beyond LRIP. **There is no waiver from LFT&E itself** — only from the FUSL/end-to-end requirement, via a PEO→SAE→USD(A&S) chain with DOT&E certification and a two-part congressional package (a certification of need plus an alternative LFT&E plan grounded in actual testing).

---

## Chapter Index

| # | Topic | Key content |
|---|-------|-------------|
| [ch01](chapters/ch01-dod-te-guidebook-te-fundamentals-types-events.md) | T&E Fundamentals & Test Types | The four test communities (CT/DT&E/OT&E/LFT&E); the five operational events; OTRR; the six OT core principles (2019); DT&E vs OT&E vs LFT&E; FUSL and its statutory waiver; the T&E Strategy/IDSK as the spine |
| [ch02](chapters/ch02-dod-te-guidebook-te-strategy-documentation.md) | T&E Strategy & Documentation | The T&E Strategy as a stakeholder agreement; TEMP/SAMP naming; minimum Strategy content; the IDSK; test plans as the execution layer; the upstream supporting documents (Table 1); approval splits on oversight; the MDID reference site; digitization and the data repository |
| [ch03](chapters/ch03-dod-te-guidebook-te-organizations-roles.md) | T&E Organizations, Oversight & Roles | OSD principals USD(R&E) and DOT&E; TRMC and the MRTFB/CTEIP/JMETC/NCRC/TENA; the Service Executives and OTAs (ATEC, OPTEVFOR, MCOTEA, AFOTEC, JITC); the T&E Oversight List; program-level PM/T&E WIPT/CDT roles; independence by design |
| [ch04](chapters/ch04-dod-te-guidebook-urgent-capability-acquisition.md) | T&E in Urgent Capability Acquisition | The UCA pathway (DoDI 5000.81); the two-year clock and cost ceilings; engage T&E at need identification; tailored, mission-focused test plans; the FUSL waiver under compressed schedule; the 60-day oversight rule; post-deployment assessment and disposition |
| [ch05](chapters/ch05-dod-te-guidebook-middle-tier-acquisition.md) | T&E in the Middle Tier of Acquisition | The MTA pathway (DoDI 5000.80); the five-year cap; Rapid Prototyping (ops demo) vs Rapid Fielding (PQT/FAT/AT, IOT&E/OA/ops demo); Strategy to DOT&E ≤45 days before program start; shared data repository and scoring boards; outcome determination and transition decision |
| [ch06](chapters/ch06-dod-te-guidebook-major-capability-acquisition.md) | T&E in Major Capability Acquisition | The deliberate MCA pathway (DoDI 5000.85); five phases and four milestone TEMPs; the risk stack (ITRA/TRA/DTSA/DTA); PDR/CDR; EOA/OA/IOT&E/FOT&E; LRIP and the 10-percent rule; the FUSL waiver chain; production-phase test variety; the Early Fielding report |
| [ch07](chapters/ch07-dod-te-guidebook-software-acquisition.md) | T&E in the Software Acquisition Pathway | The pathway (DoDI 5000.87); Planning vs Execution phases; MVP vs MVCR; continuous, automated, embedded testing; the environment ladder and pipeline/software factory; TDD/BDD/ATDD (Given-When-Then); cyber T&E and cATO; risk-informed OT&E; post-release monitoring as evidence |
| [ch08](chapters/ch08-dod-te-guidebook-defense-business-systems.md) | T&E in the Defense Business Systems Pathway | The DBS pathway (DoDI 5000.75); the five-phase BCAC and ATP gates; COTS/GOTS still needs independent T&E; the CIP and the FDSC; DT&E events (BOT, ACDT, CVI, migration, interface, scalability); the level-of-test determination; IOT&E as a Level 3 event |

## Topic Index

- **Four test communities / CT, DT&E, OT&E, LFT&E / test vs evaluate** → ch01, cheatsheet
- **DT&E (developmental test) — purpose, criteria, cyber, readiness for OT** → ch01, ch06
- **OT&E (operational test) — effectiveness, suitability, survivability** → ch01, ch03
- **LFT&E (live fire), survivability, lethality, FUSL, FUSL waiver** → ch01, ch06, cheatsheet
- **Operational events (Operational Demonstration, EOA, OA, IOT&E, FOT&E)** → ch01, ch06
- **OTRR (Operational Test Readiness Review)** → ch01
- **Six OT core principles (2019) / early operational involvement** → ch01
- **T&E Strategy / TEMP / SAMP — content and approval** → ch02, ch06, cheatsheet
- **IDSK (Integrated Decision Support Key)** → ch02, ch06
- **Test plans / supporting documents (VOLT, SEP, PPP, RFP, AoA)** → ch02
- **T&E organizations — USD(R&E), DOT&E, OSD principals** → ch03
- **TRMC / test infrastructure (MRTFB, CTEIP, JMETC, NCRC, TENA)** → ch03
- **Service T&E Executives and OTAs (ATEC, OPTEVFOR, MCOTEA, AFOTEC, JITC)** → ch03
- **T&E Oversight List / oversight as approval switch** → ch03, ch02
- **T&E WIPT, Chief Developmental Tester, PM roles** → ch03, ch02
- **Urgent Capability Acquisition (UCA) pathway / two-year clock** → ch04
- **Middle Tier of Acquisition (MTA) / Rapid Prototyping / Rapid Fielding** → ch05
- **Major Capability Acquisition (MCA) / milestone TEMP / five phases** → ch06
- **Risk-assessment stack (ITRA, TRA, DTSA, DTA)** → ch06
- **Production tests (PQT, FAT, AT) / LRIP / Early Fielding report** → ch06, ch05
- **Software Acquisition pathway / MVP / MVCR / continuous testing** → ch07
- **BDD / ATDD / TDD / Given-When-Then / pipeline / software factory** → ch07
- **Cyber T&E / cATO / Mission Based Cyber Risk Assessment** → ch07, ch08
- **Defense Business Systems (DBS) / BCAC / ATP gates / COTS GOTS** → ch08
- **Business Operations Testing (BOT), ACDT, CVI, level-of-test determination** → ch08
- **Shared body of evidence / shared data repository / scoring boards** → ch05, ch06, ch07, ch08

## Supporting Files

- [glossary.md](glossary.md) — key DoD T&E terms (test types, operational events, planning artifacts, organizations, pathways, statutory anchors), alphabetical, with chapter references
- [patterns.md](patterns.md) — reusable T&E patterns (decision-first IDSK planning, one body of evidence, T&E in the RFP/contract, embed-OT&E-early, tailoring to the mission, the LFT&E ladder & FUSL waiver, readiness/oversight gating, continuous automated software testing) with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — decision rules, the four-test-community table, the operational-event ladder, the six-pathway map, who's-who organizations, T&E Strategy minimum content, the MCA risk stack, and tells & smells

---

## Scope & Limits

**Covers**: the DoD T&E approach for defense acquisition per the OUSD(R&E) Enterprise T&E Guidebook (August 2022) — the four test communities (CT, DT&E, OT&E, LFT&E) and the distinction between test and evaluation; the five operational events and the OTRR gate; the T&E Strategy / TEMP, its minimum content and IDSK, the upstream documents that feed it and the test plans that decompose it; the T&E organizations and oversight roles (USD(R&E), DOT&E, TRMC, the Service Executives and OTAs, the T&E Oversight List, the program-level PM/T&E WIPT/CDT); LFT&E, FUSL, and the statutory FUSL waiver (10 U.S.C. §4172); IOT&E (10 U.S.C. §4171); and pathway-specific T&E for five of the six Adaptive Acquisition Framework pathways (Urgent Capability, Middle Tier, Major Capability, Software, Defense Business Systems).

**Does not cover in depth**: detailed test statistics, design of experiments, and scientific-test-and-analysis-techniques (STAT) methodology; the cross-cutting **Focus Area** chapters of the full Guidebook (for example, the Modeling & Simulation Focus Area, reliability-growth methods, and the cyber material — a Cyber T&E Focus Area plus its companion guide) — these are referenced but not reproduced here; the **Acquisition of Services** pathway (noted in the source as under review); cost estimating and JCL analysis; contracting law and the FAR/DFARS; and any CUI-marked, CAC-gated, or DOT&E-internal companion guides and procedures. The exact statutory citations, dollar thresholds, and submission timelines are stated as the source presents them and **point outward to the controlling DoDI 5000-series and Title 10** — treat them as pointers to verify against the current instructions, not as binding quotations.

**Policy vs. guidance**: this Guidebook is **guidance**; the binding T&E requirements live in **DoDI 5000.89** and the related 5000-series issuances and Title 10 statutes. Where guidance and policy disagree, defer to policy.

**Source version**: DoD Test & Evaluation Enterprise Guidebook, OUSD(R&E), **August 2022**.

**Jurisdiction**: US Government public domain work (17 U.S.C. §105; Distribution Statement A). Applies to DoD acquisition programs; non-DoD organisations may adopt the framework voluntarily.
