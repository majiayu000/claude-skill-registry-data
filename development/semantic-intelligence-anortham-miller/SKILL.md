---
name: semantic-intelligence
description: Use Miller's semantic search capabilities for conceptual code understanding. Activates when searching for concepts, cross-language patterns, business logic, or exploring unfamiliar code. Combines text and semantic search for optimal results.
allowed-tools: mcp__miller__fast_search, mcp__miller__fast_explore, mcp__miller__trace_call_path, mcp__miller__get_symbols
---

# Semantic Intelligence Skill

## Activation Announcement

**IMPORTANT**: When this skill activates, ALWAYS start your response with:

```
🧠 **Semantic Intelligence Active**
Using conceptual code understanding for cross-language discovery...
```

This provides a visual indicator to the user that the skill is running.

## Purpose
Leverage Miller's **semantic understanding** to find code by concept, not just keywords. Goes beyond text matching to understand what code does.

## When to Activate
- Searching for concepts ("authentication logic")
- Finding cross-language patterns
- Discovering business logic
- Exploring unfamiliar codebases
- When text search returns nothing
- Understanding execution flows

## Semantic vs Text Search

**Text Search** (exact/wildcard matching):
```
fast_search({ query: "console.error", method: "text" })
-> Fast (<10ms)
-> Exact matches only
-> Misses variations ("logger.error", "print_error")
```

**Semantic Search** (conceptual understanding):
```
fast_search({ query: "error logging", method: "semantic" })
-> Slower (~100ms)
-> Finds concepts
-> Discovers: console.error, logger.error, logging.error, errorHandler
-> Cross-language: Python logging, Rust tracing, Go log
```

**Hybrid Search** (best of both):
```
fast_search({ query: "authentication", method: "hybrid" })
-> Runs text + semantic in parallel
-> Fuses results intelligently
-> Boosts symbols in BOTH searches
-> Optimal: ~150ms
```

## When to Use Each Mode

### Use Text Mode When:
- Searching for specific API names
- Finding exact strings
- Speed critical (<10ms)
- You know exact symbol name

```
Examples:
- "getUserData" -> find specific function
- "console.log" -> find exact API usage
- "import React" -> exact import statement
- "TODO: fix" -> exact comment
```

### Use Semantic Mode When:
- Searching for concepts
- Cross-language patterns
- Don't know exact names
- Understanding what code does

```
Examples:
- "authentication logic" -> find ALL auth-related code
- "error handling" -> discover error patterns
- "database connections" -> find DB code (MySQL, Postgres, etc.)
- "payment processing" -> business logic discovery
```

### Use Hybrid Mode When:
- Not sure which mode is best
- Want comprehensive results
- Concept + exact matches both useful

```
Examples:
- "user authentication" -> concept + exact matches
- "API endpoints" -> finds routes, handlers, controllers
- "validation logic" -> semantic concept + exact validators
```

## Search Strategy Decision Tree

```
Know exact symbol name?
  YES -> fast_search with method="text" or get_symbols with target
        -> <10ms, exact matches

Know exact API/string?
  YES -> fast_search({ method: "text" })
        -> <10ms, exact matches

Searching for concept/behavior?
  YES -> fast_search({ method: "semantic" })
        -> ~100ms, conceptual understanding

Not sure / want comprehensive?
  YES -> fast_search({ method: "hybrid" })
        -> ~150ms, text + semantic fused
```

## Cross-Language Semantic Matching

**Miller's Superpower:** Finds similar code across languages

```
Example: Finding "user validation" across codebase

fast_search({
  query: "user input validation",
  method: "semantic",
  limit: 20
})

Results discovered:
- TypeScript: validateUser(input: UserInput)
- Python: def validate_user_input(data: dict)
- Rust: fn validate_user(user: &User) -> Result
- Go: func ValidateUserInput(input *UserInput) error

-> Same CONCEPT, different languages
-> Naming variants automatically understood
```

**Why this works:** Embeddings encode *what code does*, not just *what it's called*

## Execution Flow Tracing (Cross-Language)

**Unique capability:** Trace calls across language boundaries

```
trace_call_path({
  symbol_name: "processPayment",
  direction: "downstream",
  max_depth: 3
})

Execution flow discovered:
TypeScript: processPayment()
  -> Rust: payment_processor::process()
    -> SQL: stored_proc_charge()

-> Semantic matching finds cross-language connections
-> No other tool does this
```

## Key Behaviors

### DO
- Use semantic search for concepts and behaviors
- Use text search for exact API/symbol names
- Use hybrid when uncertain (comprehensive)
- Trace execution flows cross-language
- Combine multiple search modes for completeness

### DON'T
- Use semantic for exact symbol names (use text)
- Use text search for concepts (misses variations)
- Ignore hybrid mode (often best choice)
- Skip cross-language tracing (unique capability)
- Search without strategy (use decision tree)

## Success Criteria

This skill succeeds when:
- Concepts found across languages
- Business logic discovered efficiently
- Execution flows traced completely
- Right search mode used for query type
- Cross-language patterns identified
- Unfamiliar code understood quickly
