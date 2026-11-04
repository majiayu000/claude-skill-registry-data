---
name: nasa-systems-modeling
description: "Knowledge base from the NASA Systems Modeling Handbook for Systems Engineering (NASA-HDBK-1009A Rev A, 2025). Use for model-based systems engineering (MBSE) wired into NASA's NPR 7123.1 SE processes: the three aspects of MBSE (language / methodology / framework), the NASA SE Engine and its two OOSEM-derived steps (Model Planning, Setting Up the Model), the Modeling Plan as a SEMP subset, the tool-agnostic NASA SE metamodel of elements and relationships across the four SysML pillars (structure / behavior / requirements / parametrics), worked SysML diagrams and tables for stakeholders, requirements, structure and V&V, generating SE work products (ConOps, MOE, MOP, TPM, V&V), the MBSE Grid framework, alternative modeling approaches (PBR, Scenario, System Specification, Verification), and the ConOps model-content template. Scope is bounded to four common technical processes (Stakeholder Expectation Definition, Technical Requirements Definition, Product Verification, Product Validation). Does NOT teach SysML itself, mandate a tool, define NPR 7123.1 processes, cover technical-management processes 10-17, or reproduce the OMG SysML specification."
---

<!-- argument-hint: [MBSE aspect, SE Engine, metamodel, pillar, SysML diagram/table, work product (ConOps/MOE/MOP/TPM/V&V), MBSE Grid, alternative approach, chapter number] -->

# NASA Systems Modeling Handbook (NASA-HDBK-1009A Rev A)
**Source**: NASA (US Government work, public domain) | **Chapters**: 8

## When to use
Use this skill when you need to do model-based systems engineering *in support of* NASA's mandated SE processes rather than as a parallel diagramming activity: planning a modeling effort, setting up a model's conventions and organization, building a tool-agnostic metamodel that traces back to NPR 7123.1, capturing stakeholders / requirements / structure / behavior / V&V as SysML diagrams and tables, and harvesting those views to generate the standard NASA SE work products (ConOps, MOE, MOP, TPM, V&V) that feed technical reviews. This is the MBSE-method bridge between NASA SE governance (`nasa-npr-7123`, `nasa-se-handbook`) and the SysML/OMG modeling-language landscape (`omg-signpost`).

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime. Working knowledge of SysML helps but is not taught here.

## How to Use This Skill
- **Without arguments** — load the core frameworks below: the three aspects of MBSE, the NASA SE Engine plus its two added steps, the metamodel and its four pillars, the model→work-product extraction model, and the MBSE Grid.
- **With a topic** — ask about an aspect (language / methodology / framework), a metamodel pillar (structure / behavior / requirements / parametrics), a relationship (derive / trace / verifies / satisfies / refines / allocate), a work product (ConOps, MOE, MOP, TPM, V&V), or an alternative approach (PBR, Scenario, System Specification, Verification).
- **With a chapter** — `ch01` (MBSE overview + SE Engine), `ch03` (the metamodel), `ch04`/`ch05` (worked diagrams: structure / V&V), `ch06` (generating work products), `ch07` (MBSE Grid + alternatives), `ch08` (ConOps template).

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

> **One handbook, one thesis.** The model is the *source*; diagrams, tables, and matrices are *views* extracted from it to implement the SE processes and feed reviews. SysML v1.7, MagicDraw, and CATIA No Magic are illustrations — the **metamodel** underneath is tool-agnostic and traces to NPR 7123.1. Scope is bounded to four common technical processes by an Agency MBSE Community of Practice survey.

## Core Frameworks & Mental Models

### What this handbook is for

NASA-HDBK-1009A answers one question: how do you wire SysML system modeling directly into the SE processes NASA already mandates under **NPR 7123.1**, so the model becomes the *source* from which standard SE work products are generated? It does **not** replace NPR 7123.1 or NASA/SP-2016-6105 (the NASA SE Handbook) — it shows how to model in support of them, and existing Agency guidance always takes precedence.

### The three aspects of MBSE (the organizing spine)

MBSE decomposes into three independent dials; confusing them is the usual trap:

1. **Modeling language** — the symbols and their meaning (*what symbols mean*). The handbook uses **SysML** (OMG, v1.7): nine diagram types grouped into four pillars.
2. **Modeling methodology** — the step-by-step procedure (*what order to do things in*). The handbook uses the **NASA SE Engine plus two steps**.
3. **Modeling framework** — how the model's elements and relationships are organized (*where things go*). The handbook uses the **MBSE Grid tailored to NASA**.

