---
name: company-values-analyzer
description: Analyze an optional company talent, values, culture, or recruitment page and turn it into cover letter positioning guidance. Use when the user provides a company values URL/text, asks to match a cover letter to company culture, or wants talent-profile keywords connected to resume.md evidence. 한국어 요청도 포함합니다 - 인재상 분석, 기업 가치관, 회사 문화, 채용 홈페이지 분석, 기업 분석, 인재상에 맞춰서, 회사가 원하는 인재.
---

# Company Values Analyzer

Use this skill only when company values, talent profile, culture, mission, or recruitment-page material is available. The input is optional for cover letter writing.

## Trigger

Use this skill only when the user provides company values, culture, mission, talent profile, recruitment-page material, or asks to align a cover letter with company values.

## Do Not Trigger

Do not use this skill when no values source is available. Do not rely on built-in company stereotypes or unsourced assumptions.

## Autonomy Level

**DoF: HIGH**

You may synthesize positioning guidance from official or user-provided company material, but all source facts must remain separate from your interpretation.

Permitted inferences:

- Preferred behaviors and tone implied by repeated official wording.
- Candidate positioning angles that connect company values to `resume.md`.

Prohibited inferences:

- Do not create a company-specific values database from memory.
- Do not copy company wording verbatim into cover letters.

## Input Contract

Required context:

- Company values URL, pasted values text, culture notes, mission text, or talent-profile material.

Optional context:

- `resume.md` for evidence matching.
- JD analysis for role-specific positioning.

Required parameters:

- `company`: target company name.
- `source`: URL, pasted text, notes, or `unknown`.

Outputs produced:

- `applications/<company-role>/company-values.md`

## Workflow

1. Accept a URL, pasted page text, or short company notes.
2. Extract repeated values, preferred behaviors, and avoidable tones.
3. Distinguish official source facts from your inference.
4. Connect each usable value to candidate evidence in `resume.md` when available.
5. Do not copy company wording directly into a cover letter. Paraphrase and ground it in the user's experience.

## Output

```md
## Company Values Analysis
- Source:
- Company:
- Talent Keywords:
- Core Values:
- Preferred Behaviors:
- Tone To Use:
- Tone To Avoid:
- Resume Evidence Candidates:
- Inferences:
- Risks:
```

## Fallback

If the URL cannot be read or the page is image-heavy, ask the user to paste the relevant text. If no values input is provided, continue with JD and `resume.md` instead of blocking the workflow.
