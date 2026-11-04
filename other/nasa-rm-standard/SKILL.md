---
name: nasa-rm-standard
description: "Knowledge base from NASA-STD-8729.1A — NASA's R&M (Reliability and Maintainability) standard covering spaceflight and support systems (Revision A, 2017-06-13). Use for NASA's objectives-driven R&M framework — the R&M objectives hierarchy (one Top Objective decomposed into four sub-objectives, paired with tailorable strategies), how R&M requirements are established inside the SMA Plan required by NPR 7120.5, the SMA Technical Authority concurrence/independent-evaluation governance, milestone vs. readiness review gates, the reliability/maintainability/availability vocabulary (Ai vs. Ao, the failure causal chain, risk as a triplet), and the R&M Evidentiary Methods catalogue (FMEA/FMECA, FTA, RBDA, RCM, LORA, plus the space-environment and parts-pedigree analyses). Scoped to NASA spaceflight and support systems and to assurance planning: it is an objectives-and-strategies standard, so it deliberately does NOT prescribe step-by-step analysis procedures (those live in the referenced NASA Preferred Reliability Practices) and is thin on facility R&M, detailed math/derivations, and non-NASA or commercial life cycles."
---

<!-- argument-hint: [objective/strategy, SMA Plan, SMA Technical Authority, milestone/readiness review, availability (Ai/Ao), FMEA/FMECA/FTA/RBDA/RCM/LORA, evidentiary method, mission class/scope, failure chain, chapter number] -->

# NASA Reliability & Maintainability Standard (NASA-STD-8729.1A, Rev A, 2017-06-13)
**Source**: NASA — US Government work, public domain | **Chapters**: 6

## When to use
Use this skill when you need to work with NASA's reliability and maintainability requirements for spaceflight and support systems under NASA-STD-8729.1A (Revision A, 2017). It is the right pack when you need to understand the objectives-driven R&M framework: how the Top Objective and its four sub-objectives are established, how R&M requirements are embedded in the SMA Plan required by NPR 7120.5, and how the SMA Technical Authority concurrence and milestone/readiness review gates operate. Reach for it when reasoning about availability (Inherent Ai vs. Operational Ao), the failure causal chain, or selecting an evidentiary analysis method such as FMEA, FMECA, FTA, RBDA, RCM, or LORA for NASA missions.

**Prerequisites:** none, plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below for an overview of the objectives-driven R&M framework, the objectives hierarchy, the SMA Plan / Technical Authority governance, and the analysis vocabulary.
- **With a topic** — ask about a specific objective or strategy, the SMA Plan and how R&M requirements are established, the milestone vs. readiness review gates, the Ai/Ao availability split, the failure causal chain, or a named analysis (FMEA, FMECA, FTA, RBDA, RCM, LORA, Worst Case Analysis, etc.).
- **With a chapter** — ask for `ch01` (scope & applicability), `ch02` (terminology & definitions), `ch03` (R&M required approach: objectives & strategies), `ch04` (implementation requirements: planning, evaluation & review), `ch05` (objectives hierarchy & scope identification), or `ch06` (evidentiary analysis methods).

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### The Objectives-Driven R&M Framework
The defining caveat of this standard is that it specifies **objectives and strategies, not processes**. It tells programs *what* R&M outcome to achieve and *why*, while deliberately leaving most of the *how* to the implementing team so they can innovate. "Mandatory" here is procedural: a program must (1) **use** the objectives and strategies in planning, (2) **justify** how deeply each objective is addressed, scaled to the accepted safety-and-mission-success risk, and (3) **demonstrate** at review that the objectives are satisfied. If you are searching the standard for a required procedure, you are in the wrong layer — the standard expects you to supply the method and defend the choice.

### The R&M Objectives Hierarchy (Appendix A) — the spine
A single **Top Objective** (sustain required performance across the lifecycle so mission objectives are met) decomposes into **four sub-objectives**:
- **(a)** the system conforms to design intent across interfaces and functions, under both nominal and failed conditions;
- **(b)** the system stays functional for the intended life, environment, operating conditions, and usage;
- **(c)** the system tolerates faults, failures, and anomalies arising internally or externally;
- **(d)** the system reaches reliability and maintainability sufficient to satisfy the **availability** requirement.

The hierarchy is built from **Objective** and **Strategy** blocks used in an **alternating** fashion — every objective is paired with at least one strategy — supported by **Requirement** and **Context** blocks. Two views describe the same structure: a **flowchart view** (logical shape) and a **tabular view with Scope Identification** (Appendix B) that adds, per bottom-level strategy, the suggested **evidence** method and the **scope** appropriate to each mission class. Evidence and scope hang off the leaves, not the top.

