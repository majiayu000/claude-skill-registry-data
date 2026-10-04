---
name: rust-stack
description: Rust implementation guidance for ownership, error handling, module boundaries, and pragmatic async design.
compatibility: opencode
metadata:
  audience: engineer
  purpose: stack-guidance
---
## Focus areas

- Keep ownership and borrowing understandable.
- Prefer explicit error types and propagation.
- Keep crate and module boundaries clear.
- Use async and trait abstractions only where they add real value.
- Minimize unsafe usage and make it obvious when present.

## Guardrails

- Avoid type-system showmanship and unnecessary generic complexity.
- Be mindful of clone-heavy workarounds and hidden allocation costs.
- Prefer code that other engineers can confidently maintain.
