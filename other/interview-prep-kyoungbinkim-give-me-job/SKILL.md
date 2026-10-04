---
name: interview-prep
description: Prepare Korean interview follow-up questions and evidence-backed answer points from resume.md, JD analysis, cover letter text, and an evidence map. Use after HR review or final cover letter drafting when the user wants 면접 준비, 꼬리질문, interview defense, or claim verification before manual submission.
---

# Interview Prep

Use this skill to turn a cover letter package into interview preparation that the applicant can defend from `resume.md` evidence.

## Trigger

Use this skill after `cover-letter-draft.md` or `cover-letter-final.md` exists and an evidence map is available.

Use it when the user asks for 면접 준비, 꼬리질문, 예상 질문, 답변 포인트, 모의면접, 면접 복기, 결과 분석, or interview defense based on a Korean application package.

## Do Not Trigger

Do not use this skill before JD analysis and resume evidence exist.

Do not invent missing answers, metrics, tools, or company context. If a claim cannot be defended from `resume.md`, mark it as missing evidence.

## Autonomy Level

**DoF: LOW**

Follow the input evidence. Generate questions and answer points only from the JD, cover letter, and `resume.md`. Do not add new achievements or unsupported explanation.

Permitted inferences:

- Likely interviewer follow-up questions from a specific cover-letter claim.
- Risk level from the strength of the mapped resume evidence.

Prohibited inferences:

- Do not infer unlisted tools, metrics, responsibilities, awards, or business impact.
- Do not turn weak evidence into a confident answer point.

## Input Contract

Required context:

- `resume.md`: structured career evidence.
- `applications/<company-role>/jd-analysis.md`: role requirements and evaluation criteria.
- `applications/<company-role>/evidence-map.md`: claim-to-evidence mapping.
- `applications/<company-role>/cover-letter-final.md` or `cover-letter-draft.md`: answer text to defend.

Optional context:

- `applications/<company-role>/hr-review.md`: blocker and warning context.
- `applications/<company-role>/company-values.md`: optional company values context.

Required parameters:

- `company`: target company name.
- `role`: target role title.

Outputs produced:

- `applications/<company-role>/interview-prep.md`

## Workflow

1. Read the cover letter and split it into core claims.
2. Match each claim to `evidence-map.md` and `resume.md`.
3. Generate 2-3 follow-up questions for each core claim.
4. Add verification questions for metrics, tools, role scope, collaboration, failure handling, and JD fit when relevant.
5. For any claim whose strength rests on a decision, add a question about the
   alternatives considered and why they were rejected. Interviewers probe the
   reasoning behind a result more often than the result itself.
6. For any 실패/성장과정 claim, add a question about what the candidate changed
   afterward and where that change applied later. An answer that stops at the
   lesson is the common weak point.
7. Write answer points using only supported evidence.
8. Mark missing or thin evidence clearly.
9. Add a short preparation checklist for manual review before interview.

## Practice, Debrief, And Results

For a submitted application, use the exact company-specific answers the user
confirms they submitted, together with their evidence IDs. Do not silently
substitute a later edited answer. If that snapshot is unavailable, ask for it or
label the preparation as based on an unconfirmed version.

In mock interviews ask one question, wait for the user's answer, then give
feedback on evidence, logic, and personal contribution before the next question.
Distinguish the user's answer from suggested wording. Do not supply facts that
the user did not provide or promote practice answers into resume evidence.

For an actual interview debrief, record only user-provided questions, answers,
and impressions, retaining the distinction between recalled facts and feelings.
Link recurring improvement points to their debriefs and evidence. Aggregate only
confirmed recruitment outcomes; exclude unknown or inferred outcomes from result
counts. Never infer rejection causes or predict acceptance probabilities.

Recruitment stages come from the posting and user input, with no forced ordering
of document screening, tests, assignments, and interviews. Track separate
deadline, assignment, and interview dates with `Asia/Seoul` as the default time
zone. State changes need timestamp, source, and notes; submission requires user
confirmation. Preparation status and recruitment progress remain separate.

## Output

```md
## Interview Prep
- Company:
- Role:
- Source Cover Letter:

## Claim Defense
| Claim | Resume Evidence | Follow-Up Questions | Answer Points | Evidence Risk |
| --- | --- | --- | --- | --- |

## Metric And Tool Verification
- Question:
- Evidence To Use:
- Risk:

## JD Fit Questions
- Question:
- Answer Points:
- Resume Evidence:

## Missing Evidence
- Claim:
- Needed Evidence:

## Preparation Checklist
- Review every quantified claim.
- Prepare one concrete example per key claim.
- Do not add facts that are absent from `resume.md`.
```

## Fallback

If required inputs are missing, update `workflow.md` with `Status: paused`, list the missing files under `Missing Inputs`, and halt. In interactive mode, ask for the missing file or text. In non-interactive mode, do not continue.
