---
name: settings-management
description: Central authority for Claude Code configuration and settings. Covers settings.json files (user, project, enterprise), available settings, permission settings, sandbox settings, settings precedence, plugin configuration, environment variables, and tools available to Claude. Assists with configuring Claude Code behavior, managing permissions, setting up enterprise policies, and troubleshooting configuration issues. Delegates 100% to docs-management skill for official documentation.
allowed-tools: Read, Glob, Grep, Skill
---

# Configuration Meta Skill

## 🚨 MANDATORY: Invoke docs-management First

> **STOP - Before providing ANY response about Claude Code configuration or settings:**
>
> 1. **INVOKE** `docs-management` skill
> 2. **QUERY** for the user's specific topic
> 3. **BASE** all responses EXCLUSIVELY on official documentation loaded
>
> **Skipping this step results in outdated or incorrect information.**

### Verification Checkpoint

Before responding, verify:

- [ ] Did I invoke docs-management skill?
- [ ] Did official documentation load?
- [ ] Is my response based EXCLUSIVELY on official docs?

If ANY checkbox is unchecked, STOP and invoke docs-management first.

---

## Overview

Central authority for Claude Code configuration and settings. This skill uses **100% delegation to docs-management** - it contains NO duplicated official documentation.

**Architecture:** Pure delegation with keyword registry. All official documentation is accessed via docs-management skill queries.

## When to Use This Skill

**Keywords:** settings, configuration, settings.json, environment variables, permissions, sandbox, enterprise settings, managed-settings.json, user settings, project settings, local settings, tools, hooks configuration, model configuration, plugin settings, precedence

**Use this skill when:**

- Configuring settings.json files
- Understanding settings hierarchy and precedence
- Setting up permission rules (allow, deny, ask)
- Configuring sandbox settings
- Managing enterprise policies
- Setting environment variables
- Understanding available tools
- Configuring plugin settings
- Troubleshooting configuration issues

## Keyword Registry for docs-management Queries

Use these keywords when querying docs-management skill for official documentation:

### Settings Files

| Topic | Keywords |
| --- | --- |
| Overview | "settings", "settings.json", "configuration files" |
| User Settings | "user settings", "~/.claude/settings.json" |
| Project Settings | ".claude/settings.json", "project settings" |
| Local Settings | "settings.local.json", "local settings" |
| Enterprise | "managed-settings.json", "enterprise managed policy" |

### Available Settings

| Topic | Keywords |
| --- | --- |
| Settings Table | "available settings", "settings options" |
| Model Setting | "model setting", "model override" |
| Hooks Setting | "hooks setting", "disableAllHooks" |
| Output Style | "outputStyle setting", "output style config" |
| Status Line | "statusLine setting", "status line config" |
| API Key Helper | "apiKeyHelper", "custom script auth" |

### Permissions

| Topic | Keywords |
| --- | --- |
| Permission Settings | "permission settings", "allow deny ask rules" |
| Allow Rules | "permissions allow", "allow tool rules" |
| Deny Rules | "permissions deny", "deny tool rules", "excluding sensitive files" |
| Ask Rules | "permissions ask", "confirmation rules" |
| Default Mode | "defaultMode", "permission modes" |

### Sandbox

| Topic | Keywords |
| --- | --- |
| Sandbox Settings | "sandbox settings", "bash sandboxing" |
| Sandbox Network | "sandbox network", "allowUnixSockets", "allowLocalBinding" |
| Excluded Commands | "excludedCommands", "sandbox exclusions" |
| Auto Allow | "autoAllowBashIfSandboxed", "auto-approve sandboxed" |

### Precedence

| Topic | Keywords |
| --- | --- |
| Settings Precedence | "settings precedence", "configuration hierarchy" |
| Override Order | "enterprise project user precedence", "settings override" |

### Environment Variables

| Topic | Keywords |
| --- | --- |
| Environment Variables | "environment variables", "ANTHROPIC_API_KEY" |
| Model Variables | "ANTHROPIC_MODEL", "model environment" |
| Proxy Variables | "HTTP_PROXY", "HTTPS_PROXY", "proxy configuration" |
| Telemetry Variables | "DISABLE_TELEMETRY", "telemetry settings" |
| Bedrock Variables | "CLAUDE_CODE_USE_BEDROCK", "bedrock environment" |
| Vertex Variables | "CLAUDE_CODE_USE_VERTEX", "vertex environment" |