### Implementation, Governance & Review Gates (Section 5)
R&M requirements are **established inside the SMA Plan** required by NPR 7120.5 (addressing Appendix A objectives/strategies and Appendix B tables) — there is no separate freestanding R&M plan. The plan **references rather than restates**: it points to criteria, requirements, design/process standards, schedules, evidence products, and organizational interfaces in other documents. Governance institutionalizes a **doer/concurrer split**: the project produces the plan and evidence; the **SMA Technical Authority** concurs the plan is sufficient *before* work proceeds, **verifies** that independent evaluation actually happened, and concurs in the evidence at gates. Two review bars: **milestone reviews** test adequacy-against-plan, product maturity, standards conformance, and acceptable technical risk; **readiness reviews** test adequacy and acceptable **residual** risk. Compliance is demonstrated through **products presented as evidence**.

### The R&M Vocabulary (Section 3) — outcome words vs. method words
The standard front-loads a precise vocabulary. Sort terms into **outcome words** (reliability, maintainability, availability, dependability, operational readiness, sustainability) and **method words** (FMEA, FMECA, FTA, RBDA, RCM, LORA). Load-bearing distinctions:
- **Availability is two quantities**: **Inherent Ai = MTTF / (MTTF + MTTR)** (designer-controlled) and **Operational Ao = MTBF / (MTBF + MDT)** (folds in logistics, spares, ready/admin downtime — the bridge between readiness and supportability). The gap between them is a supportability decision, not a design decision.
- **The failure causal chain**: cause → fault → mechanism → mode → failure → effect, with propagation terms describing how problems cross product boundaries.
- **Risk is a triplet**: scenario(s), likelihood(s), consequence(s), with uncertainty folded into the last two; managed via risk management, risk reduction, and documented risk acceptance.
- **Criticality and severity are program-defined** — the standard leaves those classifications to each program/project.

### The Reliability Analysis Toolbox — failure space vs. success space
The named analyses split on two axes. **Failure space**: FMEA/FMECA (bottom-up, inductive — find failure modes, effects, single-point failures, criticality) and FTA (deductive, top-down from a defined failure top-event). **Success space**: RBDA (a symbolic-logic model where an unbroken input-to-output path means success). **RCM** settles the corrective/preventive maintenance mix for a required reliability at minimum cost; **LORA** decides the repair level (replace/repair/discard). Choose the tool by asking which space the question lives in, then which direction (inductive bottom-up vs. deductive top-down) the question runs.

### R&M Evidentiary Methods (Appendix C) — evidence over assertion
R&M objectives must be **earned with evidence**. Appendix C is a two-table catalogue — **Reliability Analysis Methods** and **Maintainability Analysis Methods** — each method described by a five-column descriptor (*what is done / why / in what circumstances / when performed / referenced NASA Preferred Reliability Practice*). Key mental models: **read the row, not the title**; the **"in what circumstances" column is a cost gate** (reserve expensive analyses like Sneak Circuit Analysis for critical hardware; invoke environment-specific analyses — IESD, surface ESD, SEE, micrometeoroid/debris — only when that threat is present); **timing is keyed to design maturity** (functional FMECA/FTA early, piece-part FMECA and Worst Case Analysis once candidate flight designs exist). The table indexes the method; the referenced practice holds the procedure.

---

## Chapter Index

| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-nasa-rm-standard-scope-and-applicability.md) | Scope, Applicability & Standard Structure | Objectives-vs-processes posture; mandatory engagement / flexible implementation; tailoring to accepted risk; applicability (NASA Centers built-in; contractors/JPL by reference); facility exclusion; order of precedence; NPR 7120.5 as the lone applicable document |
| [ch02](chapters/ch02-nasa-rm-standard-terminology-and-definitions.md) | R&M Terminology & Core Definitions | Reliability/maintainability/availability triad; Inherent (Ai) vs. Operational (Ao) availability; the failure causal chain; risk as a triplet; criticality/severity; single-point failure, failure tolerance, redundancy; the FMEA/FMECA/FTA/RBDA/RCM/LORA framework set; verification vs. validation |
| [ch03](chapters/ch03-nasa-rm-standard-objectives-and-strategies.md) | R&M Required Approach: Objectives & Strategies | The top-level objective and its four sub-objectives; strategies as tailorable minimum expectations; the objectives-driven approach; the two levers (prevention + recovery); availability as the integrating requirement; SMA Plan linkage |
| [ch04](chapters/ch04-nasa-rm-standard-implementation-requirements.md) | Implementation Requirements: Planning, Evaluation & Review | R&M requirements inside the SMA Plan (NPR 7120.5); plan-by-reference; ten plan dimensions; Appendix B minimum scope; SMA Technical Authority concurrence; resource accountability; milestone vs. readiness review bars; independent evaluation |
| [ch05](chapters/ch05-nasa-rm-standard-objectives-hierarchy-and-scope.md) | R&M Objectives Hierarchy & Scope Identification | Flowchart vs. tabular views; Objective/Strategy/SubObjective/Requirement/Context block types; the alternation rule; Top Objective; evidence and scope on the bottom-level strategies; scope dialed by mission class |
| [ch06](chapters/ch06-nasa-rm-standard-evidentiary-analysis-methods.md) | Evidentiary Methods: Reliability & Maintainability Analysis | The two-table evidentiary catalogue; five-column method descriptor; reliability methods (FMEA/FMECA, FTA, modeling, WCA, thermal/stress family, space-environment cluster, parts pedigree); maintainability methods (modeling, maintenance concept/plan, RCM, LSA, testability); NASA Preferred Reliability Practices |

