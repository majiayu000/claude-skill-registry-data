---
name: med-device-eu
description: "Reconstructed reference notes on EU and UK medical-device software, built from six sources captured 2026-10-13: MDCG 2019-11 rev.1 (June 2025), MDCG 2020-6 (April 2020), MDCG 2020-13 (July 2020), MDCG 2020-7 (April 2020), MDCG 2020-8 (April 2020), and the MHRA software-applications guidance (2023-07-01) with its stand-alone software PDF. Use for SaMD qualification and classification, legacy-device clinical evidence, the clinical evaluation assessment report, the PMCF plan, and the PMCF evaluation report, under EU MDCG guidance or UK MHRA guidance. SCOPE LIMITS: EU MDR and UK MHRA device software only; no IEC 62304, ISO 13485, or ISO 14971 text; no MDR or IVDR regulation body text; MDCG guidance is not legally binding; MHRA guidance is UK-specific; synthesized notes, not legal advice. LICENCE: Per-document: European Commission reuse policy (Decision 2011/833/EU, CC BY 4.0, attribution and indication of changes) for the MDCG documents; Open Government Licence v3.0 for the MHRA guidance; reconstructed notes with attribution; official PDFs not redistributed."
---

<!-- argument-hint: [device software question, qualification, classification, clinical evidence, PMCF, chapter number] -->

# EU and UK Device Software Guidance (MDCG and MHRA)
**Sources**: MDCG 2019-11 rev.1 (June 2025), MDCG 2020-6 (April 2020), MDCG 2020-13 (July 2020), MDCG 2020-7 (April 2020), MDCG 2020-8 (April 2020), and MHRA Medical devices: software applications (2023-07-01) with its stand-alone software guidance | **Licence**: per-document, see LICENSE | **Chapters**: 8

## When to use
**Prerequisites:** none: plain Markdown; no MCP server, API key, or licence tier needed at runtime.

Use this pack for questions about software in and around medical devices on the EU and UK side: whether an app or stand-alone package qualifies as a device or an IVD and which risk class applies, what clinical evidence a legacy device needs under the MDR, how a notified body documents its assessment of a clinical evaluation, and what a post-market clinical follow-up plan commits to and how the evaluation report closes it. Both readings are taught: the MDCG guidance route for the EU and the MHRA guidance route for Great Britain.

## How to Use This Skill
- **Without arguments**: read the Core Frameworks below, covering the two-sided qualification question, the clinical-evidence standard for legacy devices and its assessment, and the plan-and-report loop for post-market clinical follow-up.
- **With a topic**: use the Topic Index to find the chapter, then ask directly (e.g. "is this symptom checker a device in the UK", "what class is this dosing software", "what does the PMCF plan have to promise").
- **With a chapter**: ch01 is the landing chapter for "which regime applies"; ch02-ch03 qualification and classification; ch04-ch05 clinical evidence and its assessment; ch06-ch07 PMCF plan and report; ch08 UK obligations after qualification.

## Core Frameworks & Mental Models

### SaMD qualification: one question, two readings (ch02 MDCG; ch03 and ch08 MHRA)
Qualification asks whether software is a device at all, and this pack teaches both readings. The EU route (ch02) runs the MDCG five-step decision: is it software, does it touch an Annex XVI product or drive or influence a hardware device, does it act on data beyond storage, archival, communication, simple search, or lossless compression, is that action for an individual patient's benefit, and does it carry a medical purpose of its own. Classification then follows Rule 11 of Annex VIII: class IIa for information used in diagnostic or therapeutic decisions, rising to IIb or III as the harm from wrong information rises; IIa to IIb for physiological monitoring; class I for everything else. The UK route (ch03) reads medical purpose from labelling, app-store text, and other claims, keeps a verifiability discretion for calculators the intended user can easily check, and draws the decision-support line by whether software reproduces a paper path or produces a diagnosis, prognosis, or individual risk figure. Once software qualifies on the GB market, the obligations follow (ch08): UKCA marking, a classification route, registration with the MHRA, essential requirements, and post-market duties. The mental model: both readings share an ancestor, so the medical-purpose test is similar; the divergences are in the details, and they bite hardest on calculators and decision support.

### Clinical evaluation: legacy evidence and the assessment report (ch04, ch05)
For a device CE marked under the old directives (ch04), sufficient clinical evidence is the present result of a qualified assessment, not a fixed dataset. The directive-era data carries over into a gap analysis against the MDR's narrower clinical-data definition and stricter equivalence rules, and each dataset is appraised for methodological quality and bias. Two rules carry weight: complaint and incident rates alone cannot prove safety, and where the evidence will not carry the claimed intended purpose, the fix is to narrow the purpose. Well-established technologies may run on a lower evidence level; the non-clinical route exists but is exceptional. The notified body's side of the same work is the assessment report (ch05): a per-section template whose verdicts map the manufacturer's clinical evaluation, with special sections for expert-panel consultation and the non-clinical route. The mental model: the manufacturer writes the evidence case, the assessment report grades it, and both stand on the MDR's evaluation stages.