The tool-agnostic stance is exactly the claim that the *language* dial can be swapped (SysML out, something else in) without disturbing methodology and framework, because the **metamodel** sits underneath all three.

### The methodology — NASA SE Engine plus two OOSEM steps

The **NASA SE Engine** (NPR 7123.1D Fig 3-1; handbook Fig 4.1-1) is the *means* of doing SE — 17 common technical processes across three sets: **system design**, **product realization**, **technical management**. The handbook's methodology follows the Engine but inserts two model-specific steps borrowed from **OOSEM** (INCOSE's Object-Oriented Systems Engineering Method):

- **Model Planning** — lands inside Technical Process 10 (Technical Planning). Produces the **Modeling Plan** (a technical plan, a *subset of the SEMP*) covering supportable products, resources, roles, tools, conventions, accessibility, and management. Established early, updated as the system matures.
- **Setting Up the Model** — lands at the start of the System Design Processes as "Step 0." Three decisions: **conventions** (element/package naming), **standards** (profiles), **organization** (package hierarchy reflecting the system). All results are documented back into the Modeling Plan.

Remember "*name it, govern it, file it*" for the three setup decisions, and that the Modeling Plan is "*the SEMP, zoomed in*."

### The four SysML pillars

SysML's nine diagram types group into four **pillars** that jointly build one integrated model context:

| Pillar | Covers | Key SysML diagrams |
|---|---|---|
| **Structure** | logical/physical layers, systems, subsystems, components, interfaces | bdd, ibd, package |
| **Behavior** | functionality, interaction, response, info/data flow | use case (uc), activity (act), sequence (sd), state machine (stm) |
| **Requirements** | specifications and V&V | requirement diagram (req), requirements table |
| **Parametrics** | constraints, mathematical statements | parametric diagram |

### The framework — MBSE Grid tailored to NASA

The **MBSE Grid** (Morkevicius et al., INCOSE 2017) is a matrix: in native form, life-cycle phases on the rows, SysML pillars on the columns; each cross-section holds metamodel content. Tailored to NASA it puts **technical processes 1–9 on the rows** (it deliberately *excludes* technical-management processes 10–17) and the four pillars on the columns; cross-sections become organizing slots where diagrams and tables get filed (Appendix C shows a populated grid). The Grid splits into **problem** (black box = conceptual, white box = technical) and **solution** (design alternatives) sections, onto which NASA's four System Design Processes drape directly.

### The metamodel — NASA SE elements and relationships

A **metamodel** is the set of modeling elements you may create plus the relationships that legitimately connect them. The handbook builds its metamodel from the SE elements and relationships in NPR 7123.1, split across a **general metamodel (Figure 7-1)** and a **V&V metamodel (Figure 7-2)**. Two defining features:

- **Language-agnostic by construction.** The language-specific type sits in **square brackets** — `[requirement]`, `[block]`, `[activity]`, `[derives]` — and the brackets are a *substitution slot*: SysML 1.7 fills them today, SysML v2 or another language could fill them tomorrow without changing the SE-level structure.
- **One approach, not a mandate.** It is presented as one viable approach (others exist inside NASA); whatever metamodel a project adopts, plus its assumptions, is recorded in that project's Modeling Plan.

Its job is to give a **trace-back path** for the three anchor activities — Stakeholder Expectations Definition, Technical Requirements Definition, and V&V — supporting the SE Engine and the generation of SE products. Figures are deliberately simplified ("shown at one level for simplicity") — read each drawn relationship as a representative instance of something that can exist at many levels.

### The connective verbs (relationships)

- **derive / derived requirement** — flow-down (Needs → Goals → Objectives → system requirements; MOPs can derive from any requirement/MOE/higher MOP).
- **trace** — links stakeholders to needs, and MOEs/MOPs/TPMs to requirements and structure.
- **satisfies** — a requirement satisfied by a block, behavior, or value property; validation requirements carry `satisfies`.
- **verifies** — verification requirement → system requirement (one-to-many).
- **refines** — MOEs refine objectives; MOPs refine requirements similarly.
- **allocate** — activity diagrams use swim lanes to allocate behavior to structure.

### Building the model (worked SysML)

The handbook's Section 8 demonstrates the apparatus by pairing each diagram with the **metamodel fragment** it realizes ("metamodel fragment + sample instance"). **Order does not matter** — SE work can enter the SE Engine at multiple points, so the model is a connected web, not a linear pipeline. The same elements appear through **different views** (context as bdd *and* ibd; activities as activity diagram *and* functional-decomposition bdd; requirements as req diagram *and* table) — the diagram type is a choice of emphasis, not a different truth. **Verification and validation share the same machinery**, differing chiefly in `verifies` vs `satisfies`; a diagram and its matrix are two windows on one model.

