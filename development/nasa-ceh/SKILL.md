---
name: nasa-ceh
description: "Knowledge base from the NASA Cost Estimating Handbook (CEH) v4.0. Use for NASA's 12-step, three-part cost estimating process (Project Definition, Cost Methodology, Cost Estimate); the WBS, CADRe, and ONCE data backbone; estimating methodologies (analogy, parametric/CER, engineering build-up, EVM, Delphi); ground rules and assumptions, data normalization and inflation (BY/CY/RY); the point-estimate-to-S-curve cost-risk chain and Unallocated Future Expense (UFE) reserves; Joint Cost and Schedule Confidence Level (JCL) analysis via probabilistic cost-loaded schedules; decision-support analyses (sensitivity, trade studies, make/lease-vs-buy, affordability, CAIV); and economic analysis (discounting, NPV, OMB Circular A-94). The cost-estimating complement to NASA's SE and risk packs. Does NOT reproduce the handbook's tool-specific procedures, worked examples, or appendix-depth methods (it names the appendices), nor cover full DoD/GAO cost guides, schedule construction, or formal risk management beyond the cost interface."
---

<!-- argument-hint: [process task/step, WBS, CADRe, methodology (analogy/parametric/CER/build-up), GR&A, normalization, cost-risk/S-curve/UFE, JCL, sensitivity/trade/CAIV/affordability, economic analysis/NPV, chapter number] -->

# NASA Cost Estimating Handbook (CEH) v4.0
**Source**: NASA (US Government work, public domain) | **Chapters**: 7

## When to use
Use this skill to produce or review a NASA cost estimate end to end: scoping and defining what is being estimated, choosing an estimating methodology and tool, normalizing data, turning a deterministic point estimate into a confidence curve with a sized reserve, running a Joint Cost and Schedule Confidence Level analysis, supporting decisions with sensitivity/trade/affordability/CAIV analyses, and comparing alternatives with a discounted economic analysis. This is the cost-and-cost-risk complement to NASA's systems-engineering and risk material (`nasa-risk`, `nasa-se-handbook`, `nasa-npr-7123`) and to the broader government cost canon (`gao-cost`, `gao-schedule`).

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below: the 12-step process, the methodology choices, the cost-risk chain, the JCL, and the decision-support and economic-analysis toolkit.
- **With a topic** — ask about a process task (e.g. "GR&A", "normalization"), a methodology ("parametric CER", "engineering build-up"), the cost-risk chain ("S-curve", "UFE"), the JCL ("time-dependent vs. time-independent"), a decision-support method ("CAIV", "trade space"), or economic analysis ("NPV", "discount rate").
- **With a chapter** — `ch01` (process overview), `ch03` (methodology), `ch04` (cost-risk), `ch05` (JCL), `ch06` (decision support), `ch07` (economic analysis).

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

> **Cost as a design variable.** The handbook's spine is that cost is not a number reported after design — it is information that shapes decisions. Keep cost drivers visible, challenge estimates that drift from history, and always deliver *uncertainty* alongside the point value.

## Core Frameworks & Mental Models

### The NASA 12-Step Cost Estimating Process (3 parts)

The process is a twelve-step sequence in three parts. Presented in order for teaching, it is iterative and rarely linear in practice; GR&A is the most frequently revisited task.

| Part | Tasks | What it produces |
|---|---|---|
| **1 — Project Definition** | 1 customer request · 2 WBS · 3 technical description | a scoped, commonly-understood definition of *what* is estimated |
| **2 — Cost Methodology** | 4 GR&A · 5 methodology · 6 models/tools · 7 data & normalization | the *approach and framework* for the estimate |
| **3 — Cost Estimate** | 8 develop · 9 cost-risk · 10 document · 11 present · 12 update | the estimate itself — produced, hardened, justified, briefed, maintained |

Governing policy an estimator must know: **NPD 1000.5** and **NPR 7120.5E** (acquisition / life-cycle management), **NPR 7123.1B** (review entrance/exit criteria). NASA's process is deliberately consistent with — but tailored from — the **GAO Cost Estimating and Assessment Guide (GAO-09-3SP)**, with a task-level mapping between them.

### Project Definition — the data backbone (Part 1)

- **Four critical elements** — resources, data, schedule, expectations — jointly agreed between estimator and decision maker *before* a methodology is chosen.
- **WBS** — a product-oriented decomposition giving full coverage *without double counting*; mandated by NPR 7120.5E, standardized to Level 2, extended below via the **CADRe standard WBS**. The estimator owns the cost WBS and maps it back to the standard.
- **CADRe** (Cost Analysis Data Requirement) — captures programmatic/technical/cost data six times across the life cycle; stored in **ONCE** (One NASA Cost Engineering database), which also receives end-of-contract actuals to update cost models. This is the empirical grounding for future estimates.
- **Technical baseline** — one common definition of the system so the Project Office estimate and an independent-review estimate are comparable.

### Estimating Methodologies (Task 5)

