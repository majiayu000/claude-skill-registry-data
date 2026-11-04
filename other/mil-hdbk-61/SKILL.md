---
name: mil-hdbk-61
description: "Knowledge base from MIL-HDBK-61B, the DoD Configuration Management (CM) guidance handbook (7 April 2020, cataloged with Change 1, 2025). Use for defense CM across the acquisition and sustainment life cycle: the five CM functions (planning, identification, control/change management, status accounting, verification & audit), the three configuration baselines (FBL/ABL/PBL) and FCD→ACD→PCD documentation, configuration items (CIs/HWCI/CSCI), change instruments (ECP/NOR/RFV), the CCB and Class I/II classification, CDCA/AA authority, FCA/PCA audits, data management and data rights (CDRL/DID, DFARS rights ladder, master/authoritative source), and tailoring CM by phase (EIA-649-1 R/T/NR matrix, Appendix C templates), plus digital-era CM (digital twin, viewpoints, MOSA). NOTE: 61B is advisory guidance that adopts and points to the SAE EIA-649 / EIA-649-1 / GEIA-HB-649 suite for the authoritative CM requirements — this pack names and describes that suite but does not reproduce its copyrighted requirement text. Thin on: the EIA-649 requirement clauses themselves, form-level detail (DD-form field instructions, full DID content), and non-DoD/commercial CM frameworks."
---

<!-- argument-hint: [CM function, baseline FBL/ABL/PBL, CI, ECP/NOR/RFV, CCB, Class I/II, CDCA, FCA/PCA, data rights/CDRL, MOSA, tailoring/phase, chapter number] -->

# MIL-HDBK-61B — Configuration Management
**Source**: DoD (US Government work, public domain; Distribution A) | **Chapters**: 8

## When to use
Use this skill when you need to apply MIL-HDBK-61B guidance on DoD Configuration Management (CM) across the acquisition and sustainment lifecycle. It covers the five CM functions (planning, identification, control, status accounting, and verification and audit), the three configuration baselines (FBL, ABL, and PBL) and their documentation sets, configuration item selection and management, change instruments (ECP, NOR, and RFV), CCB authority and Class I/II classification, FCA/PCA audits, data management and DFARS data rights, and tailoring CM by phase using the EIA-649-1 framework. Use it when establishing or reviewing a CM program on a DoD acquisition, when classifying a proposed engineering change, or when planning configuration audits.

**Prerequisites:** none, plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the Core Frameworks below: the five CM functions, the three baselines, the change instruments, the audit pair, and how DM/tailoring frame them.
- **With a topic** — ask about a function (identification, control, CSA, audit), a baseline (FBL/ABL/PBL), a change instrument (ECP/NOR/RFV), an authority (CCB/CDCA/AA), an audit (FCA/PCA), data rights/CDRL, MOSA, or phase tailoring (R/T/NR).
- **With a chapter** — `ch01` (fundamentals/definitions), `ch03` (identification/baselines), `ch04` (control/change), `ch06` (verification/audit), `ch07` (data management/digital), `ch08` (tailoring/templates).

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

> **Guidance, not a requirement.** 61B is advisory — it cannot be cited as a contractual obligation. DoD has adopted the **SAE EIA-649 suite** (EIA-649 principles, EIA-649-1 contract requirements, GEIA-HB-649 implementation guide) as its CM baseline; 61B is the DoD application-and-tailoring layer on top. For *what* CM requires, go to the EIA-649 suite; for *how* DoD applies and tailors it, stay in 61B.

## Core Frameworks & Mental Models

### What CM is

Configuration Management is the **management process for keeping a product's performance, functional, and physical attributes consistent with its requirements, design, and operational information** across its whole life — so everyone works from correct, current, traceable information. The mental model: CM guarantees a **one-to-one correspondence** among the physical/digital thing, the documents that define it, and the requirements it must satisfy. It is the product's single source of truth, applied across both acquisition and sustainment.

A foundational principle: **responsibility cannot be delegated; authority can.** The Government Program Manager owns the configuration outcome no matter how the work is parceled out to configuration managers, contractors, and oversight agencies. CM is one shared process common to Government and contractor; planning decides how the functional activities are allocated, not whether each side runs a separate process.

### The five CM functions (one process, five activities)

