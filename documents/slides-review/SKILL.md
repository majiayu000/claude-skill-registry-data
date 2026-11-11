---
description: Review slide structure and content, then propose and apply improvements
model: opus
---

# Goal
- Given a markdown file with technical slides, review content for correctness,
  clarity, and structure
- This skill composes `/slides.reorganize` (structure) and `/slides.criticize`
  (content)

# Workflow

- Read the conventions in `.claude/skills/slides.rules.md`

## Propose Structural Improvements
- Run the flow from `.claude/skills/slides.reorganize/SKILL.md` through its
  `## Wait for User` section, and save the proposal

## Propose Content Improvements
- Run the flow from `.claude/skills/slides.criticize/SKILL.md` on the deck, with the
  same axes and High/Medium/Low ranking
- Also propose better slide titles

### Ignore TODOs and Comments
- Leave TODOs and comments in the format
  ```text
  // TODO...
  ```
  untouched

## Ask User and Implement
- Present the structural proposal and the ranked content findings together, numbered
  so each is easy to refer to
- Ask which structural moves and content fixes to apply
- After the user approves a subset, apply the reorganization and content changes
  together, in place

# Verification
- [ ] Make sure the updated slides render correctly, e.g.,
  ```bash
  > gen_slides.py -i <FILE> --notes_to_pdf_args="--skip_action open_pdf"
  ```
