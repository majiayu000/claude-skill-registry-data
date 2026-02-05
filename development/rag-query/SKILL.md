---
name: rag-query
description: This skill should be used when users ask questions about pod network development, pod smart contract language, pod APIs, pod tooling, or pod-specific features. It provides semantic search over the pod network knowledge base to retrieve relevant documentation, code examples, and best practices.
---

# rag-query

Query the pod network knowledge base for pod development information using semantic search.

## Purpose

This skill enables semantic search over the pod network knowledge base, which contains curated documentation about pod network development, the pod smart contract language, pod APIs, pod tooling, and pod-specific features. It transforms general pod development questions into targeted knowledge retrieval with source citations.

## When to Use This Skill

### Trigger this skill when users:

**pod Network Development:**

- "How do I write a smart contract in pod?"
- "What's the syntax for defining a function in pod?"
- "Show me an example of a pod contract"
- "How do I compile and deploy a contract on pod network?"
- "What are the pod-specific data types?"

**Error Troubleshooting:**

- "I'm getting a compiler error in my pod contract"
- "My pod contract won't compile. What's wrong?"
- "How do I debug pod contract errors?"

**APIs & Tooling:**

- "How do I use the pod network API?"
- "What RPC methods are available on pod network?"
- "How do I query pod network state?"
- "What tools are available for pod development?"
- "How do I interact with pod indexer?"

**Learning & Conceptual Questions:**

- "How does the pod smart contract language work?"
- "What are the differences between pod and Solidity?"
- "What are pod network's unique features?"
- "How do I get started with pod development?"
- "What are best practices for pod contract development?"

**Specific Terminology Indicators** (high confidence for skill use):

- Questions containing: pod network, pod contract, pod language, pod API, pod RPC, pod indexer, pod tooling, pod deployment, pod syntax, pod features

### Do NOT trigger this skill when:

- Users ask general programming questions not specific to pod network
  - ❌ "How do I write a for loop in JavaScript?"
  - ❌ "What's the best way to structure a database?"
- Questions are about other blockchains or technologies (not pod network)
  - ❌ "How do I build a Solidity contract?"
  - ❌ "What's the best Ethereum development framework?"
- Claude's base knowledge is clearly sufficient
  - ❌ "What is a variable?" (fundamental computer science)
  - ❌ "Explain object-oriented programming basics"
- Users ask about news, current events, or real-time information
  - ❌ "What's the current POD token price?"
  - ❌ "Have there been any recent pod network incidents?"
- Questions are about personal preferences or subjective opinions
  - ❌ "Is pod better than Ethereum?" (without technical context)
  - ❌ "What's your favorite blockchain?"

## Tools

### semantic_search

Search the knowledge base with semantic query matching. Returns ranked results with source citations.

**Parameters:**

- `query` (string, required): Natural language search query
- `limit` (number, optional): Maximum number of results to return (1-20, default: 5)
- `min_relevance` (number, optional): Minimum relevance score threshold (0.0-1.0, default: 0.5)

**Returns:**

```json
{
  "results": [
    {
      "content": "Document text content",
      "source_title": "Source document title",
      "source_url": "URL to source (if available)",
      "relevance_score": 0.85,
      "topic_tags": ["pod", "contracts"],
      "rank": 1
    }
  ],
  "search_time_ms": 234,
  "total_before_filtering": 10,
  "filtered_by_relevance": 2
}
```

**Error responses:**

- `NO_RESULTS`: No documents found or none met relevance threshold
- `VALIDATION_ERROR`: Invalid parameters provided
- `SERVER_ERROR`: Connection to RAG server failed

## Scripts

### get-synonyms.sh

Lookup synonyms for pod development terminology to improve query formulation and discover alternative search terms.

**Location:** `scripts/get-synonyms.sh`

**Usage:**

```bash
# Via argument
./scripts/get-synonyms.sh "contract"

# Via stdin
echo "RPC" | ./scripts/get-synonyms.sh

# With query refinement
SYNONYMS=$(./scripts/get-synonyms.sh "smart contract")
# Returns: "contract,pod contract,on-chain code"
```

**Parameters:**

- `TERM` (string): pod development term to lookup (case-insensitive)

**Returns:**

- CSV list of synonyms to stdout
- Exit code 0 if found, 1 if not found

**When to use:**

- Query returns low relevance results
- Uncertain about correct terminology
- Want to discover alternative search terms
- Implementing multi-angle or iterative refinement strategies
- User uses colloquial terms that need translation to domain vocabulary

**Example workflow:**

