---
description: Fix errors in slides without changing their structure
model: haiku
---

# Goal
- Given a file with slides or user content, fix errors and imprecisions without
  changing the slide structure

# Workflow

## Read the Rules
- Read `.claude/skills/slides.rules.md` and follow its conventions strictly
- A slide title is prefixed with `*` and has hierarchical bullets
  - E.g.,
    ```
    * How Can a Node Be Influenced by Its Children?

    - A **descendant can influence its ancestor** indirectly through _"explaining
      away"_
      - Evidence about the descendant can change what you believe about the
        ancestor through dependent paths
      - Information flows both ways in Bayesian networks
    ```

## Leave Structure Unchanged
- Do not change the structure of the text (e.g., title, bullet structure, div
  fenced blocks)
- Keep the content of the existing text
- Do not add formatting violations while fixing grammar. Punctuation belongs to
  `.claude/skills/slides.fix_formatting/SKILL.md`. Follow
  `.claude/skills/slides.rules.md` as read in the Read the Rules step

## Fix Mistakes
- Fix English grammar
- Fix a conceptual mistake only if you are sure of the correction

# Verification
- [ ] Make sure that the updated slides render correctly, e.g.,
  ```bash
  > gen_slides.py -i <FILE> --notes_to_pdf_args="--skip_action open_pdf"
  ```
