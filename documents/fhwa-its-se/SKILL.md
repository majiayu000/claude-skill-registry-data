---
name: fhwa-its-se
description: "Knowledge pack synthesized from Systems Engineering for ITS, fourth generation (December 2022, Federal Highway Administration, US Government work, 17 U.S.C. § 105): ITS project systems engineering for transportation agencies. SCOPE LIMITS: single-source (December 2022 FHWA PDF); not construction specifications, not FEMA, not device model-document libraries, not a general SE textbook; INCOSE, ISO/IEC/IEEE 15288, NTCIP, IEEE, and SAE named, not quoted; reconstructed reference notes, not FHWA guidance, and no FHWA endorsement."
---

# Systems Engineering for ITS

## When to use

**Prerequisites:** none required; plain Markdown. Familiarity with a project life cycle helps; the glossary defines the ITS-specific terms.

Use this skill for questions about how a transportation agency runs systems engineering on an ITS project: the Vee process steps from regional planning through retirement, the federal systems engineering analysis requirements for ITS projects, tailoring the process to project risk, the documentation set, and ITS procurement options. It does not cover construction specifications, FEMA publications, or device model-document libraries.

**Source:** Systems Engineering for ITS, fourth generation (December 2022), Federal Highway Administration. The source is a work of the US Government (17 U.S.C. § 105) and is in the public domain. These are reconstructed reference notes, not reproductions, and not official FHWA guidance; no FHWA endorsement is implied. Licence text and source identification in [LICENSE](LICENSE).

## How to use this skill

- **Without arguments**: read Core Frameworks & Mental Models below.
- **With a topic**: use the Topic Index and follow the chNN pointer to a chapter.
- **With a life-cycle question**: use the Chapter Index and read the matching chapter.
- **For a term** use `glossary.md`; **for a decision rule** use `cheatsheet.md`.

## Core Frameworks & Mental Models

### The Vee model as the ITS project process

Needs at the upper left become requirements, decomposition continues down to component design and implementation at the base, and the right side recomposes: integration and system verification climb back up against the requirements, and validation at the top right confirms the delivered system meets the user needs. Decision gates between steps are tailored: informal reviews for small projects, formal submittals and approvals for complex ones. The ITS variant adds wings for the full system life, from regional operations planning before the project to operations, maintenance, and retirement after it. Verification confirms the product was "built right" (meets its requirements); validation confirms the "right product" was built (meets the needs).

### The US DOT systems engineering analysis rule

ITS projects funded from the Highway Trust Fund must be based on a systems engineering analysis, on a scale commensurate with project scope, covering seven minimum elements: mapping to the regional (or national) ITS architecture, participating agency roles and responsibilities, requirements definition, analysis of alternative system configurations and technology options, procurement options, identification of applicable ITS standards and testing procedures, and procedures and resources for operations and management. Compliance is demonstrated to FHWA Division Offices and FTA Regional Offices, commonly through a Systems Engineering Review Form; a complete systems engineering process meets or exceeds the seven elements. Low-risk projects can satisfy the elements from categorical documents, prior project documentation, maintained regional architectures, or the FHWA Model Systems Engineering Documents.

### Tailoring: risk sets the formality, never the substance

Evaluate seven risk factors (jurisdictions and modes, software creation, technology maturity, interface complexity, requirements completeness, operating-procedure completeness, technology service life), then scale each Vee step from none-to-low effort (reuse existing documentation) through medium (update and extend) to high (develop the full documentation set). Tailoring adjusts documentation and review formality; it is not an invitation to skip steps, and even the smallest project keeps documented requirements, design, and verification procedures. Write the tailored process down as a project plan or SEMP.

### Documentation as the ownership handoff

Eleven template documents cover the life from the project management plan through the operations and maintenance plan; the SEMP carries the technical process detail and matters most when custom software is being developed. The standing test for the documentation set: could another qualified team maintain the system from these records alone?

## Chapter Index

