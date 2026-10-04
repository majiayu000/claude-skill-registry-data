---
name: mission-control-register-agent
description: >-
  Registers an agent with Mission Control via the Convex api.agents.register
  mutation. Use this skill when an agent session starts and the agent must
  announce itself (name, emoji, role, workspace, task types, budgets) before
  doing any other work. Re-registering an existing agent updates its heartbeat.
version: 1.0.0
owner: software-factory
risk: low
capabilities:
  - agent-registration
  - identity-setup
  - budget-declaration
requires_tools:
  - convex
related_skills:
  - mission-control-heartbeat
  - mission-control-task-lifecycle
---

# Register with Mission Control

Before doing anything, register with Mission Control. If you're already registered, this updates your heartbeat. All interactions use **Convex** mutations and queries — there is no REST API.

## API

```
Mutation: api.agents.register
Args:
  name: string          — Your unique agent name (e.g., "Coder")
  emoji: string         — Your emoji identifier (e.g., "💻")
  role: string          — One of: "INTERN", "SPECIALIST", "LEAD", "CEO"
  workspacePath: string — Your workspace directory
  projectId?: Id        — Project you belong to (optional)
  allowedTaskTypes?: string[] — Task types you handle:
    "CONTENT", "SOCIAL", "EMAIL_MARKETING", "CUSTOMER_RESEARCH",
    "SEO_RESEARCH", "ENGINEERING", "DOCS", "OPS"
  budgetDaily?: number  — Daily spend limit in USD
  budgetPerRun?: number — Per-run spend limit in USD
  canSpawn?: boolean    — Whether you can create sub-agents
  maxSubAgents?: number — Max sub-agents you can spawn

Returns: { agent: Agent, created: boolean }
```

## Rules

1. Register before any other Mission Control call — every other mutation needs your `agentId`.
2. Declare `allowedTaskTypes` accurately; the heartbeat response only surfaces claimable tasks matching your types.
3. Set `budgetDaily` and `budgetPerRun` if you spend money; see the `mission-control-budget-control` skill.

## Next Steps

After registering, start a heartbeat loop immediately (`mission-control-heartbeat`) — agents that miss heartbeats for 2 minutes get quarantined.
