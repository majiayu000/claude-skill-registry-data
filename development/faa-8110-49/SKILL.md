---
name: faa-8110-49
description: "Reconstructed reference notes on US FAA approval guidance for airborne software and airborne electronic hardware, built from four public-domain sources (FAA Order 8110.49A, AC 20-115D, AC 20-152A, AC 00-69; documents dated 2017-07-21 to 2022-10-07, pinned 2026-10-12). Use for how FAA certification staff plan and conduct software reviews (certification liaison, desk versus on-site review, review planning agreements), how the level of FAA involvement (LOI) is picked and scored with the Appendix A worksheets, how software conformity inspection works (software part and installation conformity, ASE and ASI tasks, Form 8120-10), what AC 20-115D recognizes and how DO-178B processes and tool qualification transition to DO-178C/DO-330 (supplements, FLS, UMS, legacy software changes), and what AC 20-152A adds for airborne electronic hardware (simple versus complex custom devices, robustness and HDL code coverage, tool assessment, previously developed hardware, COTS IP, COTS devices, circuit board assemblies), and what AC 00-69 adds as best practices for change impact analysis, data and control coupling, and design-level error handling (best practices, not guidance and not a means of compliance). SCOPE LIMITS: FAA guidance only, and guidance is not regulation (ACs are acceptable means, not the only means); no RTCA DO-178C or DO-254, EUROCAE ED-12C or ED-80, supplement, or SAE ARP text, which are copyrighted and named only (see the avionics-signpost pack); no AC 00-72 (named, not packed); no DO-178C software-level objective tables; no EASA AMC 20-115D or AMC 20-152A content (use easa-rules); reflects the pinned source dates, not later FAA actions; synthesized reference notes, not legal advice and not a substitute for the source documents. LICENCE: Public Domain (US Government work, 17 U.S.C. 105)."
---

<!-- argument-hint: [software review, LOI, conformity inspection, DO-178C transition, FLS/UMS, custom device, COTS, chapter number] -->

# FAA Airborne Software and AEH Approval Guidance
**Source**: Federal Aviation Administration. Adapted from the sibling 2026-09-27 prototype build and re-checked against the 2026-10-12 FAA source pin, the four documents vetted in LICENSE as rows S1-S4 | **Licence**: Public Domain (US Government work, 17 U.S.C. 105) | **Chapters**: 13

## When to use

**Prerequisites:** none, plain Markdown; no MCP server, API key, or licence tier needed at runtime.

Use this skill for questions about how the FAA reviews and approves the software and airborne electronic hardware sides of a certification project: how a software review is planned and what its objectives are, how much FAA involvement a project should expect and how the worksheets score it, what a software conformity inspection covers and when Form 8120-10 is used, what AC 20-115D recognizes and how DO-178B-era processes carry forward, and what AC 20-152A requires for custom devices, COTS IP, COTS devices, and circuit board assemblies. The pack answers with the FAA's own frameworks, cited by chapter and source row.

## How to Use This Skill

- **Without arguments**: read the Core Frameworks below for the review process, the level-of-involvement logic, conformity inspection, and the recognition chain from FAA guidance to the RTCA/EUROCAE standards.
- **With a topic**: use the Topic Index to find the chapter, then ask directly (e.g. "which LOI worksheet applies at software level B", "does this COTS IP block need AC 20-152A objectives").
- **With a chapter**: ch01 orientation (which document answers which question); ch02-ch04 the FAA review, involvement, and conformity machinery of Order 8110.49A; ch05-ch06 AC 20-115D software development assurance and legacy software; ch07-ch10 AC 20-152A airborne electronic hardware.

