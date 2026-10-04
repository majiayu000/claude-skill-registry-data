---
name: science-aaas
description: "Author-guideline skill for the AAAS Science family that food & nutrition researchers publish in: Science, Science Advances, Science Translational Medicine, Science Immunology, Science Signaling, Science Robotics. Use to format or check a manuscript for a Science-family journal — very tight length limits, short abstract, Science numbered reference style, and figure specs. Triggers: submit to Science, Science Advances guidelines, AAAS Science formatting. Also fires when the user wants to publish on/in this journal, format a manuscript for it, or match its reference/citation style."
metadata:
  publisher: "AAAS (American Association for the Advancement of Science)"
  verified: "2026-07"
  source: "https://www.science.org/content/page/science-information-authors"
---

# AAAS Science Family — Author Guideline Skill

**Publisher:** AAAS · **Verified:** 2026-07 · Confirm exact limits at the journal's Information for Authors (very strict; differ by title/article type).

## Applies to
Science; Science Advances (open access); Science Translational Medicine; Science
Immunology; Science Signaling; Science Robotics.

## Format (Science style)
- **References: numbered** in citation order, Science style (numbered list `1., 2., …`; in-text `(1)`, `(2, 3)`). Full author lists; include DOIs.
  > 1. A. B. Author, C. D. Author, Title of the article. *Science* **380**, 1234 (2026).
- **Abstract:** single paragraph, very short (Science Research Articles ~125 words; Science Advances longer — confirm).
- **Structure:** Science Research Articles are tightly length-limited (main text often ~2,500–4,500 words incl. references/notes; Reports shorter); Materials and Methods often in supplementary. Science Advances allows more.
- **Display items:** limited; cite `Fig. 1` in order.
- **Mandatory:** data/materials availability; competing interests; author contributions; supplementary materials for full methods.
- **Figures:** ≥300 dpi; RGB; sized to one/two columns; accessible palette.

## Formatting constraints
```yaml
publisher: AAAS Science
reference_style: science-numbered
abstract_words: 125   # Science Research Article; confirm per journal
methods: often-in-supplementary
data_availability: required
figure_dpi: 300
```
