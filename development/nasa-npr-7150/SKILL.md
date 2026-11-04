---
name: nasa-npr-7150
description: "Knowledge base from NASA NPR 7150.2D — NASA Software Engineering Requirements. Use for NASA's Agency-wide software-engineering requirements: the software classification scheme (Classes A–F), the Requirements Mapping Matrix and class-driven applicability, tailoring and Technical Authority governance, the SWE-### 'shall' requirements across software management (Ch 3) and the engineering life cycle (Ch 4), the supporting disciplines (configuration management, risk, peer reviews/inspections, measurement, non-conformance — Ch 5), safety-critical and cybersecurity requirements, IV&V applicability, traceability, and the Appendix A definitions. Does not cover detailed software-assurance/safety procedures (see NASA-STD-8739.8), implementation how-to and document content (see NASA-HDBK-2203), the systems-engineering process framework (see NPR 7123.1), or program/project management (see NPR 7120.5)."
---

<!-- argument-hint: [software class A-F, SWE number, tailoring, RMM, safety-critical, cybersecurity, IV&V, traceability, chapter number] -->

# NASA NPR 7150.2D — NASA Software Engineering Requirements
**Source**: NASA (US Government work, public domain) | **Chapters**: 8

## When to use
Use this skill when you need to apply, explain, or assess NASA's Agency-wide software-engineering requirements: classifying software (Classes A–F), reading applicability from the Requirements Mapping Matrix, justifying and approving tailoring, working any of the numbered SWE-### "shall" requirements, planning the software life cycle, meeting safety-critical and cybersecurity obligations, deciding IV&V applicability, building bidirectional traceability, or resolving a definition. This is the normative software-engineering requirements directive for NASA programs and projects; it pairs with NASA-HDBK-2203 (the non-binding Software Engineering Handbook) for implementation guidance and NASA-STD-8739.8 for assurance, safety, and IV&V detail.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below for an overview of classification, the Requirements Mapping Matrix, tailoring, and the requirement structure.
- **With a topic** — ask about a specific mechanism (e.g., "Class C definition", "tailoring approval chain", "safety-critical behaviors", "MC/DC requirement", "auto-generated code", "IV&V applicability").
- **With a chapter** — ask for `ch03` (software management), `ch04` (life-cycle engineering), `ch05` (supporting disciplines), `ch07` (definitions), or `ch08` (software classifications).

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### Software Classification (Classes A–F) — the master valve

Classification is the upstream decision that drives everything else. Each system or subsystem containing software is assigned a class (at the highest applicable class, SWE-020), and the class decides how many requirements bite and at what rigor. Five factors decide the class: how the software is used with/within a NASA system, the criticality of that system, the degree of human dependence, developmental/operational complexity, and the size of the Agency's investment. Venue (space, air, ground, desktop) narrows the branch; consequence and dependence pick the class.

- **A** — Human-Rated Space Software Systems (crew life, primary human-spaceflight objectives).
- **B** — Non-Human Space-Rated Systems or Large-Scale Aeronautics Vehicles (reliable non-human mission, large vehicle).
- **C** — Mission-Support, Smaller Aeronautics, or Major Facility Software (secondary objectives, mission support).
- **D** — Basic Science/Engineering Design and Research-and-Technology Software (development and research).
- **E** — Design Concept, Research, Technology, General-Purpose Software (throwaway exploration, desktop tools) — *never safety-critical*.
- **F** — General-Purpose Computing, Business, and IT Software (the separate Business/IT track).

Rules: one class per system/subsystem; round up on ambiguity; safety-critical software is Class D or higher; classification follows intended use and can be promoted over the life cycle; the NASA Chief Engineer is the final arbiter of definition disputes.

### The Requirements Mapping Matrix (RMM) — applicability and proof

The RMM (Appendix C) is the operative artifact. It maps every NPR requirement against a project by class: an "X" cell means mandatory for that class, a blank means optional or not invoked. The RMM records what the project commits to, what it deems "Not-Applicable," and any approved tailoring with justification and authority signatures. Compliance is *demonstrated* by a completed RMM plus internal (NPD 1200.1) and external (NPD 1210.2) controls — a paper-backed claim, not an assertion.

### Tailoring and Technical Authority

Tailoring is the governed route to relief from a requirement, consistent with objectives, acceptable risk, and constraints. A relief request is an evidence package: rationale + risk evaluation + mitigations, concurrence from impacted disciplines (safety, quality, cybersecurity, health), the signature of the authority named in Appendix C, and the responsible manager's formal acceptance of residual risk. Special cases: cybersecurity (Section 3.11) relief also needs the SAISO signature; IV&V (SWE-141) relief is the Chief of SMA's decision; human-safety risk needs the actual risk takers to agree to assume it. Engineering and SMA Technical Authority chains govern application; the Chief Engineer (A–E) and CIO (F) tracks own approval.

