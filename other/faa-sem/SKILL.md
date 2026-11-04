---
name: faa-sem
description: "Knowledge base from the FAA Systems Engineering Manual (SEM) v1.0.1. Use for civil-agency systems engineering as the FAA practices it inside the Acquisition Management System (AMS) and the National Airspace System (NAS): the five-phase AMS lifecycle and its decision points; operational concept development and implementation-free functional analysis (ConOps, FFBD/N², CMLs); requirements analysis and architectural design synthesis (PRS→MRS, the PRD ratchet pPRD→iPRD→fPRD, RAM, ISEF/DoDAF views, CPRs); the seven technical management disciplines (Integrated Technical Management/SEMP, Interface Management/IRD-ICD, Risk-Issue-Opportunity, Configuration Management, SE Information Management, Decision Analysis, Verification & Validation); and the specialty disciplines (RMA via Service Threads/STLSC, Life Cycle Engineering, E3/Spectrum, Human Factors, Information Security via the NIST RMF, System Safety via the SMS, and Hazardous Materials/Environmental/EOSH). Scope limits: this is FAA-specific guidance, not policy — it is a tailorable menu that points outward to companion handbooks (FAA-HDBK-006A for RMA, the SMS Manual, the NIST 800-series) rather than restating generic SE theory; it is thin on detailed cost estimating, contracting/FAR law, software-development methodology, named anti-pattern catalogues, and any non-FAA or non-civil-aviation lifecycle. Source has no page numbers in the extracted text (~360 pp.)."
---

<!-- argument-hint: [AMS phase/decision point, ConOps, functional analysis, FFBD/N², requirements/PRS/MRS/PRD, architecture/RAM, SEMP, interface/IRD/ICD, RIO risk, configuration management, V&V, decision analysis, RMA/Service Thread, spectrum, human factors, information security, system safety, environmental/EOSH, chapter number] -->

# FAA Systems Engineering Manual (SEM) v1.0.1
**Source**: FAA — US Government work, public domain | **Chapters**: 7

## When to use
Use this skill when you need to apply the FAA Systems Engineering Manual (SEM v1.0.1) to civil-agency SE work inside the FAA Acquisition Management System (AMS) and the National Airspace System (NAS). It covers the five-phase AMS lifecycle and its decision points, operational concept development and implementation-free functional analysis, requirements analysis and architectural design synthesis (including the pPRD to fPRD maturity ratchet), the seven technical management disciplines (SEMP, interface management, risk/issue/opportunity, configuration management, SE information management, decision analysis, and V&V), and specialty disciplines including RMA via Service Threads, human factors, information security via the NIST RMF, and system safety via the SMS. Use it when planning or executing SE activities on an FAA program and when you need to understand which SEM discipline or process applies to a given lifecycle decision.

**Prerequisites:** none, plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the Core Frameworks below for the AMS lifecycle backbone, the front-end concept/functional/requirements/architecture flow, the seven technical management disciplines, and the specialty disciplines.
- **With a topic** — ask about an AMS phase or decision point, a front-end process (ConOps, functional analysis, FFBD/N², CMLs), requirements (PRS→MRS, the pPRD→iPRD→fPRD ratchet, CPRs, VRTM), architecture (RAM, ISEF/DoDAF views, the design vs. requirements loops), a technical-management discipline (SEMP, interfaces/IRD-ICD, RIO risk, CM/baselines, SEIM, decision analysis, V&V), or a specialty (RMA/Service Threads, LCE/ILS, E3/Spectrum, Human Factors, Information Security/RMF, System Safety/SMS, environmental/EOSH).
- **With a chapter** — ask for `ch01` (intro & AMS lifecycle), `ch02` (concept & functional analysis), `ch03` (requirements, architecture, M&S), `ch04` (technical management, interfaces, risk), `ch05` (CM, SEIM, decision analysis, V&V), `ch06` (RMA, LCE, E3/Spectrum, HFE), `ch07` (infosec, safety, environmental).

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### The AMS Lifecycle — the spine of the whole manual
The FAA wraps SE around its **Acquisition Management System (AMS)**: five phases punctuated by five numbered decision points. A solution begins as an identified *service need*, matures through analysis and development, and ends as a fielded capability sustained until replaced or retired.

