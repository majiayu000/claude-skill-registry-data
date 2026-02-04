---
name: when-to-query
description: Decision guide for when to query Bluera Knowledge stores vs using Grep/Read on current project. Query BK for library/dependency questions and reference material. Use Grep/Read for current project code, debugging, and implementation details. Includes setup instructions and mental model.
---

# When to Query Bluera Knowledge

## The Rule: BK First for External Code

**When the question involves libraries, dependencies, or reference material, query BK first.**

BK provides authoritative source code from the actual libraries. This is:
- **More accurate** than training data (which may be outdated)
- **Faster** than web search (~100ms vs 2-5 seconds)
- **More complete** than documentation sites (includes tests, examples, internal APIs)
- **Zero rate limits** (local, unlimited queries)

---

## ALWAYS Query BK For:

### Library Implementation Questions
- "How does Express handle middleware errors?"
- "What does `useEffect` cleanup actually do internally?"
- "How is Pydantic validation implemented?"
- "What happens when lodash `debounce` is called?"
- "How does React's reconciliation work?"

### API and Method Questions
- "What parameters does `axios.create()` accept?"
- "What's the signature of `zod.object()`?"
- "What options can I pass to `hono.use()`?"
- "What events does EventEmitter emit?"
- "What methods are available on `prisma.client`?"

### Error and Exception Handling
- "What errors can this library throw?"
- "How do I catch validation errors in Zod?"
- "What does this error code mean in library X?"
- "Why might this function return undefined?"
- "What validation does this library perform?"

### Version-Specific Behavior
- "What changed in React 18's concurrent mode?"
- "How does this work in Express 4 vs 5?"
- "Is this method deprecated in the latest version?"
- "What's the migration path from v2 to v3?"
- "Does my version support this feature?"

### Configuration and Options
- "What configuration options exist for Vite?"
- "What are the default values for these options?"
- "How do I customize the behavior of X?"
- "What environment variables does this library use?"
- "What's the full schema for this config?"

### Testing Patterns
- "How do the library authors test this feature?"
- "How should I mock this library in tests?"
- "What fixtures do I need for testing this integration?"
- "What edge cases does the library's test suite cover?"

### Performance and Internals
- "Is this operation cached internally?"
- "What's the time complexity of this method?"
- "How is this optimized in the library?"
- "Does this run synchronously or asynchronously?"
- "What's the memory footprint of this?"

### Security and Validation
- "How does this library validate input?"
- "What sanitization is applied?"
- "How are credentials handled internally?"
- "Is this safe against injection attacks?"

### Integration and Patterns
- "How do I integrate library X with library Y?"
- "What's the idiomatic way to use this API?"
- "How do examples in the library do this?"
- "What patterns does this library use?"
- "What's the recommended project structure?"

### Reference Material
- "What does the API spec say about X?"
- "What are the project requirements for Y?"
- "How does the architecture doc describe Z?"
- "What coding standards apply here?"

---

## DO NOT Query BK For:

### Current Project Code
Use Grep/Read directly:
- "Where is the authentication middleware in THIS project?"
- "Show me OUR database models"
- "Find all API endpoints WE defined"

### General Concepts
Use training data (no tool needed):
- "What is a closure in JavaScript?"
- "Explain dependency injection"
- "What is REST?"

### Current Events
Use web search:
- "What's new in Next.js 15?"
- "Latest release notes for TypeScript"
- "Security advisory for npm packages"

---

## Setup: Index Your Dependencies

BK only knows what you've indexed. Add your key dependencies:

```bash
# Get suggestions based on package.json
/bluera-knowledge:suggest

# Add important libraries
/bluera-knowledge:add-repo https://github.com/expressjs/express
/bluera-knowledge:add-repo https://github.com/honojs/hono

# Index local docs
/bluera-knowledge:add-folder ./docs --name=project-docs

# Verify what's indexed
/bluera-knowledge:stores
```

---

## Quick Reference

| Question Pattern | Use |
|-----------------|-----|
| "How does [library] work..." | BK |
| "What does [library function] do..." | BK |
| "What options/params does [library] accept..." | BK |
| "What errors can [library] throw..." | BK |
| "How should I use [library API]..." | BK |
| "What changed in [library version]..." | BK |
| "How do I integrate [library]..." | BK |
| "Where is [thing] in OUR code..." | Grep/Read |
| "What is [general concept]..." | Training data |
| "What's new in [library] today..." | Web search |

---

## Mental Model

```
External Code (libraries, deps, specs)  →  Query BK
Your Project Code                       →  Grep/Read directly
General Knowledge                       →  Use training data
Breaking News                           →  Web search
```

BK is cheap, fast, and authoritative. When in doubt about a library, query BK.
