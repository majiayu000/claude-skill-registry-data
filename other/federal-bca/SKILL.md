---
name: federal-bca
description: "Knowledge base from OMB Circular A-94 (revised 2023-11-09) on guidelines and discount rates for benefit-cost and cost-effectiveness analysis of federal programs. Use for BCA principles, benefit/cost measurement, discount-rate policy, uncertainty/sensitivity, distributional incidence, and decision reporting. Rescoped at build to A-94 only (Army CBA Guide unreachable). Does not replace A-11 budget preparation detail, agency-specific statutory BCA rules, or Army CEAC process templates."
---

<!-- argument-hint: [BCA, discount rate, uncertainty, incidence, CEA, or chapter number] -->

# OMB Circular A-94 — Federal Benefit-Cost Analysis Guidelines
**Source**: OMB Circular A-94, revised Nov. 9, 2023 (US Government work, public domain) | **Chapters**: 6

## When to use
Reach for this pack when designing or reviewing **federal benefit-cost or cost-effectiveness analyses**—especially discount-rate selection, baseline and opportunity-cost measurement, uncertainty/sensitivity, distributional incidence, and OMB-facing documentation quality for program or legislative decisions.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below.
- **With a topic** — ask about NPV, real vs nominal rates, opportunity cost, sensitivity, incidence, or CEA vs BCA.
- **With a chapter** — ask for `ch01` through `ch06`.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### Why A-94 exists
Promote social welfare via well-informed federal decisions. Provides general BCA/CEA guidance and **specific discount-rate policy** for time-distributed benefits and costs. Revised 2023; rescinds 1992 A-94.

### Mandatory vs suggested
| Context | Force |
|---------|-------|
| Analyses to OMB under A-11 / A-19 / 1992 Presidential Memo estimates | Must follow |
| Internal Executive Branch planning | Suggested |
| Law / EO / other circulars prescribe methods | Those control |

### Analysis spine
1. Decision question + alternatives + baseline  
2. Identify/measure social benefits and costs (opportunity cost; transfers separated)  
3. Align inflation basis  
4. Discount with A-94 class-appropriate real/nominal rates  
5. Characterize uncertainty + sensitivity  
6. Report distributional incidence  
7. Document transparently for decision makers/OMB  

### BCA vs CEA
- **BCA**: Monetize benefits and costs → discounted net benefits / NPV  
- **CEA**: When benefits fixed or not monetized → compare costs for effect (still discount correctly)

### Pack scope note
Built as **A-94 only** after P7-PRE-2 dual-document gate: Army Cost Benefit Analysis Guide could not be retrieved (ASAFM host 403 from this environment). Do not expect Army CEAC step templates here.

## Chapter Index
| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-purpose-scope-and-principles.md) | Purpose, Scope, Principles | Goal, authority, mandatory use, BCA/CEA elements |
| [ch02](chapters/ch02-identifying-measuring-benefits-costs.md) | Benefits and Costs | Baseline, opportunity cost, inflation consistency |
| [ch03](chapters/ch03-discounting-and-time.md) | Discount Rate Policy | Real/nominal rates, analysis classes, NPV |
| [ch04](chapters/ch04-uncertainty-and-sensitivity.md) | Uncertainty | Expected values, sensitivity, explicit risk adjustments |
| [ch05](chapters/ch05-distributional-effects-and-incidence.md) | Distributional Effects | Groups, weights, economic incidence |
| [ch06](chapters/ch06-reporting-and-decision-use.md) | Reporting and Decision Use | OMB-grade documentation, limitations |

## Topic Index
- **Baseline / with-without** → ch02
- **BCA vs CEA** → ch01, ch02
- **Decision Analysis** → ch04, ch06
- **Discount rates (real/nominal)** → ch03
- **Distributional weights** → ch05
- **Economic incidence** → ch05
- **Expected value** → ch04
- **Inflation treatment** → ch02, ch03
- **Lease-purchase / asset sales rates** → ch03
- **Net present value (NPV)** → ch03, ch06
- **OMB A-11 / A-19 submissions** → ch01, ch06
- **Opportunity cost** → ch02
- **Opportunity cost / benefit identification** → ch01, ch02, ch06
- **Sensitivity analysis** → ch04
- **Social vs budget cost** → ch02
- **Transfers** → ch02, ch05
- **Uncertainty adjustments** → ch04

## Supporting Files
- [glossary.md](glossary.md) — BCA/discounting terms
- [patterns.md](patterns.md) — implementation patterns with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — decision rules, maps, tells & smells

---

## Scope & Limits
This pack covers **OMB Circular A-94, revised November 9, 2023** (28 pages per extraction metadata) as synthesized reference notes on federal BCA/CEA guidelines and discount-rate policy.

**Rescope (P7-PRE-2):** Planned dual source was A-94 + US Army Cost Benefit Analysis Guide. The Army PDF was not retrievable (ASAFM 403 / Wayback 503 from the build environment). Per hard gate rules, the pack was rescoped to the surviving in-source-clean document (A-94) rather than generating Army content without evidence. Re-expand if the Army guide becomes fetchable.

It does **not** cover: full OMB Circular A-11 budget formulation; agency-specific statutory BCA regimes; private-sector CFA/WACC practice as a substitute for A-94; or Army CEAC process templates. US Government public domain work. No source-material download link is published.
