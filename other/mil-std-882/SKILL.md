---
name: mil-std-882
description: "Knowledge base from MIL-STD-882E (DoD System Safety). Use for the system safety process, hazard analysis tasks (PHA/SSHA/SHA/O&SHA), the risk assessment matrix (severity x probability), software safety criticality, and risk acceptance. US-gov public domain."
---
<!-- argument-hint: [topic, task, or chapter number] -->
# MIL-STD-882E — DoD Standard Practice: System Safety
**Source**: US Department of Defense, MIL-STD-882E w/Change 1 (27 September 2023) | Public Domain, Distribution A | **Chapters**: 8

## When to use
Use this skill when working on DoD defence system safety programmes, designing or reviewing hazard analysis processes, applying the risk assessment matrix (severity × probability → High/Serious/Medium/Low), assessing software safety criticality (SCC × severity → SwCI), or determining appropriate risk acceptance authorities. Also use when cross-referencing NASA or civil aviation safety frameworks against DoD practice.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks: the 8-element safety process, risk matrix, design order of precedence, and software criticality matrix.
- **With a topic** — ask about hazard analysis (PHA, SHA, FHA), software safety (SCC, SwCI, LOR tasks), risk acceptance authorities, HAZMAT management, T&E participation, or life-cycle risk.
- **With a chapter** — ask for `ch01` (scope/definitions), `ch02` (system safety process), `ch03` (risk assessment), `ch04` (software safety), `ch05` (Task 100 management), `ch06` (Task 200 analysis), `ch07` (Task 300 evaluation), `ch08` (Task 400 verification).
- **With a task number** — ask for Task 101 (SSPP), Task 202 (PHA), Task 208 (FHA), Task 401 (safety verification), etc.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### The Eight-Element System Safety Process (Section 4.3)
Iterative, closed-loop process applicable to all DoD systems from concept through disposal:
1. **Document the system safety approach** — PM and contractor document risk management approach, applicable requirements (IM, E3, CHMR), HTS procedures, and risk acceptance authority chain.
2. **Identify and document hazards** — systematic analysis of hardware, software, human interfaces, operational environment, and all life-cycle phases; lessons learned from legacy systems.
3. **Assess and document risk** — assign Severity (I–IV) and Probability (A–F) to each hazard; express as RAC; map to risk level (High/Serious/Medium/Low) per Table III.
4. **Identify and document risk mitigation measures** — apply design order of precedence; estimate expected risk reduction for each candidate mitigation.
5. **Reduce risk** — implement selected mitigations; present hazard status at SRR, PDR, CDR, TRR, PRR.
6. **Verify, validate, and document risk reduction** — confirm implementation and effectiveness through analysis, test, demonstration, or inspection.
7. **Accept risk and document** — formal acceptance by appropriate DoDI 5000 series authority before exposing people/equipment/environment to known hazards; user representative concurrence for all Serious and High risks.
8. **Manage life-cycle risk** — continues after fielding; incorporates mishap data, configuration changes, user feedback; new or elevated risk requires fresh formal acceptance.

### Risk Assessment Matrix (Table III)
Severity I (Catastrophic: death/permanent total disability/irreversible environmental impact/>=\$10M) through IV (Negligible: no lost work day/minimal env/<\$100K).
Probability A (Frequent: >=10^-1) through F (Eliminated: physically incapable of occurrence — PPE/procedures cannot achieve F).
Risk levels: High (worst), Serious, Medium, Low. Every hazard carries three RACs: initial (baseline), target (post-mitigation), and event (configuration-specific).

### Design Order of Precedence (4.3.4)
Five levels, applied in order: (1) eliminate via design selection; (2) reduce risk via design alteration; (3) engineered features or devices; (4) warning devices; (5) signage/procedures/training/PPE. Level 5 alone is prohibited as the sole mitigation for Cat I/II (Catastrophic/Critical) hazards.

### Software Safety Criticality Matrix (Tables IV–VI)
Software risk cannot use probability-based assessment. Instead: assign Software Control Category (SCC 1=Autonomous through 5=No Safety Impact) crossed with Severity (I–IV) to produce Software Criticality Index (SwCI 1–5). SwCI drives Level of Rigor (LOR) tasks: SwCI 1 = full requirements/architecture/design/code analysis + in-depth testing; SwCI 5 = no analysis required. If LOR tasks incomplete: SwCI 1 → HIGH risk; SwCI 2 → SERIOUS; SwCI 3 → MEDIUM; SwCI 4 → LOW. The SSCM assigns rigor, not risk — risk from software contributions uses Appendix B Table B-I criteria.

### Task Structure
- **100-series (Management)**: SSPP (102) / HMP (103), HTS (106), HMMP (108), progress reports (107), IPT/WG support (105).
- **200-series (Analysis)**: PHL (201) → PHA (202) → SRHA (203) → SSHA (204) → SHA (205) → O&SHA (206); specialised: HHA (207), FHA (208), SoSHA (209), EHA (210).
- **300-series (Evaluation)**: SAR (301), HMAR (302), T&E Participation (303), ECP/Mishap Review (304).
- **400-series (Verification)**: Safety Verification (401), Explosives Hazard Classification (402), EOD Data (403).

### Key Distinctions
- Safety-critical (SCF/SCI) = Cat I/II severity consequence. Safety-related = Cat III/IV. Safety-significant = either.
- SSPP vs. HMP: SSPP is system-safety-discipline-centric; HMP coordinates multiple SE disciplines using the same methodology.
- SAR vs. HMAR: SAR is system-safety-only; HMAR covers all disciplines, includes explosives/EOD HAZMAT detail.
- Probability F requires physical hazard elimination — no administrative path to F exists.
- Task invocation: only Sections 3 and 4 are mandatory when MIL-STD-882E is cited without specific tasks; 100–400 series tasks must be individually called out in the RFP/SOW.

