---
name: paper-pdf-to-structured-html
description: Convert academic research PDFs into self-contained, highly readable standalone HTML digests that can be read instead of the original paper for normal comprehension, with important figures, captions, paper-type detection, and type-specific treatment for survey/review papers, algorithm/method papers, empirical benchmark papers, and system papers. Use when Codex is asked to read, summarize, transform, or build HTML from PDF papers, arXiv PDFs, conference papers, surveys, literature reviews, or research reports, especially when the output should preserve and explain taxonomy diagrams, comparison tables, datasets, metrics, seminal papers, algorithms, experiments, challenges, future directions, or selected branches for deeper second-pass explanation.
---

# Paper PDF To Structured HTML

## Overview

Use this skill to turn a research paper PDF into a navigable HTML reading artifact that is useful on its own, not a flat summary and not merely a guide to the original PDF. The target reader should be able to read the HTML and understand the paper's main content, structure, evidence, methods, limitations, and research directions without routinely opening the PDF. Preserve the paper's structure, extract or render important figures, classify the paper type, and choose a reading template that matches the paper's role.

## Standalone Reading Contract

The generated HTML must be a paper-replacement digest for normal study:

- Explain every major section or taxonomy branch in the HTML itself. Page references are provenance, not substitutes for content.
- For survey/review papers, a taxonomy or overview figure is not enough by itself. The `Taxonomy GPS` section must explain the logic behind the figure: organizing principle, argument flow, parallel groups, upstream/downstream dependencies, cross-cutting axes, and how the branches support the paper's thesis.
- Include enough branch/method detail that a reader can answer: what problem is addressed, how it works, what examples or representative works are used, what datasets/metrics/results support it, what limitations remain, and how it connects to the paper's thesis.
- Avoid "read Section X", "see page Y", or "the paper discusses..." as the main content. If a section is named, summarize its actual substance immediately.
- Prefer concise paraphrase and structured synthesis over long quotation. Do not paste full paper sections.
- Keep the HTML readable, but bias toward completeness over brevity when the user asks for an HTML they can read instead of the original paper.

## Workflow

1. Create a work directory for the paper:
   - `output/paper-html/<paper-slug>/`
   - `assets/` for extracted figures and page renders;
   - `manifest.json` for extraction metadata;
   - `<paper-slug>.html` for the final artifact.
2. Inspect the PDF with `scripts/inspect_paper_pdf.py` when possible:
   - if the active Python cannot import the needed PDF libraries, first try to find or create a usable environment; do not silently downgrade to page-only rendering because the default interpreter is missing packages;
   - extract title-like metadata, outline, per-page text, candidate captions, references, embedded images, and the lightweight `figure_coverage` audit;
   - use the default audit to compare captions with embedded images and drawing objects before deciding that a paper has no figures;
   - when important captions are marked `vector_crop_needed` or `page_crop_needed`, render the relevant page and crop the figure/table before finalizing visual assets.
3. Classify the paper type:
   - survey/review;
   - algorithm/method;
   - empirical/benchmark;
   - system/tool/dataset;
   - mixed or unclear.
4. Read the matching reference before writing:
   - survey/review: `references/survey-reading-workflow.md`;
   - algorithm/method or empirical papers: `references/algorithm-method-workflow.md`;
   - output rules for all types: `references/html-output-rules.md`.
5. Build a coverage ledger before writing:
   - list all major paper sections, subsections, taxonomy branches, experiments, datasets, tables, and challenge/future-direction sections;
   - mark each as `full`, `condensed`, `figure/table only`, or `omitted`;
   - only omit low-value details such as boilerplate references, author biographies, or repetitive examples, and record why in `manifest.json`.
6. Build a taxonomy/structure logic map for survey, review, tutorial, and system papers:
   - extract the paper's stated article organization from the introduction and section openings;
   - identify which nodes in the overview figure are parallel alternatives, which are prerequisites/foundations, which are downstream tasks, and which are cross-cutting evaluation or transfer layers;
   - distinguish author-stated relationships from inferred relationships, and mark uncertain links as inferred or manual-check;
   - use this logic map as prose in the `Taxonomy GPS`, not only as a hidden planning note.
7. Select important visual assets:
   - include taxonomy diagrams, architecture/method overview figures, algorithm flow diagrams, comparison tables, main result plots, dataset/metric tables, and challenge/future-direction diagrams;
   - prefer extracted embedded images when sharp;
   - treat `figure_coverage` as the required figure/table ledger: every important caption should map to `embedded_image_or_mixed`, `vector_crop_needed`, `page_crop_needed`, `manual_check`, or an explicit omission reason;
   - for pages with captions but zero extracted images and nonzero drawing objects, assume vector/PDF graphics until disproven and use page render + crop rather than declaring no image;
   - prefer precise figure/table crops when bounding boxes or visually checked coordinates are available;
   - fall back to full-page renders only after dependency recovery and crop attempts are unsafe, incomplete, or likely to lose caption/table context;
   - always include the source page and caption/provenance near the image.
8. Generate standalone HTML from `assets/paper-digest-template.html` or the repo's existing HTML note style.
9. Validate the HTML visually with Playwright or browser screenshots when layout quality matters. Check broken images, clipped tables, figure readability, mobile width, print behavior, and whether the page contains actual explanatory content for every navigation target.

## Environment And Asset Extraction Recovery

Treat missing Python PDF dependencies as a recoverable setup problem, not as permission to skip precise extraction.

1. Check the active interpreter and imports:
   - `python --version`
   - `python -c "import fitz, pdfplumber, pypdf; print('pdf deps ok')"`
