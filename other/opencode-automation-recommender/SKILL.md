---
name: opencode-automation-recommender
description: "Analyze a codebase and recommend Claude Code automations (hooks, subagents, skills, plugins, MCP servers). Use when user asks for automation recommendations, wants to optimize their Claude Code setup, mentions improving Claude Code workflows, asks how to first set up Claude Code for a project, or wants to know what Claude Code features they should use."
compatibility: opencode
---

# OpenCode Automation Recommender

Analyze the repository and recommend a small, prioritized set of OpenCode-native improvements. This skill is read-only unless the user explicitly asks to implement changes.

## When to use
Use when the user asks how to improve OpenCode for a project, configure agents or subagents, organize skills, add MCP integrations, configure permissions, create commands, or improve repeatable workflows.

## Workflow
1. Inspect the repository structure and existing `AGENTS.md`, `.opencode/`, `opencode.json`, `opencode.jsonc`, `agents/`, `commands/`, and `skills/` files before recommending changes.
2. Confirm the installed OpenCode version and consult the matching official documentation when behavior is version-sensitive. Do not assume Claude Code hooks, tools, plugin APIs, or frontmatter are supported by OpenCode.
3. Identify friction from the actual project: repeated instructions, risky operations, missing tests, documentation gaps, repeated workflows, or external-service needs.
4. Recommend only changes supported by the installed OpenCode version. Distinguish native features (agents, skills, commands, permissions, MCP, plugins) from external scripts or third-party integrations.
5. Rank recommendations by impact, effort, and risk. Give a maximum of 3 high-value recommendations first.
6. Do not modify files unless asked. If implementation is requested, propose a plan, back up existing files, edit the smallest necessary set, validate config syntax and paths, and report what was tested.

## OpenCode concepts
- Skills: `.opencode/skills/<skill-name>/SKILL.md` or `~/.config/opencode/skills/<skill-name>/SKILL.md`.
- Agents: `.opencode/agents/<agent-name>.md` or the global OpenCode agents directory supported by the installed version.
- Commands: `.opencode/command/<name>.md` or the matching documented plural form for the installed version. Verify the version's docs.
- Configuration: `opencode.json` / `opencode.jsonc`; validate against the installed version's schema.
- MCP and plugins: configure only with verified schemas and explicit user authorization for credentials or account connections.

## Output
Provide: observed context; top recommendations with rationale; exact target paths; implementation/verification steps; risks and assumptions. Never claim an integration or event hook exists without verifying it.
