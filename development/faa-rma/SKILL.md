---
name: faa-rma
description: "Knowledge base from FAA-HDBK-006D (2020), the FAA's System Reliability, Maintainability, and Availability (RMA) Handbook for National Airspace System (NAS) hardware and software. Use for RMA figures of merit (MTBF, MTBO, MTTR, the availability variants), the bathtub curve and probability distributions, the four-stage RMA lifecycle mapped to the FAA Acquisition Management System (AMS), the six-task RMA technical-management/acquisition process, service-thread criticality and the NAS-RD severity-to-target table, the RMA analysis toolbox (RBD, FMEA/FMECA, FTA, Ishikawa, Monte Carlo, Bayesian, FRACAS, ALT, reliability-growth/recovery tests), software reliability (early prediction + reliability growth), and tailorable example RMA requirements for a Program Requirements Document. Scope limits: it is FAA/NAS-specific guidance (not a requirement, by its own statement), centred on hardware-plus-software availability — it brackets out human/service/facility/communications availability, names but does not reproduce the math derivations or external standards (MIL-STDs, IEEE 1633, RTCA DO-178C/DO-278A, SAE JA1011), is thin on detailed worked numerical examples and on safety-case method, and predates any current revision beyond 006D."
---

<!-- argument-hint: [RMA figure of merit, MTBF/MTTR/availability, criticality/severity, RMA lifecycle stage, AMS task, analysis tool (RBD/FMEA/FTA), software reliability, requirement example, chapter number] -->

# FAA-HDBK-006D — Reliability, Maintainability & Availability (RMA)
**Source**: FAA (US Government work, public domain) | **Version**: FAA-HDBK-006D (8 October 2020) | **Chapters**: 8

> **Caveat — read first.** This pack is built on **FAA-HDBK-006D (2020)**, which supersedes 006C v1.1 (2015). Cite the **006D** revision, not 006B. The handbook itself states it is **guidance only and must not be cited as a requirement**.

## When to use
Use this skill when you need to apply FAA-HDBK-006D (2020) guidance on Reliability, Maintainability, and Availability (RMA) for National Airspace System hardware and software. It covers RMA figures of merit (MTBF, MTBO, MTTR, and the availability variants), statistical distributions and the bathtub curve, the four-stage RMA lifecycle mapped to the FAA Acquisition Management System, service-thread criticality and NAS-RD severity-to-target requirements, and the full RMA analysis toolbox including RBD, FMEA/FMECA, FTA, Monte Carlo, and FRACAS. Use it when writing RMA requirements for a Program Requirements Document or when selecting and applying RMA analysis methods on a FAA/NAS program.

**Prerequisites:** none, plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill

- **Without a topic** — load the Core Frameworks below: the three pillars and dependability, figures of merit, the four-stage lifecycle, criticality/severity, the analysis toolbox, and the software-reliability split.
- **With a topic** — ask about a figure of merit (MTBF, MTTR, an availability variant), a severity category, an RMA lifecycle stage or AMS task, an analysis tool (RBD, FMEA/FMECA, FTA, Monte Carlo, FRACAS), software reliability, or how to write an RMA requirement. Use the **Topic Index** to route.
- **With a chapter** — `ch02` (figures of merit & statistics), `ch03` (lifecycle stages), `ch04` (acquisition/technical-management process), `ch05` (analysis toolbox), `ch08` (requirement examples).

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### The three pillars and the umbrella

RMA treats system dependability as something you **estimate, manage, and improve**, not hope for. Three attributes, with **dependability** as the umbrella:

- **Reliability** — probability of zero failures over a stated interval/mission. Decomposes into *material* (hardware/software/firmware), *mission* (intent/goals), and *logistics* (support) reliability.
- **Maintainability** — how easily and quickly the system is restored after failure; splits into corrective (unscheduled) and preventive (scheduled) maintenance.
- **Availability** — percentage of time ready when called upon.

Two anchoring ideas: an RMA value is an **estimate under statistical uncertainty**, never an exact truth; and it is **meaningless out of context** — you must know the design, manufacturing quality, environment, support system, training, materiel, and diagnostics behind it.