## Topic Index

- **Objectives-driven framework / objectives vs. processes** → ch01, ch03, ch05
- **Applicability / scope / facility exclusion / order of precedence** → ch01
- **Tailoring to accepted risk** → ch01, ch03
- **NPR 7120.5 / SMA Plan** → ch03, ch04
- **Terminology / definitions / acronyms** → ch02
- **Availability / Inherent Ai / Operational Ao** → ch02
- **Failure causal chain / fault / failure mode / effect** → ch02
- **Risk triplet / risk acceptance / criticality / severity** → ch02
- **Single point failure / failure tolerance / redundancy** → ch02
- **Verification / validation** → ch02
- **Top objective / four sub-objectives** → ch03, ch05
- **Strategies / minimum expectation** → ch03, ch05
- **SMA Technical Authority / concurrence / independent evaluation** → ch04
- **Milestone review / readiness review / residual risk** → ch04
- **Plan by reference / Appendix B minimum scope** → ch04
- **Objectives hierarchy / Objective / Strategy / Requirement / Context blocks** → ch05
- **Mission class / scope identification** → ch05
- **Evidentiary methods catalogue** → ch06
- **FMEA / FMECA** → ch02, ch06
- **Fault Tree Analysis (FTA)** → ch02, ch06
- **Reliability Block Diagram Analysis (RBDA)** → ch02
- **Reliability Centered Maintenance (RCM)** → ch02, ch06
- **Level of Repair Analysis (LORA)** → ch02
- **Worst Case Analysis (WCA) / thermal / stress** → ch06
- **NASA Preferred Reliability Practices** → ch06

## Supporting Files

- [glossary.md](glossary.md) — key R&M terms (availability Ai/Ao, the failure chain, FMEA/FMECA/FTA/RBDA/RCM/LORA, SMA Plan, SMA Technical Authority, objectives/strategies, mission class), alphabetical, with chapter references
- [patterns.md](patterns.md) — reusable R&M patterns (justification ledger, plan-by-reference, scope-by-mission-class, doer/concurrer split, failure-space vs. success-space tool choice, gating evidentiary methods, the two availabilities, parts-pedigree chain) with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — decision rules, the objectives hierarchy and failure chain in one picture, the governance/review-gate table, the reliability & maintainability method lists, outcome-vs-method words, tells & smells

---

## Scope & Limits

**Covers**: NASA's objectives-driven R&M approach per NASA-STD-8729.1A (Revision A, 2017-06-13) — the R&M objectives hierarchy (Top Objective + four sub-objectives + tailorable strategies, in flowchart and scope-identification table views); how R&M requirements are established inside the SMA Plan required by NPR 7120.5; the SMA Technical Authority concurrence and independent-evaluation governance; milestone vs. readiness review gates; the reliability/maintainability/availability vocabulary (Ai vs. Ao, the failure causal chain, risk as a triplet, program-defined criticality/severity); and the R&M Evidentiary Methods catalogue (FMEA/FMECA, FTA, RBDA, RCM, LORA, the thermal/stress family, the space-environment cluster, and parts-pedigree controls).

**Does not cover in depth**: step-by-step analysis procedures — the standard is objectives-and-strategies, so the actual *how-to* for each method lives in the referenced **NASA Preferred Reliability Practices** (by number), which are outside this source; detailed reliability mathematics, derivations, and worked numerical examples; **facility** R&M (explicitly excluded and routed to NPD 8831.1, NPR 8820.2, NPR 8831.2, and the NASA RCM and RCBEA guides), except critical technical facilities tied to Space Flight Systems; program/project management mechanics (those live in NPR 7120.5); and non-NASA, commercial, or non-spaceflight life cycles.

**Jurisdiction**: US Government work — public domain (17 U.S.C. § 105). Approved for use by NASA Headquarters and Centers; reaches JPL, contractors, grant recipients, and agreement parties only as their instruments specify or reference it. **Source version: NASA-STD-8729.1A, Revision A, approved 2017-06-13 (superseding NASA-STD-8729.1).**
