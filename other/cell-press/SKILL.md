---
name: cell-press
description: "Shared author-guideline skill for Cell Press journals that food & nutrition researchers publish in: Cell, Cell Metabolism, Cell Host & Microbe, Molecular Cell, Immunity, Current Biology, Cell Reports Medicine, One Earth, Joule, Matter, Chem. Use to format or check a manuscript for a Cell Press journal — structure with STAR Methods, abstract + eTOC blurb, Cell Press reference style, and figure specs. Triggers: submit to Cell, Cell Metabolism, Cell Host & Microbe guidelines, Cell Press formatting. Also fires when the user wants to publish on/in this journal, format a manuscript for it, or match its reference/citation style."
metadata:
  publisher: "Cell Press (Elsevier)"
  verified: "2026-07"
  source: "https://www.cell.com/cell/authors"
---

# Cell Press — Author Guideline Skill

**Publisher:** Cell Press (Elsevier) · **Verified:** 2026-07 · Confirm the exact reference style and limits at the specific journal's Guide for Authors (Cell Press has updated citation formats; verify current style).

## Applies to (food/nutrition-relevant)
| Journal | Abbrev | Relevance |
|---|---|---|
| Cell | CELL | Flagship |
| Cell Metabolism | CELL METAB | Nutrition & metabolism |
| Cell Host & Microbe | CELL HOST MICROBE | Gut/food microbiome |
| Molecular Cell | MOL CELL | Molecular |
| Immunity | IMMUNITY | Nutr-immunology |
| Current Biology | CURR BIOL | Broad biology |
| Cell Reports Medicine | CELL REP MED | Clinical/translational |
| One Earth | ONE EARTH | Food systems/sustainability |
| Joule / Matter / Chem | — | Energy/materials/chemistry |

## Format (Cell Press style)
- **References:** Cell Press style — **confirm current format at the journal** (numbered vs author–year has changed across titles/years). Include DOIs and full author lists.
- **Abstract:** ~150 words, single paragraph; plus a short **eTOC blurb** (one–two sentences) and a **graphical abstract** for many titles; **Highlights** (3–4 bullets) required.
- **Structure:** Title → Abstract → Introduction → Results → Discussion → **STAR★Methods** (structured methods) → References → Figure legends. Research articles use STAR Methods.
- **Display items:** cite `Figure 1` in order; supplemental information allowed.
- **Mandatory:** data/code availability (STAR Methods Key Resources Table), declaration of interests, author contributions.
- **Figures:** ≥300 dpi; RGB; Cell column widths; accessible palette.

## Formatting constraints
```yaml
publisher: Cell Press
reference_style: cell-press   # confirm current numbered vs author-year at journal
abstract_words: 150
highlights: {count: "3-4", required: true}
graphical_abstract: common
methods: STAR-Methods
data_and_code_availability: required
figure_dpi: 300
```