### The Requirement Grammar (SWE-### and the verbs)

Every mandatory statement uses **shall** and carries a unique **SWE-###** identifier (e.g., SWE-013, SWE-141, SWE-219) used for traceability, RMM mapping, and tailoring. **should** = recommended; **will** = expected outcome; **may/can** = discretionary; **is/are** = descriptive. Nearly every "shall" is directed at the **project manager** as the single accountable owner.

### The Life-Cycle Engineering Sequence (Chapter 4)

Requirements → architecture → design → implementation → testing → operations/maintenance/retirement, each carried by SWE-### requirements. Quality is built in early: requirements must be well-formed, complete, consistent, verifiable, and traceable; architecture is the costliest-to-reverse decision (architecture review mandated for Category 1 and Class A/B-payload Category 2 projects, SWE-143); static analysis (SWE-135) and unit testing run during implementation; testing verifies against requirements with target-platform validation; coverage gaps triage into four causes; regression, hazard, and uplink testing close the loop. Non-custom code (COTS/GOTS/MOTS/OSS/reused) is held to the same rigor as developed code, and critical tools must be validated and accredited before their output is trusted.

### The Supporting Disciplines (Chapter 5) — the horizontal layer

Five practices run continuously alongside the phased work, each a set of "the project manager shall" obligations: **Software Configuration Management** (items, tools, and build environments under control with separated change authority and audits), **Risk Management** (with residual-risk awareness), **Peer Reviews and Inspections** (instrumented with entry/exit criteria, a reading technique, tracked actions, and recorded measures), **Software Measurement** (multi-level: project → Center → Chief Engineer, with margin and requirements-volatility tracking), and **Non-conformance / Defect Management** (severity-classified, closed-loop on high-severity issues, spanning acquired and reused software).

### Safety-Critical and Cybersecurity Hardening (Chapter 3)

Safety-critical components carry behavioral safe-state requirements (SWE-134: safe init/restart, safe state transitions, two independent operator actions for overrides, out-of-sequence command rejection, memory-integrity and prerequisite checks, no single-event hazard, timely off-nominal response) reinforced by hard gates — 100% MC/DC coverage (SWE-219) and cyclomatic complexity ≤ 15 (SWE-220). Cybersecurity is woven through development: assessments including off-the-shelf risk (SWE-156), mitigations (SWE-154/159), secure coding (SWE-207), static-analysis verification against the secure coding standard (SWE-185), and adversarial-action data reporting (SWE-210). Coding defects are treated as security weaknesses, not just quality issues.

---

## Chapter Index

| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-nasa-npr-7150-introduction-purpose-structure.md) | Introduction, Purpose, Structure | Whole-life scope, document hierarchy and precedence, class-driven applicability, RMM verification, requirement vocabulary, no mandated life-cycle model, authority chain |
| [ch02](chapters/ch02-nasa-npr-7150-roles-responsibilities-tailoring.md) | Roles, Responsibilities, Tailoring | OCE/SMA/OCIO/CHMO/Center roles, Technical Authority governance, tailoring as evidence-backed relief, RMM signatures, co-approval chains, CMMI-DEV, delegation |
| [ch03](chapters/ch03-nasa-npr-7150-software-management-requirements.md) | Software Management Requirements | Classification (SWE-020) + RMM as applicability engine, planning/cost/schedule/training, off-the-shelf and auto-generated discipline, CMMI levels, IV&V, MC/DC, cybersecurity, bidirectional traceability |
| [ch04](chapters/ch04-nasa-npr-7150-software-engineering-lifecycle-requirements.md) | Software Engineering (Life Cycle) Requirements | Requirements → architecture → design → implementation → test → ops/maintenance/retirement, SWE-### per phase, static analysis, coverage four-cause triage, regression/hazard/uplink testing, tool accreditation |
| [ch05](chapters/ch05-nasa-npr-7150-supporting-lifecycle-requirements.md) | Supporting Life Cycle Requirements | SCM, risk management, peer reviews/inspections, measurement (multi-level), non-conformance/defect management; IEEE 828, NASA-STD-8739.9, NASA-HDBK-2203 |
| [ch06](chapters/ch06-nasa-npr-7150-recommended-software-records.md) | Recommended Software Records | Typical product menu vs. content; defers content/timing to NASA-HDBK-2203; SPAN templates; reader-first, tailor-the-menu, format-flexible, living-records principles |
| [ch07](chapters/ch07-nasa-npr-7150-definitions.md) | Definitions (Appendix A) | Controlled vocabulary; off-the-shelf taxonomy; assure/ensure/accredit; defect/fault/failure; verification vs. validation; software assurance discipline set; MOTS and facility thresholds as policy switches |
| [ch08](chapters/ch08-nasa-npr-7150-software-classifications.md) | Software Classifications (Appendix D) | Classes A–F definitions, five factors, round-up rule, safety-critical floor, use-case promotion, exclusion lists, dual TA chains with Chief Engineer tiebreaker |

