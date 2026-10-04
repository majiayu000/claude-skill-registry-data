---
name: springer-food
description: "Shared author-guideline skill for Springer / Springer Nature food journals: Food Engineering Reviews, Food and Bioprocess Technology, Food Security, and the SpringerOpen journal Food Production Processing and Nutrition. Use to format or check a manuscript for a Springer food journal — structure, abstract/keyword limits, Springer reference styles, and figure specs. Triggers: submit to Food and Bioprocess Technology, Food Security, Food Engineering Reviews guidelines, Springer food formatting. Also fires when the user wants to publish on/in this journal, format a manuscript for it, or match its reference/citation style."
metadata:
  publisher: "Springer / Springer Nature"
  verified: "2026-07"
  source: "https://www.springer.com/gp/authors-editors/journal-author"
---

# Springer Food Journals — Shared Author Guideline Skill

**Publisher:** Springer / Springer Nature · **Verified:** 2026-07 · Confirm each journal's "Submission guidelines" on SpringerLink. Structure below reflects the common Springer template.

## Applies to
| Journal | Abbrev | Type focus | Access | Ref style* |
|---|---|---|---|---|
| Food Engineering Reviews | FOOD ENG REV | Reviews | Subscription | author–date |
| Food and Bioprocess Technology | FOOD BIOPROCESS TECH | Research | Subscription | author–date |
| Food Security | FOOD SECUR | Research + reviews (policy/agri) | Subscription | author–date |
| Food Production Processing and Nutrition | FOOD PROD PROCESS NU | Research (SpringerOpen) | Gold OA | numbered (Vancouver) |

*Confirm at the journal; Springer permits **Springer Basic (name–year / author–date)** or **numbered (Vancouver)**. SpringerOpen/BMC-style titles typically use numbered.

## Common Springer structure
Title page → Abstract → Keywords → Introduction → Materials and Methods → Results → Discussion → Conclusion → Statements & Declarations (funding, competing interests, ethics, author contributions, data availability) → References → Tables → Figure legends → Figures.

- **Abstract:** unstructured, typically ≤250 words.
- **Keywords:** 4–6.
- **Declarations section:** required by Springer (funding, conflicts, ethics approval, consent, data availability, author contributions).

## Reference style
Default **author–date (Springer Basic, name–year)**: in-text `(Author and Author 2023)` (note: no comma before year in Springer Basic); alphabetical list.

Example (Springer Basic):
> Author AB, Author CD (2023) Title of the article. Food Bioprocess Technol 16:1234–1245. https://doi.org/10.1007/s11947-023-xxxxx

`Food Production Processing and Nutrition` (SpringerOpen) uses **numbered** references `[1]`.

## Figures & tables
Figures ≥300 dpi (line art ≥600–1000 dpi); TIFF/EPS/PDF/PNG; RGB online; Springer figure width guidelines (~84 mm single, ~174 mm double); editable tables; cite in order.

## Submission checklist
- [ ] Correct reference style (author–date for most; numbered for Food Prod Process Nutr)
- [ ] Abstract ≤~250 words · [ ] 4–6 keywords
- [ ] Statements & Declarations block (funding, competing interests, ethics, contributions, data availability)
- [ ] Figures ≥300 dpi · [ ] Cover letter

## Also covers — Springer / Springer Nature nutrition journals
Same Springer template (author–date Springer Basic default; some numbered);
clinical titles add structured abstracts, trial registration, reporting guidelines.

| Journal | Abbrev | Notes |
|---|---|---|
| Current Obesity Reports | CURR OBES REP | Reviews |
| Current Nutrition Reports | CURR NUTR REP | Reviews |
| European Journal of Nutrition | EUR J NUTR | Research |
| International Journal of Obesity | INT J OBESITY | Clinical/obesity |
| Nutrition & Diabetes | NUTR DIABETES | OA clinical |
| European Journal of Clinical Nutrition | EUR J CLIN NUTR | Clinical |
| Plant Foods for Human Nutrition | PLANT FOOD HUM NUTR | Research |

## Formatting constraints
```yaml
publisher: Springer
scope: food & nutrition
reference_style: per-journal   # author-date (Springer Basic) default; numbered for SpringerOpen title
abstract_words: 250
keywords_max: 6
declarations_block: required
figure_dpi: {halftone: 300, line_art: 1000}
column_widths_mm: [84, 174]
```
