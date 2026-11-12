---
name: rag-patterns
description: "RAG 아키텍처 — 청킹 전략, 임베딩 모델, 검색 최적화, vector store 연동, advanced RAG, RAGAS 평가. Use when 문서 기반 질의응답 시스템을 만들거나 검색 품질·환각 문제를 개선할 때."
---

# RAG Patterns

RAG(Retrieval-Augmented Generation) 아키텍처, 청킹 전략, 임베딩 모델, 검색 최적화

## Quick Reference (결정 트리)

```
RAG 아키텍처 선택?
    │
    ├─ 단순 QA ────────────> Naive RAG (retrieve → generate)
    ├─ 정확도 필요 ────────> Advanced RAG (pre/post retrieval 최적화)
    └─ 복잡한 워크플로우 ──> Modular RAG (파이프라인 커스텀)

청킹 전략?
    │
    ├─ 범용 텍스트 ────────> Recursive Character (추천)
    ├─ 코드 ───────────────> Language-aware Splitter
    ├─ 의미 단위 필요 ─────> Semantic Chunking
    └─ 구조화 문서 ────────> Document-specific (Markdown, HTML)

검색 최적화?
    │
    ├─ 기본 ───────────────> Dense Retrieval (embedding similarity)
    ├─ 키워드 중요 ────────> Hybrid Search (dense + sparse)
    ├─ 정확도 극대화 ──────> Hybrid + Re-ranking
    └─ 쿼리 품질 낮음 ─────> Query Transformation (HyDE, Multi-query)
```

---

## RAG Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                     RAG Evolution                             │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Naive RAG          Advanced RAG         Modular RAG         │
│  ┌─────────┐       ┌─────────────┐     ┌───────────────┐    │
│  │ Retrieve │       │ Pre-Retrieval│     │ Custom Modules│    │
│  │    ↓     │       │  (query opt) │     │  ┌──┐┌──┐┌──┐│    │
│  │ Generate │       │      ↓       │     │  │R ││F ││G ││    │
│  └─────────┘       │  Retrieve    │     │  └──┘└──┘└──┘│    │
│                     │      ↓       │     │  Routing &    │    │
│  문제:              │ Post-Retrieval│     │  Orchestration│    │
│  - 낮은 정확도     │  (re-rank)   │     └───────────────┘    │
│  - 환각            │      ↓       │                          │
│  - 중복 문서       │  Generate    │     유연한 파이프라인     │
│                     └─────────────┘     구성 가능              │
└──────────────────────────────────────────────────────────────┘
```

### Naive RAG 기본 구현

```python
from openai import OpenAI
import numpy as np

client = OpenAI()

def naive_rag(query: str, documents: list[str], top_k: int = 3) -> str:
    """기본 RAG: embed → retrieve → generate"""
    # 1. Embed query
    query_embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding

    # 2. Embed documents & retrieve
    doc_embeddings = client.embeddings.create(
        model="text-embedding-3-small",
        input=documents
    ).data

    similarities = [
        np.dot(query_embedding, doc.embedding)
        for doc in doc_embeddings
    ]
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    context = "\n\n".join(documents[i] for i in top_indices)

    # 3. Generate
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "주어진 컨텍스트만을 기반으로 답변하세요."},
            {"role": "user", "content": f"컨텍스트:\n{context}\n\n질문: {query}"}
        ]
    )
    return response.choices[0].message.content
```

---

## Chunking Strategies

### 전략 비교

| 전략 | 장점 | 단점 | 적합한 경우 |
|------|------|------|------------|
| Fixed-size | 단순, 빠름 | 의미 단위 파괴 | 균일한 텍스트 |
| Recursive Character | 구조 보존 | 파라미터 튜닝 필요 | 범용 (추천) |
| Semantic | 의미 단위 보존 | 느림, 비용 | 의미 경계 중요 |
| Document-specific | 구조 활용 | 포맷별 구현 필요 | 코드, Markdown, HTML |

### Recursive Character Splitting

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,         # 토큰 수 기준 권장: 256-1024
    chunk_overlap=50,       # 문맥 유지를 위한 오버랩
    separators=[
        "\n\n",  # 단락 경계 (최우선)
        "\n",    # 줄바꿈
        ". ",    # 문장 경계
        " ",     # 단어 경계
        "",      # 문자 단위 (최후 수단)
    ],
    length_function=len,
)

chunks = splitter.split_text(document_text)
```

### Semantic Chunking

```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

semantic_splitter = SemanticChunker(
    embeddings=OpenAIEmbeddings(model="text-embedding-3-small"),
    breakpoint_threshold_type="percentile",  # percentile | standard_deviation | interquartile
    breakpoint_threshold_amount=95,
)

semantic_chunks = semantic_splitter.split_text(document_text)
```

### Code-aware Splitting

```python
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=512,
    chunk_overlap=50,
)

# 지원 언어: PYTHON, JAVA, GO, JS, TS, RUST, etc.
code_chunks = python_splitter.split_text(python_source_code)
```

