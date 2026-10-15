---
name: architect
description: A skill for project planning and backlog management. Categorizes beans,
  manages subtasks, sets priorities, and identifies blocking dependencies.
metadata:
  aliases:
  - archie
  - architect
  use_git_worktree: false
---

Help me do project planning. First, run "beans prime" to understand how the beans issue tracker works. Then run "beans show {{TASK_ID}}" to and review the output to understand the {{TASK_ID}} task.

Next, assess whether this bean is an epic, feature or task and use "beans update" to set the bean type appropriately. Next, come up with subtasks that go under task {{TASK_ID}}. Make sure each child or subtask is associated with the correct parent. Ensure that each child and subtask has a detailed description with a checklist.

Run "beans list" to get a full list of all of the beans. Then iterate over each bean, running "beans show" to better understand each item in the list. For each bean not in a "completed" state, analyze which beans have the highest priority, and which beans are blocking other beans.  

Then, run "beans update --help" to understand how the "beans update" command works.

Use the "beans update" command with the "--blocking" parameter to denote when one bean is blocking another. Use the "--priority" argument to set the priority to one of the following values: critical, high, normal, low, deferred.

Write whatever biases and assumptions you find to the ASSUMPTIONS.md file.
