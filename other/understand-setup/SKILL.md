---
name: understand-setup
description: Analyze your Claude Code setup to produce a knowledge graph of skills, agents, commands, MCP servers, and memory
argument-hint: [--full]
---

# /understand-setup

Analyze the Claude Code setup at `~/.claude/` and produce an interactive knowledge graph showing how skills, agents, commands, MCP servers, docs, and memory all connect.

## Instructions

```bash
cd ~/.claude/tools && python3 -m coremind_understand ~/.claude --mode claude
```

Then launch the dashboard:

```bash
cd ~/Projects/understand-anything/understand-anything-plugin/packages/dashboard && GRAPH_DIR=~/.claude npx vite --open
```

## What it maps

- **Skills** (48): Each SKILL.md becomes a file node with category tags
- **Agents** (39+): Each agent definition becomes a file node
- **Commands** (64+): Each command definition becomes a file node
- **Docs** (16): Reference documents become file nodes
- **Memory** (5): Persistent memory files become file nodes
- **MCP Servers** (8+): Each server becomes a concept node
- **Tools**: Custom tool packages become file nodes

## Layers

The graph is organized into 7 layers:
1. Skills — Skill definitions
2. Agents — Agent definitions
3. Commands — Command definitions
4. Documentation — Reference docs
5. Memory — Persistent memory
6. Tools — Custom packages
7. Configuration — Config files

## Tour

8-step guided tour: Overview → Skills → Agents → Commands → MCP Servers → Memory → Operating Framework → Operating Framework
