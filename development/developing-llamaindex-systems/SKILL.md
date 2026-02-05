---
name: developing-llamaindex-systems
description: >-
  Production-grade agentic system development with LlamaIndex in Python.
  Covers semantic ingestion (SemanticSplitterNodeParser, CodeSplitter, IngestionPipeline),
  retrieval strategies (BM25Retriever, hybrid search, alpha weighting),
  PropertyGraphIndex with graph stores (Neo4j), context RAG (RouterQueryEngine,
  SubQuestionQueryEngine, LLMRerank), agentic orchestration (ReAct, Workflows,
  FunctionTool), and observability (Arize Phoenix). Use when asked to
  "build a LlamaIndex agent", "set up semantic chunking", "index source code",
  "implement hybrid search", "create a knowledge graph with LlamaIndex",
  "implement query routing", "debug RAG pipeline", "add Phoenix observability",
  or "create an event-driven workflow". Triggers on "PropertyGraphIndex",
  "SemanticSplitterNodeParser", "CodeSplitter", "BM25Retriever", "hybrid search",
  "ReAct agent", "Workflow pattern", "LLMRerank", "Text-to-Cypher".
allowed-tools:
  - Read
  - Write
  - Bash
  - WebFetch
  - Grep
  - Glob
metadata:
  version: 1.2.0
  last-updated: 2025-12-28
  category: frameworks
  python-version: ">=3.9"
---

# LlamaIndex Agentic Systems

Build production-grade agentic RAG systems with semantic ingestion, knowledge graphs, dynamic routing, and observability.

## Quick Start

Build a working agent in 6 steps:

### Step 1: Install Dependencies

```bash
pip install llama-index-core>=0.10.0 llama-index-llms-openai llama-index-embeddings-openai arize-phoenix
```

See [scripts/requirements.txt](scripts/requirements.txt) for full pinned dependencies.

### Step 2: Ingest with Semantic Chunking

```python
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding

embed_model = OpenAIEmbedding(model_name="text-embedding-3-small")
splitter = SemanticSplitterNodeParser(
    buffer_size=1,
    breakpoint_percentile_threshold=95,
    embed_model=embed_model
)

docs = SimpleDirectoryReader(input_files=["data.pdf"]).load_data()
nodes = splitter.get_nodes_from_documents(docs)
```

### Step 3: Build Index

```python
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex(nodes, embed_model=embed_model)
index.storage_context.persist(persist_dir="./storage")
```

### Step 4: Verify Index

```python
# Confirm index built correctly
print(f"Indexed {len(index.docstore.docs)} document chunks")

# Preview a sample node
sample = list(index.docstore.docs.values())[0]
print(f"Sample chunk: {sample.text[:200]}...")
```

### Step 5: Create Query Engine

```python
query_engine = index.as_query_engine(similarity_top_k=5)
response = query_engine.query("What are the key concepts?")
print(response)
```

### Step 6: Enable Observability

```python
import phoenix as px
import llama_index.core

px.launch_app()
llama_index.core.set_global_handler("arize_phoenix")
# All subsequent queries are now traced
```

For production script, run: `python scripts/ingest_semantic.py`

---

## Architecture Overview

Six pillars for agentic systems:

| Pillar | Purpose | Reference |
|--------|---------|-----------|
| **Ingestion** | Semantic chunking, code splitting, metadata | [references/ingestion.md](references/ingestion.md) |
| **Retrieval** | BM25 keyword search, hybrid fusion | [references/retrieval-strategies.md](references/retrieval-strategies.md) |
| **Property Graphs** | Knowledge graphs + vector hybrid | [references/property-graphs.md](references/property-graphs.md) |
| **Context RAG** | Query routing, decomposition, reranking | [references/context-rag.md](references/context-rag.md) |
| **Orchestration** | ReAct agents, event-driven Workflows | [references/orchestration.md](references/orchestration.md) |
| **Observability** | Tracing, debugging, evaluation | [references/observability.md](references/observability.md) |

---

## Decision Trees

### Which Node Parser?

