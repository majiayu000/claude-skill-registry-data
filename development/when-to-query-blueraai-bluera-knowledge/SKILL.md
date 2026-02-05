---
name: when-to-query
description: Decision guide for when to query Bluera Knowledge stores vs using Grep/Read on current project. Query BK for library/dependency questions and reference material. Use Grep/Read for current project code, debugging, and implementation details. Includes setup instructions and mental model.
---

# When to Query BK vs Current Project

## Query BK When:

**Questions about libraries/dependencies:**
- "How does Vue's reactivity system work?"
- "What are Pydantic's built-in validators?"
- "How should I use Pino's child loggers?"
- "What middleware does Hono provide?"

**Reference material questions:**
- "What does the API spec say about authentication?"
- "What are the project requirements for error handling?"
- "How does the architecture doc describe the data flow?"
- "What coding standards apply to this project?"

**Learning library APIs:**
- Discovering available options/configs
- Finding usage examples from library itself
- Understanding internal implementation

**Verifying specifications:**
- Checking exact requirements
- Finding edge cases in specs
- Understanding design decisions

## Query Current Project (Grep/Read) When:

**Working on YOUR code:**
- "Where is the authentication middleware?"
- "Find all API endpoints"
- "Show me the database models"

**Debugging YOUR code:**
- Reading error traces
- Following call stacks
- Checking variable usage

## Setup First: Add Important Dependencies

Before BK is useful, you need to add library sources:

```
/bk:suggest                  # Get recommendations
/bk:add-repo <url> --name=<lib>   # Add important libs
/bk:stores                   # Verify what's indexed
```

## Mental Model

```
Current Project Files → Grep/Read directly
           vs
Library Sources (Vue, Pydantic, etc.) → BK (vector search OR Grep/Read)
```

BK gives you both ways to access library sources:
1. Semantic search for discovery
2. Grep/Read for precision

Use whichever works best for your question!
