---
name: doe-o-413-3
description: "Knowledge base from the DOE Order on Program and Project Management for the Acquisition of Capital Assets (DOE O 413.3 series). Use for Critical Decisions CD-0–CD-4, performance baselines, acquisition strategy and IPTs, cost/schedule/EVMS/PARS controls, risk-informed governance, reviews, and contractor requirements. Built from O 413.3C (2026-08-05), which cancels O 413.3B Chg 7 (2023-06-21); does not replace site-specific procedures, nuclear safety rules detail, or full estimating standards."
---

<!-- argument-hint: [topic, CD, or chapter number] -->

# DOE Capital Asset Project Management (O 413.3 series)
**Source**: DOE O 413.3C (2026-08-05; cancels O 413.3B Chg 7) (US Government work, public domain) | **Chapters**: 6

## When to use
Reach for this pack when planning, governing, or reviewing DOE/NNSA capital asset projects under the 413.3 Order family — mission need through completion, Critical Decision gates, performance baselines, acquisition strategy and IPTs, EVMS/PARS reporting, risk-informed approvals, exemptions, and contractor requirements flow-down.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below.
- **With a topic** — ask about CD-0–CD-4, PB, EVMS, IPT, PARS, risk, exemptions, or CRD.
- **With a chapter** — ask for `ch01` through `ch06`.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### What the Order is
Risk-informed direction for acquiring capital assets so projects meet the original performance baseline and mission/ES&H/security performance unless a directed change intervenes — aligned with OMB capital-programming expectations.

### Critical Decision spine
CD-0 mission need → CD-1 alternative and cost range → CD-2 performance baseline → CD-3 execution/construction start → CD-4 operations/completion.

### Control triad after CD-2
| Control | Role |
|---------|------|
| Performance baseline | Commitment snapshot (scope/cost/schedule) |
| Change control | Authorized evolution of the baseline |
| EVMS + PARS | Performance measurement and Department visibility |

### Governance web
Line management owns outcomes; PSO/PMSO/PM/FPD/IPT and approval authorities form the decision system; CRD carries requirements to contractors; reviews provide independent signal.

## Chapter Index
| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-purpose-applicability-governance.md) | Purpose, Applicability, Governance | Scope, thresholds, OMB links, exemptions, cancellation |
| [ch02](chapters/ch02-critical-decisions-cd0-cd4.md) | Critical Decisions CD-0–CD-4 | Gate intents, products, authorities |
| [ch03](chapters/ch03-acquisition-planning-and-ipt.md) | Acquisition Planning and IPT | Strategy, PEP, IPT, front-end planning |
| [ch04](chapters/ch04-performance-baseline-cost-schedule.md) | Baseline, Cost, Schedule, EV | PB, estimates, EVMS, PARS |
| [ch05](chapters/ch05-risk-safety-and-exceptions.md) | Risk, Safety, Exceptions | Risk-informed decisions, S&S/nuclear interfaces, exemptions |
| [ch06](chapters/ch06-reviews-responsibilities-crd.md) | Reviews, Responsibilities, CRD | Oversight, roles, contractor flow-down, closeout |

## Topic Index
- **Acquisition strategy** → ch03
- **AoA / alternatives** → ch02, ch03
- **CD-0 mission need** → ch02
- **CD-1 cost range** → ch02
- **CD-2 performance baseline** → ch02, ch04
- **CD-3 construction/execution** → ch02
- **CD-4 completion/operations** → ch02, ch06
- **Change control** → ch04
- **Contingency / management reserve** → ch04, ch05
- **CRD / contractors** → ch01, ch06
- **EVMS** → ch04
- **Exemptions / equivalencies** → ch01, ch05
- **FPD / IPT** → ch03, ch06
- **PARS** → ch01, ch04
- **Project reviews** → ch06
- **Risk management** → ch05
- **TPC thresholds** → ch01, ch02

## Supporting Files
- [glossary.md](glossary.md) — capital-asset PM terms with chapter references
- [patterns.md](patterns.md) — implementation patterns (When/How/Trade-offs)
- [cheatsheet.md](cheatsheet.md) — CD table, control stack, tells and smells

---

## Scope & Limits
This pack covers the DOE Order on Program and Project Management for the Acquisition of Capital Assets using the **consolidated current Order PDF at build time: DOE O 413.3C (approved 2026-08-05)**, which cancels **DOE O 413.3B Chg 7 (2023-06-21)**. Extract metadata **source_pages=132**. Pack slug `doe-o-413-3` (renamed from `doe-413-3b` at v1.17.x; catalog carries the old slug as an alias) tracks the current Order series. It does **not** replace site implementing procedures, full text of companion G 413.3 guides, nuclear safety rule detail (e.g., 10 CFR 830), or GAO-grade estimating standards. In-PDF third-party copyright check at build found no copyright notices. US Government public domain work. No source-material download link is published.
