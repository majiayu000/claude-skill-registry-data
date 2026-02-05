---
name: improve
description: Soul self-improvement loop. Use after introspection reveals targets, or to act on evolution insights.
---

# Soul Self-Improvement

You are improving yourself. This means actually changing code, not logging intentions.

## The Loop

```
INTROSPECT → see clearly → REASON about fix → IMPLEMENT → VERIFY → LEARN
```

## Process

### 1. Identify the Target

What specifically needs improving? Sources:
- Output from `/introspect`
- Repeated friction or pain
- Belief-action misalignment
- Wisdom that isn't being applied

Be concrete: "The coherence calculation is wrong" not "things could be better"

### 2. Understand Before Changing

```
Read the relevant code files directly
mcp__cc-memory__mem-recall(query="related past fixes")
```

Ask: Why does it work this way? What was the original intent?

### 3. Reason About the Fix

Before writing code:
- What's the root cause, not just the symptom?
- What's the simplest change that fixes it?
- What could break?
- How will I verify it works?

### 4. Implement

Make the actual changes using Edit/Write tools. Keep changes minimal and focused.

### 5. Verify

- Run tests if they exist
- Manually verify the behavior changed
- Check for regressions

### 6. Record the Learning

```
mcp__cc-memory__mem-remember(
    category="bugfix" | "refactor" | "feature",
    title="What was fixed",
    content="Root cause, solution, and why it works"
)
```

## Categories

| Type | When | Example |
|------|------|---------|
| **bugfix** | Broken behavior | "Coherence returned NaN" |
| **refactor** | Structure improvement | "Extracted common pattern" |
| **feature** | New capability | "Added pain point tracking" |
| **cleanup** | Remove cruft | "Deleted unused code" |

## Principles

- **Actually fix it** — Don't log "we should fix X". Fix X.
- **Minimal changes** — The best fix touches the least code
- **Understand first** — Read before writing
- **Verify always** — Untested fixes aren't fixes
- **Record learnings** — Future-you needs to know why

## When to Use

- After `/introspect` reveals a clear target
- When friction keeps recurring
- When behavior contradicts beliefs
- Proactive maintenance

## Anti-Patterns

- Creating proposals without implementing them
- Improving hypothetical future problems
- Refactoring without a specific goal
- Big changes when small ones suffice

## Remember

Self-improvement is action, not intention. If you didn't change code and verify it works, you didn't improve.