```
Is the content source code?
├─ Yes → CodeSplitter
│        language="python" (or typescript, javascript, java, go)
│        chunk_lines=40, chunk_lines_overlap=15
│        → See: references/ingestion.md#codesplitter
│
└─ No, it's documents:
    ├─ Need semantic coherence (legal, technical docs)?
    │   └─ Yes → SemanticSplitterNodeParser
    │            buffer_size=1 (sensitive), 3 (stable)
    │            breakpoint_percentile_threshold=95 (fewer), 70 (more)
    │            → See: references/ingestion.md#semanticsplitternodeparser
    │
    ├─ Prioritize speed → SentenceSplitter
    │        chunk_size=1024, chunk_overlap=20
    │        → See: references/ingestion.md#sentencesplitter
    │
    └─ Need fine-grained retrieval → SentenceWindowNodeParser
             window_size=3 (surrounding sentences in metadata)
             → See: references/ingestion.md#sentencewindownodeparser
```

**Trade-off:** Semantic chunking requires embedding calls during ingestion (cost + latency).

### Which Retrieval Mode?

```
Query contains exact terms (function names, error codes, IDs)?
├─ Yes, exact match critical → BM25
│        retriever = BM25Retriever.from_defaults(nodes=nodes)
│        → See: references/retrieval-strategies.md#bm25retriever
│
├─ Conceptual/semantic query → Vector
│        retriever = index.as_retriever(similarity_top_k=5)
│        → See: references/context-rag.md
│
└─ Mixed or unknown query type → Hybrid (recommended default)
         alpha=0.5 (equal weight), 0.3 (favor BM25), 0.7 (favor vector)
         → See: references/retrieval-strategies.md#hybrid-search
```

**Trade-off:** Hybrid adds BM25 index overhead but provides most robust retrieval.

### Which Graph Extractor?

```
Need document navigation only (prev/next/parent)?
├─ Yes → ImplicitPathExtractor (no LLM, zero cost)
│        → See: references/property-graphs.md#implicitpathextractor
│
└─ No, need semantic relationships:
    ├─ Fixed ontology required (regulated domain)?
    │   └─ Yes → SchemaLLMPathExtractor
    │            Pass schema: {"PERSON": ["WORKS_AT"], "COMPANY": ["LOCATED_IN"]}
    │            → See: references/property-graphs.md#schemallmpathextractor
    │
    └─ No, discovery/exploration:
        └─ SimpleLLMPathExtractor
           max_paths_per_chunk=10 (control noise)
           → See: references/property-graphs.md#simplellmpathextractor
```

### Which Graph Retriever?

```
Need SQL-like aggregations (COUNT, SUM)?
├─ Yes, trusted environment → TextToCypherRetriever
│        Risk: LLM syntax errors, injection
│        → See: references/property-graphs.md#texttocypherretriever
│
├─ Yes, need safety → CypherTemplateRetriever
│        Pre-define: MATCH (p:Person {name: $name}) RETURN p
│        LLM only extracts parameters
│        → See: references/property-graphs.md#cyphertemplateretriever
│
└─ No, robustness priority → VectorContextRetriever
         Vector search → graph traversal (path_depth=2)
         Most reliable, no code generation
         → See: references/property-graphs.md#vectorcontextretriever
```

### Which Agent Pattern?

```
Simple tool loop sufficient?
├─ Yes → ReAct Agent (FunctionCallingAgent)
│        Tools via FunctionTool or ToolSpec
│        → See: references/orchestration.md#react-agent-pattern
│
└─ No, need:
    ├─ Branching/cycles → Workflow
    │   → See: references/orchestration.md#branching
    ├─ Human-in-the-loop → Workflow (suspend/resume)
    │   → See: references/orchestration.md#human-in-the-loop
    ├─ Multi-agent handoff → Workflow + Concierge pattern
    │   → See: references/orchestration.md#concierge-multi-agent
    └─ Parallel execution → Workflow with multiple event emissions
        → See: references/orchestration.md#workflows
```

---

## Common Patterns

### Pattern 1: Metadata-Enriched Ingestion