### Generating SE work products (the payoff)

Section 9 maps each in-scope NPR 7123.1 work product to the **named set of views** (a figure showing the view family + a table itemizing them with Section 8 references) you extract from the populated model. Extraction is **mechanical and tool-flexible** (by hand or third-party tools; into templates, webpages, or browsed in-tool). The four in-scope processes: **Stakeholder Expectations Definition, Technical Requirements Definition, Verification, Validation**. The measure chain: **MOE** (qualitative stakeholder-satisfaction judgment) → **MOP** (quantitative target whose satisfaction props up the MOE) → **TPM** (time-tracked subset of MOPs). **Tailoring is a feature** — the chapter publishes the menu of candidate views; a project selects the subset matching its maturity and the review at hand.

### Alternative approaches and the ConOps overlay

Appendix D offers **pillar-targeted extensions** that still map back to the section 7 metamodel: **PBR** (Property-Based Requirements — extends Requirements), **Scenario Modeling** (extends Behavior), **System Specification** (Structure→Requirements bridge), **Verification Modeling** (V&V/parametric layer) — the last three sourced to The OpenSE Cookbook. Appendix F overlays MBSE diagrams onto the existing NASA SE Handbook (Appendix S) **ConOps annotated outline**, leaving the outline text intact and showing where model views earn their place ("draw once, reference many").

---

## Chapter Index

| # | Handbook section | Key content |
|---|------------------|-------------|
| [ch01](chapters/ch01-nasa-systems-modeling-mbse-overview-se-engine.md) | §4 (overview) | Purpose; bounded scope (4 processes); three aspects of MBSE (language/methodology/framework); SE Engine + two OOSEM steps; nine diagrams / four pillars; tool-agnostic stance |
| [ch02](chapters/ch02-nasa-systems-modeling-model-planning-and-setup.md) | §5–6 | Model Planning → the Modeling Plan (SEMP subset); Setting Up the Model (conventions / standards / organization); the plan is living |
| [ch03](chapters/ch03-nasa-systems-modeling-the-metamodel.md) | §7 | The metamodel (Fig 7-1 general, Fig 7-2 V&V); `[ ]` bracket substitution; four pillars' notes; MOE/MOP/TPM; "one approach" framing |
| [ch04](chapters/ch04-nasa-systems-modeling-building-stakeholders-requirements-structure.md) | §8.1–8.13 | Worked SysML: stakeholders, NGOs, context (bdd/ibd), behavior (uc/act), structure (bdd/ibd), requirements flow-down, MOE/MOP/TPM |
| [ch05](chapters/ch05-nasa-systems-modeling-building-verification-validation.md) | §8.14–8.22 | Worked V&V: verify-method attribute, `verifies` one-to-many, success-criteria constraints, V&V cases/configuration, matrices/VCS, validation reuse |
| [ch06](chapters/ch06-nasa-systems-modeling-generating-se-work-products.md) | §9 | Mapping work products to view sets; ConOps/MOE/MOP/TPM/V&V; figure+table pattern; extraction is tool-flexible; tailoring |
| [ch07](chapters/ch07-nasa-systems-modeling-methodology-framework-alternative-approaches.md) | App. B–E | OOSEM methodology origin; MBSE Grid framework; Grid↔NASA mapping; alternative approaches (PBR/Scenario/SystemSpec/Verification); interface metamodel |
| [ch08](chapters/ch08-nasa-systems-modeling-conops-template-with-model-content.md) | App. F | ConOps annotated outline (from SE Handbook App. S) overlaid with MBSE views; section-to-view mapping; modes as state machines; DRMs |

## Topic Index

