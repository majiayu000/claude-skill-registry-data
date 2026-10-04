---
name: food-chemistry
description: "Author-guideline skill for Food Chemistry (Elsevier, ISSN 0308-8146). Use when preparing, formatting, or checking a manuscript for submission to Food Chemistry — structure, word/abstract limits, Highlights, graphical abstract, Elsevier numbered (Vancouver) references, and figure specs. Triggers: submit to Food Chemistry, Food Chem guidelines, format for Food Chemistry. Also fires when the user wants to publish on/in this journal, format a manuscript for it, or match its reference/citation style."
metadata:
  publisher: Elsevier
  issn: "0308-8146"
  verified: "2026-07"
  source: "https://www.sciencedirect.com/journal/food-chemistry/publish/guide-for-authors"
---

# Food Chemistry — Author Guideline Skill

**Publisher:** Elsevier · **ISSN:** 0308-8146 · **Source:** [Guide for Authors](https://www.sciencedirect.com/journal/food-chemistry/publish/guide-for-authors) · **Verified:** 2026-07 (confirm exact limits at source before submission).

## Aims & scope
Food Chemistry publishes original, rigorous **analytical/chemistry-driven** research on the chemistry of food: composition and structure, bioactive compounds, analysis and authentication, processing chemistry, food safety (chemical), and sensory-linked chemistry tied to identified compounds. The bar is **chemical insight from validated methods** — not descriptive screening. Studies must report validated methods, adequate controls, genuine replication, and defensible quantification. Scope-mismatched food-engineering or purely sensory work is desk-rejected.

## Article types
Original Research Articles; Review Articles (usually invited or pre-proposed); Short Communications; Analytical Methods papers. Rapid, well-validated method papers are welcome.

## Manuscript structure
Title page → Abstract → Keywords → 1. Introduction → 2. Materials and methods → 3. Results and discussion → 4. Conclusions → (Declarations) → References → Figure/table legends. Use **continuous line numbering** and page numbers.

- **Abstract:** unstructured, single paragraph, ~200 words (confirm; graphical abstract is separate).
- **Keywords:** up to 6.
- **Highlights (required):** a separate editable file, **3–5 bullets, each ≤85 characters** including spaces.
- **Graphical abstract (required):** one concise image submitted as a separate file, legible at Elsevier's display size.

## Reference style
**Elsevier numbered (Vancouver) style.** In-text citations are bracketed numbers `[1]`, `[2,3]`, numbered in order of appearance; the reference list is numbered in the same order.

Example (journal article):
> [1] A.B. Author, C.D. Author, Title of the article, Food Chemistry 400 (2023) 133912. https://doi.org/10.1016/j.foodchem.2023.133912

## Figures & tables
- Vector where possible (EPS/PDF); raster at **≥300 dpi** (line art ≥1000 dpi). TIFF/JPEG accepted.
- Fit one (~90 mm) or two (~190 mm) column widths; embed fonts; consistent, legible labels.
- Tables editable (not images); cite all figures/tables in order.

## Method-validation requirements (journal-specific)
Report linearity, LOD/LOQ, recovery, precision, and quantitative concentrations. Compound identification needs authentic standards or MS/MS confirmation (not library hits alone). Bioactivity claims must be backed by chemistry; chemometric models must be validated; avoid single-batch-only conclusions.

## Submission checklist
- [ ] Highlights file (3–5 × ≤85 chars) · [ ] Graphical abstract · [ ] Abstract ≤~200 words
- [ ] Numbered (Vancouver) references, DOIs included · [ ] Line + page numbering
- [ ] Declaration of interest · [ ] Data availability statement · [ ] CRediT author contributions
- [ ] Figures ≥300 dpi, correct column widths · [ ] Cover letter stating scope fit and novelty

## Formatting constraints
```yaml
journal: Food Chemistry
publisher: Elsevier
reference_style: numbered-vancouver
abstract_words: 200
keywords_max: 6
highlights: {count: "3-5", max_chars: 85, required: true}
graphical_abstract: required
line_numbering: required
figure_dpi: {halftone: 300, line_art: 1000}
column_widths_mm: [90, 190]
```
