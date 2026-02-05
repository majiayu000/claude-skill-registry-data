---
name: "semantic-search"
description: "Use this when deciding between semantic search and grep/glob for code discovery. Apply for concept-based queries (find payment processing), intent-based searches (how is auth implemented), or when user doesn't know exact class names. Use grep for exact matches like specific function names"
categories: ["pattern", "technique", "search"]
tags: ["semantic-search", "weaviate", "embeddings", "discovery"]
version: "1.0.0"
---

# Semantic Search Technique

## Purpose

Decision framework and execution guide for using semantic search effectively in CodeCompass.

## When to Use Semantic Search

### ✅ Use Semantic Search When

**1. Concept-based Queries**
- "Find code that handles payment processing"
- "Where do we validate email addresses?"
- "Show me error handling patterns"

**2. Intent-based Queries**
- "How is user authentication implemented?"
- "What code calculates shipping costs?"
- "Find business rules for order approval"

**3. Cross-language/Cross-file**
- Searching across PHP, TypeScript, config files
- Pattern discovery across multiple modules
- Finding similar implementations

**4. Fuzzy/Exploratory**
- User doesn't know exact class/function names
- Exploring unfamiliar codebase
- "Code that does something like X"

**5. Natural Language**
- "Show me all database migrations"
- "Find controllers that handle file uploads"
- "Where are API rate limits defined?"

### ❌ Use Grep/Glob When

**1. Exact Matches**
- "Find class named `PaymentController`"
- "Where is `processPayment` function defined?"
- "Find all imports of `UserService`"

**2. Syntax Patterns**
- "Find all functions starting with `get`"
- "Show me all `@Injectable()` decorators"
- "Find TypeScript interfaces"

**3. Performance Critical**
- Quick lookups in known files
- Repeated searches in tight loops
- When you know exact location

**4. Structural Queries**
- "Find all `.ts` files in `src/modules`"
- "List all test files"
- "Show directory structure"

## Execution Guide

### Step 1: Formulate Effective Query

**❌ Bad Queries** (too vague):
- "payment"
- "code"
- "function"

**✅ Good Queries** (specific context):
- "business logic for processing customer payments and updating order status"
- "validation rules for user email and password requirements"
- "error handling patterns for database connection failures"

**Why**: More context = better semantic matching

**Formula**:
```
[Action/Purpose] for [Specific Entity] with [Context/Constraints]
```

**Examples**:
- "Extract business capabilities from Yii2 controllers"
- "Validation logic for user registration with email verification"
- "Database migration patterns for schema versioning"

### Step 2: Verify Indexing

**Before searching**, ensure codebase is indexed:

```bash
# Check if indexed
curl http://localhost:8081/v1/schema

# Should show collections like:
# - CodeContext
# - AtlasCode
```

**If not indexed**:
```bash
codecompass batch:index <path-to-codebase>
```

### Step 3: Execute Search

```bash
codecompass search:semantic "business logic for payment processing"
```

**Alternative** (if using as library):
```typescript
const results = await searchService.semanticSearch({
  query: "business logic for payment processing",
  limit: 10,
  certainty: 0.7 // Minimum relevance score
});
```

### Step 4: Interpret Results

**Check relevance scores**:
- **>0.8**: Highly relevant (exact match)
- **0.7-0.8**: Good match (related)
- **0.6-0.7**: Moderate match (possibly relevant)
- **<0.6**: Weak match (may be noise)

**Verify context**:
- Does the returned code actually match intent?
- Are results from expected modules?
- Multiple related files found (good signal)
- Or isolated random matches (refine query)

### Step 5: Refine if Needed

**Too many results** (>50):
- Add more specific context to query
- Increase certainty threshold
- Add domain constraints ("in authentication module")

**Too few results** (<3):
- Broaden query (less specific)
- Lower certainty threshold
- Check if area is actually indexed
- Try related terms/synonyms

**Wrong results**:
- Rephrase query with different terminology
- Add negative constraints
- Try breaking into multiple specific queries

## Behind the Scenes

### Architecture
```
Query Text
    ↓
Ollama Embedding (mxbai-embed-large)
    ↓
1024-dimensional vector
    ↓
Weaviate Vector Search (cosine similarity)
    ↓
Ranked Results
```

### Key Components

**From `.ai/capabilities.json`**:
- **Module**: `search`, `vectorizer`, `weaviate`
- **Embedding**: Ollama mxbai-embed-large (1024 dimensions)
- **Vector DB**: Weaviate with HNSW indexing
- **Collections**: `CodeContext`, `AtlasCode`

