---
name: fda-med-device
description: "Reconstructed reference notes on US FDA medical-device software regulation, built from seven public-domain FDA sources (the QMSR final rule 89 FR 7496, FDA device software guidance documents, and the eSTAR program page; pinned 2026-10-12). Use for regulatory pathways and premarket submissions (510(k), De Novo, PMA, eSTAR), premarket software documentation levels (Basic or Enhanced), software validation and Computer Software Assurance, the Quality Management System Regulation (QMSR, 21 CFR 820), medical-device cybersecurity (secure product development, SBOMs, FD&C Act section 524B, labelling), clinical decision support boundaries, off-the-shelf software, MDDS and other software-function scope questions, and the 510(k) software-change trigger. SCOPE LIMITS: US FDA device regulation only; no EU MDR or UKCA content (see `med-device-eu`); no ISO 13485, ISO 14971, or IEC 62304 text, which are named and summarized only as FDA obligations; no drug, biologic, or combination-product rules; reflects the pinned source dates, not later FDA actions; synthesized reference notes, not legal advice and not a substitute for the guidance documents. LICENCE: Public Domain (US Government work, 17 U.S.C. 105)."
---

<!-- argument-hint: [FDA device software topic, regulation question, submission section, chapter number] -->

# FDA Device Software Guidance and the QMSR
**Source**: U.S. FDA (CDRH/CBER). Adapted from the sibling 2026-09-24 prototype build and re-checked against the 2026-10-12 FDA source pin, the seven documents vetted in LICENSE as rows S1-S4 and S6-S8 | **Licence**: Public Domain (US Government work, 17 U.S.C. 105) | **Chapters**: 12

## When to use
**Prerequisites:** none: plain Markdown; no MCP server, API key, or licence tier needed at runtime.

Use this skill for US FDA questions about software in or around medical devices: what documentation a premarket submission needs, how software must be validated, what the Quality Management System Regulation requires after the 2026-02-02 transition, what cybersecurity artifacts FDA expects, where a software function stops being a device (clinical decision support, MDDS), when a software change triggers a new 510(k), and how eSTAR structures the submission. The pack answers with FDA's own frameworks, cited by chapter and source row.

## How to Use This Skill
- **Without arguments**: read the Core Frameworks below, covering documentation levels, validation vs assurance, the QMSR transition, the SBOM and 524B obligations, and the 510(k) change trigger.
- **With a topic**: use the Topic Index to find the chapter, then ask directly (e.g. "what documentation level applies for this device", "does this OTS library need enhanced testing").
- **With a chapter**: ch01 orientation; ch02-ch04 documentation and assurance; ch05-ch07 QMSR and cybersecurity; ch08-ch09 scope boundaries and the cybersecurity submission package; ch10-ch12 changes, CDS, and eSTAR.

