---
name: python-endpoint
description: >
  Python FastAPI LLM 추론 엔드포인트를 프로젝트 패턴에 맞게 생성하는 스킬.
  "/python-endpoint"를 입력하거나, "파이썬 엔드포인트 추가", "LLM 추론 API 만들어줘",
  "FastAPI 엔드포인트 추가" 같은 요청에 트리거된다.
  시스템 프롬프트 설계, RAG 컨텍스트 연동, Ollama Chat API 호출을 포함한다.
---

# Python FastAPI 엔드포인트 생성

`python-llm/app.py`에 새 LLM 추론 엔드포인트를 추가하는 스킬이다.

## 사전 확인

1. `python-llm/config.py` — 설정 구조 확인
2. `python-llm/app.py` — 기존 엔드포인트 패턴 확인
3. `python-llm/schemas.py` — 요청/응답 스키마 확인

## 엔드포인트 구조

### 동기 엔드포인트 (기본)

```python
@app.post("/infer/{domain}", response_model=InferResponse)
async def infer_{domain}(request: InferRequest) -> InferResponse:
    """
    {domain} LLM 추론
    """
    query_preview = request.query[:50] + "..." if len(request.query) > 50 else request.query
    logger.info("{Domain} infer request: query=%s", repr(query_preview))

    settings = get_settings()
    corrected_query = correct_typos(request.query)

    # (1) 컨텍스트 조회 (RAG 또는 DB)
    context = await build_{domain}_context(corrected_query)
    logger.info("{Domain} context: %d chars", len(context))

    # (2) 시스템 프롬프트 + 컨텍스트 + 사용자 질문
    messages = [{"role": "system", "content": {DOMAIN}_SYSTEM_PROMPT}]
    if context:
        messages.append({"role": "system", "content": context})
    messages.append({"role": "user", "content": corrected_query})

    # (3) Ollama Chat API 호출
    payload = {
        "model": settings.ollama_model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": request.temperature,
            "num_predict": request.max_length,
            "stop": ["<|im_start|>", "<|im_end|>", "<|endoftext|>"],
        },
    }

    async with httpx.AsyncClient(timeout=float(settings.llm_infer_timeout_sec)) as client:
        response = await client.post(
            f"{settings.ollama_base_url}/api/chat",
            json=payload,
        )
        response.raise_for_status()
        result = response.json()
        raw_text = result.get("message", {}).get("content", "")
        generated_text = clean_llm_response(raw_text)

    logger.info("{Domain} infer response: length=%d", len(generated_text))
    return InferResponse(generated_text=generated_text)
```

### SSE 스트리밍 엔드포인트 (선택)

```python
@app.post("/infer/{domain}/stream")
async def infer_{domain}_stream(request: InferRequest):
    # payload는 동기와 동일, stream=True로 변경
    # generate_sse() 제너레이터에서 토큰 단위 yield
    # 중국어/특수토큰 실시간 필터링 적용
    return StreamingResponse(generate_sse(), media_type="text/event-stream", ...)
```

## 시스템 프롬프트 설계 원칙

1. **이중 언어 지시**: 영어 + 한국어로 동일 내용 반복 (LLM 준수율 향상)
2. **한국어 전용 강제**: "You MUST respond ONLY in Korean" + "반드시 한국어로만 답변하세요"
3. **중국어/한자 금지**: CJK 문자 사용 금지 명시
4. **답변 형식 지정**: 번호 매긴 구조화된 형식
5. **참고 자료 안내**: 컨텍스트 있으면 기반 답변, 없으면 일반 지식 + 면책 안내

```python
{DOMAIN}_SYSTEM_PROMPT = (
    "You are a Korean {domain} AI assistant. "
    "You MUST respond ONLY in Korean (한국어).\n\n"
    "당신은 {역할 설명} AI 어시스턴트입니다.\n"
    "반드시 한국어로만 답변하세요.\n\n"
    "답변 규칙:\n"
    "1. ...\n"
    "2. ...\n"
)
```

## RAG 컨텍스트 서비스 추가

새 도메인에 RAG가 필요하면:

1. `python-llm/` 에 `{domain}_context_service.py` 생성
2. ChromaDB 컬렉션 추가 — `config.py`에 `chroma_{domain}_collection` 설정
3. 인덱싱 스크립트 — `index_{domain}_data.py` 생성
4. 하이브리드 검색: ChromaDB 벡터 우선 → MySQL FULLTEXT 폴백

```python
async def build_{domain}_context(query: str) -> str:
    """하이브리드 검색으로 {domain} 컨텍스트 구성"""
    settings = get_settings()
    results = []

    # 1. 벡터 검색 (우선)
    if settings.use_vector_search:
        try:
            from vector_store import get_{domain}_collection
            collection = get_{domain}_collection()
            vector_results = collection.query(
                query_texts=[query],
                n_results=settings.vector_search_top_k,
            )
            results.extend(vector_results["documents"][0])
        except Exception as exc:
            logger.warning("Vector search failed: %s", exc)

    # 2. MySQL FULLTEXT 폴백
    if not results:
        pool = await get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT content FROM {table} WHERE MATCH(content) AGAINST(%s IN BOOLEAN MODE) LIMIT %s",
                    (query, settings.vector_search_top_k),
                )
                rows = await cur.fetchall()
                results = [row[0] for row in rows]

    if not results:
        return ""

    context = "\n\n---\n\n".join(results)
    return f"[참고 자료]\n{context[:settings.medical_context_max_chars]}"
```

## Spring Boot 연동

Python 엔드포인트 추가 후 Spring 쪽에서:

1. `{Domain}Service`에 `call{Domain}LlmApi()` 메서드 추가
2. `llmWebClient.post().uri("/infer/{domain}")` 호출
3. 에러 매핑 패턴 동일 적용

## 테스트

```python
# tests/test_{domain}.py
@pytest.fixture
def mock_settings(monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "ollama")
    monkeypatch.setenv("LLM_FALLBACK_MOCK", "true")

def test_infer_{domain}_success(client, mock_settings):
    response = client.post("/infer/{domain}", json={"query": "테스트 질문"})
    assert response.status_code == 200
    assert "generated_text" in response.json()
```
