---
name: faa-ams-vv
description: "Knowledge pack synthesized from FAA AMS Lifecycle Verification and Validation Guidelines, Version 4.0 (January 2023): verify-vs-validate, the three tiers, decision-point-gated V&V across the AMS lifecycle, and shift-left. SCOPE LIMITS: single-source (the January 2023 guidelines); FAA acquisition V&V doctrine, not a general SE process model, not a requirements manual, and not a test-design textbook; CMMI for Development v1.2 named and paraphrased, never copied; surrounding AMS lifecycle is faa-sem; phase tables are January 2023 snapshots, not live authority; reconstructed reference notes, not FAA guidance, and no FAA endorsement."
---

# FAA AMS Lifecycle Verification and Validation Guidelines, Version 4.0

**Source:** Federal Aviation Administration, *AMS Lifecycle Verification and Validation Guidelines*, Version 4.0 (January 2023). US Government work, public domain under 17 U.S.C. § 105. No download link is published; source identification and licence terms: [LICENSE](LICENSE). Vetted 2026-10-28.

## When to use

Use this skill when you have a question about verification and validation across the FAA Acquisition Management System (AMS) lifecycle: whether to verify or validate, which tier an artifact sits at, which methods apply, what the minimum V&V set is at each decision point, how the DT/OT/IOA triad divides test labor, or how shift-left changes early-lifecycle checking. It does not cover the surrounding AMS lifecycle mechanics (phases, gates as process, program office roles); that context stays in the `faa-sem` pack. It is also not a requirements-writing manual, a general SE process model, or a test-design textbook.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill

- **No arguments**: start at Core Frameworks below for the guideline's spine.
- **A topic or method question**: look it up in the Topic Index, then open the chapter.
- **A lifecycle or phase question**: use the Chapter Index; SASP is `ch03`, everything after SASP is `ch04`.
- **A term, decision rule, or move**: `glossary.md` for terms and acronyms, `cheatsheet.md` for decision rules and gate tables, `patterns.md` for shift-left and independence moves.

## Core Frameworks & Mental Models

### Verification versus validation

The spine of the whole guideline. **Verification** confirms the thing is *built right*: selected work products meet their specified requirements, incrementally from initial requirements through every change to the completed product. **Validation** confirms the *right thing* was built: the product, or an end product component, will fulfill its intended purpose and user needs in its intended environment. Both definitions are consistent with CMMI for Development v1.2 (Carnegie Mellon Software Engineering Institute, August 2006), named in the guideline's page 3 footnote; that footnote also draws the QA line: V&V targets requirements, user and mission needs, and risk, while QA targets whether established processes were followed. CMMI is third-party copyrighted; this pack paraphrases it and never quotes it. The relative weight of the two questions can shift over the lifecycle as needs, concepts, requirements, and the product itself mature.

### Three tiers: work product, product component, product

V&V attaches to a hierarchy. A **work product** represents, defines, or directs the final product (designs, specs, plans, models, prototypes, contracts). A **product component** is a lower-level element integrated upward, possibly in multiple levels. The **product** is the delivered system, service, capability, facility, or operational change. V&V flows up the tiers, repeats when an item is modified, and is performed by both government and contractor organizations on both parties' work. The Enterprise Architecture is a major V&V source criterion and is itself subject to V&V; it grounds criteria for critical work products and is updated from what V&V learns.

### Plan, perform, report, decide

V&V is a four-stage pipeline, not an end-of-line test. **Plan**: required for all acquisition programs, embedded in the program's own planning documents, each carrying the nine planning elements that apply (methods, items, criteria, measures, roles, independent reviewers, tools and labs, training). **Perform**: independent stakeholders and reviewers run tier-matched methods, checking prerequisite V&V first. Work-product methods lean on inspections, peer reviews, audits, and checklists; product and component V&V is primarily Test and Evaluation — **Development Test (DT)** verifies (developer-run, FAA-witnessed), **Operational Test (OT)** validates (OT Test Director and team with Air Traffic, Technical Operations, second-level maintenance), and the **Independent Operational Assessment (IOA)** gives decision-makers an independent operational-readiness determination for designated products. **Report**: controlled, archived records with fixed minimum content (Introduction, Purpose, Criteria, Approach, Participants, Results, Recommendations). **Decide**: results serve as entrance criteria at the gates, aiding the Joint Resources Council, the Acquisition Executive Board, and in-service decision authorities.

### Decision-point-gated V&V and shift-left

The guideline organizes V&V by AMS phase (SASP, CRD, Investment Analysis, Solution Implementation, In-Service Management) plus the non-phase RSA activity. Each phase has a table (Tables 1 through 6) fixing, per decision point, the minimum work products subject to V&V, the criteria (validation = substantive upstream content; verification = templates and policy), and the responsible stakeholders. Figure 4 shows emphasis only; the tables define the required minimum, and every table is a January 2023 policy snapshot whose own footnote points to current phase guidance. Section 1.3 renders the lifecycle as a V (left-side planning work products, right-side T&E, loopback criteria) and adds Agile acquisition plus **Shift-Left**: find defects early by V&V'ing work products as soon as possible, with testers engaged from the concepts phase onward. The five primary management documents (APB, PRD, Business Case, ISPD, PMP) are all V&V'd; Appendix B checklists cover four of them, while the Business Case runs on the Investment Planning & Analysis track closed by the Independent Evaluation Review.

---

## Chapter Index

| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-introduction-and-vv-philosophy.md) | Introduction and the V&V Philosophy | Scope, verify-vs-validate (paraphrased CMMI for Development v1.2 footnote), work-product/component/product tiers, V&V vs. QA, government and contractor obligations, EA source criterion + feedback loop, V-Model, Agile acquisition and Shift-Left |
| [ch02](chapters/ch02-implementation-guidance.md) | V&V Implementation Guidance | Nine planning elements, independence and the prerequisite check, critical technical documents, work-product vs. product method catalogs, DT/OT/IOA triad, report minimum content, decision-support practices |
| [ch03](chapters/ch03-service-analysis-and-strategic-planning.md) | V&V in the AMS Lifecycle: SASP | Five phases plus RSA, Figure 4 vs. Tables 1-6, five primary management documents, Appendix B checklists, Business Case and IER track, AMS Rational Model, SASP focus and Table 1 (CRDRD) rows |
| [ch04](chapters/ch04-lifecycle-after-sasp.md) | V&V After SASP: CRD, IA, SI, ISM | CRD and Table 2 (IARD), Initial and Final IA with Tables 3-4 (IID, FID), SI with Table 5 (Contract Award through ISD: IBR, DT/OT/IOA, PDR/CDR, SMS safety, security authorization, ISR checklist), ISM with Table 6 (NCPs, FAA Form 1800-2, Order 1800.66, implemented changes) |

## Topic Index

- **Verification (built right) vs. Validation (right thing)** → `ch01`, `ch02`
- **Three tiers: work product / product component / product** → `ch01`
- **V&V vs. QA (process conformance vs. requirements and risk)** → `ch01`
- **CMMI for Development v1.2 (SEI, August 2006; named and paraphrased)** → `ch01`
- **Enterprise Architecture (EA) as V&V source criterion and feedback loop** → `ch01`, `ch03`, `ch04`
- **V-Model implementation (left side planning, right side T&E, loopback criteria)** → `ch01`
- **Agile acquisition / Shift-Left principles in V&V** → `ch01`
- **Nine V&V planning elements** → `ch02`
- **Independent stakeholders and reviewers (independence rule)** → `ch02`
- **Critical technical documents verified before downstream use** → `ch02`
- **Method catalogs (four: work-product vs. product-tier x verify vs. validate)** → `ch02`
- **Test and Evaluation: Development Test (DT), Operational Test (OT), Independent Operational Assessment (IOA)** → `ch02`, `ch04`
- **V&V report minimum content** → `ch02`
- **V&V decision support and entrance criteria** → `ch02`
- **AMS lifecycle phases (SASP, CRD, IA, SI, ISM) and RSA** → `ch03`, `ch04`
- **Service Analysis & Strategic Planning (SASP) and the CRDRD (Table 1)** → `ch03`
- **Five primary management documents (APB, PRD, Business Case, ISPD, PMP)** → `ch03`, `ch04`
- **Appendix B checklists (PRD, APB, ISPD, PMP) and the IER track for the Business Case** → `ch03`
- **AMS Rational Model (ARM)** → `ch03`
- **Concept and Requirements Definition (CRD) and the IARD (Table 2)** → `ch04`
- **Investment Analysis: Initial (IID, Table 3) and Final (FID, Table 4)** → `ch04`
- **Integrated Baseline Review (IBR) and Solution Implementation gates (Table 5)** → `ch04`
- **Preliminary Design Review (PDR) and Critical Design Review (CDR) baselines** → `ch04`
- **Safety V&V (Safety Risk Management document, FAA SMS) and security authorization (POA&M)** → `ch04`
- **In-Service Review (ISR) checklist** → `ch03`, `ch04`
- **In-Service Management changes: NCPs, FAA Form 1800-2, Order 1800.66, ISM DT/OT (Table 6)** → `ch04`
- **Tables 1 through 6 (phase V&V specifications, January 2023 snapshots)** → `ch03`, `ch04`
- **FIPS-199 and ISGSA (front-loaded information security)** → `ch03`, `ch04`

## Supporting Files

- **`glossary.md`**: alphabetical terms and acronyms (ACAT through V&V) with chapter references; Appendix C method definitions paraphrased; CMMI-traced terms marked.
- **`cheatsheet.md`**: decision rules, the plan/perform/report/decide pipeline, phase and gate tables, nine planning elements, the four checklist documents, the T&E triad, and snapshot discipline.
- **`patterns.md`**: reusable moves with When/How/Trade-offs: split verify/validate, embed planning, gate on decision points, find-your-row, verify foundations and criteria, chain V&V forward, match method tier, structural independence, shift-left, front-load security and safety, prove the change and re-prove the purpose.

## Scope & Limits

- **Source version**: FAA AMS Lifecycle Verification and Validation Guidelines, **Version 4.0 (January 2023)**, vetted **2026-10-28** (2,700,181 bytes, 63 pages). This pack reflects Version 4.0 only.
- **Single-source**: everything here is synthesized from the January 2023 guidelines; no other FAA order, policy, or handbook is incorporated.
- **CMMI**: the verify/validate definitions are consistent with CMMI for Development v1.2 (SEI, August 2006), named on the guideline's page 3 footnote. This pack paraphrases the concepts and reproduces no verbatim CMMI text; cite SEI for CMMI wording.
- **Phase tables are January 2023 snapshots.** Tables 1 through 6 carry the guideline's own footnote: detailed phase guidelines and templates exist and should be reviewed for current guidance. Treat table content as illustrative, not live authority.
- **Surrounding AMS lifecycle**: phase mechanics, gate process, and program office roles live in the `faa-sem` pack; this pack covers V&V doctrine only.
- **Not official FAA guidance** and not affiliated with the FAA; reconstructed reference notes, and the FAA does not endorse this pack or its authors. The PDF prints no supersession sentence; none is quoted here.
- **No download link is published** for the source, per the repository's no-source-link policy; the source is identified textually by title, publisher, and version.
