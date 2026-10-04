---
name: claim-check
description: Use when the user wants a final truth pass before submitting a resume, CV, cover letter, LinkedIn section, or application package. Also use when they ask whether a draft contains unsupported, inflated, or hallucinated claims.
---

## Overview

Detect and classify claims that are not supported by the evidence layer. This is a fabrication check, not a staleness check. It catches hallucinated metrics, invented tools, inflated scope, and projects that never existed before materials go to an employer.

The same verification mechanism runs in three modes:

- **Standalone** — user-facing entry point. Runs when the user asks for a final truth pass before submitting an application package.
- **Tailor** — invoked internally by `resume-tailor` and `cover-letter` before they save tailored application materials.
- **Initial-build** — invoked internally by `resume-builder` before it saves a new or rebuilt source work document.

Use the name `claim-check` in conversation and reports regardless of mode.

## Workflow

> **State layer:** reads source work documents, tailored application materials, story bank, proof assets, and reports. In standalone mode, writes a numbered `claim-check` report. Tailor and initial-build modes return findings to the caller and do not write a standalone report. See [state-layer contract](../_shared/state-layer.md).

### 1. Identify the mode

Determine which mode is running based on how the skill was invoked:

- **Standalone** — the user invoked this skill directly, or another skill called it without a mode argument.
- **Tailor** — `resume-tailor` or `cover-letter` passed a candidate tailored work document and/or cover letter before save.
- **Initial-build** — `resume-builder` passed generated content plus the current interview transcript before first save or rebuild.

Steps 4–7 (read evidence, scope scan, extract, classify, remediate) are identical across modes. Modes differ in what is scanned and what happens after findings are reported.

### 2. Scope inputs by mode

**Standalone mode:**

Ask only if the target is not obvious. Scope options:

- A pasted draft.
- A specific file path.
- A specific application id, company, or role.
- All application materials under `my-documents/applications/`.

If the user says "before I submit" and a current application is clear, check that application package: tailored work document plus cover letter.

**Tailor mode:**

The caller passes the candidate tailored work document and/or cover letter before persistence. The caller blocks save until soft and hard findings are resolved.

**Initial-build mode:**

The caller passes the generated content plus the current interview conversation. Treat the conversation transcript and any user-supplied source material (existing resume, LinkedIn export, notes) as highest-trust evidence. Skip source-version comparison because the source work document is not saved yet.

Run `node "{job_hunt_skills_root}/scripts/scaffold-state.mjs"` if state files are missing.

### 3. Read evidence

Read available evidence in priority order:

1. Source work documents: `my-documents/resume.md` and/or `my-documents/cv.md` (or the interview transcript in initial-build mode).
2. `my-documents/story-bank.md`.
3. `my-documents/proof-assets/*.md`.
4. `my-documents/reports/*.md`.

In tailor and standalone modes, also read the targeted tailored work documents (`my-documents/applications/*/resume.md`, `my-documents/applications/*/cv.md`) and tailored cover letters (`my-documents/applications/*/coverletter.md`).

For each tailored work document, read frontmatter:

- Preferred: `source_document`, `source_version`, `source_label`, `application_id`.
- Legacy fallback: `derived_from_version` as `source_version`; infer `source_document` from the tailored filename.

If no source frontmatter exists, deep scan the file and warn.

If no saved source work document exists in standalone mode, proceed on pasted source material but warn that evidence checking is limited to what the user provides in the session.

### 4. Decide scan depth

For each tailored work document:

- If `source_version` matches the current version of `source_document`, light scan only bullets or sections that diverge materially from the source.
- If `source_version` is older than the current source version, deep scan every concrete claim.
- If source metadata is missing or the source document no longer exists, deep scan and warn.

For cover letters, always scan every concrete claim because letters routinely synthesize facts across sources.

In initial-build mode, deep scan every concrete claim against the interview transcript and supplied source material.

### 5. Extract claims

Extract concrete, probeable claims:

- Quantitative claims: numbers, percentages, dates, team sizes, revenue, time spans.
- Named projects, products, publications, launches, case studies, or initiatives.
- Tools, languages, platforms, frameworks, methodologies, and credentials.
- Role specifics: titles, scope, reporting lines, management or mentorship responsibility.
- Outcome claims: business impact, customer impact, research impact, process changes.

