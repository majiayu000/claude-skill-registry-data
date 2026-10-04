---
name: react-stack
description: React implementation guidance for component boundaries, state ownership, accessibility, and practical frontend behavior.
compatibility: opencode
metadata:
  audience: engineer
  purpose: stack-guidance
---
## Focus areas

- Keep component responsibilities and boundaries clear.
- Prefer simple state ownership and predictable data flow.
- Preserve established styling, routing, and data-fetching patterns.
- Build accessible and responsive UI behavior.
- Consider rendering behavior, user interactions, and failure states together.

## Guardrails

- Avoid adding state libraries or abstraction-heavy hooks without a concrete need.
- Do not cargo-cult memoization or optimization patterns.
- Be careful with hydration, user-state transitions, and accessibility regressions.