Supporting files: `glossary.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### Documentation Level: Basic vs Enhanced (S1)
The 2023 premarket software guidance sets a two-value axis, the **Documentation Level**, picked by a risk-based determination rather than a concern-classification scheme. **Enhanced Documentation** applies where a failure or flaw of any device software function could present a hazardous situation with a probable risk of death or serious injury, to a patient, a user, or others in the environment of use; **Basic Documentation** applies everywhere Enhanced does not. The determination weighs all known and foreseeable software hazards, including those from reasonably foreseeable misuse and from cybersecurity compromises, assessed before risk controls are applied and in the context of the device's intended use; the level reflects the device as a whole, not one function in isolation. Enhanced adds submission depth: fuller development, configuration-management and maintenance practices, richer testing and V&V evidence, software version history, and unresolved-anomaly disclosure. A Class III device or a combination-product constituent part defaults to Enhanced; arguing down to Basic takes a documented rationale, and FDA can still ask for more during review. The mental model: two levels, one question ("could this software fail into death or serious injury before risk controls?"), and the answered level is a floor, not a ceiling.

### Software validation principles (S2)
The General Principles of Software Validation frame validation as **confirmation by objective evidence** that software conforms to its specifications and that those specifications match user needs and intended use. Validation spans the whole lifecycle, not a final test phase; changes after initial validation get their own validation effort scaled to the change; and the independence of review scales with risk. One boundary matters for reading everything else: Section 6 of this guidance (validation of automated process equipment and quality system software) is superseded by the CSA guidance (S3), while the rest remains the authority for device software.

### Computer Software Assurance: risk-based validation (S3)
CSA replaces check-the-box computer system validation for **production and quality management system software** with a risk-based method: establish the intended use of the system, determine the risk its failure poses to product quality or safety, and select assurance activities proportionate to that risk. Testing becomes one tool among several, and **unscripted** approaches (ad-hoc, error-guessing, exploratory) are legitimate where risk allows. The record documents intended use, the risk determination, the assurance activities chosen and why, and the results. The mental model: assurance follows risk, and the record shows the reasoning, not just a test log.

### The QMSR transition (S4)
The 2024 final rule (89 FR 7496) retitled 21 CFR part 820 from Quality System Regulation to **Quality Management System Regulation** and rewrote it around **ISO 13485:2016 incorporated by reference**, with ISO 9000:2015 clause 3 vocabulary alongside, effective 2026-02-02. FDA kept additions where ISO 13485 alone would fall short of US requirements. The working habit this pack teaches: locate the obligation in ISO 13485 by clause number, then check the rule text (S4) for the FDA-specific layer on top. ISO text itself stays out of this pack; the chapters restate obligations in FDA's words.

### Cybersecurity: the SPDF, SBOM and section 524B (S6)
FDA expects a **secure product development framework (SPDF)**: cybersecurity risk management, security architecture, and cybersecurity testing woven through design, production, and postmarket rather than bolted on at the end. Premarket submissions carry a **software bill of materials (SBOM)**: the software components the device contains, so vulnerabilities can be traced later. FD&C Act section 524B makes "cyber devices" carry standing duties: a postmarket **Cybersecurity Management Plan**, and software updates and patches for known unacceptable vulnerabilities on a reasonable timeline. The mental model: the submission is the opening position of a maintenance commitment, not a one-time disclosure.

### The 510(k) change trigger
Software changes to an existing device run through a **decision sequence**, not a gut call: what does the change touch, does it alter functionality or performance, does it introduce or shift risk, does labelling change. Answers route to either a new 510(k) or a documented decision to stay put. Both outcomes are recorded; the no-submission decision carries its own rationale. The mental model: every change is presumed to need assessment, and the flowchart is how you prove you did it.

### Scope boundaries: CDS, MDDS and OTS (S7; the MDDS and OTS guidance sits outside the source pin)
Three carve-outs and one category shape what counts as regulated device software. **Clinical decision support** stays outside the device definition when it meets four statutory criteria, including that the clinician can independently review the basis for the recommendation (S7). **MDDS** and image storage/communication functions were moved outside the device definition by the 21st Century Cures Act because they transfer or store data without modifying it (the 2022 MDDS guidance). **Off-the-shelf software** inside a device stays fully in scope: its failure modes, the verification evidence proportionate to its risk, and its maintenance and obsolescence plan are all FDA's business (the 2023 OTS guidance). The mental model: first ask "is this a device function at all", then ask "whose software is it".

### eSTAR submissions (S8)
The electronic Submission Template And Repository (eSTAR) structures 510(k) and De Novo submissions as guided PDF templates with mandatory sections and internal checks. eSTAR 510(k)s became mandatory 2023-10-01; eSTAR De Novos from 2025-10-01. The templates change authoring mechanics: content lands in fixed sections, and software and cybersecurity artifacts have designated homes.

---

## Chapter Index

| # | Chapter | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-regulatory-landscape.md) | Regulatory landscape and pathways | Which document governs which question; 510(k)/De Novo/PMA paths; where software functions fit; MDDS framing |
| [ch02](chapters/ch02-premarket-software-documentation.md) | Premarket software documentation | Documentation Level (Basic vs Enhanced), the risk-based determination, required elements per level (S1) |
| [ch03](chapters/ch03-software-validation.md) | Software validation principles | GPSV lifecycle validation, validation of changes, independence, records; Section 6 superseded (S2) |
| [ch04](chapters/ch04-computer-software-assurance.md) | Computer software assurance | Risk-based assurance for production and QMS software, intended use, activity selection, records (S3) |
| [ch05](chapters/ch05-qmsr-quality-management.md) | QMSR quality management | 21 CFR 820 after 2026-02-02, ISO 13485 incorporation by reference, FDA additions, transition (S4) |
| [ch06](chapters/ch06-cybersecurity-qms.md) | Cybersecurity and the QMS | Secure product development framework, SBOM as a QMS artifact, postmarket cyber processes (S6) |
| [ch07](chapters/ch07-cybersecurity-premarket.md) | Cybersecurity premarket content | Threat modelling, SBOM content, security architecture, security requirements, labelling (S6) |
| [ch08](chapters/ch08-software-function-scope.md) | Software function scope and OTS | MDDS and the non-device boundary, OTS/SOUP verification evidence, maintenance, obsolescence (guidance outside the pin, named in chapter) |
| [ch09](chapters/ch09-premarket-cyber-documentation.md) | Premarket cybersecurity documentation package | Assembling the cybersecurity section of a premarket submission, artifact ordering (S6) |
| [ch10](chapters/ch10-software-changes-510k.md) | Software changes and the 510(k) trigger | Change-assessment decision sequence, documenting a no-510(k) decision (guidance outside the pin, named in chapter) |
| [ch11](chapters/ch11-clinical-decision-support.md) | Clinical decision support | The four statutory criteria for non-device CDS, worked boundary cases (S7) |
| [ch12](chapters/ch12-submissions-estar.md) | eSTAR submissions | eSTAR structure for 510(k) and De Novo, mandatory dates, where software and cyber content lands (S8) |

## Topic Index

- **510(k) pathways** → ch01, ch12
- **Basic vs Enhanced documentation** → ch02
- **Change control (software)** → ch10, ch05
- **Clinical decision support (CDS)** → ch11, ch01
- **Computer software assurance (CSA)** → ch04
- **Computer system validation (legacy)** → ch04, ch03
- **Cyber device (FD&C Act 524B)** → ch06, ch07
- **Cybersecurity management plan** → ch06, ch07
- **Cybersecurity labelling** → ch07, ch09
- **De Novo pathways** → ch01, ch12
- **Documentation levels (premarket)** → ch02
- **Documentation Level determination (risk-based)** → ch02
- **eSTAR (510(k) and De Novo)** → ch12
- **Image storage and communication functions** → ch08, ch01
- **Incorporation by reference (ISO 13485)** → ch05
- **MDDS (medical device data systems)** → ch08, ch01
- **Non-device software functions** → ch11, ch08, ch01
- **Off-the-shelf software (OTS/SOUP)** → ch08
- **OTS maintenance and obsolescence** → ch08
- **Premarket submission structure** → ch12, ch02, ch09
- **PMA pathways** → ch01
- **Postmarket cybersecurity** → ch06, ch07
- **Premarket cybersecurity package** → ch09, ch07
- **QMSR (Quality Management System Regulation)** → ch05
- **Risk to health (documentation and change driver)** → ch02, ch10
- **SBOM (software bill of materials)** → ch07, ch06
- **Secure product development framework (SPDF)** → ch06
- **Security architecture views** → ch07
- **Software changes and new submissions** → ch10
- **Software functions in submissions** → ch02, ch01
- **Threat modelling** → ch07
- **Unscripted testing** → ch04
- **Validation of software changes** → ch03
- **Validation vs verification** → ch03, ch02

## Supporting Files

- [glossary.md](glossary.md): terms as FDA uses them (510(k), CSA, CDS, IBR, documentation level, MDDS, OTS/SOUP, QMSR, SBOM, eSTAR), with chapter references
- [cheatsheet.md](cheatsheet.md): decision rules covering whether a change needs a 510(k), what documentation level applies, what cyber artifacts are expected, and what validation approach fits

---

## Scope & Limits

**Covers**: US FDA regulation of software in and around medical devices, as stated in FDA guidance and rule text and re-checked against the 2026-10-12 source pin: premarket pathways and submission content, software documentation levels, validation and computer software assurance, the QMSR, device cybersecurity, software-function scope boundaries (CDS, MDDS), off-the-shelf software, the 510(k) change trigger, and eSTAR.

**Does not cover**: EU MDR, UKCA, or any non-US regime (see `med-device-eu`; nothing in this pack answers EU questions). No text from ISO 13485, ISO 9000, ISO 14971, or IEC 62304: those standards are named and their obligations summarized only as FDA states them. ISO 13485:2016 is incorporated by reference into 21 CFR 820 and stays copyrighted. A reader who needs the standard buys it or reads it at the ANSI IBR portal. No drug, biologic, or combination-product rules, and no FDA enforcement policy beyond what the pinned documents state.

**Not legal advice.** The pack is synthesized reference notes reconstructed from the sources, with quotations capped at two sentences. It is not a substitute for the guidance documents themselves, not regulatory counsel, and not a compliance determination. FDA guidance contains nonbinding recommendations; the rule text and regulations are the binding layer.

**Source dates**: re-checked against the 2026-10-12 FDA source pin, whose current documents are named in PACK.yaml, including the February 2026 CSA and cybersecurity finals, the January 2026 CDS final, and the eSTAR program page (content current 2026-09-21). A chapter that teaches a guidance outside that pin names the guidance and cites no source row. Later FDA actions, draft guidances, and docket activity after the pin date are out of scope. Check fda.gov for current versions before relying on any single requirement.

**Licence & attribution**: public domain (US Government work, 17 U.S.C. 105); FDA is credited as a courtesy in the repository NOTICE, not as a legal obligation, and does not endorse this pack. See `LICENSE` for the per-source vetting record, including dockets and supersession statements confirmed from the source texts.
