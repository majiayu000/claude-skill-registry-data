---
name: resume-writer
description: Rewrite and enhance resumes using a persistent library of principles harvested from real recruiters, hiring managers, and HR professionals. Always trigger immediately when the user's message starts with "rw". Also trigger on "resume writer", "rewrite my resume", "enhance my resume", "fix my resume", "review my resume", or any request to improve, audit, or critique a resume. Also trigger when the user pastes a recruiter or hiring manager post (LinkedIn, blog, Reddit) and says "add to my library", "add insight", "rw add", or indicates they want to capture it as a resume principle. Also trigger on "two page", "two-page", "trim to two pages", "fit on two pages", "two page audit", or "page trim" to run the two-page audit mode. Handles paste, .docx, .pdf, and screenshot inputs. Produces a full rewrite plus a condensed audit by default, with full forensic line by line audit only when requested. General-purpose skill that works for any user's resume, not just the skill owner.
version: 1.2.0
---

# Resume Writer

## Intent

Rewrite, audit, score, and target resumes with measurable impact, recruiter skim value, and role-specific positioning.

## Use When

- The user explicitly asks for `resume-writer`.
- The request matches the triggers or workflow described below.
- The task benefits from a reusable, structured output instead of a one-off answer.

## Do Not Use When

- Do not use to fabricate credentials, invent employment history, write unrelated bios, or submit applications directly.
- Required context is missing and cannot be reasonably inferred.
- A more specific skill in this repo is a better match.

## Workflow

1. Identify the exact task and available source material.
2. Apply the domain rules and output format in this skill.
3. State assumptions, uncertainty, and missing inputs clearly.
4. Return the requested artifact, recommendation, or review in a practical format.
5. Check the result against the validation checklist before finishing.

## Constraints

- Do not fabricate missing facts, measurements, dates, sources, or user context.
- Keep output aligned with Mick's direct, practical communication style unless the skill says otherwise.
- Preserve safety, legal, medical, financial, and operational boundaries stated in this file.
- Prefer concise, usable output over broad explanation.

## Validation Checklist

- [ ] The output matches the skill's intended task and platform.
- [ ] Required inputs, assumptions, and uncertainty are explicit.
- [ ] Safety, scope, and source limits are respected.
- [ ] The response follows the requested format or the skill's default output format.
- [ ] The result is practical enough to use without another cleanup pass.

Rewrites resumes using a persistent, user-curated library of principles harvested from recruiters, hiring managers, and HR professionals. Every change made is traceable back to a specific principle in `insights/principles.md` or a pattern in `references/common-patterns.md`.

`tips/` is the staging area for newly collected posts, weekly review packets, and candidate advice that has not yet been promoted into the authoritative library. Use it to keep the skill current without treating every fresh post as permanent truth.

## Three modes

This skill operates in one of three modes. Detect which one before proceeding.

### Mode 1: Enhance a resume (default)

Triggered when the user provides a resume (pasted, .docx, .pdf, or screenshot) and asks for a rewrite, review, audit, or critique.

Go to the **Enhance Workflow** section.

### Mode 2: Add an insight to the library

Triggered when the user pastes or uploads a recruiter/HR post and says something like "rw add", "add to library", "add this insight", or pastes a post without a resume present.

Go to the **Add Insight Workflow** section.

### Mode 3: Refresh tips staging area

Triggered when the user asks to refresh, review, triage, summarize, or organize recruiter/HR posts for future resume guidance, or refers to the weekly `tips/` update.

Go to the **Refresh Tips Workflow** section.

### Mode detection rules

- If a resume-shaped input is present (text with experience/education sections, or a .docx/.pdf/image file that looks like a resume), default to Enhance mode. Do not ask.
- If only a recruiter/HR post is present with no resume, default to Add Insight mode. Do not ask.
- If the user is asking to maintain the source pipeline, weekly refresh process, source roster, or `tips/` contents, use Refresh Tips mode.
- Only ask "enhance or add to library?" when the input is genuinely ambiguous (e.g., a LinkedIn profile export that could be either).

