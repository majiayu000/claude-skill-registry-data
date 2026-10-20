---
name: opencode-instructions-auditor
description: "Audit and improve CLAUDE.md files in repositories. Use when user asks to check, audit, update, improve, or fix CLAUDE.md files. Scans for all CLAUDE.md files, evaluates quality against templates, outputs quality report, then makes targeted updates. Also use when the user mentions \"CLAUDE.md maintenance\" or \"project memory optimization\"."
compatibility: opencode
---

# OpenCode Instructions Auditor

Audit and improve repository instructions used by OpenCode. Prefer `AGENTS.md` for durable project guidance and `.opencode/opencode.json` / `opencode.jsonc` plus `.opencode/agents/` and `.opencode/skills/` for supported configuration. Keep `CLAUDE.md` only when the repository intentionally supports Claude Code too.

## Workflow
1. Inventory `AGENTS.md`, nested instruction files, `.opencode/`, OpenCode config, skills, agents, commands, and project documentation.
2. Read the installed OpenCode version and matching official docs before changing version-sensitive syntax.
3. Identify duplicate, contradictory, stale, untestable, overly broad, or tool-specific instructions. Separate project facts from rules and guesses.
4. Preserve valid project decisions. Do not replace them with generic conventions or invent architecture.
5. Propose a concise change list with exact paths and expected effects. Ask before broad rewrites or deleting content.
6. After approval, make focused edits; validate frontmatter, JSON/JSONC syntax, relative links, script paths, and skill directory/name consistency.
7. Report changes, checks run, failures, and unresolved assumptions.

## Audit criteria
- Correct OpenCode paths and supported frontmatter/config keys
- Clear precedence and scope (global vs project vs nested directory)
- Explicit workflow: inspect → plan → execute → verify → report
- No unsupported Claude Code tool names or assumed hooks in OpenCode-only instructions
- Least privilege for tools, permissions, and MCP access
- Test/build commands grounded in repository documentation
- Instructions do not encourage destructive commands without confirmation and backup