**Configuration** (from `.env`):
```bash
EMBEDDING_SERVICE=ollama
OLLAMA_EMBEDDING_MODEL=mxbai-embed-large
OLLAMA_URL=http://localhost:11434
CODECOMPASS_WEAVIATE_URL=http://localhost:8081
```

## Advanced Patterns

### Pattern 1: Multi-Query Exploration

For complex questions, break into multiple searches:

```bash
# Instead of:
"authentication and authorization and session management"

# Do:
codecompass search:semantic "user authentication login process"
codecompass search:semantic "authorization and access control"
codecompass search:semantic "session management and tokens"
```

### Pattern 2: Iterative Refinement

```bash
# 1. Broad search
codecompass search:semantic "payment processing"

# 2. Review results, identify specific module
# 3. Narrow search
codecompass search:semantic "payment gateway integration in PaymentController"

# 4. Pinpoint implementation
codecompass search:semantic "Stripe API call for processing credit cards"
```

### Pattern 3: Cross-Domain Search

Search across different aspects:

```bash
# Code implementation
codecompass search:semantic "email validation logic"

# Tests
codecompass search:semantic "test cases for email validation"

# Configuration
codecompass search:semantic "email service configuration"
```

## Common Pitfalls

### ❌ Pitfall 1: Searching Before Indexing
**Symptom**: No results or error
**Solution**: Run `codecompass batch:index` first

### ❌ Pitfall 2: Too Vague Queries
**Symptom**: Returns everything or nothing useful
**Solution**: Add specific context and intent

### ❌ Pitfall 3: Expecting Exact Matches
**Symptom**: "Why didn't it find function `processPayment`?"
**Reason**: Semantic search is for concepts, not exact names
**Solution**: Use grep for exact matches

### ❌ Pitfall 4: Ignoring Relevance Scores
**Symptom**: Reading irrelevant results
**Solution**: Filter by score >0.7, ignore weak matches

### ❌ Pitfall 5: Single Query for Complex Questions
**Symptom**: Poor results for multi-faceted questions
**Solution**: Break into multiple targeted queries

## Decision Tree

```
┌─────────────────────────────────────┐
│ I need to find code that...         │
└─────────────────────────────────────┘
              ↓
        ┌─────────┐
        │ Know    │ Exact class/function name?
        │ exact   │
        │ name?   │
        └─────────┘
          ↙     ↘
        YES      NO
         ↓        ↓
    Use Grep  ┌─────────┐
              │ Concept │ Searching by meaning/purpose?
              │ search? │
              └─────────┘
                ↙     ↘
              YES      NO
               ↓        ↓
          Semantic  ┌─────────┐
          Search    │ Pattern │ Looking for code pattern?
                    │ match?  │
                    └─────────┘
                      ↙     ↘
                    YES      NO
                     ↓        ↓
                Use Glob  Use both
                          (Glob + Semantic)
```

## Performance Considerations

### Speed
- **Grep**: Milliseconds (fast, synchronous)
- **Semantic Search**: 100-500ms (embedding + vector search)

**Tradeoff**: Semantic is slower but finds conceptually related code

### Token Cost (Embeddings)
- Each query → 1 embedding generation
- Ollama local → No API cost
- But consumes local compute

### Scaling
- Small codebase (<1K files): Either method fine
- Medium codebase (1K-10K files): Semantic search advantage grows
- Large codebase (>10K files): Semantic search essential

## Integration with Other Tools

### With Yii2 Analysis
```bash
# 1. Analyze Yii2 project
codecompass analyze:yii2 <path>

# 2. Index results
codecompass batch:index <path>

# 3. Explore with semantic search
codecompass search:semantic "Yii2 controller actions for user management"
```

### With Requirements Extraction
```bash
# 1. Extract requirements
codecompass requirements:extract

# 2. Search extracted requirements
codecompass search:semantic "business rules for order validation"
```

### With Weaviate Direct Query
```bash
# Alternative: Query Weaviate GraphQL API directly
curl -X POST http://localhost:8081/v1/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{
      Get {
        CodeContext(
          nearText: { concepts: [\"payment processing\"] }
          limit: 10
        ) {
          content
          filePath
        }
      }
    }"
  }'
```

## Related Skills

- `0-discover-capabilities.md` - How to discover modules
- `analyze-yii2-project.md` - Uses semantic search in workflow

## Related Modules

From `.ai/capabilities.json`:
- `search` - SearchService, IntegratedSearchService
- `vectorizer` - Ollama embedding generation
- `weaviate` - Vector database client
- `indexing` - File indexing pipeline

---

**Remember**: Semantic search finds code by **meaning**, not by **name**. Choose the right tool for the job.