| Ch | Chapter | Sources | Coverage |
|---|---|---|---|
| 01 | [ch01-introduction.md](chapters/ch01-introduction.md) | pp. 4-6 | Purpose, audience, alignment with INCOSE and ISO/IEC/IEEE 15288, navigation, icon system, not-formal-guidance boundary. |
| 02 | [ch02-what-is-systems-engineering.md](chapters/ch02-what-is-systems-engineering.md) | pp. 7-26 | Definitions, key principles, transportation context, life cycle models (sequential, incremental, iterative/Agile), US DOT regulation and the seven analysis elements. |
| 03 | [ch03-the-systems-engineering-process.md](chapters/ch03-the-systems-engineering-process.md) | pp. 27-136 | Vee steps from regional planning to retirement, plus cross-cutting processes: project management, configuration management, traceability, risk management, trade studies. |
| 04 | [ch04-managing-se-projects.md](chapters/ch04-managing-se-projects.md) | pp. 137-158 | Agency roles, seven-factor risk evaluation, tailoring bands, procurement instruments and delivery models, staffing options, implementing the regulation with review forms. |
| 05 | [ch05-systems-engineering-resources.md](chapters/ch05-systems-engineering-resources.md) | pp. 159-160 | ITS publications, general SE references, training providers, and the ARC-IT / RAD-IT / SET-IT tool family. |
| 06 | [ch06-systems-engineering-documentation.md](chapters/ch06-systems-engineering-documentation.md) | pp. 161-213 | Eleven document templates (PMP, SEMP, CMP, ConOps, requirements, design, interface, integration, verification, deployment, validation, O&M) with per-document purpose, tailoring, and checklists. |
| 07 | [ch07-glossary-and-acronyms.md](chapters/ch07-glossary-and-acronyms.md) | pp. 214-223 | The source's glossary and acronym list as the pack vocabulary's source of record. |

## Topic Index

- V process, Vee model, decision gates, decomposition and recomposition → ch02, ch03
- Life cycle models: sequential, incremental, iterative, Agile and Scrum → ch02
- Regional ITS architecture, TSMO, operations planning, TIP and programming → ch02, ch03, ch04
- Project identification, feasibility studies, scoping → ch03
- Concept of Operations, user needs, operational scenarios, validation plan → ch03
- Requirements engineering, verification methods, traceability matrix, quality attributes → ch03
- Design, high-level and detailed, interfaces, off-the-shelf selection, specifications → ch03
- Software and hardware implementation, prototyping, unit testing → ch03
- Integration and system verification → ch03
- Deployment and acceptance, installation, transition to operations → ch03
- Validation, in-process validation, before-and-after studies → ch03
- Operations and maintenance, changes and upgrades, regression testing → ch03
- Retirement and replacement, disposal, parallel operation → ch03
- Cross-cutting processes: project management, configuration management, traceability, risk management, trade studies → ch03
- Agency roles, risk evaluation, risk factors → ch04
- Tailoring, process formality, low and medium and high risk → ch03, ch04
- ITS procurement: RFI, RFQ, RFP, ITB, P3, design-build, design-bid-build, CMAR, staffing → ch04
- Regulation compliance, Systems Engineering Analysis, review forms (SERF) → ch02, ch04
- Resources, training, ARC-IT, RAD-IT, SET-IT, model SE documents → ch05
- Documentation templates: PMP, SEMP, configuration management plan → ch06
- Documentation templates: requirements, design, interface, integration, verification, deployment, validation, O&M plans → ch06
- Glossary terms and acronyms → ch07
- Definitions: verification versus validation, baseline, configuration item → ch03, ch07

## Supporting Files

- `glossary.md`: terms the source defines, alphabetical, each with the chapter that uses it.
- `cheatsheet.md`: decision rules for risk sizing, tailoring, document sets, risk management, trade studies, and ITS procurement, in prose.

## Scope & Limits

- **Source version:** Systems Engineering for ITS, fourth generation (December 2022); pin verified 2026-10-28 against the source PDF (223 pages).
- **ITS project systems engineering only:** the pack carries the source's transportation-agency framing, not construction specifications, not FEMA publications, and not device model-document libraries.
- **Not a general SE textbook:** the source is a primer for transportation professionals; it does not replace the INCOSE handbook or ISO/IEC/IEEE 15288, which it names and stays consistent with.
- **Third-party standards named, not quoted:** INCOSE, ISO/IEC/IEEE 15288, ISO/IEC/IEEE 29148, IEEE standards, NTCIP, SAE, EIA standards, PMI, and 23 CFR 940 are identified by name; no clause text is reproduced.
- **Not official FHWA guidance:** reconstructed reference notes, not reproductions; compliance determinations belong to FHWA Division Offices and FTA Regional Offices; no FHWA endorsement. Source and licence details live only in [LICENSE](LICENSE).
