---
name: policy-engine-builder
description: Guide for creating Gemini CLI policy engine TOML rules. Covers rule syntax, priority tiers, conditions, and MCP wildcards. Use when restricting Gemini tools, creating security policies, controlling MCP server permissions, or setting up approval workflows.
allowed-tools: Read, Glob, Grep, Skill
---

# Policy Engine Builder

## 🚨 MANDATORY: Invoke gemini-cli-docs First

> **STOP - Before providing ANY response about Gemini policy engine:**
>
> 1. **INVOKE** `gemini-cli-docs` skill
> 2. **QUERY** for the specific policy topic
> 3. **BASE** all responses EXCLUSIVELY on official documentation loaded

## Overview

This skill provides guidance for configuring Gemini CLI's Policy Engine using TOML rules. The policy engine controls tool execution with fine-grained allow/deny/ask rules.

## When to Use This Skill

**Keywords:** policy engine, policy toml, tool policy, allow deny, gemini rules, security policy, mcp policy

**Use this skill when:**

- Restricting which tools Gemini can use
- Creating enterprise security policies
- Controlling MCP server permissions
- Setting up approval workflows
- Auditing tool execution rules

## Policy File Locations

### User Policies

```text
~/.gemini/policies/
├── default.toml          # User default rules
└── security.toml         # Additional security rules
```

### Project Policies

```text
.gemini/policies/
├── project.toml          # Project-specific rules
└── team.toml             # Team conventions
```

### System Policies (Enterprise)

```text
/etc/gemini-cli/policies/         # Linux
/Library/Application Support/GeminiCli/policies/  # macOS
C:\ProgramData\gemini-cli\policies\               # Windows
```

## Rule Structure

### Basic Rule

```toml
[[rule]]
toolName = "run_shell_command"
decision = "ask_user"
priority = 100
```

### Rule Fields

| Field | Type | Description |
| --- | --- | --- |
| `toolName` | string/array | Tool name(s) to match |
| `mcpName` | string | MCP server name |
| `argsPattern` | string | Regex for tool arguments |
| `commandPrefix` | string/array | Shell command prefix(es) |
| `commandRegex` | string | Regex for shell commands |
| `decision` | string | `allow`, `deny`, or `ask_user` |
| `priority` | number | 0-999 within tier |
| `modes` | array | Optional: `yolo`, `autoEdit` |

## Decision Types

### Allow

Automatically approve without prompting:

```toml
[[rule]]
toolName = "read_file"
decision = "allow"
priority = 100
```

### Deny

Block execution entirely:

```toml
[[rule]]
toolName = "run_shell_command"
commandPrefix = "rm -rf"
decision = "deny"
priority = 999
```

### Ask User

Prompt for confirmation:

```toml
[[rule]]
toolName = "write_file"
decision = "ask_user"
priority = 100
```

## Priority System

### Three Tiers

| Tier | Base | Source |
| --- | --- | --- |
| Default | 1 | Built-in defaults |
| User | 2 | User policies |
| Admin | 3 | System/enterprise |

### Priority Calculation

The formula is: `final_priority = tier_base + (toml_priority / 1000)`

Example:

- User rule with priority 100 → 2 + (100/1000) = 2.100
- Admin rule with priority 50 → 3 + (50/1000) = 3.050

**Higher tier always wins**, then higher priority within tier.

### Priority Guidelines

| Priority | Use Case |
| --- | --- |
| 0-99 | Low priority defaults |
| 100-499 | Normal rules |
| 500-799 | Important restrictions |
| 800-999 | Critical security rules |

## Tool Matching

### Single Tool

```toml
[[rule]]
toolName = "run_shell_command"
decision = "ask_user"
```

### Multiple Tools

```toml
[[rule]]
toolName = ["write_file", "replace"]
decision = "ask_user"
```

### All Tools

```toml
[[rule]]
toolName = "*"
decision = "ask_user"
```

## Shell Command Patterns

### Command Prefix

```toml
# Match commands starting with "git"
[[rule]]
toolName = "run_shell_command"
commandPrefix = "git "
decision = "allow"
priority = 100
```

