---
name: memory
description: State tracking, semantic cache, memory compaction, and agent histories.
---

# Memory

State tracking, semantic cache, memory compaction, and agent histories.

## Core Guidelines

- **Memory Compaction**: Summarize long histories periodically to free token budget space.
- **Semantic Caches**: Cache frequent query responses in a local database for fast retrieval.
- **State Serialization**: Save and restore agent graph states safely.
