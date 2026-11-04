---
name: gao-tra
description: "Knowledge base from the GAO Technology Readiness Assessment Guide (GAO-20-48G, 2020). Use for evaluating technology maturity in acquisition programs and projects: Technology Readiness Levels (TRL 1–9) and related scales (MRL, IRL), identifying Critical Technology Elements (CTEs), the five-step process for a high-quality TRA, the four characteristics of a reliable TRA (comprehensive, well-documented, credible, defensible), Technology Maturation Plans (TMPs), and using TRA results in knowledge-based, milestone decisions. Assessment/maturity oriented: it measures readiness and frames risk — it is not a full SE process model, cost-estimating, or schedule guide (see sibling packs for those)."
---

<!-- argument-hint: [TRL level, readiness scale (MRL/IRL), critical technology element (CTE), TRA step, TRA characteristic, technology maturation plan (TMP), maturity decision, chapter number] -->

# GAO Technology Readiness Assessment Guide (GAO-20-48G, 2020)
**Source**: US Government Accountability Office (GAO) — US Government work, public domain | **Chapters**: 7

## When to use
Use this skill when you need to assess, explain, or critique the **maturity and readiness of a technology** before committing it to an acquisition program or project: assigning Technology Readiness Levels, identifying which technologies are *critical* (CTEs), planning and conducting a high-quality TRA, judging whether an existing TRA is reliable, building a Technology Maturation Plan for immature technology, or using TRA results to inform a knowledge-based milestone decision. This is GAO's cross-government best-practice companion to the agency-specific SE handbooks (NASA, DoD).

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below for an overview of TRLs, CTEs, the five-step TRA process, and the four characteristics of a reliable TRA.
- **With a topic** — ask about a TRL level, a readiness scale (MRL/IRL), identifying CTEs, a TRA step, a TRA characteristic, or building a TMP.
- **With a chapter** — ask for `ch02` (TRL scale), `ch03` (CTEs), `ch04` (five-step process), `ch05` (four characteristics), `ch06` (TMPs).

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### What a TRA is (and isn't)

A **Technology Readiness Assessment (TRA)** is a systematic, evidence-based evaluation of the maturity of *critical* technologies. It produces a **snapshot** of readiness at a point in time, expressed in Technology Readiness Levels. It is a **risk-identification** tool, not a pass/fail gate and not a guarantee of program success: a high TRL reduces — but does not eliminate — technology risk. A TRA informs decisions; it does not make them.

### Technology Readiness Levels (TRL 1–9)

The nine-level maturity scale (originated by NASA, adopted across government):

| TRL | Meaning | Environment |
|---|---|---|
| 1 | Basic principles observed and reported | — |
| 2 | Technology concept and/or application formulated | — |
| 3 | Analytical/experimental proof-of-concept | Laboratory |
| 4 | Component/breadboard validated | Laboratory |
| 5 | Component/breadboard validated | **Relevant** environment |
| 6 | System/subsystem model or prototype demonstrated | **Relevant** environment |
| 7 | System prototype demonstrated | **Operational** environment |
| 8 | Actual system completed and qualified through test & demonstration | Operational |
| 9 | Actual system proven through successful **mission** operations | Operational |

The decisive jumps are **lab → relevant environment** (TRL 4→5/6) and **relevant → operational environment** (TRL 6→7). Many programs over-rate TRLs by demonstrating in a *less* representative environment than they claim. Related scales: **Manufacturing Readiness Levels (MRL)** for producibility and **Integration Readiness Levels (IRL)** for how well elements work together — readiness is more than a single TRL number.

### Critical Technology Elements (CTEs)

A technology is a **CTE** if it is **new or novel**, or **used in a new or novel way**, *and* is **needed for the system to meet its operational performance requirements** within cost and schedule. The TRA assesses **CTEs**, not every technology — so **identifying CTEs correctly is the highest-leverage step**: miss a CTE and the program carries unassessed risk; over-include and the TRA drowns in noise. CTE identification should be driven by the work breakdown structure and requirements, with independent review.

### The Five-Step TRA Process

A high-quality TRA follows five steps:

1. **Prepare the TRA plan and select the assessment team** — scope, schedule, methodology, and an *independent, credible, expert* team.
2. **Identify the Critical Technology Elements (CTEs)** — using the WBS/requirements and the "new/novel + needed" test.
3. **Assess the CTEs' readiness** — gather and evaluate evidence to assign a TRL to each CTE against defined criteria and environments.
4. **Prepare the TRA report** — document the CTEs, evidence, TRLs, assumptions, and limitations.
5. **Use the TRA results** — feed maturity findings into program decisions and, for immature CTEs, into a Technology Maturation Plan.

(Appendix II of the Guide provides "key questions" auditors use to judge how well a program followed these five steps.)

### The Four Characteristics of a Reliable TRA

GAO judges TRA quality against four characteristics — a TRA is only as useful as it is reliable:

- **Comprehensive** — all CTEs identified; readiness assessed against complete, defined criteria and the correct environment.
- **Well-documented** — evidence, assumptions, methods, and TRL rationale captured so the assessment can be traced and repeated.
- **Credible** — performed by qualified, **independent** assessors; evidence is sufficient and objective.
- **Defensible** — conclusions follow from the evidence and withstand independent scrutiny and oversight.

### Technology Maturation Plan (TMP)

