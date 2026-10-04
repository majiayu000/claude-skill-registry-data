---
name: resume-intake
description: Build or improve a job seeker's resume.md source file from conversational career input. Use when the user wants to create resume.md, organize new-grad or experienced career history, convert raw experiences into STAR/CAR evidence, add missing metrics, or prepare reusable career evidence for cover letters and job applications. 한국어 요청도 포함합니다 - 이력서 작성, 이력서 정리, 경력기술서, 경력 정리, 커리어 정리, 자소서 소재 정리, 내 경험 정리해줘, 신입 이력서, 경력직 이력서.
---

# Resume Intake

Use this skill to turn raw career material into a structured `resume.md` that
other give-me-job skills can trust.

## Trigger

Use this skill when `resume.md` is missing, thin, outdated, or lacks evidence that can support a Korean cover letter.

## Do Not Trigger

Do not use this skill when the user already has a usable `resume.md` and only needs JD analysis, cover letter drafting, HR review, or packaging.

## Autonomy Level

**DoF: LOW**

Follow user-provided facts only. Do not infer missing employers, dates, metrics, awards, tools, responsibilities, or outcomes.

Permitted inferences:

- Career type from stated graduation date, work history, or years of experience.
- Evidence strength from specificity, role clarity, and observable result.

Prohibited inferences:

- Do not upgrade a school project into professional work.
- Do not turn participation into ownership unless the user says they owned the work.

## Input Contract

Required context:

- Raw career material from the user or an existing `resume.md`.

Optional context:

- Target role, target company, JD, or desired cover-letter questions.

Required parameters:

- `target_role`: target role when available, otherwise `unknown`.
- `career_type`: `new-grad`, `experienced`, or `unknown`.

Outputs produced:

- `resume.md` draft, a patch/update plan, or focused follow-up questions.

## Workflow

1. Read `references/resume-schema.md` before creating or rewriting
   `resume.md`.
2. Determine whether the user is `new-grad`, `experienced`, or still
   `unknown`.
3. Read an existing `resume.md` if present. Preserve valid facts, but migrate
   old `Profile`, `Core Summary`, `Experience Bank`, or `Work History`
structures into the canonical sections.
4. Create or update the metadata block:
   - `last-updated`: today's date
   - `career-type`: `new-grad` or `experienced`
   - `target-role`: target role or `Unknown`
   - `intake-version`: increment the existing value, or use `1`
5. Collect raw experiences in the user's language first. Do not force every
   field before making progress, but ask for missing facts that materially
   affect evidence quality.
6. Build the canonical top-level sections in this order:
   - `Personal Info`
   - `Target Role`
   - `Summary`
   - `Work Experience` for experienced candidates, or for new graduates only
     when they have relevant work/internship/part-time experience
   - `Projects`
   - `Education`
   - `Skills`
   - `Certificates & Awards` only when relevant
7. Split work and project material into STAR/CAR bullets:
   - action verb
   - what was done
   - method, scale, or constraints
   - measurable or observable result

   When the user states why they chose an approach, rejected an alternative, or
   changed direction, capture that reasoning too. Cover-letter and interview
   questions frequently ask how a candidate decided, and that judgment cannot be
   recovered later from a result-only bullet. Ask for it when an entry is the
   candidate's strongest evidence. Never reconstruct a rationale the user did
   not give.
8. End every work role and project entry with exactly one strength comment:
   `<!-- strength: High -->`, `<!-- strength: Medium -->`, or
   `<!-- strength: Low -->`.
9. Write `Summary` last. If any core work/project evidence remains `Low`, do
   not polish a final summary; leave `Pending stronger evidence.` and ask
   follow-up questions.
10. Keep claims factual. Do not invent company names, numbers,
    responsibilities, awards, links, tools, or outcomes.

## New Grad Focus

Emphasize project depth, learning speed, role clarity, problem solving,
collaboration, and job relevance. `Projects` is required even when work
experience is absent. If metrics are weak, strengthen the explanation of
process, decision making, and learning without pretending there was business
impact.

New-grad results are usually small, so the reasoning behind them carries most
of the signal. Prefer capturing how the candidate framed a problem, what they
tried first, and what they changed after it did not work, over inflating the
outcome. Also capture mistakes the candidate owns and what they changed
afterward: 실패 경험 and 성장과정 questions are common, and an honest, resolved
mistake is usable evidence that a polished result-only bullet cannot supply.

## Experienced Focus

Separate responsibility from achievement. `Work Experience` is required for
experienced candidates. Emphasize role scope, measurable result, business
impact, cross-functional work, decision making, and repeatable contribution.

## Schema Decisions

Adopt the canonical resume-style structure in `references/resume-schema.md`.
Do not create a separate `Experience Bank` for new intake. Assign stable IDs
such as `EXP-001` to evidence in `Work Experience` or `Projects`, preserving
existing IDs. Record the source section, entry title, and current line/bullet
location alongside each ID. Never renumber IDs when entries move.

For each experience capture situation, the candidate's role, action, result,
learning, and suitable question types. Keep company/question reuse and related
follow-up questions as usage notes, separate from career facts. Rewrite reused
evidence for the selected company, role, and question purpose.

Never copy a newly generated number or claim from a cover letter into the
resume. When the user provides a new fact, show the proposed factual change
before updating the resume and related materials. Changed source facts require
revalidation of packages that used them.

Treat missing contact fields and profile links as intake gaps. Ask for them or
mark them clearly as missing; do not fabricate placeholder URLs, phone numbers,
schools, employers, or metrics.

## Output

Return one of these:

- a complete `resume.md` draft using the canonical schema
- a patch/update plan for the existing `resume.md`
- focused follow-up questions when evidence is too weak or required personal
  info is missing

Use `references/resume-schema.md` for the canonical structure.

## Fallback

If the user gives too little information, ask for 3 short prompts:

- target role
- strongest project or work experience
- one measurable or observable result
