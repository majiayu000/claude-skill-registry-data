---
name: crit-rev-food
description: "Shared author-guideline skill for Taylor & Francis food journals: Critical Reviews in Food Science and Nutrition, Food Reviews International, International Journal of Food Properties. Use to format or check a manuscript for a T&F food journal — structure, abstract/keyword limits, Taylor & Francis reference styles, and figure specs. Triggers: submit to Critical Reviews in Food Science and Nutrition, Food Reviews International, IJFP guidelines, Taylor & Francis food formatting. Also fires when the user wants to publish on/in this journal, format a manuscript for it, or match its reference/citation style."
metadata:
  publisher: "Taylor & Francis"
  verified: "2026-07"
  source: "https://www.tandfonline.com/action/authorSubmission?journalCode=bfsn20"
---

# Taylor & Francis Food Journals — Shared Author Guideline Skill

**Publisher:** Taylor & Francis · **Verified:** 2026-07 · Confirm each journal's "Instructions for authors" on tandfonline.com. Structure below reflects the common T&F template.

## Applies to
| Journal | Abbrev | Type focus | Ref style* |
|---|---|---|---|
| Critical Reviews in Food Science and Nutrition | CRIT REV FOOD SCI | Reviews only (comprehensive) | author–date (APA-style) |
| Food Reviews International | FOOD REV INT | Reviews | author–date |
| International Journal of Food Properties | INT J FOOD PROP | Research (open access) | author–date |

*T&F assigns a named reference style per journal; these food titles use an **author–date** style (APA-like). Confirm at the journal's "Instructions for authors".

## Common T&F structure
Title page (with author bios/ORCID) → Abstract → Keywords → Introduction → (Methods) → main body with headings → Conclusion → Disclosure statement → Funding → Data availability → References → Tables → Figure captions → Figures. Review journals: organize by thematic headings rather than IMRaD.

- **Abstract:** unstructured, typically ≤250 words.
- **Keywords:** 5–7.
- **Word length:** review articles are long-form; confirm any cap at the journal (CRFSN reviews are typically comprehensive, often 8,000–12,000 words).

## Reference style
**Author–date (APA-style, T&F variant).** In-text `(Author & Author, 2023)`; alphabetical reference list.

Example (APA-style):
> Author, A. B., & Author, C. D. (2023). Title of the article. *Critical Reviews in Food Science and Nutrition*, 63(10), 1234–1250. https://doi.org/10.1080/10408398.2023.xxxxxxx

## Figures & tables
Figures ≥300 dpi (line art ≥600 dpi); TIFF/EPS/PDF/PNG; color figures free online; editable tables; cite in order. T&F offers a LaTeX/Word template (Interact style).

## Submission checklist
- [ ] Author–date (APA-style) references · [ ] Abstract ≤~250 words · [ ] 5–7 keywords
- [ ] Disclosure (competing interests) + Funding + Data availability statements
- [ ] ORCID for authors · [ ] Figures ≥300 dpi · [ ] Cover letter (for reviews: scope + why comprehensive/timely)

## Also covers — Taylor & Francis / Routledge nutrition journals
Same T&F template (author–date/APA); clinical titles add trial registration and
reporting guidelines.

| Journal | Abbrev | Notes |
|---|---|---|
| Journal of the International Society of Sports Nutrition | J INT SOC SPORT NUTR | OA; sports nutrition |
| International Journal of Food Sciences and Nutrition | INT J FOOD SCI NUTR | Research |
| Journal of the American Nutrition Association | J AM NUTR ASSOC | Clinical/dietetics (Routledge) |
| Nutritional Neuroscience | NUTR NEUROSCI | Research |
| Journal of Dietary Supplements | J DIET SUPPL | Research |

## Formatting constraints
```yaml
publisher: Taylor & Francis
scope: food & nutrition
reference_style: author-date-apa
abstract_words: 250
keywords_max: 7
review_word_range: [8000, 12000]   # CRFSN reviews; confirm per journal
disclosure_statement: required
figure_dpi: {halftone: 300, line_art: 600}
```
