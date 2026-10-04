---
name: dspy-retrieval
description: DSPy retrieval modules (dspy.Retrieve, dspy.ColBERTv2, dspy.Embedder, dspy.retrievers.Embeddings) for searching documents, computing embeddings, and building RAG pipelines. Use when you need to search over documents, build a RAG pipeline, connect DSPy to a vector database, compute embeddings for semantic search, set up ChromaDB or Pinecone with DSPy, or build knowledge-grounded question answering. Also used for RAG pipeline in DSPy, vector database integration, semantic search, embedding retrieval, retrieval augmented generation setup, connect knowledge base to DSPy, search documents then answer, grounded generation with retrieval.
---

# Retrieval Modules in DSPy

Guide the user through DSPy's retrieval modules for searching documents, computing embeddings, and building RAG (retrieval-augmented generation) pipelines.

## Step 1: Gather context

Before building retrieval into a DSPy program, clarify:

1. **What are you searching over?** Your own documents, a knowledge base, an external corpus like Wikipedia?
2. **How large is the corpus?** A few hundred docs (in-memory FAISS works) vs. millions (need a dedicated vector store like Pinecone, Qdrant, or Chroma)?
3. **Do you already have a search backend?** If you have Elasticsearch, Pinecone, or another store, subclass `dspy.Retrieve` to wrap it. If not, use `dspy.retrievers.Embeddings` for a local solution.
4. **Single-hop or multi-hop?** Simple questions need one retrieval step. Compositional questions (e.g., "Where was the designer of the Eiffel Tower born?") need chained retrieval.

## What retrieval modules are

DSPy provides retrieval modules that fetch relevant documents or passages given a query. These modules plug into DSPy programs just like `dspy.Predict` or `dspy.ChainOfThought` -- declare them in `__init__`, call them in `forward()`, and optimizers handle the rest.

There are four key components:

| Component | Purpose | When to use |
|-----------|---------|-------------|
| `dspy.Retrieve` | Base retriever class | Wrap any search backend (Elastic, Pinecone, etc.) |
| `dspy.ColBERTv2` | ColBERTv2 retrieval client | Query a hosted ColBERTv2 server |
| `dspy.Embedder` | Compute embeddings | Turn text into vectors using any LiteLLM-supported model |
| `dspy.retrievers.Embeddings` | Local vector search | Build a retriever from an embedder + corpus, uses FAISS |

> `dspy.retrievers.WeaviateRM` and `dspy.retrievers.DatabricksRM` also exist in the source as undocumented `dspy.Retrieve` subclasses requiring optional extras (`pip install dspy-ai[weaviate]`). Use them with caution — no official docs page, API may change.

## dspy.Retrieve

The base class for all retrievers. Use it directly with a configured retrieval model (`rm`), or subclass it to wrap your own search backend.

### Using with a configured RM

```python
import dspy

# Configure a retrieval model globally
colbert = dspy.ColBERTv2(url="http://your-server:8893/api/search")
lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm, rm=colbert)

# Use dspy.Retrieve -- it delegates to the configured rm
retriever = dspy.Retrieve(k=5)
result = retriever("What is retrieval-augmented generation?")
print(result.passages)  # list[str] of top-k passages
```

### Key parameters

- **`k`** (int) -- number of passages to retrieve. Can be set at init time or overridden per call.

### Return value

`dspy.Retrieve` returns a `dspy.Prediction` with a `.passages` attribute -- a `list[str]` of the top-k retrieved passages.

### Subclassing for custom backends

Wrap any search system by subclassing `dspy.Retrieve` and implementing `forward()`:

```python
class MyRetriever(dspy.Retrieve):
    def __init__(self, search_client, k=3):
        super().__init__(k=k)
        self.client = search_client

    def forward(self, query, k=None):
        k = k or self.k
        results = self.client.search(query, top_k=k)
        return dspy.Prediction(passages=[r["text"] for r in results])
```

The `forward()` method must:
1. Accept `query` (str) and optional `k` (int)
2. Return a `dspy.Prediction` with a `passages` field (list of strings)

## dspy.ColBERTv2

A retrieval client that queries a hosted ColBERTv2 server. ColBERTv2 is a neural retrieval model that provides high-quality passage retrieval.