## Output Mode Handling

Default output mode is `human`.

`json-output-spec.md` is the authoritative contract for machine-readable output.

Switch output mode when user intent indicates automation needs:

- If user asks for automation, API, JSON, machine-readable, structured output, pipeline use, CLI use, n8n use, or parsing, switch to `json` or `both`.

Mode behavior:

- `human`: return the standard readable audit output.
- `json`: return valid JSON only, matching `json-output-spec.md`.
- `both`: return standard readable audit first, followed by a JSON block that matches `json-output-spec.md`.

Hard enforcement rules:

- In `json` mode, return valid JSON only.
- In `json` mode, do not use markdown fences.
- In `json` mode, do not include prose outside the JSON object.
- In `both` mode, the JSON block must still fully conform to the schema.
- Do not omit required fields from `json-output-spec.md`.
- When uncertain between two adjacent values, choose the more conservative lower score.
- When a field cannot be supported by evidence, use `null` or an empty array instead of guessing.

---

## Enhance Workflow

Read before enhancing or auditing a resume; also read the scoring reference for score outputs. [Full workflow](references/enhance-workflow.md). Paths mentioned in that reference are relative to this skill directory. Its rules are required for the selected mode.

## Scoring Workflow

Read whenever scoring a resume or producing machine-readable scores. [Full workflow](references/scoring-workflow.md). Paths mentioned in that reference are relative to this skill directory. Its rules are required for the selected mode.

## Add Insight Workflow

Read only for Add Insight mode. [Full workflow](references/add-insight-workflow.md). Paths mentioned in that reference are relative to this skill directory. Its rules are required for the selected mode.

## Refresh Tips Workflow

Read only for Refresh Tips mode. [Full workflow](references/refresh-tips-workflow.md). Paths mentioned in that reference are relative to this skill directory. Its rules are required for the selected mode.

## Principles of using this skill

- **Every audit finding must map to a library principle, a pattern in `common-patterns.md`, or be clearly flagged as "Not-in-library observations".** Do not invent principles.
- **Library principles win over patterns** when both apply. Library entries have attribution and specific framing; patterns are the fallback.
- **`tips/` is a staging layer, not the source of truth.** Raw or newly reviewed tips can inform future library growth, but only `insights/principles.md` and `references/common-patterns.md` are authoritative for normal audits.
- **Never fabricate metrics.** If a bullet needs a number the user did not supply, flag it in the "Missing data" section and rewrite with the strongest truthful framing available.
- **Preserve facts, rewrite framing.** Employers, titles, dates, certifications, and education details are never changed. Everything else is fair game.
- **The library grows over time.** If during a rewrite you notice the user would benefit from a principle not yet captured, mention it in "Next steps": "This weakness maps to a common recruiter complaint I do not have in your library yet. Want to add it?"
- **General-purpose tone.** Do not assume the resume belongs to the skill owner. Match the voice of the existing resume unless the user requests a tone change.

## Operational Constraints

- If `insights/principles.md` or `references/common-patterns.md` cannot be read, continue in degraded mode and clearly state that the audit is limited.
- If resume extraction comes from an image, screenshot, or scanned PDF and quality is poor, label the audit as partial.
- If the resume is multi column, table heavy, or visually complex, proceed but warn that parsing fidelity may be reduced.
- If a job description, target role, or target company is provided, prioritize alignment to that target over generic optimization.
- If the environment cannot write to `insights/principles.md`, return exact append ready principle text and state that manual update is required.
- If `tips/` files cannot be read, continue without them. Do not pretend fresh-source review was performed when the staging files were unavailable.

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- A current resume, target role, or job posting.

Example prompts:

- `Use resume-writer to rewrite my resume for a PowerShell automation engineer role.`
- `Score this resume against the job posting and tell me what needs to change first.`
- `Show me an example prompt for using this skill with a resume and target job description.`

