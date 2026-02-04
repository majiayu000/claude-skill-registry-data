---
name: ast-grep
description: Search code using Abstract Syntax Tree patterns with ast-grep. Use when finding code structures, bug patterns, or refactoring candidates that depend on syntax rather than text.
allowed-tools: Bash, Read, Glob
---

# ast-grep - Structural Code Search

ast-grep searches code by matching AST patterns, not text. This finds code based on structure regardless of formatting or variable names.

## Basic Usage

```bash
ast-grep run -p 'PATTERN' -l LANGUAGE
```

## Pattern Syntax

- `$VAR` - Match any single node (like a wildcard)
- `$$$` - Match zero or more nodes
- Literal code matches itself

## Common Patterns

| Goal | Pattern | Language |
|------|---------|----------|
| Find subtraction with specific left operand | `discount - $VAR` | typescript |
| Find all useEffect with empty deps | `useEffect($FN, [])` | tsx |
| Find console.log calls | `console.log($$$)` | typescript |
| Find async functions | `async function $NAME($$$) { $$$ }` | typescript |

## Example: Finding Reversed Operands

To find where `discount` appears on the left side of subtraction:

```bash
ast-grep run -p 'discount - $VAR' -l typescript
```

This would find bugs like `discount - basePrice` (should be `basePrice - discount`).

## When to Use

- Finding bug patterns based on code structure
- Locating specific API usage patterns
- Identifying refactoring candidates
- Searching for security anti-patterns
