---
name: british-food-journal
description: "Author-guideline skill for British Food Journal (Emerald, ISSN 0007-070X). Use to format or check a manuscript for BFJ — Emerald's required structured abstract, article classification, Harvard references, and figure specs. Triggers: submit to British Food Journal, Emerald food journal guidelines, structured abstract for BFJ. Also fires when the user wants to publish on/in this journal, format a manuscript for it, or match its reference/citation style."
metadata:
  publisher: "Emerald Publishing"
  issn: "0007-070X"
  verified: "2026-07"
  source: "https://www.emeraldgrouppublishing.com/journal/bfj#author-guidelines"
---

# British Food Journal (Emerald) — Author Guideline Skill

**Publisher:** Emerald · **ISSN:** 0007-070X · **Source:** [Author guidelines](https://www.emeraldgrouppublishing.com/journal/bfj#author-guidelines) · **Verified:** 2026-07 (confirm at source).

## Aims & scope
Multidisciplinary research on food across the supply chain: consumer behavior, marketing, policy, quality/safety, sustainability, and food management. Strong social-science and management orientation alongside food science.

## Article types
Research paper; Review; Conceptual paper; Case study; Viewpoint; General review. Select the correct **article classification** at submission (Emerald requirement).

## Manuscript structure (Emerald)
Title → **Structured abstract** → Keywords → Article classification → Introduction → Literature review → Methodology → Findings → Discussion → Conclusion → References. Word count typically 6,000–8,000 words including references (confirm).

- **Structured abstract (required):** headings — *Purpose*, *Design/methodology/approach*, *Findings*, *Research limitations/implications*, *Practical implications*, *Originality/value*; ≤250 words.
- **Keywords:** up to 6–8.
- **Article classification (required):** one of Emerald's categories (Research paper, Viewpoint, etc.).

## Reference style
**Harvard (author–date), Emerald style.** In-text `(Author, 2023)`; alphabetical list.

Example (Emerald Harvard):
> Author, A.B. and Author, C.D. (2023), "Title of the article", British Food Journal, Vol. 125 No. 4, pp. 1234-1250. https://doi.org/10.1108/BFJ-xx-2023-xxxx

## Figures & tables
Figures supplied as separate editable files ≥300 dpi; each figure/table cited in text and numbered; provide in the format Emerald requests (often EPS/PDF/TIFF, plus editable originals). Keep tables editable, not images.

## Submission checklist
- [ ] Structured abstract with all Emerald headings (≤250 words) · [ ] Article classification selected
- [ ] 6–8 keywords · [ ] Emerald Harvard references
- [ ] Figures as separate editable files ≥300 dpi · [ ] Declarations (funding, conflicts) · [ ] Cover letter

## Formatting constraints
```yaml
journal: British Food Journal
publisher: Emerald
reference_style: harvard-emerald
structured_abstract: {required: true, words: 250, headings: [purpose, design_methodology_approach, findings, research_limitations_implications, practical_implications, originality_value]}
article_classification: required
keywords_max: 8
word_count_range: [6000, 8000]
figure_dpi: {halftone: 300, line_art: 1000}
```
