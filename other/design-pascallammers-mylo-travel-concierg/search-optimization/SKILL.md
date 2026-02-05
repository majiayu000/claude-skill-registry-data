---
name: search-optimization
description: Guide on optimizing Bluera Knowledge search results through proper intent selection, detail level strategies, result limiting, and store filtering. Teaches when to use minimal vs contextual vs full detail, and how to choose the right search intent for different query types.
---

# Optimizing Bluera Knowledge Search

Master the `search()` MCP tool parameters to get better results with less context usage.

## Understanding Search Parameters

```typescript
search(
  query: string,                    // Your search query
  intent?: SearchIntent,            // What you're looking for
  detail?: 'minimal' | 'contextual' | 'full',  // How much context to return
  limit?: number,                   // Max results (default: 10)
  stores?: string[]                 // Which stores to search
)
```

Each parameter affects results and token usage. Choose wisely!

## Search Intent: Choosing the Right Type

The `intent` parameter helps the search engine rank results appropriately for your query type.

### Intent Decision Tree

**Looking for implementation details? Use `find-implementation`**
- "How does X work internally?"
- "Show me the implementation of Y"
- "What's inside the Z class/function?"

```
search("Vue computed properties implementation", intent='find-implementation')
→ Prioritizes: actual class/function implementations
→ Ranks higher: ComputedRefImpl class, createComputed() function
→ Ranks lower: tests, documentation, examples
```

**Looking for usage patterns? Use `find-pattern`**
- "How to use X?"
- "Examples of Y pattern"
- "Common ways to implement Z"

```
search("React hooks patterns", intent='find-pattern')
→ Prioritizes: example code, usage patterns, HOCs
→ Ranks higher: common patterns like useEffect cleanup
→ Ranks lower: internal implementation details
```

**Looking for references? Use `find-usage`**
- "Where is X used?"
- "Find all calls to Y"
- "What depends on Z?"

```
search("useCallback usage", intent='find-usage')
→ Prioritizes: call sites, import statements
→ Ranks higher: files importing and using useCallback
→ Ranks lower: useCallback's own implementation
```

**Looking for definitions/APIs? Use `find-definition`**
- "What is the API for X?"
- "Show me the type definition of Y"
- "What are the parameters for Z?"

```
search("FastAPI route decorator", intent='find-definition')
→ Prioritizes: function signatures, type definitions
→ Ranks higher: @app.get() decorator definition
→ Ranks lower: examples using the decorator
```

**Looking for documentation? Use `find-documentation`**
- "What does the doc say about X?"
- "Explain Y from the documentation"
- "API reference for Z"

```
search("Pydantic validators documentation", intent='find-documentation')
→ Prioritizes: README, docstrings, comments
→ Ranks higher: markdown docs, inline documentation
→ Ranks lower: implementation code
```

### Default (No Intent)

If unsure, omit `intent` - the search engine will use hybrid ranking:

```
search("authentication middleware")
→ Returns mixed: implementations, patterns, usage, docs
→ Balanced ranking across all categories
```

## Detail Level: Progressive Context Strategy

The `detail` parameter controls how much code context is returned **per result**.

### Detail Levels Explained

| Level | What You Get | Tokens/Result | Use When |
|-------|--------------|---------------|----------|
| `minimal` | Summary, file path, relevance | ~100 | Browsing many results |
| `contextual` | + imports, types, signatures | ~300 | Need interface context |
| `full` | + complete code, all context | ~800 | Deep dive on specific file |

### Progressive Detail Strategy (Recommended)

**Step 1: Start Minimal**
```
search(query, detail='minimal', limit=20)
→ Get 20 summaries (~2k tokens total)
→ Scan quickly for relevance
→ Identify top 3-5 candidates
```

**Step 2: Evaluate Scores**
```
Review relevance scores:
- 0.9-1.0: Excellent match (almost certainly relevant)
- 0.7-0.9: Strong match (very likely relevant)
- 0.5-0.7: Moderate match (possibly relevant)
- < 0.5: Weak match (probably not relevant)
```

**Step 3: Selective Deep Dive**
```
For top results (score > 0.7):
  get_full_context(result_ids)
  → Fetch complete code only for relevant items

For moderate results (score 0.5-0.7):
  search(refined_query, detail='contextual')
  → Try different query with more context
```

### Examples by Use Case

**Use Case: Quick Discovery**
```
"I need to find something but not sure where it is"

search("websocket handling", detail='minimal', limit=30)
→ Browse 30 summaries quickly
→ Total: ~3k tokens
→ Find general location

Then:
get_full_context(top_3_ids)
→ Deep dive on relevant files
→ Additional: ~2.5k tokens
→ Total context: ~5.5k tokens (vs ~24k if detail='full' upfront)
```

**Use Case: API Reference**
```
"I need to see function signatures and types"

search("route decorator", detail='contextual', limit=10)
→ Get imports, types, signatures
→ Total: ~3k tokens
→ See API without full implementation

Usually enough! Only get full if needed.
```

**Use Case: Deep Implementation Study**
```
"I know exactly what I'm looking for, need complete code"

search("ComputedRefImpl class", detail='full', limit=3, stores=['vue'])
→ Get complete implementation immediately
→ Total: ~2.5k tokens
→ Everything you need in one call
```

