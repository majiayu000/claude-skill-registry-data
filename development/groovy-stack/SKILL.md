---
name: groovy-stack
description: Groovy implementation guidance for application code, Gradle logic, DSLs, and Spock-oriented testing.
compatibility: opencode
metadata:
  audience: engineer
  purpose: stack-guidance
---
## Focus areas

- Prefer readable Groovy over magic-heavy dynamic behavior.
- Be careful with implicit coercion and runtime-only failures.
- Keep Gradle and DSL changes focused and easy to reason about.
- Use Spock or existing test patterns to express behavior clearly.

## Guardrails

- Do not spread custom build logic without a strong reason.
- Avoid dynamic shortcuts that reduce maintainability.
- Be explicit where Groovy interacts with typed JVM APIs.