1. **Management & Planning** — the central Government activity that plans, establishes, manages, and improves the CM program and coordinates the other four. Plan the *next* phase during the current one.
2. **Configuration Identification** — *the foundation.* Select CIs, document their performance/functional/physical attributes (and interfaces), assign identifiers, release documentation, and establish baselines. Everything else consumes its products.
3. **Configuration Control / Change Management** — the visible heart of CM: prepare, justify, evaluate, coordinate, disposition, and implement changes and variances against CIs and their baselines.
4. **Configuration Status Accounting (CSA)** — the knowledge base. Record and report the approved configuration, change status, variance status, audit results, and effectivity. CSA *accumulates as a by-product* of CM transactions — exhaust, not extra work.
5. **Configuration Verification & Audit** — prove the built item matches its documentation and performs: FCA + PCA.

### Configuration Items (CIs)

A **CI** is the unit of CM — an aggregation of hardware, software, or both, designated for CM and managed as a single entity that satisfies an end-use function. **HWCI** / **CSCI** are the hardware/software specializations (software items are almost always CIs because they typically control system functionality). Key discipline: **defining and controlling system performance does not require designating every component as a CI.** Government control reaches a lower level only when a change there would affect a Government-baselined CI specification. CI selection is an early, high-leverage, long-lived decision that sets the level of Government control for the whole life cycle.

### The three baselines (the spine)

The Government takes control of configuration documentation in three progressive stages, each with its documentation set and a strict order of precedence:

| Baseline | Captures | Doc set | Established |
|---|---|---|---|
| **FBL** (Functional) | System-level performance, interoperability, interface + verification | FCD | When FCD approved; always Government-controlled |
| **ABL** (Allocated) | CI-level performance/functional/interface allocated from above | ACD | Per CI; Government *or* contractor control |
| **PBL** (Product) | Complete functional + physical definition for production/re-procurement | PCD | Initial per CI at CDR; finalized & validated at PCA |

**Order of precedence on conflict: FCD → ACD → PCD, always.** The **developmental configuration** is the contractor's internal, evolving design before it is baselined as a PBL. Crucially, *control authority is now an independent variable from the baseline itself* — who approves changes (Government or contractor) is chosen per acquisition approach, phase, support, and interface needs. Control to the level necessary, no further.

### Change instruments and authority

- **ECP** (Engineering Change Proposal, DD 1692) — the change itself; typed **Class I** (Major — touches approved functional/allocated/product requirements, cost, warranties, or milestones → **CCB** + contract modification) or **Class II** (Minor — any other approved-doc change → local Government representative concurrence).
- **NOR** (Notice of Revision) — pins down the precise documentary edits tied to an ECP.
- **RFV** (Request for Variance, DD 1694) — bounded permission to deliver/install something off-baseline; classified minor/major/critical. **Approval of all RFVs is an inherently Governmental, non-delegable function** (FAR 7.503), requiring negotiated consideration (FAR 46.407).
- **CCB** (Configuration Control Board) — the chartered body that dispositions Class I ECPs and major/critical variances; the PM owns CCB disposition and issues a **CCBD**.
- **CDCA** (Current Document Change Authority) — exactly one per document; the sole content authority. **AAs** (Application Activities) may participate/comment but never authorize.

> Routing rule: a Government-baseline document touched, or a contractor-document change affecting contractually specified performance/supportability of a Government CI → **Government** decides; the contractor's own documents not touching a Government baseline → **contractor** decides. Recurring RFVs against the same characteristic are a warning sign — fix the requirement with a Class I ECP, don't keep granting exceptions.

### Verification & audit

**Verification is continuous; audit is a settlement.** Build configuration verification (functional + physical) into the contractor's own process — a process the Government can *validate* may substitute for independent physical inspection. Then audit as the program-level accounting:
- **FCA** (Functional Configuration Audit) — "does it perform?" Verifies actual performance against the performance specification.
- **PCA** (Physical Configuration Audit) — "does the documentation match what we deliver and support?" Verifies design documentation vs. delivered design, validates production processes, and **locks down the PBL.**

Run audits in three phases (pre-audit → audit → post-audit); not done until every action item closes. Expect audits in EMD and early production, not MSA/TMRR.

### Data management and data rights

**DM is the supply chain; CM is the warehouse.** CM controls the configuration-defining subset of data; **Data Management** governs the full life cycle of *all* product-related data — what to acquire, the rights to use it, and how to store and share it. Three separate gates: **order** data via CDRL/DID tied to a SOW task; secure the **rights** (FFF and OMIT data unlimited automatically; otherwise funding source sets unlimited / Government purpose / limited-restricted); and **hold** the official master in a Government PDM-type system. Never substitute access for delivery. Designate one authoritative **master** and keep derived/transformed copies in sync. In the **digital era** the CM principle is constant while the artifacts widen — models, viewpoints, datasets, digital artifacts, reuse libraries, digital twins (as-built + as-maintained), and **MOSA** modules whose interfaces must be held under strict configuration control.

