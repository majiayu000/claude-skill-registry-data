---
name: review-28-six-step-workbench
description: Run and initialize a six-step medical SCI review workbench distilled from Codex/Claude review-course videos and external academic/Nature skill patterns. Use when the user wants a simplified six-step workflow, course/video script, no-plugin setup, GitHub/Xiaohongshu-style skill integration, project folder templates, Zotero/reference/PDF workflow separation, or a complete review pipeline from skill setup to submission audit.
---

# Review 28 Six Step Workbench

## Purpose

Use this skill as the simplified public-facing controller for the review workbench. It compresses the longer `review-00` to `review-27` system into six teachable and executable steps.

The six-step workflow is for narrative or scoping medical SCI reviews by default. If the project is a systematic review or meta-analysis, route to PRISMA/systematic-review methods before writing.

## Key Principle

Skills are workflow instructions, not evidence. External GitHub, Xiaohongshu, Nature, or academic skills may inform process and style, but biomedical claims must still be verified through PubMed, Web of Science, Crossref, guidelines, full text, Zotero evidence, and final citation audit.

Plugins are optional. The no-plugin baseline is: local skills + browser/database export + Zotero import/export + Excel/CSV + Word/DOCX + manual BioRender/Figma if needed.

## 490 SCI Package Integration

If `00-SCI综述专家` to `20-审稿人意见回复器` are installed, use them as execution submodules when they are more detailed than the native six-step checklist. Do not replace this six-step controller.

Adopt:

- `02-SCI` and `03-SCI` for search-string calibration and complete export logs.
- `05-SCI` for benchmark-review library construction.
- `06-SCI`, `07-SCI`, and `08-SCI` for classification, Zotero import, PDF status, and reading-note workflow.
- `10-SCI` and `17-SCI` for figure/table source records and copyright/permission packages.
- `14-SCI` and `15-SCI` for target-journal matching plus five recent benchmark reviews.
- `18-SCI`, `19-SCI`, and `20-SCI` for cover letter, submission guide, and reviewer-response packages.

Do not adopt 490 rules that force every project to restart from Web of Science login, force a circular Fig. 1, force screenshot-based figure reuse, or bypass native DOI/PMID/full-text/citation gates.

## Project Folder Rule

Use six top-level folders for every review project. Keep root-level control files for dashboard, decisions, run log, and version log. Do not create many competing top-level folders.

Default top-level folders:

```text
01_topic_journal_outline/
02_literature_zotero/
03_manuscript_writing/
04_figures_tables/
05_submission_package/
06_revision_response/
```

Read `references/project-folder-structure.md` when designing or initializing a review project folder.

If the user asks to create the folder skeleton, run `scripts/init_review_project.py <project-root>` from this skill.

## Six Steps

### Step 1. Build The Workbench

Goal: create a local review workbench before writing.

Use:

- `review-00-controller`
- `review-22-skill-router`
- `review-27-github-archive`

Inputs:

- Topic area.
- Target article type.
- Target journal or journal tier.
- Local project folder.
- Any external skill sources to reference.

Outputs:

- project folder structure
- six-folder project skeleton
- skill routing map
- external skill source notes
- dashboard or run log

Gate:

- Do not start manuscript drafting until project scope, folder, review type, and target journal constraints are recorded.
- Do not scatter files outside the six-folder structure except root-level control logs.

### Step 2. Lock Topic, Journal, And Narrative Spine

Goal: decide what the review is about and why it is publishable.

Use:

- `review-01-project-init`
- `review-02-question-lock`
- `review-07-benchmark-library`
- `review-18-journal-match`

Outputs:

- topic options and scoring
- target journal match table
- benchmark review analysis
- narrative spine: background, gap, question, purpose, viewpoint
- files saved under `01_topic_journal_outline/`

Gate:

- Reject broad topics with no clear gap, no recent literature, or no target journal fit.

### Step 3. Search And Build The Literature Pool

Goal: create a traceable candidate literature set.

Use:

- `review-03-search-string`
- `review-04-search-execution`
- `review-23-reference-curator`

Inputs:

- PubMed/Web of Science/Crossref queries.
- Exported abstracts, RIS, NBIB, CSV, or Excel.
- Recent-year constraints.

Outputs:

- search strings
- raw search exports
- reference candidate table
- DOI/PMID metadata checks
- files saved under `02_literature_zotero/`

Gate:

- Search records are not usable evidence until screened and verified.

### Step 4. Screen, Download, Zotero, And Evidence Matrix

Goal: turn literature hits into usable evidence.

Use:

- `review-08-literature-classifier`
- `review-09-pdf-acquisition`
- `review-25-zotero-pdf-pipeline`
- `review-10-deep-reading`
- `review-11-evidence-matrix`

Outputs:

- screening log
- PDF status table
- Zotero import/export plan
- core reading queue
- evidence matrix
- claim-to-evidence map
- files saved under `02_literature_zotero/`

Gate:

- Missing full text cannot support numeric extraction, figure adaptation, detailed mechanism, or central claims.
- Copyrighted PDFs must remain local/private and should not be committed to public GitHub.

### Step 5. Write Sections And Produce Figures/Tables

Goal: draft the manuscript one section at a time and produce visual/table assets.

Use:

- `review-24-section-chain-writer`
- `review-12-outline-builder`
- `review-14-introduction-writer`
- `review-15-main-body-writer`
- `review-16-discussion-conclusion`
- `review-13-figure-table-planner`
- `review-26-figure-table-factory`
- `svg-tech-diagram`

Outputs:

- abstract
- introduction
- body sections
- discussion and conclusion
- figure/table plan
- SVG/BioRender/Figma prompts or exports
- Excel evidence tables
- figure legends
- manuscript files saved under `03_manuscript_writing/`
- figure and table assets saved under `04_figures_tables/`

Gate:

- Each section must have claim-citation mapping. Each figure panel/table row must have source tracing.

### Step 6. Audit, Package, And Archive

Goal: make the review submission-ready and reusable.

Use:

- `review-17-citation-audit`
- `review-18-journal-match`
- `review-19-submission-package`
- `review-21-personal-qc`
- `review-27-github-archive`

Outputs:

- citation audit report
- claim-citation table
- DOI/PMID verification table
- submission checklist
- final manuscript package
- private GitHub/local archive
- submission files saved under `05_submission_package/`
- reviewer-response files saved under `06_revision_response/` when revision begins

Gate:

- Do not submit if DOI/PMID, citation order, figure permissions, journal format, or overclaim checks fail.

## Output Format

When used, return:

1. Current step.
2. Required inputs.
3. Files to inspect or create.
4. Native skills to invoke.
5. Pass/fail gate.
6. Next action.

## Video And External Skill Notes

Read `references/video-course-notes.md` when adapting video/course logic.

Read `references/external-skill-index.md` when incorporating GitHub, Nature, academic, or public skill references.

Read `references/project-folder-structure.md` when the user asks how to organize project folders or initialize a review workbench.
