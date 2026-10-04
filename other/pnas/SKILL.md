---
name: pnas
description: "Author-guideline skill for PNAS (Proceedings of the National Academy of Sciences), a multidisciplinary journal food & nutrition researchers publish in. Use to format or check a manuscript for PNAS — structure, mandatory Significance Statement, abstract limit, PNAS numbered references, and figure specs. Triggers: submit to PNAS, Proceedings of the National Academy of Sciences guidelines, PNAS formatting. Also fires when the user wants to publish on/in this journal, format a manuscript for it, or match its reference/citation style."
metadata:
  publisher: "National Academy of Sciences (PNAS)"
  verified: "2026-07"
  source: "https://www.pnas.org/author-center/submitting-your-manuscript"
---

# PNAS — Author Guideline Skill

**Publisher:** National Academy of Sciences · **Verified:** 2026-07 · Confirm exact limits at the PNAS author center.

## Aims & scope
Multidisciplinary — biological, physical, and social sciences; food, nutrition,
agriculture, microbiology, and environmental work all in scope.

## Format (PNAS style)
- **References: numbered** in order of citation (PNAS style); numbered reference list with article titles and DOIs.
  > 1. A. B. Author, C. D. Author, Title of the article. *Proc. Natl. Acad. Sci. U.S.A.* **123**, e2412345 (2026).
- **Significance Statement (mandatory):** a plain-language paragraph for non-specialists, ~120 words (confirm limit).
- **Abstract:** ≤250 words, unstructured.
- **Structure:** Title → Author affiliations → Significance Statement → Abstract → Introduction → Results → Discussion → Materials and Methods → References. Research Reports/Articles have length guidance (confirm).
- **Mandatory:** data availability statement; author contributions; competing interest statement.
- **Figures:** ≥300 dpi; RGB/CMYK per policy; one/two-column widths; editable tables.

## Formatting constraints
```yaml
journal: PNAS
publisher: National Academy of Sciences
reference_style: pnas-numbered
significance_statement: {required: true, words: 120}
abstract_words: 250
data_availability: required
figure_dpi: 300
```
