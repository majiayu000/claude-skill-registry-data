---
name: j-dairy-science
description: "Author-guideline skill for Journal of Dairy Science (Elsevier on behalf of ADSA, ISSN 0022-0302). Use to format or check a manuscript for JDS — its distinct interpretive summary, section structure, author–date references, and figure specs differ from generic Elsevier journals. Triggers: submit to Journal of Dairy Science, JDS guidelines, ADSA formatting. Also fires when the user wants to publish on/in this journal, format a manuscript for it, or match its reference/citation style."
metadata:
  publisher: "Elsevier / American Dairy Science Association (ADSA)"
  issn: "0022-0302"
  verified: "2026-07"
  source: "https://www.journalofdairyscience.org/content/authorinfo"
---

# Journal of Dairy Science (JDS) — Author Guideline Skill

**Publisher:** Elsevier for ADSA · **ISSN:** 0022-0302 · **Source:** [Author info](https://www.journalofdairyscience.org/content/authorinfo) · **Verified:** 2026-07 (confirm at source).

## Aims & scope
Original research on dairy science: dairy foods (chemistry, microbiology, processing, safety), animal nutrition, physiology, genetics, management, and dairy production. Rigorous methodology and statistics expected.

## Article types
Research articles; Short communications; Reviews; Hot topics; Technical notes.

## Manuscript structure (JDS-specific)
Title page → **Interpretive Summary** (a short plain-language summary, ~100 words, JDS requirement) → Abstract → Keywords → Introduction → Materials and Methods → Results → Discussion (or combined Results and Discussion) → Conclusions → Acknowledgments → References → Tables → Figure legends → Figures. Continuous line numbers required.

- **Abstract:** single paragraph, ≤300 words (confirm).
- **Interpretive summary:** required; concise significance for a broad audience.
- **Keywords:** typically 5.

## Reference style
**Author–date (name–year)**, ADSA/JDS format. In-text `(Author and Author, 2023)`; list alphabetical.

Example:
> Author, A. B., C. D. Author, and E. F. Author. 2023. Title of paper. J. Dairy Sci. 106:1234–1245. https://doi.org/10.3168/jds.2023-xxxxx

## Figures & tables
Editable tables; figures ≥300 dpi (line art higher); grayscale/color per online/print policy; SI units; report means with SEM and the statistical model.

## Statistics (journal-specific)
JDS expects clear experimental design, the mixed-model/ANOVA structure, error terms, and appropriate multiple-comparison procedures; report P-values and SEM.

## Submission checklist
- [ ] Interpretive summary (~100 words) · [ ] Abstract ≤300 words · [ ] ~5 keywords
- [ ] Author–date (ADSA) references with DOIs · [ ] Line + page numbering
- [ ] Statistical model + SEM reported · [ ] Animal-care/ethics statement if applicable
- [ ] Figures ≥300 dpi · [ ] Cover letter

## Formatting constraints
```yaml
journal: Journal of Dairy Science
publisher: Elsevier/ADSA
reference_style: author-date
interpretive_summary: {required: true, words: 100}
abstract_words: 300
keywords: 5
line_numbering: required
figure_dpi: {halftone: 300, line_art: 1000}
```
