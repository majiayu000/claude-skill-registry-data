---
name: summarize-chat
disable-model-invocation: true
description: >-
  Summarize the current conversation into a structured markdown document for LLM handoff.
context: fork
background: false
---

# Chat History Summarizer

Produces a structured markdown summary a future LLM can read and act on without re-reading the
full conversation. Covers session goal, actions taken, decisions made, problems and solutions,
current file state, pending work, and key facts for the next session.

## Output Format

Only include sections that are relevant — omit empty ones.

```markdown
# Session Summary

**Date:** YYYY-MM-DD
**Branch / Repo:** <branch name and repo if known>

## Goal

One or two sentences: what was the user trying to accomplish?

## What Was Done

Ordered list of actions taken, first to last. One line per item.

- Action 1
- Action 2

## Decisions Made

Decisions that affect future work — naming, locations, approaches.

| Decision | Rationale |
| -------- | --------- |
| ...      | ...       |

## Problems and Solutions

Non-obvious issues and how they were resolved.

| Problem | Solution |
| ------- | -------- |
| ...     | ...      |

## Current State

What files were created, changed, or deleted?

- Created: `path/to/file` — purpose
- Modified: `path/to/file` — what changed
- Deleted: `path/to/file`

## Pending / Next Steps

Work discussed but not completed, or logical next actions.

- [ ] Item

## Key Facts for Next Session

Non-obvious facts a future LLM must know to avoid repeating mistakes or redundant questions.

- Fact 1
```

## Writing Rules

**Factual, not narrative.** State what was done. Avoid "we explored" or "the user wanted to".

**One fact per line.** Bullet points are easier to parse than paragraphs.

**Specific over general.** File paths, command names, and exact decisions over vague descriptions.

**Current State is the most important section.** List every file created, modified, or deleted.

**Key Facts is for gotchas.** If something caused a mistake or correction, it belongs here.

**Omit the obvious.** Skip routine tool use, standard git operations, and anything derivable
from reading the files directly.

Aim for minimum length that preserves full context. Readable in under 2 minutes by a human,
parseable in one pass by an LLM.
