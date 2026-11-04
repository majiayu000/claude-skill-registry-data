---
name: nasa-fault-management
description: "Knowledge base from the NASA Fault Management Handbook (NASA-HDBK-1002, Draft 2, April 2012). Use for the systems-engineering discipline of designing what a system does when it fails — the fault/failure/anomaly vocabulary, the five FM strategies (two prevention strategies — design-time fault avoidance and operational failure avoidance — plus three tolerance strategies — failure masking, failure recovery, and goal change), the six FM process activities across NASA mission phases Pre-A to E, response-latency-versus-time-to-criticality (TTC) design trades, fault/failure containment regions and FEPPs, the four redundancy approaches, top-down FM requirements development, FM verification vs. validation, the seven dedicated FM milestone reviews (FMCR/FMARR/FMPDR/FMCDR/FMTRR/FMLRR/FMCERR), FM organizational structure, and mined NASA Lessons Learned. Space-mission oriented (flight/ground/operations); spacecraft examples throughout. IMPORTANT: built from an UNAPPROVED DRAFT — several sections (detailed architecture building blocks, the Assessment & Analysis guidance, and Operations & Maintenance) are placeholders in the source and are thin here. Thin on detailed FDIR algorithms, terrestrial/IT fault management, and any approved-standard terminology that may have changed since Draft 2."
---

<!-- argument-hint: [FM concept (fault/failure/anomaly, TTC, FEPP, FCR, safe mode), FM strategy, process activity, requirement, redundancy type, FM review (FMCR/FMARR/FMPDR/FMCDR/FMTRR/FMLRR/FMCERR), V&V, organization, lesson learned, chapter number] -->

# NASA Fault Management Handbook (NASA-HDBK-1002 Draft 2, April 2012)
**Source**: NASA — US Government work, public domain | **Chapters**: 8 | **DRAFT SOURCE**

> **READ FIRST — DRAFT.** This pack synthesizes NASA-HDBK-1002 **Draft 2 (April 2, 2012)**, an *unapproved working draft* of the NASA Fault Management Handbook. Terminology, scope, review names, and the FM process here reflect that draft and may differ from any later released or approved edition. Several source sections are explicit placeholders (detailed FM architecture building blocks in §6.3; the Assessment & Analysis guidance; the Operations & Maintenance section §9) and are correspondingly thin in this pack. Treat all of it as informational guidance, **not a controlling standard**, and verify against the current NASA standard before citing in formal work. NASA does not endorse this pack.

## When to use
Use this skill when you need to design, assess, or explain how a system detects and accommodates failures: the fault/failure/anomaly vocabulary; deciding whether a fault is handled by flight software, firmware, hardware, crew, or ground (the response-latency-vs-TTC trade); choosing among the five FM strategies and the four redundancy approaches; writing top-down FM requirements; planning FM verification and validation; running the dedicated FM milestone reviews; organizing a project so FM has a system-level home; or checking a design against recurring NASA Lessons Learned. It is the off-nominal companion to the NASA Systems Engineering Handbook.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below for an overview of the FM discipline, its vocabulary, the latency-vs-TTC trade, the five strategies, and the FM process/review structure.
- **With a topic** — ask about a concept (e.g., "time to criticality", "failure containment region", "safe mode"), a strategy (e.g., "failure masking vs. goal change"), a process activity (e.g., "FM requirements development"), a review (e.g., "FMCDR success criteria"), or organization/lessons learned.
- **With a chapter** — ask for `ch01` (definitions), `ch02` (FM process), `ch03` (requirements), `ch04` (design & architecture / latency-vs-TTC), `ch05` (V&V), `ch06` (reviews & operations), `ch07` (fundamental concepts), `ch08` (organization & lessons learned).

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### What FM is, and the central distinction

**Fault Management (FM)** is the system-level SE discipline that governs what a system does when things go wrong — preventing, detecting, isolating, diagnosing, responding to, containing, and recovering from off-nominal conditions to preserve assets (including crew) and intended functionality. It is **not** a subsystem afterthought: a design is incomplete until failures are addressed, and FM depends on flight, ground, and operations elements cooperating.

The load-bearing distinction: a **failure** is the *unacceptable performance of an intended function* (an *effect*); a **fault** is a *cause that explains a failure* (internally rooted). An **anomaly** is the *unexpected* (not necessarily unacceptable) performance of a function. The discipline is named for faults but governs failures generally. Cause and effect are *relative* — one viewpoint's cause is another's effect — so disciplined, consistent use of "fault" and "failure" in requirements is the primary guard against contradictory interpretations and latent design faults.

