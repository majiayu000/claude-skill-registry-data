---
name: elsevier-food
description: "Shared author-guideline skill for Elsevier food-science journals (Trends in Food Science & Technology, Food Hydrocolloids, LWT, Food Research International, Food Control, Meat Science, Food Policy, Postharvest Biology & Technology, and ~20 more). Use to format or check a manuscript for any Elsevier food journal not covered by its own skill. Covers the common Elsevier Guide-for-Authors structure, Highlights, graphical abstract, reference styles, and figure specs. Triggers: submit to an Elsevier food journal, LWT/Food Hydrocolloids/Trends guidelines, Elsevier food formatting. Also fires when the user wants to publish on/in this journal, format a manuscript for it, or match its reference/citation style."
metadata:
  publisher: Elsevier
  verified: "2026-07"
  source: "https://www.elsevier.com/researcher/author/policies-and-guidelines"
---

# Elsevier Food Journals — Shared Author Guideline Skill

**Publisher:** Elsevier · **Verified:** 2026-07 · Confirm each journal's exact limits at its own *Guide for Authors* on ScienceDirect (pages block automated fetch; structure below reflects the common Elsevier template).

Flagship journals with their own skill: **Food Chemistry** (`food-chemistry`), **Journal of Dairy Science** (`j-dairy-science`). Everything else Elsevier/food is covered here.

## Applies to

| Journal | Abbrev | Ref style* | Notes |
|---|---|---|---|
| Trends in Food Science & Technology | TRENDS FOOD SCI TECH | numbered | Reviews only; no original data |
| Food Hydrocolloids | FOOD HYDROCOLLOID | numbered | Colloid/structure focus |
| Food Hydrocolloids for Health | FOOD HYDROCOLL HLTH | numbered | Open access |
| Food Packaging and Shelf Life | FOOD PACKAGING SHELF | numbered | |
| Global Food Security | GLOB FOOD SECUR-AGR | author–date | Policy/economics; review-leaning |
| Current Opinion in Food Science | CURR OPIN FOOD SCI | author–date | Invited short reviews |
| Future Foods | FUTURE FOODS | numbered | Open access |
| Food Research International | FOOD RES INT | numbered | Broad food science |
| Current Research in Food Science | CURR RES FOOD SCI | numbered | Open access |
| Postharvest Biology and Technology | POSTHARVEST BIOL TEC | author–date | |
| Innovative Food Science & Emerging Technologies | INNOV FOOD SCI EMERG | numbered | Processing/novel tech |
| LWT – Food Science and Technology | LWT-FOOD SCI TECHNOL | numbered | Open access; broad |
| Food Control | FOOD CONTROL | numbered | Safety/quality management |
| Journal of Agriculture and Food Research | J AGR FOOD RES | numbered | Open access |
| Applied Food Research | APPL FOOD RES | numbered | Open access |
| Meat Science | MEAT SCI | author–date | Muscle foods |
| Food Policy | FOOD POLICY | author–date | Social science; longer articles |
| Food Bioscience | FOOD BIOSCI | numbered | |
| Food Structure | FOOD STRUCT-NETH | numbered | |
| Journal of Food Engineering | J FOOD ENG | numbered | Engineering/modelling |
| International Journal of Food Microbiology | INT J FOOD MICROBIOL | author–date | |
| Food Quality and Preference | FOOD QUAL PREFER | author–date | Sensory/consumer science |
| Food Chemistry: Molecular Sciences | FOOD CHEM-MOL SCI | numbered | Open access |
| Food Microbiology | FOOD MICROBIOL | author–date | |
| Journal of Food Composition and Analysis | J FOOD COMPOS ANAL | numbered | Requires analytical rigor + data |
| Microbial Risk Analysis | MICROB RISK ANAL | author–date | QMRA modelling |
| Journal of Functional Foods | J FUNCT FOODS | numbered | Bioactives/health |
| Journal of Cereal Science | J CEREAL SCI | author–date | |

