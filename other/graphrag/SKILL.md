---
name: graphrag
description: Combine knowledge graphs with retrieval-augmented generation — graph construction, community summaries, and graph-guided retrieval. Use when RAG needs to answer questions spanning many documents.
category: ai-research
---

# GraphRAG

Standard RAG retrieves isolated chunks; questions spanning many documents ("how do these themes 
connect?", "summarize the whole corpus on X") need structure. GraphRAG builds a knowledge graph 
from the corpus and retrieves along its structure — entities, relationships, and community 
summaries — giving the generator a map, not just fragments.

## Overview

The pipeline: extract entities and relationships from documents into a graph, detect communities 
(clusters of densely connected entities), summarize each community, and at query time retrieve 
relevant entities, relationships, and summaries — traversing the graph to gather connected 
context. Local queries ("what does the doc say about X?") use entity neighborhoods; global queries 
("what are the main themes?") use community summaries. It's RAG with a structural index on top.

## When to use

- Corpus-level questions: themes, trends, and connections across many documents.
- Multi-hop questions requiring chaining facts from different sources.
- Domains where entity relationships carry the meaning: research corpora, investigations, 
enterprise knowledge.
- When chunk-based RAG returns fragments that don't compose into an answer.

## Core concepts

- **Graph construction**: LLM-driven extraction of entities, relationships, and claims from chunks 
— with source tracking per element. The index-building step; quality here bounds everything.
- **Community detection**: clustering the graph into thematic communities (hierarchical — 
communities within communities). Each level answers different query granularities.
- **Community summaries**: LLM-written summaries per community, capturing its entities, 
relationships, and key claims. These are what global queries retrieve.
- **Local vs. global retrieval**: local — entity lookup + neighborhood traversal for specific 
questions; global — community summaries for corpus-wide questions. Route by query type.
- **Query-time traversal**: from matched entities, walk relationships to gather connected facts — 
multi-hop context assembled structurally, not by similarity luck.
- **Cost profile**: index building is expensive (LLM calls per chunk); querying is cheap. Best for 
stable corpora queried many times.

## Practical workflow

1. Confirm the need: test whether chunk-RAG actually fails on your corpus-level questions. GraphRAG 
is for when it does.
2. Build the graph on a sample first: inspect extracted entities and relations for quality before 
full-corpus indexing.
3. Tune extraction: entity types relevant to your domain, relationship granularity, claim capture.
4. Generate community summaries hierarchically; spot-check them against source documents.
5. Implement query routing: entity-centric → local traversal; thematic → community summaries.
6. Evaluate on corpus-level questions with human-judged comprehensiveness and faithfulness — 
standard retrieval metrics undermeasure this.

```text
GraphRAG decision checklist:
[ ] Chunk-RAG demonstrably fails on target questions
[ ] Corpus stable enough to amortize index-build cost
[ ] Extraction quality validated on samples
[ ] Community summaries spot-checked vs sources
[ ] Local/global routing implemented
[ ] Evaluated on corpus-level Q&A, human-judged
```

## Common pitfalls

- **GraphRAG for everything**: using it where chunk-RAG works fine. It's heavier — justify the 
cost with failing queries.
- **Unvalidated extraction**: noisy entities and relations produce a misleading map. Validate 
before summarizing.
- **Ignoring build cost**: full-corpus LLM extraction is expensive. Budget it; consider it in the 
build-vs-buy decision.
- **No query routing**: treating all queries the same. Local and global queries need different 
retrieval paths.
- **Stale graph**: corpus updates without graph rebuilds. Plan incremental updates or accept 
staleness explicitly.
- **Standard metrics only**: recall@k doesn't capture "did the answer synthesize the corpus well." 
Use human judgment for global questions.
