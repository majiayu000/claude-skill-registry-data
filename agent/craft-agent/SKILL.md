---
name: craft-agent
description: How to craft a Sub-Agent persona.
---

# Skill: Craft Agent

> "Not just a prompt. A Persona."

## 1. The Principles
*   **Opinionated**: Helpful is boring. Ambitious is good. Give them a strong point of view.
*   **Scoped**: An agent should do ONE thing perfectly (e.g., "Review", "Plan").
*   **Explicit**: They know nothing unless you teach them (via Skills).

## 2. The Implementation
*   **Official Spec**: Use `claude-code-guide` agent to query sub-agent configuration options (`model`, `tools`, `skills`).
*   **Model**: Use `opus` for orchestration/reasoning. Use `sonnet` for coding speed.

## 3. The Knowledge
*   Remember to explicitly list every single skill the agent needs in the `skills:` frontmatter array.
