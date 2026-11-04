---
name: nasa-schedule
description: "Knowledge base from the NASA Schedule Management Handbook (2024 edition, Revision 2). Use for program/project schedule management of aerospace and large engineering efforts: the five sub-functions (Planning, Development, Assessment & Analysis, Maintenance & Control, Documentation & Communication); the Integrated Master Schedule (IMS) and the WBS/OBS/CBS breakdown structures; the Schedule Management Plan (SMP) and Basis of Estimate (BoE); Critical Path Method, logic, durations, float and margin; tiered schedule assessment (Requirements/Health/Basis checks, the Shock Test) and the Dimensions of Schedule Reliability; Schedule Risk Analysis (SRA), Integrated Cost-Schedule Risk Analysis (ICSRA), Monte Carlo, correlation, merge bias, and the Joint Confidence Level (JCL); baselining, replan vs. rebaseline, EVM schedule metrics (SPI, BEI, CEI, HMI, Earned Schedule, CPLI), and status/progress/forecast reporting. This is NASA's scheduling doctrine grounded in NPR 7120.5 and the GAO Schedule Assessment Guide. Thin on the underlying mechanics of CPM, statistics, and EVM (it points to companion handbooks); aerospace/space-flight-centric; anchored to the 2024 second edition."
---

<!-- argument-hint: [topic, technique, or chapter number] -->

# NASA Schedule Management Handbook (2024 ed., Rev 2)
**Source**: NASA (US Government work, public domain) | **Pages**: ~409 | **Chapters**: 8

## When to use
Use this skill when you need to apply NASA's scheduling doctrine to aerospace or large engineering programs. It covers the full life cycle of an Integrated Master Schedule (IMS): planning the Schedule Management Plan (SMP), building the WBS/OBS/CBS breakdown structures, performing Critical Path Method analysis, managing margin vs. float, running Schedule Risk Analysis (SRA) and Integrated Cost-Schedule Risk Analysis (ICSRA) with Monte Carlo simulation, computing the Joint Confidence Level (JCL), and maintaining or controlling the baseline with EVM schedule metrics. The content is grounded in NPR 7120.5 and the GAO Schedule Assessment Guide and is anchored to the 2024 second edition of the NASA Schedule Management Handbook.

**Prerequisites:** none, plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below; they are the working toolkit, not a summary.
- **With a topic** — ask about the IMS, the SMP, WBS/OBS/CBS, critical path, margin vs. float, the Shock Test, schedule assessment, SRA/ICSRA, the JCL, replan vs. rebaseline, EVM schedule metrics, or schedule reporting; the relevant chapter is read on demand.
- **With a chapter** — ask for `ch04` (building the schedule) or `ch06` (Schedule Risk Analysis and the JCL).
- **Supporting files** — `glossary.md` (terms with chapter refs), `patterns.md` (18 named techniques with When/How/Trade-offs), `cheatsheet.md` (selection tables, decision rules, tells & smells).

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## Core Frameworks & Mental Models

### The five Schedule Management sub-functions
The handbook decomposes the discipline into five sub-functions that map one-to-one onto the
later chapters: **Planning** (decide *how* scheduling will run — the SMP), **Development**
(build the IMS from scope), **Assessment & Analysis** (validate credibility, then test
likelihood), **Maintenance & Control** (status, measure, correct), and **Documentation &
Communication** (record and disseminate). Detail and analytical rigor scale up across the
P/p life cycle and its Key Decision Points (KDPs), from early Formulation through
Implementation to Closeout.

### The IMS is "the schedule"
NASA's schedule requirements are written against the **Integrated Master Schedule** — one
time-phased, logically linked network of all approved work, built with the **Critical Path
Method**, detailed enough to expose the longest path. Everything else (Summary Schedule for
reporting, Analysis Schedule for risk modeling) derives from and traces back to it. The
entire data set lives in a configuration-controlled **Schedule Database**.

### Plan before you build (the SMP)
The **Schedule Management Plan** is the blueprint, written before the IMS is poured. It is a
guidance plan — not a scheduling cookbook — decomposed into four sub-plans (Development;
Assessment & Analysis; Maintenance & Control; Documentation & Communication). Front-loaded
into Phase A and matured by phase, it reaches a baseline at PDR. Five named planning best
practices anchor it: an SMP exists, scheduling methods are selected, tools are selected, the
Milestone Registry is defined, and Activity Attributes are defined.

### Four breakdown structures, one schedule
Scope is captured before dates. The **WBS** is the "what" (the traceability spine; every IMS
task carries a WBS code), the **OBS** is the "who," the **CBS/RBS** is the "how much," and the
**IMS** is the "when." A **control account** sits where one WBS element meets one
organization on the Responsibility Assignment Matrix, owned by a CAM — the atom where
budget, actuals, and earned value accumulate. The rationale behind every estimate is written
down in a **Basis of Estimate (BoE)**, a reproducibility dossier whose maturity is keyed to
life-cycle reviews.

