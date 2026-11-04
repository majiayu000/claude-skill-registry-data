---
name: gao-agile
description: "Knowledge base from the GAO Agile Assessment Guide (GAO-24-105506, 2023). Use for assessing and managing Agile software development in federal programs: the Agile Manifesto and framework family (Scrum, Kanban, XP, SAFe, DA, DSDM, Lean, DevOps); the three adoption perspectives (team dynamics, program operations, organization environment); requirements decomposition (epics, features, user stories, INVEST, MoSCoW, definition of done); Agile-aware federal contracting (FAR, modular contracting, SOO/PWS/SOW, product owner vs. COR); program monitoring and control (WBS, cost, schedule, EVM at the feature level); Agile metrics (velocity, lead/cycle time, CFD, burn charts); and the auditor's key-question bank. Oversight- and acquisition-oriented: it tells you how to *assess and govern* Agile programs, not how to code. Thin on hands-on engineering practice, deep cost/schedule checklists (see gao-cost, gao-schedule), and any non-US-federal context."
---

<!-- argument-hint: [Agile framework (Scrum/Kanban/SAFe), adoption challenge, user story / INVEST, definition of done, product owner, contracting (SOO/PWS/SOW, modular), WBS / EVM / velocity, metric (CFD, lead time), auditor question, chapter number] -->

# GAO Agile Assessment Guide (GAO-24-105506, 2023)
**Source**: US Government Accountability Office (GAO) — US Government work, public domain | **Chapters**: 9

## When to use
Use this skill when you need to assess, govern, or explain **Agile software development in a federal program**: choosing among Agile frameworks, diagnosing why an Agile transition is stalling, structuring requirements and a backlog, writing or judging an Agile-aware contract, applying cost/schedule/EVM discipline to iterative work, picking meaningful metrics, or running an audit against GAO best practices. It is GAO's oversight-and-acquisition companion to the agency SE handbooks and to the sibling cost, schedule, and technology-readiness guides.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below for the mental model: Agile vs. Waterfall, the three adoption perspectives, the five planning levels, and how oversight discipline maps onto Agile artifacts.
- **With a topic** — ask about a framework (Scrum, Kanban, SAFe), an adoption challenge, user stories / INVEST, a definition of done, the product owner role, contracting (SOO/PWS/SOW, modular contracting), WBS / EVM / velocity, a metric (CFD, lead/cycle time), or an auditor question.
- **With a chapter** — ask for `ch03` (adoption best practices), `ch05` (requirements), `ch06` (contracting), `ch07` (monitoring & EVM), `ch08` (metrics), `ch09` (auditor questions).

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### What the Guide is (and isn't)
A **best-practices guide**, not a how-to. It gives federal auditors and agencies criteria to assess Agile **adoption, execution, and control**, framing Agile mainly as a way to reduce technical, programmatic, schedule, and budget risk. It is non-prescriptive: it states *what* good looks like, not step-by-step instructions. Though focused on software, its best practices apply to any incremental development effort — hardware or services included.

### Agile vs. Waterfall (the structural contrast)
Agile interleaves requirements, design, development, and testing **concurrently** in small, time-boxed iterations; Waterfall runs them in **sequence**. "Agile" is an umbrella for a family of methods — Scrum, Kanban, XP, FDD, SAFe, DA, DSDM, LeSS, Scrum@Scale, Scrumban, Crystal, DevOps, Lean. Frameworks are guiding structures, not recipes: non-exclusive and combinable. The invariant test is alignment to the **Agile Manifesto** (2001) and its 12 principles, not allegiance to any one framework. Working software each iteration is the yardstick of progress.

### The fixed/variable dials
Waterfall **fixes requirements** and lets cost and schedule float; Agile **fixes cost and schedule** and lets requirements float per iteration. In government, scope is rarely fully flexible, so split "must have" from "nice to have," deliver must-haves first, and pursue a **minimum viable product** within constraints.

