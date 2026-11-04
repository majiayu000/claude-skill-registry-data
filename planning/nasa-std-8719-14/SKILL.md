---
name: nasa-std-8719-14
description: "Knowledge base from NASA-STD-8719.14C (Process for Limiting Orbital Debris). Use for orbital-debris assessment planning, mission-related debris limits, explosion/passivation and collision risk, postmission disposal options, reentry casualty risk, and ODAR/EOMP governance. Covers STD-8719.14C (Approved 2021-11-05) synthesized notes only; does not replace NPR 8715.6 delivery timing, NASA-HDBK-8719.14 environment/modeling depth, or program-specific OSMA waivers."
---

<!-- argument-hint: [topic, technical area, or chapter number] -->

# Process for Limiting Orbital Debris (NASA-STD-8719.14C)
**Source**: NASA-STD-8719.14C (Approved 2021-11-05) (US Government work, public domain) | **Chapters**: 7

## When to use
Reach for this pack when planning or reviewing NASA (or NASA-sponsored) orbital-debris assessments — applicability and NPR 8715.6 framing, assessment overview and tools, debris released in normal operations, explosions/breakups and collisions, postmission disposal of space structures, reentry surviving debris, or ODAR/EOMP content and special-mission classes.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below.
- **With a topic** — ask about ODAR, EOMP, 25-year LEO lifetime, GEO disposal, passivation, DAS/ORSAT, or reentry casualty risk.
- **With a chapter** — ask for `ch01` through `ch07`.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### NPR + standard pair
- **NPR 8715.6**: When assessments and reports are required and delivered.
- **NASA-STD-8719.14C**: Technical shalls and assessment methods for those reports. Handbook 8719.14 is a reference companion — not ingested here.

### Six assessment issues (ODAR spine)
1. Debris released during normal operations.
2. Explosions and intentional breakups.
3. On-orbit collisions (large objects + small MMOD that can kill disposal).
4. Reliable postmission disposal of spacecraft and orbital stages.
5. Surviving reentry debris / human casualty risk.
6. Special classes (tethers, smallsats, large constellations, servicing, ADR).

### Technical-area template (every §4.x)
Definition → Requirements → Rationale → Methods to assess compliance → NASA mitigation summary.

### Disposal preference
Immediate removal (direct reentry or Earth escape) is the preferred 2019 ODMSP option. LEO default is “as short as practicable, ≤25 years.” Storage and long-term reentry are constrained alternatives, not a free graveyard.

### Evidence pair
- **ODAR**: design-time compliance case (Initial / PDR / CDR / Final).
- **EOMP**: living operations plan so mission use does not preclude safe passivation and disposal.

## Chapter Index
| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-scope-and-applicability.md) | Scope and Applicability | Purpose, Earth-orbit focus, NPR 8715.6 frame, shall language |
| [ch02](chapters/ch02-assessment-overview.md) | Assessment Overview | Six issues, DAS/ORSAT/ORDEM/MEM, ODAR vs EOMP cadence |
| [ch03](chapters/ch03-debris-released-normal-operations.md) | Debris Released in Normal Operations | 25-year LEO, 100 object-years, GEO debris band |
| [ch04](chapters/ch04-explosions-breakups-collisions.md) | Explosions, Breakups, and Collisions | 0.001 explosion / large-object collision; passivation; 0.01 small-MMOD |
| [ch05](chapters/ch05-postmission-disposal.md) | Postmission Disposal | Reentry, retrieval, storage, long-term reentry; 0.90 reliability |
| [ch06](chapters/ch06-reentry-surviving-debris.md) | Reentry Surviving Debris | 15 J threshold, 1:10,000 casualty, controlled-reentry geometry |
| [ch07](chapters/ch07-special-classes-odar-eomp.md) | Special Classes, ODAR, EOMP | ODMSP Objective 5, tethers/smallsats, report formats |

## Topic Index
- **25-year LEO lifetime** → ch03, ch05
- **Collisions (large / small MMOD)** → ch04
- **DAS / ORSAT / ORDEM / MEM** → ch02, ch06
- **Disposal** → ch05
- **EOMP** → ch02, ch07
- **Explosions / passivation** → ch04
- **GEO protection zone** → ch03, ch05
- **Maintenance (passivation, EOMP updates)** → ch04, ch07
- **Mission-related debris (MRD)** → ch03
- **NPR 8715.6 / OSMA** → ch01, ch07
- **ODAR** → ch02, ch07
- **Operations (normal-release debris)** → ch03
- **Orbital debris** → ch01, ch02
- **Postmission disposal reliability** → ch04, ch05
- **Reentry casualty / DCA** → ch06
- **Special classes / tethers / CubeSats** → ch07

## Supporting Files
- [glossary.md](glossary.md) — orbital-debris and assessment terms with chapter references
- [patterns.md](patterns.md) — implementation patterns (When/How/Trade-offs)
- [cheatsheet.md](cheatsheet.md) — requirement numbers, thresholds, tells and smells

---

## Scope & Limits
This pack covers **NASA-STD-8719.14C (Approved 2021-11-05)**, Process for Limiting Orbital Debris, as synthesized reference notes from the official NTSS PDF (77 pages per extraction metadata). It does **not** ingest NASA-HDBK-8719.14, replace NPR 8715.6 delivery tables or OSMA waiver process, reproduce DAS/ORSAT user manuals, or dump every figure/table. IADC, UN, SPD-3, and 2019 ODMSP are cited as consistency references, not licensed inserts. US Government public domain work. No source-material download link is published.
