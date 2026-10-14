---
name: decide-pipelines
description: When to use Laravel Pipelines vs sequential calls. Flow decisions.
---

# Skill: Pipelines

> "Pipelines are for transformations. Actions are for operations."

## The Decision

**Use Pipeline when:**
- Data flows through sequential transformations
- Steps are interchangeable/configurable
- Each step enriches the same payload
- 3+ steps in sequence

**Use Sequential Calls when:**
- Steps have strong dependencies on each other
- Control flow (if/else) needed between steps
- Less than 3 steps
- Steps don't share a common payload

## The Heuristic

Ask: *"Am I transforming a payload, or orchestrating operations?"*

- **Transforming** → Pipeline
- **Orchestrating** → Action composition

## The Quick Test

| Ask Yourself                     | Answer | Use      |
|----------------------------------|--------|----------|
| 3+ sequential steps?             | Yes    | Pipeline |
| Steps reorderable?               | Yes    | Pipeline |
| Needs if/else between steps?     | Yes    | Actions  |
| Steps need each other's methods? | Yes    | Actions  |

## Real-World Examples

For concrete examples, see [examples.md](examples.md).
