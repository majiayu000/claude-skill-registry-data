---
name: roblox-luau-patterns
description: "Use when writing or refactoring Roblox Luau modules, object lifecycles, signals, task scheduling, pcall, and cleanup."
when_to_use: "Also for memory leaks, connections never disconnected, duplicate handlers after respawn, task.spawn/defer/delay misuse, retries, and reviewing module structure."
last_reviewed: 2026-10-14
sources:
  - https://luau-lang.org/
  - https://luau.org/library
  - https://create.roblox.com/docs/reference/engine/classes/ObjectValue
  - https://create.roblox.com/docs/reference/engine/classes/StringValue
  - https://create.roblox.com/docs/reference/engine/classes/CFrameValue
  - https://devforum.roblox.com/t/studio-beta-reference-instances-directly-with-attributes/4753441
  - https://raw.githubusercontent.com/Kampfkarren/kampfkarren-luau-guidelines/main/README.md
  - original
---

# Luau Patterns

## When to Load

Load for module shapes, resource ownership, scheduling, and failure contracts. See `roblox-luau-core` for semantics, `roblox-luau-types` for types, `roblox-architecture` for startup.

## Quick Reference

### Choose a shape

- **Plain functions:** default for stateless transformation or validation.
- **Module with private state:** one explicit subsystem owner. Do not create a manager class merely to namespace functions.
- **Object with metatable:** multiple independent values need shared behavior and lifecycle.
- **Existing library abstraction:** follow it when the project already uses it consistently. Do not add Promise, signal, cleanup, or framework dependencies for one call site.

Constructors use `.`, instance methods use `:`, and mutable fields belong on the instance, not the class table.

### Make ownership visible

Signal connections, instances, and tasks need cleanup owners. Disconnect/cancel at teardown. Export typed custom signal payloads (`Signal<T...>`).

Configure before parenting to hide partial state. Parent earlier only when ancestry is required; explain why. This does not guarantee replication ordering.

### Preserve failure semantics

```luau
local ok, value = pcall(dataStore.GetAsync, dataStore, key)
if not ok then
    return nil, `read failed: {value}`
end
return value, nil -- value may legitimately be nil
```

Do not collapse "call succeeded and returned nil" into "call failed." Retry only when the domain operation is safe to repeat. Persistence, HTTP, purchases, and remotes belong to their domain skills.

### Naming and return contracts

Practitioner conventions: mark yielding functions `Async`, keep return counts consistent, and prefer named module exports. Respect existing project contracts; details in full.md.

### Schedule deliberately

Use `task.defer`, `task.spawn`, `task.delay`, and `task.cancel` deliberately. Avoid legacy `wait()` and unjustified polling. Prefer a real state-change signal; otherwise choose and measure an explicit cadence.

### Review

Clear owner, narrow public API, no circular require, no accidental concurrent startup, success and missing-data states remain distinct, connections/tasks cleaned up, client input routed to `roblox-networking`.

> Details: [references/full.md](references/full.md)
