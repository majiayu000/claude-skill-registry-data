---
name: nrc-nuclear
description: "Reconstructed reference notes on US NRC software assurance guidance for digital computer software in nuclear power plant safety systems, built from seven public-domain sources (Regulatory Guide 1.168 Revision 2, July 2013; Regulatory Guides 1.169, 1.170, 1.171, 1.172, and 1.173 Revision 1, July 2013; NUREG-0800 Branch Technical Position 7-14 Revision 6, August 2016; pinned 2026-10-12). Use for software life cycle process questions, software requirements specifications, software configuration management plans, verification and validation with reviews and audits, test documentation and unit testing, and what NRC staff examine in a BTP 7-14 software review of plans, implementation, and design outputs. SCOPE LIMITS: NRC Regulatory Guides and the BTP 7-14 staff review position only; the endorsed IEEE standards (IEEE Std 603-1991, 7-4.3.2-2003, 828-2005, 829-2008, 830-1998, 1008-1987, 1012-2004, 1028-2008, 1074-2006), IEC 60880, IEC 61513, IEC 62138, and IAEA guides are cited by designation and edition only, with no standard text; RG 1.152 Rev 4, BTP 7-18, BTP 7-19, other SRP Chapter 7 sections, and NUREG/CR contractor reports are outside the pack; reflects the pinned 2013 and 2016 editions, not later agency actions; synthesized reference notes, not legal or licensing advice and not a substitute for the source documents. LICENCE: Public Domain (US Government work, 17 U.S.C. § 105)."
---

<!-- argument-hint: [software assurance topic, RG number, BTP 7-14 review area, or chapter number] -->

# NRC Digital Safety-System Software Assurance
**Source**: U.S. Nuclear Regulatory Commission (NRC), 7-source reference set: RG 1.168 Rev 2 (ML13073A210), RG 1.169 Rev 1 (ML12355A642), RG 1.170 Rev 1 (ML13003A216), RG 1.171 Rev 1 (ML13004A375), RG 1.172 Rev 1 (ML13007A173), RG 1.173 Rev 1 (ML13009A190), and NUREG-0800 BTP 7-14 Rev 6 (ML16019A308); pinned 2026-10-12 | **Licence**: Public Domain (US Government work, 17 U.S.C. § 105) | **Chapters**: 8

## When to use

**Prerequisites:** basic software engineering life cycle vocabulary (requirements, design, implementation, testing, configuration management); awareness that the plant licensing basis decides which RG revision applies.

Use this skill for questions about how the NRC frames software assurance for digital computer software in nuclear power plant safety systems: which Regulatory Guide answers which life cycle question, what a software requirements specification or a software configuration management plan should contain, how verification and validation with reviews and audits are organized, what test documentation and unit testing should produce, and what NRC staff examine in a BTP 7-14 software review of planning documents, implementation, and design outputs. The pack answers with the NRC's own guidance, cited by chapter and source row.

## How to Use This Skill

- **Without arguments**: read the Core Frameworks below for the seven-source map, the six-RG life cycle structure, and the shape of a BTP 7-14 staff review.
- **With a topic**: use the Topic Index to find the chapter, then ask directly (e.g. "what belongs in a software configuration management plan", "what does BTP 7-14 check in a design output", "what are the qualities of a good software requirements specification").
- **With a chapter**: ch01 orientation (which document answers which question); ch02 life cycle processes and planning-document reviews; ch03 requirements specifications; ch04 configuration management plans; ch05 verification, validation, reviews, and audits; ch06 test documentation and unit testing; ch07 BTP 7-14 review of implementation and design outputs; ch08 endorsed-standards orientation.

