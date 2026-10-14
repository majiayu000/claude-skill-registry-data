---
name: decide-streaming
description: When to stream vs chunk vs load all. Memory vs complexity.
---

# Skill: Streaming vs Chunking

> "Memory is cheap until it isn't."

## The Decision

**Load All when:**
- Dataset fits comfortably in memory (<10K records)
- Need random access or multiple passes
- Simplicity matters more than memory

**Chunk when:**
- Processing in batches (1K-10K per batch)
- Database operations (insert/update batches)
- Can tolerate batch boundaries

**Stream when:**
- Dataset size unknown or very large (100K+)
- Processing row-by-row is natural
- Memory is constrained

## The Heuristic

Ask: *"What happens if the dataset 10x in size?"*

## The Quick Test

| Ask | Answer | Use |
|-----|--------|-----|
| Will it always be <1K records? | Yes | Load all |
| Processing in batches of N? | Yes | Chunk |
| Could be millions of records? | Yes | Stream |
| Need all data at once for calculation? | Yes | Load all |

## Real-World Examples

See [examples.md](examples.md).
