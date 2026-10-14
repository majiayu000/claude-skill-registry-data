---
name: decide-mock
description: When to mock. Real vs fake dependencies.
---

# Skill: Decide Mock

> "Mock at the boundaries, not everywhere."

## The Decision

**Mock when:**
- External service (payment gateway, email provider)
- Slow dependency (file system, network)
- Non-deterministic (time, randomness)
- You don't control it

**Don't mock when:**
- In-process dependency (your own classes)
- Database (use transactions instead)
- The mock is more complex than the real thing
- You're testing integration, not isolation

## The Heuristic

Ask: *"Does this cross a process boundary?"*

Yes → Mock it. No → Use the real thing.

## The Quick Test

| Ask                | Answer | Action             |
|--------------------|--------|--------------------|
| External API?      | Yes    | Mock               |
| Your own class?    | Yes    | Real               |
| Database?          | Yes    | Real + transaction |
| Time-dependent?    | Yes    | Freeze time        |
| Non-deterministic? | Yes    | Mock or seed       |

## Real-World Examples

See [examples.md](examples.md).
