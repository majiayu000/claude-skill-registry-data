---
name: smart-search
description: Intelligently choose between semantic and text search based on query intent. Automatically selects the best search mode (semantic for concepts, text for exact terms, symbols for definitions) and provides relevant results. Use when user wants to find code.
allowed-tools: mcp__miller__fast_search, mcp__miller__get_symbols, Read
---

# Smart Search Skill

## Activation Announcement

**IMPORTANT**: When this skill activates, ALWAYS start your response with:

```
🔍 **Smart Search Active**
Selecting optimal search strategy based on query intent...
```

This provides a visual indicator to the user that the skill is running.

## Purpose
**Automatically select the best search strategy** based on query intent. This skill understands when to use semantic search (concepts), text search (exact terms), or symbol search (definitions) and presents results effectively.

## When to Activate
Use when the user wants to find code:
- **General search**: "find the authentication code"
- **Concept search**: "where is error handling?"
- **Exact term search**: "find all console.error calls"
- **Symbol search**: "find UserService class"
- **Exploratory**: "show me the database code"

## Search Mode Selection Intelligence

### Semantic Search (Conceptual Understanding)
**Use when query describes WHAT, not HOW:**

```
Triggers:
- "authentication logic" (concept)
- "error handling" (behavior)
- "database connections" (functionality)
- "user management" (domain)
- "payment processing" (business logic)

fast_search({ query: "...", method: "semantic" })
```

**Best for:**
- Understanding intent ("find auth code" -> finds JWT, OAuth, sessions)
- Cross-language concepts
- Architecture exploration
- Business logic discovery

### Text Search (Exact Terms)
**Use when query specifies EXACT strings:**

```
Triggers:
- "console.error" (specific API)
- "import React" (exact syntax)
- "TODO: fix" (exact comment)
- "throw new Error" (specific pattern)
- "localhost:3000" (literal string)

fast_search({ query: "...", method: "text" })
```

**Best for:**
- Finding specific API usage
- Literal string matches
- Fast, precise lookups
- Code pattern matching

### Symbol Search (Definitions Only)
**Use when query asks for SPECIFIC symbols:**

```
Triggers:
- "UserService class" (class definition)
- "getUserData function" (function definition)
- "AuthToken interface" (type definition)
- "class PaymentProcessor" (explicit class)

get_symbols with target parameter
```

**Best for:**
- Finding definitions
- Locating specific symbols
- Type/interface lookup
- Class/function discovery

## Query Analysis Decision Tree

```
User query -> Analyze intent

Is it a concept/behavior? (what does it do?)
  YES -> Semantic search
  - "authentication", "error handling", "data validation"
  - Returns: Conceptually relevant code

Is it an exact string/API? (specific syntax?)
  YES -> Text search
  - "console.log", "import", "throw new"
  - Returns: Exact matches

Is it a symbol name? (class/function/type?)
  YES -> Symbol search
  - "UserService", "fetchData", "AuthToken"
  - Returns: Symbol definitions

Is it ambiguous?
  YES -> Try semantic first, fallback to text
  - Present best results from both
```

## Key Behaviors

### DO
- Analyze query intent before searching
- Use semantic for concepts and behaviors
- Use text for exact strings and API calls
- Use get_symbols for specific definitions
- Present results with context
- Offer to show file structure with get_symbols
- Suggest refinements if results unclear

### DON'T
- Default to one search mode for everything
- Return raw results without analysis
- Overwhelm with too many matches
- Skip symbol structure for unfamiliar files
- Ignore user's search language/terminology

## Success Criteria

This skill succeeds when:
- Correct search mode selected automatically
- Relevant results found quickly
- Results presented with useful context
- User doesn't need to retry with different mode
- Follow-up queries feel natural
