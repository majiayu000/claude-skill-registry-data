---
name: gao-cost
description: "Knowledge base from the GAO Cost Estimating and Assessment Guide (GAO-20-195G). Use for program cost estimating: the four characteristics of a reliable estimate (comprehensive, well documented, accurate, credible) and the 18 best practices; the 12-step cost estimating process (purpose, plan, technical baseline, WBS, ground rules and assumptions, data, point estimate, sensitivity, risk/uncertainty, document, present, update); estimating methods (analogy, parametric, engineering build-up, learning curves); Monte Carlo risk/uncertainty analysis, confidence levels and contingency; auditing and validating an estimate against the characteristics; earned value management (EIA-748, BCWS/BCWP/ACWP, CPI/SPI/TCPI, EAC, PMB, IBR); and specialized techniques (software cost estimating, learning curves, Analysis of Alternatives, WBS templates, the Green Book internal-control framework). This is the cost-estimating companion to the GAO Schedule and Technology Readiness Assessment guides. Does not cover schedule estimating/risk in depth (see the GAO Schedule Assessment Guide), agency-specific cost models, or the full text of referenced standards (EIA-748, MIL-STD-881D, the Green Book) — these are named, not reproduced."
---

<!-- argument-hint: [characteristic, 12-step process step, estimating method, risk/uncertainty, EVM term, audit, software/learning-curve/AOA, chapter number] -->

# GAO Cost Estimating and Assessment Guide (GAO-20-195G)
**Source**: GAO (US Government work, public domain) | **Chapters**: 8

## When to use
Use this skill to develop, manage, or evaluate a program **cost estimate**: framing the estimate's purpose and scope, structuring it with a WBS, choosing estimating methods, turning a point estimate into a risk-adjusted budget, documenting and updating it, auditing it against GAO's reliability criteria, and connecting it to **earned value management** for execution. This is the cost-estimating companion to the GAO `gao-schedule` and `gao-tra` guides and the management-side counterpart to a program's life cycle cost estimate.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below: the four characteristics + 18 best practices, the 12-step process, the estimating methods, risk/uncertainty, EVM, and the specialized techniques.
- **With a topic** — ask about a characteristic ("credible"), a step ("ground rules and assumptions", "point estimate"), a method ("parametric", "learning curve"), a risk concept ("Monte Carlo", "confidence level", "contingency"), or an EVM term ("CPI", "EAC", "performance measurement baseline").
- **With a chapter** — `ch02`/`ch03`/`ch05` (the 12 steps), `ch04` (risk/uncertainty), `ch06` (auditing), `ch07` (EVM), `ch08` (specialized techniques).

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

> **One discipline, two uses.** The Guide is both an **authoring** standard (how to build a reliable estimate) and an **audit** standard (how to grade one). The same four characteristics and 18 best practices serve both. EVM (ch07) is the execution-side bridge: the estimate says what a program *could* cost; EVM measures whether it is *delivering* against a baseline built from that estimate.

## Core Frameworks & Mental Models

### What a cost estimate is — and why reliability is a process, not luck

A cost estimate is the sum of individual cost elements, built from established methods and valid data, projecting what a program will cost in the future given what is known now. It is not a one-time deliverable — *managing* it means revising it as actuals arrive, adjusting it when the program changes, and analyzing the gaps. The Guide's central claim: **reliability is the predictable output of a disciplined, repeatable process**, not seniority or luck. A reliable estimate matters structurally for government — every dollar committed to one program is denied to another, so an unrealistic estimate can ripple cuts across a whole portfolio.

### The Four Characteristics of a Reliable Cost Estimate

GAO's research identifies four characteristics that a reliable estimate exhibits. They are the assessment yardstick auditors apply, and the design targets an estimator engineers toward:

| Characteristic | What it demands |
|---|---|
| **Comprehensive** | full life cycle + complete scope (a complete WBS); all GR&As documented; nothing omitted or double-counted |
| **Well documented** | sources, methods, and calculations captured so an unfamiliar analyst could rebuild it; traced to source data |
| **Accurate** | unbiased (not optimistic or conservative); most-likely-cost basis; inflation-adjusted; reconciled to actuals |
| **Credible** | limitations exposed via sensitivity and risk/uncertainty analysis; major drivers cross-checked; reconciled to an independent cost estimate (ICE) |

The **18 best practices** are the actionable steps that produce these characteristics; each best practice maps to one characteristic. An estimate that fully reflects all four is deemed **reliable**.

### The 12-Step Cost Estimating Process

The procedural backbone, grouped into four phases:

- **Plan & define (Steps 1-4)**: (1) define the estimate's **purpose** — intended use fixes scope and detail; (2) develop the **estimating plan** — team, study plan, schedule; (3) define the **program** via a cost-free **technical baseline description**; (4) determine the estimating structure — the **work breakdown structure (WBS)**, the product-oriented decomposition that ties cost, schedule, EVM, and risk together.
- **Build the number (Steps 5-7)**: (5) identify **ground rules and assumptions** (global + element-specific); (6) **obtain the data** — collect, validate, normalize (the most difficult, time-consuming step; data quality is the biggest lever); (7) develop the **point estimate** — select a method per WBS element, build the model, time-phase, sum, and cross-check against an ICE.
- **Quantify confidence (Steps 8-9)**: (8) **sensitivity analysis** (vary one input at a time); (9) **risk and uncertainty analysis** (vary many inputs together via simulation → probability distribution + confidence level).
- **Finalize & sustain (Steps 10-12)**: (10) **document** the estimate; (11) **present** it to management for formal approval (not finished until approved); (12) **update** it against actuals and program changes over the life cycle.

