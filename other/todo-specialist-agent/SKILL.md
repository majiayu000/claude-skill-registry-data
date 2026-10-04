---
name: todo-specialist-agent
description: >
  Maintain ndestates-io TODO-*.md (carry forward, prioritize, update from work). Use on /todo-specialist-agent or when syncing tasks.
argument-hint: "What to mark done, add, or reprioritize. e.g. 'mark valuations layout done, add next CDD'"
user-invocable: true
disable-model-invocation: false
---

# TODO Specialist Agent

1. Run `/load-project-cache-first`.
2. Read and embody the full instructions in [`.grok/agents/todo-specialist-agent.md`](../../.grok/agents/todo-specialist-agent.md).
3. Output Proposed TODO Updates per canonical format (include branch/date).
4. Per copilot-instructions: ensure today's TODO and tomorrow's on shutdown.
5. Propose only; approval before commit.

Handoffs: structured for main/orchestrator.
