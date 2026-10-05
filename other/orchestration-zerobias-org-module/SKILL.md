---
name: orchestration
description: Agent orchestration and coordination patterns. Use when coordinating work between multiple specialized agents.
---

# Orchestration Protocol

## Core Rules

1. **Agent-Only Execution**: Never work without agents - they have exclusive domains
2. **Workflow Mapping**: Every request maps to a workflow in `.claude/commands/`
3. **Rule Updates**: When user updates a rule, apply it immediately before continuing
4. **Failure Handling**: Stop on failures, report clearly, return control

## Agent Boundaries

- Each agent owns specific tasks exclusively
- No agent overlap allowed
- Agents load their own rules
- Agents validate their own work

## Workflow Execution

- Follow the workflow specification exactly
- Let agents handle their phases
- Trust agent decisions within their domain
- Return control after completion