---

## Embedding Models

### 모델 비교

| 모델 | 차원 | MTEB 점수 | 비용 | 특징 |
|------|------|----------|------|------|
| text-embedding-3-large | 3072 | 64.6 | $0.13/1M | 차원 축소 가능 |
| text-embedding-3-small | 1536 | 62.3 | $0.02/1M | 가성비 최고 |
| Cohere embed-v3 | 1024 | 64.5 | $0.10/1M | 다국어 강점 |
| voyage-3 | 1024 | 67.1 | $0.06/1M | 코드 검색 우수 |
| BGE-M3 | 1024 | 65.0 | 무료 | 셀프호스팅 |

### 차원 축소 (Matryoshka Embedding)

```python
# text-embedding-3 시리즈는 차원 축소 지원
response = client.embeddings.create(
    model="text-embedding-3-large",
    input="sample text",
    dimensions=256  # 3072 → 256 축소 (저장 비용 92% 절감)
)
```

---

## Retrieval Optimization

### Hybrid Search (Dense + Sparse)

```python
from pinecone import Pinecone
from pinecone_text.sparse import BM25Encoder

# Sparse encoder (BM25)
bm25 = BM25Encoder()
bm25.fit(corpus)

# Hybrid query
def hybrid_search(query: str, alpha: float = 0.7, top_k: int = 5):
    """alpha: dense 가중치 (1.0=dense only, 0.0=sparse only)"""
    dense_vec = get_embedding(query)
    sparse_vec = bm25.encode_queries(query)

    results = index.query(
        vector=dense_vec,
        sparse_vector=sparse_vec,
        top_k=top_k,
        alpha=alpha,  # dense/sparse 밸런스
    )
    return results
```

### Re-ranking

```python
import cohere

co = cohere.Client(api_key="...")

def retrieve_and_rerank(query: str, documents: list[str], top_k: int = 5):
    """2단계 검색: retrieve → re-rank"""
    # 1단계: 후보 문서 검색 (넉넉하게)
    candidates = vector_search(query, top_n=top_k * 4)

    # 2단계: Cross-encoder로 정밀 재정렬
    reranked = co.rerank(
        query=query,
        documents=[doc.text for doc in candidates],
        model="rerank-v3.5",
        top_n=top_k,
    )
    return [candidates[r.index] for r in reranked.results]
```

### Query Transformation

```python
def hyde_search(query: str) -> list[str]:
    """HyDE: Hypothetical Document Embeddings
    쿼리 대신 가상 답변을 생성하여 검색 정확도 향상"""
    # 1. LLM으로 가상 답변 생성
    hypothetical = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"다음 질문에 대한 상세한 답변을 작성하세요:\n{query}"
        }]
    ).choices[0].message.content

    # 2. 가상 답변의 임베딩으로 검색
    return vector_search(hypothetical, top_k=5)


def multi_query_search(query: str) -> list[str]:
    """Multi-Query: 쿼리를 여러 관점으로 변환하여 검색"""
    variants = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": (
                f"다음 질문을 3가지 다른 관점에서 재작성하세요.\n"
                f"각 줄에 하나씩 작성:\n{query}"
            )
        }]
    ).choices[0].message.content.strip().split("\n")

    # 모든 변형 쿼리로 검색 후 합집합
    all_results = set()
    for variant in variants:
        results = vector_search(variant, top_k=3)
        all_results.update(results)
    return list(all_results)
```

---

## Vector Store Integration

### pgvector

```python
from langchain_postgres.vectorstores import PGVector

connection = "postgresql+psycopg://user:pass@localhost:5432/vectordb"

vectorstore = PGVector(
    embeddings=OpenAIEmbeddings(model="text-embedding-3-small"),
    collection_name="documents",
    connection=connection,
    use_jsonb=True,
)

# 문서 추가
vectorstore.add_documents(documents)

# 유사도 검색 + 메타데이터 필터
results = vectorstore.similarity_search(
    query="RAG 아키텍처란?",
    k=5,
    filter={"source": "tech-blog"},
)
```

### Weaviate

```python
import weaviate
from weaviate.classes.query import MetadataQuery, Filter

client = weaviate.connect_to_local()

collection = client.collections.get("Document")

# Hybrid search (BM25 + vector)
results = collection.query.hybrid(
    query="RAG architecture",
    alpha=0.75,                     # vector 가중치
    limit=5,
    filters=Filter.by_property("category").equal("tech"),
    return_metadata=MetadataQuery(score=True),
)
```

### Chroma (로컬 개발용)

```python
import chromadb
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("documents", metadata={"hnsw:space": "cosine"})
collection.add(documents=["텍스트1"], metadatas=[{"source": "a"}], ids=["id1"])
results = collection.query(query_texts=["검색 쿼리"], n_results=5, where={"source": "a"})
```

---

## Advanced RAG Patterns

### Parent-Child Retrieval

