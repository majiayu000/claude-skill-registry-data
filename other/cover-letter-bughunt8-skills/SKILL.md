---
name: cover-letter
description: Use when the user wants a cover letter for a specific role, company, or tightly defined target lane, especially when they ask for "just a cover letter." Do not use for generic broad cover letters.
---

## Overview

Cover-letter-only entry point. It reuses the `resume-tailor` cover-letter workflow when the letter is for a specific job, and the `resume-builder` source-letter workflow when the user is building a reusable letter for a tightly defined lane.

The quality bar is specificity. A missing letter is better than a generic one.

## Workflow

> **State layer:** selects a source work document for evidence, may write `my-documents/coverletter.md` or `my-documents/applications/{id}/coverletter.md`, runs claim-check before save, and may write a numbered report. See [state-layer contract](../_shared/state-layer.md).

### 1. Determine letter type

Classify the request:

- **Specific application:** user has a company + role, job posting, or application id. Use `resume-tailor` cover-letter-only mode.
- **Source letter for a lane:** user has a tight target lane, company type/stage, problem, and proof points, but no specific employer. Use `resume-builder` just-cover-letter mode.
- **Too broad:** user asks for a generic letter for "SaaS jobs", "remote jobs", "leadership roles", or multiple unrelated targets. Pause and ask for specificity. 

Minimum specificity:

- Exact role or tight lane (e.g. "early-stage SaaS PM roles," not "tech jobs").
- Concrete company, company type, or stage.
- Two proof points from saved evidence or user-provided facts.

### 2. Gather evidence

Run `node "{job_hunt_skills_root}/scripts/scaffold-state.mjs"` if needed.

Select the source work document using [state-layer section 6](../_shared/state-layer.md#6-work-document-frontmatter-and-selection). Read:

- Selected `resume.md` or `cv.md`.
- `story-bank.md`.
- `proof-assets/`.
- Relevant application folder or company research report when available.

If no source work document exists, offer `resume-builder` first or proceed on pasted material with limited claim verification.

### 3. Draft

Write for the employer's problem and the user's proof, not the user's desire for a job.

Structure:

- Hook: company/role need + why the user's experience/skills are relevant.
- Proof paragraph 1: strongest matching achievement.
- Proof paragraph 2: second proof point or honest adjacent strength.
- Fit paragraph: why this role/company/lane makes sense now.
- Close: clear, direct, non-generic.

Rules:

- Do not prose-copy the whole work document.
- Do not invent metrics, tools, titles, dates, credentials, or achievements.
- Preserve hedges and qualifiers.
- Name gaps directly when it improves credibility.

### 4. Verify before save

Invoke `claim-check` in tailor mode before saving. Resolve soft and hard findings with the user. Cosmetic fixes may auto-apply.

### 5. Save

Specific application:

```text
my-documents/applications/{id}/coverletter.md
my-documents/reports/{###}-{id}-cover-letter-{YYYY-MM-DD}.md
```

Source letter:

```text
my-documents/coverletter.md
my-documents/reports/{###}-cover-letter-{YYYY-MM-DD}.md
```

Report frontmatter:

```yaml
---
report_id: {###}
company: {Company or null}
role: {Role or null}
application_id: {application id or null}
skill: cover-letter
date: {today ISO}
summary: Specific cover letter drafted for {role/company or lane}.
---
```

For specific applications, upsert `applications.md` with `status: saved` if no row exists. Do not advance to `applied` unless the user confirms submission. When inserting a new row, populate `comp_expected`, `source`, and `next_action_date` from the conversation if known; otherwise `-`. See [state-layer §3](../_shared/state-layer.md#3-applicationsmd-schema) for the back-compat read/write rules.

### 6. Render

Run the export script for the saved cover letter. It writes `.docx`, `.pdf`, and a `.html` preview the user can open in any browser to eyeball formatting:

```bash
node "{job_hunt_skills_root}/scripts/export-documents.mjs" my-documents/applications/{id}/coverletter.md
```

or:

```bash
node "{job_hunt_skills_root}/scripts/export-documents.mjs" my-documents/coverletter.md
```

Every run produces a PDF; the script's last stdout line reports the tier. On `EXPORT_TIER=2`, mention that installing Typst (one command, ~50MB) upgrades future PDFs to the typeset version. If Node itself is unavailable, fill `{job_hunt_skills_root}/templates/preview-template.html` natively (Tier 1) and tell the user markdown + preview are ready — installing Node unlocks the Word file and PDF. Tiers are capability unlocks, never degraded runs.

Handle content validation failures internally when possible. Report infrastructure/rendering failures with the exact rerun command.

## Common Mistakes

- **Writing a generic letter.** Stop and ask for a tighter target if you don't have enough info to write a specific and interesting cover letter.
- **Skipping claim-check.** LLMs are prone to synthesized claims and need verification.
