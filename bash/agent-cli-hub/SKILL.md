---
name: agent-cli-hub
description: >-
  Choose CLI tools and safe patterns before repo work. Install checklist,
  bounded search/read commands, and confirmation gates. Use when navigating
  the codebase, running shell commands, or setting up agent tooling on
  Windows, WSL2, or macOS.
---

# Agent CLI hub

Router for lightweight CLI tooling skills in **image-scoring-gallery**. Prefer bounded, low-memory commands before broad reads or heavyweight indexers.

## Purpose

Central entry point for agent-safe CLI workflows: which skill to use, how to install tools, how to bound output, and when to ask for confirmation.

## When to use

- Starting work in an unfamiliar repo or shell environment
- Choosing between text search, structural search, git, config tools, or MCP layers
- Before running install commands or destructive shell operations

## Skill router

| Need | Skill |
|------|-------|
| Find files / grep / browse tree | [`agent-search`](../agent-search/SKILL.md) — rg vs grep vs ast-grep vs fd; optional **fff-gallery** project MCP |
| git status, diff, gh PR/issue | [`agent-git-workflows`](../agent-git-workflows/SKILL.md) |
| jq/yq on JSON/YAML, API probes | [`agent-data-config`](../agent-data-config/SKILL.md) |
| npm lint, tsc, vitest, docker | [`agent-dev-tooling`](../agent-dev-tooling/SKILL.md) |
| Windows vs WSL2 choice | [`agent-platform-tooling`](../agent-platform-tooling/SKILL.md) |
| MCP vs CLI code intelligence | [`mcp-code-intelligence`](../mcp-code-intelligence/SKILL.md) |
| Gallery pipeline / DB triage | [`image-scoring-mcp`](../image-scoring-mcp/SKILL.md) |
| Fast indexed file search (MCP) | **[fff](https://github.com/dmtrKovalenko/fff)** — **project** `fff-gallery` in `.cursor/mcp.json`; see [AGENTS.md § fff](../../../AGENTS.md) |
| Architecture / cross-module graph | **[Graphify](https://github.com/Graphify-Labs/graphify)** — skill [`graphify`](../graphify/SKILL.md); soft rule [`.cursor/rules/graphify.mdc`](../../rules/graphify.mdc); see [AGENTS.md § Graphify](../../../AGENTS.md) |

## Required tools (baseline)

`git`, `rg`, `fd`, `jq`, `node` (+ npm). Install full set via [references/install-blocks.md](references/install-blocks.md).

## Install tiers

Install in order — see [references/install-tiers.md](references/install-tiers.md):

1. **Tier 0:** `git`, `rg`, `fd`, `jq`, `node`
2. **Block A:** canonical block in [references/install-blocks.md](references/install-blocks.md)
3. **Block B:** child-skill extensions (`yq`, `just`, `mise`, …)
4. **Deferred:** optional tools per skill (`fzf`, `semgrep`, …)

## Agent environment

After installing CLI tools, **restart Cursor** and verify PATH — see [references/agent-environment.md](references/agent-environment.md).

## Install

See [references/install-blocks.md](references/install-blocks.md) — Windows winget, WSL2 apt, macOS Homebrew.

## Agent-safe patterns

1. Inspect `git status --short` before editing.
2. Use bounded output — see [references/bounded-output-patterns.md](references/bounded-output-patterns.md).
3. Prefer project scripts (`npm run …`) over ad hoc commands — see [`.agent/COMMANDS.md`](../../../.agent/COMMANDS.md).
4. Do not assume repo language before inspecting `package.json`, `pyproject.toml`, etc.
5. Never auto-run destructive commands — see [references/commands-requiring-confirmation.md](references/commands-requiring-confirmation.md).

## Commands requiring confirmation

Full list: [references/commands-requiring-confirmation.md](references/commands-requiring-confirmation.md).

## Platform guidance

[references/windows-wsl-split.md](references/windows-wsl-split.md) — when Windows native is enough vs WSL2 for sibling backend work.

## Troubleshooting

- **Tool not found:** Re-run install block for your platform; restart shell.
- **Slow search on WSL:** Avoid `/mnt/c` for heavy repos; clone under `~/src`.
- **Gallery dev:** `npm run doctor` for config and backend URL probes.

## Verification checklist

```bash
git --version && rg --version && node --version && jq --version
npm run doctor   # gallery-specific
```
