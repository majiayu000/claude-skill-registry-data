---
name: teaching-feedback-ai-boundaries
description: Use when designing a course, assessment, or student-feedback workflow and deciding where AI assistance is acceptable, when grading or feedback must stay within academic-integrity and FERPA/KVKK boundaries, or when AI-use rules for students need stating.
---

# Teaching, Feedback, and AI Boundaries

## When to use

Use this skill when a course syllabus, assignment rubric, reading list, or student-feedback workflow is being designed and the instructor needs to decide where AI assistance is acceptable and where it must stay out. It also applies when clinical supervision materials require a confidentiality boundary, when a classroom AI-use policy needs to be written for students, and when existing feedback drafts must be checked for academic-integrity exposure. It is not for using an AI detector as a sole basis for a disciplinary action, for uploading unredacted student text to an external tool without consent, or for automating feedback so thoroughly that it bypasses the student's own learning process.

## Inputs

- The course goal, level, and student population.
- The assignment or assessment type, written, oral, project, or clinical.
- The reading list or materials requiring verification.
- The institution's current AI-use and data-privacy policy (FERPA, KVKK, or equivalent).
- Any existing feedback draft to be reviewed for boundary compliance.
- The desired feedback tone and the acceptable scope of AI contribution.

## Workflow

1. Separate the teaching objective into knowledge, skill, and disposition dimensions, because the appropriate AI boundary differs across each.
2. Audit the reading list for source verifiability and student access before using it as-is.
3. Draft the assignment prompt so that what the student must do — and what they must not delegate — is explicit.
4. Build the rubric around measurable criteria that do not inadvertently reward AI-polished prose over genuine reasoning.
5. Write the feedback draft in language that diagnoses a learning gap, not the student's character, and proposes a next step the student can take independently.
6. State the classroom AI-use policy at the level the student population can act on: which tasks, which tools, which disclosure obligations.
7. Where student text, clinical case notes, or supervision records contain identifying information, route to sensitive-data-anonymization-gate before any AI tool sees the content.
8. Attach an AI-use disclosure note covering the stage of work, the model used, the contribution level, and the human review step. Before the output leaves the course context, forward to ai-disclosure-auditor; if any course material is destined for public-facing use, hand off to public-scholarship-ethics-adapter at this stage.

## Output

Return:

- A syllabus or assignment scaffold with the AI-boundary decisions marked.
- A rubric with criteria stated in terms of demonstrable student performance.
- A feedback draft written to the learning-gap standard, not the grading-judgment standard.
- A classroom AI-use policy section, sized to the course.
- A list of points still requiring a human instructor decision, flagged explicitly.
- What to record at session end: the output file paths, the human-decision points not yet resolved, and the handoff to sensitive-data-anonymization-gate for any unredacted student or clinical material.

## Verification

- Every rubric criterion is stated in terms of observable student performance, not inferred intent.
- The feedback draft does not diagnose the student; it identifies a gap and proposes a learnable next step.
- The AI-use policy distinguishes which tasks AI may support, which it may not, and what the student must disclose.
- No unredacted identifying student or clinical material was submitted to any AI tool.
- Before closing: an instructor has reviewed and signed off on every grading or disciplinary call; the AI-use disclosure covers stage, model, contribution level, and human review.

## Safety

An AI detector score is not evidence of academic dishonesty on its own — a human instructor must review context before any disciplinary step is taken. Student privacy (FERPA, KVKK) takes precedence over workflow convenience; pass identifying material through sensitive-data-anonymization-gate first. Feedback drafted by AI must be reviewed by the instructor before it reaches the student, because an unchecked AI assessment can harm a student's academic trajectory. Route supervision or clinical materials to ethics-irb-ai-protocol when an ethics-board implication exists. AI contribution must remain on the record: the stage, the model used, the degree of contribution, and the human review step are all documented. Forward final output to ai-disclosure-auditor before submission anywhere beyond the course itself, and to public-scholarship-ethics-adapter if any course material will become public-facing content.

## Example prompt

"Bu lisans dersi için ödev yönergesini, rubriği, yapay zekâ kullanım politikasını ve bir taslak öğrenci geri bildirimi yaz. Hangi aşamalar yapay zekâ desteğine açık, hangileri öğrencinin kendi emeğine bırakılmalı?"

Expected smoke output:

- An assignment prompt that separates what AI may assist with from what the student must produce independently, with a mandatory disclosure line for any AI use.
- A four-criterion rubric with performance anchors at each level, stated in observable terms.
- A classroom AI-use policy paragraph the instructor can paste directly into the syllabus.
- A sample feedback draft for a hypothetical weak submission, written in learning-gap language with a concrete next step.

## Türkçe kullanım notu

Bu beceri, yapay zekâ desteğini öğretim sürecinin dışında tutmak için değil, pedagojik sorumluluk ve gizlilik sınırları içinde tutmak için tasarlanmıştır. Ders izlencesi, rubrik ya da okuma listesi hazırlanırken yapay zekânın nerede kullanılabileceği ve nerede insan kararının zorunlu olduğu baştan belirlenir. Öğrenci geri bildirimi tanı koymaz, öğrenme boşluğunu işaret eder ve öğrencinin yeniden yazabileceği bir adım önerir. Kimlik içeren ya da klinik nitelikli öğrenci materyali herhangi bir araca girmeden önce sensitive-data-anonymization-gate'ten geçer. Yapay zekâ dedektörü tek başına disiplin kararı için yeterli değildir — bağlamı değerlendiren bir öğretim üyesi son kararı her zaman öğretim üyesi vermelidir. Sınıf yapay zekâ politikası öğrencinin hangi araçları, hangi görevlerde, hangi açıklama yükümlülüğüyle kullanabileceğini açıkça söyler. Aşama, model, katkı düzeyi ve insan incelemesi yapay zekâ kullanım beyanına geçirilir. Ders bağlamının dışına çıkmadan önce bu beyan ai-disclosure-auditor'a devredilir. Çıktının herhangi bir bölümü kamuya açık içeriğe dönüşecekse public-scholarship-ethics-adapter da bu aşamada devreye girer.
