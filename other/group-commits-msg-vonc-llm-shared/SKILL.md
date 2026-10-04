---
name: group-commits-msg
description: 'Group files and write a conventional commit message for each group, when the user enter the prompt "group commits messages" or "group commit messages" or "group commits message".'
user-invocable: true
metadata:
  - "This skill is used to group files and write a conventional commit message for each group in the project-root `a.commit` (`%PRJ_DIR%\\a.commit`, never under `docs/` or any subfolder)."
  - "you need to use git diff --name-only --cached to get the list of staged files, and then group them based on their dependencies"
  - "Any .md files in you context, as well as previous prompts in your current conversation, can provide additional context for grouping files."
---

[Instruction](../../../instructions/group-commits-msg.md)