Supporting files: `glossary.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### The recognition chain: how FAA guidance points at industry standards
The FAA does not write avionics development standards; it recognizes them. **Advisory Circulars are the recognition instrument**: AC 20-115D recognizes EUROCAE ED-12C / RTCA DO-178C for airborne software, together with the supplement set (DO-330 tool qualification, DO-331 model-based development, DO-332 object-oriented technology, DO-333 formal methods, with EUROCAE ED-215 to ED-218 as equivalents), and cancels AC 20-115C. AC 20-152A recognizes ED-80 / DO-254 for airborne electronic hardware, cancels AC 20-152, and layers FAA-specific objectives on top for custom devices, COTS IP, COTS devices, and circuit board assemblies. **Order 8110.49A is the internal instruction to FAA staff**: how AIR offices and designees apply DO-178B/C when working certification projects (TC, STC, ATC, ASTC, TSOA). The mental model for reading any question: first decide whether it is about what the standard demands (paywalled, out of this pack) or about what the FAA does with it (in this pack). References to DO-178C in the order include its supplements and DO-330 as applicable.

### The software review process (Order 8110.49A, Ch 2)
The **certification liaison process** (DO-178B/C Section 9) is the vehicle for communication between applicant and authority, and the authority may review software life cycle processes and data to assess compliance (Sections 9.2 and 10.3). Reviews run **desk or on-site**; on-site buys access to software personnel, automation, and test setup, and both forms can be delegated to authorized designees. On-site reviews stand on nine practical arrangements agreed with the developer: scope, dates and locations, authority personnel, designees, agendas and expectations, data to be made available before and at the review, procedures, resources, and how results (including corrective actions) will be communicated. The review process serves four objectives: timely technical interpretation of the certification basis and applicable objectives; visibility into implementation compliance and data; objective evidence that the software adheres to its approved plans; and the chance to monitor designee work.

### Level of FAA involvement (Order 8110.49A, App A, criteria also in Ch 2)
Involvement is sized early, documented, and proportional: more scrutiny where risk and novelty are higher, less where experience is deep. Eight factors drive it: software level from the system safety assessment; product attributes (size, complexity, functionality, novelty, design); new technologies or unusual design features; novel software methods or life cycle models; the applicant's track record with DO-178B/C objectives; designee availability and experience; DO-178B/C Section 12 issues; and software issue papers. **Appendix A carries three worksheets**, examples not mandates: Worksheet 1 maps software level to involvement (D = LOW; C = LOW or MEDIUM; B and A = MEDIUM or HIGH); Worksheet 2 scores experience and demonstrated capability on 0-to-max scales (certification experience, DO-178B/C experience, older-standard experience, other standards, ability to consistently produce compliant software); Worksheet 3 converts the Worksheet 2 total into an involvement level. The mental model: involvement is a dial, not a gate; the worksheets justify where it is set.

### Software conformity inspection (Order 8110.49A, Ch 4)
Conformity confirms the article matches the approved type design (14 CFR 21.33(b)). For software, type design is at minimum the DO-178B Section 9.4 data: Software Requirements Data, Design Description, Source Code, Executable Object Code, the Software Configuration Index, and the Software Accomplishment Summary. Continuous compliance is assessed through **ASE (Aviation Safety Engineer) or authorized DER reviews** across the life cycle; conformity inspection adds two documented checkpoints before TC/STC/ATC/ASTC/TSOA issuance, at **test acceptance** and **installation**. **Software part conformity** covers each test flown or run for certification credit: the ASE establishes the baseline (by review, or by a DER's Form 8110-3 stating the baseline is approved for FAA testing), checks the test configuration against the test baseline, verifies artifacts are identified and controlled, confirms tool qualification status, and raises **FAA Form 8120-10, Request for Conformity**, so MIDO/MISO staff (ASI) can witness and verify. Special-purpose test software used for environmental qualification is verified, validated, and configured as part of the test setup. **Installation conformity** then verifies the as-installed software matches the approved configuration.

### DO-178B to DO-178C transition (AC 20-115D)
AC 20-115D recognizes ED-12C/DO-178C and describes the standard's method: objectives for life cycle processes, activities that satisfy them, and evidence showing satisfaction. It also defines a **transition path**: applicants with established ED-12B/DO-178B processes may keep using them (including tool qualification processes) for new development where the processes show no known process deficiencies (audits, reviews, open problem reports), were used on a certified product at an equal or higher software level, and, where model-based development, object-oriented technology, or formal methods are involved, were previously found acceptable by the FAA. **Parameter Data Item** configuration data has its own criteria. Life cycle data is submitted to the extent needed to satisfy the applicable objectives, and tool qualification moves to **DO-330** (which supersedes the DO-178B section 12.2 approach, with transition guidance the AC summarizes). Section 8 to 9 material covers **supplement use, field-loadable software (FLS), user-modifiable software (UMS)**, and a legacy software modification flow chart for previously certified software.

### Best practices companion (AC 00-69)
AC 00-69, issued the same day as AC 20-115D, states that it is best practices and not guidance. It is complementary information to ED-12C/DO-178C and to AC 20-115D. It is not an acceptable means of compliance and it does not replace AC 20-115D. Three blocks: change impact analysis (what a CIA identifies and which change classes it addresses, deepening the 9.b(4) requirement ch06 already states), data coupling and control coupling (distinct analyses, both required), and design-level error handling (foreseeable error sources, mitigated in requirements, runtime protection named for levels A and B). DO-248C FAQ #67 and DO-333 are named only.

### Airborne electronic hardware: custom devices and the AC 20-152A additions (S3)
AC 20-152A applies DO-254/ED-80 to **custom devices** and splits them by classification. A **complex custom device** (one whose failure cannot be shown sufficiently by testing alone, in ED-80/DO-254 terms) takes the full standard: ED-80/DO-254 is recognized as the industry standard for its development assurance, plus the AC's additional objectives and clarifications in its sections 5.5 to 5.11. A **simple custom device** can take significantly reduced life cycle data, but two things do not shrink: it must perform its intended function and stay under configuration management, so it can be reproduced, conformed, and analyzed for continued operational safety. The AC then extends the same objective-based style to **verification** (robustness, a stated HDL code coverage method), **tool assessment and qualification**, **previously developed hardware**, **COTS intellectual property** (provider assessment, planning, verification, Appendix B considerations), **COTS devices**, and **circuit board assemblies (CBA)**. Single event effects are explicitly out of the AC's scope. The recognition chain closes the loop: hardware questions route through AC 20-152A exactly as software questions route through AC 20-115D.

---

## Chapter Index

| Ch | File | Sources (pages) | Coverage | Cluster |
|----|------|-----------------|----------|---------|
| 01 | [ch01-airborne-approval-map](chapters/ch01-airborne-approval-map.md) | S1 + S2 + S3 (orientation; authored last in Task 8) | Which document answers which question; FAA AC to RTCA/EUROCAE recognition chain; 8110.49 Chg 2 to 8110.49A history and where deleted chapters went | Certification Liaison & Oversight |
| 02 | [ch02-software-review-process](chapters/ch02-software-review-process.md) | S1 Ch2 (pp 8-9; 2 pp) | Certification liaison, desk vs on-site review, review planning agreements, objectives of the review process | Certification Liaison & Oversight |
| 03 | [ch03-level-of-faa-involvement](chapters/ch03-level-of-faa-involvement.md) | S1 App A (pp 15-18; 4 pp). LOI criteria text also in S1 Ch2 | LOI criteria (software level, product attributes, novelty, applicant experience, designees) and worksheet scoring | Certification Liaison & Oversight |
| 04 | [ch04-software-conformity-inspection](chapters/ch04-software-conformity-inspection.md) | S1 Ch4 (pp 11-14; 4 pp) | Software part conformity, installation conformity, ASE and ASI tasks, Form 8120-10 request | Certification Liaison & Oversight |
| 05 | [ch05-do-178c-recognition-and-transition](chapters/ch05-do-178c-recognition-and-transition.md) | S2 secs 1-6 + 10 (pp 1-4 body of 1-6; sec 10 on pp 10-12 before sec 11; ~6-7 pp usable after dropping reserved/related/where-to-find) | What AC 20-115D recognises, DO-178B process reuse for new development, life cycle data submittal, tool qualification transition | Software Development Assurance |
| 06 | [ch06-legacy-software-fls-ums](chapters/ch06-legacy-software-fls-ums.md) | S2 secs 8-9 (pp 4-10; ~6-7 pp) | Supplement use, field-loadable software, user-modifiable software, legacy software modification flow chart | Software Development Assurance |
| 07 | [ch07-aeh-custom-devices](chapters/ch07-aeh-custom-devices.md) | S3 secs 1-5.5 (pp 1-8; 8 pp). Excludes 5.10 (moved beside 5.6-5.9) | DO-254 applicability, simple vs complex classification, assurance for complex and simple custom devices | Airborne Electronic Hardware |
| 08 | [ch08-aeh-verification-tools-reuse](chapters/ch08-aeh-verification-tools-reuse.md) | S3 secs 5.6-5.10 (pp 8-12; ~4-5 pp) | Robustness, HDL code coverage method, tool assessment and qualification, previously developed hardware, Appendix A clarifications | Airborne Electronic Hardware |
| 09 | [ch09-aeh-cots-ip](chapters/ch09-aeh-cots-ip.md) | S3 sec 5.11 (pp 12-19; 8 pp) | COTS IP selection, provider assessment, planning, verification, Appendix B considerations for COTS IP | Airborne Electronic Hardware |
| 10 | [ch10-cots-devices-and-cbas](chapters/ch10-cots-devices-and-cbas.md) | S3 secs 6-7 (pp 19-25 until sec 8; ~6-7 pp) | COTS device applicability and complexity assessment, circuit board assembly development assurance | Airborne Electronic Hardware |
| 11 | [ch11-software-change-impact-analysis](chapters/ch11-software-change-impact-analysis.md) | S4 sec 3.1 | CIA best-practice checklist: what a change impact analysis identifies and which change classes it addresses | Software Development Assurance |
| 12 | [ch12-data-and-control-coupling-practices](chapters/ch12-data-and-control-coupling-practices.md) | S4 sec 3.2 | Data coupling and control coupling as distinct, both-required analyses | Software Development Assurance |
| 13 | [ch13-design-level-error-handling](chapters/ch13-design-level-error-handling.md) | S4 sec 3.3 | Foreseeable error sources, mitigation in requirements, runtime protection at levels A and B | Software Development Assurance |

## Topic Index

- AC 00-69: best practices companion, not guidance → ch01, ch11, ch12, ch13
- AC 20-115D: what it recognizes and cancels → ch01, ch05
- AC 20-152A: scope and additions → ch01, ch07
- Aviation Safety Engineer (ASE) tasks → ch04
- Cancellation history (AC 20-115C, AC 20-152, Order 8110.49 Chg 2) → ch01
- CBA (circuit board assembly) development assurance → ch10
- Certification liaison process → ch02
- Change impact analysis checklist → ch11
- COTS devices → ch10
- COTS intellectual property (IP) → ch09
- Data coupling and control coupling → ch12
- Desk review vs on-site review → ch02
- Design-level error handling → ch13
- Designees (DER, ASI, involvement of) → ch02, ch03
- DO-178B process reuse for new development → ch05
- DO-254 / ED-80 applicability → ch07
- FAA Form 8110-3 (DER statement of compliance) → ch04
- FAA Form 8120-10 (Request for Conformity) → ch04
- Field-loadable software (FLS) → ch06
- HDL code coverage method → ch08
- Legacy software modification flow chart → ch06
- Level of FAA involvement (LOI) criteria and worksheets → ch03
- Life cycle data submittal → ch05
- Parameter Data Item / configuration data → ch05
- Previously developed hardware → ch08
- Recognition chain (FAA AC to RTCA/EUROCAE standard) → ch01
- Review planning agreements → ch02
- Robustness (AEH verification) → ch08
- Simple vs complex custom devices → ch07
- Software part conformity inspection → ch04
- Software installation conformity inspection → ch04
- Supplement use (DO-330 to DO-333 / ED-215 to ED-218) → ch05, ch06
- Tool qualification (DO-330 transition; AEH tool assessment) → ch05, ch08
- Type design for software (DO-178B 9.4 data items) → ch04
- User-modifiable software (UMS) → ch06

## Supporting Files

- `glossary.md`: key terms (ASE, ASI, conformity, custom device, DAL, FLS, LOI, UMS) with chapter references.
- `cheatsheet.md`: decision rules (which document governs, which worksheet, which conformity path, which AC objectives apply).

## Scope & Limits

- **FAA scope only.** This pack restates US FAA guidance: Order 8110.49A and ACs 20-115D/20-152A. It carries no RTCA DO-178C or DO-254, EUROCAE ED-12C or ED-80, supplement (DO-330 to DO-333, ED-215 to ED-218), or SAE ARP4754B/ARP4761A text; those standards are copyrighted and are named only. For designations, editions, and where to buy, use the avionics-signpost pack.
- **No standard internals.** Software-level objective tables (levels A to E), DO-178C annex tables, and DO-254 process details live in the paywalled standards; this pack covers what the FAA documents themselves say about applying them.
- **EASA not covered.** AMC 20-115D and AMC 20-152A are outside this pack; easa-rules is the pack that answers EASA software and AEH means-of-compliance questions.
- **AC 00-69 is best practices.** It is not guidance and not a means of compliance. AC 00-72 (AEH best practices) is named and not packed.
- **Guidance is not regulation.** ACs describe an acceptable means, not the only means, and do not bind the public; orders bind FAA staff, not applicants. Nothing here is legal advice or a substitute for the source documents or your certification authority.
- **Dates are pinned.** The source set is pinned to the 2026-10-12 verification; the documents are dated 2017-07-21 to 2022-10-07, and the notes were built 2026-09-27 in the sibling prototype. Later FAA actions, policy changes, and new or revised ACs are out of scope; check the FAA website for current versions before relying on a single requirement.
