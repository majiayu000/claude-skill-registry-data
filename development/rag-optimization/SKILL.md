---
name: rag-optimization
description: RAG 파이프라인 최적화 스킬. 검색 품질, 리랭킹, 쿼리 확장, 하이브리드 검색 관련 작업에서 자동으로 활성화됩니다. retrieval, rerank, embedding, vector search, semantic search 키워드에 반응합니다.
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# RAG Optimization Skill

RAG(Retrieval-Augmented Generation) 파이프라인을 최적화하는 전문 스킬입니다.

## 핵심 역량

### 1. 검색 최적화
- Hybrid Search 가중치 조정 (vector_weight, keyword_weight, graph_weight)
- Similarity threshold 튜닝
- GraphRAG-lite 활성화/비활성화

### 2. 리랭킹 최적화
- Cross-Encoder reranker 설정
- Rerank threshold 조정 (기본값: 0.85)
- Top-K 결과 수 조정

### 3. 쿼리 확장
- Multi-query expansion count (기본값: 5)
- Query variation 품질 개선

### 4. 캐싱
- Semantic cache 히트율 분석
- 캐시 무효화 전략

## 주요 파일

```
src/rag/
├── rag_pipeline.py      # 메인 파이프라인
├── retrieval_engine.py  # 검색 엔진 (핵심)
├── query_expander.py    # 쿼리 확장
├── semantic_cache.py    # 시맨틱 캐시
├── generation_engine.py # 생성 엔진
└── response_refiner.py  # 응답 정제
```

## 설정 파일

```python
# config/settings.py
RERANKER_THRESHOLD = 0.85
QUERY_EXPANSION_ENABLED = True

# src/rag/retrieval_engine.py
similarity_threshold = 0.85
rerank_top_k = 5
vector_weight = 0.5
keyword_weight = 0.5
graph_weight = 0.3
```

## 최적화 체크리스트

- [ ] Rerank threshold 0.8-0.9 범위 테스트
- [ ] Multi-query 3-7개 비교
- [ ] Hybrid weight 조합 A/B 테스트
- [ ] Cache hit rate 모니터링
- [ ] Latency vs Precision 트레이드오프 분석
