---
name: architecture
description: Design maintainable application boundaries and component relationships using framework-agnostic architecture principles.
metadata:
  internal: true
---

# architecture

Use this skill for service boundaries, modules, dependency direction, interfaces, adapters, orchestration, and architectural refactoring.

## Principles

Prefer clear responsibilities and explicit dependencies.

Separate concerns when doing so improves:

- maintainability
- testability
- replacement
- ownership
- failure isolation

Do not introduce abstraction merely for abstraction's sake.

Stable application/business logic should not depend unnecessarily on volatile infrastructure details.

Use interfaces or boundaries where multiple implementations, isolation, or testing value justifies them.

Prefer incremental architectural change over unnecessary rewrites.

Preserve public behavior during structural refactoring unless behavior change is intentional.

Architecture should follow actual project complexity, not pattern names.

## Adaptation

Use project evidence to determine the actual language, framework, runtime, and existing conventions.

When stack-specific implementation guidance is needed, prefer project evidence, native framework or language mechanisms, and relevant user-installed specialist skills. Technology-specific guidance must not redefine or weaken the core engineering requirement.