---
name: nasa-se-handbook
description: "Knowledge base from the NASA Systems Engineering Handbook (NASA/SP-2016-6105 Rev 2). Use for NASA's systems-engineering process model — the SE Engine and 17 common technical processes, the program/project life cycle (Pre-Phase A through F), Key Decision Points and technical reviews (MCR/SRR/PDR/CDR/…), stakeholder expectations, technical requirements, design solution, product verification and validation, and crosscutting technical management (planning, risk, configuration, interfaces, data, assessment, decision analysis). Strong for aerospace/spaceflight project SE and lifecycle gating; NASA-specific terminology (KDPs, NPR 7123.1)."
---

<!-- argument-hint: [topic, process name, or chapter number] -->

# NASA Systems Engineering Handbook
**Source**: NASA (US Government work, public domain) | **Document**: NASA/SP-2016-6105 Rev 2 | **Pages**: ~383 | **Chapters**: 34

## When to use

Use this pack when you need NASA's systems-engineering process model: the **SE Engine** and the **17 common technical processes**, the **program/project life cycle** (Pre-Phase A → F), **Key Decision Points** and **technical reviews** (MCR, SRR, SDR, PDR, CDR, SAR, ORR, FRR), stakeholder expectations → technical requirements → logical decomposition → design solution, product verification vs validation, and crosscutting technical management (planning, risk, configuration, interfaces, data, assessment, decision analysis). Strong for aerospace/spaceflight project SE and lifecycle gating. Less suited to general MBSE notation or AI integration.

**Prerequisites:** none — this pack is plain Markdown; no MCP server, API key, or licence tier is needed at runtime.

## How to Use This Skill

- **Without arguments** — load the core process model below for reference.
- **With a topic** — ask about `verification vs validation`, `PDR`, `trade studies`, `configuration management`, or another indexed topic; I read the relevant chapter.
- **With a chapter** — ask for `ch20` to load Design Solution Definition.
- **Browse** — ask "what chapters do you have?" for the full index.

Supporting files: `glossary.md` (108 terms), `patterns.md` (21 techniques), `cheatsheet.md` (decision rules, phase/KDP/review gates, cost thresholds).

## Core Frameworks & Mental Models

**The SE Engine (Ch 1–3).** NASA's central model: the 17 common technical processes arranged as three families — **system design** (4 processes: stakeholder expectations, technical requirements, logical decomposition, design solution), **product realization** (5: implementation, integration, verification, validation, transition), and **technical management** (8: planning, requirements management, interface management, risk, configuration, data, assessment, decision analysis). The engine is applied **recursively** down the product hierarchy and **iteratively** within each life-cycle phase.

**Program/project life cycle (Ch 7–16).** Phases **Pre-Phase A** (concept studies) → **A** (concept & technology development) → **B** (preliminary design) → **C** (final design & fabrication) → **D** (assembly, integration, test, launch) → **E** (operations) → **F** (closeout). Phase transitions are gated at **Key Decision Points (KDPs)** and supported by **technical reviews** (MCR, SRR, SDR/MDR, PDR, CDR, SIR, TRR, SAR, ORR, FRR).

**System design flow (Ch 17–20).** **Stakeholder Expectations** (captured as Needs-Goals-Objectives, ConOps, and Measures of Effectiveness) → **Technical Requirements** (validated, verifiable, with MOPs/TPMs) → **Logical Decomposition** (functional architecture, Product Breakdown Structure) → **Design Solution** (trade studies + decision analysis selecting the baseline).

**Product realization (Ch 21–25).** Implementation (make/buy/reuse) → Integration → **Verification** ("built it right" — test, analysis, inspection, demonstration) → **Validation** ("built the right thing" — against stakeholder expectations) → Transition. Verification and validation are distinct and both required.

**Crosscutting technical management (Ch 26–34).** Technical Planning (WBS, SEMP), Requirements Management (traceability, change control), Interface Management, **Technical Risk Management** (continuous, risk-informed decision making), Configuration Management, Technical Data Management, **Technical Assessment** (TPMs, EVM, reviews), and **Decision Analysis** (structured trade studies).

## Chapter Index

| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-2-0-fundamentals-of-systems-engineering.md) | 2.0 Fundamentals of SE | The SE Engine; design processes |
| [ch02](chapters/ch02-2-1-the-common-technical-processes-and-the-se.md) | 2.1 Common Technical Processes & SE Engine | The 17 processes; process families |
| [ch03](chapters/ch03-2-3-example-of-using-the-se-engine.md) | 2.3 Example of Using the SE Engine | SE Engine; Product Breakdown Structure |
| [ch04](chapters/ch04-2-5-cost-effectiveness-considerations.md) | 2.5 Cost-Effectiveness Considerations | Design trade studies; cost-effectiveness |
| [ch05](chapters/ch05-2-6-human-systems-integration-hsi-in-the-se-process.md) | 2.6 Human Systems Integration (HSI) | HSI Plan |
| [ch06](chapters/ch06-2-7-competency-model-for-systems-engineers.md) | 2.7 SE Competency Model | NASA SE Competency Model |
| [ch07](chapters/ch07-3-0-nasa-program-project-life-cycle.md) | 3.0 Program/Project Life Cycle | Life-cycle model; Key Decision Points |
| [ch08](chapters/ch08-3-1-program-formulation.md) | 3.1 Program Formulation | Program coupling taxonomy |
| [ch09](chapters/ch09-3-2-program-implementation.md) | 3.2 Program Implementation | Program technical activities; reviews |
| [ch10](chapters/ch10-3-3-project-pre-phase-a-concept-studies.md) | 3.3 Pre-Phase A: Concept Studies | ConOps; Analysis of Alternatives |
| [ch11](chapters/ch11-3-4-project-phase-a-concept-and-technology-development.md) | 3.4 Phase A: Concept & Tech Development | SEMP; mission architecture |
| [ch12](chapters/ch12-3-5-project-phase-b-preliminary-design-and-technology-completion.md) | 3.5 Phase B: Preliminary Design | Phase B baseline; the PDR |
| [ch13](chapters/ch13-3-6-project-phase-c-final-design-and-fabrication.md) | 3.6 Phase C: Final Design & Fabrication | Detailed design package; CDR |
| [ch14](chapters/ch14-3-7-project-phase-d-system-assembly-integration-and-test-launch.md) | 3.7 Phase D: AI&T, Launch | Assembly/integration/V&V; FRR/MRR |
| [ch15](chapters/ch15-3-8-project-phase-e-operations-and-sustainment.md) | 3.8 Phase E: Operations & Sustainment | Mission operations; sustainment |
| [ch16](chapters/ch16-3-9-project-phase-f-closeout.md) | 3.9 Phase F: Closeout | Compliance matrix; NPR 7123.1 tailoring |
| [ch17](chapters/ch17-4-1-stakeholder-expectations-definition.md) | 4.1 Stakeholder Expectations | NGOs; ConOps; MOEs |
| [ch18](chapters/ch18-4-2-technical-requirements-definition.md) | 4.2 Technical Requirements | Requirements definition & validation |
| [ch19](chapters/ch19-4-3-logical-decomposition.md) | 4.3 Logical Decomposition | Functional architecture; PBS |
| [ch20](chapters/ch20-4-4-design-solution-definition.md) | 4.4 Design Solution | Trade study; decision analysis |
| [ch21](chapters/ch21-5-1-product-implementation.md) | 5.1 Product Implementation | Make/buy/reuse; Material Review Board |
| [ch22](chapters/ch22-5-2-product-integration.md) | 5.2 Product Integration | Integration strategy |
| [ch23](chapters/ch23-5-3-product-verification.md) | 5.3 Product Verification | Verification process & methods |
| [ch24](chapters/ch24-5-4-product-validation.md) | 5.4 Product Validation | Validation process |
| [ch25](chapters/ch25-5-5-product-transition.md) | 5.5 Product Transition | Transition process |
| [ch26](chapters/ch26-6-0-crosscutting-technical-management.md) | 6.0 Crosscutting Technical Management | The 8 management processes |
| [ch27](chapters/ch27-6-1-technical-planning.md) | 6.1 Technical Planning | WBS; SEMP |
| [ch28](chapters/ch28-6-2-requirements-management.md) | 6.2 Requirements Management | Traceability; change control |
| [ch29](chapters/ch29-6-3-interface-management.md) | 6.3 Interface Management | Interface specs; change control |
| [ch30](chapters/ch30-6-4-technical-risk-management.md) | 6.4 Technical Risk Management | RIDM; Continuous Risk Management |
| [ch31](chapters/ch31-6-5-configuration-management.md) | 6.5 Configuration Management | CM process |
| [ch32](chapters/ch32-6-6-technical-data-management.md) | 6.6 Technical Data Management | Data management process |
| [ch33](chapters/ch33-6-7-technical-assessment.md) | 6.7 Technical Assessment | Technical reviews; Earned Value Management |
| [ch34](chapters/ch34-6-8-decision-analysis.md) | 6.8 Decision Analysis | Decision analysis / trade studies |

## Topic Index

- **SE Engine / 17 processes** → ch01, ch02, ch03
- **Life cycle phases (Pre-A–F)** → ch07, ch10–ch16
- **Key Decision Points / technical reviews (PDR, CDR, …)** → ch07, ch33, ch12, ch13
- **Stakeholder expectations / ConOps / NGOs / MOEs** → ch17, ch10
- **Technical requirements / MOPs / TPMs** → ch18, ch33
- **Logical decomposition / functional architecture / PBS** → ch19, ch03
- **Design solution / trade studies / decision analysis** → ch20, ch34, ch04
- **Verification vs validation** → ch23, ch24
- **Integration / transition** → ch22, ch25
- **Risk management (RIDM, CRM)** → ch30
- **Configuration management** → ch31
- **Interface management** → ch29
- **Requirements management / traceability** → ch28
- **Technical planning / WBS / SEMP** → ch27, ch11
- **Earned Value Management / technical assessment** → ch33
- **Human Systems Integration** → ch05
- **Competency model** → ch06

## Supporting Files

- [glossary.md](glossary.md) — 108 NASA SE terms with chapter refs
- [patterns.md](patterns.md) — 21 techniques (SE Engine application, trade studies, V&V methods, risk, CM, reviews)
- [cheatsheet.md](cheatsheet.md) — decision rules, phase/KDP/review-gate table, cost-of-late-fix thresholds, tells & smells

---

## Scope & Limits

This pack covers NASA/SP-2016-6105 Rev 2 only. It is **NASA-specific**: the process model, Key Decision Points, technical reviews, and tailoring are framed for NASA programs/projects (and reference NPR 7123.1), with an aerospace/spaceflight emphasis. It is strong for lifecycle process, gating, V&V, and technical management; it is **not** a modelling-notation reference (use the SysML pack) and does not address AI/ML integration. The source is a US Government work in the public domain.
