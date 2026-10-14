---
name: ground-topic
description: Isolate yourself. One branch, one memory.
---

# Skill: Topic

> "One topic, one branch, one memory."

## When

Run at session start. Referenced by recite hook on protected branches.

## The Protocol

1. **Detect** current git branch
2. **Resolve** memory path -> `.claude/memory/<branch>/`
3. **No memory?** Prompt to scaffold from templates

## The Anti-Patterns

- **Working on main**: Topics mix. Goals drift. Create a branch.
- **Skipping init**: No memory = cold start every session.

## The Output

**Feature branch:**
```
Topic: `<branch>`. Memory: `.claude/memory/<branch>/`
```

**Protected branch:**
```
Topic: `<branch>`. (Protected -- branch before implementing)
```

When implementation is requested on a protected branch, prompt for topic branch. Otherwise, exploration is fine.
