---
name: nasa-npr-7123
description: "Knowledge base from NASA NPR 7123.1D — Systems Engineering Processes and Requirements. Use for the 17 common SE processes (SE Engine), life-cycle reviews and entrance/success criteria, SEMP structure and content, ETA roles and tailoring/customizing rules, Technology Readiness Levels (TRL 1–9), SE work product maturity terminology, contracted project oversight, and MOE/MOP/TPM measurement frameworks. Does not cover NASA programme financial management, human spaceflight medical standards, or software engineering requirements in depth (see NPR 7150.2 for the latter)."
---

<!-- argument-hint: [SE process name, review type, TRL level, SEMP, ETA, tailoring, MOE/MOP/TPM, chapter number] -->

# NASA NPR 7123.1D — Systems Engineering Processes and Requirements
**Source**: NASA (US Government work, public domain) | **Chapters**: 9

## When to use
Use this skill when you need to apply, explain, or assess NASA's mandatory systems engineering process framework: the 17 common technical processes (SE Engine), life-cycle and technical review requirements, SEMP planning obligations, TRL assessments, tailoring vs. customizing decisions, or contracted project SE governance. This is the normative SE process standard for all NASA programs and projects; it pairs with NASA/SP-6105 (the non-mandatory SE Handbook) for implementation guidance.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below for an overview of the SE Engine, SEMP, and review system.
- **With a topic** — ask about specific processes (e.g., "logical decomposition", "product validation"), review types (e.g., "PDR entrance criteria"), TRL levels, tailoring rules, or MOE/MOP/TPM distinctions.
- **With a chapter** — ask for `ch03` (17 processes), `ch05` (reviews), `ch06` (SEMP), `ch08` (TRLs), `ch09` (review criteria).

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### The SE Engine — 17 Common Technical Processes

The SE Engine is the NASA model for systems engineering. It applies recursively to every product layer in the system structure throughout all life-cycle phases. Three process groups work together:

**System Design Processes (top-down, SE-07 to SE-10)**
1. **Stakeholder Expectations Definition** — elicit ConOps, use cases, MOEs; validate expectations.
2. **Technical Requirements Definition** — transform expectations into unique, quantitative, verifiable "shall" statements; define MOPs and TPMs.
3. **Logical Decomposition** — decompose requirements by function/behaviour/time; produce functional models and derived requirements for lower levels.
4. **Design Solution Definition** — translate logical models into preferred design alternatives satisfying derived requirements; produce end-product specifications.

**Product Realization Processes (bottom-up, SE-11 to SE-15)**
5. **Product Implementation** — make, buy, or reuse the lowest-level end product.
6. **Product Integration** — assemble verified lower-level products into the next higher-level product.
7. **Product Verification** — prove conformance to specifications ("built it right?").
8. **Product Validation** — prove the product satisfies stakeholder expectations in its intended environment ("right thing built?").
9. **Product Transition** — deliver the verified/validated end product to the next customer in the system structure.

**Technical Management Processes (cross-cutting, SE-16 to SE-23)**
10. **Technical Planning** — plan the technical effort; outputs the SEMP.
11. **Requirements Management** — maintain bidirectional traceability; manage requirement changes over the life cycle.
12. **Interface Management** — establish and control interface definitions across teams, contractors, and geographies.
13. **Technical Risk Management** — make risk-informed decisions; manage risk across health/medical, safety, technical, cost, and schedule dimensions.
14. **Configuration Management** — control configuration items; maintain integrity, traceability, and security throughout the life cycle.
15. **Technical Data Management** — capture and manage trade studies, analyses, reports, and technical data across the life cycle.
16. **Technical Assessment** — monitor technical progress; feed life-cycle reviews.
17. **Decision Analysis** — apply formal criteria, alternatives analysis, and selection to significant technical decisions.

### SEMP — The Living Technical Plan

