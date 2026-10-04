---
name: cambridge-nutrition
description: "Shared author-guideline skill for Cambridge University Press nutrition journals: British Journal of Nutrition, Nutrition Research Reviews, Proceedings of the Nutrition Society, Public Health Nutrition, Journal of Nutritional Science. Use to format or check a manuscript for a Cambridge nutrition journal — structure, structured abstracts, Harvard references, and figure specs. Triggers: submit to British Journal of Nutrition, Nutrition Research Reviews, Proceedings of the Nutrition Society guidelines, Cambridge nutrition formatting. Also fires when the user wants to publish on/in this journal, format a manuscript for it, or match its reference/citation style."
metadata:
  publisher: "Cambridge University Press"
  verified: "2026-07"
  source: "https://www.cambridge.org/core/journals/british-journal-of-nutrition/information/instructions-contributors"
---

# Cambridge Nutrition Journals — Shared Author Guideline Skill

**Publisher:** Cambridge University Press · **Verified:** 2026-07 · Confirm each journal's "Instructions for Contributors" on Cambridge Core.

## Applies to
| Journal | Abbrev | Type focus |
|---|---|---|
| British Journal of Nutrition | BRIT J NUTR | Human & animal nutrition research |
| Nutrition Research Reviews | NUTR RES REV | Reviews |
| Proceedings of the Nutrition Society | P NUTR SOC | Symposium/review papers |
| Public Health Nutrition | PUBLIC HEALTH NUTR | Population nutrition |
| Journal of Nutritional Science | J NUTR SCI | Open-access research |

## Manuscript structure
Title page → Abstract → Keywords → Introduction → (Experimental/Methods) → Results → Discussion → Acknowledgements → Financial support → Conflicts of interest → Authorship → References → Tables → Figure legends.

- **Abstract:** British Journal of Nutrition uses a concise unstructured abstract (~250 words); confirm per journal.
- **Keywords:** 4–6.
- **Human/clinical studies:** ethics approval + trial registration (where applicable), following ICMJE and the relevant reporting guideline (CONSORT/STROBE/PRISMA).

## Reference style
**Harvard (author–date), Cambridge/journal style.** In-text `(Author & Author, 2023)`; alphabetical list.

Example:
> Author AB & Author CD (2023) Title of the article. *British Journal of Nutrition* 130, 1234–1245. https://doi.org/10.1017/Sxxxxxxxx

## Figures & tables
Figures ≥300 dpi (line art higher); TIFF/EPS/PDF; editable tables; SI units; cite in order.

## Submission checklist
- [ ] Abstract ≤~250 words · [ ] 4–6 keywords · [ ] Harvard references
- [ ] Financial support + Conflicts of interest + Authorship statements
- [ ] Ethics/trial registration + reporting guideline for human/clinical studies
- [ ] Figures ≥300 dpi · [ ] Cover letter

## Formatting constraints
```yaml
publisher: Cambridge University Press
reference_style: harvard-author-date
abstract_words: 250
keywords_max: 6
declarations: [financial_support, conflicts_of_interest, authorship]
clinical: [ethics, trial_registration, reporting_guideline]
figure_dpi: {halftone: 300, line_art: 1000}
```
