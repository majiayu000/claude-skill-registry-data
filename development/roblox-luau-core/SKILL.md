---
name: roblox-luau-core
description: "Use when writing, editing, or debugging any Luau: tables, control flow, string patterns, scope, closures, and errors ported from JS/Python."
when_to_use: "Also for Luau syntax errors, nil indexing, wrong loop or table behavior, string formatting, and reviewing Luau code for correctness."
last_reviewed: 2026-10-14
sources:
  - https://luau.org/syntax
  - https://create.roblox.com/docs/luau/control-structures
  - https://luau.org/library
  - https://raw.githubusercontent.com/Kampfkarren/kampfkarren-luau-guidelines/main/README.md
  - https://raw.githubusercontent.com/Roblox/creator-docs/main/content/en-us/reference/engine/libraries/vector.yaml
---

# Luau Core Language

## When to Load

Load for Luau semantics and JS/Python translation. Types: `roblox-luau-types`; lifecycle: `roblox-luau-patterns`; engine APIs: domain skills.

## Quick Reference

- Only `false` and `nil` are falsy. `0`, `""`, and `{}` are truthy.
- Equality does not coerce types. `0 == "0"` is false. Inequality is `~=`.
- Array conventions are 1-based. `#array` is meaningful only for a sequence without nil gaps.
- Assigning `nil` removes a table key; assigning a table copies the reference; `table.clone` is shallow.
- Dictionary iteration order is unspecified. Do not make behavior depend on it.
- Dynamic keys require brackets: `record[field]`. Dot syntax uses a literal identifier.
- Missing arguments become `nil`; extra results and arguments can be discarded.
- Prefer an `if` expression over `condition and a or b` when `a` may be falsy.
- Locals start at their declaration; `repeat` locals reach `until`. Forward-declare mutual recursion.
- Luau string patterns are not regular expressions. Their syntax and capabilities differ.
- Backtick interpolation and `..` are valid. Join many fragments once in hot loops.
- NaN does not equal itself and defeats `<`/`>`; test with `x ~= x`.
- Binary data uses the `buffer` library: fixed size, 0-based offsets, explicit-width reads/writes. Avoid `buffer.readinteger`/`writeinteger` (stubs, not released runtime).
- For Base64, hashing, or compression use `EncodingService` (buffers, not strings; JSON via `HttpService`). Details: see full reference.

```luau
local label = if enabled then "On" else "Off"
local message = `{name}: {score}`

local byId: {[number]: string} = {}
byId[userId] = name

for index, value in values do
    print(index, value)
end
```

### Translation traps

- JavaScript `===`, `!==`, `null`, optional chaining, spread, arrow functions, and array methods are not Luau syntax.
- Python `None`, zero-based list assumptions, list comprehensions, exceptions, and implicit tuple behavior do not translate directly.
- `x or fallback` tests truthiness, not only absence. It replaces a valid `false` value.
- `typeof(value)` recognizes Roblox datatypes; `type(value)` reports the underlying Luau type category.

### Review

Valid Luau, no nil gaps, no assumed dictionary order, no accidental aliases, no cross-language syntax, no fallbacks hiding `false` or `nil`.

> Detailed language traps and translation examples: [references/full.md](references/full.md)