The Systems Engineering Management Plan (SEMP) is the master technical planning document. Key rules:
- Established early in Formulation; updated through SIR; reapproved by ETA and program manager at each major review.
- Must describe how all 17 processes are recursively applied across every product layer and life-cycle phase.
- All technical discipline plans (integration, V&V, HSI) must be consistent with the SEMP.
- ETA must approve the SEMP (SE-06) — this is a binding "shall" requirement.
- For small projects, SEMP content may be incorporated into the Project Plan with ETA approval.

### Tailoring vs. Customizing

| | Tailoring | Customizing |
|---|---|---|
| **What it adjusts** | What must be done (NPR requirements) | How requirements are implemented |
| **Relief mechanism** | Waiver (post-config-control) or Deviation (pre-config-control) | None needed |
| **ETA approval** | Required | Not required (but document in SEMP) |
| **Compliance matrix** | Entry required | Entry recommended |

### Measurement Cascade: MOE → MOP → TPM → Leading Indicator

- **MOE** (Measure of Effectiveness): Qualitative stakeholder-facing validation criterion; defined in Stakeholder Expectations Definition. Drives validation.
- **MOP** (Measure of Performance): Quantitative design target; two or more per MOE; defined in Technical Requirements Definition. Drives design.
- **TPM** (Technical Performance Measure): Monitored subset of MOPs tracked against plan throughout the life cycle. Drives progress tracking.
- **Leading Indicators**: Forward-looking subset of TPMs (mass margins, power margins are mandated). Drives early corrective action.

### Life-Cycle Review System

Reviews are event-based (triggered by technical maturity, not calendar). Each review requires:
1. Entrance criteria satisfied before convening.
2. Mandatory SE work products at specified maturity levels (Initial → Preliminary → Baseline → Update).
3. Review complete only when: all RIDs/RFAs dispositioned with TA concurrence, board report distributed, decision memo signed by Decision Authority.

Key mandatory products timeline:
- **MCR**: Baselined stakeholder expectations, concept definition, approved MOEs
- **SRR**: Baselined SEMP, baselined requirements, baselined HSI approach
- **PDR**: Preliminary design solution, baselined integration plans, baselined V&V Plan *(new in 7123.1D)*
- **CDR**: Baseline detailed design
- **FRR**: Baseline V&V results, final certification for flight/use

### TRL Scale Summary

| TRL | Environment | Fidelity |
|---|---|---|
| 1–3 | Laboratory | Principles, concept, proof-of-concept |
| 4–5 | Lab → Relevant | Breadboard (4), Brassboard (5) |
| 6 | Relevant environment | Full-scale prototype |
| 7 | Operational environment | Engineering unit or prototype |
| 8 | Operational environment | Final configuration, flight-qualified |
| 9 | Actual mission | Flight-proven |

TRL must be assessed in Formulation and updated at every status review. Other maturity scales must map back to TRL.

### ETA (Engineering Technical Authority)

- Independently funded from programme budgets — the structural check-and-balance.
- Approves: SEMP, waivers, deviations, key technical documents.
- Cannot approve relief from non-technical Programmatic Authority requirements.
- Raises formal dissenting opinions through the dissent process (NPR 7120.5).

---

## Chapter Index

| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-introduction.md) | Introduction | SE Framework (3 elements), 4 pillars of technical excellence, OCE, NPR applicability |
| [ch02](chapters/ch02-institutional-programmatic-requirements.md) | Institutional & Programmatic Requirements | ETA framework, tailoring vs. customizing, compliance matrix, roles (OCE, Center Directors, Technical Teams), HSI co-ownership |
| [ch03](chapters/ch03-common-technical-processes.md) | Common Technical Processes | All 17 SE processes (SE-07 to SE-23), SE Engine, product layer model, MOE/MOP/TPM definitions, bidirectional traceability |
| [ch04](chapters/ch04-contracted-projects.md) | SE on Contracted Projects | Insight vs. oversight, pre-award activities, surveillance plans, SOW/DRL, contracting officer authority, contract completion |
| [ch05](chapters/ch05-lifecycle-technical-reviews.md) | Life-Cycle & Technical Reviews | Event-based reviews, mandatory work products by review (SE-32 to SE-69), TRL tracking, HSI approach, review completion protocol |
| [ch06](chapters/ch06-systems-engineering-management-plan.md) | Systems Engineering Management Plan | SEMP function and content, ETA approval (SE-06), recursive application (SE-58), TPM requirements, leading indicators (SE-62/63), SEMP for contracted work |
| [ch07](chapters/ch07-definitions.md) | Definitions (Appendix A) | All key NPR terms: verification/validation distinction, deviation/waiver, MOE/MOP/TPM, TRL, SE Engine, tailoring, enabling products, recursive/iterative/repeatable |
| [ch08](chapters/ch08-technology-readiness-levels.md) | Technology Readiness Levels (Appendix E) | TRL 1–9 hardware and software descriptions, success criteria, breadboard/brassboard/engineering unit, relevant vs. operational environment |
| [ch09](chapters/ch09-review-entrance-success-criteria.md) | Review Entrance & Success Criteria (Appendix G) | Three-dimension review assessment framework, program vs. project tables, starred product notation, spectrum/cybersecurity review requirements, TBD/TBR tracking |

