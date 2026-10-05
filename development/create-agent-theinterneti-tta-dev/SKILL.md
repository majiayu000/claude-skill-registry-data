---
name: create-agent
description: 'Use this skill when creating, modifying, or debugging a custom Copilot agent (.agent.md file). Provides detailed patterns for agent orchestration, handoffs, sub-agent invocation, tool configuration, variable extraction, and prompt structure. Invoke when the user says "create an agent", "add a new agent", "agent handoffs", "sub-agent", or "orchestrate agents".'
---

# Create Agent

Detailed reference for building custom Copilot agents in TTA.dev.
For atomic rules (naming, frontmatter, registration), see the `agents` instruction.

## When to Use This Skill

- Creating a new `.agent.md` file from scratch
- Adding handoffs between agents for workflow transitions
- Setting up sub-agent orchestration (multi-step pipelines)
- Configuring tool access and MCP server integration
- Designing agent prompt structure with dynamic variables

## Prerequisites

- Understand the [composition model](../../docs/agents/dev/composition-model.md)
- Know which skills and workflows your agent needs (check `.github/copilot-catalog.yml`)
- Have the target agent's role and responsibilities defined

## Quick Start

1. Create `.github/agents/my-agent.agent.md` with frontmatter
2. Write the body following the Role → Responsibilities → Constraints pattern
3. Add entry to `.github/copilot-catalog.yml` with `skill_refs` and `workflow_refs`
4. Validate: `uv run python scripts/validate-catalog.py`

## Reference Docs

- [Handoffs and Orchestration](./references/handoffs-and-orchestration.md) — workflow transitions, sub-agent patterns
- [Tool Configuration](./references/tool-configuration.md) — aliases, MCP namespaces, strategies
- [Prompt Patterns](./references/prompt-patterns.md) — variables, body structure, best practices
