---
name: physio-documentation
description: "Draft accurate, traceable physiotherapy documentation from supplied facts. Use for initial evaluation, visit/daily note, re-examination/progress report, discharge or episode summary, referral, consultation, handoff, goal and outcome tracking, ICF or SOAP-style notes, patient education, consent, adverse events, and plan changes. Trigger on fizyoterapi notu, epikriz, değerlendirme formu, SOAP, taburculuk. Never invent, backdate, authenticate, submit billing, or create a final legal record; codes may only be a verified draft for authorized review. Protect health data and verify local requirements."
---

# Physio Documentation

## Mandatory first reads

Read [safety core](references/safety-core.md) and [documentation framework](references/documentation-framework.md). Use only facts provided or clearly derived calculations. Mark missing items; never fabricate a finding, consent, treatment, response, time, signature, or clinician identity.

## Workflow

1. **Identify document type and purpose.** Initial assessment, encounter note, re-examination/progress, discharge, referral/consult, handoff, incident/adverse event, or patient-facing summary.
2. **Establish jurisdiction, setting, role, and audience.** Legal, payer, coding, signature, retention, consent, and scope rules vary. Do not assume US or Turkish requirements apply elsewhere.
3. **Minimize data.** Remove unnecessary identifiers from the drafting context. Use placeholders instead of real identifying data whenever possible.
4. **Separate information types.** Patient-reported history, observed/measured findings, clinician interpretation, actions performed, response, and future plan must remain distinguishable.
5. **Preserve traceability.** Link finding → clinical interpretation → goal → intervention/education → response → outcome measure → next decision.
6. **Document safety.** Screening relevant to the presentation, escalation/referral, precautions, adverse events, stop criteria, and safety-net. Do not use boilerplate to imply an examination was completed.
7. **Document dosage actually delivered.** Mode, body region/task, intensity/load, volume/time, assistance, equipment, supervision, modifications, and patient response—not only planned dose.
8. **Document education and consent accurately.** Topic, options/risks discussed, decision, interpreter/caregiver involvement, teach-back or demonstration, and unresolved barrier. Do not state informed consent unless it occurred and met local requirements.
9. **Track outcomes.** Instrument/version, conditions, score/unit/direction, clinically relevant comparison, goal status, and whether change exceeds error/importance only when supported.
10. **Explain plan changes.** Continue, progress, regress, hold, refer, or discharge with the evidence from the encounter and patient preference.
11. **Run an integrity check.** Internal consistency, chronology, units, laterality, copied-forward text, contradictory findings, unsupported diagnosis, prohibited abbreviation, and missing authentication fields.
12. **Return a draft label.** Make clear that the responsible clinician must verify, edit, and authenticate the final record.

## Non-negotiable boundaries

- Do not backdate, fabricate, copy a previous normal finding, or imply a service occurred.
- Never submit or authenticate billing. Draft a possible code only when current jurisdiction/payer rules and the documented facts are verified, label it for authorized review, and never use a code to imply an undocumented service. Do not create legal certification, work/sport/driving clearance, or payer compliance claims.
- Do not reproduce full copyrighted forms or scale items.
- Do not expose identifiers to web search or external tools.
- A polished note cannot repair an unsafe or unsupported clinical decision; flag the issue.

## Output

1. `DRAFT — clinician verification required`
2. Document header with placeholders only
3. Relevant history/status
4. Objective findings and standardized measures
5. Assessment/clinical reasoning and safety status
6. Interventions/education and actual dose
7. Response/adverse events
8. Goal and outcome progress
9. Plan, referral, reassessment, and safety-net
10. Missing/contradictory information and jurisdiction checks

Use SOAP, ICF, narrative, or setting-specific structure only when it fits the requested document and local standards.