## Result Limiting

The `limit` parameter caps the number of results returned.

### Choosing the Right Limit

**Large limit (20-50): Discovery mode**
- You're exploring, not sure what exists
- Willing to browse many summaries
- Use with detail='minimal' to keep tokens reasonable

```
search("error handling patterns", detail='minimal', limit=40)
→ Cast wide net
→ Browse many options
→ ~4k tokens total
```

**Medium limit (10-20): Standard search**
- You have a specific question
- Expect multiple relevant files
- Balance between coverage and context

```
search("authentication middleware", detail='minimal', limit=15)
→ Good coverage
→ Not overwhelming
→ ~1.5k tokens
```

**Small limit (3-5): Targeted search**
- You know what you're looking for
- Just need the best matches
- Often combined with detail='full'

```
search("class ComputedRefImpl", detail='full', limit=3, stores=['vue'])
→ Precise target
→ Complete code immediately
→ ~2.5k tokens
```

## Store Filtering

The `stores` parameter restricts search to specific knowledge stores.

### When to Filter Stores

**✅ Use store filtering when:**
- You know which library/codebase has the answer
- Comparing specific libraries (e.g., Express vs Fastapi)
- You want more results from a specific source

```
# Focused search
search("routing", stores=['fastapi'], limit=15)
→ More FastAPI-specific results
→ Higher quality for that framework

# Comparative search
search("middleware implementation", stores=['express', 'hono'], limit=10)
→ Get perspective from both frameworks
→ Balanced results
```

**❌ Don't filter when:**
- You're discovering which library has the answer
- You want cross-library perspectives
- You're not sure where the code lives

```
# Let search find the best match across all libraries
search("dependency injection patterns", limit=15)
→ Might find great examples in FastAPI, NestJS, or Angular
→ Don't limit yourself prematurely
```

### Listing Available Stores

Before filtering, know what's indexed:

```
list_stores()
→ See all available stores
→ Note store names for filtering

Then:
search(query, stores=['store1', 'store2'])
```

## Combined Optimization Strategies

### Strategy 1: Efficient Discovery
```
Goal: Find something across many files, minimize tokens

1. search(query, detail='minimal', limit=30)
   → Browse summaries (~3k tokens)

2. Filter top 5 by score (>0.7)

3. get_full_context(top_5_ids)
   → Deep dive selectively (~4k tokens)

Total: ~7k tokens (vs ~24k with detail='full' upfront)
Savings: ~70% token reduction
```

### Strategy 2: Precise Targeting
```
Goal: Get exactly what you need, fast

1. Identify store: list_stores()

2. search(precise_query,
         intent='find-implementation',
         detail='full',
         limit=3,
         stores=['target-store'])
   → Exact match with full code

Total: ~2.5k tokens
Result: Fastest path to answer
```

### Strategy 3: Comparative Analysis
```
Goal: Compare implementations across libraries

1. search(query,
         intent='find-implementation',
         detail='minimal',
         limit=20,
         stores=['lib1', 'lib2', 'lib3'])
   → Get summaries from multiple libraries

2. Review distribution:
   - lib1: 8 results
   - lib2: 7 results
   - lib3: 5 results

3. get_full_context(top_2_from_each_lib)
   → Compare implementations

Total: ~5k tokens
Result: Balanced cross-library comparison
```

## Quick Reference

### High-Efficiency Defaults
```
search(query, detail='minimal', limit=20)
→ Good for most discovery tasks
→ Review, then selectively fetch full context
```

### High-Precision Defaults
```
search(query, intent='find-implementation', detail='full', limit=5, stores=['known-lib'])
→ When you know exactly what you're looking for
→ Fastest path to deep answer
```

### Balanced Defaults
```
search(query, detail='contextual', limit=10)
→ Good middle ground
→ See interfaces without full implementation
```

## Common Mistakes to Avoid

1. **❌ Using detail='full' with limit=50**
   - Result: ~40k tokens consumed
   - Fix: Start with detail='minimal', escalate selectively

2. **❌ Not using intent parameter**
   - Result: Mixed ranking, less relevant results
   - Fix: Choose intent based on query type

3. **❌ Over-filtering stores too early**
   - Result: Miss better answers in other libraries
   - Fix: Search broadly first, then narrow

4. **❌ Setting limit too low (1-2)**
   - Result: Miss relevant alternatives
   - Fix: Use limit=5 minimum, more for discovery

5. **❌ Not checking relevance scores**
   - Result: Waste time on low-relevance results
   - Fix: Filter by score > 0.7 before deep dive

## Token Usage Examples

Real token counts for different strategies:

```
# Inefficient approach
search("auth middleware", detail='full', limit=30)
→ 30 results × 800 tokens = 24,000 tokens
→ Most results not even relevant!

# Optimized approach
search("auth middleware", detail='minimal', limit=30)
→ 30 results × 100 tokens = 3,000 tokens
→ Identify top 3 (score > 0.8)

get_full_context([id1, id2, id3])
→ 3 results × 800 tokens = 2,400 tokens

Total: 5,400 tokens (78% reduction!)
```

Master these optimization strategies to search faster, use less context, and get better results.