### Figures of merit — name what time you count

RMA concepts become engineering-usable only as **figures of merit** defined against an explicitly scoped "system of interest." The recurring discipline: **state which downtime is in or out.**

- **Reliability**: probability (finite mission) or **MTBF**; under exponential failure `R = e^(−t/m)`. The FAA uses **uMTBO** for services/facilities with a 24-hour mission time (Order JO 6040.15H).
- **Maintainability**: **MTTR** (and sMTTR/uMTTR) — the full restore cycle from detection to return-to-service.
- **Availability**: `uptime/(uptime+downtime)`, with variants that differ only in counted downtime — **Operational (A_op)** counts all of it, **Equipment & Services (A_es)** drops scheduled downtime, **Inherent (A_i) = MTBF/(MTBF+MTTR)** counts corrective-only. Series subsystems **multiply** (nth-root rule for equal allocation); combining systems always lowers availability.

### Statistics & distributions (when data is missing)

The **bathtub curve** maps *when* failures happen — decreasing (infant mortality), constant (random/useful life), increasing (wear-out); practical MTBF lives in the flat middle. **Confidence intervals** beat point estimates, and a **data-collection plan** with a statistically significant sample is what makes a figure of merit trustworthy. When real data does not exist, approximate it with the **probability distribution** whose shape fits: Normal, Exponential, Poisson, Lognormal, Binomial, Weibull, Empirical (Lognormal and Weibull are the workhorses; never use the Normal for time variables).

### Criticality first, numbers second

Before any number, classify the **service thread** by a **Service Risk Assessment** into one of four **Service Thread Loss Severity Categories**, each carrying a NAS-RD-2013 availability floor and restore-time limit:

| Severity | Availability floor |
|---|---|
| **Safety-Critical** | ≥ 0.99999 (≥ 2 service threads) |
| **Efficiency-Critical** | ≥ 0.9999 |
| **Essential** | ≥ 0.999 |
| **Routine** | ≥ 0.99 |

### The four-stage RMA lifecycle (on the Vee)

RMA runs across the whole life of a system in four stages mapped to FAA **Acquisition Management System (AMS)** phases, decomposed into eleven steps: **Concept/Operational Assessment** → **Requirements Development** → **Testing & Implementation** → **Monitoring & Post-Implementation**. The left arm of the **Vee** determines/allocates requirements; the right arm verifies and validates them. The **Reliability Block Diagram (RBD)**, built from the functional architecture, is the central allocation artifact.

### The six-task technical-management (acquisition) process

The acquisition-facing complement: (1) Preliminary Requirements Analysis — the **bridge** from enterprise requirements to procurement specs; (2) Procurement Package Preparation (**SSD + SOW + IFPP**); (3) Proposal Evaluation (reliability modeling, fault-tolerant design, performance — **recovery-time substantiation** is critical); (4) Design Monitoring (reviews, TIMs, separate fault-tolerance risk threads); (5) Testing & Verification; (6) Requirements Analysis & Maintenance. **One allocation method does not fit all** — top-down math suits Information Systems but is wrong for gracefully-degrading Remote/Distributed and dependency-coupled Infrastructure systems.

### The analysis toolbox — pair the tools

Design-time tools (bathtub curve, QFD, RBD, FMEA, FMECA, FTA, Ishikawa, Monte Carlo, Bayesian network) plus test-time tools (FRACAS/DCACAS, accelerated life testing, parts screening, stability, reliability-growth, failure-recovery). Most are meant to be **paired**: inductive **FMEA** (bottom-up) with deductive **FTA** (top-down); criticality is the increment from FMEA to **FMECA**; **FMECA ↔ FRACAS** is a reinforcing predict/record loop. Tool choice is deterministic — read it off your AMS phase and RMA stage.

### Software reliability — predict, then grow

