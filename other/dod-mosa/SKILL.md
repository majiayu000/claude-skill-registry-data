---
name: dod-mosa
description: "Knowledge base from the OUSD(R&E) guidebook Implementing a MOSA in DoD Programs (Feb 2025). Use for the Modular Open Systems Approach as a DoD acquisition + design discipline: the statutory/regulatory basis (10 U.S.C. 4401–4403, FY2017/FY2021 NDAA, DFARS), the five OUSD(R&E) pillars, the plan→modularize→identify→define→standardize interface lifecycle, technical levers (WBS/MIL-STD-881F taxonomy, standards profiling, API-first software, COTS/cybersecurity), MOSA assessment metrics and tools (PART/OAAT/KOSS/SEAM/MAUT), technology-change and DMSMS management, roadmaps, MOSA across the six AAF pathways, and contracting/IP/data-rights mechanics. SCOPE LIMITS: this is U.S. DoD weapon-system acquisition policy, not a general open-architecture or interface-standards reference — it names standards (FACE, OMS, DISR) without reproducing them, is light on detailed engineering of any specific standard, and does not cover the underlying SE processes (use dau-se-guidebook / nasa-npr-7123) or general systems-engineering theory (use sebok)."
---

<!-- argument-hint: [MOSA pillar, interface lifecycle step, statute/DFARS, assessment tool, acquisition pathway, data rights, DMSMS, roadmap, chapter number] -->

# DoD MOSA — Implementing a Modular Open Systems Approach in DoD Programs
**Source**: OUSD(R&E), *Implementing a MOSA in DoD Programs* (Feb 2025, DOPSR 25-T-1210) — US Government work, public domain | **Chapters**: 7

## When to use
Use this skill when a U.S. defense program must adopt, plan, write into contract, assess, or sustain a Modular Open Systems Approach: framing MOSA against the statute and DFARS, working the five pillars and the interface lifecycle, making the technical decisions (WBS taxonomy, standards profiling, software/cybersecurity), levying MOSA requirements across the AAF pathways, and tying it all to data rights, assessment metrics, and roadmaps. This is the DoD *acquisition-policy* companion to the SE-process packs (`dau-se-guidebook`, `nasa-npr-7123`) and the SE canon (`sebok`).

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below: the statutory chain, the five OUSD(R&E) pillars, the interface lifecycle, and how MOSA is assessed and contracted.
- **With a topic** — ask about a pillar (e.g. "certify conformance"), an interface-lifecycle step, a statute or DFARS clause, an assessment tool (PART, OAAT, KOSS, SEAM, MAUT), an acquisition pathway, data rights, DMSMS, or roadmaps.
- **With a chapter** — `ch01` (statute/policy), `ch02` (pillars/benefits), `ch03` (program-management/interface lifecycle), `ch04` (technical considerations), `ch05` (assessment/technology change/roadmaps), `ch06` (acquisition pathways), `ch07` (implementation appendices/tools/contracting).

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

> **One discipline, two architectures.** MOSA is a *technical* architecture (modular components behind open interfaces) **and** a *business* architecture (contracting, IP, data rights). A clean interface the Government cannot legally exploit is not, in MOSA terms, a success.

## Core Frameworks & Mental Models

### What MOSA is — and why it is mandatory

A **Modular Open Systems Approach (MOSA)** is a combined acquisition and design approach that pairs a technical architecture with a business architecture, both oriented around system interfaces that conform to widely supported, consensus-based standards. The structural payoff is **severability**: components can be added, removed, or swapped incrementally across the life cycle, opening the system to efficiency, competition, and innovation. MOSA is no longer discretionary — recent law *compels* it.

### The statutory → regulatory → contract chain

Authority cascades, and a break anywhere (especially insufficient data rights) defeats the whole:
- **Statute** — **10 U.S.C. 4401–4403** (4401 = mandate + definitions for MDAPs; 4402 = capabilities development and weapon-system design; 4403 = interface availability/support). The **FY2017 NDAA** introduced *major system component* and *major system interface* and required MOSA for MDAPs at Milestone A/B after Jan 1 2019; the **FY2021 NDAA Section 804** added *modular system interface*, emphasized interface data and repositories, and expanded the mandate to all programs *to the maximum extent practicable*.
- **Regulation** — the **DFARS** (Part 207.106, 227.7203-2; clauses 252.227-7013/-7015/-7018; rulemaking case 2021-D005) and the data-rights framework of DFARS 252.227.
- **Contract** — the RFP, Acquisition Strategy, SEP, and CDD turn the mandate into a binding obligation on industry.

### The five OUSD(R&E) pillars

