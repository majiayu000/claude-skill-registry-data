---
name: agri-other
description: "Author-guideline skill for Q1/Q2 agriculture journals from society, academy, and regional publishers not covered by a dedicated publisher skill: Soil (Copernicus), Plant Soil and Environment / Czech Journal of Animal Science (Czech Academy of Agricultural Sciences), CABI titles, Crop and Pasture Science (CSIRO), Animal Bioscience (AAAP), Journal of Animal Science and Technology (KSAST), Australian Journal of Grape and Wine Research (IVES), Am. J. Enology and Viticulture, Seed Science and Technology (ISTA), Scientia Agricola (USP/ESALQ), and similar. Use to format or check a manuscript for one of these agriculture journals — with the journal's source URL and default guidance. Triggers: submit to Soil Copernicus, Crop and Pasture Science, Animal Bioscience, Scientia Agricola, Czech Journal of Animal Science guidelines. Also fires when the user wants to publish on/in one of these journals, format a manuscript for it, or match its reference/citation style."
metadata:
  publisher: "Various (Copernicus, Czech Academy of Agricultural Sciences, CABI, CSIRO, De Gruyter, society and university presses)"
  verified: "2026-07"
  source: "per-journal (see table)"
---

# Society & Regional Agriculture Journals — Author Guideline Skill

**Verified:** 2026-07 · These are the **Q1/Q2 agriculture journals whose publisher
format is not shared with any other skill in this suite** (see
`journals/_coverage_agriculture.md`). They come from societies, academies, and
university presses, so requirements vary — **always confirm at the journal's own
author guide** (linked below). Agriculture journals from Elsevier, Wiley, Springer,
Taylor & Francis, MDPI, Cambridge, Oxford, Emerald, Frontiers, BMC, KeAi, ACS, and
Annual Reviews use the existing publisher-tier skills instead — no duplicates.

## Applies to (representative Q1/Q2 titles)
| Journal | Abbrev | Publisher | Ref style* | Source |
|---|---|---|---|---|
| SOIL | SOIL | Copernicus (EGU) | author–date | https://www.soil-journal.net/submission.html |
| Plant, Soil and Environment | PLANT SOIL ENVIRON | Czech Acad. Agric. Sciences | author–date | https://pse.agriculturejournals.cz/ |
| Czech Journal of Animal Science | CZECH J ANIM SCI | Czech Acad. Agric. Sciences | author–date | https://cjas.agriculturejournals.cz/ |
| Crop and Pasture Science | CROP PASTURE SCI | CSIRO Publishing | author–date | https://www.publish.csiro.au/cp/forauthors |
| Animal Bioscience | ANIM BIOSCI | AAAP | numbered | https://www.animbiosci.org/authors/authors.php |
| Journal of Animal Science and Technology | J ANIM SCI TECHNOL | KSAST | numbered | https://www.janimscitechnol.org/authors/authors.php |
| Australian Journal of Grape and Wine Research | AUST J GRAPE WINE R | IVES | author–date | https://ives-openscience.eu/ |
| American Journal of Enology and Viticulture | AM J ENOL VITICULT | ASEV | author–date | https://www.ajevonline.org/content/information-authors |
| Seed Science and Technology | SEED SCI TECHNOL | ISTA | author–date | https://www.seedtest.org/ |
| Scientia Agricola | SCI AGR | Univ. São Paulo (ESALQ) | author–date | https://www.scielo.br/j/sa/ |
| Journal of Agricultural Engineering | J AGRIC ENG-ITALY | PagePress | numbered | https://www.agroengineering.org/ |
| International Journal of Agricultural and Biological Engineering | INT J AGR BIOL ENG | Chinese Acad. Agric. Engineering | numbered | https://www.ijabe.org/ |

*Confirm at the journal; these are the common defaults. The full Q1/Q2 list routed
here is in [`_coverage_agriculture.md`](../_coverage_agriculture.md).

## Default guidance (apply unless the journal specifies otherwise)
- Standard IMRaD; unstructured abstract ≤250 words; 4–6 keywords.
- **Field/agronomic trials:** state site (coordinates), season(s)/years, soil type and
  classification, cultivar, plot size, experimental design (RCBD/split-plot) and
  replication, agronomic management, and the statistical model — reproducibility is
  the most common reviewer complaint.
- **Animal studies:** ethics/animal-care approval and the **ARRIVE** guideline; housing,
  diet composition, and the experimental unit (pen vs animal).
- Declarations: competing interests, funding, author contributions, data availability.
- SI units; figures ≥300 dpi (line art higher); editable tables; all display items
  cited in order.
- **Reference style:** use the per-journal style above; if unknown, default to
  **APA 7.0** and flag for confirmation.

## Submission checklist
- [ ] Journal's reference style (see table) or APA 7.0 default · [ ] Abstract ≤250 words · [ ] 4–6 keywords
- [ ] Site/season/soil/cultivar/design/replication reported (field work)
- [ ] Ethics approval + ARRIVE (animal work) · [ ] Experimental unit stated
- [ ] Competing interests + funding + contributions + data availability
- [ ] Figures ≥300 dpi · [ ] Confirm exact limits at the journal source URL · [ ] Cover letter

## Formatting constraints
```yaml
publisher: various (see table)
reference_style: per-journal   # else APA 7.0 default
abstract_words: 250
keywords_max: 6
figure_dpi: {halftone: 300, line_art: 1000}
confirm_at_source: true
```
