---
name: working-with-cursor
description: Use when working with Cursor IDE, rules (.cursor/rules/*.mdc), skills, plugins, MCP servers, agents, commands, hooks, configuration, or any Cursor IDE feature - provides comprehensive official documentation for all aspects of Cursor
metadata:
  last_updated: "2026-06-05"
---

# Working with Cursor

## Overview

This skill provides complete, authoritative documentation for Cursor IDE directly from cursor.com. Instead of guessing about rule formats, plugin structures, MCP configuration, or feature capabilities, read the official docs stored in this skill's references directory.

## When to Use

Use this skill when:
- Writing or debugging `.cursor/rules/*.mdc` files
- Creating or configuring Cursor plugins
- Setting up MCP servers in Cursor
- Writing or testing Cursor skills
- Configuring Cursor agents or commands
- Setting up hooks for Cursor events
- Understanding Cursor AI modes (Agent, Ask, Plan, Debug)
- Using `@`-mention context injection
- Configuring Cursor settings or extensions
- Troubleshooting Cursor issues

## Quick Reference

| Task | Read This File |
|------|---------------|
| Write or debug rules | `rules.md` |
| Set up MCP servers | `mcp.md` |
| Create a plugin | `plugins.md` |
| Write a skill | `skills.md` |
| Configure hooks | `hooks.md` |
| Configure subagents | `subagents.md` |
| Agent mode overview | `agent-overview.md` |
| CLI usage | `cli-overview.md` |
| CLI slash commands | `cli-reference-slash-commands.md` |
| CLI auth | `cli-reference-authentication.md` |
| GitHub integration | `integrations-github.md` |
| BugBot | `bugbot.md` |
| Cloud agent | `cloud-agent.md` |
| Security | `security-agents.md` |
| Models & pricing | `models-and-pricing.md` |
| Get started | `get-started-quickstart.md` |

## Documentation Organization

All documentation is stored as individual markdown files in `references/`. Use the Read tool to access specific documentation:

```
references/
├── rules.md                       # Rules (.mdc format, activation modes, globs)
├── skills.md                      # Skill authoring guide
├── plugins.md                     # Plugin development
├── mcp.md                         # Model Context Protocol integration
├── subagents.md                   # Subagent configurations
├── hooks.md                       # Event hooks
├── agent-overview.md              # Agent mode overview
├── agent-plan-mode.md             # Plan mode
├── agent-agents-window.md         # Agents window UI
├── agent-tools-terminal.md        # Terminal tool
├── agent-tools-search.md          # Search tool
├── agent-tools-canvas.md          # Canvas tool
├── cli-overview.md                # CLI reference
├── cli-reference-slash-commands.md # Slash commands
├── cli-reference-authentication.md # Auth
├── cli-reference-configuration.md  # Config
├── cloud-agent.md                 # Cloud agent overview
├── cloud-agent-setup.md           # Cloud agent setup
├── cloud-agent-best-practices.md  # Cloud agent best practices
├── integrations-github.md         # GitHub integration
├── security-agents.md             # Security
├── models-and-pricing.md          # Model selection and pricing
├── get-started-quickstart.md      # Quickstart guide
└── ...                            # Additional docs (teams, enterprise, SDK)
```

## Key Concepts

**Rules vs Skills vs Plugins**
- **Rules** (`.cursor/rules/*.mdc`) — persistent AI guidance injected into context; team-shareable via git
- **Skills** — reusable multi-step capabilities invoked by the agent
- **Plugins** — distributable packages bundling rules, skills, commands, MCP servers, and hooks together

**Rule Activation Modes**
- `alwaysApply: true` — loaded in every request (keep under 200 words)
- `globs` set — auto-attached when matching files are in context
- `description` set, no globs — agent decides when to apply based on description
- Neither — manual invocation only (`@rule-name` in chat)

**MCP in Cursor**
Cursor supports MCP tools, prompts, and roots. Configure globally in `~/.cursor/mcp.json` or per-project in `.cursor/mcp.json`. Cursor supports up to 40 MCP tools at a time.

## Cross-References

For **plugin development workflows**, use the `developing-cursor-plugins` skill.
