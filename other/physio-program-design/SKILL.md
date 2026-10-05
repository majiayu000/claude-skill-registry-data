---
name: physio-program-design
description: "Convert a safe physiotherapy case formulation and evidence summary into a reproducible rehabilitation program. Use for exercise prescription, FITT-VP, treatment phase/session design, home exercise, task practice, load management, dose, supervision, adherence, progression, regression, stop criteria, monitoring, return-to-activity criteria, gait-aid or assistive-technology selection, orthosis/prosthesis or wheelchair training, and adaptation to equipment or setting. Trigger on egzersiz programı, tedavi dozu, set/tekrar, progresyon, yürüme yardımcısı, ortez, protez, tekerlekli sandalye. Do not prescribe patient-applicable numbers or device configuration before safety, restrictions, baseline capacity, fit, environment, and qualified oversight are known."
---

# Physio Program Design

## Mandatory first reads

Read [safety core](references/safety-core.md) and [program design framework](references/program-design-framework.md). A program starts only after safety, scope, restrictions, baseline capacity, goals, and outcome measures are sufficiently clear. Invoke `$physio-clinical-reasoning` first when they are not.

## Workflow

1. **Confirm the decision envelope.** Record diagnosis/working classification, stage, irritability, medical stability, protocol/restrictions, medications/devices, contraindications, precautions, supervision, environment, and patient priorities.
2. **Map each target.** Use `ICF problem → meaningful goal → intervention mechanism → outcome measure → reassessment date`.
3. **Gather dose-relevant evidence.** Invoke `$physio-evidence-search`; extract the actual intervention using CERT/TIDieR fields. Distinguish guideline dose, trial dose, consensus, and clinician-titrated starting dose.
4. **Choose the minimum sufficient components.** Prioritize active, goal-linked elements. Add education, task/environment modification, assistive technology, manual/device intervention, or referral only when justified.
5. **Specify every component.** Mode/type, frequency, intensity/load, time per bout, repetitions/sets, total volume, rest, session order, program duration, supervision, provider competence, setting, equipment, adherence strategy, and co-interventions.
6. **Use the assistive-technology pathway when relevant.** Define the participation problem, user/environment fit, alternatives, trial, qualified fitting/configuration, training, skin/pressure/fall checks, maintenance, follow-up, and abandonment risk. Do not fabricate dimensions, alignment, pressure, or device settings.
7. **Individualize the start.** Use baseline performance and symptom/vital response. Never copy a study dose directly when eligibility, setting, or monitoring differs.
8. **Write progression and regression rules.** Base decisions on technique, target performance, symptoms, recovery, confidence, function, and safety—not calendar time alone.
9. **Write stop/escalation rules.** Separate expected exertion, acceptable temporary response, modify/hold criteria, and urgent/emergency features. Do not invent universal pain, heart-rate, SpO₂, or swelling thresholds.
10. **Design the home version.** Use the fewest exercises/tasks that cover priorities; include setup, assistance, equipment, exact clinician-approved dose, common errors, tracking, and safety-net.
11. **Build reassessment logic.** Define adherence, exposure, outcome change, adverse events, goal attainment, and criteria to continue, progress, change, refer, or discharge.
12. **Check feasibility and equity.** Cost, transport, caregiver burden, culture/language, digital access, cognitive/sensory needs, fatigue, space, and patient preference.
13. **Create a transparent final plan.** Mark every unknown as unknown. Label extrapolation and evidence certainty.

## Phase design

Each phase must state:

- entry criteria;
- objectives and components;
- dose provenance and starting range;
- progression/regression rules;
- exit criteria;
- reassessment measures;
- adverse-response and escalation plan.

Return to activity, sport, work, or driving must be criteria-based and jurisdiction-aware. Do not issue clearance.

## High-risk boundaries

Do not provide unsupervised or do-it-yourself instructions for invasive procedures, high-velocity manipulation, blood-flow restriction, internal pelvic procedures, maximal/exertional testing, or device settings when training, authority, medical stability, manufacturer instructions, and emergency support are unverified.

## Output

1. Eligibility, restrictions, and unresolved safety data
2. Goals and baseline measures
3. Evidence and dose-provenance summary
4. Phase plan
5. Session template
6. Home program
7. Assistive technology/equipment trial, fitting, training, maintenance, and follow-up when relevant
8. Progression, regression, hold, stop, and escalation rules
9. Monitoring and reassessment schedule
10. Adherence, feasibility, and accessibility plan
11. Uncertainty and sources

Always label research numbers as **study dose—not an individual prescription** until individualized and approved within a real clinical assessment.