Supporting files: `glossary.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### Regulatory Guides, the SRP, and BTP 7-14: how the pieces fit
Three documents at three levels. NRC regulations set the high-level software requirements for safety-system instrumentation and control. **Regulatory Guides (RGs)** describe one way the agency considers acceptable for meeting them: following an RG is voluntary in the legal sense, and an applicant may propose alternatives with adequate demonstration, but the RG path is the well-traveled one. The **Standard Review Plan (SRP, NUREG-0800)** is the staff's own guidance for reviewing applications; it does not impose new requirements, it tells reviewers what to check. **BTP 7-14** is a branch technical position inside SRP Chapter 7 that applies both ideas to digital computer software: its background grounds staff acceptance of software in acceptable life cycle plans, evidence that the plans were followed, and design outputs the process produced, gives the regulatory basis for software reviews, and draws its review approach from NUREG/CR-6101 and the SRP Appendix 7.0-A review process; it then states what information an applicant should provide and sets the acceptance criteria the staff applies to plans, implementation, and design outputs. The mental model: the six RGs tell applicants what to do; BTP 7-14 tells reviewers what to look for. They are two perspectives on one body of practice, and the pack keeps both visible: ch02-ch06 carry the RG voice, ch07 carries the staff-review voice, and ch01 introduces the family as a whole.

### The six-RG life cycle map
The July 2013 family divides software assurance by life cycle concern. **RG 1.173** covers developing software life cycle processes: defining the processes themselves, their inputs and outputs, and integrating them. **RG 1.172** covers the software requirements specification, including for complex electronics, and the qualities a requirements set should have. **RG 1.169** covers software configuration management plans: configuration identification, configuration control, interface control, and configuration status accounting. **RG 1.170** covers test documentation across test plans, designs, cases, procedures, and results; **RG 1.171** covers unit testing of individual software units. **RG 1.168** is the umbrella: verification and validation (its staff positions cover software integrity, software reliability, independence of software verification and validation, conformance of materials, quality assurance, tools for software development, and verification and validation tasks) plus reviews and audits. The mental model for placing any question: 1.173 builds the process, 1.172 specifies the software, 1.169 controls change, 1.170 and 1.171 produce test evidence, and 1.168 audits the whole. Each guide also endorses a matching IEEE standard (828 to 1.169, 829 to 1.170, 830 to 1.172, 1008 to 1.171, 1012 and 1028 to 1.168, 1074 to 1.173), so the family maps one-to-one onto the standards named in ch08. The six guides share a common skeleton (purpose, discussion, staff regulatory guidance, implementation), so an answer from one family member reads like the others.

### What staff examine: the BTP 7-14 review structure
BTP 7-14 runs from background through review areas. It first describes the software aspects of the application and the information to be reviewed, then sets acceptance criteria in three blocks. **Planning (B.3.1)**: the software management plan (SMP) and the software development, quality assurance (SQAP), integration, installation, maintenance, training, operations, and safety (SSP) plans (B.3.1.1 to B.3.1.9), plus the verification and validation plan review (B.3.1.10), the configuration management plan review (B.3.1.11), and the test plan review (B.3.1.12). **Implementation (B.3.2)**: criteria for implementing the requirements, architecture, and design in code. **Design outputs (B.3.3)**: the software requirements specification (SRS), software architecture description (SAD), and software design specification (SDS), then the code listings (CL), system build documents (SBDs), installation configuration tables (ICTs), operations manuals (OMs), software maintenance manuals (SMMs), and software training manuals (STMs) (B.3.3.1 to B.3.3.9). **B.4** closes with review procedures: how the staff sequences the review and what it does with findings. The mental model: a review walks plans, then implementation, then outputs, and each criterion asks whether the submitted material is complete, correct, consistent, and traceable.

### The edition rule and the name-only rule
Two rules govern every answer. **The edition rule**: this pack pins RG 1.168 Rev 2 and RG 1.169 to 1.173 Rev 1 (all July 2013) and BTP 7-14 Rev 6 (August 2016). Which revision actually applies to a given plant is decided by its licensing basis: a plant committed to an earlier revision is reviewed against that revision, and revisions are not retroactive. Cite the pinned edition, then flag the licensing-basis caveat rather than assuming currency. The agency does revise guidance over time, so currency questions deserve a check of the current NRC listing, and later agency actions are otherwise out of scope. **The name-only rule**: each RG endorses IEEE standards with stated qualifications (603-1991 for safety-system criteria, 7-4.3.2-2003 for programmable digital devices, and 828, 829, 830, 1008, 1012, 1028, and 1074 matching the life cycle topics), and the family references IEC 60880, IEC 61513, IEC 62138, and IAEA guides. Those texts are copyrighted; the pack restates only what the NRC documents say about them, including the qualifications and conditions the RGs attach to the endorsement, and cites the standards by designation and edition. Chapter 08 holds that orientation layer and names the adjacent current documents (RG 1.152 Rev 4 for non-safety programmable logic controllers, BTP 7-18, BTP 7-19 Rev 9) that sit outside the pack.

---

## Chapter Index

| Ch | File | Sources (pages) | Coverage | Cluster |
|----|------|-----------------|----------|---------|
| 01 | [ch01-nrc-software-assurance-framework](chapters/ch01-nrc-software-assurance-framework.md) | S7 (pp 2-9) + S1-S6 purpose/background slices | Which document answers which question; each guide's purpose and discussion; the framework for assuring digital safety-system software | Regulatory Framework & Staff Review |
| 02 | [ch02-software-life-cycle-processes](chapters/ch02-software-life-cycle-processes.md) | S6 (pp 7-10) + S7 (pp 10-36) | Developing life cycle processes; information to be reviewed; acceptance criteria for planning and for the nine software plans B.3.1.1-B.3.1.9 | Life Cycle & Requirements |
| 03 | [ch03-software-requirements-specifications](chapters/ch03-software-requirements-specifications.md) | S5 (pp 6-9) | Staff regulatory guidance on the content and qualities of a software requirements specification for software and complex electronics | Life Cycle & Requirements |
| 04 | [ch04-software-configuration-management-plans](chapters/ch04-software-configuration-management-plans.md) | S2 (pp 6-10) + S7 (pp 41-43) | Configuration management plan content (identification, control, interface control, accounting); B.3.1.11 SCMP review | Life Cycle & Requirements |
| 05 | [ch05-verification-validation-reviews-audits](chapters/ch05-verification-validation-reviews-audits.md) | S1 (pp 6-11) + S7 (pp 37-40) | Verification and validation, the life cycle reviews, and audits; B.3.1.10 SVVP review | Verification & Testing |
| 06 | [ch06-test-documentation-and-unit-testing](chapters/ch06-test-documentation-and-unit-testing.md) | S3 (pp 7-10) + S4 (pp 6-7) + S7 (pp 44-45) | Test documentation (plans, designs, cases, procedures, results); unit testing; B.3.1.12 STP review | Verification & Testing |
| 07 | [ch07-btp-7-14-staff-software-review](chapters/ch07-btp-7-14-staff-software-review.md) | S7 (pp 45-68) | B.3.2 implementation acceptance; B.3.3 design-output acceptance (requirements, architecture, design, implementation, integration, and installation outputs); B.4 review procedures | Regulatory Framework & Staff Review |
| 08 | [ch08-endorsed-standards-and-adjacent-guidance](chapters/ch08-endorsed-standards-and-adjacent-guidance.md) | orientation (name-only X1-X16; no source slice) | Endorsed IEEE standards, IEC 60880/61513/62138, and IAEA guides by designation and edition; adjacent NRC documents (RG 1.152 Rev 4, BTP 7-18, BTP 7-19 Rev 9) named | Regulatory Framework & Staff Review |

## Topic Index

- Acceptance criteria for design outputs → ch07
- Acceptance criteria for implementation → ch07
- Acceptance criteria for planning → ch02
- Audits → ch05
- BTP 7-14 review structure → ch01, ch07
- Code listings (CL) review → ch07
- Complex electronics requirements → ch03
- Configuration identification → ch04
- Configuration management plan (SCMP) review → ch04
- Configuration status accounting → ch04
- Design outputs → ch07
- Endorsed IEEE standards (name-only) → ch08
- IAEA guides (name-only) → ch08
- IEC 60880 / 61513 / 62138 (name-only) → ch08
- Installation and integration plans → ch02
- Installation configuration tables (ICTs) review → ch07
- Life cycle processes, developing → ch02
- Licensing basis and applicable revision → ch01, ch08
- Maintenance and training plans → ch02
- Operations and safety plans → ch02
- Requirements traceability → ch03, ch07
- Review procedures (B.4) → ch07
- Software architecture description (SAD) → ch07
- Software design specification (SDS) → ch07
- Software development and management plans → ch02
- Software integrity, software reliability, independence of V&V, conformance of materials, quality assurance, tools for software development, V&V tasks (RG 1.168 staff positions) → ch05
- Software quality assurance plan → ch02
- Software requirements specification (SRS) → ch03, ch07
- Software test plan (STP) review → ch06
- Software verification and validation plan (SVVP) review → ch05
- Standard Review Plan (NUREG-0800) → ch01, ch07
- System build documents (SBDs) → ch07
- Test documentation → ch06
- Unit testing → ch06
- Verification and validation → ch05

## Supporting Files

- `glossary.md`: key terms (BTP, CL, ICT, ML accession, OM, SAD, SBD, SDS, SIntP, SInstP, SMaintP, SMP, SOP, SQAP, SRP, SRS, SSP, STM, STP, STrngP, SVVP) with chapter references.
- `cheatsheet.md`: decision rules (which document answers which question, which chapter, which BTP 7-14 review section applies, which edition governs).

## Scope & Limits

- **NRC staff guidance only.** The pack restates six Regulatory Guides and BTP 7-14. Other SRP Chapter 7 sections, NUREG/CR contractor reports, and non-US frameworks are outside it. RG 1.152 Rev 4 (July 2023) and BTP 7-19 Rev 9 (May 2024) are current adjacent NRC documents not covered here; BTP 7-18 and SRP Appendix 7.1-D are likewise named only.
- **Endorsed standards are citation-only.** IEEE Std 603-1991, 7-4.3.2-2003, 828-2005, 829-2008, 830-1998, 1008-1987, 1012-2004, 1028-2008, and 1074-2006, IEC 60880 (ed 2.0:2006), IEC 61513 (ed 2.0:2011), IEC 62138 (ed 2.0:2018), and IAEA guides are copyrighted or rights-reserved; no standard text, table, or clause wording appears here, only designation-and-edition citations and the NRC's own discussion of them. Chapter 08 holds the orientation.
- **Editions are pinned.** The source set is the July 2013 RGs and BTP 7-14 Rev 6 (August 2016). A 2024-01-02 periodic review decided to revise RG 1.168 Rev 2, and no revision has been issued, so Rev 2 remains the current document. Later agency actions, newer revisions, and draft guides are out of scope; the plant licensing basis, not this pack, decides which revision binds a given plant. Check the current sources before relying on any single requirement.
- **Not advice.** Content is synthesized reference notes (verbatim passages capped at two sentences); it is not legal or licensing advice and not a substitute for the source documents, the licensing basis, or counsel.
