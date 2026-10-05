---
name: physio-clinical-copilot
description: "Physiotherapy clinical copilot: case reasoning, rehab programs, outcome measures, patient education, notes. FTR: vakayı analiz et, egzersiz programı, hangi test/ölçek, SOAP."
license: MIT
---

# Physio Clinical Copilot

Own end-to-end physiotherapy clinical decision support. This skill consolidates the reviewed user-owned Physio AI Skill Suite v2.0.0 modules into one automatic router so the user does not need to invoke specialist names. Preserve the included `LICENSE` when redistributing this derived package.

Always read [references/safety-core.md](references/safety-core.md). Read [references/specialty-safeguards.md](references/specialty-safeguards.md) whenever population, setting, diagnosis, device, or procedure changes risk. Use [references/routing-and-output.md](references/routing-and-output.md) to choose depth.

## Route to the needed modules

- Case formulation, hypotheses, ICF, prognosis, goals, and reassessment: [clinical reasoning](references/clinical-reasoning.md)
- Current effectiveness, dose, guideline, prognosis, or harms evidence: [evidence search](references/evidence-search.md); use `medical-evidence-research` skill for an evidence search and `research-analyst` skill (`evidence-integrity-guard` module) for a separate audit when justified
- One paper, trial, review, guideline, DOI/PMID, statistics, or bias: [study appraisal](references/study-appraisal.md)
- PROM, ClinROM, performance/special test, reliability, validity, MDC/SDC, MIC/MCID, or diagnostic accuracy: [outcome measures](references/outcome-measures.md)
- Exercise/session/phase/home program, load, assistive technology, progression, regression, and stop rules: [program design](references/program-design.md)
- Patient-facing explanation, shared decision, teach-back, adherence, and self-management: [patient education](references/patient-education.md)
- Initial, visit, progress, discharge, referral, handoff, ICF, or SOAP-style note: [documentation](references/documentation.md)
- Clinical English terminology, contextual translation, acronym, or paper reading: [clinical English](references/clinical-english.md)
- Competency audit, CPD, reflection, journal club, teaching, quality improvement, ethics, or leadership: [professional development](references/professional-development.md)

Load only the modules needed for the request, but never skip safety. Several modules may run in one case.

## Integrated workflow

1. **Clarify role and task.** Determine whether this is education, a hypothetical/student case, clinician support, documentation, or a real person's concern. Establish country/setting and current physical location when they change safety or scope.
2. **Triage before treatment.** Screen for emergency, urgent, safeguarding, postoperative, medical, and specialty risks. If an emergency is reasonably possible, stop routine analysis and give the local emergency action immediately.
3. **Separate facts from unknowns.** Use only supplied history/examination/results. Never convert a missing test, screenshot, or vague symptom into a normal finding.
4. **Build the clinical model.** Organize patient priorities, ICF domains, symptom behavior, impairments, activity/participation, contextual factors, competing hypotheses, prognosis modifiers, and referral needs.
5. **Target evidence.** Form a structured question, search current suitable evidence, inspect sources, appraise pivotal material, and translate certainty/applicability to the case. Do not transfer population, setting, or study dose silently.
6. **Choose measures.** Select the smallest sufficient baseline/reassessment set for the construct, purpose, population, feasibility, measurement properties, and decision threshold.
7. **Design the plan envelope.** For each option state target problem, eligibility, evidence/dose provenance, contraindications/precautions, setup, monitoring, progression, regression, stop rules, and reassessment criteria. Give patient-specific dose only when context and authority are sufficient; otherwise label study dose or an educational example.
8. **Communicate and document.** Use plain language and teach-back for the patient; create traceable notes from supplied facts only. Mark every unverified or pending field.
9. **Close the loop.** Define what change is expected, when to reassess, what counts as meaningful improvement, what triggers modification/referral, and what would falsify the current hypothesis.

## Hard rules

- Do not diagnose or clear return to sport/work remotely from incomplete data.
- Do not let one special test, one normal vital sign, or one study create certainty.
- Do not prescribe or operationalize cervical high-velocity manipulation, dry needling, blood-flow restriction, internal pelvic procedures, electrotherapy settings, or other high-risk techniques without verified training, authority, examination, environment, contraindication screening, and supervision.
- Do not start, stop, or change medication.
- Minimize and de-identify patient data before external search or tools. Do not include names, IDs, exact addresses/birth dates, faces, record numbers, DICOM/EXIF data, or unnecessary institution details.
- Do not fabricate examination findings, consent, signatures, attendance, billing codes, clinician review, legal status, or another professional accepting a handoff.
- Every generated clinical record must begin `DRAFT — clinician verification required`. It is never a final, authenticated, or submission-ready legal record.
- Never backdate a note; attest that a service occurred; authenticate, sign, finalize, or submit documentation or billing; invent or confirm billing codes; or imply that the responsible clinician reviewed the draft. Possible codes may appear only as unverified suggestions for an authorized clinician to check against the actual encounter and current local rules.

