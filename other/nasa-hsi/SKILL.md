---
name: nasa-hsi
description: "Knowledge base from NASA Human Systems Integration (HSI) Practitioner's Guide (NASA/SP-2015-3709). Use for HSI process implementation, lifecycle phase activities, function allocation, ConOps development, HSI Plan writing, HSI metrics (MOE/MOP/TPM/KPP), HITL testing strategy, HSI team organisation, scaling/tailoring for program size, and V&V planning. Does not cover the specific human engineering design standards (NASA-STD-3001 content) or detailed HFE methods beyond what the guide itself provides."
---

<!-- argument-hint: [topic, phase, or chapter number] -->

# NASA Human Systems Integration (HSI) Practitioner's Guide (NASA/SP-2015-3709)
**Source**: NASA (US Government work, public domain) | **Chapters**: 9

## When to use
Use this skill when planning, scoping, or executing HSI within a NASA systems engineering lifecycle — from first concept studies through decommissioning. It answers "when do I do what", "what products are due at which milestone", and "how do I scale HSI to my program size." It is the practitioner's process companion, not a human factors design reference; for specific ergonomic or human performance standards, consult NASA-STD-3001 and the HIDH directly.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below and the HSI lifecycle overview.
- **With a topic** — ask about ConOps, function allocation, HSI Plan, HITL testing, crew time KPP, COTS screening, V&V pre-declaration, lessons learned; I read the relevant chapter.
- **With a phase** — ask about "Pre-Phase A", "Phase B", "Phase D", "Phase E"; I provide the HSI activities and milestone deliverables for that phase.
- **With a chapter** — ask for `ch01` through `ch09`.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### 1. Four HSI Key Concepts (Ch 1)
1. **System = hardware + software + human** — all three sub-systems have equal standing.
2. **All personnel, all lifecycle** — users, operators, maintainers, trainers, logistics, ground control.
3. **Integration and collaboration** — HSI resolves cross-domain conflicts before program management must engage.
4. **Early is mandatory** — LCC is locked in during early phases; Pre-Phase A HSI yields the greatest cost savings.

### 2. NASA HSI Domains (Ch 1)
| Domain | Core Focus |
|---|---|
| Human Factors Engineering (HFE) | Capabilities/limitations → hardware/software design |
| Operations Resources | Flight and ground crew operations planning |
| Maintainability and Supportability | Maintenance design, logistics, spares |
| Habitability and Environment | Living/working conditions, health, environment |
| Safety | Hazard controls, human rating, survivability |
| Training | Instructional design, training resource minimisation |

### 3. HSI in the Systems Engineering Engine (Ch 3)
HSI runs in lock-step with the 17 NASA SEE processes (NPR 7123.1B). Key mapping:
- **SEE 1–4 (Design)**: ConOps, function allocation, requirements, HITL-informed design
- **SEE 5–9 (Realization)**: Prototyping, integration, HITL V&V, operations transition
- **SEE 10–17 (Management)**: HSI plan, risk management, metrics, milestone reviews

### 4. Lifecycle Phase HSI Activities Summary
| Phase | Gate | Primary HSI Actions |
|---|---|---|
| Pre-Phase A | MCR | ConOps draft; function allocation; MOEs; HSI planning initiated |
| Phase A | SRR/SDR | ConOps baseline; HSI team formed; requirements baseline; MOPs/TPMs |
| Phase B | PDR | HITL intensified; requirements refined; V&V framework established |
| Phase C | CDR/PRR/SIR | Design finalised; production/training plans; V&V activities maturing |
| Phase D | TRR/SAR/ORR/FRR | V&V closure; Human Rating Certification Package; operational products |
| Phase E | PLAR/CERR/PFAR/DR | In-mission monitoring; lessons learned; sustaining engineering |
| Phase F | DRR | Decommissioning support; final knowledge archiving |

### 5. HSI Metrics Cascade
**MOE** (stakeholder satisfaction criterion, Pre-Phase A)
→ **MOP** (engineering-level measure, Phase A)
→ **TPM** (tracked margin, Phase A through Phase E)
→ **KPP** (program-level threshold/objective, e.g. crew time ≤40%/≤35%)

### 6. HSI Scaling (Ch 7)
| Scale | Safety | Human Involvement | Plan Format |
|---|---|---|---|
| Large | Category I / human-rated / life-sustaining | Tight coupling; crew "lives in the product" | Standalone HSI Plan |
| Medium | Category II / modest risk | Moderate coupling; crew essential | HSI in SEMP |
| Small | Category III / low risk | Loose coupling; some automation | Project documents |

