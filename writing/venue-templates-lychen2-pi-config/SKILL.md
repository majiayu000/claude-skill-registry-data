---
compatibility: Requires Python 3.11+ for helper scripts; LaTeX and Poppler command-line tools are optional for compilation and PDF inspection.
description: Format manuscripts for a target venue. Use when applying a journal or conference template and its submission rules.
license: MIT license
metadata:
    github-path: skills/venue-templates
    github-pinned: v2.65.0
    github-ref: refs/tags/v2.65.0
    github-repo: https://github.com/K-Dense-AI/scientific-agent-skills
    github-tree-sha: 75dd5bc76e065cb8d68c8c7f863a149055c6bd96
    skill-author: K-Dense Inc.
    version: "1.2"
name: venue-templates
---
# Venue Templates

Prepare publication and funding documents without treating stale formatting details as authoritative. This skill combines:

- a verification-first workflow for current venue rules;
- bundled LaTeX scaffolds for a small, explicit set of document types;
- writing-style and reviewer-expectation guides; and
- local helpers for discovering, copying, and inspecting templates.

## Current venue requirements

Venue requirements are time-sensitive. Before giving exact page limits, deadlines, style-file names, anonymity rules, or required sections:

1. Identify the exact venue, year or funding cycle, track, and article or proposal type.
2. Open the official author instructions, call, solicitation, notice of funding opportunity (NOFO), or policy guide.
3. Record the source URL and the date checked.
4. Distinguish initial submission, revision/rebuttal, and camera-ready rules.
5. Treat bundled files as scaffolds unless this skill explicitly says they are a copy of an official template.

Never infer a current style-file name by changing the year in an old filename. Never present a generic scaffold as an official venue template.

## When to Use

Use this skill for:

- locating official journal or conference author instructions;
- checking page limits, required sections, anonymity, supplemental-material rules, or citation style;
- choosing and adapting a bundled LaTeX scaffold;
- preparing NSF, NIH, DOE, DARPA, or foundation proposal documents;
- designing a research poster after checking event-specific dimensions;
- adapting prose to a venue's audience and reviewer expectations; or
- inspecting a PDF's page count and embedded fonts.

## Workflow

For general drafting or layout changes, use the available template and reasonable formatting defaults. Resolve exact official rules when preparing a specific submission or answering a venue-rule question. Reuse rules already checked for the same target and stage unless they may have changed.

Deliver the requested manuscript, template, or formatting result. Necessary editorial and production notes belong in native document or LaTeX comments; if comments are unavailable, use the conversation outside the artifact. Do not insert an unrequested compliance report or pending-verification banner into the body. Required publication statements remain content.

**Reader-view check:** inspect the rendered document without the editing conversation. The content should discuss the work, evidence, or its interpretation; do not add a “not a reproduction” or source-relationship disclaimer panel. State a scientific limitation locally as a concrete condition and consequence, and retain a formal limitations section, requested comparison, or required venue disclosure when applicable. Editorial uncertainty belongs in native source comments, not in footnotes or captions; task logs and validation reports stay outside the manuscript.

### 1. Resolve the exact target

Ask for or derive:

- venue or funding agency;
- year/cycle and track;
- document type, such as research article, short paper, main track, R01, or R21;
- submission stage; and
- authoring format, such as LaTeX or Word.

Do not combine rules from similarly named venues or tracks.

### 2. Consult the right reference

| Need | Reference |
|---|---|
| Journal submission and official publisher resources | `references/journals_formatting.md` |
| Conference rules and 2026 verified snapshots | `references/conferences_formatting.md` |
| Poster sizes, layout, and accessibility | `references/posters_guidelines.md` |
| NSF, NIH, DOE, DARPA, and foundation proposals | `references/grants_requirements.md` |
| Cross-venue writing comparison | `references/venue_writing_styles.md` |
| Nature and Science writing | `references/nature_science_style.md` |
| Cell Press writing | `references/cell_press_style.md` |
| Medical journal writing | `references/medical_journal_styles.md` |
| ML and computer-vision conference writing | `references/ml_conference_style.md` |
| ACL, EMNLP, CHI, and other CS writing | `references/cs_conference_style.md` |
| Review criteria and rebuttals | `references/reviewer_expectations.md` |

Reference files summarize rules but do not override the current official source.

### 3. Record relevant submission rules

When submission checks are part of the task, keep the applicable rules in a task log or native comment. This record is not manuscript prose. For example:

```text
Target: ICML 2026 main track, initial submission
Official source: https://icml.cc/Conferences/2026/AuthorInstructions
Checked: 2026-07-20
Main-text limit: 8 pages
References/appendices: additional pages allowed in the same PDF
Anonymity: required
Official template: ICML 2026 style package linked by the author instructions
```

This makes later validation reproducible.

### 4. Start from the official template

For annual conferences and publisher-managed workflows:

1. Download the template from the official source.
2. Keep its class/style files unchanged.
3. Add content without overriding margins, font sizes, spacing, or headers.
4. Use a bundled scaffold only for drafting or when the official source explicitly permits it.

For grants, many components are entered or uploaded separately. Do not submit a combined bundled `.tex` file as if it were an agency-issued form.

### 5. Validate manually and mechanically

Verify at least:

