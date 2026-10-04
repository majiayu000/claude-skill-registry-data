---
name: nature-food
description: "Author-guideline skill for Nature Portfolio food journals: Nature Food and npj Science of Food. Use to format or check a manuscript for these journals — strict article-type word limits, unreferenced short abstracts, Nature superscript-numbered references, display-item limits, and Methods placement. Triggers: submit to Nature Food, npj Science of Food guidelines, Nature Portfolio food formatting. Also fires when the user wants to publish on/in this journal, format a manuscript for it, or match its reference/citation style."
metadata:
  publisher: Nature Portfolio
  verified: "2026-07"
  source: "https://www.nature.com/natfood/submission-guidelines/aip-and-formatting"
---

# Nature Portfolio Food Journals — Author Guideline Skill

**Publisher:** Nature Portfolio · **Verified:** 2026-07 · Sources: [Nature Food content types](https://www.nature.com/natfood/content) · [Nature Food formatting](https://www.nature.com/natfood/submission-guidelines/aip-and-formatting) · [npj Science of Food content types](https://www.nature.com/npjscifood/content-types). Confirm at source.

## Applies to
- **Nature Food** — selective; strict word/display limits (below).
- **npj Science of Food** — open access; more flexible length but same Nature referencing and rigor.

## Nature Food article types (word/display limits)
| Type | Main text | Abstract | Display items | References |
|---|---|---|---|---|
| Article | ≤3,000 words (excl. abstract, Methods, refs, legends) | ≤150 words, unreferenced | ≤6 (figs/tables) | ~50 (guide) |
| Perspective | ≤1,500 words (incl. abstract, refs, legends), no headings | ≤70 words | ≤2 | — |
| Brief Communication | ≤1,500 words (incl. everything) | ≤70 words | small | ~20 |
| Review / Analysis | commissioned; confirm limits | — | — | — |

Title ≤10 words / ~90 characters. Methods placed after main text (Articles), not counted in the word limit.

## npj Science of Food
Standard Article structure (Introduction, Results, Discussion, Methods); no rigid word cap but concise; abstract ~150–200 words; open-access APC applies.

## Reference style
**Nature style: superscript numbers** in order of citation (`...as shown previously^12`). Reference list numbered. **Article titles are required** for Nature Food long-form manuscripts. Include DOIs.

Example:
> 12. Author, A. B. & Author, C. D. Title of the article. *Nat. Food* **4**, 123–130 (2023).

## Structure & sections
Articles: Title → Abstract (unreferenced) → main text with headings (Introduction implicit) → Results → Discussion → Methods → References → Figure legends → Tables. Figures cited as `Fig. 1`, `Fig. 2` in sequence. A data availability and code availability statement is mandatory; reporting summary required.

## Figures & tables
High-resolution (≥300 dpi at final size); RGB for online; fit ~180 mm double-column; sans-serif labels (Helvetica/Arial); avoid red/green combinations for accessibility. Editable tables.

## Submission checklist
- [ ] Correct article type + within word/display limits · [ ] Abstract unreferenced within limit
- [ ] Nature superscript-numbered refs with article titles + DOIs · [ ] Methods after main text
- [ ] Data & code availability statements · [ ] Reporting summary (Nature Food)
- [ ] Cover letter (significance, fit) · [ ] Figures ≥300 dpi, accessible palette

## Formatting constraints
```yaml
journal_group: Nature Portfolio (Nature Food, npj Science of Food)
reference_style: nature-superscript-numbered
require_article_titles: true
article_word_limit: 3000
abstract_words: {article: 150, short: 70}
display_items_max: 6
methods: after-main-text
data_availability: required
figure_dpi: 300
```
