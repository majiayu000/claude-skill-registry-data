---
name: dafman-63-119
description: "Knowledge base from DAFMAN 63-119 (15 April 2021), Mission-Oriented Test Readiness Certification. Use for continuous MOTRC replacing single-point OTRR thinking: framework/applicability, Certification Official vs PM roles, review cycle and exit criteria, certification memo/decertify gates, DT&E/contractor evidence, ITT integration and cyber resiliency, and the 31-template matrix. DAF T&E readiness process only—does not replace DoDI 5000.89, AFI 99-103, or multi-service lead policies."
---

<!-- argument-hint: [MOTRC, certification official, ITT, TEMP, DT sufficiency, contractor test, cyber resiliency, memo, template, or chapter number] -->

# DAFMAN 63-119 — Mission-Oriented Test Readiness Certification
**Source**: DAFMAN 63-119, 15 April 2021 (US Government work, public domain; no releasability restrictions) | **Chapters**: 7

## When to use
Use this pack when planning or running **Mission-Oriented Test Readiness Certification** for DAF (USAF/USSF) programs—standing up the continuous process that replaced OTRR-centric thinking, assigning the Certification Official, driving template-based reviews, writing the certification memorandum, treating DT/contractor/integrated-test evidence, and folding cyber resiliency and industry/supplier test obligations into OT readiness.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime. Pair with `dote-te-guidebook` / `dod-te-guidebook` for enterprise T&E context and DoDI 5000.89 framing.

## How to Use This Skill
- **Without arguments** — load the core frameworks below.
- **With a topic** — ask about MOTRC vs OTRR, Certification Official rules, review cycles, memos, DT sufficiency, contractor testing, ITT integration, cyber, or templates.
- **With a chapter** — ask for `ch01` through `ch07`.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### Continuous MOTRC (not a single OTRR)
DAF replaced OTRR-as-the-main-event with a **continuous** mission-oriented certification process from early development through dedicated OT, backed by 31 templates (Attachments 2–32) and mandatory through testing to operational acceptance.

### Certification Official independence
| Program type | Typical Certification Official | PM may self-certify? |
|--------------|--------------------------------|----------------------|
| ACAT I MDAP | SAF/AQ (MDA) or delegated PEO | No |
| ACAT II / OSD oversight | PEO (as assigned) | No |
| Others | As designated in TEMP/strategy | Follow designation; still separate judgment |

### Review cycle loop
Pre-cert reviews → candid assessment vs exit criteria → negotiate workarounds/limits → report (DT report + executive brief) → **memo** → OTO acknowledge → (optional) decertify/recertify.

### Evidence triangle
1. **DT & contractor test** sufficiency and representativeness  
2. **Integrated test** data with argued OT credit  
3. **OT plan** entrance/exit criteria and resources  

### Template matrix (three groups)
- Planning & documentation (strategy, requirements, TEMP, ITT, …)
- Design & performance (cyber, CT, DT, software, CM, deficiencies, OT plan, …)
- Assets & support (training, SE, spares, agreements, PHS&T, personnel, tech data, T&E resources)

### Integration & supplier lens
ITT co-chairs (CDT/TM + OTO) orchestrate; contractor/supplier data rights and test support are certification inputs, not optional annexes.

## Chapter Index
| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-motrc-framework-and-applicability.md) | MOTRC Framework and Applicability | Continuous process, scope, DT sufficiency & OT adequacy hooks |
| [ch02](chapters/ch02-roles-and-certification-official.md) | Roles and Certification Official | SAF/AQ, AF/TE, PEO, PM, CDT, OTO, LDTO, ITT |
| [ch03](chapters/ch03-continuous-process-and-review-cycle.md) | Continuous Process and Review Cycle | Tailoring, cyber thread, assessment, negotiation, reporting |
| [ch04](chapters/ch04-certification-memo-and-gates.md) | Certification Memo and Gates | Memo content, acknowledge, decertify/recertify |
| [ch05](chapters/ch05-dte-and-contractor-testing.md) | DT&E and Contractor Testing | Sufficiency, CT oversight, articles, evidence |
| [ch06](chapters/ch06-integration-itt-and-cyber.md) | Integration, ITT, and Cyber | ITT engine, TEMP/plans, cyber, supplier interfaces |
| [ch07](chapters/ch07-templates-documentation-and-tracking.md) | Templates, Documentation, Tracking | Matrix structure, OPRs, TEMP Part III, tool |

## Topic Index
- **ACAT / MDA / PEO certification authority** → ch02, ch04
- **AFOTEC / MAJCOM OTO / USSF OTO** → ch02
- **Agile / software pathway / DevSecOps test** → ch01, ch03, ch04
- **Certification memorandum** → ch04
- **Certification Official (vs former OT&E Certification Official)** → ch02
- **Contractor testing / supplier data** → ch05, ch06, ch07
- **Cyber resiliency / MBCRA / MRAP-C** → ch03, ch06
- **Decertification / recertification / pause** → ch04
- **Dedicated OT / FRP / deployment decision** → ch01, ch04
- **Deficiency resolution** → ch03, ch05, ch07
- **DT&E sufficiency (MS B / MS C)** → ch01, ch05
- **Exit criteria / get-well plans** → ch03, ch04
- **Integrated Test Team (ITT)** → ch02, ch06
- **Integrated testing / OT credit** → ch01, ch03, ch05
- **LDTO / CDT / Test Manager** → ch02, ch05
- **Lead operating command / requirements** → ch02
- **Multi-service lead rules** → ch01, ch06
- **OT adequacy / DOT&E** → ch01, ch05
- **OTRR replacement / continuous evaluation** → ch01
- **Production- / operational-representative articles** → ch01, ch05
- **Safety release** → ch02, ch05
- **TEMP Part III certification strategy** → ch02, ch07
- **Template matrix / Attachments 2–32** → ch03, ch07
- **Tracking tool (AF/TE)** → ch07
- **Urgent / prototype / JCTD tailoring** → ch01

## Supporting Files
- [glossary.md](glossary.md) — MOTRC and DAF T&E readiness terms
- [patterns.md](patterns.md) — implementation patterns with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — decision rules, maps, tells & smells

---

## Scope & Limits
This pack covers **DAFMAN 63-119, 15 April 2021** — Mission-Oriented Test Readiness Certification — as synthesized reference notes (103 pages per source title page / reader metadata). It does **not** cover: full text of DoDI 5000.89, AFI 99-103, AFMAN 63-144, or the detailed line-item content of every certification template attachment; service-specific classified/CUI procedures; or non-DAF lead-service certification manuals. Supersedes AFMAN 63-119, 26 April 2019. US Government public domain work; title-page releasability: no releasability restrictions. No source-material download link is published.