## Topic Index

- **17 processes / SE Engine** → ch03
- **Bidirectional traceability** → ch03
- **Compliance matrix (Appendix H)** → ch02, cheatsheet
- **Contracted projects / oversight / insight** → ch04
- **Customizing** → ch02, ch07, patterns
- **Decision Analysis** → ch03
- **Definitions / glossary** → ch07, glossary
- **Deviation vs. waiver** → ch02, ch07, cheatsheet
- **ETA (Engineering Technical Authority)** → ch01, ch02, ch06, ch07
- **HSI (Human Systems Integration)** → ch02, ch05, ch07
- **Interface Management** → ch03
- **Leading indicators / mass and power margins** → ch06, cheatsheet
- **Life-cycle reviews (MCR, SRR, PDR, CDR, FRR, etc.)** → ch05, ch09
- **MOE / MOP / TPM** → ch03, ch07, cheatsheet
- **Product validation** → ch03, ch07
- **Product verification** → ch03, ch07
- **Recursive application** → ch03, ch06, ch07
- **Requirements Management** → ch03
- **Review entrance/success criteria** → ch09
- **Risk Management** → ch03
- **SE Engine** → ch01, ch03
- **SEMP** → ch06, ch02
- **Stakeholder Expectations Definition** → ch03
- **Tailoring** → ch02, ch07, patterns
- **TRL (Technology Readiness Levels)** → ch05, ch08, cheatsheet
- **Work product maturity (Initial/Preliminary/Baseline/Update/Final)** → ch05, ch07, cheatsheet

## Supporting Files

- [glossary.md](glossary.md) — ~55 authoritative NASA definitions from Appendix A, alphabetical, with chapter references
- [patterns.md](patterns.md) — 14 reusable SE patterns with When/How/Trade-offs structure (recursive application, TRL gating, review closure, SEMP maintenance, etc.)
- [cheatsheet.md](cheatsheet.md) — Decision rules, 17-process table, mandatory review products, TRL reference, work product maturity terms, tells and smells, key SE requirement numbers

---

## Scope & Limits

**Covers**: All mandatory SE process requirements for NASA programs and projects per NPR 7123.1D revision D; the 17 common technical processes and their "shall" requirements (SE-07 to SE-69); life-cycle review system; SEMP obligations; ETA roles and governance; TRL scale; tailoring/customizing rules; contracted project SE activities; Appendix A definitions; Appendix E TRL descriptions; Appendix F work product maturity terminology; Appendix G review entrance/success criteria overview.

**Does not cover in depth**: NASA programme financial management and budget processes; human spaceflight medical certification standards; software engineering process requirements (see NPR 7150.2); facility project SE requirements (see NPR 8820.2); specific Center-level SE process implementations; Appendix H compliance matrix tables (cross-references to all SE requirements — use the cheatsheet SE requirement number table instead); Appendix I standards list; Appendix J deleted requirements.

**Jurisdiction**: US Government public domain work. NPR 7123.1D applies to all NASA programs and projects. Non-NASA organisations may adopt the framework voluntarily; compliance is not legally required outside a NASA contract.
