---
name: parallel-exploration
description: Use when researching unfamiliar code, multiple modules involved, or external libraries referenced
---

# Parallel Exploration

Fire search agents in parallel. Never wait sequentially when searches are independent.

## Tool Selection

| Tool | Cost | When to Use |
|------|------|-------------|
| `grep`, `glob`, `lsp_*`, `ast_grep` | FREE | Scope clear, single pattern, known location |
| `tracer` agent | FREE | Multiple search angles, unfamiliar modules, cross-layer patterns |
| `rocket` agent | CHEAP | External docs, GitHub examples, OSS reference |
| `oracle` agent | EXPENSIVE | Architecture decisions, debugging after 2+ failures |

## Tracer = Contextual Grep (Internal)

Use for searching YOUR codebase:

| Use Direct Tools | Use Tracer |
|------------------|------------|
| Exact pattern known | Multiple search angles needed |
| Single keyword suffices | Unfamiliar module structure |
| Known file location | Cross-layer pattern discovery |

## Rocket = Reference Grep (External)

Use for searching EXTERNAL resources:

- Official API documentation
- Library best practices
- OSS implementation examples
- GitHub examples

**Trigger phrases** (fire rocket immediately):
- "How do I use [library]?"
- "What's the best practice for [framework feature]?"
- Working with unfamiliar packages

## Parallel Execution Pattern

```typescript
// CORRECT: Fire and continue
background_task(agent="tracer", prompt="Find auth implementations...")
background_task(agent="tracer", prompt="Find error handling patterns...")
background_task(agent="rocket", prompt="Find JWT best practices...")
// Continue working immediately

// WRONG: Sequential blocking
result = task(...)  // Never wait synchronously
```

## Result Collection

1. Launch parallel agents → receive task_ids
2. Continue immediate work
3. When results needed: `background_output(task_id="...")`
4. BEFORE final answer: `background_cancel(all=true)`

## Stop Conditions

STOP searching when:
- Enough context to proceed confidently
- Same information appearing across multiple sources
- 2 iterations yielded no new useful data
- Direct answer found

**DO NOT over-explore. Time is precious.**