### Multiple Prefixes

```toml
[[rule]]
toolName = "run_shell_command"
commandPrefix = ["npm ", "yarn ", "pnpm "]
decision = "allow"
priority = 100
```

### Command Regex

```toml
# Match destructive commands
[[rule]]
toolName = "run_shell_command"
commandRegex = "^(rm|rmdir|del|rd)\\s"
decision = "deny"
priority = 999
```

## Argument Patterns

### JSON Argument Matching

Tool arguments are JSON strings:

```toml
# Deny writes to sensitive paths
[[rule]]
toolName = "write_file"
argsPattern = ".*\\.(env|key|pem|crt)$"
decision = "deny"
priority = 900
```

### Complex Patterns

```toml
# Allow reads only from src/
[[rule]]
toolName = "read_file"
argsPattern = "^\\{\"path\":\"src/.*\"\\}$"
decision = "allow"
priority = 100
```

## MCP Server Rules

### Server-Level Control

```toml
# Deny all tools from untrusted server
[[rule]]
mcpName = "untrusted-server"
decision = "deny"
priority = 500
```

### Tool-Level Control

```toml
# Allow specific tool from server
[[rule]]
mcpName = "my-server"
toolName = "safe_tool"
decision = "allow"
priority = 100
```

### Wildcards

```toml
# All tools from server pattern
[[rule]]
toolName = "my-server__*"
decision = "ask_user"
priority = 100
```

## Approval Modes

### YOLO Mode Rules

Apply only in YOLO mode (`--yolo`):

```toml
[[rule]]
toolName = "write_file"
decision = "allow"
modes = ["yolo"]
priority = 100
```

### Auto-Edit Mode Rules

Apply in auto-edit mode:

```toml
[[rule]]
toolName = "replace"
decision = "allow"
modes = ["autoEdit"]
priority = 100
```

## Template Library

### Secure Development Environment

```toml
# Allow read operations
[[rule]]
toolName = ["read_file", "glob", "search_file_content", "list_directory"]
decision = "allow"
priority = 100

# Ask for writes
[[rule]]
toolName = ["write_file", "replace"]
decision = "ask_user"
priority = 100

# Allow safe git commands
[[rule]]
toolName = "run_shell_command"
commandPrefix = ["git status", "git diff", "git log", "git branch"]
decision = "allow"
priority = 200

# Ask for other git commands
[[rule]]
toolName = "run_shell_command"
commandPrefix = "git "
decision = "ask_user"
priority = 150

# Deny destructive commands
[[rule]]
toolName = "run_shell_command"
commandRegex = "^(rm|rmdir|del|rd|format|mkfs)\\s"
decision = "deny"
priority = 999
```

### Read-Only Mode

```toml
# Allow all reads
[[rule]]
toolName = ["read_file", "glob", "search_file_content", "list_directory", "web_fetch"]
decision = "allow"
priority = 100

# Deny all writes
[[rule]]
toolName = ["write_file", "replace", "run_shell_command"]
decision = "deny"
priority = 500
```

### NPM/Node.js Safe

```toml
# Allow npm read commands
[[rule]]
toolName = "run_shell_command"
commandPrefix = ["npm list", "npm outdated", "npm audit"]
decision = "allow"
priority = 200

# Ask for npm install/run
[[rule]]
toolName = "run_shell_command"
commandPrefix = ["npm install", "npm run", "npm exec"]
decision = "ask_user"
priority = 150

# Deny npm publish
[[rule]]
toolName = "run_shell_command"
commandPrefix = "npm publish"
decision = "deny"
priority = 900
```

### MCP Server Restrictions

```toml
# Deny all external MCP servers by default
[[rule]]
toolName = "*__*"
decision = "deny"
priority = 100

# Allow specific trusted server
[[rule]]
mcpName = "trusted-internal-server"
decision = "allow"
priority = 200

# Allow specific tools from another server
[[rule]]
toolName = ["other-server__read_docs", "other-server__search"]
decision = "allow"
priority = 200
```

### Enterprise Lockdown

