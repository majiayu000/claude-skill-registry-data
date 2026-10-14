---
name: decide-builder
description: When to use the fluent Builder pattern vs constructors or factories.
---

# Skill: Builder

> "Many options. One fluent API."

## The Decision

**Use Builder when:**
- Object requires many optional parameters
- Construction order matters
- You want a fluent, readable API
- Configuration is context-dependent

**Use Constructor/Factory when:**
- Object is simple (few required params)
- All params are mandatory
- No variation in construction

## The Heuristic

Ask: *"Do I need to configure this object in multiple ways?"*

- **Yes, many options** → Builder
- **No, fixed construction** → Constructor/Factory

## The Quick Test

| Scenario                             | Use         |
|--------------------------------------|-------------|
| 5+ optional parameters               | Builder     |
| Context-dependent defaults           | Builder     |
| Method chaining improves readability | Builder     |
| Simple, mandatory params             | Constructor |
| Single creation path                 | Factory     |

## Real-World Examples

For concrete examples from Laravel, Spatie, and production code, see [examples.md](examples.md).