*Ref style is the common default; **always confirm at the journal's Guide for Authors** — Elsevier lets journals choose numbered (Vancouver) or author–date (Harvard).

## Common Elsevier structure
Title page (title, authors, affiliations, corresponding author) → Abstract → Keywords → Introduction → Materials and methods → Results (and) Discussion → Conclusions → declarations → References → figure/table legends → figures/tables. Use **continuous line numbers** and page numbers.

- **Abstract:** unstructured, typically ≤200–250 words (journal-specific).
- **Keywords:** usually up to 6.
- **Highlights:** separate file, **3–5 bullets ≤85 characters** each (most Elsevier journals).
- **Graphical abstract:** required or encouraged on most food journals.
- **Declarations:** Declaration of competing interest, CRediT roles, Data availability, funding, ethics where relevant.

## Reference styles (examples)
- **Numbered (Vancouver):** in-text `[1]`; list numbered by order of appearance.
  > [1] A. Author, B. Author, Title, LWT 180 (2023) 114682. https://doi.org/10.xxxx
- **Author–date (Harvard):** in-text `(Author & Author, 2023)`; list alphabetical.
  > Author, A., & Author, B. (2023). Title. *Meat Science*, 200, 109xxx. https://doi.org/10.xxxx

Use the reference manager style pack named for the specific journal.

## Figures & tables
Vector (EPS/PDF) preferred; raster ≥300 dpi (line art ≥1000 dpi); column widths ~90 mm / ~190 mm; editable tables; cite all in order.

## Submission checklist
- [ ] Correct reference style for the target journal · [ ] Highlights (if required)
- [ ] Graphical abstract (if required) · [ ] Line + page numbering
- [ ] Declaration of competing interest · [ ] CRediT · [ ] Data availability
- [ ] Figures ≥300 dpi, correct widths · [ ] Cover letter (scope fit, novelty, suggested reviewers)

## Also covers — Elsevier nutrition journals
Same Elsevier template; **clinical/nutrition** titles add structured abstracts,
trial registration, and a reporting guideline (CONSORT/STROBE/PRISMA) per ICMJE.
Reference style is per-journal (author–date or numbered — confirm at the GfA).

| Journal | Abbrev | Notes |
|---|---|---|
| Progress in Lipid Research | PROG LIPID RES | Reviews |
| Advances in Nutrition | ADV NUTR | Reviews |
| American Journal of Clinical Nutrition | AM J CLIN NUTR | Clinical; structured abstract, trial reg. |
| Clinical Nutrition | CLIN NUTR | Clinical (ESPEN); reporting guidelines |
| Clinical Nutrition ESPEN | CLIN NUTR ESPEN | Clinical |
| Journal of Nutrition | J NUTR | Nutrition research |
| Journal of Nutritional Biochemistry | J NUTR BIOCHEM | Mechanistic |
| Journal of the Academy of Nutrition and Dietetics | J ACAD NUTR DIET | Dietetics |
| Journal of Nutrition Health & Aging | J NUTR HEALTH AGING | Clinical/aging |
| Current Developments in Nutrition | CURR DEV NUTR | OA |
| Journal of Renal Nutrition | J RENAL NUTR | Clinical |
| Nutrition Metabolism and Cardiovascular Diseases | NUTR METAB CARDIOVAS | Clinical |
| Nutrition | NUTRITION | Clinical |
| Nutrition Research | NUTR RES | Research |
| Appetite | APPETITE | Behavioral/sensory |
| NFS Journal | NFS J | OA |

## Formatting constraints
```yaml
publisher: Elsevier
scope: food & nutrition
reference_style: per-journal   # numbered-vancouver OR author-date; see table
abstract_words: 250
keywords_max: 6
highlights: {count: "3-5", max_chars: 85, common: true}
graphical_abstract: common
line_numbering: required
figure_dpi: {halftone: 300, line_art: 1000}
column_widths_mm: [90, 190]
```
