---
name: ai-searching-docs
description: Build AI that searches your documents and answers questions. Use when building a knowledge base, help center Q&A, chatting with documents, answering questions from a database, search-and-answer over internal docs, customer support bot, or FAQ system. Also use when embedding search loses critical context, retrieval returns irrelevant results, the right document is buried deep in search results, RAG pipeline tutorial, semantic search over documents, or vector database search quality.
---

# Build AI-Powered Document Search

Guide the user through building an AI that searches documents and answers questions accurately. Uses DSPy's RAG (retrieval-augmented generation) pattern — retrieve relevant passages, then generate an answer grounded in them.

## Step 0: Load your data

If you have documents in files, databases, or SaaS tools, use LangChain's document loaders to get them into a standard format before building your search pipeline.

### LangChain document loaders

```python
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    WebBaseLoader,
    DirectoryLoader,
    NotionDBLoader,
    JSONLoader,
)

# PDF files
docs = PyPDFLoader("report.pdf").load()

# All text files in a directory
docs = DirectoryLoader("./docs/", glob="**/*.txt", loader_cls=TextLoader).load()

# Web pages
docs = WebBaseLoader("https://example.com/help").load()

# CSV
docs = CSVLoader("data.csv", source_column="url").load()

# JSON
docs = JSONLoader("data.json", jq_schema=".records[]", content_key="text").load()
```

### Text splitting

Split loaded documents into chunks sized for embedding and retrieval:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)
# Each chunk has .page_content (text) and .metadata (source info)
```

| Splitter | Best for |
|----------|----------|
| `RecursiveCharacterTextSplitter` | General-purpose (recommended default) |
| `MarkdownHeaderTextSplitter` | Markdown docs — splits by heading |
| `TokenTextSplitter` | When you need strict token budgets |

### Vector store setup with LangChain

```python
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")  # or HuggingFaceEmbeddings, etc.
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")

# Use as a retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
results = retriever.invoke("How do refunds work?")
```

Other stores follow the same pattern: `Pinecone.from_documents(...)`, `FAISS.from_documents(...)`.

Once your data is loaded and chunked, wire it into a DSPy retriever (Step 3 below) or use ChromaDB directly. For the full LangChain/LangGraph API, see the [LangChain docs](https://python.langchain.com/docs/integrations/document_loaders/).

## Step 1: Understand the setup

Ask the user:
1. **What documents are you searching?** (PDFs, web pages, database, help articles, etc.)
2. **What kind of questions will users ask?** (factual lookups, how-to questions, multi-step research?)
3. **Do you have a search backend already?** (Elasticsearch, Pinecone, ChromaDB, pgvector, etc.)
4. **Do questions need info from multiple documents?** (simple lookup vs. combining info)

## Step 2: Build the search-and-answer pipeline

### Basic: search then answer

```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

class AnswerFromDocs(dspy.Signature):
    """Answer the question based on the given context."""
    context: list[str] = dspy.InputField(desc="Relevant passages from the knowledge base")
    question: str = dspy.InputField(desc="User's question")
    answer: str = dspy.OutputField(desc="Answer grounded in the context")

class DocSearch(dspy.Module):
    def __init__(self, num_passages=3):
        self.retrieve = dspy.Retrieve(k=num_passages)
        self.answer = dspy.ChainOfThought(AnswerFromDocs)

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.answer(context=context, question=question)
```

### Configure the search backend

DSPy supports multiple search backends. Set up via `dspy.configure`:

```python
# ColBERTv2 (hosted)
colbert = dspy.ColBERTv2(url="http://your-server:port/endpoint")
dspy.configure(lm=lm, rm=colbert)

# Or wrap your own search (Elasticsearch, Pinecone, pgvector, etc.)
class MySearchBackend(dspy.Retrieve):
    def forward(self, query, k=None):
        k = k or self.k
        # Your search logic here
        results = your_search_function(query, top_k=k)
        return dspy.Prediction(passages=[r["text"] for r in results])
```

## Step 3: Set up a vector store

If you do not have a search backend yet, set one up. For prototyping, use `dspy.Embeddings` (built-in, no external DB needed) or ChromaDB:

### DSPy built-in retriever (simplest option)

```python
embedder = dspy.Embedder("openai/text-embedding-3-small")  # or any supported model
retriever = dspy.Embeddings(corpus=corpus_texts, embedder=embedder, k=5)
# Uses FAISS for large corpora (>20K docs), brute-force for smaller ones
# Use retriever("query") to search — returns dspy.Prediction(passages=..., indices=...)
dspy.configure(lm=lm, rm=retriever)
```

### ChromaDB setup

```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("my_docs")
```

### Load and chunk documents

Split documents into passages before adding them to the vector store. Sentence-based chunking works well for most use cases:

```python
import re

