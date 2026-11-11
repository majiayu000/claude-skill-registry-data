---
description: Move content from a file into another one without redundancy
model: haiku
---

# Goal

- You are an expert technical writer
- Given a source file `<SRC_FILE>` and a destination file `<DST_FILE>`, move and
  merge the content of `<SRC_FILE>` into `<DST_FILE>`, following the conventions in
  - `.claude/skills/markdown.rules.md`
  - `.claude/skills/text.rules.md`

# Workflow

- Move chunks of text from `<SRC_FILE>` that fit in `<DST_FILE>` without adding
  redundancy
  - Place them under the right headers of `<DST_FILE>`, following its style and
    rules
  - Delete each moved chunk from `<SRC_FILE>`
- Delete chunks of `<SRC_FILE>` that are redundant with `<DST_FILE>`
- Leave in `<SRC_FILE>` only text that does not apply to `<DST_FILE>`

# Verification
- [ ] Confirm no redundant content remains in `<DST_FILE>`
- [ ] Confirm `<SRC_FILE>` contains only content that could not be moved