The current authority's organizing framework (it supersedes the 2013 OSA guidebook), read as a progression where each pillar depends on the earlier ones:
1. **Establish an Enabling Environment** — set requirements, business practices, strategy, and T&E methods before design hardens.
2. **Employ a Modular Design** — identify each component's functionality *before* the RFP, so business and technical objectives drive the partitioning.
3. **Designate Modular Interfaces** — decouple the interface from the implementation so a component and its interface can follow separate life cycles.
4. **Leverage Consensus-Based Open Standards** — standardize interfaces with open, consensus-developed standards; manage Government-owned interface repositories.
5. **Certify Conformance** — verify and validate that the implementation actually conforms to the selected open standards. Without this, the other four are claims, not facts.

### The interface lifecycle (Figure 3-1)

A maintained, living framework: **plan → modularize → identify interfaces → define interfaces → standardize interfaces**. Plan measurable objectives and governance; decompose capability into self-contained functional modules; locate the boundaries where modules exchange data, signals, or commands; turn them into explicit protocols and data formats on open standards; lock the specifications to consistent open standards. It is a pipeline, not a menu — skip *define* or *standardize* and the modules aren't actually swappable.

### Technical levers (§3.2)

- **WBS as MOSA taxonomy** (MIL-STD-881F, MIL-STD-196G naming) — align the Work Breakdown Structure to MOSA principles (modularity, openness, scalability, flexibility, reusability), then call out modules, interfaces, and test needs (Table 3-1).
- **Standards selection and profiling** — favor consensus-based standards (10 U.S.C. 4401), search ASSIST/MOSS, and write a **profile** to pin a standard's optional variability so implementations actually interoperate.
- **Software** — design **API-first** with hardware-grade modular rigor; declare data rights at the right abstraction (DoDI 5000.87); for cybersecurity, prefer a DevSecOps + MBSE + consensus-standard (FACE/OMS) path over a single proprietary transport service.
- **COTS** — run a **business case analysis** first; a design change to a COTS baseline can trigger costly regression testing or recertification, erasing the benefit.

### Assessment, technology change, and roadmaps

- **Five benefit classes** anchor metrics: Interoperability, Technology Refresh, Enhanced Competition, Innovation, Cost Avoidance/Savings — reduced to the *necessary few* per use case and maturity. Use pass/fail for a proposed architecture, metrics-based assessment (Appendix A) when supporting mechanisms exist.
- **DMSMS** (obsolescence) is mitigated by multi-vendor sourcing through open interfaces and by involving DMSMS practitioners early; coordinate with USD(A&S).
- **Two roadmaps, one clock** — a product roadmap (*what value, when*) plus a technology roadmap (*what must be ready, when*) isolate volatile technology behind stable interfaces.

### Contracting and the implementation toolkit (Appendices)

- **Assessment tools** chosen by stakeholder and level: **PART** (Army), **OAAT/OAAM** (Navy, business + technical axes 0–4), **KOSS** (NAVAIR, lock-prone subsystems), **SEAM** (Air Force). **MAUT** scores trade-offs against life-cycle cost.
- **Enforceability rides on deliverable data** — CDRLs backed by DIDs (OSMP, SEMP, DSM) traced to WBS/GRA node levels; the DSM is constrained so it cannot alter Government-designated interfaces. Front-load: evaluate a draft OSMP before award. Non-FAR vehicles (OTAs) carry no DFARS data rights automatically while the MOSA mandate still applies.
- **Desired modularity** is a deliberate cost-benefit point on a spectrum, and **Conway's Law** warns that the architecture inherits the organization's communication seams.

---

## Chapter Index

| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-dod-mosa-introduction-and-policy.md) | Introduction & Policy | MOSA definition; statutory chain (10 U.S.C. 4401–4403, FY2017/FY2021 NDAA); DFARS policy and clauses; data rights; terminology discipline |
| [ch02](chapters/ch02-dod-mosa-pillars-and-benefits.md) | Pillars & Benefits | The five OUSD(R&E) pillars; primary benefits; secondary benefits; tri-Service memorandum; supersedes 2013 OSA |
| [ch03](chapters/ch03-dod-mosa-program-management-considerations.md) | Program Management & Interface Lifecycle | Cost-benefit gate; plan→modularize→identify→define→standardize; JCIDS integration; mandatory + supporting documents; ICD/IRS |
| [ch04](chapters/ch04-dod-mosa-technical-considerations.md) | Technical Considerations | WBS/MIL-STD-881F taxonomy; requirements; standards selection and profiling; API-first software; cybersecurity; COTS |
| [ch05](chapters/ch05-dod-mosa-assessment-tech-change-roadmaps.md) | Assessment, Technology Change & Roadmaps | Five benefit classes; pass/fail vs. metrics; DMSMS; product + technology roadmaps; Appendix A methodology |
| [ch06](chapters/ch06-dod-mosa-acquisition-pathways.md) | Acquisition Pathways & Conclusion | AAF and the six pathways; MCA prescriptiveness; EMD/P&D RFPs; MOSWG/TSWG governance |
| [ch07](chapters/ch07-dod-mosa-implementation-appendices.md) | Implementation Appendices | Assessment tools (PART/OAAT/KOSS/SEAM); GRA; contracting, CDRLs/DIDs; pillar actions; MAUT; workforce/DAU CLE 019 |

