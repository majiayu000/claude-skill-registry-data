---
name: mil-hdbk-338
description: "Knowledge base from MIL-HDBK-338B (Electronic Reliability Design Handbook). Use for electronic reliability engineering: R/M/A theory, reliability specification/allocation/prediction, parts management and derating, reliable circuit and fault-tolerant design, environmental and human performance reliability, FMEA/FMECA/FTA/sneak circuit analysis, design reviews and testability, FRACAS, reliability demonstration and growth testing, and systems-level R&M parameters. Covers selected Part 2 design-guidance topics only; skips large annex/part-stress tables. Guidance handbook — not a contractual requirement text. Does not replace MIL-HDBK-217 prediction libraries, service-specific reliability regs, or safety standards (see mil-std-882)."
---

<!-- argument-hint: [reliability topic, MTBF/MTTR, derating, FMEA/FTA, growth test, testability, or chapter number] -->

# MIL-HDBK-338B — Electronic Reliability Design
**Source**: DoD MIL-HDBK-338B (US Government work, public domain; Distribution Statement A) | **Chapters**: 9

## When to use
Reach for this pack when designing or reviewing electronic/hardware reliability programs grounded in MIL-HDBK-338B — especially reliability requirements and allocation, parts derating, prediction caveats, FMEA/FTA, testability, FRACAS, and reliability growth/demonstration strategy. Use it to brief design teams on inherent reliability levers and to structure analytical and test feedback loops.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below.
- **With a topic** — ask about MTBF/availability, allocation/prediction, derating, fault tolerance, FMEA/FTA, growth testing, FRACAS, or testability.
- **With a chapter** — ask for `ch01` through `ch09`.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

> **Guidance only.** 338B states it is not to be cited as a requirement. Synthesize practices; do not paste annex reliability tables or third-party standard text.

## Core Frameworks & Mental Models

### Inherent reliability is a design output
Once the design (parts, stresses, architecture) is approved, inherent reliability is largely fixed. Parts, derating, circuit design, and fault tolerance set that ceiling before test.

### Spec, allocate, model, predict
Quantitative requirements with environment; allocation tree; reliability model matching architecture; prediction with explicit method/assumptions; refresh when design changes.

### R/M/A and system effectiveness
Reliability, maintainability, and availability metrics (including MTBF/MTTR-class measures) feed system effectiveness. Know whether you discuss inherent or operational measures.

### Analysis pair: FMEA/FMECA + FTA (+ SCA when needed)
Inductive failure mode analysis for breadth; deductive fault trees for critical top events; sneak circuit analysis for latent paths without part failure.

### Empirical loop: FRACAS + demonstration/growth
Data collection and closed-loop corrective action; choose growth (design still plastic) vs demonstration (frozen design decision test); accelerated tests need physics-aware reading.

### Testability as a reliability property
Detection/isolation provisions and design-review gates make predicted reliability verifiable in integration and field use.

## Chapter Index
| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-rma-theory-foundations.md) | R/M/A Theory Foundations | Distributions, failure modeling, MTBF/MTTR/availability, Bayesian notes |
| [ch02](chapters/ch02-specification-allocation-prediction.md) | Spec, Allocation, Prediction | Requirements, apportionment, models, prediction methods |
| [ch03](chapters/ch03-parts-management-and-derating.md) | Parts Management & Derating | Parts control, electronic/mechanical derating |
| [ch04](chapters/ch04-circuit-design-and-fault-tolerance.md) | Circuit Design & Fault Tolerance | Robust circuits, redundancy, fault-tolerant design |
| [ch05](chapters/ch05-environmental-and-human-reliability.md) | Environment & Human Reliability | Environmental design, human performance reliability |
| [ch06](chapters/ch06-fmea-fta-and-sneak-circuits.md) | FMEA/FTA/SCA | FMEA/FMECA, fault trees, sneak circuits |
| [ch07](chapters/ch07-design-reviews-testability-safety.md) | Reviews, Testability, Safety Link | Design reviews, DFT/BIT, safety program interface |
| [ch08](chapters/ch08-data-fracas-demonstration-growth.md) | Data, FRACAS, Demo & Growth | Data uses, FRACAS, demonstration, growth, accelerated test |
| [ch09](chapters/ch09-systems-reliability-engineering.md) | Systems Reliability Engineering | Effectiveness, system R&M parameters, COTS/NDI |

## Topic Index
- **Allocation / apportionment** → ch02
- **Availability (inherent vs operational)** → ch01, ch09
- **BIT / diagnostics** → ch07
- **COTS / NDI reliability** → ch09
- **Derating** → ch03
- **Environmental stress design** → ch05
- **Failure distributions / Weibull / exponential** → ch01
- **Fault tolerance / redundancy** → ch04
- **Fault tree analysis (FTA)** → ch06
- **FMEA / FMECA** → ch06
- **FRACAS** → ch08
- **Human performance reliability** → ch05
- **MTBF / MTTR** → ch01, ch02
- **Parts management** → ch03
- **Physics-of-failure / stress drivers** → ch05, ch03
- **Reliability demonstration** → ch08
- **Reliability growth testing** → ch08
- **Reliability prediction** → ch02
- **Sneak circuit analysis** → ch06
- **System effectiveness** → ch09
- **Testability / DFT** → ch07

## Supporting Files
- [glossary.md](glossary.md) — R&M terms used across selected 338B topics
- [patterns.md](patterns.md) — implementation patterns with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — decision rules, maps, tells & smells

---

## Scope & Limits
This pack covers **selected design-guidance material** from MIL-HDBK-338B (1 Oct 1998; Notice 2 keeps active) — R/M/A theory, specification/allocation/prediction, core Section 7 design guidelines (parts through safety interface), reliability data/FRACAS/demonstration/growth, and systems reliability engineering. Extraction metadata reports **1046 PDF pages** for the nde-ed.org mirror copy (DLA catalog often cites ~716 content pages; PDF page objects can differ). It does **not** reproduce large annex part-stress/reliability tables, full worked numerical appendices, or third-party standards quoted inside 338B. Guidance only — not contractual requirements text. US Government public domain work (Distribution Statement A). No source-material download link is published.
