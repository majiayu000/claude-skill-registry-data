---
name: working-with-gemini
description: Use when working with Gemini CLI or Antigravity CLI — extensions, skills, hooks, GEMINI.md, configuration, models, or any Gemini/Antigravity feature
metadata:
  last_updated: "2026-06-04"
---

# Working with Gemini CLI & Antigravity CLI

## Overview

This skill provides complete, authoritative documentation for Gemini CLI and its successor Antigravity CLI (launched June 2026). Instead of guessing about configuration paths, extension structures, or feature capabilities, read the official docs stored in this skill's references directory.

**Antigravity CLI** is Google's official next-generation replacement for Gemini CLI. It is backward-compatible: `GEMINI.md`, `AGENTS.md`, and `SKILL.md`-based skills all work without modification. The main breaking changes are the workspace skills path (`.gemini/skills/` → `.agents/skills/`) and the extension manifest filename (`gemini-extension.json` → `plugin.json`).

## When to Use

Use this skill when:
- Creating or configuring Gemini CLI extensions (or Antigravity plugins)
- Writing or testing skills for Gemini CLI / Antigravity
- Configuring `GEMINI.md` or `AGENTS.md` session context
- Understanding CLI commands and flags
- Configuring hooks for session events
- Setting up MCP servers in extensions
- Migrating from Gemini CLI to Antigravity CLI
- Troubleshooting Gemini or Antigravity issues
- Understanding model selection, context, or sandboxing

## Quick Reference

| Task | Read This File |
|------|---------------|
| Get started | `README.md` |
| CLI commands and flags | `docs-cli-reference.md` |
| Write a skill | `docs-creating-skills.md` |
| Skills overview and invocation | `docs-skills.md` |
| Skills best practices | `docs-skills-best-practices.md` |
| Skills getting started | `docs-skills-getting-started.md` |
| Using agent skills | `docs-using-agent-skills.md` |
| `activate_skill` tool | `docs-activate-skill.md` |
| Create an extension | `docs-writing-extensions.md` |
| Configure GEMINI.md | `docs-gemini-md.md` |
| Configure hooks | `docs-writing-hooks.md` |
| Set up MCP servers | `docs-mcp-server.md` or `docs-mcp-setup.md` |
| Configuration / settings | `docs-settings.md` or `docs-configuration.md` |
| Model selection / routing | `docs-model.md` or `docs-model-routing.md` |
| Sandboxing / security | `docs-sandbox.md` |
| Remote agents / subagents | `docs-subagents.md` or `docs-remote-agents.md` |
| Plan mode | `docs-plan-mode.md` |
| Memory / auto-memory | `docs-memory.md` or `docs-auto-memory.md` |
| Troubleshooting | `docs-troubleshooting.md` |
| FAQ | `docs-faq.md` |

## Documentation Organization

All documentation is stored as individual markdown files in `references/`. Use the Read tool to access specific documentation:

```
references/
├── README.md                        # Main Gemini CLI README — start here
├── GEMINI.md                        # Repo GEMINI.md (session context format example)
├── CONTRIBUTING.md                  # Contributing guide
├── docs-creating-skills.md          # Authoring SKILL.md files
├── docs-skills.md                   # Skills overview and invocation
├── docs-skills-best-practices.md    # Skill quality and trigger patterns
├── docs-skills-getting-started.md   # Skills quick start
├── docs-using-agent-skills.md       # Using agent skills
├── docs-activate-skill.md           # activate_skill tool reference
├── docs-gemini-md.md                # GEMINI.md format and best practices
├── docs-writing-extensions.md       # Extension (plugin) development guide
├── docs-writing-hooks.md            # Hook authoring guide
├── docs-cli-reference.md            # Full CLI command reference
├── docs-settings.md                 # Settings file reference
├── docs-configuration.md            # Configuration guide
├── docs-mcp-server.md               # MCP server tool reference
├── docs-mcp-setup.md                # MCP server setup guide
├── docs-model.md                    # Model selection
├── docs-model-routing.md            # Model routing configuration
├── docs-sandbox.md                  # Sandboxing and security
├── docs-subagents.md                # Subagent usage
├── docs-remote-agents.md            # Remote agent configuration
├── docs-plan-mode.md                # Plan mode guide
├── docs-memory.md                   # Memory tools reference
├── docs-auto-memory.md              # Auto-memory feature
├── docs-checkpointing.md            # Checkpointing / rewind
├── docs-troubleshooting.md          # Troubleshooting guide
└── docs-faq.md                      # Frequently asked questions
```

> Note: References are populated by the update script. Run `node scripts/update_docs.js` to refresh all files from the official GitHub repo. Use Grep to search across all files if a topic isn't at the expected path.

## Gemini CLI vs. Antigravity CLI — Key Differences

| Feature | Gemini CLI | Antigravity CLI |
| --- | --- | --- |
| Extension manifest | `gemini-extension.json` | `plugin.json` |
| Workspace skills path | `.gemini/skills/` | `.agents/skills/` |
| Global skills path | `~/.gemini/skills/` | `~/.gemini/antigravity-cli/skills/` |
| Skill invocation | `activate_skill("name")` | `activate_skill("name")` |
| GEMINI.md support | Yes | Yes (also AGENTS.md) |
| SKILL.md format | Identical to Claude Code | Identical to Claude Code |
| Import from Gemini CLI | N/A | `agy plugin import gemini` |

## Workflow

### For Specific Questions

1. Identify the relevant documentation file from the list above
2. Use Read tool to load: `@references/filename.md`
3. Find the answer in the official documentation

**Example:**
```
User: "How do I create a Gemini CLI extension?"
→ Read @references/docs-extensions.md
→ Follow the official extension creation steps
```

### For Uncertain Topics

Use Grep to search across all documentation:

```bash
pattern: "search term"
path: ~/.claude/skills/working-with-gemini/references/
```

## Updating Documentation

The skill includes `scripts/update_docs.js` to fetch the latest docs from the official GitHub repositories.

```bash
node ~/.claude/skills/working-with-gemini/scripts/update_docs.js
```

The script fetches from:
1. `github.com/google-gemini/gemini-cli` — official Gemini CLI docs
2. `github.com/google-gemini/gemini-skills` — official Gemini skills library (if available)

## Cross-Compatibility Note

Skills using the standard `SKILL.md` format work across Claude Code, Codex CLI, Gemini CLI, and Antigravity CLI without modification. The only differences are the invocation syntax per platform:

| Platform | Invocation |
| --- | --- |
| Claude Code | `Skill` tool |
| Codex CLI | `skill("name")` |
| Gemini CLI | `activate_skill("name")` |
| Antigravity CLI | `activate_skill("name")` |

## Red Flags

If you find yourself:
- Guessing about extension manifest fields → Read `docs-extensions.md`
- Unsure about skill discovery paths → Read `docs-skills.md`
- Confused about GEMINI.md vs AGENTS.md → Read `docs-gemini-md.md`
- Unsure about Antigravity migration steps → Read `docs-antigravity-migration.md`

**Always consult the official documentation before guessing.**