```
┌─────────────────────────────────────────┐
│  Parent Document (큰 단위, 전체 문맥)     │
│  ┌──────┐ ┌──────┐ ┌──────┐            │
│  │Child1│ │Child2│ │Child3│            │
│  │(검색)│ │(검색)│ │(검색)│            │
│  └──────┘ └──────┘ └──────┘            │
│                                         │
│  검색: Child 단위 (정확도 높음)            │
│  LLM 입력: Parent 단위 (문맥 풍부)        │
└─────────────────────────────────────────┘
```

```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=InMemoryStore(),    # Parent 저장소
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)

retriever.add_documents(documents)
# 검색 시 child로 매칭 → parent 반환
results = retriever.invoke("질문")
```

### Contextual Compression

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

compressor = LLMChainExtractor.from_llm(llm)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectorstore.as_retriever(search_kwargs={"k": 10}),
)

# 검색된 문서에서 쿼리 관련 부분만 추출
compressed_docs = compression_retriever.invoke("질문")
```

### Graph RAG

```
┌──────────────────────────────────────────┐
│              Graph RAG                    │
│                                          │
│  Documents → Entity Extraction           │
│                   ↓                      │
│           Knowledge Graph                │
│          (entities + relations)           │
│                   ↓                      │
│      Community Detection (Leiden)         │
│                   ↓                      │
│      Community Summaries                 │
│                   ↓                      │
│  Query → Graph Traversal + LLM          │
│                   ↓                      │
│          Synthesized Answer              │
└──────────────────────────────────────────┘
```

```python
# Microsoft GraphRAG 사용 예시
from graphrag.index import run_pipeline
from graphrag.query import LocalSearchEngine, GlobalSearchEngine

# 인덱싱: 문서 → 엔티티/관계 추출 → 커뮤니티 탐지
await run_pipeline(config)

# 로컬 검색: 특정 엔티티 중심 답변
local_engine = LocalSearchEngine(...)
result = await local_engine.asearch("특정 기술의 장단점은?")

# 글로벌 검색: 전체 데이터셋 요약 기반 답변
global_engine = GlobalSearchEngine(...)
result = await global_engine.asearch("전체적인 트렌드는?")
```

---

## Evaluation (RAGAS)

### 핵심 메트릭

| 메트릭 | 측정 대상 | 범위 |
|--------|----------|------|
| Faithfulness | 답변이 컨텍스트 기반인지 | 0-1 |
| Answer Relevancy | 답변이 질문에 적합한지 | 0-1 |
| Context Precision | 검색된 문서의 정확도 | 0-1 |
| Context Recall | 필요한 정보가 검색되었는지 | 0-1 |

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from datasets import Dataset

eval_dataset = Dataset.from_dict({
    "question": ["RAG란 무엇인가?"],
    "answer": ["RAG는 검색 증강 생성으로..."],
    "contexts": [["RAG는 외부 지식을 활용하여..."]],
    "ground_truth": ["RAG는 Retrieval-Augmented Generation의 약자로..."],
})

result = evaluate(
    dataset=eval_dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
)

print(result)
# {'faithfulness': 0.92, 'answer_relevancy': 0.88, ...}
```

---

## Production Considerations

### 비용 최적화 체크리스트

| # | 전략 | 절감 효과 |
|---|------|----------|
| 1 | 임베딩 차원 축소 (3072 → 256) | 저장 비용 92% 절감 |
| 2 | 임베딩 캐싱 (Redis) | API 호출 50-80% 감소 |
| 3 | Batch embedding (최대 2048개/요청) | 요청 횟수 감소 |
| 4 | 작은 모델로 re-ranking 전 필터링 | 연산 비용 절감 |
| 5 | 메타데이터 필터링으로 검색 범위 축소 | 검색 속도 향상 |

### 모니터링 핵심 지표

```
- retrieval_latency_ms: 검색 단계 지연시간
- generation_latency_ms: 생성 단계 지연시간
- num_docs_retrieved: 검색된 문서 수
- prompt_tokens / completion_tokens: 토큰 사용량
- faithfulness_score: RAGAS 정기 평가 (주 1회 이상)
```

---

## Common Pitfalls

| 문제 | 원인 | 해결 |
|------|------|------|
| 환각 (Hallucination) | 컨텍스트 부족, 모델 과신 | Re-ranking 강화, faithfulness 평가 추가 |
| 관련 없는 문서 검색 | 임베딩 품질 낮음 | Hybrid search, 도메인 fine-tuned embedding |
| 청크 문맥 손실 | 작은 청크 크기 | Parent-child retrieval, 오버랩 증가 |
| 느린 응답 속도 | 대량 문서 검색 | 메타데이터 필터링, 캐싱, streaming |
| 높은 비용 | 불필요한 API 호출 | 캐싱, 차원 축소, batch 처리 |
| 중복 답변 | 유사 문서 다수 검색 | MMR(Maximal Marginal Relevance) 적용 |
