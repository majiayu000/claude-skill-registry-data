---
name: javascript-stack
description: JavaScript and Node implementation guidance for modules, async behavior, data validation, and runtime safety.
compatibility: opencode
metadata:
  audience: engineer
  purpose: stack-guidance
---
## Focus areas

- Keep modules focused and boundaries clear.
- Use consistent async and error-handling patterns.
- Validate data at system boundaries where runtime types matter.
- Respect the repo's module format, build setup, and linting patterns.
- Keep scripts and application logic straightforward.

## Guardrails

- Avoid accidental complexity in tooling or framework choices.
- Watch for runtime-only failures, weak input handling, and implicit assumptions.
- Prefer predictable behavior over clever dynamic patterns.
