---
name: nature-portfolio
description: "Shared author-guideline skill for Nature Portfolio research journals that food & nutrition researchers publish in: Nature, Nature Communications, Nature Microbiology, Nature Metabolism, Nature Sustainability, Nature Biotechnology, Nature Medicine, and Nature Reviews titles. Use to format or check a manuscript for a Nature-family journal — strict article-type word limits, unreferenced short abstracts, Nature superscript-numbered references (article titles required), display-item limits, Methods placement, reporting summary. (Nature Food and npj Science of Food are in the nature-food skill.) Triggers: submit to Nature, Nature Communications, Nature Microbiology, Nature Metabolism guidelines, Nature Portfolio formatting. Also fires when the user wants to publish on/in this journal, format a manuscript for it, or match its reference/citation style."
metadata:
  publisher: "Nature Portfolio (Springer Nature)"
  verified: "2026-07"
  source: "https://www.nature.com/nature/for-authors/formatting-guide"
---

# Nature Portfolio Research Journals — Author Guideline Skill

**Publisher:** Nature Portfolio · **Verified:** 2026-07 · Confirm each journal's own submission guidelines (limits differ by title/article type). Nature Food and npj Science of Food have their own skill (`nature-food`).

## Applies to (food/nutrition-relevant Nature journals)
| Journal | Abbrev | Relevance |
|---|---|---|
| Nature | NATURE | Multidisciplinary flagship |
| Nature Communications | NAT COMMUN | Multidisciplinary, open access |
| Nature Microbiology | NAT MICROBIOL | Food/gut microbiology |
| Nature Metabolism | NAT METAB | Nutrition & metabolism |
| Nature Sustainability | NAT SUSTAIN | Food systems, sustainability |
| Nature Biotechnology | NAT BIOTECHNOL | Food/agri biotech |
| Nature Medicine | NAT MED | Clinical nutrition |
| Nature Reviews (various) | NAT REV * | Reviews (commissioned) |

## Format (Nature style)
- **References: superscript numbers** in order of citation; numbered list; **article titles required**. Include DOIs.
  > 12. Author, A. B. & Author, C. D. Title of the article. *Nat. Commun.* **15**, 1234 (2026).
- **Abstract:** unreferenced; length by article type (e.g. Nature Article ≤150–200 words). Confirm per journal.
- **Structure:** Title → Abstract → main text → **Methods after the main text** (not counted in the word limit) → References → Figure legends → Tables.
- **Display items:** capped by article type (often ≤6–8); cite as `Fig. 1` in sequence.
- **Mandatory:** data availability + code availability statements; **Reporting Summary**; competing interests; author contributions.
- **Figures:** ≥300 dpi at final size; RGB; ~180 mm double column; accessible palette (avoid red/green as sole encoding).

## Formatting constraints
```yaml
publisher: Nature Portfolio
reference_style: nature-superscript-numbered
require_article_titles: true
abstract: unreferenced (length per article type)
methods: after-main-text
data_and_code_availability: required
reporting_summary: required
figure_dpi: 300
notes: "Nature Food + npj Science of Food -> nature-food skill"
```