Off-nominal is **three states**, not a binary: **anomalous, degraded, failed**.

### The master trade: Response Latency vs. Time to Criticality

Failure effects propagate along **failure effect propagation paths (FEPPs)** from the originating failure mode toward a **Critical Failure Effect (CFE)** — the effect that irrevocably compromises an objective. **Time to Criticality (TTC)** is how long that takes. FM is a **race condition**: the whole loop must finish *within* the TTC.

Decompose any candidate response's **latency** into five intervals — observation, detection, decision, response execution, recovery — sum them for each candidate implementer (ground operators, ground software, crew, flight software, firmware, hardware), and compare to the TTC. The response is viable only if its summed latency fits inside the clock. **Count human latency** — humans performing FM are *inside* the system boundary. The ground loop (data cadence, light time, comms schedule, human decision, uplink) is usually the longest path, which is why distance from Earth and sparse contact force **autonomy**, and short-TTC phases (powered ascent, EDL, docking) mandate **automatic onboard FDIR**.

### The Five FM Strategies (two families)

Every risk-mitigation choice for a function reduces to one of five:
- **Failure prevention** — *Design-Time Fault Avoidance* (quality, margin, high-grade parts make a fault unlikely) and *Operational Failure Avoidance* (predict a future failure and forestall it).
- **Failure tolerance** — *Failure Masking* (block the effect from reaching the higher function), *Failure Recovery* (restore the function before a goal is lost), and *Goal Change* (shift to degraded but achievable goals — typically safing).

Selection is per failure mode, per mission phase, weighed against required functionality, available resources, and risk posture.

### The Five Operational FM Functions

At run time: **Detection** (threshold + persistence/filter + notification), **Diagnosis** (fault isolation + fault identification, measured by ambiguity-group size), **Decision** (assess, find options, select, notify), **Response** (goal change / failure recovery / failure masking), and **Model Adjustment** (update the expectation models — the function most prone to *normalization of deviance*). One mechanism can implement several at once (a TMR voter detects, isolates, decides, and recovers in one stroke). Prognosis is deliberately *outside* the draft's diagram.

### Redundancy, containment, tolerance

Four **redundancy approaches**, each matched to a fault class: **hardware-identical** (random part failure — but useless against common-mode), **functional/dissimilar/analytic** (common-mode, cross-checks, workarounds), **informational** (EDAC for bit corruption), **temporal** (transients, checkpoint-rollback). A **failure containment region (FCR)** is bounded by failure-containment boundaries; placing them is a key architecture act. **Fault/failure tolerance** is always tolerance *of a named fault class* — **fail-operational** (no functionality lost) vs. **fail-safe** (a critical subset preserved). The catch-all default response is **safe mode**: a protective, command-accepting, data-transmitting holding state that hands the problem to humans with time to solve it.

### The FM Process and risk posture

FM runs as **six activities inside the SE lifecycle** across mission phases Pre-A to E: conceptual design, requirements, architecture & design, assessment & analysis, V&V, operations & maintenance — and it **matures in parallel** with the nominal system (FM bolted on late is brittle and untestable). **Risk posture** (set by NPR 8705.4 mission class A–D) is the master sizing dial for FM complexity, formality, cost, and which work products apply. Assessment answers four questions — *what can go wrong, how often, what happens, what can be done* — using FMEA/FMECA, PRA, FTA, ESD/ETA, hazard, FCR, FEPP, detection/isolation, and prognostics analyses.

### Requirements, V&V, reviews, organization

- **Requirements**: derive top-down from mission concept and risk posture under one FM lead and one driving document; default to explicit, one-concept-per-statement; target *preserved functions and a safety net*, not a one-to-one FMEA map; treat faults by **possibility over probability**; gate new technology to **TRL 6 by PDR**.
- **V&V**: FM **verification** is bottom-up to requirements ("built it right"); FM **validation** is top-down to intent ("built the right thing"). Plan early inside system V&V; capture an **Incompressible Test List** and regression suites; lean on formal modeling and automation because the failure space is too large for testing alone; keep validation independent of the design team. Beware **the Bump** (the unplanned test-phase effort spike).
- **Reviews**: a **three-tier** structure plus **seven dedicated FM reviews** — FMCR, FMARR, FMPDR, FMCDR, FMTRR, FMLRR, FMCERR — each gated by maturing artifacts and FM-specific success criteria, justified because piecemeal FM coverage reliably leaves gaps.
- **Organization**: FM needs a **system-level home** with authority sized to its area of concern, vertical and horizontal interfaces, a single chartered FM lead, its own WBS/budget, and a planned-for late staffing bump (0.5 FTE planned vs. 14+ actual). The cheapest fault analysis is **mining the NASA Lessons Learned database**.

