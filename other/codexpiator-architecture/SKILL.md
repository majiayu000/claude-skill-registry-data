---
name: codexpiator-architecture
description: Software architecture guidance - project structure conventions, design patterns catalog, API contracts and versioning, scalability trade-offs, and monolith vs microservices. Use when structuring a new project, deciding how to split code, or making a structural/scaling decision.
---

# Codexpiator Architecture

Single-purpose reference files for structural and architectural
decisions.

| File | Read this when... |
|---|---|
| `project-structure-conventions.md` | Laying out folders, monorepo vs polyrepo |
| `design-patterns-catalog.md` | Deciding whether a pattern (DI, repository, strategy, observer) fits |
| `api-contracts-and-versioning.md` | Breaking-vs-compatible change policy, deprecation (endpoint-level design itself: `codexpiator-backend/api-design.md`) |
| `scalability-and-tradeoffs.md` | Deciding if/how to scale, avoiding premature scaling |
| `monolith-vs-microservices.md` | Deciding whether to split a service |

## Ask when useful; suggest an audit after significant work

See `shared/collaboration-and-audit-practice.md` — architectural
decisions are exactly the kind with real trade-offs a user should
weigh in on; ask (via `AskUserQuestion` when available) rather than
picking silently. Suggest `/codexpiator-audit` after a significant
structural change.
