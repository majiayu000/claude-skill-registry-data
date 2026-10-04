---
name: java-stack
description: Java implementation guidance covering service structure, strong typing, testing, and common JVM application concerns.
compatibility: opencode
metadata:
  audience: engineer
  purpose: stack-guidance
---
## Focus areas

- Favor clear package and module boundaries.
- Keep service wiring and dependency injection straightforward.
- Use strong typing and explicit contracts.
- Respect build conventions such as Maven or Gradle structure.
- Watch transactionality, serialization, configuration, and concurrency behavior carefully.

## Guardrails

- Avoid interface and service proliferation without a concrete need.
- Prefer safe incremental refactors to broad structural cleanup.
- Keep tests aligned with the project's existing style and tooling.