---

## Chapter Index

| # | Chapter | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-nasa-fault-management-introduction-and-fm-definitions.md) | Introduction, Scope & FM Definitions | FM as a system-level SE discipline; fault vs. failure vs. anomaly; the off-nominal three states; the failure-response vocabulary; CFE / root cause / time-to-criticality; the state-based view; the ISO network-management analogy; FM as a cost/risk balance |
| [ch02](chapters/ch02-nasa-fault-management-process.md) | The Fault Management Process | The six FM activities mapped to mission phases Pre-A–E and reviews; FM Concept Document and the four design-principle areas (incl. safing strategy); the four fundamental FM questions; FM as a distributed function; Incompressible Test List; "test what you fly"; FM work products (Table 10); risk posture (NPR 8705.4) as the sizing dial |
| [ch03](chapters/ch03-nasa-fault-management-requirements-development.md) | FM Requirements Development | Explicit vs. implicit requirements; the five-step process and eleven-dimension FM Requirements Checklist; requirement categories (Table 11); mission classes (Table 12); driving requirements (Table 13); test-platform requirements; in-house vs. out-of-house strategy; possibility over probability; too-general and too-specific pitfalls |
| [ch04](chapters/ch04-nasa-fault-management-design-and-architecture.md) | FM Design and Architecture | Mission-to-FM flow-down; risk posture in two steps; what FM must protect; **response latency decomposed (5 intervals) vs. TTC**; distance/contact dictating autonomy; phase-driven reconfigurable FM; safe mode as universal default; interacting-vehicle FM; aborts; Backup Flight Control System (note: source §6.3 architecture detail is a placeholder) |
| [ch05](chapters/ch05-nasa-fault-management-analysis-verification-validation.md) | Assessment, Analysis, Verification & Validation | FM verification (bottom-up) vs. validation (top-down); the five V&V activities; FM validation matrix; top-down scenario selection; Required/High/Medium/Low prioritization; intent categorization; test beds and formal modeling; "the Bump" and other pitfalls (Assessment & Analysis section is a draft placeholder) |
| [ch06](chapters/ch06-nasa-fault-management-operations-and-lifecycle-reviews.md) | Operations & Lifecycle Reviews | The three-tier FM review structure; the seven dedicated FM reviews (FMCR/FMARR/FMPDR/FMCDR/FMTRR/FMLRR/FMCERR) with entrance/success criteria; six rationales for dedicated reviews; Table 28 question catalog; TRL-6-by-PDR gating; fault-set agreement; phased operations outline (Operations §9 is a draft placeholder) |
| [ch07](chapters/ch07-nasa-fault-management-fundamental-concepts-and-principles.md) | FM Fundamental Concepts & Guiding Principles | The five FM strategies; the five operational FM functions; the four redundancy approaches; fault/failure cause-effect relativity, root vs. proximate cause, contributing factors; FEPPs, FCRs, CFE, TTC, the race condition; fail-operational/fail-safe; automation vs. autonomy; the eight guiding principles; normalization of deviance |
| [ch08](chapters/ch08-nasa-fault-management-organization-and-lessons-learned.md) | Management Structure & NASA Lessons Learned | FM as crosscutting/system-level; diffused responsibility as the default failure; the three org success principles; FM lead role (programmatic + technical); FM Functional Breakdown; the staffing bump; mined NASA Lessons Learned (Mars Observer, CONTOUR, SOHO, Galileo, MRO, Voyager, Mars Polar Lander, CALIPSO) |

## Topic Index

