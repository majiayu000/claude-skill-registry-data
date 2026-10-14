---
name: craft-memory
description: Crafting effective CLAUDE.md files. Project memory that Claude won't ignore.
user-invocable: false
---

# Skill: Craft Memory

> "Would removing this line cause Claude to make mistakes? If not, cut it." — Anthropic

## Source of Truth

- https://code.claude.com/docs/en/memory
- https://code.claude.com/docs/en/best-practices

Read these first. Every time. The spec evolves.

---

## The Hierarchy

| Level        | Location                                                                                                                                              | Purpose     |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| Organization | macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`<br>Linux: `/etc/claude-code/CLAUDE.md`<br>Windows: `C:\Program Files\ClaudeCode\CLAUDE.md` | Constraints |
| User         | `~/.claude/CLAUDE.md`                                                                                                                                 | Preferences |
| Project      | `./CLAUDE.md` or `.claude/CLAUDE.md`                                                                                                                  | Context     |
| Local        | `./CLAUDE.local.md` (auto-gitignored)                                                                                                                 | Personal    |
| Rules        | `.claude/rules/*.md`                                                                                                                                  | Modular     |

Higher levels load first and take precedence.

---

## The Rules

### 1. Under 150 Lines

Bloated files get ignored. If Claude violates a rule you wrote, the file is too long.

### 2. Specific Over Vague

| Wrong                 | Right                        |
|-----------------------|------------------------------|
| Format code properly  | Use 2-space indentation      |
| Write good tests      | Tests must cover error paths |
| Follow best practices | Validate input with Zod      |

### 3. Include What Claude Can't Infer

| Include                               | Exclude                            |
|---------------------------------------|------------------------------------|
| Commands Claude can't guess           | Anything in package.json           |
| Style rules that differ from defaults | Standard language conventions      |
| Testing instructions                  | Detailed API docs (import instead) |
| Branch/PR conventions                 | Frequently changing info           |
| Architectural decisions               | File-by-file descriptions          |
| Environment quirks                    | "Write clean code"                 |
| Common gotchas                        | Tutorials                          |

## Deeper

| | |
|---|---|
| [mechanism](mechanism.md) | imports, path scoping, and how nesting loads |
| [protocol](protocol.md) | discover, interview, generate, split |
| [good](good.md) | two files that work, whole |
| [scoping](scoping.md) | a monorepo, and what imports compose |
| [bad](bad.md) | files that get ignored, and why |

## Anti-Patterns

| Pattern             | Why It Fails             |
|---------------------|--------------------------|
| Duplicate README    | Wastes tokens, drifts    |
| Giant monorepo file | No conditional loading   |
| Skip `/memory`      | Duplicate existing rules |

