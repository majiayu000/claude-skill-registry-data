---
name: orient
description: Use when entering unfamiliar code to map both breadth (peer modules, callers, dependencies, cross-cutting concerns) and depth (architecture down to critical implementation details), in the project's domain vocabulary.
disable-model-invocation: true
---

I'm unfamiliar with this code. Map it across two axes:

- **Horizontal** — peer modules at the same level, upstream callers, downstream dependencies, and cross-cutting concerns it participates in.
- **Vertical** — top-down: purpose → key abstractions/types → control and data flow → critical implementation details and gotchas.

Use the project's domain vocabulary. Cite file:line. Flag where to start and what I can safely defer.