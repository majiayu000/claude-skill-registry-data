---
name: clean-claude-memory
description: Audit, prune, rewrite, or relocate Claude Code project memory. Use when the user asks to review, clean, update, or remove Claude memory files, eliminate stale project memories, or rebuild MEMORY.md.
disable-model-invocation: true
---

# Clean Claude Memory

Claude Code stores project-scoped durable notes outside the repository:

`~/.claude/projects/<encoded-absolute-project-path>/memory/`

`MEMORY.md` is the index. Other Markdown files are topic memories. Memory is a hint for future sessions, not an authoritative source; verify every claim against current code, docs, configuration, tools, and project state.

Treat recorded plans as historical artifacts only, not as documentation or a source of truth. Never use them to implement other features or as authoritative evidence about current behavior; verify relevant claims against current code, tests, configuration, requirements, and project documentation.

Do not include these unless the user explicitly expands the scope:

- repository `CLAUDE.md` or `AGENTS.md`;
- global `~/.claude/CLAUDE.md`;
- memories belonging to another project.

## Workflow

1. Resolve the current project's memory directory.
2. Read `MEMORY.md` and inventory every sibling memory file.
3. Review topic files one at a time. For each file:
   - read it completely;
   - explain what it preserves;
   - verify its claims against current authoritative sources;
   - identify stale facts, duplication, historical narration, and transient paths, versions, plans, or commands;
   - recommend one action;
   - ask the user one direct question and wait before reviewing the next file.

Use these actions:

| Action | Use when |
|---|---|
| Keep | Unique, durable intent or preference remains accurate and useful. |
| Rewrite | A valuable core remains, but the file contains stale or excessive detail. |
| Delete | The content is obvious, obsolete, historical, or already authoritative elsewhere. |
| Move | The information belongs in code, tests, docs, a backlog task, or a reusable skill. |

For `Move`, create and verify the new home before deleting the memory:

- code invariant or non-obvious trade-off → nearby comment or test;
- actionable future work → project task or issue;
- durable project contract → project documentation;
- reusable agent workflow → skill.

Do not copy stale claims into a new location merely to preserve them.

Unless the user explicitly asks otherwise, record decisions during the review and apply them after every topic file has been considered. This avoids leaving `MEMORY.md` with temporary broken links.

## Index

Process `MEMORY.md` last.

Rebuild it from the final directory state:

- link only to surviving topic files;
- use one short factual description per link;
- do not duplicate the child file's body;
- remove stale and broken links;
- if no topic files remain, ask whether `MEMORY.md` should be empty or removed.

## Validation

After applying the decisions:

- list the directory and confirm the exact expected files;
- verify every `MEMORY.md` link resolves;
- verify moved information exists in its new home;
- confirm unrelated global or project instructions were untouched;
- report what was kept, rewritten, moved, and deleted;
- state whether deletions are recoverable;
- validate any repository code or documentation changed during a move.

Memory files are outside the repository and may require separate write approval. Never commit unrelated repository changes without the user's instruction.
