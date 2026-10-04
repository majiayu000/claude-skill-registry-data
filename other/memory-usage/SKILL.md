---
name: memory-usage
description: >
  Use when reading or writing persistent project memory before, during, or after non-trivial work.
---

## Required `<project-root>/docs` reads

Read these project-root spec files before reading or writing persistent project memory (use shell `cat`/`ls` — they may be in `.gitignore`, invisible to built-in search). Missing file → fall back to native tools, note the gap; never invent contents.

- `<project-root>/docs/memory-providers.md`

Persistent memory holds facts that are expensive to re-derive and survive across sessions.

## When to Use Memory

### Read before acting

| Trigger | Action |
| --- | --- |
| Starting a non-trivial task | List memories, then read the relevant ones. |
| Unfamiliar error, pattern, or convention | Search memories for a matching topic or pitfall. |
| User asks "how do we do X here?" | Read the related memory first. |

### Write after learning

| Trigger | Action |
| --- | --- |
| Non-obvious invariant or convention | Write it under a topic-specific name. |
| Tricky pitfall that required real investigation | Write it under a `pitfalls/` path. |
| Architectural decision with lasting rationale | Write it under a `decisions/` path. |
| User explicitly asks to remember something | Write it with the requested name. |

### Do NOT write

- Conversation state, task progress, or session scratchpads.
- Facts trivially recoverable from code, tests, or docs in seconds.
- Transient data (current branch, in-flight PR numbers, today's ticket ID).
- Duplicates of an existing memory. Edit the existing one instead.

## Core Rules

- Read before non-trivial work. Write only reusable knowledge: architecture, conventions, pitfalls, decisions.
- Never duplicate codebase-readable truth. If a quick `grep` or `read` recovers it, leave it in code.
- Keep memories structured with headings, bullets, and tables. Split entries past ~100 lines.
- Use stable slash-separated topic paths (e.g., `modules/placements/lifecycle`, not `placements_info`).
- Cross-reference with `mem:<name>`.
- Maintain actively: edit stale memories, delete obsolete ones, prefer editing over delete-and-recreate.

## Memory Naming Conventions

Use slash-separated topic paths. Be specific, not generic.

- `project_overview` — high-level project shape and constraints.
- `modules/<name>` — module-specific facts, architecture, or relationships.
- `modules/<name>/<subtopic>` — narrow subtopics (e.g., lifecycle, repositories).
- `pitfalls/<topic>` — non-obvious traps and how to avoid them.
- `decisions/<topic>` — architectural decisions and their rationale.
- `global/<topic>` — cross-project knowledge only if it truly applies everywhere.

## Generic Memory Operations

All memory drivers expose roughly the same lifecycle (see `<project-root>/docs/memory-providers.md` in the project root for exact tool names and arguments).

| Operation | Purpose |
| --- | --- |
| List | See what memories exist, optionally filtered by topic. |
| Read | Load a specific memory into context. |
| Write | Create a new memory entry. |
| Edit | Update an existing memory while keeping its name stable. |
| Delete | Remove obsolete or wrong memories. |
| Rename | Fix a memory name without breaking references. |
| Activate project | Scope the driver to the correct project before any memory call. |

## Project Activation

Many memory drivers require an active project before listing or reading. Verify the active project before memory operations. If the driver reports no active project, activate the correct one.

- Cite, don't paste: reference memories by `mem:<name>`, never paste the body.

- Read only memories you will use. Infer relevance from the name; avoid dumping every memory into context "just in case."

