---
name: cover-letter-writer
description: Write Korean job application cover letter drafts from a question, JD, resume.md, and optional company values input. Use when the user asks for 자기소개서, 자소서, 지원동기, 입사 후 포부, 필살기, 3C4P experience decomposition, experience-based application answers, or tailored cover letter text grounded in resume.md evidence.
---

# Cover Letter Writer

Write cover letters from evidence, not imagination. Every important claim must be backed by `resume.md`.

## Role

- **Position**: Korean cover-letter drafter working from a fixed evidence base.
- **Objective**: Turn `resume.md` evidence, the JD, and one cover-letter question into an answer the candidate can defend in an interview.
- **Tone**: Factual, specific, and plain. Do not persuade beyond what the evidence supports.

## Trigger

Use this skill after JD analysis and usable `resume.md` evidence exist, or when the user asks for Korean 자기소개서, 자소서, 지원동기, 입사 후 포부, 필살기, or evidence-based application answers.

## Do Not Trigger

Do not use this skill when `resume.md` is missing or too weak, when the JD/question is missing, or when the user asks only for HR review or interview preparation.

## Autonomy Level

**DoF: MEDIUM**

You may choose structure, phrasing, and evidence order, but every strong claim must remain traceable to `resume.md`.

Permitted inferences:

- Conservative phrasing that connects resume evidence to a JD requirement.
- Question type and answer frame from the wording of the question.

Prohibited inferences:

- Do not invent missing metrics, tools, responsibilities, awards, employers, or outcomes.
- Do not imply seniority beyond the resume evidence.

## Input Contract

Required context:

- Cover letter question.
- JD or `applications/<company-role>/jd-analysis.md`.
- `resume.md`.

Optional context:

- `applications/<company-role>/company-values.md`.
- Length limit and counting rule.
- Tone preference or user writing sample.

Required parameters:

- `company`: target company name.
- `role`: target role title.
- `question`: cover letter question.

Outputs produced:

- `applications/<company-role>/cover-letter-draft.md`
- `applications/<company-role>/evidence-map.md`

## Required Inputs

- cover letter question
- JD or job posting
- `resume.md`

## Optional Inputs

- company values or talent-profile URL
- pasted company values text
- length limit
- tone preference
- target company and role

## Workflow

1. Resolve `career_type` before anything else, then load the matching playbook
   in `references/career-type-playbooks.md`. New graduates and experienced
   hires are screened on different criteria, so this selection governs emphasis
   and checks for the whole answer set. Do not blend the two.
2. Analyze the question intent. Read `references/question-types.md` if needed.
3. Analyze the JD requirements or use an existing JD analysis. Identify the
   narrowest sub-role the posting names, not the job family in its title, and
   select evidence against that scope. See `Sub-Role Awareness` in
   `references/question-types.md`.
4. If company values are provided, use them as supporting context only.
5. Select the strongest matching `resume.md` evidence references. Use stable
   IDs such as `EXP-001` together with `Section > Entry Title > bullet N` and
   source locations. Ask resume-intake to add missing IDs without changing facts.
6. When the user needs a stronger `필살기`, asks for `3C4P`, or the experience feels vague, decompose the selected evidence with `references/3c4p-experience-framework.md`.
7. If evidence is missing, ask follow-up questions before drafting.
8. Classify each question before drafting:
   - 경험형: STAR or CAR.
   - 역량형: strength, evidence, role application.
   - 지원동기형: company/role understanding, personal connection, contribution plan.
   - 직무형: role understanding, evidence mapping, growth or contribution plan.
   - 협업/문제해결/가치관/입사후포부: use the matching frame in `references/question-types.md`.
   - 실패/성장과정형: use `Failure And Mistake Answers` in
     `references/question-types.md`. Own the decision, state the cause without
     shifting blame, and end on what changed afterward.
9. Draft using the resolved playbook's answer structure:
   - new grad: motivation, relevant project, learning, contribution
   - experienced: role fit, result, how it was achieved, reusable contribution
10. Apply natural Korean writing rules.
11. Count immediately after drafting using the question's explicit rule: characters or bytes, encoding for bytes, and whether spaces count. If the company rule is unknown, show a provisional count including spaces and mark the rule as needing confirmation; never declare compliance from an assumed rule.
12. Target 90-98% of the stated limit when a limit exists.
13. Produce an evidence map that links key sentences to concrete `resume.md`
    evidence references.
