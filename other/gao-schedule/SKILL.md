---
name: gao-schedule
description: "Knowledge base from the GAO Schedule Assessment Guide (GAO-16-89G, 2015). Use for building, assessing, or auditing a program's integrated master schedule (IMS): the ten best practices of a reliable schedule (capture, sequence, resource, duration, traceability, valid critical path, reasonable total float, schedule risk analysis, updating, baseline), the four characteristics (comprehensive, well-constructed, credible, controlled), critical path method arithmetic (forward/backward pass, total float), schedule risk analysis (Monte Carlo, contingency), statusing and baseline control, and the Appendix II audit triad. Scheduling/time-management oriented: it is the authority on schedule reliability, but it is NOT a cost-estimating guide, a full SE process model, an agile guide, or a risk-management framework — see sibling packs (gao-cost, dau-se-guidebook, nasa-schedule, nasa-risk) for those."
---

<!-- argument-hint: [best practice number, critical path, total float, schedule risk analysis (SRA), resource loading, duration, traceability, baseline, statusing, status date, forward/backward pass, EVM, four characteristics, audit, chapter number] -->

# GAO Schedule Assessment Guide (GAO-16-89G, 2015)
**Source**: US Government Accountability Office (GAO) — US Government work, public domain | **Chapters**: 8

## When to use
Use this skill when you need to build, explain, assess, or critique a program's **integrated master schedule (IMS)** and judge whether its forecast dates can be trusted: applying or auditing the ten best practices, computing or interpreting a critical path and total float, running or reviewing a schedule risk analysis, resource-loading and setting realistic durations, statusing against a controlled baseline, or interrogating someone else's schedule with GAO's audit questions. This is GAO's cross-government best-practice authority on **schedule reliability** — the time-domain companion to its Cost Estimating and Assessment Guide and to the agency SE handbooks (NASA, DoD).

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below for an overview of the ten best practices, the four characteristics, CPM, and schedule risk analysis.
- **With a topic** — ask about a best practice, the critical path, total float, a schedule risk analysis, resource loading, durations, traceability, the baseline, statusing, the forward/backward pass, or EVM scheduling.
- **With a chapter** — ask for `ch02` (capture & sequence), `ch03` (resources & durations), `ch04` (traceability & critical path), `ch05` (float & risk analysis), `ch06` (updating, baseline & four characteristics), `ch07` (auditing), or `ch08` (EVM, CPM arithmetic & reference data).

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### The reliable schedule (the thesis)

A program's success rests on an **integrated master schedule (IMS)** — a single, dynamic network covering *all* effort (government, contractor, subcontractor, vendor, external) from program start to finish. The schedule is the operating instrument of program management: a route map, a progress yardstick, an early-warning system, the basis for a time-phased budget, and the foundation for cost/schedule/scope tradeoffs. The through-line of the whole guide: **the reliability of the schedule determines the credibility of the dates the program forecasts** — every downstream decision inherits the schedule's reliability (or lack of it).

### The Ten Best Practices

GAO's central framework: ten practices "associated with a high-quality and reliable schedule," stated in **no particular order** and explicitly *not* a step-by-step build recipe.

1. **Capturing all activities** — every WBS element (all parties) appears as at least one activity.
2. **Sequencing all activities** — justified predecessor/successor logic so the network forecasts dates automatically.
3. **Assigning resources to all activities** — labor, material, equipment, facilities, travel loaded and checked for feasibility.
4. **Establishing the duration of all activities** — durations derived from effort/resources/productivity, not from a desired finish date.
5. **Verifying horizontal and vertical traceability** — logical hand-offs across activities; consistent dates/status/scope across schedule levels.
6. **Confirming the critical path is valid** — the path that truly drives the finish, recomputed each cycle.
7. **Ensuring reasonable total float** — float that is plausible, not a symptom of broken logic.
8. **Conducting a schedule risk analysis** — simulate duration uncertainty (Monte Carlo) to price the completion date and size contingency.
9. **Updating using actual progress and logic** — status the schedule to a real status date so the forecast stays true.
10. **Maintaining a baseline schedule** — a CM-controlled target the current schedule is measured against.

### The Four Characteristics (the ten practices roll up into four)

GAO's top-level synthesis — a reliable schedule is:

- **Comprehensive** — captures all activities, resources, durations (BP1, BP3, BP4).
- **Well-constructed** — sound sequencing, valid critical path, reasonable float (BP2, BP6, BP7).
- **Credible** — traceable and risk-informed (BP5, BP8).
- **Controlled** — statused and measured against a controlled baseline (BP9, BP10).

