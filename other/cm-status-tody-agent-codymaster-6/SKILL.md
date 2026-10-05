---
name: cm-status
description: View a quick progress summary of current tasks.
---

# Command: `/cm-status`

When this command is called, the AI Assistant should:

1. **Read progress:** Quickly read the `task.md` file or current task state.
2. **Brief report:** Return an ultra-concise message (1-2 sentences) indicating which task was just completed, which task is next, and whether anything is blocked by errors/bugs.
3. No need to print the full board (save that for `/cm-dashboard`).