## Topic Index

- **10 U.S.C. 4401–4403 / statute** → ch01, ch06
- **AAF (Adaptive Acquisition Framework)** → ch06
- **Acquisition pathways (six)** → ch06
- **Acquisition Strategy** → ch03, ch06
- **API-first / software design** → ch04
- **ASSIST / MOSS database** → ch04
- **Assessment metrics / benefit classes** → ch05
- **Assessment tools (PART, OAAT, KOSS, SEAM)** → ch07
- **Benefits of MOSA** → ch02
- **Business case analysis (COTS)** → ch04, ch07
- **Conformance certification** → ch02, ch07
- **Contracting / CDRLs / DIDs** → ch07
- **Conway's Law** → ch07
- **COTS** → ch04, ch07
- **Cost-benefit analysis** → ch03
- **Cybersecurity (software / hardware)** → ch04
- **Data rights** → ch01, ch07
- **Desired modularity** → ch07
- **DFARS** → ch01
- **DMSMS / obsolescence** → ch05
- **Government Reference Architecture (GRA)** → ch07
- **Interface lifecycle (plan/modularize/identify/define/standardize)** → ch03
- **JCIDS** → ch03
- **MAUT** → ch07
- **MIL-STD-881F / WBS taxonomy** → ch04
- **MOSWG / TSWG governance** → ch06
- **NDAA (FY2017 / FY2021 Section 804)** → ch01
- **Pillars (five OUSD(R&E))** → ch02, ch07
- **Profile (standards variability)** → ch04
- **Roadmaps (product / technology)** → ch05
- **SEP (Systems Engineering Plan)** → ch03
- **Standards (consensus-based open)** → ch04, ch02
- **Technology refresh / insertion** → ch05
- **WBS** → ch04

## Supporting Files

- [glossary.md](glossary.md) — key MOSA terms (statutory, pillar, interface, assessment, contracting), alphabetical, with chapter references
- [patterns.md](patterns.md) — reusable patterns (cost-benefit gate, interface-lifecycle pipeline, WBS taxonomy, build-in-not-bolt-on, IP-rights targeting, contractual enforceability, metrics + roadmaps) with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — quick decision rules, the five pillars, benefit classes, the statute→regulation→contract chain, MOSA across the six pathways, mandatory vs. supporting documents, tells & smells

---

## Scope & Limits

**Covers**: the Modular Open Systems Approach as U.S. DoD weapon-system acquisition and design policy per the OUSD(R&E) *Implementing a MOSA in DoD Programs* guidebook (Feb 2025) — the statutory and DFARS basis, the five pillars, the interface lifecycle, the technical levers (WBS taxonomy, standards profiling, software/cybersecurity, COTS), MOSA assessment metrics and service tools, technology-change/DMSMS management and roadmaps, MOSA across the AAF pathways, and the contracting/IP/data-rights mechanics and workforce considerations in the appendices.

**Does not cover / thin on**: the engineering of any specific interface standard — it *names* FACE, OMS, DISR, FIPS 140-2, etc. without reproducing or detailing them; the underlying systems-engineering processes that MOSA requirements ride on (use `dau-se-guidebook` / `nasa-npr-7123`) and general SE theory or open-architecture concepts beyond DoD policy (use `sebok` / `se-standards-signpost`); non-DoD or commercial open-systems practice; and the full text of the cited statutes, DFARS clauses, and 5000-series instructions (named, not reproduced). Terminology note: legacy terms such as *key interface* lack a current statutory definition and the appendices carry an older legacy five-pillar set alongside the current OUSD(R&E) pillars — anchor any non-statutory term to the statute.

**Jurisdiction & source**: U.S. Government public-domain work (Distribution A); guidance is mandatory for the DoD programs it governs and is current as of the February 2025 guidebook (DOPSR case 25-T-1210). Tracks an evolving statutory/regulatory landscape (e.g. renumbering of 10 U.S.C. 2320→3771, 2446a→4401; DFARS case 2021-D005 still finalizing) — verify citations against the current instruments.
