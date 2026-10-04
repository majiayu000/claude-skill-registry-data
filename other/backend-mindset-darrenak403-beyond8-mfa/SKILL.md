---
name: backend-mindset
description: Language-agnostic backend engineering mindset — Clean Architecture, layered dependency rules, REST API design, TDD, security principles, event-driven patterns, performance trade-offs. Use for architecture decisions, "where does this code go?", API design questions, testing strategy, or any backend reasoning task regardless of language. Activate proactively when structuring services, designing APIs, planning test coverage, or reviewing architectural decisions in Go, Python, Java, Node, .NET, or any backend stack.
---

# Backend Mindset — Language-Agnostic Principles

Load only the reference needed for the current task.

## Reference Map

| Task | When to load | File |
|------|--------------|------|
| Where does code go? What layer? | Any new feature or refactor | [`references/architecture.md`](references/architecture.md) |
| REST endpoints, routes, status codes | API design or new endpoint | [`references/api-design.md`](references/api-design.md) |
| Testing strategy, TDD cycle | Writing or planning tests | [`references/testing.md`](references/testing.md) |
| Auth, secrets, input validation, injection | Security concerns | [`references/security.md`](references/security.md) |
| Events, messaging, async patterns | Event-driven inter-service | [`references/events.md`](references/events.md) |
| Query patterns, caching, async perf | Performance optimization | [`references/performance.md`](references/performance.md) |

---

## Decision Tree

```
TASK?
│
├─ New feature / endpoint
│  ├─ Where does this code live?   → references/architecture.md
│  └─ How to structure the API?    → references/api-design.md
│
├─ Writing tests / TDD
│  └─ All test concerns            → references/testing.md
│
├─ Security concern
│  └─ Auth, validation, secrets    → references/security.md
│
├─ Microservice / async
│  └─ Events, messaging            → references/events.md
│
└─ Performance concern
   └─ Queries, caching, async      → references/performance.md
```
