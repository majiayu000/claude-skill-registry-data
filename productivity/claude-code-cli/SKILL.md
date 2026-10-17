---
skill_id: algorithms.claude_code_cli.reference
name: "Claude Code CLI -- Reference"
description: "Complete reference for Claude Code CLI: hooks, slash commands, MCP servers, settings, IDE integrations, agent mode, memory system."
version: v00.33.0
status: ADOPTED
domain_path: algorithms/claude-code-cli
anchors:
  - claude_code
  - cli
  - hooks
  - slash_commands
  - mcp_integration
  - agent_mode
  - memory
  - ide_integration
source_repo: claude-code-main
risk: safe
languages: [bash, json]
llm_compat: {claude: full, gpt4o: minimal, gemini: minimal, llama: minimal}
apex_version: v00.33.0
executor: LLM_BEHAVIOR
---

# Claude Code CLI -- Reference

## Key Capabilities

```
HOOKS: PreToolUse, PostToolUse, UserPromptSubmit
SLASH COMMANDS: /commit, /review-pr, /help
MCP: claude mcp add <name> <command>
AGENT MODE: claude --agent (autonomous multi-step)
MEMORY: .claude/CLAUDE.md (project), ~/.claude/CLAUDE.md (user)
```

## APEX Integration

APEX uses Claude Code as the FULL LLM runtime adapter (OPP-105).
ForgeSkills uses git_clone via Claude Code Bash tool.

## Source README

# Claude Code Plugins

This directory contains some official Claude Code plugins that extend functionality through custom commands, agents, and workflows. These are examples of what's possible with the Claude Code plugin system—many more plugins are available through community marketplaces.

## What are Claude Code Plugins?

Claude Code plugins are extensions that enhance Claude Code with custom slash commands, specialized agents, hooks, and MCP servers. Plugins can be shared across projects and teams, providing consistent tooling and workflows.

Learn more in the [official plugins documentation](https://docs.claude.com/en/docs/claude-code/plugins).

## Plugins in This Directory

| Name | Description | Contents |
|------|-------------|----------|
| [agent-sdk-dev](./agent-sdk-dev/) | Development kit for working with the Claude Agent SDK | **Command:** `/new-sdk-app` - Interactive setup for new Agent SDK projects<br>**Agents:** `agent-sdk-verifier-py`, `agent-sdk-verifier-ts` - Validate SDK applications against best practices |
| [claude-opus-4-5-migration](./claude-opus-4-5-migration/) | Migrate code and prompts from Sonnet 4.x and Opus 4.1 to Opus 4.5 | **Skill:** `claude-opus-4-5-migration` - Automated migration of model strings, beta headers, and prompt adjustments |
| [code-review](./code-review/) | Automated PR code review using multiple specialized agents with confidence-based scoring to filter false positives | **Command:** `/code-review` - Automated PR review workflow<br>**Agents:** 5 parallel Sonnet agents for CLAUDE.md compliance, bug detection, historical context, PR history, and code comments |
| [commit-commands](./commit-commands/) | Git workflow automation for committing, pushing, and creating pull requests | **Commands:** `/commit`, `/commit-push-pr`, `/clean_gone` - Streamlined git operations |
| [explanatory-output-style](./explanatory-output-style/) | Adds educational insights about implementation choices and codebase patterns (mimics the deprecat

## Diff History
- **v00.33.0**: Ingested from claude-code-main