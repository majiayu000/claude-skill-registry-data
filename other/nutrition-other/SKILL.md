---
name: nutrition-other
description: "Author-guideline skill for nutrition journals from smaller/niche publishers not covered by a dedicated publisher skill: Obesity Facts (Karger), Current Opinion in Clinical Nutrition and Metabolic Care (Wolters Kluwer/Lippincott), Hepatobiliary Surgery and Nutrition (AME), Beneficial Microbes (Brill), Food & Nutrition Research (Swedish Nutrition Foundation). Use to format or check a manuscript for one of these — with the journal's source URL and default guidance. Triggers: submit to Obesity Facts, Current Opinion in Clinical Nutrition, Beneficial Microbes, Food & Nutrition Research guidelines. Also fires when the user wants to publish on/in this journal, format a manuscript for it, or match its reference/citation style."
metadata:
  publisher: "Various (Karger, Wolters Kluwer/Lippincott, AME, Brill, Swedish Nutrition Foundation)"
  verified: "2026-07"
  source: "per-journal (see table)"
---

# Niche Nutrition Journals — Author Guideline Skill

**Verified:** 2026-07 · These journals come from smaller publishers; always
confirm exact requirements at each journal's own author guide (linked below).

## Applies to
| Journal | Abbrev | Publisher | Ref style* | Source |
|---|---|---|---|---|
| Obesity Facts | OBESITY FACTS | Karger | Vancouver-numbered | https://www.karger.com/Journal/Guidelines/224039 |
| Current Opinion in Clinical Nutrition and Metabolic Care | CURR OPIN CLIN NUTR | Wolters Kluwer / Lippincott | numbered | https://journals.lww.com/co-clinicalnutrition/ |
| Hepatobiliary Surgery and Nutrition | HEPATOBIL SURG NUTR | AME Publishing | numbered (AMA-style) | https://hbsn.amegroups.org/ |
| Beneficial Microbes | BENEF MICROBES | Brill / Wageningen | author–date | https://brill.com/view/journals/bm/bm-overview.xml |
| Food & Nutrition Research | FOOD NUTR RES | Swedish Nutrition Foundation | Vancouver-numbered | https://foodandnutritionresearch.net/ |

*Confirm at the journal; these are the common defaults.

## Default guidance (apply unless the journal specifies otherwise)
- Standard IMRaD structure; unstructured abstract ≤250 words; 4–6 keywords.
- Human/clinical studies: ethics approval, trial registration where applicable, and the relevant reporting guideline (CONSORT/STROBE/PRISMA), following ICMJE.
- Declarations: competing interests, funding, author contributions, data availability.
- Figures ≥300 dpi (line art higher); editable tables; cite all display items in order.
- **Reference style:** use the per-journal style in the table above; if unknown, default to **APA 7.0** and flag for confirmation.

## Submission checklist
- [ ] Journal's reference style (see table) or APA 7.0 default · [ ] Abstract ≤250 words · [ ] 4–6 keywords
- [ ] Ethics/registration/reporting guideline for clinical work
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