1. **Service Analysis & Strategic Planning** → (1) Concept & Requirements Definition Readiness Decision
2. **Concept and Requirements Definition (CRD)** → (2) Investment Analysis Readiness Decision
3. **Investment Analysis (Initial → Final IA)** → (3) Initial Investment Decision · (4) Final Investment Decision
4. **Solution Implementation** (Product Realization → Deployment & Transition) → (5) In-Service Decision
5. **In-Service Management** (operational analysis feeds shortfalls back to the front)

Two altitudes run throughout: the **enterprise level** (integration across investment programs, EA roadmaps, portfolio alignment) and the **program level** (optimizing one solution). SE is a **distributed skill set**, not a job title — the "Systems Engineering Role" describes a function being performed, whoever holds the badge.

### The maturity ratchet
Each phase raises the resolution of the same few things — the need, the requirements, the alternatives, the cost estimate, the safety picture. **Requirements maturity is the program's pulse**: pPR/pPRD → iPR/iPRD → fPR/fPRD → system specifications, kept in lockstep with the contracts track (SIRs, Statements of Work) and the enterprise architecture. An approved **fPRD with an 80%-stable set** gates the Final Investment Decision.

### Front end: keep "what for / what / how" separate
- **Operational Concept Development** fixes *what the solution is for and how it will be used* → a vetted **ConOps** plus preliminary shortfall, benefit, safety, and risk analyses. **Concept Maturity Levels (CML 1–4)** give a shared maturity vocabulary that drives funding and research priorities.
- **Functional Analysis** fixes *what it does* — implementation-free. **Functions are never allocated**; you convert function → **PRS → MRS** (requirement), and the *requirement* is allocated to the physical architecture. A complete functional model needs **both** the **FFBD** (control/sequencing) and the **N²** (data/interfaces). Output: the seven-part **Functional Architecture Document (FAD)**.
- **Physical architecture** answers *how* — deferred until the problem is understood.

### Requirements & architecture (SEM 3.3–3.5)
- **Requirements Analysis = Development + Management.** Author with `shall`/`will`/`may` (never `should`, never `and/or`); every requirement carries a verification method (Inspection/Analysis/Demonstration/Test) rolled into the **VRTM**. **CPRs** are the minimal make-or-break performance requirements, copied verbatim into the **APB**.
- **Architectural Design Synthesis** develops alternatives, allocates requirements via the **RAM**, and evaluates alternatives on cost/schedule/performance/risk. Read the *pattern* of failure: **all alternatives fail the same requirements → design loop** (back to functions); **compliance varies → requirements feedback loop**.
- **Modeling, simulation & prototyping** buy down risk before fielding; match fidelity to value-of-information.

### The seven technical management disciplines (over a mandatory QMS)
Integrated Technical Management · Interface Management · Risk Management (RIO) · Configuration Management · SE Information Management · Decision Analysis · Verification and Validation.
- **ITM = plan + control:** SEMP (Program + Contractor variants) → ISPD → Life Cycle Plan, then monitor via TPM/CPR/EVM and control via reviews and audits (`TRA·SRR·SDR·SSR·PDR·CDR·TRR·ISR·FCA·PCA·PRR`).
- **Interfaces:** the **ICD complies with the IRD complies with the fPRD**; change runs the other way (ICR → IWG → CM).
- **RIO triage by one temporal question** (*has it happened yet?*): future-negative = **Risk**, realized-negative = **Issue** (no likelihood), future-positive = **Opportunity**. Plan strategies: Avoid/Transfer/**Control**/Accept/Research-and-Knowledge; roll up the **maximum** risk through the WBS/IMS.
- **CM** holds the *product* truth (five baselines: Functional/Allocated/Product/Facility/Operational) under CCB control; **SEIM** holds the *project* truth as a PDCA cycle (acquire→validate→maintain→distribute→archive→retire).
- **Decision Analysis** is tool-agnostic — match technique fidelity to decision stakes; DA recommends, the authority decides.
- **V&V:** verification = "built right" (incremental, DT); validation = "right thing" (iterative, early, OT/IOA), anchored in the V model and the VRTM.

