---
description: Incorporate content into other material (books, slides, papers, blog ideas)
model: sonnet
---

# Goal

- The user passes, in this order:
  1. The content `<CONTENT>` to incorporate
  2. Optionally, the target `<TARGET>`: a file (e.g., a book, slides, paper,
     blog) or a part of a file (e.g., a chapter, section, slide number)
- Propose where and how to include `<CONTENT>` in `<TARGET>`

# Workflow

- Read the proposed content `<CONTENT>`
- Resolve `<TARGET>`
  - If `<TARGET>` was passed:
    - If it is a part of a file (e.g., "chapter 3", "slide 12"), open that file
      and jump to that part
    - If it is a whole file in a book or course (e.g., `book_springer/map.md`),
      read `map.md` to understand the structure of the material
  - If `<TARGET>` was not passed, find it
    - List candidate files for `<CONTENT>` (e.g., books, slides, papers, blog
      posts under the relevant course or project dir), using each file's
      `book_map.md` or table of contents when one exists
    - Compare the topic of `<CONTENT>` against each candidate's title, headers,
      and structure. Rank candidates by relevance
    - If exactly one candidate is a clear match, use it as `<TARGET>` and tell
      the user which file was picked and why
    - If several candidates are close, or none is a plausible match, STOP and ask
      the user to confirm or pick the target. Do not guess
- Find which part of `<TARGET>` the content is relevant for
  - If more than one location is plausible, or none fits well, STOP and ask the
    user where to add the content. Do not guess
- Propose how to integrate `<CONTENT>` in `<TARGET>` using bullet points,
  following `.claude/skills/markdown.rules.md` and `.claude/skills/text.rules.md`

# Verification

- [ ] `<TARGET>` is either the file the user passed or one the user confirmed,
      not guessed
- [ ] The proposed location exists in `<TARGET>` (e.g., a real chapter or slide)
- [ ] The proposal follows `.claude/skills/markdown.rules.md` and
      `.claude/skills/text.rules.md`
- [ ] The user was asked for clarification if the file or the location within it
      was ambiguous