## Topic Index

- **Acquired / off-the-shelf software (COTS/GOTS/MOTS/OSS)** → ch03, ch07, patterns
- **Architecture review** → ch04
- **Auto-generated code** → ch03, ch04, patterns
- **Bidirectional traceability** → ch03, ch07, patterns
- **Classification (Classes A–F)** → ch08, ch01, ch03, cheatsheet
- **CMMI-DEV maturity by class** → ch02, ch03, cheatsheet
- **Code coverage / four-cause triage** → ch04, patterns
- **Configuration management (SCM)** → ch05, glossary, patterns
- **Cost estimation / cost models** → ch03, cheatsheet
- **Cyclomatic complexity (≤ 15)** → ch03, ch07, cheatsheet
- **Cybersecurity requirements (Section 3.11)** → ch03, patterns, cheatsheet
- **Definitions / glossary** → ch07, glossary
- **Defect / fault / failure** → ch05, ch07, glossary
- **IV&V (Independent Verification and Validation)** → ch02, ch03, ch07
- **Life-cycle engineering phases** → ch04, cheatsheet
- **MC/DC coverage (100%)** → ch03, ch04, ch07, cheatsheet
- **Measurement program** → ch05, patterns
- **Non-conformance / defect management** → ch05, patterns
- **Peer reviews and inspections** → ch05, patterns
- **Project manager (accountable role)** → ch03, ch04, ch05
- **Records / software products** → ch06, patterns
- **Requirements Mapping Matrix (RMM)** → ch01, ch02, ch03, cheatsheet
- **Requirements (well-formed, traceable)** → ch04
- **Risk management (software)** → ch05, patterns
- **Roles and responsibilities** → ch02
- **Safety-critical software / safe states** → ch03, ch08, patterns, cheatsheet
- **SWE-### requirement identifiers** → ch03, ch04, ch05, cheatsheet
- **Static analysis** → ch04, ch07
- **Tailoring** → ch02, ch03, patterns, cheatsheet
- **Technical Authority (Engineering / SMA)** → ch02, ch08
- **Verification vs. validation** → ch04, ch07, glossary

## Supporting Files

- [glossary.md](glossary.md) — key NPR 7150.2D terms from Appendix A, alphabetical, with chapter references and source-standard notes
- [patterns.md](patterns.md) — 10 reusable techniques with When/How/Trade-offs structure (classify-first, tailor-through-the-RMM, developed-code bar, safety-critical layering, traceability spine, tools-as-CIs, coverage triage, cybersecurity-through-development, continuous supporting disciplines, reader-first records)
- [cheatsheet.md](cheatsheet.md) — decision rules, the six classes, requirement-verb key, chapter map, quantitative gates/thresholds, high-traffic SWE numbers, companion documents, tells & smells

---

## Scope & Limits

**Covers**: NASA's Agency-wide software-engineering requirements per NPR 7150.2D (Rev D, effective March 8, 2022) — the software classification scheme (Classes A–F, Appendix D); the Requirements Mapping Matrix and class-driven applicability (Appendix C); tailoring and Technical Authority governance (Ch 2); the SWE-### "shall" requirements for software management (Ch 3) and the engineering life cycle (Ch 4); the supporting disciplines of configuration management, risk, peer reviews/inspections, measurement, and non-conformance (Ch 5); safety-critical behavioral and quantitative requirements; cybersecurity requirements; IV&V applicability; bidirectional traceability; recommended software records (Ch 6); and the Appendix A definitions (Ch 7).

**Thin on / does not cover in depth**: detailed software-assurance, software-safety, and IV&V *procedures* (the directive invokes them but defers the substance to **NASA-STD-8739.8**); implementation how-to, record content, and timing (deferred to **NASA-HDBK-2203** and the SPAN library); the systems-engineering process framework (**NPR 7123.1**); program/project management and project categories (**NPR 7120.5/7/8**); the full Appendix C matrix cell-by-cell (use the cheatsheet's class table and SWE list instead); the Appendix B acronym list and Appendix E references; and any specific life-cycle model (the NPR deliberately mandates none).

**Jurisdiction**: US Government public-domain work (17 U.S.C. § 105). NPR 7150.2D binds NASA Headquarters and Centers; it reaches JPL, contractors, grant recipients, and agreement parties only as incorporated through a contract, grant, or agreement. It is neither retroactive nor a ceiling on stricter requirements. Printed copies are uncontrolled — verify the current version in the NODIS Library before relying on a requirement.