These four are the audit lens: *is everything in it? is the logic sound? does it trace and is it risk-informed? is it kept current and controlled?*

### Critical Path Method (CPM)

The schedule is a **calculable model**. The **forward pass** (`EF = ES + duration − 1`) and **backward pass** (`LS = LF − duration + 1`) deterministically yield early/late dates, **total float** (`TF = LS − ES`), and the **critical path** — the longest continuous chain that sets the earliest finish. **Total float** is both the measure of slack and a diagnostic: unreasonable float (large positive or any negative) usually means missing or invalid logic, not real room to maneuver. **Near-critical** activities sit just above critical-path float and can become critical with a small slip. When constraints, multiple calendars, out-of-sequence progress, or leveled resources distort float, trace the **driving (longest) path** back from the finish milestone instead of trusting the software-flagged path. "Critical" is precise — it means *drives the finish date*, never "important" or "long."

### Schedule Risk Analysis (SRA)

Durations are forecasts, not facts, so the program duration is uncertain — and summing deterministic durations runs **optimistic** because of **merge bias** (converging paths multiply, not average). An SRA feeds quantified risks and uncertainties into a **Monte Carlo** simulation to produce an **S-curve** of completion dates, from which the program picks a confidence-priced date, sizes **schedule contingency**, and ranks the risks driving the exposure. Inputs are three-point durations and risk drivers (combine both). Contingency is PM-owned reserve under change control — categorically **distinct from total float**.

### Statusing and the controlled baseline

A schedule earns trust only when it is continuously reconciled with reality and measured against a controlled commitment. **Statusing** loads actuals to a **status date** (the actuals/forecast boundary) and updates by *remaining duration*, not typed-in percent complete; out-of-sequence progress is handled with conservative **retained logic**. The **baseline** is the configuration-managed target, backed by a living **schedule basis document**; **performance is the variance** between baseline and current schedule — and that variance is only as valid as the schedule is reliable. Limit baseline changes to scope change or formal replanning; frequent **rebaselining** is a red flag.

---

## Chapter Index

| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-gao-schedule-introduction-reliable-schedule.md) | Introduction & the Reliable Schedule | Why schedules matter, the IMS as focal point, schedule reliability thesis, the ten best practices overview, CPM/total float/near-critical, planning vs. scheduling, the cyclic reliability process, rolling-wave planning |
| [ch02](chapters/ch02-gao-schedule-capturing-and-sequencing-activities.md) | Capturing & Sequencing Activities (BP 1–2) | WBS as cornerstone, capturing all parties' work, milestones vs. detail activities, F–S logic, forbidden logic types, constraints/lags/leads, path convergence, dangling logic |
| [ch03](chapters/ch03-gao-schedule-resources-and-durations.md) | Resources & Durations (BP 3–4) | Resource loading, effort vs. duration interdependence, BOE reconciliation, resource leveling within float, deriving durations from effort, calendars, inch-stones (QBD), durations sized to the reporting period |
| [ch04](chapters/ch04-gao-schedule-traceability-and-critical-path.md) | Traceability & Critical Path (BP 5–6) | Horizontal (hand-offs) and vertical (level-to-level) traceability, roll-up into the program schedule, validating the critical path each cycle, driving (longest) path, keeping the path clean, near/risk-critical paths |
| [ch05](chapters/ch05-gao-schedule-total-float-and-risk-analysis.md) | Total Float & Risk Analysis (BP 7–8) | Total/free/independent/interfering float, reasonable-float judgment, merge bias, Monte Carlo SRA & S-curve, three-point durations vs. risk drivers, contingency vs. float, remove-one-and-rerun prioritization |
| [ch06](chapters/ch06-gao-schedule-updating-baseline-four-characteristics.md) | Updating, Baseline & Four Characteristics (BP 9–10) | Statusing vs. revising, status date, remaining-duration updates, retained logic vs. progress override, baseline & basis document, BEI/trend analysis, recovery/acceleration techniques, the four-characteristics mapping |
| [ch07](chapters/ch07-gao-schedule-auditing-key-questions.md) | Auditing a Schedule (App. I–II) | GAO methodology/provenance, the Appendix II audit triad (Key Questions → Key Documentation → Likely Effects), coupling of practices, documentation as proof, constraints as logic-overrides to justify |
| [ch08](chapters/ch08-gao-schedule-evm-forward-backward-pass-reference-data.md) | EVM, CPM Arithmetic & Reference Data (App. III–IX) | EVM scheduling considerations & ANSI/EIA-748 mapping, forward/backward pass math, date-constraint names & effects, quantitative health measures (no tripwires), industry/agency comparisons, the 15 artifacts to request |

