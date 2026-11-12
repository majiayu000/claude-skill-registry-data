---
name: aiops
description: "AIOps 개요 — 성숙도 모델, ML 기반 이상 탐지(Anomaly Detection), OpenTelemetry 통합, 핵심 메트릭. Use when 임계값 알림을 넘어 이상 탐지 도입을 검토하거나 AIOps 단계를 설계할 때. 복구 자동화는 aiops-remediation."
---

# AIOps 가이드

AI 기반 IT 운영: 이상 탐지, OpenTelemetry 통합

## Quick Reference (결정 트리)

```
AIOps 도입 단계?
    │
    ├─ 1단계: 데이터 수집 ────> OpenTelemetry 표준화
    │       │
    │       ├─ Metrics ───────> Prometheus
    │       ├─ Logs ──────────> Loki/Elasticsearch
    │       └─ Traces ────────> Jaeger/Tempo
    │
    ├─ 2단계: 이상 탐지 ──────> ML 기반 분석
    │       │
    │       ├─ 시계열 이상 ───> Prophet/LSTM
    │       └─ 로그 이상 ─────> Log Anomaly Detection
    │
    ├─ 3단계: 근본 원인 분석 ─> RCA Automation
    │       │
    │       ├─ Causal AI ─────> 의존성 그래프
    │       └─ LLM 분석 ──────> 컨텍스트 요약
    │
    └─ 4단계: 자동 복구 ──────> Self-Healing
            │
            ├─ Runbook ───────> 자동화된 복구
            └─ Policy ────────> 정책 기반 조치
```

---

## CRITICAL: AIOps 성숙도 모델

| Level | 단계 | 자동화 수준 | 목표 |
|-------|------|------------|------|
| **L1** | 반응적 | 수동 분석 | 알림 관리 |
| **L2** | 사전 예방적 | 이상 탐지 | MTTD 단축 |
| **L3** | 예측적 | RCA 자동화 | MTTR 단축 |
| **L4** | 자율 운영 | 자동 복구 | 무중단 운영 |

---

## OpenTelemetry 통합

### OTel Collector 설정

```yaml
apiVersion: opentelemetry.io/v1beta1
kind: OpenTelemetryCollector
metadata:
  name: otel-collector
spec:
  mode: daemonset
  config:
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318
      prometheus:
        config:
          scrape_configs:
            - job_name: 'kubernetes-pods'
              kubernetes_sd_configs:
                - role: pod

    processors:
      batch:
        timeout: 10s
        send_batch_size: 1024
      memory_limiter:
        check_interval: 1s
        limit_mib: 1000
      # AI 분석용 속성 추가
      attributes:
        actions:
          - key: ai.analysis.enabled
            value: true
            action: insert

    exporters:
      otlp:
        endpoint: "tempo:4317"
        tls:
          insecure: true
      prometheus:
        endpoint: "0.0.0.0:8889"
      loki:
        endpoint: "http://loki:3100/loki/api/v1/push"

    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [memory_limiter, batch]
          exporters: [otlp]
        metrics:
          receivers: [otlp, prometheus]
          processors: [memory_limiter, batch]
          exporters: [prometheus]
        logs:
          receivers: [otlp]
          processors: [memory_limiter, batch, attributes]
          exporters: [loki]
```

---

## 이상 탐지 (Anomaly Detection)

### Prometheus + Prophet 통합

