---
name: jafc
description: "Author-guideline skill for Journal of Agricultural and Food Chemistry (ACS, ISSN 0021-8561). Use to format or check a manuscript for JAFC — ACS structure, TOC/abstract graphic, ACS reference style, and figure specs. Triggers: submit to Journal of Agricultural and Food Chemistry, JAFC guidelines, ACS food chemistry formatting. Also fires when the user wants to publish on/in this journal, format a manuscript for it, or match its reference/citation style."
metadata:
  publisher: "American Chemical Society"
  issn: "0021-8561"
  verified: "2026-07"
  source: "https://publish.acs.org/publish/author_guidelines?coden=jafcau"
---

# Journal of Agricultural and Food Chemistry (JAFC) — Author Guideline Skill

**Publisher:** American Chemical Society · **ISSN:** 0021-8561 · **Source:** [ACS author guidelines (JAFC)](https://publish.acs.org/publish/author_guidelines?coden=jafcau) · **Verified:** 2026-07 (confirm at source).

## Aims & scope
Original research on the chemistry and biochemistry of agriculture and food: chemistry/biochemistry of foods and beverages, bioactive constituents, food safety/toxicology, analytical methods, agricultural chemistry, and nutrition chemistry. Emphasis on chemical rigor and food/agriculture relevance.

## Article types
Article; Review; Perspective; New Analytical Methods (must show clear advance/validation); Letters to the Editor.

## Manuscript structure (ACS)
Title → Authors & affiliations → Abstract → Keywords → Introduction → Materials and Methods → Results and Discussion → (Conclusions) → Author Information → Acknowledgments → Abbreviations → References. A **TOC/abstract graphic** is required.

- **Abstract:** ≤200 words, single paragraph.
- **Keywords:** ~6.
- **Word/length:** confirm current page/word budget in the ACS guidelines; JAFC favors concise, data-dense papers.

## Reference style
**ACS style, numbered.** In-text superscript or italic numbers per ACS; numbered reference list. Use the ACS journal-article format with article titles.

Example (ACS):
> (1) Author, A. B.; Author, C. D. Title of the Article. *J. Agric. Food Chem.* **2023**, *71* (10), 1234–1245. https://doi.org/10.1021/acs.jafc.3cxxxxx

## Figures & tables
Figures ≥300 dpi (line art/combination higher); ACS figure widths (~8.25 cm single, ~17.78 cm double); embed fonts (Arial/Helvetica); TOC graphic sized per ACS (~8.5 × 4.75 cm); editable tables; cite in order. Follow ACS SI/units conventions and report method validation (LOD/LOQ, recovery) for analytical work.

## Submission checklist
- [ ] TOC/abstract graphic · [ ] Abstract ≤200 words · [ ] ~6 keywords
- [ ] ACS numbered references with article titles + DOIs
- [ ] Method validation reported (analytical papers) · [ ] Safety/ethics statements as applicable
- [ ] Figures ≥300 dpi, ACS widths · [ ] Cover letter (novelty + food/ag relevance)

## Formatting constraints
```yaml
journal: Journal of Agricultural and Food Chemistry
publisher: ACS
reference_style: acs-numbered
abstract_words: 200
keywords_max: 6
toc_graphic: required
figure_dpi: {halftone: 300, line_art: 1000}
column_widths_cm: [8.25, 17.78]
```
