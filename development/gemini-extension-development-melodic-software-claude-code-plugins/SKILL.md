---
name: gemini-extension-development
description: Expert guide for building and managing Gemini CLI Extensions. Covers extension anatomy, GEMINI.md context, commands, MCP integration, and publishing. Use when creating Gemini extensions, linking local extensions, packaging MCP servers, or installing extensions from GitHub. Delegates to gemini-cli-docs.
allowed-tools: Read, Glob, Grep, Skill
---

# Gemini Extension Development

## 🚨 MANDATORY: Invoke gemini-cli-docs First

> **STOP - Before providing ANY response about Gemini Extensions:**
>
> 1. **INVOKE** `gemini-cli-docs` skill
> 2. **QUERY** for the specific extension topic
> 3. **BASE** all responses EXCLUSIVELY on official documentation loaded

## Overview

Expert skill for creating, testing, and distributing Gemini CLI Extensions. Extensions are the primary plugin mechanism for Gemini.

## When to Use This Skill

**Keywords:** gemini extension, create extension, gemini extensions link, extension gallery, context files, extension commands, extension releasing, uninstall extension

**Use this skill when:**

- Creating a new extension (`gemini extensions create`)
- Linking a local extension for development (`gemini extensions link`)
- Packaging MCP servers into extensions
- Adding custom slash commands (`.toml`) to extensions
- Installing extensions from GitHub or local paths
- Releasing extensions via Git or GitHub Releases

## Extension Anatomy

An extension can contain:

1. **`extension.yaml`:** Manifest file.
2. **`GEMINI.md`:** Context "playbook" for the model.
3. **`package.json`:** Dependencies (if using Node.js/TypeScript). **Note:** Use the Unified Google Gen AI SDK (e.g., `google-genai`) as `google-generativeai` is deprecated.
4. **MCP Servers:** Embedded tools.
5. **Commands:** `*.toml` files defining custom slash commands.
6. **Tool Restrictions:** `excludeTools` configuration.

## Development Workflow

1. **Create:** `gemini extensions create my-extension`
2. **Link:** `cd my-extension && gemini extensions link .` (Enables hot-reloading)
3. **Test:** Run `gemini` and use the new capabilities.
4. **Publish:** Push to GitHub (installable via URL).

## Keyword Registry (Delegates to gemini-cli-docs)

| Topic | Query Keywords |
| :--- | :--- |
| **Creation** | `create extension`, `extension template` |
| **Manifest** | `extension.yaml schema`, `extension manifest` |
| **Commands** | `extension slash commands`, `toml commands` |
| **Linking** | `gemini extensions link`, `local extension dev` |
| **Releasing** | `extension releasing git`, `github release extension` |
| **Management** | `uninstall extension`, `update extension` |

## Quick Decision Tree

**What do you want to do?**

1. **Start a New Extension** -> Query `gemini-cli-docs`: "create extension boilerplate"
2. **Test Locally** -> Query `gemini-cli-docs`: "link local extension"
3. **Add a Command** -> Query `gemini-cli-docs`: "define command in extension"
4. **Bundle an MCP Server** -> Query `gemini-cli-docs`: "extension mcp server"
5. **Install an Extension** -> Query `gemini-cli-docs`: "install extension from url"
6. **Release an Extension** -> Query `gemini-cli-docs`: "extension releasing git vs github"

## Test Scenarios

### Scenario 1: Create Extension

**Query**: "How do I create a new Gemini CLI extension?"
**Expected Behavior**:

- Skill activates on "create extension"
- Delegates to gemini-cli-docs for template command
**Success Criteria**: User receives `gemini extensions create` syntax

### Scenario 2: Link for Development

**Query**: "How do I test my Gemini extension locally?"
**Expected Behavior**:

- Skill activates on "test extension" or "link extension"
- Provides `gemini extensions link .` workflow
**Success Criteria**: User receives local development workflow

### Scenario 3: Release Extension

**Query**: "How do I publish my Gemini extension?"
**Expected Behavior**:

- Skill activates on "release extension" or "publish"
- Delegates to docs for Git/GitHub release options
**Success Criteria**: User receives release workflow options

## References

**Official Documentation:**
Query `gemini-cli-docs` for:

- "extensions"
- "extension development"

## Version History

- v1.1.0 (2025-12-01): Added Test Scenarios section
- v1.0.0 (2025-11-25): Initial release