- main-text and total-file page rules;
- font, margin, line-spacing, and paper-size rules;
- anonymity and metadata;
- required sections, statements, checklists, and disclosures;
- figure/table placement and accessibility;
- reference and supplemental-material treatment; and
- source-package and PDF requirements.

The helper can inspect page totals and embedded fonts, but it cannot prove that margins, font sizes, excluded sections, or hidden metadata comply.

## Bundled Assets

The repository intentionally bundles only the following templates. Other venues listed in references require an official external template.

### Journal and conference scaffolds

| File | Status |
|---|---|
| `assets/journals/nature_article.tex` | Generic Nature-oriented writing scaffold; not an official Nature template |
| `assets/journals/plos_one.tex` | PLOS ONE-oriented scaffold; compare with the current official PLOS LaTeX package |
| `assets/journals/neurips_article.tex` | NeurIPS 2026 wrapper; requires the official `neurips_2026.sty` |
| `assets/journals/elsarticle-template-num.tex` | Elsevier `elsarticle` numeric example |
| `assets/journals/elsarticle-template-num-names.tex` | Elsevier `elsarticle` numbered/name example |
| `assets/journals/elsarticle-template-harv.tex` | Elsevier `elsarticle` author-year example |

The matching Elsevier `.bst` files are in `assets/journals/`.

### Grant scaffolds

| File | Status |
|---|---|
| `assets/grants/nsf_proposal_template.tex` | Planning scaffold for common NSF narrative components; upload components separately |
| `assets/grants/nih_specific_aims.tex` | Writing scaffold for a one-page NIH Specific Aims attachment |

Use SciENcv and agency-provided common forms where required. Do not recreate biosketch or current-support forms in LaTeX.

### Poster scaffold

| File | Status |
|---|---|
| `assets/posters/beamerposter_academic.tex` | Venue-agnostic beamerposter scaffold; set dimensions from the event's current presenter instructions |

## Common Workflows

### Annual conference paper

1. Open `references/conferences_formatting.md`.
2. Follow the official link for the exact year and track.
3. Download the official author kit.
4. Draft in the official template.
5. Keep identifying information out of every submitted file when review is blind.
6. Check the paper checklist, supplement, rebuttal, and camera-ready rules separately.

For NeurIPS 2026, the bundled wrapper can be copied after downloading the official style file:

```bash
python scripts/customize_template.py \
  --template neurips_article.tex \
  --output my_neurips_2026_paper.tex
```

### Journal manuscript

1. Resolve the exact journal and article type.
2. Determine whether initial submission is format-flexible.
3. Use the journal's official template or submission format when required.
4. Apply the appropriate writing-style reference.
5. Recheck final-production instructions only after acceptance or revision.

Do not apply a publisher-wide template when the journal provides its own Guide for Authors.

### Grant proposal

1. Read the solicitation or NOFO before general agency guidance.
2. Confirm the effective policy guide and form set.
3. Map every required component to its page limit and upload field.
4. Use agency systems and common forms for biosketches and support disclosures.
5. Use bundled `.tex` files only as drafting aids.
6. Have the institution's sponsored-research office review the final package.

### Research poster

1. Read the event's presenter instructions.
2. Confirm physical dimensions, orientation, file format, and upload deadline.
3. Set the poster dimensions in the scaffold.
4. Use readable type, high contrast, color-independent encodings, and a logical reading order.
5. Export and inspect the PDF at final size.

## Helper Scripts

Run scripts from the skill directory.

### List bundled templates

```bash
python scripts/query_template.py --list-all
python scripts/query_template.py --venue NeurIPS --requirements
python scripts/query_template.py --type grants
```

The query helper reports only assets that exist in this skill and includes source/currency notes.

### Copy and customize a scaffold

```bash
python scripts/customize_template.py \
  --template nature_article.tex \
  --title "Your Paper Title" \
  --authors "First Author, Second Author" \
  --affiliations "Institution Name" \
  --output my_paper.tex
```

Review every replacement and compile before adding substantial content. User-provided text may need LaTeX escaping.

### Inspect a PDF

Use a verified preset:

```bash
python scripts/validate_format.py \
  --file paper.pdf \
  --venue icml-2026 \
  --content-pages 8 \
  --check page-count,fonts
```

Or provide an explicit limit and source:

```bash
python scripts/validate_format.py \
  --file proposal.pdf \
  --max-pages 15 \
  --content-pages 15 \
  --source-url "https://www.nsf.gov/policies/pappg" \
  --check page-count,fonts \
  --report validation.txt
```

`--content-pages` must be counted according to the official rule. The script does not infer where references or appendices begin.

## Internal submission checklist

- [ ] Exact venue, year/cycle, track, article type, and stage identified
- [ ] Official source URL recorded with date checked
- [ ] Official template or form used where required
- [ ] Page-limit scope understood, including excluded sections
- [ ] Required statements, checklists, and disclosures present
- [ ] Blind-review files and PDF metadata checked for identity leaks
- [ ] Figures and tables are legible and accessible
- [ ] References, appendices, and supplements follow current rules
- [ ] PDF and source package compile cleanly
- [ ] Submission portal preview reviewed before final submission

## Maintenance

This skill was reviewed on 2026-07-20. Annual conference snapshots are labeled with their year. When updating:

1. replace year-specific claims only after checking official sources;
2. avoid adding links to assets that are not bundled;
3. keep generic guidance separate from official requirements;
4. update helper presets and examples together; and
5. increment `metadata.version`.