### Constructor

```python
colbert = dspy.ColBERTv2(url="http://your-server:8893/api/search")
```

**Parameters:**
- **`url`** (str) -- URL of the ColBERTv2 server endpoint

### Usage

```python
# Direct call
results = colbert("What is DSPy?", k=3)
# Returns list of dicts with 'text', 'score', etc.

# As a configured retrieval model
dspy.configure(lm=lm, rm=colbert)
retriever = dspy.Retrieve(k=5)
passages = retriever("search query").passages
```

### Setting up a ColBERTv2 server

Stanford hosts a public ColBERTv2 server for Wikipedia that you can use for testing:

```python
colbert = dspy.ColBERTv2(url="http://20.102.90.50:2017/wiki17_abstracts")
dspy.configure(lm=lm, rm=colbert)
```

For your own data, you need to run a ColBERTv2 server. See the [ColBERT repository](https://github.com/stanford-futuredata/ColBERT) for setup instructions.

## dspy.Embedder

Computes embeddings for text using any LiteLLM-supported embedding model. This is not a retriever itself -- it turns text into vectors that you can use with `dspy.retrievers.Embeddings` or your own vector store.

### Constructor

```python
embedder = dspy.Embedder(
    "openai/text-embedding-3-small",  # model identifier (LiteLLM format)
    dimensions=512,                    # optional: output dimensions
)
```

**Parameters:**
- **model** (str | Callable) -- embedding model in LiteLLM format (e.g., `"openai/text-embedding-3-small"`, `"cohere/embed-english-v3.0"`), or a callable for custom embedding functions
- **batch_size** (int, default 200) -- batch size for embedding multiple texts
- **caching** (bool, default True) -- whether to cache embedding responses for hosted models
- **\*\*kwargs** -- additional model-specific arguments (e.g., `dimensions=512` for models that support it)

### Usage

```python
# Embed a single text
vector = embedder("What is DSPy?")
# Returns a 1D numpy array

# Embed multiple texts
vectors = embedder(["text one", "text two", "text three"])
# Returns a 2D numpy array (shape: num_texts x embedding_dim)
```

### Supported providers

Any embedding model supported by LiteLLM works:

```python
# OpenAI
embedder = dspy.Embedder("openai/text-embedding-3-small")

# Cohere
embedder = dspy.Embedder("cohere/embed-english-v3.0")

# Local via Ollama
embedder = dspy.Embedder("ollama/nomic-embed-text")
```

## dspy.retrievers.Embeddings

A local vector search retriever that uses FAISS under the hood. Give it an `Embedder` and a corpus, and it builds an in-memory index for fast similarity search.

### Constructor

```python
import dspy

embedder = dspy.Embedder("openai/text-embedding-3-small", dimensions=512)
search = dspy.retrievers.Embeddings(
    corpus=corpus,      # list[str] of documents
    embedder=embedder,
    k=5,                # number of results to return (default 5)
)
```

**Parameters:**
- **`corpus`** (list[str]) -- the documents to index and search over
- **`embedder`** -- a `dspy.Embedder` instance
- **`k`** (int, default 5) -- default number of results to return
- **`brute_force_threshold`** (int, default 20000) -- corpus size above which FAISS indexing kicks in (below this, brute-force search)
- **`normalize`** (bool, default True) -- whether to normalize embeddings

### Saving and loading embeddings

Avoid re-embedding large corpora on every run:

```python
# Save after initial indexing
search.save("./my_embeddings")

# Load later without re-computing
search = dspy.retrievers.Embeddings.from_saved("./my_embeddings", embedder=embedder)
```

### Usage

```python
# Search
result = search("How do I reset my password?")
print(result.passages)  # list[str] of top-k matching documents

# Use in a module
class QA(dspy.Module):
    def __init__(self, search):
        self.search = search
        self.answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.search(question).passages
        return self.answer(context=context, question=question)
```

### When to use Embeddings vs. ColBERTv2

| Scenario | Use |
|----------|-----|
| Quick prototyping with small-medium corpus | `dspy.retrievers.Embeddings` |
| Need a hosted, scalable retrieval server | `dspy.ColBERTv2` |
| Already have a vector store (Pinecone, Chroma, etc.) | Subclass `dspy.Retrieve` |
| Need full control over embeddings | `dspy.Embedder` + your own vector store |

## Building RAG pipelines

RAG is the most common use of retrieval in DSPy. The pattern: retrieve relevant passages, then generate an answer grounded in them.

### Basic RAG

```python
import dspy

class RAG(dspy.Module):
    def __init__(self, retriever, k=3):
        self.retrieve = retriever
        self.generate = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.generate(context=context, question=question)

# With Embeddings retriever
embedder = dspy.Embedder("openai/text-embedding-3-small", dimensions=512)
search = dspy.retrievers.Embeddings(embedder=embedder, corpus=my_docs, k=5)
rag = RAG(retriever=search)
result = rag(question="How do refunds work?")
print(result.answer)
```

### RAG with source grounding

Use `dspy.Refine` to enforce that answers stay grounded in the retrieved context:

```python
class GroundedRAG(dspy.Module):
    def __init__(self, retriever):
        self.retrieve = retriever
        self.generate = dspy.ChainOfThought(
            "context, question -> answer, cited_sources: list[int]"
        )

    def forward(self, question):
        passages = self.retrieve(question).passages
        result = self.generate(context=passages, question=question)
        return dspy.Prediction(
            answer=result.answer,
            cited_sources=result.cited_sources,
            passages=passages,
        )

def grounding_reward(args, pred):
    score = 1.0
    if not pred.cited_sources or len(pred.cited_sources) == 0:
        score -= 0.3  # soft penalty for missing citations
    return score

grounded_rag = dspy.Refine(module=GroundedRAG(retriever=search), N=3, reward_fn=grounding_reward, threshold=0.8)
```

### Multi-hop RAG

When a question needs information from multiple documents, chain retrieval steps:

```python
class MultiHopRAG(dspy.Module):
    def __init__(self, retriever, hops=2):
        self.retrieve = retriever
        self.generate_query = [
            dspy.ChainOfThought("context, question -> search_query")
            for _ in range(hops)
        ]
        self.answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = []
        for hop in self.generate_query:
            query = hop(context=context, question=question).search_query
            new_passages = self.retrieve(query).passages
            context = list(dict.fromkeys(context + new_passages))  # deduplicate

        return self.answer(context=context, question=question)
```

## Configuring retrievers

There are two ways to wire up a retriever:

### Option 1: Global configuration with dspy.configure

```python
colbert = dspy.ColBERTv2(url="http://your-server:8893/api/search")
dspy.configure(lm=lm, rm=colbert)

# dspy.Retrieve() now uses colbert automatically
retriever = dspy.Retrieve(k=5)
```

### Option 2: Pass the retriever directly

```python
embedder = dspy.Embedder("openai/text-embedding-3-small")
search = dspy.retrievers.Embeddings(embedder=embedder, corpus=docs, k=5)

class MyRAG(dspy.Module):
    def __init__(self):
        self.search = search  # use directly, no global config needed
        self.answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.search(question).passages
        return self.answer(context=context, question=question)
```

Option 2 is more explicit and avoids global state. Prefer it when your program uses a single retriever.

## The k parameter

The `k` parameter controls how many passages to retrieve. It can be set at multiple levels:

```python
# At init time
retriever = dspy.Retrieve(k=5)

# Override per call
result = retriever("query", k=10)

# In Embeddings constructor
search = dspy.retrievers.Embeddings(embedder=embedder, corpus=docs, k=3)
```

**Choosing k:**
- Start with `k=3` to `k=5` for most tasks
- Increase `k` for questions that need broader context
- Decrease `k` for faster inference and lower token costs
- More passages means more context for the LM, but also more noise and higher cost
- Use evaluation to find the optimal `k` for your specific task

## Grounded generation with Citations

`dspy.experimental.Citations` is a **type** (not a module) that you use as an `OutputField` to get structured source references from the LM. It works with Anthropic models that support native citations, or falls back to LM-generated citation extraction.

```python
from dspy.experimental import Citations, Document

class AnswerWithSources(dspy.Signature):
    """Answer the question and cite the source documents."""
    documents: list[Document] = dspy.InputField()
    question: str = dspy.InputField()
    answer: str = dspy.OutputField()
    citations: Citations = dspy.OutputField()

lm = dspy.LM("anthropic/claude-sonnet-4-5-20250929")  # or "openai/gpt-4o", etc.
predictor = dspy.Predict(AnswerWithSources)
result = predictor(documents=docs, question="What is the refund policy?")
# result.citations contains structured Citation objects with cited_text, document_index, etc.
```

**When to use:** RAG pipelines where claims need to trace back to source documents with exact quoted text and document indices.

**Note:** This is in `dspy.experimental` — the API may change. For broader anti-hallucination patterns, see `/ai-stopping-hallucinations`.

## When not to use retrieval

- **Small, static knowledge base that fits in the prompt.** If your docs are under ~10-20 passages total, embed them directly in the system prompt instead of building a retrieval pipeline. Retrieval adds latency, embedding cost, and a retrieval-quality failure mode that does not exist when everything is in context.
- **Facts that change faster than you can re-index.** If the source data updates every minute (live prices, inventory), retrieval over stale embeddings is worse than no retrieval. Prefer a live API call or database lookup instead.
- **Single-turn factual lookups on well-known data.** For questions a capable LM already knows (dates, capitals, common definitions), retrieval adds cost and latency without improving accuracy. Try without retrieval first and only add it when the LM makes factual errors on your specific domain.
- **Avoid retrieval as a substitute for prompt engineering.** Before adding a retrieval pipeline, check whether adding a few inline examples or a clearer signature fixes the problem.

## Gotchas

- **Using `dspy.Retrieve` without configuring `rm`.** Claude often writes `dspy.Retrieve(k=5)` without setting `dspy.configure(rm=...)` first. Without a configured retrieval model, calling `Retrieve` raises a confusing error. Either configure `rm` globally or pass a concrete retriever (like `dspy.retrievers.Embeddings`) directly to your module.
- **Re-embedding the corpus on every run.** Claude builds `dspy.retrievers.Embeddings(corpus=docs, embedder=embedder)` in scripts without saving. For corpora over a few hundred docs, this wastes time and API calls. Use `search.save("./embeddings")` after initial indexing and `Embeddings.from_saved("./embeddings", embedder=embedder)` on subsequent runs.
- **Forgetting `.with_inputs()` on RAG examples.** When building training data for RAG optimization, Claude creates `dspy.Example(question=q, answer=a)` without calling `.with_inputs("question")`. The optimizer silently treats all fields as inputs. Always chain `.with_inputs()` to mark which fields are inputs vs. expected outputs.
- **Returning raw dicts instead of `dspy.Prediction` from custom retrievers.** When subclassing `dspy.Retrieve`, the `forward()` method must return `dspy.Prediction(passages=[...])` — not a list or dict. Returning the wrong type causes downstream modules to fail when they access `.passages`.
- **Setting k too high for the context window.** Claude defaults to `k=10` or higher, which can stuff too many passages into the generation prompt and exceed the LM context or degrade answer quality. Start with `k=3` to `k=5` and increase based on evaluation results.

## Additional resources

- [dspy.ColBERTv2 API docs](https://dspy.ai/api/tools/ColBERTv2/)
- [dspy.retrievers.Embeddings API docs](https://dspy.ai/api/tools/Embeddings/)
- [dspy.Embedder API docs](https://dspy.ai/api/models/Embedder/)
- [dspy.Retrieve source](https://github.com/stanfordnlp/dspy/blob/main/dspy/retrievers/retrieve.py) (no dedicated docs page; base class for custom retrievers)
- For API details, see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md)

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Building custom modules** to wrap retrieval logic -- see `/dspy-modules`
- **Vector database setup** (Qdrant, Pinecone, ChromaDB, Weaviate) -- see `/dspy-qdrant`
- **End-to-end document search** with vector stores and chunking -- see `/ai-searching-docs`
- **Keeping answers grounded** and avoiding hallucination -- see `/ai-stopping-hallucinations`
- **Dynamic few-shot selection** using `dspy.KNN` with the same embedder infrastructure -- see `/dspy-knn-few-shot`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