```bash
# User query: "How do I query pod?"
# Get synonyms to enrich search
SYNONYMS=$(./scripts/get-synonyms.sh "query")
# Use in query: "query OR RPC OR API call"

# Or refine failed search
if [ $RELEVANCE_LOW ]; then
  SYNONYMS=$(./scripts/get-synonyms.sh "$ORIGINAL_TERM")
  # Try alternative terms from synonyms
fi
```

**Coverage:**

- pod network terms (contract, deployment, RPC, indexer)
- pod language keywords (function, type, storage)
- pod APIs (RPC methods, indexer queries, state access)
- Development tools (compiler, debugger, explorer)
- pod-specific concepts and their synonyms

## Query Strategy Overview

Choose the appropriate query strategy based on the user's needs. Detailed guidance for each strategy is available in reference documents.

### Focused Strategies (references/focused-strategies.md)

Use when the user has specific, well-defined questions:

- **Precision Search**: Specific technical questions with known terminology
  - Parameters: `min_relevance`: 0.7-0.8, `limit`: 3-5
  - Best for: API usage, exact errors, specific syntax, precise implementations

- **Quick Answer**: Fast answers to straightforward questions
  - Parameters: `min_relevance`: 0.6-0.7, `limit`: 3-5
  - Best for: Syntax lookups, common patterns, simple how-to questions

**When to load**: User asks specific question with clear technical terms or needs quick syntax lookup.

### Broad Strategies (references/broad-strategies.md)

Use when the user is learning, exploring, or needs comprehensive coverage:

- **Broad Discovery**: Exploratory learning and topic exploration
  - Parameters: `min_relevance`: 0.3-0.5, `limit`: 5-8
  - Best for: Learning concepts, discovering patterns, building understanding

- **Comprehensive Research**: Thorough investigation for important decisions
  - Parameters: `min_relevance`: 0.4-0.6, `limit`: 10-15
  - Best for: Architecture decisions, security audits, comparing approaches

**When to load**: User is exploring topics, learning broadly, or making important technical decisions requiring thorough research.

### Refined Strategies (references/refined-strategies.md)

Use when initial searches are insufficient or questions are complex:

- **Multi-Angle Search**: Multiple searches from different angles
  - Parameters: Multiple queries with `min_relevance`: 0.5-0.6, `limit`: 5-7 each
  - Best for: Ambiguous questions, cross-cutting concerns, complex topics

- **Iterative Refinement**: Progressive narrowing based on initial results
  - Parameters: Start with `min_relevance`: 0.4, `limit`: 8, then adjust
  - Best for: Unfamiliar terminology, unclear technical terms, emerging topics

**When to load**: Initial search results are poor, question is ambiguous or complex, or terminology is uncertain.

## Basic Usage Workflow

Follow this workflow when the skill triggers:

### 1. Assess the Question

Determine question type and appropriate strategy:

- **Specific and clear?** → Start with Focused strategies
- **Exploratory or learning?** → Start with Broad strategies
- **Ambiguous or complex?** → Consider Refined strategies

### 2. Formulate Query

Extract the core technical question. Good query formulation:

- Uses specific technical terminology when known
- Includes relevant pod-specific terms (pod contract, RPC, indexer, etc.)
- Is concise but complete
- Focuses on the core question

Examples:

- Good: "pod contract function syntax"
- Good: "pod network RPC methods for state queries"
- Poor: "How to make pod stuff work"

### 3. Execute Search

Call `semantic_search` with appropriate parameters based on selected strategy:

```javascript
// Focused - Precision search example
semantic_search({
  query: 'pod contract function definition syntax',
  limit: 5,
  min_relevance: 0.7
});

// Broad - Discovery example
semantic_search({
  query: 'pod network development getting started',
  limit: 8,
  min_relevance: 0.4
});
```

### 4. Evaluate Results

Check result quality:

- **High relevance (>0.7)**: Results are highly relevant, can be used directly
- **Medium relevance (0.5-0.7)**: Results are useful but may need interpretation
- **Low relevance (<0.5)**: Results may be tangentially related, consider refining

If results are insufficient:

1. Load the appropriate strategy reference document
2. Follow detailed guidance for multi-angle or iterative approaches
3. Adjust parameters or try different query formulation

### 5. Synthesize Response

Create helpful response from results:

- **Cite sources**: Always include `source_title` and `source_url`
- **Prioritize by relevance**: Present higher-scoring results first
- **Include examples**: Use code examples from results when available
- **Combine insights**: Synthesize information from multiple results
- **Acknowledge gaps**: If relevant information is missing, state clearly

### 6. Handle Errors

**No results found:**