- **Activity diagram (act) / swim lanes / allocation** → ch04, ch05
- **Alternative modeling approaches (PBR / Scenario / System Specification / Verification)** → ch07, cheatsheet
- **Behavior pillar** → ch03, ch04
- **Block definition diagram (bdd) / internal block diagram (ibd)** → ch04, ch05
- **ConOps (Concept of Operations)** → ch06, ch08
- **ConOps annotated outline (SE Handbook App. S)** → ch08
- **derive / derived requirement** → ch04, glossary
- **Design Reference Mission (DRM)** → ch08
- **Four pillars (structure / behavior / requirements / parametrics)** → ch01, ch03, cheatsheet
- **Interface metamodel (Appendix E)** → ch07
- **Language / methodology / framework (three aspects of MBSE)** → ch01, cheatsheet
- **MBSE Grid** → ch01, ch07, cheatsheet
- **Measures of Effectiveness (MOE)** → ch03, ch04, ch06, cheatsheet
- **Measures of Performance (MOP)** → ch03, ch04, ch06, cheatsheet
- **Metamodel (Figures 7-1, 7-2) / `[ ]` bracket convention** → ch03, cheatsheet
- **Model Planning / Modeling Plan** → ch02, glossary
- **Model organization / conventions / standards (setup)** → ch02, cheatsheet
- **NASA SE Engine** → ch01, ch07, glossary
- **Needs, Goals, Objectives (NGOs)** → ch04, ch06, ch08
- **NPR 7123.1 (governing reference)** → ch01, ch03, ch06
- **OOSEM (methodology source)** → ch01, ch07, glossary
- **Parametric pillar / parametric diagram** → ch03, ch04
- **Property-Based Requirements (PBR)** → ch03, ch07
- **refines** → ch03, ch06
- **Requirements pillar / requirements diagram / Requirements Table** → ch03, ch04
- **Requirements Verification Matrix / Compliance Spreadsheet (VCS)** → ch05, ch06
- **satisfies** → ch03, ch05, glossary
- **SEMP (Systems Engineering Management Plan)** → ch02, glossary
- **Setting Up the Model ("Step 0")** → ch01, ch02
- **State machine (stm) / modes of operation** → ch04, ch08
- **Stakeholder Expectations Definition / stakeholders as actors** → ch04, ch06
- **Structure pillar / decomposition** → ch03, ch04
- **SysML (OMG v1.7) / nine diagram types** → ch01, ch03, glossary
- **Technical Performance Measures (TPM)** → ch03, ch04, ch06, cheatsheet
- **Tool-agnostic stance / language swappable** → ch01, ch03, ch07, cheatsheet
- **trace** → ch03, ch04, glossary
- **Verification and Validation (V&V) / V&V case / V&V configuration** → ch05, ch06
- **verifies / verify-method attribute** → ch05, glossary
- **Work products (generating views)** → ch06, cheatsheet

## Supporting Files

- [glossary.md](glossary.md) — key MBSE, NASA-SE, and SysML terms used in the handbook, alphabetical, with chapter references
- [patterns.md](patterns.md) — reusable modeling patterns (planning a model, building the metamodel, pairing metamodel-fragment with sample diagram, the V&V pattern, harvesting work products, tailoring the MBSE Grid) with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — three aspects, SE Engine + two steps, four pillars, the relationship verbs, MOE→MOP→TPM chain, MBSE Grid layout, alternative approaches, tells & smells

---

## Scope & Limits

**Covers**: model-based systems engineering as defined by NASA-HDBK-1009A Rev A (2025) — the three aspects of MBSE; the NASA SE Engine with its two OOSEM-derived steps (Model Planning, Setting Up the Model); the Modeling Plan as a SEMP subset; the tool-agnostic NASA SE metamodel (Figures 7-1 general, 7-2 V&V) and its four SysML pillars; worked SysML diagrams and tables for stakeholders, NGOs, context, behavior, structure, requirements, MOE/MOP/TPM, and V&V; generating the in-scope SE work products from a populated model; the MBSE Grid framework and its NASA tailoring; alternative pillar-targeted approaches (PBR, Scenario, System Specification, Verification) and the interface metamodel; and the ConOps model-content template overlay.

**Bounded scope (by design)**: the handbook covers modeling support for **only four** of NASA's common technical processes — **Stakeholder Expectation Definition, Technical Requirements Definition, Product Verification, Product Validation** — chosen via an Agency MBSE Community of Practice survey. The MBSE Grid is mapped only to technical processes **1–9**; the **technical-management processes (10–17)** are excluded from the Grid.

**Does not cover**: teaching SysML itself (assumed; the OMG SysML specification is referenced, not reproduced — see `omg-signpost`); defining the NPR 7123.1 SE processes (governing reference — see `nasa-npr-7123`, `nasa-se-handbook`); mandating a modeling tool (MagicDraw and CATIA No Magic are illustrations only, no NASA endorsement); product-realization process steps beyond what the Grid can be extended to cover; risk-modeling methods beyond the single block-with-value-properties illustration; and TPM calculation techniques (deferred to the NASA MBSE Community of Practice). The metamodel is bound to **SysML 1.7** as current-state; the handbook commits to updating for **SysML v2.0**.

**Jurisdiction**: NASA Technical Handbook, US Government work, public domain (17 U.S.C. 105) — Approved for Public Release, Distribution Unlimited. It references third-party OMG SysML (ISO/IEC 19514) material, which is © OMG and is *not* reproduced here. NASA does not endorse this pack or any tool named in the source.