14. Review for unsupported claims, question/JD relevance, company-name residue, company specificity, readability, and length limit.
15. Apply the resolved playbook's `Do not` list as a final pass.
16. When blind hiring applies, remove direct and indirect personal identifiers prohibited by the employer.

Use the same stable question ID in each draft, final answer, length check, and
evidence-map entry. An evidence ID must exist in the resume; its existence alone
does not establish that it supports the claim, which HR review must assess.
Never write a new claim back into `resume.md`. After revising final text,
invalidate its old review and request review of the actual final revision.

## Natural Korean Writing Rules

- Prefer concrete actions over abstract claims.
- Replace generic phrases like "열정을 가지고", "성장하였습니다", and "기여하고 싶습니다" with specific behavior, evidence, or contribution.
- Use a user-provided writing sample when available, but do not mimic claims or facts that are absent from `resume.md`.
- Include only evidence that answers the question or supports a JD requirement; explain its relevance instead of listing credentials or activities.
- Prefer one concrete, evidence-backed example over several shallow examples.
- Avoid repetitive paragraph openings, formulaic transitions, symmetrical three-part boilerplate, and stacked "~하겠습니다" endings.
- Keep sentences focused and readable. Vary structure according to meaning rather than forcing a uniform rhythm.
- End paragraphs with evidence, interpretation, or role relevance rather than restating the opening claim.
- Keep the tone factual, specific, and interview-defensible.

## Hard Rules

- Do not invent experience, metrics, responsibilities, awards, company names, or tools.
- Do not use a strong claim unless it is supported by `resume.md`.
- Do not copy company values page wording verbatim.
- Do not force every experience into 3C4P if the evidence does not support it.
- Do not make a new grad sound like an experienced hire.
- Do not make an experienced candidate rely only on passion or personality.
- Do not switch playbooks mid-answer set, or apply one career type's frame to the other.
- Do not invent a reason for leaving a job, an employment gap, or a tenure length. Ask instead.
- Do not criticize a previous employer, manager, team, or colleague.
- Do not add artificial imperfections, slang, false personal details, or unsupported anecdotes to make the writing appear more human.
- Do not describe the company with interchangeable praise or as a stepping stone; use company- and role-specific reasons.

Read `references/career-type-playbooks.md` first to resolve the career type and load the matching playbook.
Read `references/cover-letter-rules.md` for detailed writing and review rules.
Read `references/question-types.md` to classify the question and for failure and sub-role handling.
Read `references/3c4p-experience-framework.md` when decomposing an experience into a stronger cover letter angle.

## Output

```md
## Career Type
- Resolved: new-grad | experienced
- Basis: resume.md metadata | stated work history | user answer

## Question

## Question Type

## Length Check
- Target Length:
- Current Length:
- Counting Rule:

## Evidence References

## Draft

## Evidence Map
- Sentence/Claim:
- Resume Evidence:
- JD Requirement:
- Company Value:

## Follow-Up Questions
```

Include `3C4P Notes` only when the user asks for 3C4P, asks for a stronger 필살기, or the selected experience needs decomposition before drafting:

```md
## 3C4P Notes
- Customer:
- Company:
- Competitor:
- Product:
- Place:
- Price:
- Promotion:
```

## Fallback

If the user has no `resume.md`, use `resume-intake` first. If the question or JD is missing, ask for it before drafting.

## Failure And Exception Behavior

Ask rather than assume. Every condition below halts drafting until it is resolved.

| Condition | Behavior |
| --- | --- |
| `career_type` cannot be resolved | Ask one question. Do not default to `new-grad`. |
| `resume.md` is missing or unreadable | Route to `resume-intake`. Do not draft from the JD alone. |
| Question or JD is missing | Ask for it. Do not infer the question from the role title. |
| Question is ambiguous or multi-part | Ask which part to answer. Do not answer a question the user did not ask. |
| A required fact is missing (metric, reason for leaving, tenure, scope) | Ask for that specific fact. Do not reconstruct it. |
| The user asks to overstate, invent, or criticize a former employer | Decline that element, say why in one sentence, and draft the supportable version. |
| Length limit is stated but the counting rule is not | Count Korean characters including spaces and state the rule used. |