### Tailoring CM by phase

CM is a menu to **select from and scale**, not a fixed bundle. **Tailoring is subtraction from a vetted maximum, not addition from zero:** start from EIA-649-1's full "shall" catalog and remove what the phase does not need, using the Figure B-1 **R/T/NR** matrix (Recommended / Tailorable / Not Recommended, read per phase) and the Annex A Tailoring Worksheet (usable directly in contracts). Requirements drive cost. CM intensity is a curve: process stand-up in TMRR → baselines first established and CCB online in EMD → baseline maintenance in Production → maintenance-driven recording in O&S. There is **no MSA template** (CM not applicable pre-Milestone A); audits are central in EMD/Production but absent in TMRR and O&S.

---

## Chapter Index

| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-mil-hdbk-61-scope-fundamentals-definitions.md) | Scope, Fundamentals & Definitions | What 61B is (advisory guidance adopting EIA-649); CM definition; configuration & baselines; CI/HWCI/CSCI; the five functions; Class I/II; ECP/CCB/CCBD/NOR/RFV; CDCA; nonconformance/repair/rework/retrofit; form-fit-function/interface/ICWG; digital-era terms |
| [ch02](chapters/ch02-mil-hdbk-61-lifecycle-management-planning.md) | Life-Cycle Management & Planning | CM as non-delegable Government responsibility; one shared process; CM process implementation view; top-level activity model; FBL→ABL→PBL progression; CM in SE and logistics; metrics from CSA; planning the next phase; RFP/Section L as CM levers |
| [ch03](chapters/ch03-mil-hdbk-61-configuration-identification.md) | Configuration Identification | The foundational activity; seven recurring tasks; CI selection; configuration documentation; the three baselines + developmental configuration; FCD→ACD→PCD precedence; identifiers (CAGE, serial/lot/part numbers); engineering release; interface management |
| [ch04](chapters/ch04-mil-hdbk-61-configuration-control-change-management.md) | Configuration Control & Change Management | Span of control; why changes arise; who approves what; ECP Class I/II; RFV mechanics, approval, and consideration (FAR 7.503/46.407); NOR; CDCA and AA; control formality scaling with phase; pre-ECP communication |
| [ch05](chapters/ch05-mil-hdbk-61-configuration-status-accounting.md) | Configuration Status Accounting (CSA) | CSA as the configuration knowledge base; inputs/outputs model; activity model; the core records and reports; as-designed/built/delivered/modified views; Government vs. contractor data split; warranty data; phase inheritance; commercial CM/PDM tools |
| [ch06](chapters/ch06-mil-hdbk-61-configuration-verification-audit.md) | Configuration Verification & Audit | Verification (functional + physical) vs. audit; change verification and implementation; the three audit phases; FCA (performance) and PCA (design/documentation); audit timing by phase; certifications decoupled in performance-based buys; ISO 9000/10007 alignment |
| [ch07](chapters/ch07-mil-hdbk-61-data-management-emerging-technologies.md) | Data Management & Emerging Technologies | DM vs. CM; the three DM cost drivers; CDRL/DID; data-rights ladder (DFARS); access ≠ delivery; master/authoritative source; data as a corporate asset; model-based paradigm; digital artifacts, viewpoints, digital twins; reuse libraries; MOSA CM/DM |
| [ch08](chapters/ch08-mil-hdbk-61-tailoring-cm-templates-by-phase.md) | Tailoring & CM Templates by Phase | EIA-649-1 R/T/NR applicability matrix (Figure B-1); Annex A Tailoring Worksheet; CM lifecycle requirements flow; Appendix C phase templates (TMRR/EMD/P&D/O&S); requirements drive cost; tailoring factors; benefits-vs-risks framing; no MSA template |

## Topic Index

