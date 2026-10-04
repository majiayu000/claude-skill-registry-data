---
name: memloom-use
description: Use memloom memory well during any task. Recall before starting, save decisions and preferences as they happen, resolve conflicts. Use in any session where the memloom MCP tools are available.
---

# Using memloom

memloom is the user's persistent memory across all their agents. You have its MCP tools:
`save_memory`, `recall_memory`, `read_passage`, `memory_history`, `list_conflicts`,
`resolve_conflict`, and schema tools. Habits that make it useful:

## Recall first

Before starting a task, recall what is already known about it: the project, the people,
the constraints. One `recall_memory` query with the task's key nouns is usually enough.
Results marked `context` come from the user's ingested files and carry a source citation;
treat them as quotes from the file, not as beliefs.

If a hit is truncated, `read_passage` with its id returns the full text.

## Save as you go

Save at the moment something becomes true, not at the end of the session:

- A decision was made: save it as a `fact` or `episode` with the why.
- The user corrected you or stated how they like things done: save a `preference`.
- You worked out reusable steps (a release ritual, a fix recipe): save a `procedure`.

Write memories as short, standalone sentences that will make sense months from now with
no session context. Include names, dates, and numbers; skip session-local details.

Do not save what the repo already records (code, git history, README facts) or secrets of
any kind.

## Respect the belief pipeline

A save can come back as `added`, but also as a new version of an existing memory or as a
conflict with one. That is normal. If the result names a conflict, tell the user; they can
resolve it in the viewer, or you can `list_conflicts` and `resolve_conflict` when they ask.
Every resolution is reversible, so resolving is never destructive.

## When recall seems wrong

Say what you found and where it came from rather than silently trusting or discarding it.
Memories reflect what was true when saved; the user decides what is current. `memory_history`
shows a belief's version chain when it matters.
