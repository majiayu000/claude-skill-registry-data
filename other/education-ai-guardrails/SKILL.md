---
name: education-ai-guardrails
description: Use this skill when designing, reviewing, or drafting AI features for education, tutoring, grading, student support, learning analytics, classroom tools, curriculum content, academic integrity, child safety, accessibility, student-data privacy, and human educator oversight.
---

# Education AI Guardrails

Build education AI as teacher/student support with privacy, accessibility, age-appropriate design, and human oversight.

## Workflow

1. Classify the context: tutoring, lesson planning, grading feedback, assessment generation, accessibility support, student analytics, parent communication, or admin workflow.
2. Identify learners: age range, school/university/workplace setting, accessibility needs, language needs, and whether minors are involved.
3. Define the AI role: explain, draft, practice, summarize, adapt content, flag risk, or support an educator. Avoid unreviewed final grading or disciplinary decisions.
4. Check data boundaries: student records, personal data, consent, retention, vendor sharing, classroom recordings, and local policy requirements.
5. Validate pedagogy: learning objective alignment, source accuracy, age appropriateness, bias, hallucination risk, and accommodations.
6. Add human oversight: teacher review for grading, curriculum, interventions, escalations, and any high-impact student outcome.
7. Add misuse controls: plagiarism expectations, prompt-injection resistance, cyber/safety content boundaries, and audit logs for sensitive workflows.
8. Deliver a risk-based recommendation with sources checked, human owner, validation path, and unresolved policy questions.

## Checklist

- Use official curriculum, school policy, or educator-provided materials as the source of truth when available.
- Make feedback formative and explainable; avoid opaque scores without evidence.
- Provide accessibility alternatives and support for multilingual learners.
- Avoid collecting more student data than the feature needs.
- Include safe escalation for self-harm, abuse, violence, or safeguarding signals.
- Test outputs across diverse student profiles and edge cases before classroom rollout.

## Guardrails

- Do not make final grades, placement, discipline, special-education, or safeguarding decisions without authorized human review.
- Do not expose student records, minors' data, or classroom recordings to unapproved tools.
- Do not present AI-generated educational content as policy- or teacher-approved unless it was reviewed.
- Do not help students cheat; redirect to learning support, citation, and integrity-preserving guidance.
