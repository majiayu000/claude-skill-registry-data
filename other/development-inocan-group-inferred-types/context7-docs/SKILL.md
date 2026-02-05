---
name: context7-docs
description: Documentation lookup using Context7 MCP server. Use when needing up-to-date documentation for any library, crate, framework, or API. Always use this for Rust crates, npm packages, Python libraries, or any external dependency documentation.
allowed-tools: Read, Bash, Grep, Glob
---

# Context7 Documentation Lookup

Use the Context7 MCP tools to fetch accurate, up-to-date documentation for any library.

## Process

### Step 1: Resolve Library ID

First, find the Context7-compatible library ID:

```
Use tool: mcp__plugin_context7_context7__resolve-library-id
Parameter: libraryName = "<library name>"
```

Examples:
- For tokio: `libraryName = "tokio"`
- For serde: `libraryName = "serde"`
- For React: `libraryName = "react"`
- For Express: `libraryName = "express"`

### Step 2: Fetch Documentation

After getting the library ID, fetch documentation:

```
Use tool: mcp__plugin_context7_context7__get-library-docs
Parameters:
  - context7CompatibleLibraryID = "<id from step 1>"
  - topic = "<specific topic>" (optional)
  - mode = "code" or "info"
```

**Modes:**
- `code` (default): API references, code examples, function signatures
- `info`: Conceptual guides, architecture, narrative documentation

### Step 3: Paginate if Needed

If documentation is incomplete, fetch more pages:

```
Use tool: mcp__plugin_context7_context7__get-library-docs
Parameters:
  - context7CompatibleLibraryID = "<same id>"
  - topic = "<same topic>"
  - page = 2  (or 3, 4, etc.)
```

## Common Lookup Patterns

### Rust Crates

```
# Tokio async runtime
resolve-library-id: "tokio"
get-library-docs: topic="spawn", mode="code"

# Serde serialization
resolve-library-id: "serde"
get-library-docs: topic="derive", mode="code"

# Axum web framework
resolve-library-id: "axum"
get-library-docs: topic="routing", mode="code"

# sqlx database
resolve-library-id: "sqlx"
get-library-docs: topic="query", mode="code"
```

### Understanding Concepts

```
# Learn about Tokio architecture
get-library-docs: topic="runtime", mode="info"

# Understand serde data model
get-library-docs: topic="data model", mode="info"
```

### Specific APIs

```
# Tokio channels
get-library-docs: topic="mpsc channel", mode="code"

# Axum extractors
get-library-docs: topic="extractor", mode="code"

# tracing spans
get-library-docs: topic="span", mode="code"
```

## When to Use Context7

**Always use for:**
- Looking up API details for external crates
- Finding correct function signatures
- Getting usage examples
- Understanding library patterns
- Checking latest API changes

**Use mode="code" when:**
- Need function signatures
- Want code examples
- Looking for API reference
- Implementing features

**Use mode="info" when:**
- Understanding architecture
- Learning concepts
- Reading guides
- Design decisions

## Integration with Development

### Before Implementation
1. Resolve library ID for relevant crates
2. Fetch documentation for the specific API you'll use
3. Check examples for correct usage patterns

### During Debugging
1. Fetch docs for error types
2. Look up correct parameter types
3. Find working examples

### Example Workflow

Task: Implement async HTTP client with reqwest

```
1. resolve-library-id: "reqwest"
   -> Returns: "/seanmonstar/reqwest"

2. get-library-docs:
   context7CompatibleLibraryID: "/seanmonstar/reqwest"
   topic: "client"
   mode: "code"
   -> Returns: Client builder patterns, request methods

3. get-library-docs:
   context7CompatibleLibraryID: "/seanmonstar/reqwest"
   topic: "error handling"
   mode: "code"
   -> Returns: Error types, retry patterns
```

## Tips

- Be specific with topics for better results
- Use page parameter if first page doesn't have what you need
- Combine mode="info" for understanding + mode="code" for implementation
- Cache library IDs mentally for frequently used crates
- Check multiple topics if needed (e.g., "client" then "request builder")

## Common Rust Ecosystem Lookups

| Crate | Common Topics |
|-------|---------------|
| tokio | spawn, select, channel, time, sync |
| serde | derive, serialize, deserialize, attributes |
| axum | router, handler, extractor, middleware |
| sqlx | query, pool, transaction, migrate |
| tracing | span, event, subscriber, instrument |
| anyhow | context, bail, ensure |
| thiserror | error, from, source |
| clap | parser, derive, subcommand, arg |
| reqwest | client, request, response, error |
| hyper | server, client, body |
