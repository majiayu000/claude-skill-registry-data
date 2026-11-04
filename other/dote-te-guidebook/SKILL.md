---
name: dote-te-guidebook
description: "Knowledge base from the DoD Test & Evaluation Enterprise Guidebook (August 2022 edition 8.02) with DOT&E-facing enterprise emphasis. Use for T&E enterprise roles (DOT&E vs USD(R&E)), DT&E/OT&E/LFT&E, cybersecurity T&E, MOSA/automation/digital enablers, suitability/reliability growth, and TEMP/Strategy/STE planning. Distinct routing from dod-te-guidebook (same guidebook family, pathway-deep pack). Guidance only—defer to DoDI 5000.89 and Title 10 for binding requirements."
---

<!-- argument-hint: [DT&E, OT&E, LFT&E, cyber T&E, MOSA, reliability, TEMP/Strategy, DOT&E role, or chapter number] -->

# T&E Enterprise Guidebook (8.02) — DOT&E-Facing Enterprise View
**Source**: DoD T&E Enterprise Guidebook, August 2022, ed. 8.02 (US Government work, public domain; Distribution A) | **Chapters**: 8

## When to use
Reach for this pack when you need the **enterprise T&E operating system** with a **DOT&E-facing lens**: who owns OT/LFT independence vs DT infrastructure, how DT/OT/LFT and cyber fit together, how MOSA/automation/digital engineering change test tempo, how suitability/reliability growth gates OTRR, and how Strategy/TEMP/STE planning resources the body of evidence.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime. For pathway-by-pathway TEMP patterns, also load `dod-te-guidebook`.

## How to Use This Skill
- **Without arguments** — load the core frameworks below.
- **With a topic** — ask about DOT&E vs USD(R&E), DT/OT/LFT, cyber T&E, MOSA/digital enablers, suitability/reliability, or TEMP/STE.
- **With a chapter** — ask for `ch01` through `ch08`.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### Guidance, not policy
Implements/clarifies **DoDI 5000.89** across AAF pathways. On conflict, **policy and statute win**.

### Four communities, one evidence store
CT + DT&E + OT&E + LFT&E should be integrated, automated, and reused via shared repositories—without erasing independent OT/LFT judgments.

### OSD split
| Principal | Lean |
|-----------|------|
| USD(R&E) | DT&E policy/sufficiency, engineering, test infrastructure (TRMC) |
| DOT&E | OT&E/LFT&E independence, oversight-list approvals, SecDef/Congress reporting |

### Operational ladder + OTRR
Ops Demo -> EOA -> OA -> IOT&E -> FOT&E. OTRR checks R/M/S and safety manageability before operational events.

### Cross-cutting enterprise themes
- Cyber T&E across cooperative DT and adversarial OT (Focus Area/companion depth)
- MOSA + digital engineering + automation as tempo/enabler stack with VV&A
- Suitability/reliability growth as DT sufficiency + OTRR + OT outcomes
- Strategy/TEMP/test plans/STE resources as the executable spine

### Pack routing vs dod-te-guidebook
| Need | Pack |
|------|------|
| Pathway chapters (UCA/MTA/MCA/Software/DBS) deep dive | `dod-te-guidebook` |
| DOT&E-facing enterprise, cyber, MOSA/digital, suitability, Strategy/STE emphasis | `dote-te-guidebook` (this pack) |
| Same underlying August 2022 Enterprise Guidebook family (ed. 8.02) | both — not conflicting policies |

## Chapter Index
| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-te-enterprise-overview-and-roles.md) | Enterprise Overview and Roles | Structure, DOT&E/USD(R&E), oversight, pack routing |
| [ch02](chapters/ch02-developmental-te.md) | Developmental T&E | DT knowledge mission, sufficiency, CDT |
| [ch03](chapters/ch03-operational-te.md) | Operational T&E | Event ladder, OTRR, IOT&E, OTA |
| [ch04](chapters/ch04-live-fire-te.md) | Live Fire T&E | Survivability/lethality, FUSL, waiver limits |
| [ch05](chapters/ch05-cybersecurity-te.md) | Cybersecurity T&E | Lifecycle cyber, software pipeline, survivability |
| [ch06](chapters/ch06-mosa-automation-digital-te.md) | MOSA, Automation, Digital T&E | DE, VV&A, automation, MOSA testability |
| [ch07](chapters/ch07-suitability-reliability-growth.md) | Suitability and Reliability Growth | R/M/S, OTRR gates, logistics evidence |
| [ch08](chapters/ch08-temp-strategy-and-ste-planning.md) | Strategy, TEMP, STE Planning | Docs, data/IDSK, resources, approvals |

## Topic Index
- **Automation / sequential testing** → ch06, ch08
- **CDT / T&E WIPT / PM roles** → ch01, ch02
- **Cybersecurity T&E** → ch05
- **dod-te-guidebook relationship** → ch01, Scope & Limits
- **DOT&E authorities** → ch01, ch03, ch04
- **DT&E / sufficiency assessments** → ch02
- **FUSL / LFT&E waiver limits** → ch04
- **IOT&E / EOA / OA / FOT&E** → ch03
- **Logistics / supportability evidence** → ch07
- **MOSA and interface testability** → ch06
- **OTRR** → ch03, ch07
- **Reliability growth** → ch07
- **Shared data repositories** → ch01, ch02, ch08
- **STE / test resources** → ch08
- **T&E Oversight List** → ch01, ch08
- **TEMP / T&E Strategy** → ch08
- **USD(R&E) / TRMC** → ch01, ch02
- **Verification / Validation pairing with T&E** → ch02, ch06

## Supporting Files
- [glossary.md](glossary.md) — enterprise T&E terms
- [patterns.md](patterns.md) — implementation patterns with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — decision rules, maps, tells & smells

---

## Scope & Limits
This pack covers the **DoD Test & Evaluation Enterprise Guidebook, August 2022, edition 8.02** (DMI mirror of the public Distribution Statement A release; 165 pages per extraction metadata) as synthesized reference notes with a **DOT&E-facing enterprise emphasis** (roles, DT/OT/LFT, cyber, MOSA/digital enablers, suitability/reliability, Strategy/TEMP/STE).

**Relationship to `dod-te-guidebook`:** both packs derive from the same August 2022 Enterprise Guidebook family. `dod-te-guidebook` is the earlier OUSD(R&E)-framed pack with deeper **pathway-specific** chapters. This pack does **not** replace it; it cross-routes and fattens enterprise/DOT&E/cyber/suitability/strategy themes. Prefer loading both when pathway detail and enterprise oversight detail are needed together.

It does **not** cover: full text of DoDI 5000.89 or other 5000-series instructions; detailed STAT/DOE methodology; CUI/CAC-gated companion procedures; or Acquisition of Services pathway depth (under review in source). US Government public domain work (Distribution Statement A). No source-material download link is published.
