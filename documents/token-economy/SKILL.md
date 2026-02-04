---
name: token-economy
description: Apply token optimization when writing docs, changelogs, MCP tasks. Quality #1, Tokens #2.
allowed-tools: Read, Edit, Grep
---

# Token Economy

Optimize text for AI context: docs, changelogs, MCP tasks, subtasks.

**Principle**: Quality first. Never sacrifice essential info.

## 15 Techniques

| # | Technique | Use | Example |
|---|-----------|-----|---------|
| 1 | Tables over prose | Comparisons | Function params → table |
| 2 | Bullets with pipes | Multi-part | `Part1 \| Part2 \| Part3` |
| 3 | Numbered steps | Workflows | `1. Step → 2. Step` |
| 4 | One example | Code samples | Keep best, remove rest |
| 5 | Pattern statements | Repetition | `**Pattern**: All X do Y` |
| 6 | Add "Why" | Decisions | `**Why**: [reason]` |
| 7 | Concrete errors | Debugging | `**Error**: \`exact message\`` |
| 8 | No fluff | Decorations | Remove ASCII art, emojis |
| 9 | Scannable | Structure | Headers, bullets, tables |
| 10 | Consolidate | Duplicates | Merge similar sections |
| 11 | Compact code | Examples | 3-5 key lines only |
| 12 | Quick lists | Reference | Command/param tables |
| 13 | Inverted pyramid | Info order | Critical → Details → Context |
| 14 | Conditional verbosity | Complexity | High for complex, low for simple |
| 15 | No teaching | Reference | State facts, skip basics |

## Quick Workflow

1. **Identify**: Prose → tables? Multiple examples → one? ASCII → numbered? Teaching → facts?
2. **Apply**: Convert, consolidate, compact
3. **Check**: Essential info preserved? Scannable? No fluff?

## MCP Templates

**Task**:
```
Requirements: [WHAT] | Files: [PATH:LINES] (action) | Acceptance: [CRITERIA] | Why: [CONTEXT]
```

**progress_notes**: `[ACTION] [WHAT]. [NEXT]`

**completion_summary**: `[DONE]. [TECH]. Files: [PATHS]. [IMPACT]`

## Examples

**Before** (prose):
```
This function validates user input. Takes string input_text, returns bool.
If valid returns true, otherwise false. Checks empty, special chars, length ≤100.
```

**After** (compact):
```
**validate_input(input_text: str) → bool**: True if valid (non-empty, no special chars, ≤100)
```

**Before** (ASCII art - 180 tokens):
```
┌─────────┐
│  Auth?  │
└────┬────┘
     ▼
┌─────────┐
│ Valid?  │
└──┬───┬──┘
   Y   N
```

**After** (numbered - 36 tokens):
```
1. Check auth
2. Valid → YES: Process | NO: Reject
```

## Common Fixes

| Issue | Fix |
|-------|-----|
| Multiple examples | Keep 1 (#4) |
| Prose comparison | Table (#1) |
| Teaching | Facts only (#15) |
| ASCII art | Numbered (#3) |
| No "why" | Add context (#6) |

See [TEMPLATES.md](TEMPLATES.md) for copy-paste templates.