Software has **no wear-out phase**, and new features/fixes temporarily *raise* failure counts. The work splits along the acquisition relationship: **Government early prediction** (before vendor/code — organizational maturity + process → defect density; IEEE 1633-2016; Neufelder Full-Scale Model) and **developer reliability growth** (problem-report metrics, software FMEA/fault trees). The fault → error → failure chain underlies every analysis method.

---

## Chapter Index

| # | Source section | Title | Key content |
|---|---|---|---|
| [ch01](chapters/ch01-faa-rma-introduction-and-key-documents.md) | §1–§3 | Introduction, Key Documents & Definitions | What RMA is and why the NAS needs it; the three pillars and dependability; estimate-under-uncertainty and context; the fault/error/failure chain; hardware vs. software RMA; RMA vs. safety vs. resiliency; the full reference base (SEM, SMS, MIL-STDs, NASA, NUREG, IEEE 1633, RTCA DO-178C/278A) |
| [ch02](chapters/ch02-faa-rma-fundamentals.md) | §4 | RMA Fundamentals: Figures of Merit, Statistics & Distributions | Figures of merit; reliability/maintainability/availability metrics and formulas; series allocation; bathtub curve; confidence intervals; data-collection plan; the seven probability distributions |
| [ch03](chapters/ch03-faa-rma-lifecycle-stages.md) | §5 | Stages in the RMA Lifecycle | The four stages and eleven steps on the Vee, mapped to AMS; Service Risk Assessment and the four severity categories; RBD allocation; FTA/FMEA; reliability growth (Duane/Crow); RCM; DCACAS closed loop |
| [ch04](chapters/ch04-faa-rma-technical-management-process.md) | §6 | RMA Technical Management Process | The six acquisition tasks; SSD/SOW/IFPP package; proposal evaluation; design monitoring; the three FAA system categories; why one allocation method does not fit all; the safety-hazard interval |
| [ch05](chapters/ch05-faa-rma-methods-and-tools.md) | §7 | Processes, Methods & Tools for RMA Implementation | The development and testing toolbox; inductive vs. deductive analysis; criticality from FMEA to FMECA; FMECA↔FRACAS loop; phase-appropriate tool selection (Table 7-1, Figure 7-6); tool limitations |
| [ch06](chapters/ch06-faa-rma-glossary-and-definitions.md) | App. A | Acronyms, Glossary & Key Definitions | The controlled vocabulary: availability variants, the mean-time family (MTBF/MTBO/MTTR/MTBM/MDT/MLDT/MMT), fault/error/failure, outage vs. interruption, recovery accounting, series/parallel, service threads, STLSC |
| [ch07](chapters/ch07-faa-rma-software-reliability.md) | App. C | Software Reliability | Why software ≠ hardware; the predict-vs-grow split; Government early prediction; IEEE 1633-2016 model catalog; Neufelder Full-Scale Model (forms A/B/C); reliability-growth program; fault taxonomies |
| [ch08](chapters/ch08-faa-rma-requirements-guidelines.md) | App. D | RMA Requirements Guidelines | Tailorable example PRD requirements; criticality-thread allocation; the NAS-RD severity-to-target table; per-discipline (reliability/availability/maintainability) requirement language; FAA Order 1000.36 "must" |

## Topic Index