Each step's chapter closes with a "Survey of Step" — Process Tasks, Best Practices, and Likely Effects if criteria are not fully met — which is what makes each step **auditable**.

### Estimating Methods

Choose by program maturity and available data; the method can differ per WBS element:

| Method | Use when | Trade-off |
|---|---|---|
| **Analogy** | early; a close similar system exists | fast, low data; weak without a good analog |
| **Parametric** | drivers + cost history, design still vague | repeatable via cost estimating relationships (CERs); needs valid data range |
| **Engineering build-up** | mature design | most accurate; slow and data-hungry |

Supplemented by expert opinion, extrapolation from actuals (averages, EACs), and **learning curves** (Y = AX^b) for recurring production.

### Risk and Uncertainty → a risk-adjusted budget

A point estimate alone carries no confidence information and tends to under-fund. **Sensitivity analysis** isolates one input at a time (ranked on a tornado chart) to find what the estimate is most responsive to. **Risk and uncertainty analysis** lets inputs vary together — via the **three-point** method (min/most-likely/max) and/or the **risk-driver** method (probability × cost effect, from the risk register) — driven by **Monte Carlo simulation**, producing a total-cost probability distribution. Reading the **cumulative distribution (S curve)** gives a defensible **confidence level**; **contingency** is sized as the gap between the point estimate and that level.

### Earned Value Management (EVM) — measuring execution

Spending data alone misleads (the railroad example: looks under-budget while badly behind). EVM adds the missing third number — the *value of work performed*. Three measures: **BCWS** (planned value), **BCWP** (earned value), **ACWP** (actual cost). Derived indexes: **CPI** = BCWP/ACWP (cost), **SPI** = BCWP/BCWS (schedule), **TCPI** (efficiency needed on remaining work). The **EAC** forecasts total cost from cumulative CPI. The estimate is converted into a time-phased **performance measurement baseline (PMB)**; an **integrated baseline review (IBR)** confirms it is executable — the crucial link between cost estimating and EVM. EVM systems are validated against **EIA-748's 32 guidelines**. OMB requires EVM for major acquisitions with development effort.

### Specialized Techniques & Internal Control

Beyond the 12 steps: **software cost estimating** (size first via SLOC/function points/COSMIC, convert to effort; classify code new/reused/adapted/auto-generated); **learning curves** (unit vs. cumulative-average theory; Anderlohr/retrograde for production breaks); **Analysis of Alternatives (AOA)** (22 best practices in 5 phases; NPV where benefits monetize); **WBS templates** (MIL-STD-881D, NASA/DOE/PMI handbooks); and the **Green Book** (GAO-14-704G) internal-control framework (5 components, 17 principles) — because the cost estimating process *is itself an internal control*.

---

## Chapter Index

| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-gao-cost-fundamentals-credible-estimates.md) | Fundamentals & the four characteristics | What a cost estimate is; reliability as process; the four characteristics; 18 best practices; 12-step process; LCCE; why government needs reliable estimates |
| [ch02](chapters/ch02-gao-cost-process-planning-program-definition.md) | Steps 1-4: Planning & program definition | Purpose & scope; estimating plan/team; technical baseline description; the work breakdown structure (WBS) |
| [ch03](chapters/ch03-gao-cost-data-ground-rules-point-estimate.md) | Steps 5-7: Ground rules, data, point estimate | Global vs. element-specific GR&As; data collection/validation/normalization; estimating methods (analogy/parametric/build-up); cross-checks and the ICE |
| [ch04](chapters/ch04-gao-cost-sensitivity-risk-uncertainty.md) | Steps 8-9: Sensitivity, risk & uncertainty | Sensitivity (one-at-a-time, tornado chart); three-point & risk-driver methods; Monte Carlo; S curve, confidence level, contingency |
| [ch05](chapters/ch05-gao-cost-document-present-update.md) | Steps 10-12: Document, present, update | Documentation template & rationale; management approval; updating against actuals and program changes |
| [ch06](chapters/ch06-gao-cost-auditing-validating.md) | Auditing & validating | The characteristics/best practices as gradable criteria; mapping practices to characteristics; assessing agency guidance against the 12 steps; audit criteria & data collection |
| [ch07](chapters/ch07-gao-cost-earned-value-management.md) | Earned value management | EIA-748 (32 guidelines); 13 EVM activities; PMB/IBR/CPR; BCWS/BCWP/ACWP; CPI/SPI/TCPI; EAC; OTB/OTS; EVM system acceptance |
| [ch08](chapters/ch08-gao-cost-specialized-techniques-internal-control.md) | Specialized techniques & internal control | Software cost estimating; learning curves (Anderlohr/retrograde); WBS templates; TRLs; AOA (22 practices); the Green Book (5 components, 17 principles) |

