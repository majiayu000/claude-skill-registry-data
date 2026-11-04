---
name: easa-rules
description: "Reconstructed reference notes on EASA acceptable means of compliance for airborne software and airborne electronic hardware, built from AMC 20-115D (ED Decision 2017/020/R, AMC-20 Amendment 14, consolidated in Amendment 23) and AMC 20-152A (ED Decision 2020/010/R, AMC-20 Amendment 19, consolidated in Amendment 23), read from the Easy Access Rules AMC-20 compilation (Amendment 23, June 2023) and pinned 2026-09-26. Use for EASA software means of compliance, EASA AEH means of compliance, AltMoC, ETSO software, and the joint software and hardware certification workflow. SCOPE LIMITS: the two AMC sections only; no FAA content (use faa-8110-49); no RTCA DO-178C or DO-254, EUROCAE ED-12C or ED-80, or supplement clause text (use avionics-signpost to name them); no Part-21 body; no bulk AMC-20; AMC 20-193 and AMC 20-189 are name-only; reflects Amendment 23 as consolidated in the June 2023 EAR, not a later AMC-20 amendment; synthesized reference notes, not legal advice and not the official AMC. LICENCE: per-document (EASA site reproduction-with-acknowledgement grant, qualified by ED Decision all-rights-reserved footers); pack-level commercial use is not granted."
---

<!-- argument-hint: [AMC 20-115D, AMC 20-152A, AltMoC, ETSO software, custom device, COTS, CBA, chapter number] -->

# EASA AMC 20-115D and AMC 20-152A
**Source**: European Union Aviation Safety Agency (EASA): AMC 20-115D (ED Decision 2017/020/R, AMC-20 Amendment 14) and AMC 20-152A (ED Decision 2020/010/R, AMC-20 Amendment 19), both consolidated in AMC-20 Amendment 23 (June 2023 Easy Access Rules compilation); pinned 2026-09-26. Adapted from the sibling prototype and re-checked against the 2026-10-13 EASA source pin | **Licence**: per-document, see LICENSE | **Chapters**: 7

## When to use

**Prerequisites:** airborne software or airborne electronic hardware vocabulary (DAL, life cycle processes, assurance); the question names EASA, not the FAA.

Use this skill for questions about the EASA means of compliance for airborne software and airborne electronic hardware: which AMC answers which question and how the decision instruments anchor them, where AMC 20-115D applies and what its replacement of AMC 20-115C changed, how the AMC frames software life cycle assurance without dumping the standard's objectives, where AMC 20-152A applies and what it adds beyond recognising ED-80/DO-254, and how the software and hardware sides meet in one certification workflow. The pack answers with the AMCs' own frameworks, cited by chapter and source row.

## How to Use This Skill

- **Without arguments**: read the Core Frameworks below for the means-of-compliance landscape, the two applicability models, and the added hardware objectives.
- **With a topic**: use the Topic Index to find the chapter, then ask directly (e.g. "does AMC 20-152A apply at DAL D", "what AltMoC requires").
- **With a chapter**: ch01 orientation (which AMC and which decision answer which question); ch02-ch04 AMC 20-115D scope, software assurance, and transition/GM material; ch05-ch06 AMC 20-152A scope and the added AEH objectives; ch07 the joint software and hardware workflow.