### Specialty engineering — front-loaded and wired back in
Cost is front-loaded, pain is back-loaded, so each discipline starts its own closed-loop risk cycle early and routes outputs back into requirements, risk, and V&V.
- **RMA:** allocate dependability by **Service Thread / STLSC** (Essential .9999, Efficiency-Critical .99999, Safety-Critical = two independent .99999 threads), *not* by an availability spec for software-intensive systems; validate via reliability growth with Government-controlled "expunging."
- **Life Cycle Engineering / ILS:** early decisions lock in most lifetime cost (support can exceed 70% of operations budget); favor technology insertion over wholesale replacement.
- **E3 / Spectrum:** EMC is a bidirectional relationship, not a property; FCC compliance is necessary but not sufficient. Spectrum is a scarce governed resource — no RF system fields without an assignment.
- **Human Factors:** operators and maintainers are first-class system elements (Human Performance Interfaces taxonomy + 24 Areas of Interest).
- **Information Security:** categorize-then-tailor under FIPS 199/200 and the **NIST RMF**; the FAA Security Authorization (FAA Order 1370.82A) accepts residual risk via POA&Ms toward ongoing authorization.
- **System Safety:** the **SMS** five-phase SRM loop and the OSA→CSA→PHA→SSHA→SHA→O&SHA→SSAR analysis ladder.
- **HMM/EE/EOSH:** bidirectional, cradle-to-grave compliance (CAA, CWA, NEPA, RCRA, OSHA) folded into the APB.

---

## Chapter Index

| # | Chapter | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-faa-sem-introduction-ams-lifecycle.md) | Introduction & the AMS Lifecycle | Purpose of the SEM, the five AMS phases and decision points, enterprise vs. program SE, SE as a distributed skill set, the requirements maturity ratchet, PDCA, System of Systems, ISO 15288 mapping, NextGen |
| [ch02](chapters/ch02-faa-sem-concept-functional-analysis.md) | Operational Concept Development & Functional Analysis | Concept development/validation, ConOps, shortfall analysis, OI/OS, CML 1–4, implementation-free functional decomposition, FFBD & N², PRS, the Functional Architecture Document (FAD) |
| [ch03](chapters/ch03-faa-sem-requirements-architecture-crosscutting.md) | Requirements, Architectural Design Synthesis & Cross-cutting Methods | Requirements Development + Management, PRS→MRS, directive verbs & quality characteristics, VRTM, pPRD→iPRD→fPRD, Type A/B/C specs, CPRs, RAM, ISEF/FEAF/DoDAF views, design vs. requirements loops, modeling/simulation/prototyping |
| [ch04](chapters/ch04-faa-sem-technical-management-interface-risk.md) | Integrated Technical Management, Interface Management & Risk | Seven TM disciplines over a QMS, SEMP/CSEMP, ISPD, WBS, TPM/CPR/EVM, control gates & audits, IRD/ICD compliance chain, IWG/ICR, Risk-Issue-Opportunity five-step process, RMB & status lifecycle, PID |
| [ch05](chapters/ch05-faa-sem-configuration-decision-vv.md) | Configuration Management, SEIM, Decision Analysis & V&V | FAA Order 1800.66, CCB/NAS CCB/CCD, the five baselines, change vehicles (ECP/NCP/PTR/HDR), CSA/MCI, SEIM PDCA lifecycle, decision-analysis techniques & fidelity, the V model, DT/OT/IOA, VRTM, TEMP |
| [ch06](chapters/ch06-faa-sem-specialty-rma-lifecycle-e3-humanfactors.md) | Specialty Engineering I — RMA, LCE, E3/Spectrum, Human Factors | Why the FAA distrusts availability, Service Threads & STLSC, the three availability constructs, six RMA tasks, FTA & FMEA/FMECA, reliability growth/expunging, LCE & ILS/NAILS, ISPR/OEA/ISR, E3 vocabulary, spectrum management, Human Factors Engineering |
| [ch07](chapters/ch07-faa-sem-specialty-infosec-safety-environmental.md) | Specialty Engineering II — Information Security, System Safety, Environmental | ISE (Clinger-Cohen/FISMA, FIPS 199/200, NIST RMF & SP 800-series, Security Authorization, POA&M, ISCM), SSE (SMS, SRMGSA, SRM loop, OSA→SSAR ladder), HMM/EE & EOSH (CAA/CWA/NEPA/RCRA/OSHA, cradle-to-grave) |

## Topic Index

