---
name: vertical-slice-planning
description: Use this skill when discussing feature breakdown, PR structure, implementation ordering, or how to decompose work. Guides thinking about vertical slices (end-to-end functionality) rather than horizontal layers (all of one layer first). Triggers on "how should we break this down?", "what order should we implement?", "how many PRs?", or decomposition discussions.
---

# Vertical Slice Planning Skill

This skill guides the decomposition of features into vertical slices - thin, end-to-end pieces of functionality that can be shipped independently.

## When to Use

Apply this skill when:
- Breaking down a feature into Subtasks
- Deciding implementation order for a feature
- Planning PR structure for a feature
- Users ask "how should we break this down?"
- Discussing what to build first
- Reviewing feature decomposition plans

## What is a Vertical Slice?

A vertical slice cuts through ALL layers of the application to deliver a thin piece of complete functionality.

```
┌─────────────────────────────────────────┐
│              HORIZONTAL LAYERS           │
├─────────────────────────────────────────┤
│  UI Layer      │ █ │     │     │        │
├────────────────┼───┼─────┼─────┼────────┤
│  API Layer     │ █ │     │     │        │
├────────────────┼───┼─────┼─────┼────────┤
│  Service Layer │ █ │     │     │        │
├────────────────┼───┼─────┼─────┼────────┤
│  Data Layer    │ █ │     │     │        │
└────────────────┴───┴─────┴─────┴────────┘
                  ↑
            Vertical Slice
         (Complete feature)
```

## Vertical vs Horizontal

### Horizontal Approach (Avoid)
Building all of one layer before moving to the next.

**Problems:** Nothing works until everything is done, late integration issues.

### Vertical Approach (Prefer)
Building thin, complete features:
1. User can view empty product list (UI → API → DB)
2. User can add a product (UI → API → DB)
3. User can edit a product (UI → API → DB)

**Benefits:** Each slice is shippable, visible progress, early feedback.

## Naming Convention for Jira Subtasks

Since Jira Subtasks are flat (no nesting), use prefixes:
```
SLICE 1: Basic product list display
SLICE 1.1: Add product image support
SLICE 2: Product search functionality
REFACTOR: Extract shared product utils
TEST: Integration tests for product API
```

## Slice Sizing Guidelines

| Size | Indicators |
|------|------------|
| **Too Big** | Multiple user actions, >2 days work, many acceptance criteria |
| **Too Small** | Just infrastructure, just types, <1 hour work |
| **Just Right** | One capability, 1-2 days, 3-5 acceptance criteria |

## Integration with Jira Workflow

When creating Jira Stories:
- Parent Story = Full feature context
- Subtasks = Vertical slices (potential PRs)

Each Subtask should be independently deployable, testable, and valuable.

Remember: **Ship working software frequently. Slices make this possible.**
