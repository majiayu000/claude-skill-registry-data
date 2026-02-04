---
name: llm-context
description: Guidelines for working with LLM context stored in the .llm/ directory.
---

# LLM Context Guidelines

Extra context for LLMs may be stored in the `.llm/` directory at the root of a git repository.

## Directory Structure

- If `.llm/` exists, it will be at the root directory of the git repository
- The `.llm/` should not be tracked in version control
- If `.llm/` appears to contain untracked content, ensure that it appears in `.git/info/exclude`

## Editable Context

- If `.llm/todo.md` exists, it is the task list we are working on
- The `@markdown-tasks:tasks` skill will handle task completion
- As we work on an implementation, plans will change
  - Feel free to edit the task list to keep it relevant and in sync with our plans

## Read-only Context

- Everything else in the `.llm/` directory is read-only context for your reference
- It may contain entire git clones for tools we use
- It may contain saved documentation
