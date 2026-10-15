---
name: rag-pipelines
description: "RAG pipeline design — chunking, embeddings, retrieval strategies, evaluation, and demo patterns."
context: fork
globs: []
alwaysApply: false
---

# RAG Pipelines

Retrieval-Augmented Generation pipeline design: chunking, embeddings, vector stores, retrieval strategies, and evaluation.

---

## Pipeline Architecture

```
Documents → Chunk → Embed → Store → Retrieve → Generate
```

---

## Chunking Strategies

| Strategy | Best For | Chunk Size |
|----------|----------|------------|
| **Fixed-size** | General docs | 500-1000 tokens |
| **Semantic** | Long-form content | By paragraph/section |
| **Code-aware** | Source code | By function/class |
| **Recursive** | Mixed content | 1000 → 500 → 200 tokens |

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " ", ""]
)
```

---

## Embedding Models

| Model | Dimensions | Speed | Quality |
|-------|-----------|-------|---------|
| `text-embedding-3-small` | 1536 | Fast | Good |
| `text-embedding-3-large` | 3072 | Medium | Best |
| `bge-large-en` | 1024 | Fast | Good |
| `e5-large-v2` | 1024 | Fast | Good |

---

## Vector Stores

| Store | Use Case | Scaling |
|-------|----------|---------|
| **Pinecone** | Production, managed | Auto-scales |
| **Weaviate** | Production, self-hosted | Horizontal |
| **pgvector** | PostgreSQL shops | Vertical |
| **Chroma** | Prototyping, local | Single-node |

```python
from langchain.vectorstores import Chroma

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
```

---

## Retrieval Strategies

### Similarity Search
```python
retriever = vector_store.as_retriever(search_type="similarity", k=4)
```

### MMR (Diversity-focused)
```python
retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 4, "lambda_mult": 0.7}
)
```

### Hybrid (BM25 + Semantic)
```python
from langchain.retrievers import EnsembleRetriever

retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.3, 0.7]
)
```

### Self-Querying
```python
from langchain.retrievers.self_query.base import SelfQueryRetriever

retriever = SelfQueryRetriever.from_llm(
    llm, vector_store, document_contents, metadata_field_info
)
```

---

## Evaluation (RAGAS)

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevance, context_precision

result = evaluate(
    dataset=eval_dataset,
    metrics=[faithfulness, answer_relevance, context_precision]
)
```

| Metric | Target |
|--------|--------|
| Faithfulness | ≥0.8 |
| Answer Relevance | ≥0.8 |
| Context Precision | ≥0.7 |

---

## Demo Patterns

### Gradio
```python
import gradio as gr

def answer(question):
    return qa_chain.run(question)

gr.Interface(fn=answer, inputs="text", outputs="text").launch()
```

### Streamlit
```python
import streamlit as st

question = st.text_input("Ask a question")
if question:
    st.write(qa_chain.run(question))
```

---

## Best Practices

- **Chunk overlap** prevents context loss at boundaries
- **Metadata filtering** improves retrieval precision
- **Hybrid retrieval** balances recall and precision
- **Evaluate before deploying** — use RAGAS metrics
- **Cache frequent queries** to reduce latency
