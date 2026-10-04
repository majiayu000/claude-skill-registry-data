---
name: branch-context-agent
description: >
  Branch scope and TODO-alignment analyzer for ndestates-io. Summarize branch purpose, changes vs active TODO, detect drift before merge or major work.
  Use when user runs /branch-context-agent or orchestrator needs context.
argument-hint: "Provide branch name and what context you need summarized."
user-invocable: true
disable-model-invocation: false
---

# Branch Context Agent

1. Run `/load-project-cache-first`.
2. Read and embody the full instructions in [`.grok/agents/branch-context-agent.md`](../../.grok/agents/branch-context-agent.md).
3. Gather branch info (`git branch --show-current`, log, status), cross vs TODO.
4. Report alignment verdict (aligned/partial/misaligned) + risks + next actions.
5. Cite caches used.

Handoffs: include branch_context details for main agent.