Supporting files: `glossary.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### Where the means of compliance lives
EASA publishes its acceptable means in the AMC-20 volume of Easy Access Rules (free to read), but the actual development standards it points at are paywalled industry documents. **AMC 20-115D recognises EUROCAE ED-12C/RTCA DO-178C plus the supplement set; AMC 20-152A recognises EUROCAE ED-80/RTCA DO-254.** Neither AMC reprints the standard; this pack restates what the AMCs themselves say and names the paywalled documents only (see avionics-signpost). The FAA AC twin exists: FAA AC 20-115D and AC 20-152A cover the same two standards from the US side (see faa-8110-49), and AMC 20-115D states its technical content is harmonised with the FAA AC. **AltMoC** is the AMC's own escape valve: compliance with the AMC is not mandatory, and an applicant may use an alternative means of compliance, but it must meet the relevant requirements, ensure an equivalent level of safety, and be approved by EASA on a product or ETSO article basis.

### AMC 20-115D applicability
AMC 20-115D applies to applicants, design approval holders, and developers of airborne systems and equipment whose software is installed on type-certified aircraft, engines, and propellers, or used in ETSO articles: product certification and ETSO authorisation both sit inside its domain. **Replacing AMC 20-115C (12 September 2013) moved the recognised basis to ED-12C/DO-178C and the supplement set**, and the replacement AMC adds two things its predecessor did not carry: guidance for reusing established ED-12B/DO-178B processes on new development under stated criteria, and guidance for transitioning software previously approved under earlier ED-12/DO-178 editions. Applicability stops at software; the hardware question belongs to AMC 20-152A.

### Software assurance as the AMC frames it
The AMC frames software development assurance as a set of **life cycle processes**: planning, development, verification, configuration management, quality assurance, and certification liaison. Its guidance takes a fixed form borrowed from the recognised standard: objectives for the processes, activities that provide a means of satisfying the objectives, and descriptions of the evidence showing satisfaction. The AMC does not restate the standard's objective tables, and neither does this pack (see ED-12C/DO-178C, not reproduced). What the AMC layer adds on top of the recognition is process guidance: when ED-12B/DO-178B processes may continue (no known process deficiencies, prior certified use at an equal or higher software level, EASA-accepted handling of new techniques and parameter data), and how modification and reuse of previously developed software is handled.

### AMC 20-152A applicability
AMC 20-152A applies to the same audience (applicants, design approval holders, developers) for airborne electronic hardware on type-certified aircraft, engines, and propellers, including developers of ETSO articles. It covers **AEH contributing to hardware DAL A, DAL B, or DAL C functions**; at DAL C only a limited set of its objectives applies, with any per-DAL restriction written into the objective text itself. **The use of this AMC is not required for AEH contributing to DAL D functions**, though its appendix clarifications remain available for showing DAL D hardware performs its intended function. The AMC recognises ED-80/DO-254 as the development assurance standard and goes further than recognition: it describes when to apply them and supplements them with additional guidance of its own. Single Event Effects are outside the AMC's scope (handled through certification review item practice; name-only here).

### Hardware objectives the AMC adds
Beyond recognising ED-80/DO-254, AMC 20-152A adds objectives-based guidance for the three hardware areas the standard does not develop: **custom devices, including the use of COTS intellectual property inside them; COTS devices; and circuit board assemblies (CBAs)**. Each area is organised the same way: background on the topic, then objectives the applicant satisfies by describing the process and activities used. The objectives are the AMC's own text, and this pack summarises them as original notes (ch06), never as transcribed tables.

---

## Chapter Index

| Ch | File | Sources (pages) | Coverage | Cluster |
|----|------|-----------------|----------|---------|
| 01 | [ch01-moc-map](chapters/ch01-moc-map.md) | S5 + S6 decision anchors; S1/S2 opening sections (EAR pp. 416-417, 497-498; cite) | Which AMC answers which question; ED Decision numbers and dates; AltMoC rule; ETSO software | Certification Liaison & Oversight |
| 02 | [ch02-amc-20-115d-scope](chapters/ch02-amc-20-115d-scope.md) | S1 secs 1-3 (EAR pp. 416-417; 2 pp) | AMC 20-115D purpose, applicability (product certification and ETSO software), replacement of AMC 20-115C | Software Development Assurance |
| 03 | [ch03-software-assurance-115d](chapters/ch03-software-assurance-115d.md) | S1 secs 4-9 (EAR pp. 417-424; 8 pp) | Software life cycle processes as the AMC frames them; ED-12B/DO-178B process reuse; modifying and reusing software | Software Development Assurance |
| 04 | [ch04-transition-tools-gm](chapters/ch04-transition-tools-gm.md) | S1 sec 10 + GM1-GM3 (EAR pp. 424-426, 428-430) | Tool qualification pointer (name-only); GM1 CIA; GM2 data and control coupling; GM3 error handling at design level | Software Development Assurance |
| 05 | [ch05-amc-20-152a-scope](chapters/ch05-amc-20-152a-scope.md) | S2 secs 1-4 (EAR pp. 497-498; 2 pp) | AMC 20-152A purpose, applicability, DAL A-C coverage, DAL D note, document history and background | Airborne Electronic Hardware |
| 06 | [ch06-aeh-objectives](chapters/ch06-aeh-objectives.md) | S2 secs 5-7 (EAR pp. 498-515; sec 5-7) | Added objectives: custom devices including COTS IP, COTS devices, circuit board assemblies | Airborne Electronic Hardware |
| 07 | [ch07-joint-sw-aeh-workflow](chapters/ch07-joint-sw-aeh-workflow.md) | S1/S2 planning-interface passages (EAR pp. 418-419, 423, 497-498, 514-515; cite) | Joint software and hardware certification workflow; PSAC/PHAC-style planning interfaces | Certification Liaison & Oversight |

## Topic Index


- Airborne electronic hardware applicability (DAL A, B, C) → ch05
- AltMoC (alternative means of compliance) → ch01, ch02
- AMC 20-115C, replacement and cancellation of → ch02
- AMC 20-152A applicability and DAL coverage → ch05
- CBA (circuit board assembly) objectives → ch06
- Configuration management (software life cycle process) → ch03
- COTS devices → ch06
- COTS intellectual property (IP) in custom devices → ch06
- Custom device development → ch06
- DAL D (AMC 20-152A use not required) → ch05
- Decision anchors (ED Decision 2017/020/R, ED Decision 2020/010/R) → ch01
- ED-12B/DO-178B process reuse for new development → ch03
- ED-80/DO-254 recognition and supplementation → ch05
- Error handling at design level (GM3) → ch04
- ETSO articles and ETSO software → ch01, ch02, ch05
- GM1 to GM3 (AMC 20-115D general clarification material) → ch04
- Hardware/software planning interfaces (PSAC/PHAC-style) → ch07
- Modification and reuse of previously approved software → ch03
- Parameter data items (process criteria) → ch03
- Planning, development, verification, quality assurance (as the AMC frames them) → ch03
- Single Event Effects (name-only pointer) → ch05, ch06
- Tool qualification pointer (ED-12C section 12.2 / DO-330 family, name-only) → ch04
## Supporting Files

- `glossary.md`: key terms (AEH, AltMoC, CBA, COTS, custom device, DAL, ETSO, GM) with chapter references.
- `cheatsheet.md`: decision rules (which AMC governs, which DAL row applies, which objectives attach, where the FAA twin sits).

## Scope & Limits

- **Amendment 23 pin.** This pack reflects AMC-20 as consolidated in Amendment 23, read from the June 2023 Easy Access Rules compilation; it does not reflect a later AMC-20 amendment. Pin re-verified 2026-10-13. Check the EASA document library for the current consolidated text before relying on a single point.
- **Two sections only.** The pack carries the AMC 20-115D and AMC 20-152A sections and their GM material; no Part-21 body, no bulk AMC-20 content. AMC 20-193 and AMC 20-189 are named as pointers only.
- **Paywalled standards named only.** RTCA DO-178C and DO-254, EUROCAE ED-12C and ED-80, and the supplement set (DO-330 to DO-333, ED-215 to ED-218) are identified, never reproduced; avionics-signpost is the place that names and locates them.
- **US counterpart.** For the FAA side of the same two standards, use faa-8110-49.
- **Not official, not advice.** These are synthesized reference notes, not the official AMC text, not legal advice, and not a substitute for the ED Decision annexes; EASA does not endorse this pack (see LICENSE).
