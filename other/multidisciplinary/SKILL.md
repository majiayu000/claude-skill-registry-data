---
name: multidisciplinary
description: "Author-guideline skill for multidisciplinary and cross-discipline journals that food & nutrition researchers publish in but which sit outside the food/nutrition JCR categories: eLife, PLOS Biology, PLOS Medicine, National Science Review, The Innovation, Environmental Science & Technology (food safety/contaminants), Gut and Gastroenterology (nutrition/GI), Diabetes Care (clinical nutrition), and The ISME Journal (food/gut microbial ecology). Use to format or check a manuscript for one of these — with the journal's publisher, reference style, and source URL. Triggers: submit to eLife, PLOS, National Science Review, Environmental Science & Technology, Gut, Gastroenterology, Diabetes Care, ISME Journal guidelines. Also fires when the user wants to publish on/in this journal, format a manuscript for it, or match its reference/citation style."
metadata:
  publisher: "Various (see table)"
  verified: "2026-07"
  source: "per-journal (see table)"
---

# Multidisciplinary & Cross-Discipline Journals — Author Guideline Skill

**Verified:** 2026-07 · These journals are high-priority venues (multidisciplinary
or adjacent fields) that food & nutrition researchers publish in. Always confirm
the current requirements at each journal's own author guide.

## Applies to
| Journal | Abbrev | Publisher | Ref style* | Source |
|---|---|---|---|---|
| eLife | ELIFE | eLife Sciences | numbered (Vancouver) | https://elifesciences.org/author-guide |
| PLOS Biology | PLOS BIOL | PLOS | numbered (Vancouver) | https://journals.plos.org/plosbiology/s/submission-guidelines |
| PLOS Medicine | PLOS MED | PLOS | numbered (Vancouver) | https://journals.plos.org/plosmedicine/s/submission-guidelines |
| National Science Review | NATL SCI REV | Oxford / NSFC | numbered | https://academic.oup.com/nsr/pages/General_Instructions |
| The Innovation | INNOVATION | Cell Press / Youth Innov. | numbered | https://www.cell.com/the-innovation/authors |
| Environmental Science & Technology | ENVIRON SCI TECHNOL | ACS | ACS numbered | https://publish.acs.org/publish/author_guidelines?coden=esthag |
| Gut | GUT | BMJ | numbered (Vancouver) | https://gut.bmj.com/pages/authors/ |
| Gastroenterology | GASTROENTEROLOGY | Elsevier / AGA | numbered | https://www.gastrojournal.org/authors |
| Diabetes Care | DIABETES CARE | American Diabetes Assoc. | numbered | https://diabetesjournals.org/care/pages/instructions-for-authors |
| The ISME Journal | ISME J | Oxford / ISME (Springer Nature legacy) | numbered | https://academic.oup.com/ismej/pages/general-instructions |

*Best-known default; confirm at the source. Most of these use numbered
(Vancouver-style) references; ES&T uses ACS style.

## Common requirements
- Standard IMRaD (clinical titles may want structured abstracts + trial
  registration + CONSORT/STROBE; see `../../food-research/references/reporting-guidelines.md`).
- Mandatory declarations: competing interests, funding, author contributions, data availability; ethics for human/animal work.
- Figures ≥300 dpi; editable tables; cite display items in order.
- **Reference style:** use the per-journal style in the table; if unsure, default to numbered (Vancouver) and flag for confirmation.

## Formatting constraints
```yaml
publisher: various (see table)
reference_style: per-journal   # mostly numbered-vancouver; ES&T = ACS
abstract: per-journal (structured for clinical titles)
data_availability: required
figure_dpi: 300
confirm_at_source: true
```
