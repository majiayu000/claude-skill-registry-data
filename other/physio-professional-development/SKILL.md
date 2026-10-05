---
name: physio-professional-development
description: "Plan physiotherapy CPD, journal clubs, research and practice improvement. Use for mesleki gelişim, portfolios, mentoring, ethics, clinical audit and literature watch."
---

# Physio Professional Development

Original standalone scope and trigger coverage: Build evidence-based physiotherapy professional development, research, and practice-improvement plans. Use for competency self-audit, CPD portfolio, learning goals, literature watch, journal club, reflection, mentorship, teaching, ethics, scope, interprofessional work, clinical audit, quality improvement, service evaluation, research/thesis protocol, preregistration, data governance, leadership, or career development. Trigger on mesleki gelişim, CPD, öğrenme planı, journal club, klinik audit, araştırma protokolü, tez. Do not invent credentials, credits, ethics approval, registration, or results, and never replace local regulatory, employer, sponsor, ethics, statistical, or supervision requirements.

## Current literature and clinical handoff

Use `medical-evidence-research` for journal-club appraisal/search and evidence-watch work when actually available; use `physio-clinical-copilot` for integrated clinical application. Keep this package's CPD, ethics, teaching, mentorship, portfolio and QI/research functions. If canonical packages are unavailable, use the original specialist fallback and the local [literature-watch workflow](references/literature-watch.md), [native queries](references/search-strategy.md), [retrieval integrity](references/tool-routing.md) and [appraisal rules](references/appraisal-and-synthesis.md). Return one integrated output, not repeated specialist reports.

## Mandatory first reads

Read [safety core](references/safety-core.md) and [professional development framework](references/professional-development-framework.md). Keep clinical competence, legal authority, and credentialing separate.

## Workflow

1. **Define role and context.** Country/region, practice setting, career stage, population, responsibilities, available supervision, and local competence/CPD requirements.
2. **Map the competency profile.** Audit practice, professionalism, communication/collaboration, evidence/research, learning/teaching, quality, management, and leadership. Use concrete behavior or work evidence—not confidence alone.
3. **Prioritize one gap.** Combine patient/service importance, safety risk, frequency, performance gap, feasibility, and personal goal.
4. **Form a learning question.** Specify what the physiotherapist should be able to do differently and how it will be observed.
5. **Choose the best learning method.** Guideline/evidence review, case discussion, simulation, supervised practice, course, mentoring, peer observation, journal club, audit, teaching, or quality-improvement project.
6. **Verify source and quality.** Check provider expertise, conflicts, learning outcomes, evidence basis, assessment, feedback, accessibility, and transfer to practice. Do not equate attendance with competence.
7. **Build a transfer plan.** Pre-work, practice opportunity, feedback/supervision, workplace barrier, implementation cue, and first real case or service change.
8. **Measure impact.** Use knowledge/skill assessment, behavior change, documentation/audit data, patient-relevant outcomes, safety signals, and reflective evidence as appropriate.
9. **Create a CPD record.** Need, objective, activity, evidence/source, reflection, changed behavior, impact, follow-up, and artifact. Do not invent attendance, hours, accreditation, or credits.
10. **Use journal club rigor.** Use `medical-evidence-research` for appraisal and current evidence when available; otherwise invoke `$physio-study-appraisal` and `$physio-evidence-search` with the updated local method references.
11. **Use QI/research rigor.** For QI, define process/problem, baseline, stakeholders, measure, small change, balancing measure, review cycle, and sustainability. For research/thesis work, use the reference's protocol, ethics, preregistration, methods, and data-governance gate. Protect health data and distinguish QI, audit, service evaluation, and research under local rules.
12. **Reassess and iterate.** Decide continue, deepen, supervise, stop, or select the next gap.

## Literature monitoring

For a current-evidence watch, define topic/PICO, authoritative sources, query, inclusion rules, cadence, deduplication, appraisal threshold, contradiction logic, and output format. The skill does not run in the background by itself. For an authorized recurring watch, use a separate available alert/automation with an agreed scope, cadence and meaningful-change threshold. Distinguish last attempt from last complete checkpoint, use justified overlap, retrieve required pages, and keep DOI/PMID versions and notices. Preserve the complete checkpoint after partial retrieval. Never claim a schedule or account alert is active without verification.

## Ethical and scope guardrails

- A course, certificate, or AI-generated plan does not expand legal scope or prove competence.
- Use informed consent, privacy, equity, accessibility, cultural humility, and patient partnership.
- Seek supervision or referral when a task exceeds competence.
- Do not convert reflective notes into self-blame; focus on decisions, context, learning, and system improvement.
- Do not fabricate CPD evidence, audit results, patient outcomes, or citations.

## Output

1. Role/context and regulatory assumptions
2. Competency map with evidence
3. Prioritized gap and rationale
4. Learning objective and success criteria
5. Learning activities and source-quality checks
6. Practice-transfer and supervision plan
7. Impact measures and review date
8. CPD portfolio entry
9. Research/QI governance and protocol scaffold when relevant
10. Next learning cycle
