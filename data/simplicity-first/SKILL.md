---
name: Simplicity First
description: This skill should be used when the user asks to "implement", "build", "create", "add feature", "develop", "design", "architect", "plan", "structure", "refactor", "improve", "optimize", "fix", "solve", "handle", "choose between", "which approach", or discusses implementation strategies. Apply this philosophy to ALL development work as a cornerstone principle.
version: 1.0.0
---

# Simplicity First: The Cornerstone Development Philosophy

## Core Principle

**YAGNI (You Aren't Gonna Need It) is the supreme design principle.** It supersedes single-responsibility, DRY, clean architecture, and tool selection concerns. When in conflict, simplicity wins.

Great software design looks underwhelming. The observable difference between clever design and simple design is that simple solutions remain maintainable despite unknown future conditions—because they remain fundamentally understandable.

## The Simplicity Mindset

Real mastery involves learning when to do **less**, not more. Complexity is easy to add; true expertise is knowing what to leave out.

### What Simplicity IS

- Fewer moving parts requiring cognitive overhead
- Components with clear, straightforward interfaces
- Minimal internal connections between systems
- Stability across time without ongoing maintenance (if requirements stay unchanged)
- Solutions that fit entirely in working memory
- Boring, proven technology over cutting-edge alternatives

### What Simplicity IS NOT

- Quick hacks or kludges (these ADD complexity through hidden maintenance burden)
- Taking shortcuts that require "remembering" special behaviors
- Incomplete solutions that defer complexity to users
- Ignoring error cases (handle them simply, not elaborately)

## Decision Heuristics

Before implementing anything, ask these questions in order:

### 1. Do We Actually Need This?

Challenge assumptions about requirements. Often the existing system already solves the problem:
- Does the edge proxy already handle rate limiting?
- Does the framework already provide this validation?
- Is this "requirement" actually used in practice?

### 2. What's the Simplest Solution That Works?

Start with the most straightforward approach:
- In-memory before persistent storage
- Single process before distributed systems
- Direct code before abstractions
- Built-in features before external dependencies
- Boring technology before novel solutions

### 3. What Are We Actually Solving For?

Design for current requirements, not imagined futures:
- Current traffic, not 100x traffic
- Current team size, not future team size
- Current features, not speculative features
- Known problems, not anticipated problems

### 4. Does This Add Coordination Cost?

Every abstraction adds cognitive overhead:
- Does this require understanding another system?
- Does this add a network hop?
- Does this require synchronization?
- Does this make debugging harder?

## Implementation Guidelines

### Layer Solutions Progressively

When building features, start simple and add complexity only when genuinely necessary:

```
Level 1: In-memory / direct code
    ↓ (only if proven insufficient)
Level 2: Local persistence / simple abstraction
    ↓ (only if proven insufficient)
Level 3: Distributed / external service
```

**Example - Rate Limiting:**
1. First: In-memory counter with process-local tracking
2. Only if horizontal scaling demands it: Add Redis
3. Never start at Redis because "we might need it"

### Avoid Premature Architecture

Common over-engineering patterns to reject:

| Don't Do This | Do This Instead |
|---------------|-----------------|
| Abstract "for reusability" with one use case | Write direct code |
| Add configuration for hypothetical needs | Hardcode current values |
| Create service layers before needed | Call functions directly |
| Design for 10x scale on day one | Design for current scale |
| Add caching "just in case" | Profile first, cache proven hotspots |
| Build plugin systems for one plugin | Write the plugin inline |

### Embrace Boring Solutions

The best solution is often the most boring one:
- REST over GraphQL (unless you have proven pagination/federation needs)
- PostgreSQL over specialized databases (it handles 95% of cases)
- Server-rendered HTML over SPA (unless genuine interactivity demands it)
- Monolith over microservices (until team scale demands separation)
- Cron jobs over message queues (for non-critical async work)

### Delete Before Adding

When changing code:
- Remove unused code rather than commenting it out
- Delete old abstractions when consolidating
- Remove feature flags after features ship
- Clear out backwards-compatibility code after migrations complete

## Recognizing Over-Engineering

Watch for these signals that a solution is too complex:

**Code Smells:**
- More than 3 levels of abstraction for simple operations
- Configuration files longer than the code they configure
- "Infrastructure" code exceeding business logic code
- Tests that are harder to understand than the code they test
- Interfaces with single implementations (unless clear extension point)

**Architecture Smells:**
- Services that only wrap other services
- Message queues for synchronous-feeling operations
- Caches without measured performance problems
- "Platform" code written before the first use case

**Process Smells:**
- Design documents longer than the implementation
- Multiple approval layers for simple changes
- "Future-proofing" discussions without concrete requirements

## When Complexity IS Warranted

Complexity is justified when:
- The simple solution has been tried and proven insufficient
- Requirements genuinely demand it (not "might someday demand it")
- The complexity cost is smaller than the problem it solves
- The team has capacity to maintain the added complexity

Before adding complexity, ask: "Would I bet $1000 that we'll need this in the next 6 months?"

## Applying This Philosophy

When implementing any feature:

1. **Start by understanding the actual requirement** - not the imagined future requirement
2. **Look for existing solutions** - frameworks, libraries, built-in features
3. **Propose the simplest approach first** - even if it feels "too simple"
4. **Add complexity only when the simple approach fails** - with evidence
5. **Delete unnecessary code** - past abstractions, unused features, dead paths

When reviewing or refactoring code:

1. **Identify unnecessary abstraction layers** - collapse them
2. **Find coordination points that could be eliminated** - inline or simplify
3. **Look for "just in case" code** - remove it
4. **Check for over-configuration** - hardcode stable values
5. **Question external dependencies** - can built-in features suffice?

## Reference

For detailed patterns, anti-patterns, and technology-specific guidance, consult:
- **`references/design_guide.md`** - Comprehensive examples, layered solutions, and specific anti-patterns

---

*"It is not easy to do the simplest thing that could possibly work. It requires deeply understanding the existing system and having enough knowledge to identify the right approach. Great software design looks underwhelming because complexity has been stripped away, not added."*
