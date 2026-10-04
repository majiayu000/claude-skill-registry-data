---
name: github-expert
description: >
  GitHub platform expert for ndestates-io workflows, Actions, PRs, security scanning, automation. Use when /github-expert or managing CI/deploy.
argument-hint: "What GitHub area or task (e.g. 'review deploy workflow', 'branch protection')"
user-invocable: true
disable-model-invocation: false
---

# GitHub Expert Agent

1. Run `/load-project-cache-first`.
2. Read and embody the full instructions in [`.grok/agents/github-expert.md`](../../.grok/agents/github-expert.md).
3. For analysis, prefer/update docs under docs/ or reference existing caches.
4. Follow copilot-instructions + guardrails for any changes.
5. Output with summary, findings, recommendations, actions, next steps.

Cite caches.
