---
name: food-function
description: "Shared author-guideline skill for Royal Society of Chemistry food journals: Food & Function and Sustainable Food Technology. Use to format or check a manuscript for an RSC food journal — article types, structure, RSC superscript-numbered references, and figure specs. Triggers: submit to Food & Function, Sustainable Food Technology guidelines, RSC food formatting. Also fires when the user wants to publish on/in this journal, format a manuscript for it, or match its reference/citation style."
metadata:
  publisher: "Royal Society of Chemistry"
  verified: "2026-07"
  source: "https://www.rsc.org/journals-books-databases/author-and-reviewer-hub/authors-information/"
---

# RSC Food Journals — Shared Author Guideline Skill

**Publisher:** Royal Society of Chemistry · **Verified:** 2026-07 · Sources: [Food & Function](https://pubs.rsc.org/en/journals/journalissues/fo), [Sustainable Food Technology](https://pubs.rsc.org/en/journals/journalissues/fb). Use the RSC article template.

## Applies to
| Journal | Abbrev | Scope |
|---|---|---|
| Food & Function | FOOD FUNCT | Physical/biological function of food, nutrition, health effects |
| Sustainable Food Technology | SUSTAIN FOOD TECHNOL | Sustainable food processing/technology (open access) |

## Article types
Full papers (Research Articles), Communications (urgent, high-impact, short), Reviews, and Perspectives. Food & Function expects a clear link to biological/physiological function, not composition alone.

## Manuscript structure
Title → Author list & affiliations → Abstract → Introduction → Results and discussion → Experimental (methods placed after results, RSC convention) → Conclusions → Conflicts of interest → Acknowledgements → References. A **table-of-contents (TOC) graphic + one-sentence TOC entry** is required.

- **Abstract:** concise, unstructured (~150–200 words).
- **Experimental section:** after Results & Discussion (RSC style).
- **Conflicts of interest statement:** mandatory (state "There are no conflicts to declare" if none).

## Reference style
**RSC style: superscript numbers** in order of citation; numbered reference list. Journal names abbreviated, year bold, volume italic, first page only.

Example:
> 1  A. B. Author and C. D. Author, *Food Funct.*, 2023, **14**, 1234.

## Figures & tables
Figures ≥300 dpi (≥600 for line art); fit single (~8.3 cm) or double (~17.1 cm) column; RGB online; editable tables; cite in order. TOC graphic ~8 × 4 cm.

## Submission checklist
- [ ] TOC graphic + one-sentence TOC text · [ ] Abstract ~150–200 words
- [ ] Experimental after Results & Discussion · [ ] RSC superscript-numbered references
- [ ] Conflicts of interest statement · [ ] Data availability (RSC requirement)
- [ ] Figures ≥300 dpi · [ ] Cover letter (significance / function link)

## Formatting constraints
```yaml
publisher: RSC
reference_style: rsc-superscript-numbered
abstract_words: 200
toc_graphic: required
methods_section: after-results   # "Experimental"
conflicts_statement: required
figure_dpi: {halftone: 300, line_art: 600}
column_widths_cm: [8.3, 17.1]
```
