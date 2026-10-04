---
name: resume-builder
description: Use when the user wants to create or update a source work document in resume or CV format, or create a source cover letter from scratch. Triggers on US resumes ("build my resume") and UK/EU-style work CVs ("build my CV", "I need a CV for a UK role", "European CV"). US academic CVs are out of scope. For first-time users setting up from a fresh clone, prefer `get-started`.
---

## Terminology

Two document categories:

- **Work document:** the user's source career document. It may be saved in resume format at `my-documents/resume.md` or CV format at `my-documents/cv.md`. These are format variants of the same workflow; downstream resume skills must accommodate either.
- **Cover letter:** an accompanying letter for a specific role, company, or tightly defined target lane. `my-documents/coverletter.md` is a source letter, not permission to create something generic enough to send anywhere.

Format-specific conventions:

- **Resume format:** US 1-2 page work document with concise sections and optional Professional Summary.
- **CV format:** UK/EU 1-2 page work document with Personal Statement, degree classification when relevant, Languages with CEFR when relevant, and "References available on request" where expected. Not the US academic CV.

**Disambiguation rule:** If the user says "CV" without naming a region, ask whether they need a UK/EU-style work CV or are using CV to mean a US resume. If academic signals appear, say directly that academic CVs with publications, grants, and teaching sections are out of scope; offer a UK/EU-style work CV or US-style resume for industry applications.

**Vocabulary rule:** Mirror the user's word. If they say "CV," say "CV." If they say "resume," say "resume." Save that word in the `label` frontmatter field and preserve it on future edits.

## Workflow

