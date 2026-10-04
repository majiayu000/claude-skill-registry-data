---
name: resume-tailor
description: Use when the user has a specific job posting and wants to customize their resume, CV, work document, and/or cover letter for that role. Also use when they say "I'm applying to..." or share a job link.
---

## Overview

Reshape the user's work document for a specific role. This is not keyword swapping; it is adjusting which experiences lead, which language matches the posting, and how the argument is framed. Never modifies source work documents.

## Workflow

> **State layer:** reads `applications.md` for dedup, selects either `resume.md` or `cv.md` as the source work document, runs claim verification before saving, writes a numbered tailor report, and upserts the tracker at `status: saved`. See [state-layer contract](../_shared/state-layer.md).

### 0. Scaffold and select the source work document

Follow the [Workspace Preflight (state-layer §10)](../_shared/state-layer.md#10-workspace-preflight). Run `node "{job_hunt_skills_root}/scripts/scaffold-state.mjs"` if the state layer is missing; fall back to native file tools per §10 step 5 if Node is unavailable. If the scaffolder exits with the "working directory is the plugin install dir" message, surface that message verbatim and stop — the source document may already exist in the user's real workspace and is invisible only because no folder is bound. Verify the four canonical directories and two markdown files exist before continuing.

Select the source work document using [state-layer section 6](../_shared/state-layer.md#6-work-document-frontmatter-and-selection):

1. If the user names resume or CV, use that file.
2. If the job posting clearly implies a format, use the matching file when it exists.
3. If only one of `my-documents/resume.md` or `my-documents/cv.md` exists, use it.
4. If both exist and the choice is ambiguous, ask which work document to tailor.
5. If neither exists, distinguish the two cases per [state-layer §10](../_shared/state-layer.md#10-workspace-preflight): empty/missing `my-documents/` likely means the workspace is unbound (rerun the preflight, do not offer `resume-builder` yet); populated `my-documents/` without a source work document means offer `resume-builder` or proceed from pasted source material with limited evidence checking.

Read the selected file's `version` and `label`. Let:

- `{document_filename}` be `resume.md` or `cv.md`.
- `{source_document}` be `my-documents/{document_filename}`.
- `{label}` be the frontmatter label, falling back to `resume` or `CV`.

Use `{label}` in all user-facing prose.

### 0.5. Quick-tailor mode (in-chat, no scaffold)

Use this mode when invoked by `get-started`'s fast path, or whenever a first-time user pastes a resume and a posting and just wants to see what tailoring does before committing to setup. The point is a useful answer fast: a tailored draft plus an honest read in minutes, entirely in conversation, **with nothing written to disk**. The full path (steps 0–9) remains the default for users who already have a bound workspace and a source document.

**When to use it:**

- The user pasted resume/CV text (or a LinkedIn profile) rather than pointing at `my-documents/resume.md`, and
- there is no bound workspace yet, or they explicitly want a fast preview first.

**What it does — skip the plumbing, keep the honesty:**

1. **No preflight, no scaffold, no writes.** Do not run `scaffold-state.mjs` and do not confirm a workspace folder. This mode never touches disk. Evidence is the pasted material only.
2. **Analyze the posting and pick the angle** exactly as steps 3–4 describe.
3. **Tailor from the pasted source** per step 5's rules. The never-invent rule is absolute here too — with only pasted material as evidence, be *more* conservative, not less. Anything the pasted text doesn't support gets flagged, not asserted.
4. **Condensed audit pass.** Run a lightweight `resume-auditor` read focused on the single most callback-blocking issue, rather than a full bullet-by-bullet audit.
5. **Output shape** — in this order, so the most useful part lands first:
   - **60-second read-back:** one short paragraph proving you understood the material and how it maps to the posting.
   - **Two or three before/after bullet rewrites:** show the transform as a diff with the reasoning, not a wall of finished text.
   - **One honest audit flag:** the top issue, plus any claim the pasted material doesn't support, named plainly.
6. **Claim verification is paste-based.** There is no evidence layer to check against, so classify claims against the pasted source only and say so. Do not imply deeper verification happened than did.
7. **Close with the unlock hook**, per [state-layer §11](../_shared/state-layer.md#11-progress-and-reward): name what a saved workspace and source document would add (verified claims instead of flagged ones, a baseline every future application starts from), then offer to save.
   - **User wants to save** → now run step 0's preflight and scaffold, then follow the required transition below. Do not continue to steps 7–9 from pasted material alone.
   - **User is done** → that's a complete run. Do not force the save.

**Resume Builder import/update transition.** After the user confirms which pasted material should become the baseline, invoke `resume-builder` for a short import/update pass. It saves or updates `my-documents/resume.md` or `my-documents/cv.md` with the user's chosen label and an integer `version`; hard claim questions must be resolved before that save. Wait for the user to confirm the versioned source. Then invoke `resume-tailor` on that saved file, rerun claim verification, and continue through steps 1–9. The tailored artifact must record the exact `source_document` and `source_version` in its frontmatter. If the user declines the source import/update, keep the result in chat and do not save a tailored artifact.

Do not run the dedup check, tracker upsert, capture pass, or export in quick mode — those all assume disk. They apply only after the user opts to save and the run continues through the normal steps.

### 1. Dedup check

Read `my-documents/applications.md`. Compute the target `id` as `{company-slug}-{role-slug}` unless the user supplies a specific application id.

Check for both:

- Existing tracker row with that `id`.
- Existing tailored file at `my-documents/applications/{id}/{document_filename}`.

If either exists, warn the user:

> You already have a tailored {label} for **{Role} at {Company}**. Iterate on that version, replace it, or create a separate variant with a suffix like `{id}-referral`?

- **Iterate:** load the existing tailored file and continue from it.
- **Replace:** write to the same path after explicit confirmation. This is usually fine because tailored documents are per job, but `my-documents/` is gitignored, so do not imply git can recover overwritten personal files.
- **Separate variant:** use the user-confirmed suffixed id.

Warn, do not block. Users can always proceed.

### 2. Accept inputs

- **Job posting:** URL or pasted text. If URL access fails, ask for pasted text.
- **Source work document:** the selected `resume.md` or `cv.md`.
- **Source letter:** read `my-documents/coverletter.md` if it exists; treat it as source material, not a script to paraphrase mechanically.
- **Evidence:** read `story-bank.md`, `proof-assets/`, and relevant reports when needed for claim verification.

### 3. Analyze the posting

Extract:

- Role problem and likely success criteria.
- Top requirements and nice-to-haves.
- Required terminology and domain language.
- Company values and work-model signals.
- Any gaps the user should acknowledge directly.

### 4. Identify the angle

Decide the strongest honest case for this role:

- Which experiences map most directly to the posting?
- Which bullets or sections should lead?
- Which terminology should change for readability?
- Which gaps should be named instead of hidden?
- Which format conventions must be preserved from the source document?

For CV-format sources, preserve CV conventions such as Personal Statement, Education details, Languages, Publications when present, and References if present. For resume-format sources, preserve concise resume conventions. The skill adapts the content; it does not force one format into the other.

### 5. Tailor the work document

Match terminology, reorder bullets by relevance, and highlight remote or async signals where relevant. You may add or revise a Summary or Personal Statement if it strengthens the role-specific argument. Do not remove source sections unless they are clearly irrelevant to the role and the user agrees.

Never invent experience. Do not add tools, metrics, credentials, titles, employment dates, management scope, or domain exposure that the source work document or evidence layer does not support.

### 6. Tailor or write the cover letter

Address the specific role/company. Use the source letter only as raw material for voice and proof points. If it is missing, too broad, or weaker than a fresh draft from the posting plus evidence layer, write the tailored cover letter from scratch.

**Opening paragraph variants.** The opening determines whether the rest gets read. Produce **3 variants** of the opening paragraph labeled A/B/C, each with a one-line **angle label** stating what it leads with — e.g. *"A: leads with the company-need observation. B: leads with a proof-point hook tied to that need. C: leads with the why-now reason for this role."* The angles must be substantively different, not synonym rewrites. If you can only produce two honestly distinct angles, output two with a note explaining why. Surface the variants to the user, let them pick (or remix), then write only the chosen opening into `coverletter.md`. Body and closing remain single-output — they're constrained by the proof points and the ask, not by angle.

Quality bar (applies to whichever opening is chosen, plus the full letter):

- Name the company's need or problem, not just the user's job-search goal.
- Expand 1-2 proof points that map directly to that need.
- Explain why this role or company makes sense now.
- Name honest gaps directly instead of smoothing them over.
- Rewrite before save if the letter could work for five companies with only company-name swaps.

### 7. Claim verification before save

Invoke `claim-check` in tailor mode on the tailored work document and cover letter before files are persisted. Claim-check classifies concrete claims against the evidence layer and returns both class and severity.

Handle findings:

- **Cosmetic:** claim-check may auto-fix placeholders, typos, and format glitches.
- **Soft:** surface the issue, suggested fix, and underlying question. Prefer asking the underlying question over weakening the output by guesswork.
- **Hard:** block save until resolved. Contradicted or fabricated claims must not be written.

Gaps in the source work document itself still use `[ASK: ...]` placeholders and should be sent back through `resume-builder`; tailoring should not invent missing source facts.

### 8. Save outputs

Save only after verification returns a clean verdict: all cosmetic findings auto-fixed, all soft and hard findings resolved by user action.

**Tailored artifacts:**

```text
my-documents/applications/{id}/{document_filename}
my-documents/applications/{id}/coverletter.md
```

**Frontmatter on the tailored work document:**

```yaml
---
source_document: my-documents/{document_filename}
source_version: {current source version}
source_label: {label}
tailored_date: {today ISO}
application_id: {id}
---
```

**Tailor report:** write `my-documents/reports/{###}-{id}-tailor-{YYYY-MM-DD}.md`.

Report frontmatter:

```yaml
---
report_id: {###}
company: {Company}
role: {Role}
application_id: {id}
skill: resume-tailor
date: {today ISO}
summary: One-line tailoring angle.
---
```

Body: the angle chosen, important section or bullet changes, evidence gaps resolved, and any manual review notes. **For the cover letter opening: record all variants with their angle labels, then mark which one the user chose** — so a future rerun can revisit unchosen angles without redrafting from scratch. **For capture pass: record what was offered, what was accepted, where it was routed, and what was skipped** — so a future rerun or audit can trace canonical-layer growth back to its source application.

**Tracker:** upsert `applications.md` with `status: saved` if no row exists, or leave existing status alone if it has already advanced. Follow the upsert and status rules in [state-layer section 3](../_shared/state-layer.md#3-applicationsmd-schema).

When inserting a new row, also populate:

- `source` if the user mentioned how they found the role (referral, board, cold, recruiter, watch). Otherwise `-`.
- `comp_expected` if the user has already told the employer a number (recruiter screen, application form). Otherwise `-` — the field tracks what was stated, not a target band or the posted range.
- `next_action_date` to today + 7 days as the default first follow-up window when status is `saved`. The user can edit it.

If the existing tracker row was read with a missing-column header (state-layer §3 rule 6), emit the full canonical schema on write per rule 7.

**DOCX/PDF:** after the tailored artifacts, report, and tracker have been persisted, invoke the export script once with both tailored files:

```bash
node "{job_hunt_skills_root}/scripts/export-documents.mjs" my-documents/applications/{id}/{document_filename} my-documents/applications/{id}/coverletter.md
```

The script writes `.docx`, `.pdf`, and `.html` next to each input. The HTML preview lets the user eyeball formatting in a browser without opening the docx — DOCX and PDF remain canonical for submission. Run the export after tracker state is saved so rendering failure does not block the application record.

Every run produces a PDF; the script's last stdout line reports the tier. On `EXPORT_TIER=2`, mention that installing Typst (one command, ~50MB) upgrades future PDFs to the typeset version. On `EXPORT_TIER=3`, nothing to add. If Node itself is unavailable, fill `{job_hunt_skills_root}/templates/preview-template.html` natively (Tier 1) and tell the user markdown + preview are ready — installing Node unlocks the Word file and PDF. Tiers are capability unlocks, never degraded runs.

Handle failures:

- **Content validation failure:** fix unresolved placeholders, comments, `[ASK:]`, `[VERIFY:]`, or `year TBD` internally and rerun. Ask the user only when the blocker requires a missing fact.
- **Infrastructure/rendering failure:** report the failed file and exact rerun command.

### 8.5. Capture pass

Once the application is on disk, diff the tailored output against the source work document and source cover letter (if one exists). The goal: identify content that is **meaningfully different** — newly verified evidence the user signed off on — and offer to capture it in the right canonical home before the skill exits.

**Floor threshold.** Skip this step silently if nothing passes the meaningfulness bar. Do not prompt with "0 captures available."

**Meaningfulness.** Use judgment. The bar is "would future-me want this in canonical evidence, or is it just role-specific phrasing?"

| Class | Examples | Action |
|---|---|---|
| Meaningfully new fact | New metric, new tool/skill, new scope (team size, budget, users), new outcome, new role detail not previously stated | Capture candidate |
| New STAR+R narrative | Story content surfaced during tailoring that has situation, task, action, result shape | Capture candidate |
| Notable cover-letter phrasing | Strong opening, sharp "why now" paragraph, reusable hook tied to a target lane | Capture candidate |
| Phrasing variant | Same fact in posting vocabulary, synonym swap, clause reorder, active/passive change | Skip |
| Reordering / emphasis | Existing content moved or promoted | Skip |
| Removed for fit | Source content cut from tailored version | Skip |

**Route each candidate** to a proposed destination:

- **New bullet, metric, tool, or scope under an existing role** → source work document (`resume.md` / `cv.md`)
- **STAR+R-shaped narrative** → `story-bank.md`
- **Reusable case study with metrics and narrative** → `proof-assets/{slug}.md`
- **Notable cover-letter phrasing** → source `coverletter.md` if one exists for this lane; otherwise offer to seed one
- **Ambiguous** → ask the user

**Prompt shape:**

> Claim-check passed and the tailored {label} introduced 2 new facts not in your source:
>
> 1. "Reduced onboarding time 40% via async docs"
>    Propose: capture as new bullet under {Role at Company} in {document_filename}
>    [accept / redirect to story-bank / redirect to proof-asset / skip]
>
> 2. "Led incident response during the 2024 Stripe outage"
>    Propose: capture as story-bank entry (STAR+R shape detected)
>    [accept / redirect to resume bullet / skip]

**Write semantics:**

- **Source work-document captures:** hand off to `resume-builder` in update mode with the new content. `resume-builder` owns the `version` bump and `updated`. Never write to `resume.md`/`cv.md` directly from this skill.
- **Story-bank captures:** append to `story-bank.md` using [state-layer §7](../_shared/state-layer.md#7-story-bank-schema). Generate a kebab-case `id`, infer `themes` from content, set `created` to today, `usage: []`.
- **Proof-asset captures:** write `my-documents/proof-assets/{slug}.md`. Confirm the slug with the user.
- **Source cover-letter captures:** append to or seed `my-documents/coverletter.md`. Confirm before creating from scratch.

Captures are derived from material already validated by claim-check, so no second verification pass is needed. Skip the prompt entirely when nothing qualifies.

### 9. Summary and post-run prompt

Report:

- Files written.
- Key changes and why.
- Alignment strengths.
- Any remaining manual review notes.
- The tracker row for this application.
- Anything captured to the canonical layer, or note that nothing qualified.

Then the closing beats from [state-layer §11](../_shared/state-layer.md#11-progress-and-reward):

- **What this unlocked** — one sentence naming what the user can now do, e.g. "This application is on your board and anything we captured strengthens every future tailor." If the capture pass banked a story or proof asset, name that gain specifically.
- **Momentum pulse** — since this run wrote `applications.md`, print the tracker momentum line (`node "{job_hunt_skills_root}/scripts/profile-strength.mjs" --pulse`, or derive it natively): in-flight count, interviewing count, and the nearest next action. This is the user's scoreboard; frame it around progress and the next concrete step, never as pressure to apply more.

Then ask:

> Did you submit this application? If so, I can update the status to `applied`.

If the user confirms, upsert `applications.md` with `status: applied` and `updated: {today ISO}`. Only the user can trigger this transition, then reprint the momentum pulse so the advance is visible.

## Cover-Letter-Only Mode

When invoked by the `cover-letter` skill or when the user explicitly asks for only a cover letter:

- Still select and read the source work document for evidence.
- Still run claim verification before save.
- Save only `my-documents/applications/{id}/coverletter.md` for a specific role, or `my-documents/coverletter.md` only when building a source letter for a tightly defined lane.
- Do not generate a generic letter.

## Common Mistakes

- **Keyword stuffing.** Match terminology naturally; do not cram keywords.
- **Only changing the top section.** Tailoring means relevance ordering across the document.
- **Direct writes to source.** Capture pass surfaces meaningfully new facts as user-gated candidates and hands off to `resume-builder` for source updates. This skill never modifies `resume.md`/`cv.md` directly.
- **Over-prompting capture pass.** Skip silently when nothing is meaningfully different. Posting-vocabulary rewording is not a capture candidate.
- **Forcing CV into resume or resume into CV.** Preserve the selected source format.
- **Tightening inference beyond evidence.** If the source states facts separately, do not assert a new connection unless the user confirms it.
