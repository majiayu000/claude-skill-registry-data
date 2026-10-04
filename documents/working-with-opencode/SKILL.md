---
name: working-with-opencode
description: Use when working with OpenCode CLI, plugins, skills, hooks, configuration, or any OpenCode feature - provides comprehensive official documentation for all aspects of the OpenCode AI coding assistant
metadata:
  last_updated: "2026-06-04"
---

# Working with OpenCode

## Overview

This skill provides complete, authoritative documentation for OpenCode — a Go-based AI coding agent CLI with a TUI interface. Instead of guessing about configuration paths, plugin structures, or feature capabilities, read the official docs stored in this skill's references directory.

## When to Use

Use this skill when:
- Creating or configuring OpenCode plugins (npm packages using `@opencode-ai/plugin`)
- Writing or testing skills for OpenCode
- Configuring hooks or agents for OpenCode sessions
- Understanding OpenCode CLI commands and TUI shortcuts
- Troubleshooting OpenCode issues
- Setting up integrations (VS Code, GitHub Actions, MCP servers)
- Configuring model selection, providers, or session context
- Working with `opencode.json` and `AGENTS.md` session context

## Quick Reference

| Task | Read This File |
|------|----------------|
| Get started / install | `README.md` |
| Config schema (opencode.json) | `skill-customize-opencode.md` or `v2-config.md` |
| Session instructions / AGENTS.md | `v2-instructions.md` |
| Write a skill | `skill-customize-opencode.md` + `effect-SKILL.md` (example) |
| Custom commands examples | `command-commit.md`, `command-changelog.md`, etc. |
| Agent configuration | `AGENTS.md` + `agent-triage.md`, `agent-duplicate-pr.md` |
| Provider / model config | `v2-provider-model.md` |
| Plugin lifecycle | `v2-catalog-config-plugin-lifecycle.md` |
| Session internals | `v2-session.md` |
| Contributing | `CONTRIBUTING.md` |
| Context file format | `CONTEXT.md` |

## Documentation Organization

All documentation is stored as individual markdown files in `references/`. Use the Read tool to access specific documentation:

```
references/
├── README.md                         # Main OpenCode README — start here
├── AGENTS.md                         # Repo AGENTS.md — session bootstrap format example
├── CONTEXT.md                        # Context file format
├── skill-customize-opencode.md       # Skill + config docs (MOST USEFUL — start here)
├── v2-config.md                      # opencode.json config spec v2
├── v2-instructions.md                # Session instructions format
├── v2-provider-model.md              # Provider and model configuration
├── v2-provider-policy.md             # Provider policy configuration
├── v2-session.md                     # Session internals
├── v2-catalog-config-plugin-lifecycle.md  # Plugin lifecycle
├── effect-SKILL.md                   # Example SKILL.md from the repo
├── command-commit.md                 # Example custom command: commit
├── command-changelog.md              # Example custom command: changelog
├── command-issues.md                 # Example custom command: issues
├── agent-triage.md                   # Example agent: triage
├── agent-duplicate-pr.md             # Example agent: PR dedup
└── ...                               # Additional files fetched by update script
```

> Note: The references directory is populated by the update script. Run `node scripts/update_docs.js` to refresh all files from the GitHub repo.

## Workflow

### For Specific Questions

1. Identify the relevant documentation file from the list above
2. Use Read tool to load: `references/filename.md`
3. Find the answer in the official documentation
4. Apply the solution

**Example:**
```
User: "How do I create an OpenCode plugin?"
→ Read references/docs-plugins.md
→ Follow the official plugin creation steps
```

### For Broad Topics

When exploring a topic, start with the README, then drill into specific files:

- **Getting started**: `README.md` → `docs-installation.md`
- **Writing skills**: `docs-skills.md`
- **Plugin development**: `docs-plugins.md`
- **Configuration**: `docs-configuration.md`
- **MCP integration**: `docs-mcp.md`

### For Uncertain Topics

Use Grep tool to search across all documentation:

```bash
pattern: "search term"
path: ~/.agents/skills/working-with-opencode/references/
```

## Updating Documentation

The skill includes `scripts/update_docs.js` to fetch the latest documentation.

Run when:
- Documentation seems outdated
- New OpenCode features are released
- Official docs have been updated

```bash
node ~/.agents/skills/working-with-opencode/scripts/update_docs.js
```

The script:
1. Tries to fetch from `opencode.ai/llms.txt` to discover doc URLs
2. Falls back to the GitHub API (`github.com/opencode-ai/opencode`) to discover markdown files
3. Always fetches the main README from the GitHub repo
4. Downloads all found pages to `references/`
5. Reports success/failures

## Common Patterns

### Plugin Development

Read `docs-plugins.md` for overview, then `docs-skills.md` for writing skills and `docs-commands.md` for custom commands.

### Session Configuration

Read `docs-configuration.md` for `opencode.json` schema and `docs-instructions.md` for how session context (AGENTS.md) is loaded.

### MCP Integration

Read `docs-mcp.md` for configuring MCP servers in `opencode.json`.

## What This Skill Does NOT Do

- This skill provides **documentation access**, not procedural guidance
- For workflows on **how to build** plugins/skills, use the `developing-opencode-plugins` skill
- This skill is a **reference library**, not a tutorial

## Red Flags

If you find yourself:
- Guessing about CLI flags → Read `docs-cli.md`
- Speculating about plugin structure → Read `docs-plugins.md`
- Unsure about skill format → Read `docs-skills.md`
- Making assumptions about opencode.json format → Read `docs-configuration.md`
- Unsure about config options → Read `docs-configuration.md`

**Always consult the official documentation before guessing.**
