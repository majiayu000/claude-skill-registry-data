---
name: copilot-cli-agent-customization
description: '**WORKFLOW SKILL** — Create, update, review, fix, or debug Copilot CLI customization files (`copilot-instructions.md`, `AGENTS.md`, `*.instructions.md`, `*.agent.md`, `SKILL.md`, hook JSON, `plugin.json`, and plugin command files). USE FOR: authoring terminal-first customization workflows; troubleshooting why CLI instructions, skills, agents, hooks, or plugins are ignored; configuring `applyTo` and `excludeAgent`; defining CLI tool restrictions; creating custom agents or command packs; packaging reusable CLI customizations. DO NOT USE FOR: general coding questions; non-customization runtime debugging; Copilot in VS Code customization (use `copilot-vscode-agent-customization` instead); MCP server configuration; VS Code prompt files or extension development. INVOKES: file system tools, ask-questions tool, subagents for codebase exploration. FOR SINGLE OPERATIONS: For quick YAML or JSON fixes, or for creating one known file from a clear pattern, edit directly instead of loading the full skill.'
metadata: 
  author: arisng
  version: 0.1.0
---

# Agent Customization for Copilot CLI

## Decision Flow

| Primitive | When to Use |
|-----------|-------------|
| Workspace Instructions | Always-on defaults for the repository or your personal CLI environment |
| File Instructions | Explicit via `applyTo`, scoped by `excludeAgent`, or discovered on demand from `description` |
| MCP | Connect external systems, APIs, or data sources; use MCP-specific docs for server setup |
| Hooks | Deterministic shell commands at lifecycle points like `preToolUse` or `postToolUse` |
| Custom Agents | Specialized personas, tool restrictions, or CLI orchestration workflows |
| Commands / Plugins | Reusable terminal shortcuts, distributed command packs, or bundled CLI customizations |
| Skills | On-demand workflows with bundled references, scripts, and reusable operational context |

## Quick Reference

Consult the reference docs for templates, path rules, CLI-only frontmatter, hook schema details, plugin packaging, and troubleshooting steps. If the references are not enough, load the official GitHub Copilot CLI documentation for the relevant primitive.

| Type | File | Location | Reference |
|------|------|----------|-----------|
| Workspace Instructions | `copilot-instructions.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` | `.github/`, repo root, or CLI instruction roots | [Link](./references/workspace-instructions.md) |
| File Instructions | `*.instructions.md` | `.github/instructions/` or roots listed in `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` | [Link](./references/instructions.md) |
| Commands / Plugins | `plugin.json`, `commands/*.md` | `plugins/cli/<name>/` | [Link](./references/commands-and-plugins.md) |
| Hooks | `*.json` | `.github/hooks/` | [Link](./references/hooks.md) |
| Custom Agents | `*.agent.md` | `.github/agents/` or `~/.copilot/agents/` | [Link](./references/agents.md) |
| Skills | `SKILL.md` | `.github/skills/<name>/` or `~/.copilot/skills/<name>/` | [Link](./references/skills.md) |

**User-level CLI**: `~/.copilot/copilot-instructions.md`, `~/.copilot/agents/`, and `~/.copilot/skills/` are the main personal discovery locations. `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` can add extra instruction roots. Hooks are repo-scoped from the current working directory.

## Creation Process

If you need to explore or validate existing patterns in the codebase, use a read-only subagent. If the ask-questions tool is available, use it to lock naming, scope, and packaging choices before editing multiple files.

Follow these steps when creating any Copilot CLI customization file.

### 1. Determine Scope

Ask where the customization belongs:
- **Repository**: Team-shared defaults and reusable assets -> `.github/` or repo-managed plugin directories
- **Home directory**: Personal, cross-repo CLI customizations -> `~/.copilot/`
- **Plugin bundle**: Shareable packaged commands, skills, hooks, or agents -> `plugins/cli/<name>/`

### 2. Choose the Right Primitive

Use the Decision Flow above to pick the narrowest CLI surface that fits the request.

### 3. Create the File

Create the file directly at the appropriate path:
- Use the location tables in each reference file
- Include the required YAML or JSON structure
- Prefer plugin `commands` or skills instead of `.prompt.md`
- Keep `SKILL.md` lean and push detailed material into `references/`

### 4. Validate

After creating:
- Confirm the file is in the correct CLI discovery path
- Verify YAML or JSON syntax
- Check that `description` is present and keyword-rich
- Confirm CLI-only keys (`disable-model-invocation`, `excludeAgent`, hook event names, plugin fields) are valid for the chosen primitive
- Re-publish or reinstall when plugin-backed files change

## Edge Cases

**Instructions vs Skill?** If it should affect most work or all matching files, use instructions. If it is an on-demand workflow, use a skill.

**Skill vs Command / Plugin?** Use a command or plugin command for a lightweight terminal shortcut. Use a skill when the workflow needs bundled references, scripts, or a larger reusable capability.

**Command / Plugin vs Custom Agent?** Use a command when the user starts a focused workflow directly. Use a custom agent when you need a persistent persona, isolated tool restrictions, or a reusable specialist that other agents can delegate to.

**Skill vs Custom Agent?** Use a skill when one workflow can run with the same capabilities throughout. Use a custom agent when you need context isolation or a specialist identity with specific CLI tool access.

**Hooks vs Instructions?** Instructions guide the model. Hooks enforce behavior with deterministic shell commands. If the behavior must always happen, use a hook.

**`AGENTS.md` vs `copilot-instructions.md`?** In Copilot CLI they are additive, not mutually exclusive. Use both only when their responsibilities are clearly separated.

## Guardrails

- Use this skill only for **Copilot CLI** and terminal-first customization surfaces.
- If the request mentions VS Code prompt files, Chat Customizations UI, Settings Sync, editor prompt recommendations, `agents:`, or `argument-hint:`, stop and use [copilot-vscode-agent-customization](../copilot-vscode-agent-customization/SKILL.md) instead.
- Do not teach `.prompt.md`, VS Code custom-agent schema, or editor-only UX from this skill; keep this skill focused on CLI paths, CLI hooks, CLI agents, and commands/plugins.

## Common Pitfalls

**Description is the discovery surface.** `description` is how the agent decides whether to load a skill, instruction, or agent. Include trigger phrases and "Use when..." wording.

**`.prompt.md` does not port to CLI.** Prompt files are IDE-only. For terminal-first reuse, prefer plugin commands or skills.

**Do not copy VS Code-only schema into CLI.** `agents:` and `argument-hint:` belong to VS Code custom agents, not CLI agents. CLI hooks also use a different schema and lowercase event names.

**CLI instruction loading is additive.** Copilot CLI can load `.github/copilot-instructions.md` and `AGENTS.md` together. Do not teach a fake "choose one" rule as a product constraint.

**Plugin changes are not live.** After editing plugin files, rebuild or reinstall the plugin so Copilot CLI picks up the new bundle contents.

**Avoid broad `applyTo` defaults.** `applyTo: "**"` loads everywhere and burns context. Use focused globs unless the instruction truly belongs in every request.