Three core methods plus a fourth data source; the choice follows **data availability**, which shifts across the life cycle:
- **Analogy** — adjust a similar fielded system's cost; fast but subjective, still needs normalization.
- **Parametric** — apply a **Cost Estimating Relationship (CER)**, a regression-derived Y-vs-X equation whose drivers need both statistical correlation *and* a sound logical rationale; valid only inside its data range. Built via the seven-step parametric process.
- **Engineering build-up** — decompose the WBS into work packages, estimate each (labor and material separately), aggregate; defensible and severable but costly, slow, "what-if"-resistant.
- **EVM extrapolation** — a fourth source once a program produces actuals.
- **Delphi** — a documented expert-judgment fallback only when empirical data are absent.

### GR&A, Models, and Normalization (Tasks 4, 6, 7)

- **Ground Rules and Assumptions (GR&A)** — global (whole-estimate: dollars, schedule, inclusions/exclusions, quantities) and element-specific; documented continuously as they evolve, agreed with the P/pM and stakeholders.
- **Models mechanize a methodology but don't replace judgment** — no single model fits all purposes; calibrate parametric models to comparable history, validate before use, cross-check with a second method, keep current.
- **Normalization** makes raw data comparable: inflation (BY/CY/RY dollars; **NASA New Start Inflation Index** for new efforts, DCAA forward pricing for contracted work), plus learning curves, production rate, scope, anomalies, and reporting-system mapping. Collect risk data here — uncertainty drives the later cost-risk analysis.

### The Cost-Risk Chain (Tasks 8–9)

**Point estimate → S-curve (CDF) → UFE reserve.**
- The deterministic **LCC point estimate** is the *start* of cost-risk work, not the deliverable — summing most-likely values understates the total.
- The Task 9 cost-risk assessment produces a credible **S-curve / Cumulative Distribution Function** across the cost range; the confidence level is read off it.
- **Unallocated Future Expense (UFE)** is the reserve sized to reach the management-chosen confidence; phase it where risk realizes (PDR→CDR, Integration & Test).
- Document to the **rebuild standard** (Basis of Estimate complete enough for an independent analyst to reproduce the number); keep the estimate a living baseline (Task 12, with EVM against actuals).

### Joint Cost and Schedule Confidence Level (JCL)

The probability of finishing at or under **both** the cost target **and** the schedule target — jointly, not as two separate confidences. Produced via a **Probabilistic Cost-Loaded Schedule (PCLS)** in six steps (0 goals · 1 schedule · 2 cost-load · 3 risk · 4 uncertainty · 5 results).
- **Time-Dependent (TD)** cost grows when the schedule slips (the "marching army"); **Time-Independent (TI)** cost (e.g. materials) does not.
- **Risk** = discrete probability-and-impact event; **uncertainty** = indefiniteness of the baseline (triangular distribution; usually dominates variance). Modeled together but kept distinct.
- The scatterplot's **lower-left quadrant** fraction *is* the JCL; **frontier lines** mark chosen confidence levels; the chart is a snapshot of the current plan only.
- Policy: ABC = 70% JCL, MA ≥ 50%, reviewed by the Standing Review Board, set at KDP-C (projects) / KDP-I (programs).

### Decision-Support and Economic Analysis (Ch 6–7)

- **Five decision-support categories**: Sensitivity, Trade Studies, Affordability, CAIV, Economic Analysis (procedures in Appendix N).
- **CAIV / Affordability** invert the default flow: cost becomes an input/constraint and **design converges on cost** while meeting *threshold* performance.
- **Economic Analysis** layers discounting and cost-vs-benefit on the LCCE: seven steps, **NPV** as the criterion (most-positive wins), **OMB Circular A-94** for discount rates, and inflation (NNSI) kept distinct from the time-value-of-money.

---

## Chapter Index

| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-nasa-ceh-introduction-and-process-overview.md) | Introduction & Process Overview | Why cost estimating exists; cost as a design variable; the 12-step / 3-part process; governing policy (NPD 1000.5, NPR 7120.5E, NPR 7123.1B); mapping to the GAO guide |
| [ch02](chapters/ch02-nasa-ceh-project-definition-tasks.md) | Project Definition (Tasks 1–3) | Customer request and the four critical elements; the WBS (coverage without double counting, Level 2 standard, CADRe extension); CADRe and ONCE; the technical baseline |
| [ch03](chapters/ch03-nasa-ceh-cost-methodology-tasks.md) | Cost Methodology (Tasks 4–7) | GR&A; analogy / parametric (CER) / engineering build-up / Delphi; models and tools; data gathering and normalization; inflation (BY/CY/RY) and the NASA New Start Inflation Index |
| [ch04](chapters/ch04-nasa-ceh-cost-estimate-tasks.md) | Cost Estimate (Tasks 8–12) | The LCC point estimate; probabilistic estimating; the S-curve / CDF; cost-risk assessment and UFE; the Basis of Estimate and the rebuild standard; presentation and updating; EVM |
| [ch05](chapters/ch05-nasa-ceh-jcl-analysis.md) | Joint Cost & Schedule Confidence Level (JCL) | The PCLS method; the six steps; time-dependent vs. time-independent cost; risk vs. uncertainty; the scatterplot, quadrants and frontier lines; ABC/MA policy thresholds |
| [ch06](chapters/ch06-nasa-ceh-decision-support-analyses.md) | Decision-Support Analyses | Sensitivity analysis (five steps); cost-performance trade studies and the trade space; make-vs-buy and lease-vs-buy; affordability; Cost As an Independent Variable (CAIV) |
| [ch07](chapters/ch07-nasa-ceh-economic-analysis.md) | Economic Analysis | Discounting and the time-value-of-money; NPV and measures of merit; the seven-step EA process; OMB Circular A-94; nominal vs. real rates; cost-effectiveness when benefits won't quantify |