When a CTE is **immature** (below the TRL needed for the upcoming decision), the program responds with a **Technology Maturation Plan**: the steps, resources, schedule, and level of effort to raise the CTE to the required TRL, plus alternatives/off-ramps if it cannot mature in time. The TMP turns a TRA finding into managed action.

### Knowledge-Based Acquisition

The reason TRAs matter: **knowledge-based acquisition** holds that major investment decisions should be made only when the requisite knowledge (including technology maturity) is in hand. Demonstrating CTEs at **TRL 7 (operational environment)** before committing to product development is the best-practice maturity threshold; starting development with immature CTEs is a leading, well-documented cause of cost growth and schedule slip.

---

## Chapter Index

| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-tra-fundamentals.md) | TRA Fundamentals | What a TRA is/isn't, why technology maturity matters, the snapshot/risk-tool nature, audience (developers, PMs, oversight, auditors), relationship to acquisition decisions |
| [ch02](chapters/ch02-technology-readiness-levels.md) | Technology Readiness Levels | TRL 1–9 definitions, lab/relevant/operational environments, the decisive transitions, hardware vs. software TRLs, related scales (MRL, IRL), common over-rating pitfalls |
| [ch03](chapters/ch03-critical-technology-elements.md) | Critical Technology Elements | The CTE definition ("new/novel + needed"), identifying CTEs from the WBS/requirements, why CTE selection is highest-leverage, independent review, common omissions |
| [ch04](chapters/ch04-five-step-tra-process.md) | The Five-Step TRA Process | Plan & team selection, identify CTEs, assess readiness, report, use results; Appendix II key questions; roles and independence |
| [ch05](chapters/ch05-four-characteristics.md) | Four Characteristics of a Reliable TRA | Comprehensive, well-documented, credible, defensible — what each means, the evidence each requires, and how a weak TRA fails each |
| [ch06](chapters/ch06-technology-maturation-plans.md) | Technology Maturation Plans | Responding to immature CTEs, TMP content (steps/resources/schedule/off-ramps), maturing to the required TRL, linking TMP to risk management |
| [ch07](chapters/ch07-using-tras-in-decisions.md) | Using TRAs in Decisions | Knowledge-based acquisition, TRL thresholds at milestones (TRL 6/7), TRAs in governance/oversight, pitfalls (calendar-driven, optimistic, non-independent assessments) |

## Topic Index

- **TRA — definition, purpose, snapshot/risk nature** → ch01
- **Audience / who uses a TRA** → ch01
- **Technology Readiness Levels (TRL 1–9)** → ch02, cheatsheet
- **Environments (lab / relevant / operational)** → ch02, cheatsheet
- **Hardware vs. software TRLs** → ch02
- **Manufacturing Readiness Levels (MRL) / Integration Readiness Levels (IRL)** → ch02
- **TRL over-rating pitfalls** → ch02, ch07
- **Critical Technology Elements (CTEs) — definition & identification** → ch03, cheatsheet
- **Work breakdown structure / requirements as CTE source** → ch03
- **Five-step TRA process** → ch04, cheatsheet
- **Assessment team / independence** → ch04, ch05
- **Appendix II key questions** → ch04
- **Four characteristics (comprehensive / well-documented / credible / defensible)** → ch05, cheatsheet
- **TRA report** → ch04, ch05
- **Technology Maturation Plan (TMP)** → ch06, cheatsheet
- **Immature technology / off-ramps** → ch06, ch07
- **Knowledge-based acquisition** → ch07, ch01
- **TRL thresholds at milestones (TRL 6/7)** → ch07, cheatsheet
- **TRAs in governance / oversight / audit** → ch07, ch01
- **Pitfalls (calendar-driven, optimistic, non-independent)** → ch07

## Supporting Files

- [glossary.md](glossary.md) — key TRA terms (TRL, CTE, TMP, MRL/IRL, the four characteristics, environments), alphabetical, with chapter references
- [patterns.md](patterns.md) — reusable patterns (identifying CTEs, assigning a defensible TRL, running an independent assessment, building a TMP, judging an existing TRA) with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — TRL table, environment cues, CTE test, five steps, four characteristics, milestone TRL thresholds, tells & smells

---

## Scope & Limits

**Covers**: GAO best practices for technology readiness assessment per GAO-20-48G — what a TRA is and why technology maturity matters; the TRL 1–9 scale and the lab/relevant/operational environments; related readiness scales (MRL, IRL); identifying Critical Technology Elements; the five-step process for conducting a high-quality TRA; the four characteristics of a reliable TRA (comprehensive, well-documented, credible, defensible); Technology Maturation Plans for immature technology; and using TRA results in knowledge-based, milestone decisions.

**Does not cover in depth**: the full systems-engineering process (see `dau-se-guidebook`, `nasa-se-handbook`, `nasa-npr-7123`); cost estimating (see a cost-estimating source / GAO-20-195G); schedule assessment (see the GAO Schedule Assessment Guide); agile adoption (see the GAO Agile Assessment Guide); detailed agency-specific TRA procedures (DoD/DOE/NASA have their own implementing guidance); and the engineering of any specific technology domain.

**Jurisdiction**: US Government public domain work (GAO). Best practices are cross-government and adoptable by any organisation; they are guidance, not binding requirements outside an agency that adopts them.
