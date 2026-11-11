---
description: Move completed tasks from ai_task_queue.md into DONE.md, organized by the topics in ai_task_queue.md's ALL TOPICS section
---

# Goal

- Find every top-level completed task (`### [x] <Title>`) in `ai_task_queue.md`
- Move each into `DONE.md`, under the same `## <Topic>` headers as the
  `# ALL TOPICS` section of `ai_task_queue.md`
- Leave in-progress (`[ ]`, `[.]`) tasks and nested checklist items untouched

# References

- `.claude/skills/todo.rules.md`: defines the H1 stage / H2 topic / H3 task
  organization, and that `DONE.md` reuses the `# ALL TOPICS` H2 headers

# Workflow

## Load the Conventions

- Read `.claude/skills/todo.rules.md`
- Read `# ALL TOPICS` in `ai_task_queue.md` and extract the ordered `## <Topic>`
  headers (ignore `// <group>` comment lines: they are visual grouping, not topics)

## Find Completed Tasks

- Find every H3 header matching exactly `### [x] <Title>` in `ai_task_queue.md`
  - Do NOT move `### [ ]`, `### [.]`, or other markers
  - Do NOT move nested items like `- [x] ...`: they are subtask progress in a task
    that is not done
- Capture each full task block: the header line through the line before the next
  H1/H2/H3 header

## Determine the Target Topic

- Use the nearest enclosing H2 header in the source file if it matches an ALL TOPICS
  entry (case-insensitive)
- Otherwise infer the topic from the task's content against the ALL TOPICS list
- If no entry is a plausible match, do not guess: list the task and ask the user
  which topic to use, or whether to add a new topic to `# ALL TOPICS`

## Move the Tasks

- For each completed task, in source-file order:
  - Remove the block from its source file, closing the blank line gap so spacing
    stays normal
  - Append the block, unchanged, under the matching `## <Topic>` header in `DONE.md`
    - If `DONE.md` lacks that header, create it, keeping headers in `# ALL TOPICS`
      order
    - Keep tasks of the same topic together under one header

## Report

- List each moved task as `<Title> (<source file>) -> ## <Topic>`
- List separately any task that could not be confidently mapped to a topic, and why

# Verification

- [ ] Every `### [x] ...` task from `ai_task_queue.md` is now in `DONE.md`, and gone
      from its source file
- [ ] No `[ ]`, `[.]`, or nested `- [x]` item was moved or altered
- [ ] Each moved task sits under a `## <Topic>` header that appears in
      `# ALL TOPICS`
- [ ] Task content (title, body) is unchanged
- [ ] Source files keep valid markdown structure (no orphaned headers, no broken
      spacing)