2. If imports fail, look for a newer installed Python or launcher entry (`py -0p` on Windows). Prefer Python 3.10+ when available.
3. If no suitable ready environment exists, create a local virtual environment with the selected interpreter inside the work directory, for example `.venv`, then install the needed packages there:
   - `<selected-python> -m venv output/paper-html/<paper-slug>/.venv`
   - `output/paper-html/<paper-slug>/.venv/Scripts/python -m pip install --upgrade pip`
   - `output/paper-html/<paper-slug>/.venv/Scripts/python -m pip install pymupdf pdfplumber pypdf`
4. Run extraction scripts with the verified interpreter. Record the interpreter path, dependency status, extraction method, and any failures in `manifest.json`.
5. Use Poppler `pdftotext` and full-page renders as a reliable baseline, but not as the first and only asset strategy when figure/table crops are important.

Precise crops are preferred for single-page figures, overview diagrams, architecture diagrams, plots, and compact tables. Full-page renders are acceptable when:

- a table spans pages and exact cropping would risk losing repeated headers, continuation labels, or final rows;
- caption, labels, or surrounding explanatory text are too close to isolate safely;
- the figure/table coordinates remain uncertain after dependency recovery and visual inspection;
- the user explicitly prioritizes provenance over visual polish.

When using full-page renders, explain in the manifest why crops were not used and identify which pages contain the relevant figure or table.


## Figure Coverage Audit

Use an `always audit, selectively analyze` policy so figure coverage does not multiply token cost:

- Always run the lightweight audit that records per-page caption labels, embedded image counts, image block counts, and drawing counts.
- Treat `caption_count > extracted_image_count` as a coverage gap until `figure_coverage` explains it.
- Interpret pages with captions, `embedded_image_count == 0`, and `drawing_count > 0` as likely vector/PDF graphics requiring page render and crop.
- Do not ask the model to analyze every crop. Analyze only method overview figures, architecture diagrams, algorithm flow diagrams, main result tables/plots, ablations, comparison tables, or user-specified figures.
- Record unselected figures as omitted or low-priority in `manifest.json`; do not silently ignore them.

## Type-Specific Output

For survey/review papers, build the HTML around:

- boundary from title and abstract;
- contributions and article structure from the introduction;
- taxonomy tree as the central navigation object, with an explicit interpretation of the tree's logic: section order, hierarchy depth, parallel branches, upstream/downstream relations, cross-cutting axes, and why the survey uses this organization;
- branch-by-branch explanation, not just branch cards: include the branch's motivation, core techniques, representative works, datasets/metrics, strengths, weaknesses, and open problems;
- comparison tables, datasets, and evaluation metrics with explanatory text that interprets what the table means;
- frequently cited foundational papers with why each matters;
- challenges and future directions with concrete research entry points and required resources;
- optional second-pass branch deep dives requested by the user.

For algorithm/method papers, build the HTML around:

- problem setting and assumptions;
- method overview and architecture;
- core algorithm, objective, or pipeline with enough detail to understand the method without returning to the PDF;
- novelty versus prior work;
- experimental setup, datasets, metrics, baselines, and ablations with actual result trends or values when reliably extracted;
- main results, failure cases, and limitations interpreted in context;
- reusable implementation notes.

For empirical benchmark, system, or dataset papers, adapt the same structure around tasks, evaluation protocol, system components, dataset construction, limitations, and reproducibility.

## Second-Pass Branch Deepening

When the user has already read the initial HTML and asks about specific branches such as `[branch A, branch B]`, generate a focused follow-up HTML section or companion page:

- restate where each branch sits in the taxonomy;
- explain its core idea, representative methods, strengths, weaknesses, datasets, metrics, and open problems;
- include the relevant figures/tables again if they are needed for understanding;
- link back to the original taxonomy and source pages.

The initial HTML should already include a useful first-pass explanation of every major branch. Second-pass deepening is for extra detail, not for content that was missing from the first artifact.

## Guardrails

- Do not invent citations, benchmark numbers, datasets, or figure meanings. Mark uncertain extraction results as `needs manual check`.
- Do not treat OCR/extracted text as layout truth. Render the relevant PDF pages when figures, tables, formulas, or multi-column structure matter.
- Do not include every extracted image. Curate images for reading value and record why each one was included.
- Do not flatten a survey into a generic summary. Preserve the taxonomy and comparison structure.
- Do not paste a taxonomy or overview figure as the entire `Taxonomy GPS`. The GPS must teach the reader how to read the structure and what logical relationships the figure encodes.
- Do not flatten an algorithm paper into background prose. Preserve the method pipeline, assumptions, experiments, and ablations.
- Do not deliver a navigation shell whose main value is telling the reader where to look in the PDF. Every link and section in the HTML must contain substantive explanation.
- Do not use "guide", "reading route", or "what to read next" sections to replace the content itself.
- Keep the final HTML readable from disk without a build step.

## Resources

- `scripts/inspect_paper_pdf.py`: extract text, candidate captions, references, outlines, embedded images, page drawing counts, and figure coverage status into a manifest.
- `assets/paper-digest-template.html`: standalone HTML skeleton for the final digest.
- `references/survey-reading-workflow.md`: four-stage survey reading workflow and branch deepening pattern.
- `references/algorithm-method-workflow.md`: method/algorithm/benchmark paper structure.
- `references/html-output-rules.md`: required sections, figure handling, and validation checks.

## Common Commands

```bash
python skills/paper-pdf-to-structured-html/scripts/inspect_paper_pdf.py paper.pdf --out output/paper-html/paper-slug
python skills/paper-pdf-to-structured-html/scripts/inspect_paper_pdf.py paper.pdf --out output/paper-html/paper-slug --render-figure-pages
```

Install missing PDF dependencies before falling back to coarse extraction: `pymupdf`, `pdfplumber`, `pypdf`, and Poppler utilities for page rendering.


