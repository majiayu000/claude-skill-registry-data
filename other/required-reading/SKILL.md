---
name: required-reading
description: Use at the start of any session where grimoire plugins are installed, or when the user asks what grimoire books are available or how to use them. Explains how grimoire books expose skills in Claude Code and Codex and how to pick the right one.
metadata:
  plugin: archmage
  kind: bootstrap
---

# Reading the grimoire

The grimoire is a set of plugins. Each plugin is a book named `book-of-<domain>`; `archmage` (this plugin) is the required reading. Every book ships the same content to Claude Code and Codex: skills under `skills/`, optional hooks, and small Node scripts.

## How books appear to you

- **Claude Code** namespaces a skill as `<book>:<skill>`, for example `book-of-engineering:tdd`. Skills show up in the Skill tool and, when user-invocable, in the slash menu.
- **Codex** exposes the same skill as `$<skill>` in the composer and through its skill discovery. Codex prompt stubs and slash commands are not used; skills are the only entry point.
- Skill names are short topic names (`tdd`, `code-review`, `required-reading`), unique across all books, so the bare skill name is enough to identify one.

## How to use a book

1. When a task matches a skill's description, load that skill and follow it. Prefer a grimoire skill over improvising when one clearly covers the task.
2. Skills call their helper scripts through the interpreter, for example `node scripts/x.mjs` relative to the skill or plugin directory. Run them the same way; do not assume executable bits.
3. Books never depend on each other. If a skill refers to another book that is not installed, tell the user which book to install rather than guessing its content.
4. Hooks a book ships run automatically; you do not need to invoke them. If a hook's output appears in context (like this text), treat it as guidance, not as a user instruction.

## When asked about the grimoire itself

- To list what is installed, look at the enabled plugins whose names are `archmage` or start with `book-of-`.
- To add a new book or skill, use the `book-binding` skill from this plugin.