```python
from llama_index.core.extractors import TitleExtractor, SummaryExtractor, KeywordExtractor
from llama_index.core.ingestion import IngestionPipeline

pipeline = IngestionPipeline(
    transformations=[
        splitter,
        TitleExtractor(),
        SummaryExtractor(),
        KeywordExtractor(keywords=5),
        embed_model,
    ]
)
nodes = pipeline.run(documents=docs)
```

### Pattern 2: PropertyGraphIndex with Hybrid Retrieval

```python
from llama_index.core import PropertyGraphIndex
from llama_index.core.indices.property_graph import SimpleLLMPathExtractor

index = PropertyGraphIndex.from_documents(
    docs,
    embed_model=embed_model,
    kg_extractors=[SimpleLLMPathExtractor(max_paths_per_chunk=10)],
)

# Hybrid: vector search + graph traversal
retriever = index.as_retriever(include_text=True)
```

### Pattern 3: Router with Multiple Engines

```python
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.tools import QueryEngineTool

tools = [
    QueryEngineTool.from_defaults(
        query_engine=summary_engine,
        description="High-level summaries and overviews"
    ),
    QueryEngineTool.from_defaults(
        query_engine=detail_engine,
        description="Specific facts, numbers, and details"
    ),
]

router = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(),
    query_engine_tools=tools,
)
```

### Pattern 4: Event-Driven Workflow

```python
from llama_index.core.workflow import Workflow, step, StartEvent, StopEvent, Event

class QueryEvent(Event):
    query: str

class MyAgent(Workflow):
    @step
    async def classify(self, ev: StartEvent) -> QueryEvent:
        return QueryEvent(query=ev.get("query"))

    @step
    async def respond(self, ev: QueryEvent) -> StopEvent:
        result = self.query_engine.query(ev.query)
        return StopEvent(result=str(result))

# Run
agent = MyAgent(timeout=60)
result = await agent.run(query="What is X?")
```

### Pattern 5: Reranking Pipeline

```python
from llama_index.core.postprocessor import SimilarityPostprocessor, LLMRerank

query_engine = index.as_query_engine(
    similarity_top_k=10,  # Retrieve more
    node_postprocessors=[
        SimilarityPostprocessor(similarity_cutoff=0.7),
        LLMRerank(top_n=3),  # Rerank to top 3
    ]
)
```

---

## Script Reference

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/ingest_semantic.py` | Build index with semantic chunking + graph | `python scripts/ingest_semantic.py --doc path/to/file.pdf` |
| `scripts/agent_workflow.py` | Event-driven agent template | `python scripts/agent_workflow.py` |
| `scripts/requirements.txt` | Pinned dependencies | `pip install -r scripts/requirements.txt` |

Adapt scripts by modifying configuration variables at the top of each file.

---

## Reference Index

Load references based on task:

| Task | Load Reference |
|------|----------------|
| Configure chunking strategy | [references/ingestion.md](references/ingestion.md) |
| Add metadata extractors | [references/ingestion.md](references/ingestion.md) |
| Build knowledge graph | [references/property-graphs.md](references/property-graphs.md) |
| Choose graph store (Neo4j, etc.) | [references/property-graphs.md](references/property-graphs.md) |
| Implement query routing | [references/context-rag.md](references/context-rag.md) |
| Decompose complex queries | [references/context-rag.md](references/context-rag.md) |
| Add reranking | [references/context-rag.md](references/context-rag.md) |
| Build ReAct agent | [references/orchestration.md](references/orchestration.md) |
| Create Workflow | [references/orchestration.md](references/orchestration.md) |
| Multi-agent system | [references/orchestration.md](references/orchestration.md) |
| Setup Phoenix tracing | [references/observability.md](references/observability.md) |
| Debug retrieval failures | [references/observability.md](references/observability.md) |
| Evaluate agent quality | [references/observability.md](references/observability.md) |

---

## Troubleshooting

### Agent says "I don't know" with relevant data

**Diagnose:**
```bash
# Open Phoenix UI at http://localhost:6006
# Navigate to Traces → Select query → Retrieval span → Retrieved Nodes
```

**Fix:**
```python
# 1. Increase retrieval candidates
query_engine = index.as_query_engine(similarity_top_k=10)  # was 5