- **Allocated Baseline (ABL) / ACD** → ch03, ch02
- **Application Activity (AA)** → ch04
- **As-built / as-delivered / as-maintained / as-designed** → ch05, ch07
- **Audit (configuration), three phases** → ch06
- **Baselines (FBL / ABL / PBL)** → ch03, ch02, cheatsheet
- **CAGE code / document identity** → ch03
- **Change classification (Class I / Class II)** → ch04, ch01
- **Configuration Control Board (CCB) / CCBD** → ch04, ch01
- **Configuration Item (CI / HWCI / CSCI)** → ch03, ch01
- **Configuration identification** → ch03
- **Configuration Status Accounting (CSA)** → ch05, ch02
- **Current Document Change Authority (CDCA)** → ch04, ch01
- **Data Management (DM)** → ch07
- **Data rights (unlimited / Government purpose / limited / FFF / OMIT)** → ch07, cheatsheet
- **CDRL / DID** → ch07
- **Developmental configuration** → ch03
- **Digital twin / digital artifact / digital engineering** → ch07, ch01
- **Engineering Change Proposal (ECP)** → ch04, ch01
- **Engineering release** → ch03
- **Form, fit, function / interface** → ch01, ch03
- **Functional Baseline (FBL) / FCD** → ch03, ch02
- **Functional Configuration Audit (FCA)** → ch06, ch01
- **Interface Control Working Group (ICWG)** → ch03, ch01
- **Master / authoritative source** → ch07
- **Metrics (CM, from CSA)** → ch02
- **MOSA (Modular Open Systems Approach)** → ch07, ch01
- **Notice of Revision (NOR)** → ch04, ch01
- **Order of precedence (FCD → ACD → PCD)** → ch03
- **PDM (Product Data Management) systems** → ch07
- **Physical Configuration Audit (PCA)** → ch06, ch01
- **Product Baseline (PBL) / PCD** → ch03, ch02
- **Repair / rework / retrofit / nonconformance** → ch01, ch06
- **Request for Variance (RFV)** → ch04, ch01
- **Responsibility (non-delegable) vs. authority** → ch02
- **SAE EIA-649 / EIA-649-1 / GEIA-HB-649 (the suite)** → ch01, ch02, ch03, ch08
- **Serial / lot / part numbers** → ch03
- **Tailoring (R / T / NR, Annex A worksheet)** → ch08
- **Verification (configuration)** → ch06
- **Viewpoint (model-based)** → ch07

## Supporting Files

- [glossary.md](glossary.md) — key CM terms, alphabetical, with chapter references
- [patterns.md](patterns.md) — 12 reusable CM techniques (adopt-and-tailor, progressive baselining, route-by-ownership, pick-the-right-instrument, CSA-as-exhaust, build-in verification, the three data gates, master/authoritative source, digital-era CM, MOSA interfaces, phase tailoring) with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — the five functions, three baselines, change instruments, FCA/PCA, CM-intensity-by-phase, tailoring flow, data-rights ladder, and tells & smells

---

## Scope & Limits

**Covers**: configuration management for DoD systems per MIL-HDBK-61B across acquisition and sustainment — the five CM functions; the three baselines (FBL/ABL/PBL) and FCD→ACD→PCD documentation; CI selection and identifiers; change instruments (ECP/NOR/RFV), the CCB, Class I/II classification, and CDCA/AA authority; configuration status accounting; verification and the FCA/PCA audits; data management and data rights (CDRL/DID, DFARS rights ladder, master/authoritative source); digital-era CM (model-based, digital artifacts, viewpoints, digital twins, MOSA); and tailoring CM by life-cycle phase (the EIA-649-1 R/T/NR matrix and Appendix C phase templates).

**Does not cover in depth**: the authoritative CM *requirements* themselves — those live in the **SAE EIA-649 / EIA-649-1 / GEIA-HB-649** suite that 61B adopts and points to; this pack names and describes the suite and 61B's tailoring of it but does not reproduce its copyright-protected requirement clauses. Also thin on: form-level instruction detail (DD Form 1692/1694/1423 field instructions, full DID content — deferred to ASSIST and the instruction sheets); the contractual/regulatory text behind references (DFARS Parts 27/52/227, FAR 7.503/46.407, DoD 5010.12-M, DoDI 5000.02); and non-DoD or commercial CM frameworks (for the broader SE-standards landscape see `se-standards-signpost`; for adjacent DoD SE process see `dau-se-guidebook`; for civil-space CM see `nasa-npr-7123` / `nasa-se-handbook`).

**Source version**: MIL-HDBK-61B (61B, 7 April 2020), cataloged with Change 1 (15 Aug 2025). This is the current revision — *not* the superseded 2001 MIL-HDBK-61A(SE), whose process model and standards references are out of date. The digital-engineering, digital-twin, and MOSA material exists only in the B revision.

**Jurisdiction**: US Government work, public domain (not subject to copyright in the US); Distribution A (approved for public release, distribution unlimited). The handbook is advisory guidance, not a citable contractual requirement.
