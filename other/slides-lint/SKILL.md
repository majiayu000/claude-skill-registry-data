---
description: Lint the slides incrementally to follow the conventions
model: haiku
---

# Goal
- The user passes:
  - `<FILE>`: a pointer to a file storing slides
  - `<NUM_SLIDES>`: number of slides to fix at a time (default: 5). The user can
    ask to fix all slides in one shot
- Fix the slides in `<FILE>`, `<NUM_SLIDES>` at a time, so the user can review
  each chunk

# Workflow
- Read `.claude/skills/slides.rules.md`

## Process Slides
- Process `<NUM_SLIDES>` slides at a time from `<FILE>`
  - Each slide is a chunk of text starting with `* <TITLE>`
- Find the rules in `.claude/skills/slides.rules.md` that the current slides break
- Apply changes so the slides follow the rules

## Wait for Confirmation
- Wait for the user to confirm before moving on to the next chunk of
  `<NUM_SLIDES>` slides

# Verification
- [ ] Once all chunks of `<FILE>` are processed, make sure the slides render
  correctly, e.g.,
  ```bash
  > gen_slides.py -i <FILE> --notes_to_pdf_args="--skip_action open_pdf"
  ```