**Rule**: Scale by safety and human involvement, NOT by budget.

### 7. HSI Plan Structure (Ch 8, Ch 9)
1. Introduction (Purpose, Scope, Definitions)
2. Applicable Documents
3. HSI Objectives (System Description + HSI Relevance)
4. HSI Strategy (Summary + Domains)
5. HSI Requirements, Organisation, and Risk Management
6. HSI Implementation (Activities, Products, Update Schedule)

### 8. Three Technical Authorities (Ch 2)
- **ETA** (OCE) → NPR 7123.1B; engineering design oversight
- **SMA TA** (OSMA) → NPR 8705.2B; safety and human-rating mandate
- **HMTA** (OCHMO) → NASA-STD-3001; health and medical standards

---

## Chapter Index
| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-introduction-to-hsi.md) | Introduction to HSI | Four key concepts, HSI domains, HFE/HCD/HSI distinctions, LCC motivation |
| [ch02](chapters/ch02-implementing-hsi.md) | Implementing HSI | Three TAs (ETA/SMA/HMTA), control boards, IPT collaboration, HSI tools |
| [ch03](chapters/ch03-hsi-in-the-see-engine.md) | HSI in the SEE Engine | 17 SEE processes, Product Maturity Matrix, ConOps, function allocation, MOE→MOP→TPM |
| [ch04](chapters/ch04-pre-phase-a-and-phase-a.md) | Pre-Phase A and Phase A | MCR/SRR/SDR deliverables, HITL mockups, function allocation, HSI team formation |
| [ch05](chapters/ch05-phases-b-and-c.md) | Phases B and C | PDR/CDR activities, HITL intensification, V&V pre-declaration, design finalisation |
| [ch06](chapters/ch06-phases-d-e-f.md) | Phases D, E, and F | V&V closure, Human Rating Certification Package, operational monitoring, lessons learned |
| [ch07](chapters/ch07-hsi-products-scaling-tailoring.md) | Products, Scaling, Tailoring | Three-tier scaling, COTS assessment, crew time KPP, Agile integration |
| [ch08](chapters/ch08-hsi-plan-writing-and-execution.md) | HSI Plan Writing and Execution | HSI Plan structure, ConOps development, SME integration, requirements derivation, metrics |
| [ch09](chapters/ch09-appendices-hsi-plan-checklist-cases.md) | Appendices: Plan, Checklist, Cases | Appendix A annotated outline, Appendix B checklist, Appendix C case studies (F-22, Shuttle, ISS, Constellation) |

## Topic Index
- **ConOps development** → ch03, ch04, ch08
- **COTS screening** → ch07
- **Crew time KPP** → ch07, ch08
- **Function allocation** → ch03, ch04, ch08
- **HITL testing** → ch03, ch04, ch05, ch06
- **HSI Plan writing** → ch08, ch09
- **HSI scaling and tailoring** → ch07
- **HSI team formation** → ch02, ch04
- **Lifecycle milestone deliverables** → ch03, ch04, ch05, ch06
- **LCC and cost avoidance** → ch01, ch07, ch08
- **Metrics (MOE/MOP/TPM/KPP)** → ch03, ch08
- **Phase D V&V closure** → ch06
- **Pre-declaration** → ch05, ch06
- **Requirements development** → ch08
- **SME integration** → ch02, ch08
- **Technical authorities** → ch02
- **Training domain** → ch01, ch08

## Supporting Files
- [glossary.md](glossary.md) — ~50 terms with chapter references, from CDR to V&V
- [patterns.md](patterns.md) — 13 reusable when/how/trade-off patterns for HSI practice
- [cheatsheet.md](cheatsheet.md) — decision rules, milestone map, tells-and-smells, four key concepts

---

## Scope & Limits
This skill covers the NASA HSI process and management framework as documented in NASA/SP-2015-3709: HSI lifecycle phases, SEE integration, product maturity, scaling, HSI Plan structure, metrics, V&V strategy, and program case studies. It does not cover the detailed engineering design standards in NASA-STD-3001 (human factors design requirements for space systems), the HIDH human performance data, or specific HFE analysis methodologies beyond what the Practitioner's Guide itself describes. This is a US Government public domain work (NASA); no copyright restriction applies.
