---
name: workflow-methodology
description: Core development methodology for claude-flow. Enforces TDD (test-first), systematic debugging (4-phase), and verification gates. Use when starting any development task, fixing bugs, or completing features.
---

# Claude-Flow Development Methodology

## The 5 Iron Laws

### 1. TDD Iron Law
**"NO production code without a failing test first"**

```
RED → GREEN → REFACTOR
```

- Write ONE failing test
- Implement MINIMAL code to pass
- Refactor while tests pass
- Commit at each green

### 2. Verification Law
**"Evidence before claims, always"**

Before claiming ANY task complete:
- Run fresh tests (not cached)
- Read complete output
- Confirm exit code 0
- Verify original symptom fixed

### 3. Debugging Law
**"Root cause before fix attempts"**

4-Phase Protocol:
1. **Investigate** - Reproduce, read errors, check recent changes
2. **Analyze** - Find working examples, compare patterns
3. **Hypothesize** - Test ONE change at a time, max 3 attempts
4. **Implement** - TDD the fix after understanding

### 4. Planning Law
**"Plans executable with zero context"**

Plans must include:
- Exact file paths
- Complete code examples
- Verification commands
- No assumptions about reader knowledge

### 5. Isolation Law
**"Isolated workspace for each feature"**

Use git worktrees:
```bash
git worktree add .worktrees/feature-name -b feature/feature-name
```

## Red Flags (STOP immediately)
- Writing code before tests
- Tests passing immediately
- Multiple simultaneous changes
- "Just this once" thinking
- Using "should," "probably," "seems to"
- Third fix attempt failed

## Thinking Budget
| Keyword | Tokens | Use For |
|---------|--------|---------|
| `think` | ~4k | Simple tasks |
| `think hard` | ~10k | Debugging |
| `think harder` | ~20k | Complex changes |
| `ultrathink` | ~32k | Architecture |
