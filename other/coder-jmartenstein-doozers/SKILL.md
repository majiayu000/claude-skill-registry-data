---
name: coder
description: A skill for executing development tasks using the beans utility. Handles
  task initialization, child ticket management, status updates, and PR summary generation.
metadata:
  aliases:
  - cary
  - coder
  use_git_worktree: true
---

Start working on {{TASK_ID}}. Runs "beans prime" and "beans show {{TASK_ID}}". Use the "beans query" utility to get a list of all of the child tickets for {{TASK_ID}} Study the parents and child tickets. Work on all child tickets subtasks for {{TASK_ID}}. Use "beans update" with the "--status" option to mark the status of each ticket as in_progress. Update the beans to mark commands as done. Do not stop working until "{{TASK_ID}}" is deemed complete. When complete, create a file to be added to the pull request, titled "PR_SUMMARY.md".
