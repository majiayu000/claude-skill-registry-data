---
name: physio-clinical-reasoning
description: "Structure safety-first, evidence-based physiotherapy reasoning for a patient case. Use for vaka/case prompts involving symptoms, examination findings, surgery or injury, triage, differential hypotheses, ICF problem lists, red/yellow/blue/black flags, goals, prognosis, treatment options, contraindications, referral, reassessment, or return-to-activity criteria across MSK, neurological, cardiopulmonary, pediatric, geriatric, pelvic, oncology, and postoperative rehabilitation. Turkish triggers: hasta değerlendirmesi, klinik akıl yürütme, FTR vaka analizi. This is decision support, not remote diagnosis or clearance."
---

# Physio Clinical Reasoning

## Mandatory first reads

Read [safety core](references/safety-core.md) and [clinical reasoning framework](references/clinical-reasoning-framework.md). Pass the safety and data-sufficiency gates before forming a rehabilitation plan.

## Workflow

1. **Structure the case.** Extract age/development, reason for referral, onset/mechanism, time course, medical/surgical history, medications, comorbidities, imaging/labs, vital/system review, prior function, living/work/sport demands, preferences, and goals.
2. **Identify decisive missing data.** Ask only questions that materially change escalation, eligibility, or plan. If they remain unanswered, create conditional branches—not false certainty.
3. **Assign an escalation class.** Use `emergency now`, `urgent`, `concurrent consultation`, or `physiotherapy management with safety-net`. State the action and time window. Do not diagnose serious pathology from a single sign.
4. **Write a one-sentence problem representation.** Include time course, main functional loss, setting, and important modifiers.
5. **Rank hypotheses.** Use `most likely`, `plausible`, and `must not miss`; show supporting, weakening, and missing evidence for each. Do not present a remote hypothesis as a definitive diagnosis.
6. **Build an ICF problem list.** Separate body functions/structures, activity capacity, real-world performance, participation, environmental facilitators/barriers, and personal/contextual factors.
7. **Map recovery barriers and safeguards.** Treat red, yellow, blue, and black flags as actionable information—not labels or personality judgments. Handle self-harm, abuse, neglect, or safeguarding concerns through a separate local pathway.
8. **Gather targeted current evidence.** Invoke `$physio-evidence-search` for the relevant population and decisions; use `$physio-study-appraisal` when a pivotal paper needs scrutiny.
9. **Set shared goals.** Anchor goals in patient priorities and meaningful function. Make them measurable and time-bounded; distinguish short-, medium-, and long-term goals.
10. **Compare options.** Classify first-line, adjunct, not recommended, and uncertain options. Show expected benefit, harm, burden, alternatives—including no change/watchful waiting—certainty, and patient fit.
11. **Select outcome measures.** Invoke `$physio-outcome-measures` for the smallest sufficient baseline and reassessment set.
12. **Define the plan envelope.** For every option state target problem, evidence, eligibility, study dose, contraindications/precautions, monitoring, and decision criteria. Invoke `$physio-program-design` only after safety and restrictions are clear.
13. **Estimate prognosis as a range.** State expected course, confidence, favorable/unfavorable modifiers, and reassessment date. Do not count natural recovery as treatment effect.
14. **Create a safety-net.** Specify what change, what action, and how soon.

## Population and setting gates

Before patient-applicable dosage or progression, verify relevant modules:

- postoperative protocol, weight-bearing status, wound/implant/device, and surgeon restrictions;
- child development, guardian consent, child assent, safeguarding, and population-specific evidence;
- pregnancy week or postpartum interval and obstetric warning signs;
- pelvic-health consent, privacy, trauma-informed care, chaperone preference, and clinician training;
- neurological deterioration, autonomic dysreflexia risk, cognition/communication, and falls;
- cardiopulmonary symptoms, disease-specific vital targets, medication effects, and device reliability;
- oncology treatment phase, bone stability/metastasis, infection/bleeding risk, lines/ports, anemia, and cardiotoxicity;
- remote-care location, emergency plan, helper, environment, equipment, and suitability.

Do not provide return-to-sport, return-to-work, driving, work-capacity, or medical clearance without the required in-person examination, objective criteria, protocol/medical input, and jurisdictional authority. Describe criteria and missing evidence instead.

## Output

1. Safety and referral decision
2. Critical missing information
3. Problem representation
4. Ranked hypotheses with supporting/weakening/missing evidence
5. ICF problem list and actionable flags
6. Patient priorities, shared goals, and prognosis range
7. Evidence summary and contradictions
8. Option comparison
9. Plan envelope with dose provenance and decision rules
10. Contraindications, precautions, and medication/device considerations
11. Outcome measures and reassessment schedule
12. Safety-net, uncertainty, jurisdiction, and sources

If emergency concern is plausible, stop after the immediate action and safety-net. Do not continue into a routine treatment plan.
