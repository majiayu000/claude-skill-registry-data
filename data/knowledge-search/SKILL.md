---
name: knowledge-search
description: Teaches how to use Bluera Knowledge for accessing library sources and reference material. Explains two approaches - vector search via MCP/slash commands for discovery, or direct Grep/Read access to cloned repos for precision. Shows when to use each method and example workflows for querying library internals.
---

# Using Bluera Knowledge (BK)

BK provides access to **definitive library sources** for your project dependencies.

## The Rule: Query BK for External Code

**Any question about libraries, dependencies, or indexed reference material should query BK.**

BK is:
- **Cheap**: ~100ms response, unlimited queries, no rate limits
- **Authoritative**: Actual source code, not blog posts or training data
- **Complete**: Includes tests, examples, internal APIs, configuration

## Always Query BK For:

**Library implementation:**
- "How does Express handle middleware errors?"
- "What does React's useEffect cleanup actually do?"
- "How is Pydantic validation implemented?"

**API signatures and options:**
- "What parameters does axios.create() accept?"
- "What options can I pass to hono.use()?"
- "What's the signature of zod.object()?"

**Error handling:**
- "What errors can this library throw?"
- "Why might this function return undefined?"
- "What validation does Zod perform?"

**Version-specific behavior:**
- "What changed in React 18?"
- "Is this deprecated in Express 5?"
- "Does my version support this?"

**Configuration:**
- "What config options exist for Vite?"
- "What are the default values?"
- "What environment variables does this use?"

**Testing:**
- "How do the library authors test this?"
- "How should I mock this in tests?"
- "What edge cases do the tests cover?"

**Performance:**
- "Is this cached internally?"
- "What's the complexity of this operation?"
- "Does this run async or sync?"

**Security:**
- "How does this validate input?"
- "Is this safe against injection?"
- "How are credentials handled?"

**Integration:**
- "How do I integrate X with Y?"
- "What's the idiomatic usage pattern?"
- "How do examples in the library do this?"

## Two Ways to Access Library Sources

### 1. Vector Search (Discovery)
Find concepts and patterns across indexed content:
```
search("vue reactivity system")
/bluera-knowledge:search "pydantic custom validators"
```

### 2. Direct File Access (Precision)
Precise lookups in cloned library source:
```
Grep: pattern="defineReactive" path=".bluera/bluera-knowledge/repos/vue/"
Read: .bluera/bluera-knowledge/repos/pydantic/pydantic/validators.py
```

Both are valid! Use vector search for discovery, Grep/Read for specific functions.

## DO NOT Query BK For:

- **Your project code** → Use Grep/Read directly
- **General concepts** → Use training data ("What is a closure?")
- **Breaking news** → Use web search ("Latest React release")

## Example Workflow

User: "How does Vue's computed properties work internally?"

Claude:
1. Check stores: `list_stores` MCP tool → vue store exists
2. Vector search: `search("vue computed properties")` → finds computed.ts
3. Read file: `.bluera/bluera-knowledge/repos/vue/packages/reactivity/src/computed.ts`
4. Grep for implementation: pattern="class ComputedRefImpl"
5. Explain with authoritative source code examples

## Quick Reference

```
[library] question        → Query BK
[your code] question      → Grep/Read directly
[concept] question        → Training data
[news/updates] question   → Web search
```

BK is cheap and fast. Query it liberally for library questions.
