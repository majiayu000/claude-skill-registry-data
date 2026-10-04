---
name: multi-provider-plugins
description: Use when making a Claude Code plugin compatible with other AI coding assistants (Codex, OpenCode, Cursor, Gemini CLI), designing multi-provider plugin architecture, adding a provider adapter, or structuring a portable shared skills library
metadata:
  last_updated: "2026-06-04"
---

# Multi-Provider Plugins

Route to the reference that matches your task.

## Task → Reference

| Task | Read |
|------|------|
| Understand the shared-skills + thin-adapter architecture | `references/architecture-overview.md` |
| Add or configure a provider-specific adapter (Claude Code, Codex, OpenCode, Cursor, Gemini) | `references/provider-adapters.md` |
| Map tool names across providers in skill content | `references/tool-mapping.md` |
| Implement session-start bootstrap injection for a provider | `references/bootstrap-patterns.md` |
| Structure or audit a portable shared skills library | `references/shared-skills-library.md` |

## Instruction File Conventions (CLAUDE.md / AGENTS.md)

**Non-obvious and commonly wrong** — apply whenever creating a new project or touching either file:

- **Claude Code** reads `CLAUDE.md`. Supports `@filename` import syntax (e.g. `@AGENTS.md` inlines it).
- **Codex CLI** reads `AGENTS.md` as plain Markdown — **no `@import` or include syntax exists**. `@CLAUDE.md` in AGENTS.md is a broken line, not an import.
- **Best pattern:** Write everything in `AGENTS.md`. Make `CLAUDE.md` contain only `@AGENTS.md`. All tools read AGENTS.md directly; Claude Code imports it inline via the `@` syntax.
- **Codex plugins:** `codex plugin marketplace add/upgrade/remove` only — no `install` subcommand.

## Universal Principles

1. **One `skills/` directory, many adapters.** Skills live once; provider adapters point to them. Never duplicate skill content per provider.

2. **Adapters are thin.** A provider adapter does the minimum: declare the plugin, point at `skills/`, and inject a bootstrap if the provider needs it. No business logic in adapters.

3. **Skills are portable markdown.** SKILL.md frontmatter format is identical across providers. Use clearly-labeled `### Claude Code` / `### Codex` subsections within skill bodies when tool names differ — don't branch in frontmatter.

4. **Bootstrap injection is a last resort.** Claude Code discovers skills natively. Only write bootstrap code when a provider lacks native skill discovery.

5. **Reference implementation.** [obra/superpowers](https://github.com/obra/superpowers) is the canonical example of this architecture running across Claude Code, Codex, OpenCode, Cursor, and Gemini CLI.