### Build with logic; manage margin, not float
Construction proceeds as an ordered build: tool, codes, method, scope, detail, logic,
durations, critical path, margin, loading, time-phasing, risk mapping. **Finish-to-Start** is
the default relationship; hard constraints, leads/lags, and non-FS logic distort float and
must be justified. Durations are captured as owner-approved three-point ranges. **Float** is
calculated by the engine; **margin** is reasoned from quantified risk, placed where risks
occur, and held as a lien against Management Reserve/UFE. NASA manages margin over float
because margin ties directly to risk adequacy.

### Assess credibility before analyzing likelihood
**Schedule Assessment** validates that the IMS *can be believed*; **Schedule Analysis** then
asks *how likely* the dates are — and analysis is meaningless without assessment first. NASA's
umbrella quality measure is **reliability**, parsed into four near-orthogonal dimensions
(Comprehensiveness, Construction, Realism, Affordability) and traced through the **Schedule
Reliability Matrix** to tiered procedures: 1st/2nd Tier are assessment (Requirements, Health,
Risk ID & Mapping; then Critical Path & Structural with the **Shock Test**, Basis, Resource
Integration); 3rd Tier is analysis (SRA/ICSRA). The Health Check's color codes are a roadmap
for investigation, not a grade.

### Put odds on the schedule (SRA → ICSRA → JCL)
A **Schedule Risk Analysis** runs Monte Carlo over the IMS to convert a deterministic date
into a probability statement. Distinguish **uncertainty** (applied every iteration, no
likelihood gate) from discrete **risk** (Bernoulli likelihood × impact distribution). Assess
**correlation** always (default 0.3). An **ICSRA** adds a cost model — built via TD/TI
hammocks — to produce the **Joint Confidence Level**: the probability of meeting both cost and
schedule targets, taken at the equal-probability knee of the frontier curve. Read the
S-curve's shape, and guard against double counting, hard constraints, and non-zeroed margin.

### Keep the baseline honest; report from one database
**Maintenance** keeps the current schedule accurate; **Control** measures performance against
pre-set thresholds and dispositions variances through **Watch / Retain / Replan / Rebaseline**.
A replan is internal (PM authority within the MA); a rebaseline changes the external ABC.
Measure with a corroborating suite of deterministic (SV, BEI, CEI, HMI, SPI, Earned Schedule,
CPLI) and stochastic metrics — no single needle tells the truth. All reporting comes from one
integrated Schedule Database, classified as **Status / Progress / Forecast**, traced to the
IMS, archived per records-retention rules.

---

## Chapter Index

| # | Title | Key content |
|---|---|---|
| [ch01](chapters/ch01-nasa-schedule-foundations.md) | Foundations: Purpose, Life Cycle, Requirements & Best Practices | Schedule Management as a PP&C function; life-cycle/KDPs; IMS as the schedule; five sub-functions; SMP; SRA/ICSRA/JCL; roles; SCoPe |
| [ch02](chapters/ch02-nasa-schedule-management-planning.md) | Schedule Management Planning | The SMP and its four sub-plans; SM.P.1–5 best practices; CPM and rolling wave; Milestone Registry; Activity Attributes; requirements sources; tool categories |
| [ch03](chapters/ch03-nasa-schedule-development-scope-and-boe.md) | Schedule Development I: Scope, WBS/IMP/OBS/CBS, Basis of Estimate | Scope-first; the four breakdown structures; control accounts and the RAM; IMP; funding vs. budget; the Schedule BoE and its maturity |
| [ch04](chapters/ch04-nasa-schedule-development-build-and-outputs.md) | Schedule Development II: Logic, Durations, Critical Path, Margin & Outputs | The ordered build; CPM and SERs; FS default and constraints; three-point durations; critical/driving paths; margin vs. float; loading; the five schedule outputs |
| [ch05](chapters/ch05-nasa-schedule-assessment.md) | Schedule Assessment and Health Checks | Reliability dimensions; the Schedule Reliability Matrix; tiered procedures; Requirements/Health/Basis checks; the Shock Test; BoE as engine of change; construction defects |
| [ch06](chapters/ch06-nasa-schedule-risk-analysis.md) | Schedule Risk Analysis (SRA & ICSRA) | Monte Carlo; uncertainty vs. risk; risk modeling; correlation; merge bias; cost hammocks; the JCL scatterplot; sensitivity/criticality/cruciality; the seven applications |
| [ch07](chapters/ch07-nasa-schedule-maintenance-and-control.md) | Schedule Maintenance and Control | Five-procedure loop; baselining; MA/ABC/PMB; CCB/BCR; deterministic and stochastic metrics; replan vs. rebaseline; margin management; mandated thresholds |
| [ch08](chapters/ch08-nasa-schedule-documentation-and-communication.md) | Schedule Documentation and Communication | CM/DM backbone; single integrated database; status/progress/forecast taxonomy; report catalog; contractor/partner reporting; archives, retention, lessons learned |