- Acknowledge knowledge base limitation
- Try broader query or lower `min_relevance`
- Fall back to Claude's base knowledge if appropriate
- Suggest official documentation or community resources

**Low relevance scores:**

- State confidence level explicitly
- Consider loading refined strategies for iterative refinement
- Note results may be tangentially related
- Suggest query refinement

**Server errors:**

- Inform user the knowledge base is temporarily unavailable
- Fall back to Claude's base knowledge
- Suggest retrying or consulting official documentation

## Best Practices

### Query Formulation

Effective query formulation is critical for retrieving relevant results. Basic guidelines:

- **Use technical terminology**: "pod contract deployment" not "put code on chain"
- **Include pod-specific terms**: pod network, pod contract, RPC, indexer when relevant
- **Be specific**: "pod RPC method for balance queries" not "get balance"
- **Remove question words**: "pod contract function syntax" not "how do I write functions"
- **Use synonym script**: `./scripts/get-synonyms.sh "term"` for alternative terminology
- **Inject context**: Add pod version, API version, and project context when available

**For in-depth guidance**, load the comprehensive query formulation reference:

**references/query-formulation.md** - Complete guide including:

- Core principles (preserve intent, technical precision, terminology layers)
- Synonym expansion with get-synonyms.sh integration
- Technical term expansion strategies (functions, standards, versions, frameworks)
- Advanced reformulation patterns (conceptual→implementation, problem→solution, vague→specific)
- Code-specific patterns (analyzing user code, syntax questions)
- Anti-patterns to avoid (generic queries, question words, colloquialisms)
- Contextual enhancement (project context, conversation history)
- Query optimization by search type (conceptual, implementation, troubleshooting, security)
- Query templates by question type ("how do I", "what is", "why is", error messages)
- Multi-query generation strategy
- Quality checklist and complete examples

**When to load this reference:**

- Initial queries return low relevance results (<0.5)
- User uses colloquial or vague terminology
- Complex question requiring multi-dimensional queries
- Implementing iterative refinement or multi-query strategies
- Need systematic approach to query formulation
- Want to improve query quality for better results

### Source Citation

- Always cite using `source_title` and `source_url`
- Make citations easy to find and verify
- Include multiple sources for important claims
- Note source authority (official docs, well-known libraries)

### Response Quality

- Lead with actionable information
- Include working code examples when available
- Structure complex responses with headings
- Note trade-offs when multiple approaches exist
- Indicate confidence level based on relevance scores

### Performance

- Target <3 seconds per search
- Avoid redundant queries for same information
- Inform user if search is slow
- For multi-angle searches, consider executing queries in parallel

### Progressive Loading

When uncertain about strategy or need detailed guidance:

1. Start with basic workflow above
2. If results are insufficient, load appropriate reference document:
   - `references/query-formulation.md` for query quality issues or terminology challenges
   - `references/focused-strategies.md` for specific questions
   - `references/broad-strategies.md` for exploratory/comprehensive needs
   - `references/refined-strategies.md` for complex/ambiguous questions
3. Follow detailed strategy guidance from reference
4. Synthesize results according to strategy best practices

## Reference Documents

Load these documents as needed for detailed guidance:

### Query Strategy References

- **references/focused-strategies.md**: Precision Search and Quick Answer strategies with detailed examples
- **references/broad-strategies.md**: Broad Discovery and Comprehensive Research strategies with detailed examples
- **references/refined-strategies.md**: Multi-Angle Search, Iterative Refinement, Comprehensive Multi-Query Research, and Exploratory Discovery strategies with detailed examples

These strategy references contain:

- Detailed parameter guidance
- Multiple worked examples
- Query formulation guidelines for each strategy
- Result evaluation criteria
- Synthesis best practices
- Common pitfalls and solutions

### Query Formulation Reference

- **references/query-formulation.md**: Comprehensive guide to transforming user questions into high-quality search queries

This reference contains:

- Core principles (preserve intent, technical precision, terminology layers)
- Synonym expansion with get-synonyms.sh script integration
- Technical term expansion strategies (functions, standards, versions, frameworks, errors)
- Advanced reformulation patterns (conceptual→implementation, problem→solution, vague→specific, context injection, comparative)
- Code-specific patterns (analyzing code, syntax questions)
- Anti-patterns to avoid (over-generic, question words, user phrasing, metadata, over-expansion, losing specificity)
- Contextual enhancement (project context, conversation history)
- Query optimization by search type (conceptual, implementation, troubleshooting, security)
- Query templates by question type ("how do I", "what is", "why is", error messages)
- Multi-query generation strategy for comprehensive coverage
- Quality checklist and complete worked examples
