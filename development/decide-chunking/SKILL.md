---
name: decide-chunking
description: When and how to process large datasets. Memory-efficient iteration.
---

# Skill: Chunking

> "Memory is finite. Chunk accordingly."

## The Decision

| Method             | Use when                                        | Because                                            |
|--------------------|-------------------------------------------------|----------------------------------------------------|
| `chunk()`          | Read and process in a callback, no writes       | Offsets stay stable while the rows do              |
| `chunkById()`      | The callback updates or deletes the rows        | Offset paging skips rows the moment you mutate them |
| `cursor()`/`lazy()`| Read-only streaming — exports, reports          | One row in memory, no callback                     |
| `lazyById()`       | Streaming *and* mutating                        | Lazy iteration with the `chunkById()` guarantee    |

## The Heuristic

Ask: *"Am I modifying records during iteration?"*

- **Yes** → `chunkById()`
- **No, need callback** → `chunk()`
- **No, just streaming** → `cursor()`

## The Anti-Patterns

| ❌ Don't                                | ✅ Do                              | Why                                              |
|----------------------------------------|-----------------------------------|--------------------------------------------------|
| Break a chain into a temp per stage "for memory" | Break a chain only for readability | Every temp stays pinned for the scope's lifetime — measurably the *worst* variant, not the fix |

Break a chain for readability, never for memory. The memory lever is eager-vs-lazy — `lazy()`, `cursor()`, a builder chain — not syntax.

## Real-World Examples

For concrete examples from this codebase, see [examples.md](examples.md).
