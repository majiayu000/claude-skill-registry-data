---
name: agent-rag
description: Build or modify a RAG retrieval pipeline — vector store search, corpus routing, citation rendering, book fidelity. Use when adding retrieval to agents.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent, mcp__openai-docs__search_openai_docs, mcp__openai-docs__fetch_openai_doc
---

Build or modify RAG pipeline: $ARGUMENTS

## Before Starting

1. Search OpenAI docs for retrieval patterns:
   - Use `mcp__openai-docs__search_openai_docs` with query "vector stores" for vector store management
   - Use `mcp__openai-docs__search_openai_docs` with query "file search tool" for file_search tool configuration
   - Use `mcp__openai-docs__search_openai_docs` with query "retrieval augmented generation" for RAG best practices
2. Read the existing RAG implementation in ai-lab-agent:
   - `/Users/joshuashepherd/Desktop/dev/repos/ai-lab-agent/src/agents/ai-lab/retrieval/router.ts` — intent classification and corpus routing
   - `/Users/joshuashepherd/Desktop/dev/repos/ai-lab-agent/src/agents/ai-lab/retrieval/search.ts` — full pipeline (search → filter → re-sort → cite)
   - `/Users/joshuashepherd/Desktop/dev/repos/ai-lab-agent/src/agents/ai-lab/retrieval/citations/parseSource.ts` — file path → book/chapter/section
   - `/Users/joshuashepherd/Desktop/dev/repos/ai-lab-agent/src/agents/ai-lab/retrieval/citations/renderSources.ts` — citation line + sources block
3. Read the vector store integration:
   - `/Users/joshuashepherd/Desktop/dev/repos/ai-lab-agent/src/agents/shared/tools.ts` — `executeFileSearch()` using OpenAI Vector Store Search API
   - `/Users/joshuashepherd/Desktop/dev/repos/movemental-dashboard/src/lib/writing-assistant/file-search.ts` — org-specific vector store lookup

## RAG Pipeline Architecture

```
User Message
    │
    ▼
┌─────────────────┐
│  Intent Router   │  Classify: QUOTE_REQUEST, BOOK_SPECIFIC, CROSS_BOOK_COMPARISON,
│                  │  GLOSSARY_DEFINITION, RESEARCH_MODE, TOPIC_GUIDE, GENERAL
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  File Search     │  POST /v1/vector_stores/{id}/search
│  (Vector Store)  │  with constructed query + max_results from router
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Post-Filter     │  Filter by booksFocus / topicsSelected from user context
│  + Re-Sort       │  Re-score by preferred corpus slice (chapters > topics > quotes)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Fallback Search │  If results < threshold, broaden query and retry
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Citation Render │  Parse file paths → book slug + chapter + section
│                  │  Render per-result citationLine + sourcesBlock
└────────┬────────┘
         │
         ▼
  EnrichedResultItem[] → injected into agent context
```

## Intent Router

Classifies user messages to determine retrieval strategy:

```typescript
type RetrievalIntent =
  | 'QUOTE_REQUEST'           // "What does Alan say about..."
  | 'CROSS_BOOK_COMPARISON'   // "Compare Forgotten Ways with Reframation on..."
  | 'GLOSSARY_DEFINITION'     // "What is mDNA?"
  | 'RESEARCH_MODE'           // Deep exploration with multiple sources
  | 'TOPIC_GUIDE'             // Broad topic overview
  | 'BOOK_SPECIFIC'           // Question about a specific book
  | 'GENERAL_CONVERSATION';   // No retrieval needed

function routeRetrieval(message: string, context: RunContract): {
  intent: RetrievalIntent;
  query: string;
  maxResults: number;
  preferredSlices: string[];
  temperatureOverride?: number;
}
```

The router:
- Detects book/topic slugs from the message and user context (booksFocus, topicsSelected)
- Sets `maxResults` (3-10 depending on intent)
- Chooses preferred corpus slices (chapters, topics, comparisons, quotes, supplemental, index)
- Overrides temperature for book fidelity (0.2-0.3 for BOOK_SPECIFIC, QUOTE_REQUEST)

## File Search Integration

```typescript
async function executeFileSearch(query: string, maxResults: number): Promise<SearchResult[]> {
  const vectorStoreId = process.env.OPENAI_VECTOR_STORE_ID;
  if (!vectorStoreId) return []; // graceful degradation

  const response = await openai.vectorStores.search(vectorStoreId, {
    query,
    max_num_results: maxResults,
  });

  return response.data.map(result => ({
    content: result.content,
    score: result.score,
    filename: result.filename,
  }));
}
```

## Citation Rendering

Parse source file paths into human-readable citations:

```typescript
// Input: "books/forgotten-ways/ch03-apostolic-environment.md"
// Output: { bookSlug: "forgotten-ways", chapter: 3, section: "apostolic-environment" }

function parseSource(filename: string): ParsedSource { ... }

// Render per-result citation
function renderCitationLine(source: ParsedSource): string {
  return `— Alan Hirsch, *${bookTitle}*, Chapter ${source.chapter}`;
}

// Render sources block for model context
function renderSourcesBlock(sources: ParsedSource[]): string {
  return `**Sources:** ${uniqueBooks.join(', ')}`;
}
```

## Book Fidelity Contract

When queries are book-related, enforce strict fidelity:

1. **Cache skipping**: Book-related requests ALWAYS bypass the agent response cache to enable fresh retrieval
2. **Temperature override**: Use 0.2-0.3 (not the agent's default 0.5-0.8) to reduce paraphrase drift
3. **Mandatory tool usage**: Instructions must include "🚨 MANDATORY: Always use file_search before answering questions about specific books"
4. **Citation requirement**: Output guardrail checks for citation presence on book-related responses

```typescript
function isBookRelated(message: string, context: RunContract): boolean {
  const bookKeywords = /\b(book|chapter|quote|wrote|writes|according to|says)\b/i;
  const hasBookFocus = context.booksFocus?.length > 0;
  return bookKeywords.test(message) || hasBookFocus;
}
```

## Multi-Tenant Vector Stores

For org-specific corpora (movemental-dashboard pattern):

```typescript
// Look up org-specific vector store ID
const org = await organizationsService.findById(organizationId);
const vectorStoreId = org?.settings?.openai_vector_store_id || process.env.OPENAI_VECTOR_STORE_ID;
```

## Rules

- Always gracefully degrade when vector store is unavailable — return empty results, not errors
- Post-filter results by user context (booksFocus, topicsSelected) to improve relevance
- Include fallback search with broadened query when initial results are insufficient
- Citation rendering must be deterministic — same file path always produces same citation
- Book fidelity is non-negotiable: skip cache, lower temperature, require retrieval, verify citations
- Keep retrieval result payloads concise — truncate long passages before injecting into context
- Test retrieval quality with smoke tests that assert tool invocation and citation presence
- Check OpenAI docs MCP for any changes to vector store API or file_search tool