- **Acquisition Management System (AMS) phases** → ch03, ch04
- **Availability variants (operational, equipment & services, inherent)** → ch02, ch06
- **Availability allocation method by system category** → ch04
- **Bathtub curve** → ch02, ch05
- **Bayesian network analysis** → ch05, ch06
- **Confidence intervals and sample size** → ch02
- **Criticality / service thread loss severity categories** → ch03, ch08
- **Data collection and corrective action (DCACAS / FRACAS)** → ch05, ch03
- **Dependability (umbrella term)** → ch01, ch06
- **Distributions (Normal, Exponential, Poisson, Lognormal, Binomial, Weibull, Empirical)** → ch02
- **Fault, error, and failure chain** → ch01, ch06
- **Figures of merit** → ch02
- **FMEA (failure mode and effects analysis)** → ch05, ch06
- **FMECA (criticality analysis)** → ch05, ch06
- **Fault tree analysis (FTA)** → ch05, ch06
- **Hardware versus software RMA** → ch01
- **Ishikawa / fishbone diagram** → ch05, ch06
- **Maintainability and MTTR** → ch02, ch08
- **Mean-time family (MTBF, MTBO, MTTR, MTBM, MDT, MLDT, MMT)** → ch06, ch02
- **Monte Carlo simulation** → ch05, ch06
- **NAS-RD severity-to-target table** → ch08, ch03
- **Outage versus interruption** → ch06
- **Procurement package (SSD, SOW, IFPP)** → ch04, ch06
- **Probability distributions** → ch02
- **Proposal evaluation and recovery-time substantiation** → ch04
- **Quality function deployment (QFD)** → ch05, ch06
- **RMA lifecycle stages and the eleven steps** → ch03
- **RMA versus safety risk** → ch01, ch04
- **Recovery time accounting** → ch06
- **Redundancy and fault tolerance** → ch04, ch08
- **Reliability block diagram (RBD)** → ch03, ch05
- **Reliability-centered maintenance (RCM)** → ch03
- **Reliability growth (Duane / Crow models)** → ch03, ch05
- **Requirement examples for a PRD** → ch08
- **Resiliency layered on RMA** → ch01
- **Series and parallel composition** → ch03, ch06
- **Software early reliability prediction** → ch07
- **Software reliability growth and problem-report metrics** → ch07
- **System categories (information, remote/distributed, infrastructure)** → ch04
- **Technical management process (the six tasks)** → ch04
- **Testing tools (ALT, parts screening, stability, reliability-growth, failure-recovery)** → ch05
- **Vee model (iterative lifecycle)** → ch03, ch05

## Supporting Files

- [glossary.md](glossary.md) — key RMA terms, alphabetical, with chapter references (synthesized, not reproduced)
- [patterns.md](patterns.md) — eight reusable RMA patterns (criticality-first authoring, RBD allocation, paired failure analysis, distribution modeling, field-then-grow software, allocation-by-failure-structure, the procurement bridge, the post-fielding loop) with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — decision rules, the three pillars, the four severity categories, the "nines," the four stages and six tasks, the toolbox, the seven distributions, and tells & smells

---

## Scope & Limits

**Covers**: FAA RMA practice per FAA-HDBK-006D (2020) — the three pillars and dependability; the figures of merit and their statistical underpinning (bathtub curve, confidence intervals, the seven distributions); the four-stage RMA lifecycle on the Vee mapped to the AMS, with service-thread criticality and the NAS-RD severity targets; the six-task technical-management/acquisition process and the three FAA system categories; the design-and-test analysis toolbox (RBD, FMEA/FMECA, FTA, Ishikawa, Monte Carlo, Bayesian, FRACAS/DCACAS, ALT, reliability-growth and failure-recovery tests); software reliability (Government early prediction + developer reliability growth); and a tailorable library of example RMA requirements for a PRD.

**Does not cover / thin on**: the handbook is **guidance only** and explicitly must not be cited as a requirement; it is **FAA/NAS-specific** and scopes its analysis to **hardware-plus-software availability**, deliberately bracketing out human, service, facility, and communications availability. It **names but does not reproduce** the external standards it leans on — MIL-STD-721C/882E/1629A/3034A, MIL-HDBK-217F/189C, NASA SP-2016-6105 / NASA-STD-8729.1A, NUREG/CR-6101, IEEE Std 1633-2016, RTCA DO-178C/DO-278A, SAE JA1011 — so it is a router into, not a substitute for, those documents. It is **thin on**: fully worked numerical examples and derivations (it points to Blanchard & Fabrycky and to SEBoK for the deeper math/statistics), formal safety-case / system-safety method (handled by FAA SMS and MIL-STD-882), and any revision beyond 006D. The supersession note means **006B references are out of scope here**.

**Jurisdiction / licence**: a work of the US Government (Federal Aviation Administration), in the **public domain** in the US — free to reproduce, transform, and redistribute, including commercially. The third-party standards it cites remain their publishers' copyright and are not reproduced in this pack.
