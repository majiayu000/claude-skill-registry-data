---
name: documentation-writer
description: >-
  Writing a Russian school пояснительная записка (ПЗ) that has to survive a jury:
  the НИР and проект/сайт structures, title page, format profiles, [N, с. X]
  citations, markdown-to-docx build and the pre-submission review. Use for
  "написать пояснительную записку", "оформить работу для конкурса", a project or
  site description, or preparing a school work for submission.
---

# documentation-writer — documents that go to a jury

> Home branch in Memora: `root/skill/documentation-writer`.

## Choosing a part

| Situation | Part |
|---|---|
| A school ПЗ for a research or project contest, its structure, format and pre-submission review | `parts/pz-writer/` |
| A long-form HTML document or PR review instead of a contest paper | the `documents` router |

## Rules

- **The organizer's requirements beat this skill.** A volume limit that is not
  published online is a question for the районное управление образования, not a
  number to guess (`parts/pz-writer/` says the same and means it).
- **Forks worth `ask_questions`**: which contest and genre (НИР or проект), which
  format profile, missing facts for the title page (school by charter, author,
  class, year), and a claim the work cannot evidence. Placeholders stay
  placeholders until the owner fills them — names are never invented.
- **The document is a build artifact.** The markdown source is edited; the .docx is
  generated (`parts/pz-writer/scripts/build_pz_docx.py`) and checked
  (`pz_check.py`), never hand-edited. Both go into the commit.
- **No machinery in the text**: no test names, script paths, dev servers, git talk
  or wording about an assistant. The jury reads results, not the production process.
- **Finished work and its lessons** become Memora nodes under
  `root/skill/documentation-writer`, with the contest result when it is known.

## Related

`documents` (md → HTML, reading Word files, diagrams), `antislop` (`references/prose-editing.md`
for tone and slop patterns), `decks` when the same work also needs a defence deck.
