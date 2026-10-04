---
name: go-stack
description: Go implementation guidance for package design, explicit error handling, concurrency, and operational simplicity.
compatibility: opencode
metadata:
  audience: engineer
  purpose: stack-guidance
---
## Focus areas

- Keep packages small and responsibilities clear.
- Prefer explicit error handling and direct control flow.
- Use `context` consistently for cancellation and deadlines.
- Add concurrency only where it clearly helps.
- Keep interfaces narrow and justified.

## Guardrails

- Avoid interface-first design without a real substitution need.
- Watch for goroutine leaks, data races, blocking behavior, and retry mistakes.
- Prefer simple code that is easy to trace in production.