### The three adoption perspectives
Adoption is a change-management effort, not a tooling swap, across three nested rings:
- **Team dynamics & activities** — self-organizing, cross-functional, **stable** teams; a dedicated, empowered **product owner**; **user stories** (INVEST); **relative estimation**; **value-based prioritization** (MoSCoW); story mapping.
- **Program operations** — **continuous integration** and automation; code-quality methods and **technical debt** management; the repeatable cadence of **standups, demonstrations, retrospectives**; an architecture with an **architectural runway**; a **sustainable pace**.
- **Organization environment** — goal alignment; **cascading sponsorship** and Agile champions; trained sponsors; a culture of trust and transparency; Agile-aligned **incentives**; acquisition policy and contracts that match the cadence.

Adopt incrementally and prioritize practices **across** the three rings; if you omit a practice, record the risk.

### Five Agile planning levels & rolling wave
Vision → epic → release → iteration → user story — an inverted triangle that keeps detail traceable from strategy down to coded work. **Rolling wave planning** details near-term work and leaves later work coarse, bounded by the road map (Agile is not a license for boundless development).

### Requirements as relocated discipline
Agile compresses up-front specification but replaces it with sustained **elicitation, refinement, and management** (eight best practices). Requirements decompose progressively across governance layers, each with a matching artifact (road map, release plan, backlog). A two-tier completion gate — per-story **acceptance criteria** plus a universal **definition of done**, fronted by a **definition of ready** — defines start and finish. Non-functional requirements (security, privacy, Section 508 accessibility) need deliberate capture. Traceability replaces the Waterfall RTM with the road map and backlog.

### Agile-aware federal contracting
The **FAR** never names Agile but permits it (1.102-4(e): innovate where not prohibited). Three best practices: tailor planning and structure (encourage **modular contracting**; prefer **SOO/PWS** over SOW when the end state will evolve; let the goods-vs-services decision drive contract type); build oversight on Agile metrics, artifacts, and retrospectives (tailor the CDRL); and integrate the program office with developers. The **product owner** and **COR** must both be empowered government employees; the contractor must not perform inherently governmental functions.

### Monitoring & control mapped to Agile
Federal accountability does not bend to method. One product-oriented **WBS** built from Agile artifacts (epics → features → user stories) is the spine feeding cost, schedule, and **EVM**. **Keep monitoring at the epic/feature level**, where work is stable enough to baseline; let stories/tasks churn as quantifiable backup data. Earn value at the feature level by percent complete, crediting stories 0/100. A disciplined **baseline-change process** (with a freeze period) reconciles reprioritization with credible measurement — an unstable *program* baseline, not iteration flexibility, is what destroys EVM. Reconcile relative estimation (story points) with consistent sizing (function points, SLOC) for a defensible estimate.

### Metrics: outcome over output
Pick metrics early, tailored to framework and audience; make each quantifiable, meaningful, repeatable, actionable; trace goals down through road map → releases → backlog. Recurring instruments: **velocity** (team-internal only), **lead time**, **cycle time**, **cumulative flow diagram**, **burn up/burn down**. Use **counterbalanced pairs** so no single number can be gamed; tie metrics to team-based incentives and set thresholds.

### The auditor's instrument
The appendices pair **key questions** (what to ask) with **likely effects** (why it matters). Agree shared terminology first, gather documentation, learn the local method, then reason from each gap to its consequence. The **product owner**'s authority and availability is the most heavily probed risk. The framework catalog and the **ten Agile myths** equip the auditor with what "normal" looks like and ready counters to common objections.

---

## Chapter Index

| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-gao-agile-introduction-background.md) | Introduction & Background | Agile vs. Waterfall; the Agile Manifesto & 12 principles; the framework family (Table 1: Scrum, Kanban, XP, FDD, DA, DSDM, LeSS, SAFe, Scrum@Scale, Scrumban, Crystal, DevOps, Lean); Agile as risk reduction; why GAO wrote the guide |
| [ch02](chapters/ch02-gao-agile-adoption-challenges-federal-response.md) | Federal Adoption Challenges & Response | The 14 challenges in four areas (commitment/collaboration, preparation, execution, evaluation); cultural root cause; Table 3 federal responses (18F, USDS, TechFAR, FITARA, DODIs); supplement Agile with internal controls |
| [ch03](chapters/ch03-gao-agile-adoption-best-practices.md) | Adoption Best Practices | The three perspectives; self-organizing/cross-functional/stable teams; product owner; user stories (INVEST), relative & affinity estimation, MoSCoW, story mapping; CI, technical debt, standups/demos/retrospectives; architectural runway; sustainable pace; sponsorship, champions, incentives |
| [ch04](chapters/ch04-gao-agile-execution-and-controls.md) | Execution & Controls (overview) | Five planning levels; rolling wave; fixed-vs-variable constraint model; release vs. deployment; cadence/time-boxing; estimating as commitment; MVP; the three program-management areas |
| [ch05](chapters/ch05-gao-agile-requirements-development-management.md) | Requirements Development & Management | The eight requirements best practices; progressive decomposition across governance layers; epics/features/user stories; non-functional requirements; definition of ready/acceptance/done; value-based backlog; spike; MVP; traceability via road map & backlog |
| [ch06](chapters/ch06-gao-agile-federal-contracting-process.md) | Federal Contracting Process | FAR flexibility; modular contracting; SOO vs. PWS vs. SOW; goods vs. services; CDRL tailored to Agile metrics; retrospectives as oversight; reviews on cadence; product owner vs. COR vs. contracting officer; ATO; scope/change management |
| [ch07](chapters/ch07-gao-agile-program-monitoring-control.md) | Monitoring & Control (WBS, Cost, Schedule, EVM) | WBS as shared spine; monitor at epic/feature level; 12-step cost process; reliable-estimate characteristics; schedule best practices & IMS; EVM activities, control accounts, percent-complete/0-100, effort-based EAC; baseline change & freeze period; F-35 / FEMA cases |
| [ch08](chapters/ch08-gao-agile-metrics.md) | Agile Metrics | Six metrics best practices; metric attributes; product vs. team performance; cumulative flow diagram; lead/cycle time; velocity; burn up/down; counterbalanced metric pairs; automation & information radiators; thresholds & incentives |
| [ch09](chapters/ch09-gao-agile-assessment-reference-auditor-questions-frameworks.md) | Assessment Reference (Auditor Questions & Frameworks) | Question-and-effect pairing; product-owner empowerment as single point of failure; INVEST & estimation; backlog prioritization; repeatable processes; the framework catalog (DevOps/DevSecOps, DA, DSDM, XP, Kanban, Lean, SAFe, Scrum, Scrum@Scale, Scrumban); the ten Agile myths |

## Topic Index

