---
description: Move tasks out of ai_task_queue.md's TO REORG section into the right H1 stage and H2 topic, using an optional Priority tag, after user confirmation
---

# Goal

- Find every H3 task under `# TO REORG` in `ai_task_queue.md`
- For each task, find its target H1 stage (from an optional `- Priority: <Stage>`
  line in the body, default `# BACKLOG`) and its target H2 topic (from the
  `# ALL TOPICS` list)
- Get explicit user confirmation of all proposed moves before changing the file
- Move each confirmed task under `## <Topic> (<Stage>)` in its H1 section,
  stripping the used `Priority:` line
- Remove the `# TO REORG` header once it has no tasks left

# References

- `.claude/skills/todo.rules.md`: defines the H1 stage / H2 topic / H3 task
  organization, the `## <Topic> (<Stage>)` header convention, and the `# ALL TOPICS`
  master list

# Workflow

## Load the Conventions

- Read `.claude/skills/todo.rules.md`
- Record the ordered `## <Topic>` headers in `ai_task_queue.md`'s `# ALL TOPICS`
  section. Ignore `// <group>` comment lines: they are visual grouping, not topics
- Record the H1 stage headers in the file (e.g. `# IN PROGRESS`,
  `# BACKLOG - HIGH PRIORITY`, `# BACKLOG`, `# ICEBOX`). These are the only valid
  move targets

## Find the Tasks to Reorg

- Find every H3 header under `# TO REORG`
- Capture each full task block: the header line through everything before the
  next H1/H2/H3 header

## Determine the Target H1 Stage

- Find a `- Priority: <Stage>` line anywhere in the task body
  - Match `<Stage>` case-insensitively to an existing H1 stage (e.g. `Icebox` ->
    `# ICEBOX`, `High Priority` -> `# BACKLOG - HIGH PRIORITY`, `Backlog` ->
    `# BACKLOG`, `In Progress` -> `# IN PROGRESS`)
  - If `<Stage>` does not clearly match an H1, do not guess. List the task and ask
    the user which H1 stage to use
- If there is no `- Priority:` line, propose `# BACKLOG` as the default. This is
  only a proposal and can be overridden at confirmation

## Determine the Target H2 Topic

- Match the task content against the `# ALL TOPICS` list, the same way
  `todo.move_done` infers a topic
- If no entry is a plausible match, do not guess. List the task and ask whether to
  use the closest existing topic or add a new one to `# ALL TOPICS`

## Propose the Moves

- Before changing anything, print one line per task in the form:

  ```
  ### <Title> -> ## <Topic> (<Stage>)
  ```

- Group the list by target `<Stage>` so the user can scan it stage by stage
- Flag any task whose stage came from the default (no `Priority:` tag). It is a
  guess, not a tag-driven placement
- Stop and wait for explicit confirmation of the whole list, or corrections, before
  any edit to `ai_task_queue.md`

## Execute the Moves

- Only after confirmation, for each approved task in source order:
  - Remove the `- Priority: <Stage>` line and the blank line it leaves. The tag only
    routes the task out of `# TO REORG` and is not part of the normal task format
  - If the H3 header has no `[ ]`, `[x]`, or `[.]` marker, rewrite it to
    `### [ ] <Title>`. Leave an existing marker unchanged
  - Cut the task block from `# TO REORG`, closing the resulting blank line gap
  - Append the task block under `## <Topic> (<Stage>)` in the confirmed H1 section
    - If that H2 does not exist under the target H1, create it at the end of the
      section
    - Keep tasks for the same topic together under one header

## Clean Up

- After all confirmed tasks move, if `# TO REORG` has no task content left, remove
  the `# TO REORG` header
- If some tasks stay unresolved (ambiguous stage or topic), keep `# TO REORG` with
  only those tasks

# Ask User

- Any task whose `Priority:` value or topic does not match confidently. Do not guess
- The full proposed move list, before any file edit

# Report

- List each executed move as `<Title>: TO REORG -> ## <Topic> (<Stage>)`
- List each task left in `# TO REORG` unresolved, and why
- State whether the `# TO REORG` header was removed or kept

# Verification

- [ ] No file edit happened before the user confirmed the proposed move list
- [ ] Every moved task sits under a `## <Topic> (<Stage>)` header whose bare topic
      also appears in `# ALL TOPICS`
- [ ] Every moved task's H1 section matches its confirmed target stage
- [ ] No `- Priority:` line remains in any moved task
- [ ] Every H3 task header carries a `[ ]`, `[x]`, or `[.]` marker after the move
- [ ] Task content (title, body) is unchanged, aside from the removed `Priority:`
      line and its position
- [ ] `# TO REORG` is removed if empty, or kept with only unresolved tasks
- [ ] `# ALL TOPICS` is unchanged except for topics explicitly added during this
      pass
