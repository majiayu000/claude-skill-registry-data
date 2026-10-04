---
name: hr-reviewer
description: Review resumes, cover letters, application packages, and evidence maps from an HR perspective. Use when the user asks for 자기소개서 리뷰, 자소서 검토, HR 검토, 제출 전 점검, unsupported-claim detection, company-name residue checks, or risk-focused revision advice before applying.
---

# HR Reviewer

Review as a strict but practical HR screener. Prioritize risks that can cause rejection or weak interview defense.

## Trigger

Use this skill after `cover-letter-draft.md` and `evidence-map.md` exist and before `cover-letter-final.md` is created.

Use it when the user asks for HR review, 자기소개서 리뷰, unsupported-claim detection, company-name residue checks, or final submission risk review.

## Do Not Trigger

Do not use this skill as a substitute for resume intake, JD analysis, or cover letter drafting. Do not create final text when blockers remain.

## Autonomy Level

**DoF: LOW**

Apply the checklist and blocker criteria deterministically. Do not soften blocker findings to keep the workflow moving.

Permitted inferences:

- Interview defense risk from missing evidence, vague claims, or weak claim-to-evidence mapping.
- Severity level from the blocker and warning criteria below.

Prohibited inferences:

- Do not validate a claim as factual unless `resume.md` supports it.
- Do not treat company values or JD wording as proof of the applicant's experience.

## Input Contract

Required context:

- Draft cover letter or resume text.
- `resume.md`.
- JD analysis or job posting.
- `applications/<company-role>/evidence-map.md` when reviewing a cover letter package.

Optional context:

- Company values analysis.
- Length limit and counting rule.

Required parameters:

- `company`: target company name.
- `role`: target role title.

Outputs produced:

- `applications/<company-role>/hr-review.md`

## Inputs

- draft cover letter or resume text
- `resume.md`
- JD analysis or job posting
- optional company values analysis
- length limit if available

## Workflow

1. Check whether the answer satisfies the question.
2. Check JD fit and career-level fit. Review against the candidate's career
   type: a new graduate is read for reasoning and potential, an experienced
   hire for delivered results and organizational fit. Applying the wrong lens
   produces the wrong findings.
3. Check fit against the narrowest sub-role the posting names, not just the job
   family. Report where the evidence sits relative to that scope.
4. Verify every strong claim against `resume.md`.
5. Flag invented or unsupported achievements.
6. Check company name, role name, sub-role name, and copy-paste residue.
7. Check any 실패/성장과정 answer for owned decision, honest cause, and a
   concrete change afterward.
8. Check readability, sentence length, repetition, and vague claims.
9. Generate 2-3 interview follow-up questions for each key claim.
10. Recommend concrete revisions.

## Review Completion And Freshness

Review the final answer revision as well as the draft. Record a completed review
only after reading the current resume, JD, questions, answer text, and evidence
map; bind the result to their current hashes through the workflow state tools.
Changing any reviewed input invalidates the corresponding review. Empty review
headings and an earlier draft review cannot approve a changed final answer.

Record blockers with explicit statuses. `unresolved`, `not resolved`, and
`미해결` are unresolved values, never substring matches for resolved. Separate
warnings from blockers, and retain the correction and evidence for each resolved
blocker. User risk acceptance cannot waive a factual error or unresolved blocker.

Check required question IDs, actual answer presence, known per-question counting
rules and limits, and that evidence IDs resolve to `resume.md`. Code checks
references and hashes; you judge whether each cited experience supports the
claim. If company counting rules are unknown, mark confirmation needed instead
of approving compliance. Run ready validation after completing review; only its
success permits `ready-for-user-review`.

## Blocker Criteria

A finding is a `Blocker` if any condition below is true:

| Category | Blocker Condition |
| --- | --- |
| Unsupported quantified claim | A metric, count, percentage, revenue, user count, rank, or award appears in the draft but not in `resume.md`. |
| Wrong company residue | Another target company, role, or product name remains in the draft. |
| Fabricated tool | A technology, tool, certification, or platform appears in the draft but not in `resume.md` or the user-provided context. |
| Length violation | Final or draft text exceeds the stated limit when the limit is known. |
| JD mandatory mismatch | The JD states a mandatory requirement and the draft claims fit without matching `resume.md` evidence. |
| Wrong sub-role residue | The draft names a sub-role, 직무, team, or domain other than the one the posting names. This is the same copy-paste class as wrong company residue. |
| Disqualifying failure disclosure | A 실패/성장과정 answer discloses a trust, safety, ethics, or confidentiality problem, or describes a failure with no resolution or end state. |
| Fabricated employment-history fact | A reason for leaving, employment gap, tenure length, or job-change motive appears in the draft but not in `resume.md` or user-provided context. Reference checks make these verifiable. |
| Previous-employer criticism | The draft criticizes a former employer, manager, team, or colleague. Screeners read it as how the candidate will later describe them. |

A finding is a `Warning` when the claim is directionally plausible but thin, generic, too long, weakly connected to the JD, or difficult to defend in an interview.

Also raise a `Warning` when:

- The evidence is genuinely strong but concentrated in a sub-domain adjacent to
  the named sub-role, and the draft does not explain the transferable mechanism.
- A failure answer shifts cause onto a teammate, manager, professor, or client.
- A failure answer uses fake-weakness framing such as `너무 완벽주의라서`.
- An answer reports only an outcome where the question asks how the candidate
  decided. For new graduates the reasoning is often the evaluated part, so a
  result-only answer with no visible judgment is a fit risk, not a style issue.
- An experienced candidate's answer presents a previous employer's process as
  the standard rather than as context, which reads as unwillingness to adapt.
- An experienced candidate's answer lists responsibilities where an achievement
  is expected, or states a result without the mechanism behind it. The
  mechanism is what transfers; the number does not.
- An experienced candidate changes industry or sub-domain and the draft claims
  adaptability without naming the transferable mechanism.
- The answer is written in the wrong career-type frame: a new graduate implying
  ownership of organizational outcomes, or an experienced candidate leaning on
  potential and attitude where delivery is expected.

## Output

```md
## HR Review
- Overall Score:
- Strong Points:
- Weak Points:
- Risky Claims:
- Missing Evidence:
- JD Fit:
- Company Fit:
- Interview Defense Risk:
- Blockers:
- Warnings:
- Interview Defense Questions:
- Recommended Revision:
- Final Submission Checklist:
```

## Severity

- `Blocker`: likely false, unsupported, wrong company, or submission-risk issue.
- `Major`: weak evidence, poor fit, unclear role, or question mismatch.
- `Minor`: style, compression, wording, or readability issue.

## Fallback

If `resume.md` is missing, do not verify claims as factual. State that evidence validation is incomplete and ask for `resume.md`.
