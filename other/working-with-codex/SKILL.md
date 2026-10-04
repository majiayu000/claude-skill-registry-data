---
name: working-with-codex
description: Use when working with Codex CLI, plugins, skills, hooks, configuration, or any Codex feature - provides comprehensive official documentation for all aspects of the OpenAI Codex CLI
metadata:
  last_updated: "2026-06-04"
---

# Working with Codex

## Overview

This skill provides complete, authoritative documentation for the OpenAI Codex CLI. Instead of guessing about configuration paths, plugin structures, or feature capabilities, read the official docs stored in this skill's references directory.

## When to Use

Use this skill when:
- Creating or configuring Codex plugins
- Writing or testing skills for Codex
- Configuring hooks for Codex sessions
- Understanding Codex CLI commands and flags
- Troubleshooting Codex issues
- Setting up integrations (VS Code, GitHub Actions, etc.)
- Configuring model selection, memory, or context
- Working with AGENTS.md and session context

## Quick Reference

| Task | Read This File |
|------|---------------|
| Get started | `README.md` or `docs-getting-started.md` |
| Install / update | `docs-install.md` or `references-installing-and-updating.md` |
| CLI commands and flags | `references-cli.md` |
| Write a skill | `docs-skills.md` |
| Configure AGENTS.md | `docs-agents_md.md` |
| Configure sessions / config.yaml | `docs-config.md` |
| Plugin JSON spec | `references-plugin-json-spec.md` |
| Slash commands | `docs-slash_commands.md` |
| Execution policy / sandbox | `docs-execpolicy.md` or `docs-sandbox.md` |
| Authentication | `docs-authentication.md` |
| MCP interface | `docs-codex_mcp_interface.md` |
| Prompting guidance | `references-prompting-guide.md` or `references-prompting.md` |
| FAQ | `docs-faq.md` |
| Changelog | `CHANGELOG.md` |
| Security | `SECURITY.md` |

## Documentation Organization

All documentation is stored as individual markdown files in `references/`. Use the Read tool to access specific documentation:

```
references/
├── README.md                        # Main Codex CLI README — start here
├── CHANGELOG.md                     # Release history
├── AGENTS.md                        # Repo AGENTS.md (session context format example)
├── docs-getting-started.md          # Getting started guide
├── docs-install.md                  # Installation instructions
├── docs-config.md                   # Configuration (config.yaml, env vars)
├── docs-agents_md.md                # AGENTS.md format and best practices
├── docs-skills.md                   # Skill authoring guide
├── docs-slash_commands.md           # Slash command reference
├── docs-exec.md                     # Execution model
├── docs-execpolicy.md               # Execution policy configuration
├── docs-sandbox.md                  # Sandbox and security isolation
├── docs-authentication.md           # Authentication setup
├── docs-api-reference.md            # API reference
├── docs-codex_mcp_interface.md      # MCP (Model Context Protocol) interface
├── docs-faq.md                      # Frequently asked questions
├── docs-contributing.md             # Contributing guide
├── references-cli.md                # CLI flags and command reference
├── references-plugin-json-spec.md   # Plugin manifest (plugin.json) specification
├── references-prompting-guide.md    # Prompting best practices
├── references-prompting.md          # Additional prompting reference
├── references-installing-and-updating.md  # Install and update instructions
├── references-upgrade-guide.md      # Migration / upgrade guide
├── references-latest-model.md       # Current default model info
├── config-schema.md                 # Config file JSON schema
└── SECURITY.md                      # Security policy
```

> Note: The references directory is populated by the update script. Run `node scripts/update_docs.js` to refresh all files from the GitHub repo.

## Workflow

### For Specific Questions

1. Identify the relevant documentation file from the list above
2. Use Read tool to load: `@references/filename.md`
3. Find the answer in the official documentation
4. Apply the solution

**Example:**
```
User: "How do I create a Codex plugin?"
→ Read @references/plugins.md
→ Follow the official plugin creation steps
```

### For Broad Topics

When exploring a topic, start with the README, then drill into specific files:

- **Getting started**: `README.md` → `docs-getting-started.md`
- **Writing skills**: `docs-skills.md`
- **Plugin development**: `references-plugin-json-spec.md`
- **Configuration**: `docs-config.md`
- **FAQ / troubleshooting**: `docs-faq.md`

### For Uncertain Topics

Use Grep tool to search across all documentation:

```bash
pattern: "search term"
path: ~/.claude/skills/working-with-codex/references/
```

## Updating Documentation

The skill includes `scripts/update_docs.js` to fetch the latest documentation.

Run when:
- Documentation seems outdated
- New Codex CLI features are released
- Official docs have been updated

```bash
node ~/.claude/skills/working-with-codex/scripts/update_docs.js
```

The script:
1. Tries to fetch from `platform.openai.com/llms.txt` and extract Codex CLI doc URLs
2. Falls back to the GitHub API (`github.com/openai/codex`) to discover markdown files
3. Always fetches the main README from the GitHub repo
4. Downloads all found pages to `references/`
5. Reports success/failures

## Common Patterns

### Plugin Development

Read `plugins.md` for overview, then `skills.md` for writing skills and `hooks.md` for hooks.

### AGENTS.md Configuration

Read `configuration.md` for how AGENTS.md bootstraps Codex sessions.

### CI/CD Integration

Read `github-actions.md` for GitHub Actions configuration.

## What This Skill Does NOT Do

- This skill provides **documentation access**, not procedural guidance
- For workflows on **how to build** plugins/skills, use the `developing-codex-plugins` skill
- This skill is a **reference library**, not a tutorial

## Red Flags

If you find yourself:
- Guessing about CLI flags → Read `references-cli.md`
- Speculating about plugin structure → Read `references-plugin-json-spec.md`
- Unsure about skill format → Read `docs-skills.md`
- Making assumptions about AGENTS.md format → Read `docs-agents_md.md`
- Unsure about config options → Read `docs-config.md`

**Always consult the official documentation before guessing.**