Ignore purely stylistic claims unless they imply evidence, seniority, or scope.

### 6. Classify each claim

Search the evidence layer in priority order from step 3.

**Class:**

| Class | Rule |
| --- | --- |
| Supported | Direct or faithful paraphrase match in priority sources 1–3, or explicit interview answer in initial-build mode. |
| Unverifiable but plausible | Hit only in reports. |
| Unverifiable | No hit anywhere. |
| Contradicted | Conflicts with a higher-priority source. |

**Severity:**

| Severity | Applies to | Handling |
| --- | --- | --- |
| Cosmetic | Unresolved placeholders, stale `[ASK:]` or `[VERIFY:]` markers resolved in conversation, typos, format glitches. | Safe to auto-fix. |
| Soft | Plausible but unsupported paraphrases, inference tightening, dropped qualifiers, or subtle padding. | Surface with suggested fix and underlying question. |
| Hard | Contradicted claims, fabricated employers/dates/metrics, invented credentials, or invented experience. | Block save. |

Common soft patterns to check explicitly:

- **Inference tightening:** evidence states facts A and B separately; output asserts a connection between them.
- **Invented tool specifics:** evidence says "AWS" or "databases"; output lists specific services or engines the user never named.
- **Dropped proficiency qualifiers:** evidence says "learning", "intermediate", "scripting only", or similar; output strips the hedge.
- **Paraphrase-that-tightens:** "contributed to" becomes "led", "co-supervised" becomes "managed", or "worked on" becomes "built".

Classification is a prompt for review, not a final truth verdict. Some legitimate claims live in the user's head and need to be added to the source document or story bank.

### 7. Remediate by severity

**Cosmetic findings:** auto-fix only placeholders, stale markers resolved in conversation, typos, and obvious format glitches. Never auto-fix a claim-level span.

**Soft findings:** show the user:

- File path and rough location.
- The offending span.
- What the output asserts.
- What the evidence supports.
- A suggested fix that restores fidelity.
- The underlying question that would let the stronger claim stand honestly.

Preferred options:

1. **Answer the underlying question** so the real fact can be used.
2. **Adjust** to the suggested faithful version.
3. **Confirm and add evidence** to the source work document or story bank.

**Hard findings:** block save until resolved. The user may correct the source, adjust the claim, or replace the span with a supported claim.

In tailor and initial-build modes, return findings to the caller; the caller blocks save and resolves with the user. In standalone mode, resolve directly with the user. Do not silently rewrite claim-level spans — cosmetic fixes are the only auto-fixes.

### 8. Save the report (standalone mode only)

Tailor and initial-build modes do not write a standalone report — findings flow back to the caller, which records them in its own report.

Write `my-documents/reports/{###}-claim-check-{YYYY-MM-DD}.md`.

Report frontmatter:

```yaml
---
report_id: {###}
company: {Company or null}
role: {Role or null}
application_id: {application id or null}
skill: claim-check
date: {today ISO}
summary: Checked {N} files - {A} supported, {B} unverifiable, {C} contradicted.
---
```

If scoped to a tracked application, set `company`, `role`, and `application_id`.

Body structure:

- Overview counts by class and severity.
- Per-file findings.
- Each flagged claim with exact span, classification, best evidence source, and recommended action.
- Any user-confirmed actions taken.

### 9. Close

Report:

- Whether the package is safe to send.
- Any hard blockers.
- Any soft claims the user chose to confirm, adjust, or remove.
- Files changed, if any cosmetic fixes were applied.

If the user confirmed new facts during remediation, recommend adding them to the source work document or story bank so future checks pass.

If the materials are clean and tied to an application, ask whether the user submitted them. If yes, offer to advance the tracker to `applied`.

## Common Mistakes

- **Calling this a fact guarantee.** It is an evidence check against saved materials, not a background investigation.
- **Treating classification as truth.** A claim can be real but absent from the evidence layer.
- **Overflagging faithful paraphrases.** Same fact in different words is supported.
- **Ignoring reports as weak evidence.** Reports can downgrade a claim from unverifiable to unverifiable but plausible, but they are not primary evidence.
- **Silent claim patching.** Only cosmetic findings auto-apply. Soft and hard claim-level findings require user action.
- **Ignoring pasted drafts.** If the user supplies only pasted text, check that text against whatever evidence they also provide.