## Topic Index

- **As-built schedule / fragnet** → ch06
- **Audit triad (Key Questions / Documentation / Likely Effects)** → ch07, patterns, cheatsheet
- **Baseline / baseline schedule** → ch06, cheatsheet
- **Baseline Execution Index (BEI) / trend analysis** → ch06
- **Best practices (the ten)** → ch01, cheatsheet
- **Calendars** → ch03
- **Constraints (date) / lags / leads** → ch02, ch08, cheatsheet
- **Contingency (schedule reserve)** → ch05, cheatsheet
- **Critical path / critical path method (CPM)** → ch04, ch08, cheatsheet
- **Driving path (longest path)** → ch04, cheatsheet
- **Durations (establishing)** → ch03
- **Earned value management (EVM) scheduling** → ch08
- **Float (total / free / independent / interfering)** → ch05, cheatsheet
- **Forward / backward pass** → ch08, cheatsheet
- **Four characteristics (comprehensive / well-constructed / credible / controlled)** → ch06, ch01, cheatsheet
- **Horizontal traceability** → ch04
- **Integrated Master Schedule (IMS)** → ch01, ch02
- **Industry/agency comparisons (DCMA 14PA, NDIA PASEG, NASA, DHS)** → ch08
- **Level of effort (LOE)** → ch02, ch04
- **Merge bias** → ch05
- **Milestones** → ch02
- **Monte Carlo simulation** → ch05
- **Near-critical activities** → ch01, ch04
- **Out-of-sequence progress (retained logic vs. progress override)** → ch06
- **Path convergence** → ch02, ch05
- **Planning vs. scheduling** → ch01
- **Quantitative schedule health measures** → ch08
- **Rebaselining / replanning** → ch06
- **Recovery & acceleration (crashing, fast tracking)** → ch06
- **Resource loading / leveling** → ch03, cheatsheet
- **Rolling-wave planning** → ch01, ch03
- **Schedule basis document** → ch06
- **Schedule narrative** → ch06
- **Schedule risk analysis (SRA)** → ch05, cheatsheet
- **Sequencing / logic** → ch02, cheatsheet
- **Status date (data date)** → ch06, cheatsheet
- **Statusing vs. revising** → ch06
- **Tells & smells (unreliable schedule)** → cheatsheet, ch07
- **Total float (reasonable)** → ch05, cheatsheet
- **Vertical traceability** → ch04
- **Work breakdown structure (WBS)** → ch02, ch01

## Supporting Files

- [glossary.md](glossary.md) — key scheduling terms (IMS, CPM, total float, SRA, the four characteristics, status date, baseline, merge bias), alphabetical, with chapter references
- [patterns.md](patterns.md) — seven reusable patterns (capture from the WBS, sequence with sound logic, resource-load & set durations, validate the critical/driving path, run an SRA & size contingency, status & control the baseline, audit with the Appendix II triad) with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — the ten best practices table, four-characteristics mapping, CPM arithmetic, logic/constraint rules, statusing & SRA quick rules, tells & smells, quantitative health & industry comparisons

---

## Scope & Limits

**Covers**: GAO best practices for schedule reliability per GAO-16-89G — the integrated master schedule as the focal point of program management; the ten best practices (capturing, sequencing, resourcing, durations, traceability, valid critical path, reasonable total float, schedule risk analysis, updating, baseline maintenance); the four characteristics (comprehensive, well-constructed, credible, controlled); critical-path-method arithmetic (forward/backward pass, total float, the driving path); schedule risk analysis (Monte Carlo, merge bias, contingency); statusing and configuration-controlled baselines; EVM scheduling considerations; and the Appendix II audit instrument (Key Questions / Key Documentation / Likely Effects).

**Does not cover in depth**: cost estimating — the dollar side (see `gao-cost` / GAO-09-3SP, which this guide defers to for EVM and cost detail); the full systems-engineering process (see `dau-se-guidebook`, `nasa-se-handbook`, `nasa-npr-7123`); agile schedule assessment (see GAO's separate Agile Assessment Guide); risk management as a discipline (the guide consumes a risk register for the SRA but is not a risk-management framework — see `nasa-risk`); technology readiness (see `gao-tra`); and detailed operation of any specific scheduling tool (the guide is tool-agnostic and names tool behaviors only as cautions). The guide is also thin on portfolio/multi-program scheduling and on procurement/contracting mechanics beyond what the IMS must integrate.

**Jurisdiction**: US Government public domain work (GAO). The best practices are cross-government and adoptable by any organisation; they are guidance, not binding requirements outside an agency that adopts them.
