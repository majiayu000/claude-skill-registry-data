---
name: monitoring
description: 모니터링 및 관측성 스킬. Langfuse 트레이싱, Prometheus 메트릭, 로깅 관련 작업 시 자동으로 활성화됩니다. trace, metric, log, alert, dashboard 키워드에 반응합니다.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# Monitoring Skill

Langfuse, Prometheus, Grafana 기반 모니터링 전문 스킬입니다.

## 핵심 역량

### 1. Langfuse 트레이싱
- LLM 호출 추적
- 토큰 사용량 모니터링
- 비용 분석
- 품질 평가

### 2. Prometheus 메트릭
- 커스텀 메트릭 정의
- 히스토그램/카운터/게이지
- 알림 규칙 설정

### 3. 로깅
- 구조화된 로깅
- 로그 레벨 관리
- 상관관계 ID 추적

### 4. Grafana 대시보드
- 메트릭 시각화
- 알림 채널 설정

## 프로젝트 구조

```
src/monitoring/
├── langfuse.py           # Langfuse 통합
├── prometheus_exporter.py # Prometheus 익스포터
├── metrics_collector.py   # 메트릭 수집
├── tracing.py            # 분산 트레이싱
├── logging_setup.py      # 로깅 설정
└── performance_monitor.py # 성능 모니터
```

## Langfuse 트레이싱 패턴

```python
from src.monitoring.langfuse import LangfuseIntegration

langfuse = LangfuseIntegration(config)

# 트레이스 시작
trace_id = await langfuse.start_trace(
    name="rag_query",
    user_id=user_id,
    session_id=session_id,
    metadata={"query_type": "search"}
)

# 스팬 로깅
await langfuse.log_rag_pipeline(
    trace_id=trace_id,
    query=query,
    retrieved_docs=docs,
    response=response,
    processing_time=duration
)

# 트레이스 종료
await langfuse.end_trace(trace_id, output=response)
```

## Prometheus 메트릭

```python
from prometheus_client import Counter, Histogram, Gauge

# 요청 카운터
request_count = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

# 레이턴시 히스토그램
request_latency = Histogram(
    'api_request_duration_seconds',
    'Request latency',
    ['endpoint'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
)

# 활성 연결 게이지
active_connections = Gauge(
    'active_connections',
    'Number of active connections'
)
```

## 알림 규칙 예시

```yaml
groups:
  - name: api_alerts
    rules:
      - alert: HighLatency
        expr: histogram_quantile(0.99, api_request_duration_seconds) > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High API latency detected"

      - alert: HighErrorRate
        expr: rate(api_requests_total{status=~"5.."}[5m]) > 0.01
        for: 2m
        labels:
          severity: critical
```

## 주요 메트릭

| 메트릭 | 타입 | 설명 |
|--------|------|------|
| api_request_duration_seconds | Histogram | API 응답 시간 |
| llm_tokens_total | Counter | LLM 토큰 사용량 |
| rag_retrieval_count | Counter | RAG 검색 횟수 |
| cache_hit_ratio | Gauge | 캐시 히트율 |