## Chapter Index

| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-scope-purpose-definitions.md) | Scope, Purpose & Key Definitions | Mandatory vs. optional sections, definitions of hazard/mishap/risk/safety/ESOH, life-cycle scope |
| [ch02](chapters/ch02-system-safety-process.md) | System Safety Process & General Requirements | 8-element process, design order of precedence, HTS requirements, risk acceptance obligations |
| [ch03](chapters/ch03-risk-assessment.md) | Risk Assessment | Severity I–IV, Probability A–F (with quantitative thresholds), Risk Assessment Matrix Table III, RAC codes, acceptance authorities |
| [ch04](chapters/ch04-software-system-safety.md) | Software System Safety | SCC 1–5, SSCM Table V, SwCI 1–5, LOR task requirements, Table VI default risk levels, Appendix B guidance |
| [ch05](chapters/ch05-task-100-management.md) | Task Section 100 — Management | Tasks 101–108: SSPP, HMP, HTS, IPT/WG support, HMMP, progress reporting, Govt reviews |
| [ch06](chapters/ch06-task-200-analysis.md) | Task Section 200 — Analysis | Tasks 201–210: PHL, PHA, SRHA, SSHA, SHA, O&SHA, HHA, FHA, SoSHA, EHA |
| [ch07](chapters/ch07-task-300-evaluation.md) | Task Section 300 — Evaluation | Tasks 301–304: SAR, HMAR, T&E participation, ECP/mishap/deviation review |
| [ch08](chapters/ch08-task-400-verification.md) | Task Section 400 — Verification | Tasks 401–403: safety verification, explosives hazard classification, EOD data |

## Topic Index

- **Acceptable risk** → ch01, ch02, ch03
- **COTS/GOTS/NDI/GFE safety** → ch06 (every 200-series task), patterns.md Pattern 11
- **Design order of precedence** → ch02, cheatsheet.md
- **ECP / change management** → ch07 (Task 304)
- **Engineering Change Proposal review** → ch07 (Task 304)
- **Environmental hazard analysis (EHA)** → ch06 (Task 210)
- **Explosives / ordnance** → ch08 (Tasks 402, 403)
- **FHA (Functional Hazard Analysis)** → ch06 (Task 208), ch04
- **HAZMAT management** → ch05 (Task 108), ch06 (Tasks 207, 210)
- **Health hazard analysis** → ch06 (Task 207)
- **HTS (Hazard Tracking System)** → ch02, ch05 (Task 106), cheatsheet.md
- **LOR tasks (software)** → ch04, cheatsheet.md
- **Mishap** → ch01, ch03
- **O&SHA** → ch06 (Task 206)
- **PHA (Preliminary Hazard Analysis)** → ch06 (Task 202)
- **PHL (Preliminary Hazard List)** → ch06 (Task 201)
- **Probability levels (A–F)** → ch03, cheatsheet.md
- **RAC (Risk Assessment Code)** → ch03, cheatsheet.md
- **Risk acceptance** → ch02, ch03, ch05, cheatsheet.md
- **Risk assessment matrix** → ch03, cheatsheet.md
- **Safety Assessment Report (SAR)** → ch07 (Task 301)
- **Safety Release** → ch07 (Task 303)
- **Safety-critical / safety-related / safety-significant** → ch01
- **SCC (Software Control Category)** → ch04, cheatsheet.md
- **Severity categories (I–IV)** → ch03, cheatsheet.md
- **SHA (System Hazard Analysis)** → ch06 (Task 205)
- **Software safety** → ch04
- **SoS (System-of-Systems)** → ch01, ch06 (Task 209)
- **SRHA** → ch06 (Task 203)
- **SSPP** → ch05 (Task 102)
- **SSHA (Subsystem Hazard Analysis)** → ch06 (Task 204)
- **SSCM** → ch04, cheatsheet.md
- **SwCI** → ch04, cheatsheet.md
- **T&E participation** → ch07 (Task 303)
- **Task application by programme phase** → cheatsheet.md, Appendix A
- **User representative** → ch03

## Supporting Files

- [glossary.md](glossary.md) — ~55 defined terms from MIL-STD-882E Sections 3.1–3.2, cross-referenced to standard paragraphs
- [patterns.md](patterns.md) — 16 reusable patterns and techniques with When/How/Trade-offs structure; covers hazard identification, risk assessment, design order of precedence, HTS management, analysis hierarchy, software criticality, T&E risk, ECP review, life-cycle continuity
- [cheatsheet.md](cheatsheet.md) — Risk Assessment Matrix, SSCM, task-by-phase matrix, severity/probability quick reference, HTS minimum data elements, tells and smells

---

## Scope & Limits

This knowledge pack covers MIL-STD-882E w/Change 1 (27 September 2023) only. The standard is DoD-specific and US Government public domain. It does not cover:
- Specific DoDI 5000 series acceptance authority thresholds (these are in acquisition policy documents, not in MIL-STD-882E itself)
- Detailed LOR task content (refer to the Joint Software Systems Safety Engineering Handbook and AOP 52)
- Civil aviation safety (DO-178C, ARP 4761) or nuclear safety standards
- ISO/IEC 61508 functional safety levels, though conceptual cross-walk with SILs is feasible
- FAA, OSHA, or EPA regulatory requirements referenced in Task 207 (HHA) reference lists

Claims about risk levels, severity thresholds, and task applicability are grounded in the standard text. Programme-specific tailoring (alternative matrices, modified probability definitions) requires formal DoD Component policy approval and is outside this knowledge pack's scope.