### Plugins

| Topic | Keywords |
| --- | --- |
| Plugin Configuration | "plugin configuration", "enabledPlugins" |
| Marketplaces | "extraKnownMarketplaces", "plugin marketplaces config" |

### Tools

| Topic | Keywords |
| --- | --- |
| Available Tools | "tools available to Claude", "tool table" |
| Tool Permissions | "tool permissions", "permission required tools" |

## Quick Decision Tree

**What do you want to do?**

1. **Configure settings file** -> Query docs-management: "settings.json", "available settings"
2. **Set up permissions** -> Query docs-management: "permission settings", "allow deny rules"
3. **Configure sandbox** -> Query docs-management: "sandbox settings", "bash sandboxing"
4. **Understand precedence** -> Query docs-management: "settings precedence", "configuration hierarchy"
5. **Set environment variables** -> Query docs-management: "environment variables", specific variable name
6. **Configure enterprise policy** -> Query docs-management: "managed-settings.json", "enterprise managed policy"
7. **Set up plugin settings** -> Query docs-management: "plugin configuration", "enabledPlugins"
8. **Understand available tools** -> Query docs-management: "tools available to Claude"
9. **Exclude sensitive files** -> Query docs-management: "excluding sensitive files", "deny rules"
10. **Configure model** -> Query docs-management: "model setting", "ANTHROPIC_MODEL"
11. **Troubleshoot config issues** -> Query docs-management: "configuration troubleshooting" + specific issue

## Topic Coverage

### Settings File Types

- User settings (~/.claude/settings.json)
- Project settings (.claude/settings.json)
- Local settings (.claude/settings.local.json)
- Enterprise policies (managed-settings.json)
- Platform-specific paths (macOS, Linux, Windows)

### Key Settings Options

- apiKeyHelper: Custom auth script
- cleanupPeriodDays: Transcript retention
- companyAnnouncements: Startup messages
- env: Environment variables
- includeCoAuthoredBy: Git commit attribution
- permissions: Tool access rules
- hooks: Custom tool event handlers
- model: Model selection override
- statusLine: Status display configuration
- outputStyle: Output format configuration
- forceLoginMethod: Authentication restrictions

### Permission Settings

- allow: Auto-approve tool patterns
- ask: Require confirmation patterns
- deny: Block tool patterns
- additionalDirectories: Extended file access
- defaultMode: Initial permission mode
- disableBypassPermissionsMode: Prevent bypass

### Sandbox Settings

- enabled: Bash sandboxing toggle
- autoAllowBashIfSandboxed: Auto-approve sandboxed commands
- excludedCommands: Commands outside sandbox
- allowUnsandboxedCommands: Escape hatch control
- network.allowUnixSockets: Socket access
- network.allowLocalBinding: Localhost binding
- network.httpProxyPort: HTTP proxy
- network.socksProxyPort: SOCKS5 proxy

### Settings Precedence

- Enterprise managed policies (highest)
- Command line arguments
- Local project settings
- Shared project settings
- User settings (lowest)

### Environment Variable Categories

- Authentication (ANTHROPIC_API_KEY, tokens)
- Model configuration (ANTHROPIC_MODEL, etc.)
- Provider settings (Bedrock, Vertex, Foundry)
- Proxy configuration (HTTP_PROXY, HTTPS_PROXY)
- Telemetry and updates (DISABLE_TELEMETRY, etc.)
- Tool behavior (BASH_DEFAULT_TIMEOUT_MS, etc.)

### Plugin Configuration

- enabledPlugins: Plugin enable/disable map
- extraKnownMarketplaces: Additional marketplace sources
- Marketplace source types (github, git, directory)

### Tools Available to Claude

- File operations (Read, Write, Edit, Glob, Grep)
- Execution (Bash, BashOutput, KillShell)
- User interaction (AskUserQuestion, TodoWrite)
- Specialized (Task, Skill, SlashCommand, WebFetch, WebSearch)
- Notebook (NotebookEdit)

## Delegation Patterns

