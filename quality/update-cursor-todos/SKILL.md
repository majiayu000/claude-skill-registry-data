---
name: update-cursor-todos
description: Update Cursor plan and agent todo items. Invoke only when explicitly called by user.
user-invocable: true
disable-model-invocation: false
---
# Update Todos

Review the plan and cursor todos, validate status of each, then update with the correct status of each.

If a plan is fully complete, move it to appropriate folder if one is available.
If unsure, stop and ask.