- **Agile vs. Waterfall** → ch01, ch04
- **Agile Manifesto and 12 principles** → ch01, ch03
- **Agile frameworks (Scrum, Kanban, XP, SAFe, DA, DSDM, Lean, DevOps)** → ch01, ch09
- **Adoption challenges (federal)** → ch02
- **Internal controls / federal response (18F, USDS, TechFAR, FITARA)** → ch02
- **Three adoption perspectives** → ch03
- **Self-organizing and cross-functional teams** → ch03, ch09
- **Product owner** → ch03, ch05, ch06, ch09
- **User stories and INVEST** → ch03, ch09
- **Relative and affinity estimation** → ch03, ch07
- **Value-based prioritization and MoSCoW** → ch03, ch09
- **Story mapping** → ch03
- **Continuous integration** → ch03, ch05
- **Technical debt** → ch03, ch09
- **Standups, demonstrations, retrospectives** → ch03, ch06
- **Architectural runway** → ch03
- **Sustainable pace and velocity** → ch03, ch08
- **Sponsorship, champions, and incentives** → ch03, ch08
- **Five Agile planning levels** → ch04
- **Rolling wave planning** → ch04, ch07
- **Fixed vs. variable (constraint model)** → ch04
- **Release vs. deployment** → ch04
- **Cadence and time-boxing** → ch04, ch07
- **Minimum viable product (MVP)** → ch04, ch05
- **Eight requirements best practices** → ch05
- **Requirements decomposition and traceability** → ch05
- **Non-functional requirements** → ch05, ch03
- **Definition of ready / acceptance criteria / definition of done** → ch05
- **Prioritized backlog** → ch05, ch09
- **Spike** → ch05
- **Federal Acquisition Regulation (FAR)** → ch06
- **Modular contracting** → ch06
- **SOO vs. PWS vs. SOW** → ch06
- **Contracting officer's representative (COR)** → ch06, ch09
- **Authority to Operate (ATO)** → ch06
- **Reviews aligned to cadence** → ch06
- **Work breakdown structure (WBS)** → ch07
- **Cost estimating (12-step process)** → ch07
- **Schedule and integrated master schedule** → ch07
- **Earned value management (EVM)** → ch07, ch08
- **Baseline change and freeze period** → ch07
- **Epics, features, and control accounts** → ch07, ch05
- **Agile metrics (six best practices)** → ch08
- **Cumulative flow diagram (CFD)** → ch08
- **Lead time and cycle time** → ch08
- **Burn up and burn down charts** → ch08
- **Counterbalanced metric pairs** → ch08
- **Auditor key questions and effects** → ch09
- **The ten Agile myths** → ch09

## Supporting Files

- [glossary.md](glossary.md) — key Agile and oversight terms (epic, user story, INVEST, definition of done, velocity, WBS, EVM, modular contracting, SOO/PWS/SOW), alphabetical, with chapter references
- [patterns.md](patterns.md) — ten reusable patterns (incremental adoption, progressive requirements decomposition, the two-tier done gate, non-functional capture, estimation reconciliation, monitor-high, baseline protection, Agile-aware contracting, balanced metrics, paired-question auditing) with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — the three perspectives, planning levels, fixed/variable dials, document-selection and monitoring-level tables, metric pairs, tells & smells, and the ten myths

---

## Scope & Limits

**Covers**: GAO best practices for assessing and governing Agile in federal programs per GAO-24-105506 — Agile vs. Waterfall and the framework family; the three adoption perspectives and the federal adoption challenges; requirements development and management (the eight practices, decomposition, definition of done, traceability); Agile-aware federal contracting (FAR flexibility, modular contracting, SOO/PWS/SOW, role clarity); program monitoring and control (WBS, the 12-step cost process, scheduling, EVM at the feature level); Agile metrics; and the auditor's paired key-questions/effects bank with the framework catalog and ten myths.

**Does not cover in depth**: hands-on software engineering or coding practice (the guide is about oversight, not development technique); the full cost-estimating and EVM checklists (it defers to the GAO Cost Estimating and Assessment Guide — see `gao-cost`) and the detailed scheduling checklists (the GAO Schedule Assessment Guide — see `gao-schedule`); technology-maturity assessment (see `gao-tra`); the broader systems-engineering life cycle (see `sebok`, `dau-se-guidebook`, `nasa-se-handbook`); and any specific Agile framework's full internal mechanics (it summarizes Scrum, SAFe, etc., rather than teaching them).

**Source version**: GAO-24-105506, published November 2023 (revised 15 December 2023); an update to the GAO-20-590G exposure draft. GAO intends to refresh it periodically, so verify against the latest edition for current guidance.

**Jurisdiction**: US Government public domain work (GAO). The best practices are cross-government and adoptable by any organization, but the contracting and oversight material is framed around US federal law (FAR, FITARA, OMB guidance) and is guidance, not binding requirement, outside an agency that adopts it.