### Standard Query Pattern

```text
User asks: "How do I configure permissions?"

1. Invoke docs-management skill
2. Use keywords: "permission settings", "allow deny rules"
3. Load official documentation
4. Provide guidance based EXCLUSIVELY on official docs
```

### Multi-Topic Query Pattern

```text
User asks: "I want enterprise settings with sandbox and restricted permissions"

1. Invoke docs-management skill with multiple queries:
   - "managed-settings.json", "enterprise managed policy"
   - "sandbox settings", "bash sandboxing"
   - "permission settings", "deny rules"
2. Synthesize guidance from official documentation
```

### Troubleshooting Pattern

```text
User reports: "My settings aren't taking effect"

1. Invoke docs-management skill
2. Use keywords: "settings precedence", "configuration hierarchy"
3. Guide user through precedence rules from official docs
```

## Troubleshooting Quick Reference

| Issue | Keywords for docs-management |
| --- | --- |
| Settings not applied | "settings precedence", "configuration hierarchy" |
| Permission denied | "permission settings", "deny rules" |
| Sandbox blocking commands | "sandbox settings", "excludedCommands" |
| Environment variable not working | "environment variables", specific variable name |
| Enterprise policy override | "managed-settings.json", "enterprise policy" |
| Plugin not loading | "plugin configuration", "enabledPlugins" |
| Tool not available | "tools available", "tool permissions" |

## Repository-Specific Notes

This repository has project-level settings in `.claude/settings.json` including:

- Custom hooks configuration
- Permission rules
- Model settings

When modifying this repository's settings, ensure changes align with the hook-management skill guidance for hook configurations.

## Auditing Settings

This skill provides the validation criteria used by the `settings-auditor` agent for formal audits.

### Audit Resources

| Resource | Location | Purpose |
| --- | --- | --- |
| Audit Framework | `references/audit-framework.md` | Query guides and scoring criteria |

### Scoring Categories

| Category | Points | Key Criteria |
| --- | --- | --- |
| JSON Validity | 20 | Valid syntax, well-formed |
| Schema Compliance | 25 | Only valid settings options |
| Permission Rules | 25 | Valid patterns, appropriate restrictions |
| Environment Config | 15 | Valid env vars, no secrets |
| Precedence Awareness | 15 | Correct scope usage |

**Thresholds:** 85+ = PASS, 70-84 = PASS WITH WARNINGS, <70 = FAIL

### Related Agent

The `settings-auditor` agent (Haiku model) performs formal audits using this skill:

- Auto-loads this skill via `skills: settings-management`
- Uses audit framework and docs-management for rules
- Generates structured audit reports
- Invoked by `/audit-settings` command

### External Technology Validation

When auditing settings that reference external technologies (scripts, packages, runtimes), the auditor MUST validate claims using MCP servers before flagging findings.

**Technologies Requiring MCP Validation:**

- .NET/C# scripts: Validate with microsoft-learn + perplexity
- Node.js/npm packages: Validate with context7 + perplexity
- Python scripts/packages: Validate with context7 + perplexity
- Shell scripts: Validate with perplexity
- Any version-specific claims: ALWAYS validate with perplexity

**Validation Rule:**

Never flag a technology usage as incorrect without first:

1. Querying appropriate MCP server(s) for current documentation
2. Verifying with perplexity for recent changes (especially .NET 10+)
3. Documenting MCP sources in the finding

**Stale Data Warning:**

- microsoft-learn can return cached/outdated documentation
- ALWAYS pair microsoft-learn with perplexity for version verification
- Trust perplexity for version numbers and recently-released features

## References

**Official Documentation (via docs-management skill):**

- Primary: "settings" documentation
- Related: "iam", "hooks", "sandboxing", "model-config", "network-config"

**Repository-Specific:**

- Project settings: `.claude/settings.json`
- Hooks configuration: `.claude/hooks/`

## Version History

- **v1.0.0** (2025-11-26): Initial release
  - Pure delegation architecture
  - Comprehensive keyword registry
  - Quick decision tree
  - Topic coverage for all configuration features
  - Troubleshooting quick reference

---

## Last Updated

**Date:** 2025-11-28
**Model:** claude-opus-4-5-20251101