- **Abort (ascent / rendezvous / descent)** → ch04
- **Ambiguity group / diagnosis** → ch07
- **Anomaly vs. failure vs. fault** → ch01, ch07
- **Architecture (FM) / flow-down** → ch04, ch02; cheatsheet
- **Assessment & analysis (four FM questions)** → ch02, ch05
- **Automation vs. autonomy** → ch04, ch07
- **Backup Flight Control System (BFCS)** → ch04
- **Containment / FCR / FEPP** → ch07, ch04
- **Critical Failure Effect (CFE)** → ch01, ch04, ch07
- **Distributed FM function / single authoritative voice** → ch02
- **Driving requirements** → ch03, ch04
- **Fail-operational vs. fail-safe** → ch04, ch07; cheatsheet
- **Fault vs. failure (cause vs. effect)** → ch01, ch07
- **Five FM strategies** → ch07; cheatsheet, patterns
- **FM process (six activities) / mission phases** → ch02; cheatsheet
- **FM reviews (FMCR/FMARR/FMPDR/FMCDR/FMTRR/FMLRR/FMCERR)** → ch06; cheatsheet, patterns
- **Guiding principles (eight)** → ch07
- **Incompressible Test List** → ch02, ch05
- **Lessons Learned (NASA database) / mishap cases** → ch08, ch07
- **Mission class (A–D) / risk posture** → ch03, ch04, ch02; cheatsheet
- **Normalization of deviance** → ch07
- **Operational FM functions (detection/diagnosis/decision/response/model adjustment)** → ch07
- **Operations & maintenance (FM)** → ch02, ch06 (draft placeholder)
- **Organization / authority / FM lead / staffing bump** → ch08; cheatsheet, patterns
- **Possibility over probability** → ch03
- **Redundancy (four approaches)** → ch07; cheatsheet
- **Requirements (explicit vs. implicit, checklist, categories)** → ch03; patterns
- **Response latency (five intervals) vs. TTC** → ch04, ch07; cheatsheet, patterns
- **Safe mode / safing** → ch04, ch02; cheatsheet, patterns
- **Safety net** → ch02, ch03, ch06
- **State / behavior / measurement uncertainty** → ch01, ch07
- **System boundary (incl. operators inside it)** → ch07
- **Test as you fly / test beds / HITL** → ch02, ch05, ch06
- **Time to Criticality (TTC) / race condition** → ch01, ch04, ch07; cheatsheet
- **TRL 6 by PDR** → ch02, ch06
- **Verification vs. validation (FM)** → ch05; cheatsheet
- **"The Bump" (V&V effort spike)** → ch05, ch08

## Supporting Files

- [glossary.md](glossary.md) — key FM terms (fault/failure/anomaly, TTC, FEPP, FCR, the five strategies, the operational functions, redundancy, reviews, work products), alphabetical, with chapter references
- [patterns.md](patterns.md) — reusable FM patterns (parallel maturation, risk-posture-then-distribute, latency-vs-TTC budgeting, explicit top-down requirements, safe-mode fallback, fault-class-matched redundancy, top-down V&V scenarios, dedicated reviews, system-level FM organization, lessons-learned mining) with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — decision rules, the six process activities, latency decomposition, redundancy-to-fault-class table, mission-class posture, the seven FM reviews, organization principles, tells & smells

---

## Scope & Limits

**Draft status (state explicitly):** This pack is built from **NASA-HDBK-1002 Draft 2 (April 2, 2012)** — an *unapproved, unreleased working draft*. It is informational guidance only, not a controlling standard. Three areas are explicit **placeholders** in the source and are therefore thin here: the detailed FM architecture building blocks (source §6.3), the Assessment & Analysis guidance (a topic outline only — see ch05), and the Operations & Maintenance section (§9, a Phase-A–E outline only — see ch06). Lesson identifiers and mission references are reproduced as named in the draft and should be verified against the current NASA Lessons Learned database.

**Covers**: the FM discipline and vocabulary (fault/failure/anomaly, states, errors, containment, tolerance, CFE/root cause/TTC); the five FM strategies and five operational FM functions; the four redundancy approaches; the six FM process activities across NASA mission phases; risk posture and mission classification (NPR 8705.4); top-down FM requirements development; response-latency-vs-TTC design trades and the flight/ground/crew/automation split; FM verification vs. validation and the V&V planning, scenario-selection, and prioritization methods; the three-tier review structure and the seven dedicated FM milestone reviews; FM organizational structure, roles, and authority; and the mined NASA Lessons Learned.

**Does not cover in depth**: detailed FDIR algorithms, estimator/observer design, or specific diagnostic-engine implementations (the handbook is methodological, not algorithmic); the populated FM architecture catalog (a draft placeholder); quantitative reliability/PRA mechanics (see `nasa-pra`); hazard analysis and system-safety method detail (see `nasa-system-safety`, `mil-std-882`); the general SE lifecycle and review machinery FM rides on (see `nasa-npr-7123`, `nasa-se-handbook`); requirements-engineering fundamentals (see `requirements-writing`); and terrestrial / IT / network fault management beyond the single ISO analogy. **Domain**: NASA space missions (flight/ground/operations), with spacecraft examples throughout — non-space adopters must translate.

**Jurisdiction / licence**: US Government work — public domain (17 U.S.C. 105). Free to reproduce, transform, and redistribute, including commercially. Attribution to NASA is a courtesy, not an obligation; NASA does not endorse this pack.