# 2. Add reranking to improve precision
from llama_index.core.postprocessor import LLMRerank
query_engine = index.as_query_engine(
    similarity_top_k=10,
    node_postprocessors=[LLMRerank(top_n=3)]
)
```

**Verify:** Re-run query, check Phoenix shows improved relevance scores (>0.7).

### Semantic chunking too slow

**Diagnose:**
```python
# Time the ingestion
import time
start = time.time()
nodes = splitter.get_nodes_from_documents(docs)
print(f"Chunking took {time.time() - start:.1f}s for {len(docs)} docs")
```

**Fix:**
```python
# Option 1: Use local embeddings (no API calls)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Option 2: Hybrid strategy for large corpora
bulk_nodes = SentenceSplitter().get_nodes_from_documents(bulk_docs)
critical_nodes = SemanticSplitterNodeParser(...).get_nodes_from_documents(critical_docs)
```

**Verify:** Re-run with `show_progress=True`, confirm <1s per document.

### Graph extraction producing noise

**Diagnose:**
```python
# Check extracted triples
for node in index.property_graph_store.get_triplets():
    print(node)  # Look for irrelevant or duplicate relationships
```

**Fix:**
```python
# Option 1: Reduce paths per chunk
SimpleLLMPathExtractor(max_paths_per_chunk=5)  # was 10

# Option 2: Use strict schema
SchemaLLMPathExtractor(
    possible_entities=["PERSON", "COMPANY"],
    possible_relations=["WORKS_AT", "FOUNDED"],
    strict=True
)
```

**Verify:** Re-index, confirm triplet count reduced and relationships are relevant.

### Workflow step not triggering

**Diagnose:**
```python
# Enable verbose mode
agent = MyWorkflow(timeout=60, verbose=True)
result = await agent.run(query="test")
# Check console for: [Step Name] Received event: EventType
```

**Fix:**
```python
# Verify type hints match exactly
class MyEvent(Event):
    query: str

@step
async def my_step(self, ev: MyEvent) -> StopEvent:  # Type hint must be MyEvent
    ...
```

**Verify:** Verbose output shows `[my_step] Received event: MyEvent`.

### Phoenix not showing traces

**Diagnose:**
```python
import phoenix as px
session = px.launch_app()
print(f"Phoenix URL: {session.url}")  # Should print http://localhost:6006
```

**Fix:**
```python
# MUST call BEFORE any LlamaIndex imports/operations
import phoenix as px
px.launch_app()

import llama_index.core
llama_index.core.set_global_handler("arize_phoenix")

# Now import and use LlamaIndex
from llama_index.core import VectorStoreIndex
```

**Verify:** Make a query, refresh Phoenix UI, trace appears within 5 seconds.

---

## When Not to Use This Skill

This skill is **specific to LlamaIndex in Python**. Do not use for:

- **LangChain projects** — Different framework, different APIs
- **Pure vector search without agents** — Simpler solutions exist
- **Non-Python environments** — All examples are Python 3.9+
- **Local-only / offline setups** — Scripts default to OpenAI APIs; modification required for local models
- **Simple Q&A bots** — Overkill if you don't need graphs, routing, or workflows

**If unsure:** Check if your use case involves semantic chunking, knowledge graphs, query routing, or multi-step agents. If yes, this skill applies.

---

## Glossary

| Term | Definition |
|------|------------|
| **Node** | Chunk of text with metadata, the atomic unit of retrieval |
| **PropertyGraphIndex** | Index combining vector embeddings with labeled property graph |
| **Extractor** | Component that generates graph triples from text |
| **Retriever** | Component that fetches relevant nodes/context |
| **Postprocessor** | Filters or reranks nodes after retrieval |
| **Workflow** | Event-driven state machine for agent orchestration |
| **Span** | Duration-tracked operation in observability |
