---
name: scigs
description: Use when an existing academic manuscript must be adapted to a named journal, especially DOCX submissions requiring current Instructions for Authors, conservative reference-style conversion, blinded or non-blinded variants, figure/table/supplement checks, and a traceable pre-submission package.
---

# SCIGS — Scientific Journal Submission Formatter

This is the SciXZ child Skill for journal-specific manuscript formatting and submission-package preparation.

This skill combines two complementary patterns: package-first fact recovery and pre-submit verification, plus journal-family baselines and explicit journal profiles. It is DOCX-first and content-locked: formatting is allowed, silent scientific rewriting is not.

## When It Applies

Use it for requests such as:

- “Format this existing Word manuscript for Journal X.”
- “Convert this paper to another journal’s submission style.”
- “Prepare blinded and non-blinded DOCX files.”
- “Check figures, supplements, references, and metadata before submission.”

Do not use it to rewrite scientific claims, repair unsupported results, invent declarations, or click a final external submission button.

## Required Workflow

1. **Lock the source.** Copy the manuscript and supplied package. Record filenames and SHA-256 values. Inventory DOCX parts, fields, metadata, figures, tables, and supplements.
2. **Verify the journal.** Use the current official journal or publisher Instructions for Authors and article-type page. A family profile is only a baseline. Save the source URL, access date, evidence snapshot, and unresolved conflicts in `journal_requirements.yaml`.
3. **Review extracted rules.** Run `scripts/fetch_official_requirements.py` only to create candidate rules. Do not mark a rule `verified` until the official page has been read and the rule is confirmed. Map confirmed rules to explicit `actions`.
4. **Format conservatively.** Run `scripts/format_docx.py`. It applies only explicit actions such as page size, margins, font, spacing, line numbering, and page numbering. It refuses to overwrite the source and compares body/footnote text before and after.
5. **Convert references safely.** Keep Zotero/EndNote/Mendeley fields intact. If dynamic fields are present, `scripts/reference_style.py` blocks plain-text replacement by default. For plain numeric references, use DOI metadata from `scripts/fetch_references.py`, then convert only mapped entries.
6. **Prepare anonymity.** If the journal requires blinded review, run `scripts/anonymize_docx.py` on a copy, then `scripts/anonymity_scan.py` with all known author, institution, repository, grant, and project terms. A low scan result is not proof of anonymity; inspect comments, revisions, custom properties, filenames, and supplements manually.
7. **Audit assets.** Run `scripts/asset_inventory.py` and `scripts/reference_audit.py`. Reconcile in-text citations, captions, embedded/separate figures, table numbering, supplements, file names, and technical limits from the official instructions.
8. **Render and inspect.** Run `scripts/render_docx.py`; visually inspect every page at readable zoom. A missing renderer, failed conversion, clipping, overlap, broken table, missing glyph, or wrong page break is a blocker.
9. **Package.** Run `scripts/prepare_submission.py`, which writes `FORMAT_CHANGE_LOG.md`, `submission-result.json`, and an explicit `submission-package/`. Only required files are included.

## Release States

- `READY`: all mandatory rules are verified, content integrity passes, references and assets pass, and every rendered page was inspected.
- `READY_WITH_MANUAL_ACTIONS`: formatting is complete but named portal or human actions remain.
- `BLOCKED`: any mandatory rule is unverified, a content digest changes unexpectedly, dynamic fields would be flattened, rendering is unavailable, identity leakage remains, or reference/asset integrity is unresolved.

## Guardrails

- Preserve the untouched source and never silently edit scientific wording, numbers, units, tables, figures, claims, conclusions, author order, or declaration facts.
- Do not infer a mandatory journal rule from memory, a cached profile, or a third-party summary.
- Do not add optional graphical abstracts, highlights, separate figure sets, or supplementary files unless required or requested.
- Do not submit externally. Stop before `Submit`, `Approve submission`, `Run checks and submit`, or equivalent final action unless the user explicitly confirms that exact action.

## Execution

Install dependencies with `python -m pip install -r requirements.txt`. Run `python scripts/prepare_submission.py --help` for the full command. The total pipeline intentionally requires an official requirements YAML and a real rendering tool; missing evidence or tooling must remain visible as `BLOCKED`.

Read the relevant references only when needed: `references/requirements-workflow.md`, `references/docx-formatting.md`, `references/references-citations.md`, `references/anonymization.md`, `references/figures-supplements.md`, and `references/quality-gates.md`.