## Topic Index

- **Affordability analysis** → ch06
- **Analogy method** → ch03
- **Basis of Estimate (BOE) / rebuild standard** → ch04
- **CADRe (Cost Analysis Data Requirement)** → ch02, ch04
- **CAIV (Cost As an Independent Variable)** → ch06
- **Cost as a design variable** → ch01
- **Cost Estimating Relationship (CER)** → ch03, ch04
- **Cost-risk assessment** → ch04
- **Cross check** → ch04
- **Cumulative Distribution Function (CDF) / S-curve** → ch04
- **Decision support (five categories)** → ch06
- **Delphi method** → ch03
- **Discounting / discount rate** → ch07
- **Earned Value Management (EVM)** → ch04, ch03
- **Economic Analysis (EA)** → ch07
- **Engineering build-up method** → ch03
- **Four critical elements** → ch02
- **Frontier line (JCL)** → ch05
- **Ground Rules and Assumptions (GR&A)** → ch03, ch04
- **Inflation / dollar types (BY / CY / RY)** → ch03
- **Joint Cost and Schedule Confidence Level (JCL)** → ch05
- **Lease-versus-buy analysis** → ch06
- **Life-Cycle Cost (LCC) point estimate** → ch04
- **Make-versus-buy analysis** → ch06
- **Methodology selection (data availability)** → ch03
- **NASA New Start Inflation Index (NNSI)** → ch03, ch07
- **Net Present Value (NPV)** → ch07
- **Nominal versus real rate** → ch07
- **Normalization** → ch03
- **OMB Circular A-94** → ch07, ch06
- **ONCE database** → ch02
- **Parametric method** → ch03
- **Point estimate** → ch04, ch06
- **Probabilistic cost estimate** → ch04
- **Probabilistic Cost-Loaded Schedule (PCLS)** → ch05
- **Process overview (12 steps, 3 parts)** → ch01
- **Project Definition tasks** → ch02
- **Risk versus uncertainty** → ch05
- **Sensitivity analysis** → ch06, ch04
- **Technical baseline / description** → ch02
- **Time-Dependent vs. Time-Independent cost** → ch05
- **Trade study / trade space** → ch06
- **Unallocated Future Expense (UFE)** → ch04, ch05
- **Work Breakdown Structure (WBS)** → ch02

## Supporting Files

- [glossary.md](glossary.md) — key cost-estimating terms, alphabetical, with chapter references
- [patterns.md](patterns.md) — reusable patterns (define-before-price, method by data availability, normalize-then-compare, point-estimate-to-S-curve, rebuild-standard documentation, the JCL/PCLS, affordability/CAIV, the seven-step EA) with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — the 12-step process table, methodology selection table, dollar types, the cost-risk chain, the JCL, decision-support analyses, economic analysis formulas, tells & smells

---

## Scope & Limits

**Covers**: NASA's cost estimating process per the NASA Cost Estimating Handbook v4.0 — the 12-step, three-part process; Project Definition (customer request, WBS, CADRe/ONCE, technical baseline); methodology selection (analogy, parametric/CER, engineering build-up, EVM, Delphi); GR&A, model/tool selection, and data normalization/inflation; the deterministic-to-probabilistic cost-risk chain (point estimate, S-curve/CDF, UFE) and documentation/presentation/updating; JCL analysis via probabilistic cost-loaded schedules; the five decision-support analyses (sensitivity, trade studies, make/lease-vs-buy, affordability, CAIV); and economic analysis (discounting, NPV, OMB Circular A-94).

**Does not cover in depth**: the handbook's appendix-depth procedures, worked examples, and tool-specific instructions (named here as Appendices C, F, G, H, I, J, K, N and pointers to ACEIT/PCEC/NAFCOM/SEER/PRICE — not reproduced); detailed regression/statistical method for building CERs; schedule *construction* (see `nasa-schedule` / `gao-schedule` and the NASA Schedule Management Handbook); formal risk identification and handling beyond the cost interface (see `nasa-risk`); and the full GAO and DoD cost guides (see `gao-cost`; complemented by `dau-se-guidebook`).

**Source version**: NASA Cost Estimating Handbook (CEH) Version 4.0, February 2015. Public-domain US Government work; guidance is NASA-specific and not a substitute for the current controlled handbook in a live estimating engagement.
