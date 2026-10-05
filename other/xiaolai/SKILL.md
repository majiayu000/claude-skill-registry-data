---
name: xiaolai
description: "Xiaolai's Claude tools collection. Use when user types /xiaolai. Routes to: (1) claude-agent-sdk — Agent SDK reference for building autonomous AI agents, or (2) nlpm — Natural-Language Programming Manager for scanning, scoring, and fixing NL artifacts."
user-invocable: true
---

# Xiaolai's Claude Tools

You have two tools available. Ask the user which one they want to use:

## Available Tools

### 1. Claude Agent SDK (`/xiaolai sdk` or `/xiaolai agent`)
Build autonomous AI agents with Claude Agent SDK (TypeScript v0.2.96 / Python v0.1.56).
Covers: `query()`, hooks, subagents, MCP, permissions, sandbox, structured outputs, sessions.

**Use when:** building AI agents, configuring MCP servers, setting up permissions/hooks, using structured outputs, troubleshooting SDK errors, or working with subagents.

### 2. NLPM (`/xiaolai nlpm`)
Natural-Language Programming Manager — scan, lint, and score NL artifacts with Claude-native quality scoring.

**Commands:**
- `/nlpm:ls` — discover NL artifacts
- `/nlpm:score` — 100-point quality scoring
- `/nlpm:check` — cross-component consistency
- `/nlpm:fix` — auto-fix mechanical issues
- `/nlpm:trend` — track score history
- `/nlpm:test` — run NL-TDD specs
- `/nlpm:init` — configure project
- `/nlpm:security-scan` — scan plugin for security risks

---

## Routing Logic

1. If the user typed `/xiaolai` with no argument, show the menu above and ask which tool to use.
2. If the user typed `/xiaolai sdk` or `/xiaolai agent` — read `claude-agent-sdk/SKILL.md` and follow its instructions.
3. If the user typed `/xiaolai nlpm` — read `nlpm/CLAUDE.md` and follow its instructions. For specific nlpm commands, read the corresponding file under `nlpm/commands/`.
4. If the user's context makes it obvious which tool applies (e.g. they're building an agent → sdk, they want to score/lint NL artifacts → nlpm), route directly without asking.

## File Locations

All files are relative to this skill's directory (`~/.claude/skills/xiaolai/`):

- **SDK entry:** `claude-agent-sdk/SKILL.md`
  - TypeScript details: `claude-agent-sdk/SKILL-typescript.md`
  - Python details: `claude-agent-sdk/SKILL-python.md`
  - Agent templates: `claude-agent-sdk/templates/`
  - Agent rules: `claude-agent-sdk/rules/`
- **NLPM entry:** `nlpm/CLAUDE.md`
  - Commands: `nlpm/commands/*.md`
  - Agents: `nlpm/agents/*.md`
  - Skills/knowledge: `nlpm/skills/nlpm/`

## Auto-Update

Both repos are git clones. To update, run:
```bash
cd ~/.claude/skills/xiaolai/claude-agent-sdk && git pull
cd ~/.claude/skills/xiaolai/nlpm && git pull
```