```python
# anomaly_detector.py
from prometheus_api_client import PrometheusConnect
from prophet import Prophet
import pandas as pd

class AnomalyDetector:
    def __init__(self, prometheus_url: str):
        self.prom = PrometheusConnect(url=prometheus_url)

    def detect_metric_anomaly(
        self,
        query: str,
        lookback_hours: int = 168,  # 1주
        sensitivity: float = 0.95
    ) -> list:
        # 메트릭 조회
        data = self.prom.custom_query_range(
            query=query,
            start_time=datetime.now() - timedelta(hours=lookback_hours),
            end_time=datetime.now(),
            step="5m"
        )

        # Prophet 형식으로 변환
        df = pd.DataFrame({
            'ds': [datetime.fromtimestamp(d[0]) for d in data[0]['values']],
            'y': [float(d[1]) for d in data[0]['values']]
        })

        # 모델 학습 및 예측
        model = Prophet(interval_width=sensitivity)
        model.fit(df)
        forecast = model.predict(df)

        # 이상치 탐지
        df['yhat'] = forecast['yhat']
        df['yhat_lower'] = forecast['yhat_lower']
        df['yhat_upper'] = forecast['yhat_upper']
        df['anomaly'] = (df['y'] < df['yhat_lower']) | (df['y'] > df['yhat_upper'])

        return df[df['anomaly']].to_dict('records')
```

### Grafana ML 기반 이상 탐지

```yaml
# Grafana Alerting Rule with ML
apiVersion: 1
groups:
  - name: aiops-anomaly-detection
    folder: AIOps
    interval: 1m
    rules:
      - uid: anomaly-cpu
        title: CPU Anomaly Detection
        condition: C
        data:
          # A: 현재 값
          - refId: A
            relativeTimeRange:
              from: 600
              to: 0
            datasourceUid: prometheus
            model:
              expr: |
                avg(rate(container_cpu_usage_seconds_total{
                  namespace="production"
                }[5m])) by (pod)

          # B: 예측 기준선 (이동 평균 + 표준편차)
          - refId: B
            relativeTimeRange:
              from: 86400  # 24시간
              to: 0
            datasourceUid: prometheus
            model:
              expr: |
                avg_over_time(
                  avg(rate(container_cpu_usage_seconds_total{
                    namespace="production"
                  }[5m])) by (pod)[24h:5m]
                ) + 3 * stddev_over_time(
                  avg(rate(container_cpu_usage_seconds_total{
                    namespace="production"
                  }[5m])) by (pod)[24h:5m]
                )

          # C: 이상 여부 판단
          - refId: C
            datasourceUid: __expr__
            model:
              type: math
              expression: $A > $B
```

---

## 핵심 메트릭

### AIOps KPIs

| 메트릭 | 설명 | 목표 |
|--------|------|------|
| MTTD | 탐지까지 시간 | < 5분 |
| MTTR | 복구까지 시간 | < 30분 |
| 노이즈 감소율 | 알림 통합 효율 | > 80% |
| 자동 복구율 | 자동화된 해결 | > 40% |
| 예측 정확도 | 이상 탐지 정밀도 | > 90% |

### PromQL 쿼리

```promql
# MTTD (탐지 시간)
avg(incident_detection_time_seconds)

# MTTR (복구 시간)
avg(incident_resolution_time_seconds)

# 알림 노이즈 감소율
1 - (
  sum(increase(alerts_deduplicated_total[24h])) /
  sum(increase(alerts_raw_total[24h]))
)

# 자동 복구 성공률
sum(increase(remediation_success_total[7d])) /
sum(increase(remediation_attempts_total[7d]))
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 데이터 사일로 | 상관관계 분석 불가 | OTel 통합 |
| 과도한 알림 | 알림 피로 | 노이즈 필터링 |
| LLM 맹신 | 잘못된 RCA | 인과 모델 병행 |
| 자동화 과신 | 예상치 못한 조치 | 승인 게이트 |
| 데이터 폭증 | 비용 증가 | 샘플링/보존 정책 |

---

## 체크리스트

### AIOps Level 1 (반응적)
- [ ] OpenTelemetry 표준화
- [ ] 중앙 집중식 로깅
- [ ] 기본 알림 설정

### AIOps Level 2 (사전 예방적)
- [ ] ML 기반 이상 탐지
- [ ] 알림 중복 제거/그룹화
- [ ] 서비스 의존성 맵핑

**관련 agent**: `incident-responder`, `k8s-troubleshooter`
**관련 skill**: `/observability:aiops-remediation` (RCA, 자동 복구), `/observability:observability`, `/alerting`
