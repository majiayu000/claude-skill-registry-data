---
name: applying-code-principles
description: >
  Fundamental software principles - SOLID, DRY, Occam's Razor, Miller's Law, YAGNI.
  Triggers: 原則, シンプル, 複雑, アーキテクチャ, リファクタリング, 保守性, コード品質,
  design pattern, best practice, clean code
allowed-tools: Read, Grep, Glob
---

# Code Principles

Claude knows all principles. This file defines project-specific thresholds and priority.

## Priority Order

When principles conflict:

1. **Safety First** - Security, data integrity
2. **YAGNI** - Don't build what you don't need
3. **Occam's Razor** - Simplest solution
4. **SOLID** - For complex systems
5. **DRY** - Eliminate duplication (not at cost of clarity)
6. **Miller's Law** - Respect 7±2 cognitive limit

## Quick Decision Questions

- "Is there a simpler way?" (Occam's Razor)
- "Understandable in <1 min?" (Miller's Law)
- "Duplicating knowledge?" (DRY)
- "Needed now?" (YAGNI)
- "Single reason to change?" (SOLID/SRP)

## Thresholds

### Miller's Law

| Target | Ideal | Max | Limit |
| --- | --- | --- | --- |
| Function args | 3 | 5 | 7 |
| Class methods | 5 | 7 | 9 |
| Conditionals | 3 | 5 | 7 |

### DRY

- **Rule of Three**: Abstract on 3rd duplication

### SOLID

- Create interface only when 2nd implementation appears
- No single-implementation interfaces

### YAGNI

Before adding, confirm:

1. Problem exists now? → No = don't build
2. Failed in production? → No = no error handling yet
3. User requested? → No = no feature yet
4. Measured evidence? → No = no optimization yet
