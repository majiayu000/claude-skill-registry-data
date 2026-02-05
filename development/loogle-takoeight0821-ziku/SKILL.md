---
name: loogle
description: Search for Lean 4 and Mathlib theorems, lemmas, and definitions by type signature, name, or subexpression pattern. Use when the user asks to find a theorem, look up a Lean definition, search for lemmas, or needs help discovering Mathlib functions.
---

# Loogle - Lean/Mathlib Search

Search for Lean 4 and Mathlib declarations using the Loogle API.

## How to Search

Use WebFetch to query the Loogle JSON API:

```
https://loogle.lean-lang.org/json?q=<URL-encoded-query>
```

## Query Syntax

| Type | Syntax | Example |
|------|--------|---------|
| By constant | `ConstantName` | `List.map` |
| By name substring | `"text"` | `"differ"` |
| By subexpression | `_ * (_ ^ _)` | Pattern matching |
| By type signature | `(?a -> ?b) -> List ?a -> List ?b` | Type search |
| By conclusion | `|- goal` | `|- tsum _ = _` |
| Combined | `filter1, filter2` | AND logic |

## Response Handling

**Success response:**
- `count`: Total matches found
- `hits`: Array of results (max 200)
  - `name`: Declaration name
  - `type`: Type signature
  - `module`: Source module
  - `doc`: Documentation (may be null)

**Error response:**
- `error`: Error message
- `suggestions`: Array of suggested corrections

When presenting results, show the declaration name, type signature, and module. Include documentation if available.

## Example Queries

- Find list functions: `List, ?a -> ?b`
- Search by name: `"append"`
- Type signature: `Nat -> Nat -> Bool`
- Parsec functions: `Std.Internal.Parsec`
- Option operations: `Option, "map"`
