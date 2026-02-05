---
name: rag-systems
description: Retrieval Augmented Generation systems with vector search, document processing, and hybrid retrieval.
sasmp_version: "1.3.0"
bonded_agent: 03-rag-systems
bond_type: PRIMARY_BOND
---

# RAG Systems

Build production-grade Retrieval Augmented Generation pipelines.

## Quick Start

### Simple RAG with LangChain
```python
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# 1. Load documents
loader = PyPDFLoader("document.pdf")
documents = loader.load()

# 2. Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = splitter.split_documents(documents)

# 3. Create embeddings and store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)

# 4. Create RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
)

# 5. Query
answer = qa_chain.run("What is the main topic?")
```

## Core Components

### Document Processing Pipeline
```python
from typing import List
import hashlib

class DocumentProcessor:
    def __init__(self, chunk_size=1000, overlap=200):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def process(self, documents: List[str]) -> List[dict]:
        processed = []
        for doc in documents:
            # Clean text
            cleaned = self._clean_text(doc)

            # Split into chunks
            chunks = self._chunk_text(cleaned)

            # Add metadata
            for i, chunk in enumerate(chunks):
                processed.append({
                    'id': self._generate_id(chunk),
                    'text': chunk,
                    'chunk_index': i,
                    'total_chunks': len(chunks)
                })

        return processed

    def _chunk_text(self, text: str) -> List[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]

            # Find natural break point
            if end < len(text):
                last_period = chunk.rfind('.')
                if last_period > self.chunk_size // 2:
                    end = start + last_period + 1
                    chunk = text[start:end]

            chunks.append(chunk.strip())
            start = end - self.overlap

        return chunks
```

### Embedding Strategies
```python
from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingService:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts, show_progress_bar=True)

    def embed_query(self, query: str) -> np.ndarray:
        # Query prefix for asymmetric retrieval
        return self.model.encode(f"query: {query}")
```

### Retrieval Methods
```yaml
Dense Retrieval:
  description: Semantic similarity using embeddings
  pros: Captures meaning, handles synonyms
  cons: Computationally expensive
  use_when: Semantic understanding needed

Sparse Retrieval (BM25):
  description: Keyword matching with TF-IDF
  pros: Fast, exact matching
  cons: Misses synonyms
  use_when: Exact term matching important

Hybrid Retrieval:
  description: Combines dense + sparse
  pros: Best of both worlds
  cons: More complex setup
  use_when: Production systems
```

## RAG Architecture Patterns

### Basic RAG
```
Query → Embed → Search → Retrieve Top-K → Generate Answer
```

### Advanced RAG with Re-ranking
```python
from typing import List, Tuple

class AdvancedRAG:
    def __init__(self, retriever, reranker, llm):
        self.retriever = retriever
        self.reranker = reranker
        self.llm = llm

    def query(self, question: str, k: int = 10) -> str:
        # 1. Initial retrieval (over-fetch)
        candidates = self.retriever.search(question, k=k*3)

        # 2. Re-rank with cross-encoder
        reranked = self.reranker.rerank(question, candidates)[:k]

        # 3. Build context
        context = "\n\n".join([doc.text for doc in reranked])

        # 4. Generate answer
        prompt = f"""Context: {context}

Question: {question}

Answer based on the context above:"""

        return self.llm.generate(prompt)
```

### Query Expansion
```python
def expand_query(query: str, llm) -> List[str]:
    """Generate alternative phrasings of the query."""
    prompt = f"""Generate 3 alternative ways to ask this question:
    Original: {query}

    Alternatives:
    1."""

    response = llm.generate(prompt)
    alternatives = parse_alternatives(response)

    return [query] + alternatives
```

## Chunking Strategies

| Strategy | Chunk Size | Overlap | Best For |
|----------|------------|---------|----------|
| Fixed | 500-1000 | 50-100 | General documents |
| Sentence | 3-5 sentences | 1 sentence | Conversations |
| Paragraph | Natural breaks | None | Structured docs |
| Semantic | By topic | Topic boundary | Long documents |
| Recursive | Hierarchical | Varies | Code, markdown |

## Evaluation Metrics

```python
def evaluate_rag(qa_pairs, rag_system):
    metrics = {
        'faithfulness': [],  # Is answer grounded in context?
        'relevance': [],     # Is retrieved context relevant?
        'answer_quality': [] # Is answer correct and helpful?
    }

    for qa in qa_pairs:
        answer, contexts = rag_system.query_with_sources(qa['question'])

        metrics['faithfulness'].append(
            check_faithfulness(answer, contexts)
        )
        metrics['relevance'].append(
            check_relevance(contexts, qa['question'])
        )
        metrics['answer_quality'].append(
            compare_answers(answer, qa['expected'])
        )

    return {k: np.mean(v) for k, v in metrics.items()}
```

## Best Practices

1. **Chunk wisely**: Balance context vs. precision
2. **Use metadata**: Filter before semantic search
3. **Re-rank results**: Cross-encoders improve quality
4. **Cache embeddings**: Avoid recomputation
5. **Monitor retrieval**: Track relevance scores
6. **Handle no-results**: Graceful fallback responses

## Error Handling & Retry

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def embed_with_retry(text):
    return embedding_model.encode(text)

def query_with_fallback(question):
    try:
        return vector_search(question)
    except Exception:
        return keyword_search(question)  # Fallback
```

## Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| No results | Threshold too high | Lower similarity_threshold |
| Wrong answers | Poor chunking | Adjust chunk_size |
| Slow queries | Large index | Add HNSW indexing |

## Unit Test Template

```python
def test_rag_retrieval():
    rag.index(["Test document"])
    results = rag.search("test")
    assert len(results) > 0
```
