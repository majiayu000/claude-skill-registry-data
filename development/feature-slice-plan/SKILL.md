---
name: feature-slice-plan
description: Create a minimal, step-based plan for implementing a feature across Clean Architecture layers without over-generation.
---

Rules:

- Follow AGENTS.md and all .codex policies.
- Output plan only. No code.

Plan sections:

- Feature intent and acceptance criteria
- Domain changes (types, invariants, events) + tests
- Application changes (service/use case, ports) + tests
- Infrastructure changes:
  - Web adapter (controller/DTOs/Problem Details mapping) + tests
  - Persistence adapter (JPA/QueryDSL/MapStruct) + tests if needed
- Wiring/config changes (only if required)
- File list per step (exact paths)
- Build commands per module (mvnw)