### PMS and PMCF: the plan-and-report loop (ch06, ch07)
Post-market clinical follow-up is a continuous process that updates the clinical evaluation, run as a controlled document pair inside post-market surveillance. The plan (ch06) commits every activity to one of five aims, states where the need came from, justifies method, sample size, and endpoints, and fixes timelines at quarterly or yearly resolution; a decision not to run PMCF at all needs its own justification. The report (ch07) closes a named, versioned plan: every performed activity reported, deviations justified, findings discussed whether positive or negative, and every finding routed into the clinical evaluation report, the risk management file, the PMS plan, and the SSCP. The mental model: the plan promises, the report reconciles, and the conclusions feed the next round of all four documents.

---

## Chapter Index

| # | Chapter | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-eu-uk-device-software-orientation.md) | EU and UK orientation | Question-to-document map; MDR, IVDR, and UK MDR 2002 as the binding layers; guidance as non-binding but operative (S1-S6) |
| [ch02](chapters/ch02-samd-qualification-classification.md) | SaMD qualification and classification | The five-step qualification decision, Rule 11 sub-rules, the IVD MDSW track, rev.1 changes, modular placement (S1) |
| [ch03](chapters/ch03-mhra-software-qualification.md) | MHRA software qualification | The boundary test, the app examples, the calculator verifiability discretion, where the UK reading diverges from the MDCG one (S6) |
| [ch04](chapters/ch04-clinical-evidence-legacy-devices.md) | Clinical evidence for legacy devices | The sufficient-evidence definition, the gap analysis, appraisal tools, the evidence hierarchy, well-established technologies (S2) |
| [ch05](chapters/ch05-clinical-evaluation-assessment-report.md) | Clinical evaluation assessment report | CEAR sections A to H, per-section verdicts, the special sections for panel consultation and the non-clinical route (S3) |
| [ch06](chapters/ch06-pmcf-plan.md) | PMCF plan | The five aims, per-activity justification, registry and real-world evidence rules, the hard study requirement for implantable and class III devices (S4) |
| [ch07](chapters/ch07-pmcf-evaluation-report.md) | PMCF evaluation report | Plan-bound closure, per-activity reporting, the routing table, the conclusions loop (S5) |
| [ch08](chapters/ch08-mhra-uk-device-obligations.md) | MHRA UK device obligations | UKCA marking and placement, classification routes, essential requirements, registration, vigilance, field safety, end of life (S6) |

## Topic Index

- **SaMD qualification** → ch02, ch03
- **software classification** → ch02
- **legacy device clinical evidence** → ch04
- **clinical evaluation assessment report** → ch05
- **PMCF plan** → ch06
- **PMCF evaluation report** → ch07
- **MHRA software apps** → ch03
- **UKCA device software** → ch08
- **which regime applies** → ch01

## Supporting Files

- [glossary.md](glossary.md): the ten working terms (SaMD, legacy device, PMCF, PMS, clinical evaluation, CEAR, MDR, IVDR, UKCA, MDCG), each with the chapter that teaches it
- [cheatsheet.md](cheatsheet.md): decision shortcuts for the qualification question, the template to reach for, and which regime a question belongs to

---

## Scope & Limits

**Covers**: the EU and UK regulatory treatment of medical device software as stated in the six captured sources: qualification and classification, legacy-device clinical evidence, the clinical evaluation assessment report, the PMCF plan and evaluation report, and UKCA-era obligations for qualified software.

The binding text is the regulation: Regulation (EU) 2017/745 (MDR), Regulation (EU) 2017/746 (IVDR), and the UK Medical Devices Regulations 2002. This pack names them and does not reproduce them. A reader who needs the regulation text reads it on EUR-Lex or legislation.gov.uk.

The US counterpart is `fda-med-device`. That pack owns FDA questions, including 510(k) and De Novo pathways and FDA risk categorization; this pack does not answer FDA questions.

Scope limits, repeated: IEC 62304, ISO 13485, and ISO 14971 are named only and not reproduced; MDR and IVDR are named only and not reproduced; the pack is synthesized reference notes and not legal advice; MDCG guidance is not legally binding; MHRA guidance is UK-specific. These documents revise, so check for the current revision before relying on any single requirement.