## Topic Index

- **Schedule Management sub-functions** → ch01, ch02
- **Integrated Master Schedule** → ch01, ch03, ch04
- **Schedule Database** → ch03, ch04, ch08
- **Life cycle and KDP** → ch01, ch07
- **Schedule Management Plan** → ch02, ch01
- **Milestone Registry** → ch02
- **Activity Attributes** → ch02, ch04
- **Critical Path Method** → ch02, ch04
- **Rolling wave planning** → ch02, ch04
- **Work Breakdown Structure** → ch03, ch01
- **Organizational Breakdown Structure** → ch03
- **Cost Breakdown Structure** → ch03
- **Control account** → ch03
- **Responsibility Assignment Matrix** → ch03
- **Integrated Master Plan** → ch03
- **Funding versus budget** → ch03
- **Basis of Estimate** → ch03, ch05, ch08
- **Schedule Estimating Relationships** → ch04, ch06
- **Duration estimating** → ch04
- **Critical path** → ch04, ch05
- **Driving path** → ch04
- **Float** → ch04, ch07
- **Margin** → ch04, ch07
- **Hard constraints** → ch04, ch05
- **Resource loading** → ch04, ch06
- **Schedule outputs** → ch04
- **Schedule assessment** → ch05
- **Reliability dimensions** → ch05
- **Health check** → ch05
- **Shock test** → ch05
- **Basis check** → ch05
- **Vertical and horizontal traceability** → ch04, ch05
- **Schedule Risk Analysis** → ch06, ch01
- **Integrated Cost-Schedule Risk Analysis** → ch06, ch07
- **Monte Carlo** → ch06
- **Uncertainty versus risk** → ch06
- **Correlation** → ch06
- **Merge bias** → ch06
- **Joint Confidence Level** → ch06, ch01
- **Analysis schedule** → ch06, ch04
- **Sensitivity criticality cruciality** → ch06
- **Stochastic critical path** → ch06, ch07
- **Maintenance and control** → ch07
- **Agency Baseline Commitment** → ch07, ch06
- **Management Agreement** → ch07
- **Performance Measurement Baseline** → ch07, ch03
- **Baseline change request** → ch07
- **Replan versus rebaseline** → ch07
- **Schedule Performance Index** → ch07, ch04
- **Baseline Execution Index** → ch07, ch04
- **Earned Schedule** → ch07, ch04
- **Critical Path Length Index** → ch07
- **Integrated Baseline Review** → ch07
- **Documentation and communication** → ch08
- **Configuration management** → ch08
- **Status progress forecast reporting** → ch08
- **Schedule Repository** → ch08, ch04
- **Lessons learned** → ch08
- **Earned Value Management** → ch04, ch07

## Supporting Files
- [glossary.md](glossary.md) — key terms with chapter references, from Activity Attributes to Work Breakdown Structure
- [patterns.md](patterns.md) — 18 named techniques with When/How/Trade-offs, from "plan before you build" to "one database, many lenses"
- [cheatsheet.md](cheatsheet.md) — sub-function map, breakdown-structure and loading-method tables, SRA/JCL rules, the corrective-action decision, and tells & smells

---

## Scope & Limits
This skill covers the *NASA Schedule Management Handbook*, 2024 edition (Revision 2, effective
2024-03-15), a US Government public-domain work. It is NASA's **scheduling doctrine**: how to
plan, build, assess, analyze, control, and communicate an Integrated Master Schedule across the
program/project life cycle, grounded in NPR 7120.5 and the GAO Schedule Assessment Guide. It is
a *best-practice handbook*, not a textbook, so it deliberately points to companion references
for the underlying mechanics — CPM and network theory, the statistics behind Monte Carlo and
correlation, and the EVM apparatus (the NASA Cost Estimating Handbook, the Joint Cost, Schedule,
Risk, and Uncertainty Handbook, the NASA EVM System Description, the NASA Risk Management
Handbook, NDIA PASEG, and GAO-16-89G). It does **not** teach those disciplines from first
principles, nor does it cover the qualitative risk-decision framework (RIDM/CRM — see the
nasa-risk pack) or the quantitative reliability engine (see nasa-pra). Examples and
requirements are space-flight-centric (KDPs, launch dates, the $250M / $1B cost thresholds, the
Agency Baseline Commitment) and anchored to the 2024 second edition; do **not** rely on the
superseded 2010 edition (NASA/SP-2010-3403).
