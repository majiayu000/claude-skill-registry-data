---
name: application-packager
description: Create a company-specific job application package from a JD, resume.md, cover letter drafts, HR review, and optional company values input. Use when the user wants 지원 패키지, submission checklist, application folder structure, final answer snippets, email draft support, or safe pre-submission preparation without automatic final submission.
---

# Application Packager

Create submission-ready materials, but do not submit applications automatically.

## Trigger

Use this skill after the JD analysis, cover letter draft/final, evidence map, HR review, and optional interview prep are ready or when the user asks to assemble a final Korean application package.

## Do Not Trigger

Do not use this skill to bypass HR review, submit an application, send email, log in, solve CAPTCHA, or transmit personal information.

## Autonomy Level

**DoF: LOW**

Create and validate the package structure deterministically. Do not mark an application submitted unless the user explicitly confirms manual submission.

Permitted inferences:

- ASCII package slug from company and role.
- Missing package files from the canonical package structure.

Prohibited inferences:

- Do not create unsupported cover letter claims.
- Do not invent deadlines, required documents, or submission status.

## Input Contract

Required context:

- Company name and role name.
- JD or `applications/<company-role>/jd-analysis.md`.
- `resume.md`.
- Cover letter draft or final.
- `applications/<company-role>/evidence-map.md`.
- `applications/<company-role>/hr-review.md`.

Optional context:

- Company values analysis.
- `applications/<company-role>/interview-prep.md`.
- Deadline, file requirements, and length limits.

Required parameters:

- `company`: target company name.
- `role`: target role title.

Outputs produced:

- `applications/<company-role>/workflow.md`
- `applications/<company-role>/submission-checklist.md`

## Inputs

- company name
- role name
- JD or JD analysis
- `resume.md`
- cover letter draft or final
- optional company values analysis
- deadline, file requirements, and length limits if available

## Workflow

1. Normalize the application slug as `company-role`.
2. Create or propose the package structure from `references/package-structure.md`.
3. Save JD analysis, company values analysis, cover letter draft/final, evidence map, and checklist.
4. Save interview preparation when available.
5. Check company name, role name, file names, length limits, and required attachments.
6. Prepare manual submission snippets or email draft text when requested.
7. Record submission status only after the user confirms what happened.
8. Run structure validation for newly initialized templates. Run ready validation
   for completed answers, checking required questions, length rules, evidence
   references, completed current final review, and unresolved blockers. Only
   successful ready validation records `ready-for-user-review`.

Use `state.json` as the machine-readable preparation state and generate the
`workflow.md` status summary from it. Keep recruitment progress in the tracker.
Record interruption reasons and next actions; reuse completed steps only while
their reviewed input hashes remain current. Legacy packages without current
review metadata require revalidation and remain readable without overwriting
their existing prose. User risk acceptance never waives unresolved blockers.

An AI request from CLI, TUI, or dashboard is a prepared prompt, not a completed
package. Execute it in the existing agent, save the requested files, validate,
and reload the interface. Installation, upgrade, and uninstall must not touch
resume facts, saved jobs, tracking data, or application packages.

## Hard Rules

- Do not click or trigger a final submit/send action.
- Do not bypass CAPTCHA, login, payment, consent, or sensitive personal information prompts.
- Do not create unsupported claims that are absent from `resume.md`.
- Do not auto-create user data during skill installation. Create files only when the user asks during a task.

## Output

```md
## Application Package
- Company:
- Role:
- Deadline:
- Package Path:
- Included Files:
- Missing Inputs:
- Interview Prep:
- Submission Checklist:
- Manual Submission Notes:
```

## Fallback

If final cover letter text is not ready, call for `cover-letter-writer` and `hr-reviewer` work before packaging.
