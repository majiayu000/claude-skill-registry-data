---
name: biome-gritql
description: Creates and manages Biome GritQL custom lint rules to enforce coding patterns. Use when creating linter rules, enforcing code conventions, preventing anti-patterns, or when the user mentions Biome, GritQL, custom lint rules, or AST-based linting.
allowed-tools:
  - Write
  - Read
  - Edit
  - Bash
  - Glob
---

# Biome GritQL Custom Lint Rules

Create AST-based custom lint rules using Biome's GritQL plugin system.

## Quick Start

Create a rule file (`rules/no-use-effect-fetch.grit`):

```gritql
`useEffect($callback, $deps)` where {
    $callback <: contains `fetch`,
    register_diagnostic(
        span = $callback,
        message = "Don't fetch inside useEffect. Use TanStack Query instead.",
        severity = "error"
    )
}
```

Add to `biome.json`:

```json
{
  "plugins": ["./rules/no-use-effect-fetch.grit"]
}
```

Run: `bunx biome check` or any equivalent command to run linter in the codebase

## GritQL Syntax

### Basic Pattern Matching

```gritql
`pattern_to_match` where {
    register_diagnostic(
        span = $matched_var,
        message = "Your message here",
        severity = "error"  // hint | info | warn | error
    )
}
```

make sure to read documentation

- [BiomeJS Documentation](https://biomejs.dev/)
- [Blog examples](https://laulau.land/context-window-ate-your-instructions/)
- [BiomeJS GitHub Repository](https://github.com/biomejs/biome)
- [GritQL GitHub Repository](https://github.com/biomejs/gritql)

### Variables

- `$name` - captures any single node
- `$args` - captures arguments
- `$_` - wildcard (match but don't capture)

### Operators

| Operator | Meaning |
|----------|---------|
| `<:` | matches / contains |
| `<: contains` | deep contains |
| `<: r"regex"` | regex match |
| `not` | negation |
| `and` | both conditions |
| `or` | either condition |

## Common Rule Patterns

### Ban a Function Call

```gritql
`console.log($args)` where {
    register_diagnostic(
        span = $args,
        message = "Remove console.log before committing",
        severity = "warn"
    )
}
```

### Ban a Hook (React)

```gritql
`useMemo($args)` where {
    register_diagnostic(
        span = $args,
        message = "useMemo unnecessary with React Compiler. Remove it.",
        severity = "warn"
    )
}
```

### Ban Dynamic Imports

```gritql
`await import($path)` where {
    register_diagnostic(
        span = $path,
        message = "Use static imports at the top of the file",
        severity = "error"
    )
}
```

### Require Pattern in Context

```gritql
`useState($initial)` where {
    not $initial <: contains `atom`,
    register_diagnostic(
        span = $initial,
        message = "Prefer Jotai atoms over useState for shared state",
        severity = "info"
    )
}
```

### CSS Rules

```gritql
language css;

`$selector { $props }` where {
    $props <: contains `color: $color` as $rule,
    not $selector <: r"\.color-.*",
    register_diagnostic(
        span = $rule,
        message = "Use .color-* utility classes instead of explicit colors"
    )
}
```

## Project Structure

```
project/
├── biome.json
└── rules/
    ├── no-console-log.grit
    ├── no-use-memo.grit
    ├── no-use-callback.grit
    ├── no-dynamic-import.grit
    └── no-fetch-in-effect.grit
```

## biome.json Configuration

```json
{
  "$schema": "https://biomejs.dev/schemas/2.0.0/schema.json",
  "plugins": [
    "./rules/no-console-log.grit",
    "./rules/no-use-memo.grit",
    "./rules/no-use-callback.grit"
  ],
  "linter": {
    "enabled": true
  }
}
```

## Creating Rules Workflow

1. Identify the pattern to ban/enforce
2. Create `.grit` file in `rules/` directory
3. Write the GritQL pattern with clear error message
4. Add path to `biome.json` plugins array
5. Test with `bunx biome check` or any equivalent command to run linter in the codebase

## Guidelines

- Keep error messages actionable - tell the user what to do instead
- Use `severity = "error"` for hard requirements, `"warn"` for preferences
- Put all `.grit` files in a `rules/` directory
- Name files descriptively: `no-X.grit` or `prefer-Y.grit`
- Test rules against real code before committing

## Why This Matters

Instructions in CLAUDE.md degrade as context fills up. Linter rules provide immediate, persistent feedback. When Claude violates a pattern, it sees the error and self-corrects - no context drift.


# Resources 

- [BiomeJS Documentation](https://biomejs.dev/)
- [Blog examples](https://laulau.land/context-window-ate-your-instructions/)
- [BiomeJS GitHub Repository](https://github.com/biomejs/biome)
- [GritQL GitHub Repository](https://github.com/biomejs/gritql)
