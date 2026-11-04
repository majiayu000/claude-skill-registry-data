---
name: mil-std-881f
description: "Knowledge base from MIL-STD-881F (13 May 2022), DoD Standard Practice for Work Breakdown Structures for Defense Materiel Items. Use for Program/Contract/Subcontract WBS construction, 100% rule and dictionary discipline, commodity appendices A–J, Common Elements (K), sustainment CES reporting (L), Government ST&E (M), and RFP/post-award implementation. Technical planning & WBS and PM/measurement focus—not a cost manual substitute for CAPE policy."
---

<!-- argument-hint: [WBS, Program WBS, Contract WBS, 100% rule, dictionary, appendix A-J, common elements, sustainment, CSDR, IMP/IMS, software placement, or chapter number] -->

# MIL-STD-881F — Work Breakdown Structures for Defense Materiel Items
**Source**: MIL-STD-881F, 13 May 2022 (US DoD; public domain; Distribution Statement A per ASSIST QuickSearch Dist Stmt for Rev F) | **Chapters**: 7

## When to use
Use this pack when building or reviewing a **defense Program or Contract WBS**: choosing commodity appendices, applying the 100% rule, writing WBS dictionaries, placing software/cyber/SoS work, hanging Appendix K common elements, aligning IMP/IMS and cost reporting identifiers, implementing post-award WBS control, or applying Appendix L sustainment CES / Appendix M Government ST&E structures under 881F.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime. Pair with program cost/CSDR guidance and service tailoring memos for reporting specifics.

## How to Use This Skill
- **Without arguments** — load the core frameworks below.
- **With a topic** — ask about Program vs Contract WBS, 100% rule, dictionaries, a commodity appendix, common elements, sustainment L, or software placement.
- **With a chapter** — ask for `ch01` through `ch07`.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### Three-layer WBS spine
1. **Program WBS** (Government) — whole materiel item / PE  
2. **Contract WBS** — performer extension of program parents  
3. **Subcontract WBS** — lower-tier extension with same product parents  

### 100% rule
Decomposition children must represent 100% of parent work/resources. Never promote a child to sibling of its former parent for 'visibility'.

### Commodity + commons pattern
| Layer | Source |
|-------|--------|
| Product taxonomy | Appendices A–J |
| Enabling commons | Appendix K (A–J only) |
| Sustainment CES reporting | Appendix L |
| Government ST&E | Appendix M |

### Dictionary discipline
Every managed element needs definition, inclusions, exclusions—this is interface control for cost, schedule, and engineering.

### Software dual path
- Embedded on weapon equipment → prefer equipment parent (elevate only if unpartitionable)  
- IS/Defense Business Systems → Appendix J  

### Pre-award → post-award flow
Program WBS + dictionary → RFP extension requirements → Contract WBS CM → reporting levels ≤ definition depth → L/M where applicable.

## Chapter Index
| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-wbs-principles-and-definitions.md) | WBS Principles and Definitions | Purpose, PE/materiel item, 100% rule, dictionary, layers |
| [ch02](chapters/ch02-program-wbs-roles-and-preaward.md) | Program WBS, Roles, Pre-Award | Government construction, RFP, pitfalls |
| [ch03](chapters/ch03-contract-wbs-and-programmatic-issues.md) | Contract WBS and Programmatic Issues | Extension, SoS, cyber, software, IMP/IMS |
| [ch04](chapters/ch04-commodity-wbs-air-missile-sea-space.md) | Commodity Templates A–F | Aircraft, electronics, missile, strategic, sea, space |
| [ch05](chapters/ch05-commodity-wbs-ground-umms-launch-is.md) | Commodity Templates G–J | Ground, unmanned maritime, launch, IS/DBS |
| [ch06](chapters/ch06-common-elements-appendix-k.md) | Common Elements (K) | SE/PM, ST&E, training, data, SE, facilities, spares |
| [ch07](chapters/ch07-numbering-reporting-sustainment.md) | Implementation, Reporting, Sustainment | Numbering, CSDR, Appendix L CES, Appendix M |

## Topic Index
- **100% rule / parent-child integrity** → ch01, ch03
- **Aircraft WBS (Appendix A)** → ch04
- **CAPE Sustainment CES / Appendix L** → ch07
- **Common Elements / Appendix K** → ch06
- **Contract WBS extension** → ch03, ch07
- **CSDR / reporting levels** → ch07
- **Cybersecurity placement** → ch03
- **Dictionary** → ch01, ch02
- **Electronics / avionics / generic (B)** → ch04
- **Government ST&E / Appendix M** → ch07
- **Ground vehicle (G)** → ch05
- **IMP / IMS linkage** → ch03
- **Information Systems / DBS (J)** → ch05, ch03
- **Launch vehicle (I)** → ch05
- **Missile / ordnance (C) / strategic (D)** → ch04
- **PM / measurement / EVMS mapping** → ch07
- **Program Element / defense materiel item** → ch01
- **Program WBS / pre-award / RFP** → ch02
- **Sea systems (E)** → ch04
- **SE/PM / SEIT/PM** → ch06
- **Software placement (embedded vs IS)** → ch03, ch05
- **Space systems (F)** → ch04
- **Subcontract WBS** → ch03
- **System of Systems / Family of Systems** → ch03
- **Technical planning & WBS** → ch01, ch02, ch07
- **Training / data / support equipment elements** → ch06
- **Unmanned maritime (H)** → ch05

## Supporting Files
- [glossary.md](glossary.md) — core 881F WBS terms with chapter refs
- [patterns.md](patterns.md) — eight build/review patterns with trade-offs
- [cheatsheet.md](cheatsheet.md) — appendix picker, checklists, smells

---

## Scope & Limits
- Covers MIL-STD-881F WBS standard practice only (13 May 2022 text used at build).
- Does not replace CAPE CSDR manuals, service-unique WBS memos, or contract clauses.
- Synthesized reference notes; not a substitute for the official ASSIST publication for contractual citation.
- No source PDF or full-text redistribution in this pack.