```toml
# System-level (Admin tier)
# Block all network access
[[rule]]
toolName = ["web_fetch", "google_web_search"]
decision = "deny"
priority = 999

# Block all MCP servers
[[rule]]
toolName = "*__*"
decision = "deny"
priority = 999

# Allow only reads
[[rule]]
toolName = ["read_file", "glob", "search_file_content"]
decision = "allow"
priority = 100

# Block all shell commands except safe ones
[[rule]]
toolName = "run_shell_command"
decision = "deny"
priority = 500

[[rule]]
toolName = "run_shell_command"
commandPrefix = ["ls ", "cat ", "echo ", "pwd"]
decision = "allow"
priority = 600
```

## Validation

### Check TOML Syntax

```bash
python -c "import tomllib; tomllib.load(open('policy.toml', 'rb'))"
```

### Common Errors

| Error | Cause | Fix |
| --- | --- | --- |
| Parse error | Invalid TOML | Check quotes, brackets |
| Rule ignored | Lower priority | Increase priority |
| Rule conflicts | Overlapping patterns | Refine patterns |
| Regex fails | Bad escape | Use `\\` for backslash |

### Debug Rules

```bash
# Test which rule matches
gemini "Test shell command" --debug-policy
```

## Best Practices

### 1. Start Restrictive

```toml
# Default deny, then allow specific
[[rule]]
toolName = "*"
decision = "ask_user"
priority = 1

[[rule]]
toolName = "read_file"
decision = "allow"
priority = 100
```

### 2. Use Clear Priorities

```toml
# Security rules at 900+
[[rule]]
commandRegex = "^rm\\s"
decision = "deny"
priority = 999

# Normal rules at 100-499
[[rule]]
commandPrefix = "git "
decision = "allow"
priority = 200
```

### 3. Document Rules

```toml
# SECURITY: Block destructive file operations
# Reason: Prevent accidental data loss
# Author: security-team
# Date: 2025-11-30
[[rule]]
toolName = "run_shell_command"
commandRegex = "^(rm|rmdir)\\s+-r"
decision = "deny"
priority = 999
```

### 4. Test Before Deploy

```bash
# Test in interactive mode first
gemini --policy-file ./test-policy.toml
```

### 5. Layer Policies

```text
System policies (enterprise defaults)
  └── User policies (personal preferences)
       └── Project policies (project-specific)
```

## Related Skills

- `gemini-cli-docs` - Official policy documentation
- `toml-command-builder` - Custom command creation

## Keyword Registry

| Topic | Keywords |
| --- | --- |
| Basic | `policy engine`, `toml rules`, `tool policy` |
| Decisions | `allow`, `deny`, `ask_user`, `decision` |
| Matching | `toolName`, `commandPrefix`, `commandRegex`, `argsPattern` |
| Priority | `priority tier`, `rule priority`, `precedence` |
| MCP | `mcp policy`, `mcpName`, `server rules` |
| Modes | `yolo mode`, `autoEdit`, `approval mode` |

## Test Scenarios

### Scenario 1: Create Policy Rule

**Query**: "How do I create a Gemini policy to block rm commands?"
**Expected Behavior**:

- Skill activates on "policy engine" or "tool policy"
- Provides TOML rule with commandPrefix/commandRegex
**Success Criteria**: User receives working deny rule for destructive commands

### Scenario 2: Priority Configuration

**Query**: "How do Gemini policy priorities work?"
**Expected Behavior**:

- Skill activates on "priority tier" or "rule priority"
- Explains tier system and calculation
**Success Criteria**: User understands tier-based priority (Admin > User > Default)

### Scenario 3: MCP Server Policy

**Query**: "How do I restrict MCP server tools in Gemini?"
**Expected Behavior**:

- Skill activates on "mcp policy" or "server rules"
- Provides mcpName and wildcard patterns
**Success Criteria**: User receives MCP-specific policy rules

## Version History

- v1.1.0 (2025-12-01): Added MANDATORY section, Test Scenarios, Version History
- v1.0.0 (2025-11-25): Initial release
