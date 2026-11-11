---
description: Make sure that the PDF rendering of a slide smd file is well formed
model: haiku
---

# Goal
- Make sure that the PDF rendering of a slide `.smd` file is well formed

# Inputs
- `<SMD_FILE>`: lecture file to check
  - E.g., `msml610/lectures_source/Lesson01.4-Brief_History_of_AI.smd`

# Workflow

## Render the Slides
- Run:
  ```bash
  > gen_slides.py <SMD_FILE> -- --toc_type=remove_headers
  ```
- Read the generated PDF `<PDF_FILE>`
  - E.g., `msml610/lectures_pdf.tmp/Lesson01.4-Brief_History_of_AI.pdf`

## Check the Slide Count
- Check that the slide count in `<SMD_FILE>`:
  ```bash
  > grep "^* " <SMD_FILE> | wc -l
  ```
  equals the PDF page count, not counting the `References` page
- If the counts differ, some slides `* <TITLE>` render in more than one PDF page
- Then adjust the picture sizes and the text, so each slide fits exactly in one page

# Conventions
- Follow the role in `.claude/skills/role.ai_researcher.md`
- Read `.claude/skills/slides.rules.md`

# Verification
- [ ] The number of slides in `<SMD_FILE>` is the same as in `<PDF_FILE>`