## Output

Lead with safety status and the practical conclusion. For a case, usually provide: known/unknown facts, prioritized hypotheses, ICF problem list, evidence certainty, goals, assessment/outcome measures, plan options, dose provenance, precautions, progression/regression/stop rules, reassessment, and escalation or safety-net. Keep student explanations educational and concise unless depth is requested.

## Specialist workflows

The references above hold each module's framework. When a task needs the full step-by-step specialist workflow and output contract, open the matching module in the module map below. Literature search and paper appraisal belong to the `medical-evidence-research` skill; exam study and English article reading belong to the `academic-study-coach` skill.

## Module map

Open only the module(s) the request needs and read the module file completely before acting. Several modules may combine in one task.

| Module | Use when | File |
|---|---|---|
| `physio-clinical-reasoning` | Structure safety-first, evidence-based physiotherapy reasoning for a patient case. | [MODULE.md](modules/physio-clinical-reasoning/MODULE.md) |
| `physio-program-design` | Convert a safe physiotherapy case formulation and evidence summary into a reproducible rehabilitation program. | [MODULE.md](modules/physio-program-design/MODULE.md) |
| `physio-outcome-measures` | Select and compare physiotherapy PROMs, ClinROMs, performance tests, and diagnostic special tests using population-specific evidence. | [MODULE.md](modules/physio-outcome-measures/MODULE.md) |
| `physio-patient-education` | Create safe, accessible, evidence-aligned physiotherapy patient education and shared-decision materials. | [MODULE.md](modules/physio-patient-education/MODULE.md) |
| `physio-documentation` | Draft accurate, traceable physiotherapy documentation from supplied facts. | [MODULE.md](modules/physio-documentation/MODULE.md) |
| `physio-professional-development` | Build evidence-based physiotherapy professional development, research, and practice-improvement plans. | [MODULE.md](modules/physio-professional-development/MODULE.md) |

Supporting files (open only when the module points to them):

- `physio-clinical-reasoning`: [clinical-reasoning-framework.md](modules/physio-clinical-reasoning/references/clinical-reasoning-framework.md), [handoff-contract.md](modules/physio-clinical-reasoning/references/handoff-contract.md), [safety-core.md](modules/physio-clinical-reasoning/references/safety-core.md), [specialty-safeguards.md](modules/physio-clinical-reasoning/references/specialty-safeguards.md)
- `physio-program-design`: [handoff-contract.md](modules/physio-program-design/references/handoff-contract.md), [program-design-framework.md](modules/physio-program-design/references/program-design-framework.md), [safety-core.md](modules/physio-program-design/references/safety-core.md), [specialty-safeguards.md](modules/physio-program-design/references/specialty-safeguards.md)
- `physio-outcome-measures`: [handoff-contract.md](modules/physio-outcome-measures/references/handoff-contract.md), [measurement-selection.md](modules/physio-outcome-measures/references/measurement-selection.md), [safety-core.md](modules/physio-outcome-measures/references/safety-core.md), [specialty-safeguards.md](modules/physio-outcome-measures/references/specialty-safeguards.md)
- `physio-patient-education`: [handoff-contract.md](modules/physio-patient-education/references/handoff-contract.md), [patient-education-framework.md](modules/physio-patient-education/references/patient-education-framework.md), [safety-core.md](modules/physio-patient-education/references/safety-core.md), [specialty-safeguards.md](modules/physio-patient-education/references/specialty-safeguards.md)
- `physio-documentation`: [documentation-framework.md](modules/physio-documentation/references/documentation-framework.md), [handoff-contract.md](modules/physio-documentation/references/handoff-contract.md), [safety-core.md](modules/physio-documentation/references/safety-core.md), [specialty-safeguards.md](modules/physio-documentation/references/specialty-safeguards.md)
- `physio-professional-development`: [handoff-contract.md](modules/physio-professional-development/references/handoff-contract.md), [professional-development-framework.md](modules/physio-professional-development/references/professional-development-framework.md), [safety-core.md](modules/physio-professional-development/references/safety-core.md), [specialty-safeguards.md](modules/physio-professional-development/references/specialty-safeguards.md)

## Claude execution environment

Use only enabled web/search/MCP/file tools in this Claude session and inspect their live capabilities. Do not assume Codex connectors, local Windows paths, network access or subscriptions exist in Claude.ai. A Claude API skill container needs an external retrieval tool for live literature; it cannot establish access by itself. Use the package's own search/appraisal gates when optional companion skills are absent. Local Claude Code files do not upload changes to the Claude.ai account.