> **Onboarding hand-off:** If the user appears to be on a fresh clone or is new to Job Hunt Skills, hand off to `get-started`. This skill focuses on the document itself.
>
> **State layer:** this skill owns source work-document version bumps. See [state-layer contract section 6](../_shared/state-layer.md#6-work-document-frontmatter-and-selection).

### 1. First-run scaffolding

Follow the [Workspace Preflight (state-layer §10)](../_shared/state-layer.md#10-workspace-preflight).

- **If `my-documents/` does not yet exist** at the resolved path, hand off to `get-started` for the workspace confirmation flow. Do not run the scaffolder yourself — the user needs the novice-friendly "where will my files live" conversation before any file is written.
- **If `my-documents/` already exists**, run `node "{job_hunt_skills_root}/scripts/scaffold-state.mjs"` to fill in any missing pieces. If it exits with the "working directory is the plugin install dir" message, surface that message verbatim and stop. If it fails for any other reason (Node missing, no shell access), fall back to creating any missing structure with native file tools per state-layer §10 step 5.
- **Verify before writing.** Regardless of which path was taken, confirm the four canonical directories and two markdown files exist under `my-documents/` before producing a resume. A skill that generates a resume into an unscaffolded workspace is the failure mode this check exists to prevent.

On first scaffold per session, mention the path once: "Your files will live under `{absolute path}`."

### 2. Decide scope and format

Clarify:

- Resume format, CV format, cover letter, or a combination.
- New build, rebuild, or update.
- Target country/region and target roles.
- Whether the user has an existing resume, CV, LinkedIn export, job posting, or notes.

If updating, select the existing work document using [state-layer section 6](../_shared/state-layer.md#6-work-document-frontmatter-and-selection), read its frontmatter, and preserve `label`.

### 3. Gather existing materials

Ask:

> Do you have an existing resume, CV, LinkedIn profile, or notes you'd like to work from? If not, we can build from scratch together.

If provided, read and analyze it before asking follow-ups. If starting from scratch, run the structured interview below.

### 4. Structured interview

**Set expectations before the first prompt.** Before any structured form, batched questionnaire, or interview-style question is presented, briefly recap in conversational prose: what's about to happen (gathering work history, accomplishments, target roles), how long it will take, that blanks are fine and gaps will be surfaced later rather than invented, and what the user will have at the end. Only after that recap may the interview begin. A batched form is acceptable; a batched form delivered *before* the user knows what it's for is what testers reported as confusing.

**Run the interview as episodes, not one long form.** A 20-minute unbroken interview is a slog, especially for a first-time user. Break it into chapters, and after each chapter show visible progress so the user feels the document taking shape rather than filling out a survey:

- **Chapter 1 — work history:** current and prior roles, titles, timeframes. After it, show a *skeleton draft* — the document's structure with roles and dates in place, bullets still to come. The user sees an actual document appear.
- **Chapter 2 — accomplishments and proof:** probe outcomes per role. After it, show the bullets sharpening on the roles already on screen.
- **Chapter 3 — targeting and extras:** target roles, skills, education, CV-format extras, cover-letter specificity if in scope.

Each chapter ends with a one-line "here's what we have so far" beat before the next begins. Keep chapters short; seeing the resume take shape after five minutes makes the next five worth it. This is presentation, not a different data model — the same fields get gathered, just paced so progress is visible.

Probe for outcomes, not responsibilities.

- **Current role:** title, day-to-day, 4-6 strongest accomplishments. Push for numbers, timeframes, scope, users, revenue, costs, quality, speed, risk, or research impact.
- **Internal promotions:** if tenure at an employer is 3+ years and the user names one title, ask whether they held other roles there.
- **Prior experience:** 3-4 accomplishments per recent role; 1-2 is fine for older roles.
- **Skills/tools:** technologies, platforms, certifications, methodologies, spoken languages when relevant.
- **Target roles:** roles, industries, seniority, region, and work model.
- **Cover letter specificity:** only if a cover letter is in scope. Ask for exact role or tightly defined lane, employer or company type/stage, the problem they want to solve, proof points, and any honest gap.
- **Remote signals:** remote experience, cross-timezone work, documentation, independent delivery, async habits, or self-directed projects.
- **Education:** degree, school, year. For CV format, also ask degree classification and whether Education should lead for early-career users.
- **Story/angle:** specialist, generalist, leader, career changer, academic-to-industry, or another honest frame.
- **CV-format extras:** Personal Statement seed, languages with proficiency, target country/region, and whether Publications/Selected Talks are relevant for industry.

**STAR+R inline enrichment.** While probing accomplishments, watch for ones with clear STAR shape (situation, task, action, result). When you find one, ask the Reflection prompt inline — "What would you do differently, or what did you learn?" — so the story is complete enough to bank in step 6.5 without a second round of prompting. Skip the prompt for routine accomplishments that are not story-bank candidates.

### 5. Generate outputs

Produce markdown for the requested documents. Do not save yet; claim verification runs first.

**Resume format:** follow `{job_hunt_skills_root}/templates/resume-template.md`. Use achievement bullets: action + work + outcome. Use past tense throughout, including current role. Include remote-readiness evidence where relevant. Target path: `my-documents/resume.md`.

**CV format:** follow `{job_hunt_skills_root}/templates/resume-eu-template.md`. Lead with a Personal Statement rather than a US-style Professional Summary. Preserve useful academic-to-industry evidence such as selected publications or talks only when it strengthens the target role. Skip photo, DOB, full address, and marital status unless the user explicitly needs a locale where they are expected. Target path: `my-documents/cv.md`.

**Cover letter:** generate `my-documents/coverletter.md` only when there is enough specificity to write something the user would actually send. Minimum bar: one exact role or tight lane, one concrete employer or company type/stage, one clear problem, and two proof points. If the answers are vague, say so and skip the letter.

Cover letter quality bar:

- Lead with the employer's need and relevant proof.
- Expand 1-2 proof points instead of prose-copying the work document.
- Explain why this role or lane makes sense now.
- Name honest gaps directly when useful.
- Rewrite or skip if the letter survives a five-company swap.

### 6. Claim verification before save

Invoke `claim-check` in initial-build mode with the generated content and current interview conversation as evidence.

Handle findings:

- **Cosmetic:** auto-fix placeholders, typos, and format glitches.
- **Soft:** stop and surface the issue, suggested fix, and underlying question. Prefer asking the user the underlying question.
- **Hard:** block save. Fabricated employers, dates, metrics, credentials, or experience must be corrected before the file exists.

Only save after every non-cosmetic finding is resolved.

### 6.5. Capture pass for interview overflow

Source work documents are space-constrained. A structured interview surfaces more material than fits in 1-2 pages. After claim-check passes, identify content the user told you that did not make it into the work document but has a natural canonical home outside it.

**Floor threshold.** Skip silently if nothing qualifies.

**Meaningfulness.** Same bar as `resume-tailor` capture pass: would future-me want this in canonical evidence, or is it scaffolding chatter? Routine context, vague aspirations, and accomplishments already covered by a saved bullet are not capture candidates.

**Route each candidate:**

- **STAR+R-shaped narrative captured during the interview** → `story-bank.md` entry
- **Reusable case study with metrics and ≥1 paragraph of narrative** → `proof-assets/{slug}.md`
- **Ambiguous** → ask the user

**Prompt shape:**

> The interview surfaced 2 stories that didn't fit in the work document but are worth banking:
>
> 1. "Stripe outage incident response" — STAR+R complete
>    Propose: capture as story-bank entry [accept / redirect / skip]
>
> 2. "Migration of legacy billing system, 6-month project, $2M cost reduction"
>    Propose: capture as proof-asset {legacy-billing-migration} [accept / redirect / skip]

**Write semantics:** story-bank entries follow [state-layer §7](../_shared/state-layer.md#7-story-bank-schema) — kebab-case `id`, themes inferred from content, `created` set to today, `usage: []`. Proof-assets use a confirmed kebab-case slug. Captures are derived from material the user just told you, validated implicitly by the conversation, so no second claim-check pass is needed. Captured artifacts are persisted in step 7 alongside the source work document.

### 7. Save and version

Source work-document frontmatter:

```yaml
---
version: 1
updated: 2026-04-08
label: resume
---
```

On first build, set `version: 1`. On update, increment only the file changed and preserve `label` verbatim. If both `resume.md` and `cv.md` exist, they version independently because they are separate files, but the skills treat them as work-document format variants.

`coverletter.md` does not need frontmatter.

**Captured artifacts from step 6.5** (if any) are written in this step alongside the source work document — story-bank entries appended to `story-bank.md`, proof-assets created at `my-documents/proof-assets/{slug}.md`. Captures do not affect the source work document's `version`.

### 8. Export DOCX, PDF, and HTML preview

After writing markdown, invoke the export script once with all files written:

```bash
node "{job_hunt_skills_root}/scripts/export-documents.mjs" my-documents/resume.md my-documents/coverletter.md
```

or:

```bash
node "{job_hunt_skills_root}/scripts/export-documents.mjs" my-documents/cv.md my-documents/coverletter.md
```

In single-document modes, pass only the file written. The script writes `.docx`, `.pdf`, and `.html` next to each input. The `.html` is a browser-openable preview that mirrors the page geometry; DOCX and PDF remain canonical for submission. Every run produces a PDF — its last stdout line reports which renderer produced it:

- `EXPORT_TIER=3` — the PDF was typeset with Typst. Nothing to add.
- `EXPORT_TIER=2` — the PDF came from the built-in renderer. Mention that this is the standard render, and that installing Typst (one command, ~50MB: `brew install typst` / `winget install --id Typst.Typst` / `snap install typst`) upgrades future PDFs to the typeset version.

If Node itself is unavailable, fall back to Tier 1: fill `{job_hunt_skills_root}/templates/preview-template.html` (`{{name}}`/`{{contact}}`/`{{body}}` slots) with native file tools and tell the user their markdown and browser-openable preview are ready — installing Node unlocks the Word file and PDF. Report tiers as what the user has, plus the one command that unlocks the next tier — never as a degraded run.

Handle failures:

- **Content validation failure:** fix unresolved placeholders, template comments, `[ASK:]`, `[VERIFY:]`, or `year TBD` internally and rerun. Ask the user only when a missing fact is required.
- **Infrastructure/rendering failure:** report the file, error, and exact rerun command.

### 8.5. Close the run

After the files are saved and exported, end with the two closing beats from [state-layer §11](../_shared/state-layer.md#11-progress-and-reward):

- **What this unlocked** — name the new capability in plain terms, e.g. "Your {label} now lives here as a source document, so tailoring to a role, honest audits, and interview prep all draw from it — and any stories we banked will back up claims automatically." Not a file count; a capability.
- **Where things stand** — show the profile-strength line (`node "{job_hunt_skills_root}/scripts/profile-strength.mjs"`, or derive it natively when Node is unavailable) so the user sees their progress and the single highest-leverage next step. Frame it as momentum, not a to-do list.

### 9. Modes

- **Resume format:** writes `my-documents/resume.md`.
- **CV format:** writes `my-documents/cv.md`.
- **Just cover letter:** requires specificity; do not force a generic letter.
- **Update:** select the relevant source work document, ask what changed, revise, and bump only that file's `version`.
- **Capture pass hand-off:** when invoked by `resume-tailor` capture pass with new content already specified, skip the "what changed" prompt, integrate the content into the appropriate role/section, run claim-check on the integrated draft, and bump `version` on save. The user has already approved the content; do not re-litigate it.

## Common Mistakes

- **Inventing metrics.** Use `[ASK: what was the result?]` for gaps.
- **Dropping proficiency qualifiers.** Preserve "learning", "intermediate", "scripting only", "~1 year", or similar hedges.
- **Inventing tool specifics.** Do not expand "AWS" into service names, "databases" into engines, or "CI/CD" into tools unless the user named them.
- **Over-polishing.** The document should sound like the user at their most articulate.
- **Ignoring the angle.** Every work document needs a coherent story.
- **Skipping remote signals.** Surface evidence of self-direction, async work, documentation, or independent delivery when relevant.

## Reference

See [../../guides/resume-philosophy.md](../../guides/resume-philosophy.md) and [../../guides/ats-myths.md](../../guides/ats-myths.md).