## Topic Index

- **18 best practices** → ch01, ch06, cheatsheet
- **Accurate (characteristic)** → ch01, ch06
- **Analogy method** → ch03, cheatsheet
- **Analysis of Alternatives (AOA)** → ch08, ch01
- **Anderlohr / retrograde (production break)** → ch08
- **Audit / validation of an estimate** → ch06, patterns
- **CPI / SPI / TCPI (performance indexes)** → ch07, cheatsheet
- **Comprehensive (characteristic)** → ch01, ch06
- **Confidence level / S curve** → ch04, cheatsheet
- **Contingency / management reserve** → ch04, ch07
- **Cost estimating relationship (CER)** → ch03, ch04
- **Credible (characteristic)** → ch01, ch06
- **Data collection / validation / normalization** → ch03
- **Documentation (Step 10)** → ch05, patterns
- **Earned value management (EVM)** → ch07, ch01, cheatsheet
- **EIA-748 / 32 guidelines** → ch07
- **Engineering build-up method** → ch03, cheatsheet
- **Estimate at completion (EAC)** → ch07
- **Four characteristics (reliable estimate)** → ch01, ch06, cheatsheet
- **Green Book / internal control** → ch08
- **Ground rules & assumptions (GR&A)** → ch03
- **Independent cost estimate (ICE)** → ch03, ch05
- **Integrated baseline review (IBR)** → ch07, ch08
- **Learning curve (Y = AX^b)** → ch08, ch03
- **Life cycle cost estimate (LCCE)** → ch01, ch02
- **Monte Carlo simulation** → ch04
- **Parametric method** → ch03, cheatsheet
- **Performance measurement baseline (PMB)** → ch07
- **Point estimate (Step 7)** → ch03
- **Present / management approval (Step 11)** → ch05
- **Risk & uncertainty analysis (Step 9)** → ch04, cheatsheet
- **Risk driver / risk register** → ch04
- **Sensitivity analysis (Step 8)** → ch04, cheatsheet
- **Software cost estimating** → ch08
- **Technical baseline description (Step 3)** → ch02
- **Technology readiness level (TRL)** → ch08
- **Three-point estimate** → ch04
- **Tornado chart** → ch04
- **12-step process** → ch02, ch03, ch04, ch05, cheatsheet
- **Update the estimate (Step 12)** → ch05
- **Well documented (characteristic)** → ch01, ch05, ch06
- **Work breakdown structure (WBS)** → ch02, ch08
- **WBS templates (MIL-STD-881D, NASA/DOE/PMI)** → ch08

## Supporting Files

- [glossary.md](glossary.md) — key cost-estimating, risk, and EVM terms, alphabetical, with chapter references
- [patterns.md](patterns.md) — reusable patterns (run the 12 steps; engineer toward the four characteristics; pick a method by maturity; convert the point estimate to a risk-adjusted budget; document/update; audit; pair with EVM; specialized techniques) with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — the 12 steps, four-characteristics table, method-selection table, risk toolkit, EVM index reference, and tells & smells

---

## Scope & Limits

**Covers**: program cost estimating per the GAO Cost Estimating and Assessment Guide (GAO-20-195G, March 2020) — the four characteristics of a reliable estimate and the 18 best practices; the full 12-step cost estimating process; estimating methods (analogy, parametric, engineering build-up, learning curves); sensitivity, risk, and uncertainty analysis (Monte Carlo, confidence levels, contingency); documenting, presenting, and updating; auditing/validating an estimate against the characteristics; earned value management (EIA-748, the EVM measures and indexes, PMB, IBR, EAC forecasting, system acceptance); and specialized techniques (software cost estimating, Analysis of Alternatives, WBS templates, technology readiness levels, the Green Book internal-control framework).

**Thin on / does not cover in depth**: **schedule** estimating and **schedule risk analysis** — the Guide deliberately hands these to the GAO **Schedule Assessment Guide** (GAO-16-89G; see `gao-schedule`), and technology-maturity assessment to the **Technology Readiness Assessment Guide** (GAO-20-48G; see `gao-tra`). It does **not reproduce** the full text of referenced standards and frameworks — **EIA-748**, **MIL-STD-881D**, the **Green Book** (GAO-14-704G), ICEAA/AACEI/PMI standards — these are named and summarized, not copied. Embedded source figures and tables (discipline maps, WBS diagrams, worked method tables, EVM exhibits) are described/paraphrased here, not reproduced; redraw from the originals if a rendered exhibit is needed. The Guide is GAO best-practice guidance, oriented to US federal acquisitions and DoD/NASA examples; it is not a regulation, though several statutes (Weapon Systems Acquisition Reform Act, Nunn-McCurdy, FASA, Clinger-Cohen, the FAR/DFARS EVM provisions) make parts of it effectively mandatory for major acquisitions.

**Jurisdiction**: US Government public domain work. The guidance is voluntary best practice but is broadly adopted and partly mandated for federal major acquisitions; it is adaptable to non-federal programs.