def chunk_text(text, max_sentences=5):
    """Split text into chunks of N sentences."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    chunks = []
    for i in range(0, len(sentences), max_sentences):
        chunk = " ".join(sentences[i:i + max_sentences])
        if chunk:
            chunks.append(chunk)
    return chunks

# Load and chunk your documents
for doc in documents:
    chunks = chunk_text(doc["text"])
    collection.add(
        documents=chunks,
        ids=[f"{doc['id']}_chunk_{i}" for i in range(len(chunks))],
        metadatas=[{"source": doc["source"]}] * len(chunks),
    )
```

### Custom embeddings

ChromaDB uses its default embedding function, but you can swap in others:

```python
# SentenceTransformers (local, free)
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
ef = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# OpenAI embeddings (API, paid)
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
ef = OpenAIEmbeddingFunction(api_key="...", model_name="text-embedding-3-small")

collection = client.get_or_create_collection("my_docs", embedding_function=ef)
```

### Chunking strategies

| Strategy | How it works | Best for |
|----------|-------------|----------|
| Sentence-based | Split on sentence boundaries | Articles, docs, help pages |
| Fixed-size | Split every N characters with overlap | Long unstructured text |
| Paragraph | Split on double newlines | Well-structured documents |
| Overlap | Fixed-size with N-character overlap between chunks | When context at chunk boundaries matters |

### Wire it up as a DSPy retriever

```python
class ChromaRetriever(dspy.Retrieve):
    def __init__(self, collection, k=3):
        super().__init__(k=k)
        self.collection = collection

    def forward(self, query, k=None):
        k = k or self.k
        results = self.collection.query(query_texts=[query], n_results=k)
        return dspy.Prediction(passages=results["documents"][0])

# Use it
retriever = ChromaRetriever(collection)
dspy.configure(lm=lm, rm=retriever)
```

## Step 3b: Connect an existing vector store

If you already have a vector store, wire it up as a DSPy retriever. Each follows the same pattern — subclass `dspy.Retrieve` and implement `forward()`:

### Provider comparison

| Store | Type | Best for | Setup |
|-------|------|----------|-------|
| ChromaDB | Embedded | Prototyping, small datasets | `pip install chromadb` |
| Pinecone | Cloud | Managed, serverless, scales to billions | `pip install pinecone` |
| Qdrant | Self-hosted or cloud | Open-source, filtering, hybrid search | `pip install qdrant-client` |
| Weaviate | Self-hosted or cloud | Multi-modal, GraphQL, hybrid search | `pip install weaviate-client` |
| pgvector | Postgres extension | Teams already using Postgres | `pip install pgvector sqlalchemy` |

### Pinecone retriever

```python
from pinecone import Pinecone

class PineconeRetriever(dspy.Retrieve):
    def __init__(self, index_name, api_key, embed_fn, k=3):
        super().__init__(k=k)
        pc = Pinecone(api_key=api_key)
        self.index = pc.Index(index_name)
        self.embed_fn = embed_fn  # function: str -> list[float]

    def forward(self, query, k=None):
        k = k or self.k
        vector = self.embed_fn(query)
        results = self.index.query(vector=vector, top_k=k, include_metadata=True)
        passages = [m["metadata"]["text"] for m in results["matches"]]
        return dspy.Prediction(passages=passages)
```

### Qdrant retriever

```python
from qdrant_client import QdrantClient

class QdrantRetriever(dspy.Retrieve):
    def __init__(self, collection_name, url, embed_fn, k=3):
        super().__init__(k=k)
        self.client = QdrantClient(url=url)
        self.collection = collection_name
        self.embed_fn = embed_fn

    def forward(self, query, k=None):
        k = k or self.k
        vector = self.embed_fn(query)
        results = self.client.query_points(
            collection_name=self.collection, query=vector, limit=k,
        )
        passages = [p.payload["text"] for p in results.points]
        return dspy.Prediction(passages=passages)
```

### Weaviate retriever

```python
import weaviate

class WeaviateRetriever(dspy.Retrieve):
    def __init__(self, collection_name, url, k=3):
        super().__init__(k=k)
        self.client = weaviate.connect_to_local(url=url)  # or connect_to_weaviate_cloud
        self.collection = self.client.collections.get(collection_name)

    def forward(self, query, k=None):
        k = k or self.k
        results = self.collection.query.near_text(query=query, limit=k)
        passages = [o.properties["text"] for o in results.objects]
        return dspy.Prediction(passages=passages)
```

### pgvector retriever (PostgreSQL)

```python
from sqlalchemy import create_engine, text

class PgvectorRetriever(dspy.Retrieve):
    def __init__(self, engine, table, embed_fn, k=3):
        super().__init__(k=k)
        self.engine = engine
        self.table = table
        self.embed_fn = embed_fn

    def forward(self, query, k=None):
        k = k or self.k
        vector = self.embed_fn(query)
        sql = text(f"""
            SELECT content FROM {self.table}
            ORDER BY embedding <=> :vec LIMIT :k
        """)
        with self.engine.connect() as conn:
            rows = conn.execute(sql, {"vec": str(vector), "k": k}).fetchall()
        passages = [row[0] for row in rows]
        return dspy.Prediction(passages=passages)
```

All of these work as drop-in replacements for `dspy.Retrieve`:

```python
retriever = PineconeRetriever("my-index", api_key="...", embed_fn=embed)
dspy.configure(lm=lm, rm=retriever)
# Or pass directly to your module
```

## Step 4: Multi-document search (for complex questions)

When questions need info from multiple places:

```python
class GenerateSearchQuery(dspy.Signature):
    """Generate a search query to find missing information."""
    context: list[str] = dspy.InputField(desc="Information gathered so far")
    question: str = dspy.InputField(desc="The question to answer")
    query: str = dspy.OutputField(desc="Search query to find missing information")

class MultiStepSearch(dspy.Module):
    def __init__(self, num_passages=3, num_searches=2):
        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate_query = [dspy.ChainOfThought(GenerateSearchQuery) for _ in range(num_searches)]
        self.answer = dspy.ChainOfThought(AnswerFromDocs)

    def forward(self, question):
        context = []

        for hop in self.generate_query:
            query = hop(context=context, question=question).query
            passages = self.retrieve(query).passages
            context = deduplicate(context + passages)

        return self.answer(context=context, question=question)

def deduplicate(passages):
    seen = set()
    result = []
    for p in passages:
        if p not in seen:
            seen.add(p)
            result.append(p)
    return result
```

## Step 5: Test the quality

```python
def search_metric(example, prediction, trace=None):
    # Exact match (simple)
    return prediction.answer == example.answer

# Or use an AI judge for open-ended answers
class JudgeAnswer(dspy.Signature):
    """Is the predicted answer correct given the expected answer?"""
    question: str = dspy.InputField()
    gold_answer: str = dspy.InputField()
    predicted_answer: str = dspy.InputField()
    is_correct: bool = dspy.OutputField()

def judge_metric(example, prediction, trace=None):
    judge = dspy.Predict(JudgeAnswer)
    result = judge(
        question=example.question,
        gold_answer=example.answer,
        predicted_answer=prediction.answer,
    )
    return result.is_correct
```

## Step 6: Improve accuracy

```python
optimizer = dspy.BootstrapFewShot(metric=search_metric, max_bootstrapped_demos=4)
optimized = optimizer.compile(DocSearch(), trainset=trainset)

# Typical improvement: 45-60% exact match -> 65-80% after optimization
# For further gains, upgrade to MIPROv2:
# optimizer = dspy.MIPROv2(metric=search_metric, auto="medium")
```

## When NOT to use RAG

- **Data fits in context** — if all your documents fit within the LM context window (under ~100K tokens), pass them directly as context instead of building a retrieval pipeline. RAG adds complexity for no benefit.
- **Questions are always about the same document** — if every query targets one known document, skip retrieval and just include it.
- **You need exact keyword search** — if users search by ID, SKU, or exact phrases, a database query or full-text search (Elasticsearch, Postgres `tsvector`) outperforms embedding search. Use RAG only when queries are semantic.
- **Real-time data** — if the answer changes every minute (stock prices, live dashboards), a retrieval index will be stale. Query the source directly.

## Key patterns

- **Prefer `ChainOfThought`** for the answer step — reasoning typically helps ground answers in the documents. Use `Predict` if latency matters more than accuracy
- **Include context in the signature** so the AI knows to use the retrieved passages
- **Multi-step search for complex questions** — if one search is not enough, chain search queries
- **Use `dspy.Refine`** to ensure answers actually cite the documents by scoring citation presence in a reward function
- **Separate search from answer generation** — optimize each independently
- **Consider joint prompt + retrieval optimization** — the GEPA paper (arxiv 2507.19457) shows a RAG adapter that jointly optimizes prompts and retrieval strategy for multiplicative gains. See `/dspy-gepa` for details
- **Consider `dspy.Embeddings`** as a built-in retriever — it handles embedding, FAISS indexing, and search in one class without needing a separate vector store (see reference.md for API details)

## Gotchas

- **Chunk size matters more than retriever choice** — most RAG failures trace to bad chunking, not bad embeddings. Start with 512 tokens with 50-token overlap and tune from there.
- **Do not skip the reranking step** — embedding similarity retrieves candidates; a reranker (or LM-based reranker) filters them. Without reranking, irrelevant passages dilute the context.
- **k=3 is not always right** — the default `k` (number of retrieved passages) is a critical hyperparameter. Too few and you miss relevant context; too many and you overwhelm the LM. Tune it against your dev set.
- **Test with questions that require combining information** — single-hop retrieval fails when the answer spans multiple chunks. Use `dspy.ChainOfThought` with multi-step retrieval for these cases.
- **Embedding models and chunk sizes must match at index and query time** — if you re-chunk or switch embedding models, you must rebuild the vector index. Stale indexes silently return bad results.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- Need to summarize docs instead of answering questions? Use `/ai-summarizing`
- Put your document search behind a REST API — see `/ai-serving-apis`
- Building a chatbot on top of doc search? Use `/ai-building-chatbots`
- Measure and improve your AI — see `/ai-improving-accuracy`
- Define input/output contracts for your signatures — see `/dspy-signatures`
- Add reasoning to your answer step — see `/dspy-chain-of-thought`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- For DSPy retrieval API details (Embeddings, Retrieve, ColBERTv2, Embedder), see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md)
