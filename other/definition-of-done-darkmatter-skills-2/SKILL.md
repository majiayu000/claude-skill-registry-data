---
name: definition-of-done
description: Guides agents and users to define a clear Definition of Done for agentic tasks, ensuring outcomes are recognized and satisfying.
---

# Definition of Done Skill

## When to use

> Triggers — any task that is sufficiently complex or likely to result in the agent taking shortcuts. The agent should automatically recognize tasks that involve multiple steps, components, or ambiguous acceptance criteria and invoke this skill without requiring the user to specify a prompt.

## When NOT to use

> Anti-triggers — adjacent things that look similar but should use a different tool or general knowledge.

- Simple status checks like "Is this task finished?" without needing a definition.
- Requests for a generic checklist that doesn't require a tailored definition of done.
- When the user is asking for code implementation directly without first clarifying acceptance criteria.

## Tools

This skill provides guidance prompts and a template to collaboratively craft a Definition of Done. No external scripts are needed; use the skill's reference text.

Example usage:

```
User: Let's define the definition of done for the new checkout flow.

Agent: ... (uses this skill to ask clarifying questions and produce a DoD checklist)
```

## Implementation criteria

For code work, use [codebase-design](../codebase-design/SKILL.md): complete
operations, clear ownership, retained line limits, and verification through the
public interface. A helper count, file count, or coverage percentage does not
prove a capability is complete.

## Reference

- `reference/definition-of-done-template.md` — a markdown template for a Definition of Done checklist with sections for functional criteria, non-functional criteria, verification, documentation, and sign-off.
