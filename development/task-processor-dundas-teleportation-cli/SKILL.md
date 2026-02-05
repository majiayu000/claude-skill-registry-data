---
name: task-processor
description: Process a task list one sub-task at a time with pause/confirm gates, test/commit protocol, and file tracking.
---

# Task Processor

## Task Implementation
- One sub-task at a time. Do not start the next sub-task until user says "yes" or "y".
- Completion protocol:
  1. When finishing a sub-task, mark it `[x]`.
  2. If all sub-tasks under a parent are `[x]`, then:
     - Run full test suite.
     - If tests pass: stage changes (`git add .`).
     - Clean up temporary files/code.
     - Commit using conventional commit style with multi-`-m` messages describing changes and referencing task/PRD.
        ```
        git commit -m "feat: add payment validation logic" -m "- Validates card type and expiry" -m "- Adds unit tests for edge cases" -m "Related to T123 in PRD"
        ```
  3. After commit, mark the parent task `[x]`.
- Stop after each sub-task and wait for user go-ahead.

## Task List Maintenance
1. Update the task list as you work: mark `[x]`, add tasks if needed.
2. Maintain the "Relevant Files" section with one-line purpose per file.

## AI Instructions
1. Regularly update the task list after finishing significant work.
2. Follow completion protocol strictly.
3. Add newly discovered tasks.
4. Keep "Relevant Files" accurate and up to date.
5. Before starting, check which sub-task is next.
6. After implementing a sub-task, update the file and pause for approval.

## References
- See `reference.md`.
