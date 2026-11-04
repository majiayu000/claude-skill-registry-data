---
name: sd-22-dmsms
description: "Knowledge base from the SD-22 DMSMS Guidebook (DSPO, SD-22, 06-JAN-2026 (cover dated December 2025)). Use for managing Diminishing Manufacturing Sources and Material Shortages (DMSMS) and obsolescence across a long-lived system's life cycle: the five-step process (Prepare, Identify, Assess, Analyze, Implement); standing up a DMSMS Management Team (DMT) and Management Plan (DMP); FMS communication and FMS considerations on partner configurations; risk-based monitoring and surveillance (predictive tools, vendor surveys, GIDEP/DLA PDNs, critical-materials analysis); health assessments and resolution timing; costing and selecting resolutions (life-of-need buys, substitutes, redesign, technology refreshment) by AoA/BCA, including system security engineering as an Analyze consideration; and budgeting/executing resolutions through modification funding and related accounts. Defense-sustainment / DoD-acquisition framing throughout. Does NOT teach general systems engineering, parts-management standards, or contracting law in depth, and does not reproduce DoD policy text or the source's tables and figures."
---

<!-- argument-hint: [DMSMS step, DMT/DMP, monitoring/PDN, health assessment, resolution option/LON buy, FMS note, obsolescence relation, chapter number] -->

# SD-22 DMSMS (06-JAN-2026)

**Source**: Defense Standardization Program Office (DSPO), US Government work, public domain (17 U.S.C. 105); Distribution A from ASSIST metadata; no printed DOPSR case | **Chapters**: 8 | See `LICENSE`

## When to use

Use this skill to manage obsolescence and supply loss on a system that must stay supportable for decades while commercial technology turns over in years. It covers the SD-22, 06-JAN-2026 discipline: set up a DMSMS program, decide what to watch, judge when an issue threatens cost/schedule/readiness, choose a durable resolution, fund and field it, and handle FMS partner configurations when DoD sells or supports them.

**Prerequisites:** none. Plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill

- **Without arguments**  -  load the five-step spine, DMT/DMP infrastructure, monitoring model, and resolution logic below.
- **With a topic**  -  ask about a step (Prepare/Identify/Assess/Analyze/Implement), FMS practice, a monitoring concept (predictive tools, PDN, vendor survey, critical materials), a resolution family (life-of-need buy, substitute, redesign, technology refreshment), or an artifact (DMT, DMP, health assessment).
- **With a chapter**  -  `ch03` (Prepare/DMT/DMP/FMS communication), `ch04` (Identify/monitoring/BOM), `ch05` (Assess/health assessment), `ch06` (Analyze/BCA/security consideration), `ch07` (Implement/funding/roadmaps), `ch08` (obsolescence relationship).

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

> **State versus event.** Obsolescence is a context-dependent state. A DMSMS issue is the event where supply cannot meet demand. Most DMSMS problems grow from obsolescence, but not all, and not every obsolete item is a DMSMS problem.

## Core Frameworks & Mental Models

### What DMSMS is

DMSMS is the loss or impending loss of manufacturers and suppliers of the items, materials, and software a system depends on. SD-22 frames management as risk-based, multidisciplinary, and life-cycle-long. Electronics, MaSME items, and software are all in scope.

**Two mechanisms.** First-order obsolescence comes from market or regulatory cuts to buy/license/support paths. Lower-order (derived) obsolescence is functional loss the program's own changes create.

### The five-step process

1. **Prepare**  -  foundations, DMT, DMP, operations funding, contracts, workforce, FMS communication.
2. **Identify**  -  monitoring and surveillance into an issue list.
3. **Assess**  -  whether, when, and at what level to resolve.
4. **Analyze**  -  options, costs, BCA/AoA, security-engineering screen, preferred path.
5. **Implement**  -  fund, field, close; align with mods and roadmaps.

This edition does not name a Strategize step.

### FMS in this edition

Security-cooperation sales add communication paths in Prepare and step-level notes in Identify, Analyze, and Implement so partner configurations are not surprises.

## Chapter Index

| File | Job |
|---|---|
| [ch01-sd-22-dmsms-introduction.md](chapters/ch01-sd-22-dmsms-introduction.md) | Scope, mechanisms, five-step overview |
| [ch02-sd-22-dmsms-policy-and-lifecycle.md](chapters/ch02-sd-22-dmsms-policy-and-lifecycle.md) | Policy and life-cycle guidance |
| [ch03-sd-22-dmsms-prepare.md](chapters/ch03-sd-22-dmsms-prepare.md) | DMT, DMP, contracts, FMS communication |
| [ch04-sd-22-dmsms-identify.md](chapters/ch04-sd-22-dmsms-identify.md) | Monitoring, BOM method, FMS identify |
| [ch05-sd-22-dmsms-assess.md](chapters/ch05-sd-22-dmsms-assess.md) | Need, timing, level, health assessment |
| [ch06-sd-22-dmsms-analyze.md](chapters/ch06-sd-22-dmsms-analyze.md) | Options, BCA/AoA, security consideration |
| [ch07-sd-22-dmsms-implement.md](chapters/ch07-sd-22-dmsms-implement.md) | Funding, execution, folded appendices |
| [ch08-sd-22-dmsms-obsolescence-relationship.md](chapters/ch08-sd-22-dmsms-obsolescence-relationship.md) | Obsolescence versus DMSMS |

## Topic Index

- Prepare / DMT / DMP / FMS communication: ch03
- Identify / monitoring / PDN / BOM: ch04
- Assess / health assessment / timing: ch05
- Analyze / BCA / AoA / security engineering: ch06
- Implement / funding / roadmaps / provisioning: ch07
- Obsolescence relationship: ch08
- Policy / SETR / ILA hooks: ch02
- Mechanisms / five-step overview: ch01

## Supporting Files

- `glossary.md`  -  Appendix P abbreviations and Appendix R definitions
- `cheatsheet.md`  -  quick rules for 06-JAN-2026
- `patterns.md`  -  When / How / Trade-offs patterns

## Scope & Limits

Does NOT teach general systems engineering, parts-management standards, or contracting law in depth, and does not reproduce DoD policy text or the source's tables and figures.