- **AMS lifecycle / phases / decision point** → ch01
- **Enterprise vs. program SE / System of Systems / SoS** → ch01
- **ISO 15288 mapping / NextGen / PDCA** → ch01
- **Operational Concept Development / ConOps / shortfall** → ch02
- **Concept Maturity Levels / CML** → ch02
- **Functional Analysis / FFBD / N-squared** → ch02
- **Functional Architecture Document / FAD / PRS** → ch02, ch03
- **Requirements Analysis / requirements development** → ch03
- **MRS / directive verbs / requirements quality** → ch03
- **VRTM / verification method** → ch03, ch05
- **Program Requirements Document / pPRD / iPRD / fPRD** → ch03
- **Critical Performance Requirements / CPR** → ch03, ch04
- **Architectural Design Synthesis / RAM / architecture views** → ch03
- **Modeling and simulation / prototyping** → ch03
- **Integrated Technical Management / SEMP / ISPD / WBS** → ch04
- **Technical Performance Measurement / TPM / EVM** → ch04
- **Interface Management / IRD / ICD / IWG** → ch04
- **Risk Issue Opportunity / RIO / risk** → ch04
- **Configuration Management / baseline / CCB** → ch05
- **SE Information Management / SEIM** → ch05
- **Decision Analysis** → ch05
- **Verification and Validation / V model** → ch05
- **RMA / Service Thread / availability** → ch06
- **Life Cycle Engineering / ILS / supportability** → ch06
- **E3 / electromagnetic / spectrum** → ch06
- **Human Factors Engineering** → ch06
- **Information Security / RMF / security authorization** → ch07
- **System Safety / SMS / hazard** → ch07
- **Environmental / EOSH / hazardous materials** → ch07

## Supporting Files

- [glossary.md](glossary.md) — key FAA SEM terms (AMS lifecycle, ConOps, PRS/MRS, RAM, SEMP, IRD/ICD, RIO, baselines, Service Thread/STLSC, SMS, RMF), alphabetical, with chapter references.
- [patterns.md](patterns.md) — 12 reusable SE patterns (maturity ratchet, implementation-free front end, FFBD+N², design vs. requirements loops, 80%-stability gate, RIO triage, max-risk roll-up, Service-Thread allocation, front-loaded specialty engineering, categorize-then-tailor security, DA fidelity, interface compliance chain) with When/How/Trade-offs.
- [cheatsheet.md](cheatsheet.md) — decision rules, the AMS lifecycle table, the five baselines, reviews/audits, RIO at a glance, the interface compliance chain, STLSC targets, specialty-engineering anchors, and tells & smells.

---

## Scope & Limits

**Covers**: civil-agency systems engineering as the FAA's Systems Engineering Manual v1.0.1 institutionalizes it inside the Acquisition Management System and the National Airspace System — the five-phase AMS lifecycle and decision points; operational concept development and implementation-free functional analysis; requirements analysis and architectural design synthesis (PRS→MRS, the PRD ratchet, RAM, ISEF/DoDAF views, CPRs, VRTM); the seven technical management disciplines (ITM/SEMP, Interface Management, Risk-Issue-Opportunity, Configuration Management, SEIM, Decision Analysis, V&V); and the specialty disciplines (RMA via Service Threads, Life Cycle Engineering/ILS, E3/Spectrum, Human Factors, Information Security via the NIST RMF, System Safety via the SMS, and Hazardous Materials/Environmental/EOSH).

**Does not cover in depth** (where the source is thin or points elsewhere): the SEM is a **pointer document** — RMA detail lives in the FAA RMA Handbook (FAA-HDBK-006A), safety method detail in the SMS Manual and SRMGSA, and information-security control detail in the NIST 800-series; use those for discipline depth. The manual is **guidance, not policy** (binding policy is the AMS itself, via FAST). It does **not** develop generic SE theory (read the NASA SE Handbook, the DAU SE Guidebook, the SEBoK, or ISO/IEC/IEEE 15288 for that); it is thin on detailed cost estimating and earned-value mechanics, contracting/FAR-DFARS law, software-development methodology, and a labeled catalogue of named anti-patterns (it gives positive guidance with scattered cautions). It does not address non-FAA, non-civil-aviation, or international lifecycles except where it maps to ISO 15288 and DoDAF.

**Jurisdiction & version**: FAA Systems Engineering Manual, **Version 1.0.1 (2014-06-19)** — US Government work, public domain. The extracted source text carries no page numbering (estimated ~360 pp.). Applies to FAA acquisitions affecting the NAS; other organisations may adopt the framework voluntarily. Replaces the 2006 NAS SEM v3.1.
